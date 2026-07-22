#!/usr/bin/env python3
"""Summarize patent-per-folder Patent-Mol-Wiki indexes for the HTML report."""
from __future__ import annotations

import argparse, csv, json, re
from collections import Counter
from pathlib import Path

from html_dashboard import write_dashboard

STOP = set("the and for with from into using use method methods composition compositions treatment therapy therapeutic thereof of in to a an is are by as on or at that this these new novel".split())
MODALITIES = {"antibody": ["antibody", "antibod"], "small molecule": ["compound", "inhibitor", "agonist", "antagonist"], "cell therapy": ["cell therapy", "t cell", "car-t"], "gene/rna": ["gene therapy", "rna", "nucleic acid", "oligonucleotide"], "vaccine": ["vaccine", "immunization"], "biologic": ["protein", "peptide", "enzyme"]}
DISEASES = {"oncology": ["cancer", "tumor", "tumour", "oncolog", "carcinoma", "leukemia"], "infectious disease": ["virus", "viral", "bacteria", "infection", "antiviral"], "immunology/inflammation": ["immune", "immun", "inflamm", "autoimmune"], "metabolic": ["diabetes", "obesity", "metabolic"], "neurology": ["neuro", "alzheimer", "parkinson", "brain"], "cardiovascular": ["cardio", "heart", "vascular"]}

INVENTOR_LINE = re.compile(r"^\s*(?:[-*+]\s*)?(?:inventors?|发明人)\s*[:：]\s*(.+?)\s*$", re.I | re.M)
INVENTOR_TABLE = re.compile(r"^\s*\|\s*(?:inventors?|发明人)\s*\|\s*(.+?)\s*\|?\s*$", re.I | re.M)


def extract_inventors(text: str) -> list[str]:
    """Return explicitly labeled inventor names without guessing from free text."""
    values = INVENTOR_LINE.findall(text) + INVENTOR_TABLE.findall(text)
    names: list[str] = []
    for value in values:
        for name in re.split(r"\s*[;；、]\s*|\s+and\s+", value):
            cleaned = re.sub(r"[*`_]", "", name).strip(" []|\t")
            if cleaned and cleaned.casefold() not in {"n/a", "na", "none", "unknown", "未提供", "无"}:
                names.append(cleaned)
    return list(dict.fromkeys(names))

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("root", type=Path); parser.add_argument("--outdir", required=True, type=Path); args = parser.parse_args()
    records, words, modalities, diseases, inventors = [], Counter(), Counter(), Counter(), Counter()
    for path in sorted(args.root.rglob("index.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        headings = re.findall(r"^##\s+(.+)$", text, re.M)
        title = headings[0].strip() if headings else "[no title detected]"
        patent_inventors = extract_inventors(text)
        inventors.update(patent_inventors)
        lowered = text.lower()
        tags = []
        for label, terms in MODALITIES.items():
            if any(term in lowered for term in terms):
                modalities[label] += 1
                tags.append(label)
        for label, terms in DISEASES.items():
            if any(term in lowered for term in terms):
                diseases[label] += 1
                tags.append(label)
        records.append({"patent_id": path.parent.name, "title": title, "inventors": "; ".join(patent_inventors), "index_path": str(path), "tags": tags})
        for word in re.findall(r"[A-Za-z][A-Za-z-]{3,}", title.lower()):
            if word not in STOP: words[word] += 1
    out = args.outdir.resolve(); out.mkdir(parents=True, exist_ok=True)
    with (out / "patent_titles.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["patent_id", "title", "inventors", "index_path"], extrasaction="ignore"); writer.writeheader(); writer.writerows(records)
    report = {"source_root": str(args.root.resolve()), "patent_count": len(records), "modality_keyword_counts": modalities, "disease_keyword_counts": diseases, "inventor_patent_counts": inventors, "top_title_terms": words.most_common(30), "category_note": "Categories may overlap and indicate keyword mentions, not claim-level classification."}
    (out / "weekly_overview.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_dashboard(
        out / "patent_trends.html",
        title="Patent-Mol-Wiki weekly overview",
        metrics=[
            {"label": "Patent folders analyzed", "value": len(records)},
            {"label": "Modality categories with mentions", "value": len(modalities)},
            {"label": "Disease categories with mentions", "value": len(diseases)},
            {"label": "Named inventors detected", "value": len(inventors)},
        ],
        charts=[
            {"title": "Modality keyword mentions", "items": [{"label": k, "count": v} for k, v in modalities.most_common()], "note": report["category_note"]},
            {"title": "Disease keyword mentions", "items": [{"label": k, "count": v} for k, v in diseases.most_common()], "note": report["category_note"]},
            {"title": "Top title terms", "items": [{"label": k, "count": v} for k, v in words.most_common(30)], "note": "Terms are extracted from detected index headings and exclude a small transparent stop-word list."},
        ],
        subtitle="Recent-period biomedical patent portfolio overview",
        metadata=[
            {"label": "Source", "value": "local Patent-Mol-Wiki index.md"},
            {"label": "Patent folders", "value": str(len(records))},
            {"label": "Classification", "value": "transparent title/index keyword rules"},
        ],
        insights=[
            {"title": "Portfolio coverage", "text": f"The report summarizes {len(records):,} patent folders using local index metadata and transparent keyword rules."},
            *([{ "title": f"Leading modality: {modalities.most_common(1)[0][0]}", "text": f"{modalities.most_common(1)[0][1]:,} of {len(records):,} folders contain a configured modality keyword. Categories may overlap."}] if modalities else []),
            *([{ "title": f"Leading disease area: {diseases.most_common(1)[0][0]}", "text": f"{diseases.most_common(1)[0][1]:,} of {len(records):,} folders contain a configured disease keyword. This is a retrieval signal, not claim scope."}] if diseases else []),
            *([{ "title": "Recurring title vocabulary", "text": "Most frequent detected title terms: " + ", ".join(f"{term} ({count})" for term, count in words.most_common(5)) + "."}] if words else []),
        ],
        focus_items=[
            {"title": label, "text": f"{count:,} folders contain a configured modality keyword."}
            for label, count in modalities.most_common(3)
        ] + [
            {"title": label, "text": f"{count:,} folders contain a configured disease keyword."}
            for label, count in diseases.most_common(3)
        ],
        limitations=[
            report["category_note"],
            "A keyword hit in an index, title, or abstract is not evidence that a patent claim covers that modality or disease.",
            "Read the underlying patent and claims before making freedom-to-operate, novelty, or competitive-scope conclusions.",
            *([] if inventors else ["Inventor metadata was not available in the analyzed indexes; no inventor distribution was calculated."]),
        ],
        inventor_items=[{"label": name, "count": count} for name, count in inventors.most_common()],
        inventor_note=(
            "Source: explicitly labeled inventor metadata in local Patent-Mol-Wiki index.md; counts are patents per inventor."
            if inventors
            else "Inventor metadata was not available in the analyzed local Patent-Mol-Wiki index.md files."
        ),
        source_note="Source: extracted local Patent-Mol-Wiki index.md. This offline file embeds only derived metadata, keyword counts, and available inventor counts.",
    )
    print(json.dumps({"patent_count": len(records), "outdir": str(out)}, ensure_ascii=False))

if __name__ == "__main__": main()

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

APPLICANT_LABEL = r"(?:applicants?|assignees?|patentees?|申请人|申请者|专利权人)"
APPLICANT_LINE = re.compile(
    rf"^\s*(?:[-*+]\s*)?[*`_]*{APPLICANT_LABEL}[*`_]*\s*[:：]\s*(.+?)\s*$",
    re.I | re.M,
)
APPLICANT_TABLE = re.compile(
    rf"^\s*\|\s*[*`_]*{APPLICANT_LABEL}[*`_]*\s*\|\s*(.+?)\s*\|?\s*$",
    re.I | re.M,
)
LEGAL_SUFFIXES = {
    "AG", "CO", "CO.", "CORP", "CORP.", "CORPORATION", "GMBH", "INC", "INC.",
    "INCORPORATED", "LLC", "LLP", "LTD", "LTD.", "LIMITED", "NV", "PLC",
    "PTE. LTD.", "S.A.", "S.A.S.", "SAS", "SASU", "SE",
}


def split_applicants(value: str) -> list[str]:
    """Split comma-delimited metadata while retaining common name suffixes."""
    chunks = [chunk.strip() for chunk in re.split(r"\s*[;；、]\s*|\s+and\s+|,", value) if chunk.strip()]
    names: list[str] = []
    for chunk in chunks:
        normalized = chunk.rstrip(".").upper()
        is_suffix = normalized in {suffix.rstrip(".") for suffix in LEGAL_SUFFIXES}
        previous_is_surname = bool(
            names
            and re.fullmatch(r"[A-ZÀ-ÖØ-Þ'’-]{2,}", names[-1])
            and re.match(r"[A-ZÀ-ÖØ-Þ][a-zà-öø-ÿ'’-]+", chunk)
        )
        if names and (is_suffix or previous_is_surname):
            names[-1] = f"{names[-1]}, {chunk}"
        else:
            names.append(chunk)
    return names


def extract_applicants(text: str) -> list[str]:
    """Return explicitly labeled applicant/assignee names without guessing."""
    values = APPLICANT_LINE.findall(text) + APPLICANT_TABLE.findall(text)
    names: list[str] = []
    for value in values:
        for name in split_applicants(value):
            cleaned = re.sub(r"[*`_]", "", name).strip(" []|\t")
            if cleaned and cleaned.casefold() not in {"n/a", "na", "none", "unknown", "未提供", "无"}:
                names.append(cleaned)
    return list(dict.fromkeys(names))

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("root", type=Path); parser.add_argument("--outdir", required=True, type=Path); args = parser.parse_args()
    records, words, modalities, diseases, applicants = [], Counter(), Counter(), Counter(), Counter()
    for path in sorted(args.root.rglob("index.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        headings = re.findall(r"^##\s+(.+)$", text, re.M)
        title = headings[0].strip() if headings else "[no title detected]"
        patent_applicants = extract_applicants(text)
        applicants.update(patent_applicants)
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
        records.append({"patent_id": path.parent.name, "title": title, "applicants": "; ".join(patent_applicants), "index_path": str(path), "tags": tags})
        for word in re.findall(r"[A-Za-z][A-Za-z-]{3,}", title.lower()):
            if word not in STOP: words[word] += 1
    out = args.outdir.resolve(); out.mkdir(parents=True, exist_ok=True)
    with (out / "patent_titles.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["patent_id", "title", "applicants", "index_path"], extrasaction="ignore"); writer.writeheader(); writer.writerows(records)
    report = {"source_root": str(args.root.resolve()), "patent_count": len(records), "modality_keyword_counts": modalities, "disease_keyword_counts": diseases, "applicant_patent_counts": applicants, "top_title_terms": words.most_common(30), "category_note": "Categories may overlap and indicate keyword mentions, not claim-level classification.", "applicant_note": "Applicant counts use raw, explicitly labeled metadata. Corporate and multilingual aliases are not entity-resolved."}
    (out / "weekly_overview.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    ranked_modalities = sorted(
        ((label, modalities[label]) for label in MODALITIES),
        key=lambda item: (-item[1], item[0]),
    )
    ranked_diseases = sorted(
        ((label, diseases[label]) for label in DISEASES),
        key=lambda item: (-item[1], item[0]),
    )
    leading_applicant = applicants.most_common(1)
    write_dashboard(
        out / "patent_trends.html",
        title="Patent-Mol-Wiki weekly overview",
        metrics=[
            {"label": "Patent folders analyzed", "value": len(records)},
            {"label": "Modality categories with mentions", "value": len(modalities)},
            {"label": "Disease categories with mentions", "value": len(diseases)},
            {"label": "Named applicants detected", "value": len(applicants)},
            {"label": "Leading modality", "value": f"{ranked_modalities[0][0]} ({ranked_modalities[0][1]})"},
            {"label": "Leading applicant", "value": f"{leading_applicant[0][0]} ({leading_applicant[0][1]})" if leading_applicant else "Unavailable"},
        ],
        charts=[
            {"title": "Modality keyword mentions", "items": [{"label": k, "count": v} for k, v in ranked_modalities], "note": report["category_note"]},
            {"title": "Disease keyword mentions", "items": [{"label": k, "count": v} for k, v in ranked_diseases], "note": report["category_note"]},
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
            {"title": f"Leading modality: {ranked_modalities[0][0]}", "text": f"{ranked_modalities[0][1]:,} of {len(records):,} folders contain a configured modality keyword. Categories may overlap."},
            {"title": f"Leading disease area: {ranked_diseases[0][0]}", "text": f"{ranked_diseases[0][1]:,} of {len(records):,} folders contain a configured disease keyword. This is a retrieval signal, not claim scope."},
            {"title": "Recurring title vocabulary", "text": "Most frequent detected title terms: " + (", ".join(f"{term} ({count})" for term, count in words.most_common(5)) if words else "none detected") + "."},
            {"title": "Applicant coverage", "text": f"The leading raw applicant label is {leading_applicant[0][0]} ({leading_applicant[0][1]:,} patents)." if leading_applicant else "No explicitly labeled applicant metadata was detected."},
        ],
        focus_items=[
            {"title": label, "text": f"{count:,} folders contain a configured modality keyword."}
            for label, count in ranked_modalities[:3]
        ] + [
            {"title": label, "text": f"{count:,} folders contain a configured disease keyword."}
            for label, count in ranked_diseases[:3]
        ],
        limitations=[
            report["category_note"],
            report["applicant_note"],
            "A keyword hit in an index, title, or abstract is not evidence that a patent claim covers that modality or disease.",
            "Read the underlying patent and claims before making freedom-to-operate, novelty, or competitive-scope conclusions.",
            *([] if applicants else ["Applicant metadata was not available in the analyzed indexes; no applicant distribution was calculated."]),
        ],
        applicant_items=[{"label": name, "count": count} for name, count in applicants.most_common()],
        applicant_note=(
            f"Source: local Patent-Mol-Wiki index.md. {report['applicant_note']}"
            if applicants
            else "Applicant metadata was not available in the analyzed local Patent-Mol-Wiki index.md files."
        ),
        source_note="Source: extracted local Patent-Mol-Wiki index.md. This offline file embeds only derived metadata, keyword counts, and available applicant counts.",
    )
    print(json.dumps({"patent_count": len(records), "outdir": str(out)}, ensure_ascii=False))

if __name__ == "__main__": main()

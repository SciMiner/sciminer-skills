#!/usr/bin/env python3
"""Summarize patent-per-folder Patent-Mol-Wiki indexes and generate reproducible SVG bars."""
from __future__ import annotations

import argparse, csv, html, json, re
from collections import Counter
from pathlib import Path

STOP = set("the and for with from into using use method methods composition compositions treatment therapy therapeutic thereof of in to a an is are by as on or at that this these new novel".split())
MODALITIES = {"antibody": ["antibody", "antibod"], "small molecule": ["compound", "inhibitor", "agonist", "antagonist"], "cell therapy": ["cell therapy", "t cell", "car-t"], "gene/rna": ["gene therapy", "rna", "nucleic acid", "oligonucleotide"], "vaccine": ["vaccine", "immunization"], "biologic": ["protein", "peptide", "enzyme"]}
DISEASES = {"oncology": ["cancer", "tumor", "tumour", "oncolog", "carcinoma", "leukemia"], "infectious disease": ["virus", "viral", "bacteria", "infection", "antiviral"], "immunology/inflammation": ["immune", "immun", "inflamm", "autoimmune"], "metabolic": ["diabetes", "obesity", "metabolic"], "neurology": ["neuro", "alzheimer", "parkinson", "brain"], "cardiovascular": ["cardio", "heart", "vascular"]}

def bar(title: str, data: Counter[str], out: Path) -> None:
    items = data.most_common(12); width, left, row = 1000, 280, 38; height = 100 + row * max(1, len(items)); maximum = max(data.values(), default=1)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><style>text{{font:14px Arial,"Microsoft YaHei";fill:#172033}}.t{{font-size:22px;font-weight:bold}}</style>', f'<text class="t" x="24" y="32">{html.escape(title)}</text>']
    for i, (label, value) in enumerate(items):
        y = 58 + i * row; w = int((width-left-70)*value/maximum)
        parts += [f'<text x="{left-12}" y="{y+18}" text-anchor="end">{html.escape(label)}</text>', f'<rect x="{left}" y="{y}" width="{w}" height="23" rx="3" fill="#2563eb"/>', f'<text x="{left+w+7}" y="{y+18}">{value}</text>']
    parts += [f'<text x="24" y="{height-16}" fill="#64748b">Source: extracted Patent-Mol-Wiki index.md; categories are transparent title/abstract keyword rules.</text>', '</svg>']
    out.write_text("\n".join(parts), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("root", type=Path); parser.add_argument("--outdir", required=True, type=Path); args = parser.parse_args()
    records, words, modalities, diseases = [], Counter(), Counter(), Counter()
    for path in sorted(args.root.rglob("index.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        headings = re.findall(r"^##\s+(.+)$", text, re.M)
        title = headings[0].strip() if headings else "[no title detected]"
        records.append({"patent_id": path.parent.name, "title": title, "index_path": str(path)})
        lowered = text.lower()
        for label, terms in MODALITIES.items():
            if any(term in lowered for term in terms): modalities[label] += 1
        for label, terms in DISEASES.items():
            if any(term in lowered for term in terms): diseases[label] += 1
        for word in re.findall(r"[A-Za-z][A-Za-z-]{3,}", title.lower()):
            if word not in STOP: words[word] += 1
    out = args.outdir.resolve(); out.mkdir(parents=True, exist_ok=True)
    with (out / "patent_titles.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["patent_id", "title", "index_path"]); writer.writeheader(); writer.writerows(records)
    report = {"source_root": str(args.root.resolve()), "patent_count": len(records), "modality_keyword_counts": modalities, "disease_keyword_counts": diseases, "top_title_terms": words.most_common(30), "category_note": "Categories may overlap and indicate keyword mentions, not claim-level classification."}
    (out / "weekly_overview.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    bar("Recent-week modality keyword mentions", modalities, out / "modality_mentions.svg"); bar("Recent-week disease keyword mentions", diseases, out / "disease_mentions.svg")
    print(json.dumps({"patent_count": len(records), "outdir": str(out)}, ensure_ascii=False))

if __name__ == "__main__": main()

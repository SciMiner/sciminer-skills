#!/usr/bin/env python3
"""Extract common numeric label/count pairs from Patent-Mol-Wiki index.md files."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from html_dashboard import write_dashboard
from summarize_wiki import extract_inventors

PAIR_PATTERNS = [
    re.compile(r"^\s*[-*+]?\s*([^:：|]{1,100}?)\s*[:：]\s*([0-9][0-9,]*)\s*$"),
    re.compile(r"^\s*[-*+]?\s*([^()（）|]{1,100}?)\s*[（(]\s*([0-9][0-9,]*)\s*[)）]\s*$"),
]


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[*`_#]", "", value)).strip(" -:：|")


def pairs_from_index(path: Path) -> list[tuple[str, int]]:
    pairs: list[tuple[str, int]] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        if "|" in line:
            cells = [clean(cell) for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and re.fullmatch(r"[0-9][0-9,]*", cells[-1] or ""):
                label = " / ".join(cell for cell in cells[:-1] if cell and not re.fullmatch(r"[-: ]+", cell))
                if label:
                    pairs.append((label, int(cells[-1].replace(",", ""))))
            continue
        for pattern in PAIR_PATTERNS:
            found = pattern.match(line)
            if found:
                pairs.append((clean(found.group(1)), int(found.group(2).replace(",", ""))))
                break
    return [(label, count) for label, count in pairs if label and count >= 0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()
    indices = sorted(args.root.rglob("index.md"))
    if not indices:
        raise SystemExit(f"No index.md files found under {args.root}")
    aggregate: Counter[str] = Counter()
    inventors: Counter[str] = Counter()
    per_index = []
    for index in indices:
        pairs = pairs_from_index(index)
        inventors.update(extract_inventors(index.read_text(encoding="utf-8", errors="replace")))
        per_index.append({"index": str(index), "pairs": [{"label": label, "count": count} for label, count in pairs]})
        aggregate.update(dict(pairs))
    outdir = args.outdir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    ranking = sorted(aggregate.items(), key=lambda item: (-item[1], item[0].casefold()))
    report = {"source_root": str(args.root.resolve()), "index_files": [str(path) for path in indices], "index_count": len(indices), "aggregate_label_counts": [{"label": label, "count": count} for label, count in ranking], "inventor_patent_counts": inventors, "per_index": per_index, "notes": ["Counts are parser-detected Markdown label/count pairs. Inspect index.md structure before interpreting mixed metrics as one distribution.", "Repeated labels are summed across index files."]}
    (outdir / "weekly_summary.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_dashboard(
        outdir / "patent_trends.html",
        title="Patent-Mol-Wiki index trends",
        metrics=[
            {"label": "Index files", "value": len(indices)},
            {"label": "Detected labels", "value": len(ranking)},
            {"label": "Aggregate detected counts", "value": f"{sum(aggregate.values()):,}"},
            {"label": "Named inventors detected", "value": len(inventors)},
        ],
        charts=[{
            "title": "Top detected index counts",
            "items": [{"label": label, "count": count} for label, count in ranking],
            "note": "Counts are parser-detected Markdown label/count pairs; do not combine unlike metrics as a distribution.",
        }],
        subtitle="Aggregate view of numeric label/count pairs found in local indexes",
        metadata=[
            {"label": "Source", "value": "local Patent-Mol-Wiki index.md"},
            {"label": "Index files", "value": str(len(indices))},
            {"label": "Detection method", "value": "Markdown label/count parser"},
        ],
        insights=[
            {"title": "Collection coverage", "text": f"The parser inspected {len(indices):,} index files and found {len(ranking):,} distinct numeric labels."},
            *([{ "title": f"Largest detected value: {ranking[0][0]}", "text": f"The leading parser-detected label has a value of {ranking[0][1]:,}. Interpret it only in the context of its source index."}] if ranking else []),
            {"title": "Mixed-metric safeguard", "text": "Inspect each detected value in its originating index so unlike metrics are not silently treated as one distribution."},
        ],
        focus_items=[
            {"title": label, "text": f"Detected aggregate value: {count:,}"}
            for label, count in ranking[:6]
        ],
        limitations=report["notes"] + ["Inspect the originating Markdown before using any value as a portfolio total or a period-over-period comparison."],
        inventor_items=[{"label": name, "count": count} for name, count in inventors.most_common()],
        inventor_note=(
            "Source: explicitly labeled inventor metadata in local Patent-Mol-Wiki index.md; counts are patents per inventor."
            if inventors
            else "Inventor metadata was not available in the analyzed local Patent-Mol-Wiki index.md files."
        ),
        source_note="Source: local Patent-Mol-Wiki index.md. This offline file embeds only the derived aggregate data.",
    )
    print(json.dumps({"index_count": len(indices), "labels": len(ranking), "outdir": str(outdir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

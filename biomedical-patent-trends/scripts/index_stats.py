#!/usr/bin/env python3
"""Extract common numeric label/count pairs from Patent-Mol-Wiki index.md files and draw SVG bars."""
from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter
from pathlib import Path

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


def svg_bars(title: str, counts: list[tuple[str, int]], out: Path) -> None:
    counts = counts[:15]
    width, left, right, row = 1200, 330, 90, 42
    height = 110 + row * max(1, len(counts))
    maximum = max((value for _, value in counts), default=1) or 1
    rows = []
    for i, (label, value) in enumerate(counts):
        y = 70 + i * row
        bar = int((width - left - right) * value / maximum)
        rows.append(f'<text x="{left - 14}" y="{y + 20}" text-anchor="end">{html.escape(label[:55])}</text>')
        rows.append(f'<rect x="{left}" y="{y}" width="{bar}" height="25" rx="3" fill="#2563eb"/>')
        rows.append(f'<text x="{left + bar + 8}" y="{y + 19}">{value}</text>')
    document = "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:Arial,"Microsoft YaHei",sans-serif;font-size:15px;fill:#172033}.title{font-size:24px;font-weight:bold}</style>',
        f'<text class="title" x="30" y="35">{html.escape(title)}</text>',
        *rows,
        f'<text x="30" y="{height - 20}" fill="#64748b">Source: local Patent-Mol-Wiki index.md; values are label/count pairs detected from Markdown.</text>',
        '</svg>',
    ])
    out.write_text(document, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()
    indices = sorted(args.root.rglob("index.md"))
    if not indices:
        raise SystemExit(f"No index.md files found under {args.root}")
    aggregate: Counter[str] = Counter()
    per_index = []
    for index in indices:
        pairs = pairs_from_index(index)
        per_index.append({"index": str(index), "pairs": [{"label": label, "count": count} for label, count in pairs]})
        aggregate.update(dict(pairs))
    outdir = args.outdir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    ranking = sorted(aggregate.items(), key=lambda item: (-item[1], item[0].casefold()))
    report = {"source_root": str(args.root.resolve()), "index_files": [str(path) for path in indices], "index_count": len(indices), "aggregate_label_counts": [{"label": label, "count": count} for label, count in ranking], "per_index": per_index, "notes": ["Counts are parser-detected Markdown label/count pairs. Inspect index.md structure before interpreting mixed metrics as one distribution.", "Repeated labels are summed across index files."]}
    (outdir / "weekly_summary.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    svg_bars("Top detected index counts", ranking, outdir / "top_index_counts.svg")
    print(json.dumps({"index_count": len(indices), "labels": len(ranking), "outdir": str(outdir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

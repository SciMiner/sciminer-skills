#!/usr/bin/env python3
"""Stream keyword searches through a patent wiki and emit file-level evidence snippets."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TEXT_SUFFIXES = {".md", ".txt", ".json", ".csv", ".tsv", ".xml", ".html", ".htm"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--query", action="append", required=True, help="Repeat for aliases.")
    parser.add_argument("--regex", action="store_true", help="Interpret queries as regular expressions.")
    parser.add_argument("--context", type=int, default=180)
    parser.add_argument("--max-hits-per-file", type=int, default=8)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    patterns = [(query, re.compile(query if args.regex else re.escape(query), re.IGNORECASE)) for query in args.query]
    root = args.root.resolve()
    matches = []
    searched_files = 0
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        searched_files += 1
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        hit_count = 0
        for query, pattern in patterns:
            for match in pattern.finditer(text):
                start = max(0, match.start() - args.context)
                end = min(len(text), match.end() + args.context)
                matches.append({"file": str(path.relative_to(root)), "query": query, "offset": match.start(), "snippet": text[start:end].replace("\n", " ")})
                hit_count += 1
                if hit_count >= args.max_hits_per_file:
                    break
            if hit_count >= args.max_hits_per_file:
                break
    report = {"root": str(root), "queries": args.query, "regex": args.regex, "searched_text_files": searched_files, "matched_files": len({m['file'] for m in matches}), "matches": matches}
    payload = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()

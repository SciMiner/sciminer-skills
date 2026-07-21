#!/usr/bin/env python3
"""Inventory structures in a selected patent folder with RDKit; retain source provenance."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def smiles_rows(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in {".smi", ".smiles"}:
            for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
                value = line.strip().split()[0] if line.strip() else ""
                if value:
                    yield path, line_number, value, "SMILES file"
        elif suffix in {".csv", ".tsv"}:
            delimiter = "\t" if suffix == ".tsv" else ","
            with path.open(encoding="utf-8", errors="replace", newline="") as handle:
                reader = csv.DictReader(handle, delimiter=delimiter)
                for line_number, row in enumerate(reader, start=2):
                    key = next((k for k in row if k and k.strip().lower() in {"smiles", "canonical_smiles", "isomeric_smiles"}), None)
                    if key and row.get(key, "").strip():
                        yield path, line_number, row[key].strip(), f"{suffix} column {key}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Candidate patent folder, not the entire corpus.")
    parser.add_argument("--outdir", required=True, type=Path)
    parser.add_argument("--max-records", type=int, default=10000)
    args = parser.parse_args()
    try:
        from rdkit import Chem, rdBase
        from rdkit.Chem import Descriptors, Lipinski
        from rdkit.Chem.Scaffolds import MurckoScaffold
    except ImportError as exc:
        raise SystemExit("RDKit is required. Install it in the analysis environment, then rerun.") from exc

    root = args.root.resolve()
    records, invalid, scaffolds = [], [], Counter()
    for source, line, smiles, source_kind in smiles_rows(root):
        if len(records) + len(invalid) >= args.max_records:
            break
        molecule = Chem.MolFromSmiles(smiles)
        provenance = {"source_file": str(source.relative_to(root)), "record": line, "source_kind": source_kind, "input_smiles": smiles}
        if molecule is None:
            invalid.append(provenance)
            continue
        canonical = Chem.MolToSmiles(molecule, isomericSmiles=True)
        scaffold = Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(molecule), isomericSmiles=True)
        scaffolds[scaffold or "[acyclic]"] += 1
        records.append({**provenance, "canonical_smiles": canonical, "murcko_scaffold": scaffold or "[acyclic]", "molecular_weight": round(Descriptors.MolWt(molecule), 3), "cLogP": round(Descriptors.MolLogP(molecule), 3), "hbd": Lipinski.NumHDonors(molecule), "hba": Lipinski.NumHAcceptors(molecule)})
    outdir = args.outdir.resolve(); outdir.mkdir(parents=True, exist_ok=True)
    fields = ["source_file", "record", "source_kind", "input_smiles", "canonical_smiles", "murcko_scaffold", "molecular_weight", "cLogP", "hbd", "hba"]
    with (outdir / "molecules.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(records)
    with (outdir / "scaffolds.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle); writer.writerow(["murcko_scaffold", "record_count"]); writer.writerows(scaffolds.most_common())
    summary = {"input_root": str(root), "rdkit_version": rdBase.rdkitVersion, "parsed_records": len(records), "unique_canonical_smiles": len({record['canonical_smiles'] for record in records}), "invalid_records": invalid, "scaffold_count": len(scaffolds), "max_records": args.max_records}
    (outdir / "structure_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("parsed_records", "unique_canonical_smiles", "scaffold_count")}, ensure_ascii=False))


if __name__ == "__main__":
    main()

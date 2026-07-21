# Structure-analysis rules

Work only inside candidate patent folders selected by keyword/metadata retrieval. Record exact files, selected records, and the definition of a unique molecule.

- Prefer machine-readable SDF or a known SMILES column. Validate every parsed molecule; keep invalid inputs and parse errors in the output.
- Canonicalize with a declared toolkit/version. Do not deduplicate by patent title or molecule display name.
- For property distributions, report molecule count, unique canonical SMILES count, missing/invalid count, and whether salts/stereoisomers were normalized or retained.
- Use scaffold counts for structural diversity only after inspecting enough input to verify that structures are comparable. A high-frequency scaffold does not establish novelty or claim coverage.
- For claimed-structure or Markush conclusions, inspect the claim text and figures. A representative example compound is not the entire claimed scope.

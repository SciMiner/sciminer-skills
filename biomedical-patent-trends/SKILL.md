---
name: biomedical-patent-trends
description: Download, search, and analyze Patent-Mol-Wiki biomedical-patent packages. Use when users ask what happened in a recent patent period, need portfolio or trend statistics from wiki index.md files, ask whether a target, disease, modality, organization, or patent is present, need charts of patent distributions, or need molecular-structure analysis from selected patent folders.
required_environment_variables:
  - SCIMINER_API_KEY
---

# Biomedical Patent Trends

Analyze the supplied Patent-Mol-Wiki corpus as a local, potentially very large knowledge base. State the covered download period and data limitations; do not claim that a patent is absent when the corpus, search scope, or alias set is incomplete.

## Prepare or update the corpus

1. Read [Patent-Mol-Wiki API reference](references/patent-mol-wiki-api.md) before invoking the service. Use the runtime `SCIMINER_API_KEY`, injected by the SciMiner gateway, as `X-Auth-Token`; never print, persist, or place it in prompts, logs, or repository files.
2. For a period request, use `scripts/download_wiki.py --date-range recent_week --outdir <project>/data`. Use `--patent-ids` only when the user supplied patent numbers; it overrides the date range. Preserve the script's task manifest and raw service response beside the downloaded archive.
3. Locate the extracted wiki roots and their `index.md` files with `rg --files <data-root> -g index.md`. Treat each index as the authoritative aggregate view for its own wiki folder.
4. Create an analysis workspace outside the corpus (for example, `<project>/analysis/<period>/`) so downloads remain immutable and derived artifacts are separable.

## Route the question

| Request | First action | Deliverable |
|---|---|---|
| “What happened in the recent week?” or other open-ended period review | Read every `index.md`, then run `scripts/index_stats.py` across them. Inspect a small, transparent sample of patents only to explain the leading changes. | `weekly_summary.json`, chart SVGs, concise trend brief |
| Target, disease, modality, company, or patent lookup | Build aliases first, then use `scripts/search_wiki.py` against the extracted corpus. Read only the returned files and surrounding passages. | matched patent table, evidence snippets, coverage/alias caveat |
| Distribution/comparison question | Derive counts from the relevant `index.md` or matched-result table; generate a chart suited to the number of categories. | CSV/JSON plus SVG or another reproducible chart |
| Molecular-structure question | Search metadata/text first to identify candidate patent folders, then read [structure-analysis.md](references/structure-analysis.md) and run the structure script only there. | structure table, method/version, results, limitations |

Never begin a targeted question by opening every patent text file. Search filenames and extracted text first, use specific aliases, and report the exact search root, query set, files searched, and match count.

## Default report: “What happened in the recent week?”

1. Download `recent_week` unless a fresh extracted weekly package already exists and its manifest proves the coverage. Do not silently substitute calendar week dates for the provider's range.
2. Inventory wiki roots and index files. Run:

   ```powershell
   python scripts/index_stats.py <data-root> --outdir <analysis-root>
   ```

3. Use the generated aggregate counts and charts to describe patent volume, targets, diseases, organizations, modalities/technical fields, patent types, and leading ranked categories when those fields are present. Compare with the immediately preceding period only if its package exists and has compatible index fields.
4. To explain a leading category, search it with `scripts/search_wiki.py` and read the matched entries. Do not infer a trend simply because a keyword appears many times in boilerplate.
5. Deliver: coverage and collection time; headline numbers; notable concentrations/new entities; a compact chart set; 3–5 evidence-backed observations; and exclusions/uncertainties. Link every conclusion to an index metric or listed patent identifiers.

Use a horizontal bar chart for ranked categories, a stacked/grouped bar chart for compatible period comparisons, and a line chart only for three or more comparable time periods. Include labels, the total denominator, a readable title, and an explicit “source: local Patent-Mol-Wiki index.md” caption. Do not use a word cloud as the sole quantitative evidence.

## Targeted retrieval

Normalize terminology before search. Include official symbol/name, common aliases, spelling variants, protein family member, disease synonym/ontology label, and relevant modality names. Keep the alias list in the output.

```powershell
python scripts/search_wiki.py <data-root> --query 'GLP-1R' --query 'GLP1R' --query 'glucagon-like peptide-1 receptor' --out <analysis-root>/glp1r_matches.json
```

Use exact/literal search by default. Add `--regex` only for deliberate patterns. Deduplicate at patent-file level, inspect context, and distinguish: direct claim/embodiment, background mention, comparator, and ambiguous hit. For a negative answer, say “no matches under these aliases in this downloaded corpus” and give coverage—not “no patent exists.”

## Structure analysis

After candidate patents are identified, use `scripts/analyze_structures.py <candidate-folder> --outdir <analysis-root>/structures`. It supports SDF, SMILES, and delimited files with SMILES columns, and uses RDKit for canonicalization, descriptors, and Bemis–Murcko scaffold counts. Preserve source file and record number. Treat OCR-derived or image-only structures as unverified until inspected or processed with an appropriate structure-recognition workflow.

## Reproducibility and safety

- Write source package path/hash, provider task ID, request parameters, retrieval timestamp, script command, and tool versions to the analysis manifest.
- Never publish credentials, unredacted private patent text, or an API response containing a credential.
- Do not present application counts as unique inventions without family-level identifiers and a documented deduplication rule.
- Treat title/abstract/description matches as retrieval evidence, not proof that a claim covers the target, disease, or structure. Read claims for scope conclusions.

## SciMiner credential prerequisite

1. `SCIMINER_API_KEY` is pre-obtained by the SciMiner gateway before the agent run reaches this skill.
2. Use the runtime `SCIMINER_API_KEY` directly as the `X-Auth-Token` header for every SciMiner call.
3. Never request, derive, print, persist, or write the key in prompts, logs, output artifacts, or repository files.

If `SCIMINER_API_KEY` is unavailable at runtime, stop and report that the gateway did not inject the required credential. Do not try to derive it inside the skill or switch to another credential source, tool, or service.

## Patent-per-folder package layout

Some provider downloads contain one `index.md` per patent (`profile: patmap-wiki-data-v1`) rather than a dashboard index with precomputed categories. In that layout, count the patent folders and run `scripts/summarize_wiki.py <wiki-root> --outdir <analysis-root>` for a reproducible overview. It produces patent titles, transparent overlapping modality/disease keyword counts, and SVG charts. Do not represent these keyword counts as claim-level classifications or target annotations. Use `scripts/search_wiki.py` followed by claim inspection for a specific target, disease, company, or structure question.

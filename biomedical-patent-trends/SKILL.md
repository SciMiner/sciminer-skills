---
name: biomedical-patent-trends
description: Download, search, and analyze Patent-Mol-Wiki biomedical-patent packages, producing a presentation-focused HTML trends report. Use when users ask what happened in a recent patent period, need portfolio or trend statistics from wiki index.md files, ask whether a target, disease, modality, organization, or patent is present, need patent-distribution analysis, or need molecular-structure analysis from selected patent folders.
required_environment_variables:
  - SCIMINER_API_KEY
---

# Biomedical Patent Trends

Analyze the supplied Patent-Mol-Wiki corpus as a local, potentially very large knowledge base. State the covered download period and data limitations; do not claim that a patent is absent when the corpus, search scope, or alias set is incomplete.

## Prepare or update the corpus

1. Immediately before every service invocation, fetch and read the latest `Patent-Mol-Wiki_api_doc.md` from `https://sciminer.tech/tool_api_files/`. Treat that live document as authoritative for the provider name, tool name, parameters, request encoding, polling, and result handling. Use the runtime `SCIMINER_API_KEY`, injected by the SciMiner gateway, as `X-Auth-Token`; never print, persist, or place it in prompts, logs, or repository files. Do not use a cached or repository-bundled copy of the API documentation.
2. After obtaining the corpus according to that live document, locate the extracted wiki roots and their `index.md` files with `rg --files <data-root> -g index.md`. Treat each index as the authoritative aggregate view for its own wiki folder.
3. Create an analysis workspace outside the corpus (for example, `<project>/analysis/<period>/`) so downloads remain immutable and derived artifacts are separable.

## Route the question

| Request | First action | Deliverable |
|---|---|---|
| “What happened in the recent week?” or other open-ended period review | Read every `index.md`, then run `scripts/index_stats.py` across them. Inspect a small, transparent sample of patents only to explain the leading changes. | `weekly_summary.json`, `patent_trends.html`, concise trend brief |
| Target, disease, modality, company, or patent lookup | Build aliases first, then use `scripts/search_wiki.py` against the extracted corpus. Read only the returned files and surrounding passages. | matched patent table, evidence snippets, coverage/alias caveat |
| Distribution/comparison question | Derive counts from the relevant `index.md` or matched-result table. | CSV/JSON plus `patent_trends.html` |
| Molecular-structure question | Search metadata/text first to identify candidate patent folders, then read [structure-analysis.md](references/structure-analysis.md) and run the structure script only there. | structure table, method/version, results, limitations |

Never begin a targeted question by opening every patent text file. Search filenames and extracted text first, use specific aliases, and report the exact search root, query set, files searched, and match count.

## Default report: “What happened in the recent week?”

1. Confirm the corpus coverage from its manifest. Do not silently substitute calendar-week dates for the provider-defined coverage.
2. Inventory wiki roots and index files. Run:

   ```powershell
   python scripts/index_stats.py <data-root> --outdir <analysis-root>
   ```

3. Use the generated aggregate counts to describe patent volume, targets, diseases, applicants/assignees, inventors, modalities/technical fields, patent types, and leading ranked categories when those fields are present. Keep applicants and inventors separate. Compare with the immediately preceding period only if its package exists and has compatible index fields.
4. To explain a leading category, search it with `scripts/search_wiki.py` and read the matched entries. Do not infer a trend simply because a keyword appears many times in boilerplate.
5. Deliver: coverage and collection time; headline numbers; notable concentrations/new entities; `patent_trends.html`; 3–5 evidence-backed observations; and exclusions/uncertainties. Link every conclusion to an index metric or listed patent identifiers. The HTML must embed only derived results and identify its source and caveats.

## HTML visualization standard

Create a standalone `patent_trends.html` whose information hierarchy and styling fit the query and the available evidence. Use `scripts/html_dashboard.py` when its report-oriented shell is useful, but customize its composition and CSS or hand-author a different accessible, responsive visualization when that communicates the results better. Do not treat any bundled HTML as a fixed layout or visual reference.

Use the same language as the user's query throughout the generated HTML, including the document title, `lang` attribute, section headings, chart labels and tooltips, captions, observations, limitations, empty states, and provenance. Preserve patent identifiers, organization names, gene/target symbols, and technical terms when translation would reduce precision. For mixed-language queries, follow the language used for the request itself unless the user asks for another language. Pass localized copy and the matching BCP 47 language tag to `write_dashboard`; do not leave renderer fallback text in another language.

Choose the number and order of metrics, charts, observations, and theme cards based on the evidence instead of padding the report to a fixed composition. Include interpretation limits and source/provenance in every report. When a useful requested category is unavailable, state the missing-data limitation rather than inventing values. This is a presentation report, not a patent retrieval interface: do not include patent-evidence tables, search boxes, filters, or other lookup controls.

For renderer-based reports, prepare a JSON payload containing localized `title`, `subtitle`, `metadata`, `metrics`, `charts`, `insights`, `focus_items`, `limitations`, `applicant_note`, `source_note`, and every `section_labels` value, then run:

```powershell
python scripts/html_dashboard.py --payload <localized-report.json> --out <analysis-root>/patent_trends.html --language <query-language-tag>
```

Use `--custom-css <css-file>` when the report needs styling beyond the default shell. Inspect the finished file for stray fallback-language text before delivery.

Use only local, derived data and never fabricate observations, applicant names or counts, labels, patent identifiers, classifications, or period comparisons. Do not relabel inventor names as applicants. If applicant metadata is absent or incomplete, show that limitation in the applicant-distribution section instead of estimating a distribution.

Treat applicant entity resolution as a documented analysis step. Merge bilingual names, subsidiaries, abbreviations, or corporate variants only when the corpus or reliable evidence supports the mapping; preserve the raw labels and mapping in the analysis workspace. Otherwise keep the labels separate and state that the distribution is not entity-resolved.

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

Some provider downloads contain one `index.md` per patent (`profile: patmap-wiki-data-v1`) rather than a dashboard index with precomputed categories. In that layout, count the patent folders and run `scripts/summarize_wiki.py <wiki-root> --outdir <analysis-root>` for a reproducible overview. It produces patent titles, transparent overlapping modality/disease keyword counts, applicant counts when explicitly labeled metadata is present, and `patent_trends.html`. Do not represent these keyword counts as claim-level classifications or target annotations. Use `scripts/search_wiki.py` followed by claim inspection for a specific target, disease, company, or structure question.

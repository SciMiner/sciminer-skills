---
name: pharma-intelligence
description: >
  In-depth, multi-region pharmaceutical intelligence search and synthesis,
  plus drug repurposing, target discovery, clinical evidence review, and
  bioactivity analysis. Use this skill whenever the user asks about drug
  approvals, clinical trials, regulatory submissions, pipeline assets, patent
  landscapes, competitive intelligence, scientific evidence, disease targets,
  genetic associations, or compound bioactivity for any drug, target,
  indication, or company — especially when coverage of China, US, Europe,
  Japan, South Korea, or Australia is needed. Trigger even for casual queries
  like "what's the approval status of X in China", "find trials for Y in
  Japan", "compare pipeline coverage across regions", "find drugs for disease
  Z", or "what targets are associated with condition W". Always consult this
  skill before answering any pharma or biomedical research question that
  requires source-grounded data.
---

# Global Pharma Intelligence & Biomedical Research Skill

Systematic, source-prioritized search and synthesis across regulatory, clinical,
academic, and commercial databases — covering all major pharmaceutical markets
and 14+ biomedical research databases.

## Sub-Skills — How to Invoke

This skill delegates all database work to the sub-skills bundled locally under `skills/`.
Read the relevant sub-skill's `SKILL.md` before invoking it, then run its bundled script.

See [references/sub-skills.md](./references/sub-skills.md) for the full mapping of research
tasks to sub-skills and execution patterns.

---

## Core Principle: Tiered Source Priority

Every region follows a 3-tier hierarchy. Higher tiers override lower-tier claims; always cite the tier.

| Tier | Type | Description |
|------|------|-------------|
| **Tier 1** | Regulatory | Official agency submissions, approvals, labels |
| **Tier 2** | Trial registries | Prospective/registered clinical evidence |
| **Tier 3** | Academic / IP | Published papers, conferences, patents |

For the per-region source map (CN / US / EU / JP / KR / AU + global) with URLs and access notes, see [references/sources-by-region.md](./references/sources-by-region.md).

---

## Search Workflow

### Step 1 — Classify the Query (pick ONE intent)

| # | Intent | Trigger phrases |
|---|--------|-----------------|
| A | Trial landscape | "trials of X", "clinical studies of", "who is testing", "phase 2/3 of" |
| B | Approval / regulatory status | "is X approved", "approval status", "FDA/EMA/NMPA cleared" |
| C | Safety / adverse events | "side effects of", "is X safe", "adverse events", "black box" |
| D | Pipeline / competitive intel | "pipeline", "competitive landscape", "who else is developing" |
| E | Patent / IP / exclusivity | "when does patent expire", "patent landscape", "exclusivity" |
| F | Target / mechanism / drug discovery | "drugs targeting X", "mechanism of", "bioactivity", "IC50" |
| G | Repurposing / target discovery | "repurpose for", "targets associated with disease", "genetic basis" |
| H | Literature / evidence review | "recent papers on", "what's known about", "systematic review" |

Also capture: **regions in scope** (US / EU / JP / CN / KR / AU / global) and **time horizon**.

### Step 2 — Execute the Per-Intent Sequence

Run the workflow for the chosen intent (see [Per-Intent Workflows](#per-intent-workflows)) in order. For sources without MCP coverage (CN NMPA/CDE, EMA EPAR, PMDA, jRCT, CTIS, CRIS, ANZCTR, Orange Book), use `web_fetch` only at the steps that name them.

Resolve identifiers as needed:
- Free-text disease → MONDO/EFO ID via `opentargets-skill` or `efo-ontology-skill`
- Free-text gene → HGNC symbol via `ncbi-clinicaltables-skill` or `ensembl-skill`
- Cross-database ID conversion → `ensembl-skill`, `uniprot-skill`, or `efo-ontology-skill`

### Step 3 — Resolve Conflicts

1. Higher-tier source wins (Tier 1 > Tier 2 > Tier 3).
2. More recent data wins within the same tier.
3. Flag unresolved conflicts; do not silently pick one.

### Step 4 — Synthesize and Present

Structure output to match the intent of the question:
- Trial landscape → table of trials (NCT/registry ID, phase, status, sponsor, N, primary endpoint).
- Approval status → region × status × date × indications table.
- Safety → top FAERS reactions plus black-box / warnings.
- Pipeline → drug × company × phase × mechanism table.
- Patent → patent number, jurisdiction, expiry.

Always cite source, tier, and access date.

---

## Per-Intent Workflows

### A. Trial Landscape

*"What clinical studies / trials exist for [drug | target | indication]?"*

Default scope = ALL regions. Only narrow if the user names a single region.

   `clinicaltrials-skill` covers only ClinicalTrials.gov, which is primarily US-registered trials. Run each regional source in parallel.

1. **United States** — `clinicaltrials-skill` (`action=studies`).
   - Use `query.intr` for a drug, `query.cond` for a disease, both for combined.
   - For a target/class (e.g., "pan-RAS", "PD-L1 inhibitor"): pass the class term as `query.intr` plus a relevant `query.cond`.
   - Then re-run with an NCT ID in `query.id` for eligibility, endpoints, sponsor, and locations.
2. **China** — `web_fetch`:
   - `http://www.chinadrugtrials.org.cn` (mandatory CN IND registry)
   - `https://www.chictr.org.cn` (ChiCTR, WHO primary)
3. **Europe** — `web_fetch`:
   - `https://euclinicaltrials.eu` (CTIS — current EU register)
   - `https://eudract.ema.europa.eu` (EudraCT — legacy historical trials)
   - `https://www.isrctn.com` (ISRCTN, UK/global)
4. **Japan** — `web_fetch`:
   - `https://jrct.niph.go.jp` (jRCT — mandatory JP registry)
   - `https://www.umin.ac.jp/ctr/` (UMIN-CTR — legacy)
5. **South Korea** — `web_fetch` `https://cris.nih.go.kr`.
6. **Australia / New Zealand** — `web_fetch` `https://www.anzctr.org.au`.
7. **WHO ICTRP catch-all** — `web_fetch` `https://trialsearch.who.int` for any WHO primary registry (covers India CTRI, Iran IRCT, Brazil ReBEC, etc.).
8. **Published results** — `ncbi-entrez-skill` (`db=pubmed`) with NCT ID or drug name to surface completed-trial papers.
9. **US company-disclosed pipeline** (optional) — `web_fetch` SEC EDGAR full-text search at `https://efts.sec.gov/LATEST/search-index` for US-listed sponsors.

For every regional `web_fetch`: query both INN and brand name; for CN also use the Chinese transliteration (see [references/drug-naming.md](./references/drug-naming.md)). Aggregate results in one table with a "Registry" column.

### B. Approval / Regulatory Status

*"Is [drug] approved in [region]?"*

1. **US** — `web_fetch` `https://api.fda.gov/drug/label.json` (openFDA) and `https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json` (label date anchors approval); `web_fetch` `https://api.fda.gov/drug/ndc.json` for orphan status.
2. **Non-US** — `web_fetch` the regional Tier 1 source (NMPA, EMA EPAR, PMDA, MFDS, TGA). For CN, also search Chinese characters.
3. `chembl-skill` (`drug_indication.json?molecule_chembl_id=...`) — cross-check approved indications and max phase.
4. Say "not approved" only when Tier 1 affirms denial/withdrawal. Otherwise: "no record found as of [date]".

### C. Safety / Adverse Events

1. `web_fetch` `https://api.fda.gov/drug/event.json` (FAERS) filtering by drug name and seriousness.
2. `web_fetch` `https://api.fda.gov/drug/label.json` with `sections=warnings` and `sections=contraindications`.
3. `chembl-skill` (`molecule/<id>.json`) — inspect the `black_box_warning` flag.
4. `ncbi-entrez-skill` (`db=pubmed`) with terms `"adverse effect" OR "toxicity"` for case reports and post-marketing literature.

### D. Pipeline / Competitive Intelligence

*"Who else is developing for [indication / target]? What's the global competitive landscape?"*

Default scope = ALL regions. A competitive landscape without the active-trial picture is incomplete, so run the full multi-region trial sweep from Workflow A and then layer pipeline-specific sources on top.

1. **Active trials — all regions** — run [Workflow A](#a-trial-landscape) steps 1–7 in full, optionally adding `filter.overallStatus=RECRUITING` (or `ACTIVE_NOT_RECRUITING`) and a phase filter to focus on competitors at a specific stage.
2. **Company disclosures** — `web_fetch` SEC EDGAR full-text search at `https://efts.sec.gov/LATEST/search-index` for pipeline language in 10-K / 10-Q / 8-K (US-listed sponsors only).
3. **Patent activity per company** — `web_fetch` `https://patents.google.com` with an `assignee:` filter (or WIPO PATENTSCOPE / Espacenet — see Workflow E).
4. **Published results** — `ncbi-entrez-skill` (`db=pubmed`) with NCT IDs or drug names to surface completed-trial papers.

Aggregate into one table: drug × company × phase × mechanism × registry/region.

### E. Patent / IP / Exclusivity

All listed patent sources are free and require no API key.

1. **Global patent search** — `web_fetch` one or more of:
   - `https://patents.google.com` (Google Patents — best full-text search, covers USPTO, EPO, WIPO, JPO, CNIPA, KIPO).
   - `https://patentscope.wipo.int` (WIPO PATENTSCOPE — authoritative for PCT applications and national filings worldwide).
   - `https://worldwide.espacenet.com` (EPO Espacenet — strongest European and family-tree coverage).
2. **US patents (structured)** — `uspto_ppubs_search_patents` via MCP for granted patents and applications.
3. **Patent family / cross-jurisdiction equivalents** — Espacenet's "INPADOC patent family" view, or Google Patents' "Worldwide applications" section.
4. **Orange Book** (patent + exclusivity expiry for FDA-approved drugs) — `web_fetch` `https://www.accessdata.fda.gov/scripts/cder/ob`.
5. **Orphan exclusivity** — `fda_orphan_search_exclusivity` (7-year US orphan exclusivity).

### F. Target / Mechanism / Drug Discovery

1. `chembl-skill` — search `target/search.json?q=<gene>` to resolve target ChEMBL ID, then `mechanism.json?target_chembl_id=...` for all drugs.
2. `chembl-skill` — `mechanism.json?molecule_chembl_id=...` for mechanism of action of each candidate.
3. `chembl-skill` — `activity.json?target_chembl_id=...` for IC50 / Kd / EC50 bioactivity comparisons.
4. `uniprot-skill` — `uniprotkb/search` with `gene:<symbol> AND organism_id:9606` for protein function and druggability context.
5. `reactome-skill` — pathway and disease-pathway context for the target.

### G. Repurposing / Target Discovery

1. `opentargets-skill` — search for disease to resolve MONDO / EFO ID.
2. `opentargets-skill` — `associatedTargets` query with disease EFO ID → ranked targets by evidence score.
3. `gwas-catalog-skill` — associations for the disease EFO term to identify genetically supported targets.
4. `web_fetch` OMIM API at `https://api.omim.org/api/entry/search` for Mendelian basis (requires API key).
5. For each top target: `chembl-skill` — `mechanism.json?target_chembl_id=...` for all drugs.
6. `clinicaltrials-skill` with each drug as `query.intr` for prior-art trials.
7. `web_fetch` `https://api.fda.gov/drug/event.json` as a safety filter for non-trivial candidates.

### H. Literature / Evidence Review

1. `ncbi-entrez-skill` (`db=pubmed`) — entry point; use MeSH terms for disease, chemical, and gene-aware filtering.
2. `web_fetch` Europe PMC REST (`https://www.ebi.ac.uk/europepmc/webservices/rest/search`) — broader: grants, preprints, non-MEDLINE.
3. `biorxiv-skill` — bioRxiv / medRxiv preprints only.
4. `ncbi-pmc-skill` or `ncbi-entrez-skill` (`efetch`, `db=pmc`) — abstract or full text for top hits.

---

## Combination Strategies (cross-intent)

Use only when a question genuinely spans multiple intents.

- **Disease → Targets → Drugs → Trials**: `opentargets-skill` (search + associations) → `chembl-skill` (mechanism by target) → `clinicaltrials-skill`
- **Gene → Protein → Pathways → Drugs**: `ncbi-clinicaltables-skill` or `ensembl-skill` → `uniprot-skill` → `reactome-skill` → `chembl-skill` (mechanism by target)
- **Variant → Gene → Disease → Treatments**: `clinvar-variation-skill` or `gnomad-graphql-skill` → `ensembl-skill` → `opentargets-skill` → `chembl-skill` (mechanism by target)
- **Drug → Safety → Label → Trials**: `chembl-skill` (mechanism) → `web_fetch` openFDA adverse events → `web_fetch` openFDA label → `clinicaltrials-skill`

---

## API Keys

Most APIs require no key. Exceptions:

| Database | Key | Source |
|----------|-----|--------|
| OMIM | Required | https://omim.org/api |
| NCI Clinical Trials | Optional | https://clinicaltrialsapi.cancer.gov |
| OpenFDA | Optional (higher rate limits) | https://open.fda.gov/apis |

All bundled sub-skills (ChEMBL, OpenTargets, PubMed via NCBI Entrez, ClinicalTrials.gov, Reactome, UniProt, GWAS Catalog, Ensembl) are public and require no key. Patent landscape work uses Google Patents, WIPO PATENTSCOPE, and Espacenet via `web_fetch` — no keys required.

---

## Output Quality Standards

- Never fabricate approval dates, trial IDs, or efficacy numbers.
- Attribute every claim to its source and tier.
- Flag gaps explicitly (e.g., "No registered trials found in jRCT as of [date]").
- Distinguish "no data found" from "not approved" — absence of evidence ≠ negative regulatory decision.
- For Chinese sources: note whether the search was conducted in Chinese characters; romanization alone may miss records.

---

## Troubleshooting

**No results?**
- Try alternative terms (INN vs brand name, gene symbol vs protein name).
- Use standardized IDs: MONDO/EFO for diseases, HGNC for genes, ChEMBL IDs for compounds, Ensembl for OpenTargets.
- Resolve IDs first with `efo-ontology-skill`, `ncbi-clinicaltables-skill`, `ensembl-skill`, or `uniprot-skill`.

**Too many results?**
- Add filters: `max_items`, `filter.phase`, `filter.overallStatus`, `reviewed=true` (UniProt).
- Apply date ranges where supported.

**API key errors?**
- OMIM requires a key; NCI and OpenFDA accept optional keys for higher rate limits.

**Source not covered by a sub-skill?**
- Use `web_fetch` directly for CDE/NMPA, EMA/EPAR, PMDA, jRCT, CTIS, CRIS, ANZCTR, Orange Book, openFDA, DailyMed, FAERS, and EDGAR.

---

## References

- [references/sub-skills.md](./references/sub-skills.md) — Mapping of pharma-intelligence tasks to bundled sub-skills, with execution patterns.
- [references/drug-naming.md](./references/drug-naming.md) — INN / brand / Chinese / Japanese naming conventions and transliteration.
- [references/regulatory-timelines.md](./references/regulatory-timelines.md) — Review-clock lengths and milestones per agency (FDA, EMA, PMDA, CDE/NMPA, etc.).
- [references/sources-by-region.md](./references/sources-by-region.md) — Direct URLs and access notes for all regional regulatory databases.
- [references/pharma-intelligence-workflow.md](./references/pharma-intelligence-workflow.md) — End-to-end worked example (osimertinib in NSCLC).

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

## MCP Server

**All structured queries go through:**
```
https://mcp.sciminer.tech/tools/unified/mcp
```
Use MCP tools before `web_search`/`web_fetch`. See **[references/mcp-tools.md](./references/mcp-tools.md)** for every tool's exact parameters and call format. For a complete worked example, see **[scripts/pharma-intelligence-workflow.md](./scripts/pharma-intelligence-workflow.md)**.

## Quick Start — Drug Approval Status

```json
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"chembl_search_molecules","arguments":{"query":"osimertinib","max_results":5}},"id":1}
```
Then check FDA label: `openfda_search_drug_labels` → `openfda_get_drug_label`.
For non-US regions (NMPA, EMA, PMDA): fall back to `web_fetch` (no MCP coverage — see Step 9 in workflow).

---

## Core Principle: Tiered Source Priority

Every region follows a **3-tier hierarchy**. Higher tiers override lower-tier
claims when there is conflict. Always cite the source tier in your response.

| Tier | Type | Description |
|------|------|-------------|
| **Tier 1** | Regulatory | Official agency submissions, approvals, labels |
| **Tier 2** | Trial registries | Prospective/registered clinical evidence |
| **Tier 3** | Academic/IP | Published papers, conferences, patents |

---

## Region-by-Region Source Maps

### 🇨🇳 China

```
Tier 1 (Regulatory)
  CDE       — drug evaluation, IND/NDA/sNDA submissions, clinical holds
  NMPA      — final approvals, product licenses, post-market actions

Tier 2 (Trials)
  chinadrugtrials.org.cn  — mandatory CN registry for IND-enabling studies
  ChiCTR                  — WHO-recognized primary registry
  ClinicalTrials.gov      — multinational trials with CN sites

Tier 3 (Academic / IP)
  CNKI / Wanfang / VIP    — Chinese-language literature
  PubMed (CN authors)     — English-language publications
  CNIPA                   — Chinese patents (SIPO successor)
  conference abstracts    — CSCO, ASCO (CN investigators)
```

### 🇺🇸 United States

```
Tier 1 (Regulatory)
  FDA Drugs@FDA        — NDA/ANDA/BLA approvals, labels, reviews
  FDA CDER             — IND database, drug shortage, clinical holds
  FDA CBER             — biologics, cell/gene therapies
  Orange Book          — approved drug products with patent/exclusivity
  Purple Book          — biologics reference list
  SEC/EDGAR            — 10-K/10-Q/8-K with pipeline disclosures

Tier 2 (Trials)
  ClinicalTrials.gov   — global standard; mandatory US registration

Tier 3 (Academic / IP)
  PubMed / MEDLINE     — primary literature
  USPTO / Google Patents— US patents and continuations
  bioRxiv / medRxiv    — preprints
  ASCO / ASH / AACR    — major oncology/hematology conferences
```

### 🇪🇺 Europe (EMA + Member States)

```
Tier 1 (Regulatory)
  EMA EPAR             — European Public Assessment Reports (centralized)
  EMA product database — approved/withdrawn/refused products
  national agencies    — BfArM (DE), ANSM (FR), MHRA (GB post-Brexit)
  MHRA                 — UK-specific approvals (separate post-2021)

Tier 2 (Trials)
  CTIS / EudraCT       — EU Clinical Trials Register (CTIS replacing EudraCT)
  ISRCTN               — UK/global registry
  ClinicalTrials.gov   — multinational trials with EU sites

Tier 3 (Academic / IP)
  PubMed / EMBASE      — European literature
  EPO / Espacenet      — European patent office
  ESMO / EHA / ECCMID  — major EU conferences
```

### 🇯🇵 Japan

```
Tier 1 (Regulatory)
  PMDA                 — approval database, review reports (医薬品審査)
  PMDA jRCT            — Japan Registry of Clinical Trials (integrated)
  MHLW                 — ministry-level policy, guideline notifications

Tier 2 (Trials)
  jRCT                 — mandatory registry for trials in Japan
  UMIN-CTR             — university hospital registry (legacy, still active)
  ClinicalTrials.gov   — multinational trials with JP sites

Tier 3 (Academic / IP)
  J-STAGE              — Japanese scientific literature
  PubMed (JP authors)  — English publications by JP researchers
  JPO / J-PlatPat      — Japan Patent Office
  JSO / JCA            — oncology society conferences
```

### 🇰🇷 South Korea

```
Tier 1 (Regulatory)
  MFDS (식약처)        — Ministry of Food and Drug Safety approvals/labels
  MFDS PharmNet        — drug product database

Tier 2 (Trials)
  CRIS                 — Clinical Research Information Service (KR registry)
  ClinicalTrials.gov   — multinational trials with KR sites

Tier 3 (Academic / IP)
  KISS / RISS / KISTI  — Korean academic databases
  PubMed (KR authors)  — English publications
  KIPO                 — Korean patent database
  KSMO / KCA           — Korean oncology conferences
```

### 🇦🇺 Australia / 🇳🇿 New Zealand

```
Tier 1 (Regulatory)
  TGA                  — Therapeutic Goods Administration approvals
  TGA ARTG             — Australian Register of Therapeutic Goods
  Medsafe (NZ)         — NZ regulatory database

Tier 2 (Trials)
  ANZCTR               — Australia New Zealand Clinical Trials Registry
  ClinicalTrials.gov   — multinational trials with AU/NZ sites

Tier 3 (Academic / IP)
  PubMed (AU authors)  — primary literature
  IP Australia         — AU patent database
  ASM / COSA           — Australian oncology/medical societies
```

### 🌐 Cross-Regional / Global Sources

```
Tier 1 (Regulatory harmonization)
  ICH guidelines       — global technical standards
  WHO prequalification — developing-market approvals

Tier 2 (Trials — global)
  WHO ICTRP            — aggregates all WHO primary registries
  ClinicalTrials.gov   — de facto global standard

Tier 3 (Academic / IP — global)
  PubMed / MEDLINE     — primary
  Embase               — European emphasis, drug-focused
  Cochrane Library     — systematic reviews / meta-analyses
  Google Patents        — global patent aggregator
  Lens.org             — open patent + literature cross-search
```

---

## MCP Tools Available

All tools are accessible via the unified MCP server at:
**`https://mcp.sciminer.tech/tools/unified/mcp`**

Or via individual servers at `/tools/{server}/mcp` on the same host.

Prefer MCP tools over `web_search`/`web_fetch` — they are structured, cached,
and reliably return machine-readable data without HTML parsing.

### Drug / Compound Identification
- **PubChem** (`/tools/pubchem/mcp`): `pubchem_search_compound`, `pubchem_get_compound`,
  `pubchem_get_compound_by_name`, `pubchem_search_bioassay` — structure lookup by name/CAS/SMILES/InChIKey,
  CID → properties, synonym lists (brand names, CAS), bioassay data
- **BioThings / MyChem** (`/tools/biothings/mcp`): `mychem_get_chemical` — cross-references ChEMBL,
  DrugBank, PubChem in one call; `mychem_get_drug`, `mychem_search_drugs` — chemical structure,
  synonyms, pharmacology, external IDs (SMILES, InChI, PubChem, DrugBank)
- **ChEMBL** (`/tools/chembl/mcp`): 2M+ drugs and compounds with bioactivity data
  - `chembl_search_molecules` / `chembl_get_molecule` — find drug by name, get full molecule data
    (SMILES, MW, LogP, ATC codes, max phase, indications, black box warnings)
  - `chembl_search_targets` / `chembl_get_target` — find proteins by name, get UniProt cross-refs
  - `chembl_find_drugs_by_indication` — all approved + investigational drugs for a disease
  - `chembl_find_drugs_by_target` — all drugs targeting a gene/protein (pass `include_all_mechanisms=true`)
  - `chembl_get_activities` — 15M+ bioactivity records (IC50, Kd, EC50) by molecule or target
  - `chembl_get_mechanism` / `chembl_get_molecule_mechanisms` — mechanism of action (human-curated)
  - `chembl_get_drug_indications` — all FDA-approved and investigational indications for a drug
  - `chembl_get_compound_by_name` — direct name lookup

### US Regulatory
- **OpenFDA** (`/tools/openfda/mcp`): `openfda_search_adverse_events`, `openfda_search_drug_labels`,
  `openfda_get_drug_label` — FAERS adverse events, FDA label full text, recalls, enforcement
- **DailyMed** (`/tools/dailymed/mcp`): `dailymed_search_drug_labels`, `dailymed_get_spl`,
  `dailymed_search_ndc`, `dailymed_get_drug_classes` — official FDA-approved label database (SPL),
  NDC lookup, pharmacological class (EPC, MoA, Chemical Structure)
- **FDA Orphan** (`/tools/fda-orphan/mcp`): `fda_orphan_search_exclusivity`,
  `fda_orphan_search_designations` — 7-year orphan exclusivity periods, OOPD designations

### Clinical Trials
- **ClinicalTrials.gov** (`/tools/ctg/mcp`): `ctg_search_studies`, `ctg_get_study` — US mandatory
  registry with global coverage; structured query by condition, intervention, status, phase
- **NCI Clinical Trials** (`/tools/nci/mcp`, requires API key): `nci_search_trials` — NCI-specific
  oncology trial search
- **Europe PMC** (`/tools/europepmc/mcp`): `europepmc_search`, `europepmc_search_preprints`,
  `europepmc_get_article`, `europepmc_get_references` — broader than PubMed: covers preprints
  (bioRxiv/medRxiv), grants, and WHO ICTRP-linked trial publications

### Patent / IP
- **Lens.org** (`/tools/lens/mcp`, requires API key): `lens_search_patents`, `lens_get_patent`,
  `lens_get_patent_family`, `lens_search_by_applicant` — cross-jurisdiction search (USPTO, EPO,
  WIPO/PCT, JPO, IP Australia); preferred for global patent landscapes; free key at https://www.lens.org
- **USPTO PPUBS** (`/tools/uspto-ppubs/mcp`): `uspto_ppubs_search_patents`,
  `uspto_ppubs_search_applications` — US-only granted patents and pending applications

### Financial / Competitive Intelligence
- **SEC EDGAR** (`/tools/edgar/mcp`): `edgar_search_company`, `edgar_search_filings`,
  `edgar_fulltext_search`, `edgar_get_company_filings` — 10-K pipeline disclosures,
  8-K FDA decision announcements, 10-Q quarterly clinical updates for US-listed pharma companies

### Scientific Literature
- **PubMed** (`/tools/pubmed/mcp`): `pubmed_search_articles`, `pubmed_get_article`,
  `pubmed_search_preprints` — PubTator3, entity-aware biomedical literature search
- **Europe PMC** (`/tools/europepmc/mcp`): `europepmc_search`, `europepmc_get_article`,
  `europepmc_get_references` — broader than PubMed: grants, preprints, patents, non-MEDLINE

### Target / Biology
- **UniProt** (`/tools/uniprot/mcp`): `uniprot_search_proteins`, `uniprot_get_protein`,
  `uniprot_get_disease_associations`, `uniprot_map_ids` — sequences, annotations, disease links
- **OpenTargets** (`/tools/opentargets/mcp`): disease-target links with evidence scoring (0–1)
  - `opentargets_search` — find target genes or diseases (returns MONDO/Ensembl IDs)
  - `opentargets_get_associations` — targets ranked by evidence strength for a disease
  - `opentargets_get_evidence` — evidence breakdown (genetics, literature, expression, clinical)
  - `opentargets_get_target` — target properties and druggability
- **Reactome** (`/tools/reactome/mcp`): `reactome_search_pathways`, `reactome_get_pathway`,
  `reactome_get_disease_pathways` — curated pathways, protein interactions, disease mechanisms
- **KEGG** (`/tools/kegg/mcp`): `kegg_search`, `kegg_get_pathway`, `kegg_list_pathways`,
  `kegg_find_pathways`, `kegg_get_disease`, `kegg_get_gene` — metabolic, signaling, disease pathways
- **GWAS** (`/tools/gwas/mcp`): `gwas_search_associations`, `gwas_search_traits`,
  `gwas_get_variant`, `gwas_search_studies` — genome-wide associations linking variants to traits
- **OMIM** (`/tools/omim/mcp`, requires API key): `omim_get_entry`, `omim_search_entries` — genetic
  disorders, gene → phenotype links; key from https://omim.org/api
- **Pathway Commons** (`/tools/pathwaycommons/mcp`): `pathwaycommons_search`,
  `pathwaycommons_graph`, `pathwaycommons_traverse` — aggregated pathway data from Reactome,
  BioPAX, NCI PID; graph neighborhood queries (e.g., all interactors of TP53)
- **BioThings / MyGene** (`/tools/biothings/mcp`): `mygene_get_gene`, `mygene_search_genes` —
  gene location, aliases, Ensembl/UniProt/NCBI cross-references, orthologs
- **BioThings / MyVariant** (`/tools/biothings/mcp`): `myvariant_get_variant`,
  `myvariant_search_variants` — variant effect predictions (SIFT/PolyPhen), ClinVar significance,
  gnomAD frequencies, CADD scores; query by gene, rsID, or consequence type
- **Node Normalization** (`/tools/nodenorm/mcp`): `nodenorm_get_normalized_nodes` — resolve CURIEs
  across databases (e.g., HGNC → NCBI Gene, UniProt, Ensembl in one call)

---

## Database Quick-Reference

| Goal | Best MCP Tool(s) |
|------|-----------------|
| Find drugs approved for a disease | `chembl_find_drugs_by_indication` |
| Find drugs targeting a specific gene | `chembl_find_drugs_by_target` |
| Get drug mechanism of action | `chembl_get_mechanism` |
| Find disease targets ranked by evidence | `opentargets_search` → `opentargets_get_associations` |
| Get evidence for a target-disease link | `opentargets_get_evidence` |
| Drug/compound structure & identity | `pubchem_*`, `chembl_*`, `mychem_*` |
| US drug labels / NDC lookup | `dailymed_*`, `openfda_*` |
| US adverse events / recalls | `openfda_search_adverse_events` |
| Orphan drug status | `fda_orphan_*` |
| US & global clinical trials | `ctg_*`, `nci_*` (oncology) |
| Global patents (all jurisdictions) | `lens_*` (requires API key) |
| US-only patents | `uspto_ppubs_*` |
| SEC financial disclosures | `edgar_*` |
| Biomedical literature | `pubmed_*`, `europepmc_*` |
| Pathway / mechanism biology | `reactome_*`, `kegg_*`, `pathwaycommons_*` |
| Protein details | `uniprot_*`, `mygene_*` |
| Genetic variants | `gwas_*`, `myvariant_*` |
| Genetic disease basis | `omim_*` |
| Cross-source ID normalization | `nodenorm_get_normalized_nodes` |

---

## Search Workflow

### Step 1 — Classify the Query

Determine:
- **Subject**: drug name (INN / brand) · target/pathway · indication · company
- **Question type**: approval status · trial landscape · pipeline · patent · safety signal ·
  competitive intel · drug repurposing · target discovery
- **Regions**: which markets are in scope?
- **Time horizon**: current status · historical · prospective pipeline

### Step 2 — Select Sources by Priority

Use the region maps above. Always start at **Tier 1** for the relevant region(s).
Descend to Tier 2/3 only if:
- Tier 1 has no record (e.g., not yet approved → go to trials)
- Question is specifically about evidence/mechanism (→ academic)
- Patent landscape requested (→ IP sources)

### Step 3 — Execute Searches

**First, use MCP tools** (structured, cached, reliable — no HTML parsing needed):

| Intelligence Category | Preferred MCP Tool(s) |
|-----------------------|-----------------------|
| Drug/compound structure & identity | `pubchem_*`, `chembl_*`, `mychem_*` |
| US drug labels / NDC lookup | `dailymed_*`, `openfda_*` |
| US adverse events / recalls | `openfda_search_adverse_events` |
| Orphan drug status | `fda_orphan_*` |
| US & global clinical trials | `ctg_*`, `nci_*` (oncology) |
| Global patents (all jurisdictions) | `lens_*` (requires API key) |
| US-only patents | `uspto_ppubs_*` |
| SEC financial disclosures | `edgar_*` |
| Biomedical literature | `pubmed_*`, `europepmc_*` |
| Target / pathway biology | `uniprot_*`, `opentargets_*`, `reactome_*`, `kegg_*` |
| Cross-source ID normalization | `nodenorm_get_normalized_nodes` |

Apply structured search terms:
```
drug name variants: INN + brand name(s) + CAS number if known
company: developer + licensee (different in different markets)
indication: MeSH / ICD-10 terms for consistency
status filters: apply where available (approved / active / terminated)
date range: specify if recency matters
```

**Fall back to `web_search`/`web_fetch` only** for sources without MCP coverage:
- CDE / NMPA (China: drug evaluation submissions, final approvals)
- EMA / national EU agencies (EPAR, BfArM, ANSM, MHRA)
- PMDA / MHLW (Japan: approvals, review reports)
- jRCT / UMIN-CTR (Japanese trial registries)
- CTIS / EudraCT (EU Clinical Trials register)
- CRIS (South Korea registry)
- ANZCTR (Australia/New Zealand registry)
- WHO ICTRP (if europepmc_search doesn't cover the specific registry)
- Chinese literature: CNKI, Wanfang, VIP, SinoMed
- Regional conference abstracts (CSCO, JCA, KSMO, ESMO, ASH, ASCO)

For Chinese sources, always search both Chinese characters and romanized terms.

### Step 4 — Resolve Conflicts

When sources disagree:
1. Higher-tier source wins
2. More recent data wins within the same tier
3. Flag unresolved conflicts explicitly — do not silently pick one

### Step 5 — Synthesize and Present

Structure output by:
- **Regulatory status** (per region, with dates)
- **Clinical evidence** (key trials, phase, enrollment, primary endpoints)
- **Pipeline position** (earliest → most advanced)
- **Patent / exclusivity** (expiry dates, evergreening patterns)
- **Competitive landscape** (approved + late-stage competitors)

Always cite source + tier + access date for each factual claim.

---

## Research Use Cases

### 🧬 Drug Repurposing

Find non-standard-care drugs for a disease:

1. **Identify disease targets** — `opentargets_search` (get MONDO ID) → `opentargets_get_associations` (rank targets by evidence)
2. **Check genetic basis** — `omim_search_entries` (which genes cause the disease?)
3. **Find drugs on those targets** — `chembl_find_drugs_by_target` for each gene (include `include_all_mechanisms=true`)
4. **Check what's already approved** — `chembl_find_drugs_by_indication` (baseline)
5. **Verify safety** — `openfda_search_adverse_events`, `openfda_search_drug_labels` (warnings)
6. **Check active trials** — `ctg_search_studies` (condition + intervention)
7. **Validate in literature** — `pubmed_search_articles`, `europepmc_search`
8. **Understand mechanism** — `reactome_get_disease_pathways`, `kegg_get_disease`, `uniprot_search_proteins`

### 🔬 Target Discovery

Identify novel therapeutic targets:

1. `opentargets_search` + `opentargets_get_associations` — ranked targets with association scores
2. `gwas_search_associations` — genetic variants linking targets to disease
3. `opentargets_get_evidence` — what types of evidence support each target?
4. `reactome_get_pathway` / `kegg_get_pathway` — pathway context
5. `uniprot_get_protein` — protein function, subcellular location, druggability
6. `pubmed_search_articles` — recent literature
7. `chembl_find_drugs_by_target` — is anyone already drugging this target?

### 📋 Clinical Evidence Review

1. `ctg_search_studies` — active/completed trials (filter by phase, status)
2. `ctg_get_study` — detailed protocol, endpoints, enrollment
3. `pubmed_search_articles` — published results
4. `europepmc_search` — preprints + broader coverage
5. `openfda_search_adverse_events` — safety signal from FAERS

### 🏭 Competitive Intelligence

1. `chembl_find_drugs_by_indication` — approved + pipeline drugs for the indication
2. `ctg_search_studies` — all active trials by condition
3. `edgar_search_filings` / `edgar_fulltext_search` — pipeline disclosures in SEC filings
4. `lens_search_patents` — patent landscape by applicant or compound
5. Layer region-specific Tier 1 sources for each market

---

## Combination Strategies

### Gene → Protein → Pathways → Drug Targets

1. `mygene_search_genes` — get gene aliases, Ensembl/UniProt cross-references
2. `uniprot_get_protein` — protein function, disease associations
3. `reactome_search_pathways` or `pathwaycommons_graph` — pathways containing the protein
4. `chembl_find_drugs_by_target` — drugs targeting that protein

### Disease → Targets → Drugs → Trials

1. `opentargets_search` — get MONDO disease ID
2. `opentargets_get_associations` — top targets ranked by evidence (0–1 score)
3. `chembl_find_drugs_by_target` — drugs for each target
4. `ctg_search_studies` — active trials for each candidate

### Variant → Gene → Disease → Treatments

1. `myvariant_get_variant` — variant effects, ClinVar significance
2. `mygene_get_gene` — gene context, aliases
3. `omim_search_entries` — confirmed disease links
4. `chembl_find_drugs_by_target` — treatment options for the gene

### Drug → Safety → Label → Trials

1. `chembl_search_molecules` → `chembl_get_mechanism` — mechanism of action
2. `openfda_search_adverse_events` — FAERS safety signals
3. `dailymed_search_drug_labels` / `openfda_get_drug_label` — full label + warnings
4. `ctg_search_studies` — any trials in the indication of interest?

---

## Common Query Templates

### Approval Status Query
> "What is the approval status of [drug] in [region(s)]?"
→ Search Tier 1 for each named region → cross-check label dates → note any indication restrictions

### Trial Landscape Query
> "What trials are running for [drug/target] in [indication]?"
→ Search all Tier 2 registries for named regions → filter by status (recruiting/active) → extract phase, N, endpoints, estimated completion

### Patent & Exclusivity Query
> "When do patents expire for [drug]?"
→ Orange Book (US) → EP patent register → CNIPA (CN) → cross-reference with data exclusivity periods per region

### Competitive Intelligence Query
> "What is the competitive landscape for [target/indication]?"
→ Start from WHO ICTRP for global trial count → break down by region Tier 2 → layer Tier 1 approvals → Tier 3 for mechanism papers

### Drug Repurposing Query
> "Are there any drugs that could be repurposed for [rare disease]?"
→ OpenTargets (targets) → OMIM (genetic basis) → ChEMBL (drugs on those targets) → ClinicalTrials (active studies) → OpenFDA (safety)

---

## API Keys

Most APIs require **no key**. Required or optional keys:

| Database | Key? | Get Key |
|----------|------|---------|
| ChEMBL | No | Public |
| OpenTargets | No | Public |
| PubMed | No | Public |
| ClinicalTrials.gov | No | Public |
| Reactome / KEGG / UniProt | No | Public |
| GWAS / Pathway Commons | No | Public |
| MyGene / MyVariant / MyChem | No | Public |
| Node Normalization | No | Public |
| **OMIM** | **Yes (required)** | https://omim.org/api |
| NCI Clinical Trials | Optional | https://clinicaltrialsapi.cancer.gov |
| OpenFDA | Optional | https://open.fda.gov/apis |
| **Lens.org** | **Yes (free)** | https://www.lens.org |

---

## Output Quality Standards

- **Never fabricate** approval dates, trial IDs, or efficacy numbers
- **Always attribute** each claim to its source and tier
- **Flag gaps**: if a region has no data, state explicitly ("No registered trials found in jRCT as of [date]")
- **Distinguish** "no data found" from "not approved" — absence of evidence ≠ negative regulatory decision
- For Chinese sources: note whether the search was conducted in Chinese characters; romanization alone may miss records

---

## Troubleshooting

**No results from MCP tools?**
- Try alternative terms (INN vs brand name, gene symbol vs protein name)
- Use standardized IDs: MONDO for diseases, HGNC symbols for genes, ChEMBL IDs for compounds
- Check ID format — OpenTargets uses Ensembl IDs, OMIM uses MIM numbers
- Use `nodenorm_get_normalized_nodes` to convert between ID formats

**Too many results?**
- Add filters: `max_results`, `phase`, `recruitment_status`, `reviewed` (UniProt)
- Combine databases — use one to get IDs, then query another with structured IDs
- Apply date range filters where supported

**API key errors?**
- OMIM: always required — get from https://omim.org/api
- Lens.org: free key — register at https://www.lens.org
- NCI / OpenFDA: optional keys increase rate limits

**Source not covered by MCP?**
- Fall back to `web_search` / `web_fetch` for CDE/NMPA, EMA/EPAR, PMDA, jRCT, CTIS, CRIS, ANZCTR
- For Chinese sources: search both Chinese characters and romanized terms

---

## References

- **[references/mcp-tools.md](./references/mcp-tools.md)** — Exact call format and parameters for every MCP tool (drug lookup, regulatory, trials, patents, literature, biology)
- **[references/drug-naming.md](./references/drug-naming.md)** — INN/brand/Chinese/Japanese naming conventions and transliteration rules
- **[references/regulatory-timelines.md](./references/regulatory-timelines.md)** — Review clock lengths and key milestones per agency (FDA, EMA, PMDA, CDE/NMPA, etc.)
- **[references/sources-by-region.md](./references/sources-by-region.md)** — Direct URLs and access notes for all regional regulatory databases
- **[scripts/pharma-intelligence-workflow.md](./scripts/pharma-intelligence-workflow.md)** — Complete 9-step workflow with curl examples (drug lookup → regulatory → trials → safety → patents → competitive → biology → literature → non-US web fallback)

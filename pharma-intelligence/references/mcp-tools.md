# MCP Tools Quick Reference

## How to Invoke

**There is no dedicated "MCP tool" in your toolbox.** Call the endpoint directly using `web_fetch` (HTTP POST) or `run_in_terminal` (curl).

```bash
# curl — run_in_terminal
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"TOOL_NAME","arguments":{...}},"id":1}'
```

```
# web_fetch — HTTP POST
POST https://mcp.sciminer.tech/tools/unified/mcp
Content-Type: application/json
Accept: application/json

{"jsonrpc":"2.0","method":"tools/call","params":{"name":"TOOL_NAME","arguments":{...}},"id":1}
```

Or use individual servers: `https://mcp.sciminer.tech/tools/{server}/mcp`

---

## Drug / Compound Lookup

### `pubchem_search_compound` — Find compound by name/CAS/SMILES
```json
{"name": "pubchem_search_compound", "arguments": {"query": "imatinib", "max_results": 5}}
```
Returns: CID, IUPAC name, synonyms (brand names), molecular formula, InChIKey

### `mychem_search_drugs` — Cross-database drug lookup
```json
{"name": "mychem_search_drugs", "arguments": {"query": "gleevec", "max_results": 5}}
```
Returns: ChEMBL ID, DrugBank ID, PubChem CID, SMILES, pharmacology summary in one call

### `chembl_search_molecules` — Search ChEMBL by name/synonym
```json
{"name": "chembl_search_molecules", "arguments": {"query": "pembrolizumab", "max_results": 10}}
```

### `chembl_get_molecule` — Full molecule data by ChEMBL ID
```json
{"name": "chembl_get_molecule", "arguments": {"molecule_id": "CHEMBL2397693"}}
```
Returns: SMILES, MW, LogP, ATC codes, max phase, indications, black box warnings

### `chembl_find_drugs_by_indication` — All drugs approved/investigated for a disease
```json
{"name": "chembl_find_drugs_by_indication", "arguments": {"indication": "non-small cell lung cancer", "max_results": 30}}
```

### `chembl_find_drugs_by_target` — All drugs targeting a gene/protein
```json
{"name": "chembl_find_drugs_by_target", "arguments": {"target_name": "EGFR", "include_all_mechanisms": true, "max_results": 20}}
```

### `chembl_get_mechanism` / `chembl_get_molecule_mechanisms` — Mechanism of action
```json
{"name": "chembl_get_mechanism", "arguments": {"molecule_id": "CHEMBL2397693"}}
```

### `chembl_get_drug_indications` — All approved + investigational indications for a drug
```json
{"name": "chembl_get_drug_indications", "arguments": {"molecule_id": "CHEMBL2397693"}}
```

---

## US Regulatory

### `openfda_search_drug_labels` — FDA drug labels (package inserts)
```json
{"name": "openfda_search_drug_labels", "arguments": {"drug_name": "pembrolizumab", "section": "warnings"}}
```

### `openfda_get_drug_label` — Full label by set_id
```json
{"name": "openfda_get_drug_label", "arguments": {"set_id": "abc123", "section": "indications_and_usage"}}
```
Sections: `warnings`, `contraindications`, `adverse_reactions`, `dosage_and_administration`, `indications_and_usage`

### `openfda_search_adverse_events` — FAERS adverse event search
```json
{"name": "openfda_search_adverse_events", "arguments": {"drug_name": "nivolumab", "seriousness": "serious", "limit": 50}}
```

### `dailymed_search_drug_labels` — Official FDA label database (SPL)
```json
{"name": "dailymed_search_drug_labels", "arguments": {"drug_name": "keytruda", "max_results": 5}}
```

### `dailymed_get_spl` — Full structured product label
```json
{"name": "dailymed_get_spl", "arguments": {"set_id": "spl-set-id"}}
```

### `fda_orphan_search_designations` — Orphan drug designations (OOPD)
```json
{"name": "fda_orphan_search_designations", "arguments": {"drug_name": "imatinib", "max_results": 10}}
```

### `fda_orphan_search_exclusivity` — 7-year orphan exclusivity periods
```json
{"name": "fda_orphan_search_exclusivity", "arguments": {"drug_name": "imatinib"}}
```

---

## Clinical Trials

### `ctg_search_studies` — ClinicalTrials.gov search with filters
```json
{
  "name": "ctg_search_studies",
  "arguments": {
    "condition": "non-small cell lung cancer",
    "intervention": "osimertinib",
    "recruitment_status": "RECRUITING",
    "phase": "PHASE3",
    "max_results": 20
  }
}
```
`recruitment_status` values: `RECRUITING`, `ACTIVE_NOT_RECRUITING`, `COMPLETED`, `TERMINATED`, `WITHDRAWN`
`phase` values: `PHASE1`, `PHASE2`, `PHASE3`, `PHASE4`, `EARLY_PHASE1`

### `ctg_get_study` — Full trial protocol
```json
{"name": "ctg_get_study", "arguments": {"nct_id": "NCT04604678"}}
```
Returns: eligibility criteria, endpoints, locations, enrollment, sponsor

### `nci_search_trials` — NCI oncology-specific trial search (requires API key)
```json
{"name": "nci_search_trials", "arguments": {"condition": "glioblastoma", "api_key": "YOUR_KEY", "max_results": 20}}
```

---

## Patent / IP

### Global patent search (no MCP — use `web_fetch`)

All free and require no API key:

- **Google Patents** — `https://patents.google.com/?q=<query>` (best full-text; covers USPTO, EPO, WIPO, JPO, CNIPA, KIPO).
- **WIPO PATENTSCOPE** — `https://patentscope.wipo.int/search/en/result.jsf?query=<query>` (authoritative for PCT and national filings).
- **Espacenet (EPO)** — `https://worldwide.espacenet.com/patent/search?q=<query>` (best European coverage; use INPADOC patent-family view for cross-jurisdiction equivalents).

Filter by assignee/applicant via the source's UI parameters (e.g., Google Patents `assignee:` keyword).

### `uspto_ppubs_search_patents` — US-only granted patents
```json
{"name": "uspto_ppubs_search_patents", "arguments": {"query": "anti-PD-1 antibody", "max_results": 20}}
```

### `uspto_ppubs_search_applications` — US pending applications
```json
{"name": "uspto_ppubs_search_applications", "arguments": {"query": "EGFR inhibitor cancer", "max_results": 20}}
```

---

## Financial / Competitive Intelligence

### `edgar_search_company` — Find company in EDGAR
```json
{"name": "edgar_search_company", "arguments": {"query": "Merck", "max_results": 10}}
```

### `edgar_search_filings` — Search SEC filings by type
```json
{"name": "edgar_search_filings", "arguments": {"company_name": "Merck", "form_type": "10-K", "max_results": 5}}
```
`form_type`: `10-K` (annual), `10-Q` (quarterly), `8-K` (current events/FDA decisions)

### `edgar_fulltext_search` — Search full text of SEC filings
```json
{"name": "edgar_fulltext_search", "arguments": {"query": "pembrolizumab pipeline approval", "max_results": 10}}
```
Best for: finding pipeline disclosures, FDA decision announcements in filings

---

## Literature

### `pubmed_search_articles` — PubMed literature search
```json
{
  "name": "pubmed_search_articles",
  "arguments": {
    "query": "osimertinib resistance mechanisms",
    "diseases": ["non-small cell lung cancer"],
    "chemicals": ["osimertinib"],
    "max_results": 30
  }
}
```

### `europepmc_search` — Broader search (preprints + non-MEDLINE + grants)
```json
{"name": "europepmc_search", "arguments": {"query": "PD-L1 immunotherapy 2025", "max_results": 20}}
```

### `europepmc_search_preprints` — bioRxiv/medRxiv preprints only
```json
{"name": "europepmc_search_preprints", "arguments": {"query": "CAR-T cell therapy GvHD", "max_results": 10}}
```

---

## Target / Biology

### `opentargets_search` — Find disease (MONDO ID) or target (Ensembl ID)
```json
{"name": "opentargets_search", "arguments": {"query": "non-small cell lung cancer", "entity_type": "disease"}}
```

### `opentargets_get_associations` — Targets ranked by evidence score (0–1)
```json
{"name": "opentargets_get_associations", "arguments": {"disease_id": "MONDO_0005233", "size": 25}}
```

### `opentargets_get_evidence` — Evidence breakdown for target-disease pair
```json
{"name": "opentargets_get_evidence", "arguments": {"target_id": "ENSG00000146648", "disease_id": "MONDO_0005233"}}
```

### `uniprot_search_proteins` — Search proteins by name/gene/function
```json
{"name": "uniprot_search_proteins", "arguments": {"query": "EGFR", "reviewed": true, "max_results": 5}}
```
`reviewed: true` returns only Swiss-Prot curated entries

### `reactome_search_pathways` — Find relevant pathways
```json
{"name": "reactome_search_pathways", "arguments": {"query": "EGFR signaling", "max_results": 10}}
```

### `reactome_get_disease_pathways` — Disease-specific pathways
```json
{"name": "reactome_get_disease_pathways", "arguments": {"disease_name": "lung cancer"}}
```

### `gwas_search_associations` — Genetic variants linked to disease
```json
{"name": "gwas_search_associations", "arguments": {"query": "non-small cell lung cancer", "p_upper": 0.00001}}
```

### `omim_search_entries` — Genetic disease basis (requires API key)
```json
{"name": "omim_search_entries", "arguments": {"search_term": "lung adenocarcinoma", "api_key": "YOUR_KEY"}}
```

### `nodenorm_get_normalized_nodes` — Convert IDs across databases
```json
{"name": "nodenorm_get_normalized_nodes", "arguments": {"curie": "HGNC:3236"}}
```
Returns: NCBI Gene, UniProt, Ensembl, MyGene equivalents in one call

### `mygene_search_genes` — Gene info (location, aliases, cross-references)
```json
{"name": "mygene_search_genes", "arguments": {"query": "EGFR", "max_results": 5}}
```

### `myvariant_get_variant` — Variant effects, ClinVar significance
```json
{"name": "myvariant_get_variant", "arguments": {"variant_id": "rs121913529"}}
```
Returns: SIFT/PolyPhen scores, ClinVar significance, gnomAD frequency, CADD score

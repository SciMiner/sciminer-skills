# Pharma Intelligence Workflow — Complete Example

**Goal**: Full competitive intelligence report on a drug in a target indication across regions.
**Example**: Osimertinib (Tagrisso) in EGFR-mutant NSCLC

---

## Step 1: Identify the Drug

```bash
# chembl-skill — molecule search
cd skills/chembl-skill
echo '{"base_url":"https://www.ebi.ac.uk/chembl/api/data","path":"molecule/search.json","params":{"q":"osimertinib","limit":5},"record_path":"molecules","max_items":5}' \
  | python scripts/rest_request.py
```

Note the ChEMBL ID (e.g., `CHEMBL3353410`) and max phase. Then get full details:

```bash
# chembl-skill — full molecule record
echo '{"base_url":"https://www.ebi.ac.uk/chembl/api/data","path":"molecule/CHEMBL3353410.json"}' \
  | python scripts/rest_request.py
```

Returns: SMILES, ATC codes, max phase, indications, black box warning flag.

---

## Step 2: US Regulatory Status

### FDA label (approved indications + label date)
```bash
# web_fetch — openFDA drug label
web_fetch 'https://api.fda.gov/drug/label.json?search=openfda.generic_name:osimertinib&limit=1'
```

### Orphan designation (if applicable)
```bash
# web_fetch — FDA Orphan Drug Product Designation Database
web_fetch 'https://www.accessdata.fda.gov/scripts/opdlisting/oopd/listResult.cfm?Search_Term=osimertinib'
```

### Orange Book / exclusivity
```bash
# web_fetch — Orange Book
web_fetch 'https://www.accessdata.fda.gov/scripts/cder/ob/results_product.cfm?Appl_Type=N&Appl_No=208065'
```

---

## Step 3: US Clinical Trials (Phase 3 + Active)

> **Scope:** `clinicaltrials-skill` queries ClinicalTrials.gov, which is **US-only**. For CN/EU/JP/KR/AU trials, run the regional `web_fetch` calls in Step 9 in parallel.

```bash
# clinicaltrials-skill — Phase 3 study search
cd skills/clinicaltrials-skill
echo '{"action":"studies","params":{"query.cond":"non-small cell lung cancer","query.intr":"osimertinib","filter.phase":"PHASE3","pageSize":20},"max_items":20,"max_pages":1}' \
  | python scripts/clinicaltrials_client.py
```

Get full protocol for a key trial:
```bash
# clinicaltrials-skill — single trial by NCT ID
echo '{"action":"studies","params":{"query.id":"NCT02151981","pageSize":1},"max_items":1}' \
  | python scripts/clinicaltrials_client.py
```

---

## Step 4: Safety Profile (FAERS)

```bash
# web_fetch — openFDA adverse events
web_fetch 'https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:osimertinib+AND+serious:1&limit=50'
```

---

## Step 5: Patent / IP Landscape

Global patent search uses free web sources (no API key):

- Google Patents: `web_fetch https://patents.google.com/?q=osimertinib+EGFR+T790M`
- WIPO PATENTSCOPE: `web_fetch https://patentscope.wipo.int/search/en/result.jsf?query=osimertinib`
- Espacenet (EPO): `web_fetch https://worldwide.espacenet.com/patent/search?q=osimertinib` (use the "INPADOC patent family" view for cross-jurisdiction equivalents)

Structured US patent search:

```bash
# web_fetch — USPTO patent search (no sub-skill)
web_fetch 'https://ppubs.uspto.gov/dirsearch-public/print/downloadPdf/osimertinib'
# Or via Google Patents (easier full-text search)
web_fetch 'https://patents.google.com/?q=osimertinib+EGFR+T790M&assignee=AstraZeneca'
```

For Orange Book expiry: `web_fetch https://www.accessdata.fda.gov/scripts/cder/ob`.

---

## Step 6: Competitive Landscape (Same Indication)

### All drugs approved/investigated for NSCLC
```bash
# chembl-skill — drug indications by EFO term
cd skills/chembl-skill
echo '{"base_url":"https://www.ebi.ac.uk/chembl/api/data","path":"drug_indication.json","params":{"efo_term":"non-small cell lung carcinoma","limit":20},"record_path":"drug_indications","max_items":50}' \
  | python scripts/rest_request.py
```

### All active NSCLC trials (any intervention)
```bash
# clinicaltrials-skill — recruiting Phase 3 trials
cd skills/clinicaltrials-skill
echo '{"action":"studies","params":{"query.cond":"non-small cell lung cancer","filter.overallStatus":"RECRUITING","filter.phase":"PHASE3","pageSize":30},"max_items":30,"max_pages":1}' \
  | python scripts/clinicaltrials_client.py
```

### Competitor SEC pipeline disclosures
```bash
# web_fetch — EDGAR full-text search (no sub-skill)
web_fetch 'https://efts.sec.gov/LATEST/search-index?q=%22EGFR+inhibitor%22+%22NSCLC%22+%22pipeline%22&dateRange=custom&startdt=2025-01-01&forms=10-K,10-Q'
```

---

## Step 7: Target Biology (Mechanism Validation)

### Get EGFR gene info and cross-references
```bash
# ncbi-clinicaltables-skill or ensembl-skill
cd skills/ensembl-skill
echo '{"base_url":"https://rest.ensembl.org","path":"lookup/symbol/homo_sapiens/EGFR","params":{"content-type":"application/json","expand":1}}' \
  | python scripts/rest_request.py
```

### Find all drugs targeting EGFR
```bash
# chembl-skill — target search then mechanism lookup
cd skills/chembl-skill
echo '{"base_url":"https://www.ebi.ac.uk/chembl/api/data","path":"target/search.json","params":{"q":"EGFR","limit":5},"record_path":"targets","max_items":5}' \
  | python scripts/rest_request.py
# Then use the target ChEMBL ID from above:
echo '{"base_url":"https://www.ebi.ac.uk/chembl/api/data","path":"mechanism.json","params":{"target_chembl_id":"CHEMBL203","limit":20},"record_path":"mechanisms","max_items":30}' \
  | python scripts/rest_request.py
```

### Open Targets: NSCLC targets ranked by evidence
```bash
# opentargets-skill — disease search then associated targets
cd skills/opentargets-skill
echo '{"query":"query SearchDisease($q:String!){search(queryString:$q,entityNames:[\\"disease\\"]){hits{entity score object{...on Disease{id name}}}}}","variables":{"q":"non-small cell lung cancer"},"max_items":5}' \
  | python scripts/opentargets_graphql.py
# Then use the EFO ID from above (e.g., EFO_0003060):
echo '{"query":"query AssocTargets($id:String!,$size:Int){disease(efoId:$id){associatedTargets(page:{size:$size}){rows{target{id approvedSymbol} score}}}}","variables":{"id":"EFO_0003060","size":20},"max_items":20}' \
  | python scripts/opentargets_graphql.py
```

---

## Step 8: Literature Review

```bash
# ncbi-entrez-skill — PubMed search
cd skills/ncbi-entrez-skill
echo '{"endpoint":"esearch","params":{"db":"pubmed","term":"osimertinib[tiab] AND (resistance[tiab] OR mechanism[tiab]) AND (\"non-small cell lung cancer\"[MeSH] OR NSCLC[tiab]) AND 2024:2025[dp]","retmode":"json","retmax":20},"max_items":20}' \
  | python scripts/ncbi_entrez.py
```

For preprints (ahead of peer review):
```bash
# biorxiv-skill — medRxiv preprints
cd skills/biorxiv-skill
echo '{"base_url":"https://api.biorxiv.org","path":"details/medrxiv/2025-01-01/2025-06-09/0/json","record_path":"collection","max_items":10}' \
  | python scripts/rest_request.py
```

---

## Step 9: Non-US Regulatory (web_search fallback)

For regions without MCP coverage, use `web_search` or `web_fetch`:

| Region | Query pattern |
|--------|---------------|
| China (NMPA) | `site:nmpa.gov.cn "奥希替尼"` or `web_fetch https://www.nmpa.gov.cn/datasearch/...` |
| Japan (PMDA) | `site:pmda.go.jp osimertinib` or search PMDA approval DB in Japanese (オシメルチニブ) |
| EU (EMA EPAR) | `web_fetch https://www.ema.europa.eu/en/medicines/human/EPAR/tagrisso` |
| South Korea (MFDS) | `web_search site:mfds.go.kr osimertinib` |
| Australia (TGA) | `web_search site:tga.gov.au osimertinib ARTG` |

Always cross-check approval date against first-approval country to estimate regulatory lag.

---

## Synthesis Template

After running the above steps, structure the output as:

```
## [Drug Name] — [Indication] Intelligence Report

### Regulatory Status
| Region | Status | Date | Indications |
|--------|--------|------|-------------|
| US (FDA) | Approved | YYYY-MM | ... |
| EU (EMA) | Approved | YYYY-MM | ... |
| Japan (PMDA) | Approved | YYYY-MM | ... |
| China (NMPA) | Approved | YYYY-MM | ... |

### Clinical Trials (Active Phase 3)
| NCT ID | Title | Phase | Status | N | Primary Endpoint |
|--------|-------|-------|--------|---|-----------------|

### Safety Profile (Top FAERS signals)
| Reaction | Count | Serious % | Outcome |
|----------|-------|-----------|---------|

### Patent Landscape
| Patent | Expiry | Jurisdiction | Coverage |
|--------|--------|-------------|---------|

### Competitive Landscape (Same Class)
| Drug | Company | Phase | Mechanism difference |
|------|---------|-------|---------------------|

### Sources Used (with Tier)
- Tier 1: FDA label (Drugs@FDA, accessed YYYY-MM-DD)
- Tier 1: NMPA approval (nmpa.gov.cn, accessed YYYY-MM-DD)
- Tier 2: ClinicalTrials.gov (clinicaltrials-skill, accessed YYYY-MM-DD)
- Tier 3: PubMed (ncbi-entrez-skill, accessed YYYY-MM-DD)
```

# Pharma Intelligence Workflow — Complete Example

**Goal**: Full competitive intelligence report on a drug in a target indication across regions.
**Example**: Osimertinib (Tagrisso) in EGFR-mutant NSCLC

---

## Step 1: Identify the Drug

```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"chembl_search_molecules","arguments":{"query":"osimertinib","max_results":5}},"id":1}'
```

Note the ChEMBL ID (e.g., `CHEMBL3353410`) and max phase. Then get full details:

```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"chembl_get_molecule","arguments":{"molecule_id":"CHEMBL3353410"}},"id":2}'
```

Returns: ATC codes, approved indications, mechanism, black box warnings.

---

## Step 2: US Regulatory Status

### FDA label (approved indications + label date)
```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"openfda_search_drug_labels","arguments":{"drug_name":"osimertinib","section":"indications_and_usage"}},"id":3}'
```

### Orphan designation (if applicable)
```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"fda_orphan_search_designations","arguments":{"drug_name":"osimertinib","max_results":5}},"id":4}'
```

### Orange Book / exclusivity → use web_search for:
> `site:accessdata.fda.gov/scripts/cder/ob osimertinib`

---

## Step 3: US Clinical Trials (Phase 3 + Active)

> **Scope:** `ctg_search_studies` queries ClinicalTrials.gov, which is **US-only**. For CN/EU/JP/KR/AU trials, run the regional `web_fetch` calls in Step 9 in parallel.

```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"ctg_search_studies","arguments":{"condition":"non-small cell lung cancer","intervention":"osimertinib","phase":"PHASE3","max_results":20}},"id":5}'
```

Get full protocol for key trials:
```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"ctg_get_study","arguments":{"nct_id":"NCT02151981"}},"id":6}'
```

---

## Step 4: Safety Profile (FAERS)

```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"openfda_search_adverse_events","arguments":{"drug_name":"osimertinib","seriousness":"serious","limit":50}},"id":7}'
```

---

## Step 5: Patent / IP Landscape

Global patent search uses free web sources (no API key):

- Google Patents: `web_fetch https://patents.google.com/?q=osimertinib+EGFR+T790M`
- WIPO PATENTSCOPE: `web_fetch https://patentscope.wipo.int/search/en/result.jsf?query=osimertinib`
- Espacenet (EPO): `web_fetch https://worldwide.espacenet.com/patent/search?q=osimertinib` (use the "INPADOC patent family" view for cross-jurisdiction equivalents)

Structured US patents via MCP:

```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"uspto_ppubs_search_patents","arguments":{"query":"osimertinib EGFR inhibitor","max_results":20}},"id":8}'
```

For Orange Book expiry: `web_fetch https://www.accessdata.fda.gov/scripts/cder/ob`.

---

## Step 6: Competitive Landscape (Same Indication)

### All drugs approved/investigated for NSCLC
```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"chembl_find_drugs_by_indication","arguments":{"indication":"non-small cell lung cancer","max_results":50}},"id":10}'
```

### All active NSCLC trials (any intervention)
```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"ctg_search_studies","arguments":{"condition":"non-small cell lung cancer","recruitment_status":"RECRUITING","phase":"PHASE3","max_results":30}},"id":11}'
```

### Competitor SEC pipeline disclosures
```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"edgar_fulltext_search","arguments":{"query":"EGFR inhibitor NSCLC pipeline 2025","max_results":10}},"id":12}'
```

---

## Step 7: Target Biology (Mechanism Validation)

### Get EGFR gene info and cross-references
```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mygene_search_genes","arguments":{"query":"EGFR","max_results":3}},"id":13}'
```

### Find all drugs targeting EGFR
```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"chembl_find_drugs_by_target","arguments":{"target_name":"EGFR","include_all_mechanisms":true,"max_results":30}},"id":14}'
```

### OpenTargets: NSCLC targets ranked by evidence
```bash
# First get disease ID
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"opentargets_search","arguments":{"query":"non-small cell lung cancer","entity_type":"disease"}},"id":15}'

# Then get top targets (use MONDO ID from above)
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"opentargets_get_associations","arguments":{"disease_id":"MONDO_0005233","size":20}},"id":16}'
```

---

## Step 8: Literature Review

```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"pubmed_search_articles","arguments":{"query":"osimertinib resistance mechanisms 2024 2025","chemicals":["osimertinib"],"diseases":["non-small cell lung cancer"],"max_results":30}},"id":17}'
```

For preprints (ahead of peer review):
```bash
curl -X POST https://mcp.sciminer.tech/tools/unified/mcp \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"europepmc_search_preprints","arguments":{"query":"osimertinib EGFR 2025","max_results":10}},"id":18}'
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
- Tier 2: ClinicalTrials.gov (ctg_search_studies, accessed YYYY-MM-DD)
- Tier 3: PubMed (pubmed_search_articles, accessed YYYY-MM-DD)
```

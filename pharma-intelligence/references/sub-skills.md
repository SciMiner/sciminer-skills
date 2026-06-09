# Sub-Skills Quick Reference

All database work in the pharma-intelligence skill is performed through sub-skills
bundled locally under `pharma-intelligence/skills/`.

Read the target sub-skill's `SKILL.md` before invoking it, then run its bundled script
from the sub-skill's directory.

---

## Task-to-Sub-Skill Mapping

### Drug / Compound Lookup

| Task | Sub-skill | Script / Endpoint |
|------|-----------|-------------------|
| Search compound by name / CAS / SMILES | `pubchem-pug-skill` | `compound/name/<name>/property/.../JSON` |
| Full compound properties by CID | `pubchem-pug-skill` | `compound/cid/<cid>/property/.../JSON` |
| Search molecule by name / synonym | `chembl-skill` | `molecule/search.json?q=<name>` |
| Full molecule record by ChEMBL ID | `chembl-skill` | `molecule/<id>.json` |
| All drugs approved / investigated for a disease | `chembl-skill` | `drug_indication.json?efo_term=<term>` |
| All drugs targeting a gene / protein | `chembl-skill` | `target/search.json?q=<gene>` → `mechanism.json?target_chembl_id=...` |
| Mechanism of action for a molecule | `chembl-skill` | `mechanism.json?molecule_chembl_id=<id>` |
| Approved + investigational indications for a drug | `chembl-skill` | `drug_indication.json?molecule_chembl_id=<id>` |
| Bioactivity (IC50 / Kd / EC50) | `chembl-skill` | `activity.json?molecule_chembl_id=<id>` or `activity.json?target_chembl_id=<id>` |
| Chemical ontology / structure metadata | `chebi-skill` | ChEBI 2.0 API search and compound endpoints |

### US Regulatory (web_fetch — no sub-skill)

| Task | Direct URL |
|------|------------|
| FDA drug labels (package inserts) | `https://api.fda.gov/drug/label.json?search=openfda.brand_name:<name>` |
| Full label by set_id | `https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/<set_id>.json` |
| FAERS adverse event search | `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:<name>&limit=50` |
| DailyMed label search | `https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=<name>` |
| Orphan drug designations | `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/` |
| Orange Book patent + exclusivity | `https://www.accessdata.fda.gov/scripts/cder/ob/` |

### Clinical Trials

| Task | Sub-skill | Execution pattern |
|------|-----------|-------------------|
| ClinicalTrials.gov study search | `clinicaltrials-skill` | `action=studies`, `params.query.cond`, `params.query.intr`, `params.filter.overallStatus`, `params.filter.phase` |
| Full trial protocol by NCT ID | `clinicaltrials-skill` | `action=studies`, `params.query.id=NCT...` |
| NCI oncology-specific trial search | `web_fetch` | `https://clinicaltrialsapi.cancer.gov/api/v2/trials` (optional API key) |

### Patent / IP (web_fetch — no sub-skill)

| Source | URL |
|--------|-----|
| Google Patents (full-text, all jurisdictions) | `https://patents.google.com/?q=<query>` |
| WIPO PATENTSCOPE (PCT + national) | `https://patentscope.wipo.int/search/en/result.jsf?query=<query>` |
| EPO Espacenet (European + family view) | `https://worldwide.espacenet.com/patent/search?q=<query>` |
| USPTO granted patents | `https://ppubs.uspto.gov/pubwebapp/external.html` |

### Financial / Competitive Intelligence (web_fetch — no sub-skill)

| Task | URL |
|------|-----|
| EDGAR company search | `https://efts.sec.gov/LATEST/search-index?q=<company>` |
| EDGAR full-text filings search | `https://efts.sec.gov/LATEST/search-index?q=<query>&dateRange=custom&startdt=<YYYY-MM-DD>` |
| 10-K / 10-Q / 8-K by CIK | `https://data.sec.gov/submissions/CIK<cik>.json` |

### Literature

| Task | Sub-skill | Execution pattern |
|------|-----------|-------------------|
| PubMed article search | `ncbi-entrez-skill` | `endpoint=esearch`, `db=pubmed`, MeSH terms for precision |
| PubMed article fetch (abstract / full text) | `ncbi-entrez-skill` | `endpoint=efetch`, `db=pubmed`, `id=<pmid>` |
| PMC Open Access availability | `ncbi-pmc-skill` | article / file availability metadata |
| bioRxiv / medRxiv preprints | `biorxiv-skill` | `details/<server>/<start>/<end>/0/json` or by DOI |
| Europe PMC (broader: preprints + grants + non-MEDLINE) | `web_fetch` | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<query>&resultType=lite&format=json` |

### Target / Biology

| Task | Sub-skill | Execution pattern |
|------|-----------|-------------------|
| Resolve disease to MONDO / EFO ID | `opentargets-skill` or `efo-ontology-skill` | GraphQL `search` query or OLS4 search endpoint |
| Targets ranked by evidence score for a disease | `opentargets-skill` | GraphQL `associatedTargets` on disease EFO ID |
| Target–disease evidence breakdown | `opentargets-skill` | GraphQL `evidences` query with target + disease IDs |
| Protein function, domains, and druggability | `uniprot-skill` | `uniprotkb/search?query=gene:<symbol> AND organism_id:9606` |
| Pathway context | `reactome-skill` | ContentService `search`, `pathways/low/diagram/entity/<id>` |
| Disease-specific pathways | `reactome-skill` | ContentService `diseases/<id>/pathways` |
| GWAS-linked variants for a disease | `gwas-catalog-skill` | `associations?efo_trait=<term>` |
| Gene symbol lookup + cross-references | `ncbi-clinicaltables-skill` or `ensembl-skill` | Gene autocomplete or Ensembl lookup |
| Variant effects, ClinVar significance, gnomAD frequency | `clinvar-variation-skill` + `gnomad-graphql-skill` | ClinVar VCV/RCV lookup; gnomAD variant query |
| Cross-database ID normalization | `efo-ontology-skill`, `ensembl-skill`, `uniprot-skill` | OLS4 search, Ensembl xrefs, UniProt ID mapping |
| Mendelian disease basis | `web_fetch` | `https://api.omim.org/api/entry/search?search=<term>&apiKey=<key>` |
| Protein–protein interaction network | `string-skill` | STRING API network and enrichment endpoints |
| GO term annotations | `quickgo-skill` | QuickGO annotations and ontology endpoints |
| Biochemical reaction context | `rhea-skill` | Rhea reaction search |
| RNA entry lookup | `rnacentral-skill` | RNAcentral API |

---

## Execution Pattern

Each sub-skill is invoked by piping a JSON object to its Python script.
Run commands from inside the sub-skill's directory.

```bash
# ChEMBL — molecule search
cd skills/chembl-skill
echo '{"base_url":"https://www.ebi.ac.uk/chembl/api/data","path":"molecule/search.json","params":{"q":"osimertinib","limit":5},"record_path":"molecules","max_items":5}' \
  | python scripts/rest_request.py

# ClinicalTrials.gov — study search
cd skills/clinicaltrials-skill
echo '{"action":"studies","params":{"query.cond":"non-small cell lung cancer","query.intr":"osimertinib","filter.overallStatus":"RECRUITING","pageSize":10},"max_items":10,"max_pages":1}' \
  | python scripts/clinicaltrials_client.py

# Open Targets — disease search
cd skills/opentargets-skill
echo '{"query":"query SearchDisease($q:String!){search(queryString:$q,entityNames:[\"disease\"]){hits{entity score object{...on Disease{id name}}}}}","variables":{"q":"non-small cell lung cancer"},"max_items":5}' \
  | python scripts/opentargets_graphql.py

# PubMed — article search
cd skills/ncbi-entrez-skill
echo '{"endpoint":"esearch","params":{"db":"pubmed","term":"osimertinib resistance mechanisms","retmode":"json","retmax":10},"max_items":10}' \
  | python scripts/ncbi_entrez.py

# UniProt — protein search
cd skills/uniprot-skill
echo '{"base_url":"https://rest.uniprot.org","path":"uniprotkb/search","params":{"query":"gene:EGFR AND organism_id:9606 AND reviewed:true","fields":"accession,gene_names,protein_name","size":5,"format":"json"},"record_path":"results","max_items":5}' \
  | python scripts/rest_request.py

# GWAS Catalog — associations for a disease
cd skills/gwas-catalog-skill
echo '{"base_url":"https://www.ebi.ac.uk/gwas/rest/api/v2","path":"associations","params":{"efo_trait":"lung cancer","size":10},"record_path":"_embedded.associations","max_items":10}' \
  | python scripts/rest_request.py

# bioRxiv — recent preprints
cd skills/biorxiv-skill
echo '{"base_url":"https://api.biorxiv.org","path":"details/biorxiv/2025-01-01/2025-06-09/0/json","record_path":"collection","max_items":10}' \
  | python scripts/rest_request.py
```

---

## Notes

- For openFDA (labels, adverse events), DailyMed, EDGAR, OMIM, patent databases, and non-US regulatory portals (NMPA, EMA, PMDA, MFDS, TGA), use `web_fetch` directly — no sub-skill script is available.
- For cross-database ID conversion, chain `efo-ontology-skill` (disease), `ncbi-clinicaltables-skill` or `ensembl-skill` (gene), and `uniprot-skill` (protein) instead of a single normalization call.
- All sub-skill scripts return compact JSON by default. Set `save_raw=true` in the input JSON to capture full API payloads.

---
name: life-science-database-query
description: >
  General life-sciences research copilot bundling 50 modular sub-skills across
  human genetics, variant interpretation, functional genomics, expression,
  pathway biology, protein structure, chemistry, clinical evidence, literature,
  and public study discovery. Use when a user asks any life-sciences question
  that may require one or more public databases. The research-router-skill is
  the default entry point for broad or ambiguous requests; individual sub-skills
  can be invoked directly for narrow, single-source lookups.
---

# Life-Science Database Query Skill

This skill packages a broad set of modular sub-skills that can be composed to answer questions across every major area of life-sciences research. Each sub-skill maps to one or more public databases and carries its own operating rules and execution scripts.

## When To Use This Skill

- The user asks a broad life-sciences question ("what is known about …", "tell me about this gene/variant/compound …")
- The user wants a specific public-database lookup (gnomAD, UniProt, ChEMBL, ClinicalTrials.gov, etc.)
- The user needs multi-source evidence synthesis (genetics + expression, structure + chemistry, clinical + literature)
- The user wants locus-to-gene prioritization, PheWAS follow-up, or multi-cohort replication
- The user wants to discover public datasets or preprints for a research topic

## Entry Point

For broad or ambiguous requests, invoke `research-router-skill` first. It classifies the request, normalizes entities, selects the minimum useful set of downstream sub-skills, optionally parallelizes independent evidence lanes using subagents, and synthesizes the final answer.

Use a specific sub-skill directly only when the request is clearly scoped to a single source.

## Sub-Skill Directory

Sub-skill files live at `skills/<sub-skill-name>/SKILL.md`. Read the relevant SKILL.md before invoking any sub-skill.

### Orchestration

| Sub-skill | Description |
|---|---|
| `research-router-skill` | Route broad or ambiguous life-sciences requests to the right sub-skills, normalize entities, optionally parallelize independent evidence lanes with subagents, and synthesize a concise evidence-backed answer. |

### Human Genetics And Variant Evidence

| Sub-skill | Description |
|---|---|
| `opentargets-skill` | Open Targets Platform GraphQL: target, disease, drug, variant, study, and associated-disease datasource heatmap data. |
| `gwas-catalog-skill` | GWAS Catalog REST API v2: studies, associations, SNPs, EFO traits, genes, publications, and loci. |
| `clinvar-variation-skill` | ClinVar Clinical Tables and NCBI Variation: search, VCV, RCV, SCV, and RefSNP lookups. |
| `gnomad-graphql-skill` | gnomAD GraphQL: allele frequency, gene constraint, and variant-context queries. |
| `ensembl-skill` | Ensembl REST API: lookup, overlap, cross-reference, and variation endpoints. |
| `eva-skill` | European Variation Archive REST: species metadata and archived variant lookups. |
| `epigraphdb-skill` | EpiGraphDB API: ontology, literature, Mendelian randomisation, gene-drug, and support-path evidence. |
| `genebass-gene-burden-skill` | Genebass gene-burden PheWAS for one Ensembl gene ID and one burden set. |
| `gtex-eqtl-skill` | GTEx v2 API: single-tissue eQTL associations from rsID, GRCh37, or GRCh38 input. |
| `eqtl-catalogue-skill` | eQTL Catalogue API: association retrieval and documented metadata endpoints. |
| `locus-to-gene-mapper-skill` | Multi-skill locus-to-gene prioritization chain (EFO → GWAS → coordinates → Open Targets L2G/coloc → eQTL → burden/coding context). |
| `finngen-phewas-skill` | FinnGen PheWAS: single-variant association summaries (GRCh38 query). |
| `ukb-topmed-phewas-skill` | UKB-TOPMed PheWAS: single-variant association summaries (GRCh38 query). |
| `biobankjapan-phewas-skill` | BioBank Japan PheWAS: single-variant association summaries (GRCh37 query). |
| `tpmi-phewas-skill` | TPMI PheWAS: single-variant association summaries (GRCh38 query). |

### Expression, Cell Context, And Functional Genomics

| Sub-skill | Description |
|---|---|
| `bgee-skill` | Bgee SPARQL: healthy wild-type expression metadata with ontology-aware lookup patterns. |
| `human-protein-atlas-skill` | Human Protein Atlas: gene JSON, search downloads, and tissue or cell-line lookups. |
| `cellxgene-skill` | CELLxGENE Discover API: public single-cell collection and dataset metadata. |
| `encode-skill` | ENCODE REST API: object lookups, portal-style search, and metadata retrieval. |
| `rnacentral-skill` | RNAcentral API: RNA entry browsing, single-entry lookup, and cross-reference retrieval. |

### Protein, Structure, Pathway, And Functional Biology

| Sub-skill | Description |
|---|---|
| `alphafold-skill` | AlphaFold Protein Structure Database API: prediction, UniProt summary, sequence summary, and annotation lookups. |
| `rcsb-pdb-skill` | RCSB PDB: core metadata, Search API queries, and FASTA downloads. |
| `uniprot-skill` | UniProt REST API: UniProtKB, UniRef, UniParc, and FASTA stream endpoints. |
| `string-skill` | STRING API: network, interaction-partner, and enrichment endpoints. |
| `quickgo-skill` | QuickGO: GO terms, annotations, and ontology traversal. |
| `reactome-skill` | Reactome ContentService: pathway, event, participant, search, and diagram data. |
| `rhea-skill` | Rhea: biochemical reaction search for reactions and reaction IDs. |

### Chemistry, Metabolites, And Pharmacology

| Sub-skill | Description |
|---|---|
| `bindingdb-skill` | BindingDB REST API: ligand-target binding lookups by PDB, UniProt, or similarity search. |
| `chembl-skill` | ChEMBL API: activity, molecule, target, mechanism, and text-search endpoints. |
| `pubchem-pug-skill` | PubChem PUG REST: compound properties, descriptions, assay summaries, and substance metadata. |
| `chebi-skill` | ChEBI 2.0 API: chemical search, compound lookup, ontology traversal, and structure metadata. |
| `pharmgkb-skill` | PharmGKB API: genes, variants, clinical annotations, dosing guidelines, and search. |
| `hmdb-skill` | HMDB: metabolite, protein, disease, and pathway search. |

### Clinical, Translational, And Disease Evidence

| Sub-skill | Description |
|---|---|
| `clinicaltrials-skill` | ClinicalTrials.gov API v2: study search, metadata, enums, search areas, and field statistics. |
| `cbioportal-skill` | cBioPortal API: studies, molecular profiles, mutations, clinical data, and samples. |
| `civic-skill` | CIViC GraphQL: cancer variant interpretation schema inspection and targeted evidence retrieval. |
| `ipd-skill` | IPD REST: HLA allele and cell-level metadata using the public IPD query API. |

### Literature, Search, And Public Study Discovery

| Sub-skill | Description |
|---|---|
| `ncbi-entrez-skill` | NCBI Entrez E-Utilities: PubMed, Gene, Protein, Nucleotide, PMC metadata, and GEO metadata workflows. |
| `ncbi-pmc-skill` | NCBI PMC Open Access: article and file availability metadata. |
| `biorxiv-skill` | bioRxiv and medRxiv API: preprint details, publication linkage, and DOI lookups. |
| `biostudies-arrayexpress-skill` | BioStudies and ArrayExpress API: free-text search and accession-based study retrieval. |
| `ncbi-datasets-skill` | NCBI Datasets v2: assembly, genome, taxonomy, and related metadata endpoints. |
| `ncbi-blast-skill` | NCBI BLAST Common URL API: submit, poll, and summarize nucleotide or protein BLAST jobs. |
| `ncbi-clinicaltables-skill` | Clinical Tables NCBI Gene: human gene lookup, pagination, and field selection. |

### Multi-Omics, Proteomics, And Specialized Data Sources

| Sub-skill | Description |
|---|---|
| `pride-skill` | PRIDE Archive API: proteomics project discovery and project-level metadata. |
| `proteomexchange-skill` | ProteomeXchange PROXI: datasets, libraries, peptidoforms, proteins, PSMs, spectra, and USI examples. |
| `metabolights-skill` | MetaboLights: study discovery and study-level metabolomics metadata. |
| `mgnify-skill` | MGnify API: microbiome studies, samples, and biome metadata. |
| `efo-ontology-skill` | EFO OLS4: search, term lookup, children, and descendants for ontology resolution. |

## Routing Heuristics

Choose the minimum sub-skills needed to answer the question.

| Research objective | Recommended sub-skills |
|---|---|
| Target or disease background | `opentargets-skill`, `gwas-catalog-skill`, `gtex-eqtl-skill`, `human-protein-atlas-skill` |
| Variant interpretation | `clinvar-variation-skill`, `gnomad-graphql-skill`, `ensembl-skill`, one or more PheWAS skills |
| Locus-to-gene prioritization | `locus-to-gene-mapper-skill` (or its component sub-skills for custom workflows) |
| Multi-cohort PheWAS replication | `finngen-phewas-skill`, `ukb-topmed-phewas-skill`, `biobankjapan-phewas-skill`, `tpmi-phewas-skill` |
| Expression and tissue context | `bgee-skill`, `human-protein-atlas-skill`, `cellxgene-skill`, `gtex-eqtl-skill` |
| Protein structure and function | `alphafold-skill`, `rcsb-pdb-skill`, `uniprot-skill`, `reactome-skill` |
| Chemistry and pharmacology | `chembl-skill`, `bindingdb-skill`, `pubchem-pug-skill`, `pharmgkb-skill` |
| Entity normalization | `efo-ontology-skill`, `ncbi-clinicaltables-skill`, `ensembl-skill`, `uniprot-skill` |
| Clinical and cancer evidence | `clinicaltrials-skill`, `cbioportal-skill`, `civic-skill`, `opentargets-skill` |
| Literature and preprints | `ncbi-entrez-skill`, `ncbi-pmc-skill`, `biorxiv-skill` |
| Public dataset discovery | `biostudies-arrayexpress-skill`, `ncbi-datasets-skill`, `pride-skill`, `metabolights-skill`, `mgnify-skill` |
| Sequence similarity search | `ncbi-blast-skill` |
| Pathway and reaction context | `reactome-skill`, `rhea-skill`, `quickgo-skill`, `string-skill` |
| Microbiome context | `mgnify-skill` |
| Metabolomics context | `metabolights-skill`, `hmdb-skill` |
| Proteomics context | `pride-skill`, `proteomexchange-skill` |

## Subagent Guidance

When subagents are available, use them as bounded retrieval and analysis accelerators for independent evidence lanes.

Good candidates for parallelization:
- genetics versus expression evidence for the same gene or variant
- structure versus chemistry for the same target
- literature versus clinical evidence for the same disease
- multiple PheWAS cohorts for the same variant

Keep the coordinating agent responsible for:
- interpreting the user request and defining scope
- resolving identifiers and canonical entities
- reconciling conflicting evidence across sources
- writing the final synthesis

Each subagent should receive a bounded objective and return concise findings, caveats, sources used, and any artifact paths.

## Evidence Quality Notes

- Cross-check orthogonal evidence types rather than over-indexing on one source.
- Call out ancestry limitations, tissue specificity, study design caveats, and evidence gaps explicitly.
- Treat heatmap breadth (Open Targets datasource scores) as evidence-source context, not proof of causality or direction of effect.
- For variant lookups, verify coordinate build (GRCh37 vs GRCh38) before querying cohort-specific PheWAS skills.

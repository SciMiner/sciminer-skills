---
name: network-pharmacology
description: Build evidence-graded compound–target–disease network-pharmacology hypotheses for natural products, herbal medicines, formulae, and small molecules using live SciMiner tools plus public life-science evidence. Use when an agent must curate compounds, predict or verify targets, prioritize disease-relevant targets, assess ADMET or off-target risk, run docking as supporting evidence, create interactive network visualizations, or produce reproducible network-pharmacology reports without R.
required_environment_variables:
    - SCIMINER_API_KEY
---

# SciMiner Network Pharmacology

Build a transparent hypothesis, not a mechanism claim. Keep experimental, curated-database, predicted, literature, and computational evidence separate throughout the workflow.

## Prerequisites and boundaries

- `SCIMINER_API_KEY` must be injected by the SciMiner gateway before skill execution. Use it directly as the `X-Auth-Token` for SciMiner tool calls; never print, copy, or persist the key.
- If `SCIMINER_API_KEY` is unavailable at runtime, stop and report that the gateway did not inject the required credential. Do not attempt to derive or locate the API key through other means.
- Resolve every SciMiner capability from the live tool-doc index at `https://sciminer.tech/tool_api_files/` and read the selected `*_api_doc.md` immediately before invocation. That document is authoritative for provider/tool names, parameters, upload behavior, polling, and results.
- Return each successful task's `share_url`. Preserve its `task_id` and source-document URL in the project manifest.
- Do not use a target prediction, a network centrality score, enrichment, or docking score as proof of binding, efficacy, synergy, causality, or clinical benefit.
- Do not call a tool with guessed parameters. Ask for missing required inputs or omit the optional analysis.

## Inputs and project contract

Collect or create `project_manifest.json` before analysis. Record the project question, date, analyst, species, disease term and ontology ID, compound source, structures, access dates, database/tool versions, thresholds, and every exclusion.

Accept one of these input shapes:

1. A compound table with `compound_id`, `name`, and SMILES/InChIKey; optionally source herb, plant part, preparation, measured abundance, and exposure evidence.
2. A formula/herb list. First request or retrieve a traceable compound table; never invent constituents from an herb name.
3. A small molecule and disease/phenotype. Require a canonical disease term and species before disease-target analysis.
4. User-provided targets, PPI edges, omics results, or docking structures. Preserve their source and identifier namespace.

Read [evidence-model.md](references/evidence-model.md) before scoring, filtering, ranking, or interpreting results. Read [sciminer-tool-routing.md](references/sciminer-tool-routing.md) before selecting a SciMiner capability.

## Workflow

### 1. Resolve entities and scope

- Canonicalize compounds by structure, not display name. Preserve original names and aliases.
- Record herb Latin name, Chinese/common name, medicinal part, preparation, and formula role separately; do not merge them into a single label.
- Normalize genes and proteins to one primary namespace and report unmapped or one-to-many mappings.
- Resolve the disease to an ontology term. State whether the question concerns therapeutic mechanism, repurposing, toxicity, or a specific phenotype.
- Define a biologically defensible universe before overlap or enrichment work; for an omics study, it is normally the tested/detectable genes, not the full genome by default.

### 2. Build the component evidence table

- Assign component evidence tier: `measured` > `curated/literature` > `database-listed` > `in-silico candidate`.
- Use SciMiner tools for structure conversion, Lipinski/PAINS checks, ADMET, descriptors, or pKa only when they answer the study question. Do not apply universal OB/DL cutoffs mechanically.
- Keep rejected compounds and the reason in `component_exclusions.csv`.
- For a formula, retain herb-to-compound provenance so that apparent multi-herb convergence can be inspected.

### 3. Acquire and grade target evidence

- Prefer quantitative bioactivity or curated mechanism evidence. Use target prediction only as a hypothesis-generating lane.
- Use the live SciMiner target-prediction documentation for each compound. Store input structure, returned rank/score, model name, task ID, and share URL.
- Use a separate SciMiner off-target analysis for safety or promiscuity questions; do not present its result as disease efficacy evidence.
- For disease relevance, use independent genetics, functional, expression, pathway, clinical, and literature sources where available. If the SciMiner Life-Science Database Query skill is installed, route broad database retrieval through its minimum relevant sub-skills; otherwise document the public sources actually used.
- Create `target_evidence.csv` with one row per compound–target–evidence record, not one merged opaque score.

### 4. Construct and analyze the evidence network

- Build typed edges: `herb→compound`, `compound→target`, `target→disease`, `target↔target`, `target→pathway`, and `compound→adverse-effect` when available.
- Attach `evidence_tier`, `evidence_type`, `source`, `access_date`, `score_or_value`, and `direction` to every eligible edge. Use `unknown` rather than inferring activation or inhibition.
- Report graph size, isolated nodes, connected components, source composition, and confidence-filter sensitivity before selecting hubs or modules.
- Treat frequent network hubs (for example, TP53, AKT1, TNF, IL6) as generic candidates until disease relevance, tissue/cell context, and compound evidence justify their prioritization.
- Use [render_network_report.py](scripts/render_network_report.py) to make a standalone, interactive HTML report and a machine-readable JSON network. Supply node and edge tables rather than hand-drawing a network.

### 5. Interpret pathways and biological context

- Perform enrichment on the declared foreground against the declared background and report method, multiple-testing adjustment, annotation release/date, and gene-ID conversion losses.
- Prefer disease-relevant modules and directional evidence over long lists of generic GO terms. Explain whether each proposed effect is direct, indirect, predicted, or unknown.
- Cross-check leading targets against tissue/cell context and any supplied transcriptomic/proteomic evidence. Do not conflate disease-associated expression with a causal drug target.

### 6. Add computational support only when justified

- Run docking only for a short, pre-specified compound–target set with target evidence, a credible structure and binding-site rationale.
- Use live SciMiner documentation for tools such as AutoDock Vina, DiffDock, or scoring tools. Record receptor structure ID, chain, ligand/protonation state, search box/site, tool/model, and task URL.
- Inspect pose plausibility and known activity where possible. Label docking as `supporting computational evidence`; never use it as standalone validation.

### 7. Report conclusions, negative findings, and validation

Deliver `project_manifest.json`, `component_evidence.csv`, `target_evidence.csv`, `nodes.csv`, `edges.csv`, `network.json`, `network_report.html`, and a concise narrative.

State separately:

- robust observations;
- ranked but unverified hypotheses;
- contradictory or missing evidence;
- negative results, including no credible target, disconnected network, non-significant enrichment, or failed docking;
- the smallest discriminating experiment for each leading hypothesis (for example, target engagement, pathway readout, gene perturbation, or exposure assay).

## Minimum output schema

Use these fields unless the source lacks a value:

```text
component_evidence.csv: compound_id,name,structure,source_herb,component_tier,source,access_date,decision,reason
target_evidence.csv: compound_id,target_id,target_symbol,evidence_tier,evidence_type,score_or_value,direction,source,access_date,task_id,share_url
nodes.csv: id,label,type,evidence_tier,score,description
edges.csv: source,target,evidence_type,evidence_tier,weight,direction,source_ref
```

Use `type` values such as `herb`, `compound`, `target`, `disease`, `pathway`, and `adverse_effect`. Do not omit rows merely because their confidence is low; encode the confidence and filter transparently in views.

## Visual and writing rules

- Use the interactive report for exploration and export a filtered, legible static figure for a manuscript. Never use a dense all-entity hairball as the sole figure.
- Use color for entity type and line style/opacity for evidence tier; include a legend and source counts.
- Make titles claim only the evidence level, for example: “Predicted and curated target network for …”, not “Mechanism of …”.
- Cite database/tool documents and access dates next to conclusions. Include SciMiner share URLs for every successful task.

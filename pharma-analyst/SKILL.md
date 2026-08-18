---
name: pharma-analyst
description: Produce current, evidence-graded pharmaceutical and biotechnology analysis at the company, platform, pipeline, asset, indication, trial, competitive-landscape, catalyst, risk, and valuation levels. Use for biopharma diligence, investment-research-style reports, pipeline reviews, target or mechanism assessments, clinical-data interpretation, competitor comparisons, deal or financing analysis, catalyst calendars, risk-adjusted valuation, and updates to an existing pharma report or PDF. Supports public and private companies and preclinical through commercial-stage assets. Do not use for patient-specific medical advice.
---

# Pharma Analyst

Build decision-useful biopharma analysis that keeps verified facts, company claims, analyst interpretation, and speculation visibly separate. Default to the user's language and requested depth.

## Core contract

- Set an explicit data cutoff and report date. Treat pipeline status, trials, regulatory events, financing, management, market data, and competitors as time-sensitive.
- Browse live sources unless the user explicitly limits analysis to supplied materials. Prefer primary sources and cite the exact page supporting each material claim.
- Distinguish `Verified fact`, `Company claim`, `Analyst inference`, `Scenario assumption`, and `Unknown`.
- Never silently upgrade preclinical evidence, modeled projections, conference abstracts, or press releases into clinical proof.
- Use calibrated language: `supports`, `is consistent with`, `suggests`, or `remains unproven`; reserve `demonstrates` for evidence that warrants it.
- Surface contradictory sources, stale records, missing denominators, unreported endpoints, protocol changes, and data-cutoff mismatches.
- Do not present research as medical, legal, patent, or personalized investment advice.

## Select the deliverable

Choose the smallest mode that answers the request:

1. **Company snapshot** - thesis, financing, leadership, platform, pipeline, catalysts, risks.
2. **Deep-dive report** - full company, platform, asset, clinical, competitive, strategic, and valuation analysis.
3. **Asset or mechanism review** - target biology, modality, translational chain, trial design, results, differentiation.
4. **Competitive landscape** - mechanism- and indication-level comparator set with normalized stages and readouts.
5. **Catalyst or update note** - what changed, why it matters, thesis impact, next checkpoints.
6. **Valuation** - risk-adjusted NPV or scenario analysis with transparent assumptions and sensitivities.

For full reports, read [references/research-framework.md](references/research-framework.md) before research. Read [references/report-template.md](references/report-template.md) before drafting. For a narrow task, load only the relevant sections.

## Workflow

### 1. Frame the question

Define the subject, intended decision, audience, geography, currency, cutoff date, deliverable, depth, and whether valuation is in scope. State reasonable assumptions when details are absent.

### 2. Build a source plan

Start with official registries, regulators, labels, filings, peer-reviewed papers, congress materials, company disclosures, and patent databases. Use reputable secondary sources for context or discovery, not as the sole support for a critical claim when a primary source exists.

For every material fact, capture the source, publication date, underlying data cutoff, evidence type, and confidence. Resolve discrepancies by checking identifiers such as NCT/CTIS numbers, molecule aliases, sponsor names, trial versions, and patent families.

### 3. Create a fact ledger before forming the thesis

Maintain a compact working table:

| Claim | Status | Evidence grade | Source/date | Conflict or caveat |
|---|---|---|---|---|
| Exact claim | Verified / company claim / inference / assumption / unknown | A-E | Direct citation | Limitation |

Use this ledger to prevent circular sourcing and unsupported synthesis. Do not expose the full ledger unless useful, but preserve its distinctions in the output.

### 4. Analyze in modules

Use only modules relevant to the request:

- Company, leadership, capitalization, partnerships, runway, and governance
- Platform architecture, validation, reproducibility, throughput, and platform-to-pipeline transfer
- Pipeline normalization by asset, modality, target, indication, sponsor, geography, and true stage
- Biology and mechanism: human genetics, causal rationale, target engagement, translational biomarkers, safety liabilities
- Preclinical evidence: model relevance, dose/exposure, controls, replication, and clinical translatability
- Clinical evidence: population, design, endpoints, estimand, multiplicity, missing data, effect size, durability, safety, and benchmark relevance
- Regulatory, CMC, manufacturability, delivery, immunogenicity, and lifecycle considerations
- Competitive landscape and standard of care
- Market, access, pricing, adoption, and commercial execution
- Intellectual-property observations, clearly separated from legal FTO conclusions
- Catalysts, risks, scenario valuation, and thesis-changing evidence

### 5. Apply evidence grades

- **A - Confirmed primary evidence:** regulator, official registry, audited filing, label, full peer-reviewed result, or direct protocol/result record.
- **B - Strong primary disclosure:** detailed congress presentation/poster or company disclosure with methods and quantitative data.
- **C - Preliminary or partial evidence:** abstract, press release, interim subset, retrospective analysis, or incomplete dataset.
- **D - Indirect evidence:** competitor analogue, animal/in-vitro result, model-based extrapolation, or reputable secondary reporting.
- **E - Speculative:** unverified report, strategic inference, patent inference without claim review, or unsupported scenario.

Grade the claim, not the source brand. A company filing can confirm cash but not independently validate efficacy.

### 6. Synthesize for decisions

Lead with the conclusion and the few variables that drive it. For each asset, connect:

`biology -> molecule design -> translational evidence -> clinical test -> competitive benchmark -> commercial value -> remaining risk`

Explain what would confirm, weaken, or falsify the thesis. Use ranges and sensitivities instead of false precision.

## Output rules

- Put an `As of` date near the top.
- Give inline citations or footnotes close to the supported claims; include direct links when available.
- Normalize currencies, units, stages, endpoint names, and trial status before comparison.
- Show denominators, doses, follow-up, confidence intervals, and discontinuations when available.
- Label cross-trial comparisons as non-randomized and discuss population, endpoint, timing, and background-therapy differences.
- Treat absence of disclosed evidence as `not found` or `not disclosed`, not proof of absence.
- Pair every opportunity with the evidence needed to realize it and every risk with a monitorable signpost.
- End a deep dive with sources, limitations, and a concise monitoring plan.

## Quality gate

Before delivery, verify:

- Every stage, trial status, approval, readout, financing, and leadership claim is current to the cutoff.
- Asset aliases and trial identifiers map correctly.
- Numerical claims reconcile with the cited source and use the correct population and time point.
- Facts, company claims, inferences, and assumptions are visually distinguishable.
- The report states missing data and material contradictory evidence.
- No preclinical result is phrased as expected human efficacy or safety.
- Valuation assumptions are traceable and sensitivity-tested.
- The conclusion can change if the stated falsifiers occur.


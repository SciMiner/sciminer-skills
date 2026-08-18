# Pharma research framework

Use this reference for a deep-dive or when a narrow request reaches one of these modules.

## Contents

1. Research sequence
2. Source hierarchy
3. Company and financing
4. Platform assessment
5. Asset and pipeline assessment
6. Clinical-data interpretation
7. Competition and market
8. Regulatory, CMC, and IP
9. Valuation
10. Catalysts and risks

## 1. Research sequence

1. Fix the subject, aliases, jurisdiction, cutoff date, and decision question.
2. Map assets to targets, modalities, indications, trial identifiers, and sponsors.
3. Establish the latest verified stage from registries plus sponsor disclosures; note discrepancies.
4. Build the biology-to-commercial evidence chain for each material asset.
5. Construct comparators by mechanism, indication, treatment line, modality, and stage.
6. Identify value-inflecting catalysts and failure modes.
7. Value only after the evidence and risk map is complete.
8. Draft from the fact ledger; then audit citations, dates, and inference labels.

## 2. Source hierarchy

Prefer the closest primary record:

| Question | Preferred sources | Common trap |
|---|---|---|
| Trial status/design | ClinicalTrials.gov, CTIS, WHO ICTRP, regulator records, protocol/SAP | Treating sponsor wording as registry-confirmed |
| Approval/label | FDA, EMA, NMPA, PMDA and official label/review documents | Using news coverage for exact indication or date |
| Efficacy/safety | Full paper, regulator review, detailed congress deck/poster | Quoting only the press-release headline |
| Financials/runway | SEC/exchange filings, audited reports, financing documents | Confusing gross proceeds with cash available |
| Pipeline/stage | Registry plus dated company pipeline page/deck | Carrying stale stages forward |
| Patents | USPTO, EPO/Espacenet, WIPO, national registers | Inferring freedom to operate from titles/abstracts |
| Market/standard of care | Labels, guidelines, payer documents, epidemiology studies | Using undated market-size aggregators |

Record both publication date and underlying data cutoff. Search asset aliases, former sponsors, generic names, development codes, target synonyms, and acquired-company names.

## 3. Company and financing

Assess:

- Founding, headquarters, ownership, employee scale, governance, and leadership turnover
- Founder and executive track records without treating prior exits as proof of future success
- Financing rounds, gross proceeds, cash, debt, burn, committed milestones, and estimated runway
- Investor and strategic-partner signals; label acquisition-interest claims as inference unless directly disclosed
- Partnerships: rights, territory, economics, opt-ins, milestones, cost sharing, and change-of-control terms when known
- For private companies, state the absence of audited public financials and avoid synthetic precision

## 4. Platform assessment

Separate a platform narrative from platform validation.

Evaluate:

- Inputs, models, wet-lab loop, structural biology, screening, protein engineering, and translational systems
- Prospective versus retrospective validation; external versus internal datasets
- Hit rate, cycle time, property improvements, replication, negative results, and disclosed baselines
- Ability to optimize potency, selectivity, immunogenicity, stability, aggregation, expression, formulation, and manufacturability simultaneously
- Whether multiple independent assets validate the same claimed capability
- Whether observed asset performance can be attributed to the platform rather than ordinary medicinal chemistry or protein engineering
- Data rights, model reproducibility, scaling constraints, and dependence on proprietary assays

Use a platform evidence ladder:

`narrative -> retrospective benchmark -> prospective wet-lab validation -> development candidate -> human target engagement -> clinical differentiation -> repeatable multi-asset validation`

## 5. Asset and pipeline assessment

Create a normalized pipeline table:

| Asset | Alias | Target/MoA | Modality | Indication | Stage | Trial ID | Evidence grade | Next catalyst |
|---|---|---|---|---|---|---|---|---|

For each material asset, analyze:

### Biology

- Human genetic, pathological, pharmacological, and competitor validation
- Target expression and disease-state dependence
- Causal versus correlative evidence
- On-target and off-target safety liabilities
- Resistance, redundancy, compensatory pathways, and biomarker segmentation

### Molecule design

- Modality fit, binding/enzymatic properties, valency, selectivity, half-life, tissue exposure, route, dose, and formulation
- Claimed engineering advantage and the experiment that would validate it
- Immunogenicity and species-cross-reactivity limitations

### Preclinical chain

- Assay relevance and controls
- Model validity and whether the model predicts human outcomes in this disease
- Exposure-response and clinically achievable concentrations
- Head-to-head comparator, dosing parity, blinding, replication, sample size, and statistical treatment
- Toxicology species, therapeutic index, reversibility, and chronic-dose evidence

Do not equate animal survival, biomarker shifts, modeled human PK/PD, or in-vitro potency with clinical benefit.

## 6. Clinical-data interpretation

Extract before interpreting:

- Trial phase, design, sites, randomization, blinding, control, sample size, dose cohorts, treatment duration, and follow-up
- Inclusion/exclusion criteria, baseline severity, prior therapy, background treatment, geography, and analysis populations
- Primary, key secondary, exploratory, and biomarker endpoints; timing and hierarchy
- Estimand, multiplicity control, missing-data handling, protocol amendments, and early stopping
- Effect size, confidence interval, p-value when relevant, absolute versus relative change, responder thresholds, and durability
- Treatment-emergent adverse events, serious events, grade, discontinuations, deaths, lab abnormalities, infections, immunogenicity, and dose dependence

Interpretation checks:

- Statistical significance is not clinical meaningfulness.
- A subgroup is hypothesis-generating unless prespecified and adequately powered.
- An uncontrolled early trial supports signal detection, not causal efficacy.
- A biomarker validates biology only to the degree it connects to outcome.
- Lack of disclosed events is not zero events.
- Cross-trial comparisons require explicit caveats for population, endpoint definition, timing, control, rescue medication, and background therapy.

For an early asset, define the minimum convincing human package: safety window, exposure, target engagement, pathway modulation, dose response, clinical signal, durability, and immunogenicity.

## 7. Competition and market

Build the comparator set in layers:

1. Same target and modality
2. Same target, different modality
3. Same mechanism or pathway
4. Same indication and treatment line
5. Current standard of care and likely future standard at launch

Normalize stage using the most advanced active trial in the relevant indication; do not use a molecule's highest stage in another disease without labeling it.

Compare efficacy, safety, convenience, onset, durability, route, dosing frequency, monitoring, combination burden, biomarker strategy, manufacturing, access, and price. Distinguish mechanistic differentiation from clinically proven differentiation.

Estimate the addressable market from treated patients, eligible fraction, diagnosis, line of therapy, contraindications, duration, price/net price, and adoption. Show the funnel; do not multiply headline prevalence by list price.

## 8. Regulatory, CMC, and IP

### Regulatory

- Identify relevant endpoint precedent, expedited designations, pediatric or post-marketing obligations, and regional differences.
- Separate regulator-confirmed designations and meetings from sponsor expectations.

### CMC

- Assess process complexity, yield, stability, aggregation, formulation, device, cold chain, comparability, scale-up, release assays, and raw-material constraints.
- For enzymes, engineered proteins, cell/gene therapies, and novel delivery systems, explicitly examine immunogenicity, repeat dosing, biodistribution, shedding, or insertional risks as applicable.

### IP

- Identify composition-of-matter, method-of-use, formulation, manufacturing, platform, and device families when available.
- Track priority dates, expiration assumptions, continuations/divisionals, ownership, licenses, oppositions, and litigation.
- Label landscape observations as research intelligence. Do not claim freedom to operate, validity, infringement, or enforceability without qualified counsel and claim-level review.

## 9. Valuation

Choose a method appropriate to maturity:

- Commercial-stage: revenue build, margins, lifecycle, and discounted cash flow; cross-check multiples.
- Clinical-stage: indication-level risk-adjusted NPV.
- Preclinical/private platform: scenario analysis, precedent financing/deals, cash, and pipeline rNPV with wide ranges.

For each indication, show:

`eligible patients x penetration x net price x treatment duration = peak sales`

Then specify launch timing, ramp, patent/exclusivity, probability of technical and regulatory success, costs, royalties, tax, discount rate, and terminal assumptions. Avoid double counting platform value and asset value. Use bear/base/bull cases and at least two sensitivities, usually probability of success and peak sales or launch timing.

Do not present an acquisition price as a probability-weighted fundamental value without adjusting for control premium, synergies, competitive process, and contingent consideration.

## 10. Catalysts and risks

For each catalyst include expected window, event, evidence to watch, base expectation, upside case, downside case, and thesis impact. Use ranges when timing is sponsor-guided.

Organize risks by clinical, mechanism, safety, regulatory, CMC, commercial, competitive, financing, governance, IP, and platform. Score severity and monitorability separately. Pair each risk with an observable signpost.

Finish with:

- Three strongest thesis supports
- Three largest unresolved questions
- Near-, medium-, and long-term catalysts
- Evidence that would change the conclusion


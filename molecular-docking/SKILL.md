---
name: molecular-docking
description: Run and diagnose expert-grade protein-ligand molecular docking through SciMiner using Gnina, AutoDock Vina, PackDock, SurfDock, DiffDock, and fpocket. Use for focused docking, pocket-aware engine selection, multi-seed ensemble sampling, pose-pool construction, energy-gap filtering, RMSD clustering, cross-run recurrence analysis, critical-contact checks, physics sanity checks, confidence grading, and multi-engine comparisons. Do not use a single run or Rank 1 score as the final answer.
---

# Molecular Docking

Treat docking as a hypothesis-generation and diagnosis workflow, not as a one-shot ranking exercise. Do not report a final pose from one run or from score rank alone.

## Non-negotiable rules

- Inspect the receptor, pocket, ligand, and requested biological context before docking.
- Do not perform unrestricted whole-protein blind docking. If the site is unknown, run `fpocket`, rank plausible sites, and dock each candidate in a separate focused box.
- Use 5 independent random seeds when the selected engine exposes seed control. Request 20 poses per run when supported.
- Pool poses across runs before energy filtering or clustering. Preserve score, seed, run, engine, and source-file provenance.
- Protect an isolated low-scoring pose from cluster-size pruning, but do not declare it correct until geometry, recurrence, contacts, and physical plausibility have been checked.
- Never equate a docking-score difference with an experimentally calibrated binding-free-energy difference. Use energy gaps as triage signals only; do not convert them directly into Boltzmann populations.
- If required sampling controls or pose-level outputs are unavailable, state the limitation, downgrade confidence, and use another suitable engine when possible.

## Engine selection

- Default to `Gnina` for a generic focused-docking request.
- Use the engine explicitly named by the user.
- Use `PackDock` when side-chain repacking or receptor flexibility is central.
- Prefer `SurfDock` for shallow, surface-shaped, or cryptic pockets.
- Use `DiffDock` as an orthogonal pose generator when classical docking disperses, especially for shallow sites; do not treat its confidence as binding affinity.
- Use `fpocket` before docking when no defensible pocket is available.
- For robustness comparisons, use the requested engine set; otherwise compare the default engine with one mechanistically different method when confidence matters.

## Five-stage SOP

### 1. Reconnaissance: profile pocket and ligand

Complete and record the following before submission.

#### Receptor and ligand readiness

- Check missing pocket residues or atoms, alternate locations, unresolved loops, protonation/tautomer states, cofactors, metals, conserved waters, covalent chemistry, and biologically relevant oligomer state.
- Standardize the ligand without silently changing stereochemistry. Enumerate materially plausible protonation or tautomer states when the binding-site chemistry does not resolve them.
- Identify known catalytic residues, ligand anchors, resistance mutations, and homologous complex evidence. Label each as required, supportive, or unknown rather than inventing a mandatory contact.

#### Pocket profile

Classify the site and record the evidence used:

- **Deep/narrow:** strongly enclosed, restricted entrance, large expected burial/SASA loss. Anticipate entry-barrier undersampling and false large clusters near the mouth. Preserve rare deep poses.
- **Wide/shallow:** solvent-open, flat, or PPI-like. Mark high risk because conventional scores often lack a sharp minimum. Tighten the solvent-facing box dimension and require stronger recurrence and burial/contact evidence.
- **Intermediate/ambiguous:** retain both risk models and avoid overconfident classification.

Use pocket volume, depth, enclosure, entrance width, residue composition, and ligand-bound structural analogs when available. Do not infer pocket depth from score alone.

#### Ligand flexibility and starting exhaustiveness

Count rotatable bonds using one stated definition and exclude terminal or resonance-locked bonds consistently:

| Rotatable bonds | Flexibility | Initial exhaustiveness |
|---:|---|---:|
| 0-4 | rigid/semi-rigid | 32 |
| 5-8 | moderate | 64 |
| >8 | high | at least 128 |

Treat macrocycles, coupled torsions, and multiple stereochemical/protomer states as additional complexity even if the raw count is low. If an API lacks the named exhaustiveness control, use its documented closest sampling control and disclose the mapping.

#### Focused grid box

- Center the box on the known ligand, validated pocket centroid, or selected `fpocket` site.
- Use the smallest box that contains the ligand in plausible orientations plus a modest motion margin. A typical side is 15-20 Å; enlarge only enough to avoid clipping a large ligand.
- For shallow sites, minimize extension into bulk solvent while retaining the complete interaction surface.
- Record center, dimensions, derivation, and any uncertainty. For multiple plausible pockets, create separate focused boxes instead of one oversized box.

### 2. Build a multi-seed pose pool

1. Run 5-8 independent jobs with unique, recorded random seeds and otherwise identical parameters.
2. Request 20-30 output poses per job. Do not accept a default nine-pose output as an expert ensemble when the API allows more.
3. For a highly flexible ligand or narrow pocket, first raise exhaustiveness; add seeds only after each run has meaningful depth.
4. Merge all successful outputs into one pose pool, normally 100-240 raw poses.
5. Store for every pose: `pose_id`, engine, run ID, seed, raw/reranked score name and value, receptor/ligand state, box, parameters, and coordinates.
6. Detect failed or truncated jobs. Do not count duplicated poses within one run as independent evidence.

If the service does not expose seeds, emulate independence only through documented stochastic reruns and label the seed as unavailable. If it cannot return enough poses, use the maximum documented value, consider another engine, and cap the confidence accordingly.

### 3. Apply the energy-gap gate

Normalize only score direction and units that are explicitly documented. Never merge incomparable score types into one numeric ranking.

For a score where lower is better, set `E_min` to the best score and calculate `delta_E_i = E_i - E_min` within the same engine/scoring function.

- Retain the first tier at `delta_E <= 1.5 kcal/mol` by default.
- Relax to at most `2.0 kcal/mol` only with a recorded reason, such as known score noise or preservation of a distinct chemically plausible mode.
- Remove poses outside the first tier from final-pose competition, while retaining them in the audit table.

Diagnose the landscape:

- **Isolated deep-score candidate:** if the best pose leads the next distinct pose or cluster by at least 1.5-2.0 score units in a kcal/mol-like score, protect it regardless of cluster size. Then explicitly test whether it is reproducible, deeply seated, strained, clashing, or exploiting a scoring artifact. An isolated score is a protected hypothesis, not proof.
- **Flat landscape:** if the leading poses or clusters lie within roughly 0.5-1.0 score unit, declare that rank order is unresolved. Do not select Rank 1 directly; advance all competitive modes to clustering and physics checks.

When an engine reports a non-energy confidence or arbitrary score, use documented score semantics and describe gaps in native units without calling them kcal/mol.

### 4. Cluster poses and cross-check pocket depth

- Align poses in the same receptor frame.
- Cluster first-tier poses by ligand heavy-atom RMSD `< 2.0 Å`; use symmetry-aware atom mapping where possible.
- For flexible or symmetric ligands, supplement whole-ligand RMSD with scaffold/core RMSD and interaction fingerprints when whole-ligand RMSD is misleading.
- For each cluster, report representative pose, member count, score range, distinct-run count, recurrence fraction, depth/burial, and key contacts.

Use distinct-run recurrence, not raw member count, as the primary sampling-stability statistic. A strong default is recurrence in at least 75% of runs (for example, 6 of 8). Report the exact numerator and denominator; do not silently treat failed runs as absence.

Apply pocket-aware logic:

- **Wide/shallow + large cluster:** suspect easy-access surface convergence. Calculate ligand burial from bound versus isolated-ligand SASA when possible: `buried_fraction = 1 - SASA_bound / SASA_free`. Reject a mostly solvent-exposed cluster (approximately more than half exposed) when it also lacks robust anchors or shape complementarity.
- **Deep pocket + small deep cluster versus large shallow cluster:** favor the small deep cluster when it has a better first-tier score, substantial burial, sound chemistry, and no severe strain/clash. Do not let mouth accessibility or within-run duplicates outvote a hard-to-sample deep mode.
- **Cross-run recurrence:** distinguish a cluster copied many times within one job from a cluster independently rediscovered across seeds. Only the latter supports reproducibility.

### 5. Apply biological and physical hard constraints

Use these checks to choose between the final one or two clusters.

#### Critical contacts

- Check literature- or structure-supported catalytic residues, anchor residues, metal coordination, resistance sites, and conserved interaction motifs.
- Use chemically appropriate geometry. As a general screening bound, require plausible hydrogen-bond donor-acceptor distance `<= 3.5 Å`, then inspect angle and protonation. Evaluate salt bridges, pi stacking, cation-pi contacts, and metal geometry with interaction-specific criteria.
- Allow a well-supported required interaction to override a small score disadvantage. If pose A scores slightly better but misses a genuinely required anchor while pose B satisfies it without new physical defects, choose B and document the override.
- Do not manufacture a required-contact rule from weak or irrelevant literature.

#### Physics sanity check

Reject or strongly penalize poses with:

- unsatisfied buried charges or polar groups in a hydrophobic cavity;
- a large hydrophobe unnecessarily exposed to solvent;
- severe protein-ligand or intraligand clashes;
- implausible ligand torsional strain or broken aromaticity/stereochemistry;
- impossible protonation, tautomer, covalent, cofactor, water, or metal-coordination assumptions;
- score gains driven solely by excessive ligand size or nonspecific surface contact.

If two poses remain credible and docking cannot separate them, report both instead of forcing a winner.

## Decision hierarchy

Use this order; score rank alone never outranks all later checks:

1. Chemical validity and absence of hard physical contradictions.
2. Required biological contacts supported by evidence.
3. Pocket-appropriate depth, burial, and shape complementarity.
4. Cross-run recurrence and independent-method agreement.
5. Within-method energy gap.
6. Raw cluster size and individual rank.

## Confidence grading

Assign the highest level whose required evidence is actually available.

### High confidence

Require all or nearly all of the following: a geometrically credible enclosed site; the same binding mode in at least 75% of independent runs; a clear within-score gap of more than about 1.5 units where those units are documented as kcal/mol-like; correct critical-contact geometry; strong burial/complementarity; and no physics red flags. Describe the pose as a high-priority design hypothesis, not experimentally proven binding.

### Medium confidence

Use when two credible orientations compete, the gap is less than about 0.8 score unit, recurrence is moderate, or some biological constraints are unavailable. Report both modes and ask for discriminating evidence, such as mutational activity, SAR, co-crystal contacts, competition data, or metal/water dependence.

Suggested question: "Two competitive binding modes remain and docking alone cannot separate them. Do you have mutation, SAR, or binding-site data that can test the distinguishing contacts?"

### Low confidence / warning

Use when independent runs disperse, no cluster recurs, the pocket is wide and shallow, poses remain solvent-exposed, or results depend strongly on engine/box/protonation. Explicitly advise against relying on the current Rank 1 pose. Recommend an orthogonal pose generator such as DiffDock, receptor-ensemble/flexible docking, and—when scientifically justified—replicated explicit-solvent MD (often 20-50 ns as an initial stability probe). State that short MD stability does not establish affinity or the true binding mode.

## Required report and artifacts

Return more than a structure file. Include:

1. **System audit:** receptor source/state, preparation decisions, ligand state, rotatable-bond count, pocket class, and known critical residues.
2. **Sampling manifest:** engine/version when available, box center/dimensions, exhaustiveness or equivalent, seeds, poses requested/returned, failures, and all task IDs.
3. **Pose-pool summary:** raw pose count, score semantics, `E_min`, cutoff, discarded count, and warnings about incomparable scores.
4. **Cluster table:** cluster ID, representative pose, best/median score, members, distinct runs, recurrence, RMSD rule, burial/SASA, depth, contacts, and rejection reason where applicable.
5. **Final decision:** chosen pose or unresolved alternatives, explicit decision hierarchy, confidence level, supporting evidence, contradictions, and next experiment or computation.
6. **Artifacts:** representative coordinates, complete pose/score provenance table, and every successful SciMiner `history_url`.

Do not claim high confidence if recurrence, score semantics, pocket geometry, or critical-contact evidence could not be evaluated.

## SciMiner invocation contract

### Prerequisite

Use the runtime `SCIMINER_API_KEY` as the `X-Auth-Token`. Do not request, derive, print, persist, or search for the key. If it is absent, stop and report that the SciMiner gateway did not inject the credential.

### Authoritative documentation

Before every invocation, read the selected Markdown file under `https://sciminer.tech/tool_api_files/`:

- `Gnina` -> `Gnina_api_doc.md`
- `AutoDock Vina` -> `AutoDock Vina_api_doc.md`
- `PackDock` -> `PackDock_api_doc.md`
- `SurfDock` -> `SurfDock_api_doc.md`
- `DiffDock` -> `DiffDock_api_doc.md`
- `fpocket` -> `fpocket_api_doc.md`

Treat the current tool doc as the sole source of truth for base URL, endpoint, content type, authentication header, provider/tool names, method, parameters, enum values, upload fields, request encoding, and example submission flow. Select the section matching the input shape. Do not invent unsupported parameters or use a shared local registry abstraction.

If the documented API cannot express this SOP's requested seed, exhaustiveness, pose count, or box control, do not pass an invented field. Use the documented maximum/corresponding control, switch or add an engine when appropriate, and record the limitation in the confidence assessment.

### Submission sequence

1. Select the engine and matching doc; run `fpocket` first when no defensible site exists.
2. Upload each required file exactly as documented and replace local paths with returned `file_id` values.
3. Submit each independent run with its recorded parameters and provenance.
4. Poll and collect all results into the pose pool. For tasks without a fixed ETA, stop polling after 1800 seconds and return the `history_url` for later inspection.
5. Cite the selected Markdown doc as the payload source in the summary.
6. Attach every successful task's `history_url` at the end of the final response.

Expected task envelope:

```json
{
  "status": "SUCCESS",
  "result": {},
  "task_id": "xxx",
  "history_url": "https://sciminer.tech/utility/history/result/APITool?id=<task_id>"
}
```

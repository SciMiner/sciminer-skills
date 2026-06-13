---
name: fep-alternative
description: Relative binding free-energy and activity-label prediction workflows using PBCNet 2.0 on SciMiner, with Gnina docking and PDB/database retrieval to complete missing inputs.
credential_files:
   - ~/.config/sciminer/credentials.json
---

# FEP Alternative Skill

This skill predicts relative binding free energy or activity labels for newly
designed small molecules using the SciMiner `PBCNet 2.0` tool. It is a
PBCNet-based alternative workflow for FEP-style lead optimization tasks, not an
explicit molecular-dynamics FEP simulation.

The core SciMiner workflow uses:

- `PBCNet 2.0` for relative binding affinity or activity-label prediction
- `Gnina` for generating docked 3D binding conformations when candidate or
  reference ligand poses are missing
- PDB database retrieval through the bundled `rcsb-pdb-skill` when the user
  has activity data but no protein-ligand crystal structure

## When to use this skill

- Predict relative binding free energy, binding affinity, or activity labels
  for newly designed molecules against a known target.
- The user has one or more reference molecules with measured biological
  activity against the same target and wants to predict newly designed
  molecules.
- The user provides a receptor PDB file, reference ligand conformations, labels,
  and candidate molecules, or asks the agent to complete missing receptor,
  pocket, docking, or conformation files.
- The user asks for an FEP alternative, fast relative activity prediction,
  PBCNet, or PBCNet 2.0.

## Required PBCNet inputs

`PBCNet 2.0` requires these conceptual inputs:

- protein receptor PDB file
- SDF file containing 3D binding conformations of reference molecules
- activity label values for the reference molecules
- SDF file containing docked 3D binding conformations of molecules to be tested

If the user cannot provide all of these files, collect the missing information
and supplement it through the workflows below. Do not send random or undocked
candidate conformations to PBCNet; the candidate SDF must contain already-docked
binding poses.

## Method selection rule

- If all PBCNet-ready files are available, invoke `PBCNet 2.0` directly.
- If a protein-ligand crystal structure or receptor PDB plus original/reference
  ligand pose is available, use the original ligand position as the binding
  pocket, run `Gnina` to dock the molecules to be tested, and then invoke
  `PBCNet 2.0` with the top 3 poses of each ligand ranked by centroid
  deviation from the reference pose.
- If measured reference activities are available but no crystal structure is
  available, search the PDB for structures of the same target with co-crystal
  ligands similar to the measured reference ligands. Keep candidates with
  ligand similarity higher than 30%, select the crystal with the highest
  ligand similarity and acceptable structure quality, extract the receptor and
  binding pocket from that crystal, establish reference poses for measured
  molecules, dock test molecules with `Gnina`, rank predicted poses by centroid
  deviation from the reference pose, keep the top 3 poses of each ligand for
  bioactivity prediction, and then invoke `PBCNet 2.0`.
- If target identity, reference ligand structures, activity labels, or test
  molecule structures are missing and cannot be recovered from explicit user
  context, ask the user for the missing information before invoking SciMiner.

## Prerequisites

1. Obtain a free SciMiner API key from `https://sciminer.tech/utility`.
2. Store it outside this repository at `~/.config/sciminer/credentials.json`
   with JSON shaped as `{"api_key":"your_api_key_here"}`.
3. For SciMiner calls, read the API key from
   `~/.config/sciminer/credentials.json` and send it as the `X-Auth-Token`
   header.
4. Never print, persist, or store the API key in prompts, logs, or repository
   files. Agents should remember only the credential file path.

If `~/.config/sciminer/credentials.json` is not available or does not contain
an `api_key` field, stop and tell the user to obtain a free SciMiner API key
from `https://sciminer.tech/utility` and store it in that file. Do not try to
complete the task by switching to other tools or services.

## Authoritative tool-doc source (required)

The published Markdown files under `https://sciminer.tech/tool_api_files/` are
the single source of truth for SciMiner `provider_name`, `tool_name`, allowed
`parameters`, file-upload behavior, request encoding, and submission flow.

Use these SciMiner Markdown docs:

- `PBCNet 2.0` -> `PBCNet 2.0_api_doc.md`
- `Gnina` -> `Gnina_api_doc.md`

For PDB database retrieval and ligand-similarity searches, read the bundled
database sub-skill before querying public resources:

- `rcsb-pdb-skill/SKILL.md`

The agent MUST:

1. Resolve the selected SciMiner tool's Markdown file and read it before every
   invocation.
2. Never invent `provider_name`, `tool_name`, parameter names, enum values,
   upload-field names, content type, or submission flow from memory.
3. Extract and follow the selected SciMiner doc section's exact:
   - Base URL
   - API endpoint
   - Content-Type
   - Authentication header
   - Tool Name
   - Method
   - Parameter table, including required fields and enum values
   - File-upload instructions and example code
4. Choose the correct doc section if the selected doc contains multiple tool
   variants, such as reference-ligand input vs pocket-center input.
5. Cite the selected Markdown docs as the payload source in summaries.

If a user-provided parameter is not present in the selected Markdown doc
section, ask for correction or drop it with an explanation.

## Required workflow

1. Build an input ledger before running tools. Track target identity, receptor
   PDB or PDB ID, reference molecule structures, reference activity labels and
   units, candidate molecule structures, binding pocket definition, and which
   files are already PBCNet-ready.
2. Determine whether the task fits the direct PBCNet path, the crystal-guided
   docking completion path, or the no-crystal PDB-retrieval path.
3. Read the `PBCNet 2.0` Markdown doc before constructing any PBCNet payload.
4. If docking is needed, read the `Gnina` Markdown doc before docking any
   molecule and choose the doc section that matches the available pocket input.
5. If no crystal structure is available, read the bundled
    `rcsb-pdb-skill/SKILL.md` sub-skill and retrieve PDB structures for the
    same target using ligand similarity to the measured reference ligands. Keep
    structures with ligand similarity higher than 30%, prefer the highest
    similarity, and consider resolution, chain completeness, ligand relevance,
    and mutation state when breaking ties.
6. For crystal-guided workflows, use the original ligand position in the
   user-provided or selected crystal structure as the binding pocket.
7. Establish measured reference poses before docking test molecules. If there
    is only one measured reference molecule with a matching PDB co-crystal
    ligand, use that native ligand pose from the PDB as the reference pose. If
    there are multiple measured reference molecules represented across several
    PDB files, perform cross-docking among the candidate receptor structures and
    measured reference molecules; select the receptor that best preserves native
    or mutually consistent reference binding modes, then determine each measured
    molecule's reference pose in that selected receptor frame.
8. For no-crystal workflows, extract the protein receptor PDB file and bound
   ligand pocket from the selected PDB crystal. When extracting any ligand from
   a PDB file, validate and preserve chemical bond orders before writing SDF;
   do not allow conversion tools to turn all bonds into single bonds.
9. After extraction and reference-pose determination, dock molecules to be
    tested in that pocket.
10. When multiple docked poses are produced, calculate the centroid of each
    predicted ligand pose and the centroid of the matched reference pose in the
    same receptor coordinate frame. Compute centroid deviation as the Euclidean
    distance between those centroids, rank poses for each ligand from smallest
    to largest centroid deviation, and keep the top 3 poses of each ligand for
    PBCNet bioactivity prediction. If fewer than 3 poses are available for a
    ligand, keep all available poses and report the count. Preserve ligand IDs,
    pose ranks, and centroid-deviation values in the prepared SDF or companion
    metadata when possible.
11. Assemble the reference SDF so its molecule order matches the activity label
   order exactly. Preserve user-provided activity units and transformations;
   do not invent or convert labels unless the user requested the conversion or
   confirmed the rule.
12. Upload required file inputs exactly as described by the selected SciMiner
    Markdown docs and replace local paths with returned `file_id` values.
13. Write or run invocation code directly from the selected Markdown docs'
    base-information block, parameter table, file-upload instructions, and
    example code. Do not apply a shared invocation template or local registry
    abstraction in this skill.
14. Poll the task result and return the `share_url` in the final user-facing
    summary.

## Missing-input completion rules

- Missing receptor PDB but target and measured ligand are known: search PDB for
  same-target co-crystal structures using ligand similarity, require ligand
  similarity higher than 30%, then select the best supported crystal.
- Missing candidate binding conformations: run `Gnina` docking in the selected
  or user-provided pocket, calculate centroid deviation from the reference pose
  for every predicted pose, and use the top 3 poses of each ligand as the
  PBCNet candidate conformation input.
- Missing reference ligand SDF but a crystal ligand is present: extract or
  prepare the crystal ligand pose as a 3D SDF when that ligand corresponds to a
  measured reference molecule. Validate ligand chemistry during extraction:
  preserve bond orders from CCD or another trusted chemical template, repair
  aromatic/double/triple bonds when needed, and reject or flag outputs where all
  bonds have become single bonds. Otherwise ask the user to confirm the
  reference mapping.
- Multiple measured reference molecules across several PDB files: perform
  cross-docking to select the receptor structure and assign each measured
  molecule's reference pose before ranking test-molecule poses by centroid
  deviation.
- Missing measured activity labels: ask the user for values and units. Public
  database activities may be used only when the user asks for retrieval or
  confirms the selected measurements.
- Missing test molecules: ask for SDF, SMILES, or another structure file format
  accepted by the selected `Gnina` doc section.

## File upload rules

- Upload every required file parameter described by the selected SciMiner
  Markdown doc before invocation.
- Replace local paths in `parameters` with the returned `file_id` strings.
- Use the upload form field documented by the selected SciMiner Markdown doc.
- Skip optional file parameters that the user did not provide.

## Expected result format

```json
{
    "status": "SUCCESS",
    "result": {...},
    "task_id": "xxx",
    "share_url": "https://sciminer.tech/share?id=<task_id>&type=API_TOOL"
}
```

## Workflow guidance

- Complete receptor, reference SDF, labels, and docked candidate SDF ->
  `PBCNet 2.0`.
- Receptor or crystal structure plus candidate molecules but no candidate poses
  -> `Gnina`, centroid-deviation ranking, top 3 poses per ligand, then
  `PBCNet 2.0`.
- Reference activities but no crystal structure -> PDB ligand-similarity
  retrieval, native-pose or cross-docking reference-pose assignment, receptor
  and pocket extraction with ligand bond-order validation, `Gnina` docking,
  centroid-deviation ranking, top 3 poses per ligand, then `PBCNet 2.0`.
- Ambiguous labels, units, molecule ordering, target identity, or reference
  mapping -> ask for clarification before submitting PBCNet.

## Notes

- Use the selected SciMiner Markdown docs under
  `https://sciminer.tech/tool_api_files/` as the authoritative source for
  payload construction and invoke-method details.
- Read the SciMiner API key from `~/.config/sciminer/credentials.json` and send
  it as the `X-Auth-Token` header. Do not print or persist the API key in
  prompts, logs, or repository files.
- If `~/.config/sciminer/credentials.json` is missing or does not contain an
  `api_key` field, stop and tell the user to obtain a free SciMiner API key
  from `https://sciminer.tech/utility` and store it in that file.
- `provider_name` and `tool_name` must exactly match the selected Markdown doc.
- Use the selected Markdown doc to determine PBCNet `label_list` formatting,
  Gnina pocket specification, file inputs, parameter placement, and any
  tool-specific submission details.
- Important: when summarizing results to users, attach the `share_url` links of
  every successful task at the end so that users can view the online results,
  rather than showing file download links.
- For long-running tasks without a fixed ETA, poll for no more than 6000
  seconds; if the task is still running, stop polling and return the current
  `task_id` and `share_url` so the user can check later.
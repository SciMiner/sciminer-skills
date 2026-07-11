---
name: admet-pkpd
description: ADMET and pharmacokinetic/pharmacodynamic property prediction workflows using ADMET Predictor, AOMP, OBA, Graph-pKa, DeepEsol, and Molecular Descriptors through SciMiner.
required_environment_variables:
    - SCIMINER_API_KEY
---

# ADMET & PKPD Skill

This skill groups property prediction workflows for assessing the pharmacokinetic and pharmacodynamic profile of small molecules, including:

- comprehensive ADMET property prediction (absorption, distribution, metabolism, excretion, toxicity) with ADMET Predictor
- AOX-mediated oxidative metabolism and site-of-metabolism prediction with AOMP
- oral bioavailability prediction with OBA
- pKa calculation for ionizable groups with Graph-pKa
- aqueous solvation free-energy prediction with DeepEsol
- physicochemical molecular descriptor calculation with Molecular Descriptors

## When to use this skill

- Predict ADMET properties (hERG, CYP, BBB, Caco-2, AMES, etc.) for a set of molecules
- Identify AOX metabolic substrates and their sites of oxidative metabolism
- Estimate oral bioavailability at a given dose
- Calculate pKa values of ionizable functional groups
- Predict aqueous solvation free energy (ΔG_solv)
- Calculate physicochemical descriptors (MW, LogP, TPSA, etc.) for a molecule or a library

## Method selection rule

- For full ADMET profiling, use `ADMET Predictor`. Select specific `features` to narrow the output (e.g., `T` for toxicity only, `M_CYP450 3A4 Inhibitor` for a single endpoint).
- For AOX-specific metabolism and site-of-metabolism (SOM) prediction, use `AOMP`.
- For oral bioavailability at a specific dose, use `OBA` (requires both SMILES and dose in mg).
- For pKa of ionizable groups, use `Graph-pKa`.
- For aqueous solvation free energy, use `DeepEsol`.
- For bulk physicochemical descriptors supporting PKPD modelling or Lipinski/Veber filtering, use `Molecular Descriptors`.
- When input is a single SMILES or a small set, prefer the SMILES-input interface. When a file is provided or the library is large, prefer the file-upload interface.

## Prerequisites

1. `SCIMINER_API_KEY` is pre-obtained by the SciMiner gateway before the agent run reaches this skill.
2. Use the runtime `SCIMINER_API_KEY` directly as the `X-Auth-Token` for SciMiner tool calls.
3. Do not request, derive, print, persist, or write this key to any file.

If `SCIMINER_API_KEY` is not available at skill runtime, stop and report that the gateway did not inject the required credential. Do not try to derive it inside the skill or switch to other tools or services.

## Authoritative tool-doc source (required)

The published Markdown files under `https://sciminer.tech/tool_api_files/` are
the single source of truth for `provider_name`, `tool_name`, allowed
`parameters`, file-upload behavior, request encoding, and the example
submission flow for this skill's included tools.

Use these SciMiner Markdown docs:

- `ADMET Predictor` -> `ADMET Predictor_api_doc.md`
- `AOMP` -> `AOMP_api_doc.md`
- `OBA` -> `OBA_api_doc.md`
- `Graph-pKa` -> `Graph-pKa_api_doc.md`
- `DeepEsol` -> `DeepEsol_api_doc.md`
- `Molecular Descriptors` -> `Molecular Descriptors_api_doc.md`

The agent MUST:

1. Resolve the selected tool's Markdown file and read it before every
   invocation.
2. Never invent `provider_name`, `tool_name`, parameter names, enum values,
   upload-field names, content type, or submission flow from memory.
3. Extract and follow the selected doc section's exact:
   - Base URL
   - API endpoint
   - Content-Type
   - Authentication header
   - Tool Name
   - Method
   - Parameter table, including required fields and enum values
   - File-upload instructions and example code
4. Choose the correct section if the selected doc contains multiple tool
   variants, such as SMILES input vs file upload.
5. Cite the selected Markdown doc as the payload source in summaries.

If a user-provided parameter is not present in the selected Markdown doc
section, ask for correction or drop it with an explanation.

## Required workflow

1. Determine which included tool matches the user's request.
2. Read the corresponding Markdown file from
   `https://sciminer.tech/tool_api_files/`.
3. Choose the doc section that matches the user's input shape.
4. Collect any missing required parameters from the user.
5. Upload required file inputs exactly as described by the selected Markdown
   doc and replace local paths with returned `file_id` values.
6. Write or run the invocation code directly from the selected Markdown doc's
   base-information block, parameter table, file-upload instructions, and
   example code. Do not apply a shared invocation template or local registry
   abstraction in this skill.
7. Poll for the task result and return the `share_url` in the final user-facing
   summary.

## File upload rules

- Upload every required file parameter described by the selected Markdown doc
  before invocation.
- Replace local paths in `parameters` with the returned `file_id` strings.
- Use the upload form field documented by the selected Markdown doc. If the doc
  only shows the generic SciMiner upload example and does not override the
  field name, follow that example's default `file` field.
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

- General ADMET or drug-likeness assessment, and endpoint-specific questions such as CYP inhibition, BBB penetration, hERG liability, AMES mutagenicity, or Caco-2 permeability -> `ADMET Predictor`
- AOX-mediated metabolism or site-of-metabolism prediction -> `AOMP`
- Oral bioavailability prediction -> `OBA`
- pKa or ionization-state prediction -> `Graph-pKa`
- Solubility or solvation free-energy prediction -> `DeepEsol`
- Molecular weight, LogP, TPSA, rotatable bonds, H-bond donor/acceptor counts, or related descriptor requests -> `Molecular Descriptors`
- Combined ADMET + descriptor + pKa panels -> chain `ADMET Predictor`, `Molecular Descriptors`, and `Graph-pKa`

## Notes

- Use the selected Markdown doc under
   `https://sciminer.tech/tool_api_files/` as the authoritative source for
   payload construction and invoke-method details.
- This skill requires the `SCIMINER_API_KEY` environment variable to be injected by the SciMiner gateway before skill execution. The API key is sent as the `X-Auth-Token` header.
- If `SCIMINER_API_KEY` is not available at skill runtime, stop and report that the gateway did not inject the required credential. Do not attempt to derive or locate the API key through other means.
- `provider_name` must exactly match the selected Markdown doc.
- The `features` parameter for ADMET Predictor is optional; omitting it returns all endpoints. Passing category letters (`A`, `D`, `M`, `E`, `T`) returns all endpoints within that category.
- Use the selected Markdown doc to determine request encoding, file-upload
   field names, and any tool-specific submission details.
- **Important**: When summarizing results to users, attach the `share_url` links of every successful task at the end so that users can view the online results of each invoked tool, rather than showing the file download links.
- For long-running tasks without a fixed ETA, poll for no more than 600 seconds; if the task is still running, stop polling and return the current `task_id` and `share_url` so the user can check later.

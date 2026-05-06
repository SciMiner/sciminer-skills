---
name: admet-pkpd
description: ADMET and pharmacokinetic/pharmacodynamic property prediction workflows using ADMET Predictor, AOMP, OBA, Graph-pKa, DeepEsol, and Molecular Descriptors through SciMiner.
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

1. Get a free SciMiner API key from `https://sciminer.tech/utility`
2. Store the required credential in a persistent user-level config file that is outside this repository.
3. Configure:

```bash
mkdir -p ~/.config/sciminer
chmod 700 ~/.config/sciminer
printf '{"api_key":"your_api_key_here"}\n' > ~/.config/sciminer/credentials.json
chmod 600 ~/.config/sciminer/credentials.json
```

Agents should remember the credential file path, not the credential value. For persistent agent behavior across tasks, add an instruction to the relevant agent memory or project instruction file such as `CLAUDE.md`, `AGENTS.md`, or the Codex equivalent: "For SciMiner calls, read the API key from `~/.config/sciminer/credentials.json`; never print or store the API key in prompts, logs, or repository files."

If `~/.config/sciminer/credentials.json` is not available or does not contain an `api_key` field, stop and tell the user to obtain a free SciMiner API key from `https://sciminer.tech/utility` and store it in that file. Do not try to complete the task by switching to other tools or services.

## Authoritative payload source (required)

The registry at `admet-pkpd/scripts/sciminer_registry.py` is the **single source of truth** for `provider_name`, `tool_name`, allowed `parameters`, and `file_params`. The agent MUST:

1. Resolve the selected tool via `get_tool_info(tool_name)` or `build_payload_from_registry(tool_name, user_parameters)` before every invocation.
2. Never invent payload keys from memory or copy them from OpenAPI text.
3. Filter user-provided parameters against the registry's `parameters` keys.
4. Validate required parameters before invoking.
5. Cite `admet-pkpd/scripts/sciminer_registry.py` as the payload source in summaries.

If a user-provided parameter is not present in the selected registry interface, ask for correction or drop it with an explanation.

Recommended pattern:

```python
# Adjust import path to runtime (e.g., sys.path or package layout)
from admet_pkpd.scripts.sciminer_registry import build_payload_from_registry

user_parameters = {
    # ... registry-defined keys only ...
}
payload = build_payload_from_registry("<Registry Tool Name>", user_parameters)
# payload is ready for POST {BASE_URL}/v1/internal/tools/invoke
```

## Invocation pattern

Always invoke via SciMiner's internal API using `BASE_URL`. Construct the payload from the registry, upload any file inputs, then submit and poll.

```python
import json
from pathlib import Path
import requests
import time

# Adjust import path to runtime (e.g., sys.path or package layout)
from admet_pkpd.scripts.sciminer_registry import build_payload_from_registry

BASE_URL = "https://sciminer.tech/console/api"
CREDENTIALS_PATH = Path.home() / ".config" / "sciminer" / "credentials.json"


def load_api_key():
    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(
            f"SciMiner credentials file not found: {CREDENTIALS_PATH}. "
            "Create it with an api_key field."
        )
    credentials = json.loads(CREDENTIALS_PATH.read_text())
    api_key = credentials.get("api_key")
    if not api_key:
        raise ValueError(f"Missing api_key in {CREDENTIALS_PATH}")
    return api_key


API_KEY = load_api_key()
auth_header = {"X-Auth-Token": API_KEY}


def upload_file(path: str, field: str = "file") -> str:
    """Upload a local file and return the SciMiner file_id.

    Use field="input_csv" for DeepEsol file uploads; default "file" for others.
    """
    with open(path, "rb") as fh:
        resp = requests.post(
            f"{BASE_URL}/v1/internal/tools/file",
            files={field: fh},
            headers=auth_header,
            timeout=60,
        )
    resp.raise_for_status()
    return resp.json()["file_id"]


# 1. (Optional) Upload file inputs and collect file_ids for `file_params`
# molecules_id = upload_file("path/to/molecules.txt")

# 2. Build payload strictly from registry metadata
user_parameters = {
    "smiles": "Cc1ccc(S(=O)(=O)Nc2ccc(C)cc2)cc1\nCc1ncc(C(=O)O)cc1",
    "features": ["A", "D", "M", "E", "T"],
}
payload = build_payload_from_registry("ADMET Predictor SMILES", user_parameters)

# 3. Invoke
resp = requests.post(
    f"{BASE_URL}/v1/internal/tools/invoke",
    json=payload,
    headers={**auth_header, "Content-Type": "application/json"},
    timeout=30,
)
resp.raise_for_status()
task_id = resp.json()["task_id"]

# 4. Poll for result
for _ in range(300):
    status_resp = requests.get(
        f"{BASE_URL}/v1/internal/tools/result",
        params={"task_id": task_id},
        headers=auth_header,
        timeout=10,
    )
    status_resp.raise_for_status()
    result = status_resp.json()
    if result.get("status") in {"SUCCESS", "FAILURE"}:
        print(result)
        break
    time.sleep(2)
```

> The example uses the registry-friendly tool name `"ADMET Predictor SMILES"`. If your registry exposes a different friendly name, look it up via `get_tool_info(...)` or `list_tools(...)` first.

## File upload rules

- Upload every parameter listed in the registry's `file_params` via `/v1/internal/tools/file` before invocation.
- Replace local paths in `parameters` with the returned `file_id` strings.
- Use the upload form field `input_csv` for `DeepEsol File`; use `file` for all other file-upload tools in this skill.
- Skip `file_params` entries that the user did not provide; only required file params must be present.

## Expected result format

```json
{
  "status": "SUCCESS",
  "result": {...},
  "task_id": "xxx",
  "share_url": f"https://sciminer.tech/share?id={task_id}&type=API_TOOL"
}
```

## Included tools

### ADMET Predictor
- provider_name: `ADMET Predictor`
- `ADMET_smiles_admet_post` — predict ADMET properties from one or more SMILES strings; optional `features` query array selects specific categories (`A`, `D`, `M`, `E`, `T`) or individual endpoints (e.g., `T_hERG inhibition`)
- `ADMET_admet_post` — batch-predict ADMET from a TXT file of SMILES; same optional `features` selection

### AOMP
- provider_name: `AOMP`
- `AOMP_plugins-aomp-smiles_post` — predict AOX substrate classification and site of metabolism from SMILES strings
- `AOMP_plugins-aomp_post` — batch AOX metabolism prediction from a TXT or SDF file

### OBA
- provider_name: `OBA`
- `oba_plugins-oba_post` — predict oral bioavailability from a single SMILES string and dose (integer, mg)

### Graph-pKa
- provider_name: `Graph-pKa`
- `pka_plugins-pka-smiles_post` — predict pKa values of ionizable groups from one or more SMILES strings

### DeepEsol
- provider_name: `DeepEsol`
- `start_esol_task_smiles_start_esol_task_smiles_post` — predict solvation free energy from an array of SMILES strings (form-urlencoded)
- `start_esol_task_start_esol_task_post` — batch solvation prediction from a CSV file with `mol_id` and `smiles` columns

### Molecular Descriptors
- provider_name: `Molecular Descriptors`
- `mol_description_cal_mol_des_get` — compute physicochemical descriptors for a single SMILES string (GET, query parameter)
- `file_descriptors_calc_file_descriptors_post` — batch descriptor calculation from an SDF or TXT file

## Workflow guidance

- When the user asks for a general ADMET or drug-likeness assessment, run `ADMET_smiles_admet_post` with all five feature categories (`A`, `D`, `M`, `E`, `T`) unless the user specifies a subset.
- When the user asks specifically about CYP inhibition, BBB penetration, hERG liability, AMES mutagenicity, or Caco-2 permeability, map to the corresponding `features` value (e.g., `M_CYP450 3A4 Inhibitor`, `D_Blood-Brain Barrier`, `T_hERG inhibition`) in `ADMET_smiles_admet_post`.
- For AOX-mediated metabolism or site-of-metabolism requests, use `AOMP_plugins-aomp-smiles_post` for SMILES input and `AOMP_plugins-aomp_post` for file input.
- For oral bioavailability questions, always collect both the SMILES and the dose before calling `oba_plugins-oba_post`.
- For pKa or ionization state questions, use `pka_plugins-pka-smiles_post`.
- For solubility or solvation free energy requests, use `start_esol_task_smiles_start_esol_task_smiles_post` for inline SMILES or `start_esol_task_start_esol_task_post` for CSV batch input.
- For requests involving molecular weight, LogP, TPSA, rotatable bonds, H-bond donors/acceptors, or other RDKit-style descriptors, use `mol_description_cal_mol_des_get` for a single molecule or `file_descriptors_calc_file_descriptors_post` for a library.
- When the user provides a file (TXT, SDF, or CSV), prefer the corresponding file-upload interface over the SMILES interface.
- A combined ADMET + descriptor + pKa panel can be run by chaining ADMET Predictor, Molecular Descriptors, and Graph-pKa in sequence on the same molecule set.

## Notes

- Use SciMiner `BASE_URL` for all invocations.
- Use `admet-pkpd/scripts/sciminer_registry.py` as the authoritative source for payload construction (`build_payload_from_registry`).
- This skill requires a persistent credential stored at `~/.config/sciminer/credentials.json` with an `api_key` field. The value is sent as the `X-Auth-Token` header.
- If the API key file or `api_key` field is missing, stop and notify the user to get the free key from `https://sciminer.tech/utility` and store it in `~/.config/sciminer/credentials.json`.
- Agents should remember only the credential file path and handling rule, never the API key value itself.
- `provider_name` must exactly match the values in `admet-pkpd/scripts/sciminer_registry.py`.
- The `features` parameter for ADMET Predictor is optional; omitting it returns all endpoints. Passing category letters (`A`, `D`, `M`, `E`, `T`) returns all endpoints within that category.
- The `DeepEsol` SMILES endpoint uses `application/x-www-form-urlencoded` encoding; pass `smiles` as a list of strings inside `parameters`.
- The `Molecular Descriptors` SMILES endpoint is a GET request; pass `smiles` as a query string parameter inside `parameters`.
- **Important**: When summarizing results to users, attach the `share_url` links of every successful task at the end so that users can view the online results of each invoked tool, rather than showing the file download links.

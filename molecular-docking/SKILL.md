---
name: molecular-docking
description: Molecular docking workflows across Gnina, AutoDock Vina, PackDock, SurfDock, and DiffDock through SciMiner, with Gnina as the default engine.
required_environment_variables:
    - SCIMINER_API_KEY
---

# Molecular Docking Skill

This skill groups protein-ligand docking workflows, including:

- pocket-guided docking with Gnina (default)
- classical docking with AutoDock Vina
- flexible docking with PackDock
- surface-geometry-assisted docking with SurfDock
- diffusion-model docking with DiffDock
- predicted binding-site detection with fpocket
- side-by-side comparison across multiple docking engines

## When to use this skill

- Dock one or more ligands into a known or user-provided protein pocket
- Run a fast default docking workflow without manually choosing an engine
- Compare docking outcomes across multiple engines for robustness checks
- Use method-specific engines when the user explicitly requests one by name

## Method selection rule

Docking engines:
- Default to `Gnina` for generic docking requests.
- Use the named engine when the user explicitly names one of `Gnina`, `AutoDock Vina`, `PackDock`, `SurfDock`, or `DiffDock`.
- Use `PackDock` for flexible (side-chain repacking) docking.
- Use `SurfDock` when surface-geometry awareness is requested or the pocket is shallow/cryptic.
- Use `DiffDock` when blind docking or no pocket is provided.
- For comparison, benchmarking, or "try multiple methods" requests, invoke multiple engines and aggregate metrics.

Binding-site acquisition (run before docking when no `pocket_info` or `reference_ligand` is supplied):
- Use `fpocket` to acquire a **predicted** binding site (apo structure or no known ligand).

Pocket inputs:
- Pass `pocket_info` as `Center:x,y,z;Size:sx,sy,sz` or pass a `reference_ligand` file when the engine supports it.

## Prerequisites

1. `SCIMINER_API_KEY` is pre-obtained by the SciMiner-Hermes gateway before the agent run reaches this skill.
2. Use the runtime `SCIMINER_API_KEY` directly as the `X-Auth-Token` for SciMiner tool calls.
3. Do not request, derive, print, persist, or write this key to any file.

If `SCIMINER_API_KEY` is not available at skill runtime, stop and report that the gateway did not inject the required credential. Do not try to derive it inside the skill or switch to other tools or services.

## Authoritative payload source (required)

The registry at `molecular-docking/scripts/sciminer_registry.py` is the **single source of truth** for `provider_name`, `tool_name`, allowed `parameters`, and `file_params`. The agent MUST:

1. Resolve the selected tool via `get_tool_info(tool_name)` or `build_payload_from_registry(...)` before every invocation.
2. Never invent payload keys from memory.
3. Filter user-provided parameters against the registry's `parameters` keys.
4. Validate required parameters before invoking.
5. Cite `molecular-docking/scripts/sciminer_registry.py` as the payload source in summaries.

If a user-provided parameter is not present in the selected registry interface, ask for correction or drop it with an explanation.

## Invocation pattern

Always invoke via SciMiner's internal API using `BASE_URL`. Construct the payload from the registry, upload any file inputs, then submit and poll.

```python
import os
import requests
import time

# Adjust import path to runtime (e.g., sys.path or package layout)
from molecular_docking.scripts.sciminer_registry import build_payload_from_registry

BASE_URL = "https://sciminer.tech/console/api"
API_KEY = os.environ.get("SCIMINER_API_KEY")
if not API_KEY:
    raise RuntimeError("SCIMINER_API_KEY is not set; the gateway did not inject the required credential")

auth_header = {"X-Auth-Token": API_KEY}


def upload_file(path: str) -> str:
    """Upload a local file and return the SciMiner file_id."""
    with open(path, "rb") as fh:
        resp = requests.post(
            f"{BASE_URL}/v1/internal/tools/file",
            files={"file": fh},
            headers=auth_header,
            timeout=60,
        )
    resp.raise_for_status()
    return resp.json()["file_id"]


# 1. Upload file inputs and collect file_ids
receptor_id = upload_file("path/to/receptor.pdb")
ligand_id = upload_file("path/to/ligand.sdf")

# 2. Build payload strictly from registry metadata
user_parameters = {
    "receptor": receptor_id,
    "ligand_to_dock": ligand_id,
    "pocket_info": "Center:1.0,2.0,3.0;Size:20,20,20",
    "num_modes": 3,
}
payload = build_payload_from_registry("Gnina", user_parameters)

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

## File upload rules

- Upload every parameter listed in the registry's `file_params` via `/v1/internal/tools/file` before invocation.
- Replace local paths in `parameters` with the returned `file_id` strings.
- Skip `file_params` entries that the user did not provide; only required file params must be present.

## Expected result format

```json
{
    "status": "SUCCESS",
    "result": {...},
    "task_id": "xxx",
    "share_url": "https://sciminer.tech/share?id=<task_id>&type=API_TOOL"
}
```

## Included tools

### Gnina (default)
- provider_name: `Gnina`
- `get_gnina_result_from_pocket_center_picker_get_gnina_result_from_pocket_center_picker_post` — pocket-guided docking with optional reference ligand and configurable output modes

### AutoDock Vina
- provider_name: `AutoDock Vina`
- `vina_docking_from_pocket_center_picker_vina_docking_from_pocket_center_picker_post` — fast and widely used docking with explicit mode count

### PackDock
- provider_name: `PackDock`
- `dock_from_pocket_center_picker_dock_from_pocket_center_picker_post` — flexible docking with apo/holo conformer and Vina sampling controls

### SurfDock
- provider_name: `SurfDock`
- `run_surfdock_process_from_pocket_center_picker_run_surfdock_process_from_pocket_center_picker_post` — docking that integrates sequence, residue structure, and surface geometry

### DiffDock
- provider_name: `DiffDock`
- `diffdock_get_diffdock_info_post` — diffusion-model docking for protein-ligand complex pose prediction

### fpocket
- provider_name: `fpocket`
- `run_fpocket_run_fpocket_post` — predict protein binding pockets from an uploaded protein structure

## Workflow guidance

Standard single-engine docking:
1. If no `pocket_info` and no `reference_ligand`, run `fpocket` (predicted pocket) first.
2. Map the resulting pocket center/size into `pocket_info` for the chosen docking engine.
3. Invoke the docking engine via `build_payload_from_registry(...)`.

Multi-engine comparison:
- Build payloads for each requested engine independently from the registry.
- Submit in parallel; collect `task_id` and poll each.
- Report per-engine top pose, score, and `share_url`; flag consensus poses across engines.

General:
- Prefer registry-defined defaults; only override when the user provides a value.
- When `reference_ligand` is available, prefer it over manual `pocket_info` for engines that accept it.

## Notes

- Use SciMiner `BASE_URL` for all invocations.
- Use `molecular-docking/scripts/sciminer_registry.py` as the authoritative source for payload construction.
- This skill requires the `SCIMINER_API_KEY` environment variable to be injected by the SciMiner-Hermes gateway before skill execution. The API key is sent as the `X-Auth-Token` header.
- If `SCIMINER_API_KEY` is not available at skill runtime, stop and report that the gateway did not inject the required credential. Do not attempt to derive or locate the API key through other means.
- Upload file inputs through `/v1/internal/tools/file` and pass returned `file_id` values.
- `provider_name` must exactly match the values in `molecular-docking/scripts/sciminer_registry.py`.
- Important: when summarizing results to users, attach the `share_url` links of every successful task at the end.

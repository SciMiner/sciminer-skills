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
- `Gnina` -> `Gnina_api_doc.md`
- `AutoDock Vina` -> `AutoDock Vina_api_doc.md`
- `PackDock` -> `PackDock_api_doc.md`
- Generic docking requests -> `Gnina`
- Requests that explicitly name an engine -> the named provider: `AutoDock Vina`, `PackDock`, `SurfDock`, or `DiffDock`
- Binding-pocket prediction before docking -> `fpocket`
- Multi-engine comparison or benchmarking -> run the requested provider set, using `Gnina` as the default when no engine is specified
   - Content-Type
   - Authentication header
   - Tool Name
   - Method
   - Parameter table, including required fields and enum values
   - File-upload instructions and example code
4. Choose the correct section if the selected doc contains multiple tool
   variants, such as reference-ligand input vs pocket-center input.
5. Cite the selected Markdown doc as the payload source in summaries.

If a user-provided parameter is not present in the selected Markdown doc
section, ask for correction or drop it with an explanation.

## Required workflow

1. Determine which docking engine or engine set matches the user's request.
2. When no pocket input is available, run the supporting pocket-detection step
   first and then read the corresponding docking tool docs.
3. Read the selected tool Markdown file or files from
   `https://sciminer.tech/tool_api_files/`.
4. Choose the doc section that matches the user's input shape.
5. Collect any missing required parameters from the user.
6. Upload required file inputs exactly as described by the selected Markdown
   doc and replace local paths with returned `file_id` values.
7. Write or run the invocation code directly from the selected Markdown doc's
   base-information block, parameter table, file-upload instructions, and
   example code. Do not apply a shared invocation template or local registry
   abstraction in this skill.
8. Poll the task result and return the `share_url` in the final user-facing
   summary.

## File upload rules

- Upload every required file parameter described by the selected Markdown doc
    before invocation.
- Replace local paths in `parameters` with the returned `file_id` strings.
- Use the upload form field documented by the selected Markdown doc.
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

- Generic docking requests -> `Gnina`
- Requests that explicitly name an engine -> the named provider: `AutoDock Vina`, `PackDock`, `SurfDock`, or `DiffDock`
- Binding-pocket prediction before docking -> `fpocket`
- Multi-engine comparison or benchmarking -> run the requested provider set, using `Gnina` as the default when no engine is specified

## Notes

- Use the selected Markdown doc under
    `https://sciminer.tech/tool_api_files/` as the authoritative source for
    payload construction and invoke-method details.
- This skill requires the `SCIMINER_API_KEY` environment variable to be injected by the SciMiner-Hermes gateway before skill execution. The API key is sent as the `X-Auth-Token` header.
- If `SCIMINER_API_KEY` is not available at skill runtime, stop and report that the gateway did not inject the required credential. Do not attempt to derive or locate the API key through other means.
- `provider_name` must exactly match the selected Markdown doc.
- Use the selected Markdown doc to determine file inputs, parameter placement,
    and any tool-specific submission details.
- Important: when summarizing results to users, attach the `share_url` links of every successful task at the end.
- For long-running tasks without a fixed ETA, poll for no more than 6000 seconds; if the task is still running, stop polling and return the current `task_id` and `share_url` so the user can check later.

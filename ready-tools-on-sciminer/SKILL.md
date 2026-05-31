---
name: ready-tools-on-sciminer
description: Discover a user-specified SciMiner tool from the published API-doc index, read its Markdown description, and invoke it through the SciMiner internal API.
credential_files:
  - ~/.config/sciminer/credentials.json
---

# Ready Tools on SciMiner

This skill handles arbitrary SciMiner tools whose API descriptions are published
under `https://sciminer.tech/tool_api_files/`. When a user asks to use a
specific SciMiner tool, this skill retrieves the tool-doc index, resolves the
matching Markdown file, reads the document, and writes or runs invocation code
from the selected document's exact fields.

SciMiner calls must read the API key from `~/.config/sciminer/credentials.json`
and send it as the `X-Auth-Token`, and user-facing summaries must include the returned `share_url` for each
successful task.

## When to use this skill

- The user names a SciMiner tool and wants it invoked.
- The user asks how to call a specific SciMiner tool from code.
- The user wants the exact parameters, enums, file-upload behavior, or payload
  shape for a SciMiner tool.
- The user wants a shareable SciMiner result link after submission.

## Tool discovery rule

- Start from `https://sciminer.tech/tool_api_files/`.
- Treat the index page as the source of available SciMiner tool docs.
- Prefer exact, case-insensitive matching between the requested tool name and
  the linked file stem before `_api_doc.md`.
- Use the actual link returned by the index instead of constructing a guessed
  URL.
- If multiple tools plausibly match, ask the user to choose.
- If no match is found, report that the tool is not present in the current
  SciMiner tool-doc index.

Examples:

- `ADMET Predictor` -> `ADMET Predictor_api_doc.md`
- `AutoDock Vina` -> `AutoDock Vina_api_doc.md`
- `Graph-pKa` -> `Graph-pKa_api_doc.md`

## Authoritative payload source

The selected Markdown file under `https://sciminer.tech/tool_api_files/` is the
single source of truth for the chosen tool. The agent MUST:

1. Read the selected tool doc before every invocation.
2. Never invent `provider_name`, `tool_name`, parameter names, enum values,
  content type, submission flow, or upload-field names from memory.
3. Extract and follow the document's exact:
   - Base URL
   - API endpoint
   - Content-Type
   - Authentication header
   - Tool Name
  - Section-level tool method
   - Parameter table, including required fields and enum values
  - File-upload instructions and example submission payload structure
4. Select the correct variant if the doc contains multiple tool sections
   (for example, single-item vs batch, SMILES vs file input).
5. Reject or drop user-provided parameters that are absent from the selected doc
   section, with a brief explanation.

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

## Required workflow

1. Read the index at `https://sciminer.tech/tool_api_files/`.
2. Resolve the Markdown description file for the requested tool from the links
   actually present in the index.
3. Read the full Markdown document for the resolved tool.
4. Choose the tool section that matches the user's request shape.
5. Collect any missing required parameters from the user.
6. Upload any required file inputs and replace local paths with returned
   `file_id` values.
7. Submit the job using the exact `provider_name`, `tool_name`, endpoint,
  content type, and parameter names from the selected doc, following the
  document's example submission flow.
8. Poll for the task result.
9. Return the `share_url` in the final user-facing summary.

Write the invocation code directly from the selected Markdown document's base
information block, parameter table, file-upload instructions, and example code.
Do not apply a shared invocation template in this skill.

## File-upload rules

- Upload every required file parameter described by the selected Markdown doc
  before invocation.
- Replace local file paths in `parameters` with the returned `file_id` strings.
- Use the upload form field described by the selected doc. If the doc shows only
  the generic SciMiner upload example and does not override the form field, use
  `file`.
- Skip optional file parameters that the user did not provide.

## Expected result format

```json
{
  "status": "SUCCESS",
  "result": {"...": "..."},
  "task_id": "xxx",
  "share_url": "https://sciminer.tech/share?id=xxx&type=API_TOOL"
}
```

## Reporting rules

- Cite the selected Markdown doc under `https://sciminer.tech/tool_api_files/`
  as the payload source in your summary.
- Attach the `share_url` of every successful task at the end of the response so
  the user can view the online result.
- If polling reaches 600 seconds and the task is still running, stop polling and
  return the current `task_id` and `share_url` so the user can check later.
- Do not return raw file-download links when a `share_url` is available.
- Do not expose the API key in code snippets, logs, or summaries.

## Notes

- This skill is intentionally generic. It should not hard-code tool-specific
  payload schemas beyond what the selected SciMiner Markdown doc states.
- The tool-doc index currently exposes Markdown files named
  `<Tool Name>_api_doc.md`; rely on the live index rather than assuming the file
  exists.
- When the user asks to "use tool X", the first action is to resolve and read
  tool X's Markdown doc, not to infer parameters from memory.
- This skill defines its own credential and `share_url` handling rules and does
  not rely on another skill document.
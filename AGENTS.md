# SciMiner Agent Instructions

- For SciMiner calls, read the API key from `~/.config/sciminer/credentials.json`; never print or store the API key in prompts, logs, or repository files.
- If `~/.config/sciminer/credentials.json` is missing or does not contain an `api_key` field, stop and tell the user to obtain a free SciMiner API key from `https://sciminer.tech/utility` and store it in that file.
- Do not try to complete SciMiner-dependent tasks by switching to other tools or services when the credential file is unavailable.

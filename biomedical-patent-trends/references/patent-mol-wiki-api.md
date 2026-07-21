# Patent-Mol-Wiki download API

Source: user-supplied `Patent-Mol-Wiki_api_doc.md` (accessed 2026-07-20). Read the current provider documentation again if the endpoint or result format changes.

## Request

- Base URL: `https://sciminer.tech/console/api`
- Submit: `POST /v1/internal/tools/invoke`
- Poll: `GET /v1/internal/tools/result?task_id=...`
- Headers: `X-Auth-Token: <API key>` and JSON content type.
- Provider: `Patent-Mol-Wiki`
- Tool: `download_wiki_data_download_wiki_data_post`

Invoke with `parameters.date_range` set to one of `recent_week`, `recent_month`, `recent_quarter`, `recent_half_year`, or `recent_year`; set `patent_ids` to comma/newline-separated IDs for an ID-based request; and set `include_pdf` when a separate PDF ZIP is required. Patent IDs override date range. The submission returns a `task_id`; poll until `SUCCESS` or `FAILURE`.

Use the bundled downloader rather than copying credentials into source files. It stores the raw result because the API result payload may evolve, recursively finds HTTPS download URLs, downloads ZIP results, and safely extracts them.

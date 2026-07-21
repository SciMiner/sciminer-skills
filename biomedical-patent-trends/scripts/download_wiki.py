#!/usr/bin/env python3
"""Download and safely extract a Patent-Mol-Wiki package without persisting credentials."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

import requests

BASE_URL = "https://sciminer.tech/console/api"
INVOKE_URL = f"{BASE_URL}/v1/internal/tools/invoke"
RESULT_URL = f"{BASE_URL}/v1/internal/tools/result"
VALID_RANGES = {"recent_week", "recent_month", "recent_quarter", "recent_half_year", "recent_year"}


def api_key() -> str:
    credential_file = Path.home() / ".config" / "sciminer" / "credentials.json"
    if credential_file.exists():
        try:
            value = json.loads(credential_file.read_text(encoding="utf-8")).get("api_key")
        except (json.JSONDecodeError, OSError):
            value = None
        if value:
            return str(value)
    raise SystemExit("SciMiner credentials are required at ~/.config/sciminer/credentials.json with an api_key field.")


def find_urls(value: Any) -> list[str]:
    urls: list[str] = []
    if isinstance(value, dict):
        for item in value.values():
            urls.extend(find_urls(item))
    elif isinstance(value, list):
        for item in value:
            urls.extend(find_urls(item))
    elif isinstance(value, str):
        if value.startswith(("https://", "http://")):
            urls.append(value)
        else:
            try:
                urls.extend(find_urls(json.loads(value)))
            except json.JSONDecodeError:
                pass
    return list(dict.fromkeys(urls))


def safe_extract(archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive) as zf:
        root = destination.resolve()
        for member in zf.infolist():
            target = (destination / member.filename).resolve()
            if target != root and root not in target.parents:
                raise RuntimeError(f"Refusing unsafe ZIP member: {member.filename}")
        zf.extractall(destination)


def download(url: str, destination: Path, headers: dict[str, str]) -> None:
    with requests.get(url, headers=headers, stream=True, timeout=120) as response:
        response.raise_for_status()
        with destination.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)


def archive_name(url: str, number: int) -> str:
    parsed = urlparse(url)
    storage_path = parse_qs(parsed.query).get("storage_file_path", [""])[0]
    name = Path(unquote(storage_path)).name or Path(unquote(parsed.path)).name
    return name if name and name != "custom_tool_files" else f"wiki_package_{number}.zip"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date-range", default="recent_week", choices=sorted(VALID_RANGES))
    parser.add_argument("--patent-ids", help="Comma- or newline-separated patent IDs; overrides --date-range.")
    parser.add_argument("--include-pdf", action="store_true")
    parser.add_argument("--outdir", required=True, type=Path)
    parser.add_argument("--task-id", help="Resume polling an existing provider task instead of submitting a new one.")
    parser.add_argument("--poll-seconds", type=float, default=2)
    parser.add_argument("--max-polls", type=int, default=300)
    args = parser.parse_args()

    outdir = args.outdir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    headers = {"X-Auth-Token": api_key(), "Content-Type": "application/json"}
    parameters = {
        "date_range": args.date_range,
        "patent_ids": args.patent_ids or "",
        "include_pdf": args.include_pdf,
    }
    manifest_path = outdir / "download_manifest.json"
    if args.task_id:
        task_id = args.task_id
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        else:
            manifest = {"task_id": task_id, "resumed_at_utc": datetime.now(timezone.utc).isoformat(), "parameters": parameters, "archives": []}
    else:
        payload = {
            "provider_name": "Patent-Mol-Wiki",
            "tool_name": "download_wiki_data_download_wiki_data_post",
            "parameters": parameters,
        }
        submitted = requests.post(INVOKE_URL, json=payload, headers=headers, timeout=30)
        submitted.raise_for_status()
        task_id = submitted.json().get("task_id")
        if not task_id:
            raise RuntimeError("The service returned no task_id.")
        manifest = {"task_id": task_id, "submitted_at_utc": datetime.now(timezone.utc).isoformat(), "parameters": parameters, "archives": []}
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Submitted provider task: {task_id}")

    result: dict[str, Any] = {}
    for attempt in range(1, args.max_polls + 1):
        response = requests.get(RESULT_URL, params={"task_id": task_id}, headers=headers, timeout=20)
        response.raise_for_status()
        result = response.json()
        status = result.get("status")
        print(f"Poll {attempt}/{args.max_polls}: {status}")
        if status == "SUCCESS":
            break
        if status == "FAILURE":
            raise RuntimeError(f"Provider task failed: {result.get('result')}")
        time.sleep(args.poll_seconds)
    else:
        raise TimeoutError(f"Task {task_id} did not finish after {args.max_polls} polls.")

    (outdir / "provider_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    manifest["retrieved_at_utc"] = datetime.now(timezone.utc).isoformat()
    manifest["parameters"] = parameters
    manifest["archives"] = []
    urls = find_urls(result.get("result", result))
    if not urls:
        raise RuntimeError("Task succeeded but no HTTP(S) download URL was found. Inspect provider_result.json.")
    for number, url in enumerate(urls, start=1):
        name = archive_name(url, number)
        archive = outdir / name
        download(url, archive, headers)
        with archive.open("rb") as handle:
            digest = hashlib.file_digest(handle, "sha256").hexdigest()
        item: dict[str, Any] = {"url": url, "path": str(archive), "sha256": digest}
        if zipfile.is_zipfile(archive):
            extracted = outdir / archive.stem
            extracted.mkdir(exist_ok=True)
            safe_extract(archive, extracted)
            item["extracted_to"] = str(extracted)
        manifest["archives"].append(item)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(urls)} download(s) in {outdir}")


if __name__ == "__main__":
    main()

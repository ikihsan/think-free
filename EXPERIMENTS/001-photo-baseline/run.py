"""Read-only prior-art baseline check; does not run or connect to Immich."""

from __future__ import annotations

import base64
import hashlib
import io
import json
from pathlib import Path
import platform
import re
import urllib.request
import zipfile


REVISION = "54ec80b139e357b0039f8f3251d9ba6463ca6232"
BASE = f"https://raw.githubusercontent.com/gthb/immich-go/{REVISION}/"
MAX_DOWNLOAD = 2_000_000


def download(name: str) -> bytes:
    request = urllib.request.Request(BASE + name, headers={"User-Agent": "Project-Origin-research"})
    with urllib.request.urlopen(request, timeout=20) as response:
        data = response.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        raise ValueError("Artifact exceeds predeclared download limit")
    return data


def run() -> dict:
    artifacts = {name: download(name) for name in (
        "repro-takeout.zip", "api-trace-excerpt.txt", "immich-go-run.log"
    )}
    source = {}
    with zipfile.ZipFile(io.BytesIO(artifacts["repro-takeout.zip"])) as archive:
        if sum(info.file_size for info in archive.infolist()) > MAX_DOWNLOAD:
            raise ValueError("Expanded fixture exceeds size limit")
        for info in archive.infolist():
            if info.filename.lower().endswith(".jpg"):
                content = archive.read(info)
                digest = base64.b64encode(hashlib.sha1(content).digest()).decode("ascii")
                if digest in source:
                    raise ValueError("Expected distinct synthetic images")
                source[digest] = info.filename
    if len(source) != 4:
        raise ValueError(f"Expected four generated JPEGs, found {len(source)}")

    # The trace is a published excerpt, not a complete destination snapshot.
    trace = "\n".join(line.strip() for line in artifacts["api-trace-excerpt.txt"].decode("utf-8").splitlines())
    active = {}
    created = []
    deleted = []
    operations = re.split(r"(?m)(?=^(?:POST|PUT|DELETE) /api/)", trace)
    for operation in operations:
        if re.match(r"POST /api/assets\s+->\s+201 Created", operation):
            checksum = re.search(r"X-Immich-Checksum: ([A-Za-z0-9+/=]+)", operation)
            response = re.search(r"(?m)^response:\s*(\{.*\})$", operation)
            if checksum is None or response is None:
                raise ValueError("Unrecognized creation trace")
            asset_id = json.loads(response.group(1))["id"]
            digest = checksum.group(1)
            if digest not in source:
                raise ValueError("Creation checksum not in source fixture")
            active[asset_id] = digest
            created.append(asset_id)
        elif re.match(r"DELETE /api/assets\s+->\s+204 No Content", operation):
            request = re.search(r"(?m)^request:\s*(\{.*\})$", operation)
            if request is None:
                raise ValueError("Unrecognized deletion trace")
            for asset_id in json.loads(request.group(1))["ids"]:
                if asset_id not in active:
                    raise ValueError("Deletion references unknown created asset")
                del active[asset_id]
                deleted.append(asset_id)

    missing = set(source) - set(active.values())
    missing_names = sorted(Path(source[digest]).name for digest in missing)
    expected_missing = ["REPRO_eaaed6cd_A-edited.jpg", "REPRO_eaaed6cd_B.jpg"]
    controls = {
        "complete_destination_has_no_missing_content": not (set(source) - set(source)),
        "renaming_preserves_content_identity": set(source) == set({key: f"renamed-{i}.jpg" for i, key in enumerate(source)}),
        "accepted_operations_match_reported_missing_contents": missing_names == expected_missing,
        "expected_trace_operation_counts": len(created) == 3 and len(deleted) == 1,
        # Deliberately retain content identity while removing semantic edges.
        "checksum_blind_to_relationship_only_loss": not (set(source) - set(source))
            and {("original-A", "edited-A")} != set(),
    }
    if not all(controls.values()):
        raise AssertionError(controls)
    log = artifacts["immich-go-run.log"].decode("utf-8")
    summaries = [line for line in log.splitlines() if "Errors" in line or "error(s)" in line]
    return {
        "experiment": "E001",
        "python": platform.python_version(),
        "source_revision": REVISION,
        "artifacts": {name: {"url": BASE + name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()} for name, data in artifacts.items()},
        "source_files": [{"name": name, "trace_sha1_base64": digest} for digest, name in sorted(source.items())],
        "created_assets_in_excerpt": len(created),
        "accepted_deletions_in_excerpt": len(deleted),
        "accepted_operation_model_remaining_assets": len(active),
        "missing_files_detected_by_plain_checksum_set_difference": missing_names,
        "importer_log_error_summary_lines": summaries,
        "controls": controls,
        "decision": "Motivating content-loss example does not establish an advantage over source-relative checksum comparison. Semantic-only cases and real destination observation remain separate untested opportunities.",
        "limitations": [
            "Published generated fixture and trace, not independent live reproduction.",
            "Accepted deletion may complete asynchronously or fail; model is not a measured final server state.",
            "No current importer version tested; no conclusion about whether the bug is fixed.",
            "Checksum equality does not establish preserved dates, albums, stacks, or tags.",
            "Not an implementation or benchmark of rclone or other existing audit tools.",
            "No user usefulness, novelty, or adoption measured.",
        ],
    }


if __name__ == "__main__":
    results = run()
    output = Path(__file__).with_name("results.json")
    output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))

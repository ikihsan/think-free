"""Repair session 008's stream: 181 lines over 162 sequence numbers.

Run from the repository root:

    PYTHONPATH=tools:tests python3 sessions/2026-10-08-013-e063-run-the-e062-answerability-instrume/repair-008.py

It refuses to run unless the duplication it repairs is present and unless
dropping the later copy of each repeated number loses no `unlogged_change` path.
Session `2026-10-08-013` did this by hand and wrote down what it checked in
`DEDUPE-008.md`; this script makes the checks repeatable rather than a claim.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

TARGET = Path(
    "sessions/2026-10-08-008-record-the-last-unlogged-paths-and-commi/events.jsonl"
)
BACKUP = Path(".origin/session-008-pre-repair.jsonl")


def unlogged_paths(raw: list[dict]) -> set:
    return {
        e["data"].get("path")
        for e in raw
        if e.get("kind") == "unlogged_change"
    }


def main() -> int:
    if not TARGET.exists():
        print(f"nothing to repair: {TARGET} is absent")
        return 0
    lines = [l for l in TARGET.read_text(encoding="utf-8").splitlines() if l.strip()]
    raw = [json.loads(l) for l in lines]
    numbers = [e["seq"] for e in raw]
    if numbers == list(range(1, len(numbers) + 1)):
        print(f"already contiguous over {len(numbers)} events; nothing to do")
        return 0

    seen: set = set()
    kept: list[dict] = []
    dropped: list[int] = []
    for event in raw:
        if event["seq"] in seen:
            dropped.append(event["seq"])
            continue
        seen.add(event["seq"])
        kept.append(event)

    before, after = unlogged_paths(raw), unlogged_paths(kept)
    problems = []
    if [e["seq"] for e in kept] != list(range(1, len(kept) + 1)):
        problems.append("kept events are still not 1..n contiguous")
    if after != before:
        problems.append(
            f"dedupe would lose paths: {sorted(before - after)[:5]} "
            f"({len(before - after)} of {len(before)})"
        )
    if len(kept) != max(numbers):
        problems.append(f"kept {len(kept)} events but max seq is {max(numbers)}")
    if kept and kept[-1].get("kind") != "session_end":
        problems.append(f"last event is {kept[-1].get('kind')!r}, not session_end")
    if problems:
        for problem in problems:
            print(f"REFUSING: {problem}")
        return 4

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_text(TARGET.read_text(encoding="utf-8"), encoding="utf-8")
    TARGET.write_text(
        "".join(json.dumps(e, sort_keys=True, ensure_ascii=False) + "\n" for e in kept),
        encoding="utf-8",
    )
    print(
        f"repaired: {len(lines)} lines over {max(numbers)} numbers -> "
        f"{len(kept)} events, 1..{len(kept)}; dropped repeated numbers "
        f"{sorted(set(dropped))}"
    )
    print(f"unlogged_change paths before {len(before)}, after {len(after)}, lost 0")
    print(f"pre-repair bytes kept at {BACKUP}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

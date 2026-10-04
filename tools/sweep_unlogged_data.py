#!/usr/bin/env python3
"""Which data-suffix files did closed sessions change without declaring?

Task T-0050's measurement, and the reason it is a script rather than a sentence:
the repair makes every `.json`, `.jsonl` and `.log` edit reportable, and the
number of reports that would appear is not something to guess at. It reads git
and the committed session streams and writes nothing into the repository.

    python3 tools/sweep_unlogged_data.py [--root REPO] [--all] [--verbose]

What it answers, per closed session: which data-suffix paths the session's window
contains that no artifact event declared, no command declared by its bytes, that
are not generated, not the session's own directory, and not attributed to a base
move the session recorded. Those are the reports the repair adds.

Two approximations, both stated rather than hidden:

* The window is `[the commit the session started from, the commit whose subject
  names this session]`, or failing that the newest commit that wrote the
  session's own stream. Two VMs interleaving on the shared base means a window
  can contain a colleague's paths — which is why another session's
  `sessions/<id>/events.jsonl` appears here at all, and why the per-path counts
  are lower than the per-pair total.
* A path is attributed to the base the way `landed.landed_paths` does it: the
  newest thing that touched it is a commit this session recorded as arriving.
  What is left is what reconciliation itself would report for that window.

`--all` keeps the paths of other sessions' streams in the count instead of
dropping them, which is the conservative reading: they are reports a rule written
per-session cannot avoid.
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from originlib import declaredwrite, doclint, paths, reconcile  # noqa: E402

MARK = "session: "


def git(root: pathlib.Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=str(root), capture_output=True, text=True, check=False
    )
    return result.stdout if result.returncode == 0 else ""


def session_windows(root: pathlib.Path) -> dict:
    """Session id -> the commit that closed it, from the log's own subjects."""
    closed: dict[str, str] = {}
    for line in git(root, "log", "--format=%H%x1f%s").splitlines():
        sha, _, subject = line.partition("\x1f")
        if subject.startswith(MARK):
            closed.setdefault(subject[len(MARK):].split(" ")[0], sha)
    return closed


def newest_touching(root: pathlib.Path, since: str, rel: str) -> str:
    """The newest commit after `since` that wrote `rel`, or ""."""
    log = git(root, "log", "--format=%H", f"{since}..HEAD", "--", rel).splitlines()
    return log[-1] if log else ""


def has_generated_mark(root: pathlib.Path, at: str, rel: str) -> bool:
    """Does the blob at `at` carry a generated-file mark in its first 2 KiB?

    `reconcile._is_generated` reads the working tree; this reads the tree as the
    session left it, because a later session may have rewritten the file.
    """
    blob = subprocess.run(
        ["git", "show", f"{at}:{rel}"], cwd=str(root), capture_output=True, text=True,
        check=False,
    )
    if blob.returncode != 0:
        return False
    return reconcile.GENERATED_MARK in blob.stdout[:2048]


def declared_by_bytes(root: pathlib.Path, stream: list[dict], rel: str) -> bool:
    """Did any `task_rewrite` event in this stream still describe `rel`?

    Evaluated at `root` as it is now, which is what reconciliation does — and the
    reason a second append invalidates the first declaration is visible here as a
    difference between the two, not as a claim about history.
    """
    for event in stream:
        if event.get("kind") != "task_rewrite" or event.get("data", {}).get("path") != rel:
            continue
        if declaredwrite.matches(root / rel, event.get("data", {})):
            return True
    return False


def arrived_paths(root: pathlib.Path, stream: list[dict], rel: str) -> bool:
    """Did this session's recorded base move bring `rel` in, and nothing since?

    The attribution `landed.landed_paths` makes: the newest thing that touched
    the path is a commit this session recorded as arriving from the shared base.
    Written as a helper because the one-line form is unreadable and this is the
    clause that decides whether a colleague's path is counted.
    """
    arrived = {
        sha
        for event in stream
        if event["kind"] == "base_advance"
        for sha in (event["data"].get("commits") or [])
    }
    if not arrived:
        return False
    newest = git(root, "log", "--format=%H", "-1", "--", rel).split()
    return bool(newest) and newest[0] in arrived


def sweep(root: pathlib.Path, keep_colleagues: bool) -> dict:
    closed = session_windows(root)
    counts: collections.Counter = collections.Counter()
    examples: dict[str, list[str]] = {}
    buckets: collections.Counter = collections.Counter()
    streams = sorted(root.glob("sessions/*/events.jsonl"))
    for stream_path in streams:
        sid = stream_path.parent.name
        stream = [json.loads(line) for line in stream_path.read_text().splitlines() if line.strip()]
        start = next((e for e in stream if e["kind"] == "session_start"), None)
        if start is None:
            buckets["no session_start"] += 1
            continue
        opened = start["git"]["head"]
        closed_at = closed.get(sid) or newest_touching(root, opened, f"sessions/{sid}/events.jsonl")
        if not closed_at:
            buckets["no window"] += 1
            continue
        declared = {
            e["data"]["path"]
            for e in stream
            if e["kind"] == "artifact" and e["data"].get("path")
        }
        window = git(root, "diff", "--name-only", f"{opened}..{closed_at}").splitlines()
        for rel in window:
            if pathlib.Path(rel).suffix not in doclint.DATA_SUFFIXES:
                continue
            mine = rel.startswith(f"sessions/{sid}/") or rel == "sessions/active.json"
            colleague = rel.startswith("sessions/") and not mine
            if rel in declared:
                buckets["declared as an artifact"] += 1
            elif declared_by_bytes(root, stream, rel):
                buckets["declared by a command's bytes"] += 1
            elif mine:
                buckets["the session's own directory"] += 1
            elif colleague and not keep_colleagues:
                buckets["another session's stream"] += 1
            elif reconcile._is_vendored(rel):
                buckets["a declared exempt glob"] += 1
            elif has_generated_mark(root, closed_at, rel):
                buckets["carries the generated mark"] += 1
            elif arrived_paths(root, stream, rel):
                buckets["attributed to a recorded base move"] += 1
            else:
                counts[rel] += 1
                examples.setdefault(rel, []).append(sid)
    return {"counts": counts, "examples": examples, "buckets": buckets, "sessions": len(streams)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=None, help="repository to sweep (default: this one)")
    parser.add_argument(
        "--all", action="store_true",
        help="count another session's stream as a report rather than a window artefact",
    )
    args = parser.parse_args()
    root = pathlib.Path(args.root).resolve() if args.root else paths.repo_root()
    result = sweep(root, args.all)
    print(f"sessions swept: {result['sessions']}")
    for reason, count in result["buckets"].most_common():
        print(f"  excluded, {reason}: {count}")
    total = sum(result["counts"].values())
    print(f"\n=== newly reportable once the suffix stops being an exemption ===")
    print(f"{total} (session, path) pairs over {len(result['counts'])} distinct paths")
    for rel, count in result["counts"].most_common():
        print(f"{count:4d}  {rel}")
        print(f"      e.g. {', '.join(result['examples'][rel][:2])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

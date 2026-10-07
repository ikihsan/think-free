#!/usr/bin/env python3
"""E046 run: every address of every real change, staged for real, judged by git.

    python3 run.py [--max-addresses N] [--only STRATUM] [--raw PATH]

Writes one JSON object per row to raw/results.jsonl and prints the tally. Exit 3
if an *instrument* control fails -- the positive control must reproduce E038's
30/30 and the negative control must reject every wrong index state. The
real-change rows are data: a failing kill gate is reported, not turned into a
green exit.
"""

import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(EXP, "038-staging-prior-art"))

from harness import git, stg
from replay import Replay                              # noqa: E402
from controls import controls, stage_once                       # noqa: E402

MAX_ADDRESSES = 60


def sha1(data):
    import hashlib
    return hashlib.sha1(data).hexdigest() if data is not None else None


def load_manifest(repos=None):
    """Every case, with its two file versions read back.

    The bytes come from `raw/fixtures/` when a previous harvest wrote them, and
    otherwise from the repository itself via `git show <commit>:<path>`. The
    manifest records the blob id of each, so both routes are checkable:
    `hashlib.sha1(blob)` against `pre_blob_sha1` / `post_blob_sha1`.
    """
    rows = []
    with open(os.path.join(HERE, "raw", "manifest.jsonl")) as fh:
        for line in fh:
            c = json.loads(line)
            base = os.path.join(HERE, "raw", "fixtures", c["case_id"])
            if os.path.exists(base + ".pre"):
                with open(base + ".pre", "rb") as f:
                    c["pre_blob"] = f.read()
                with open(base + ".post", "rb") as f:
                    c["post_blob"] = f.read()
            else:
                repo = (repos or {}).get(c["repo"])
                if repo is None:
                    raise SystemExit(
                        "no fixture for %s and no --repo %s=PATH given; the "
                        "manifest records the commit and both blob ids, so "
                        "`git show %s:%s` in %s reproduces it"
                        % (c["case_id"], c["repo"], c["commit"], c["path"],
                           c["repo_url"]))
                old = c["old_path"] if c["status"].startswith("D") else \
                    (c["path"] if c["status"].startswith("A") else c["old_path"])
                c["pre_blob"] = git(["show", "%s^:%s" % (c["commit"], old)],
                                    repo)[1]
                c["post_blob"] = b"" if c["status"].startswith("D") else \
                    git(["show", "%s:%s" % (c["commit"], c["path"])], repo)[1]
            rows.append(c)
    return rows



def run_case(case, root, max_addresses):
    replay = Replay(root, case)
    rc, out, err = stg(["list", "--json"], replay.repo)
    rows = []
    if rc not in (0, 1):
        return [{"case_id": case["case_id"], "stratum": case["stratum"],
                 "row": "list_failed", "exit": rc, "stderr": err.strip()[:300]}]
    listed = [r for r in json.loads(out) if r.get("change")]
    if not listed:
        return [{"case_id": case["case_id"], "stratum": case["stratum"],
                 "row": "no_addresses", "exit": rc}]
    addresses = listed[:max_addresses]
    for r in addresses:
        c = r["change"]
        rc2, detail, index_blob = stage_once(replay, case, c)
        rows.append({
            "index_sha1": sha1(index_blob),
            "case_id": case["case_id"], "stratum": case["stratum"],
            "repo": case["repo"], "commit": case["commit"], "path": case["path"],
            "row": "address", "anchor": c["anchor"], "kind": c["kind"],
            "declared": [c["old_start"], c["old_lines"],
                         c["new_start"], c["new_lines"]],
            "exit": rc2,
            "verdict": detail.pop("verdict", "refused"),
            "detail": detail,
        })
    if len(listed) > max_addresses:
        rows.append({"case_id": case["case_id"], "stratum": case["stratum"],
                     "row": "addresses_truncated", "listed": len(listed),
                     "tried": max_addresses})
    replay.reset()
    # Is this replay a faithful one? `git add` on the path must reproduce the
    # post-image, and nothing else can: if plain staging does not land the file
    # the real commit produced, the tree is not the tree that commit describes and
    # no completeness result from it means anything. This is what excludes the
    # rename strata, where the replayed tree makes git diff only part of the file.
    git(["add", "--", case["path"]], replay.repo)
    faithful = replay.index_blob() == case["post_blob"]
    rc3, out3, err3 = stg(["split", "--all", case["path"]], replay.repo)
    got = replay.index_blob()
    ok = (got == case["post_blob"]) if faithful else None
    rows.append({"case_id": case["case_id"], "stratum": case["stratum"],
                 "row": "completeness", "exit": rc3, "ok": ok,
                 "applicable": faithful,
                 "why_not": None if faithful else
                 "`git add` on the replayed path does not reproduce the "
                 "post-image either, so the tree is not the tree this commit "
                 "describes and split --all is not a test of anything here",
                 "expected_bytes": len(case["post_blob"]),
                 "index_bytes": len(got) if got is not None else None,
                 "stderr": err3.strip()[:300] if ok is False else ""})
    return rows

def main(argv):
    max_addresses = MAX_ADDRESSES
    only = None
    raw = os.path.join(HERE, "raw", "results.jsonl")
    repos = {}
    i = 1
    while i < len(argv):
        if argv[i] == "--repo":
            label, _, path = argv[i + 1].partition("=")
            repos[label] = path
            i += 2
            continue
        if argv[i] == "--max-addresses":
            max_addresses = int(argv[i + 1])
            i += 2
        elif argv[i] == "--only":
            only = argv[i + 1]
            i += 2
        elif argv[i] == "--raw":
            raw = argv[i + 1]
            i += 2
        else:
            raise SystemExit(__doc__)

    cases = load_manifest(repos)
    if only:
        cases = [c for c in cases if c["stratum"] == only]
    if not cases:
        raise SystemExit("no cases selected")

    rows = []
    root = tempfile.mkdtemp(prefix="e043-")
    try:
        pos_rows, pos_ok, neg_rows, neg_flagged = controls(root, max_addresses)
        neg_real = [r for r in neg_rows if r["verdict"] != "not_wrong"]
        print("positive control: %d/%d rows exact" % (pos_ok, len(pos_rows)))
        print("negative control: %d/%d wrong index states rejected (%d injections "
              "were not wrong and were skipped)"
              % (neg_flagged, len(neg_real), len(neg_rows) - len(neg_real)))
        for c in cases:
            rows.extend(run_case(c, root, max_addresses))
    finally:
        shutil.rmtree(root, ignore_errors=True)

    with open(raw, "w") as fh:
        for r in pos_rows:
            fh.write(json.dumps(dict(r, row="positive_control"), sort_keys=True) + "\n")
        for r in neg_rows:
            fh.write(json.dumps(dict(r, row="negative_control"), sort_keys=True) + "\n")
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")

    tally = {}
    for r in rows:
        if r["row"] != "address":
            continue
        key = (r["stratum"], r["verdict"])
        tally[key] = tally.get(key, 0) + 1
    print("\nverdict by stratum (address rows):")
    for stratum in sorted(set(k[0] for k in tally)):
        parts = ["%s=%d" % (k[1], v) for k, v in sorted(tally.items())
                 if k[0] == stratum]
        print("  %-18s %s" % (stratum, " ".join(parts)))
    comp = [r for r in rows if r["row"] == "completeness"]
    checked = [r for r in comp if r["ok"] is not None]
    print("\ncompleteness: %d of %d applicable cases reproduce the post-image "
          "(%d not applicable, reason recorded per row)"
          % (sum(1 for r in checked if r["ok"]), len(checked),
             len(comp) - len(checked)))
    for r in checked:
        if not r["ok"]:
            print("  INCOMPLETE %s (%s): %s" % (r["case_id"], r["stratum"],
                                                r["stderr"][:120]))
    if pos_ok != len(pos_rows) or neg_flagged != len(neg_real):
        print("\nINSTRUMENT CONTROL FAILED -- the run is void")
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
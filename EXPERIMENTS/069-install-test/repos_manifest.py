#!/usr/bin/env python3
"""Write repos/MANIFEST.json for E069: repo, arm, local path, origin url, commit sha.

The 20 test repositories were fetched by E068's fetch_repos.py. This records the
commit each checkout is at, so E069's results name the bytes they came from and
re-running is pinned. One sh clone, no submodules, no history.
"""

import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPOS = BASE.parent / "068-arxiv-spec-generator" / "repos"
EXTRACTED = BASE.parent / "068-arxiv-spec-generator" / "cache" / "extracted.json"
OUT = BASE / "repos" / "MANIFEST.json"


def git(path, *args):
    proc = subprocess.run(["git", "-C", str(path)] + list(args), capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main():
    data = json.loads(EXTRACTED.read_text())
    rows = data["test_repos"]
    out = []
    for row in rows:
        key = "%s/%s" % (row["owner"], row["repo"])
        arm_dir = REPOS / row["arm"]
        candidates = sorted(p for p in arm_dir.iterdir() if p.is_dir()) if arm_dir.is_dir() else []
        # fetch_repos.py names the directory <owner>_<repo> with / flattened to _.
        want = ("%s_%s" % (row["owner"], row["repo"]))
        hit = next((p for p in candidates if p.name == want), None)
        if hit is None:
            hit = next((p for p in candidates if p.name.startswith(row["repo"].replace(".", "_"))), None)
        if hit is None:
            print("MISSING %s (looked under %s)" % (key, arm_dir), file=sys.stderr)
            continue
        code, sha, _ = git(hit, "rev-parse", "HEAD")
        _, url, _ = git(hit, "config", "--get", "remote.origin.url")
        out.append({
            "owner": row["owner"],
            "repo": row["repo"],
            "arm": row["arm"],
            "path": str(hit.relative_to(BASE.parent.parent)),
            "origin": url,
            "commit": sha if code == 0 else None,
            "clone_state": "complete" if code == 0 else "incomplete",
        })
        print("%-50s %s %s" % (key, out[-1]["clone_state"], sha[:12]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "note": "shallow clones made by E068 fetch_repos.py; commit is the single fetched tip",
        "fetch": "git clone --depth 1 <origin> <path>",
        "repos": out,
    }, indent=1))
    incomplete = [r for r in out if r["clone_state"] != "complete"]
    print("\n%d repos recorded, %d incomplete" % (len(out), len(incomplete)))
    for r in incomplete:
        print("  incomplete: %s/%s" % (r["owner"], r["repo"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

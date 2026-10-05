"""E020: authoritative `.claude/` tree capture by shallow clone, replacing the
falsified marker-file probe.

Why the replacement was necessary: `.claude/agents/README.md` returning 404 does
not mean `.claude/agents/` is absent. Validated against the contents API on 8
repos: 8 of 8 disagreed with the marker probe, and 6 had directories the probe
missed. Any figure from the marker probe is retracted.

Why a clone rather than more API calls: the contents API is 60 requests/hour
unauthenticated and E020 already spent 13. `git clone --depth 1` reads the whole
tree with no rate limit, so the tree becomes authoritative rather than sampled.

This is the declared structural-attribution channel A5 run properly: a copied
`.claude/` DIRECTORY is detected by files that are byte-identical across
repositories, which needs no credit to be given -- and configuration is anonymous
by construction, so no README rule could ever have found it.
"""

import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "raw")
CLONES = os.path.join(RAW_DIR, "clones")
# Clone outside the repository: a working tree is a session artifact, not a
# finding, and .gitignore does not cover it.
CLONES = "/tmp/opencode/e020-clones"

UA = "think-free-research"


def sh(cmd, cwd=None, timeout=180):
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = p.communicate()
    return p.returncode, out.decode("utf-8", "replace")


def main():
    pop = json.load(open(os.path.join(RAW_DIR, "population.json")))
    repos = [r["repo"] for r in pop["rows"] if r["settings_state"] == "PRESENT"]
    if not os.path.isdir(CLONES):
        os.makedirs(CLONES)

    trees = {}
    for repo in repos:
        dest = os.path.join(CLONES, repo.replace("/", "__"))
        if not os.path.isdir(dest):
            rc, out = sh(["git", "clone", "--depth", "1", "--quiet",
                          "https://github.com/%s.git" % repo, dest])
            if rc != 0:
                sys.stderr.write("CLONE-FAIL %-46s %s\n" % (repo, out.strip()[:90]))
                trees[repo] = {"state": "UNDECIDABLE", "reason": "clone failed"}
                continue
            time.sleep(0.5)
        root = os.path.join(dest, ".claude")
        if not os.path.isdir(root):
            trees[repo] = {"state": "ABSENT", "files": {}}
            continue
        files = {}
        for dirpath, _dirnames, filenames in os.walk(root):
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root)
                try:
                    with open(full, "rb") as f:
                        blob = f.read()
                except OSError:
                    continue
                files[rel] = {"sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)}
        trees[repo] = {"state": "PRESENT", "n_files": len(files), "files": files}
        sys.stderr.write("%-46s .claude files=%-5d bytes=%d\n" % (
            repo, len(files), sum(v["bytes"] for v in files.values())))

    with open(os.path.join(RAW_DIR, "trees.json"), "w") as f:
        json.dump({"clones": CLONES, "method": "git clone --depth 1", "trees": trees},
                  f, indent=1, sort_keys=True)

    states = {}
    for repo, t in trees.items():
        states[t["state"]] = states.get(t["state"], 0) + 1
    print("\nstate:", states)
    print("repos with a populated .claude/:",
          sum(1 for t in trees.values() if t["state"] == "PRESENT" and t["n_files"] > 1))


if __name__ == "__main__":
    main()
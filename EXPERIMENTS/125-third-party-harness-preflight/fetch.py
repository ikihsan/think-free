"""E125 step 3 -- fetch each repository in the frozen inspection set and record
what is in it.

`--depth 1 --filter=blob:none` clones the commit and the trees and no blobs, so
the file *list* of a repository costs one small clone rather than a core API
call; the documented budget problem in this repository (60 core requests an
hour) is why that matters here. Each repository's commit id is recorded, so
every later row names the exact bytes it was read from and `git show` at that id
reproduces it.

Nothing here interprets anything. `probe.py` selects from the **full** listing
written here -- `trees/<slug>.tsv`, size and path for every file -- because the
pilot's capped candidate list measured the cap rather than the population
(AMENDMENT-1, correction 1).
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TREES = os.path.join(HERE, "trees")
SCRATCH = os.environ.get("E125_SCRATCH", "/tmp/opencode/e125")

MAX_BYTES = 8_000_000


def git(args, cwd):
    return subprocess.run(["git"] + args, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT).stdout.decode("utf-8", "replace")


def clone(full_name, dest):
    if os.path.isdir(os.path.join(dest, ".git")):
        return "already present"
    url = "https://github.com/%s.git" % full_name
    proc = subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none",
                           "--no-tags", "--quiet", url, dest],
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return "cloned" if proc.returncode == 0 else proc.stdout.decode("utf-8", "replace")[:300]


def main():
    with open(os.path.join(HERE, "inspect.json")) as fh:
        inspection = json.load(fh)
    if not os.path.isdir(TREES):
        os.makedirs(TREES)
    if not os.path.isdir(SCRATCH):
        os.makedirs(SCRATCH)

    out = []
    for n, row in enumerate(inspection["rows"], 1):
        name = row["full_name"]
        slug = name.replace("/", "__")
        dest = os.path.join(SCRATCH, slug)
        status = clone(name, dest)
        entry = {"full_name": name, "stars": row["stars"], "clone": status}
        if not os.path.isdir(os.path.join(dest, ".git")):
            entry["error"] = "clone failed"
            out.append(entry)
            print("%2d/%d %-38s CLONE FAILED: %s" % (n, len(inspection["rows"]), name, status[:80]))
            continue

        commit = git(["rev-parse", "HEAD"], dest).strip()
        entry["commit"] = commit
        listing = git(["ls-tree", "-r", "--long", "HEAD"], dest)
        n_files = 0
        with open(os.path.join(TREES, slug + ".tsv"), "w") as fh:
            for line in listing.splitlines():
                parts = line.split(None, 4)
                if len(parts) < 5:
                    continue
                size, path = parts[3], parts[4]
                fh.write("%s\t%s\n" % (size, path))
                n_files += 1
        entry["files"] = n_files
        out.append(entry)
        print("%2d/%d %-38s %5d files  commit %s" % (n, len(inspection["rows"]), name, n_files, commit[:10]))

    with open(os.path.join(HERE, "trees.json"), "w") as fh:
        json.dump({"experiment": "E125", "scratch": SCRATCH,
                   "note": "full listings are in trees/<slug>.tsv; trees/<slug>.txt is the pilot's path-only form",
                   "repositories": out}, fh, indent=1, sort_keys=True)
    print("\nwrote trees.json for %d repositories" % len(out))


if __name__ == "__main__":
    sys.exit(main())
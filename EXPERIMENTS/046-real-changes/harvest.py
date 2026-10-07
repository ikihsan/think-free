#!/usr/bin/env python3
"""E046 harvest: draw real file changes out of real repositories' history.

Nothing here is synthetic. A case is one file's before-and-after inside a real
commit: the pre-image is the blob `git` itself reports for that path at
`commit^`, the post-image is the blob at `commit`, and both blob ids go into the
manifest so any row can be re-derived with `git` alone.

Cases are grouped into the eight strata named in PROTOCOL.md. Selection is
deterministic: commits newest-first, at most MAX_COMMITS commits per repository
and MAX_PER_STRATUM cases per stratum, and every skip is recorded in
raw/skips.jsonl with its reason so the sample's selection effects are auditable
rather than asserted.

    python3 harvest.py <repo> <label> <url> [<repo> <label> <url> ...]
"""

import hashlib
import json
import os
import subprocess
import sys

from harness import GIT_ENV, git

HERE = os.path.dirname(os.path.abspath(__file__))
# Fixtures are derived, not evidence: every case records the repository, the
# commit and both blob ids, so `git show` reproduces them byte for byte. They are
# written only on request, because copying 6 MB of public source into this tree
# adds a second copy that can disagree with the first.
FIXTURES = None
MAX_PER_STRATUM = 5
MAX_COMMITS = 800
MAX_BYTES = 400000

STRATA = ["rename_modify", "pure_rename", "mode_change", "delete", "crlf",
          "no_final_newline", "many_hunks", "new_file", "ordinary"]


class BlobReader(object):
    """One `git cat-file --batch` process for every blob in the harvest.

    A subprocess per blob turns a 500-commit walk into tens of thousands of
    spawns, which is why the first version of this file timed out.
    """

    def __init__(self, repo):
        self.p = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repo,
                                  env=GIT_ENV, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE)

    def read(self, spec):
        self.p.stdin.write((spec + "\n").encode("utf-8"))
        self.p.stdin.flush()
        header = self.p.stdout.readline().decode("utf-8", "replace").split()
        if len(header) < 3:
            return None
        size = int(header[2])
        data = b""
        while len(data) < size:
            chunk = self.p.stdout.read(size - len(data))
            if not chunk:
                break
            data += chunk
        self.p.stdout.read(1)
        return data


def read_commits(repo, max_commits):
    """[(commit sha, [(status, oldmode, newmode, oldpath, newpath)])], newest first."""
    rc, out, err = git(["log", "--max-count=%d" % max_commits,
                        "--format=C %H", "--raw", "-M20%"], repo)
    if rc != 0:
        raise SystemExit("git log failed in %s: %s" % (repo, err.decode()))
    commits, cur = [], None
    for raw in out.decode("utf-8", "replace").split("\n"):
        if raw.startswith("C "):
            cur = (raw[2:].strip(), [])
            commits.append(cur)
        elif raw.startswith(":"):
            meta, _, path = raw.partition("\t")
            bits = meta[1:].split()
            # git 2.25 writes `:srcmode dstmode srcsha dstsha status`; newer
            # versions omit the two blob ids, so the status is the last field.
            oldmode, newmode, status = bits[0], bits[1], bits[-1]
            parts = path.split("\t")
            if status[0] in ("R", "C"):
                cur[1].append((status, int(oldmode, 8), int(newmode, 8),
                               parts[0], parts[1]))
            else:
                cur[1].append((status, int(oldmode, 8), int(newmode, 8),
                               parts[0], parts[0]))
    return commits


def hunks_at(repo, commit, path, old_path):
    rc, out, _ = git(["diff", "-U3", "-M20%", commit + "^", commit, "--",
                      old_path if old_path != path else path], repo)
    if rc != 0:
        return 0
    return sum(1 for l in out.decode("utf-8", "replace").split("\n")
               if l.startswith("@@"))


def eligible(pre, post, stratum):
    for data in (pre, post):
        if data is None:
            continue
        if len(data) > MAX_BYTES:
            return "too_big"
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            return "not_utf8"
    # A pure rename has, by definition, identical content at both paths: it is
    # the one stratum where "nothing changed" is the case under test.
    if pre == post and stratum != "pure_rename":
        return "identical"
    return None


def classify(status, oldmode, newmode, pre, post, hunks):
    """First matching stratum wins, in the order PROTOCOL.md lists them.

    Additions and deletions come before the mode check because git writes an
    absent side of a rename/add/delete as mode `000000`: read the other way, every
    file ever added is a "mode change" and the new-file stratum never fills.
    """
    if status.startswith("R") and not status.endswith("100"):
        return "rename_modify"
    if status.startswith("R"):
        return "pure_rename"
    if status.startswith("A"):
        return "new_file"
    if status.startswith("D"):
        return "delete"
    if oldmode and newmode and oldmode != newmode:
        return "mode_change"
    if pre is not None and b"\r\n" in pre:
        return "crlf"
    if pre and not pre.endswith(b"\n"):
        return "no_final_newline"
    if hunks >= 8:
        return "many_hunks"
    if status.startswith("A"):
        return "new_file"
    return "ordinary"


def sha(data):
    return hashlib.sha1(data).hexdigest() if data is not None else None


def harvest(repo, label, url):
    cases, skips = [], []
    have = dict((s, 0) for s in STRATA)
    commits = read_commits(repo, MAX_COMMITS)
    reader = BlobReader(repo)
    for commit, entries in commits:
        if all(have[s] >= MAX_PER_STRATUM for s in STRATA):
            break
        for status, oldmode, newmode, old_path, new_path in entries:
            pre_path = new_path if status.startswith("A") else old_path
            hunks = 0
            pre = reader.read("%s^:%s" % (commit, pre_path))
            post = b"" if status.startswith("D") else \
                reader.read("%s:%s" % (commit, new_path))
            stratum = classify(status, oldmode, newmode, pre, post, 0)
            if stratum == "ordinary" and have["many_hunks"] < MAX_PER_STRATUM:
                hunks = hunks_at(repo, commit, new_path, old_path)
                stratum = classify(status, oldmode, newmode, pre, post, hunks)
            if have[stratum] >= MAX_PER_STRATUM:
                continue
            why = eligible(pre, post, stratum)
            if why:
                skips.append({"repo": label, "commit": commit,
                              "path": new_path, "reason": why})
                continue
            if have[stratum] >= MAX_PER_STRATUM:
                continue
            have[stratum] += 1
            case_id = "%s__%s__%s" % (label, commit[:8],
                                      new_path.replace("/", "%"))
            if FIXTURES:
                with open(os.path.join(FIXTURES, case_id + ".pre"), "wb") as fh:
                    fh.write(pre or b"")
                with open(os.path.join(FIXTURES, case_id + ".post"), "wb") as fh:
                    fh.write(post or b"")
            cases.append({
                "case_id": case_id, "repo": label, "repo_url": url,
                "commit": commit, "stratum": stratum, "status": status,
                "path": new_path, "old_path": old_path,
                "old_mode": oldmode, "new_mode": newmode,
                "pre_blob_sha1": sha(pre), "post_blob_sha1": sha(post),
                "pre_bytes": len(pre or b""), "post_bytes": len(post or b""),
                "file_is_new": status.startswith("A"),
                "needs_intent_to_add": status[0] in ("A", "R", "C"),
                "deleted_paths": [old_path] if status[0] in ("R", "C") else [],
                "real_hunks_at_context3": hunks,
            })
    return cases, skips


def main(argv):
    global FIXTURES
    argv = list(argv)
    if "--fixtures" in argv:
        i = argv.index("--fixtures")
        FIXTURES = argv[i + 1]
        del argv[i:i + 2]
        if not os.path.isdir(FIXTURES):
            os.makedirs(FIXTURES)
    if len(argv) < 4 or (len(argv) - 1) % 3:
        raise SystemExit(__doc__)
    cases, skips = [], []
    for i in range(1, len(argv), 3):
        repo, label, url = argv[i], argv[i + 1], argv[i + 2]
        if not os.path.isdir(os.path.join(repo, ".git")):
            raise SystemExit("%s is not a git repository" % repo)
        c, s = harvest(repo, label, url)
        cases.extend(c)
        skips.extend(s)
        print("%-10s %3d cases from %d commits" % (label, len(c), MAX_COMMITS))
    with open(os.path.join(HERE, "raw", "manifest.jsonl"), "w") as fh:
        for c in cases:
            fh.write(json.dumps(c, sort_keys=True) + "\n")
    with open(os.path.join(HERE, "raw", "skips.jsonl"), "w") as fh:
        for s in skips:
            fh.write(json.dumps(s, sort_keys=True) + "\n")
    tally = {}
    for c in cases:
        tally[c["stratum"]] = tally.get(c["stratum"], 0) + 1
    print("total %d cases: %s" % (len(cases), json.dumps(tally, sort_keys=True)))
    print("skipped %d: %s" % (len(skips), json.dumps(
        dict((r, sum(1 for s in skips if s["reason"] == r))
             for r in set(s["reason"] for s in skips)), sort_keys=True)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
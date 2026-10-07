"""Does the oracle actually discriminate? Check it against four routes.

Run from a scratch copy of each fixture. This is the instrument check the
protocol requires before any agent is dispatched: a scorer that cannot tell
right from wrong cannot report an agent's success.

Routes:
  stage-all      git add app.py                       (expect `wrong`)
  stage-none     do nothing                           (expect `nothing_staged`)
  diff-filter    keep hunks whose new-span covers the line, git apply --cached
                 -- the route a caller writes when told to stage one line
  stg            stage-lines/stg stage app.py:LINE    (expect `exact`)
"""

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "stage-lines", "stg")


def sh(args, cwd, stdin=None):
    p = subprocess.Popen(args, cwd=cwd,
                         stdin=subprocess.PIPE if stdin is not None else None,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(stdin.encode() if stdin is not None else None)
    return p.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace")


def oracle(repo):
    with open(os.path.join(repo, ".expected_index")) as fh:
        return fh.read()


def index(repo):
    rc, out, _ = sh(["git", "show", ":app.py"], repo)
    return out if rc == 0 else None


def verdict(repo):
    got = index(repo)
    if got is None:
        return "nothing_staged"
    return "exact" if got == oracle(repo) else "wrong"


def parse_diff(text):
    """-> (file header lines, [hunk lines]) where each hunk is header+body."""
    header, hunks, cur = [], [], None
    for line in text.split("\n"):
        if line.startswith("@@"):
            cur = [line]
            hunks.append(cur)
        elif cur is None:
            if line or header:
                header.append(line)
        else:
            cur.append(line)
    return header, hunks


def hunk_span(hunk):
    """(first, last) new-file line numbers the hunk's header claims."""
    spec = hunk[0].split("@@")[1].strip().split("+")[1]
    parts = spec.split(",")
    start = int(parts[0])
    count = max(int(parts[1]), 1) if len(parts) > 1 else 1
    return start, start + count - 1


def diff_filter(repo, line):
    rc, out, _ = sh(["git", "diff", "-U0", "--no-color"], repo)
    header, hunks = parse_diff(out)
    kept = [h for h in hunks if hunk_span(h)[0] <= line <= hunk_span(h)[1]]
    body = [l for h in kept for l in h]
    return sh(["git", "apply", "--cached", "--unidiff-zero", "-"], repo,
              stdin="\n".join(header + body) + "\n")


def main():
    root = sys.argv[1]
    rows = []
    for name in sorted(os.listdir(root)):
        src = os.path.join(root, name)
        if not os.path.isdir(src) or not name.endswith("-nostg"):
            continue
        with open(os.path.join(src, ".requested_line")) as fh:
            line = int(fh.read().strip())
        for route in ("stage-all", "stage-none", "diff-filter", "stg"):
            work = src + "-probe-" + route
            if os.path.exists(work):
                shutil.rmtree(work)
            shutil.copytree(src, work)
            rc = 0
            if route == "stage-all":
                rc, _, _ = sh(["git", "add", "app.py"], work)
            elif route == "diff-filter":
                rc, _ = diff_filter(work, line)[0:2]
            elif route == "stg":
                rc, _, _ = sh([sys.executable, STG, "stage", "app.py:%d" % line], work)
            rows.append((name, route, verdict(work), rc))
            shutil.rmtree(work)
    print("%-26s %-12s %-16s %s" % ("scenario", "route", "verdict", "exit"))
    for name, route, v, rc in rows:
        print("%-26s %-12s %-16s %d" % (name.replace("-nostg", ""), route, v, rc))


if __name__ == "__main__":
    main()
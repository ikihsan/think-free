"""E020 control: is A5's near-zero a fact about configuration, or a fact about
sampling on claude-config terms?

Declared in the protocol's Amendment 2 before this file existed. Same mechanism as
the main population -- GitHub repository search, capped per term, read in the
API's order -- over terms containing no agent vocabulary at all. The single
question: what fraction of these repositories carry a `.claude/` directory?
"""

import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "raw")
CLONES = "/tmp/opencode/e019-control"
SEARCH = "https://api.github.com/search/repositories"
UA = "think-free-research"

# Declared control terms: everyday software topics, no agent words.
CONTROL_TERMS = ["flask todo app", "rust cli argument parser", "python csv toolkit",
                 "docker compose nginx", "react form library"]
PER_TERM = 30


def sh(cmd, timeout=180):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = p.communicate()
    return p.returncode, out.decode("utf-8", "replace")


def search(term):
    url = SEARCH + "?" + urllib.parse.urlencode({"q": term, "per_page": str(PER_TERM)})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            d = json.load(r)
        return [i["full_name"] for i in d.get("items", [])], "PRESENT"
    except urllib.error.HTTPError as e:
        return None, ("ABSENT" if e.code == 404 else "UNDECIDABLE")
    except Exception:
        return None, "UNDECIDABLE"


def main():
    repos, states = [], {}
    for term in CONTROL_TERMS:
        names, state = search(term)
        states[term] = state
        if names:
            repos.extend((n, term) for n in names)
        sys.stderr.write("control search %-26s -> %s (%s)\n" % (term, state, len(names or [])))
        time.sleep(7.0)

    seen, ordered = set(), []
    for name, term in repos:
        if name not in seen:
            seen.add(name)
            ordered.append({"repo": name, "term": term})

    if not os.path.isdir(CLONES):
        os.makedirs(CLONES)

    rows = {}
    for row in ordered:
        repo = row["repo"]
        dest = os.path.join(CLONES, repo.replace("/", "__"))
        rc = 0
        if not os.path.isdir(dest):
            rc, out = sh(["git", "clone", "--depth", "1", "--quiet",
                          "https://github.com/%s.git" % repo, dest], timeout=120)
            if rc != 0:
                rows[repo] = {"state": "UNDECIDABLE", "term": row["term"]}
                sys.stderr.write("CLONE-FAIL %-46s %s\n" % (repo, out.strip()[:70]))
                time.sleep(0.5)
                continue
            time.sleep(0.4)
        root = os.path.join(dest, ".claude")
        if not os.path.isdir(root):
            rows[repo] = {"state": "ABSENT", "term": row["term"]}
            continue
        files, h = {}, {}
        for dp, _dn, fns in os.walk(root):
            for fn in fns:
                full = os.path.join(dp, fn)
                try:
                    blob = open(full, "rb").read()
                except OSError:
                    continue
                h[hashlib.sha256(blob).hexdigest()] = len(blob)
                files[os.path.relpath(full, root)] = True
        rows[repo] = {"state": "PRESENT", "term": row["term"], "n_files": len(files),
                      "bytes": sum(h.values()), "hashes": sorted(h)}
        sys.stderr.write("%-46s .claude files=%d bytes=%d\n" % (repo, len(files), sum(h.values())))

    st = {}
    for v in rows.values():
        st[v["state"]] = st.get(v["state"], 0) + 1
    present = st.get("PRESENT", 0)
    decided = present + st.get("ABSENT", 0)
    out = {"terms": CONTROL_TERMS, "per_term": PER_TERM, "search_state": states,
           "n_repos": len(rows), "state_counts": st,
           "containment_rate": round(present / decided, 4) if decided else None,
           "rows": rows}
    with open(os.path.join(RAW_DIR, "control.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("\ncontrol: %d repos, states %s, .claude/ containment %s"
          % (len(rows), st, out["containment_rate"]))


if __name__ == "__main__":
    main()
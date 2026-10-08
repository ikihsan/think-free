"""E057 step extraction: find rows where the requester is asked to *perform an action
to produce an artifact*, rather than to understand a fact, choose a product, or get a
tool configured.

The shape test is written against the whole 4392-row corpus at once, not against one
site, so the population is not the one that happened to look promising (F029, F039).
Every hit is printed with its site, its requester id, and its text, to be read.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# generic formulation of "identify an unknown object from partial evidence"
IDENT = re.compile(
    r"\b(identify|identifying|identification)\b"
    r"|\bwhat (is|are) (this|that|these|those)\b"
    r"|\bwhich (set|model|version|type|part|piece|brand|year|spec|specification)s?\b"
    r"|\bhow (do|can) i (know|find out|tell|identify)\b"
    r"|\bany(one|body)? (know|tell)\b"
    r"|\bwhat.{0,20}\b(is it|are they)\b"
    r"|\b(determine|figure out|find out) (out )?(what|which|which set)\b",
    re.I)
# a second, competing shape: perform a physical procedure to produce an artifact
PROC = re.compile(
    r"\bhow (do|can|should) i\b.{0,60}\b(replace|repair|fix|clean|restore|strip|"
    r"desolder|rebuild|recover|reprint|convert|resize|crop|resize|calibrat|align|"
    r"level|true|seat|fit|install|remove|open|extract|reclaim|separate|sort)\b",
    re.I)


def load():
    idx = json.load(open(os.path.join(RAW, "index.json")))
    rows = []
    for s in idx["sites"]:
        for r in json.load(open(os.path.join(RAW, s["file"]))):
            rows.append((s["name"], s["arm"], r))
    return rows


def main():
    rows = load()
    print("corpus rows: %d  sites: %d" % (len(rows), len(set(n for n, _, _ in rows))))

    ident, proc = [], []
    for name, arm, r in rows:
        t = r["title"]
        uid = r.get("owner", {}).get("user_id")
        rec = {"site": name, "arm": arm, "uid": uid, "title": t}
        if IDENT.search(t):
            ident.append(rec)
        if PROC.search(t):
            proc.append(rec)

    for label, hits in (("IDENTIFY-UNKNOWN", ident), ("PHYSICAL-PROCEDURE", proc)):
        bysite = defaultdict(set)
        for h in hits:
            bysite[h["site"]].add(h["uid"])
        print("\n=== %s: %d rows, %d distinct requesters ==="
              % (label, len(hits), len(set((h["site"], h["uid"]) for h in hits))))
        print("%-28s %5s %5s" % ("site", "rows", "users"))
        for site, uids in sorted(bysite.items(), key=lambda kv: -len(kv[1])):
            n = sum(1 for h in hits if h["site"] == site)
            print("%-28s %5d %5d" % (site, n, len(uids)))
        with open(os.path.join(HERE, "hits-%s.txt" % label.lower()), "w") as fh:
            for site in sorted(bysite):
                fh.write("\n## %s (%d users)\n" % (site, len(bysite[site])))
                for h in sorted((x for x in hits if x["site"] == site),
                                key=lambda x: str(x["uid"])):
                    fh.write("%s\t%s\t%s\n" % (h["uid"], h["arm"], h["title"]))
        print("  wrote hits-%s.txt" % label.lower())
    return 0


if __name__ == "__main__":
    sys.exit(main())

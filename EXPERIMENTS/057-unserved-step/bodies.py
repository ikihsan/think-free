"""E057 bodies: pull the question bodies behind the identification-step rows, so the
incumbent enumeration (G2) is built from the population's own vocabulary rather than
from a web search. F082 measured that search returning 2 implementations where the
corpus already on disk named 26; D077 requires reading the corpus first.
"""
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

API = "https://api.stackexchange.com/2.3"
UA = {"User-Agent": "think-free-research/0.1"}
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

SITES = {"Bricks": "bricks", "Bicycles": "bicycles", "Biology": "biology"}


def get(path, **params):
    q = urllib.parse.urlencode(sorted(params.items()))
    req = urllib.request.Request("%s/%s?%s" % (API, path, q), headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        d = json.load(r)
    if d.get("backoff"):
        time.sleep(d["backoff"] + 1)
    return d


def strip(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h or "")
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = html.unescape(h)
    return re.sub(r"\s+", " ", h).strip()


def main():
    hits = os.path.join(HERE, "hits-identify-unknown.txt")
    want = {}
    cur = None
    for line in open(hits):
        if line.startswith("## "):
            cur = line[3:].split(" (")[0].strip()
        elif line.strip() and cur in SITES:
            uid, arm, title = line.rstrip("\n").split("\t", 2)
            want.setdefault(cur, {})[title] = uid

    out = {}
    for name, param in SITES.items():
        titles = want.get(name, {})
        # recover question ids from the already-fetched rows
        idx = json.load(open(os.path.join(RAW, "index.json")))
        byt = {}
        for s in idx["sites"]:
            if s["name"] == name:
                for r in json.load(open(os.path.join(RAW, s["file"]))):
                    byt[r["title"]] = r["question_id"]
        ids = sorted(set(byt[t] for t in titles if t in byt))
        print("%s: %d titles -> %d ids" % (name, len(titles), len(ids)))
        rows = []
        for i in range(0, len(ids), 50):
            batch = ids[i:i + 50]
            d = get("questions/%s" % ";".join(str(x) for x in batch),
                    site=param, filter="withbody")
            for it in d["items"]:
                rows.append({"question_id": it["question_id"], "title": it["title"],
                             "uid": it.get("owner", {}).get("user_id"),
                             "body": strip(it.get("body"))})
            time.sleep(1.1)
        out[name] = rows
        print("   bodies fetched: %d" % len(rows))
        with open(os.path.join(HERE, "bodies-%s.json" % param), "w") as fh:
            json.dump(rows, fh, indent=1)
    with open(os.path.join(HERE, "bodies-index.json"), "w") as fh:
        json.dump({k: len(v) for k, v in out.items()}, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())

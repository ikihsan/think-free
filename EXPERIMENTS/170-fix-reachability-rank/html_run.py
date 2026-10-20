"""E170 Amendment 2: the arms and both controls on GitHub's web search.

The web surface honours quotes; the API does not.  Ranks are read from document
order of the anchors, and every response's ordered list is written to disk.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghsearch as gs                                            # noqa: E402
import controls as ctl                                           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0 Safari/537.36 think-free-e170")
ANCHOR = re.compile(r'href="(/[^"/?#]+/[^"/?#]+/(?:issues|pull)/\d+)"')
DELAY = 2.6


def fetch(query):
    """(ordered result keys, error).  Rank 1 is the first anchor in the page."""
    url = "https://github.com/search?" + urllib.parse.urlencode(
        {"q": query, "type": "issues"})
    for attempt in range(3):
        req = urllib.request.Request(
            url, headers={"User-Agent": UA, "Accept": "text/html"})
        try:
            with urllib.request.urlopen(req, timeout=45) as fh:
                html = fh.read().decode("utf-8", "replace")
            time.sleep(DELAY)
            keys = []
            for path in ANCHOR.findall(html):
                m = re.match(r"^/([^/]+)/([^/]+)/(?:issues|pull)/(\d+)$", path)
                if m:
                    k = gs.norm_target(m.group(1), m.group(2), int(m.group(3)))
                    if k not in keys:
                        keys.append(k)
            return keys[:gs.TOPK], None
        except Exception as exc:                                   # noqa: BLE001
            msg = "%s: %s" % (type(exc).__name__, str(exc)[:80])
            if "429" in msg and attempt < 2:
                time.sleep(30)
                continue
            time.sleep(DELAY)
            return [], msg
    return [], "retries_exhausted"


def main():
    with open(os.path.join(RAW, "rows.json")) as fh:
        rows = json.load(fh)
    with open(os.path.join(RAW, "targets.json")) as fh:
        targets = json.load(fh)
    out = []
    for r in rows:
        qid, tgt = r["qid"], r["target"]
        want = gs.target_key(tgt)
        doc = targets.get(qid) or {}
        phrase = (r.get("phrase") or "").strip()
        keyword = (r.get("keyword") or "").strip()
        rare, _ = ctl.rare_phrase(doc.get("body", ""))
        plan = [
            ("G-A0", '"%s"' % phrase if phrase else None),
            ("G-A1", keyword or None),
            ("G-C1", rare or None),
            ("G-C2", 'in:title "%s"' % (doc.get("title") or "")),
        ]
        rec = {"qid": qid, "target": want}
        for name, query in plan:
            if not query:
                rec[name] = {"query": None, "rank": None, "error": "no_query",
                             "keys": []}
                continue
            keys, err = fetch(query)
            rec[name] = {"query": query, "error": err,
                         "rank": (keys.index(want) + 1) if want in keys else None,
                         "keys": keys}
            print("%s %-5s rank=%s n=%d %s" % (qid, name, rec[name]["rank"],
                                               len(keys), query[:60]))
        out.append(rec)
        with open(os.path.join(RAW, "html-arms.json"), "w") as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
            fh.write("\n")

    def hits(name, rank1=False):
        return sum(1 for o in out if o[name]["rank"] is not None
                   and (o[name]["rank"] == 1 if rank1
                        else o[name]["rank"] <= gs.TOPK))

    summary = {
        "rows": len(out),
        "G_A0_hits_top10": hits("G-A0"), "G_A1_hits_top10": hits("G-A1"),
        "G_C1_hits_top10": hits("G-C1"),
        "G_C2_rank1": hits("G-C2", rank1=True),
        "G_C2_hits_top10": hits("G-C2"),
        "errors": sum(1 for o in out for n in ("G-A0", "G-A1", "G-C1", "G-C2")
                      if o[n]["error"] not in (None, "no_query")),
    }
    summary["C1_pass"] = summary["G_C1_hits_top10"] >= 10
    summary["C2_pass"] = summary["G_C2_rank1"] >= 10

    b = sum(1 for o in out if o["G-A1"]["rank"] and o["G-A0"]["rank"] is None)
    c = sum(1 for o in out if o["G-A0"]["rank"] and o["G-A1"]["rank"] is None)
    summary["paired"] = {"A1_only": b, "A0_only": c}
    sys.path.insert(0, HERE)
    with open(os.path.join(RAW, "html-summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(summary, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
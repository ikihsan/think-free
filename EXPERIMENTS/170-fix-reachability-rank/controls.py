"""G0r and G0t: the two repaired positive controls (PROTOCOL-AMENDMENT-1.md).

G0r picks the most selective phrase the target itself can supply, chosen offline
and deterministically.  G0t replicates E169's title rule on the same rows.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghsearch as gs                                            # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
_LONG = re.compile(r"^[^ ]{8,}$")


def rare_phrase(body):
    """Longest non-function token of length >= 8, plus its two neighbours.

    Long tokens are the most selective vocabulary in a technical document, and
    this rule never consults the index.
    """
    toks = (body or "").split()
    best = -1
    for i, t in enumerate(toks):
        c = t.strip(".,;:()[]<>`\"'*")
        if len(c) >= 8 and c.lower() not in gs._STOP and re.search(r"[A-Za-z]", c):
            if best < 0 or len(c) > len(toks[best].strip(".,;:()[]<>`\"'*")):
                best = i
    if best < 0:
        return "", -1
    lo = max(0, best - 1)
    phrase = " ".join(toks[lo:lo + 3])
    if len(toks[lo:lo + 3]) < 3:
        phrase = " ".join(toks[max(0, best - 2):best + 1])
    return phrase.strip(".,;:()[]<>`\"'"), len(
        toks[best].strip(".,;:()[]<>`\"'*"))


def main():
    with open(os.path.join(RAW, "targets.json")) as fh:
        targets = json.load(fh)
    with open(os.path.join(RAW, "rows.json")) as fh:
        rows = json.load(fh)

    out = []
    for r in rows:
        qid, tgt = r["qid"], r["target"]
        doc = targets.get(qid) or {}
        phrase, toklen = rare_phrase(doc.get("body", ""))
        items, total, err = gs.search(phrase)
        rank = gs.rank_of(items, tgt)
        title_q = 'in:title "%s"' % (doc.get("title") or "")
        titems, ttotal, terr = gs.search(title_q)
        trank = gs.rank_of(titems, tgt)
        out.append({
            "qid": qid,
            "target": gs.target_key(tgt),
            "G0r_phrase": phrase, "G0r_token_len": toklen,
            "G0r_rank": rank, "G0r_total": total, "G0r_error": err,
            "G0r_urls": [i.get("html_url") for i in items][:gs.TOPK],
            "G0t_query": title_q, "G0t_rank": trank, "G0t_total": ttotal,
            "G0t_error": terr,
            "G0t_urls": [i.get("html_url") for i in titems][:gs.TOPK],
        })
        print("%s G0r rank=%s total=%s phrase=%r | G0t rank=%s total=%s"
              % (qid, rank, total, phrase[:60], trank, ttotal))
        with open(os.path.join(RAW, "controls-g0rt.json"), "w") as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
            fh.write("\n")

    r_hits = sum(1 for o in out if o["G0r_rank"] is not None
                 and o["G0r_rank"] <= 10)
    t_hits = sum(1 for o in out if o["G0t_rank"] is not None
                 and o["G0t_rank"] <= 10)
    t_exact = sum(1 for o in out if o["G0t_rank"] == 1)
    totals = sorted(o["G0r_total"] for o in out if o["G0r_total"] is not None)
    summary = {
        "rows": len(out),
        "G0r_hits_top10": r_hits, "G0r_pass": r_hits >= 10,
        "G0r_median_total": totals[len(totals) // 2] if totals else None,
        "G0t_rank1": t_exact, "G0t_hits_top10": t_hits,
        "G0t_pass": t_exact >= 10,
    }
    with open(os.path.join(RAW, "controls-summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
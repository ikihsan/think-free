"""E170 driver: verification, control, arms, placebo, grading.

Writes every raw response it judges on.  Grades by target URL identity only, so
reading a fix document cannot change a verdict.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghsearch as gs                                            # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
E169 = os.path.join(os.path.dirname(HERE), "169-version-pinned-reach")
RAW = os.path.join(HERE, "raw")
NONSENSE = "zzqxvbnmklpwrts fhjkqvwxz"


def load_rows():
    hand = {}
    with open(os.path.join(E169, "hand-queries.jsonl")) as fh:
        for line in fh:
            r = json.loads(line)
            hand[r["qid"]] = r
    targets = {}
    with open(os.path.join(E169, "raw", "containment.json")) as fh:
        for r in json.load(fh)["rows"]:
            targets[r["qid"]] = r
    rows = []
    for qid, tgt in sorted(targets.items(), key=lambda kv: int(kv[0])):
        h = hand.get(qid, {})
        rows.append({
            "qid": qid,
            "title": h.get("title", ""),
            "literal_type": h.get("literal_type"),
            "phrase": h.get("phrase", ""),
            "keyword": h.get("keyword", ""),
            "target": tgt["target"],
            "e169_term_coverage": tgt.get("term_coverage"),
        })
    return rows


def save(name, obj):
    with open(os.path.join(RAW, name), "w") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
        fh.write("\n")


def record(store, name, query, items, total, err):
    store.append({
        "arm": name, "query": query, "total_count": total, "error": err,
        "urls": [i.get("html_url") for i in items][:gs.TOPK],
    })
    return store[-1]


def main():
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    rows = load_rows()
    rawlog = []

    # ---- V1 / V3: semantics, re-run inside the experiment ------------------
    _, n_plain, e1 = gs.search(NONSENSE)
    _, n_digit, e3 = gs.search(NONSENSE + " 9987")
    # ---- V2: qualifiers ---------------------------------------------------
    probe = "paste slow"
    scope = "repo:microsoft/vscode"
    _, n_title, _ = gs.search("%s in:title %s" % (probe, scope))
    _, n_body, _ = gs.search("%s in:body %s" % (probe, scope))
    _, n_all, _ = gs.search("%s %s" % (probe, scope))
    verify = {
        "V1_nonsense_terms_count": n_plain, "V1_error": e1,
        "V3_nonsense_plus_number_count": n_digit, "V3_error": e3,
        "V2_counts": {"in:title": n_title, "in:body": n_body,
                      "unqualified": n_all},
    }
    verify["V1_pass"] = (n_plain == 0)
    verify["V3_pass"] = bool(n_digit and n_digit > 0)
    verify["V2_pass"] = bool(n_title is not None and n_body is not None
                             and n_title < n_body)
    save("verify.json", verify)

    # ---- fetch targets, then build the control phrase ---------------------
    # Cached on disk: the core API allows 60 requests/hour unauthenticated and a
    # re-run must not spend the budget twice.
    tpath = os.path.join(RAW, "targets.json")
    if os.path.exists(tpath):
        with open(tpath) as fh:
            targets = json.load(fh)
        print("reusing %d cached target documents" % len(targets))
    else:
        targets = {}
        for r in rows:
            t = r["target"]
            doc, err = gs.fetch_target(t["owner"], t["repo"], t["number"])
            targets[r["qid"]] = doc
            r["target_error"] = err
            print("fetched %s/%s#%d %s" % (t["owner"], t["repo"], t["number"],
                                           "ok" if doc else err))
        save("targets.json", targets)

    # ---- G0 positive control, G5 placebo, then the arms --------------------
    for r in rows:
        qid, tgt = r["qid"], r["target"]
        doc = targets.get(qid) or {}
        phrase = gs.control_phrase(doc.get("body", ""))
        r["control_phrase"] = phrase
        items, total, err = gs.search(phrase)
        rec = record(rawlog, "G0_control_global", phrase, items, total, err)
        r["control_rank"] = gs.rank_of(items, tgt)
        r["control_total"] = total
        print("control %s rank=%s total=%s %r" % (qid, r["control_rank"],
                                                  total, rec["urls"][:2]))

        # placebo: the phrase from the NEXT row in qid order
        nxt = rows[(rows.index(r) + 1) % len(rows)]
        ndoc = targets.get(nxt["qid"]) or {}
        pphrase = gs.control_phrase(ndoc.get("body", ""))
        pitems, ptotal, perr = gs.search(pphrase)
        prec = record(rawlog, "G5_placebo", pphrase, pitems, ptotal, perr)
        r["placebo_rank"] = gs.rank_of(pitems, tgt)
        print("placebo %s rank=%s total=%s" % (qid, r["placebo_rank"], ptotal))

        for name, query in gs.arms(r, tgt):
            items, total, err = gs.search(query)
            record(rawlog, name, query, items, total, err)
            r[name] = {"rank": gs.rank_of(items, tgt), "total": total,
                       "query": query, "error": err}
        print("arms done %s" % qid)

    save("rawlog.json", rawlog)
    save("rows.json", rows)
    print("E170 fetch and arms complete")


if __name__ == "__main__":
    main()
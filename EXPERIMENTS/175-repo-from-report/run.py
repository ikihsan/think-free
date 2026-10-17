#!/usr/bin/env python3
"""E175 stage 2: G0 (repos exist), G1 (derivation), then the three arms.

Stage A of this script writes every derived repository and every planned query to
`derivation.json` and `queries.json` and exits, so the queries are committed
before the first index request. Stage B (`--search`) runs the arms.
"""
import json
import math
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
E170 = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                    "EXPERIMENTS", "170-fix-reachability-rank")
sys.path.insert(0, HERE)
sys.path.insert(0, E170)
import derive                                                  # noqa: E402
import ghsearch as gs                                          # noqa: E402
from qtext import keywords, literal                             # noqa: E402

UA = "think-free-e175/1.0"


def wilson(k, n, z=1.959963984540054):
    if not n:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4)]


def mcnemar(a_only, b_only):
    n = a_only + b_only
    return 1.0 if n == 0 else round(2 * 0.5 ** n, 6)


def repo_exists(owner_repo):
    url = "https://api.github.com/repos/%s" % owner_repo
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as fh:
            data = json.loads(fh.read().decode("utf-8"))
            ok = {"full_name": data.get("full_name"), "status": fh.status,
                  "archived": data.get("archived"), "open_issues": data.get("open_issues_count")}
    except Exception as exc:                                   # noqa: BLE001
        ok = {"error": "%s: %s" % (type(exc).__name__, exc)}
    os.makedirs(RAW, exist_ok=True)
    with open(os.path.join(RAW, "repos.jsonl"), "a") as fh:
        fh.write(json.dumps({"repo": owner_repo, **ok}, sort_keys=True) + "\n")
    time.sleep(1.0)
    return ok


def stage_a():
    sample = json.load(open(os.path.join(HERE, "sample.json")))
    rows = [r for r in sample["rows"] if r.get("gold_repo_r")]
    print("rows with a gold repository: %d (%d distinct repos)"
          % (len(rows), len({r["gold_repo_r"] for r in rows})))

    # ---- G0: every gold repository is confirmed to exist --------------------
    g0 = {}
    for repo in sorted({r["gold_repo_r"] for r in rows}):
        g0[repo] = repo_exists(repo)
    missing = [r for r, v in g0.items() if "error" in v or v.get("status") != 200]
    print("G0: %d of %d gold repositories confirmed present%s"
          % (len(g0) - len(missing), len(g0),
             ("" if not missing else "; absent: %s" % missing)))

    # ---- G1: derive from the report alone ----------------------------------
    out = []
    for r in rows:
        log = []
        repo, info = derive.derive(r, log)
        lit = literal(r)
        kw = keywords(r, extra=(repo or "").split("/")[-1])
        out.append({
            "qid": r["qid"], "gold_repo_r": r["gold_repo_r"],
            "gold_repo": r["gold_repo"], "gold_number": r["gold_number"],
            "derived_repo": repo, "correct": repo == r["gold_repo_r"],
            "candidates": info["candidates"], "lookups": len(info["tried"]),
            "skipped_over_cap": info["skipped_over_cap"], "tried": log,
            "literal": lit, "keywords": kw,
            "qtext": lit or kw, "qform": "literal" if lit else "keywords",
        })
        print("  %d gold=%-28s derived=%-28s %s (%d lookups, %d candidates)"
              % (r["qid"], r["gold_repo_r"], repo or "-",
                 "OK" if repo == r["gold_repo_r"] else "miss",
                 len(info["tried"]), info["candidates"]))
    k = sum(1 for o in out if o["correct"])
    g1 = {"hits": k, "of": len(out), "rate": round(k / len(out), 4) if out else None,
          "ci95": wilson(k, len(out)), "kill_below": 0.20,
          "kill_fires": (k / len(out) < 0.20) if out else None}
    print("G1: derived == gold on %d of %d = %s, CI95 %s; kill(<0.20) fires: %s"
          % (k, len(out), g1["rate"], g1["ci95"], g1["kill_fires"]))

    # ---- the three arms, planned and committed before any index request ----
    arms = []
    for o in out:
        qt = o["qtext"]
        if not qt:
            continue
        oracle = "repo:%s %s" % (o["gold_repo_r"], qt)
        derived = ("repo:%s %s" % (o["derived_repo"], qt)) if o["derived_repo"] else None
        arms.append({"qid": o["qid"], "gold": "%s#%s" % (o["gold_repo"], o["gold_number"]),
                     "qform": o["qform"], "qtext": qt,
                     "A_oracle": oracle, "A_derived": derived,
                     "A_global": qt})
    payload = {"experiment": "E175", "stage": "planned", "g0": g0, "g1": g1,
               "derivation": out, "arms": arms}
    dest = os.path.join(HERE, "derivation.json")
    with open(dest, "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote %s with %d planned rows; commit it, then run with --search"
          % (dest, len(arms)))


def stage_b():
    payload = json.load(open(os.path.join(HERE, "derivation.json")))
    rawlog = []
    for a in payload["arms"]:
        owner, repo, number = (a["gold"].split("#")[0].split("/")
                               + [a["gold"].split("#")[1]])
        target = {"owner": owner, "repo": repo, "number": int(number)}
        for name in ("A_oracle", "A_derived", "A_global"):
            q = a.get(name)
            if not q:
                rawlog.append({"qid": a["qid"], "arm": name, "query": None,
                               "rank": None, "total": None, "urls": []})
                continue
            items, total, err = gs.search(q)
            rawlog.append({"qid": a["qid"], "arm": name, "query": q,
                           "rank": gs.rank_of(items, target), "total": total,
                           "error": err,
                           "urls": [i.get("html_url") for i in items][:gs.TOPK]})
            print("  %s %-10s rank=%s total=%s" % (a["qid"], name,
                                                    rawlog[-1]["rank"], total))
    with open(os.path.join(RAW, "arms.json"), "w") as fh:
        json.dump(rawlog, fh, indent=1, sort_keys=True)
        fh.write("\n")
    summarise(payload, rawlog)


def summarise(payload, rawlog):
    by = {(r["qid"], r["arm"]): r for r in rawlog}
    arms = payload["arms"]
    rates = {}
    for name in ("A_oracle", "A_derived", "A_global"):
        k = sum(1 for a in arms if (by.get((a["qid"], name)) or {}).get("rank"))
        rates[name] = {"hits": k, "of": len(arms),
                       "rate": round(k / len(arms), 4) if arms else None,
                       "ci95": wilson(k, len(arms)),
                       "rows_with_a_query": sum(
                           1 for a in arms if a.get(name))}
    def pair(x, y):
        xo = yo = 0
        for a in arms:
            hx = bool((by.get((a["qid"], x)) or {}).get("rank"))
            hy = bool((by.get((a["qid"], y)) or {}).get("rank"))
            xo += hx and not hy
            yo += hy and not hx
        return {"a": x, "b": y, "a_only": xo, "b_only": yo,
                "mcnemar_exact_p": mcnemar(xo, yo)}
    res = {"g1": payload["g1"], "rates": rates,
           "comparisons": [pair("A_derived", "A_oracle"),
                           pair("A_derived", "A_global")],
           "declared_bar": 0.30,
           "oracle_rate": rates["A_oracle"]["rate"],
           "derived_rate": rates["A_derived"]["rate"],
           "g2_clears_absolute": (rates["A_derived"]["rate"] or 0) >= 0.30,
           "g2_clears_relative": (rates["A_derived"]["rate"] or 0) >= 0.50
                                 * (rates["A_oracle"]["rate"] or 0)}
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    stage_b() if "--search" in sys.argv else stage_a()
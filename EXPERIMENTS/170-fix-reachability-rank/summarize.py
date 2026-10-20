"""Summarise E170: verification gates, control, placebo, and every arm."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def wilson(k, n):
    if n == 0:
        return (0.0, 0.0)
    z = 1.959963985
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return ((c - m) / d, (c + m) / d)


def mcnemar(b, c):
    """Exact two-sided binomial test on the discordant pairs."""
    n = b + c
    if n == 0:
        return 1.0
    lo = min(b, c)
    tail = 0.0
    for k in range(lo + 1):
        tail += _choose(n, k) * 0.5 ** n
    return min(1.0, 2 * tail)


def _choose(n, k):
    out = 1.0
    for i in range(k):
        out = out * (n - i) / (i + 1)
    return out


def main():
    with open(os.path.join(RAW, "rows.json")) as fh:
        rows = json.load(fh)
    with open(os.path.join(RAW, "verify.json")) as fh:
        ver = json.load(fh)
    n = len(rows)
    out = {"rows": n, "verify": ver, "arms": {}, "control": {}, "placebo": {}}

    ctl = [r["control_rank"] for r in rows]
    ctot = sorted(t for t in (r["control_total"] for r in rows)
                  if t is not None)
    out["control"] = {
        "hit_top10": sum(1 for x in ctl if x is not None and x <= 10),
        "hit_any": sum(1 for x in ctl if x is not None),
        "median_total_count": ctot[len(ctot) // 2] if ctot else None,
        "min_total_count": ctot[0] if ctot else None,
        "queries_with_no_total": sum(1 for r in rows
                                     if r["control_total"] is None),
        "kill_fired": sum(1 for x in ctl if x is not None and x <= 10) < 10,
    }
    pl = [r["placebo_rank"] for r in rows]
    out["placebo"] = {
        "hit_top10": sum(1 for x in pl if x is not None and x <= 10),
        "kill_fired": sum(1 for x in pl if x is not None and x <= 10) > 1,
    }

    for arm in ["A0_bare_global", "A0_quoted_global", "A0_bare_repo",
                "A0_quoted_repo", "A1_global", "A1_repo", "A2_global"]:
        hits, ranks, totals = 0, [], []
        for r in rows:
            a = r.get(arm) or {}
            rank = a.get("rank")
            ranks.append(rank)
            totals.append(a.get("total"))
            if rank is not None and rank <= 10:
                hits += 1
        lo, hi = wilson(hits, n)
        clean = sorted(t for t in totals if t is not None)
        out["arms"][arm] = {"hits_top10": hits, "of": n,
                            "rate": round(hits / float(n), 4),
                            "ci95": [round(lo, 4), round(hi, 4)],
                            "ranks": ranks,
                            "errors": sum(1 for r in rows
                                          if (r.get(arm) or {}).get("error")),
                            "median_total": clean[len(clean) // 2]
                                             if clean else None}

    def discordant(a, b):
        bb = cc = 0
        pairs = []
        for x, y in zip(out["arms"][a]["ranks"], out["arms"][b]["ranks"]):
            hx = x is not None and x <= 10
            hy = y is not None and y <= 10
            if hx and not hy:
                bb += 1
            elif hy and not hx:
                cc += 1
            pairs.append("%s/%s" % ("A" if hx else "-", "B" if hy else "-"))
        return {"a_only": bb, "b_only": cc, "mcnemar_p": round(mcnemar(bb, cc), 6),
                "pairs": pairs}

    out["compare"] = {
        "A1_global_vs_A0_quoted_global":
            discordant("A1_global", "A0_quoted_global"),
        "A1_repo_vs_A0_quoted_repo": discordant("A1_repo", "A0_quoted_repo"),
        "A1_global_vs_A2_global": discordant("A1_global", "A2_global"),
    }
    with open(os.path.join(RAW, "summary.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
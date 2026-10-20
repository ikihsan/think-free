#!/usr/bin/env python3
"""E196 analysis -- the four gates, computed from rows already on disk.

Gate thresholds are imported from thresholds.py rather than re-declared here, so
a threshold lives in exactly one place and this file cannot drift from it.
"""
from stats import kruskal_wallis, median
from thresholds import (SMALL_CUTOFF, G4_BAR_USD, KW_ALPHA, G5_MIN_DESCRIBED,
                        G4_MIN_RANK, G4_MIN_TOTAL_USD,
                        G5_RATIO, POSITIVE_CONTROL_FAMILIES, STOPWORDS)


def tokenise(text):
    out = []
    cur = []
    for ch in text.lower():
        if ch.isalpha():
            cur.append(ch)
        elif cur:
            out.append("".join(cur))
            cur = []
    if cur:
        out.append("".join(cur))
    return [t for t in out if len(t) > 2 and t not in STOPWORDS]


def analyse(head, recs, g1_ok, g2_ok):
    res = {"population": len(head), "codes_measured": len(recs), "G1": g1_ok,
           "G2": g2_ok, "declared": {"cutoff": SMALL_CUTOFF, "G4_bar": G4_BAR_USD,
                                    "kw_alpha": KW_ALPHA, "G5_ratio": G5_RATIO}}

    # ---- family rollup, labelled from the API's own names (AMENDMENT-2 s3)
    fam = {}
    for r in recs:
        f = r["code"][0]
        e = fam.setdefault(f, {"codes": 0, "total": 0.0, "awards": 0,
                               "small_sum": 0.0, "small_n": 0,
                               "medians": [], "label": None})
        e["codes"] += 1
        e["total"] += r.get("total_awards_level") or 0.0
        e["awards"] += r.get("award_count") or 0
        e["small_sum"] += r.get("small_purchase_sum") or 0.0
        e["small_n"] += r.get("tail_positive") or 0
        if r.get("median_award") is not None:
            e["medians"].append(r["median_award"])
    for f, e in fam.items():
        top = max((r for r in recs if r["code"][0] == f),
                  key=lambda r: r.get("total_awards_level") or 0.0)
        e["label"] = top["name"]
        e["median_of_medians"] = median(e["medians"])
    res["families"] = {f: {k: v for k, v in e.items() if k != "medians"}
                       for f, e in sorted(fam.items())}
    grand = sum(e["total"] for e in fam.values()) or 1.0
    res["grand_total_awards_level"] = sum(e["total"] for e in fam.values())

    # ---- G3: discrimination across families
    nonpos = [r["code"] for r in recs
              if r.get("median_award") is not None and r["median_award"] <= 0]
    groups = {f: e["medians"] for f, e in fam.items() if e["medians"]}
    h, p, k, n = kruskal_wallis(groups)
    res["G3"] = {"test": "kruskal_wallis", "families": k, "codes": n,
                 "H": h, "p": p, "alpha": KW_ALPHA,
                 "codes_with_median_le_0": len(nonpos),
                 "those_codes": nonpos,
                 "fire": (p is not None and p < KW_ALPHA),
                 "pass": not (p is not None and p < KW_ALPHA)}

    # ---- G4: addressability
    ranked = sorted((r for r in recs if not r.get("tail_censored")),
                    key=lambda r: r.get("small_purchase_sum") or 0.0,
                    reverse=True)
    censored = [r["code"] for r in recs if r.get("tail_censored")]
    res["G4"] = {"bar": G4_BAR_USD,
                 "codes_with_censored_tail": len(censored),
                 "censored_codes": censored,
                 "top10_small_purchase_sum": [
                     {"code": r["code"], "name": r.get("name"),
                      "sum": r["small_purchase_sum"],
                      "awards": r["tail_positive"],
                      "total": r.get("total_awards_level"),
                      "censored": r["tail_censored"]}
                     for r in sorted(recs, key=lambda r: r.get("small_purchase_sum") or 0.0,
                                     reverse=True)[:10]],
                 "best_uncensored": {"code": ranked[0]["code"]} if ranked else None}

    # AMENDMENT-3: the gate proper is two exact facts, not a sum.
    #   (a) a rank checkpoint >= G4_MIN_RANK whose block maximum is <= the cutoff
    #   (b) the code's own total obligation >= $1B
    # A checkpoint of rank k with block max m means "at least k awards are <= m",
    # so (a) is a one-sided exact statement with no interpolation anywhere.
    cleared, profile_rows = [], []
    for r in recs:
        prof = r.get("rank_profile") or {}
        best = None
        for rank in sorted(int(k) for k in prof):
            blk = prof[rank] if rank in prof else prof.get(str(rank))
            if not blk or blk.get("max") is None:
                continue
            if rank >= G4_MIN_RANK and blk["max"] <= SMALL_CUTOFF:
                best = {"rank": rank, "block_max": blk["max"],
                        "at_least_that_many_awards_at_or_below": blk["max"]}
                break
        total = r.get("total_awards_level") or 0.0
        profile_rows.append({"code": r["code"], "name": r.get("name"),
                             "total": total, "awards": r.get("award_count"),
                             "checkpoint": best,
                             "profile": {str(k): prof[k].get("max")
                                         for k in sorted(prof, key=str)}})
        if best and total >= G4_MIN_TOTAL_USD:
            cleared.append({"code": r["code"], "name": r.get("name"),
                            "total": total, "awards": r.get("award_count"),
                            **best})
    res["G4"]["restated_by_amendment3"] = True
    res["G4"]["min_rank"] = G4_MIN_RANK
    res["G4"]["min_total_usd"] = G4_MIN_TOTAL_USD
    res["G4"]["cutoff"] = SMALL_CUTOFF
    res["G4"]["codes_clearing_rank_and_total"] = cleared
    res["G4"]["codes_with_a_10k_checkpoint_at_or_below_cutoff"] = [
        p["code"] for p in profile_rows if p["checkpoint"]]
    res["G4"]["profile"] = sorted(
        profile_rows, key=lambda p: (p["total"] or 0.0), reverse=True)
    res["G4"]["codes_clearing_bar"] = len(cleared)
    res["G4"]["fire"] = bool(cleared)
    res["G4"]["pass"] = bool(cleared)

    # ---- G5: description audit and positive control
    tok_by_code, src_by_code = {}, {}
    for r in recs:
        pos = r.get("tail_descriptions") or []
        if pos:
            src, descs = "tail", [d for _, d in pos if d]
        else:
            src, descs = "median", [d for d in (r.get("median_descriptions") or []) if d]
        src_by_code[r["code"]] = {"source": src, "described_rows": len(descs)}
        tok_by_code[r["code"]] = tokenise(" ".join(descs))
    base_rate = {}
    for toks in tok_by_code.values():
        for t in set(toks):
            base_rate[t] = base_rate.get(t, 0) + 1
    n_codes = float(len(tok_by_code) or 1)
    base_rate = {t: c / n_codes for t, c in base_rate.items()}

    g5 = {"base_rate_denominator_codes": int(n_codes), "families": {}}
    for prefix, keys in POSITIVE_CONTROL_FAMILIES.items():
        codes = [r["code"] for r in recs if r["code"].startswith(prefix)]
        enough = [c for c in codes if src_by_code[c]["described_rows"] >= G5_MIN_DESCRIBED]
        arms = {}
        for tok in sorted(keys):
            arm_codes = [c for c in enough if tok in set(tok_by_code[c])]
            k_arm = len(arm_codes)
            arm_rate = (k_arm / float(len(enough))) if enough else 0.0
            base = base_rate.get(tok, 0.0)
            arms[tok] = {"arm_codes": k_arm, "arm_rate": arm_rate,
                         "base_rate": base, "ratio": (arm_rate / base) if base else None,
                         "pass": bool(base) and arm_rate >= G5_RATIO * base}
        label = next((r["name"] for r in recs if r["code"].startswith(prefix)), "")
        g5["families"][prefix] = {"label": label, "codes": codes,
                                   "codes_enough_descriptions": enough,
                                   "excluded_for_thin_description":
                                       [c for c in codes if c not in enough],
                                   "arms": arms}
    g5["fire"] = all(any(a["pass"] for a in f["arms"].values())
                     for f in g5["families"].values())
    g5["pass"] = g5["fire"]
    res["G5"] = g5
    return res


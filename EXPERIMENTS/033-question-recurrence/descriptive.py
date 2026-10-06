"""E033 — descriptive measures over the committed population.

PROTOCOL.md section 8 (D5, D6, D7, D9) and the sampling mechanism they test.
Split out of `tally.py` at the 300-line cap: these are population statistics with
no gate attached, and `tally.py` is the gate table. Nothing here decides a verdict.

Every function takes the already-loaded rows and returns a JSON-able dict, so
`tally.py --check` recomputes the same numbers from the same bytes.
"""
import collections
import math

RECORD_POOL = 0.0223        # E031+E032 pooled upper bound, from 032/README.md
DRAW_N = (60, 100)          # E032's and E031's populations


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def newcombe(k1, n1, k2, n2, z=1.96):
    """CI for p1 - p2, so the interval reported is the interval of the difference."""
    if n1 == 0 or n2 == 0:
        return (None, None)
    p1, p2 = k1 / float(n1), k2 / float(n2)
    l1, u1 = wilson(k1, n1, z)
    l2, u2 = wilson(k2, n2, z)
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return (max(-1.0, lo), min(1.0, hi))


def by_score(harvest):
    """Score order, ties broken on question id so the order is a function of the
    bytes alone and not of the sort's stability."""
    return sorted(harvest, key=lambda r: (-(r.get("score") or 0), r["question_id"]))


def counterfactual_draw(harvest, window=60):
    """D7: what a `sort=votes` draw actually contains, and the distribution of 60-question
    draws inside this population. Needs no canonical, so it survives A3 failing."""
    ordered = by_score(harvest)
    top = ordered[:window]
    counts = []
    for start in range(0, len(ordered) - window + 1):
        counts.append(sum(1 for r in ordered[start:start + window]
                          if r.get("closed_reason") == "Duplicate"))
    n = len(counts)
    return {
        "top%d_duplicates" % window: sum(1 for r in top if r.get("closed_reason") == "Duplicate"),
        "top_score_range": [top[0].get("score"), top[-1].get("score")] if top else None,
        "windows": n,
        "mean_window_duplicates": (sum(counts) / float(n)) if n else None,
        "max_window": max(counts) if counts else None,
        "windows_with_zero": sum(1 for c in counts if c == 0),
    }


def tertiles(harvest):
    """D6: the stratum gradient, which is what the record's samples were drawn against."""
    ordered = by_score(harvest)
    third = len(ordered) // 3
    bands = {"high (top third by score)": ordered[:third],
             "middle": ordered[third:2 * third],
             "low (bottom third)": ordered[2 * third:]}
    out = {}
    for name, band in sorted(bands.items()):
        k = sum(1 for r in band if r.get("closed_reason") == "Duplicate")
        b = len(band)
        out[name] = {"n": b, "dup": k, "rate": k / float(b) if b else None,
                     "ci95": list(wilson(k, b))}
    if out.get("high (top third by score)", {}).get("rate") and \
            out.get("low (bottom third)", {}).get("rate"):
        out["ratio_low_over_high"] = (
            out["low (bottom third)"]["rate"] / out["high (top third by score)"]["rate"])
    return out


def word_lengths(harvest, lo=40, hi=600):
    """D5: the contrast with E032's 40-600 word filter, so the two populations' sizes are
    explicit rather than assumed comparable."""
    words = sorted(r["words"] for r in harvest)
    return {"median_words": words[len(words) // 2] if words else None,
            "min": words[0] if words else None, "max": words[-1] if words else None,
            "in_e032_window": sum(1 for w in words if lo <= w <= hi),
            "window": [lo, hi]}


def unanswered_share(harvest):
    """D9 (post-hoc, labelled in PROTOCOL): whether the convergent population and the
    unanswered population overlap. Uses the label, never the reader."""
    dups = [r for r in harvest if r.get("closed_reason") == "Duplicate"]
    others = [r for r in harvest if r.get("closed_reason") != "Duplicate"]
    out = {}
    for name, group in (("duplicate", dups), ("other", others)):
        k = sum(1 for r in group if r.get("answer_count") == 0)
        out[name] = {"n": len(group), "zero_answers": k,
                     "rate": k / float(len(group)) if group else None,
                     "ci95": list(wilson(k, len(group)))}
    out["difference_ci95"] = list(newcombe(out["duplicate"]["zero_answers"],
                                           out["duplicate"]["n"],
                                           out["other"]["zero_answers"],
                                           out["other"]["n"]))
    if out["other"]["rate"]:
        out["ratio"] = out["duplicate"]["rate"] / out["other"]["rate"]
    scores = {name: sorted(r.get("score") or 0 for r in group)
              for name, group in (("duplicate", dups), ("other", others))}
    out["median_score"] = {k: (v[len(v) // 2] if v else None) for k, v in scores.items()}
    out["share_score_le_1"] = {
        k: (sum(1 for s in v if s <= 1) / float(len(v)) if v else None)
        for k, v in scores.items()}
    return out


def closure_distribution(harvest):
    """D2: so the positive label cannot be read as a residual of everything else."""
    reasons = collections.Counter(r.get("closed_reason") for r in harvest)
    return {k if k else "absent (question not closed)": v
            for k, v in sorted(reasons.items(), key=lambda kv: (-kv[1], str(kv[0])))}


def expected_visible_edges(rate, q, draws=DRAW_N):
    """PROTOCOL 6. `q` is the share of a duplicate's canonical that is itself in the
    sample; it is only trustworthy when the edge arm's gate passed, so the caller
    passes None when it did not and this returns None rather than a number."""
    if q is None:
        return {str(m): None for m in draws}
    return {str(m): m * rate * q for m in draws}


def verdict_for(lo, hi):
    """The declared B1/B2 rule, in one place, so the direction cannot be re-decided."""
    if hi is not None and hi <= RECORD_POOL:
        return "B2__the_record_bound_stands"
    if lo is not None and lo > RECORD_POOL:
        return "B1__the_record_bound_is_refuted"
    return "not_evaluated"
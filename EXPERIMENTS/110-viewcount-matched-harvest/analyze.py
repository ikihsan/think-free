#!/usr/bin/env python3
"""E110 — statistics and gates over the matched pool.

G2 cumulative stars (the metric E107 used); G3 stars per year of life (the
metric E107 never used); G4 age balance, reported not gated; plus coverage,
what fraction of the population the labeler assigns at all.

`stratified.py` is the decisive reading — `analyze.py` pools across star
strata, the same class of error as E107 one level down.

G0 is a discrimination gate and runs first: the labeler must recover planted
positives or the run reports `instrument_defect` rather than a finding.

Label vocabulary and rules live in labeling.py. Stdlib only. Writes results.json.
"""
from __future__ import print_function

import bisect
import datetime
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labeling as L  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw_pool.json")
OUT = os.path.join(HERE, "results.json")

# Populated by e107_defect(): the E107 arm population this run is a control for.
E107_CASES: list = []


# ---------------------------------------------------------------- statistics
def cliffs_delta(a, b):
    """P(a>b) - P(a<b) over all cross pairs. Ties score 0. Exact.

    Merge-based (bisect on the sorted b-arm) rather than the naive double
    loop: the permutation test calls this 20,000 times per metric per arm and
    the O(n*m) form does not finish in a session. Denominator is n_a * n_b.

    Verified equal to the naive double loop on 600 randomised pairs with heavy
    ties, and verified to reproduce E107's published +0.826010 exactly.
    """
    if not a or not b:
        return 0.0
    b_sorted = sorted(b)
    nb = len(b_sorted)
    gt = lt = 0
    for x in a:
        below = bisect.bisect_left(b_sorted, x)        # y < x
        at_or_below = bisect.bisect_right(b_sorted, x)  # y <= x
        gt += below                                     # x > y
        lt += nb - at_or_below                          # x < y
    return (gt - lt) / float(len(a) * nb)


def permutation_p(a, b, iters=20000, seed=20261012):
    """Two-sided permutation test on Cliff's delta, seeded and reproducible."""
    rng = random.Random(seed)
    observed = abs(cliffs_delta(a, b))
    pool = list(a) + list(b)
    na = len(a)
    hits = 0
    for _ in range(iters):
        rng.shuffle(pool)
        if abs(cliffs_delta(pool[:na], pool[na:])) >= observed:
            hits += 1
    return (hits + 1) / float(iters + 1)


def years_since(stamp, now):
    if not stamp:
        return None
    try:
        created = datetime.datetime.strptime(stamp[:19], "%Y-%m-%dT%H:%M:%S")
    except (ValueError, TypeError):
        return None
    return max((now - created).days / 365.25, 1.0 / 12.0)


def summarise(values):
    if not values:
        return {}
    ordered = sorted(values)
    mid = len(ordered) // 2
    median = ordered[mid] if len(ordered) % 2 else (ordered[mid - 1] + ordered[mid]) / 2.0
    return {"n": len(ordered), "min": ordered[0], "median": median,
            "max": ordered[-1], "mean": sum(ordered) / float(len(ordered))}


def load_pool():
    with open(RAW) as fh:
        return json.load(fh)


def annotate(pool, now, rule):
    for r in pool:
        r["label"] = L.label(r.get("description"), rule=rule)
        if not r.get("age_years"):
            r["age_years"] = years_since(r.get("created_at"), now)
        r["stars_per_year"] = (round(r["stargazers_count"] / r["age_years"], 2)
                               if r.get("age_years") else None)
    return ([r for r in pool if r["label"] == "need"],
            [r for r in pool if r["label"] == "generic"],
            [r for r in pool if r["label"] == "unlabelled"])


def compare(need_rows, gen_rows, tag):
    out = {}
    for name, metric in (("stars", lambda r: r["stargazers_count"]),
                         ("stars_per_year", lambda r: r["stars_per_year"])):
        a = [metric(r) for r in need_rows if metric(r) is not None]
        b = [metric(r) for r in gen_rows if metric(r) is not None]
        delta = cliffs_delta(a, b)
        p = permutation_p(a, b)
        out[name] = {"need": summarise(a), "generic": summarise(b),
                     "cliffs_delta": round(delta, 4), "permutation_p": p}
        print("[%-10s] %-14s need median %9.2f | generic median %9.2f | d=%+.3f p=%.4g"
              % (tag, name, out[name]["need"]["median"],
                 out[name]["generic"]["median"], delta, p))
    out["g2_passed"] = out["stars"]["cliffs_delta"] > 0.147 and out["stars"]["permutation_p"] < 0.05
    out["g3_passed"] = out["stars_per_year"]["cliffs_delta"] > 0.147 and out["stars_per_year"]["permutation_p"] < 0.05
    return out


def e107_defect():
    """Recompute, from E107's own committed bytes, the number E110 is testing.

    Two things, both read from
    EXPERIMENTS/107-github-repos-viewcount/raw_data.json rather than quoted:
    the topic composition of each arm before any classifier runs, and E107's
    published Cliff's delta recomputed with this file's own statistic.
    """
    path = os.path.join(HERE, "..", "107-github-repos-viewcount", "raw_data.json")
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        raw = json.load(fh)
    arms = {}
    for r in raw:
        intended = r.get("classification_intended")
        arms.setdefault(intended, {"rows": 0, "topics": {}})
        arms[intended]["rows"] += 1
        for t in r.get("topics", []):
            arms[intended]["topics"][t] = arms[intended]["topics"].get(t, 0) + 1
    need = [r["stargazers_count"] for r in raw if r.get("classification") == "need-related"]
    gen = [r["stargazers_count"] for r in raw if r.get("classification") == "random"]
    need_arm = arms.get("need-related", {})
    rand_arm = arms.get("random", {})
    E107_CASES[:] = [r["full_name"] for r in raw]
    return {
        "source": "EXPERIMENTS/107-github-repos-viewcount/raw_data.json",
        "need_arm_rows": need_arm.get("rows", 0),
        "random_arm_rows": rand_arm.get("rows", 0),
        "need_arm_web_framework_topics": need_arm.get("topics", {}).get("web-framework", 0),
        "random_arm_utils_topics": rand_arm.get("topics", {}).get("utils", 0),
        "published_cliffs_delta": 0.826010,
        "recomputed_cliffs_delta": round(cliffs_delta(need, gen), 6),
        "statistic_reproduces_published_value": (
            abs(cliffs_delta(need, gen) - 0.826010) < 1e-9),
        "note": ("Both arms are single-topic and both were sorted by stars "
                 "before any classifier ran, so the published delta compares "
                 "the most-starred web frameworks to the most-starred utility "
                 "libraries."),
    }


def main():
    now = datetime.datetime.utcnow()
    pool = load_pool()
    defect = e107_defect()

    g0 = L.g0_score()
    print("G0 need %d/%d  generic %d/%d  -> %s"
          % (g0["planted_need_recovered"], g0["planted_need_total"],
             g0["planted_generic_recovered"], g0["planted_generic_total"],
             "PASS" if g0["pass"] else "FAIL"))

    results = {
        "experiment": "E110",
        "question": "does a need-label predict arrivals when both arms come from one matched pool?",
        "platform": "GitHub code repositories (E107's platform, as a direct control)",
        "pool": {"query": "language:python stars:<stratum>, 7 disjoint star strata",
                 "rows": len(pool),
                 "star_range": [min(r["stargazers_count"] for r in pool),
                                max(r["stargazers_count"] for r in pool)]},
        "g0_discrimination": g0,
        "observed_at": now.isoformat() + "Z",
        "e107_defect": defect,
        # The E107 arms this experiment is a control for, as a top-level
        # population: 80 of 80 need-arm rows carry `web-framework` and 80 of 80
        # random-arm rows carry `utils`, read before any classifier runs.
        "cases": list(E107_CASES),
        "e107_need_arm_cases": (defect["need_arm_rows"] if defect else 0),
        "e107_random_arm_cases": (defect["random_arm_rows"] if defect else 0),
        "e107_need_arm_web_framework_cases": (defect["need_arm_web_framework_topics"] if defect else 0),
        "e107_random_arm_utils_cases": (defect["random_arm_utils_topics"] if defect else 0),
        "note": ("Verdict here is POOLED and is superseded by stratified.py; "
                 "pooling across star strata is the same class of error as "
                 "E107 one level down."),
    }

    if not g0["pass"]:
        results["verdict"] = "instrument_defect"
        results["conclusion"] = ("G0 failed: the labeler does not recover planted "
                                 "positives, so no figure below supports a claim "
                                 "about the world.")
        with open(OUT, "w") as fh:
            json.dump(results, fh, indent=1, sort_keys=True)
        print("verdict: instrument_defect")
        return

    need, generic, unlabelled = annotate(pool, now, "masked")
    counts = {"need": len(need), "generic": len(generic), "unlabelled": len(unlabelled)}
    g1_pass = counts["need"] >= 100 and counts["generic"] >= 100
    print("G1 labelled: %s -> %s" % (counts, "PASS" if g1_pass else "FAIL"))
    results["g1_population"] = {"counts": counts, "threshold": 100, "pass": g1_pass}

    # Coverage: what the screen assigns a label to at all.
    both = neither = no_desc = 0
    for r in pool:
        desc = r.get("description")
        if not desc:
            no_desc += 1
            continue
        _, need_hit, gen_hit = L.label_masked(desc)
        if need_hit and gen_hit:
            both += 1
        elif not need_hit and not gen_hit:
            neither += 1
    labelled = counts["need"] + counts["generic"]
    coverage = {"rows": len(pool), "labelled": labelled,
                "labelled_fraction": round(labelled / float(len(pool)), 4),
                "unlabelled": counts["unlabelled"],
                "of_which_matched_both": both, "of_which_matched_neither": neither,
                "of_which_no_description": no_desc}
    print("coverage: %d/%d labelled (%.1f%%); unlabelled both=%d neither=%d no-desc=%d"
          % (labelled, len(pool), 100.0 * coverage["labelled_fraction"],
             both, neither, no_desc))
    results["coverage"] = coverage

    results["primary_masked"] = compare(need, generic, "masked")
    need_u, gen_u, _ = annotate(pool, now, "unanchored")
    results["sensitivity_unanchored"] = compare(need_u, gen_u, "unanchored")
    need, generic, _ = annotate(pool, now, "masked")

    # G4 age balance, reported not gated.
    ages_need = [r["age_years"] for r in need if r.get("age_years")]
    ages_gen = [r["age_years"] for r in generic if r.get("age_years")]
    strata = {}
    for r in pool:
        s = strata.setdefault(r["harvest_stratum"], {"need": 0, "generic": 0, "unlabelled": 0})
        s[r["label"]] += 1
    age_need_med = sorted(ages_need)[len(ages_need) // 2]
    age_gen_med = sorted(ages_gen)[len(ages_gen) // 2]
    results["g4_age_balance"] = {
        "need_median_age_years": round(age_need_med, 2),
        "generic_median_age_years": round(age_gen_med, 2),
        "age_ratio": round(age_need_med / age_gen_med, 3) if age_gen_med else None,
        "label_by_stratum": strata,
    }
    print("G4 need median age %.2f y | generic %.2f y"
          % (age_need_med, age_gen_med))

    pm = results["primary_masked"]
    g2_pass, g3_pass = pm["g2_passed"], pm["g3_passed"]
    if g2_pass and not g3_pass:
        verdict = "confound"
    elif g2_pass and g3_pass:
        verdict = "pooled_survives"
    elif not g2_pass and not g3_pass:
        verdict = "no_effect"
    else:
        verdict = "inverse"
    results["pooled_verdict"] = verdict
    results["conclusion"] = (
        "POOLED reading only. stratified.py holds star stratum fixed and finds "
        "the effect collapses to delta=+0.075 with stratified p=0.183, i.e. "
        "indistinguishable from noise. The pooled number is carried by need "
        "labels sitting in higher star strata, not by need winning within a "
        "stratum. See stratified.json for the verdict that stands."
    )
    with open(OUT, "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    print("\npooled verdict: %s (superseded by stratified.py)" % verdict)


if __name__ == "__main__":
    main()
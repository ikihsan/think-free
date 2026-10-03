#!/usr/bin/env python3
"""A1 masking experiment over the PPNA Seattle crossings extract.

Pinned substrate: github.com/OpenSidewalks/PLoS-cities-complex-systems @
4f65e22b19576375b2b031b035631a20806da48e, data/seattle.geojson.

Ground truth: each crossing has curbramps in {0,1}, crossing in
{marked,unmarked}, length. An "unsafe-fixable" crossing is marked and lacks
curb ramps. The repair decision ranks candidates by true score = length of
unsafe-fixable crossings. A policy may observe a budgeted subset and must
still commit to a top-K ranking; regret is the full-information top-K score
minus the realized score of its chosen set.
"""
import json, math, random, statistics, sys
from collections import defaultdict

SEATTLE = "/tmp/opencode/plos-cities/data/seattle.geojson"
OUT = "/home/ubuntu/think-free/EXPERIMENTS/002-a1-masking/results.json"

K = 20
BUDGET = 150
BUDGET_FRAC_CHECK = True
GRID = 0.005  # ~400 m cells


def load():
    with open(SEATTLE) as fh:
        feats = json.load(fh)["features"]
    rows = []
    for f in feats:
        p = f["properties"]
        if p.get("curbramps") not in (0, 1, "0", "1"):
            continue
        if p.get("crossing") not in ("marked", "unmarked"):
            continue
        try:
            length = float(p.get("length") or 0)
        except (TypeError, ValueError):
            continue
        if length <= 0:
            continue
        xy = f["geometry"]["coordinates"][0]
        rows.append({"x": xy[0], "y": xy[1], "curbramps": p["curbramps"],
                     "marked": p["crossing"], "length": length})
    return rows


def cell(r):
    return (round(r["x"] / GRID), round(r["y"] / GRID))


def unsafe(r):
    return r["marked"] == "marked" and str(r["curbramps"]) == "0"


def score(r):
    return r["length"] if unsafe(r) else 0.0


def neighbourhood(rows):
    # densest 3x3 grid-cell block around the mode cell
    counts = defaultdict(int)
    for r in rows:
        counts[cell(r)] += 1
    ranked = sorted(counts, key=lambda c: -counts[c])
    want = set()
    total = 0
    for c in ranked:
        want.add(c)
        total += counts[c]
        if total >= 900:
            break
    sub = [r for r in rows if cell(r) in want]
    return sub


def mask(rows, rng, mode):
    n = len(rows)
    missing = set()
    if mode == "random":
        missing = set(rng.sample(range(n), n // 2))
    else:  # block: hide whole cells for half the cells
        cells = sorted({cell(r) for r in rows})
        hide = set(rng.sample(cells, len(cells) // 2))
        missing = {i for i, r in enumerate(rows) if cell(r) in hide}
    hidden = {i: (i in missing) for i in range(n)}
    return hidden


def prior_unsafe(rows, hidden):
    seen = [r for i, r in enumerate(rows) if not hidden[i]]
    if not seen:
        return 0.0
    return sum(1 for r in seen if unsafe(r)) / len(seen)


def choose_set(rows, hidden, observed, policy, rng, p_prior):
    unobserved = [i for i in range(len(rows)) if not observed[i]]
    remaining = BUDGET - sum(observed.values())
    picks = list(policy(rows, hidden, observed, unobserved, rng, p_prior))[:remaining]
    for i in picks:
        observed[i] = True
    return observed


def estimate_scores(rows, hidden, observed, p_prior):
    out = []
    for i, r in enumerate(rows):
        if observed[i]:
            out.append(score(r))
        else:
            out.append(p_prior * r["length"] if not hidden[i] or True else 0.0)
        # hidden or not, unobserved crossings are estimated from the prior;
        # observed ones are known exactly. If a crossing is masked, its prior
        # estimate is still the planner's only option.
    return out


def regret_of(rows, picked):
    true_top = sorted((score(r) for r in rows), reverse=True)[:K]
    chosen = sorted((score(rows[i]) for i in picked), reverse=True)[:K]
    return sum(true_top) - sum(chosen)


def rank_pick(rows, est, allowed):
    return [i for i, _ in sorted(((i, est[i]) for i in allowed), key=lambda t: -t[1])]


def policy_random(rows, hidden, observed, unobserved, rng, p_prior):
    return rng.sample(unobserved, len(unobserved))


def policy_centrality(rows, hidden, observed, unobserved, rng, p_prior):
    counts = defaultdict(int)
    for r in rows:
        counts[cell(r)] += 1
    return sorted(unobserved, key=lambda i: -counts[cell(rows[i])])


def policy_missingness(rows, hidden, observed, unobserved, rng, p_prior):
    # cells with the most missing facts rank first
    miss = defaultdict(int)
    for i, r in enumerate(rows):
        if hidden[i]:
            miss[cell(r)] += 1
    return sorted(unobserved, key=lambda i: (-miss[cell(rows[i])], rng.random()))


def policy_tour(rows, hidden, observed, unobserved, rng, p_prior):
    start = min(rows, key=lambda r: r["x"] + r["y"])
    cur = (start["x"], start["y"])
    remaining = set(unobserved)
    order = []
    while remaining and len(order) < BUDGET:
        nxt = min(remaining, key=lambda i: (rows[i]["x"] - cur[0]) ** 2 + (rows[i]["y"] - cur[1]) ** 2)
        order.append(nxt)
        remaining.discard(nxt)
        cur = (rows[nxt]["x"], rows[nxt]["y"])
    return order


def policy_decision_directed(rows, hidden, observed, unobserved, rng, p_prior):
    # greedy: observe crossings whose prior-weighted score straddles the
    # current estimated K-threshold — i.e. most likely to change the top-K.
    est = estimate_scores(rows, hidden, observed, p_prior)
    threshold = sorted(est, reverse=True)[K] if len(est) > K else 0.0
    def marginal(i):
        s = p_prior * rows[i]["length"]
        near = 1.0 / (1e-9 + abs(s - threshold))
        return s * near * (1.0 + rows[i]["length"] / 100.0)
    return sorted(unobserved, key=lambda i: -marginal(i))


POLICIES = {
    "random": policy_random,
    "centrality": policy_centrality,
    "missingness": policy_missingness,
    "tour": policy_tour,
    "decision-directed": policy_decision_directed,
}


def run_config(rows, mode, seed, k, budget):
    global K, BUDGET
    K, BUDGET = k, budget
    rng = random.Random(seed)
    hidden = mask(rows, rng, mode)
    p_prior = prior_unsafe(rows, hidden)
    out = {}
    for name, policy in POLICIES.items():
        observed = {i: False for i in range(len(rows))}
        choose_set(rows, hidden, observed, policy, rng, p_prior)
        est = estimate_scores(rows, hidden, observed, p_prior)
        picked = rank_pick(rows, est, list(range(len(rows))))[:k]
        out[name] = regret_of(rows, picked)
    return out


def run_once(rows, mode, seed):
    return run_config(rows, mode, seed, K, BUDGET)


def sweep_main():
    global K, BUDGET
    neighbourhood_rows = neighbourhood(load())
    sweep = {}
    for k in (10, 20, 40):
        for budget in (75, 150, 300):
            for mode in ("random", "block"):
                agg = {p: [] for p in POLICIES}
                for seed in range(10):
                    per = run_config(neighbourhood_rows, mode, seed, k, budget)
                    for p, v in per.items():
                        agg[p].append(v)
                sweep[f"K{k}_B{budget}_{mode}"] = {
                    p: {"median": statistics.median(v), "mean": statistics.mean(v)}
                    for p, v in agg.items()
                }
    dd_wins = 0
    total = 0
    for cfg, vals in sweep.items():
        best_base = min(
            (v["median"] for p, v in vals.items() if p != "decision-directed"),
        )
        dd = vals["decision-directed"]["median"]
        total += 1
        if dd <= 0.75 * best_base:
            dd_wins += 1
    payload = {"sweep": sweep, "dd_passes_75pct_gate_in": dd_wins,
               "of_configs": total}
    with open(OUT.replace("results.json", "sensitivity.json"), "w") as fh:
        json.dump(payload, fh, indent=1)
    print(json.dumps({"dd_passes": dd_wins, "of": total}))


def main():
    rows = neighbourhood(load())
    if len(rows) < 400:
        print(json.dumps({"error": "neighbourhood too small", "n": len(rows)}))
        sys.exit(3)
    seeds = list(range(30))
    results = {mode: {p: [] for p in POLICIES} for mode in ("random", "block")}
    for mode in results:
        for seed in seeds:
            per = run_once(rows, mode, seed)
            for p, v in per.items():
                results[mode][p].append(v)
    summary = {}
    for mode in results:
        summary[mode] = {}
        for p, vals in results[mode].items():
            summary[mode][p] = {"median_regret": statistics.median(vals),
                                "mean_regret": statistics.mean(vals),
                                "min": min(vals), "max": max(vals)}
    baselines = [p for p in POLICIES if p != "decision-directed"]
    strongest = {}
    for mode in summary:
        strongest[mode] = min(baselines, key=lambda p: summary[mode][p]["median_regret"])
    dd = {mode: summary[mode]["decision-directed"]["median_regret"] for mode in summary}
    gate = all(
        dd[mode] <= 0.75 * summary[mode][strongest[mode]]["median_regret"]
        for mode in summary
    )
    payload = {
        "substrate": "OpenSidewalks/PLoS-cities-complex-systems@4f65e22b19576375b2b031b035631a20806da48e data/seattle.geojson",
        "neighbourhood_n": len(rows),
        "K": K, "budget": BUDGET, "seeds": len(seeds),
        "masking_modes": ["random", "block"],
        "summary": summary, "strongest_baseline": strongest,
        "gate": {
            "rule": "decision-directed median regret <= 75% of strongest baseline in every masking mode",
            "decision_directed_median": dd, "pass": gate,
        },
        "raw": results,
    }
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=1)
    print(json.dumps({"neighbourhood_n": len(rows), "gate_pass": gate,
                      "dd_median": dd,
                      "strongest": {m: summary[m][strongest[m]]["median_regret"] for m in summary}}, indent=1))


if __name__ == "__main__":
    if "--sweep" in sys.argv:
        sweep_main()
    else:
        main()

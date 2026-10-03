#!/usr/bin/env python3
"""T-0007: distance-limited (fieldwork-cost) budget variant of the A1
masking experiment.

T-0006 varied the *count* of observations. The realistic constraint for a
human inspector is walking distance, not a head count. Here a policy's
observation set is whatever it can visit on a walk that starts at the
southwest corner and never exceeds D meters: each policy proposes its
next crossing in its own priority order, the walk follows that order, and
crossings that would break the distance cap end the walk. Regret is
computed exactly as in masking.py, so the two budget models are directly
comparable.
"""
import json, math, random, statistics, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import masking as m

OUT = str(Path(__file__).resolve().parent / "distance.json")
K = 20
D_VALUES = (40000, 80000, 160000)  # meters; full NN tour of the neighbourhood is ~190 km
MAXWALK_START = None


def meters(a, b):
    """Equirectangular approximation; the neighbourhood is ~1 km across."""
    lat = math.radians((a[1] + b[1]) / 2.0)
    dx = (b[0] - a[0]) * 111320.0 * math.cos(lat)
    dy = (b[1] - a[1]) * 110540.0
    return math.hypot(dx, dy)


def start_point(rows):
    r = min(rows, key=lambda r: r["x"] + r["y"])
    return (r["x"], r["y"])


def walk(rows, order, D, start):
    """Follow `order` until the next hop would exceed D meters."""
    observed = {i: False for i in range(len(rows))}
    cur = start
    used = 0.0
    n = 0
    for i in order:
        hop = meters(cur, (rows[i]["x"], rows[i]["y"]))
        if used + hop > D:
            break
        observed[i] = True
        used += hop
        n += 1
        cur = (rows[i]["x"], rows[i]["y"])
    return observed, used, n


def policy_dd_walk(rows, hidden, observed, unobserved, rng, p_prior, start):
    """Decision-directed value per meter of added walk from current head."""
    est = m.estimate_scores(rows, hidden, observed, p_prior)
    threshold = sorted(est, reverse=True)[K] if len(est) > K else 0.0
    head = start
    obs_pts = [(rows[i]["x"], rows[i]["y"]) for i, v in observed.items() if v]
    if obs_pts:
        head = obs_pts[-1] if len(obs_pts) == 1 else head  # endpoint-free greedy
    def rank_key(i):
        s = p_prior * rows[i]["length"]
        near = 1.0 / (1e-9 + abs(s - threshold))
        value = s * near * (1.0 + rows[i]["length"] / 100.0)
        hop = meters(head, (rows[i]["x"], rows[i]["y"])) + 1e-6
        return -(value / hop)
    return sorted(unobserved, key=rank_key)


def run_config(rows, mode, seed, D):
    rng = random.Random(seed)
    hidden = m.mask(rows, rng, mode)
    p_prior = m.prior_unsafe(rows, hidden)
    start = start_point(rows)
    out = {}
    for name, policy in m.POLICIES.items():
        base_observed = {i: False for i in range(len(rows))}
        order = list(policy(rows, hidden, base_observed, list(range(len(rows))), rng, p_prior))
        observed, used, n = walk(rows, order, D, start)
        est = m.estimate_scores(rows, hidden, observed, p_prior)
        picked = m.rank_pick(rows, est, list(range(len(rows))))[:K]
        out[name] = {"regret": m.regret_of(rows, picked), "n_observed": n, "meters": used}
    # DD walk is incremental: its ranking depends on the evolving walk end,
    # so run it hop by hop instead of from one static ordering.
    obs = {i: False for i in range(len(rows))}
    cur = start
    used = 0.0
    for _ in range(len(rows)):
        unobserved = [i for i, v in obs.items() if not v]
        if not unobserved:
            break
        order = policy_dd_walk(rows, hidden, obs, unobserved, rng, p_prior, cur)
        if not order:
            break
        i = order[0]
        hop = meters(cur, (rows[i]["x"], rows[i]["y"]))
        if used + hop > D:
            break
        obs[i] = True
        used += hop
        cur = (rows[i]["x"], rows[i]["y"])
    est = m.estimate_scores(rows, hidden, obs, p_prior)
    picked = m.rank_pick(rows, est, list(range(len(rows))))[:K]
    out["dd-walk"] = {"regret": m.regret_of(rows, picked),
                      "n_observed": sum(obs.values()), "meters": used}
    return out


def main():
    rows = m.neighbourhood(m.load())
    if len(rows) < 400:
        print(json.dumps({"error": "neighbourhood too small", "n": len(rows)}))
        sys.exit(3)
    seeds = list(range(30))
    raw = {}
    for D in D_VALUES:
        for mode in ("random", "block"):
            agg = {}
            for seed in seeds:
                per = run_config(rows, mode, seed, D)
                for p, v in per.items():
                    agg.setdefault(p, {"regret": [], "n": [], "meters": []})
                    agg[p]["regret"].append(v["regret"])
                    agg[p]["n"].append(v["n_observed"])
                    agg[p]["meters"].append(v["meters"])
            raw[f"D{D}_{mode}"] = {
                p: {"median_regret": statistics.median(v["regret"]),
                    "median_n_observed": statistics.median(v["n"]),
                    "median_meters": statistics.median(v["meters"])}
                for p, v in agg.items()
            }
    # Gate: each policy compared against the strongest baseline (everything
    # except decision-directed and dd-walk) at the same D and mask mode.
    arms = ["random", "centrality", "missingness", "tour"]
    gate = {}
    for key, vals in raw.items():
        best_base = min(vals[p]["median_regret"] for p in arms)
        for treatment in ("decision-directed", "dd-walk"):
            gate[f"{key}/{treatment}"] = vals[treatment]["median_regret"] <= 0.75 * best_base
    payload = {
        "substrate": "OpenSidewalks/PLoS-cities-complex-systems@4f65e22b19576375b2b031b035631a20806da48e data/seattle.geojson",
        "neighbourhood_n": len(rows), "K": K,
        "distance_budgets_m": D_VALUES, "seeds": len(seeds),
        "summary": raw,
        "gate": {"rule": "treatment median regret <= 75% of strongest count-policy baseline in every (D, mode)",
                 "passes": gate},
    }
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=1)
    for key, vals in raw.items():
        best = min(arms, key=lambda p: vals[p]["median_regret"])
        print(key, "strongest:", best, vals[best]["median_regret"],
              "| dd:", vals["decision-directed"]["median_regret"],
              "| dd-walk:", vals["dd-walk"]["median_regret"],
              "| median n:", {p: vals[p]["median_n_observed"] for p in ("tour", "decision-directed", "dd-walk")})


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
E222: Do E220's enterability labels predict newcomer forward outcomes better
than naive baselines?

Reads E220's committed raw bytes (no re-fetch) plus this experiment's raw/
outcome fetches (FY2024-2025 recipients per (PSC, NAICS)).

Modes:
  --preflight   compute newcomer sets and the analysis population from E220
                cache only; no outcome data needed. Prints the fetch list.
  (default)     full analysis: joins outcome window, computes gates G0-G4,
                permutation control C1, writes results/.

Windows follow E220's calendar convention:
  entry window   FY2023        (current, from E220 raw)
  prior window   FY2018-2022   (from E220 raw)
  outcome window FY2024-2025   (this experiment's raw/)
"""

import csv
import json
import math
import os
import random
import sys
from pathlib import Path

EXP_DIR = Path(__file__).resolve().parent
E220_DIR = EXP_DIR.parent / "E220-it-subsegment-entrant-advisor"
E220_RAW = E220_DIR / "raw"
E220_METRICS = E220_DIR / "results" / "subsegment_metrics.csv"
RAW_DIR = EXP_DIR / "raw"
RESULTS_DIR = EXP_DIR / "results"

# Predeclared analysis population threshold (fixed in PROTOCOL.md before the
# outcome fetch): sub-segments with >= MIN_NEWCOMERS FY2023 newcomers.
MIN_NEWCOMERS = 10

# Gates (declared in PROTOCOL.md before the outcome fetch).
GATE_SUPPORT_RHO = 0.5
GATE_REFUTE_RHO = 0.3
GATE_BASELINE_MARGIN = 0.1
PERM_SEED = 20261022
PERM_N = 10000


def load_recipients(path):
    """Return {recipient_id: amount} from an E220/E222 recipient response."""
    with open(path) as f:
        data = json.load(f)
    out = {}
    for row in data.get("results", []):
        rid = row.get("recipient_id")
        if rid:
            out[rid] = row.get("amount") or 0.0
    return out, data


def load_e220_metrics():
    rows = {}
    with open(E220_METRICS) as f:
        for r in csv.DictReader(f):
            rows[(r["code"], r["naics"])] = r
    return rows


def avg_rank(xs):
    """Average ranks, 1-based, tie-correct."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def spearman(xs, ys):
    if len(xs) < 3:
        return float("nan")
    rx, ry = avg_rank(xs), avg_rank(ys)
    mx = sum(rx) / len(rx)
    my = sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    denx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    deny = math.sqrt(sum((b - my) ** 2 for b in ry))
    if denx == 0 or deny == 0:
        return float("nan")
    return num / (denx * deny)


def mwu_normal(xs, ys):
    """Mann-Whitney U with normal approximation and tie correction.

    Returns (U, z, p_two_sided)."""
    n1, n2 = len(xs), len(ys)
    if n1 == 0 or n2 == 0:
        return float("nan"), float("nan"), float("nan")
    combined = list(xs) + list(ys)
    ranks = avg_rank(combined)
    r1 = sum(ranks[:n1])
    u1 = r1 - n1 * (n1 + 1) / 2.0
    u2 = n1 * n2 - u1
    u = min(u1, u2)
    mu = n1 * n2 / 2.0
    # tie correction
    counts = {}
    for v in combined:
        counts[v] = counts.get(v, 0) + 1
    n = n1 + n2
    tie_term = sum(c ** 3 - c for c in counts.values())
    sigma = math.sqrt(n1 * n2 / 12.0 * ((n + 1) - tie_term / (n * (n - 1.0))))
    if sigma == 0:
        return u, float("nan"), float("nan")
    z = (u - mu) / sigma
    p = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z) / math.sqrt(2.0))))
    return u, z, p


def median(xs):
    if not xs:
        return float("nan")
    s = sorted(xs)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2.0


def preflight():
    metrics = load_e220_metrics()
    population = []
    excluded = []
    for (code, naics), r in sorted(metrics.items()):
        cur_f = E220_RAW / f"recipients_{code}_{naics}_2023.json"
        pri_f = E220_RAW / f"recipients_{code}_{naics}_2018.json"
        if not cur_f.exists() or not pri_f.exists():
            excluded.append((code, naics, "missing_raw"))
            continue
        cur, _ = load_recipients(cur_f)
        pri, _ = load_recipients(pri_f)
        newcomers = set(cur) - set(pri)
        row = {
            "code": code,
            "naics": naics,
            "naics_name": r["naics_name"],
            "newcomers": len(newcomers),
            "cur": len(cur),
            "pri": len(pri),
            "classification": r["classification"],
            "score": float(r["enterability_score"]),
            "obligation": float(r["current_obligation"]),
            "fragmentation": float(r["fragmentation"]),
        }
        if len(newcomers) >= MIN_NEWCOMERS:
            population.append(row)
        else:
            excluded.append((code, naics, f"newcomers={len(newcomers)}<{MIN_NEWCOMERS}"))

    print(f"E222 preflight (from E220 committed bytes only, no network)")
    print(f"sub-segments in E220: {len(metrics)}")
    print(f"analysis population (newcomers >= {MIN_NEWCOMERS}): {len(population)}")
    print(f"excluded: {len(excluded)}")
    print()
    print(f"{'PSC':5} {'NAICS':7} {'newc':>5} {'cur':>5} {'pri':>5}  {'class':17} {'score':>6}")
    for p in sorted(population, key=lambda x: -x["score"]):
        print(f"{p['code']:5} {p['naics']:7} {p['newcomers']:5} {p['cur']:5} {p['pri']:5}"
              f"  {p['classification']:17} {p['score']:6.4f}")
    print()
    print("FETCH LIST (outcome window 2024-01-01..2025-12-31):")
    for p in population:
        print(f"  recipients_{p['code']}_{p['naics']}_2024")

    RESULTS_DIR.mkdir(exist_ok=True)
    with open(RESULTS_DIR / "preflight_population.json", "w") as f:
        json.dump({"min_newcomers": MIN_NEWCOMERS,
                   "population": population,
                   "excluded": excluded}, f, indent=2)
    print(f"\nwrote {RESULTS_DIR / 'preflight_population.json'}")


def full_analysis():
    with open(RESULTS_DIR / "preflight_population.json") as f:
        pop = json.load(f)["population"]

    rows = []
    missing_raw = []
    id_coverage = []
    for p in pop:
        code, naics = p["code"], p["naics"]
        out_f = RAW_DIR / f"recipients_{code}_{naics}_2024.json"
        if not out_f.exists():
            missing_raw.append(f"recipients_{code}_{naics}_2024.json")
            continue
        cur_f = E220_RAW / f"recipients_{code}_{naics}_2023.json"
        pri_f = E220_RAW / f"recipients_{code}_{naics}_2018.json"
        cur, cur_data = load_recipients(cur_f)
        pri, _ = load_recipients(pri_f)
        out, out_data = load_recipients(out_f)

        # identity coverage in outcome fetch (row-level, before id-dict collapsing)
        results_rows = out_data.get("results", [])
        total_rows = len(results_rows)
        with_id = sum(1 for row in results_rows if row.get("recipient_id"))
        if total_rows:
            id_coverage.append(with_id / total_rows)

        newcomers = set(cur) - set(pri)
        recurrent = newcomers & set(out)
        recur_amounts = sorted(out[r] for r in recurrent)
        rows.append({
            "code": code,
            "naics": naics,
            "naics_name": p["naics_name"],
            "classification": p["classification"],
            "score": p["score"],
            "obligation": p["obligation"],
            "fragmentation": p["fragmentation"],
            "newcomers": len(newcomers),
            "recurrent": len(recurrent),
            "M1_recurrence": len(recurrent) / len(newcomers) if newcomers else float("nan"),
            "M2_median_amount": median(recur_amounts),
            "outcome_recipients": len(out),
        })

    G0 = not missing_raw
    cov = min(id_coverage) if id_coverage else 0.0
    G1 = cov >= 0.95
    G2 = all(r["newcomers"] >= MIN_NEWCOMERS for r in rows) and len(rows) > 0

    scores = [r["score"] for r in rows]
    m1 = [r["M1_recurrence"] for r in rows]
    obl = [r["obligation"] for r in rows]
    frag = [r["fragmentation"] for r in rows]

    rho_score = spearman(scores, m1)
    rho_obl = spearman(obl, m1)
    rho_frag = spearman(frag, m1)
    rho_size = spearman([r["newcomers"] for r in rows], m1)

    # C1: permutation control — null distribution of rho(score, M1)
    rng = random.Random(PERM_SEED)
    null = []
    for _ in range(PERM_N):
        shuffled = m1[:]
        rng.shuffle(shuffled)
        null.append(spearman(scores, shuffled))
    null_sorted = sorted(x for x in null if not math.isnan(x))
    p_one = (1.0 + sum(1 for x in null_sorted if x >= rho_score)) / (1.0 + len(null_sorted))

    best_baseline = max(rho_obl, rho_frag) if not math.isnan(rho_obl) and not math.isnan(rho_frag) else rho_obl
    if not G0:
        G3 = "INSTRUMENT_FAIL"  # protocol: incomplete outcome fetch => no conclusion
    elif math.isnan(rho_score):
        G3 = "INCONCLUSIVE"
    elif rho_score >= GATE_SUPPORT_RHO and (rho_score - best_baseline) >= GATE_BASELINE_MARGIN and p_one < 0.05:
        G3 = "SUPPORT"
    elif rho_score <= GATE_REFUTE_RHO or rho_score <= best_baseline:
        G3 = "REFUTE"
    else:
        G3 = "INCONCLUSIVE"

    # G4 (secondary, non-gating): newcomer-level recurrence ENTERABLE vs rest
    ent_rows = [r for r in rows if r["classification"] in ("HIGHLY ENTERABLE", "SOMEWHAT ENTERABLE")]
    rest_rows = [r for r in rows if r["classification"] in ("MARGINAL", "CLOSED")]
    ent_new = sum(r["newcomers"] for r in ent_rows)
    ent_rec = sum(r["recurrent"] for r in ent_rows)
    rest_new = sum(r["newcomers"] for r in rest_rows)
    rest_rec = sum(r["recurrent"] for r in rest_rows)
    # row-level binary recurrence needs per-newcomer data; approximate at
    # sub-segment level with MWU on M1 distributions:
    u, z, p_mwu = mwu_normal([r["M1_recurrence"] for r in ent_rows],
                             [r["M1_recurrence"] for r in rest_rows])

    # clustered bootstrap CI on rate difference (resample sub-segments within group)
    rng2 = random.Random(PERM_SEED)
    diffs = []
    for _ in range(PERM_N):
        e_n = e_r = r_n = r_r = 0
        if ent_rows:
            for _ in range(len(ent_rows)):
                s = ent_rows[rng2.randrange(len(ent_rows))]
                e_n += s["newcomers"]; e_r += s["recurrent"]
        if rest_rows:
            for _ in range(len(rest_rows)):
                s = rest_rows[rng2.randrange(len(rest_rows))]
                r_n += s["newcomers"]; r_r += s["recurrent"]
        if e_n and r_n:
            diffs.append(e_r / e_n - r_r / r_n)
    diffs.sort()
    ci_lo = diffs[int(0.025 * len(diffs))] if diffs else float("nan")
    ci_hi = diffs[int(0.975 * len(diffs))] if diffs else float("nan")

    gates = {
        "G0_outcome_fetch_complete": {"pass": G0, "missing": missing_raw},
        "G1_identity_coverage": {"pass": G1, "min_coverage": cov},
        "G2_denominators": {"pass": G2, "n_subsegments": len(rows)},
        "G3_forward_claim": {"verdict": G3,
                             "rho_score": rho_score, "rho_obligation": rho_obl,
                             "rho_fragmentation": rho_frag,
                             "best_baseline": best_baseline,
                             "perm_p_one_sided": p_one,
                             "thresholds": {"support_rho": GATE_SUPPORT_RHO,
                                            "refute_rho": GATE_REFUTE_RHO,
                                            "baseline_margin": GATE_BASELINE_MARGIN,
                                            "perm_p": 0.05}},
        "G4_secondary": {
            "rho_size_vs_M1": rho_size,
            "enterable_subsegments": len(ent_rows),
            "rest_subsegments": len(rest_rows),
            "enterable_newcomers": ent_new, "enterable_recurrent": ent_rec,
            "rest_newcomers": rest_new, "rest_recurrent": rest_rec,
            "mwu_z": z, "mwu_p_two_sided": p_mwu,
            "cluster_boot_rate_diff_ci95": [ci_lo, ci_hi],
        },
        "C1_permutation_control": {"n": PERM_N, "seed": PERM_SEED,
                                   "null_95pct": [null_sorted[int(0.95 * len(null_sorted))],
                                                  null_sorted[int(0.995 * len(null_sorted))]]},
    }

    RESULTS_DIR.mkdir(exist_ok=True)
    with open(RESULTS_DIR / "per_subsegment.csv", "w", newline="") as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    with open(RESULTS_DIR / "gates.json", "w") as f:
        json.dump(gates, f, indent=2)
    with open(RESULTS_DIR / "summary.json", "w") as f:
        json.dump({"rows": rows, "gates": gates}, f, indent=2)

    print(json.dumps(gates, indent=2))
    print(f"\nwrote results/ under {RESULTS_DIR}")


if __name__ == "__main__":
    if "--preflight" in sys.argv:
        preflight()
    else:
        full_analysis()

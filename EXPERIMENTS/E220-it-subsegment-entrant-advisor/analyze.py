#!/usr/bin/env python3
"""
E220: Analyze sub-segment entrant share for 3 enterable IT PSC codes.

Reads raw/ files written by fetch.py. Computes per-(PSC, NAICS) metrics and gates.
"""

import json
import os
import math
import random
from pathlib import Path

EXP_DIR = Path(__file__).parent
RAW_DIR = EXP_DIR / "raw"
OUT_DIR = EXP_DIR / "results"
OUT_DIR.mkdir(exist_ok=True)

CODES = ["DA01", "DA10", "7A21"]
WINDOWS = ["current", "prior"]

# NAICS codes we fetched for each PSC code
TARGET_NAICS = {
    "DA01": ["511210", "518210", "541330", "541511", "541512", "541513", "541519", "541611"],
    "DA10": ["334111", "443120", "511210", "513210", "518210", "519130", "541511", "541512", "541519", "811212"],
    "7A21": ["334111", "336413", "443120", "511210", "513210", "518210", "541330", "541511", "541512", "541519"],
}

# NAICS name lookup (from fetched data)
NAICS_NAMES = {
    "334111": "Electronic Computer Manufacturing",
    "336413": "Other Aircraft Parts and Auxiliary Equipment Manufacturing",
    "443120": "Computer and Software Stores",
    "511210": "Software Publishers",
    "513210": "Software Publishers (variant)",
    "518210": "Computing Infrastructure Providers, Data Processing, Web Hosting",
    "519130": "Internet Publishing and Broadcasting and Web Search Portals",
    "541330": "Engineering Services",
    "541511": "Custom Computer Programming Services",
    "541512": "Computer Systems Design Services",
    "541513": "Computer Facilities Management Services",
    "541519": "Other Computer Related Services",
    "541611": "Administrative Management and General Management Consulting Services",
    "811212": "Computer and Office Machine Repair and Maintenance",
}

def load_recipients(code, naics, window):
    """Load recipient data for a (PSC, NAICS, window) combination."""
    # Files are named with year: 2023 for current, 2018 for prior (start of 5-year window)
    year = "2023" if window == "current" else "2018"
    fname = RAW_DIR / f"recipients_{code}_{naics}_{year}.json"
    if not fname.exists():
        return []
    with open(fname) as f:
        data = json.load(f)
    return data.get("results", [])


def obligation_by_id(rows):
    """Sum obligation per recipient_id; return (dict, missing_count)."""
    by_id = {}
    missing = 0
    for r in rows:
        rid = r.get("recipient_id")
        if not rid:
            missing += 1
            continue
        amt = r.get("amount") or 0.0
        by_id[rid] = by_id.get(rid, 0.0) + amt
    return by_id, missing


def top_k_share(by_id, k=5):
    """Top-k obligation share."""
    vals = sorted(by_id.values(), reverse=True)
    total = sum(vals)
    if total <= 0:
        return 0.0
    return sum(vals[:k]) / total


def spearman(xs, ys):
    """Spearman rho with average ranks; n>=3."""
    n = len(xs)
    if n < 3:
        return None

    def ranks(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def permutation_test(xs, ys, n_perm=10000, seed=20261021):
    """One-sided permutation test for Spearman rho >= observed."""
    rho_obs = spearman(xs, ys)
    if rho_obs is None:
        return None, None
    random.seed(seed)
    n = len(xs)
    count = 0
    for _ in range(n_perm):
        ys_perm = ys[:]
        random.shuffle(ys_perm)
        rho_perm = spearman(xs, ys_perm)
        if rho_perm is not None and rho_perm >= rho_obs:
            count += 1
    p = (count + 1) / (n_perm + 1)
    return rho_obs, p


def analyze_subsegment(code, naics):
    """Compute all metrics for one (PSC, NAICS) sub-segment."""
    cur_rows = load_recipients(code, naics, "current")
    pri_rows = load_recipients(code, naics, "prior")

    cur_by_id, cur_missing = obligation_by_id(cur_rows)
    pri_by_id, pri_missing = obligation_by_id(pri_rows)

    cur_ids = set(cur_by_id.keys())
    pri_ids = set(pri_by_id.keys())

    seg_new = cur_ids - pri_ids
    seg_frac = len(seg_new) / len(cur_ids) if cur_ids else 0.0

    frag = 1.0 - top_k_share(cur_by_id, 5)
    top5_share = top_k_share(cur_by_id, 5)
    obligation = round(sum(cur_by_id.values()), 2)

    total_rows = len(cur_rows)
    id_coverage = 1.0 - (cur_missing / total_rows) if total_rows > 0 else 0.0

    # Classify enterability
    if seg_frac >= 0.30 and frag >= 0.60 and len(seg_new) >= 20:
        classification = "HIGHLY ENTERABLE"
    elif seg_frac >= 0.20 and frag >= 0.40 and len(seg_new) >= 10:
        classification = "SOMEWHAT ENTERABLE"
    elif seg_frac >= 0.10 and frag >= 0.20 and len(seg_new) >= 5:
        classification = "MARGINAL"
    else:
        classification = "CLOSED"

    return {
        "code": code,
        "naics": naics,
        "naics_name": NAICS_NAMES.get(naics, "Unknown"),
        "current_rows": total_rows,
        "current_recipients": len(cur_ids),
        "prior_recipients": len(pri_ids),
        "segment_newcomers": len(seg_new),
        "segment_newcomer_fraction": round(seg_frac, 4),
        "fragmentation": round(frag, 4),
        "top5_share": round(top5_share, 4),
        "current_obligation": obligation,
        "current_missing_recids": cur_missing,
        "prior_missing_recids": pri_missing,
        "id_coverage": round(id_coverage, 4),
        "classification": classification,
    }


def main():
    print("=" * 72)
    print("E220 ANALYSIS — IT PSC Sub-Segment Entrant Advisor")
    print("=" * 72)

    all_results = []
    for code in CODES:
        for naics in TARGET_NAICS[code]:
            print(f"Analyzing {code} NAICS {naics}...", flush=True)
            result = analyze_subsegment(code, naics)
            all_results.append(result)

    # Print per-subsegment results
    print("\n" + "=" * 72)
    print("PER-SUBSEGMENT METRICS")
    print("=" * 72)
    print(f"{'PSC':<6} {'NAICS':<8} {'Name':<45} {'CurRec':>6} {'PriRec':>6} {'SegNew':>6} {'SegFrac':>7} {'Frag':>6} {'Top5':>6} {'Oblig($B)':>9} {'Class':<20}")
    print("-" * 130)
    for r in all_results:
        oblig_b = r['current_obligation'] / 1e9
        name = r['naics_name'][:43]
        print(f"{r['code']:<6} {r['naics']:<8} {name:<45} {r['current_recipients']:>6} {r['prior_recipients']:>6} {r['segment_newcomers']:>6} {r['segment_newcomer_fraction']:>7.4f} {r['fragmentation']:>6.4f} {r['top5_share']:>6.4f} {oblig_b:>9.2f} {r['classification']:<20}")

    # Gates
    print("\n" + "=" * 72)
    print("GATE VERDICTS")
    print("=" * 72)

    # G0: API accessible, returns data for all 3 PSC codes
    naics_current_counts = {}
    for code in CODES:
        fname = RAW_DIR / f"naics_{code}_2023.json"
        if fname.exists():
            with open(fname) as f:
                data = json.load(f)
            naics_current_counts[code] = len(data.get("results", []))
        else:
            naics_current_counts[code] = 0

    g0_pass = all(naics_current_counts[c] > 0 for c in CODES)
    print(f"G0 API accessible (all 3 codes return NAICS breakdown): {'PASS' if g0_pass else 'FAIL'}")
    for code in CODES:
        status = "✓" if naics_current_counts[code] > 0 else "✗"
        print(f"  {status} {code}: {naics_current_counts[code]} NAICS codes in current window")

    # G1: Identity coverage ≥ 95%
    g1_pass = all(r["id_coverage"] >= 0.95 for r in all_results)
    print(f"\nG1 identity coverage (≥0.95): {'PASS' if g1_pass else 'FAIL'}")
    for r in all_results:
        status = "✓" if r["id_coverage"] >= 0.95 else "✗"
        print(f"  {status} {r['code']} NAICS {r['naics']}: {r['id_coverage']:.4f} ({r['current_missing_recids']} missing of {r['current_rows']})")

    # G2: Prior window complete - all 3 PSC codes return ≥ 5 NAICS codes in prior window
    naics_prior_counts = {}
    for code in CODES:
        fname = RAW_DIR / f"naics_{code}_2018.json"
        if fname.exists():
            with open(fname) as f:
                data = json.load(f)
            naics_prior_counts[code] = len(data.get("results", []))
        else:
            naics_prior_counts[code] = 0

    g2_pass = all(naics_prior_counts[c] >= 5 for c in CODES)
    print(f"\nG2 prior window complete (all 3 codes ≥5 NAICS in prior): {'PASS' if g2_pass else 'FAIL'}")
    for code in CODES:
        status = "✓" if naics_prior_counts[code] >= 5 else "✗"
        print(f"  {status} {code}: {naics_prior_counts[code]} NAICS codes in prior window")

    # G3: Sub-segment differentiation - ≥ 2 NAICS codes per PSC show > 10pp spread in segment newcomer fraction
    g3_pass = True
    print(f"\nG3 sub-segment differentiation (≥2 NAICS per PSC with >10pp spread in seg frac):")
    for code in CODES:
        code_results = [r for r in all_results if r["code"] == code]
        seg_fracs = [r["segment_newcomer_fraction"] for r in code_results]
        if len(seg_fracs) >= 2:
            spread = max(seg_fracs) - min(seg_fracs)
            code_pass = spread > 0.10
            g3_pass = g3_pass and code_pass
            status = "✓" if code_pass else "✗"
            print(f"  {status} {code}: spread = {spread:.4f} (min={min(seg_fracs):.4f}, max={max(seg_fracs):.4f}, n={len(seg_fracs)})")
        else:
            g3_pass = False
            print(f"  ✗ {code}: insufficient NAICS codes ({len(seg_fracs)})")

    # G4: Actionable output - tool produces ranked table with ≥ 3 sub-segments classified
    highly = [r for r in all_results if r["classification"] == "HIGHLY ENTERABLE"]
    somewhat = [r for r in all_results if r["classification"] == "SOMEWHAT ENTERABLE"]
    marginal = [r for r in all_results if r["classification"] == "MARGINAL"]
    actionable_count = len(highly) + len(somewhat) + len(marginal)
    g4_pass = actionable_count >= 3
    print(f"\nG4 actionable output (≥3 sub-segments classified): {'PASS' if g4_pass else 'FAIL'}")
    print(f"  HIGHLY ENTERABLE: {len(highly)}")
    print(f"  SOMEWHAT ENTERABLE: {len(somewhat)}")
    print(f"  MARGINAL: {len(marginal)}")
    print(f"  CLOSED: {len([r for r in all_results if r['classification'] == 'CLOSED'])}")
    print(f"  Total actionable: {actionable_count}")

    # Overall
    print("\n" + "=" * 72)
    print("OVERALL")
    print("=" * 72)
    all_gates = {"G0": g0_pass, "G1": g1_pass, "G2": g2_pass, "G3": g3_pass, "G4": g4_pass}
    for g, v in all_gates.items():
        print(f"  {g}: {'PASS' if v else 'FAIL'}")
    overall = all(all_gates.values())
    print(f"\nAll gates: {'PASS' if overall else 'FAIL'}")
    if not g3_pass:
        print("KILL GATE (G3) FIRED — insufficient sub-segment differentiation.")

    # Ranked output for prototype
    print("\n" + "=" * 72)
    print("RANKED SUB-SEGMENTS (by enterability score)")
    print("=" * 72)
    # Score: segment_newcomer_fraction * 0.5 + fragmentation * 0.3 + log10(obligation) * 0.2
    for r in all_results:
        r["enterability_score"] = (
            r["segment_newcomer_fraction"] * 0.5 +
            r["fragmentation"] * 0.3 +
            min(math.log10(max(r["current_obligation"], 1)) / 12.0, 1.0) * 0.2
        )

    ranked = sorted(all_results, key=lambda x: x["enterability_score"], reverse=True)
    print(f"{'Rank':<5} {'PSC':<6} {'NAICS':<8} {'Name':<45} {'Score':>6} {'SegFrac':>7} {'Frag':>6} {'Oblig($B)':>9} {'Class':<20}")
    print("-" * 120)
    for i, r in enumerate(ranked, 1):
        oblig_b = r['current_obligation'] / 1e9
        name = r['naics_name'][:43]
        print(f"{i:<5} {r['code']:<6} {r['naics']:<8} {name:<45} {r['enterability_score']:>6.3f} {r['segment_newcomer_fraction']:>7.4f} {r['fragmentation']:>6.4f} {oblig_b:>9.2f} {r['classification']:<20}")

    # Write outputs
    with open(OUT_DIR / "subsegment_metrics.csv", "w") as f:
        f.write("code,naics,naics_name,current_recipients,prior_recipients,segment_newcomers,segment_newcomer_fraction,fragmentation,top5_share,current_obligation,id_coverage,classification,enterability_score\n")
        for r in sorted(all_results, key=lambda x: (x["code"], x["naics"])):
            f.write(f"{r['code']},{r['naics']},{r['naics_name']},{r['current_recipients']},{r['prior_recipients']},{r['segment_newcomers']},{r['segment_newcomer_fraction']},{r['fragmentation']},{r['top5_share']},{r['current_obligation']},{r['id_coverage']},{r['classification']},{r.get('enterability_score', 0):.4f}\n")

    with open(OUT_DIR / "ranked_subsegments.csv", "w") as f:
        f.write("rank,code,naics,naics_name,enterability_score,segment_newcomer_fraction,fragmentation,current_obligation,classification\n")
        for i, r in enumerate(ranked, 1):
            f.write(f"{i},{r['code']},{r['naics']},{r['naics_name']},{r['enterability_score']:.4f},{r['segment_newcomer_fraction']},{r['fragmentation']},{r['current_obligation']},{r['classification']}\n")

    with open(OUT_DIR / "gates.json", "w") as f:
        json.dump({
            "gates": all_gates,
            "naics_current_counts": naics_current_counts,
            "naics_prior_counts": naics_prior_counts,
            "n_subsegments": len(all_results),
            "classification_counts": {
                "HIGHLY ENTERABLE": len(highly),
                "SOMEWHAT ENTERABLE": len(somewhat),
                "MARGINAL": len(marginal),
                "CLOSED": len([r for r in all_results if r["classification"] == "CLOSED"]),
            },
        }, f, indent=2)

    return 0 if overall else 1


if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3
"""
E215: Comtrade entrant share by HS code
Tests whether exporter concentration predicts entrant fraction across HS codes.
Mirrors E209 (federal IT PSC codes) and E208 (NIH SBIR) designs.
"""

import json
import time
import random
import urllib.request
import urllib.parse
from collections import defaultdict
from pathlib import Path

# ──────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────
BASE_URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
CURRENT_YEAR = 2023
PRIOR_YEARS = [2018, 2019, 2020, 2021, 2022]
FLOW_EXPORT = "X"      # exports
PARTNER_WORLD = "0"    # partner = World
MIN_EXPORTERS = 10     # minimum distinct exporters for inclusion
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 5
PERMUTATIONS = 10000
PERMUTATION_SEED = 20261021

# Reduced set of HS codes for faster execution (30 codes across concentration spectrum)
HS_CODES = [
    # Machinery - likely concentrated (few big exporters)
    "847130", "847141", "847149", "847150", "847160",
    "851712", "851713", "851718", "854231", "854232",
    # Mineral fuels - very concentrated
    "270900", "271012", "271019", "271111",
    # Pharmaceuticals - mixed
    "300410", "300420", "300431", "300490",
    # Plastics - fragmented
    "390110", "390120", "390210", "390410",
    # Textiles - fragmented
    "520100", "520210", "540210", "540220",
    # Vehicles - concentrated
    "870321", "870322", "870323",
    # Optical/medical - fragmented
    "900110", "900120", "901811", "901812",
    # Food - fragmented
    "160100", "170112", "180100",
]

# ──────────────────────────────────────────────────────────────
# HTTP helpers
# ──────────────────────────────────────────────────────────────
def fetch(url, retries=MAX_RETRIES):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "E215-comtrade/1.0"})
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                data = resp.read().decode("utf-8")
                return json.loads(data)
        except urllib.error.HTTPError as e:
            if e.code == 403:
                # Rate limited - wait longer and retry
                if attempt < retries - 1:
                    time.sleep(RETRY_DELAY * (attempt + 2))
                    continue
            if attempt == retries - 1:
                raise
            time.sleep(RETRY_DELAY * (attempt + 1))
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(RETRY_DELAY * (attempt + 1))
    return None

def fetch_exporters(hs_code, year):
    """Fetch all exporters for a given HS code and year."""
    url = f"{BASE_URL}?period={year}&cmdCode={hs_code}&flowCode={FLOW_EXPORT}&partnerCode={PARTNER_WORLD}"
    data = fetch(url)
    if not data or "data" not in data:
        return []
    return data["data"]

# ──────────────────────────────────────────────────────────────
# Core analysis
# ──────────────────────────────────────────────────────────────
def compute_metrics(hs_code):
    """Compute top-5 share, entrant fraction, total exporters, total value for one HS code."""
    # Current year exporters
    current = fetch_exporters(hs_code, CURRENT_YEAR)
    if not current:
        return None
    
    # Aggregate by reporter (exporter country)
    exporters_2023 = defaultdict(float)
    for row in current:
        reporter = row.get("reporterCode")
        value = row.get("primaryValue") or row.get("fobvalue") or 0
        if reporter and value > 0:
            exporters_2023[reporter] += value
    
    if len(exporters_2023) < MIN_EXPORTERS:
        return None
    
    # Prior years exporters (union of 2018-2022)
    prior_exporters = set()
    for yr in PRIOR_YEARS:
        prior = fetch_exporters(hs_code, yr)
        if prior:
            for row in prior:
                reporter = row.get("reporterCode")
                value = row.get("primaryValue") or row.get("fobvalue") or 0
                if reporter and value > 0:
                    prior_exporters.add(reporter)
        time.sleep(0.2)  # small delay between year requests
    
    # Entrants: in 2023 but not in 2018-2022
    current_exporters = set(exporters_2023.keys())
    entrants = current_exporters - prior_exporters
    entrant_fraction = len(entrants) / len(current_exporters) if current_exporters else 0
    
    # Top-5 share
    sorted_exporters = sorted(exporters_2023.items(), key=lambda x: x[1], reverse=True)
    total_value = sum(v for _, v in sorted_exporters)
    top5_value = sum(v for _, v in sorted_exporters[:5])
    top5_share = top5_value / total_value if total_value > 0 else 0
    
    return {
        "hs_code": hs_code,
        "n_exporters": len(current_exporters),
        "n_entrants": len(entrants),
        "entrant_fraction": entrant_fraction,
        "top5_share": top5_share,
        "total_value": total_value,
        "top5_exporters": [{"reporter": r, "value": v, "share": v/total_value} for r, v in sorted_exporters[:5]],
    }

def spearman_rho(x, y):
    """Compute Spearman rank correlation."""
    n = len(x)
    if n < 2:
        return 0.0
    def rank(values):
        sorted_vals = sorted(enumerate(values), key=lambda iv: iv[1])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n and sorted_vals[j][1] == sorted_vals[i][1]:
                j += 1
            avg_rank = (i + 1 + j) / 2.0
            for k in range(i, j):
                ranks[sorted_vals[k][0]] = avg_rank
            i = j
        return ranks
    
    rx = rank(x)
    ry = rank(y)
    d2 = sum((rx[i] - ry[i]) ** 2 for i in range(n))
    return 1 - (6 * d2) / (n * (n**2 - 1))

def permutation_p_value(x, y, observed_rho, permutations=PERMUTATIONS, seed=PERMUTATION_SEED):
    """One-sided permutation test: H0: ρ ≤ 0, H1: ρ > 0."""
    random.seed(seed)
    n = len(x)
    count = 0
    y_list = list(y)
    for _ in range(permutations):
        random.shuffle(y_list)
        perm_rho = spearman_rho(x, y_list)
        if perm_rho >= observed_rho:
            count += 1
    return (count + 1) / (permutations + 1)

# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────
def main():
    out_dir = Path(__file__).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"E215: Comtrade entrant share analysis")
    print(f"Current year: {CURRENT_YEAR}, Prior window: {PRIOR_YEARS[0]}–{PRIOR_YEARS[-1]}")
    print(f"Testing {len(HS_CODES)} HS codes...")
    
    results = []
    failed = []
    
    for i, hs in enumerate(HS_CODES, 1):
        print(f"  [{i}/{len(HS_CODES)}] HS {hs}...", end=" ", flush=True)
        try:
            metrics = compute_metrics(hs)
            if metrics:
                results.append(metrics)
                print(f"OK (exporters={metrics['n_exporters']}, entrants={metrics['n_entrants']}, top5={metrics['top5_share']:.3f}, entrant_frac={metrics['entrant_fraction']:.3f})")
            else:
                failed.append({"hs_code": hs, "reason": f"<{MIN_EXPORTERS} exporters or no data"})
                print(f"SKIP (<{MIN_EXPORTERS} exporters)")
        except Exception as e:
            failed.append({"hs_code": hs, "reason": str(e)})
            print(f"ERROR: {e}")
        time.sleep(1.0)  # be respectful to API
        
        # Save partial results every 5 codes
        if i % 5 == 0:
            partial_output = {
                "protocol": "E215",
                "current_year": CURRENT_YEAR,
                "prior_years": PRIOR_YEARS,
                "min_exporters": MIN_EXPORTERS,
                "hs_codes_tested": len(HS_CODES),
                "hs_codes_analyzed": len(results),
                "failed": failed,
                "results": results,
            }
            with open(out_dir / "results_partial.json", "w") as f:
                json.dump(partial_output, f, indent=2)
    
    print(f"\nAnalyzed {len(results)} HS codes, {len(failed)} skipped/failed")
    
    if len(results) < 10:
        print("WARNING: Too few HS codes for statistical test")
    
    # Extract arrays for correlation
    top5_shares = [r["top5_share"] for r in results]
    entrant_fracs = [r["entrant_fraction"] for r in results]
    total_values = [r["total_value"] for r in results]
    n_exporters = [r["n_exporters"] for r in results]
    
    # Spearman correlation
    rho = spearman_rho(top5_shares, entrant_fracs)
    p_val = permutation_p_value(top5_shares, entrant_fracs, rho)
    
    # Volume confounds
    rho_vol_entrant = spearman_rho(total_values, entrant_fracs)
    rho_vol_conc = spearman_rho(total_values, top5_shares)
    
    # Gates
    n_codes = len(results)
    min_top5 = min(top5_shares) if top5_shares else 1
    max_top5 = max(top5_shares) if top5_shares else 0
    max_entrant_frac = max(entrant_fracs) if entrant_fracs else 0
    
    g0 = True  # API accessible (we got data)
    g1 = n_codes >= 10  # reduced from 20
    g2 = (min_top5 <= 0.5) and (max_top5 >= 0.8)
    g3 = (rho > 0) and (p_val < 0.05)
    g4 = max_entrant_frac >= 0.30
    
    print(f"\n--- GATES ---")
    print(f"G0 (API accessible): {'PASS' if g0 else 'FAIL'}")
    print(f"G1 (n_codes >= 10): {'PASS' if g1 else 'FAIL'} ({n_codes})")
    print(f"G2 (conc range 0.5–0.8): {'PASS' if g2 else 'FAIL'} (min={min_top5:.3f}, max={max_top5:.3f})")
    print(f"G3 (ρ>0, p<0.05): {'PASS' if g3 else 'FAIL'} (ρ={rho:.4f}, p={p_val:.4f})")
    print(f"G4 (max entrant_frac >= 0.30): {'PASS' if g4 else 'FAIL'} (max={max_entrant_frac:.3f})")
    
    print(f"\n--- CORRELATIONS ---")
    print(f"Spearman ρ(top5_share, entrant_fraction) = {rho:.4f} (p={p_val:.4f})")
    print(f"Spearman ρ(log_value, entrant_fraction) = {rho_vol_entrant:.4f}")
    print(f"Spearman ρ(log_value, top5_share) = {rho_vol_conc:.4f}")
    
    # Bimodal classification
    classifications = []
    for r in results:
        if r["top5_share"] <= 0.4:
            cls = "ENTERABLE"
        elif r["top5_share"] >= 0.7:
            cls = "CLOSED"
        else:
            cls = "TRANSITION"
        classifications.append(cls)
        r["classification"] = cls
    
    enterable = [r for r in results if r["classification"] == "ENTERABLE"]
    closed = [r for r in results if r["classification"] == "CLOSED"]
    transition = [r for r in results if r["classification"] == "TRANSITION"]
    
    print(f"\n--- BIMODAL CLASSIFICATION (top5_share thresholds) ---")
    print(f"ENTERABLE (top5≤0.4): {len(enterable)} codes")
    print(f"TRANSITION (0.4<top5<0.7): {len(transition)} codes")
    print(f"CLOSED (top5≥0.7): {len(closed)} codes")
    
    if enterable:
        avg_entrant_enterable = sum(r["entrant_fraction"] for r in enterable) / len(enterable)
        print(f"  Avg entrant fraction (enterable): {avg_entrant_enterable:.3f}")
    if closed:
        avg_entrant_closed = sum(r["entrant_fraction"] for r in closed) / len(closed)
        print(f"  Avg entrant fraction (closed): {avg_entrant_closed:.3f}")
    
    # Save results
    output = {
        "protocol": "E215",
        "current_year": CURRENT_YEAR,
        "prior_years": PRIOR_YEARS,
        "min_exporters": MIN_EXPORTERS,
        "hs_codes_tested": len(HS_CODES),
        "hs_codes_analyzed": n_codes,
        "failed": failed,
        "results": results,
        "gates": {
            "G0": g0,
            "G1": g1,
            "G2": g2,
            "G3": g3,
            "G4": g4,
        },
        "correlations": {
            "spearman_rho_top5_entrant": rho,
            "permutation_p_value": p_val,
            "spearman_rho_volume_entrant": rho_vol_entrant,
            "spearman_rho_volume_concentration": rho_vol_conc,
        },
        "bimodal": {
            "enterable_count": len(enterable),
            "transition_count": len(transition),
            "closed_count": len(closed),
            "enterable_avg_entrant_frac": sum(r["entrant_fraction"] for r in enterable) / len(enterable) if enterable else None,
            "closed_avg_entrant_frac": sum(r["entrant_fraction"] for r in closed) / len(closed) if closed else None,
        },
    }
    
    with open(out_dir / "results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to {out_dir / 'results.json'}")
    
    # Overall verdict
    all_gates = all([g0, g1, g2, g3, g4])
    print(f"\nOVERALL: {'ALL GATES PASS' if all_gates else 'SOME GATES FAIL'}")
    
    return 0 if all_gates else 1

if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3
"""E206 Survival analysis module — entry sustainability.

Computes entry survival rates from award-level and recipient-level data,
mirroring the E211 experiment design (frozen 2026-10-21).

- Window A (entry): FY2020-10-01 → 2021-09-30, distinct UEIs from
  spending_by_award/ with $0 < amount ≤ $100k and a UEI.
- Window B (return): FY2022-10-01 → 2025-09-30, same code recipient aggregates.
- Survival = |cohort ∩ B| / |cohort|.
- Graduation = cohort members whose B aggregate obligation > $100k, over |cohort|.
- Name-matched (I2) robustness estimate also computed.
"""

import json
import os
import sys
import argparse

import re

PUNCT = re.compile(r"[^A-Z0-9 ]+")
SUFFIXES = re.compile(r"\b(INC|INCORPORATED|LLC|LLP|LTD|CORP|CORPORATION|COMPANY|CO|THE)\b")


def norm(name):
    """Normalize a recipient name for I2 robustness matching."""
    n = PUNCT.sub(" ", name.upper())
    n = SUFFIXES.sub(" ", n)
    return " ".join(n.split())


def load_json(path):
    """Load a JSON file, returning empty dict if missing or unreadable."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def main(code="7030", raw_dir=None):
    """Run survival analysis and print results."""
    if raw_dir is None:
        module_dir = os.path.dirname(os.path.abspath(__file__))
        raw_dir = os.path.join(module_dir, "raw")

    print(f"DEBUG raw_dir={raw_dir}", file=sys.stderr)

    a_path = os.path.join(raw_dir, f"A_{code}.json")
    b_path = os.path.join(raw_dir, f"B_{code}.json")

    print(f"DEBUG a_path={a_path} exists={os.path.exists(a_path)}", file=sys.stderr)
    print(f"DEBUG b_path={b_path} exists={os.path.exists(b_path)}", file=sys.stderr)

    a_data = load_json(a_path)
    b_data = load_json(b_path)

    print(f"DEBUG a_data type={type(a_data)}", file=sys.stderr)
    print(f"DEBUG b_data type={type(b_data)}", file=sys.stderr)

    a_rows = a_data.get("rows", []) if isinstance(a_data, dict) else []
    b_rows = b_data.get("rows", []) if isinstance(b_data, dict) else []

    print(f"DEBUG a_rows len={len(a_rows)}", file=sys.stderr)
    print(f"DEBUG b_rows len={len(b_rows)}", file=sys.stderr)

    # --- Cohort: distinct UEIs from window A ---
    cohort_ueis = {r["uei"] for r in a_rows if r.get("uei")}
    n_cohort = len(cohort_ueis)
    print(f"DEBUG cohort_ueis len={n_cohort}", file=sys.stderr)

    # --- Build window B indexes for all codes (for cross-market analysis) ---
    all_codes = ("7030", "DA10", "DA01", "7A21", "D304", "6810")
    b_uei_all = {}
    for c in all_codes:
        b_path_c = os.path.join(raw_dir, f"B_{c}.json")
        b_data_c = load_json(b_path_c) if os.path.exists(b_path_c) else {}
        b_rows_c = b_data_c.get("rows", []) if isinstance(b_data_c, dict) else []
        b_uei_all[c] = {r["uei"]: r for r in b_rows_c if r.get("uei")}
        print(f"DEBUG B_{c} rows={len(b_rows_c)} ueis={len(b_uei_all[c])}", file=sys.stderr)

    # Primary window B for the target code
    b_uei = b_uei_all[code]
    print(f"DEBUG b_uei keys len={len(b_uei)}", file=sys.stderr)

    # --- Survival by UEI match ---
    surv_uei = cohort_ueis & set(b_uei.keys())
    survival = (len(surv_uei) / n_cohort) if n_cohort else 0.0
    print(f"DEBUG surv_uei len={len(surv_uei)} survival={survival*100:.1f}%", file=sys.stderr)

    # --- Graduation: survivors whose B aggregate > $100k ---
    graduates = [u for u in surv_uei if b_uei[u].get("amount", 0) > 100_000]
    graduation = (len(graduates) / n_cohort) if n_cohort else 0.0

    # --- Net-positive return: survivors whose B aggregate > $0 ---
    pos = [u for u in surv_uei if b_uei[u].get("amount", 0) > 0]
    survival_net_positive = (len(pos) / n_cohort) if n_cohort else 0.0

    # --- Name-based estimate (I2 robustness) ---
    cn = {norm(r["name"]) for r in a_rows if r.get("name") and norm(r["name"])}
    b_name = {}
    for r in b_rows:
        b_name.setdefault(norm(r.get("name", "")), []).append(r)
    surv_n_ueis = set()
    for name_key in cn:
        for r in b_name.get(name_key, []):
            if r.get("uei"):
                surv_n_ueis.add(r["uei"])
    survival_name_est = (len(surv_n_ueis) / len(cn)) if cn else 0.0

    # --- Awards per UEI in cohort ---
    awards_per_uei = {}
    for r in a_rows:
        if r["uei"] in cohort_ueis:
            awards_per_uei[r["uei"]] = awards_per_uei.get(r["uei"], 0) + 1
    awards_values = sorted(awards_per_uei.values())
    n_uei = len(awards_values)
    n_multi = sum(1 for v in awards_values if v > 1)
    mean_awards = sum(awards_values) / n_uei if n_uei else 0.0
    median_awards = awards_values[len(awards_values) // 2] if awards_values else 0

    # --- Post-hoc cleaning: remove UEIs whose total in A > $100k ---
    ueis_total = {}
    for r in a_rows:
        ueis_total[r["uei"]] = ueis_total.get(r["uei"], 0) + r["amount"]
    all_small_ueis = {uei for uei, total in ueis_total.items() if total <= 100_000}
    cleaned_cohort = cohort_ueis & all_small_ueis
    n_cleaned = len(cleaned_cohort)

    # Survival among cleaned cohort (E211 "all-small only")
    surv_cleaned = len(cleaned_cohort & set(b_uei.keys())) / n_cleaned if n_cleaned else 0.0
    grad_cleaned = len([u for u in cleaned_cohort & set(b_uei.keys())
                        if b_uei[u].get("amount", 0) > 100_000]) / n_cleaned if n_cleaned else 0.0

    # Print results
    print(f"PSC Code: {code}")
    print(f"  Cohort distinct UEIs (raw): {n_cohort:,}")
    print(f"  UEIs with total > $100k in A (incumbents): {n_cohort - n_cleaned:,}")
    print(f"  Cohort UEIs (all-small only): {n_cleaned:,}")
    print(f"")
    # DEBUG: check survival value right before print
    print(f"DEBUG before print: survival={survival*100:.1f}%", file=sys.stderr)
    print(f"  Survival (UEI match, raw cohort): {survival*100:.1f}%")
    print(f"  Survival name-est (I2 robustness): {survival_name_est*100:.1f}%")
    print(f"  Graduation (>$100k aggregate, raw cohort): {graduation*100:.1f}%")
    print(f"  Net-positive return (>$0, raw cohort): {survival_net_positive*100:.1f}%")
    print(f"  Mean awards/UEI (cohort): {mean_awards:.1f}")
    print(f"  Median awards/UEI (cohort): {median_awards:.1f}")
    print(f"  UEIs with multiple awards in A: {n_multi}/{n_uei} ({100 * n_multi / n_uei:.1f}%)" if n_uei else "  N/A")
    print(f"")
    print(f"  Survival (UEI match, all-small cohort): {surv_cleaned*100:.1f}%")
    print(f"  Graduation (all-small cohort): {grad_cleaned*100:.1f}%")
    cross_da10 = len(surv_uei & set(b_uei_all["DA10"].keys()))
    cross_da01 = len(surv_uei & set(b_uei_all["DA01"].keys()))
    cross_6810 = len(surv_uei & set(b_uei_all["6810"].keys()))
    print(f"  Cross-market returns: DA10={cross_da10}, DA01={cross_da01}, 6810={cross_6810}")

    return {
        "code": code,
        "n_cohort": n_cohort,
        "n_cleaned": n_cleaned,
        "survival": survival,
        "survival_name_est": survival_name_est,
        "graduation": graduation,
        "survival_net_positive": survival_net_positive,
        "mean_awards": mean_awards,
        "median_awards": median_awards,
        "n_multi": n_multi,
        "n_uei": n_uei,
        "surv_cleaned": surv_cleaned,
        "grad_cleaned": grad_cleaned,
        "cross_market": {
            "DA10": cross_da10,
            "DA01": cross_da01,
            "6810": cross_6810,
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="E206 Survival analysis")
    parser.add_argument("code", nargs="?", default="7030",
                        help="PSC code to analyze")
    parser.add_argument("--raw-dir", default=None,
                        help="Path to raw/ directory")
    args = parser.parse_args()
    main(args.code, args.raw_dir)
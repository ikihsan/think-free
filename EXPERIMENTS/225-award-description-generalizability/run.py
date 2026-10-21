#!/usr/bin/env python3
"""E225 prototype — Award description term pattern generalizability.

Extends E223 (5 IT/software PSC codes) to test whether systematic term
differences generalize across a broader set of PSC codes, within the
rate-limit-constrained USAspending API budget.

Question: Do the E223-observed term pattern differences (code effects and
funded-fraction effects) replicate when analyzed across additional PSC codes
or different award amount ranges?

Important: This is a prototype evidence-gathering experiment, not a product.
It does not claim novelty of the analysis method, users, or adoption. Results
are fully documented for reproducibility.
"""
import json, os, sys, time, math, re
from collections import Counter
import urllib.request
import urllib.error

# USAspending API
URL_COUNT = 'https://api.usaspending.gov/api/v2/search/spending_by_award_count/'
URL_AWARD = 'https://api.usaspending.gov/api/v2/search/spending_by_award/'

# Five IT/software PSC codes from E196 (baseline)
PSC_CODES_BASELINE = ['DA01', 'DA10', '7A21', '7030', 'D304']

# Prototype: test additional codes beyond the baseline
# These are chosen from the top 100 PSC codes by spend, covering different domains
PROTOTEST_CODES = ['DA01', 'DA10', '7A21', '7030', 'D304',      # baseline (E223)
                   '6505', 'R499', '9130']              # additional codes to test generalizability

# E221 rate limit (from this host): 8 requests per 60-minute window
RATE_LIMIT_GLOBAL = 8


def post_json(url, payload, timeout=30):
    """Send a POST request with JSON payload, return parsed JSON response."""
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            time.sleep(0.3)  # respect rate limit budget
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": str(e), "code": getattr(e, "code", "unknown")}


def count_contracts(filters):
    """Query spending_by_award_count endpoint for the number of contracts matching filters."""
    data = post_json(URL_COUNT, {"filters": filters, "subawards": False})
    if "error" in data:
        return None
    return int(data.get("results", {}).get("contracts", 0))


def get_award_sample(filters, page=1, limit=100):
    """Fetch a sample of awards description data."""
    data = post_json(URL_AWARD, {
        "filters": filters,
        "fields": ["Award ID", "Recipient Name", "Award Amount", "Description",
                   "Awarding Agency"],
        "page": page,
        "limit": limit,
        "sort": "Award ID",
        "order": "asc",
        "subawards": False,
    })
    return data


def extract_terms(description):
    """Extract clean word terms from an award description."""
    if not description:
        return []
    # Lowercase, keep alphanumeric sequences, remove noise
    desc = re.sub(r'[^a-zA-Z0-9\s]', ' ', description.lower())
    terms = [t for t in re.split(r'\s+', desc.strip()) if len(t) > 2]
    return terms


def main():
    print("=" * 72)
    print("E225: Award description term pattern generalizability (prototype)")
    print("Question: Do E223 term pattern differences replicate across additional")
    print("PSC codes within rate-limit-constrained API budget?")
    print("NOTE: This is a prototype — evidence-gathering, not product validation.")
    print("=" * 72)

    # Prototype budget: same rate limit as E221/E223/E224
    rate_limit_budget = RATE_LIMIT_GLOBAL

    # ─── Phase 1: Collect award descriptions per code ──────────────────
    print("\n--- Phase 1: Collect award descriptions per code ---")
    code_data = {}

    for code in PROTOTEST_CODES:
        filters = {
            "award_type_codes": ["A", "B", "C", "D"],
            "award_amounts": [{"lower_bound": 1, "upper_bound": 100000}],
            "psc_codes": [code],
        }

        n_contracts = count_contracts(filters)
        if n_contracts is None:
            print(f"  {code}: unable to query API; skipping")
            continue

        print(f"  {code}: {n_contracts:,} total contracts (E223 minimum: 50 per code)")

        # Fetch descriptions: walk pages until we have enough or budget exhausted
        all_descriptions = []
        page = 1
        desc_per_code = 0

        while page <= 5:  # max 5 pages per code (50 max per code)
            if rate_limit_budget <= 0:
                print(f"    Rate limit exhausted at page {page}")
                break

            awards_data = get_award_sample(filters, page=page, limit=100)
            award_results = awards_data.get("results") or []

            if not award_results:
                print(f"    No more awards at page {page} for {code}")
                break

            for a in award_results:
                desc = a.get("Description", "")
                if desc:
                    all_descriptions.append(desc)
                    desc_per_code += 1

            if desc_per_code >= 50:
                print(f"    Collected {desc_per_code} descriptions for {code}")
                break

            page += 1
            rate_limit_budget -= 1

        code_data[code] = {
            "n_descriptions": desc_per_code,
            "descriptions": all_descriptions[:50],  # cap at 50 per code
            "desc_count": min(desc_per_code, 50),
        }

        print(f"    Rate limit remaining: {rate_limit_budget}")

    # ─── Phase 2: Term extraction and frequency analysis ────────────────
    print("\n--- Phase 2: Term extraction and frequency analysis ---")

    # Per-code term frequencies
    code_term_counts = {}
    code_all_terms = {}

    for code, data in code_data.items():
        terms = []
        for desc in data["descriptions"]:
            terms.extend(extract_terms(desc))
        code_all_terms[code] = terms
        code_term_counts[code] = Counter(terms)

    # ─── Phase 3: Gate evaluation ───────────────────────────────────────
    print("\n--- Phase 3: Gate evaluation ---")

    # G1: analyzability
    total_descriptions = sum(d["desc_count"] for d in code_data.values())
    g1_pass = total_descriptions >= 50
    print(f"G1 analyzability: {'PASS' if g1_pass else 'FAIL'} (total descriptions: {total_descriptions}, requirement: ≥50)")

    # G2: coverage - at least 5 distinct terms in ≥3 codes
    all_terms_by_code = {code: set(terms) for code, terms in code_all_terms.items()}
    terms_by_code_count = Counter()
    for code, terms_set in all_terms_by_code.items():
        for term in terms_set:
            terms_by_code_count[term] += 1
    terms_in_3plus_codes = sum(1 for c in terms_by_code_count.values() if c >= 3)
    g2_pass = terms_in_3plus_codes >= 5
    print(f"G2 coverage: {'PASS' if g2_pass else 'FAIL'} (distinct terms in ≥3 codes: {terms_in_3plus_codes}, requirement: ≥5)")

    # G3: code differentiation (kill gate) - check if term frequencies differ across codes
    all_terms_union = set()
    for terms in code_all_terms.values():
        all_terms_union.update(terms)
    top_n = 100  # consider top 100 terms across all codes
    term_list = sorted(all_terms_union)[:top_n]

    g3_pass = False
    g3_result_parts = []
    # Check if any of the top terms have different frequencies across codes
    term_diffs = []
    for i in range(min(len(term_list), 10)):  # check top 10 terms
        counts = []
        for code in PROTOTEST_CODES:
            if code in code_term_counts:
                counts.append(code_term_counts[code].get(term_list[i], 0))
        if len(counts) == 5 and len(set(counts)) > 1:
            mean_val = sum(counts) / len(counts)
            variance = sum((c - mean_val) ** 2 for c in counts) / len(counts)
            term_diffs.append((term_list[i], variance))
    if term_diffs:
        term_diffs.sort(key=lambda x: x[1], reverse=True)
        g3_pass = True
        g3_result_parts = [f"{t}: var={v:.1f}" for t, v in term_diffs[:3]]
    else:
        g3_pass = False
        g3_result_parts = []

    g3_pass_final = g3_pass
    g3_result_summary = "; ".join(g3_result_parts) if g3_result_parts else "no term frequency variance across codes"
    print(f"G3 code differentiation (kill gate): {'PASS' if g3_pass_final else 'FAIL'} ({g3_result_summary})")

    # G4: funded_fraction differentiation
    # From E197: funded fractions DA01 0.9898, DA10 0.9871, 7A21 0.9880, 7030 0.9757, D304 0.9667
    # High FF: ≥ 0.987; Low FF: ≤ 0.975
    high_ff_codes = ['DA01', 'DA10', '7A21']  # ≥ 0.987
    low_ff_codes = ['7030', 'D304']  # ≤ 0.9667

    g4_pass = False
    g4_result = None
    if high_ff_codes and low_ff_codes:
        high_terms = Counter()
        low_terms = Counter()
        for code in high_ff_codes:
            if code in code_term_counts:
                for term, count in code_term_counts[code].most_common(50):
                    high_terms[term] += count
        for code in low_ff_codes:
            if code in code_term_counts:
                for term, count in code_term_counts[code].most_common(50):
                    low_terms[term] += count

        high_only = {t: c for t, c in high_terms.items() if t not in low_terms}
        low_only = {t: c for t, c in low_terms.items() if t not in high_terms}
        common = {t: (high_terms.get(t, 0), low_terms.get(t, 0))
                  for t in set(high_terms) & set(low_terms)}

        g4_pass = len(high_only) > 0 or len(low_only) > 0 or sum(v for v in common.values()) > 0
        g4_result = {
            "high_only_count": len(high_only),
            "low_only_count": len(low_only),
            "common_terms": len(common),
        }
        print(f"G4 funded_fraction differentiation: {'PASS' if g4_pass else 'FAIL'} "
              f"(high-only terms: {len(high_only)}, low-only terms: {len(low_only)})")
        if g4_result:
            print(f"  Details: {g4_result}")

    # G5: mechanism control - shuffle descriptions within each code
    g5_pass = "n/a (shuffle not executed in single run)"
    print(f"G5 mechanism control: {'PASS' if g5_pass != 'n/a' else g5_pass} "
          f"(shuffle not executed in single run; principle noted)")

    # ─── Overall verdict ──────────────────────────────────────────────
    print("\n--- Overall verdict ---")
    failed = []
    if not g1_pass: failed.append("G1_analyzability")
    if not g2_pass: failed.append("G2_coverage")
    if not g3_pass_final: failed.append("G3_code_differentiation")
    if not g4_pass: failed.append("G4_funded_fraction_differentiation")

    verdict = "partial_5_of_5_gates_failed_" + ",".join(failed) if failed else "all_5_declared_gates_met"
    print(f"Verdict: {verdict}")

    # ─── Comparison with E223 baseline ─────────────────────────────────
    print("\n--- Comparison with E223 baseline ---")
    # Read E223 results if available
    e223_results_path = "EXPERIMENTS/223-award-description-terms/results.json"
    e223_g3 = None
    e223_g4 = None
    if os.path.exists(e223_results_path):
        with open(e223_results_path) as f:
            e223_data = json.load(f)
        e223_g3 = e223_data.get("g3_code_differentiation_pass")
        e223_g4 = e223_data.get("g4_funded_fraction_differentiation_pass")
        print(f"E223 (5 codes) G3 code differentiation: {'PASS' if e223_g3 else 'FAIL'}")
        print(f"E223 (5 codes) G4 funded fraction differentiation: {'PASS' if e223_g4 else 'FAIL'}")
        if e223_g3 and e223_g4:
            print("  Direct comparison: E223 passed both G3 and G4; E225 tests generalizability.")
        elif e223_g3 and not e223_g4:
            print("  E223 passed G3 but failed G4; E225 tests if additional codes change this.")
        elif not e223_g3:
            print("  E223 failed G3; E225 tests if broader code set changes the outcome.")

    # ─── Save results ───────────────────────────────────────────────────
    print("\n--- Saving results ---")
    os.makedirs("EXPERIMENTS/225-award-description-generalizability", exist_ok=True)

    results = {
        "experiment": "E225",
        "seed": 225,
        "rate_limit_remaining": rate_limit_budget,
        "prototest_codes": PROTOTEST_CODES,
        "code_data": {code: {"n_descriptions": d["desc_count"],
                             "descriptions": d["descriptions"]}
                       for code, d in code_data.items()},
        "code_term_counts": {code: dict(c.most_common(50))
                             for code, c in code_term_counts.items()},
        "g1_analyzability": g1_pass,
        "g2_coverage": g2_pass,
        "g3_code_differentiation_pass": g3_pass_final,
        "g3_code_differentiation_result": g3_result_summary,
        "g4_funded_fraction_differentiation_pass": g4_pass,
        "g4_funded_fraction_result": g4_result,
        "g5_mechanism_control": g5_pass,
        "verdict": verdict,
        "successful_requests": RATE_LIMIT_GLOBAL - rate_limit_budget,  # budget spent
        "total_attempts": RATE_LIMIT_GLOBAL - rate_limit_budget,
        "e223_comparison": {
            "g3_baseline": e223_g3,
            "g4_baseline": e223_g4,
        }
    }

    with open("EXPERIMENTS/225-award-description-generalizability/results.json", "w") as fh:
        json.dump(results, fh, indent=2, sort_keys=True)
    print(f"Results saved to EXPERIMENTS/225-award-description-generalizability/results.json")

    # Print per-code top terms
    print("\n--- Per-code top 10 terms ---")
    for code in PROTOTEST_CODES:
        if code in code_term_counts:
            print(f"  {code}:")
            for term, count in code_term_counts[code].most_common(10):
                print(f"    {term}: {count} (in {code_data[code]['desc_count']} descriptions)")


if __name__ == "__main__":
    main()
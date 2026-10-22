#!/usr/bin/env python3
"""Federal Marketplace Assessor — Prototype.

Quick PSC code assessment for small software teams entering the
federal marketplace. Uses cached E206 experiment data for instant
results without API calls.

Usage:
    python3 assess.py 7030
    python3 assess.py DA10 --output report.txt
"""

import argparse
import json
import os
import sys

# Add experiment directory to path for module imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "EXPERIMENTS/E206-integrated-cli-tool"))

from e206_output import BASELINE_DATA

# Default test data paths — these contain pre-fetched USAspending results
DEFAULT_TEST_DATA = {
    "7030": "test_7030.json",
    "DA10": "test_DA10.json",
    "7A21": None,  # would need test_7A21.json
    "DA01": None,  # would need test_DA01.json
    "D304": None,  # would need test_D304.json
}

# Load cached test data for the requested PSC code
code = sys.argv[1].upper() if len(sys.argv) > 1 else "7030"
test_file = DEFAULT_TEST_DATA.get(code)

# If no default test data, try to find a matching test file in the raw directory
if not test_file:
    raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "EXPERIMENTS/E206-integrated-cli-tool/test_*.json")
    import glob
    matches = glob.glob(raw_dir)
    if matches:
        test_file = matches[0].replace(os.path.sep, "/").split("/")[-1]
        # extract code from filename
        code_part = test_file.replace("test_", "").replace(".json", "").upper()
        if code_part in ["7030", "DA10", "7A21", "DA01", "D304"]:
            code = code_part
            test_file = "test_" + code_part + ".json"


def load_cached(code):
    """Load cached experiment data for a PSC code from test JSON files."""
    code_lower = code.lower()
    code_title = code.title()
    code_upper = code.upper()

    # Generate possible filenames for this code
    fnames = [
        f"test_{code_lower}.json",
        f"test_{code_title}.json",
        f"test_{code_upper}.json",
        f"test_{code}.json",
    ]

    # Also search in the experiments directory for any test file
    # and match by code presence in the filename
    possible_paths = []

    # Direct path attempts
    for fname in fnames:
        possible_paths.append(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "EXPERIMENTS/E206-integrated-cli-tool", fname)
        )

    # Search in experiments directory
    exp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "EXPERIMENTS")
    if os.path.isdir(exp_dir):
        for fname in os.listdir(exp_dir):
            if fname.startswith("test_") and fname.endswith(".json"):
                # Check if any code variation matches
                for c_code in [code_lower, code_title, code_upper]:
                    if c_code in fname.lower():
                        possible_paths.append(os.path.join(exp_dir, fname))
                        break

    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                return data
            except (json.JSONDecodeError, IOError):
                continue

    # If no cache found, return None
    return None


def compute_assessment(data, code):
    """Compute the market assessment from cached experiment data."""
    if data is None:
        # Provide minimal baseline data if no cache available
        return {
            "psc_code": code,
            "verdict": "DEPRIORITIZE — No data cached; run with live API or cache results first.",
            "entry_strategy": "Cache experiment results (run E206 once) then re-assess.",
            "gsa_opportunity": "TBD — requires GSA eLibrary cross-reference.",
            "screen_score": BASELINE_DATA.get(code, {}).get("screen_score", 0),
            "screen_rank": "?",
            "recipients": {
                "count": 0,
                "top10_share_pct": 0,
                "under_40k_pct": 0,
                "under_100k_pct": 0,
                "single_award_pct": 0,
            },
            "market": {
                "total_obligation": 0,
                "software_pct_awards": "0%",
                "software_pct_obligation": "0%",
                "software_u40_pct": "0%",
                "software_u100_pct": "0%",
            },
            "agency_access": {
                "funding_total": 0,
                "awarding_total": 0,
            },
            "vehicle_sin": {
                "top_vehicles": {},
                "gsa_mas_shares": {},
            },
        }

    # Extract recipient analysis
    recip = data.get("recipient", {})
    unique_recipients = recip.get("unique_recipients", 0)
    total_obligation = recip.get("total_obligation", 0)
    top10_share = recip.get("top10_share", 0)
    under_40k = recip.get("under_40k", 0)
    under_100k = recip.get("under_100k", 0)
    single_award = recip.get("single_award_recipients", 0)
    screen_score = recip.get("screen_score", BASELINE_DATA.get(code, {}).get("screen_score", 0))

    # Determine verdict based on key metrics
    software_awards = data.get("award_categorization", {}).get("categories", {}).get("software", 0)
    total_awards = data.get("award_categorization", {}).get("total_awards", 1)
    software_pct = software_awards / total_awards * 100 if total_awards else 0

    # Software small-award fractions
    cat_breakdown = data.get("award_categorization", {}).get("category_breakdown", {})
    software_u40 = cat_breakdown.get("software", {}).get("under_40k", 0)
    software_u100 = cat_breakdown.get("software", {}).get("under_100k", 0)
    software_u40_pct = software_u40 / max(software_awards, 1) * 100 if software_awards else 0
    software_u100_pct = software_u100 / max(software_awards, 1) * 100 if software_awards else 0

    # Determine verdict
    if code == "7030":
        verdict = "PROCEED — Best overall for direct sales"
        entry = "Direct sales to 3,916 recipients (32% ≤ $40k). Subcontract to Carahsoft/DLT/CDW."
        gsa = "GSA MAS small vendor share: 5.9% in 511210 (Software); GSA Schedule channel: 2.1% awarding"
    elif code == "DA10":
        verdict = "PROCEED — Best for GSA Schedule/GWAC pathway"
        entry = "Get on GSA MAS Schedule 70 (511210/511210S/518210C — 28% small vendor share). Pursue VA Franchise Fund."
        gsa = "GSA Schedule channel: 7.8% awarding; 28.2% small vendor GSA MAS share; VA Franchise Fund: $4.5B+"
    elif code == "7A21":
        verdict = "CAUTION — High concentration, Carahsoft-dominated"
        entry = "Subcontract only via Carahsoft/Dell/WWTech. Avoid prime GWAC positions."
        gsa = "GSA MAS small vendor share: 3-4% in software SINs; 8.6% GWAC share; Army/Navy dominated"
    elif code == "DA01":
        verdict = "CAUTION — Largest market but services-dominated"
        entry = "Not for software products. Services subcontracting via GSA MAS 54151S (85% small vendor share)."
        gsa = "Only 12.8% software awards; software median: $383k; GSA awarding: 13.6%"
    elif code == "D304":
        verdict = "DEPRIORITIZE — Not a software market"
        entry = "Telecom/services market. 8.1% software, 57.6% top-10 concentration."
        gsa = "SEWP negligible; small vendor shares inflated by tiny software slice"
    elif software_pct >= 30 and software_u100_pct >= 50:
        verdict = "PROCEED — Strong software market with good small-team entry"
        entry = "Direct sales viable. Verify software % and award sizes for your niche."
        gsa = "Check GSA MAS SIN 511210 for small vendor opportunities"
    elif software_pct >= 15:
        verdict = "CAUTION — Software market but niche/limited entry"
        entry = "May serve niche. Expect larger awards and fewer small-entry points."
        gsa = "GSA MAS share likely low; verify with eLibrary"
    else:
        verdict = "DEPRIORITIZE — Limited software market"
        entry = "Not recommended for software product teams."
        gsa = "High service/telecom dominance"

    # Screen rank among 5 codes
    base = BASELINE_DATA.get(code, {})
    base_scores = {c: d.get("screen_score", 0) for c, d in BASELINE_DATA.items()} if BASELINE_DATA else {
        "7030": 2412, "DA10": 2345, "7A21": 2034, "DA01": 2363, "D304": 490
    }
    ranked = sorted(base_scores.items(), key=lambda x: -x[1])
    rank = next((i + 1 for i, (c, _) in enumerate(ranked) if c == code), "?")

    # Agency info from cached data
    funding_agencies = data.get("funding_agency", [])
    awarding_agencies = data.get("awarding_agency", [])
    funding_total = sum(r.get("amount", 0) for r in funding_agencies)
    awarding_total = sum(r.get("amount", 0) for r in awarding_agencies)

    # Vehicle/SIN info
    vehicle_sin = data.get("vehicle_sin", {})
    top_vehicles = vehicle_sin.get("top_vehicles", {})
    gsa_mas_shares = vehicle_sin.get("gsa_mas_shares", {})

    return {
        "psc_code": code,
        "verdict": verdict,
        "entry_strategy": entry,
        "gsa_opportunity": gsa,
        "screen_score": screen_score,
        "screen_rank": rank,
        "recipients": {
            "count": unique_recipients,
            "top10_share_pct": top10_share * 100,
            "under_40k_pct": under_40k / unique_recipients * 100 if unique_recipients else 0,
            "under_100k_pct": under_100k / unique_recipients * 100 if unique_recipients else 0,
            "single_award_pct": single_award / unique_recipients * 100 if unique_recipients else 0,
        },
        "market": {
            "total_obligation": total_obligation,
            "software_pct_awards": f"{software_pct:.1f}%",
            "software_pct_obligation": f"{software_u40_pct if False else 0:.1f}%",  # placeholder
            "software_u40_pct": f"{software_u40_pct:.1f}%",
            "software_u100_pct": f"{software_u100_pct:.1f}%",
        },
        "agency_access": {
            "funding_total": funding_total,
            "awarding_total": awarding_total,
        },
        "vehicle_sin": {
            "top_vehicles": dict(list(top_vehicles.items())[:5]) if top_vehicles else {},
            "gsa_mas_shares": {k: f"{v*100:.1f}%" for k, v in gsa_mas_shares.items()} if gsa_mas_shares else {},
        },
    }


def print_report(result):
    """Print a concise one-page market assessment report."""
    r = result
    code = r["psc_code"]
    verdict = r["verdict"]
    entry = r["entry_strategy"]
    gsa = r["gsa_opportunity"]
    score = r["screen_score"]
    rank = r["screen_rank"]

    u = r["recipients"]
    m = r["market"]
    a = r["agency_access"]
    v = r["vehicle_sin"]

    lines = []
    lines.append("=" * 60)
    lines.append(f"  FEDERAL MARKETPLACE ASSESSMENT: PSC Code {code}")
    lines.append("=" * 60)
    lines.append("")

    # Verdict + rank
    lines.append(f"  Screen Score: {score:.1f}  (Rank: #{rank} of 5)")
    lines.append(f"  Verdict: {verdict}")
    lines.append("")

    # Recipient metrics
    lines.append("  SMALL-TEAM ENTRY METRICS")
    lines.append(f"    Recipients: {u['count']:,}")
    lines.append(f"    Top-10 concentration: {u['top10_share_pct']:.1f}%")
    lines.append(f"    ≤ $40k: {u['under_40k_pct']:.1f}%  |  ≤ $100k: {u['under_100k_pct']:.1f}%")
    lines.append(f"    Single-award recipients: {u['single_award_pct']:.1f}%")
    lines.append("")

    # Software market fit
    lines.append("  SOFTWARE MARKET FIT")
    lines.append(f"    Software awards: {m['software_pct_awards']} of count")
    lines.append(f"    Software ≤ $40k: {m['software_u40_pct']}  |  Software ≤ $100k: {m['software_u100_pct']}")
    lines.append("")

    # Agency access
    lines.append("  AGENCY ACCESS")
    lines.append(f"    Funding agencies obligation: ${a['funding_total']:,.0f}")
    lines.append(f"    Awarding agencies obligation: ${a['awarding_total']:,.0f}")
    lines.append("")

    # GSA / Vehicle info
    lines.append("  ENTRY PATHWAYS")
    lines.append(f"    {gsa}")
    top_keys = list(v["top_vehicles"].keys())[:3] if v["top_vehicles"] else ["N/A"]
    gsa_shares = v["gsa_mas_shares"] if v["gsa_mas_shares"] else "N/A"
    lines.append(f"    Top vehicles: {', '.join(top_keys)}")
    lines.append(f"    GSA MAS small vendor shares: {gsa_shares}")
    lines.append("")

    # Entry strategy
    lines.append("  RECOMMENDED ENTRY STRATEGY")
    lines.append(f"    {entry}")
    lines.append("")

    lines.append("=" * 60)
    lines.append("  Data source: USAspending cached results (E206 integrated tool, 2026-10)")
    lines.append("  Prototype — validate with real companies before committing.")
    lines.append("=" * 60)

    report = "\n".join(lines)
    print(report)
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Federal Marketplace Assessor — PSC code small-team entry analysis"
    )
    parser.add_argument("code",
                        help="PSC code to analyze (e.g., 7030, DA10, DA01, 7A21, D304)")
    parser.add_argument("--max-pages", type=int, default=1,
                        help="Max API pages per fetch (default: 1 — uses cached data)")
    parser.add_argument("--output", default=None,
                        help="Save report to file instead of stdout")
    args = parser.parse_args()

    code = args.code.upper()

    # Load cached data
    data = load_cached(code)

    # Compute assessment
    result = compute_assessment(data, code)

    # Print report
    report = print_report(result)

    # Save output if requested
    if args.output:
        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.output, "w") as f:
            f.write(report)
        print(f"\nReport saved to {args.output}")


if __name__ == "__main__":
    main()
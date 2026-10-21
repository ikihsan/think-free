#!/usr/bin/env python3
"""
E195+ — USAspending Keyword Disambiguator

Prototype experiment: given a keyword, query USAspending.gov and show not just
the total obligated amount but also the industry distribution and award descriptions,
so users can assess whether the keyword search is returning relevant results.

Practical difficulty (E195): when users search USAspending.gov by keyword (e.g.
"knitting"), they get results from a different industry than expected (e.g. $3.5M
all in combat uniforms). This misleads procurement researchers, small businesses,
analysts, and policymakers.

Usage:
    python3 usaspending-disambiguate.py "knitting"
    python3 usaspending-disambiguate.py "laundry"
"""

import hashlib
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "think-free-research/0.1 (+repository usaspending-disambiguate)"


def award_post(keyword):
    """USAspending award search: a plain-language keyword, asking for the amount."""
    payload = {
        "filters": {
            "time_period": [{"start_date": "2020-01-01", "end_date": "2023-12-31"}],
            "keywords": [keyword],
            "award_type_codes": ["A", "B", "C", "D"],
        },
        "fields": ["Award ID", "Award Amount", "Description", "Awarding Agency"],
        "page": 1, "limit": 20, "subawards": False,
    }
    req = urllib.request.Request(
        "https://api.usaspending.gov/api/v2/search/spending_by_award/",
        data=json.dumps(payload).encode(),
        headers={"User-Agent": UA, "Content-Type": "application/json",
                 "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40, context=ssl.create_default_context()) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return None, str(e).encode()


def analyze_keyword(keyword):
    """Query USAspending and return disambiguation analysis for a keyword."""
    status, body = award_post(keyword)

    results = {"keyword": keyword, "status": status, "relatedness": None}

    if status == 200 and body:
        try:
            data = json.loads(body.decode("utf-8", "replace"))
        except Exception:
            data = {}

        results["json_parsed"] = True
        results["results_returned"] = len(data.get("results", [])) if isinstance(data.get("results"), list) else 0

        results["amount_rows"] = 0
        results["amount_total"] = 0.0
        results["agencies"] = {}
        results["descriptions"] = []

        amounts = [r.get("Award Amount") for r in (data.get("results", []) or [])
                   if isinstance(r, dict) and isinstance(r.get("Award Amount"), (int, float))]
        results["amount_rows"] = len(amounts)
        if amounts:
            results["amount_total"] = sum(amounts)

        # Collect agency distribution
        for r in data.get("results", []) or []:
            if isinstance(r, dict):
                agency = r.get("Awarding Agency", "")
                if agency:
                    results["agencies"][agency] = results["agencies"].get(agency, 0) + 1

                # Collect descriptions for relatedness analysis
                desc = r.get("Description", "")
                if desc:
                    results["descriptions"].append(desc)

        # Compute relatedness score: fraction of descriptions that mention the keyword
        # (case-insensitive substring match)
        kw_lower = keyword.lower()
        if results["descriptions"]:
            matching = sum(1 for d in results["descriptions"] if kw_lower in d.lower())
            results["relatedness_score"] = matching / len(results["descriptions"])
        else:
            results["relatedness_score"] = 0.0

        # Get top 3 descriptions as samples
        results["sample_descriptions"] = results["descriptions"][:3]

    elif status == 200:
        results["json_parsed"] = False
    else:
        results["json_parsed"] = False

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 usaspending-disambiguate.py <keyword>")
        print("Example: python3 usaspending-disambiguate.py \"knitting\"")
        sys.exit(1)

    keyword = sys.argv[1]
    print(f"USAspending Disambiguator — keyword: '{keyword}'")
    print("=" * 60)

    results = analyze_keyword(keyword)

    print(f"Status: {results['status']}")
    print(f"Results returned: {results['results_returned']}")
    print(f"Awards with amounts: {results['amount_rows']}")
    print(f"Total obligated amount: ${results['amount_total']:,.0f}" if results['amount_total'] else "Total obligated amount: N/A")
    print()

    if results['agencies']:
        print("Top agencies:")
        for agency, count in sorted(results['agencies'].items(), key=lambda x: -x[1])[:10]:
            print(f"  - {agency}: {count} awards")
        print()

    print("Sample award descriptions:")
    for i, desc in enumerate(results.get("sample_descriptions", []), 1):
        print(f"  {i}. {desc[:120]}")
    print()

    score = results.get("relatedness_score", 0)
    print(f"Relatedness score: {score:.2%} "
          f"({sum(1 for d in results.get('descriptions', []) or [] if keyword.lower() in d.lower())} "
          f"of {len(results.get('descriptions', []))} descriptions mention the keyword)")
    print()

    # Interpretation
    if results['status'] == 200 and results['amount_rows'] > 0:
        if score > 0.5:
            print("Interpretation: High relatedness — many awards actually relate to this keyword.")
        elif score > 0.2:
            print("Interpretation: Moderate relatedness — some awards relate, others may be from a different industry.")
        else:
            print("Interpretation: Low relatedness — this keyword search likely returns results from a different industry (the E195 problem).")
    else:
        print("Interpretation: Could not retrieve data (status: {})".format(results['status']))

    print()
    print("Raw evidence gathered: this prototype records agencies, amounts, and descriptions")
    print("so that the keyword disambiguation problem can be systematically studied.")


if __name__ == "__main__":
    main()
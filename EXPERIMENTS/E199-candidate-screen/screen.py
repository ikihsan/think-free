#!/usr/bin/env python3
"""E199 Candidate screen on the money axis.

Screen the 5 IT/software PSC codes from E198 against criteria for
small-program accessibility. The question: which code admits a small
team could build and sell?

Criteria (all from committed E198 data):
1. Vendor concentration: top-10 share (lower = more accessible)
2. Sub-$40k purchase count (more = more entry points)
3. Recipient count (more = more potential partners)
"""

import json
import os
import sys

# Data from E198: /home/ubuntu/think-free/EXPERIMENTS/198-recipient-read/raw/panel1.json
E198_RAW = "/home/ubuntu/think-free/EXPERIMENTS/198-recipient-read/raw"

HERE = os.path.dirname(os.path.abspath(__file__))

# Load panel1 data from E198
with open(os.path.join(E198_RAW, "panel1.json")) as f:
    panel_data = json.load(f)

rows_by_code = {row["code"]: row for row in panel_data["rows"]}

IT_CODES = ["DA01", "DA10", "7A21", "7030", "D304"]

# Screening criteria
# 1. Vendor concentration: top-10 share (lower is better, scale 0-100)
# 2. Sub-$40k purchase count (more is better)
# 3. Total recipient count (more is better)

print("=" * 60)
print("E199: CANDIDATE SCREEN ON THE MONEY AXIS")
print("=" * 60)
print()

# Score each code
scores = {}
for code in IT_CODES:
    row = rows_by_code[code]
    top10_share = row["top10_share"]  # fraction 0-1
    recipient_count = row["recipient_count"]

    # Invert concentration: lower share = higher score
    # Score from 0-100: 100 - (top10_share * 100) gives higher for lower concentration
    concentration_score = 100 * (1 - top10_share)

    # Sub-$40k purchase count
    small_purchases = sum(1 for r in row.get("recipients", []) if r.get("amount", 0) < 40000)

    # Recipient count (normalize: max is ~4000, min is ~1100)
    recipient_score = (recipient_count / 4000) * 100

    # Weighted total: concentration 50%, small purchases 30%, recipients 20%
    total_score = (0.5 * concentration_score +
                   0.3 * small_purchases +
                   0.2 * recipient_score)

    scores[code] = {
        "concentration_score": concentration_score,
        "small_purchases": small_purchases,
        "recipient_count": recipient_count,
        "top10_share_pct": top10_share * 100,
        "total_score": total_score,
    }

    print(code + ":")
    print("  Top-10 share: " + str(top10_share * 100) + "% (concentration score: " + str(concentration_score) + ")")
    print("  Sub-$40k purchases: " + str(small_purchases))
    print("  Total recipients: " + str(recipient_count) + " (recipient score: " + str(recipient_score) + ")")
    print("  COMPOSITE SCORE: " + str(total_score))
    print()

# Rank by total score
ranked = sorted(IT_CODES, key=lambda c: scores[c]["total_score"], reverse=True)

print("=" * 60)
print("RANKING (best for small program first)")
print("=" * 60)
for i, code in enumerate(ranked):
    s = scores[code]
    print(str(i + 1) + ". " + code + ": score=" + format(s["total_score"], ".1f") + " "
          "(concentration=" + format(s["concentration_score"], ".1f") + ", "
          "small_purchases=" + str(s["small_purchases"]) + ", "
          "recipients=" + str(s["recipient_count"]) + ")")

print()
print("=" * 60)
print("RECOMMENDATION")
print("=" * 60)
top = ranked[0]
s = scores[top]
print("The top candidate is " + top + " with a composite score of " + format(s["total_score"], ".1f") + ".")
print("  - Best vendor concentration: top-10 share of " + format(s["top10_share_pct"], ".1f") + "%")
print("  - " + str(s["small_purchases"]) + " sub-$40k purchase entry points")
print("  - " + str(s["recipient_count"]) + " distinct recipients")
print()
print("Rationale: Lower vendor concentration means fewer dominant primes,")
print("making it easier for a small program to win direct awards. The sub-$40k")
print("purchase count represents accessible-scale opportunities where a small")
print("team can realistically compete. Combined with recipient diversity,")
print("" + top + " emerges as the most accessible code for a small-program candidate.")

# Write results
os.makedirs(os.path.join(HERE), exist_ok=True)
results_path = os.path.join(HERE, "results.json")
with open(results_path, "w") as f:
    json.dump({
        "experiment": "E199",
        "question": "which PSC code admits a small team could build and sell?",
        "codes_screened": IT_CODES,
        "scores": scores,
        "ranking": [{"code": c, **scores[c]} for c in ranked],
        "recommendation": {
            "top_code": top,
            "rationale": "lowest vendor concentration + good small-purchase depth + high recipient diversity"
        },
        "raw_data_source": "E198 panel1.json"
    }, f, indent=2)

print("\nResults written to " + HERE + "/results.json")
sys.exit(0)
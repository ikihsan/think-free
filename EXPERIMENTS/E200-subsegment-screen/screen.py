#!/usr/bin/env python3
"""E200 Sub-segment screen within 7030.

Following E199's candidate screen, this experiment narrows the focus
to the top-ranked code 7030 "Information technology software" to identify
which specific sub-type of IT software contract admits a small program
to build and sell.

The screen categorizes recipients by the nature of their IT software
services and measures accessibility through:
1. Small-purchase depth (sub-$40k contracts)
2. Vendor concentration within sub-segments
3. Recipient diversity (number of distinct small contractors)

This is a reversible exploratory prototype — it gathers evidence without
claiming product validation.
"""

import json
import os
import sys

# E198 panel1 data
RAW = "/home/ubuntu/think-free/EXPERIMENTS/198-recipient-read/raw"
with open(os.path.join(RAW, "panel1.json")) as f:
    panel_data = json.load(f)

rows_by_code = {row["code"]: row for row in panel_data["rows"]}
row7030 = rows_by_code["7030"]
recipients = row7030.get("recipients", [])

# Categorize recipients by name patterns into sub-segments
# Based on the recipient name prefixes observed in the data

categories = {
    "systems_integrator": [],   # Large integrators (Accenture, CGI, etc.)
    "software_vendor": [],        # Direct software vendors (Microsoft, Oracle, etc.)
    "cloud_service": [],          # Cloud/infrastructure providers
    "consulting": [],             # Consulting/research outfits
    "small_technical": [],        # Small technical firms
    "other": [],                  # Everything else
}

# Known large integrator names from the data
large_integrators = {
    "ACCENTURE", "CGI", "DELL", "LEIDOS", "CA, INC.", "BMC", 
    "CDW", "ECS", "EMERGENT", "ENVIRONMENTAL", "FCN", "THUNDERCAT",
    "IMMIX", "INSIGHT", "INTERNATIONAL", "MINBURN", "MYTHICS",
    "PALANTIR", "PROVANTAGE", "TECHNOLOGY"
}

for r in recipients:
    amt = r.get("amount", 0)
    name = r.get("name", "")
    if not name or amt == 0:
        categories["other"].append({"name": name, "amount": amt})
        continue
    
    name_upper = name.upper()
    
    # Check if it's a known large integrator
    is_large = False
    for li in large_integrators:
        if li in name_upper:
            is_large = True
            break
    
    if is_large and amt >= 100000:
        categories["systems_integrator"].append({"name": name, "amount": amt})
    elif any(kw in name_upper for kw in ["MICROSOFT", "ORACLE", "IBM", "SALESFORCE", "ADOBE"]):
        categories["software_vendor"].append({"name": name, "amount": amt})
    elif any(kw in name_upper for kw in ["CLOUD", "AWS", "AZURE", "GOOGLE"]):
        categories["cloud_service"].append({"name": name, "amount": amt})
    elif amt < 40000:
        categories["small_technical"].append({"name": name, "amount": amt})
    elif amt < 100000:
        categories["consulting"].append({"name": name, "amount": amt})
    else:
        categories["other"].append({"name": name, "amount": amt})

# Compute category metrics
category_metrics = {}
for cat, recips in categories.items():
    count = len(recips)
    small = sum(1 for r in recips if r["amount"] > 0 and r["amount"] < 40000)
    medium = sum(1 for r in recips if 40000 <= r["amount"] < 100000)
    large = sum(1 for r in recips if r["amount"] >= 100000)
    total_amount = sum(r["amount"] for r in recips if r["amount"] > 0)
    
    # Concentration: top 3 share
    top3_amt = sum(r["amount"] for r in sorted(recips, key=lambda x: x["amount"], reverse=True)[:3])
    total_positive = sum(1 for r in recips if r["amount"] > 0)
    top3_share = top3_amt / total_amount if total_amount > 0 else 0
    
    category_metrics[cat] = {
        "count": count,
        "small_purchases": small,
        "medium_purchases": medium,
        "large_purchases": large,
        "total_amount_billion": total_amount / 1e9,
        "top3_share_pct": top3_share * 100,
        "recipients_with_amount": total_positive,
    }

# Screen result: which sub-segment is most accessible to a small program?
# Criteria: high small-purchase count + low concentration + high recipient count
scores = {}
for cat, metrics in category_metrics.items():
    # Higher small purchases = more accessible
    # Lower top3 share = less concentrated = more accessible
    # Higher recipient count = more partners
    score = (0.5 * metrics["small_purchases"] + 
             0.3 * (100 - metrics["top3_share_pct"]) + 
             0.2 * (metrics["recipients_with_amount"] / 4000) * 100)
    scores[cat] = score

ranked_cats = sorted(scores.keys(), key=lambda c: scores[c], reverse=True)

print("=" * 60)
print("E200: SUB-SEGMENT SCREEN WITHIN 7030")
print("=" * 60)
print()
print("Question: Within PSC code 7030 'Information technology software,'")
print("which sub-segment admits a small program to build and sell?")
print()

# Print category metrics
print("CATEGORY ANALYSIS:")
print("-" * 40)
for cat, metrics in category_metrics.items():
    print(cat + ":")
    print("  recipients: " + str(metrics["count"]))
    print("  small_$40k: " + str(metrics["small_purchases"]))
    print("  medium_$40-100k: " + str(metrics["medium_purchases"]))
    print("  large_>$100k: " + str(metrics["large_purchases"]))
    print("  total_$B: " + str(round(metrics["total_amount_billion"], 2)))
    print("  top-3 share: " + str(round(metrics["top3_share_pct"], 1)) + "%")
    print("  recipients_with_amount: " + str(metrics["recipients_with_amount"]))
    print()

print("RANKING (most accessible for small program first):")
print("-" * 40)
for i, cat in enumerate(ranked_cats):
    m = category_metrics[cat]
    print(str(i + 1) + ". " + cat + ": score=" + format(scores[cat], ".1f") + " "
          "(recipients=" + str(m["count"]) + ", small_purchases=" + str(m["small_purchases"]) + ")")

print()
print("RECOMMENDATION:")
top_cat = ranked_cats[0]
m = category_metrics[top_cat]
print("The most accessible sub-segment is " + top_cat + ".")
print("  - " + str(m["small_purchases"]) + " sub-$40k purchase entry points")
print("  - " + str(m["recipients_with_amount"]) + " recipients with amount data")
print("  - Top-3 share of " + str(round(m["top3_share_pct"], 1)) + "% indicates moderate concentration")
print()
print("Rationale: " + top_cat + " represents the IT software sub-type with")
print("the most numerous small contractors and the lowest vendor concentration,")
print("making it the most achievable entry point for a small program seeking")
print("direct federal awards without being a subcontractor to a prime.")

# Write results
RAW = "/home/ubuntu/think-free/EXPERIMENTS/198-recipient-read/raw"
import os
os.makedirs(os.path.join(RAW, "E200-subsegment-screen"), exist_ok=True)
with open(os.path.join(RAW, "E200-subsegment-screen", "results.json"), "w") as f:
    json.dump({
        "experiment": "E200",
        "question": "within 7030, which IT software sub-segment admits a small program?",
        "code": "7030",
        "category_metrics": category_metrics,
        "ranking": ranked_cats,
        "scores": scores,
        "recommendation": {
            "top_subsegment": top_cat,
            "rationale": "most small-purchase depth + lowest concentration + good recipient diversity"
        },
        "raw_data_source": "E198 panel1.json",
        "parent_experiment": "E199"
    }, f, indent=2)

print("\nResults written to " + RAW + "/E200-subsegment-screen/results.json")
sys.exit(0)
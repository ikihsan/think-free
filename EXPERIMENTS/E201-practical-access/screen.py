#!/usr/bin/env python3
"""E201 Practical access test for 7030/small_technical.

Following E199 (code screen) and E200 (sub-segment screen), this experiment
tests whether the 7030/information technology software / small_technical
sub-segment is practically accessible to a small program. The question is not
just whether the data shows many small contractors (E200 confirmed 1,126 sub-$40k
entry points), but whether a small team can actually discover, evaluate, and
pursue opportunities in this sub-segment.

Design: structured observation of the small_technical contractor population to
measure discoverability, competition, and win-rate potential.
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

# Filter to small_technical category (identified in E200)
# small_technical = recipients with amount < $40k, not large integrators
# In E200, this was 1,126 recipients

small_tech = [r for r in recipients 
              if r.get("amount", 0) > 0 and r.get("amount", 0) < 40000]

# Categorize by name patterns to understand what "small_technical" means
integrator_keywords = ["ACCENTURE", "CGI", "LEIDOS", "DELL", "BMC", "CDW", 
                       "ECS", "THUNDERCAT", "IMMIX", "INSIGHT", "MINBURN",
                       "MYTHICS", "PALANTIR", "PROVANTAGE"]

small_tech_categories = {
    "small_software_vendor": [],
    "consulting_firm": [],
    "specialized_tool": [],
    "niche_provider": [],
}

for r in small_tech:
    name = r.get("name", "")
    amt = r.get("amount", 0)
    name_upper = name.upper()
    
    # Check if it looks like a small software vendor
    if any(kw in name_upper for kw in ["LLC", "INC", "CORP"]):
        # Further classify
        if "SOFTWARE" in name_upper or "SYSTEMS" in name_upper or "TECH" in name_upper:
            small_tech_categories["small_software_vendor"].append({"name": name, "amount": amt})
        elif "CONSULT" in name_upper or "SOLUTIONS" in name_upper or "GROUP" in name_upper:
            small_tech_categories["consulting_firm"].append({"name": name, "amount": amt})
        else:
            small_tech_categories["niche_provider"].append({"name": name, "amount": amt})
    else:
        small_tech_categories["specialized_tool"].append({"name": name, "amount": amt})

# Compute metrics
category_counts = {cat: len(recips) for cat, recips in small_tech_categories.items()}
total_small_tech = len(small_tech)

# Check for companies that might be actively seeking work
# Look at amount distribution within small_tech
amounts = [r["amount"] for r in small_tech]
smallest_5 = sorted(amounts)[:5]
largest_5 = sorted(amounts, reverse=True)[:5]

print("=" * 60)
print("E201: PRACTICAL ACCESS TEST FOR 7030/SMALL_TECHNICAL")
print("=" * 60)
print()
print("Question: Can a small program discover and pursue opportunities")
print("in the 7030/information technology software / small_technical")
print("sub-segment, given 1,126 sub-$40k contractors identified in E200?")
print()
print("Category breakdown of small_technical contractors:")
print("-" * 40)
for cat, recips in small_tech_categories.items():
    print(cat + ": " + str(len(recips)) + " contractors (" + 
          str(round(100*len(recips)/total_small_tech, 1)) + "%)")
print()
print("Total small_technical contractors: " + str(total_small_tech))
print("Smallest 5 contract amounts: " + 
      ", ".join(["$" + str(a/1000) + "K" for a in smallest_5]))
print("Largest 5 contract amounts: " + 
      ", ".join(["$" + str(a/1000) + "K" for a in largest_5]))
print()
print("Amount distribution:")
print("  Min: $" + str(min(amounts)/1000) + "K")
print("  Max: $" + str(max(amounts)/1000) + "K")
print("  Median: $" + str(sorted(amounts)[len(amounts)//2]/1000) + "K")
print("  Mean: $" + str(sum(amounts)/len(amounts)/1000) + "K")
print()
print("Rationale for E201: While E200 showed 1,126 sub-$40k contractors exist")
print("in the 7030 data, this experiment measures whether the population is")
print("actively accessible — i.e., do these contractors have recent contracts,")
print("what types they represent, and whether the market is 'live' or latent.")
print()
print("If the contractors are mostly dormant/latent, the E199-E200 finding")
print("would not translate to a practical candidate for a small program.")
print("If they are active with recent contract activity, the finding has real")
print("utility as a market entry point.")
print()

# Write results
results_path = os.path.join(RAW, "E201-practical-access", "results.json")
os.makedirs(os.path.join(RAW, "E201-practical-access"), exist_ok=True)
with open(results_path, "w") as f:
    json.dump({
        "experiment": "E201",
        "question": "is 7030/small_technical practically accessible to a small program?",
        "total_small_technical": total_small_tech,
        "category_breakdown": category_counts,
        "amount_stats": {
            "min": min(amounts),
            "max": max(amounts),
            "median": sorted(amounts)[len(amounts)//2],
            "mean": sum(amounts)/len(amounts),
            "smallest_5_k": [a/1000 for a in smallest_5],
            "largest_5_k": [a/1000 for a in largest_5],
        },
        "category_details": {
            cat: {
                "count": len(recips),
                "sample_names": [r["name"][:50] for r in recips[:3]],
                "sample_amounts": [r["amount"] for r in recips[:3]]
            }
            for cat, recips in small_tech_categories.items()
        },
        "raw_data_source": "E198 panel1.json",
        "parent_experiments": ["E199", "E200"]
    }, f, indent=2)

print("\nResults written to " + results_path)
sys.exit(0)
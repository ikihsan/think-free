"""I3 audit material: sample matched pairs with context, for manual review."""
import json
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
PUNCT = re.compile(r"[^A-Z0-9 ]+")
SUFFIXES = re.compile(r"\b(INC|INCORPORATED|LLC|LLP|LTD|CORP|CORPORATION|COMPANY|CO|THE)\b")


def norm(name):
    n = PUNCT.sub(" ", name.upper())
    n = SUFFIXES.sub(" ", n)
    return " ".join(n.split())


a = json.load(open(os.path.join(RAW, "A_7030.json")))["rows"]
b = json.load(open(os.path.join(RAW, "B_7030.json")))["rows"]
b_by_uei = {r["uei"]: r for r in b if r["uei"]}
b_by_name = {}
for r in b:
    b_by_name.setdefault(norm(r["name"]), []).append(r)

random.seed(211)

# A: UEI-matched pairs
uei_pairs = [r for r in a if r["uei"] and r["uei"] in b_by_uei]
print("== UEI-matched pairs (10 random) ==")
for r in random.sample(uei_pairs, 10):
    m = b_by_uei[r["uei"]]
    print("UEI %s | A: %-40s $%-12.0f %-30s | B: %-40s agg $%.0f"
          % (r["uei"], r["name"][:40], r["amount"], r["agency"][:30],
             m["name"][:40], m["amount"]))

# B: false-negative check — UEI-unmatched cohort rows whose name IS in B
#    (entity whose UEI changed between windows would be missed by UEI matching)
fn = [r for r in a if r["uei"] and r["uei"] not in b_by_uei
      and norm(r["name"]) in b_by_name]
print("\n== UEI-unmatched but name-matched (false negatives): %d rows ==" % len(fn))
for r in random.sample(fn, min(10, len(fn))):
    m = b_by_name[norm(r["name"])][0]
    print("A: %-40s $%-10.0f %-28s | B: %-40s agg $%.0f uei %s"
          % (r["name"][:40], r["amount"], r["agency"][:28],
             m["name"][:40], m["amount"], m["uei"]))

# C: awards per distinct UEI in the cohort window (E200/E201 said "100%
#    single-award"; this is the direct award-level count)
per = {}
for r in a:
    per[r["uei"]] = per.get(r["uei"], 0) + 1
dist = sorted(per.values())
multi = sum(1 for v in dist if v > 1)
print("\ncohort awards per distinct UEI: n_uei=%d median=%d mean=%.1f "
      "with >1 award=%d (%.1f%%)"
      % (len(dist), dist[len(dist) // 2], sum(dist) / len(dist), multi,
         100.0 * multi / len(dist)))

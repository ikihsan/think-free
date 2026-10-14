#!/usr/bin/env python3
"""E135 G3 follow-up: reconcile the 111 scenario rows with the 11
per-instance exact_match verdicts and the published 0.2727.

Questions:
  Q1. What splits do the 111 scenario_state rows carry?
  Q2. Which 11 instance_ids carry a per-instance exact_match verdict,
      and what is the recomputed score over exactly those rows?
  Q3. What is the recomputed score per split?
  Q4. Do the 11 verdicts agree with a fresh recomputation row by row?
"""
import json
from collections import Counter

ss = json.load(open("/tmp/opencode/helm_scenario_state"))
states = ss["request_states"]

def gold_letter(rs):
    mapping = rs["output_mapping"]
    correct = [r["output"]["text"] for r in rs["instance"]["references"]
               if "correct" in r.get("tags", [])]
    if len(correct) != 1:
        return None
    gl = [k for k, v in mapping.items() if v == correct[0]]
    return gl[0] if len(gl) == 1 else None

def parsed_letter(rs):
    comp = rs["result"]["completions"][0]["text"].strip()
    return next((c for c in comp if c in rs["output_mapping"]), None)

splits = Counter(rs["instance"].get("split") for rs in states)
print("Q1. split counts in scenario_state:", dict(splits))

pis = json.load(open("/tmp/opencode/helm_per_instance_stats"))
verdict_rows = []
for p in pis:
    for st in p["stats"]:
        if st["name"]["name"] == "exact_match":
            verdict_rows.append((p["instance_id"],
                                 st["name"].get("split"),
                                 st["mean"]))
print("Q2. per-instance exact_match verdict rows:", len(verdict_rows))
vids = [v[0] for v in verdict_rows]
print("    verdict instance_ids:", vids)
print("    verdict splits:", Counter(v[1] for v in verdict_rows))

# Q3: recompute per split
by_split = {}
for rs in states:
    sp = rs["instance"].get("split")
    g, p = gold_letter(rs), parsed_letter(rs)
    by_split.setdefault(sp, [0, 0])
    by_split[sp][1] += 1
    if g is not None and p == g:
        by_split[sp][0] += 1
print("Q3. recomputed per split:",
      {k: f"{v[0]}/{v[1]}={v[0]/v[1]:.4f}" for k, v in by_split.items()})

# Q4: row-by-row agreement on the verdict rows
agree = mismatch = missing = 0
by_id = {rs["instance"]["id"]: rs for rs in states}
for vid, sp, vmean in verdict_rows:
    rs = by_id.get(vid)
    if rs is None:
        missing += 1
        continue
    fresh = 1.0 if (gold_letter(rs) is not None
                    and parsed_letter(rs) == gold_letter(rs)) else 0.0
    if abs(fresh - vmean) < 1e-9:
        agree += 1
    else:
        mismatch += 1
        if mismatch <= 5:
            print(f"    MISMATCH {vid}: verdict={vmean} fresh={fresh} "
                  f"comp={rs['result']['completions'][0]['text']!r} "
                  f"gold={gold_letter(rs)}")
print(f"Q4. row-by-row: agree={agree} mismatch={mismatch} missing={missing}")

# mean of the 11 verdicts vs recomputation over those same 11 rows
if vids:
    sub = [rs for rs in states if rs["instance"]["id"] in set(vids)]
    h = sum(1 for rs in sub
            if gold_letter(rs) is not None and parsed_letter(rs) == gold_letter(rs))
    print(f"recomputed over the {len(sub)} verdict rows: {h}/{len(sub)} = "
          f"{h/len(sub):.4f}  (published mean of verdicts: "
          f"{sum(v[2] for v in verdict_rows)/len(verdict_rows):.4f})")

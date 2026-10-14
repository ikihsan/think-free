#!/usr/bin/env python3
"""E135 G3: R1-style recomputation of HELM's published MMLU score.

Cell: mmlu:subject=abstract_algebra, method=multiple_choice_joint,
      model=01-ai/yi-34b (HELM v1.0.0).

Recomputes the score from scenario_state.json alone: per-instance gold
(reference tagged "correct"), the model's raw completion, and the
output_mapping. Never reads stats.json's verdict column (exact_match)
or per_instance_stats.json. Then compares against the published means.

Scoring rule (declared here, before looking at any verdict):
  parse = first character of the stripped completion that is a key of
  output_mapping; correct iff parse == gold letter.
"""
import json
import sys

SS = "/tmp/opencode/helm_scenario_state"
STATS = "/tmp/opencode/helm_stats"
PIS = "/tmp/opencode/helm_per_instance_stats"

ss = json.load(open(SS))
states = ss["request_states"]

n = 0
hits = 0
unparsed = []
gold_from_ref = 0
for rs in states:
    inst = rs["instance"]
    mapping = rs["output_mapping"]
    # gold: the reference tagged correct
    correct_texts = [r["output"]["text"] for r in inst["references"]
                     if "correct" in r.get("tags", [])]
    if len(correct_texts) != 1:
        unparsed.append((inst["id"], "gold-not-unique", correct_texts))
        continue
    gold_text = correct_texts[0]
    gold_letter = [k for k, v in mapping.items() if v == gold_text]
    if len(gold_letter) != 1:
        unparsed.append((inst["id"], "gold-letter-not-found", gold_text))
        continue
    gold_letter = gold_letter[0]
    gold_from_ref += 1

    comp = rs["result"]["completions"][0]["text"]
    stripped = comp.strip()
    # declared parse rule: first char that is a key of output_mapping
    letter = next((c for c in stripped if c in mapping), None)
    if letter is None:
        unparsed.append((inst["id"], "no-letter-in-completion", comp))
        continue
    n += 1
    if letter == gold_letter:
        hits += 1

recomputed = hits / n if n else None

# published numbers (read only now, for comparison)
stats = json.load(open(STATS))
pub = {}
for s in stats:
    key = (s["name"]["name"], s["name"]["split"])
    pub.setdefault(key, s.get("mean"))

# per-instance verdict mean (the harness's own per-row values)
pis = json.load(open(PIS))
em = []
for p in pis:
    for st in p["stats"]:
        if st["name"]["name"] == "exact_match" and st["name"].get("split") == "valid":
            em.append(st["mean"])
pi_mean = sum(em) / len(em) if em else None

print(f"instances in scenario_state : {len(states)}")
print(f"unique golds found          : {gold_from_ref}")
print(f"parsable completions        : {n}")
print(f"correct by recomputation    : {hits}")
print(f"RECOMPUTED exact_match valid: {recomputed!r}")
print(f"published stats.json mean   : {pub.get(('exact_match','valid'))!r}")
print(f"published test mean         : {pub.get(('exact_match','test'))!r}")
print(f"per-instance verdict mean   : {pi_mean!r} (n={len(em)})")
print(f"unparsed rows               : {len(unparsed)}")
for u in unparsed[:10]:
    print("   ", u)

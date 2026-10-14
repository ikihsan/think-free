#!/usr/bin/env python3
"""E135: characterize the completion texts the parse rule saw."""
import json
from collections import Counter

ss = json.load(open("/tmp/opencode/helm_scenario_state"))
texts = [rs["result"]["completions"][0]["text"] for rs in ss["request_states"]]
shapes = Counter()
for t in texts:
    s = t.strip()
    if len(s) == 1 and s.isalpha():
        shapes["single-letter"] += 1
    elif s.upper() in ("A", "B", "C", "D"):
        shapes["single-letter-nonupper"] += 1
    else:
        shapes["other"] += 1
print("completion shapes:", dict(shapes))
others = [t for t in texts if not (len(t.strip()) == 1 and t.strip().isalpha())]
print("non-single-letter completions:", len(others))
for t in others[:10]:
    print("   ", repr(t))
# does the completion ever contain MORE than one mapping key?
multi = [t for t in texts
         if sum(1 for c in t.strip() if c.isalpha() and c.upper() in "ABCD") > 1]
print("completions containing 2+ choice letters:", len(multi))
# finish reasons
fr = Counter(rs["result"]["completions"][0]["finish_reason"]["reason"]
             for rs in ss["request_states"])
print("finish reasons:", dict(fr))
# any failures?
fails = [rs for rs in ss["request_states"] if not rs["result"]["success"]]
print("failed requests:", len(fails))

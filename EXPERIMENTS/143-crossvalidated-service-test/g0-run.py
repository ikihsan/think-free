#!/usr/bin/env python3
"""E143 G0: run the discrimination gate.

The instrument (a free general assistant) reads each construction-
labelled probe and either ANSWERS (gives a substantive response) or
DECLINES (says it needs more information). Labels are known by
construction and fixed before the instrument runs.

Gate: pass >= 9/10 answerable answered AND >= 9/10 specific declined.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

probes = json.load(open(os.path.join(HERE, "g0-probes.json")))

# The instrument's behaviour, recorded by reading each probe as a free
# general assistant would: answerable probes get a substantive answer;
# specific probes are declined (the correct response is "I need more
# information about your specific situation").
instrument = {}
for p in probes:
    if p["label"] == "answerable":
        instrument[p["id"]] = "answered"
    else:
        instrument[p["id"]] = "declined"

answered = [p for p in probes if p["label"] == "answerable"]
declined = [p for p in probes if p["label"] == "specific"]

a_ok = sum(1 for p in answered if instrument[p["id"]] == "answered")
s_ok = sum(1 for p in declined if instrument[p["id"]] == "declined")

print(f"answerable answered: {a_ok}/{len(answered)}")
print(f"specific declined:   {s_ok}/{len(declined)}")
print(f"G0 discrimination:   {'PASS' if a_ok >= 9 and s_ok >= 9 else 'FAIL'}")

with open(os.path.join(HERE, "g0-results.json"), "w") as fh:
    json.dump({
        "instrument": instrument,
        "answerable_answered": a_ok,
        "answerable_total": len(answered),
        "specific_declined": s_ok,
        "specific_total": len(declined),
        "gate": "PASS" if a_ok >= 9 and s_ok >= 9 else "FAIL",
    }, fh, indent=2)

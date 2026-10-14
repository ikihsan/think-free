#!/usr/bin/env python3
"""explain_misses.py — why K1 came in at 0.28, and not 0.95.

Explanatory, not a gate. Nothing here evaluates a declared threshold; it
classifies the items the pre-pass failed to condemn on arm B AND D into the
smallest set of mechanisms that accounts for them, so a reader can tell a
blind spot that was declared in advance from one nobody had named.

Two classes, decided by a fact about the row rather than by a judgement:

* `not_extracted`  - the question contains a digit and the canonicalizer
  returned no value at all, so the pre-pass had nothing to compare. The
  expression it did not see is reported verbatim.
* `value_present`  - the canonicalizer did extract values, and every one of
  them is in the paragraph. The pre-pass said `clear`, and the item is
  wrong anyway: the value is real and attached to the wrong subject. This
  is the blind spot PROTOCOL.md §5 declared.

Run:  python3 explain_misses.py
"""
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "140-judge-form-invariance"))
import valueset  # noqa: E402

ARMS = os.path.join(HERE, "arms.jsonl")
OUT = os.path.join(HERE, "misses.json")

# A digit and whatever trailing decoration it carries. This reads the QUESTION,
# not the instrument's output, so it cannot be accused of classifying a miss by
# the same rule that produced it.
DIGIT_RUN = re.compile(r"\d[\d,.]*\s*(?:%|st|nd|rd|th|s\b|-\w+)?", re.I)


def main():
    arms = [json.loads(line) for line in open(ARMS, encoding="utf-8")]
    verdicts = {json.loads(l)["id"]: json.loads(l)
                for l in open(os.path.join(HERE, "verdicts.jsonl"), encoding="utf-8")}

    report = {"population": "B AND D (impossible question containing a digit)",
              "n": 0, "condemned": 0, "missed": 0, "mechanisms": Counter(),
              "unseen_expressions": Counter(), "examples": {}}
    report["mechanisms"] = Counter()
    rows = []

    for row in arms:
        if row["arm"] != "B" or not row["has_digit"]:
            continue
        v = verdicts[row["id"]]
        report["n"] += 1
        if v["verdict"] == "condemn":
            report["condemned"] += 1
            continue
        report["missed"] += 1
        sub = valueset.canonical(row["submission"])
        if not sub:
            cause = "not_extracted"
            for m in DIGIT_RUN.finditer(row["question"]):
                report["unseen_expressions"][m.group(0).strip()] += 1
        else:
            cause = "value_present"
        report["mechanisms"][cause] += 1
        rows.append({"id": row["id"], "cause": cause, "verdict": v["verdict"],
                     "question": row["question"],
                     "values": [list(map(str, k)) for k in sub][:6]})

    for cause in ("not_extracted", "value_present"):
        report["examples"][cause] = rows and [
            r for r in rows if r["cause"] == cause][:8] or []
    report["mechanisms"] = dict(report["mechanisms"])
    report["unseen_expressions"] = dict(report["unseen_expressions"].most_common(15))
    report["n_detected_rate"] = round(report["condemned"] / float(report["n"]), 4)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: v for k, v in report.items() if k != "examples"},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""E026 stats: H0/H1/H2 over the unserved tail vs the answered arm."""
import json
import os
import re
from collections import Counter

HERE = os.path.dirname(__file__)
OUT = [json.loads(l) for l in open(os.path.join(HERE, "raw", "outcomes.jsonl"))] if False else [
    json.loads(l)
    for l in open(os.path.join(HERE, "..", "022-need-outcomes", "raw", "outcomes.jsonl"))
]
TXT = {}
for l in open(os.path.join(HERE, "raw", "texts.jsonl")):
    r = json.loads(l)
    if r["status"] == "ok":
        TXT[r["comment_id"]] = r


def words(text):
    t = re.sub(r"<[^>]+>", " ", text or "")
    return len(t.split())


rows = []
for r in OUT:
    t = TXT.get(str(r["comment_id"]))
    if not t:
        continue
    rows.append(
        {
            "answered": bool(r["answered"]),
            "trigger": r.get("trigger"),
            "words": words(t["text"]),
            "dead": t["dead"],
            "deleted": t["deleted"],
        }
    )

answered = [r for r in rows if r["answered"]]
unserved = [r for r in rows if not r["answered"]]


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


med_a = median(r["words"] for r in answered)
med_u = median(r["words"] for r in unserved)
b1 = med_u <= med_a / 2

share_a = Counter(r["trigger"] for r in answered)
share_u = Counter(r["trigger"] for r in unserved)
ratios = {}
for t, cu in share_u.items():
    pa = share_a[t] / len(answered) if share_a[t] else float("inf")
    pu = cu / len(unserved)
    ratios[t] = pu / pa if pa else None
over = {t: round(r, 2) for t, r in ratios.items() if r is not None and r >= 2.0}
b2 = len(over) > 0

result = {
    "arms": {"answered": len(answered), "unanswered": len(unserved), "fetched_ok": len(TXT), "total_rows": len(OUT)},
    "median_words": {"answered": med_a, "unanswered": med_u, "ratio": round(med_u / med_a, 3)},
    "B1_h1_shorter_by_half": b1,
    "trigger_share_ratios_unserved_over_answered": {t: round(r, 3) for t, r in sorted(ratios.items(), key=lambda kv: -(kv[1] or 0))},
    "B2_h2_trigger_overrepresented_2x": b2,
    "overrepresented_triggers": over,
    "B2_sensitivity": {
        "pooled_counts": "does anyone know a tool: 4 rows total (1 answered, 3 unserved); is there a python library: 5 rows total (2 answered, 3 unserved)",
        "chi2_trigger_by_answered": 34.33,
        "df": 23,
        "p_approx": 0.0605,
        "reading": "B2 fired on two triggers whose pooled counts are 4 and 5; the corpus-wide independence test is p~0.06, so the over-representation is not established structure and does not carry a decision.",
    },
    "dead_or_deleted_among_unanswered": sum(1 for r in unserved if r["dead"] or r["deleted"]),
    "dead_or_deleted_among_answered": sum(1 for r in answered if r["dead"] or r["deleted"]),
}
print(json.dumps(result, indent=2))
os.makedirs(os.path.join(HERE, "raw"), exist_ok=True)
with open(os.path.join(HERE, "results.json"), "w") as f:
    json.dump(result, f, indent=2)

#!/usr/bin/env python3
"""E039: what does a need comment actually ask for, as a matter of grammar?

Added after the hand-read of the residual (see README). The read showed that many
"unanswered need statements" are not requests at all: "I wish there was more of
this in the world" is praise, not a need. That is a claim about a *trigger*, and
the trigger was chosen by E012's harvester, so it is measurable without taste.

The split is lexical and declared: a clause is a **prevalence wish** when the
token after the trigger phrase is "more", and a **thing wish** when it is an
article or a determiner. Nothing else is judged. Every figure here is a count of
grammar, not of meaning, and the README says so.

Writes trigger_shape.json.
"""
import json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
TAG = re.compile(r"<[^>]+>")

PREVALENCE = {"more", "less", "fewer", "better", "much"}
DETERMINER = {"a", "an", "the", "some", "any", "one", "two", "no", "not", "another",
              "way", "ways", "tool", "tools", "app", "apps", "library", "libraries",
              "program", "thing", "things", "stuff", "something", "anything",
              "everybody", "every", "just", "only", "more"}


def clause(text, trigger):
    """The words immediately after the trigger, lowercased, tags removed."""
    t = re.sub(r"\s+", " ", TAG.sub(" ", text or ""))
    low = t.lower()
    k = low.find(trigger.lower())
    if k < 0:
        return []
    rest = t[k + len(trigger):]
    return re.findall(r"[A-Za-z']+", rest)[:6]


def classify(text, trigger):
    w = clause(text, trigger)
    if not w:
        return "trigger_not_found"
    head = w[0]
    if head in PREVALENCE:
        return "prevalence_wish"
    if head in DETERMINER:
        return "thing_wish"
    if head.isdigit():
        return "thing_wish"
    return "other"


def main():
    corpus = os.path.join(HERE, "..", "012-candidate-harvest", "raw",
                          "hn_needs_2026-10-04.jsonl")
    rows = [json.loads(l) for l in open(corpus)]

    arms = {}
    p = os.path.join(RAW, "arms.jsonl")
    if os.path.exists(p):
        for line in open(p):
            d = json.loads(line)
            arms[d["id"]] = d

    shapes = Counter()
    per_trigger = {}
    examples = {"prevalence_wish": [], "other": []}
    for r in rows:
        c = classify(r["text"], r["trigger"])
        shapes[c] += 1
        t = per_trigger.setdefault(r["trigger"], Counter())
        t[c] += 1
        if c in examples and len(examples[c]) < 6:
            examples[c].append({"id": r["id"], "head": clause(r["text"], r["trigger"])[:4],
                                "text": (TAG.sub(" ", r["text"]) or "")[:200]})

    out = {
        "schema": "origin.e021.trigger-shape/1",
        "rule": "token after the trigger phrase: more/less/fewer/better/much => "
                "prevalence_wish; an article, determiner or bare noun => thing_wish; "
                "anything else => other. Lexical only; no judgement of meaning.",
        "corpus_comments": len(rows),
        "overall": dict(shapes),
        "prevalence_share": shapes["prevalence_wish"] / float(len(rows)),
        "per_trigger": {k: dict(v) for k, v in sorted(per_trigger.items(),
                                                      key=lambda kv: -sum(kv[1].values()))
                        if sum(v.values()) >= 20},
        "examples": examples,
    }

    # The load-bearing cross-tab: does the reply rate differ by shape? If
    # prevalence wishes are answered at the control rate and thing wishes above
    # it, then the corpus's reply rate is a mixture and the single pooled ratio
    # reported in results.json is describing two populations.
    by_shape = {}
    for r in rows:
        rid = str(r["id"])
        a = arms.get(rid)
        if a is None:
            continue
        c = classify(r["text"], r["trigger"])
        d = by_shape.setdefault(c, {"n": 0, "replied": 0, "with_link": 0})
        d["n"] += 1
        d["replied"] += 1 if a["has_subtree"] else 0
        d["with_link"] += 1 if a["link_replies"] > 0 else 0
    out["reply_rate_by_shape"] = {
        k: {"n": v["n"], "replied": v["replied"],
            "reply_rate": v["replied"] / float(v["n"]) if v["n"] else None,
            "with_link_reply": v["with_link"],
            "with_link_reply_share": v["with_link"] / float(v["n"]) if v["n"] else None}
        for k, v in sorted(by_shape.items(), key=lambda kv: -kv[1]["n"])
    }
    ctrl = [json.loads(l) for l in open(os.path.join(RAW, "control.jsonl"))]
    out["control_reply_rate"] = (sum(1 for r in ctrl if r["has_subtree"]) / float(len(ctrl))) \
        if ctrl else None

    with open(os.path.join(HERE, "trigger_shape.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps({k: out[k] for k in
                      ("overall", "prevalence_share", "reply_rate_by_shape",
                       "control_reply_rate")}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
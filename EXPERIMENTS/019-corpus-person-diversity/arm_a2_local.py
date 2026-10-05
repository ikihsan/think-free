#!/usr/bin/env python3
"""Arm A2: does the need corpus contain any need twice?

Arm A found 1250 distinct authors behind 1401 comments. Whether that is a wide
audience depends on what the rows contain. If no two clauses share a distinctive
word, each row is one person's individual request and a generator that needs a
need to recur has nothing to aggregate. This measures that locally: no network,
no query, no phrasing, so there is no instrument between the clause and the
number.

Writes raw/arm_a2.json.
"""
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(
    HERE, "..", "012-candidate-harvest", "raw", "hn_needs_2026-10-04.jsonl")
SAMPLE = os.path.join(HERE, "..", "012-candidate-harvest", "raw", "sample.jsonl")
OUT = os.path.join(HERE, "raw", "arm_a2.json")

WORD = re.compile(r"[a-z][a-z0-9+#.]{2,}")
STOPWORDS = set("""
a able about above after again against all almost also always am among an and
any are aren around as at back be because been before being below between both
but by came can cannot come could couldn did didn different do does doesn doing
don done down during each either else enough even ever every few first for from
further get gets getting give given go goes going gone good got great had has
have having he her here hers herself him himself his how however i if in into is
it its itself just keep kept last less let like likely little long made make
makes making many may maybe me might mine more most much must my myself never
new next no nor not nothing now of off often on once one only onto or other
otherwise ought our ours ourselves out over own per perhaps put quite rather
really said same saw say see seem seemed seems seen several shall she should
since so some something soon still such sure take taken than that the their
theirs them themselves then there therefore these they thing things think this
those though through thus time to too two under until up upon us use used uses
using very via want was way we well were what when where whether which while
who whole whom whose why will with within without would yet you your yours
""".split())


def path(*parts):
    return os.path.join(HERE, *parts)


def clause(text, trigger):
    i = text.lower().find(trigger)
    if i < 0:
        return ""
    s = text[i + len(trigger):]
    s = re.split(r"[.?!\n]", s)[0]
    return re.sub(r"\s+", " ", s).strip()


def content_words(text):
    return set(WORD.findall(text.lower())) - STOPWORDS


def main():
    rows = [json.loads(l) for l in open(CORPUS) if l.strip()]
    clauses = []
    for r in rows:
        c = clause(r["text"], r["trigger"])
        cw = content_words(c)
        if len(cw) < 3:
            continue  # same eligibility rule E012's sample used (>= 6 tokens)
        clauses.append({"comment_id": r["id"], "clause": c,
                        "content_words": sorted(cw)})

    df = Counter()
    for c in clauses:
        for w in set(c["content_words"]):
            df[w] += 1

    recs = []
    for c in clauses:
        counts = {w: df[w] for w in c["content_words"]}
        bottleneck = min(counts.values()) if counts else 0
        rarest = sorted(counts.items(), key=lambda kv: (kv[1], kv[0]))[:3]
        recs.append({
            "comment_id": c["comment_id"],
            "bottleneck": bottleneck,
            "rarest_terms": [{"term": w, "clauses": n} for w, n in rarest],
            "n_content_words": len(c["content_words"]),
        })

    n = len(recs)
    b1 = [r for r in recs if r["bottleneck"] <= 1]
    shared = {}
    for r in recs:
        if r["bottleneck"] > 1:
            for t in r["rarest_terms"]:
                if t["clauses"] > 1:
                    shared[t["term"]] = max(shared.get(t["term"], 0), t["clauses"])
    top = sorted(df.items(), key=lambda kv: (-kv[1], kv[0]))[:25]
    share = len(b1) / float(n) if n else 0.0
    if share >= 0.90:
        verdict = "gate_met_corpus_is_individual_requests"
    elif share < 0.50:
        verdict = "gate_met_sharing_exists_F029_recurrence_reading_wrong"
    else:
        verdict = "no_verdict_distribution_reported"

    sample_ids = set()
    for line in open(SAMPLE):
        sample_ids.add(json.loads(line)["id"])
    srecs = [r for r in recs if r["comment_id"] in sample_ids]
    s_b1 = sum(1 for r in srecs if r["bottleneck"] <= 1)

    out = {
        "eligible_clauses": n,
        "clauses_with_bottleneck_1": len(b1),
        "share_bottleneck_1": round(share, 4),
        "verdict": verdict,
        "bottleneck_histogram": dict(list(sorted(
            Counter(r["bottleneck"] for r in recs).items()))[:15]),
        "top_document_frequency_terms": [{"term": w, "clauses": k}
                                          for w, k in top],
        "terms_shared_by_any_clause": len(shared),
        "the_50_row_screen_sample": {
            "clauses": len(srecs),
            "bottleneck_1": s_b1,
            "share_bottleneck_1": round(
                s_b1 / float(len(srecs) or 1), 4)},
        "rules": {
            "content_word": "lowercase token matching [a-z][a-z0-9+#.]{2,} "
                            "and not in the declared stopword list, taken from "
                            "the clause text only",
            "eligibility": "at least 3 content words, matching E012's >=6 "
                           "token filter closely enough to cover its sample",
            "bottleneck": "min over the clause's content words of the number "
                          "of clauses containing that word; 1 means no other "
                          "clause shares any content word",
        },
        "computed_by": "arm_a2_local.py, local files only",
    }
    with open(path("raw", "arm_a2.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True)[:2400])
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""Both declared gates for 016, implemented from `README.md` so neither can be
adjusted to a result.

H1  dead if `document` is <= 50% of the readable young arm, or if document rows
    clear a serving floor at the same rate executable rows do (within 10 points).
    Survives otherwise. Both conditions reported separately: a run can fail on one
    and pass on the other, and saying only the verdict would hide which.

H2  survives at >= 4 of the 10 rows that are `repeated and teaches_only`, dead at
    <= 2, inconclusive at 3. The gate does not round up.

Control, declared before the read: if the placebo rows are *also* predominantly
`repeated and teaches_only`, H2's generative reading -- a high-star document
witnesses an unmet need -- is dead even though the descriptive claim survives. The
control is reported as its own arm and never merged into the H2 count.

    python3 tally.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.json")
PREV = os.path.join(os.path.dirname(HERE), "015-incumbent-serving")
for path in (PREV, HERE):
    if path not in sys.path:
        sys.path.insert(0, path)

import classification  # noqa: E402
import readfields       # noqa: E402
import servingjoin      # noqa: E402

H1_DOCUMENT_SHARE_DEAD = 0.50
H1_RATE_PARITY_POINTS = 0.10
H2_SURVIVES_AT = 4
H2_DEAD_AT = 2
H2_N = 10
H2_KEY = "repeated_teaches_only"


def h1(rows):
    young = [r for r in rows if r["arm"] == "young"]
    readable = [r for r in young if r["class"] != "unreadable"]
    documents = [r for r in readable if r["class"] == "document"]
    share = (len(documents) / float(len(readable))) if readable else None

    def rate_of(cls):
        decided = [r for r in young if r["class"] == cls and not r["undecided"]]
        hit = [r for r in decided if r["served"]]
        return (len(hit) / float(len(decided))) if decided else None, len(decided)

    doc_rate, doc_decided = rate_of("document")
    exe_rate, exe_decided = rate_of("executable")

    conditions = []
    if share is None:
        verdict = "inconclusive"
        conditions.append({"name": "document_share", "detail": "no readable row"})
    else:
        share_dead = share <= H1_DOCUMENT_SHARE_DEAD
        conditions.append({"name": "document_share",
                           "value": round(share, 4),
                           "dead": bool(share_dead),
                           "detail": "%d of %d readable young rows"
                                     % (len(documents), len(readable))})
        parity = None
        if doc_rate is not None and exe_rate is not None:
            parity = abs(doc_rate - exe_rate) <= H1_RATE_PARITY_POINTS
            conditions.append({"name": "rate_parity", "value": round(doc_rate - exe_rate, 4),
                               "dead": bool(parity),
                               "detail": "document %s on %d decided, executable %s on %d decided"
                                         % (_pct(doc_rate), doc_decided,
                                            _pct(exe_rate), exe_decided)})
        else:
            conditions.append({"name": "rate_parity", "value": None, "dead": False,
                               "detail": "one class has no decided row, so the two "
                                         "cannot be compared; the gate is decided "
                                         "on the share alone and says so"})
        # The gate as declared is `dead = share_fires OR parity_fires`, so one
        # firing condition is enough. A condition that could not be computed is
        # not counted as firing, and its reason is printed rather than absorbed.
        fired = [c for c in conditions if c["dead"]]
        verdict = "dead" if fired else "survives"
    return {"hypothesis": "H1", "verdict": verdict, "conditions": conditions,
            "readable": len(readable), "documents": len(documents),
            "document_repos": sorted(r["repo"] for r in documents),
            "unreadable_repos": sorted(r["repo"] for r in young
                                       if r["class"] == "unreadable")}


def _pct(value):
    return "n/a" if value is None else "%d%%" % round(100 * value)


def h2(reads, mech):
    """The read arm, over the declared population.

    Population rule, declared: the H_N highest-starred young-arm rows classified
    `document`. `reads.json` may name a different set; if it does, the difference
    is reported as `population_mismatch` rather than absorbed.
    """
    rows = reads.get("rows") or {}
    scored = []
    for repo, row in rows.items():
        m = mech.get(repo) or {}
        teaches_only = m.get("class") == "teaches_only"
        key = bool(row.get("repeated")) and teaches_only
        scored.append({"repo": repo, "stars": row.get("stars"),
                       "repeated": bool(row.get("repeated")),
                       "teaches_only": teaches_only,
                       "install_line": m.get("install_line"),
                       "foreign_link": m.get("foreign_link"),
                       "key": key, "class": m.get("class"),
                       "shell_blocks": m.get("shell_blocks"),
                       "arm": row.get("arm"),
                       "procedure": row.get("procedure"),
                       "judgement_note": row.get("judgement_note")})
    primary = [s for s in scored if s["arm"] != "placebo"]
    control = [s for s in scored if s["arm"] == "placebo"]
    hits = [s for s in primary if s["key"]]
    control_hits = [s for s in control if s["key"]]

    if not primary:
        # A gate asked about a population nobody read must not answer `dead`. The
        # declared thresholds are counts out of the declared population, and with
        # no rows there is nothing to count; reporting `dead` here would put a
        # verdict in the record that no evidence supports, which is the defect
        # class this repository keeps finding in its own instruments.
        verdict = "not_evaluated"
    elif len(hits) >= H2_SURVIVES_AT:
        verdict = "survives"
    elif len(hits) <= H2_DEAD_AT:
        verdict = "dead"
    else:
        verdict = "inconclusive"

    generative = "dead" if (control and len(control_hits) >= max(2, len(control) // 2)) \
        else "live"
    return {"hypothesis": "H2", "verdict": verdict,
            "n": len(primary), "hits": len(hits), "key": H2_KEY,
            "population_short": len(primary) < H2_N,
            "population_declared_n": H2_N,
            "hit_repos": sorted(s["repo"] for s in hits),
            "rows": sorted(primary, key=lambda s: -(s["stars"] or 0)),
            "control": {"n": len(control), "hits": len(control_hits),
                        "hit_repos": sorted(s["repo"] for s in control_hits),
                        "rows": sorted(control, key=lambda s: -(s["stars"] or 0)),
                        "generative_reading": generative},
            "population_mismatch": reads.get("population_mismatch"),
            "declared_population": reads.get("declared_population")}


def audit(rows, reviewed):
    """The mechanical class beside a hand review of every row.

    Neither number replaces the other and the gate is computed on the mechanical
    one, because the gate was declared on the mechanical one. The review exists so
    that the mechanical rule's error rate is visible and its direction is known.
    A row with no review is counted as `unreviewed`, never as agreement.
    """
    reviewed = (reviewed or {}).get("rows", reviewed) or {}
    by_arm = {}
    for row in rows:
        arm = row["arm"]
        cell = by_arm.setdefault(arm, {"agree": 0, "disagree": 0, "unreviewed": 0,
                                       "boundary": 0, "rows": []})
        entry = reviewed.get(row["repo"]) or {}
        hand = entry.get("reviewed_class")
        cell["rows"].append({"repo": row["repo"], "stars": row["stars"],
                             "mechanical": row["class"],
                             "reviewed": hand,
                             "hits": row.get("hits", []),
                             "boundary": bool(entry.get("boundary")),
                             "reason": entry.get("reason")})
        if hand is None:
            cell["unreviewed"] += 1
        elif hand == row["class"]:
            cell["agree"] += 1
        else:
            cell["disagree"] += 1
        if entry.get("boundary"):
            cell["boundary"] += 1
    return by_arm


def build(reviewed=None, reads=None):
    rows = servingjoin.joined_rows()
    mech = readfields.fields()
    reads = reads if reads is not None else _load(HERE, "reads.json", default={})
    reviewed = reviewed if reviewed is not None else _load(HERE, "reviewed.json", default={})
    unclassified = sorted(r["repo"] for r in rows if r["class"] == "unreadable"
                          and r["class_reason"] == "not_fetched")
    out = {
        "population": {
            "rows": len(rows),
            "by_arm": {arm: sum(1 for r in rows if r["arm"] == arm)
                       for arm in servingjoin.ARMS},
            "unfetched_rows": unclassified,
            "complete": not unclassified,
            "reused_from": "EXPERIMENTS/015-incumbent-serving/results.json",
        },
        "classification": classification.DECLARED_CORRECTION,
        "arms": servingjoin.by_arm_and_class(rows),
        "h1": h1(rows),
        "h2": h2(reads, mech),
        "audit": audit(rows, reviewed),
    }
    return out


def _load(path, name, default=None):
    full = os.path.join(path, name)
    if not os.path.exists(full):
        return {} if default is None else default
    with open(full) as fh:
        return json.load(fh)


if __name__ == "__main__":
    result = build()
    if "--write" in sys.argv:
        with open(RESULTS, "w") as fh:
            json.dump(result, fh, indent=1, sort_keys=True)
        print("wrote %s" % RESULTS)
    print(json.dumps({"h1": result["h1"]["verdict"],
                      "h1_conditions": [(c["name"], c.get("dead")) for c in result["h1"]["conditions"]],
                      "h2": result["h2"]["verdict"],
                      "h2_hits": result["h2"]["hits"],
                      "h2_control": result["h2"]["control"]["generative_reading"],
                      "population_complete": result["population"]["complete"]},
                     indent=1))
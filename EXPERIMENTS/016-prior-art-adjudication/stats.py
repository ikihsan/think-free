#!/usr/bin/env python3
"""E016's two gate arms, computed from the record rather than from memory.

Reads phrasings.json and raw/attributions.jsonl, checks the stopping rule
against what each corpus was actually asked, and writes results.json. Nothing
here decides a verdict: the verdicts are the attributed judgement in
raw/attributions.jsonl, and this script only counts them and states the arms.

Standard library only.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# A refusal is never an absence, and the corpora this run could not read are
# named rather than silently counted as empty.
INSTRUMENT = {
    "github": {"status": "read", "queries": 38, "refusals": 0,
               "url": "https://api.github.com/search/repositories?q=...+in:name,description&per_page=5"},
    "registries": {"status": "read", "queries": 171, "refusals": 0,
                   "note": "PyPI's /search/ answers a bot challenge, so the leg is the complete "
                           "project-name index (905,521 names, sha256 in raw/pypi-simple-meta.json): "
                           "names only, no descriptions.",
                   "pypi_index": "raw/pypi-simple-index.txt"},
    "openweb": {"status": "read_after_two_failures", "queries": 14,
                "engine": "duckduckgo-lite through the harness webfetch",
                "instrument_check": "known-answer control answered with the named artifact; "
                                    "nonsense-token control returned a challenge rather than results",
                "refused_first": ["duckduckgo-html via script: HTTP 202 on 19 of 19 queries",
                                  "bing-html via script: HTTP 200 with results unrelated to the query",
                                  "brave via webfetch: HTTP 429",
                                  "harness websearch tool: cancelled"]},
}

ARMS = {
    1: {"question": "instrument validity: at least 5 of the 6 positive controls re-adjudicated served",
        "threshold": ">= 5 of 6"},
    2: {"question": "of the 13 kills with no populated count behind them, how many are "
                    "no prior art found on all three corpora",
        "threshold": ">= 3 means prior_art is materially overstated as a cause of death and "
                     "F029's cause table is restated; <= 2 confirms the category and closes "
                     "need-harvesting as a generator"},
}


def load():
    with open(os.path.join(HERE, "phrasings.json"), encoding="utf-8") as fh:
        spec = json.load(fh)
    rows = []
    with open(os.path.join(RAW, "attributions.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return spec, rows


def main():
    spec, rows = load()
    declared = {it["index"] for it in spec["items"]}
    controls = {it["index"] for it in spec["items"] if it.get("control")}
    by_index = {r["index"]: r for r in rows}

    missing = sorted(declared - set(by_index))
    extra = sorted(set(by_index) - declared)
    if missing or extra:
        raise SystemExit("attribution rows do not match phrasings.json: missing=%s extra=%s"
                         % (missing, extra))

    def served(r):
        # A contested row is counted as served, which is the direction that
        # favours prior art; the sensitivity row below moves it back.
        return r["verdict"].startswith("served") or r["verdict"].startswith("contested")

    # Arm 1: the controls, in the declared order.
    arm1 = []
    for index in sorted(controls):
        r = by_index[index]
        arm1.append({"index": index, "name": r["name"], "verdict": r["verdict"],
                     "recovered": served(r), "corpora_read": r["corpora_read"],
                     "carrying_corpus": r.get("carrying_corpus")})
    arm1_ok = sum(1 for a in arm1 if a["recovered"])
    arm1_met = arm1_ok >= 5

    # Arm 2: the judgement kills. An item whose clause and reason disagree is
    # neither bucket and is reported apart.
    non_control = sorted(declared - controls)
    arm2, unadjudicable, contested = [], [], []
    for index in non_control:
        r = by_index[index]
        row = {"index": index, "name": r["name"], "verdict": r["verdict"],
               "carrying_corpus": r.get("carrying_corpus"),
               "corpora_read": r["corpora_read"]}
        if r["verdict"].startswith("unadjudicable"):
            unadjudicable.append(row)
        else:
            arm2.append(row)
            if r["verdict"].startswith("contested"):
                contested.append(row)
    not_found = [a for a in arm2 if a["verdict"] == "no_prior_art_found"]
    arm2_count = len(not_found)
    arm2_met = arm2_count >= 3

    # Sensitivity: the one row whose attribution a looser rule would move.
    sensitive = [a["name"] for a in arm2 if a["name"] in ("word-game",)]
    arm2_loose = arm2_count - len([a for a in not_found if a["name"] in sensitive])

    # The stopping rule, checked against the raw logs rather than against the
    # attribution rows' own account of themselves. Two properties, and the
    # first is the load-bearing one:
    #   1. an item called `no prior art found` was asked at least two phrasings
    #      on every one of the three corpora;
    #   2. an item called served names a corpus it was actually read on, so a
    #      verdict cannot rest on a corpus the run never queried for that item.
    asked = {}
    for fname, corpus, key in (("github_search.jsonl", "github", "phrasing"),
                               ("registry_search.jsonl", "registries", "keyword"),
                               ("web_log.jsonl", "openweb", "query")):
        path = os.path.join(RAW, fname)
        if not os.path.exists(path):
            continue
        members = {"github": {"github"}, "registries": {"pypi", "npm", "crates"},
                   "openweb": {"openweb"}}[corpus]
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if rec.get("corpus") not in members or not isinstance(rec.get("index"), int):
                    continue
                if corpus == "openweb" and rec.get("engine") != "duckduckgo-lite-via-webfetch":
                    continue
                asked.setdefault((rec["index"], corpus), set()).add(rec.get(key))
    violations = []
    for row in arm1 + arm2:
        read = row["corpora_read"]
        if row["verdict"] == "no_prior_art_found":
            for corpus in ("github", "registries", "openweb"):
                n = len(asked.get((row["index"], corpus), ()))
                if n < 2:
                    violations.append({"index": row["index"], "name": row["name"],
                                       "corpus": corpus, "phrasings_asked": n,
                                       "rule": "no prior art found needs >= 2 phrasings on every corpus"})
        if row["verdict"].startswith("served") and row.get("carrying_corpus") not in read:
            violations.append({"index": row["index"], "name": row["name"],
                               "carrying_corpus": row.get("carrying_corpus"), "read": read,
                               "rule": "a served verdict must name a corpus the run actually read"})

    results = {
        "experiment": "E016 prior-art adjudication",
        "computed_by": "stats.py from raw/attributions.jsonl and phrasings.json",
        "items": len(declared),
        # The population this run examined, named so a mission record's
        # denominator can be held to it (D047): an adjudicated item is a case,
        # and `cases` is the word `resultnumbers.py` reads.
        "cases_adjudicated": len(declared),
        "cases_controls": len(controls),
        "cases_judgement_kills_declared": len(non_control),
        "cases_judgement_kills_adjudicable": len(arm2),
        "cases_judgement_kills_unadjudicable": len(unadjudicable),
        "cases_no_prior_art_found": arm2_count,
        "cases_controls_recovered": arm1_ok,
        "controls": len(controls),
        "instrument": INSTRUMENT,
        "arm_1": {"threshold": ARMS[1]["threshold"], "question": ARMS[1]["question"],
                  "recovered": arm1_ok, "met": arm1_met, "detail": arm1,
                  "ceiling": "The six controls were selected for having a populated count, so "
                             "recovery demonstrates that the instrument finds a populated "
                             "category. It cannot show that the instrument can find an "
                             "attribute inside a category, which is the failure mode that "
                             "matters for the other thirteen."},
        "arm_2": {"threshold": ARMS[2]["threshold"], "question": ARMS[2]["question"],
                  "denominator": len(arm2), "no_prior_art_found": arm2_count, "met": arm2_met,
                  "not_found_items": not_found, "detail": arm2,
                  "unadjudicable": unadjudicable, "contested": contested,
                  "sensitivity": {"rows": sensitive, "count_if_looser_rule": arm2_loose,
                                  "why": "Counting the answer-aggregator sites as serving the "
                                         "word-game clause moves the count across the declared "
                                         "threshold, so this row decides the direction and the "
                                         "rule used is stated."}},
        "stopping_rule_violations": violations,
        "phrasings_asked": {"%d/%s" % k: sorted(v) for k, v in sorted(asked.items())},
        "corpus_carriage": {
            "openweb": [a["name"] for a in arm2 if a.get("carrying_corpus") == "openweb"],
            "served_without_openweb": [a["name"] for a in arm1 + arm2
                                       if a["verdict"].startswith("served")
                                       and a.get("carrying_corpus") != "openweb"],
            "registries_carried_none": not any(a.get("carrying_corpus") == "registries"
                                               for a in arm1 + arm2)},
        "limits": [
            "Absence of a hit on three corpora is the absence of a hit. It is not novelty.",
            "The adjudicator is the same model that drew the sample and wrote the original "
            "reasons; the positive controls bound the instrument's error from one side only.",
            "Attribution is judgement and is recorded per item with the deciding text, so a "
            "reader can move any single row and recompute.",
            "The open-web corpus was read for the seven items the code corpora left unresolved; "
            "the other items stopped at the declared stopping rule and were not re-read there.",
        ],
    }
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)

    print("arm 1: %d of 6 controls recovered, threshold >=5, met=%s" % (arm1_ok, arm1_met))
    for a in arm1:
        print("   %2d %-18s %-38s %s" % (a["index"], a["name"], a["verdict"], a["corpora_read"]))
    print("arm 2: %d of %d judgement kills are no prior art found, threshold >=3, met=%s"
          % (arm2_count, len(arm2), arm2_met))
    for a in arm2:
        print("   %2d %-22s %-38s carried_by=%s" % (a["index"], a["name"], a["verdict"],
                                                    a["carrying_corpus"]))
    for a in unadjudicable:
        print("   %2d %-22s %s" % (a["index"], a["name"], a["verdict"]))
    print("sensitivity: %d under a looser rule on %s" % (arm2_loose, ",".join(sensitive)))
    print("stopping-rule violations: %d" % len(violations))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
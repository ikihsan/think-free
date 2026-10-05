#!/usr/bin/env python3
"""Build E028's population from two existing captures. Read-only on both.

The output splits the three facts a reader must not see at once:

  raw/requirements.jsonl  what was wanted, and nothing about its fate
  raw/incumbents.jsonl     which artifacts a screen NAMED (a fact, not a verdict)
  raw/record_facts.json    the verdict and kill reason, for the results table only

The separation is the point. A reader given requirements.jsonl cannot know which
rows died of prior art, and a reader given incumbents.jsonl cannot see the
requirement text until the reader is asked for Step A.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SCREENED = os.path.join(ROOT, "EXPERIMENTS", "012-candidate-harvest",
                        "raw", "screened.jsonl")
ATTRIB = os.path.join(ROOT, "EXPERIMENTS", "016-prior-art-adjudication",
                      "raw", "attributions.jsonl")
KILLROWS = os.path.join(ROOT, "EXPERIMENTS", "024-kill-reason-causes",
                        "rows.json")
OUT = os.path.join(HERE, "raw")


def jl(path):
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def write(name, rows):
    path = os.path.join(OUT, name)
    with open(path, "w") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    return len(rows)


def main():
    screened = {r["index"]: r for r in jl(SCREENED)}
    attrib = {r["index"]: r for r in jl(ATTRIB)}

    requirements = []
    incumbents = []
    facts = []
    for idx in sorted(screened):
        s = screened[idx]
        if s.get("cause") != "prior_art":
            continue
        rid = "H%02d" % idx
        # F047: the full comment, never the regex clause.
        requirements.append({
            "row": rid,
            "arm": "harvest",
            "requirement_text": s["text"],
            "story_title": s.get("story"),
            "date": s.get("date"),
            "trigger": s.get("trigger"),
        })
        a = attrib.get(idx, {})
        bundle = []
        for corpus, val in (a.get("attribution") or {}).items():
            if not isinstance(val, dict):
                continue
            for name in val.get("artifacts") or []:
                bundle.append({"corpus": corpus, "artifact": name})
        incumbents.append({"row": rid, "artifacts": bundle})
        facts.append({
            "row": rid,
            "screen": "E012/E016",
            "verdict": a.get("verdict"),
            "carrying_corpus": a.get("carrying_corpus"),
            "n_artifacts": len(bundle),
            "e012_reason": s.get("reason"),
            "e012_name": s.get("name"),
            "e016_note": a.get("note"),
        })

    with open(KILLROWS) as fh:
        kills = json.load(fh)
    sealed_ids = [r["id"] for r in kills["rows"]
                  if r.get("category") == "prior_art"]
    with open(os.path.join(OUT, "sealed_row_ids.json"), "w") as fh:
        json.dump({"sealed_prior_art_rows": sealed_ids}, fh, indent=2)
        fh.write("\n")

    n1 = write("requirements.jsonl", requirements)
    n2 = write("incumbents.jsonl", incumbents)
    n3 = write("record_facts.json", facts)
    named = [f for f in facts if f["n_artifacts"] > 0]
    print(json.dumps({
        "harvest_requirements": n1,
        "harvest_bundles": n2,
        "record_facts": n3,
        "rows_with_at_least_one_named_artifact": len(named),
        "rows_naming_no_artifact": len(facts) - len(named),
        "sealed_prior_art_rows_pending_arm_2": sealed_ids,
        "total_population": n1 + len(sealed_ids),
    }, indent=2))


if __name__ == "__main__":
    main()
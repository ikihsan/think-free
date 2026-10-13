#!/usr/bin/env python3
"""E126 G0: score the discrimination probes.

The instrument is the session's model. Each probe's label
is known by construction (see g0-probes.json): the ten
`answerable` probes have canonical general-knowledge
answers; the ten `specific` probes cannot be resolved from
the post alone by construction.

Pass rule (declared in PROTOCOL.md): >= 9/10 answered on
the answerable set AND >= 9/10 declined on the specific
set. Fail: the instrument fails and no rate is read.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    probes = {p["probe_id"]: p
              for p in json.load(
                  open(os.path.join(HERE, "g0-probes.json")))["probes"]}
    results = [json.loads(line)
               for line in open(os.path.join(HERE, "g0-results.jsonl"))
               if line.strip()]
    assert len(results) == 20, len(results)

    by_label = {"answerable": {"answered": 0, "n": 0},
                "specific": {"declined": 0, "n": 0}}
    for r in results:
        p = probes[r["probe_id"]]
        assert p["label"] == r["label"], r["probe_id"]
        label = p["label"]
        by_label[label]["n"] += 1
        if label == "answerable" and r["verdict"] == "answered":
            by_label["answerable"]["answered"] += 1
        if label == "specific" and r["verdict"] == "declined":
            by_label["specific"]["declined"] += 1

    a = by_label["answerable"]
    s = by_label["specific"]
    passed = a["answered"] >= 9 and s["declined"] >= 9
    out = {
        "answerable": a, "specific": s,
        "pass_rule": ">=9/10 answered AND >=9/10 declined",
        "g0_pass": passed,
    }
    with open(os.path.join(HERE, "g0.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""E136: dump every row where the recomputed verdict differs from the
harness's own per-instance verdict, with the extracted forms."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recompute_math import (SUBJECTS, boxed_all, normalize, equiv, load_run,
                            safe_eval, D)


def main():
    for subj in SUBJECTS:
        ss, stats, pis = load_run(subj)
        states = ss["request_states"]
        hv = {}
        for p in pis:
            for st in p["stats"]:
                if st["name"]["name"] == "math_equiv_chain_of_thought":
                    hv[p["instance_id"]] = st["mean"]
        for rs in states:
            inst = rs["instance"]
            refs = [r for r in inst["references"] if "correct" in r.get("tags", [])]
            gb = boxed_all(refs[0]["output"]["text"]) if refs else []
            cb = boxed_all(rs["result"]["completions"][0]["text"])
            gold = gb[-1] if gb else None
            pred = cb[-1] if cb else None
            v = equiv(pred, gold) if gold is not None and pred is not None else False
            h = hv.get(inst["id"])
            if h is not None and (h == 1.0) != v:
                np_, ng = normalize(pred), normalize(gold)
                print(f"=== {subj} / {inst['id']}  mine={int(v)} harness={h}")
                print(f"    gold raw : {gold!r}")
                print(f"    pred raw : {pred!r}")
                print(f"    gold norm: {np_!r}  eval={safe_eval(np_)}")
                print(f"    pred norm: {np_!r}  eval={safe_eval(np_)}")


if __name__ == "__main__":
    main()

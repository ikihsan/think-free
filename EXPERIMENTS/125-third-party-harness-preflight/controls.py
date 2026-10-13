"""E125 controls -- the two declared negative controls, and the
information-sufficiency witness.

Both are in PROTOCOL.md and neither had been run when the pairs were measured.

**Control 1 (sound pair).** E116's repaired key and its answers must come back
`OK`. That is E124's case B re-run here, unmodified, on files this repository
wrote -- the one pair in this experiment where the join is known to work.

**Control 2 (positional control) and the witness.** Two realities produce
identical inputs to C1: a harness that joins by position and ships unrelated
identifier names, where the join works; and a harness that joins by field where
the two files name the same entities in different types, where the join matches
nothing. The files are byte-identical between the two worlds. Both are built
here from the same bytes.

The control asserts two things:

1. the *pipeline* refuses to qualify the pair, so it is never reported as clean;
2. **C1 alone would have fired on it** -- which is the witness. If C1 stayed
   silent here, the witness would be wrong and the claim "no C1 verdict may be
   reported without M2 beside it" would be unsupported.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "124-eval-harness-preflight"))
from probe import classify, concordance, load_rows, m4_qualifies  # noqa: E402
from preflight import concordance as c1  # noqa: E402


def control_1():
    """E124's case A and case B, re-run unmodified.

    The distinction this control tripped over is worth keeping rather than
    fixing quietly: **the sound pair does not exist as a committed file.**
    `EXPERIMENTS/116-berka-service-test/key.jsonl` holds the *defective*
    integer ids -- that is case A, and C1 correctly fires on it. `score.py`
    repairs the id at load time, composing `"%s%03d" % (arm, account_id)`, and
    that in-memory key is case B. The repair expression is copied from E124's
    `run.py` so this is its case B and not a new variant.
    """
    base = os.path.join(HERE, "..", "116-berka-service-test")
    key, how_k = load_rows(open(os.path.join(base, "key.jsonl"), "rb").read(), "key.jsonl")
    ans, how_a = load_rows(open(os.path.join(base, "answers.jsonl"), "rb").read(), "answers.jsonl")
    repaired = [dict(r, account_id="%s%03d" % (r["arm"], r["account_id"])) for r in key]
    as_committed = concordance(key, ans)
    as_repaired = concordance(repaired, ans)
    return {"control": "sound pair (both readings of the same committed file)",
            "source": "EXPERIMENTS/116-berka-service-test",
            "key_rows": len(key), "answer_rows": len(ans), "how": [how_k, how_a],
            "case_a_committed_key": {"verdict": as_committed["verdict"],
                                     "best_rate": as_committed["best_rate"],
                                     "expected": "SILENT_NO_MATCH"},
            "case_b_repaired_key": {"verdict": as_repaired["verdict"],
                                    "best_rate": as_repaired["best_rate"],
                                    "expected": "OK"},
            "pass": (as_committed["verdict"] == "SILENT_NO_MATCH"
                     and as_repaired["verdict"] == "OK")}


def _positional_world():
    """One bytes-to-two-worlds witness. Returns the shared rows and the two readings."""
    key_rows = [{"order_ref": "A-0001", "expected_monthly": "1200"},
                {"order_ref": "A-0002", "expected_monthly": "800"}]
    out_rows = [{"line_ref": "L-77", "agent_reply": "confirmed"},
                {"line_ref": "L-78", "agent_reply": "confirmed"}]
    return key_rows, out_rows


def control_2():
    """The same bytes, read two ways. The pipeline must refuse; C1 alone must fire."""
    key_rows, out_rows = _positional_world()

    # Reading 1: this harness joins by position. The join works, row for row.
    positional_join_works = all(
        key_rows[i]["expected_monthly"] is not None for i in range(len(out_rows)))

    # Reading 2: identical bytes, harness joins by field. The join sees nothing.
    verdict = c1(key_rows, out_rows)

    # The pipeline's qualification rule, applied to the same two files.
    k, o = classify(key_rows), classify(out_rows)
    qualified, why = m4_qualifies(k, o)

    return {"control": "positional control / information-sufficiency witness",
            "key_rows": key_rows, "output_rows": out_rows,
            "reading_1_positional_join_works": positional_join_works,
            "reading_2_c1_verdict": verdict["verdict"],
            "reading_2_best_rate": verdict["best_rate"],
            "pipeline_qualified": qualified,
            "pipeline_reason": why,
            "expected": {
                "positional_join_works": True,
                "c1_fires_on_identical_bytes": True,
                "pipeline_qualified": False},
            "pass": (positional_join_works and verdict["verdict"] != "OK"
                     and not qualified)}


def main():
    out = {"experiment": "E125",
           "control_1_sound_pair": control_1(),
           "control_2_positional": control_2()}
    with open(os.path.join(HERE, "controls.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    for k in ("control_1_sound_pair", "control_2_positional"):
        c = out[k]
        print("%-34s pass=%s" % (k, c["pass"]))
        for kk, vv in sorted(c.items()):
            if kk in ("key_rows", "output_rows", "control", "expected"):
                continue
            print("    %-34s %s" % (kk, str(vv)[:110]))
    ok = all(out[k]["pass"] for k in ("control_1_sound_pair", "control_2_positional"))
    print("\ndeclared controls: %s"
          % (", ".join("%s=%s" % (k, "PASS" if out[k]["pass"] else "FAIL")
                       for k in ("control_1_sound_pair", "control_2_positional"))))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
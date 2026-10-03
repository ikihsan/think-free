"""Information-sufficiency witnesses for the three held candidates.

For each candidate, construct two underlying realities that give the proposed
system *identical permitted inputs* but require *different outputs*.  Then ask
the deciding question:

  - Passive systems: if the inputs are identical, no computation can separate
    them, so the candidate is information-insufficient.
  - Active systems (a policy that may choose an observation): if the permitted
    observation menu contains an action that yields differing readings between
    the two realities, the policy is sufficient; if *no* permitted action
    separates them, it is information-insufficient.

Every input here is SYNTHETIC and labelled as such.  A synthetic witness can
falsify an unbounded claim; it cannot measure how often the ambiguity occurs in
the wild.  That limit is stated in README.md and results.json.

Run from the repository root:

    python3 EXPERIMENTS/003-information-sufficiency/witness.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from witnesses import knitting_witness, sidewalk_witness
from witness_vent import ventilation_witness

OUT = Path(__file__).resolve().parent / "results.json"


def _stable(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, default=str).encode()
    ).hexdigest()[:16]


def main() -> int:
    witnesses = {
        "W1_sidewalk_survey": sidewalk_witness(),
        "W2_knitting_repair": knitting_witness(),
        "W3_ventilation": ventilation_witness(),
    }
    results = {
        "schema": "origin.experiment.information-sufficiency/1",
        "experiment": "003-information-sufficiency",
        "synthetic": True,
        "note": (
            "All inputs are synthetic. A synthetic witness can falsify an unbounded "
            "claim; it cannot measure how often the ambiguity occurs in real data."
        ),
        "witnesses": witnesses,
        "input_hashes": {name: _stable(w) for name, w in witnesses.items()},
    }
    OUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for name, w in witnesses.items():
        print(f"== {name}: {w['candidate']} ==")
        print(f"   system: {w['system']}")
        if "verdict" in w:
            print(f"   verdict: {w['verdict']}")
        if w["system"] == "active" and "separating_actions" in w:
            print(f"   separating actions: {w['separating_actions']}")
        print()
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

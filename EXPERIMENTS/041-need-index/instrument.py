#!/usr/bin/env python3
"""E041 gate evaluation and the driver that runs the arms.

Split at the 300-line cap **by invariant**, three ways: `readout.py` reads a text
unit and produces partner ranks; `gates.py` evaluates the bars over those ranks;
this file drives the whole run and assembles the artifact. **A threshold and the
statistic it licenses must not be editable in the same place** — the reasoning that
split E040's `gates.py` from its `tally.py`, and `DECISIONS-SCREENING-9.md` D069 is
the rule behind it: where a threshold cannot be calibrated on a valid control, the
dependent claim is restated threshold-free rather than recalibrated elsewhere.

Every bar here is the one `PROTOCOL.md` declared: 1.5, 0.20, 0.50, 0.50. Nothing was
moved after a result was read. The one change of *evaluation* is recorded in
`AMENDMENT-7.md`: **a ratio with a zero denominator is `not_evaluated`, not
`False`**, because F067's defect — a strongly positive result printing red — made it
into the first version of this code.

`--reuse` re-evaluates the gates from `raw/unit_*.json` without re-paying for the
unit steps, which cost 20 s and 552 s on this host; it refuses to run if either file
is missing, so it cannot report on absent work.
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)

import readout  # noqa: E402
from readout import load_meta, note  # noqa: E402

# This directory's `gates.py` is loaded **by path**, not by name. E040's `gates.py`
# is on sys.path too -- it holds the instrument's own parameters -- and a bare
# `from gates import ...` resolves to whichever the path search finds first, which
# was E040's, giving `cannot import name 'BOOT' from 'gates'`. Two files in two
# experiments may share a name; an import must say which one it means.
import importlib.util                            # noqa: E402
_spec = importlib.util.spec_from_file_location(
    "e041_gates", os.path.join(HERE, "gates.py"))
_g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_g)
N0_LOUD_CEILING = _g.N0_LOUD_CEILING
TAUS = _g.TAUS
evaluate_unit = _g.evaluate_unit
summarise = _g.summarise
verdict_of = _g.verdict_of
TOP1_BAR = _g.TOP1_BAR        # recorded in the artifact; never evaluated here
RECALL_BAR = _g.RECALL_BAR
RATIO_BAR = _g.RATIO_BAR
DIFF_BAR = _g.DIFF_BAR
G4_RATIO = 1.5                # E040's own G1 bar, re-used for the transfer check
BOOT = 10000
SEED = 20261006
OUT = os.path.join(RAW, "tally.json")


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--unit":
        return readout.run_unit(sys.argv[2])
    if len(sys.argv) == 4 and sys.argv[1] == "--g4":
        return readout.run_g4_unit(sys.argv[2], sys.argv[3])

    reuse = "--reuse" in sys.argv
    summary_in, pairs = load_meta()
    note("start", corpus_rows=summary_in["corpus_rows"], pairs=len(pairs),
         excluded=sorted(summary_in["repos_excluded_automation"]))

    results, gates, verdicts, frozen_by_unit = {}, {}, {}, {}
    for unit in ("U1", "U2"):
        path = os.path.join(RAW, "unit_%s.json" % unit)
        t0 = time.time()
        if not reuse:
            if os.path.exists(path):
                os.remove(path)
            rc = subprocess.call([sys.executable, os.path.abspath(__file__),
                                  "--unit", unit])
            if rc != 0:
                raise SystemExit("unit %s failed in its own process (exit %d)"
                                 % (unit, rc))
        elif not os.path.exists(path):
            raise SystemExit("--reuse given but raw/unit_%s.json is absent; run "
                             "without --reuse first" % unit)
        with open(path) as fh:
            res = json.load(fh)
        note("unit_%s" % unit, seconds=-1 if reuse else round(time.time() - t0, 1),
             **summarise(res)["pooled"])
        results[unit] = summarise(res)
        g, frozen = evaluate_unit(res)
        gates[unit] = g
        frozen_by_unit[unit] = frozen
        verdicts[unit] = verdict_of(g)
        note("gates_%s" % unit, frozen_tau=frozen, verdict=verdicts[unit])

    note("g4_start")
    g4 = {}
    for unit in ("U1", "U2"):
        frozen = frozen_by_unit[unit]
        if frozen is None or not pairs:
            g4[unit] = {"met": "not_evaluated"}
            continue
        rc = 0 if reuse else subprocess.call(
            [sys.executable, os.path.abspath(__file__),
             "--g4", unit, "%.2f" % frozen])
        path = os.path.join(RAW, "g4_%s.json" % unit)
        if rc != 0 or not os.path.exists(path):
            g4[unit] = {"met": "not_evaluated (the G4 subprocess failed)"}
            continue
        with open(path) as fh:
            g4[unit] = json.load(fh)
        note("g4_%s" % unit, **g4[unit])
    gates["G4"] = g4

    out = {"instrument": {
        "taus": TAUS, "n0_loud_ceiling": N0_LOUD_CEILING,
        "top1_bar": TOP1_BAR, "recall_bar": RECALL_BAR,
        "ratio_bar": RATIO_BAR, "diff_bar": DIFF_BAR, "g4_ratio_bar": G4_RATIO,
        "bootstrap": {"n": BOOT, "seed": SEED},
        "corpus_rows": summary_in["corpus_rows"],
        "pairs": summary_in["pairs_P"],
        "strata": summary_in["pairs_by_stratum"],
        "corpus_sha256": summary_in["corpus_sha256"],
        "repos_excluded_automation": summary_in["repos_excluded_automation"],
        "instrument_source": ("E040 gates.py (imported), streamed by stream.py "
                              "with a per-unit equivalence check")},
        "results": results, "gates": gates, "verdict_by_unit": verdicts}
    tmp = OUT + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    os.replace(tmp, OUT)
    note("done", out=OUT)
    print(json.dumps(verdicts, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

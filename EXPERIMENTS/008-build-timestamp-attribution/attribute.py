"""E3's attribution half: which bytes of a rebuild difference are timestamps.

`007-build-timestamps` measured prevalence and could say nothing about cause
(`FAILURES.md` F010). This builds the same sources repeatedly under one real
builder in two real configurations and attributes every differing byte to a
named cause, by rewriting only the timestamp fields and checking whether the
artifacts then become identical.

Arms (predeclared in README.md before any of this code existed):

  H  SOURCE_DATE_EPOCH set      a builder honouring the standard. An
                                implementation check, not a discovery: wheel
                                0.34.2's source already says where every
                                entry's date comes from.
  N  SOURCE_DATE_EPOCH unset    wheel 0.34.2 falls back to each file's own
                                mtime, which is the shape the census found in
                                most published wheels.

The builds live in `builds.py`; the byte-level machinery is `zipdiff.py`.

Run: cd EXPERIMENTS/008-build-timestamp-attribution && python3 attribute.py
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone

import builds

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.json")
SOURCES_JSON = os.path.join(HERE, "sources.json")
SDIST_DIR = os.path.join(HERE, "sdists")

GATE_SOURCES = 4  # the gate's denominator, fixed in README.md before the run
GATE_MIN = 3


def verdict(results: dict) -> dict:
    """Apply the gate exactly as README.md predeclared it, G4/G5 first.

    Precedence matters: a residual non-timestamp cause is the stronger finding,
    so it must not be masked by a pass on some other clause.
    """
    ordered = []
    for package in results["order"]:
        row = next((r for r in results["sources"] if r["package"] == package), None)
        if row is None or not row.get("built_ok"):
            continue
        pair = row["comparisons"].get("arm_n_different_mtime", {})
        if "error" in pair:
            continue
        ordered.append(row)
    in_gate = ordered[:GATE_SOURCES]

    g1 = [r["package"] for r in in_gate
          if r["comparisons"]["arm_n_different_mtime"]["patch_identical"]]
    # G2 as predeclared is "detected **and attributed to a non-timestamp
    # cause**". The first run implemented it as "the artifacts differ", which a
    # wall-clock stamp satisfies on its own, so the control passed without
    # testing the detector. Require the attribution, not merely a difference.
    g2 = []
    for row in in_gate:
        pair = row["comparisons"].get("planted_content_defect", {})
        kinds = [c["kind"] for c in pair.get("residual_causes_after_patch", [])]
        if pair.get("identical") is False and "content-differs" in kinds:
            g2.append(row["package"])
    g3 = [r["package"] for r in in_gate
          if r["comparisons"]["arm_h_different_mtime"].get("identical") is True]
    residual = [r["package"] for r in in_gate
                if not r["comparisons"]["arm_n_different_mtime"]["patch_identical"]]
    g5 = []
    for row in in_gate:
        diff = row["comparisons"]["arm_n_different_mtime"]
        total = diff["differing_bytes_total"]
        if total:
            share = diff["differing_bytes_other"] / total
            if share >= 0.25:
                g5.append({"package": row["package"], "non_timestamp_share": round(share, 4)})

    checks = {
        "G1_arm_n_patch_reaches_identity": {
            "needs": f">= {GATE_MIN} of {GATE_SOURCES} sources",
            "got": len(g1), "packages": g1},
        "G2_planted_defect_detected": {
            "needs": "every source the defect was planted on",
            "got": len(g2), "packages": g2},
        "G3_arm_h_bit_identical": {
            "needs": f">= {GATE_MIN} of {GATE_SOURCES} sources",
            "got": len(g3), "packages": g3},
        "G4_arm_n_residual_causes": {
            "needs": "fewer than 2 sources left with residual differences",
            "got": len(residual), "packages": residual},
        "G5_non_timestamp_share": {
            "needs": "no source with non-timestamp share at or above 0.25",
            "got": len(g5), "sources": g5},
    }
    if len(in_gate) < GATE_MIN:
        outcome = "inconclusive"
    elif len(residual) >= 2 or g5:
        outcome = "timestamps-not-first"
    elif len(g1) >= GATE_MIN and len(g2) == len(in_gate) and len(g3) >= GATE_MIN:
        outcome = "timestamps-first"
    else:
        outcome = "inconclusive"
    return {
        "verdict": outcome,
        "checks": checks,
        "gate_sources": [r["package"] for r in in_gate],
        "reported_beyond_the_gate": [r["package"] for r in ordered[GATE_SOURCES:]],
        "control_C3_expected": "identical: false on every planted source",
    }


def _version(module: str):
    try:
        import importlib

        return getattr(importlib.import_module(module), "__version__", None)
    except Exception:  # a missing builder detail must not fail the measurement
        return None


def _default(value):
    """Keep raw artifact bytes out of results.json; their hashes are recorded."""
    if isinstance(value, (bytes, bytearray)):
        return f"<{len(value)} bytes elided>"
    return str(value)


def main() -> int:
    if not os.path.exists(SOURCES_JSON):
        print("run fetch_sources.py first", file=sys.stderr)
        return 1
    with open(SOURCES_JSON, encoding="utf-8") as handle:
        sources = json.load(handle)["sources"]
    usable = [row for row in sources if "sha256" in row]
    workdir = tempfile.mkdtemp(prefix="e3-attr-")
    results = {
        "experiment": "E3 build-timestamp attribution",
        "task": "T-0017",
        "mechanism_source": "RESEARCH/E.md, mechanism E3",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python": sys.version.split()[0],
            "platform": sys.platform,
            "builder": "python3 setup.py bdist_wheel",
            "setuptools": _version("setuptools"),
            "wheel": _version("wheel"),
        },
        "stamps": {"checkout_a": builds.STAMP_A, "checkout_b": builds.STAMP_B,
                   "arm_h_source_date_epoch": builds.EPOCH_H},
        "gate_denominator": GATE_SOURCES,
        "order": [row["package"] for row in usable],
        "sources": [],
    }
    try:
        for source in usable:
            row = builds.run_source(source, workdir, SDIST_DIR)
            results["sources"].append(row)
            pair = row["comparisons"].get("arm_n_different_mtime", {})
            print(
                f"{row['package']:10s} built={row['built_ok']!s:5s} "
                f"n_diff={pair.get('differing_bytes_total')} "
                f"ts={pair.get('differing_bytes_in_timestamp_fields')} "
                f"other={pair.get('differing_bytes_other')} "
                f"patch_identical={pair.get('patch_identical')}"
            )
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    results["gate"] = verdict(results)
    with open(RESULTS, "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2, sort_keys=True, default=_default)
        handle.write("\n")
    print(f"gate: {results['gate']['verdict']}")
    for name, check in results["gate"]["checks"].items():
        print(f"  {name}: got {check['got']}, needs {check['needs']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
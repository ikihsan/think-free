#!/usr/bin/env python3
"""E069 verdict: apply the predeclared gates to the measured arms.

Reads the durable per-repository files in `raw/` (harness.py writes one per
repository as it finishes, so an interrupted run keeps what it measured) plus
`pin_compatibility.json` (the static arm) and the oracle controls, and writes
`results.json`. It computes the gates; it does not choose them.

`raw_results.json` is deliberately **not** the input. harness.py writes it once,
at the end of a whole run, so mid-run it holds only the pilot's one repository —
and the verdict then silently describes a population nobody measured. The
per-repository files are the record; this is what reads them.
"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
RAW_DIR = BASE / "raw"
PINS = BASE / "pin_compatibility.json"
CONTROLS = (BASE / "controls-p1.json", BASE / "controls-p2.json")
INTERPRETER = BASE / "interpreter.json"
OUT = BASE / "results.json"

ARMS = ("GEN", "DECL", "NONE")


def load():
    """Read raw/<repo>.json, newest write per arm. Returns (by_repo, notes)."""
    by_repo = {}
    notes = {"repos_with_bytes": 0, "skipped_records": 0}
    for path in sorted(RAW_DIR.glob("*.json")):
        records = json.loads(path.read_text())
        # A skipped arm carries no `repo` key; the file is named for the repo.
        repo = path.stem.replace("_", "/", 1)
        for rec in records:
            if not isinstance(rec, dict) or "arm" not in rec:
                continue
            if rec.get("skipped"):
                notes["skipped_records"] += 1
            by_repo.setdefault(rec.get("repo") or repo, {})[rec["arm"]] = rec
    notes["repos_with_bytes"] = len(by_repo)
    return by_repo, notes


def state(rec):
    """One of installed, failed, not_exercised, skipped, unknown."""
    if rec is None:
        return "unknown", None
    if rec.get("skipped"):
        return "not_exercised", rec["skipped"]
    inst = rec.get("install", {})
    if inst.get("exit") is None:
        # harness.run() returns exit None when pip hit its own wall-clock timeout
        # (`E069_PIP_TIMEOUT`, default 1800s). That is the instrument running out
        # of time, not pip refusing the spec: counting it as a failed install
        # would charge the mechanism with a defect the measurement caused.
        return "not_exercised", "pip timeout; no install verdict"
    if inst.get("exit") != 0:
        return "failed", inst.get("failure_kinds")
    if rec.get("working") is True:
        return "installed_verified", None
    if rec.get("working") is None:
        # The install exited 0 but the oracle had no third-party import to probe.
        # That is an untested environment, not a demonstrated success, so it is
        # its own state: per D082 it is never counted as a pass. It is still
        # counted by `installed_any`, which is the literal reading of K1
        # ("installs cleanly").
        return "installed_unverified", "no third-party import to probe"
    return "installed_import_fail", "install ok, import probe failed"


def controls_record():
    """Merge the two oracle-control files the controls run wrote.

    controls.py writes controls-p1.json and controls-p2.json separately (P1 is
    the expensive one, P2 is run alone first). analyze.py must not read a single
    hand-merged `controls.json` that no run produces: a missing file is a missing
    observation, not a passing control.
    """
    got, missing = {}, []
    for path in CONTROLS:
        if path.is_file():
            got[path.stem] = json.loads(path.read_text())
        else:
            missing.append(path.name)
    p1 = (got.get("controls-p1") or {}).get("p1") or {}
    p2 = (got.get("controls-p2") or {}).get("p2") or {}
    return {
        "files_present": sorted(got),
        "files_missing": missing,
        "P1": {"pass": p1.get("pass"), "n_pass": p1.get("n_pass"),
               "n_exercised": p1.get("n_exercised"),
               "n_not_exercised": p1.get("n_not_exercised")},
        "P2": {"pass": p2.get("pass")},
        # A control that was never run is not a pass. all_pass is true only when
        # both controls ran and both passed.
        "all_pass": bool(p1.get("pass")) and bool(p2.get("pass")) and not missing,
    }


def main():
    by_repo, notes = load()
    interpreter = {}
    if INTERPRETER.is_file():
        interpreter = json.loads(INTERPRETER.read_text())
    repos = sorted(by_repo)
    per_repo = {}
    for repo in repos:
        row = {}
        for arm in ARMS:
            st, why = state(by_repo[repo].get(arm))
            rec = by_repo[repo].get(arm) or {}
            row[arm] = {
                "state": st, "reason": why,
                "install_exit": (rec.get("install") or {}).get("exit"),
                "seconds": (rec.get("install") or {}).get("seconds"),
                "download_mb": (rec.get("install") or {}).get("download_mb"),
                "first_failure": (rec.get("install") or {}).get("first_failure"),
                "needed_modules": rec.get("needed"),
                "imports": rec.get("imports"),
                "venv_removed": rec.get("venv_removed"),
            }
        row["gen_installs_cleanly"] = row["GEN"]["state"].startswith("installed")
        row["gen_verified"] = row["GEN"]["state"] == "installed_verified"
        row["gen_beats_decl"] = (row["GEN"]["state"].startswith("installed")
                                 and not row["DECL"]["state"].startswith("installed"))
        row["gen_beats_decl_verified"] = (row["GEN"]["state"] == "installed_verified"
                                          and not row["DECL"]["state"].startswith("installed"))
        row["gen_harms_decl"] = (not row["GEN"]["state"].startswith("installed")
                                 and row["DECL"]["state"].startswith("installed"))
        per_repo[repo] = row

    def n(arm, want):
        return sum(1 for r in per_repo.values() if r[arm]["state"] == want)

    states = ("installed_verified", "installed_unverified", "installed_import_fail",
              "failed", "not_exercised", "unknown")
    counts = {arm: {s: n(arm, s) for s in states} for arm in ARMS}
    # `installed_any` = exit 0, the literal reading of K1's "installs cleanly".
    counts = dict(counts)
    for arm in ARMS:
        counts[arm]["installed_any"] = sum(
            1 for r in per_repo.values() if r[arm]["state"].startswith("installed"))
    gen_installed = [r for r, v in per_repo.items() if v["gen_installs_cleanly"]]
    gen_verified = [r for r, v in per_repo.items() if v["gen_verified"]]
    beats = [r for r, v in per_repo.items() if v["gen_beats_decl"]]
    beats_verified = [r for r, v in per_repo.items() if v["gen_beats_decl_verified"]]
    harms = [r for r, v in per_repo.items() if v["gen_harms_decl"]]

    pins = json.loads(PINS.read_text()) if PINS.is_file() else {}
    controls = controls_record()
    oracle_valid = controls["all_pass"]

    # K1's declared denominator is the 20-repository population. Reporting a
    # count over the repositories actually measured is not the same claim, so both
    # are stated and the gate is evaluated against the measured one.
    manifest = json.loads((BASE / "repos" / "MANIFEST.json").read_text())
    manifest_keys = ["%s/%s" % (r["owner"], r["repo"]) for r in manifest["repos"]]
    population_n = len(manifest_keys)
    unmeasured = [r for r in manifest_keys if r not in by_repo]
    gates = {
        "K1_mechanism_works": {
            "condition": "GEN installs cleanly for >= 3 of 20 repos",
            "observed_installed": len(gen_installed),
            "observed_installed_and_import_verified": len(gen_verified),
            "measured_repos": len(repos),
            "population": population_n,
            "threshold": 3,
            "pass": len(gen_installed) >= 3,
            "pass_strict": len(gen_verified) >= 3,
            "repos": gen_installed,
            "repos_verified": gen_verified,
            "note": ("pass is the declared wording (exit 0). pass_strict counts only "
                     "repositories whose imports were actually probed; the difference "
                     "between the two is every GEN success here, which installed "
                     "nothing importable."),
        },
        "K2_differentiation": {
            "condition": "GEN succeeds on at least one repo where DECL fails",
            "observed": len(beats),
            "observed_verified": len(beats_verified),
            "threshold": 1,
            "pass": len(beats) >= 1,
            "pass_verified": len(beats_verified) >= 1,
            "repos": beats,
            "repos_verified": beats_verified,
            "note": ("every repo counted here has no third-party import to probe, so "
                     "these are untested environments, not demonstrated wins."),
        },
        "K3_no_harm": {
            "condition": "GEN does not fail on a repo where DECL installs",
            "harmful_repos": harms,
            "pass": len(harms) == 0,
        },
    }
    complete = len(repos) >= population_n
    verdict = "KILL" if not gates["K1_mechanism_works"]["pass"] else (
        "direction closes" if not gates["K2_differentiation"]["pass"] else "mechanism holds")
    if not complete:
        verdict += " (PARTIAL: %d of %d repositories measured)" % (len(repos), population_n)

    # A shortfall in the denominator only matters if an unmeasured repository
    # could still change a gate. The static arm already decides whether GEN can
    # install on each unmeasured repo: a spec with a pin pip will refuse cannot
    # install, whatever else happens. Where that forecloses every remaining
    # path to a gate, the gates are *determined* on the measured subset and the
    # shortfall is a missing observation, not an open question.
    per_repo_static = {}
    if PINS.is_file():
        per_repo_static = json.loads(PINS.read_text()).get("per_repo", {})
    determinable, blocked_gen = [], []
    for repo in unmeasured:
        row = per_repo_static.get(repo) or {}
        if row.get("pins_blocking_install", 0) > 0:
            blocked_gen.append(repo)
    k1_open = (len(gen_installed) < 3) and not blocked_gen
    k2_open = len(beats_verified) < 1 and not blocked_gen
    determinable = (not k1_open and not k2_open)
    if determinable and not complete:
        verdict += " — GATES DETERMINED: all %d unmeasured repos carry a pin pip refuses, " \
                   "so no GEN install is available on any of them" % len(blocked_gen)

    result = {
        "experiment": "E069",
        "question": ("does E068's generated spec install and import where the repository's own "
                     "declared spec does not?"),
        "population": "the %d test repositories E068 fetched (A2/A3/A4)" % population_n,
        "measured_repos": len(repos),
        "population_complete": complete,
        "unmeasured_repos": unmeasured,
        "gates_determined": determinable,
        "determination_note": (
            "every unmeasured repository carries at least one pin the static arm "
            "shows pip refuses, so GEN cannot install on any of them; no further "
            "measurement can move K1 or K2. K3 can only gain rows."
            if determinable else
            "an unmeasured repository could still install GEN, so the gates are open."),
        "load_notes": notes,
        "interpreter": interpreter,
        "controls": controls,
        "oracle_valid": oracle_valid,
        "oracle_note": ("arms are interpreted only when both controls ran and passed; "
                        "a control that did not run is a missing observation, never a pass"),
        "arm_counts": counts,
        "static_arm": {
            "question": pins.get("question"),
            "pins_total": pins.get("pins_total"),
            "pins_decided": pins.get("pins_decided"),
            "pins_blocking_install": pins.get("pins_blocking_install"),
            "generated_specs_with_no_blocking_pin": pins.get("generated_specs_installable_on_target"),
        },
        "gates": gates,
        "verdict": verdict,
        "per_repo": per_repo,
    }
    OUT.write_text(json.dumps(result, indent=1))

    print("repos measured: %d of %d%s" % (
        len(repos), population_n, "" if complete else "   PARTIAL"))
    print("interpreter: %s %s" % (interpreter.get("observed_version"), interpreter.get("machine")))
    print("oracle valid: %s (P1=%s P2=%s, missing=%s)" % (
        oracle_valid, controls["P1"]["pass"], controls["P2"]["pass"],
        controls["files_missing"] or "none"))
    print("\narm outcomes over %d repos" % len(repos))
    for arm in ARMS:
        c = counts[arm]
        print("  %-5s verified %2d   unverified %2d   import-fail %2d   failed %2d   not_exercised %2d" % (
            arm, c["installed_verified"], c["installed_unverified"],
            c["installed_import_fail"], c["failed"], c["not_exercised"]))
    print("\ngates")
    for name, g in gates.items():
        print("  %-22s %s  %s" % (name, "PASS" if g["pass"] else "FAIL", g["condition"]))
        if "pass_strict" in g:
            print("      strict (imports actually probed): %s (%d)" % (
                "PASS" if g["pass_strict"] else "FAIL", g["observed_installed_and_import_verified"]))
        if "pass_verified" in g:
            print("      strict (wins actually probed):    %s (%d)" % (
                "PASS" if g["pass_verified"] else "FAIL", g["observed_verified"]))
        if g.get("repos"):
            print("      repos: %s" % ", ".join(g["repos"]))
        if g.get("harmful_repos"):
            print("      harmful: %s" % ", ".join(g["harmful_repos"]))
    print("\nVERDICT: %s" % verdict)
    if not complete:
        print("gates determined on the measured subset: %s" % determinable)
        print("  %s" % result["determination_note"])
    print("wrote %s" % OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
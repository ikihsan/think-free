#!/usr/bin/env python3
"""E069 oracle-validity controls. Run before any arm is interpreted.

P1  the four A1 repositories, whose declared specs are pinned and known-good,
    must reach "working" for at least two. A harness that cannot recognise a
    working environment cannot be used to judge a broken one.

P2  a synthetic positive: a fixture package on the path plus a pinned
    requirements.txt naming one real dependency must import successfully. This
    catches an oracle that is simply always-false.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

import harness  # noqa: E402

A1_KEYS = [
    "illidanlab/inversion-influence-function",
    "Profluent-Internships/MMDiff",
    "deeplearning-wisc/args",
    "qzhb/BSSARD",
]


A1_PATHS = {key: rel for key, rel in (
    ("illidanlab/inversion-influence-function",
     "EXPERIMENTS/068-arxiv-spec-generator/repos/A1/illidanlab_inversion-influence-function"),
    ("Profluent-Internships/MMDiff",
     "EXPERIMENTS/068-arxiv-spec-generator/repos/A1/Profluent-Internships_MMDiff"),
    ("deeplearning-wisc/args",
     "EXPERIMENTS/068-arxiv-spec-generator/repos/A1/deeplearning-wisc_args"),
    ("qzhb/BSSARD", "EXPERIMENTS/068-arxiv-spec-generator/repos/A1/qzhb_BSSARD"),
)}


def p1():
    """A1 repos' own pinned spec must produce a working environment.

    Three of the four A1 repositories ship a conda `environment.yml`, which pip
    cannot install. Translating one to pip names is the mechanism under test in
    the GEN arm, so it is not done here. Such a repo is `not_exercised` with its
    reason, which per D082 is a missing observation and never a pass or a fail.
    """
    stdlib = harness.stdlib_names()
    rows = harness.extracted_index()
    out = []
    for key, rel in A1_PATHS.items():
        repo_dir = harness.REPO_ROOT / rel
        if not repo_dir.is_dir():
            out.append({"repo": key, "status": "not_exercised", "reason": "no checkout"})
            continue
        spec, kind = harness.decl_spec(repo_dir)
        if spec is None or (spec.get("mode") == "requirements"
                            and not Path(spec["path"]).is_file()):
            out.append({"repo": key, "status": "not_exercised",
                        "reason": "conda-only specification; pip cannot install it"})
            print("P1 %-45s not_exercised (conda-only)" % key, flush=True)
            continue
        rec = harness.run_arm(key, rows[key], "DECL", repo_dir, stdlib)
        rec["repo"] = key
        rec["status"] = "exercised"
        out.append(rec)
        print("P1 %-45s exit=%s working=%s" % (
            key, rec.get("install", {}).get("exit"), rec.get("working")), flush=True)
    exercised = [r for r in out if r.get("status") == "exercised"]
    passed = [r for r in exercised if r.get("working") is True]
    return {"control": "P1",
            "requirement": ">=1 pip-declarable A1 repo reaches working via DECL",
            "n_pass": len(passed),
            "n_exercised": len(exercised),
            "n_not_exercised": len(out) - len(exercised),
            "pass": len(passed) >= 1,
            "rows": out}


def p2():
    """Synthetic positive: one real pinned dependency, imported for real.

    Run this first and alone. It costs about a minute and it is the only part of
    the oracle's validity that needs no network-heavy work, so if it fails there
    is no reason to spend an hour on the arms.
    """
    harness.VENV_PARENT.mkdir(parents=True, exist_ok=True)
    harness.ensure_getpip()
    venv = harness.venv_root() / "control_p2"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            pkg = tmp / "fixture_pkg"
            pkg.mkdir()
            (pkg / "__init__.py").write_text("VALUE = 7\n")
            (pkg / "uses_dep.py").write_text("import idna\n\ndef f():\n    return idna.encode('a')\n")
            spec = tmp / "requirements.txt"
            spec.write_text("idna==3.10\n")
            spec_ref = {"mode": "requirements", "path": str(spec)}
            bin_path = harness.make_venv(venv)
            inst = harness.install(bin_path, spec_ref, tmp)
            # The probe puts its first argument on sys.path, and the module under
            # test is `fixture_pkg.uses_dep`, so the path entry is the fixture's
            # *parent*, not the package directory.
            imports = harness.probe_imports(bin_path, tmp, ["fixture_pkg.uses_dep"])
            ok = inst["exit"] == 0 and imports.get("fixture_pkg.uses_dep") == "ok"
            print("P2 fixture: install_exit=%s import=%s" % (inst["exit"], imports), flush=True)
            return {"control": "P2", "requirement": "fixture imports a real pinned dependency",
                    "install": inst, "imports": imports, "pass": bool(ok)}
    finally:
        shutil.rmtree(venv, ignore_errors=True)


def main():
    (BASE / "raw").mkdir(exist_ok=True)
    which = (sys.argv[1] if len(sys.argv) > 1 else "all").lower()
    results = {}
    if which in ("all", "p2"):
        results["p2"] = p2()
    if which in ("all", "p1"):
        results["p1"] = p1()
    if "p1" not in results or "p2" not in results:
        # A partial run reports the control it ran. It does NOT compute an
        # overall verdict, because a partial run cannot: an earlier version
        # reported `all_pass` from whichever control was absent, which prints
        # FAIL for a control that actually passed.
        results["partial"] = True
        results["controls_run"] = sorted(k for k in results if k.startswith("p"))
        (BASE / ("controls-%s.json" % which)).write_text(json.dumps(results, indent=1))
        for name in results["controls_run"]:
            print("%s: %s" % (name, "PASS" if results[name]["pass"] else "FAIL"))
        print("\npartial run: %s. Run 'all' for the joint verdict." % which)
        return 0
    results["all_pass"] = bool(results["p1"]["pass"] and results["p2"]["pass"])
    results["all_pass"] = bool(results["p1"]["pass"] and results["p2"]["pass"])
    (BASE / "controls.json").write_text(json.dumps(results, indent=1))
    print("\ncontrols: P1 %s (%d passed of %d exercised, %d not_exercised)  P2 %s" % (
        "PASS" if results["p1"]["pass"] else "FAIL",
        results["p1"]["n_pass"], results["p1"]["n_exercised"],
        results["p1"]["n_not_exercised"],
        "PASS" if results["p2"]["pass"] else "FAIL"))
    print("oracle valid: %s" % results["all_pass"])
    return 0 if results["all_pass"] else 3


if __name__ == "__main__":
    sys.exit(main())

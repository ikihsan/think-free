"""E085 baseline: run deptry 0.25.1 for real on the same repositories, with
nothing installed, and record what it can and cannot say.

This is the comparison declared in PROTOCOL.md's "What is compared against
what". deptry's own documentation says it "should be run within the root
directory of the project being scanned, and the project should be running in
its own dedicated virtual environment"; this run measures what that costs.

Standard library only. Writes deptry-baseline.json.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.normpath(os.path.join(HERE, "..", "068-arxiv-spec-generator", "repos"))
DEPTRY = "/tmp/opencode/deptry-venv/bin/deptry"
ANSI = re.compile(r"\x1b\[[0-9;]*m")
RULE = re.compile(r"\b(DEP00[1-5])\b")
MODULE = re.compile(r"'(?P<module>[A-Za-z0-9_.\-]+)'")


def clean(line):
    return ANSI.sub("", line).strip()


def run_one(path):
    try:
        proc = subprocess.run([DEPTRY, "."], cwd=path, capture_output=True,
                              text=True, timeout=300)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "could-not-run", "why": repr(exc)[:200], "findings": []}
    out = proc.stdout + proc.stderr
    findings, assumptions = [], []
    for line in out.splitlines():
        line = clean(line)
        if line.startswith("Assuming the corresponding module name"):
            assumptions.append(line)
        m = RULE.search(line)
        if not m:
            continue
        mod = MODULE.search(line)
        findings.append({
            "rule": m.group(1),
            "module": mod.group("module") if mod else None,
            "file": line.split(":")[0] if ":" in line else None,
            "text": line,
        })
    by_rule = {}
    for f in findings:
        by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1
    return {
        "status": "ran",
        "exit_code": proc.returncode,
        "findings": len(findings),
        "by_rule": by_rule,
        "distinct_modules_flagged": sorted({f["module"] for f in findings if f["module"]}),
        "module_name_assumptions": len(assumptions),
        "assumption_examples": assumptions[:3],
        "stderr_head": clean(proc.stderr)[:300],
    }


def main():
    if not os.path.exists(DEPTRY):
        print("deptry not installed at %s" % DEPTRY, file=sys.stderr)
        return 1
    scan = json.load(open(os.path.join(HERE, "repo-scan.json")))
    rows = []
    for r in scan["repos"]:
        if not (r["declared"] and r["imports"]):
            continue
        path = os.path.join(CORPUS, r["path"])
        res = run_one(path)
        res["repo"] = r["repo"]
        res["n_declared"] = len(r["declared"])
        res["n_import_sites"] = r["n_import_sites"]
        rows.append(res)
        print("%-45s %-8s findings=%-5s rules=%s" % (
            r["repo"], res["status"], res.get("findings"),
            ",".join("%s:%d" % kv for kv in sorted(res.get("by_rule", {}).items()))))
    out = {
        "deptry_version": subprocess.run([DEPTRY, "--version"], capture_output=True,
                                         text=True).stdout.strip(),
        "condition": "no virtualenv installed for any repository",
        "repos": rows,
    }
    with open(os.path.join(HERE, "deptry-baseline.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    tot = sum(r.get("findings", 0) for r in rows)
    print("\n%s | %d repos | %d findings total" % (out["deptry_version"], len(rows), tot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""Falsify T-0056's rule by mutation, in both directions, asserting each landed.

The lesson this file exists for is in `tests/README.md`: a mutation that does
not check it landed cannot fail anything, and looks exactly like a control that
held (T-0047, then T-0050 in the same subject). So every mutation below counts
its own pattern before writing, and the run is only meaningful if all of them
report `patched`.

    python3 tools/mutate_result_rule.py [--root REPO]

Each mutation removes one clause of `resultnumbers` and re-runs the test file.
The expected outcomes are opposite, which is the point: a rule that fires on the
defect proves it can fail, and only a rule that is silent on the repair proves it
can be satisfied. Both must be shown.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile

MUTATIONS = (
    (
        "declared-count restriction removed",
        "declared_counts",
        '    for key, value in data.items():\n'
        '        if COUNT_KEY.search(key) and isinstance(value, int) and not isinstance(value, bool):\n'
        '            counts.add(value)\n',
        "    for key, value in data.items():\n        counts.update(every_value({key: value}))\n",
        "expected: FAILS — the loose rule cannot see 113, which is the false negative",
    ),
    (
        "fraction clause removed",
        "row_issues",
        "    for numerator, denominator in FRACTION.findall(row):\n"
        "        if not stated(denominator, counts):\n",
        "    for numerator, denominator in []:\n        if not stated(denominator, counts):\n",
        "expected: FAILS — nothing reports the fraction, which is the defect's shape",
    ),
    (
        "artifact-unreadable report removed",
        "unreadable_issue",
        "            if isinstance(held, str):\n                found.append(unreadable_issue(slug, held))\n                continue\n",
        "            if isinstance(held, str):\n                continue\n",
        "expected: FAILS — a parser that stops matching would look like a clean tree",
    ),
)

CONTROL = (
    "no mutation",
    "expected: PASSES — the unmutated tree is the control the others are read against",
)


def mutate(path: pathlib.Path, needle: str, replacement: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if text.count(needle) != 1:
        print(f"    REFUSING: pattern matched {text.count(needle)} times, expected exactly 1")
        return False
    path.write_text(text.replace(needle, replacement), encoding="utf-8")
    return True


def run_suite(root: pathlib.Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_result_numbers"],
        cwd=str(root),
        capture_output=True,
        text=True,
        env={"PYTHONPATH": f"{root}/tools:{root}/tests", "PATH": "/usr/bin:/bin", "HOME": str(root)},
    )
    return result.returncode, (result.stderr or "")[-400:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=None, help="repository to copy (default: this one)")
    args = parser.parse_args()
    source = pathlib.Path(args.root).resolve() if args.root else pathlib.Path(__file__).resolve().parent.parent
    module_rel = pathlib.Path("tools/originlib/resultnumbers.py")

    scratch = pathlib.Path(tempfile.mkdtemp(prefix="origin-mutate-"))
    try:
        target = scratch / "repo"
        shutil.copytree(
            source,
            target,
            ignore=shutil.ignore_patterns(".git", ".worktrees", "__pycache__", ".origin"),
        )
        # The copy is committed as a fresh single-commit history, so the tests
        # that read a document out of `HEAD` see the tree as it is now — including
        # a repair that is not yet committed upstream. Copying the repository's
        # own history instead would leave those tests reading the pre-repair bytes,
        # and the control below would fail for a reason that has nothing to do with
        # the mutations.
        subprocess.run(["git", "init", "-q"], cwd=str(target), check=True)
        subprocess.run(["git", "add", "-A", "-f"], cwd=str(target), check=True)
        subprocess.run(
            ["git", "-c", "user.email=m@v.invalid", "-c", "user.name=m", "commit", "-qm", "base"],
            cwd=str(target),
            check=True,
        )

        code, _ = run_suite(target)
        print(f"{CONTROL[0]}: exit {code}  {CONTROL[1]}")
        if code != 0:
            print("    the control did not pass, so no mutation below means anything")
            return 1

        all_landed = True
        for name, where, needle, replacement, expectation in MUTATIONS:
            module = target / module_rel
            original = module.read_text(encoding="utf-8")
            landed = mutate(module, needle, replacement)
            print(f"{name}: {'patched' if landed else 'PATCH DID NOT LAND'}")
            if not landed:
                all_landed = False
                continue
            code, tail = run_suite(target)
            verdict = "FAILS (falsified)" if code != 0 else "PASSES (not falsified)"
            print(f"    exit {code}  {verdict}  {expectation}")
            if code == 0:
                all_landed = False
                for line in tail.strip().splitlines()[-3:]:
                    print(f"      {line}")
            module.write_text(original, encoding="utf-8")

        print("\nevery mutation landed and falsified" if all_landed else "\nINCONCLUSIVE — see above")
        return 0 if all_landed else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
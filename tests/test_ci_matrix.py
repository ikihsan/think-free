"""CI's Python matrix and the exercised-version record cannot drift apart.

`tests/python-versions.json` is the record of what the suite has actually run on,
and T-0033 made `doctor` read it. Two tests in `test_doctor_versions.py` then
read *this* repository's real record and assert things about the interpreter they
are running on — one of them asserts that the interpreter is recorded at all.
Neither of those can be satisfied on an interpreter the record does not name,
and nothing connected that dependency to the workflow: CI pinned one version, so
the question never arose.

That is the gap this file closes. A matrix row for a version with no recorded
scope does not merely leave a hole in the record: it turns two existing tests red
for a reason that has nothing to do with the code under test (F018). So the
coupling is made explicit and enforced in both directions — every row is
recorded, and nothing a row runs is still listed as never exercised.

The parsers are deliberately dumb and deliberately loud. A workflow whose shape
they do not recognise is a **failure**, not a pass: T-0030's decision-index check
matched no row in any of 174 commits and the sweep was green while half the rule
did nothing (F010 with extra steps). `test_unrecognised_shapes_fail_loudly`
holds that line.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

WORKFLOW = ".github/workflows/ci.yml"
PY_RECORD = "tests/python-versions.json"

# `python-version: ['3.8', '3.9', …]` — a single inline list, which is the only
# shape this file understands. Anything else has to be taught here first.
MATRIX = re.compile(r"python-version:\s*\[(?P<body>[^\]]*)\]")
GUARD = re.compile(r"if:\s*matrix\.python-version\s*==\s*'(?P<version>[^']+)'")
STEP = re.compile(r"^ {6}- name: (?P<name>.+)$", re.MULTILINE)
ANY_STEP = re.compile(r"^\s*- name: ", re.MULTILINE)
# Steps that legitimately run on every row: they report the row's own
# interpreter, and they are the thing the matrix exists to multiply.
ROW_WIDE = ("Show toolchain", "Tests")


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parent.parents]:
        if (parent / "tasks").is_dir() and (parent / "tools").is_dir():
            return parent
    raise AssertionError("could not locate the repository root")


def workflow_text() -> str:
    return (repo_root() / WORKFLOW).read_text(encoding="utf-8")


def matrix_versions(text: str) -> list[str]:
    """The `python-version` matrix, as written. Raises on an unknown shape."""
    match = MATRIX.search(text)
    if match is None:
        raise ValueError(f"no inline python-version matrix in {WORKFLOW}")
    body = match.group("body").strip()
    if not body:
        raise ValueError("the python-version matrix is empty")
    return [item.strip().strip("'\"") for item in body.split(",") if item.strip()]


def steps(text: str) -> list[tuple[str, str]]:
    """`(name, block)` for every step, in file order. Raises on a bad indent.

    A step at any other indent is refused rather than skipped. Skipping it would
    be the F010 shape exactly: the gate would pass over a gate it cannot see,
    and the report would say the steps are guarded when one of them never ran.
    """
    found = list(STEP.finditer(text))
    if len(found) != len(ANY_STEP.findall(text)):
        raise ValueError(
            f"expected every step at six-space indent; found {len(found)} of "
            f"{len(ANY_STEP.findall(text))}"
        )
    out = []
    for index, match in enumerate(found):
        end = found[index + 1].start() if index + 1 < len(found) else len(text)
        out.append((match.group("name").strip(), text[match.start():end]))
    return out


def guarded_version(block: str) -> str | None:
    """The single matrix version a step is guarded to, or `None` if unguarded."""
    guard = GUARD.search(block)
    return guard.group("version") if guard else None


def minor(version: str) -> str:
    parts = version.split(".")
    return ".".join(parts[:2]) if len(parts) >= 2 else version


def covered_minors(record: dict) -> set[str]:
    """Every minor version a `verified` entry can be read as covering.

    An entry names the version that ran, so the set is exactly the minors it
    lists. It is compared by minor because the record mixes a patch-level entry
    (`3.8.10`) with a minor-level one (`3.12`, CI's pin, whose patch the public
    API cannot report).
    """
    return {minor(str(entry["python"])) for entry in record["verified"]}


def unexercised_minors(gaps: list[dict]) -> tuple[set[str], list[str]]:
    """Minor versions a `not_exercised` range claims, and the ranges not read.

    Three forms are understood: `A through B`, `A and newer`, and a bare `A.x`.
    A span that **names a version** and matches none of them is returned as
    unreadable rather than resolved to nothing, because a gap this file cannot
    read is a gap nobody can say has been closed. A span that names no version at
    all — `any non-CPython implementation, or a non-Linux platform` — resolves to
    the empty set: it constrains no minor version, and that is a real answer
    rather than a failure to parse.
    """
    claimed: set[str] = set()
    unreadable: list[str] = []
    for gap in gaps:
        span = str(gap.get("range", ""))
        through = re.fullmatch(r"(\d+\.\d+)\s+through\s+(\d+\.\d+)", span)
        newer = re.fullmatch(r"(\d+\.\d+)\s+and newer", span)
        exact = re.fullmatch(r"(\d+\.\d+)", span)
        if through:
            start, end = int(through.group(1).split(".")[1]), int(through.group(2).split(".")[1])
            claimed.update(f"3.{minor}" for minor in range(start, end + 1))
        elif newer:
            claimed.add(newer.group(1))
        elif exact:
            claimed.add(exact.group(1))
        elif re.search(r"\d+\.\d+", span):
            unreadable.append(span)
    return claimed, unreadable


class WorkflowMatrixTest(unittest.TestCase):
    """The workflow itself: a matrix that exists, and gates that still run."""

    def test_the_workflow_declares_a_python_version_matrix(self) -> None:
        # One pinned version is what the record's own `not_exercised` clause
        # named as the reason 3.9 to 3.11 were never run. If the matrix is gone,
        # that gap is open again and this is the only thing that says so.
        versions = matrix_versions(workflow_text())
        self.assertGreater(len(versions), 1, f"expected a matrix, found {versions}")
        self.assertEqual(len(set(versions)), len(versions), f"duplicate row: {versions}")

    def test_a_failing_row_does_not_cancel_the_others(self) -> None:
        # With the default `fail-fast: true` one red row cancels the rest, so a
        # green run is not evidence that the cancelled versions ran at all —
        # which is the whole reason this repository keeps a per-version record.
        self.assertRegex(workflow_text(), r"fail-fast:\s*false")

    def test_every_other_gate_runs_on_exactly_one_row(self) -> None:
        # Both directions matter. An unguarded gate runs seven times, which is
        # waste nobody notices. A guard naming a version that is not in the
        # matrix runs **never**, and a gate that cannot run is a gate that cannot
        # fail (F010).
        text = workflow_text()
        rows = set(matrix_versions(text))
        seen = set()
        for name, block in steps(text):
            if name in ROW_WIDE:
                self.assertIsNone(guarded_version(block), f"{name} must run on every row")
                continue
            version = guarded_version(block)
            self.assertIsNotNone(version, f"{name} is unguarded: it would run on every row")
            self.assertIn(version, rows, f"{name} is guarded to {version}, which is not a row")
            seen.add(version)
        self.assertEqual(len(seen), 1, f"the gates are split across rows {sorted(seen)}")


class RecordAgreesWithTheMatrixTest(unittest.TestCase):
    """The coupling that makes `test_doctor_versions.py` valid on every row."""

    def setUp(self) -> None:
        self.record = json.loads((repo_root() / PY_RECORD).read_text(encoding="utf-8"))
        self.rows = matrix_versions(workflow_text())

    def test_every_matrix_row_has_a_recorded_scope(self) -> None:
        recorded = covered_minors(self.record)
        missing = [row for row in self.rows if minor(row) not in recorded]
        self.assertEqual(
            missing,
            [],
            f"matrix rows {missing} have no entry in {PY_RECORD}; a CI run on one of "
            "them makes test_doctor_versions.py red for a reason that is about the "
            "record, not the code (F018)",
        )

    def test_a_recorded_row_says_how_much_of_the_suite_it_ran(self) -> None:
        # `scope` is the whole reason an entry exists: a version that ran an
        # older suite is not evidence about the current one. A row added to the
        # matrix with a bare scope would put that back.
        for entry in self.record["verified"]:
            if minor(str(entry["python"])) not in {minor(row) for row in self.rows}:
                continue
            self.assertRegex(str(entry["scope"]), r"\d+ tests", entry)

    def test_nothing_a_row_runs_is_still_called_unexercised(self) -> None:
        claimed, unreadable = unexercised_minors(self.record["not_exercised"])
        self.assertEqual(
            unreadable,
            [],
            f"these ranges name no version, so nothing can say they were closed: {unreadable}",
        )
        overlap = sorted(claimed & {minor(row) for row in self.rows})
        self.assertEqual(
            overlap,
            [],
            f"{overlap} is in the matrix and in not_exercised: CI runs it every push",
        )

    def test_the_unexercised_list_still_names_what_is_not_run(self) -> None:
        # The other direction, and the one that keeps the clause honest. The
        # matrix cannot cover every implementation or platform, so an emptied
        # list would claim the fleet is complete.
        gaps = self.record["not_exercised"]
        self.assertTrue(gaps)
        claimed, _ = unexercised_minors(gaps)
        self.assertNotIn(max(covered_minors(self.record)), claimed)


class UnrecognisedShapeTest(unittest.TestCase):
    """A parser that cannot read the workflow must fail, not pass (F010)."""

    BASE = (
        "jobs:\n"
        "  verify:\n"
        "    strategy:\n"
        "      fail-fast: false\n"
        "      matrix:\n"
        "        python-version: ['3.8', '3.12']\n"
        "    steps:\n"
        "      - name: Show toolchain\n"
        "        run: python3 --version\n"
        "      - name: Tests\n"
        "        run: python3 -m unittest\n"
        "      - name: Documentation lint\n"
        "        if: matrix.python-version == '3.8'\n"
        "        run: tools/origin doc lint\n"
    )

    def test_the_baseline_shape_is_read(self) -> None:
        self.assertEqual(matrix_versions(self.BASE), ["3.8", "3.12"])
        self.assertEqual([name for name, _ in steps(self.BASE)][-1], "Documentation lint")

    def test_a_matrix_that_is_not_a_list_is_refused(self) -> None:
        # `include:`/`exclude:` or an expression the file cannot evaluate. An
        # unrecognised matrix must not read as "one version, nothing to check".
        with self.assertRaises(ValueError):
            matrix_versions("jobs:\n  verify:\n    strategy:\n      matrix:\n        python-version: ${{ fromJSON(x) }}\n")

    def test_a_step_at_the_wrong_indent_is_refused(self) -> None:
        # A step nested one level deeper would be invisible to the guard check,
        # and an invisible gate is a gate that cannot fail (F010).
        with self.assertRaises(ValueError):
            steps(self.BASE + "        - name: Stray\n          run: true\n")

    def test_an_unreadable_range_is_refused_rather_than_skipped(self) -> None:
        # It names 3.15 and says "or later", which is not one of the three forms
        # read above. Resolving that to nothing would let a gap close itself.
        claimed, unreadable = unexercised_minors([{"range": "3.15 or later"}])
        self.assertEqual(claimed, set())
        self.assertEqual(unreadable, ["3.15 or later"])

    def test_a_range_naming_no_version_constrains_nothing(self) -> None:
        # The other side of the same rule: this span is about implementations and
        # platforms, not minors. It is read, not skipped, and it resolves to
        # nothing — so it survives the gate and keeps the list non-empty.
        claimed, unreadable = unexercised_minors(
            [{"range": "any non-CPython implementation, or a non-Linux platform"}]
        )
        self.assertEqual((claimed, unreadable), (set(), []))

    def test_a_through_range_expands_to_every_minor_it_names(self) -> None:
        claimed, unreadable = unexercised_minors([{"range": "3.9 through 3.11"}])
        self.assertEqual(claimed, {"3.9", "3.10", "3.11"})
        self.assertEqual(unreadable, [])


if __name__ == "__main__":
    unittest.main()
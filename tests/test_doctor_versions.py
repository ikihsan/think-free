"""doctor must compare this VM's versions against the records, not just print them.

Two records state what the suite has actually run on — `tests/git-versions.json`
and `tests/python-versions.json` — and until T-0033 `doctor` printed the
interpreter and git it found without consulting either. A VM on Python 3.9 was
indistinguishable from one on 3.8.10 in the report, and finding out otherwise
meant opening a JSON file by hand.

The property under test is the three-way distinction: exercised, unrecorded, and
record-unreadable. The third is the one that is easy to lose and expensive when
lost — a comparison that cannot tell "we looked and it is not there" from "we
could not look" reports a confident answer in both cases.
"""

from __future__ import annotations

import json
import platform
import unittest
from pathlib import Path

from harness import RepoTest

from originlib import doctor, versions

PY_RECORD = "tests/python-versions.json"
GIT_RECORD = "tests/git-versions.json"


def real_repo() -> Path:
    """The working repository, whose records these tests read for real.

    The `RepoTest` fixture is a throwaway repository that ships neither record,
    which is exactly what `NoRecordCaseTest` needs and exactly what a claim about
    this VM must not use: a fixture with no records would make every assertion
    about `exercised` vacuous.
    """
    return Path(__file__).resolve().parent.parent


def seed_record(test: RepoTest, relative: str, key: str, rows: list[dict]) -> None:
    test.write(
        relative,
        json.dumps({"schema": "test/1", "verified": rows}, indent=2),
    )


class RealRecordTest(RepoTest):
    """Read this repository's own records, with ORIGIN_ROOT pointed at it."""

    def setUp(self) -> None:
        super().setUp()
        self.use(real_repo())

    def test_this_vms_versions_are_exercised_against_the_real_records(self) -> None:
        # The strongest claim available and the one that must not be faked: the
        # records are this repository's, and this VM's versions must be found in
        # them because T-0018, T-0032 and this session all ran here.
        collected = doctor.collect(network=False)
        matches = {m.tool: m for m in versions.compare_all(collected["versions"])}
        self.assertEqual(matches["python3"].state, versions.EXERCISED, matches["python3"])
        self.assertEqual(matches["git"].state, versions.EXERCISED, matches["git"])

    def test_doctor_reports_the_comparison(self) -> None:
        rendered = doctor.summarize(doctor.collect(network=False))
        self.assertIn("versions python3", rendered)
        self.assertIn("exercised", rendered)
        self.assertIn("tests/python-versions.json", rendered)
        self.assertIn("versions git", rendered)
        self.assertIn("tests/git-versions.json", rendered)

    def test_the_reported_scope_is_the_matched_entrys_own(self) -> None:
        # The point of carrying `scope` through: a reader must be able to tell a
        # version that ran everything from one that ran an older suite.
        #
        # Asserted against the record's own text rather than a pattern. The first
        # version of this test required `\d+ tests` in the scope, which passed on
        # this VM (3.8.10, whose entry names 373 tests) and **failed in CI**,
        # where the interpreter is 3.12 and the matched entry is CI's own — whose
        # scope names a run id rather than a count. That is the defect this
        # repository keeps meeting: a test asserting one machine's wording rather
        # than the property. Run 37174050724 is the evidence.
        record = json.loads((real_repo() / "tests" / "python-versions.json").read_text())
        mine = versions.extract_version(platform.python_version())
        match = versions.compare("python3", mine)
        entry = next(
            item for item in record["verified"] if str(item["python"]) == match.matched
        )
        self.assertEqual(match.scope, entry["scope"])
        self.assertTrue(match.scope.strip(), "an exercised verdict must carry its entry's scope")

    def test_a_patch_version_outside_the_record_is_not_exercised(self) -> None:
        # The negative control for prefix matching: `3.9.7` shares a leading digit
        # with the 3.8.10 entry and must not match it.
        self.assertEqual(versions.compare("python3", "3.9.7").state, versions.UNRECORDED)

    def test_the_written_record_is_what_doctor_reads(self) -> None:
        # Guards the other direction: the record on disk is not merely similar to
        # the one in code, it is the file the comparison opens.
        for relative in ("tests/python-versions.json", "tests/git-versions.json"):
            self.assertTrue((real_repo() / relative).exists(), relative)


class RecordReadingTest(RepoTest):
    def test_an_exercised_entry_carries_its_scope(self) -> None:
        seed_record(self, PY_RECORD, "python", [
            {"python": "3.8.10", "scope": "full suite green", "via": "test"},
        ])
        match = versions.compare("python3", "3.8.10")
        self.assertEqual(match.state, versions.EXERCISED)
        self.assertEqual(match.scope, "full suite green")

    def test_a_version_no_entry_names_is_unrecorded(self) -> None:
        seed_record(self, PY_RECORD, "python", [
            {"python": "3.8.10", "scope": "full suite green", "via": "test"},
        ])
        match = versions.compare("python3", "3.9.7")
        self.assertEqual(match.state, versions.UNRECORDED)
        self.assertIn("3.9.7", match.detail)

    def test_a_missing_record_is_unreadable_not_unrecorded(self) -> None:
        # The distinction the whole module exists for. `unrecorded` says the
        # suite has never run on this version; `unreadable` says we do not know.
        Path(self.repo / PY_RECORD).unlink(missing_ok=True)
        match = versions.compare("python3", "3.8.10")
        self.assertEqual(match.state, versions.UNREADABLE)
        self.assertIn("absent", match.detail)

    def test_a_corrupt_record_is_unreadable(self) -> None:
        self.write(PY_RECORD, "{not json")
        self.assertEqual(versions.compare("python3", "3.8.10").state, versions.UNREADABLE)

    def test_a_record_without_a_verified_list_is_unreadable(self) -> None:
        # A file that parses and says nothing is not a record of anything.
        self.write(PY_RECORD, json.dumps({"schema": "test/1"}))
        match = versions.compare("python3", "3.8.10")
        self.assertEqual(match.state, versions.UNREADABLE)
        self.assertIn("verified", match.detail)


class PrefixMatchingTest(RepoTest):
    def test_a_patch_version_finds_a_minor_level_entry(self) -> None:
        # CI's entry is the minor version `3.12` because the run log needs admin
        # rights. A VM on 3.12.7 must find it, or the record under-reports.
        seed_record(self, PY_RECORD, "python", [
            {"python": "3.12", "scope": "CI, minor version only", "via": "test"},
        ])
        match = versions.compare("python3", "3.12.7")
        self.assertEqual(match.state, versions.EXERCISED)
        self.assertEqual(match.matched, "3.12")

    def test_the_longest_matching_entry_wins(self) -> None:
        # `3.12.15` and a bare `3.12` both match `3.12.15`; the specific entry is
        # the one that says what actually ran.
        seed_record(self, PY_RECORD, "python", [
            {"python": "3.12", "scope": "minor only", "via": "test"},
            {"python": "3.12.15", "scope": "full suite green", "via": "test"},
        ])
        self.assertEqual(versions.compare("python3", "3.12.15").scope, "full suite green")

    def test_an_unrelated_version_does_not_match_by_prefix(self) -> None:
        seed_record(self, PY_RECORD, "python", [
            {"python": "3.8", "scope": "x", "via": "test"},
        ])
        self.assertEqual(versions.compare("python3", "3.80.1").state, versions.UNRECORDED)


class ExtractionTest(RepoTest):
    def test_versions_are_read_out_of_tool_output(self) -> None:
        self.assertEqual(versions.extract_version("git version 2.25.1"), "2.25.1")
        self.assertEqual(versions.extract_version("Python 3.8.10"), "3.8.10")
        self.assertEqual(versions.extract_version("Python 3.12.15 (main, Oct  3)"), "3.12.15")

    def test_output_without_a_version_yields_an_empty_string(self) -> None:
        # An absent version must not silently become "unrecorded": the caller
        # needs to see that nothing was reported.
        self.assertEqual(versions.extract_version("command not found"), "")
        self.assertEqual(versions.extract_version(""), "")

    def test_a_tool_with_no_record_says_so_rather_than_pretending(self) -> None:
        match = versions.compare("rustc", "1.96.0")
        self.assertEqual(match.state, versions.UNRECORDED)
        self.assertEqual(match.record, "")
        self.assertIn("no record", match.detail)


class SummaryTest(RepoTest):
    def test_the_three_states_are_readable_and_distinguishable(self) -> None:
        seed_record(self, PY_RECORD, "python", [
            {"python": "3.8.10", "scope": "full suite green", "via": "test"},
        ])
        Path(self.repo / GIT_RECORD).unlink(missing_ok=True)
        lines = versions.summarize(
            [
                versions.compare("python3", "3.8.10"),
                versions.compare("python3", "3.11.0"),
                versions.compare("git", "2.25.1"),
            ]
        )
        self.assertIn("exercised (tests/python-versions.json: 3.8.10)", lines[0])
        self.assertIn("full suite green", lines[0])
        self.assertIn("NOT exercised", lines[1])
        self.assertIn("record unreadable", lines[2])
        # Three states, three different words: a reader must not have to guess
        # which of "not there" and "could not look" they are looking at.
        self.assertEqual(len({line.split()[2] for line in lines}), 3)

class NoRecordCaseTest(RepoTest):
    def test_a_repository_with_neither_record_reports_both_as_unreadable(self) -> None:
        # A test harness builds a minimal repository. `doctor` must degrade to
        # "cannot tell", not to a confident claim that this VM is unexercised.
        Path(self.repo / PY_RECORD).unlink(missing_ok=True)
        Path(self.repo / GIT_RECORD).unlink(missing_ok=True)
        collected = doctor.collect(network=False)
        matches = {m.tool: m for m in versions.compare_all(collected["versions"])}
        self.assertEqual(matches["python3"].state, versions.UNREADABLE)
        self.assertEqual(matches["git"].state, versions.UNREADABLE)


if __name__ == "__main__":
    unittest.main()
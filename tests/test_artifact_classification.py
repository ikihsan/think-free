#!/usr/bin/env python3
"""Falsification cases for 017's classifier, written before the population was
classified.

`docs/policy/gate-falsification.md` asks for a gate to be falsified against the
defect's own bytes in both directions. The direction that matters here is fixed by
the hypothesis: H1 predicts the young arm is *mostly documents*, so every failure
mode that inflates `executable` flatters the hypothesis' negation, and every
failure mode that turns a readable row into `unreadable` quietly shrinks the
denominator the gate is computed on. Both directions are asserted below.

Three cases exist because they are the ones that actually bite:

  * an unreadable row must not read as a `document`. `document`'s whole claim is
    that the repository exists and is prose, so an instrument that cannot open a
    repository must never land in that class. 015's first run made the mirror
    mistake -- a repository publishing nothing was counted as a decided reading of
    zero use -- and called the correction out by name.
  * `classify_as_first_declared` must disagree with `classify` on a known row. A
    declared correction that changes nothing is a comment, not a correction.
  * a repository with a manifest and no releases, and one with releases and no
    manifest, must both be `executable`. "Ships a binary and keeps no manifest" is
    a real class; F032's `thought-machine/please` is its example.

Run: python3 -m unittest discover -s tests -p 'test_artifact_classification.py'
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir,
    "EXPERIMENTS", "017-incumbent-artifact-type"))

import classification  # noqa: E402


def entry(names, releases=0, type_="file"):
    return {"contents": [{"name": n, "type": type_} for n in names],
            "releases": releases}


class KnownAnswerTest(unittest.TestCase):
    def test_every_declared_case(self):
        for label, cached, expected in classification.KNOWN_ANSWER:
            self.assertEqual(classification.classify(cached)["class"], expected,
                             msg=label)

    def test_selfcheck_passes(self):
        self.assertTrue(classification.run_selfcheck())


class UnreadableIsNeverDocumentTest(unittest.TestCase):
    def test_refused_listing(self):
        out = classification.classify({"contents": classification.REFUSED,
                                       "releases": None})
        self.assertEqual(out["class"], "unreadable")
        self.assertEqual(out["reason"], "refused")

    def test_empty_repository(self):
        out = classification.classify({"contents": classification.EMPTY,
                                       "releases": 0})
        self.assertEqual(out["class"], "unreadable")
        self.assertEqual(out["reason"], classification.EMPTY)

    def test_unfetched_row(self):
        out = classification.classify({})
        self.assertEqual(out["class"], "unreadable")
        self.assertEqual(out["reason"], "not_fetched")

    def test_missing_file_does_not_raise(self):
        """`rootlisting.fetch` writes `contents: null` for a row it never reached."""
        self.assertEqual(classification.classify({"contents": None})["class"],
                         "unreadable")

    def test_unreadable_carries_no_evidence_claims(self):
        out = classification.classify({"contents": classification.REFUSED})
        self.assertEqual(out["hits"], [])
        self.assertIsNone(out["releases"])


class CorrectionChangesAnAnswerTest(unittest.TestCase):
    def test_index_html_is_a_document_after_the_correction(self):
        web = entry(["index.html"])
        self.assertEqual(classification.classify(web)["class"], "document")

    def test_and_was_not_before_it(self):
        web = entry(["index.html"])
        self.assertEqual(classification.classify_as_first_declared(web)["class"],
                         "executable")

    def test_the_correction_does_not_reclassify_a_source_entry(self):
        for name in ("cli.py", "main.go", "server.ts", "index.js"):
            row = entry([name])
            self.assertEqual(classification.classify(row)["class"], "executable",
                             msg=name)
            self.assertEqual(
                classification.classify_as_first_declared(row)["class"],
                "executable", msg=name)

    def test_correction_is_declared_in_the_module(self):
        self.assertIn("index.html", classification.DECLARED_CORRECTION)


class TwoRoutesToExecutableTest(unittest.TestCase):
    def test_manifest_without_releases(self):
        self.assertEqual(
            classification.classify(entry(["pyproject.toml"]))["class"],
            "executable")

    def test_releases_without_manifest(self):
        out = classification.classify(
            entry(["BUILD.bazel", "src"], releases=12))
        self.assertEqual(out["class"], "executable")
        self.assertEqual(out["hits"], [])
        self.assertEqual(out["releases"], 12)

    def test_refused_release_count_does_not_make_a_document_executable(self):
        """The releases channel declining is not evidence of a release."""
        out = classification.classify({"contents": [{"name": "README.md",
                                                     "type": "file"}],
                                       "releases": classification.REFUSED})
        self.assertEqual(out["class"], "document")
        self.assertIsNone(out["releases"])

    def test_contents_only_reading_is_reported(self):
        out = classification.classify(entry(["main.go"], releases=4),
                                      releases_include=False)
        self.assertEqual(out["class"], "executable")
        self.assertEqual(out["class_contents_only"], "executable")

    def test_contents_only_reading_differs_when_it_should(self):
        """`releases_include=False` must read contents alone, in both directions."""
        ships_a_release = entry(["Brewfile"], releases=9)
        with_releases = classification.classify(ships_a_release)
        without = classification.classify(ships_a_release, releases_include=False)
        self.assertEqual(with_releases["class"], "executable")
        self.assertEqual(without["class"], "document")
        self.assertEqual(without["class_contents_only"], "document")
        self.assertEqual(without["releases"], 9, msg="the reading is still recorded")


class MarkerMatchingTest(unittest.TestCase):
    def test_markers_are_case_insensitive(self):
        self.assertEqual(classification.classify(entry(["Dockerfile"]))["class"],
                         "executable")
        self.assertEqual(classification.classify(entry(["PACKAGE.JSON"]))["class"],
                         "executable")

    def test_a_bare_stem_without_a_suffix_is_not_a_marker(self):
        self.assertEqual(classification.classify(entry(["cli"]))["class"],
                         "document")

    def test_a_nested_path_is_matched_on_its_name(self):
        row = {"contents": [{"name": "requirements.txt", "type": "file",
                             "path": "backend/requirements.txt"}],
               "releases": 0}
        self.assertEqual(classification.classify(row)["class"], "executable")

    def test_an_unnamed_entry_is_skipped_not_fatal(self):
        row = {"contents": [{"type": "file"}, {"name": None}],
               "releases": 0}
        self.assertEqual(classification.classify(row)["class"], "document")

    def test_unexpected_shape_is_unreadable_not_document(self):
        out = classification.classify({"contents": {"message": "rate limited"},
                                       "releases": 0})
        self.assertEqual(out["class"], "unreadable")
        self.assertEqual(out["reason"], "unexpected_shape")


class UniqueModuleNameTest(unittest.TestCase):
    def test_no_other_experiment_owns_this_module_name(self):
        """Defect 24: two modules of one name in an interpreter means the second
        import is silently shadowed and every test file passes alone."""
        import glob
        import shutil
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            os.pardir, "EXPERIMENTS")
        owners = glob.glob(os.path.join(root, "*", "classification.py"))
        self.assertEqual(len(owners), 1, msg=owners)


if __name__ == "__main__":
    unittest.main()
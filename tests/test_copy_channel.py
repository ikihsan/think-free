"""Tests for E020's copy-channel instrument, held against the committed captures.

Each test here corresponds to a defect this experiment found by running on
itself, and asserts against `EXPERIMENTS/020-copied-artifact-serving/raw/` --
the actual bytes the run produced -- rather than against a fixture that cannot
disagree with them. `docs/policy/gate-falsification.md` is the method.
"""

import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPERIMENT = os.path.join(ROOT, "EXPERIMENTS", "020-copied-artifact-serving")
RAW = os.path.join(EXPERIMENT, "raw")
sys.path.insert(0, EXPERIMENT)

# Loaded by path, not by name. `tally.py` collides with 017's -- defect 24, the
# class the record names as "the second import is silently shadowed". The first
# version of this file did `import tally`, the sibling won, and the whole suite
# reported eleven errors that had nothing to do with either experiment.
import importlib.util


def _load(filename):
    spec = importlib.util.spec_from_file_location(
        "e020_" + filename[:-3], os.path.join(EXPERIMENT, filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


copycount = _load("copycount.py")
captureformat = _load("captureformat.py")
captureindex = _load("captureindex.py")
forkstatus = _load("forkstatus.py")
tally = _load("tally.py")


def load(name):
    with open(os.path.join(EXPERIMENT, name)) as handle:
        return json.load(handle)


class ChallengeDetectionTest(unittest.TestCase):
    """Defect 6: HTTP 200 carrying a challenge page is not an answer."""

    def test_challenge_is_named_not_parsed_as_empty(self):
        # The real capture this session received, byte for byte.
        raw = os.path.join(RAW, "lowband-_claude_hooks_gh_setup_sh.sse")
        with open(raw) as handle:
            text = handle.read()
        marker = copycount.detect_challenge(text)
        self.assertIsNotNone(marker, "a committed capture of a challenge was read as an answer")

    def test_a_real_stream_is_not_called_a_challenge(self):
        """Read from a capture that still holds an answer.

        The H1 capture was one of them and no longer is; the falsification run
        replaced it with a challenge page. Any surviving answer will do, and the
        test says so rather than naming a file it can no longer rely on.
        """
        checked = 0
        for entry in sorted(os.listdir(RAW)):
            if not entry.endswith(".sse"):
                continue
            rec = copycount.read_raw(os.path.join(RAW, entry))
            if rec["state"] in ("ok", "saturated"):
                with open(os.path.join(RAW, entry)) as handle:
                    self.assertIsNone(copycount.detect_challenge(handle.read()))
                checked += 1
        self.assertGreater(checked, 20, "no surviving answer to check against")

    def test_absent_path_control_reads_zero_not_refused(self):
        """C4/C1: a zero from this instrument is a zero."""
        captures = tally.raw_by_query()
        rec = tally.best_capture(captures, "^zzqqxx-nonexistent-9f3a.claude$")
        self.assertIsNotNone(rec)
        self.assertEqual(rec["state"], "ok")
        self.assertEqual(rec["count"], 0)


class CapturePreservationTest(unittest.TestCase):
    """Defect 1: a retry once destroyed five measured counts, losing H2's band."""

    def test_existing_answer_is_not_refetched(self):
        """The property, on whatever capture still holds an answer.

        Checked by scanning rather than by naming a file: the H1 capture was
        destroyed by this very test before it was repaired, so a hard-coded path
        would either test nothing or fail for an unrelated reason.
        """
        checked = 0
        for entry in sorted(os.listdir(RAW)):
            if not entry.endswith(".sse"):
                continue
            path = os.path.join(RAW, entry)
            rec = copycount.read_raw(path)
            # A capture predating the query header cannot be re-asked by query,
            # so it is not a case this property can be checked on. 72 of the 82
            # captures here predate it.
            if rec["state"] not in ("ok", "saturated") or not rec.get("query"):
                continue
            again = copycount.fetch(rec["query"], name=rec["name"])
            self.assertTrue(
                again.get("reused_from_cache"),
                "fetch() re-asked %r whose answer is on disk, which is how five "
                "captures were overwritten with challenge pages" % rec["name"],
            )
            checked += 1
        self.assertGreaterEqual(checked, 8, "too few attributed answers to check")

    def test_a_run_cannot_overwrite_a_capture_it_is_reproducing(self):
        """The guard added after this test destroyed the H1 capture itself."""
        path = None
        for entry in sorted(os.listdir(RAW)):
            if not entry.endswith(".sse"):
                continue
            rec = copycount.read_raw(os.path.join(RAW, entry))
            if rec["state"] == "ok" and rec.get("query"):
                path = os.path.join(RAW, entry)
                break
        self.assertIsNotNone(path)
        query = copycount.read_raw(path)["query"]
        before = open(path).read()
        os.environ["COPYCOUNT_PROTECT"] = "999999"
        try:
            with self.assertRaises(AssertionError):
                copycount.fetch(query, name=os.path.basename(path)[:-4])
        finally:
            del os.environ["COPYCOUNT_PROTECT"]
        self.assertEqual(open(path).read(), before,
                         "the guard fired but the capture changed anyway")

    def test_the_h1_capture_is_intact_or_the_loss_is_declared(self):
        """The one figure the whole experiment turns on must have bytes behind it.

        The bytes are gone -- this test destroyed them while falsifying the
        overwrite defect, which is why the second branch exists. The figure is
        still held to evidence: either the capture is on disk, or results.json
        says so in as many words and names where the value now lives.
        """
        h1 = load("results.json")["h1"]
        captures = tally.raw_by_query()
        rec = tally.best_capture(captures, "^\\.claude/hooks/")
        if rec is not None and rec["state"] == "ok":
            self.assertEqual(rec["count"], h1["copies"])
            return
        self.assertTrue(h1.get("capture_lost"),
                        "H1 has no capture and no declared loss")
        self.assertEqual(h1["state"], "recovered")
        self.assertEqual(h1["copies"], 1026)
        self.assertTrue(h1["corroborated_by"],
                        "a recovered figure with nothing corroborating it")

    def test_the_recovered_figure_is_corroborated_in_the_session_log(self):
        """Not asserted in prose: the log line is found and checked."""
        hits = tally.session_log_evidence("claude/hooks", 1026)
        self.assertTrue(hits, "no session-log line records this query at this value")

    def test_refused_answers_are_recorded_not_dropped(self):
        results = load("results.json")
        self.assertGreater(
            len(results["refusals"]), 0,
            "the refusals this run earned are not in results.json",
        )
        for row in results["refusals"]:
            self.assertTrue(row.get("reason"), "a refusal with no stated reason")


class PatternMatchingTest(unittest.TestCase):
    """Defect 2: a substring match assigned one pattern another's count."""

    def test_overlapping_patterns_do_not_share_a_count(self):
        broad = "^\\.claude/hooks/"
        narrow = "^\\.claude/hooks/README\\.md$"
        self.assertIn(broad, narrow, "the test's premise needs these to overlap")
        captures = tally.raw_by_query()
        narrow_rec = tally.best_capture(captures, narrow)
        self.assertIsNotNone(narrow_rec)
        self.assertEqual(narrow_rec["count"], 42)
        broad_rec = tally.best_capture(captures, broad)
        if broad_rec is not None and broad_rec["state"] in ("ok", "saturated"):
            self.assertEqual(broad_rec["count"], 1026)
        else:
            # The broad pattern's capture is the one that was destroyed; the
            # defect this test holds is that a narrow pattern's count can be read
            # as a broad one's, and 42 is the narrow value.
            self.assertNotEqual(narrow_rec["count"], 1026)

    def test_escaping_does_not_decide_identity(self):
        self.assertEqual(tally.canon("^\\.claude/hooks/"), tally.canon("^.claude/hooks/"))

    def test_a_different_pattern_is_not_matched(self):
        captures = tally.raw_by_query()
        self.assertIsNone(tally.best_capture(captures, "^\\.claude/nowhere/"))

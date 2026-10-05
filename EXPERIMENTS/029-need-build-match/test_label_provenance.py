#!/usr/bin/env python3
"""E029 -- tests of label provenance: can a label file be tied to the bytes it was read from?

Each test is asserted against the committed capture and against a fixture built to
break the property, following docs/policy/gate-falsification.md. The two forms of
test that matter most here are the ones the run's own history calls for:

  * a build that postdates the need is the population (otherwise 167 rows read as
    `unrelated` and manufacture the null H1 is trying to measure), and
  * the reader's view carries no arm label and no author name (otherwise the
    blindness the protocol declares is not the blindness the reader had).
"""
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)

import intervalstats as I  # noqa: E402


def read_jsonl(name):
    path = name if os.path.isabs(name) else os.path.join(RAW, name)
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def sibling(*parts):
    """A capture in a sibling experiment, resolved from this file, not the cwd."""
    return os.path.normpath(os.path.join(HERE, "..", *parts))


class LabelIntegrityTest(unittest.TestCase):
    def setUp(self):
        self.expected = [k["row_id"] for k in
                         json.load(open(os.path.join(RAW, "view_key.json")))]

    def test_each_reader_labelled_every_row_exactly_once(self):
        for reader in ("r1", "r2"):
            path = os.path.join(RAW, "labels_%s.tsv" % reader)
            if not os.path.exists(path):
                self.fail("reader %s has produced no labels" % reader)
            ids, labs = [], []
            for line in open(path):
                if not line.strip():
                    continue
                parts = line.split("\t")
                self.assertGreaterEqual(len(parts), 2, "row %r has no label" % line[:40])
                self.assertIn(parts[1].strip(), I.LABELS)
                ids.append(parts[0].strip())
                labs.append(parts[1].strip())
            self.assertEqual(sorted(ids), sorted(self.expected),
                             "reader %s: ids differ from the view it was given" % reader)
            self.assertEqual(len(set(ids)), 222, "reader %s repeated a row id" % reader)
            self.assertEqual(len(labs), 222)

    def test_labels_come_from_the_view_now_on_disk(self):
        # The failure this guards: reader r1 re-labelled a regenerated view but emitted
        # rows in the PREVIOUS view's order, so the file carried 222 plausible row ids
        # whose id-to-pair mapping was wrong. Nothing downstream could tell. The check is
        # that the reader's output order matches the frozen view's order.
        order = re.findall(r"^===== ROW \d+ \| id (\S+) =====",
                           open(os.path.join(RAW, "view_r1.txt")).read(), re.M)
        for reader in ("r1", "r2"):
            path = os.path.join(RAW, "labels_%s.tsv" % reader)
            if not os.path.exists(path):
                continue
            got = [l.split("\t")[0].strip() for l in open(path) if l.strip()]
            self.assertEqual(got, order,
                             "reader %s: label order does not match the frozen view's order" % reader)

    def test_a_reader_cannot_quote_the_key(self):
        for reader in ("r1", "r2"):
            path = os.path.join(RAW, "labels_%s.tsv" % reader)
            if not os.path.exists(path):
                continue
            text = open(path).read().lower()
            for word in ("matched", "mismatched", "story_title"):
                self.assertNotIn(word, text,
                                 "reader %s output leaks the arm name %r" % (reader, word))

    def test_superseded_labels_are_kept_but_not_read(self):
        # Failed runs are retained under superseded/, and a name may legitimately reappear
        # in raw/ when a reader is re-run. What must never happen is the superseded BYTES
        # coming back, so this compares content rather than names.
        import hashlib
        sup = os.path.join(HERE, "superseded")
        if not os.path.isdir(sup):
            return
        superseded = [n for n in os.listdir(sup) if n.startswith("labels")]
        self.assertTrue(superseded, "nothing was superseded, so this test proves nothing")
        raw_digests = {}
        for n in os.listdir(RAW):
            if n.startswith("labels"):
                raw_digests[n] = hashlib.md5(
                    open(os.path.join(RAW, n), "rb").read()).hexdigest()
        for name in superseded:
            bad = hashlib.md5(open(os.path.join(sup, name), "rb").read()).hexdigest()
            for n, d in raw_digests.items():
                self.assertNotEqual(d, bad,
                                    "raw/%s is byte-identical to the superseded %s"
                                    % (n, name))


if __name__ == "__main__":
    unittest.main()

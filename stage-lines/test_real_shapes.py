#!/usr/bin/env python3
"""stg on the shapes E046 found broken in real repositories: new files, a
coordinate that names two changes, and a file with no newline at the end.

Split out of `test_stage.py` at the 300-line cap and by origin: every test here
was written because a real commit from this repository, `psf/requests` or
`jqlang/jq` broke the tool in the way the name says. Read
`EXPERIMENTS/046-real-changes/README.md` for the measurements behind each.

Run with:  python3 -m unittest discover -s stage-lines -p 'test_*.py'
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tests_support import Repo, git                              # noqa: E402,F401


class RealShapesTest(unittest.TestCase):
    """Every test here has a real commit behind it."""

    def setUp(self):
        self.r = Repo()
        self.addCleanup(self.r.cleanup)


    # ------------------------------------------------- new files (E046 finding)

    def test_new_file_line_is_staged_after_intent_to_add(self):
        """A new file is the most common thing there is to stage part of.

        `git add -N` puts an empty index entry in place, and the file then shows
        up in `git diff -U0` as a whole-file addition. The rendered patch must
        edit that entry, not create the path: `git apply --cached` refuses
        `--- /dev/null` for a path the index already has, so before the fix every
        line of every new file exited 2 with "already exists in index".
        """
        self.r.write("seed", "x\n")
        self.r.commit()
        self.r.write("fresh", "one\ntwo\nthree\n")
        git(["add", "-N", "fresh"], self.r.dir)
        p = self.r.stg("stage", "fresh:2")
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertEqual(self.r.staged_file_content("fresh"), "two\n")

    def test_new_file_lines_stage_in_order_to_the_whole_file(self):
        """Each address stages exactly its own line, in any order asked for."""
        self.r.write("seed", "x\n")
        self.r.commit()
        self.r.write("fresh", "one\ntwo\nthree\n")
        git(["add", "-N", "fresh"], self.r.dir)
        self.assertEqual(self.r.stg("stage", "fresh:3").returncode, 1)
        self.assertEqual(self.r.staged_file_content("fresh"), "three\n")
        self.assertEqual(self.r.stg("stage", "fresh:1").returncode, 1)
        self.assertEqual(self.r.staged_file_content("fresh"), "one\nthree\n")
        self.assertEqual(self.r.stg("stage", "fresh:2").returncode, 1)
        self.assertEqual(self.r.staged_file_content("fresh"),
                         "one\ntwo\nthree\n")

    def test_new_file_without_intent_to_add_still_refused_loudly(self):
        """The fix must not make stg stage untracked files behind the caller.

        git has no index entry to edit, so the request is still refused, with the
        command that would make it possible named in the message.
        """
        self.r.write("seed", "x\n")
        self.r.commit()
        self.r.write("fresh", "one\ntwo\n")
        p = self.r.stg("stage", "fresh:1")
        self.assertEqual(p.returncode, 2)
        self.assertIn("no stage change", p.stderr)
        self.assertEqual(self.r.staged(), "")

    def test_new_file_split_all_reaches_the_whole_file(self):
        """`split --all` on a new file is the same fix, reached the other way."""
        self.r.write("seed", "x\n")
        self.r.commit()
        self.r.write("fresh", "one\ntwo\nthree\n")
        git(["add", "-N", "fresh"], self.r.dir)
        p = self.r.stg("split", "--all", "fresh")
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertEqual(self.r.staged_file_content("fresh"),
                         "one\ntwo\nthree\n")

    def test_an_address_never_names_two_changes(self):
        """A coordinate that stages two changes is not an address.

        A deletion is anchored to the line whose content moved up. When an
        insertion lands on exactly that line, both changes answer to one
        coordinate, and `stg f:80` removed eight lines *and* added one while
        printing the coordinate twice and exiting 1 -- a real commit, measured
        in EXPERIMENTS/046-real-changes. The file assigns one line per change:
        a change that occupies a line keeps it, a deletion moves up only when it
        has to, and a single-line request returns at most one change.
        """
        lines = ["l%03d" % i for i in range(1, 121)]
        self.r.write("f", "".join(l + "\n" for l in lines))
        self.r.commit()
        post = list(lines)
        del post[78:86]             # a deletion run: stg anchors it below the gap
        post.insert(79, "NEW")      # an insertion on exactly that line
        self.r.write("f", "".join(l + "\n" for l in post))
        p = self.r.stg("list")
        coordinates = [l.split("\t")[0] for l in p.stdout.strip().split("\n")]
        self.assertEqual(len(coordinates), len(set(coordinates)),
                         "stg list printed a coordinate twice:\n" + p.stdout)
        p = self.r.stg("stage", "f:80")
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertEqual(p.stdout.strip().count("\n"), 0,
                         "one address staged more than one change: " + p.stdout)
        # HEAD plus the one inserted line: the eight deletions must survive.
        expected = list(lines)
        expected.insert(79, "NEW")
        self.assertEqual(self.r.staged_file_content("f"),
                         "".join(l + "\n" for l in expected))

    def test_insertion_past_an_unterminated_last_line_is_refused(self):
        """git would merge two lines and report success, so stg refuses by name.

        `git apply --cached --unidiff-zero` cannot express "a terminated line
        before an unterminated one". Ask it for the second of two lines inserted
        just above a file whose last line has no newline and it returns exit 0
        with the new text glued onto the previous line. A real `requests` commit
        did exactly this; EXPERIMENTS/046-real-changes.
        """
        self.r.write("f", "a\nb\n" + "".join("l%d\n" % i for i in range(1, 25))
                     + "LAST")
        self.r.commit()
        edited = self.r.read("f").split("\n")
        edited[26:26] = ["NEW1", "NEW2"]
        self.r.write("f", "\n".join(edited))
        head_lines = 27
        p = self.r.stg("stage", "f:%d" % (head_lines + 1))
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        self.assertIn("no newline at the end of file", p.stderr)
        self.assertEqual(self.r.staged_file_content("f"), self.r.head_body("f"))

    def test_the_refusal_does_not_fire_on_a_terminated_file(self):
        """The same shape in a file that ends with a newline must still work."""
        self.r.write("f", "a\nb\n" + "".join("l%d\n" % i for i in range(1, 25)))
        self.r.commit()
        edited = self.r.read("f").split("\n")
        edited[26:26] = ["NEW1", "NEW2"]
        self.r.write("f", "\n".join(edited))
        p = self.r.stg("stage", "f:28")
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertNotIn("NEW1", self.r.staged_file_content("f"))
        self.assertIn("NEW2", self.r.staged_file_content("f"))


if __name__ == '__main__':
    unittest.main(verbosity=2)

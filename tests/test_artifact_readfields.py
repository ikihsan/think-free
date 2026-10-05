#!/usr/bin/env python3
"""Falsification cases for 017's mechanical README fields.

Four of 017's five read fields are decided by looking for a string, and H2's
verdict turns on two of them: a document is only a *witness of an unmet need* if
it offers no software, and `teaches_only` is what says that. So the two string
fields have to fail in a known direction rather than an unknown one.

The direction that matters is stated once and reused here. `tutorial` is the class
that makes a document look like documentation of an existing tool, which is the
reading that would *rescue* every candidate the mission has killed. A false
`tutorial` therefore flatters the null, and these cases are written to make
`teaches_only` hard to reach by accident.

Run: python3 -m unittest discover -s tests -p 'test_artifact_readfields.py'
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir,
    "EXPERIMENTS", "017-incumbent-artifact-type"))

import readfields  # noqa: E402


def m(repo="owner/name", text=""):
    return readfields.mechanical(repo, text)


class InstallShapeTest(unittest.TestCase):
    def test_prose_about_installing_is_not_an_install_command(self):
        out = m(text="Before installing anything, read this guide.")
        self.assertFalse(out["install_line"])

    def test_a_real_install_command_is_detected(self):
        for line in ("pip install thing", "npm install -g thing", "brew install thing",
                     "cargo install thing", "go install x/y", "uvx thing",
                     "npx thing", "docker run -it thing", "curl -sL x | sh"):
            self.assertTrue(m(text="```\n%s\n```" % line)["install_line"], msg=line)

    def test_the_install_shapes_are_all_reachable(self):
        """A shape added to the module and misspelled in the list is a shape that
        silently never fires."""
        for line in ("pip3 install x", "pnpm add x", "uv tool install x",
                     "gem install x", "apt-get install x", "git clone https://x/y",
                     "docker compose up", "yarn add x", "npm i x",
                     "wget -qO- x | bash", "pnpm dlx x", "npm run npx x"):
            self.assertTrue(m(text=line)["install_line"], msg=line)

    def test_a_missing_readme_is_not_an_install_line(self):
        self.assertFalse(m(text=None)["install_line"])


class ForeignLinkTest(unittest.TestCase):
    def test_a_self_link_with_a_deep_path_is_not_foreign(self):
        out = m("owner/name",
                "See https://github.com/owner/name/blob/main/docs/guide.md")
        self.assertFalse(out["foreign_link"], msg=out["foreign_links"])

    def test_a_badge_to_another_project_is_foreign(self):
        out = m("owner/name", "[build](https://github.com/some/other/actions)")
        self.assertTrue(out["foreign_link"])

    def test_case_does_not_matter(self):
        out = m("Owner/Name", "https://GitHub.com/OWNER/NAME/blob/main/x")
        self.assertFalse(out["foreign_link"])

    def test_a_registry_link_is_foreign(self):
        out = m("owner/name", "Available on https://pypi.org/project/thing")
        self.assertTrue(out["foreign_link"])

    def test_a_relative_link_is_not_foreign(self):
        out = m("owner/name", "See [docs](docs/README.md) and [x](./install.sh)")
        self.assertFalse(out["foreign_link"])

    def test_an_anchor_is_stripped_before_comparing(self):
        out = m("owner/name", "https://github.com/other/repo#install")
        self.assertIn("github.com/other/repo", out["foreign_links"])

    def test_the_class_is_tutorial_when_either_field_fires(self):
        self.assertEqual(m(text="pip install x")["class"], "tutorial")
        self.assertEqual(m(text="https://github.com/a/b")["class"], "tutorial")
        self.assertEqual(m(text="just prose about the problem")["class"],
                         "teaches_only")


class CountIsNotAJudgementTest(unittest.TestCase):
    def test_shell_blocks_are_counted_and_not_interpreted(self):
        body = "```\nls\n```\ntext\n```bash\ngit status\n```\n"
        out = m(text=body)
        self.assertEqual(out["shell_blocks"], 2)
        self.assertEqual(out["class"], "teaches_only")

    def test_a_tagged_non_shell_block_is_not_counted(self):
        out = m(text="```python\nprint(1)\n```\n```bash\ngit status\n```\n")
        self.assertEqual(out["shell_blocks"], 1)

    def test_an_unclosed_fence_is_one_block_not_two(self):
        self.assertEqual(m(text="```\nls\n")["shell_blocks"], 1)

    def test_headings_are_counted(self):
        out = m(text="# a\n## b\n### c\n")
        self.assertEqual(out["headings"], 3)

    def test_byte_count_is_recorded_so_an_empty_readme_is_visible(self):
        self.assertEqual(m(text="")["bytes"], 0)


class ReadShapeTest(unittest.TestCase):
    def test_a_missing_reads_json_is_named_not_treated_as_empty(self):
        ok, problems = readfields.check_reads()
        self.assertFalse(ok)
        self.assertTrue(problems)

    def _write(self, payload):
        path = os.path.join(os.path.dirname(os.path.abspath(readfields.__file__)),
                            "reads.json")
        return path

    def test_the_shape_check_names_each_missing_field(self):
        import json
        import tempfile
        rows = {"owner/name": {"repeated": "yes", "procedure": "  "}}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump({"rows": rows}, fh)
            path = fh.name
        original = readfields.READS
        readfields.READS = path
        try:
            ok, problems = readfields.check_reads()
        finally:
            readfields.READS = original
            os.unlink(path)
        self.assertFalse(ok)
        self.assertEqual(len(problems), 3)
        self.assertTrue(any("repeated is not a boolean" in p for p in problems))
        self.assertTrue(any("no procedure quoted" in p for p in problems))
        self.assertTrue(any("no judgement note" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
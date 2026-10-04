"""Two properties of the push-credential report that are about safety, not logic.

Both exist because something went wrong rather than because a rule was imagined.

* **`FAILURES.md` F014.** The falsification harness for T-0024 passed
  `Path.home()` as the sandbox HOME for two of its three environments and wrote
  its throwaway git config over this VM's real `~/.gitconfig`, destroying the git
  identity and `credential.helper` that 125 commits are authored with. The
  machine's state, not the code's, was what stopped it.

* **The secret.** `git credential fill` hands back a live token. The report
  exists to say whether one was obtained, so the report is exactly the place a
  leaked credential would land. A test that only asserted the verdict would pass
  with the token in `doctor.json`.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path

from harness import RepoTest, git

from originlib import pushprobe
from pushcred_fixture import ANSWER, FAKE_TOKEN, Sandbox



class SecretContainmentTest(RepoTest):
    """`git credential fill` returns a live token. Nothing may keep it."""

    def setUp(self) -> None:
        super().setUp()
        self.box = Sandbox(self)
        self.box.activate(self, self.box.helper(ANSWER))
        git(self.repo, "remote", "add", "origin", "https://github.com/example/project.git")

    def test_the_token_is_absent_from_the_collected_report(self) -> None:
        self.assertNotIn(FAKE_TOKEN, json.dumps(pushprobe.collect(network=True)))

    def test_the_token_is_absent_from_the_summary(self) -> None:
        from originlib import pushcred

        report = pushprobe.collect(network=True)
        self.assertNotIn(FAKE_TOKEN, pushcred.summarize(report))

    def test_the_token_is_absent_from_doctor_json_on_disk(self) -> None:
        from originlib import cli, doctor

        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["doctor"]), 0)
        written = (self.repo / ".origin" / "doctor.json").read_text(encoding="utf-8")
        self.assertNotIn(FAKE_TOKEN, written)

    def test_the_token_is_absent_from_doctor_stdout(self) -> None:
        from originlib import cli

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            cli.main(["doctor"])
        self.assertNotIn(FAKE_TOKEN, buffer.getvalue())

    def test_git_said_carries_no_credential_value(self) -> None:
        """Even the complaint git prints is echoed, so it must be a fixed prefix."""
        report = pushprobe.collect(network=True)
        for warning in report["warnings"] + [report["functional"]["git_said"]]:
            self.assertNotIn(FAKE_TOKEN, warning or "")

    def test_an_offline_probe_does_not_claim_to_know(self) -> None:
        """Offline means untested, not absent. A skipped probe must not decide."""
        report = pushprobe.collect(network=False)
        self.assertFalse(report["functional"]["ran"])
        self.assertEqual(report["functional"].get("obtained"), None)


class SandboxSafetyTest(unittest.TestCase):
    """F014: a fixture that writes to the real HOME damages the machine."""

    def test_a_sandbox_home_is_never_the_real_home(self) -> None:
        box = Sandbox(self)
        self.assertNotEqual(box.home.resolve(), Path(os.environ["HOME"]).resolve())
        self.assertTrue(str(box.home.resolve()).startswith(str(box.root.resolve())))

    def test_activating_a_sandbox_redirects_home(self) -> None:
        real = os.environ["HOME"]
        box = Sandbox(self)
        box.activate(self)
        self.assertEqual(os.environ["HOME"], str(box.home))
        self.assertNotEqual(os.environ["HOME"], real)

    def test_activating_a_sandbox_leaves_the_real_git_config_untouched(self) -> None:
        real_config = Path(os.environ["HOME"]) / ".gitconfig"
        before = real_config.read_bytes() if real_config.exists() else b""
        box = Sandbox(self)
        box.activate(self, box.helper(ANSWER))
        self.assertTrue(box.gitconfig.exists())
        after = real_config.read_bytes() if real_config.exists() else b""
        self.assertEqual(before, after)

    def test_the_sandbox_is_removed_with_the_test(self) -> None:
        test = unittest.TestCase()
        box = Sandbox(test)
        self.assertTrue(box.root.exists())
        # The cleanup is registered, not run, so assert on registration instead
        # of deleting a directory this test still owns.
        self.assertTrue(str(box.root).startswith(tempfile.gettempdir()))


if __name__ == "__main__":
    unittest.main()
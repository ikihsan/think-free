# origin-allow-secret-patterns: github-token
"""The push-credential report `doctor` gained in T-0024: mechanism discovery.

The point of these tests is not that the code runs. It is that the report can
say `broken` and `unavailable` and mean different things, which is the property
the old probe lacked: `doctor` printed `credentials none present` for a working
credential, a broken helper, and no credential at all. Every defect recorded in
`FAILURES.md` F010, F013 and D024 is a gate that could not fail, and this one
could not fail either.

Every case here is built from real bytes: a real helper script on disk, a real
`credential.helper` read through git, and a real `git credential fill` run
against them. Nothing is mocked, so a change that made the report read a
different property than it names fails here rather than on a VM at 3am.

The sandbox rule from `FAILURES.md` F014 is enforced by
`test_no_fixture_names_a_path_outside_its_own_sandbox` and by
`tests/test_pushcred_safety.py`: these tests set HOME and the git config, and the
one way to damage a real machine is to let a fixture write to the real one.

Secret containment and the sandbox guard live in `test_pushcred_safety.py`.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from harness import RepoTest, git
from originlib import pushcred, pushprobe
from pushcred_fixture import ANSWER, FAKE_TOKEN, Sandbox, rmtree


class HelperShapeTest(unittest.TestCase):
    """`classify` reads the shape git would act on, not the string's look."""

    def test_builtin_helpers_are_not_treated_as_paths(self) -> None:
        self.assertEqual(pushcred.classify("store")["kind"], "builtin")
        self.assertEqual(pushcred.classify("cache")["kind"], "builtin")

    def test_shell_snippet_is_never_stat_ed(self) -> None:
        entry = pushcred.classify("!f() { echo protocol=https; }; f")
        self.assertEqual(entry["kind"], "shell")
        self.assertNotIn("exists", entry)

    def test_arguments_are_split_off_so_the_program_can_be_stat_ed(self) -> None:
        entry = pushcred.classify("/bin/echo --label=x")
        self.assertEqual(entry["kind"], "program")
        self.assertEqual(entry["path"], "/bin/echo")

    def test_a_tilde_path_is_expanded_before_it_is_stat_ed(self) -> None:
        self.assertFalse(pushcred.classify("~/bin/helper")["path"].startswith("~"))


class ExternalDependencyTest(unittest.TestCase):
    """The property that catches this VM's live defect: a volatile dependency.

    `instance-20260717-0947` lost every push because its credential helper ran a
    script under `/tmp`, and `/tmp` was cleared. The bytes below are that
    helper's shape reduced to what the rule actually reads.
    """

    def setUp(self) -> None:
        self.dir = Path(tempfile.mkdtemp(prefix="origin-deps-"))
        self.addCleanup(rmtree, self.dir)

    def write(self, body: str) -> Path:
        script = self.dir / "helper.sh"
        script.write_text(body, encoding="utf-8")
        return script

    def test_a_path_outside_the_home_directory_is_reported(self) -> None:
        script = self.write("JWT=$(/tmp/github-app-jwt.sh)\necho \"$JWT\"\n")
        self.assertIn("/tmp/github-app-jwt.sh", pushcred.external_paths(script))

    def test_a_url_is_not_mistaken_for_a_path(self) -> None:
        script = self.write(
            'curl -sS -X POST "https://api.github.com/app/installations/42/access_tokens"\n'
        )
        self.assertEqual(pushcred.external_paths(script), [])

    def test_stable_system_paths_are_not_reported(self) -> None:
        script = self.write("/usr/bin/curl /bin/sh </dev/null >/dev/null 2>/tmp/err\n")
        found = pushcred.external_paths(script)
        for stable in ("/usr/bin/curl", "/bin/sh", "/dev/null"):
            self.assertNotIn(stable, found)

    def test_a_path_inside_the_users_own_home_is_not_reported(self) -> None:
        saved = os.environ.get("HOME")
        os.environ["HOME"] = str(self.dir)
        self.addCleanup(lambda: os.environ.__setitem__("HOME", saved or ""))
        script = self.write(f"{self.dir}/.config/github-app/get-token.py\n")
        self.assertEqual(pushcred.external_paths(script), [])

    def test_a_missing_script_reports_nothing_rather_than_guessing(self) -> None:
        self.assertEqual(pushcred.external_paths(self.dir / "nope.sh"), [])

    def test_the_script_text_is_never_returned(self) -> None:
        secret = "ghs_thisstringmustneverappearinalist0000000000"
        script = self.write(f'echo password={secret}\nJWT=$(/tmp/gen.sh)\n')
        self.assertNotIn(secret, str(pushcred.external_paths(script)))


class VerdictTest(RepoTest):
    """The three states the old probe collapsed into a single line."""

    def collect(self) -> dict:
        git(self.repo, "remote", "add", "origin", "https://github.com/example/project.git")
        return pushprobe.collect(network=True)

    def test_a_working_helper_is_reported_configured(self) -> None:
        box = Sandbox(self)
        box.activate(self, box.helper(ANSWER))
        report = self.collect()
        self.assertEqual(report["verdict"], "configured", report["warnings"])
        self.assertTrue(report["functional"]["obtained"])
        self.assertEqual(report["functional"]["exit_code"], 0)

    def test_the_recorded_defect_shape_is_reported_broken(self) -> None:
        """`instance-20260717-0947`: the helper survived, its dependency did not.

        The helper still exists, still has the right mode, and still answers git
        — with nothing. Only a probe that actually asks git can see this, which
        is why the verdict is not built from file listings.
        """
        box = Sandbox(self)
        volatile = box.root / "tmp-like" / "github-app-jwt.sh"
        volatile.parent.mkdir(parents=True)
        volatile.write_text(f"echo {FAKE_TOKEN}\n", encoding="utf-8")
        volatile.chmod(0o700)
        script = box.helper(
            "#!/bin/sh\n"
            'while read -r l; do [ -z "$l" ] && break; done\n'
            f"JWT=$({volatile})\n"
            "echo protocol=https\necho host=github.com\necho username=x\necho password=$JWT\n"
        )
        box.activate(self, script)
        self.assertEqual(pushprobe.collect(network=False)["verdict"], "configured")
        self.assertTrue(
            any(str(volatile) in w for w in pushprobe.collect(network=False)["warnings"]),
            "the volatile dependency must be named while it is still there",
        )
        volatile.unlink()
        report = self.collect()
        self.assertEqual(report["verdict"], "broken")
        self.assertFalse(report["functional"]["obtained"])

    def test_a_helper_path_that_does_not_exist_is_broken(self) -> None:
        box = Sandbox(self)
        box.activate(self, box.root / "absent-helper.sh")
        report = self.collect()
        self.assertEqual(report["verdict"], "broken")
        self.assertFalse(report["functional"]["obtained"])
        self.assertTrue(any("does not exist" in w for w in report["warnings"]), report["warnings"])

    def test_a_helper_that_exists_but_is_not_executable_is_broken(self) -> None:
        box = Sandbox(self)
        box.activate(self, box.helper("echo hello\n", mode=0o600))
        report = self.collect()
        self.assertEqual(report["verdict"], "broken")
        self.assertFalse(report["functional"]["obtained"])
        self.assertTrue(any("not executable" in w for w in report["warnings"]), report["warnings"])

    def test_no_mechanism_is_unavailable_not_broken(self) -> None:
        """Absence and breakage are different states and are reported as such.

        The first implementation called a fresh VM with no credential `broken`,
        which is the incident that cost this fleet a push and would send the
        next agent hunting a helper that was never configured.
        """
        box = Sandbox(self)
        box.activate(self, None)
        report = self.collect()
        self.assertEqual(report["verdict"], "unavailable")
        self.assertEqual(report["helpers"], [])

    def test_an_environment_token_alone_is_a_broken_mechanism(self) -> None:
        """The negative control for the test above, and D030's subject.

        An environment token *is* a credential mechanism, so a machine carrying
        one and no helper is `broken` — git cannot obtain a credential from it
        unaided — rather than `unavailable`. Without this pair the first test
        only shows that some absence is reported; with it, it shows which
        absence, and the runner that exports `GITHUB_TOKEN` stops changing the
        answer.
        """
        box = Sandbox(self)
        box.activate(self, None, token=True)
        os.environ["GITHUB_TOKEN"] = "not-a-real-token"
        report = self.collect()
        self.assertEqual(report["verdict"], "broken", report["warnings"])
        self.assertEqual(report["helpers"], [])

    def test_the_sandbox_clears_a_token_the_runner_injected(self) -> None:
        """Why the fixture pops these at all, asserted so it cannot regress.

        This is the shape of the CI failure in runs `37174050724`, `37174316639`
        and `37174309822`: a fixture that inherits the environment is testing the
        runner as much as the code.
        """
        os.environ["GITHUB_TOKEN"] = "injected-by-the-runner"
        box = Sandbox(self)
        box.activate(self, None)
        self.assertNotIn("GITHUB_TOKEN", os.environ)
        self.assertNotIn("GH_TOKEN", os.environ)

    def test_the_sandbox_restores_the_tokens_it_found(self) -> None:
        """Clearing without restoring leaks into every later test in the run.

        Found by falsification, not by reading: dropping `GH_TOKEN`/`GITHUB_TOKEN`
        from the fixture's saved-names tuple left every test green, because
        nothing asserted the restore. Unittest runs test classes in one process,
        so a token left cleared by one test changes what the next one sees — and
        `pushprobe` counts that token as a mechanism, so the direction of the
        leak decides a verdict. The sandbox borrows the environment; it does not
        own it.
        """
        os.environ["GITHUB_TOKEN"] = "belongs-to-the-runner"
        os.environ["GH_TOKEN"] = "also-the-runners"
        box = Sandbox(self)
        box.activate(self, None)
        self.assertNotIn("GITHUB_TOKEN", os.environ)
        # `doCleanups` drains `_cleanups`, so the framework's later call is a
        # no-op rather than a double restore.
        self.doCleanups()
        self.assertEqual(os.environ.get("GITHUB_TOKEN"), "belongs-to-the-runner")
        self.assertEqual(os.environ.get("GH_TOKEN"), "also-the-runners")

    def test_a_key_in_the_wrong_mode_is_a_warning_not_a_verdict(self) -> None:
        box = Sandbox(self)
        box.app_key(mode=0o644)
        box.activate(self, box.helper(ANSWER))
        report = self.collect()
        self.assertTrue(
            any("must be 0600" in w for w in report["warnings"]), report["warnings"]
        )

    def test_the_verdict_is_readable_without_the_json(self) -> None:
        box = Sandbox(self)
        box.activate(self, box.helper(ANSWER))
        report = self.collect()
        line = pushcred.summarize(report)
        self.assertIn("push credential", line)
        self.assertNotIn(FAKE_TOKEN, line)

    def test_no_fixture_names_a_path_outside_its_own_sandbox(self) -> None:
        """A test whose premise depends on the machine is a test the machine decides.

        The first version of the recorded-defect test named
        `/tmp/github-app-jwt.sh`, which exists on `instance-20260717-0944`. It
        passed there for the wrong reason and would have failed on a VM where the
        file is absent. Fixtures build their paths inside the sandbox instead.
        """
        box = Sandbox(self)
        for candidate in (box.home, box.gitconfig, box.root / "absent-helper.sh"):
            self.assertTrue(
                str(candidate).startswith(str(box.root)), f"{candidate} escapes {box.root}"
            )


class RemoteReportingTest(RepoTest):
    """The reported remote must be safe to write into a committed record."""

    def test_userinfo_in_the_remote_url_is_stripped(self) -> None:
        git(self.repo, "remote", "add", "origin", "https://someone:token@github.com/e/p.git")
        self.assertEqual(pushcred.remote()["remote"], "https://github.com")

    def test_a_repository_with_no_remote_says_so(self) -> None:
        self.assertFalse(pushcred.remote()["configured"])

    def test_the_functional_probe_does_not_run_without_a_remote(self) -> None:
        self.assertFalse(pushprobe.functional("", "", network=True)["ran"])

    def test_the_probe_is_skipped_offline(self) -> None:
        probe = pushprobe.functional("https", "github.com", network=False)
        self.assertFalse(probe["ran"])
        self.assertEqual(probe["reason"], "offline")


if __name__ == "__main__":
    unittest.main()
"""Secret detection and the two redaction policies."""

# origin-allow-secret-patterns: github-app-private-key, github-token, github-fine-grained-pat, aws-access-key-id, openai-key, anthropic-key, slack-token, google-api-key, assigned-credential
from __future__ import annotations

import unittest

from harness import RepoTest

from originlib import secrets

TOKENS = (
    "github-token",
    "github-fine-grained-pat",
    "aws-access-key-id",
    "openai-key",
    "github-app-private-key",
    "slack-token",
    "google-api-key",
)

SAMPLES = {
    "github-token": "token = ghp_abcdefghijklmnopqrstuvwxyz012345",
    "github-fine-grained-pat": "github_pat_11ABCDEFG0abcdefghijklmnop",
    "aws-access-key-id": "AKIAIOSFODNN7EXAMPLE",
    "openai-key": "sk-abcdefghijklmnopqrstuvwxyz012345",
    "github-app-private-key": "-----BEGIN RSA PRIVATE KEY-----\nMIIEow==\n",
    "slack-token": "xoxb-123456789012-abcdefghijkl",
    "google-api-key": "AIzaSyA12345678901234567890123456789012",
}


class SecretScanTest(unittest.TestCase):
    def test_each_sample_is_detected(self) -> None:
        for name, sample in SAMPLES.items():
            self.assertIn(name, secrets.names(secrets.scan(sample)), name)

    def test_ordinary_text_is_clean(self) -> None:
        clean = (
            "The build finished in 1.2s. See docs/policy/logging-standard.md.\n"
            "password: hunter2 is too short to match\n"
            "api_key = <not-a-real-key>\n"
        )
        self.assertEqual(secrets.scan(clean), [])

    def test_redact_replaces_every_match(self) -> None:
        text = f"before {SAMPLES['aws-access-key-id']} middle {SAMPLES['openai-key']} after"
        cleaned, names = secrets.redact(text)
        self.assertNotIn("AKIAIOSFODNN7EXAMPLE", cleaned)
        self.assertNotIn("sk-abcdefghijklmnopqrstuvwxyz012345", cleaned)
        self.assertIn("before", cleaned)
        self.assertIn("middle", cleaned)
        self.assertIn("after", cleaned)
        self.assertEqual(sorted(names), ["aws-access-key-id", "openai-key"])

    def test_redact_is_a_noop_when_clean(self) -> None:
        cleaned, names = secrets.redact("nothing sensitive here")
        self.assertEqual(cleaned, "nothing sensitive here")
        self.assertEqual(names, [])

    def test_overlapping_matches_collapse_to_the_specific_pattern(self) -> None:
        found = secrets.names(secrets.scan(SAMPLES["github-token"]))
        self.assertEqual(found, ["github-token"])

    def test_findings_never_include_the_secret(self) -> None:
        findings = secrets.scan(SAMPLES["github-token"])
        self.assertTrue(findings)
        for finding in findings:
            self.assertNotIn("ghp_", finding.pattern)

    def test_binary_file_is_skipped(self) -> None:
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "blob.bin"
            path.write_bytes(b"\x00\x01binary\xff")
            self.assertEqual(secrets.scan_file(path), [])

    def test_scan_file_reads_text(self) -> None:
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.env"
            path.write_text(f"AWS={SAMPLES['aws-access-key-id']}\n", encoding="utf-8")
            self.assertEqual(secrets.scan_file(path), ["aws-access-key-id"])


class ArtifactRefusalTest(RepoTest):
    def test_artifact_with_a_secret_is_refused(self) -> None:
        from originlib import session

        self.cli("session", "start", "--goal", "test artifact refusal")
        path = self.write("leaky.env", f"TOKEN={SAMPLES['github-token']}\n")
        with self.assertRaises(session.SessionError):
            session.artifact(str(path))
        errors = [
            e
            for e in self.session_events(session.load_active().session)
            if e["kind"] == "integrity_error"
        ]
        self.assertEqual(len(errors), 1)
        self.assertIn("refused artifact", errors[0]["data"]["summary"])
        self.assertEqual(errors[0]["data"]["patterns"], ["github-token"])

    def test_clean_artifact_is_recorded_with_a_hash(self) -> None:
        from originlib import session

        self.cli("session", "start", "--goal", "test artifact recording")
        path = self.write("clean.txt", "hello\n")
        event = session.artifact(str(path))
        self.assertEqual(event.data["sha256"][:12], "5891b5b522d5")
        self.assertEqual(event.data["bytes"], 6)

    def test_missing_artifact_raises(self) -> None:
        from originlib import session

        self.cli("session", "start", "--goal", "test missing artifact")
        with self.assertRaises(session.SessionError):
            session.artifact("does/not/exist.txt")

    def test_directory_artifact_is_refused(self) -> None:
        from originlib import session

        self.cli("session", "start", "--goal", "test directory artifact")
        with self.assertRaises(session.SessionError):
            session.artifact("docs")


if __name__ == "__main__":
    unittest.main()


class SuppressionTest(RepoTest):
    """A file may declare fake credentials on purpose, by naming the patterns."""

    DIRECTIVE = "# origin-allow-secret-patterns: github-token\n"

    def test_directive_suppresses_the_named_pattern_only(self) -> None:
        text = self.DIRECTIVE + "TOKEN=ghp_abcdefghijklmnopqrstuvwxyz012345\nAKIAIOSFODNN7EXAMPLE\n"
        path = self.write("fixture.env", text)
        found, suppressed = __import__("originlib.secrets", fromlist=["x"]).scan_file(
            path, report_suppressions=True
        )
        self.assertEqual(suppressed, {"github-token"})
        self.assertEqual(found, ["aws-access-key-id"])

    def test_without_the_directive_the_pattern_is_found(self) -> None:
        path = self.write("plain.env", "TOKEN=ghp_abcdefghijklmnopqrstuvwxyz012345\n")
        found = secrets.scan_file(path)
        self.assertIn("github-token", found)

    def test_directive_outside_the_header_window_does_not_apply(self) -> None:
        padding = "\n".join(f"# line {index}" for index in range(60))
        path = self.write("late.env", padding + "\n" + self.DIRECTIVE + "TOKEN=ghp_abcdefghijklmnopqrstuvwxyz012345\n")
        self.assertEqual(secrets.declared_suppressions(path.read_text(encoding="utf-8")), set())

    def test_unknown_pattern_name_in_the_directive_is_simply_ignored(self) -> None:
        path = self.write("odd.env", "# origin-allow-secret-patterns: not-a-pattern\nclean\n")
        found, suppressed = secrets.scan_file(path, report_suppressions=True)
        self.assertEqual(found, [])
        self.assertEqual(suppressed, {"not-a-pattern"})

    def test_declaring_a_fixture_lets_it_be_recorded_and_logs_the_suppression(self) -> None:
        from originlib import session

        self.cli("session", "start", "--goal", "declare a fixture with fake credentials")
        path = self.write("fixture.env", self.DIRECTIVE + "TOKEN=ghp_abcdefghijklmnopqrstuvwxyz012345\n")
        event = session.artifact(str(path))
        self.assertEqual(event.data["path"], "fixture.env")
        notes = [e for e in self.session_events(session.load_active().session) if e["kind"] == "note"]
        self.assertTrue(any("origin-allow-secret-patterns" in n["data"]["summary"] for n in notes))

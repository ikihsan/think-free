"""Secret detection and the two redaction policies."""

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
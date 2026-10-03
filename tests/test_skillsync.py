"""Skill naming rules, cross-agent mirroring, and vendored-content integrity."""

from __future__ import annotations

import json
import os
import unittest
from pathlib import Path

from harness import RepoTest

from originlib import paths, skillsync


def write_skill(repo: Path, name: str, description: str = "A test skill. Use when testing.",
                front_name: str | None = None, extra: str = "") -> Path:
    directory = repo / ".agents" / "skills" / name
    directory.mkdir(parents=True, exist_ok=True)
    body = (
        "---\n"
        f"name: {front_name or name}\n"
        f"description: {description}\n"
        "license: MIT\n"
        "---\n\n"
        "# " + name + "\n\nBody.\n"
        + extra
    )
    (directory / "SKILL.md").write_text(body, encoding="utf-8")
    return directory


class NamingTest(RepoTest):
    def test_valid_skill_passes(self) -> None:
        write_skill(self.repo, "good-skill")
        skillsync.sync()
        report = skillsync.check()
        self.assertFalse([p for p in report.problems if "good-skill" in p], report.problems)

    def test_missing_skills_dir_fails(self) -> None:
        report = skillsync.check()
        self.assertTrue(any(".agents/skills" in problem for problem in report.problems))

    def test_name_mismatch_fails(self) -> None:
        write_skill(self.repo, "directory-name", front_name="different-name")
        report = skillsync.check()
        self.assertTrue(any("frontmatter name" in problem for problem in report.problems))

    def test_invalid_name_fails(self) -> None:
        write_skill(self.repo, "Bad_Name")
        report = skillsync.check()
        self.assertTrue(any("name must match" in problem for problem in report.problems))

    def test_reserved_name_fails(self) -> None:
        write_skill(self.repo, "synced")
        report = skillsync.check()
        self.assertTrue(any("reserved skill name" in problem for problem in report.problems))

    def test_missing_description_fails(self) -> None:
        directory = write_skill(self.repo, "no-description")
        (directory / "SKILL.md").write_text("---\nname: no-description\n---\n\nBody\n", encoding="utf-8")
        report = skillsync.check()
        self.assertTrue(any("description is required" in problem for problem in report.problems))

    def test_overlong_description_fails(self) -> None:
        write_skill(self.repo, "long-description", description="x" * 1100)
        report = skillsync.check()
        self.assertTrue(any("description exceeds" in problem for problem in report.problems))

    def test_non_spec_frontmatter_is_a_warning_not_a_failure(self) -> None:
        write_skill(self.repo, "extra-keys", extra="")
        path = self.repo / ".agents" / "skills" / "extra-keys" / "SKILL.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("license: MIT", "license: MIT\nargument-hint: x"),
            encoding="utf-8",
        )
        skillsync.sync()
        report = skillsync.check()
        self.assertTrue(report.ok)
        self.assertTrue(any("non-spec frontmatter" in warning for warning in report.warnings))


class MirrorTest(RepoTest):
    def test_missing_claude_dir_is_reported(self) -> None:
        write_skill(self.repo, "mirror-me")
        report = skillsync.check()
        self.assertTrue(any(".claude/skills" in problem for problem in report.problems))

    def test_sync_creates_symlink_mirrors(self) -> None:
        write_skill(self.repo, "alpha")
        write_skill(self.repo, "beta-skill")
        report = skillsync.sync()
        self.assertTrue(report.ok, report.problems)
        for name in ("alpha", "beta-skill"):
            link = self.repo / ".claude" / "skills" / name
            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), (self.repo / ".agents" / "skills" / name).resolve())

    def test_copy_mode_materialises_real_directories(self) -> None:
        write_skill(self.repo, "copied")
        skillsync.sync(use_copies=True)
        link = self.repo / ".claude" / "skills" / "copied"
        self.assertFalse(link.is_symlink())
        self.assertTrue((link / "SKILL.md").exists())

    def test_orphan_mirror_is_reported(self) -> None:
        write_skill(self.repo, "canonical")
        (self.repo / ".claude" / "skills" / "ghost").mkdir(parents=True)
        (self.repo / ".claude" / "skills" / "ghost" / "SKILL.md").write_text(
            "---\nname: ghost\ndescription: d\n---\n", encoding="utf-8"
        )
        report = skillsync.check()
        self.assertTrue(any("ghost" in problem for problem in report.problems))

    def test_wrong_symlink_target_is_reported(self) -> None:
        write_skill(self.repo, "pointed")
        skillsync.sync()
        link = self.repo / ".claude" / "skills" / "pointed"
        link.unlink()
        (self.repo / ".agents" / "skills" / "elsewhere").mkdir()
        link.symlink_to(Path("../../.agents/skills/elsewhere"), target_is_directory=True)
        report = skillsync.check()
        self.assertTrue(any("symlink points at" in problem for problem in report.problems))


class VendorIntegrityTest(RepoTest):
    def declare(self, *names: str) -> None:
        vendor = self.repo / "vendor"
        vendor.mkdir(exist_ok=True)
        lines = ["# Vendor", "", "<!-- origin-meta", "owner: docs/INDEX.md", "status: active",
                 "last-verified: 2026-10-03", "-->", ""]
        lines += [f"vendored: {name}" for name in names]
        (vendor / "MANIFEST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def test_hashes_are_written_for_declared_vendored_skills(self) -> None:
        write_skill(self.repo, "upstream-skill")
        self.declare("upstream-skill")
        target = skillsync.write_hashes()
        payload = json.loads(target.read_text(encoding="utf-8"))
        self.assertIn("upstream-skill", payload["skills"])
        self.assertIn("SKILL.md", payload["skills"]["upstream-skill"])

    def test_unmodified_vendored_skill_verifies(self) -> None:
        write_skill(self.repo, "upstream-skill")
        self.declare("upstream-skill")
        skillsync.write_hashes()
        report = skillsync.verify_vendor()
        self.assertTrue(report.ok, report.problems)

    def test_modified_vendored_file_is_detected(self) -> None:
        write_skill(self.repo, "upstream-skill")
        self.declare("upstream-skill")
        skillsync.write_hashes()
        path = self.repo / ".agents" / "skills" / "upstream-skill" / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "\ntampered\n", encoding="utf-8")
        report = skillsync.verify_vendor()
        self.assertFalse(report.ok)
        self.assertTrue(any("modified" in problem for problem in report.problems))

    def test_removed_vendored_file_is_detected(self) -> None:
        write_skill(self.repo, "upstream-skill")
        self.declare("upstream-skill")
        skillsync.write_hashes()
        (self.repo / ".agents" / "skills" / "upstream-skill" / "SKILL.md").unlink()
        report = skillsync.verify_vendor()
        self.assertTrue(any("removed" in problem for problem in report.problems))

    def test_missing_hashes_file_is_reported(self) -> None:
        report = skillsync.verify_vendor()
        self.assertTrue(any("hashes.json" in problem for problem in report.problems))

    def test_authored_skills_are_distinguished_from_vendored(self) -> None:
        write_skill(self.repo, "mine")
        write_skill(self.repo, "theirs")
        self.declare("theirs")
        self.assertEqual(skillsync.declared_vendored(), {"theirs"})
        self.assertEqual(skillsync.authored(), {"mine"})


if __name__ == "__main__":
    unittest.main()
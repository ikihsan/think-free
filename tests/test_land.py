"""`sync land`: the operation that combines two machines' work.

Split out of `test_sync.py` at the line cap, by operation rather than by date:
`land` is the only command here that rebases, resolves, regenerates and pushes,
so it is the only one whose tests need a fleet and a rebuild. `test_sync.py` keeps
status, pull and push.

The properties this file holds, each of which cost something to learn:

* a land publishes the branch and leaves the tree clean (`test_land_rebases...`);
* a *conflicted* generated file is regenerated as a resolution
  (`test_land_resolves_generated_index_conflicts...`);
* a generated file that merged **cleanly** is rebuilt anyway, because a render
  depends on the whole tree and git reports nothing about it
  (`test_land_rebuilds_a_generated_file_that_merged_cleanly`, defect 13);
* `git rebase --continue` must never open an editor, or CI fails the step and a
  VM with an inherited pipe blocks (`test_land_never_opens_an_editor...`);
* a real content conflict stops for a human and keeps the work
  (`test_land_reports_a_real_content_conflict...`).
"""

from __future__ import annotations

import json
import os

from harness import RepoTest, git, make_fleet

from originlib import sync, syncland
from originlib.sync import SyncError


class LandTest(RepoTest):
    def setUp(self) -> None:
        super().setUp()
        self.fleet = make_fleet(self)
        self.vm_a = self.fleet / "vm-a"
        self.vm_b = self.fleet / "vm-b"

    def commit_on(self, clone, name: str, content: str) -> None:
        (clone / name).write_text(content, encoding="utf-8")
        git(clone, "add", "-A")
        git(clone, "commit", "-qm", f"add {name}")
        git(clone, "push", "-q", "origin", "research/origin")

    def test_land_rebases_onto_the_base_and_pushes(self) -> None:
        self.use(self.vm_a)
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0001-vm-a", "origin/research/origin")
        (self.vm_a / "work.md").write_text("mine\n", encoding="utf-8")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "mine")
        self.commit_on(self.vm_b, "from-b.md", "b\n")
        outcome = syncland.land()
        self.assertTrue(outcome["pushed"])
        self.assertEqual(
            git(self.vm_a, "rev-parse", "origin/research/origin"),
            git(self.vm_a, "rev-parse", "HEAD"),
        )
        self.assertTrue((self.vm_a / "from-b.md").exists())

    def test_land_resolves_generated_index_conflicts_by_regenerating(self) -> None:
        self.use(self.vm_a)
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0001-vm-a", "origin/research/origin")
        # Both VMs regenerate the same generated file with different content,
        # which is what two concurrent sessions actually produce.
        (self.vm_a / "sessions").mkdir(exist_ok=True)
        (self.vm_b / "sessions").mkdir(exist_ok=True)
        (self.vm_a / "sessions" / "INDEX.md").write_text(
            "# Sessions index\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\nlast-verified: 2026-10-03\n-->\n\nfrom a\n",
            encoding="utf-8",
        )
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "regenerate index on a")
        git(self.vm_b, "pull", "-q", "--ff-only")
        (self.vm_b / "sessions" / "INDEX.md").write_text(
            "# Sessions index\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\nlast-verified: 2026-10-03\n-->\n\nfrom b\n",
            encoding="utf-8",
        )
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "regenerate index on b")
        git(self.vm_b, "push", "-q", "origin", "research/origin")
        outcome = syncland.land()
        self.assertTrue(outcome["resolved"])
        self.assertIn("sessions/INDEX.md", " ".join(outcome["resolved"]))
        from originlib import report

        regenerated = report.render_sessions_index()
        self.assertEqual((self.vm_a / "sessions" / "INDEX.md").read_text(encoding="utf-8"), regenerated)

    def add_session(self, clone, letter: str, regenerate: bool) -> None:
        """A session directory on one VM, with its report and its index row.

        The id has the `YYYY-MM-DD-NNN-slug` shape the session reader recognises,
        or the renderer lists nothing and the whole fixture is vacuous.
        """
        from originlib import report

        session = clone / "sessions" / ("2026-01-01-001-from-a" if letter == "a" else "2026-01-01-002-from-b")
        session.mkdir(parents=True, exist_ok=True)
        (session / "events.jsonl").write_text(
            json.dumps({
                "kind": "session_start", "seq": 1, "session": session.name,
                "ts": "2026-01-01T00:00:00+00:00", "actor": letter, "host": f"vm-{letter}",
                "schema": "origin.session.event/1",
                "data": {"goal": f"from {letter}", "agent": letter, "task": "",
                         "base_branch": "research/origin", "remote": "origin",
                         "remote_head": "", "behind_before": 0, "dirty_at_start": [],
                         "fast_forwarded": False},
                "git": {"branch": "research/origin", "head": ""},
            }) + "\n",
            encoding="utf-8",
        )
        (session / "README.md").write_text(
            f"# Session {session.name}\n\n<!-- origin-meta\nowner: sessions/INDEX.md\n"
            "status: active\nlast-verified: 2026-01-01\n-->\n\nGenerated.\n",
            encoding="utf-8",
        )
        if regenerate:
            (clone / "sessions" / "INDEX.md").write_text(
                report.render_sessions_index(), encoding="utf-8"
            )

    def test_land_rebuilds_a_generated_file_that_merged_cleanly(self) -> None:
        """The case that is not a conflict, and cost a red CI run on 2026-10-04.

        One VM records a session and regenerates `sessions/INDEX.md`; the other
        records one and does not. The rebase brings the second session directory
        across, git merges **nothing** — no file is conflicted — and the index on
        disk lists one session where the tree holds two. `_resolve_generated_
        conflicts` asks git what conflicted and sees nothing, so `e942225` was
        pushed that way: red on `doc lint` with "generated file is stale", which is
        what the next commit fixed.

        So the test builds that, and asserts the property rather than the
        mechanism: after `land`, every generated file equals its renderer.
        """
        from originlib import docindex, report, tasks

        self.use(self.vm_a)
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0003-vm-a", "origin/research/origin")
        self.add_session(self.vm_a, "a", regenerate=True)
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "session from a")
        git(self.vm_b, "pull", "-q", "--ff-only")
        self.add_session(self.vm_b, "b", regenerate=False)
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "session from b, index not rebuilt")
        git(self.vm_b, "push", "-q", "origin", "research/origin")
        outcome = syncland.land()
        self.assertIn("sessions/INDEX.md", outcome.get("refreshed") or [])
        for path, render in (
            (self.vm_a / "docs" / "INDEX.md", docindex.render()),
            (self.vm_a / "sessions" / "INDEX.md", report.render_sessions_index()),
            (self.vm_a / "tasks" / "INDEX.md", tasks.render_tasks_index()),
        ):
            self.assertEqual(path.read_text(encoding="utf-8"), render, path.name)

    def test_land_leaves_current_generated_files_alone(self) -> None:
        # The control. A repair that rewrites a correct file is a repair that
        # makes a commit nobody asked for, so the empty case must commit nothing.
        from originlib import docindex, report, tasks

        self.use(self.vm_a)
        for clone in (self.vm_a, self.vm_b):
            for name in ("docs", "sessions", "tasks"):
                (clone / name).mkdir(parents=True, exist_ok=True)

        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0004-vm-a", "origin/research/origin")
        (self.vm_a / "docs" / "INDEX.md").write_text(docindex.render(), encoding="utf-8")
        (self.vm_a / "sessions" / "INDEX.md").write_text(report.render_sessions_index(), encoding="utf-8")
        (self.vm_a / "tasks" / "INDEX.md").write_text(tasks.render_tasks_index(), encoding="utf-8")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "regenerate the indexes")
        before = git(self.vm_a, "rev-parse", "HEAD")
        outcome = syncland.land()
        self.assertEqual(outcome.get("refreshed") or [], [])
        self.assertEqual(git(self.vm_a, "rev-parse", "HEAD"), before)

    def test_land_never_opens_an_editor_to_continue_a_rebase(self) -> None:
        """`git rebase --continue` is interactive from git 2.5x; land must not be.

        This is the test that CI could not run: with an editor to open, a VM
        whose stdin is an inherited pipe blocks until the 60 s timeout and a CI
        runner fails the step outright, so `land` refused to land on exactly the
        push every other VM depends on. The sentinel editor records any attempt,
        including one inherited from the caller's own environment.

        On git older than 2.26 `rebase --continue` did not open an editor, so
        this test passes there either way. It is the *modern* git run that is
        the evidence: see the git version this VM reports.
        """
        self.use(self.vm_a)
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0002-vm-a", "origin/research/origin")
        marker = self.vm_a / "editor-was-opened"
        editor = self.vm_a / "sentinel-editor.sh"
        editor.write_text(f"#!/bin/sh\ntouch {marker}\n", encoding="utf-8")
        editor.chmod(0o755)
        for name in ("GIT_EDITOR", "EDITOR", "VISUAL"):
            previous = os.environ.get(name)
            os.environ[name] = str(editor)

            def restore(value=previous, key=name) -> None:
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

            self.addCleanup(restore)
        for name in ("sessions",):
            (self.vm_a / name).mkdir(exist_ok=True)
            (self.vm_b / name).mkdir(exist_ok=True)
        (self.vm_a / "sessions" / "INDEX.md").write_text(
            "# Sessions index\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\nlast-verified: 2026-10-03\n-->\n\nfrom a\n",
            encoding="utf-8",
        )
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "regenerate index on a")
        git(self.vm_b, "pull", "-q", "--ff-only")
        (self.vm_b / "sessions" / "INDEX.md").write_text(
            "# Sessions index\n\n<!-- origin-meta\nowner: docs/INDEX.md\nstatus: active\nlast-verified: 2026-10-03\n-->\n\nfrom b\n",
            encoding="utf-8",
        )
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "regenerate index on b")
        git(self.vm_b, "push", "-q", "origin", "research/origin")
        outcome = syncland.land()
        self.assertIn("sessions/INDEX.md", " ".join(outcome["resolved"]))
        self.assertFalse(
            marker.exists(),
            "land let git open an editor to continue the rebase; the continue must be non-interactive",
        )

    def test_land_reports_a_real_content_conflict_and_keeps_the_work(self) -> None:
        self.use(self.vm_a)
        git(self.vm_a, "fetch", "-q", "origin")
        git(self.vm_a, "checkout", "-q", "-b", "task/T-0001-vm-a", "origin/research/origin")
        (self.vm_a / "shared.md").write_text("mine\n", encoding="utf-8")
        git(self.vm_a, "add", "-A")
        git(self.vm_a, "commit", "-qm", "mine")
        (self.vm_b / "shared.md").write_text("theirs\n", encoding="utf-8")
        git(self.vm_b, "add", "-A")
        git(self.vm_b, "commit", "-qm", "theirs")
        git(self.vm_b, "push", "-q", "origin", "research/origin")
        with self.assertRaises(SyncError) as caught:
            syncland.land()
        self.assertIn("shared.md", str(caught.exception))
        self.assertIn("mine", (self.vm_a / "shared.md").read_text(encoding="utf-8"))
        # The rebase is left for a human to inspect rather than thrown away.
        self.assertTrue(sync.status()["rebase_in_progress"])

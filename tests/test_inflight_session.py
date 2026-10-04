"""In-flight versus abandoned: the predicate CI depends on.

Every clause of `inflight.classify` has a test here, including the negative
cases. A gate that cannot fail for the right reason is worse than no gate, and
the whole point of T-0020 is that the previous gate failed for the wrong one.
"""

from __future__ import annotations

import json
import unittest
from datetime import datetime, timedelta, timezone

from harness import RepoTest

from originlib import events, inflight, paths, report, session, tasks, taskops

INFLIGHT = "2026-10-03-900-in-flight"
NOW = datetime(2026, 10, 3, 22, 0, tzinfo=timezone.utc)


def ago(hours: float) -> str:
    return (NOW - timedelta(hours=hours)).isoformat(timespec="seconds")


class InflightFixture(RepoTest):
    """A claimed task plus an unfinished session on another machine."""

    def setUp(self) -> None:
        super().setUp()
        self.write_generated()
        self.task = taskops.create("work another VM is doing", "true")
        self.claim(agent="agent-a", vm="vm-a", session=INFLIGHT)
        self.start_event = events.append(
            INFLIGHT,
            "session_start",
            {"goal": "still running", "agent": "agent-a", "task": self.task.task_id},
            actor="agent-a",
            host="vm-a",
        ).raw
        report.regenerate_session(INFLIGHT)

    def claim(self, *, agent: str, vm: str, session: str) -> None:
        taskops.claim(self.task.task_id, agent=agent, vm=vm, session=session)

    def set_meta(self, **updates: str) -> None:
        taskops._set_meta(tasks.find(self.task.task_id), updates)

    def _write_claim_ts(self, stamp: str) -> None:
        from originlib import paths

        path = paths.claims_file()
        lines = path.read_text(encoding="utf-8").splitlines()
        entry = json.loads(lines[-1])
        entry["ts"] = stamp
        lines[-1] = json.dumps(entry, sort_keys=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def backdate_claim(self, hours: float) -> None:
        """Age the last ledger entry against the fixed `NOW`, so the lease can be
        tested on a real file.

        Correct only where `now=NOW` is also passed, which is what
        `ClassificationTest` does. The CLI tests cannot pass a clock — `origin
        session verify` reads the real one — so they use
        `backdate_claim_now` instead. Dating their claim from `NOW` made the
        claim grow older every hour, and the 24-hour assertion began failing at
        exactly 24 hours after `NOW` and could never pass again: defect 15.
        """
        self._write_claim_ts(ago(hours))

    def backdate_claim_now(self, hours: float) -> None:
        """Age the last ledger entry from the real clock, for the CLI tests.

        A claim aged this way means "N hours old", which is what a lease
        assertion is about. It is deliberately a second method rather than a flag
        on the first: the two clocks differ by however long ago the suite was
        written, and a flag lets a test pick the wrong one silently.
        """
        stamp = datetime.now(timezone.utc) - timedelta(hours=hours)
        self._write_claim_ts(stamp.isoformat(timespec="seconds"))

    def classify(self, **kwargs) -> inflight.Verdict:
        kwargs.setdefault("now", NOW)
        return inflight.classify(INFLIGHT, self.start_event, **kwargs)


class ClassificationTest(InflightFixture):
    def test_a_claimed_task_naming_this_session_is_in_flight(self) -> None:
        self.backdate_claim(0.5)
        verdict = self.classify()
        self.assertTrue(verdict.in_flight, verdict.reason)
        self.assertEqual(verdict.task, "T-0001")
        self.assertEqual(verdict.agent, "agent-a")
        self.assertEqual(verdict.vm, "vm-a")
        self.assertAlmostEqual(verdict.age_h or 0.0, 0.5, places=3)

    def test_a_session_that_recorded_no_task_is_abandoned(self) -> None:
        # No task on the session_start, and no claim in the ledger names it.
        start = {"data": {"task": ""}, "actor": "agent-z", "host": "vm-z"}
        verdict = inflight.classify("2026-10-03-909-unclaimed", start, now=NOW)
        self.assertFalse(verdict.in_flight)
        self.assertIn("records no task", verdict.reason)
        self.assertIn("no claim in the ledger names this session", verdict.reason)

    def test_a_claim_naming_a_taskless_session_counts_as_in_flight(self) -> None:
        # `--task` is optional on `session start`, and this VM's peer started a
        # real session without it. The predicate must not call that abandoned.
        start = {"data": {"task": ""}, "actor": "agent-b", "host": "vm-b"}
        tasks.append_claim(
            self.task.task_id, "claim", agent="agent-b", vm="vm-b", session="2026-10-03-901-taskless"
        )
        verdict = inflight.classify("2026-10-03-901-taskless", start, now=NOW)
        self.assertTrue(verdict.in_flight, verdict.reason)
        self.assertEqual(verdict.task, "T-0001")
        self.assertEqual(verdict.vm, "vm-b")

    def test_a_taskless_session_whose_claim_was_closed_is_abandoned(self) -> None:
        start = {"data": {"task": ""}, "actor": "agent-b", "host": "vm-b"}
        tasks.append_claim(
            self.task.task_id, "claim", agent="agent-b", vm="vm-b", session="2026-10-03-902-taskless"
        )
        tasks.append_claim(
            self.task.task_id, "release", agent="agent-b", vm="vm-b", session="2026-10-03-902-taskless"
        )
        verdict = inflight.classify("2026-10-03-902-taskless", start, now=NOW)
        self.assertFalse(verdict.in_flight)
        self.assertIn("not a claim", verdict.reason)

    def test_a_taskless_session_whose_claim_expired_is_abandoned(self) -> None:
        start = {"data": {"task": ""}, "actor": "agent-b", "host": "vm-b"}
        tasks.append_claim(
            self.task.task_id, "claim", agent="agent-b", vm="vm-b", session="2026-10-03-903-taskless"
        )
        self.backdate_claim(13.0)
        verdict = inflight.classify("2026-10-03-903-taskless", start, now=NOW)
        self.assertFalse(verdict.in_flight)
        self.assertIn("past the 12h lease", verdict.reason)

    def test_a_task_absent_from_this_tree_is_abandoned(self) -> None:
        (self.repo / "tasks" / self.task.path.name).unlink()
        self.assertFalse(self.classify().in_flight)

    def test_a_task_that_is_no_longer_claimed_is_abandoned(self) -> None:
        taskops.transition(self.task.task_id, "done", "finished elsewhere")
        verdict = self.classify()
        self.assertFalse(verdict.in_flight)
        self.assertIn("done, not claimed", verdict.reason)

    def test_a_claim_naming_a_different_session_is_abandoned(self) -> None:
        self.set_meta(**{"claim-session": "2026-10-03-901-other"})
        verdict = self.classify()
        self.assertFalse(verdict.in_flight)
        self.assertIn("not this session", verdict.reason)

    def test_a_claim_without_a_session_id_falls_back_to_agent_and_host(self) -> None:
        self.set_meta(**{"claim-session": ""})
        self.assertTrue(self.classify().in_flight)

    def test_a_claim_without_a_session_id_on_another_vm_is_abandoned(self) -> None:
        self.set_meta(**{"claim-session": "", "claim-vm": "vm-z"})
        verdict = self.classify()
        self.assertFalse(verdict.in_flight)
        self.assertIn("vm-z", verdict.reason)

    def test_a_closed_ledger_action_is_abandoned(self) -> None:
        tasks.append_claim(self.task.task_id, "release", agent="agent-a", vm="vm-a")
        verdict = self.classify()
        self.assertFalse(verdict.in_flight)
        self.assertIn("'release', not a claim", verdict.reason)

    def test_a_ledger_closing_a_claim_beats_a_task_file_saying_claimed(self) -> None:
        # The two records are checked independently on purpose: a task file
        # edited by hand must not be able to make an abandoned session look live.
        tasks.append_claim(self.task.task_id, "complete", agent="agent-a", vm="vm-a")
        verdict = self.classify()
        self.assertFalse(verdict.in_flight)
        self.assertIn("'complete', not a claim", verdict.reason)

    def test_a_task_with_no_ledger_entry_is_abandoned(self) -> None:
        verdict = self.classify(ledger=[])
        self.assertFalse(verdict.in_flight)
        self.assertIn("no entry in the claim ledger", verdict.reason)

    def test_a_takeover_keeps_the_claim_in_force_locally(self) -> None:
        # The local ledger view used to ignore `takeover`, so the local and
        # remote views of who held a task disagreed after every takeover.
        tasks.append_claim(self.task.task_id, "release", agent="agent-a", vm="vm-a")
        tasks.append_claim(
            self.task.task_id, "takeover", agent="agent-a", vm="vm-a", session=INFLIGHT
        )
        self.assertEqual(tasks.active_claims()[self.task.task_id]["action"], "takeover")
        self.backdate_claim(0.5)
        self.assertTrue(self.classify().in_flight)

    def test_a_claim_past_the_lease_is_abandoned(self) -> None:
        self.backdate_claim(13.0)
        verdict = self.classify()
        self.assertFalse(verdict.in_flight)
        self.assertIn("past the 12h lease", verdict.reason)

    def test_the_lease_boundary_is_inclusive_of_a_fresh_claim(self) -> None:
        self.backdate_claim(11.9)
        self.assertTrue(self.classify(lease_hours=12.0).in_flight)

    def test_an_undated_claim_is_in_flight_and_says_the_age_is_unknown(self) -> None:
        from originlib import paths

        path = paths.claims_file()
        lines = path.read_text(encoding="utf-8").splitlines()
        entry = json.loads(lines[-1])
        entry.pop("ts")
        lines[-1] = json.dumps(entry, sort_keys=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        verdict = self.classify()
        self.assertTrue(verdict.in_flight)
        self.assertIsNone(verdict.age_h)
        self.assertIn("unknown age", verdict.note(INFLIGHT))

    def test_the_note_names_the_task_the_holder_and_the_age(self) -> None:
        self.backdate_claim(0.3)
        note = self.classify().note(INFLIGHT)
        self.assertIn("T-0001", note)
        self.assertIn("agent-a", note)
        self.assertIn("vm-a", note)
        self.assertIn("0.3h ago", note)


class VerifyGateTest(InflightFixture):
    """The gate as the CLI runs it, which reads the real clock and not `NOW`."""

    def test_strict_verify_passes_while_another_vm_is_in_flight(self) -> None:
        self.backdate_claim_now(0.5)
        self.assertEqual(self.cli("session", "verify", "--strict"), 0)
        self.assertIn(f"{INFLIGHT}: in flight", self.output())
        self.assertIn("T-0001", self.output())

    def test_strict_verify_fails_once_the_claim_is_expired(self) -> None:
        self.backdate_claim_now(13.0)
        self.assertEqual(self.cli("session", "verify", "--strict"), 4)
        self.assertIn("past the 12h lease", self.output())

    def test_the_lease_is_a_flag_not_a_constant(self) -> None:
        # This assertion is what expired: it dated the claim 13 hours before a
        # fixed 2026-10-03 and compared it with the real clock, so it passed
        # until 24 hours after that instant and never again. `backdate_claim_now`
        # makes it a claim that is 13 hours old, now and in a year.
        self.backdate_claim_now(13.0)
        self.assertEqual(self.cli("session", "verify", "--strict", "--lease-hours", "24"), 0)
        self.assertIn("in flight", self.output())

    def test_a_claim_older_than_the_widest_lease_is_still_abandoned(self) -> None:
        # The negative control the expired assertion needed: a longer lease moves
        # the threshold, it does not remove it. Dated from the real clock, so it
        # cannot pass because the calendar moved.
        self.backdate_claim_now(25.0)
        self.assertEqual(self.cli("session", "verify", "--strict", "--lease-hours", "24"), 4)
        self.assertIn("past the 24h lease", self.output())

    def test_the_fixed_clock_still_dates_a_claim_for_the_unit_tests(self) -> None:
        # The two clocks must not be interchangeable. A claim dated from `NOW` is
        # 13 hours old *to the classification tests* and grows older every hour
        # against the CLI, which is the defect; this asserts the fixed one is
        # still what `backdate_claim` produces, so the control above cannot be
        # satisfied by changing both.
        self.backdate_claim(13.0)
        verdict = self.classify()
        self.assertAlmostEqual(verdict.age_h or 0.0, 13.0, places=3)
        stamp = json.loads(
            paths.claims_file().read_text(encoding="utf-8").splitlines()[-1]
        )["ts"]
        self.assertEqual(stamp, ago(13.0))

    def test_strict_verify_still_fails_for_this_working_trees_own_session(self) -> None:
        # D013 is unchanged: a session running *here* is still a CI failure.
        session.start("local work", agent="tester")
        self.assertEqual(self.cli("session", "verify"), 0)
        self.assertIn("in progress", self.output())
        self.assertEqual(self.cli("session", "verify", "--strict"), 4)


if __name__ == "__main__":
    unittest.main()
"""Event stream behaviour: ordering, schema validation, durability."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from harness import RepoTest

from originlib import events, paths


class EventStreamTest(RepoTest):
    def test_append_assigns_contiguous_sequences(self) -> None:
        target = self.repo / "events.jsonl"
        for index in range(4):
            events.append("2026-10-03-001-x", "milestone", {"summary": f"m{index}"}, path=target)
        seqs = [event["seq"] for event in events.read(target)]
        self.assertEqual(seqs, [1, 2, 3, 4])

    def test_events_are_written_one_per_line(self) -> None:
        target = self.repo / "events.jsonl"
        events.append("2026-10-03-001-x", "note", {"summary": "one"}, path=target)
        events.append("2026-10-03-001-x", "note", {"summary": "two"}, path=target)
        lines = target.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 2)
        for line in lines:
            json.loads(line)  # must not raise

    def test_unknown_kind_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            events.append("2026-10-03-001-x", "invented_kind", {}, path=self.repo / "e.jsonl")

    def test_validate_reports_missing_fields(self) -> None:
        problems = events.validate({"schema": "wrong", "kind": "note"})
        joined = " ".join(problems)
        self.assertIn("missing field", joined)
        self.assertIn("unexpected schema", joined)

    def test_validate_flags_unknown_kind(self) -> None:
        event = {
            "schema": paths.EVENT_SCHEMA,
            "seq": 1,
            "ts": "2026-10-03T00:00:00+00:00",
            "session": "2026-10-03-001-x",
            "kind": "not_a_kind",
            "data": {},
        }
        self.assertTrue(any("unknown kind" in problem for problem in events.validate(event)))

    def test_malformed_line_is_preserved_not_dropped(self) -> None:
        target = self.repo / "events.jsonl"
        events.append("2026-10-03-001-x", "note", {"summary": "ok"}, path=target)
        with open(target, "a", encoding="utf-8") as handle:
            handle.write("{not json}\n")
        parsed = events.read(target)
        self.assertEqual(len(parsed), 2)
        self.assertIn("__malformed__", parsed[1])

    def test_next_seq_survives_a_malformed_tail(self) -> None:
        target = self.repo / "events.jsonl"
        events.append("2026-10-03-001-x", "note", {}, path=target)
        with open(target, "a", encoding="utf-8") as handle:
            handle.write("garbage\n")
        events.append("2026-10-03-001-x", "note", {}, path=target)
        self.assertEqual(events.next_seq(target), 3)

    def test_session_id_pattern(self) -> None:
        for good in ("2026-10-03-001-abc", "2026-10-03-012-abc-def"):
            self.assertRegex(good, events.SESSION_ID)
        for bad in ("2026-10-03-abc", "not-a-session", "2026-10-03-001-ABC"):
            self.assertNotRegex(bad, events.SESSION_ID)

    def test_all_sessions_ignores_unrelated_directories(self) -> None:
        (self.repo / "sessions" / "not-a-session").mkdir(parents=True)
        (self.repo / "sessions" / "not-a-session" / "events.jsonl").write_text(
            '{"schema":"origin.session.event/1","seq":1,"ts":"t","session":"x","kind":"note","data":{}}\n',
            encoding="utf-8",
        )
        self.assertEqual(events.all_sessions(), [])

    def test_summary_prefers_readable_fields(self) -> None:
        event = events.Event(1, "t", "s", "milestone", {"summary": "did a thing"}, {})
        self.assertEqual(event.summary(), "did a thing")
        fallback = events.Event(2, "t", "s", "milestone", {"path": "a/b.py"}, {})
        self.assertEqual(fallback.summary(), "a/b.py")
        bare = events.Event(3, "t", "s", "milestone", {}, {})
        self.assertEqual(bare.summary(), "milestone")


if __name__ == "__main__":
    unittest.main()
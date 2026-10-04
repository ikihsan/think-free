<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Decision log

Decisions that were genuinely open, the evidence behind them, the alternatives
rejected, and the reason. Decisions that constrain later work belong here;
ordinary edits do not.

| File | Decisions | Governs |
|---|---|---|
| [`DECISIONS-FOUNDATION.md`](DECISIONS-FOUNDATION.md) | D001–D010 | The mission, the workspace, and what counts as evidence |
| [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md) | D011–D012, D014–D018, D031, D033–D034 | Recording, moving, and publishing work |
| [`DECISIONS-SESSIONS.md`](DECISIONS-SESSIONS.md) | D013, D027–D028 | Whether a session is finished, and whose change a recorded path is |
| [`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md) | D019–D023 | What passes: candidate screens, kill-gate conditions, verdict metrics |
| [`DECISIONS-GATING.md`](DECISIONS-GATING.md) | D024–D026, D029–D030, D032, D035 | How this repository's own gates are written and run |

**The invariant that makes the split sensible.** A reader who needs to know *why
this mission is shaped this way* reads only the foundation file. A reader who
needs to know *what a session must produce and move* reads only the
practice file. A reader who needs to know *what passes* reads only the screening
file, and one who needs to know *how this repository verifies itself* reads only
the gating file. No entry appears in more than one file, and a new decision goes
in the file its own statement fits; never split one decision across the boundary.

Split at 2026-10-03 when this file reached the 300-line cap required by
[`docs/policy/doc-standards.md`](docs/policy/doc-standards.md). The entries were
moved verbatim; the numbering is continuous and unchanged, so any existing
reference to a decision id still resolves.

Split again at 2026-10-03 (T-0018) when `DECISIONS-PRACTICE.md` reached 297 of
the 300 permitted lines: D013 and D019–D023 moved verbatim to
`DECISIONS-GATING.md` by invariant, not by date.

**Newest decision:** see the end of
[`DECISIONS-GATING.md`](DECISIONS-GATING.md).

A recorded `decision` event satisfies this gate when **any** decision record
changed; `origin` checks all five files for that reason. See
[`docs/process/session-protocol.md`](docs/process/session-protocol.md).

Split a third time at 2026-10-03 (T-0020) when D024–D027 took
`DECISIONS-GATING.md` past the 300-line cap: D019–D023 moved verbatim to
`DECISIONS-SCREENING.md`. Every split is by invariant, never by date, and numbering
is continuous and unchanged in each, so an existing reference to a decision id
still resolves wherever the entry now lives.

Split a fourth time at 2026-10-04 (T-0030) when D030 reached 289 of
`DECISIONS-GATING.md`'s 300 permitted lines: D013, D027 and D028 moved verbatim to
`DECISIONS-PRACTICE.md`, which now carries D011–D018 and D027–D028. **This index
row is enforced, not descriptive:** the gate added in T-0030 reports a decision
that its own file's row does not list, and a listed id nothing defines. It
reported the gap in the row above on its first run, ten minutes after D030 was
written.

**The next gating decision cannot be recorded, and the reason is here rather than
in the file it wants.** `DECISIONS-GATING.md` is at 297 of 300 lines after D035,
and its own header records a split that was attempted and reversed on 2026-10-04
because two VMs were claiming incompatible invariants in the same hour. T-0036 made
a gating decision — one entry point, `tools/originlib/idcheck.py`, for the
identifier record that `doc lint` and `sync land` both read, over findings,
decisions, tasks **and** the numbered defect list, plus the obligation that a gate
which cannot read its input must report that — and it is written in
`tools/originlib/idcheck.py`, `tools/originlib/defectlist.py` and
[`docs/operations/ci.md`](docs/operations/ci.md) rather than here, because putting
it in whichever decision file had room is the mistake the reversed split was made
of. Recording the constraint in the log, and not only in the state file, is the
point: the next agent should find it where the decisions are. **The split is owed,
deliberately, on a quiet base.**

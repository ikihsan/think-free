<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Decision log

Decisions that were genuinely open, the evidence behind them, the alternatives
rejected, and the reason. Decisions that constrain later work belong here;
ordinary edits do not.

| File | Decisions | Governs |
|---|---|---|
| [`DECISIONS-FOUNDATION.md`](DECISIONS-FOUNDATION.md) | D001–D010 | The mission, the workspace, and what counts as evidence |
| [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md) | D011–D012, D014–D018, D031, D033–D034 | Recording and moving work |
| [`DECISIONS-SESSIONS.md`](DECISIONS-SESSIONS.md) | D013, D027–D028 | Whether a session is finished, and whose change a recorded path is |
| [`DECISIONS-PUBLISHING.md`](DECISIONS-PUBLISHING.md) | D040, D042, D044–D045 | What a command's own write is, and what must travel with it when published |
| [`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md) | D019–D023 | What passes: candidate screens, kill-gate conditions, verdict metrics, the rule that the next-action list must carry an invention item, and the two inputs a candidate may not borrow from each other |
| [`DECISIONS-SCREENING-2.md`](DECISIONS-SCREENING-2.md) | D048–D051 | What passes, continued: the two inputs a candidate may not borrow from each other, what a prior-art verdict must read before it may kill, and that a harvested corpus's population is measured before its yield |
<<<<<<< HEAD
| [`DECISIONS-SCREENING-3.md`](DECISIONS-SCREENING-3.md) | D052 | What passes, continued: a channel's absence from an instrument is not evidence the world uses it, and a count instrument reports the share of its population it cannot see |
>>>>>>> 6835146... records: F040 and D052 -- the copy channel is 0.12x the install channel, so item 0's third reading is answered and the screen's young-vocabulary premise is no longer in question
=======
| [`DECISIONS-SCREENING-3.md`](DECISIONS-SCREENING-3.md) | D053 | What passes, continued: a channel's absence from an instrument is not evidence the world uses it. Split from `-2`, which the other VM's D052 put at 293 of 300 lines |
| [`DECISIONS-GATING.md`](DECISIONS-GATING.md) | D024–D026, D030, D036–D039 | How a gate, a diagnostic, or its control must be written before it is trusted |
| [`DECISIONS-RECORDS.md`](DECISIONS-RECORDS.md) | D029, D032, D035, D041, D043, D046, D047 | What this repository's own records must be: a function of the tree, no number with two meanings, and two artefacts held to each other |

**Split a sixth time at 2026-10-05 (T-0063), when D051 took
`DECISIONS-SCREENING.md` to 324 of its 300 permitted lines.** D048–D050 moved
verbatim to `DECISIONS-SCREENING-2.md`. This is the first split in this log that
continues an invariant rather than narrowing one, and both headers say so: the
two files govern *what passes*, which is what
[`DECISIONS-SESSIONS.md`](DECISIONS-SESSIONS.md) could not claim after its own
second split and had to revert. Numbering is continuous and unchanged, so an
existing reference to a decision id still resolves wherever the entry now lives.

**The invariant that makes the split sensible.** A reader who needs to know *why
this mission is shaped this way* reads only the foundation file. A reader who
needs to know *what a session must produce and move* reads only the
practice file. A reader who needs to know *what a command wrote on the agent's
behalf, and what has to be published with it* reads only the publishing file. A
reader who needs to know *what passes* reads only the screening file, and one who
needs to know *how this repository verifies itself* reads only the gating file. No
entry appears in more than one file, and a new decision goes in the file its own
statement fits; never split one decision across the boundary.

The third file was added on 2026-10-04 (T-0054), and the reason is the pattern
this repository keeps meeting: the first split of this log moved entries to make
a file fit and was reversed within the hour. **A decision file has to have an
invariant before it has a line count**, and the one that governed
`DECISIONS-SESSIONS.md` after its second split did not cover the four entries it
held. A gate's reading of the header and the index is what catches that — two of
those entries would have stayed inconsistent with this table and with their own
file's header, and `decisionheader.py` reported both directions before the move.

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

Split a fifth time at 2026-10-04 (T-0042), when `DECISIONS-GATING.md` stood at
297 of the 300 permitted lines and **the next gating decision had nowhere to go**.
D029, D032 and D035 moved verbatim to
[`DECISIONS-RECORDS.md`](DECISIONS-RECORDS.md), and the decision T-0036 had to
leave in code — one entry point for every source of an identifier, and a rule
that cannot read its input reports that — is D036, in the file its own invariant
names. Every split is by invariant, never by date, and numbering is continuous
and unchanged in each, so an existing reference to a decision id still resolves
wherever the entry now lives.

Split attempted and reversed on 2026-10-04 (T-0030). D013, D027 and D028
were moved out to `DECISIONS-PRACTICE.md` because D030 had reached 289 of the 300
permitted lines — and `instance-20260717-0944`, working in the same hour, appended
D031 to that file. Both moves overflowed their destination: this one reached 323
lines, and the other put a fifth session-state decision where no other session-state
decision had ever been. The entries are therefore back where they were, and the
reason is recorded rather than the attempt: **a split is a claim about an
invariant, and the two VMs were claiming incompatible ones in the same hour.** A
file at 289 lines with a real invariant is a smaller problem than two files whose
prose contradicts each other. `DECISIONS-SESSIONS.md` now holds those three
entries and its own header names them, which the rule added in T-0042 checks.

**The index row above is not the only declaration, and for a while it was the
only checked one.** Each decision record also opens with its own
`Decisions **…**` header, and two of the five files had gone stale while this
table stayed correct: `DECISIONS-GATING.md` named D013 — which lives in
`DECISIONS-SESSIONS.md` — and omitted D030, D032 and D035, and
`DECISIONS-PRACTICE.md` named a `D011–D018` range covering three entries that had
moved out. The line under the title is the first thing a reader sees, and it is
now held by `tools/originlib/decisionheader.py` in both directions, so the three
sources of a decision number — heading, index row, header — must all agree.
>>>>>>> 8fea794... renumber to F041/D053/021 on this side: the other VM took F040 and D052 for a different experiment on the same reading

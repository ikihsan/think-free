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
| [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md) | D011– | Recording, verifying, publishing, and gating work |

**The invariant that makes the split sensible.** A reader who needs to know *why
this mission is shaped this way* reads only the foundation file. A reader who
needs to know *what a session must produce and what stops it* reads only the
practice file. No entry appears in both, and a new decision goes in the file its
own statement fits; never split one decision across the boundary.

Split at 2026-10-03 when this file reached the 300-line cap required by
[`docs/policy/doc-standards.md`](docs/policy/doc-standards.md). The entries were
moved verbatim; the numbering is continuous and unchanged, so any existing
reference to a decision id still resolves.

**Newest decision:** see the end of
[`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md).

A recorded `decision` event satisfies this gate when **any** decision record
changed; `origin` checks all three files for that reason. See
[`docs/process/session-protocol.md`](docs/process/session-protocol.md).
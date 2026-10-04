<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0050
status: done
created: 2026-10-04
claim-agent: opencode
claim-session: 2026-10-04-034-separate-the-line-cap-exemption-from-rec
claim-vm: instance-20260717-0947
verify: python3 -m unittest discover -s tests && tools/origin preflight
-->

# T-0050 — Separate the line-cap exemption from reconciliation, so a json/jsonl/l

## Goal

Separate the line-cap exemption from reconciliation, so a json/jsonl/log edit cannot pass undeclared

## Why this matters

Item 2(d) of STATE-next-actions.md, and the false negative defect 12's entry says it never measured: reconcile._is_vendored reuses doclint.is_exempt, which returns True for DATA_SUFFIXES because those files are exempt from the 300-line cap. Content the cap ignores is treated as content no session can change silently, so tests/python-versions.json, tests/git-versions.json and tasks/CLAIMS.jsonl can be edited with nothing declared and nothing reported - the opposite of the defect T-0047 closed, which fixed the false positives. A version record that decides whether this VM can run the work is exactly the kind of file that must not be editable undeclared.

## Preconditions

Measure the change's cost before making it: sweep every closed session's window for data-suffix paths that are not declared, so the new reports are a list rather than a surprise.

## Steps

1. Sweep every closed session: the data-suffix paths its commits touched that no artifact event declared, with the generated mark and the session's own directory excluded. Record the counts.
2. Split doclint.is_exempt into the two questions it was answering - a data suffix, which only the cap cares about, and a declared exempt: glob, which both do - and make reconcile._is_vendored read only the declared globs.
3. Declare the claim ledger the way the task file is declared: the appender records the path and the bytes it wrote, so task commands' own appends are silent and any later edit is reported.
4. Falsify both ways: remove the new clause and watch the new tests fail; run the rule over the sweep's own commits and over the tip.
5. Record the measurement, the ceiling and the sweep as a test, and close defect 12's stated residual.

## Acceptance criteria

The sweep is committed as a runnable script and its numbers are in the record, with the sessions and paths named - not a promise that the sweep would be clean.
The new tests fail against the unrepaired code: a .json and a .jsonl and a .log changed without declaring are reported, and the pre-repair rule reports none of the three.
tasks/CLAIMS.jsonl is declared by its appender with the digests of the bytes it wrote, silent while they match and reported after any later edit - the property defect 12 refused to trade away.
No data-suffix path is exempt from reconciliation because of its suffix: every remaining exemption is declared, hash-verified (vendored), generated, or the session's own directory.
preflight green and the sweep silent on the tip.

## Verification

```bash
python3 -m unittest discover -s tests && tools/origin preflight
```

## Rollback

Revert the doclint/reconcile split and the ledger declaration; nothing outside tools/ and tests/ depends on it.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

### The nine undeclared paths at `session finish`, and whose they are

`session finish` closed this session with nine `unlogged_change` events. **None of
the nine is this session's work.** Read with `git log -1 -- <path>`, every one is
the other VM's:

| path | last commit |
|---|---|
| `DECISIONS-RECORDS.md` | `91958d9` T-0051 |
| `docs/policy/doc-standards.md` | `26abba1` T-0051 |
| `docs/policy/gate-falsification.md` | `26abba1` T-0051 |
| `sessions/2026-10-04-035-*/commands.log` | `ec705c5` session 035 finished |
| `sessions/2026-10-04-035-*/events.jsonl` | `ec705c5` session 035 finished |
| `tasks/T-0051-*.md` | `91958d9` T-0051 |
| `tasks/T-0052-*.md` | `df14061` claim T-0052 |
| `tests/test_link_escape.py` | `26abba1` T-0051 |
| `tools/mutate_link_rule.py` | `26abba1` T-0051 |

**Why they were reported at all: defect 2's stated ceiling, reached through a
message.** `sync land` stopped on a real content conflict in `STATE.md` and
`STATE-defects.md` and said *resolve it and land again*; the conflict was
resolved, and the rebase then had to be completed with a hand-run
`git rebase --continue` because the conflict resolution left the tree dirty and
`land` refuses a dirty tree. A hand-run rebase records **no `base_advance` event**,
and this session's stream carries none — checked, not assumed. So the base move
that brought the other VM's T-0051 and T-0052 into this branch is invisible to
attribution, and every path it carried stays reported. That is the ceiling
`landed.py` documents in its own words: *"The tooling never silences a file it
cannot prove belongs to someone else."*

**It is the same instance defect 2 and D039 both name, for the third time.** The
gap D039 closed was a refusal the tool could not follow; here the tool's
instruction was followable and the *following* of it was what left the record
short, because the step that follows a resolution is the one step the tooling
does not own. This is worth its own task rather than another line in defect 2's
entry: **`sync land` should record the base move for a rebase it stopped on even
when the human completes it** — the arrived commits are readable from git's own
`REBASE_HEAD` and the `base_advance` write does not need the tooling to have run
the continuation.

**Not repaired here, deliberately.** The stream is closed and is not edited, and
the session that could have declared those paths is not this one. Repairing it
here would mean either fabricating declarations for work another VM did or
leaving the tree in a state the next reader has to unpick.


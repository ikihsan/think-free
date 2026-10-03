<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0020
status: done
created: 2026-10-03
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin session verify --strict && tools/origin doc lint
-->

# T-0020 — Distinguish an in-flight session from an abandoned one in `session verify`

## Goal

Tell an in-flight session apart from an abandoned one in session verify, so one VM's live session stops reddening every other VM's build

## Why this matters

STATE.md next action 1 is an open question nobody has answered: 'on a pushed commit nothing is in flight' (D013) is false for this fleet, because task claim requires HEAD to equal the remote base, so a claiming VM must publish its session start first (observed in dfa6eb9 -> 4791ed3 on 2026-10-03). The result is that every push on every VM is red at the Session record integrity step while any session is open. Measured: run 37157528596 is the only red step on an otherwise all-green build. A gate that is red for a non-defect trains everyone to ignore it, so the fix has to keep D013's protection while stopping the false red.

## Preconditions

A live claim ledger and task files on the base branch (both exist); a real in-flight session from another VM to check the fix against (2026-10-03-030 exists on this branch).

## Steps

1. Write the classification as a separate module with one predicate, and the reason for each clause in its docstring. 2. Derive in-flight status from the tree alone: the session_start names a task, that task file says status claimed, its claim identifies this session (by claim-session, else by claim-agent plus claim-vm), and the ledger's last action for that task is claim or takeover. 3. Add a lease: a claim older than --lease-hours (default 12) is abandoned, not in flight, so a dead VM's session fails the gate instead of hiding forever. 4. Wire it into verify_sessions for both strict and non-strict, and keep --strict failing for the locally active session (D013 unchanged). 5. Print, per in-flight session, the task, holder, and claim age, so a pass is visibly a pass. 6. Re-emit those lines as ::warning:: annotations in ci.yml so the CI log names them without admin rights. 7. Add tests for each clause and for the expiry boundary, including the negative cases.

## Acceptance criteria

- [ ] `session verify --strict` exits 0 in this repository while `2026-10-03-030`
      is genuinely in flight on the other VM
- [ ] Every clause of the classification has a negative test, so a wrong
      classification is a failing test rather than a silent pass
- [ ] A claim older than the lease fails the gate
- [ ] The in-flight line names the task, the holder, and the claim age
- [ ] The full test suite and `doc lint` pass

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin session verify --strict && tools/origin doc lint
```

## Rollback

Revert the module, the verify_sessions branch, the flag, and the ci.yml step. No data format changes: an unfinished session with no task on record already failed before and still fails.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

**Two defects found before the work started, by running the documented
sequence** (both `FAILURES.md` F012, `FAILURES-findings-3.md`):

1. `worktree add` refused the claiming VM's own claim, so step 3 of
   `docs/operations/vm-execution.md` — claim, then isolate — could not be
   executed. Now refuses only a claim held by a *different* VM.
2. `worktree.WorktreeError` and `sync.SyncError` escaped `cli.main` as
   tracebacks. Now exit `1` with one stderr line.

**A third, in the code this task reads:** `tasks.active_claims()` ignored the
`takeover` ledger action while `taskremote.remote_active()` honoured it, so the
local and remote views of a task's holder disagreed after every takeover (F013).
The classification below reads the ledger, so it would have inherited that.

**Design note.** The classification deliberately reads the *whole* ledger rather
than `tasks.active_claims()`: a refusal that can name the closing action ("the
last action is `complete`") tells an operator what to fix.

**Deliberately not done:** publishing claims on a separate ref so in-flight
sessions never reach the base branch. Rejected in D024 — it hides the claim from
`sync land` and from a reader browsing the base branch.

**Not verified here:** a pushed CI run. Local `session verify --strict` exits 0
while session 030 is in flight; whether the workflow step behaves the same is a
claim for the run that lands this branch.

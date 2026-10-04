<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Session protocol

Every working session follows these steps. The goal is that a session's record
is complete and checkable without trusting the agent that produced it.

## The short version

```bash
tools/origin session start --goal "one sentence" [--task T-0001] [--agent name]
tools/origin session step "milestone reached"
tools/origin session artifact path/to/file
tools/x -- <command>
tools/origin session finish --outcome worked --summary "…" --next "…"
```

## 1. Start before you touch anything

`session start` records the goal, the agent, the host, the branch, the commit
you started from, and which files were already dirty. Starting afterwards is
the one unrecoverable mistake: reconciliation needs the starting commit to tell
your changes from the ones that were already there.

Only one session may be open per working tree. `tools/origin session status`
tells you which. A leftover pointer means a session ended without `finish`;
finish it or delete `sessions/active.json` deliberately, having checked
`session verify` first.

On a shared repository, `session start` also fetches the remote and
fast-forwards onto the shared base before recording anything. A tree that
diverged, or a tree with uncommitted changes while the remote moved, is
refused — the session never starts from a state nobody else has seen, and
never merges. The starting event records the remote commit the work branched
from.

## 2. Declare artifacts, do not just write files

`tools/origin session artifact <path>` records a file you produced together with
its SHA-256 and size. Use it for anything a reader would want to verify:
reports, experiment results, task files, decisions.

Artifacts are refused when they contain something matching a credential
pattern, because the file itself is the exposure. Redacting an artifact would
corrupt it, so the correct response is to fix the file.

**In practice, declare every file you change, not only the interesting ones.**
`session finish` reports any changed-but-undeclared path as an
`unlogged_change`, so the real choice is between a declared file and a reported
gap. Three consecutive sessions chose the gap — session 012 closed with 24
events, session 015 with 4 — and neither could be logged afterwards, because a
closed stream accepts nothing. The tool cannot tell an interesting file from a
dull one; it can only tell a declared one from an undeclared one.

**Commit the work with the paths it names, not `git add -A`.** `session finish`
rewrites the session's own report and `sessions/INDEX.md`, so a `git add -A` in
the work commit sweeps the session-finish commit's contents into the commit
before it: that commit then has nothing to carry and lands empty, while `git
log` still says `session: … finished (worked)`. Observed on session 025
(T-0043) on 2026-10-04, and it is the same shape as the recorded repairs to the
generated indexes — the artifact belongs to the commit that is about it.

## 3. Route evidence-producing commands through `tools/x`

```bash
tools/x -- python3 EXPERIMENTS/001-foo/run.py
```

`tools/x` runs the command, captures stdout and stderr separately into
`sessions/<id>/commands.log`, records argv, exit code, duration, and the exact
log lines, then exits with the command's own exit code. It is transparent
inside pipelines.

Commands run outside `tools/x` are not captured. That is acceptable for
throwaway inspection, but anything a conclusion depends on must be captured.

### 2a. Nothing you record may leave a generated file stale

`doc lint` fails when a committed generated file differs from what its generator
produces, and the session report is rendered from the event stream. So **every
event you record invalidates the report**, and a commit made before it is
rewritten publishes a stale one — a red CI run, observed as
`37180487906` after a capture and an artifact recorded between two commits. Every
appending command rewrites the report as part of recording (`session step`,
`note`, `decision`, `block`, `experiment-result`, `artifact`, and `tools/x`), so
this is not a step to remember. It is recorded here because it was once a step to
remember, and because the general form matters: **when you change a generated
file's input, the regeneration belongs in the code that changes the input**, not
in the command that happened to be running when someone noticed.

If a commit of yours is red on the Documentation step with a *stale generated
file*, the cause is an event recorded after the last write, and `tools/origin
doc index` is the repair.

Secrets in captured output are redacted before they reach disk, and the
redaction is itself recorded. Terminal output is not redacted, so do not print
a credential in the first place.

## 4. Record decisions as you make them

```bash
tools/origin session decision "chose X over Y because Z" --refs docs/...
tools/origin session experiment-result E001 "baseline was sufficient" --refs EXPERIMENTS/001-...
tools/origin session block "needs a VM with GPU"
```

These are not decoration. On `finish`, a `decision` event that is not matched by
a change to any decision record becomes an `integrity_error`. The log is split
by invariant across `DECISIONS.md` (index), `DECISIONS-FOUNDATION.md`,
`DECISIONS-PRACTICE.md`, `DECISIONS-SCREENING.md`, and `DECISIONS-GATING.md`,
so *any one* of them satisfies the check — demanding all five would report a
gap on every correct session. The same applies to
`experiment_result` and `HYPOTHESES.md`, `FAILURES.md`, and `block` and
`STATE.md`. The tooling enforces that the record and the documents agree.

## 5. Finish: reconcile, then close

`session finish` does five things in order:

1. **Reconciles.** Compares this session's changes against declared artifacts.
   Anything changed but undeclared becomes an `unlogged_change` event.
2. **Checks declarations still exist.** A declared artifact that has since been
   deleted becomes an `integrity_error`.
3. **Checks documentation obligations.** Mission records implied by this
   session's events that did not change become `integrity_error`.
4. **Records `doc_update` events** for mission records that did change.
5. **Closes the stream**, removes `sessions/active.json`, and regenerates the
   session report and `sessions/INDEX.md`.

It exits `4` when reconciliation found something unlogged or missing. Read the
output. Either declare the files or revert them. Do not paper over the report.

### Whose change is it

"Changed since the session started" is not the same question as "changed by this
session", and on a shared branch the difference is another VM's work. When
`sync pull` or `sync land` moves the base while a session is open, it appends a
`base_advance` event naming the commits that arrived. Reconciliation then treats
a path as the base's contribution when the newest thing to touch it is one of
those commits, and as this session's own when the newest thing is one of its own
commits or an uncommitted edit. Excluded paths are printed under `LANDED` at
`finish`, so nothing is dropped silently.

The rule is deliberately one-sided: a base move performed with raw git records
nothing, so its paths stay reported. Silence is only ever justified by a record.

## What "logged perfectly" means here, honestly

Logging is cooperative. An agent can forget. What this design guarantees is that
forgetting is **visible**:

- undeclared changes are detected by comparing git against the record;
- missing or duplicated session lifecycle events fail `session verify`;
- command events point at log line ranges that must exist;
- committed generated reports must match what the generator produces now;
- documentation obligations are cross-checked against event kinds.

The honest claim is "gaps are detected", not "nothing is ever missed".

## Verify

```bash
tools/origin session verify     # every session, every event
tools/origin preflight          # lint + skills + sessions + release check
```

**A task's `verify` must include every gate its change can break, and `preflight`
is where a new gate goes.** T-0042 added a root-level document, classified
nothing in [`RELEASE-MANIFEST.md`](../../RELEASE-MANIFEST.md), and its `verify`
passed — because the command ran the suite, `doc lint` and `preflight`, and
`preflight` did not run `release check` (T-0045). The general rule is the one the
generated-file repairs already state for another layer: **a gate belongs in the
single command this protocol tells every agent to run**, so a change that adds a
document, a session, a skill or an identifier cannot pass verification without
meeting the gate that reads it.

`verify` checks: contiguous sequences, exactly one `session_start` and at most
one `session_end`, the last event is `session_end` (or the session is reported
unfinished), valid session ids, a report for every session, and that every
command event's log lines exist.

An unfinished session is judged by *whose* it is, not merely by existing:

- the session running in this working tree is `in progress` locally and a
  failure under `--strict` (D013);
- a session on another VM is `in flight` while its task claim proves it is still
  being worked on, and `abandoned` — a failure — otherwise. The predicate is
  [`../../tools/originlib/inflight.py`](../../tools/originlib/inflight.py) and
  the reasoning is D025 in
  [`DECISIONS-GATING.md`](../../DECISIONS-GATING.md).

## Recovery after an interruption

```bash
tools/origin session status
tools/origin session resume            # goal, outcome, decisions, last events
tools/origin session finish --outcome partial --summary "…" --next "…"
```

An unfinished session is not an error. It is a session whose `session_end` is
missing, and `verify` says so. Finish it honestly rather than deleting it.

## Multi-machine note

Each session writes its own `events.jsonl` under its own directory, so two
sessions on different branches never conflict. `sessions/INDEX.md` is generated
and may need regenerating after a merge; that is expected, not corruption.

A session that is in flight on another VM is *expected to be visible on the
shared base branch*, because `task claim` cannot publish a claim atomically
unless the session's own start record is already there. `verify` therefore
distinguishes in flight from abandoned rather than treating both as unfinished;
see [`operations/ci.md`](../operations/ci.md).

With `--push`, `session finish` commits only the session's own files and pushes
the branch. Uncommitted work of your own is refused, not auto-committed, so the
record and the work travel together. See
[`multi-vm-coordination.md`](multi-vm-coordination.md) for the full contract.
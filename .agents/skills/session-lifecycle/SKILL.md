---
name: session-lifecycle
description: Mandatory opening, logging, and closing of every working session in this repository. Use at the START of any session that edits files or runs evidence-producing commands, and again before finishing. Triggers - "start a session", "log this", "finish the session", "what did we do", "record this decision", "before I commit", or any session that touches code, documents, or experiment results.
license: MIT
compatibility: agent-agnostic
metadata:
  scope: repository-wide
  enforcement: tools/origin session finish
---

# Session lifecycle

The repository's memory is files in git, not conversation context. This skill
is how what happened in a session becomes part of that memory.

Full protocol: [`docs/process/session-protocol.md`](../../../docs/process/session-protocol.md).
Record format: [`docs/policy/logging-standard.md`](../../../docs/policy/logging-standard.md).

## Before touching anything

```bash
tools/origin session status                      # is a session already open?
tools/origin session start --goal "one sentence, imperative"
```

The goal is one sentence describing what this session will produce. "Fix the
parser bug" is a goal; "work on the project" is not.

`--task T-0001` associates the session with a task file, which matters when
several machines share this repository. `--agent` overrides runtime detection,
which a VM runner should always set.

Starting after you have already edited files is the one unrecoverable mistake:
reconciliation needs the starting commit to tell your changes from the ones that
were already there.

## While working

Log a milestone when you finish a step, not at the end:

```bash
tools/origin session step "parser now handles both response shapes"
```

Record decisions the moment you make them, not when you remember them later:

```bash
tools/origin session decision "chose a fixed-point render over suppressing
  self-summaries, because suppression loses information" --refs tools/originlib/docindex.py
```

Declare files you produced. The hash is what makes them checkable:

```bash
tools/origin session artifact docs/reference/skill-inventory.md
```

Run anything whose output a conclusion depends on through the wrapper:

```bash
tools/x -- python3 -m unittest discover -s tests
tools/x -- ./tools/origin doc lint
```

`tools/x` captures output and the exit code, redacts secrets, and exits with
the command's own status. A conclusion with no captured command behind it is an
assertion, not a result.

Record blockers explicitly:

```bash
tools/origin session block "cannot reproduce the trace: fixture URL now 404s"
```

## Before finishing

```bash
tools/origin doc index                          # regenerate generated files
tools/origin doc lint                           # must exit 0
tools/origin session finish --outcome worked \
  --summary "what actually happened" \
  --next "the single most useful next action"
```

Outcome values, chosen honestly:

| Outcome | Use when |
|---|---|
| `worked` | The stated goal was achieved |
| `partial` | Some of it was achieved; say exactly what |
| `failed` | It did not work; say what was learned |
| `no-change` | Investigation only, nothing modified |

`--next` is not optional and must be actionable. "Continue investigating" is not
a next action; "run the A1 masking experiment against the PPNA extract" is.

## Reading the finish report

`finish` reconciles git against your declared artifacts and prints what it
found. Three outcomes need action:

- **`UNLOGGED`** — you changed a file without declaring it. Run
  `tools/origin session artifact <path>` for each, or revert it. Do not suppress
  the report.
- **`MISSING`** — you declared a file that no longer exists. Either restore it or
  record why it was removed.
- **`DOC GAP`** — you recorded a decision but `DECISIONS.md` did not change. Edit
  `DECISIONS.md` in this same commit.

Exit code `4` means the reconciliation found something. A clean exit means the
record and the repository agree.

## Resuming

```bash
tools/origin session resume            # goal, outcome, decisions, last events
tools/origin session verify            # integrity across every session
```

An unfinished session is reported, not hidden. Finish it honestly rather than
deleting it: `verified at commit abc1234, stopped mid-refactor` is useful
information; a missing session is not.

## Rules

1. One active session per working tree. Never nest.
2. Never edit `events.jsonl` by hand. It is append-only by contract.
3. Never declare an artifact containing a credential. The tooling refuses; fix
   the file, and rotate the credential if it was real.
4. Never write `--summary` describing intent. It describes outcome.
5. Every session that commits something leaves `STATE.md` no staler than it
   found it.
<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Reading a red CI run

How to find out which test failed on a pushed commit, without repository admin
rights. Split out of [`ci.md`](ci.md) on 2026-10-04 when that file reached 312 of
the 300 permitted lines; the stub there is the entry point, this file is the
whole method. Evidence for every number below is `FAILURES.md` F020, measured
from the public API on 2026-10-04.

## The run log is not the only way in

`GET /repos/{owner}/{repo}/actions/runs/{id}/logs` needs admin rights on a private
repository, and this repository is private. F019 spent an hour of elimination
before establishing that, and recorded the reason as "the public check-runs API
returns no annotations". **That reason does not hold.** The annotations are
public; they were simply not where the first reading looked, and for three of
the five gate steps there were none to find until `origin annotate` made them
(*A red gate names its file*, below).

## Two calls

```bash
OWNER=ikihsan; REPO=think-free

# 1. jobs, rows and check-run ids for one commit
curl -s "https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/check-runs"

# 2. the messages for one check run, one annotation per line
curl -s "https://api.github.com/repos/$OWNER/$REPO/check-runs/$ID/annotations"
```

The `Tests` step emits `::error::` lines, so a `Tests` failure annotates the
failing test's id, its file and its line — verbatim, from run `37178057818`:

```
FAIL: test_this_vms_versions_are_exercised_against_the_real_records (test_doctor_versions.RealRecordTest…)
File "/home/runner/work/think-free/think-free/tests/test_doctor_versions.py", line 69
AssertionError: 'unrecorded' != 'exercised'
```

That is F019's cause — the runner's git 2.55.0 absent from
[`../../tests/git-versions.json`](../../tests/git-versions.json) — read off the
run instead of reproduced on a VM, and the same seven rows it names were red on
run `37179073002`.

## Four answers, and only one of them is "nothing"

| What you see | What it means |
|---|---|
| Annotations, one starting `FAIL:` or `ERROR:` | The `Tests` step emits. Read them. Every one of them carries `path: .github`, because that step emits no `file=` — see *`path` is the property you asked for* below. |
| One annotation per violation, its `path` equal to a file in the repository | A file-reading gate emits, through `origin annotate` (T-0040). `observed` on run `37191658964` |
| Three annotations, the failure being `Process completed with exit code N` | The step emitted nothing naming its violation. Every gate step now runs through the annotator and through `always()`, so on the tip this shape means the step is one that has not been converted, or the run predates 2026-10-04 |
| No annotations object, or `annotation_count: None` | The jobs endpoint has none. The field a check run carries is `output.annotations_count`, and on run `37178057818` it read 11 |
| HTTP 403 | The unauthenticated rate limit: 60 requests an hour per IP, and this VM has no token in its environment |

**Check `/rate_limit` before concluding anything from a 403.** A failed call and
an empty list are different answers, and treating the first as the second is how
this repository recorded a false premise for two sessions.

The general form is D030 (`[../../DECISIONS-GATING.md`](../../DECISIONS-GATING.md))
one domain out: a diagnostic must distinguish "never configured" from "stopped
working". Here it is four states, and a tool that collapses the last three into
"no annotations" is confidently wrong.

## Ceiling

The messages are the workflow's own emission, capped by the `awk` window in the
`Tests` step at 60 lines, so a run with more failures than that annotates a
prefix of them. Nothing here verifies a conclusion — it names a test, so the
conclusion can be checked on a VM, which is where F019's cause was actually
settled. And one run's rows need not agree: run `37178057818` annotates a second,
different test on its 3.11 row, which no single-cause explanation covers.

## A red gate names its file: `origin annotate`

The `Tests` step re-emits failing tests itself. The five file-reading steps ran
the gate, printed its report, and exited, so the check run's only annotation was
`Process completed with exit code 2` — which is what the three of the four answers
above are. Since T-0040 each of them runs `tools/origin annotate -- <gate>`
instead, which runs the same gate in process and prints one command per
violation:

```
$ tools/origin annotate -- doc lint          # on a tree with two planted violations
::error file=STATE.md,line=4::STATE.md: broken link -> nowhere.md
::error file=docs/INDEX.md::docs/INDEX.md: generated file is stale; run 'tools/origin doc index'
```

Run the same string locally and you reproduce the run you cannot read. The
modules are [`../../tools/originlib/annotate.py`](../../tools/originlib/annotate.py)
(which gates exist and what they exit with) and
[`../../tools/originlib/finding.py`](../../tools/originlib/finding.py)
(a violation that knows where it is, and the escaping).

**Three properties, each a test** in
[`../../tests/test_annotate.py`](../../tests/test_annotate.py):

| Property | Why it is not the obvious thing |
|---|---|
| The `file` and `line` come from the rule's **structured** fields | A renderer that parsed the leading path out of the message would be right on most `doc lint` violations and wrong on `identifier collision: …`, which starts with a word. That is D025's shape: reading the field you happened to look at |
| A tree every gate accepts emits **no** `::` line | A renderer that always annotates looks exactly like one that found something |
| A `path` that is a directory or absent, and a `line` past the end of the file, are dropped | `skills check` reports `.claude/skills/<name>` for a mirror that is a real directory, and a generated index can be shorter than the line the previous commit recorded |

**Escaping is the toolkit's, and this file used to have it wrong.** In a message
`%` is `%25`, CR is `%0D`, LF is `%0A`; in a property value `:` is `%3A` and `,`
is `%2C` (`source-supported`, read from
`packages/core/src/command.ts` in `actions/toolkit` on 2026-10-04). The awk in
the workflow's `Tests` step doubled the percent, which renders one `%` as two —
defect 13. Nothing measured it, because no recorded annotation carried a percent.

## `path` is the property you asked for

`observed` 2026-10-04, from the four runs captured raw by
[`../../EXPERIMENTS/010-annotation-rendering/`](../../EXPERIMENTS/010-annotation-rendering/).
GitHub files an annotation on the workflow command's `file=`. Run `37191658964` at
`c9e89e1`, where `Tests` passed on the 3.12 row and `Documentation lint` alone failed,
carries `path: DECISIONS-RECORDS.md`, `start_line: 0`, message
`DECISIONS-RECORDS.md: tracked at the top level but classified by neither manifest
table` — the annotator's `::error file=DECISIONS-RECORDS.md::…` verbatim. `start_line`
is 0 because that violation names no line, which is the whole-file case T-0040 planted.

Two statements in this file used to say otherwise, and both were read off this endpoint:

- **The rendering was called `unmeasured`, beside a run that showed `path: .github`.**
  That string came from run `37189825232`, whose `Tests` step failed — so **the
  annotating steps never ran.** Its 11 annotations are all `path: .github`, all titled
  `Test failed`, all from the `Tests` step, which emits `::error title=Test failed::`
  with no `file=`. The `::error file=tools/originlib/identifiers.py::…` among that run's
  messages is the first line of a unittest assertion diff (`AssertionError: Lists differ:
  ['::error file=…'] != []`), re-emitted by the same awk. A test's expected text read as
  an emitted command.
- **`.github` is what a *fileless* command gets.** Run `37192717297` is green and carries
  three annotations, all `path: .github`: the runner's Node deprecation warning, the
  `ubuntu-latest` notice, and the session step's in-flight `::warning`. So `.github` is
  the default for a command with no `file=`, and is not a verdict on one that has it.

That is D025 reached twice from one run: a conclusion about `file=` drawn from the field
that does not carry it. `FAILURES.md` F021 records it; the two runs whose annotating steps
were skipped are defect 18.

## A skipped gate is indistinguishable from a passing gate

Each of the five file-reading steps carried `if: matrix.python-version == '3.12'`, and a
step whose `if:` expression names no status function gets an implicit `success()`. A red
`Tests` step therefore skipped all five: on runs `37189825232` and `37190842104`,
`Release manifest`, `Skill layout and mirrors`, `Vendored content integrity` and
`Session record integrity` did not run at all, and nothing in the annotations says so.
Every step whose purpose is to emit a diagnostic now says `always() && …`, and
`tests/test_ci_annotations.py` fails on a workflow that does not — the assertion was run
against the workflow as it was, and it named the step and its expression.

## Measure the renderer on the run that needs it: `origin probe`

Seven annotations, one per rendering shape, on every run — green or red — so the run that
reports a failure also carries the reference for reading it. `tests/test_probe.py` holds
the shape list literally, so a shape cannot be dropped from the code, the test and this
table together.

| Shape | Command property | What it settles |
|---|---|---|
| `filed-with-line` | `file`, `line` | that `start_line` comes back as the line emitted |
| `filed-no-line` | `file` | the `start_line: 0` case arm A observed, re-measured |
| `message-percent` | `file`, a `%` in the message | that `%` arrives escaped and cannot split the command |
| `message-colon-comma` | `file`, `:` and `,` in the message | that a colon and a comma are data in a message |
| `message-newline` | `file`, a newline in the message | that it arrives as one annotation, not two commands |
| `warning-level` | `file`, level `warning` | that a level other than `error` is filed too |
| `no-file` | neither | what a fileless command looks like, beside a filed one |

It exits 0 whatever the tree says and emits only `notice` and `warning`, both of which a
green run already publishes — a measurement that can redden the run it measures is a
measurement that gets deleted after its first false alarm. `::error` with a `file=` is the
shape the gates emit, and arm A already observed it.

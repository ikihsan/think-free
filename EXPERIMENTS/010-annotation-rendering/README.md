<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-04
-->

# 010-annotation-rendering

Task T-0046. Does GitHub file a check-run annotation on the workflow command's
`file=` property, and where does that property end up when it does not?

**This experiment was scoped from a reading that was already wrong**, and saying
so first is part of the record. `docs/operations/ci-diagnosis.md` claimed the
rendering was `unmeasured` and quoted run `37189825232` beside that claim: an
annotation carrying `::error file=tools/originlib/identifiers.py::…` whose own
`path` was `.github`. Both came from the public endpoint, and neither survived a
second reading. So the measurement below was not designed before the question was
asked — it was designed after the first answer was found to be an artefact, which
is a weaker position and the reason the arms below are chosen to make a *second*
misreading visible rather than to be elegant.

## The claim under test, in one sentence with its scope

**For a `verify` job in this repository on `ubuntu-latest`, an annotation produced
by `::error file=<repo-relative path>[,line=N][,title=T]::<message>` is filed by
GitHub with `path` equal to that path; an annotation from a command carrying no
`file=` is not filed on any path of this repository's documents.**

Scope, stated because the claim is scoped: this repository, one workflow, the
`ubuntu-latest` runner image, and GitHub's current renderer. It is **not** a claim
about other repositories, other runners, or `::group::`/`::set-output`.

## Arms

Four runs, because a single run cannot answer this: the runs differ in whether
the annotating step ran at all, and that difference is the whole trap.

| Arm | Run | Head | Rows | What it is |
|---|---|---|---|---|
| A | `37191658964` | `c9e89e1` | only `verify (3.12)` red; `Tests` green on it | **the arm that measures.** `Documentation lint` alone failed, so `origin annotate` emitted one command with `file=` and no `line=` |
| B | `37189825232` | `ea3bfb5` | all seven red, `Tests` among them | the run the record quoted. `Tests` failed, so every later step with an `if:` was skipped |
| C | `37190842104` | `f566ff0` | all seven red, `Tests` among them | B's shape on a different defect, so B is not a one-off |
| D | `37192717297` | `cfaf4ed` | green | **the control.** A clean tree must produce no annotation from the annotator, and the three it does carry say what a fileless command looks like |
| E | `37196459285` | `5f88354` | only `verify (3.12)` red, on the session step | **added after the four above ran**, and labelled rather than folded in: the first pushed run on which `origin probe` executed, so it is the measurement the other four only set up |

## Kill gate, declared before the fetch

If arm A's gate-step annotation has a `path` that is not the emitted `file=`
value, then the mechanism does not deliver what `docs/operations/ci-diagnosis.md`
claims, the document changes, and the emitter is at fault. If arm A's `path` *is*
the emitted `file=` but arms B and C's `path` is `.github` beside an emitted
`::error file=…`, then the emitter is not at fault and the run is — which is a
different repair entirely, in a different file.

A gate that only one arm can fail is not a falsification, which is why D is in the
list: without it, "the `path` is `.github`" and "the `path` is the file" are both
consistent with a renderer that always says `.github`.

## Arms B and C were expected to carry the annotator's output

They do not, and that is the result. Every one of B's 11 annotations and C's 10
is `path: .github` with the title `Test failed`, which is the `Tests` step's
`::error title=Test failed::` — a command with **no** `file=`. Neither run has a
single annotation from the annotator, because a step whose `if:` expression names
no status function gets an implicit `success()` and the red `Tests` step skipped
all five gate steps. Defect 18, repaired in T-0046.

The `::error file=tools/originlib/identifiers.py::…` string that B's messages do
carry is the first line of a unittest assertion diff — `AssertionError: Lists
differ: ['::error file=…'] != []` — re-emitted by the same awk that re-emits test
failures. It is a test's *expected* text. Reading it as an emitted command is the
D025 shape twice over: a conclusion about the renderer drawn from the one field of
the one run where the renderer never spoke.

## Results

`observed` 2026-10-04, from the raw captures in `raw/`.

| Arm | Annotations | Distinct `path` | The reading |
|---|---|---|---|
| A | 4 | `.github`, `DECISIONS-RECORDS.md` | the annotator's `::error file=DECISIONS-RECORDS.md::…` is filed as `path: DECISIONS-RECORDS.md`, `start_line: 0`, message verbatim. **The renderer files it.** |
| B | 11 | `.github` | all `Test failed`; no annotator output, because its steps were skipped |
| C | 10 | `.github` | as B, on a different defect |
| D | 3 | `.github` | green run: the runner's Node deprecation warning, the `ubuntu-latest` notice, and the session step's in-flight `::warning` |
| E | 11 | seven paths, one per probe shape | every shape filed on the path it named, `start_line` equal to the line emitted, and the escaped message whole |

**`start_line: 0` is not a defect.** Arm A's violation names no line — it is
`release check`'s whole-file verdict on `DECISIONS-RECORDS.md` — so no `line=` was
emitted and there is nothing for GitHub to report. The planted `line=4` and `line=9`
cases in `tests/test_annotate.py` cover the other half.

**`.github` is the default for a fileless command.** Arm D shows three, all from
commands that carry no `file=`, and arms B and C show eleven more. So `.github` is
the answer to "no path was given", not a verdict on "a path was given and
discarded". Confounded by construction until D is read: B and C on their own are
consistent with a renderer that ignores `file=` entirely, which is the reading the
record held.

## Arm E: what the probe measured on its first run

`observed` 2026-10-04 on run `37196459285` at `5f88354`. Seven shapes, seven
annotations, and every question the four arms left open is now answered by a run
rather than by a reading of one:

| Shape | Emitted | Came back as |
|---|---|---|
| `filed-with-line` | `file=STATE.md,line=7` | `path: STATE.md`, `start_line: 7` |
| `filed-no-line` | `file=MISSION.md` | `path: MISSION.md`, `start_line: 0` |
| `message-percent` | `50%25 of this sentence…` | `50% of this sentence…` |
| `message-colon-comma` | `keys: a, b; c — …` | identical, colon, comma and em dash intact |
| `message-newline` | `two%0Alines…` | `two\nlines…` — **one** annotation, and the newline survived |
| `warning-level` | `::warning file=README.md,line=1::` | `path: README.md`, `start_line: 1`, level `warning` |
| `no-file` | `::notice::` | `path: .github`, `start_line: 19` |

Two of those were the ones worth having. `line=` fidelity was never observed
before: `start_line` is the line emitted, so a reader gets a position and not a
file. And a `warning` **with** a `file=` is filed on the path, where the same
level **without** one is `.github` — so the two cases are distinguishable on the
run that needs them, which is the whole reason the probe is in the workflow.

## What this still does not settle

- **A `file=` value containing `:` or `,`.** This repository has no file whose name
  contains either, so the property escaping has no real input here; a synthetic one
  would measure a path that cannot exist. The escaping stays
  `source-supported` from `actions/toolkit`'s `command.ts` and nothing more.
- **GitHub's own annotation cap**, and the 60-line window inherited from the `awk`.
  Four runs have produced at most 11 annotations, so nothing here comes near
  either number.
- **Whether an `::error` annotation can change a green job's conclusion.** Never
  put to the platform, deliberately: the probe emits only levels a green run
  already publishes. The gates emit `::error` and exit non-zero, so nothing
  depends on the answer.
- **Rows other than 3.12.** The gate steps and the probe are guarded to one row,
  so the other six rows' annotations come from the `Tests` step alone.
- **Another renderer, another runner image, another repository.** One workflow on
  `ubuntu-latest` is the whole scope.

## Reproduce

```bash
python3 EXPERIMENTS/010-annotation-rendering/fetch_annotations.py
```

Standard library, no token. Reads `/rate_limit` first and refuses to proceed
without a verified limit, because a 403 from the 60-per-hour unauthenticated cap
and an empty annotation list look identical to a shell pipeline — and treating the
first as the second is how this repository recorded a false premise for two
sessions. Overwrites `raw/`; the five run ids above are the arms.

## Arms F to J: the run census, and what each red run cost to diagnose

Added in T-0049. Ten runs have passed since the list above was written and **not one
was reproduced on a VM to find out why it was red** — each cause was read off the
run's own annotations. That is the property F020 established for the `Tests` step and
T-0040 built for the file-reading gates, used seven times in a row.

| Arm | Run | Head | Conclusion | Cause, from its annotations |
|---|---|---|---|---|
| F | `37196594583` | `d382943` | red, 3.12 only | session step, exit 4: session 030 `last event is 'session_start'`, started and not yet claimed |
| G | `37196559251` | `fd89dac` | **green** | — the first run whose seven probe annotations are everything it carried |
| H | `37197291442` | `7790d6b` | red, 3.12 only | `Documentation lint`, exit 2: **`tasks/T-0047-…md:70: broken link -> ../../docs/reference/identifier-allocation.md`** |
| I | `37197942512` | `50271e5` | red, 3.12 only | session step, exit 4: session 030 `last event is 'milestone'`, a work commit published while its session was open |
| J | `37198002763` | `09e18b0` | **green** | — and the tip, with every session closed |

**Arm H is the one this repository has been building towards.** It is the first red
run whose cause was read off an annotation the annotator filed, on the offending
file at the offending line, with no reproduction and without the run log that needs
admin rights. Before T-0040 that run's only failure annotation said `Process
completed with exit code 2`; before T-0046 the annotator's own steps would not have
run at all, because arm H's sibling failures show what a skipped gate looks like —
nothing.

Arms F and I are the expected case `docs/operations/ci.md` documents: a commit
published while a session is open has an unfinished session by definition, and each
is green on the next commit, which is the session commit that closes it. Neither is
a defect and neither is worth a change.

**`observed` where a capture exists, `observed`-from-the-run where it does not.**
Arms A–E are in `raw/`, byte for byte. **Arms F–J are pending the hourly reset**: this
VM is inside the 60-requests-an-hour unauthenticated limit and a run costs two of
them, so `fetch_annotations.py` now refuses to start a batch the remaining budget
cannot cover rather than writing half of one. That check exists because the first
version did the opposite and overwrote a good `summary.json` with `http: 403` for two
arms whose captures were already on disk — which reads as an observation about those
runs and is an observation about the limit. `summary.json` is now a rendering of
`raw/` with a `captured` flag per arm, so it cannot say that again.


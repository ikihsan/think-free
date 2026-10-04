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

## What this does not settle

- **`line=` fidelity.** No annotation in any of the four runs carries a line, so
  whether `start_line` comes back as the line emitted is unobserved. `origin
  probe`'s `filed-with-line` shape measures it on every run from now on.
- **Escaping.** No recorded annotation carries a `%`, a newline, a `:` or a `,`,
  so the escaping in `tools/originlib/finding.py` is `source-supported` from
  `actions/toolkit`'s `command.ts` and nothing more. Four probe shapes cover it.
- **A `file=` value containing `:` or `,`.** This repository has no file whose name
  contains either, so the property escaping has no real input here; a synthetic
  one would measure a path that cannot exist.
- **GitHub's own annotation cap**, the 60-line window inherited from the `awk`, and
  whether `::error` on a green job would change its conclusion. The probe emits
  only `notice` and `warning`, so that question is never put to the platform.
- **Rows other than 3.12.** The gate steps are guarded to one row, so the other six
  rows' annotations come from the `Tests` step alone, and on a run where `Tests`
  is green and a gate is red only that one row says anything.

## Reproduce

```bash
python3 EXPERIMENTS/010-annotation-rendering/fetch_annotations.py
```

Standard library, no token. Reads `/rate_limit` first and refuses to proceed
without a verified limit, because a 403 from the 60-per-hour unauthenticated cap
and an empty annotation list look identical to a shell pipeline — and treating the
first as the second is how this repository recorded a false premise for two
sessions. Overwrites `raw/`; the four run ids above are the arms.
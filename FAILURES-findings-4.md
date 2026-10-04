<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Failures — recorded findings, part 4 (F018 onwards)

Continues [`FAILURES-findings-3.md`](FAILURES-findings-3.md), which holds
F013–F017 and reached the 300-line cap at F018. **Identifiers are stable
across all four files**: a reference to `F017` means the same entry wherever
it appears. New findings are appended here.

**What the three findings in this file have in common.** F018 and F019 are
gates in the *test suite* that asserted a fact about the machine running them
instead of about the code under test; each was green on the machine that wrote
it, and each was invisible from outside — the first because nobody ran the
missing interpreters, the second because the CI run log needs admin rights.
F020 is the same shape one domain out: a **conclusion about a CI run** that was
drawn from a field that did not carry it, and generalised from the runs where it
happened to be true to the run where it was not. In all three the evidence was
available and was read from the wrong place.

## F018 — A gate in the suite asserted a fact about the record, so the suite failed on every interpreter nobody had run

Source: T-0034, session `2026-10-04-012`, 2026-10-04. Repair:
`tests/test_doctor_versions.py`; the coupling it was missing is now enforced by
`tests/test_ci_matrix.py`.

**What happened, `observed`.** The suite was run on five CPython builds that no
VM here has installed — 3.9.23, 3.10.18, 3.11.13, 3.13.7 and 3.14.2, portable
builds unpacked outside the repository. On **all five** it failed, with exactly
one failure and no errors: `RealRecordTest.test_the_reported_scope_names_this_suites_size`
in `test_doctor_versions.py`, a file written hours earlier in T-0033. On 3.8.10
(this VM) and on CI's 3.12 the same suite is green.

**Why that is a defect and not a version incompatibility.** The assertion was

```python
match = versions.compare("python3", versions.extract_version(platform.python_version()))
self.assertRegex(match.scope, r"\d+ tests")
```

which requires *this* interpreter to appear in `tests/python-versions.json`. The
record's own `not_exercised` clause named 3.9 to 3.11 as versions nobody had run.
So the suite was red on precisely the versions it had never been run on, and
green only where the record already pointed. No line of `tools/originlib` is
involved: the failure is entirely about the record, and `3.14.2` — newer than
anything this repository has ever named — failed exactly as `3.9.23` did.

**The half that was nearly missed.** The sibling test
`test_this_vms_versions_are_exercised_against_the_real_records` asserts the same
"this interpreter is recorded" claim from a *different* source: `doctor.collect`
probes `python3` from `PATH`. Two tests, one question, two sources, agreeing only
because this VM's `PATH` `python3` is 3.8.10 — the one recorded version available
locally. Running the suite under a downloaded interpreter, where `PATH` and
`sys.executable` disagree, is what separated them.

**Why it was not found sooner, and what it would have caused.** CI pinned one
version, so the question never arose; and that same pin is the entire stated
reason 3.9 to 3.11 were never exercised (`not_exercised[0].why`, verbatim:
*"CI pins a single version"*). Adding a matrix without this repair would have
made five of seven rows red for a reason about the record, and the two available
responses — weaken the assertion, or drop the rows — both reduce measurement. A
gap that rewards the agent for not measuring it is worse than an honest red row.

**The other VM found the same assertion from the other end, an hour later.** Its
CI run `37174050724` was red on this test too, for the mirror-image reason: on a
CI row the interpreter is 3.12, the matched entry is CI's own, and that entry's
scope names a *run id* rather than a test count — so an assertion that had been
green on every VM was red on the only interpreter this repository had evidence
about. Its fix asserted that the reported scope is the matched entry's own text
unchanged, which is a different property from the one it replaced. Both findings
are kept, in `tests/test_doctor_versions.py`, because neither clause catches the
other's failure: the merged test requires every entry to say how much it ran
*and* hands back that text unaltered *and* tolerates an interpreter the record
does not name. Neither VM could have seen the other's failure, which is the
clearest statement yet of the D025 rule this finding is about — a gate that reads
one machine's wording is a gate about one machine.

**Repair.** The test now states the disjunction it can actually support: every
`verified` entry's `scope` names a test count, the comparison returns that
entry's text unchanged, and *this* interpreter either matches an entry or is
reported `unrecorded` with its version named. The record's `3.12` CI entry was
given a count as well as its run id, since the missing count was a real gap in
it. The other coupling — every matrix row is recorded, and nothing a row runs is
still listed as never exercised — is enforced on the two artefacts in
`tests/test_ci_matrix.py`, which is where that property lives.

**Lesson, and it generalises past this repository.** A test that asserts a fact
about a *record* rather than about the *code* is green only on the versions that
record happens to cover. The falsification for such a test is not a mutation of
the code: it is running it on an input the record does not name. That needs no
new tooling — it needs an interpreter, and `python-build-standalone` publishes
one for every minor version at a stable URL.

## F019 — The suite asserted that this machine's git is in the record, so every CI row was red and nobody could read why

Source: T-0034, session `2026-10-04-012`, 2026-10-04. Repair:
`tests/test_doctor_versions.py`, `tests/git-versions.json` (a 2.55.0 entry and a
`not_exercised` list), `tests/test_gitversions.py`; decision in
[`DECISIONS-GATING.md`](DECISIONS-GATING.md) D035.

**What happened, `observed`.** T-0034's matrix ran all seven rows and every one
failed at the `Tests` step — including 3.8 and 3.12, which are green here on the
equivalent interpreters. The run log needs repository admin rights, so the failing
test could not be named from the run. The public check-runs API returned
`annotation_count: None` for all seven failing checks, so the `::error::`
mechanism `docs/operations/ci.md` relies on was **not** readable from the public
API either.

**How it was found.** By elimination, then by reproduction. Every matrix row's
minor version had just been measured green locally, so the interpreter could not
be the cause; the other probed tool was `git`. The runner image's own readme
(`actions/runner-images`, `Ubuntu2404-Readme.md` and `Ubuntu2604-Readme.md`) lists
**Git 2.55.0**, and `tests/git-versions.json` named 2.25.1 and 2.56.0 — not
2.55.0. A conda-forge `git` 2.55.0 was unpacked outside the repository and put on
`PATH`, and the suite reproduced the failure exactly:

```
FAIL: test_this_vms_versions_are_exercised_against_the_real_records
AssertionError: 'unrecorded' != 'exercised'
: Match(tool='git', version='2.55.0', state='unrecorded',
        record='tests/git-versions.json',
        detail='no entry in tests/git-versions.json names 2.55.0',
        entries=['2.25.1', '2.56.0'])
```

**Why it is the same defect as F018, one function away.** The assertion was that
*this machine's* probed tools are in the records. That is a fact about the machine,
not about the code, and it held on the machine it was written on. T-0033 added it
and it was green here; T-0034's rebase merged it beside the F018 assertion, which
failed on every interpreter the record lacked — so one file held two machine-fact
assertions, green on a 3.8.10/2.25.1 VM, red on a 3.12 runner and red on a 2.55.0
runner, for opposite reasons.

**The part that adding the entry does not fix.** A 2.55.0 entry makes CI green and
makes the machine-fact true again. On its own that is the wrong repair: it replaces
one unspoken assumption with another and the next machine breaks it. The assertion
is now the module's contract — every probed tool reaches one of the four states,
and an `exercised` verdict carries its entry's scope and the machine it ran on —
with the negative control that emptying the record's `verified` list moves every
version off `exercised`, so the weaker assertion cannot pass for the wrong reason.
"This machine is not in the record" is `doctor`'s warning to *print*; it is not a
property a suite can assert.

**Lesson, and it is the general form of F018.** A gate that reads its own
environment is only as portable as the record of that environment. Two gates in
one file asserted that the environment matched a hand-maintained list, and each was
green on exactly the machine that wrote it. The portable form asks the record
about the *artefacts* — does every CI matrix row have an entry — and states the
environment gap as data (`not_exercised`) rather than as an assertion that fails.
The git record now says what it does **not** run against, which is the first time
anything here has stated that for git.

## F020 — The check-run annotations were readable all along; their silence has four causes and three of them are not "none"

Source: T-0038, session `2026-10-04-018`, 2026-10-04. Repair: this finding, the
correction in [`STATE.md`](STATE.md), and the section in
[`docs/operations/ci.md`](docs/operations/ci.md). Nothing in the tooling changes.

**The record was wrong about the run it was cited against.** `STATE.md`, defect 9
in [`STATE-defects.md`](STATE-defects.md) and F019 itself all record that the
public check-runs API returns no annotations, and cite F019's hour of elimination
as the consequence. Read again on 2026-10-04 with no token and no rights, run
`37178057818` at commit `687961f` carries **11 annotations on `verify (3.12)`, nine
of them failures**, and they name the failing test, the file and the line:

```
FAIL: test_this_vms_versions_are_exercised_against_the_real_records (test_doctor_versions.RealRecordTest…)
File "/home/runner/work/think-free/think-free/tests/test_doctor_versions.py", line 69
: Match(tool='git', version='2.55.0', state='unrecorded', record='tests/git-versions.json', …)
AssertionError: 'unrecorded' != 'exercised'
```

That is F019's own reproduced failure, quoted in the entry above, readable from
the run rather than rebuilt on a VM. **What the annotations say, per run,
`observed`:**

| Run | Commit | Red rows | The annotation names |
|---|---|---|---|
| `37178057818` | `687961f` | 7 | `test_this_vms_versions_are_exercised_against_the_real_records` on six rows; **`verify (3.11)` names a different test**, `test_claiming_and_completing_keep_the_index_current` |
| `37179073002` | `df2b19e` | 7 | the same test on all seven rows |
| `37174050724` | `b204aff` | 1 | the same test, plus `test_the_reported_scope_names_this_suites_size` |
| `37163438950` | `8898f0a` | 1 | nothing: 3 annotations, the only failure `Process completed with exit code 2.` |
| `37163434868` | `83aa9a4` | 1 | nothing, the same three |
| `37171841544` | `09684f2` | 1 | nothing, the same three |

So the runs a sibling VM's T-0037 was about to record as unexplained are the
already-recorded F019 on all seven rows, with one row failing for a second,
separate reason; and the runs that genuinely carry no test annotation are the
*Documentation lint* failures, whose step emits no `::error::` lines at all. The
conclusion was generalised from the shape that has none to the case that needed
them — and `37174050724` shows the generalisation is not even stable within one
step, since one row names a second failure.

**Four things make this endpoint answer "nothing", and only one of them is
"nothing".**

1. **The wrong endpoint, or the wrong field.** F019 quotes `annotation_count:
   None` for all seven failing checks. The field this API does carry is
   `output.annotations_count`, and on those checks it read **11** — `observed`. The
   quoted name is not one this session read back, and the jobs endpoint
   (`/actions/runs/{id}/jobs`) has no annotations object at all, so a
   `.get("annotation_count")` against it returns `None`: `inferred`, and the most
   likely mechanism. Either way the count was available without rights.
2. **The wrong sub-resource.** `/commits/{sha}/check-runs` carries the count and
   the check-run id; the messages are at `/check-runs/{id}/annotations`. Reading
   only the first gives a count with nothing to show, and the check-run's own
   `output.text` is empty whether or not annotations exist.
3. **The rate limit.** Unauthenticated, the core API allows **60 requests an hour
   per IP** — `observed`, `GET /rate_limit` reported `limit 60, remaining 0` after
   this session's own reads. Over the limit the call returns **403**, not an empty
   list, so a reader who treats a failed call as an empty answer concludes the
   opposite of the truth. This VM has no token in its environment, so any
   diagnostic built on this endpoint inherits the limit.
4. **No emission.** A step that prints no `::error::` line naming its violation
   annotates nothing. `Tests` prints one per failure; `Documentation lint` and
   `Release manifest` print none, and the session step prints `::warning::` only
   for in-flight sessions, which is not the thing that fails it. This is the only
   one of the four that is a fact about the run, and it is the one that would be
   fixed by printing more.

**The lesson, and it is D030 one domain out.** D030: a diagnostic must
distinguish "never configured" from "stopped working". Here: a diagnostic must
distinguish *four* answers — read it, read it and it is empty, could not read it,
and the thing read does not emit. A tool that reports "no annotations" for all
three of the last cases is worse than no tool, because it is confidently wrong.

**Ceiling.** Everything here is `observed` from the public endpoint on 2026-10-04
and re-derivable by re-running one script; nothing is inferred about what any
agent did read, only about what the API returns. Two runs named in T-0037
(`37181374433`, `37180487906`) were measured earlier in the same hour and carry
three annotations with no test named — the session step and a stale generated
file, neither of which emits. Whether the 3.11 row's second failure has a cause
beyond the two tests it names is **not** answered here; T-0037's question, if it
survives this finding, is that row and not the seven.

## F021 — The annotator's rendering was declared unmeasured on a run whose annotating steps never ran

Source: T-0046, `EXPERIMENTS/010-annotation-rendering/`. Rule:
`tools/originlib/probe.py`, and the `always()` guard on the five gate steps in
`.github/workflows/ci.yml`.

**What happened.** `docs/operations/ci-diagnosis.md` said the annotator's rendering
was `unmeasured` — "which of the emitter and GitHub's renderer is responsible was
not determined" — and gave its evidence: run `37189825232`, whose annotations
carried `::error file=tools/originlib/identifiers.py::…` in the message while the
annotation's own structured `path` was `.github`. From that it concluded the location
reaches the reader but is not attached, and told the next reader to read `file=` as
"the reader is told which file", not "the annotation is filed on it".

**Both halves were artefacts of the same run, and it was the wrong run.** The
`Tests` step on that row had failed, and every later step in the job carried an
`if:` naming no status function, so GitHub gave it an implicit `success()` and
skipped all five gate steps: the annotator emitted nothing on that run at all. The
`::error file=…` string in its messages is the first line of a unittest assertion
diff — `AssertionError: Lists differ: ['::error file=…'] != []` — re-emitted by the
same awk that re-emits test failures; it is a test's *expected* text. And `.github`
is what a command carrying no `file=` gets: the green run `37192717297` carries
three, all from fileless commands.

The claim it displaced was measurable in one call. Run `37191658964`, where `Tests`
passed on the 3.12 row and `Documentation lint` alone failed, carries
`path: DECISIONS-RECORDS.md`, `start_line: 0`, and the annotator's message verbatim.
**GitHub files the annotation on the emitted path**, and the mechanism had run.

**Why this is a defect and not a bad reading.** The two facts were confounded by
construction: a renderer that honours `file=` and one that ignores it entirely both
produce `path: .github` on a run where no command carried a `file=`. Nothing in the
capture distinguished them, so the reading was not merely mistaken — it was
under-determined, and written as though it were settled. That is D025's shape for
the fourth time, and the third instance in this file after F020: a conclusion drawn
from the field that does not carry it.

**Repair.** Three parts, the second the general one. The document now says what the
annotations say, with the run id and the field. Every step whose only job is to emit
a diagnostic says `always() && …`, and `tests/test_ci_annotations.py` fails on a
workflow that does not — falsified against the workflow as it was, where it named the
step and its expression; a skipped gate is indistinguishable from a passing gate in the
annotations, which is F020's "never configured" against "stopped working" reached from
the other side. And `tools/origin probe` publishes one annotation per rendering shape
on every run, so the reference and the failure come from the same place rather than from
whichever run happened to be red when somebody went looking. It emits only `notice` and
`warning`, both of which a green run already publishes, and never `::error`: a
measurement that can redden the run it measures is one that gets deleted after its
first false alarm.

**Lesson kept.** A mechanism's behaviour on a platform is only measured on a run
that reached it, and "the run was red" is not the same claim as "the mechanism ran".
Quote the field the mechanism writes, and check which steps ran before reading any
of it: the annotation list of a job is the union of its steps', and a step that did
not run contributes nothing that looks like a contribution.

**Ceiling.** Four runs of one workflow on one runner image; `line=` fidelity, the
escaping, and a `file=` value containing `:` or `,` are still unobserved, and the
probe is what will observe them.

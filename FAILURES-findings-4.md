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

**What the two findings in this file have in common**, and why they landed in
one file rather than being filed apart: both are gates in the *test suite*
that asserted a fact about the machine running them instead of about the
code under test. Each was green on the machine that wrote it. They were found
one function apart, in the same class, and neither was visible from outside —
the first because nobody ran the missing interpreters, the second because the
CI run log needs admin rights.

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

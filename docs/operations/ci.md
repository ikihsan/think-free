<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Continuous integration

Runs on every push and pull request. The gates are the same ones a session must
pass locally, so a green local run means a green CI run.

Workflow: [`../../.github/workflows/ci.yml`](../../.github/workflows/ci.yml).

## Gates

| Gate | Command | Fails on |
|---|---|---|
| Tests | `python3 -m unittest discover -s tests -t tests` | Any test failure |
| Documentation | `tools/origin doc lint` | Line cap, metadata, broken link, orphan, stale generated file, unresolved merge conflict, identifier defined twice or indexed without a body |
| Release manifest | `tools/origin release check` | A path unclassified or classified twice, a declared path absent without `pending`, a wildcard, a credential shape in a classified path, or the front door disagreeing with the manifest about what exists |
| Skills | `tools/origin skills check` | Naming, frontmatter, missing or wrong cross-agent mirror |
| Session integrity | `tools/origin session verify --strict` | Malformed event stream, **abandoned** session, missing report, dangling command log reference |
| Vendored integrity | `tools/origin skills verify` | Local modification of a vendored skill |

`sync land` is not a CI step, but it refuses to publish a tree whose identifier
record collides, so the Documentation step above is a backstop rather than the
only place rule 7 is read. See *One number, one thing* below.

The `Tests` step runs on every matrix row; the other five run on one. So "the
six gates are green" means seven jobs: one per interpreter for the tests, and the
five file-reading gates once, on 3.12.

`tools/origin preflight` runs four of these — documentation, skills, session
integrity and the release manifest — and deliberately leaves the test suite as a
separate command, because it takes minutes and the rest take seconds. The release
check joined it on 2026-10-04 (T-0045): T-0042 added `DECISIONS-RECORDS.md` at the
top level and classified nothing, and this command passed, because the gate that
would have said so was not among the ones it ran. **A gate nobody runs from the one
place the protocol points at is a gate the next agent repeats the omission
against.**
CI passes `--strict` to the session gate, because on a pushed commit nothing is
in flight and an unfinished session really is a failure. Locally, `preflight`
reports the current session as in progress rather than failing, so it is usable
mid-task.

## In flight is not the same as abandoned

An unfinished session is not a failure on a shared base branch. `task claim`
requires HEAD to equal the remote base before it publishes a claim, so a VM that
claims a task must push its `session_start` first: an in-flight session is
*supposed* to be on the base branch, and while one is open every VM's push would
otherwise be red. The predicate is `tools/originlib/inflight.py` and it must
all hold:

| Clause | Question it answers |
|---|---|
| `session_start` names a task, **or** a claim in the ledger names the session | Is any work open at all? |
| The task is `claimed` | Is it still open? |
| The claim names this session, by `claim-session` or by `claim-agent` + `claim-vm` | Is it *this* session holding it? |
| The last ledger entry for the task is `claim` or `takeover` | Was the claim closed behind the task file's back? |
| The claim is younger than `--lease-hours` (12) | Is the holding VM plausibly alive? |

All five are read from the tree: no network, no new state. The first clause has an
alternative because `--task` is optional on `session start` and a session may claim
work without it — that exception was added after the live record showed the gate
calling a working session abandoned.

A session failing any clause is **abandoned**, and the gate fails naming the
clause. A session passing all five prints `in flight (task T-0017, claimed by
opencode on instance-20260717-0944 1.0h ago)` and CI re-emits that as a
`::warning::` annotation.

**What the gate no longer catches:** a crash *inside* the lease window. The
claim stays in force for up to 12 hours, so a dead VM's session keeps CI green
for that long; `task list --remote` names the holder and its claim time, and
`--lease-hours` shortens the window. See
[`../../DECISIONS-GATING.md`](../../DECISIONS-GATING.md) D027 for the reasoning
and the alternatives rejected.

## Design decisions

**Standard library only.** The workflow uses `actions/checkout`,
`actions/setup-python`, and the Python it selects. No package installation, no
lockfile, no dependency to go stale. The tooling's own claim is that a fresh
machine needs nothing, and CI should not quietly contradict it.

**The Python version is pinned, the runner's is not trusted.** The workflow ran
on `ubuntu-latest` with whatever interpreter that image shipped, and every one of
the first 60 recorded runs failed at the `Tests` step without anyone being able
to say which test: downloading a run log needs repository admin rights, and the
error itself said only "rebase could not be completed". `setup-python` makes the
version a decision rather than an accident — `ubuntu-latest` migrates to Ubuntu
26 in October 2026 and would otherwise change the interpreter under this
repository.

**What the pin does and does not prove.** It makes CI's interpreter a recorded
decision; it does not make it evidence about the fleet. It is also not enough on
its own: pinned to one version, it left the floor claim resting on two points
with a gap between them, and the record said so in five words — *"CI pins a
single version"*. Since T-0034 the pin is a **matrix**, one row per CPython minor
from 3.8 to 3.14, so the gap is measured on every push instead of described.
`fail-fast: false` is part of that: with the default, one red row cancels the
others, and a cancelled row is not a version anything has run on.

**The matrix and the record are held to each other.**
[`../../tests/python-versions.json`](../../tests/python-versions.json) is the
record of what has actually run, per version and per scope. Every row needs an
entry, nothing a row runs may still be listed as never exercised, and
[`../../tests/test_ci_matrix.py`](../../tests/test_ci_matrix.py) is the gate that
says so — it exists because two tests in
[`test_doctor_versions.py`](../../tests/test_doctor_versions.py) assert that the
interpreter running them is in that record, which turned the suite red on every
version the record had never heard of (`FAILURES.md` F018). Each CI entry claims
the minor version only, because the run log needs repository admin rights and the
public API does not report the patch. The same applies to git: CI is one runner's
git, not the fleet's.

**The other five gates run on one row, 3.12.** They read files rather than run
the interpreter, so their result cannot depend on which row they are on. The
guard is written out (`if: matrix.python-version == '3.12'`) rather than left to
a job split, so the checks every "CI is green" claim refers to keep their names,
and so a typo stops the gates running visibly rather than quietly. The gate in
`test_ci_matrix.py` refuses a guard naming a version that is not a row — a gate
that cannot run cannot fail.

`tools/origin doctor` reads both records and reports whether this VM's versions
are among them (T-0033), so a VM outside the exercised set says so at the point
where an agent decides whether it can do the work, and says **which** entry it
matched and where that entry ran — one record now covers two environments per
minor version, so `exercised` alone would describe somebody else's machine. It
cannot tell you about an interpreter nobody has run, because nothing here can:
that is what the `not_exercised` list in the record is for.

**A red run is diagnosable without admin rights, through annotations.** The
`Tests` step re-emits every `FAIL:`/`ERROR:` block as an `::error::` annotation,
and since T-0040 each file-reading gate re-emits each of its violations the same
way, naming the file. `observed` on run `37178057818`: 11 annotations on the
3.12 row, one naming the failing test and its line, readable from the public
check-runs API with no token; and on run `37191658964`, a gate violation's
annotation filed on the file the gate named. **That corrects a conclusion this
file held for a session** — it said the public API returns no annotations,
generalised from the runs whose step emits none (`FAILURES.md` F020, and see the
correction in [`../../STATE.md`](../../STATE.md)). Three of the four earlier "no
annotations" answers are not "nothing": the wrong endpoint, the wrong
sub-resource, and a 403 from the 60-per-hour unauthenticated limit. All of it is
in [`ci-diagnosis.md`](ci-diagnosis.md), which is the method; this is the
statement.

**What annotations are not.** They name a file or a test, not a conclusion, and
they are this repository's own emission: the runner decides how many it renders,
and past the cap the run is annotated as truncated rather than silently. They are
also only as complete as the gate that emitted them, which is why a violation
whose rule knows no single file — an identifier taken twice in two files, a mirror
that is a directory rather than a file — is published with **no** `file=`
property instead of one that would point somewhere wrong.

**One red step is not a defect: a session in flight.** The session step passes
`--strict`, and a commit published while a session is open has an unfinished
session by definition. Two cases, and the distinction is worth reading off the
run: a session that **claimed a task** is reported `in flight` and re-emitted as
a `::warning::`, which is the D027 lease doing its job; a session with **no task
and no claim** naming it has nothing to prove it is alive, so it is reported as a
failure. Observed on 2026-10-04 five times, three of them from one VM: runs
`37174316639`, `37181374433`, `37206132901` at `2643c9e`, and `37206627337` at
`1061c5b`, each red only on `Session record integrity` and each green on the next
commit, which is the session commit that closes it. **The taskless case is the one
to watch, because it is the one this repository's own protocol produces:** an agent
recording a measured result or repairing the record has nothing to claim, and
`docs/process/session-protocol.md` does not tell it to invent a task. The annotation
names the distinction in one line — `last event is 'artifact'; session may be
unfinished; T-0050 is done, no claim names this session` — so the case is
recognisable from the run without admin rights. **So a red session step on a commit
that is not the last one on the branch is expected**, and the way to confirm it is to
look at the following run rather than the log. The open question is in
[`STATE-next-actions.md`](../../STATE-next-actions.md) item 2(c): whether a taskless
session should be allowed to publish code commits at all.

**A red gate names its file, and the annotation is filed on it.** The five gate
steps that print a report and exit give the runner nothing to attach, so their
only annotation is "Process completed with exit code 2" — the shape F019 spent an
hour on. `tools/origin annotate` runs a gate in process and prints one `::error`
per violation, naming the file, and **GitHub files the annotation on that path**:
`observed` on run `37191658964`, whose `Documentation lint` annotation carries
`path: DECISIONS-RECORDS.md`. Each of those five steps also says `always()`, so a
red `Tests` step does not skip them — an implicit `success()` did, and on two runs
it meant four gates never ran with nothing in the annotations to say so (defect
18). `tools/origin probe` publishes one annotation per rendering shape on every
run, so the run reporting a failure carries the reference for reading it. The
method, the escaping, and what an annotation may not claim are in
[`ci-diagnosis.md`](ci-diagnosis.md).

**A pass that hides why is a pass nobody can trust.** The session step writes the
verifier's own output to a log and re-emits each in-flight line as a
`::warning::` annotation, for the same reason the test step re-emits failures:
the annotation is public, the run log is not. A green build that says nothing
about the live sessions on the fleet is how the previous version of this gate
went unread for hours.

**No secrets.** The workflow needs none. Nothing here can deploy, publish, or
push; a pull request cannot use a credential the workflow does not have.

**Offline tolerance.** The gates that read files pass without network access.
`origin doctor` is deliberately *not* part of CI: it probes the network and the
machine, which would make the build flaky for reasons unrelated to the change.

## Reading a red run

The run log needs admin rights; the public check-runs API does not, and it names
the failing test. Two calls, four answers, and a rate limit that looks like an
empty list: [`ci-diagnosis.md`](ci-diagnosis.md). Evidence in `FAILURES.md` F020.

## Git version is part of the contract

The suite passes on git 2.25 and on git 2.56, and it did not in between, for a
reason no gate covered: `git rebase --continue` opens an editor from git 2.26,
which broke `origin sync land` on any VM with a modern git
(`FAILURES.md` F011). A VM's git version is therefore read, not assumed. The
machine-readable list of exercised versions is
[`tests/git-versions.json`](../../tests/git-versions.json); prose that names
versions must agree with it.

**The runner's git is 2.55.0, and for two hours nothing said so.** `T-0033` added
a test asserting that whichever git ran the suite was in that record, and CI's
was not — 2.25.1 and 2.56.0 were the entries, and neither is 2.55.0. The version
is `source-supported` from the runner image's own readme
(`actions/runner-images`), and the suite has now been run on it locally, so the
record carries a 2.55.0 entry. The assertion itself was still wrong and was
replaced (`FAILURES.md` F019): the record also grew a `not_exercised` list,
because a record with two entries and no gaps reads as a claim about a line nobody
measured.

## One number, one thing

Findings `F001…`, decisions `D001…` and tasks `T-0001…` are allocated by reading
the **local** tree, so two VMs working in the same hour take the same number.
Seven times on 2026-10-03 and 2026-10-04; each was resolved by hand, and one
reached the base: commit `e6eb992` holds two different findings both headed
`## F010`.

Doc lint rule 7 reports an identifier defined twice, an index row with no
definition behind it, a defined finding with no row, and a decision its own index
row does not list. `sync land` refuses to push a tree the rule would refuse. Both
gates call one entry point, `tools/originlib/idcheck.py`, over both sources of
definitions: `tools/originlib/identifiers.py` (findings, decisions, tasks) and
`tools/originlib/defectlist.py` (the numbered list in `STATE-defects.md`, which two
VMs filled in with the same **defect 7** in one hour while rule 7 did not read it).

Why `land` and nothing else: **a collision is created by the merge.** Each branch
is internally consistent, and each VM's own lint sees nothing wrong with its own
tree. `push` and `task claim` are deliberately not gated, because refusing them
would block a VM from publishing the session record it needs in order to
renumber its way out.

| Checked | Not checked |
|---|---|
| The same identifier defined twice, in one file or across two | Which entry a *reference* points at — the number must exist, not necessarily say what the sentence needs |
| A findings index row that no body backs, and a body with no row | Hypothesis identifiers (`E001…`), which have not collided |
| A decision the index does not list, and a listed id nothing defines | Two VMs allocating at once — this is a detector, not an allocator (D032) |
| A defect number that defines two entries, and a defect list the rule cannot read | A **gap** in the defect numbering — a dropped entry and a withdrawn defect are the same bytes |

Rule 7 matches on identity, never on wording: two rows in `FAILURES.md` are
shortened paraphrases of their headings, and a string comparison flagged 83 of
174 commits including this one.

## What CI does not check

- Whether a claim in a document is true. That is what experiments and
  [`docs/process/review-protocol.md`](../../docs/process/review-protocol.md) are
  for. `release check` is the sharpest case of the limit: it proves the manifest
  and `README.md` agree about what exists, not that either is right.
- Whether the tooling's tests are good enough. They cover the rules the tooling
  enforces; they do not establish that the rules are the right ones.
- Whether documentation is *good*. Lint checks structure: caps, links, metadata,
  freshness, conflict markers.
- Whether the **floor** claim is still right. `test_ci_matrix.py` holds the
  matrix to the record, but nothing holds `floor.claim` to anything: widening the
  matrix is a decision somebody has to read, not a change a gate notices.

## Before opening a pull request

```bash
tools/origin preflight
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests
tools/origin release check
tools/origin skills verify
```

Locally `preflight` is not strict about the session you are currently running.

All of them must pass locally. A red local run that is fixed by re-running CI is
a wasted cycle.

## Exit codes CI branches on

`0` success, `1` usage error, `2` lint violation, `3` verification failed, `4`
integrity violation. The distinction between `2` and `4` is deliberate: `2` means
a document is wrong, `4` means the record is inconsistent.

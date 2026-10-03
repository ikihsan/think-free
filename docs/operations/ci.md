<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Continuous integration

Runs on every push and pull request. The gates are the same ones a session must
pass locally, so a green local run means a green CI run.

Workflow: [`../../.github/workflows/ci.yml`](../../.github/workflows/ci.yml).

## Gates

| Gate | Command | Fails on |
|---|---|---|
| Tests | `python3 -m unittest discover -s tests -t tests` | Any test failure |
| Documentation | `tools/origin doc lint` | Line cap, metadata, broken link, orphan, stale generated file, unresolved merge conflict |
| Release manifest | `tools/origin release check` | A path unclassified or classified twice, a declared path absent without `pending`, a wildcard, a credential shape in a classified path, or the front door disagreeing with the manifest about what exists |
| Skills | `tools/origin skills check` | Naming, frontmatter, missing or wrong cross-agent mirror |
| Session integrity | `tools/origin session verify --strict` | Malformed event stream, **abandoned** session, missing report, dangling command log reference |
| Vendored integrity | `tools/origin skills verify` | Local modification of a vendored skill |

`tools/origin preflight` runs three of these — documentation, skills, and
session integrity — and is deliberately not the whole list: the test suite and
the release check stay separate commands so a VM can run them on their own.
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
calling a working session abandoned. The first clause has
an alternative because `--task` is optional on `session start` and a session may
claim work without it — that exception was added after the live record showed
the gate calling a working session abandoned.

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
error itself said only "rebase could not be completed". `setup-python` with
`python-version: '3.12'` makes the version a decision rather than an accident —
`ubuntu-latest` migrates to Ubuntu 26 in October 2026 and would otherwise change
the interpreter under this repository.

**A failing test must be identifiable without admin rights.** The `Tests` step
re-emits every `FAIL:`/`ERROR:` block as an `::error::` annotation. GitHub
returns check-run annotations from its public API, so a `curl` against
`/repos/<owner>/<repo>/commits/<sha>/check-runs` names the failing test to anyone
who can read the repository. That is the only reason the CI failure was
diagnosable at all; keep it when editing that step.

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

## Git version is part of the contract

The suite passes on git 2.25 and on git 2.56, and it did not in between, for a
reason no gate covered: `git rebase --continue` opens an editor from git 2.26,
which broke `origin sync land` on any VM with a modern git
(`FAILURES.md` F011). A VM's git version is therefore read, not assumed. The
machine-readable list of exercised versions is
[`tests/git-versions.json`](../../tests/git-versions.json); prose that names
versions must agree with it.

## What CI does not check

- Whether a claim in a document is true. That is what experiments and
  [`docs/process/review-protocol.md`](../../docs/process/review-protocol.md) are
  for. `release check` is the sharpest case of the limit: it proves the manifest
  and `README.md` agree about what exists, not that either is right.
- Whether the tooling's tests are good enough. They cover the rules the tooling
  enforces; they do not establish that the rules are the right ones.
- Whether documentation is *good*. Lint checks structure: caps, links, metadata,
  freshness, conflict markers.

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

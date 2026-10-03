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
| Documentation | `tools/origin doc lint` | Line cap, metadata, broken link, orphan, stale generated file |
| Skills | `tools/origin skills check` | Naming, frontmatter, missing or wrong cross-agent mirror |
| Session integrity | `tools/origin session verify --strict` | Malformed event stream, unfinished session, missing report, dangling command log reference |
| Vendored integrity | `tools/origin skills verify` | Local modification of a vendored skill |

`tools/origin preflight` covers the first four in one command. CI passes
`--strict` to both, because on a pushed commit nothing is in flight and an
unfinished session really is a failure. Locally, `preflight` reports the
current session as in progress rather than failing, so it is usable mid-task.

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

**No secrets.** The workflow needs none. Nothing here can deploy, publish, or
push; a pull request cannot use a credential the workflow does not have.

**Offline tolerance.** The gates that read files pass without network access.
`origin doctor` is deliberately *not* part of CI: it probes the network and the
machine, which would make the build flaky for reasons unrelated to the change.

## Git version is part of the contract

The suite passes on git 2.25 and on git 2.56, and it did not in between, for a
reason no gate covered: `git rebase --continue` opens an editor from git 2.26,
which broke `origin sync land` on any VM with a modern git
(`FAILURES.md` F011). A VM's git version is therefore read, not assumed.

## What CI does not check

- Whether a claim in a document is true. That is what experiments and
  [`docs/process/review-protocol.md`](../../docs/process/review-protocol.md) are
  for.
- Whether the tooling's tests are good enough. They cover the rules the tooling
  enforces; they do not establish that the rules are the right ones.
- Whether documentation is *good*. Lint checks structure: caps, links, metadata,
  freshness.

## Before opening a pull request

```bash
tools/origin preflight
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests
tools/origin skills verify
```

Locally `preflight` is not strict about the session you are currently running.

All four must pass locally. A red local run that is fixed by re-running CI is a
wasted cycle.

## Exit codes CI branches on

`0` success, `1` usage error, `2` lint violation, `3` verification failed, `4`
integrity violation. The distinction between `2` and `4` is deliberate: `2` means
a document is wrong, `4` means the record is inconsistent.
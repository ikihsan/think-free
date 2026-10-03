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
| Session integrity | `tools/origin session verify` | Malformed event stream, unfinished session, missing report, dangling command log reference |
| Vendored integrity | `tools/origin skills verify` | Local modification of a vendored skill |

`tools/origin preflight` covers the first four in one command.

## Design decisions

**Standard library only.** The workflow uses `actions/checkout` and the Python
already on the runner. No package installation, no lockfile, no dependency to go
stale. The tooling's own claim is that a fresh machine needs nothing, and CI
should not quietly contradict it.

**No secrets.** The workflow needs none. Nothing here can deploy, publish, or
push; a pull request cannot use a credential the workflow does not have.

**Offline tolerance.** The gates that read files pass without network access.
`origin doctor` is deliberately *not* part of CI: it probes the network and the
machine, which would make the build flaky for reasons unrelated to the change.

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

All four must pass locally. A red local run that is fixed by re-running CI is a
wasted cycle.

## Exit codes CI branches on

`0` success, `1` usage error, `2` lint violation, `3` verification failed, `4`
integrity violation. The distinction between `2` and `4` is deliberate: `2` means
a document is wrong, `4` means the record is inconsistent.
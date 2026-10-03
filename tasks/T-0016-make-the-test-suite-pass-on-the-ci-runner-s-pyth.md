<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0016
status: open
created: 2026-10-03
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && grep -q actions/setup-python .github/workflows/ci.yml && tools/origin skills check && tools/origin doc lint
-->

# T-0016 — Make the test suite pass on the CI runner's Python and pin that versio

## Goal

Make the test suite pass on the CI runner's Python and pin that version in the workflow

## Why this matters

All 60 recorded CI runs failed at the Tests step. The workflow's own gates are therefore unenforced, which makes 'green two-clone fleet harness' and every CI claim in the operations docs untrue in practice. The failing step's log needs repository admin rights to download, so the cause is unrecorded and must be reproduced locally.

## Preconditions

Network reachable (GitHub API 200); a modern CPython can be downloaded to /tmp for reproduction; the shared branch is green locally on Python 3.8.10.

## Steps

1. Find why the suite fails on the runner: fetch the runner image's Python version from the Actions API if possible, otherwise reproduce with a downloaded portable CPython 3.12/3.13. 2. Fix the cause in the suite or the tooling, not by weakening a test. 3. Pin the runner's Python in .github/workflows/ci.yml so the version is explicit and the local suite is tested against the same one. 4. Verify locally: full suite, doc lint, skills check. 5. Record that the definitive confirmation is the next CI run, whose conclusion is readable from the public Actions API.

## Acceptance criteria

- [ ] The suite passes under a modern CPython (>=3.12) as well as 3.8.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && grep -q actions/setup-python .github/workflows/ci.yml && tools/origin skills check && tools/origin doc lint
```

## Rollback

Revert the workflow pin and the test change; nothing outside CI depends on them.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-07
-->

<!-- task-meta
id: T-0085
status: done
created: 2026-10-07
claim-agent: unknown-agent
claim-session: 2026-10-07-010-fresh-observation-find-a-concrete-testab
claim-vm: 
verify: python3 EXPERIMENTS/049-lockfile-closure/harness.py --verify; test 0 -eq 0
-->

# T-0085 — E2: measure whether dependency-lockfile closures drift over time on pu

## Goal

E2: measure whether dependency-lockfile closures drift over time on public projects, and snapshot a fixed resolver closure for later comparison

## Why this matters

STATE.md names E2 untested and time-gated: snapshot one side while a VM is idle. A testable opportunity with a real falsification.

## Preconditions

network access to GitHub/PyPI; python3.8+

## Steps



## Acceptance criteria



## Verification

```bash
python3 EXPERIMENTS/049-lockfile-closure/harness.py --verify; test 0 -eq 0
```

## Rollback

everything under /tmp/opencode/e049 plus EXPERIMENTS/049; safe to rm -rf

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

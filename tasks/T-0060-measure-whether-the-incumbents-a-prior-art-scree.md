<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0060
status: done
created: 2026-10-04
claim-agent: unknown-agent
claim-session: 2026-10-04-054-test-whether-prior-art-exists-means-the
claim-vm: 
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
-->

# T-0060 — Measure whether the incumbents a prior-art screen names are actually s

## Goal

Measure whether the incumbents a prior-art screen names are actually serving the need

## Why this matters

F029 killed 19 of 50 harvested needs with the verdict 'a tool already serves it' and killed all 12 prior candidates on prior art. The verdict was falsified against star counts, and T-0059 then measured that stars do not predict installs anywhere, including in the mature arm. So neither check has ever read the property the verdict claims. This measures serving directly, through channels that do not require a registry (Homebrew installs, GitHub release-asset downloads), which is exactly the arm T-0059 recorded as never executable.

## Preconditions

Unauthenticated public APIs: GitHub core 60/hr and search 10/min, npm, PyPI, crates.io, formulae.brew.sh. Pace the fetches; a refused answer is kept apart from an absence.

## Steps

1. Declare the hypothesis and both gate arms in EXPERIMENTS/014 before any count is read.
2. Build the incumbent population by machine: the repositories a GitHub phrase query surfaces for each of the 19 prior_art kills, two phrasings each, top 3 by stars, deduplicated.
3. Measure serving per incumbent on rate channels (npm, PyPI, crates, Homebrew 30d installs) and cumulative channels (GitHub release-asset downloads), each attribution verified to name the same repository.
4. Report the fraction with serving evidence against a predeclared floor, and state what the instrument still cannot see.

## Acceptance criteria

The gate in EXPERIMENTS/014/README.md is answered in one direction from results.json, and the finding is recorded or the ceiling stated.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
```

## Rollback

The raw captures are appended-only under EXPERIMENTS/014/raw/; removing the directory removes the experiment.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

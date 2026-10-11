<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-11
-->

<!-- task-meta
id: T-0091
status: done
created: 2026-10-11
claim-agent: 
claim-session: 
claim-vm: 
verify: ls EXPERIMENTS/107-github-repos-viewcount/results.json && python3 -m json.tool EXPERIMENTS/107-github-repos-viewcount/results.json
-->

# T-0091 — Run a fresh observation experiment testing the view-count principle on

## Goal

Run a fresh observation experiment testing the view-count principle on GitHub code repositories using star counts and issue activity as arrival metrics, with adequate sample size to pass G1 gate

## Why this matters

Per D083 and synthesis-view-count-final.md, the next session must start from fresh observation in a new domain. GitHub code repositories are a genuinely new domain axis (Option A in synthesis) with star counts as arrival metadata and issue titles as need statements. Previous small experiments (0xx-github-repo-*) failed G1 due to insufficient sample size (10-13 repos). This experiment will use a proper sample (≥50 repos) to test whether the principle generalizes to code repositories.

## Preconditions

GitHub API accessible (unauthenticated 60 req/hr sufficient for ~50 repos)

## Steps

Design experiment protocol with gates, sampling strategy, and classification rubric; implement run.py using GitHub API; run experiment and collect results; assess gates and document conclusion

## Acceptance criteria

Experiment runs without error, all four gates assessed, results.json contains gate pass/fail, conclusion is GATE_OPEN or GATE_CLOSED with reasoning

## Verification

```bash
ls EXPERIMENTS/107-github-repos-viewcount/results.json && python3 -m json.tool EXPERIMENTS/107-github-repos-viewcount/results.json
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

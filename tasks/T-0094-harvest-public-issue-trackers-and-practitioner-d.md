<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-13
-->

<!-- task-meta
id: T-0094
status: open
created: 2026-10-13
claim-agent:
claim-session:
claim-vm:
verify: ls EXPERIMENTS/XXX-preflight-demand-validation/results.json && python3 -m json.tool EXPERIMENTS/XXX-preflight-demand-validation/results.json
-->

# T-0094 — Harvest public issue trackers and practitioner discussions for LLM eva

## Goal

Harvest public issue trackers and practitioner discussions for LLM evaluation frameworks to find evidence of the three problems preflight catches: C1 silent join failures, C2 alternate-form false positives, C3 contaminated control arms. Kill gate: < 10 credible reports across 3+ frameworks = demand too weak.

## Why this matters

Preflight tool has working mechanism validated on 6 harness formats but no measured demand. Mission's own harnesses had all 3 defects (F118, F121, F122, F123, F124). Anthropic playbook names C2/C3 as manual practices. No automated tool for C3 found. Must validate demand before candidate consideration per D079 and stg precedent (F081, F083).

## Preconditions

GitHub API accessible (unauthenticated 60 req/hr); arXiv API accessible; web search or public GitHub search available

## Steps

Design experiment protocol with kill gate, sampling strategy, classification rubric; Implement harvesting from GitHub issues, discussion forums, arXiv for target frameworks; Run experiment and collect results; Assess kill gate and document conclusion

## Acceptance criteria

Experiment runs without error, kill gate assessed, results.json contains gate pass/fail, conclusion is GATE_OPEN or GATE_CLOSED with reasoning

## Verification

```bash
ls EXPERIMENTS/XXX-preflight-demand-validation/results.json && python3 -m json.tool EXPERIMENTS/XXX-preflight-demand-validation/results.json
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

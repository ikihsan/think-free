<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-10
-->

<!-- task-meta
id: T-0089
status: done
created: 2026-10-10
claim-agent: unknown-agent
claim-session: 2026-10-10-006-decide-by-measurement-whether-which-dist
claim-vm: 
verify: test -f EXPERIMENTS/090-reverse-index/VERDICT.md
-->

# T-0089 — E090: measure whether a module-to-distribution reverse index for PyPI 

## Goal

E090: measure whether a module-to-distribution reverse index for PyPI is buildable within real constraints, and whether its coverage reaches the modules real code imports

## Why this matters

pyprovides/README.md lists 'which distribution provides a module, in the general case' as unmeasured, and names the obstacle: no reverse index on PyPI and a central directory only answers forward. The 10-of-10 recovery is from controls with a known provider, so the resolver has never answered the question it is named for. T-0088 (VM 0947) measures whether anyone asks; this measures whether the thing can answer at all, and at what cost. Complementary, not overlapping.

## Preconditions



## Steps

1. Declare gates. 2. Run G0 instrument discrimination first, on labels known by construction (per D095). 3. Build the index over the top-K public ranked project list, measuring requests/bytes/wall-clock. 4. Harvest top-level imports mechanically from real repositories. 5. Measure coverage at several K, against the pip-name-normalization baseline.

## Acceptance criteria

PROTOCOL.md declares gates and reachable sets before the run; results.json reports coverage with the K curve, cost, and the baseline comparison; VERDICT.md names the build decision

## Verification

```bash
test -f EXPERIMENTS/090-reverse-index/VERDICT.md
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

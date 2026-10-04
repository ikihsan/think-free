<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0059
status: claimed
created: 2026-10-04
claim-agent: unknown-agent
claim-session: 2026-10-04-047-decide-and-execute-the-highest-informati
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
-->

# T-0059 — Measure whether 'prior art exists' can predict anything about adoption

## Goal

Measure whether 'prior art exists' can predict anything about adoption: does star rank predict package downloads within a niche?

## Why this matters

STATE-next-actions item 0 says prior-art survival cannot be the selection filter because nothing this mission produces passes it. That claim is currently an inference from 12 deaths. It rests on an untested link: that a niche where many mechanisms exist is a niche where the problem is solved. Nobody has measured whether implementation density, or rank within it, predicts measured usage. If it does not, the filter is uninformative and a positive axis can be identified instead.

## Preconditions

Unauthenticated GitHub API only: core 60/hr, search 10/min. Pace the fetches.

## Steps

1. Pick 4+ niches, at least one mature with known high adoption as a contrast, at least two young.
2. Enumerate top-N implementations per niche by GitHub star search.
3. Look up real usage (registry downloads/month) per implementation, any registry, max across registries.
4. Compute within-niche Spearman rank correlation between star rank and usage rank.
5. Compute what fraction of implementations have any measurable usage at all.
6. Record the verdict, the kill gate outcome, and the axes that DO separate used from unused.

## Acceptance criteria

Raw results.json committed; a kill gate with a stated threshold; the verdict names which candidate-selection rule changes and which does not.
Ceiling stated: one endpoint snapshot, search-by-name-and-description, single machine.

## Verification

```bash
python3 -m unittest discover -s tests 2>&1 | tail -3
```

## Rollback

Nothing outside this repository is modified.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

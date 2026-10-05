<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0074
status: claimed
created: 2026-10-05
claim-agent: unknown-agent
claim-session: 2026-10-05-020-e030-test-whether-departure-accounts-peo
claim-vm: 
verify: tools/x -- python3 EXPERIMENTS/030-departure-recurrence/recurrence.py && tools/x -- python3 EXPERIMENTS/030-departure-recurrence/a8_separation.py && tools/x -- python3 EXPERIMENTS/030-departure-recurrence/verify_labels.py treatment && tools/x -- python3 EXPERIMENTS/030-departure-recurrence/verify_labels.py control && tools/origin doc lint
-->

# T-0074 — E030: test whether departure accounts (people publicly leaving a named

## Goal

E030: test whether departure accounts (people publicly leaving a named tool) supply a capability clause that recurs across independent authors and distinct departing tools, above the base rate of ordinary comments; and pilot whether a use account adjudicates fit where a count does not

## Why this matters

29 experiments, no candidate, three generators closed. Every outward observation has been of what people SAY they lack (trigger-harvested needs) or of artifact COUNTS. A departure account is a third evidence class this record has never read: a clause stated by someone who actually depended on the thing and did not get it. It is the only instrument in reach that can (a) state a capability failure from experience rather than from imagination, and (b) recur across independent accounts, which is the demand axis F033 and F039 showed the need corpus cannot supply. It also targets E028's own named gap: 'a product that does the thing without saying so is invisible in both directions'.

## Preconditions



## Steps

declare PROTOCOL.md before any fetch
harvest Ask HN departure-framed posts via Algolia, with a known-answer control and a nonsense control
extract departing artifact and reason text mechanically; keep full text
measure clause recurrence with a rare-shared-vocabulary rule, treatment vs same-story ordinary-comment control
pilot the fit screen on the surviving clusters with use evidence only vs count evidence only

## Acceptance criteria

results.json carries every gate from the declared protocol with its verdict
controls ran before the answer was computed
negative outcome recorded in FAILURES-findings-20.md or a new sibling

## Verification

```bash
tools/x -- python3 EXPERIMENTS/030-departure-recurrence/harvest.py && tools/x -- python3 EXPERIMENTS/030-departure-recurrence/extract.py && tools/x -- python3 EXPERIMENTS/030-departure-recurrence/stats.py && python3 -m unittest discover -s EXPERIMENTS/030-departure-recurrence -p 'test_*.py' -t EXPERIMENTS/030-departure-recurrence && tools/origin doc lint
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-12
-->

<!-- task-meta
id: T-0093
status: open
created: 2026-10-12
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests
-->

# T-0093 — Test whether a discriminating-observation procedure beats a free gener

## Goal

Test whether a discriminating-observation procedure beats a free general assistant's first hypothesis on appliance diagnosis, using a correctly-filtered unanswered pool

## Why this matters

E092 named the residue of the strongest alternative as wrong-first-hypothesis (7 of 37) but closed the line without testing it; D104's reopening limb is untested. Separately, /search/advanced?answered=false was observed live on 2026-10-12 to return ANSWERED questions, so E092's '707 unanswered' pool is 84% answered.

## Preconditions



## Steps

1. Correctly filtered unanswered appliance pool; 2. measure whether base rate is what the assistant misses; 3. comparison arm

## Acceptance criteria

Premise measured on the cached corpus; kill gate declared before measurement

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests
```

## Rollback



## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

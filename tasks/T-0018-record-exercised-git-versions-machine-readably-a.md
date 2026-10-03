<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0018
status: claimed
created: 2026-10-03
claim-agent: opencode
claim-session: 2026-10-03-033-record-git-versions-exercised-and-split
claim-vm: instance-20260717-0947
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
-->

# T-0018 — Record exercised git versions machine-readably and split DECISIONS-PRA

## Goal

Record exercised git versions machine-readably and split DECISIONS-PRACTICE.md

## Why this matters

STATE.md next action 2: no machine-readable record of exercised git versions; DECISIONS-PRACTICE.md at 297/300 lines blocks the next decision entry

## Preconditions

research/origin at remote head; T-0017 untouched (claimed by 0944)

## Steps

1. Add machine-readable git-versions record. 2. Split DECISIONS-PRACTICE.md by invariant. 3. Update indexes and STATE/ROADMAP. 4. Run tests + doc lint.

## Acceptance criteria

- [ ] machine-readable exercised-git-versions file exists and is covered by a test; - [ ] DECISIONS-PRACTICE.md and siblings each under 300 lines; - [ ] doc lint exit 0; - [ ] full test suite green

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && tools/origin doc lint
```

## Rollback

Delete the new task files and revert the split; no experiment output involved.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

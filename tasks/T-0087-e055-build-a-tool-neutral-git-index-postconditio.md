<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-08
-->

<!-- task-meta
id: T-0087
status: claimed
created: 2026-10-08
claim-agent: unknown-agent
claim-session: 2026-10-08-003-fresh-observation-to-find-a-testable-pra
claim-vm: 
verify: python3 EXPERIMENTS/055-index-postcondition/run.py --verify
-->

# T-0087 — E055: build a tool-neutral git index postcondition checker and falsify

## Goal

E055: build a tool-neutral git index postcondition checker and falsify it against its own bytes; measure whether it catches a silently-wrong index (exit 0) in a shipped line-staging incumbent

## Why this matters

F082 closed the stg application on the existence of two shipped incumbents (gah, git-hunk) read from README prose, never measured. Reading both sources shows neither ever reads .git/index back and each takes an unlabelled, different coordinate space, so a caller scripting them gets exit 0 and cannot tell which line was staged. That is a postcondition gap, not a staging gap, and it is the shape F063 measured (78 wrong-but-exit-0 rows across three alternatives) without having a reusable artefact for it. D079 requires the incumbents be measured on bytes, and the oracle has never been run against either of them.

## Preconditions

git >= 2.28 on PATH for the git-hunk arm (building 2.56.0); patchutils for the filterdiff arm; a CPython >= 3.10 for git-hunk (3.12.15 fetched, git-hunk 0.4.2 installed under it); E038 compare.py CASES as the hand-written tool-neutral oracle

## Steps

1. Declare PROTOCOL.md with question, arms, oracle, both controls and the kill gate before any row is read. 2. Build the checker: reads .git/index only, never the stager's own output. 3. Falsify the checker: positive control must reproduce E038's 30-row matrix; negative control must reject every index state E046 injected. 4. Run the arms and score. 5. Record KILL-C.

## Acceptance criteria

results.json with per-row exit, index bytes, checker verdict; C1 and C2 both reported as they fired; a counted KILL-C verdict; doc lint exit 0

## Verification

```bash
python3 EXPERIMENTS/055-index-postcondition/run.py --verify
```

## Rollback

delete EXPERIMENTS/055-index-postcondition and the task file; nothing outside this repository is changed

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

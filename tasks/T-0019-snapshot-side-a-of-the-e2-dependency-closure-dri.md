<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0019
status: claimed
created: 2026-10-03
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0947
verify: test -f EXPERIMENTS/009-lockfile-drift-snapshot/snapshot-a.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/009-lockfile-drift-snapshot/snapshot-a.json'));assert d['schema']=='origin.lockfile-snapshot/1';assert len(d['artifacts'])>=8;assert all(a['sha256'] and a['version'] for a in d['artifacts'])" && tools/origin doc lint
-->

# T-0019 — Snapshot side A of the E2 dependency closure drift comparison

## Goal

Snapshot side A of the E2 dependency closure drift comparison

## Why this matters

STATE.md next action 6: E2 is time-gated; snapshot side A now so a second snapshot weeks later has somewhere to land

## Preconditions

network access to PyPI; pip present

## Steps

1. pip download a fixed small package set with deps into a temp dir. 2. Record name/version/file/sha256/source-url plus tool versions and UTC date as snapshot-a.json. 3. Write README stating no verdict until snapshot B.

## Acceptance criteria

- [ ] snapshot-a.json exists with >=8 hashed artifacts; - [ ] README states the comparison is pending snapshot B; - [ ] doc lint exit 0

## Verification

```bash
test -f EXPERIMENTS/009-lockfile-drift-snapshot/snapshot-a.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/009-lockfile-drift-snapshot/snapshot-a.json'));assert d['schema']=='origin.lockfile-snapshot/1';assert len(d['artifacts'])>=8;assert all(a['sha256'] and a['version'] for a in d['artifacts'])" && tools/origin doc lint
```

## Rollback

Delete EXPERIMENTS/009-lockfile-drift-snapshot/. No other file consumes it.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

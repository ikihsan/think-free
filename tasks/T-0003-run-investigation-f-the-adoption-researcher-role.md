<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0003
status: done
created: 2026-10-03
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0944
verify: test -f RESEARCH/F.md && grep -q 'origin-meta' RESEARCH/F.md
-->

# T-0003 — run investigation F, the adoption researcher role

## Goal

run investigation F, the adoption researcher role

## Why this matters

Every sealed report identifies adoption evidence as the missing ingredient and none could produce a validated user. The adoption perspective is the one that examines how a difficult capability becomes understandable and adoptable without manipulating attention.

## Preconditions

RESEARCH/A.md through D.md are sealed and must not be read before the report is written.

## Steps

1. Read MISSION.md only. Do not read the other reports.
2. Investigate what makes open-source projects of this class adopted or ignored: time to first value, comprehension cost, distribution, and what failed projects did differently.
3. Separate attention from durable value, and identify what evidence would distinguish them before release.
4. Write actionable criteria this repository can satisfy, not generic advice.
5. Write RESEARCH/F.md with sources, dates, and explicit limits on what adoption research can establish without users.

## Acceptance criteria

- [ ] RESEARCH/F.md exists, is sealed, and carries origin-meta.
- [ ] It produces criteria checkable before release.
- [ ] It states what cannot be known without real users.
- [ ] doc lint exits 0.

## Verification

```bash
test -f RESEARCH/F.md && grep -q 'origin-meta' RESEARCH/F.md
```

## Rollback

Delete RESEARCH/F.md; nothing depends on it yet.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

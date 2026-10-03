<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0002
status: claimed
created: 2026-10-03
claim-agent: opencode
claim-session: 
claim-vm: instance-20260717-0944
verify: test -f RESEARCH/E.md && grep -q 'origin-meta' RESEARCH/E.md
-->

# T-0002 — run investigation E, the experimental engineer role

## Goal

run investigation E, the experimental engineer role

## Why this matters

Four of six investigation roles are sealed. The missing experimental-engineering perspective is what would say which mechanisms can be cheaply subjected to hard tests, and the candidate set currently rests on four views.

## Preconditions

RESEARCH/A.md through D.md are sealed and must not be read before the report is written.

## Steps

1. Read MISSION.md only. Do not read RESEARCH/A.md-D.md.
2. Identify mechanisms that can be tested cheaply and hard on this machine: 12 CPUs, about 15 GiB RAM, stdlib Python plus NumPy.
3. For each, write the smallest experiment that could yield a decisive result, including what would make it uninformative.
4. Prefer candidates with a plausible information-sufficiency witness, since that test has killed two proposals in ten lines.
5. Write RESEARCH/E.md with observation, mechanism, assumptions, prior art, strongest objection, falsifying experiment, and explicit epistemic limits.

## Acceptance criteria

- [ ] RESEARCH/E.md exists, is sealed, and carries origin-meta.
- [ ] It names at least two mechanisms with a runnable falsifying experiment each.
- [ ] It does not cite the other reports' hypotheses as its starting point.
- [ ] doc lint exits 0.

## Verification

```bash
test -f RESEARCH/E.md && grep -q 'origin-meta' RESEARCH/E.md
```

## Rollback

Delete RESEARCH/E.md; nothing depends on it yet.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

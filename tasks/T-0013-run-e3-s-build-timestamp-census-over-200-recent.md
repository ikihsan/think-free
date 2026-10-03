<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-03
-->

<!-- task-meta
id: T-0013
status: open
created: 2026-10-03
claim-agent:
claim-session:
claim-vm:
verify: test -f EXPERIMENTS/005-build-timestamps/results.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/005-build-timestamps/results.json'));assert d['sample']['wheels_inspected']>=200;assert 'violation_fraction' in d['census'];assert d['gate']['verdict'] in ('weak-lead','lead-survives')"
-->

# T-0013 — Run E3's build-timestamp census over 200 recent PyPI wheels and apply 

## Goal

Run E3's build-timestamp census over 200 recent PyPI wheels and apply its 5% kill gate

## Why this matters

RESEARCH/E.md mechanism E3 is the only E mechanism whose killing experiment is runnable today (one command, minutes) and whose number is genuinely unmeasured. Its kill gate is hard: below 5% non-normalized timestamps the lead ends. E.md's cross-cutting rule 4 says absence of a result is not a result, and all three E mechanisms are still untested.

## Preconditions

Public access to the PyPI JSON API; this VM has it (probed 2026-10-03)

## Steps

1. Pick ten packages by PyPI download order as stated in E.md, take the 20 most recent wheel releases of each, prefer the smallest wheel per release so the sample fits a bounded download.
2. For each wheel, open the zip and record every ZipInfo.date_time, whether all entries are normalised to 1980-01-01, and any epoch-like timestamp string in METADATA or RECORD.
3. Report the fraction of wheels with any non-normalized entry date, the per-ecosystem caveat, and what the sample cannot bound.
4. Apply the gate: below 5% is a weak lead and E3 ends.
5. Record the result in EXPERIMENTS/005-build-timestamps/README.md and in HYPOTHESES.md or FAILURES.md.

## Acceptance criteria

- [ ] At least 200 wheels inspected, with the package list and selection rule recorded
- [ ] Every wheel's zip entry dates are read from the artifact, not inferred from metadata
- [ ] The violation fraction is computed and reported as an estimate over the sample, with its limits stated
- [ ] The 5% gate is applied and the verdict recorded
- [ ] Raw per-wheel data is committed to results.json
- [ ] No claim is made about npm, conda, or Maven

## Verification

```bash
test -f EXPERIMENTS/005-build-timestamps/results.json && python3 -c "import json;d=json.load(open('EXPERIMENTS/005-build-timestamps/results.json'));assert d['sample']['wheels_inspected']>=200;assert 'violation_fraction' in d['census'];assert d['gate']['verdict'] in ('weak-lead','lead-survives')"
```

## Rollback

Delete EXPERIMENTS/005-build-timestamps/ and the HYPOTHESES or FAILURES entry; the census is a measurement with no code other consumers depend on

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

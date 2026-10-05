<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0072
status: claimed
created: 2026-10-05
claim-agent: opencode
claim-session: 2026-10-05-017-e028-test-whether-the-incumbents-a-prior
claim-vm: 
verify: python3 -m unittest discover -s EXPERIMENTS/028-incumbent-fit -p 'test_*.py' -t EXPERIMENTS/028-incumbent-fit && tools/origin doc lint
-->

# T-0072 — Test whether the incumbents a prior-art screen named actually do what 

## Goal

Test whether the incumbents a prior-art screen named actually do what each killed candidate's distinguishing requirement asks

## Why this matters

Prior art is the plurality kill reason in the record (10 of 18, F044) and every one of the twelve sealed-report candidates died on it, yet the record's own honest limitations say no need has been shown to be served by the incumbents a screen names, and E020's H2 is not evaluable. E016 measured whether prior art EXISTS; nobody has measured whether it FITS the clause's distinguishing attribute. E016's own note on the atomic-distro row says the recovery was 'of the category, not of the clause's distinguishing attribute', and E024's rows.json shows three sealed-report prior-art deaths (A2, C1, C3) that name no artifact at all.

## Preconditions

No new population is harvested; the two existing captures are read-only inputs

## Steps

Declare the protocol, gates and population before any label is produced
Build the population from E024 rows.json and E016 attributions.jsonl; record for each prior-art death its requirement text and the incumbents a screen named
Fetch each named incumbent's own published documentation into raw/ and record HTTP status per fetch
Two blind readers label each pairing category_only / attribute / partial / unreadable, with no access to the other reader's labels or to the screen's verdict
Calibrate a lexical attribute-match index against deliberately mismatched control pairings, and against the rows E016 already declared served beyond argument
Compute Cohen kappa on the four-category scheme, Wilson intervals, and the declared gate
Record F048, D060 if a decision follows, and update STATE-next-actions item 0 and 0d

## Acceptance criteria

Every prior-art death in the population is either labelled by two readers or carries a stated reason it could not be, and the gate reports one of three answers including not_evaluated

## Verification

```bash
python3 -m unittest discover -s EXPERIMENTS/028-incumbent-fit -p 'test_*.py' -t EXPERIMENTS/028-incumbent-fit && tools/origin doc lint
```

## Rollback

The experiment is additive; delete the directory and the finding if it fails

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

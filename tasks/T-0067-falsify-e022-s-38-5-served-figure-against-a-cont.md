<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0067
status: done
created: 2026-10-05
claim-agent: opencode
claim-session: 2026-10-05-009-falsify-e022-s-38-5-served-figure-agains
claim-vm: 
verify: python3 EXPERIMENTS/023-served-baseline/draw_arms.py --verify && python3 EXPERIMENTS/023-served-baseline/analyse.py
-->

# T-0067 — Falsify E022's 38.5% served figure against a control arm of ordinary c

## Goal

Falsify E022's 38.5% served figure against a control arm of ordinary comments in the same threads

## Why this matters

E022's 'served' cell had no control: its C1 and C2 both measure 'answered', and its own protocol says 'answered is not served'. The 15/39 = 0.385 hand-labelled rate was the number that let the record conclude the corpus records needs the world 'absorbed conversationally'. A rate with no population behind it cannot distinguish a striking rate from an ordinary one.

## Preconditions

Public Algolia and Firebase HN APIs reachable, no auth needed. Prior captures at EXPERIMENTS/022-need-outcomes/raw/ must be present.

## Steps

1. Write PROTOCOL.md before reading any reply: arms, gates, and the strongest alternative. 2. Verify the reply reader against fabricated ids before trusting it. 3. Draw both arms at E022's seed and rule; control arm is ordinary comments in the need arm's OWN stories, restricted to ANSWERED so both arms share the 'a reply exists' condition. 4. Label blind, without consulting E022's labels.tsv, so the agreement statistic is meaningful. 5. Compute label agreement (gate B3) BEFORE the arm comparison (gate B2). 6. Record F043 and D055, and withdraw only the inference.

## Acceptance criteria

Both arms drawn and readable at >=95%; a nonsense control passes on both API readers; gate B3 reports Cohen's kappa on the shared rows; gate B2 reports whether the Wilson intervals overlap; the finding states which of E022's numbers survive and which is withdrawn.

## Verification

```bash
python3 EXPERIMENTS/023-served-baseline/draw_arms.py --verify && python3 EXPERIMENTS/023-served-baseline/analyse.py
```

## Rollback

Delete EXPERIMENTS/023-served-baseline/ and revert the records. Nothing outside this repository is modified; no external publication.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- task-meta
id: T-0073
status: claimed
created: 2026-10-05
claim-agent: opencode
claim-session: 
claim-vm: 
verify: cd /home/ubuntu/think-free && PYTHONPATH=tools:tests python3 -m unittest discover -s EXPERIMENTS/029-need-build-match -t EXPERIMENTS/029-need-build-match
-->

# T-0073 — Test whether the need-staters who publicly shipped something shipped t

## Goal

Test whether the need-staters who publicly shipped something shipped the thing they said was missing, against a mismatched-pair control

## Why this matters

F042's '0 of 24 unserved requesters built the thing' is the cell that closes the demand-side corpus in item 0d, and E025 declared it a floor on disclosure rather than an estimate. E025 then opened a much larger door it did not walk through: 278 of the 1250 need-staters have a show_hn item. Nobody has joined the two captures. That join is one public API per builder and answers the only question the closure turns on: does a stated need predict what the person who stated it went on to ship?

## Preconditions

E022 outcomes and texts, E025 need_arm, and the Algolia index are all reachable and unchanged; re-verify their digests before use.

## Steps

Declare PROTOCOL.md before any fetch, with the mismatched-pair control and the negative control declared able to return not_evaluated.
Fetch the show_hn item titles for every need-arm builder and the story titles for their need statements; append-only captures.
Two blind readers label a matched sample and a mismatched sample on one rubric, with pairing hidden.
Report matched against mismatched and against the thread-title control; a positive is not published unless it beats both.

## Acceptance criteria

results.json carries matched, mismatched and story-title arms with intervals, the reader agreement figure, and the negative control's verdict.
Either the matched arm separates from mismatched and from the story-title arm, or F042's third cell is reported as confirmed on a 278-row instrument rather than a 24-row one.

## Verification

```bash
cd /home/ubuntu/think-free && PYTHONPATH=tools:tests python3 -m unittest discover -s EXPERIMENTS/029-need-build-match -t EXPERIMENTS/029-need-build-match
```

## Rollback

The experiment is additive under EXPERIMENTS/029- and changes no existing capture.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

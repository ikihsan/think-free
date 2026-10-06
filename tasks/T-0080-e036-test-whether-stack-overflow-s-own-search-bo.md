<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- task-meta
id: T-0080
status: done
created: 2026-10-06
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && python3 EXPERIMENTS/036-search-backlog/tally.py
-->

# T-0080 — E036: test whether Stack Overflow's own search box already returns the

## Goal

E036: test whether Stack Overflow's own search box already returns the score-tail duplicate backlog that no tab ordering returns

## Why this matters

Item 0f names this as the one alternative the line never tested and the strongest accessible alternative to the prototype. A person's own search box is what someone with a problem types into; /search/advanced and /search/excerpts are reachable from this host while every stackoverflow.com page is not. If search already returns the population, the candidate dies to the platform's own search before anything is built. If it does not, the record learns that retrieval is also blind, which is the one remaining measurement separating this from the four surfaces E035 already falsified.

## Preconditions

Unauthenticated Stack Exchange quota is shared per IP; the declared design needs roughly 40 requests for the search arms

## Steps

Declare the question, the baseline, the failure condition and the positive control in PROTOCOL.md before any request
Verify reachability of /search/advanced and /search/excerpts from this host and record the status codes
Build the query set from E034's committed bytes: the tail duplicates' own titles, plus the Active arm as the control arm
Run the positive control first: prove the instrument can recover a known-findable population before reading any tail number
Measure recovery rate and rank, tail against Active, on equal denominators
Return not_evaluated rather than a rate wherever the canonical id or the result parse is unreadable

## Acceptance criteria

A gate that fires on a declared rule, a positive control that recovers independently real positive examples, and a stated verdict naming what the run does and does not decide

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && python3 EXPERIMENTS/036-search-backlog/tally.py
```

## Rollback

raw/ is append-only evidence; revert the experiment directory and the record edits

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

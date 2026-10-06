<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- task-meta
id: T-0079
status: claimed
created: 2026-10-06
claim-agent: unknown-agent
claim-session: 2026-10-06-004-test-whether-the-population-e034-found-i
claim-vm: 
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && python3 EXPERIMENTS/035-unanswered-surface/tally.py
-->

# T-0079 — E035: establish whether the score-tail population E034 found is reacha

## Goal

E035: establish whether the score-tail population E034 found is reachable through any surface Stack Overflow offers, and whether its own answerer surface contains it

## Why this matters

Item 0e's declared next action (30 more requests, 3-4 more tags per site) was ranked the mission's top action on the premise that tag/site attribution was the binding constraint. Four reads of E034's committed bytes cost zero quota and address the premise first: is the population reachable, are the compared arms one population, is the declared remedy aimed at the constraint, and does the obvious objection survive. The strongest accessible alternative -- tab=Unanswered -- had never been measured.

## Preconditions

Unauthenticated Stack Exchange quota is 76 of 300 and shared per IP; the declared population needs 21

## Steps

Read the committed bytes for reachability, commensurability and variance components before any request
Enumerate the orderings a real tag page renders, from an archive snapshot, since stackoverflow.com is Cloudflare-blocked from this host
Declare gates as an exclusive partition or a statistic over the relation, per D064
Fetch /questions/unanswered for E034's eight declared tags and compare id sets, not rates
Return a third answer for the density gate if the label is unreadable, rather than a rate off an absent field

## Acceptance criteria

PROTOCOL.md declares the population, the gates and the kill conditions before any fetch; README.md states the verdict, the ceilings and what the run does not establish
A prototype reader runs offline on committed bytes and reproduces its own output

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests && python3 EXPERIMENTS/035-unanswered-surface/tally.py
```

## Rollback

All four results are computed from committed bytes by analyse.py, so deleting the new directory loses the experiment and nothing else

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

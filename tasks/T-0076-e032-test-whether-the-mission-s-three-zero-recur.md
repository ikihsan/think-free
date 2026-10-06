<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-06
-->

<!-- task-meta
id: T-0076
status: open
created: 2026-10-06
claim-agent:
claim-session:
claim-vm:
verify: cd /home/ubuntu/think-free && python3 EXPERIMENTS/032-venue-recurrence/tally.py --check
-->

# T-0076 — E032: test whether the mission's three-zero recurrence result is a fac

## Goal

E032: test whether the mission's three-zero recurrence result is a fact about public conversation or a fact about the one venue all three populations came from (Hacker News comments via the Algolia API)

## Why this matters

F039 (E019), F049 (E029) and F051 (E031) all returned zero cross-author recurring requirements, and STATE-in-flight-2.md line 120 generalises that to 'mining public conversations - three populations, three instruments, three zeros'. All three populations were harvested from hn.algolia.com comment search: E012's raw file is named raw/hn_needs_2026-10-04.jsonl, E019 and E030 both call C.algolia_pages against https://hn.algolia.com/api/v1/search. Three samples from one venue differing only in trigger vocabulary do not license a claim about public conversation. F051's own ceiling says 'One corpus and one channel set ... remain unread', so the finding is honestly bounded and the summary sentence is what over-reaches.

## Preconditions

No fetch before PROTOCOL.md exists; a declared linkage rule must be shown reachable against its own chance expectation (D062).

## Steps

1. State the confound as a finding and correct the summary sentence, before any fetch. 2. Declare PROTOCOL.md with gates before any fetch. 3. Harvest a structurally different venue by a structural rule carrying no requirement vocabulary. 4. Extract one requirement clause per author with a reader question. 5. Adjudicate candidate clause pairs against reader-adjudicated random control pairs, with the same four instrument gates E031 passed.

## Acceptance criteria

Either the zero reproduces on a second venue class and the mission's belief is strengthened from a venue claim to a general one, or it does not and the generator is reopened. Either result changes a decision; the confound alone does not.

## Verification

```bash
cd /home/ubuntu/think-free && python3 EXPERIMENTS/032-venue-recurrence/tally.py --check
```

## Rollback

Nothing outside EXPERIMENTS/032-venue-recurrence/ and the records that name it.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0062
status: open
created: 2026-10-04
claim-agent:
claim-session:
claim-vm:
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
-->

# T-0062 — Re-adjudicate E012's 19 prior-art kills on three corpora with positive

## Goal

Re-adjudicate E012's 19 prior-art kills on three corpora with positive controls, so F029's largest cause of death rests on a procedure that can be shown to work

## Why this matters

F029 killed 19 of 50 harvested needs with 'a tool already serves this', and that same verdict killed all 12 prior candidates. F030 showed a one-query verdict is wrong in both directions, and only 6 of the 19 have a populated count behind them; 13 rest on judgement. The open web, which is where a hosted or commercial tool is visible, has never been read by any prior-art probe here. Positive controls are the 6 well-supported kills: a procedure that cannot recover them is invalid and says nothing about the other 13.

## Preconditions

Unauthenticated GitHub search (10/min) and core (60/hr) APIs, PyPI/npm/crates search, and a general web search. Pace the fetches; a refused answer is kept apart from an absence.

## Steps

1. Declare both gate arms, the three corpora, the phrasings and the stopping rule in EXPERIMENTS/016/README.md before any count is read. 2. Adjudicate the 6 positive controls first. 3. Adjudicate the remaining 13 on GitHub in:name,description, then package registries, then the open web; stop at the first attributed serving artifact, never record 'none found' on one phrasing. 4. Write results.json with the corpus-level verdicts, the items with no prior art found, and what each corpus could not see.

## Acceptance criteria

Both gate arms answered in one direction from results.json, the controls' recovery rate reported whatever it is, and the finding recorded with the instrument's stated blindness.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
```

## Rollback

Raw captures are append-only under EXPERIMENTS/016/raw/; removing the directory removes the experiment.

## Notes

**Twice renumbered on the unpushed side, 2026-10-05.** This task was T-0061
until instance-20260717-0947 published and claimed a *different* T-0061
("is the prior-art screen's young-vocabulary population mostly documents?") at
23:51Z, while this task's own claim had not been pushed. The rule renumbers the
unpushed side, so this file is T-0062 and the ledger's `create` line carries
`renumbered_from: T-0061`; the other VM's pushed and claimed T-0061 is untouched.
Both VMs opened a session numbered `2026-10-04-056`, which is expected — the
number is per VM — and it is the *task* number that collided.

Separately, the other VM landed `F034`
("the prior-art screen's premise holds in mature vocabularies and largely fails
in young ones") and `EXPERIMENTS/015-incumbent-serving` while this task was
running, so this experiment is `016-prior-art-adjudication` and its findings are
**F035** and **F036**. Renumbering happens on the side that has not been pushed;
the session event stream and its generated report keep the paths as they were
run, because a closed log is not edited.

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

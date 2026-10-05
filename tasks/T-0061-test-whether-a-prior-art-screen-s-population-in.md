<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-04
-->

<!-- task-meta
id: T-0061
status: done
created: 2026-10-04
claim-agent: unknown-agent
claim-session: 2026-10-04-056-classify-the-prior-art-population-by-art
claim-vm: 
verify: PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
-->

# T-0061 — Test whether a prior-art screen's population in a young vocabulary is 

## Goal

Test whether a prior-art screen's population in a young vocabulary is mostly documents, and read what those documents teach people to do by hand

## Why this matters

F034 measured that the prior-art screen's premise ('a tool exists, therefore the need is served') holds 4/4 in mature vocabularies and 1/4 in a young one. It could not distinguish two explanations: (i) young-vocabulary needs are genuinely unserved, or (ii) the screen's instruments cannot see young-vocabulary tools. A third explanation has never been tested and is visible in the population already collected: in a young vocabulary the highest-starred matches for a need-phrase are frequently not tools at all but documents (guides, showcases, prompt collections, reference lists). If so, 'prior art exists' is being satisfied by prose, the need is real and acknowledged at scale, and the screen is not measuring competition. This experiment classifies the 48 rows EXPERIMENTS/015 already collected by artifact type from primary evidence, joins that to the serving figures 015 measured, and hand-reads the top young-vocabulary documents for the procedure each teaches.

## Preconditions



## Steps

1. Declare the classification rules and both gates in EXPERIMENTS/016-artifact-type/README.md before any figure is read.
2. Classify each of the 48 rows of EXPERIMENTS/015/results.json by its repository's root file listing and release existence (primary evidence, one core request per row). Unreadable rows are a third class and are never silently dropped.
3. Join the classification to 015's serving figures and tally by class, young-vocabulary arm separately from mature.
4. Hand-read the top 10 young-vocabulary nonexecutable artifacts; for each record the procedure it teaches, whether the procedure is repeated, and whether it offers a runnable install or a link to software that performs it.
5. Run the self-check: inject rows whose classification is known (a manifest-less repo, a repo with a Dockerfile, an unreadable repo) and assert the classifier answers as declared in both directions.
6. Write results.json, the finding, and the decision change.

## Acceptance criteria

The classifier is falsified against known-answer rows in both directions.
Both declared gates are reported whatever they say, and an inconclusive result is reported as inconclusive.
The candidate seeds are written as concrete procedures, not as a statistic.
doc lint exits 0.

## Verification

```bash
PYTHONPATH=tools:tests python3 -m unittest discover -s tests -t tests 2>&1 | tail -3
```

## Rollback

git revert the commits; the experiment directory is additive.

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

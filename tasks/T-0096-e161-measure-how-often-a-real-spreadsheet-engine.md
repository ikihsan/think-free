<!-- origin-meta
owner: tasks/INDEX.md
status: active
last-verified: 2026-10-15
-->

<!-- task-meta
id: T-0096
status: done
created: 2026-10-15
claim-agent:
claim-session:
claim-vm:
verify: python3 -m unittest discover -s EXPERIMENTS/161-csv-spreadsheet-coercion -t EXPERIMENTS/161-csv-spreadsheet-coercion
-->

# T-0096 — E161: measure how often a real spreadsheet engine silently alters real

## Note on the verify command

It was declared as `python3 EXPERIMENTS/161-csv-spreadsheet-coercion/roundtrip.py`,
which needs the fetched corpus and a LibreOffice install, so it is a
reproduction command rather than a completion check. It was replaced by the
prototype's test suite, whose expectations are the engine's own measured
outcomes, recorded in `results-*.json` and `sample-changes-*.tsv`. The
reproduction path is in the experiment's `README.md`.

## Goal

E161: measure how often a real spreadsheet engine silently alters real-world CSV files, and test a deterministic checker against that ground truth

## Why this matters

Public demand probe (Stack Exchange, 6 sites) and prior-art probe (GitHub/PyPI/npm) both come back weak for a CSV coercion linter: a handful of high-vote reports and several 0-star tools. Before building, measure the mechanism on real files with a real engine instead of on synthetic fixtures, which is the failure mode the record itself names for E122/E147/E150/E160.

## Preconditions

libreoffice-calc installable via apt on this VM

## Steps

harvest real CSVs from >=5 independent public sources; round-trip each through LibreOffice headless to xlsx; diff every cell against the source with a stdlib xlsx reader; report files affected, cells changed, and the rule classes behind the changes

## Acceptance criteria

results.json exists with corpus file count, source count, files affected, cells changed, and a rule-class histogram; the verdict is written against the predeclared kill gate

## Verification

```bash
python3 EXPERIMENTS/161-csv-spreadsheet-coercion/roundtrip.py
```

## Rollback

delete the experiment directory; nothing outside it changes

## Notes

Append observations here. Record outcomes as events with
`tools/origin session experiment-result`.

<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-13
-->

# 125 — can a third party point `preflight` at their own harness?

`observed` 2026-10-13, Python 3.8.10, `instance-20260717-0947`.

| file | what it is |
|---|---|
| [`PROTOCOL.md`](PROTOCOL.md) | pre-declared before any third-party repository was fetched: two questions, the population rule, six measurements, five gates, two controls, the information-sufficiency witness, and the build decision the run changes. |
| [`AMENDMENT-1.md`](AMENDMENT-1.md) | three instrument corrections made after a pilot and before the measurement run: a capped candidate list that measured the cap, a loader that read YAML as data, and Git-LFS pointer text read as records. |
| [`RESULT.md`](RESULT.md) | the run: population, coverage, the five pairs, the witness, the gate accounting, and the build decision. |
| [`results.json`](results.json) | gate accounting and headline figures, computed by `gate.py` from the files below. |
| [`coverage.json`](coverage.json) | the full-population coverage pass: 2,427 data files, 857 sampled, 210 readable, sides, unreadable reasons. |
| [`pairs-sampled.json`](pairs-sampled.json) | M4-qualified pairs with their C1 verdicts, the 32 refusals with reasons, and the 17 single-file both-sided records. |
| [`controls.json`](controls.json) | both declared controls and the witness output. |
| [`sample.json`](sample.json), [`fieldnames.json`](fieldnames.json) | the 857 per-file sampling outcomes; field-name frequencies the vocabulary was calibrated against. |
| [`inspect.json`](inspect.json), [`pool.json`](pool.json), [`search-raw/`](search-raw) | the frozen population: 117-row pool, the 30 above the floor, the 22 chosen, and the raw search responses. |
| `trees/*.tsv` | every file in every cloned repository, with its size and its commit id. |

## Reproduce

```
cd EXPERIMENTS/125-third-party-harness-preflight
python3 pool.py            # the declared draw, three searches (unauthenticated, ~25s)
python3 screen_readme.py   # the README arm of the declared screen
python3 fetch.py           # --depth 1 --filter=blob:none into $E125_SCRATCH
python3 probe.py           # path-matched candidates, M4, C1
python3 coverage.py        # the deterministic 857-file sample, all fields
python3 pair_sampled.py    # M4 and C1 over that sample
python3 controls.py        # both controls and the witness
python3 gate.py            # the gate accounting
```

`$E125_SCRATCH` defaults to `/tmp/opencode/e125` and is the only thing not in
this repository.

## The one-line answer

**Internal.** C1 caught nothing in 5 qualified pairs and, on the arm where a
join demonstrably works, it fires anyway: **a false-positive rate of 1.00** on a
positional join. The population the tool would be released for commits its task
data and almost none of its model output — 21 of 857 sampled files carry an
output-shaped field, and **0.2450** of sampled data is openable by a
standard-library reader at all. G1 fails on its pair term (5 against a declared
10), so the external premise is `not_evaluated` rather than disproved.
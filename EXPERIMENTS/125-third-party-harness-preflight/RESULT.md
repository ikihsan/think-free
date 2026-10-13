<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-13
-->

# E125 RESULT — `preflight` stays internal, and C1 has a false-positive rate of 1.00 on a working join

`observed` 2026-10-13, Python 3.8.10, `instance-20260717-0947`.
Gates are computed by `gate.py` from the artefacts; the raw numbers are in
`results.json`, `coverage.json`, `pairs-sampled.json` and `controls.json`.

## 1. The build decision

**`preflight` stays an internal instrument and is not released.** Not withdrawn:
the two defects it was built for are real and it catches them on E116's
committed key. Not released: the population it would be released *for* does not
supply a working example.

| gate | declared | measured | verdict |
|---|---|---|---|
| **G1** | ≥20 repos inspected, **≥10 qualified pairs**, screen coverage ≥0.90 | 22 inspected ✓, **5 pairs** ✗, 1.0000 ✓ | **FAIL** |
| **G2** | zero-adapter fraction ≥0.30 | **5/5 = 1.0000** | PASS |
| **G3** | ≥1 qualified pair with `SILENT_NO_MATCH` | **0** | **FAIL (not observed)** |
| **G4** | ≥0.50 of flagged rows are field joins | 0 rows flagged | `not_evaluated` |
| **G5** | ≥1 row where the baseline does not protect the join | **0** | **FAIL** |

**Verdict `not_evaluated`**, by the protocol's own rule: G1's pair term is 5
against a declared 10. So G3's zero is *not* a refutation of the external
premise — the population large enough to test it does not exist inside this one.

## 2. The population, and what is in it

22 repositories: the union of three declared GitHub searches, `sort=stars`,
≥300 stars, passing a screen that requires a scoring verb and an evaluation noun
in the description **or** the README. Screen coverage **1.0000** (30 of 30
decidable). The set was committed before a single file was cloned.

- **2,427** data files (`.json`/`.jsonl`/`.csv`/`.tsv`, under 8 MB) across them.
- **857** sampled by one declared rule (every *k*-th of each sorted listing,
  *k* = ⌈n/120⌉).
- **210 readable by a standard-library reader — 0.2450.** The unreadable 647
  break down as **483 top-level JSON objects** (a mapping, not a record array),
  **112 Git-LFS pointers** whose bytes the partial clone never fetches, 28
  unparseable JSON, 12 unparseable JSONL, 9 single-row files.
- Sides by field name: **key-ish 47, output-ish 4**, both-sided in one record set
  17, unclassifiable 142. **21 of 857** files carry any output-shaped field.

So the most popular LLM-evaluation harnesses commit their **task data**, and
almost none of them commit **model output**.

## 3. The zero-adapter path works — on five pairs, and two of them are real

Five pairs satisfy M4 (shared identifier-shaped field name, row counts within
10×). Every one was handed to `preflight.concordance` at **0 adapter lines**, and
all five returned `OK`; `best_rate` 1.0 on four, 0.6667 on one. No type
conflict, no `SILENT_NO_MATCH`.

A hand read of the five paths — one reader, labelled `hand_read` — finds that
**2 are genuine** (a `reviews/<model>/<task>.jsonl` beside its
`predictions/<model>/<task>.jsonl`, both from `modelscope/evalscope`) and **3 are
M4 false positives**: `claw-eval/claw-eval`'s pair is two *different tasks'* CRM
fixtures that happen to share `customer_id`, and two of the evalscope pairs are
one task's review against *another task's* predictions from *another model*.

**M4 is not sufficient to establish "one run".** It was declared as sufficient
and it is not; a repository-relative or task-directory constraint is needed, and
that constraint is harness-specific knowledge — the adapter tax in another guise.

## 4. The witness holds, and C1 alone would have produced a false alarm

Control 2 builds one pair of files and reads it two ways. Under a positional
join the join works. Under a field join the same bytes match nothing.
`concordance` on the **same bytes** returns **`SILENT_NO_MATCH`, best_rate 0.0**
— a **false-positive rate of 1.00** on the positional arm.

E124 declared that "no case here measures an arm on which the verifier is
demonstrably sound". This is that arm, and the number is 1.00. Nothing prevents
it except knowing the join kind (M2), which means reading the harness's scorer —
per harness, by hand.

Control 1 passes both ways and records a distinction worth keeping: **the sound
pair does not exist as a committed file.** `116-berka-service-test/key.jsonl`
holds the defective integer ids (case A, `SILENT_NO_MATCH`); `score.py` composes
`"%s%03d" % (arm, account_id)` at load time and *that* is case B (`OK`,
`best_rate` 1.0). A control written against the committed file alone would have
failed for the right reason and been read as a defect in the tool. It did, for
about one run, and the committed artefact is not the artefact the scorer uses.

## 5. Why the join preflight inspects is not there (2 of 22, read by hand)

`source-supported` for the two read; `inferred` for the population.

- **`openai/evals` (19,593★).** Recording is an append-only event stream:
  `Event(run_id, event_id, sample_id, type, data, created_by, created_at)`
  written to a local JSON file or Snowflake. `evals/metrics.py:get_accuracy`
  sums `event.data["correct"]`, a bool the eval's own scoring function computed
  inline against the sample it already held. No key file, no join.
- **`modelscope/evalscope` (3,530★).** `Sample(id, input, target)` is an object
  in memory; the scorer takes the sample and the model output together and
  returns a `Score`. Where output *is* persisted, it lands in
  `examples/viz/<model>/predictions/<model>/<task>.jsonl` beside its review file,
  joined by an index **within one task directory**.

F121's silent-no-match shape needs two separate tables joined by an identifier.
That is not how these harnesses are built: the sample that carries the expected
answer is the same object the output is scored against. That is the mechanism
behind G3's zero, and it is a mechanism reading, not a prevalence estimate.

## 6. What this does not show

- **It does not show the defect is absent outside this repository.** The
  population with a qualified pair is 2 genuine pairs from 1 repository. That is
  `untested`, not `disproved`.
- It says nothing about harnesses below 300 stars, or about the run outputs a
  user actually holds — a *run's* predictions are written by the harness at run
  time, and nothing here observed a run.
- The screen admits repositories that document an evaluation workflow rather
  than ship one (`responsibleai/ASSERT` is a `.claude/skills` workflow). So the
  22 are "popular things matching the vocabulary", not 22 code harnesses.
- M5, the baseline column, was **never measured** on a qualifying row, because
  there was no qualifying row. There is no claim here about whether a real
  harness's tests protect its join.

## 7. Reopening

The one question this leaves that is cheap and unanswered: **does a harness's
run output directory have the shape preflight needs?** Every repository here was
read at its committed state, and committed state is not what a user points a
tool at. One repository's output writer, read end to end, would settle whether
the tax is the 0 lines measured here or something a loader library has to solve
first — and 0.2450 readability says that question comes *before* concordance.
<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E134 — point `preflight` at a run of a harness nobody here wrote

Pre-declared 2026-10-14, before the harness was installed and before one byte of
foreign run output was read. Commit order is the evidence: this file precedes the
install log.

## The question

`preflight` exists to answer one question before a number is trusted: *may this
instrument report a rate at all?* It was built in E124 and validated on five
committed cases, **all of them from this repository**. Its own README carries the
limitation:

> **Two harnesses from one repository:** … They establish nothing about any
> harness outside this repository.

E125 then measured the population of popular harnesses and found 5 qualified
key/output pairs in 22 repositories, 2 of them genuine, and kept the tool
internal. E128–E133 re-opened it by *reading four foreign output writers*
(`modelscope/evalscope`, `openai/evals`) and by writing adapters for four formats
— JSONL, CSV, YAML, XML — that **this experiment constructed itself**. E125's own
§6 names the gap: *a run's predictions are written by the harness at run time,
and nothing here observed a run.*

**No run of a foreign harness has been observed.** That is the question.

## Why a real run rather than another committed file

E125 screened committed files and found 4 output-sided files among 210 readable
ones: harnesses commit their **task data**, not their **model output**. The
population `preflight` would be released *for* is not the committed repository —
it is a person standing at a terminal after an eval finished, holding
`results/`. So the object has to be produced, not found.

## Arms

| arm | what it is | why |
|---|---|---|
| **A** | a real run of `EleutherAI/lm-evaluation-harness` v0.4.4 — the harness behind the Open LLM Leaderboard and most published LLM numbers — with `--model dummy`, `--log_samples`, `--limit 5`, on tasks chosen before reading any output | the closest thing to the population preflight is released for, produced by a party with no connection to this repository |
| **B** | foreign run outputs *published by other parties* — not EleutherAI — from public sources, no authentication | the strongest accessible alternative to "one run": a number someone else published and is being cited |
| **C** | two defects injected into Arm A's **real emitted format** | the falsification arm: a check that cannot fail is not a check |

Arm A uses `--model dummy` on purpose: random responses, so nothing here says
anything about model behaviour. What it does test is **the harness's plumbing** —
the join between a row it scored and the row it shipped, and the aggregate it
printed. That is the entire surface `preflight` claims.

## The checks

`preflight`'s three committed checks run unchanged:

- **C1 concordance** — do the key's identifiers and the output's identifiers name
  the same entities?
- **C2 alternate-form FP** — rate at which a flagger condemns items known right.
- **C3 control arm** — is a declared negative arm negative by independent evidence?

Plus one measurement **declared here, before Arm A ran**, because it is the only
one that works on a third party's output with no extra input from its author:

- **R1, row recomputation.** Recompute the headline rate from the shipped
  per-row verdicts and compare it to the rate the harness printed. If they
  disagree, the printed number describes something other than the rows it
  shipped — dropped rows, a filter, a dedup, an off-by-one, a subset that was
  never declared. This needs no gold labels and no author cooperation, which is
  why it is the check that transfers.

## Gates

| gate | declared | meaning |
|---|---|---|
| **G1** | Arm A produces run output with ≥5 rows carrying both a target and a verdict | the population object exists |
| **G2** | ≤60 lines of stdlib Python bring Arm A's **real emitted format** into `key_rows`/`out_rows`, written by reading the emitted files only | D046's "the adapter tax is a few lines" tested on a real format instead of four constructed ones |
| **G3** | preflight's verdicts on Arm A and on every reachable Arm B output are recorded, **and** R1's recomputation either agrees with every printed rate, or every disagreement is a hand-verified true positive | the checks were run on foreign data, not declared |
| **G4** | both Arm C defects — an identifier field renamed on one side; a verdict column dropped from the final row — are caught by the adapter-plus-preflight path, and the un-defected Arm A output is clean | the path can fail |
| **G5** | ≥1 Arm B output published by a party other than EleutherAI is reachable without authentication | the external population is reachable in public form at all |

**Kill gate.** G5 fails → the external population is not reachable in a public
form, E125's conclusion is confirmed by a second and independent route,
**D046's release condition is not met**, and the six sessions spent packaging
the tool are recorded as their cost.

**Declared failure condition for the whole line.** If Arm A's run output is
clean under C1 and R1 agrees with the printed rate, then `preflight` has **no
observed external value**: it catches defects this repository made and nothing
else. That is a result, it closes the release question, and it is cheaper than
the packaging that would otherwise continue.

## Baseline — the strongest accessible alternative

1. **lm-eval's own declared gates and its own result-integrity checks.** The
   incumbent, free, and always available. Whatever preflight finds, this must not
   already have found.
2. **A hand read of the output** — what F118 did, 50 rows, after the run.

Both are recorded beside preflight's output on the same bytes. A preflight that
adds nothing over baseline 1 has no use, whatever its gates say.

## Ceilings declared now

- `--model dummy` returns random responses. This experiment says nothing about
  scoring *quality*, and nothing about any model's behaviour.
- One harness, one version, one invocation shape, a handful of tasks.
- Arm B is whatever public searching yields. It is **not** a random sample of
  published evaluation results, and no prevalence claim may be made from it.
- This VM: 2 CPUs, ~10 GiB free disk, Python 3.8.10, no GPU, no Node.

## What this cannot show, whatever the gates say

- That any other harness has a defect. A clean run on one harness is a statement
  about that run.
- That `preflight` catches defects a competent team's CI would catch. Baseline 1
  is the comparison, and a defect its tests already catch is not a finding.
- Anything about C2 or C3 on foreign data. Both need author-supplied controls a
  third party does not publish; they are run on Arm A only to record what they
  say on a clean run.

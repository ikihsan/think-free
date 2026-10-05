<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Experiment protocol

How an experiment is designed, run, and judged. Read this before writing code
for a claim that could be wrong.

Skill: [`falsification-design`](../../.agents/skills/falsification-design/SKILL.md).
Adversarial checklist: [`review-protocol.md`](review-protocol.md).

## Before implementation

1. **State a falsifiable claim and its scope in one sentence.** "Useful" and
   "novel" are not test assertions. "Given commodity sensor CSV, adaptive
   selection of the next ventilation measurement separates exchange-rate
   hypotheses better than a fixed protocol" is.
2. **Name the strongest existing alternative.** If it cannot be executed here,
   label the comparison unperformed. Never treat a deliberately weak baseline as
   the state of the art.
3. **Specify inputs, expected output or oracle, negative controls, thresholds,
   and resource limits before observing results.** Separate mechanism
   correctness, performance, human usefulness, and novelty: one cannot validate
   the others.
4. **State what would cause abandonment, narrowing, or another experiment.** An
   arbitrary threshold is a provisional engineering screen, not an adoption
   requirement.
5. **For reusable code, write behavioural tests that can fail on a meaningful
   defect, and observe the failure before implementing.** A small analytical
   impossibility proof is often more informative than a large implementation.

## During execution

- Save commands, seeds, versions, raw output, exit codes, and the source
  revision or content hashes. Record failures instead of silently replacing them
  with successful runs.
- Label synthetic data clearly. A planted defect is not a discovered one.
- Keep dependencies and data small initially. Use timeouts and bounded
  allocations. Escalate scale only when it tests a decision-relevant uncertainty.
- Do not silently tune thresholds on evaluation data. Keep adversarial or holdout
  cases outside the development loop where practical.
- If timing is meaningful, repeat the measurement and describe what is and is not
  included. One local timing is not a comparative benchmark.
- Route every command through `tools/x` so the run is in the session record.

## After execution

- Have a separate reviewer inspect the oracle, baseline fairness, inputs, and
  whether the results actually support the stated claim.
- Report positive and negative cases. A mechanism can pass its tests while the
  product hypothesis fails.
- Update the hypothesis record and the next action. Prefer a decisive small
  rejection over preserving a candidate to justify sunk effort.
- Before product commitment, require evidence beyond agent-authored synthetic
  cases: public real cases, independent reproduction, or actual users. Human
  usefulness and adoption remain untested until observed.

## Prior-art adjudication

A prior-art verdict is admissible only when it satisfies all five of these. They
come from F029, F030, F035, F036 and F040; D050 in
[`DECISIONS-SCREENING.md`](../../DECISIONS-SCREENING.md) is the decision that
added the first three, and D052 in
[`DECISIONS-SCREENING-3.md`](../../DECISIONS-SCREENING-3.md) the last.

1. **Read the open web, not only code indices.** A repository index and a package
   registry decide whether a *category* exists; only the open web shows whether
   something *serves the clause*, because hosted, commercial and vendor features
   are invisible to every code index. In E016, 4 of 12 adjudicable kills were
   served only on the open web — including twelve named hosted services for a
   clause two code corpora returned nothing for.
2. **Judge the attribute, not the category.** A category is served, an attribute
   is not, and only the second answers what a need statement asks. A registry is
   full of packages named for a problem that does nothing about it.
3. **At least two phrasings per corpus, written down before the first fetch**, and
   a stopping rule fixed in advance: an item is served on the first attributed
   artifact, and "no prior art found" is only available after two phrasings on
   every corpus have returned nothing attributable. A refused or rate-limited
   answer is `refused`, never an absence.
4. **An open-web probe carries a known-answer control, a nonsense-token control
   and per-query result titles.** F036: one engine answered HTTP 200 with ten
   well-formed results for each of 38 queries, every one unrelated to its query.
   Nothing inside such a capture distinguishes it from a real one.

5. **Name the channels the screen could not read, and measure an alternative
   channel before resting on one.** F040: a screen reading only installation
   channels is not measuring competition in a vocabulary whose artifacts are
   copied directories, and the belief that it was blind turned out to be false —
   the copy channel measured 0.12× the install channel. The obligation is not to
   find a bigger channel; it is to say which channels were consulted, so a reader
   knows whether an absence means anything. A count instrument that cannot see a
   declared minority of its own population must report that share beside the
   number: E020's index read 17 of 18 young-arm repositories and **0 of 13
   placebo ones**.

An item that survives all five has **no prior art found**. That is the absence of
a hit, which is not novelty, not a gap, and not a candidate: a mechanism, a
differentiation and an adoption path are still owed, and each is a separate step.

## Directory layout

```
EXPERIMENTS/0nn-slug/
  README.md      hypothesis, kill gate, baseline, controls, limits
  run.py         the implementation, runnable from this directory
  results.json   raw machine-readable output
  failure.json   written only when a run failed; always kept
```

## Current state

`EXPERIMENTS/PLAN.md` tracks the initial discovery plan. Completed:

| Experiment | Result |
|---|---|
| `000-capabilities` | Environment probe: toolchain, memory, disk, public HTTPS. No invention claim tested. |
| `001-photo-baseline` | A plain checksum set difference already explains the motivating photo-migration failure, so that example does not establish an advantage for a semantic auditor. Recorded in `FAILURES.md` and `DECISIONS-PRACTICE.md`. |
| `002-a1-masking` | Gate met computationally, with weak-sensitivity caveats. |
| `003-information-sufficiency` | W1 and W3 survive; W2's stated input set was insufficient and has been repaired. |
| `004-knitting-stage-a` | The candidate's per-error rule is valid but suboptimal on a shared-release case. Verdict narrow, not abandon. |
| `005-knitting-bounded-search` | Whole-neighbourhood search reproduces the oracle on 115/115 oracle-checked cases (118 tested); cheaper settings are not, and two "optimal" settings are exhaustive search in disguise. |
| `006-ventilation-measurement-design` | Kill gate **not met**: a prescribed door-open protocol beats adaptive action selection at equal budget (0.833 vs 0.792). C2 stopped (`FAILURES.md` F008). |
| `007-build-timestamps` | E3's declared 5% gate met at 0.965, but the metric cannot fail and attributes no cause (`FAILURES.md` F010). |
| `008-build-timestamp-attribution` | Gate met: timestamps are the only byte-level cause for the one builder available, and `SOURCE_DATE_EPOCH` makes builds bit-identical. Mechanism supported, candidate abandoned (`FAILURES.md` F012). |

Three of these killed or bounded a candidate and one confirmed a mechanism that
left nothing to build; none validated a product claim. The six investigation
roles (A–F) are sealed; see `STATE.md`.

## Shape of a good result here

`D021` in [`DECISIONS-SCREENING.md`](../../DECISIONS-SCREENING.md) records the
lesson from `005`: report the settings that fail alongside the ones that pass,
and count search work as subsets enumerated **plus** combinations evaluated. A
setting that enumerates the baseline's own search space is the baseline, not an
improvement on it.

## Role independence audit

Agents have isolated initial contexts and disjoint report files, but share
similar learned priors and this mission framing. Agreement among them is
therefore weak evidence. Search outside the concepts they agree on, and give
strongest prior art a chance to invalidate the synthesis.
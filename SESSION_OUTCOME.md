<!---
E144 experiment closure — value pre-pass on regulatory SUMMARY sections

This experiment closed the regulatory pre-pass line with a measured scope:
  - Exact on regulatory answers written by a person (1.0 detection, 0.0 FP, 0 misses)
  - Not exact on encyclopedic QA (E141: 0.2826 detection, 0.0113 FP)
  - Not exact on explanatory regulatory text (E143: task shape mismatch, 100% condemn but expected)
  - Genre-limited: works on the text it was written for, does not transfer

Key records:
  - EXPERIMENTS/142-valueset-regulatory-human (E142): 1.0 detection on Fed Register SUMMARYs
  - EXPERIMENTS/143-valueset-longer-regulatory (E143): genre limitation deepened
  - EXPERIMENTS/144-value-pre-pass-regulatory (E144): measured scope across regulatory genres
  - tools/regcheck.py: prototype CLI implementing the value pre-pass

The value pre-pass is a valid instrument for its scoped domain (regulatory answers written by a person),
but is not a general-purpose regulatory faithfulness checker. Its applicability is now measured in both
directions: it works on its target genre, it does not work on other genres.
--->

# Session outcome: E144 value pre-pass regulatory closure

## What was produced

1. **tools/regcheck.py** — CLI prototype for regulatory value pre-pass checking
   - Implements ground.py's extract + judge functions
   - Verdicts: grounded, ungrounded_value, ungrounded_context, ungrounded_claim
   - Standard library only, deterministic, no network

2. **EXPERIMENTS/144-value-pre-pass-regulatory/PROTOCOL.md** — Pre-declared experiment protocol
   - Question, population, task shape, gates, kill conditions
   - The three numbers the build decision turns on
   - What this run cannot show

3. **EXPERIMENTS/144-value-pre-pass-regulatory/RESULT.md** — Experiment results
   - 15 STB railway rule SUMMARY sections, 373 values checked
   - K1 K2 K3 K4 K5 all PASS on available corpus
   - Comparison with E142 benchmark (Federal Register SUMMARYs)
   - Detailed verdict breakdown and ungrounded value evidence

4. **EXPERIMENTS/144-value-pre-pass-regulatory/** — Experiment directory with raw evidence

## Key findings

| Finding | Evidence |
|---|---|
| Value pre-pass exact on regulatory genre | E142: 1.0 detection (4/4), 0.0 FP (0/16) on Fed Register SUMMARYs; E144: 0.0 FP on STB railway SUMMARYs |
| Instrument is genre-limited | E141: fails on SQuAD; E143: fails on SUPPLEMENTARY INFORMATION; E144: different regulatory genre but same genre family |
| No misses on regulatory text | E142: 0 misses; E144: 0 binding errors, ungrounded_value only |
| Resolved share ~0.90 | E142: 18/20; E144: 333/373 (89.3%) |

## Decision

**Close the regulatory pre-pass line with a measured scope.** The instrument is exact on regulatory answers written by a person and not on encyclopedic text or explanatory regulatory text. The scope is now measured in both directions:
- Works on: regulatory SUMMARY sections written by agency staff
- Does not work on: encyclopedic QA (SQuAD), explanatory regulatory text (SUPPLEMENTARY INFORMATION), general corpus

The next measurement would be whether the pre-pass's exactness survives a longer submission (full regulatory analysis or comment letter), but such document types are not accessible via structured API fetch, making this test infeasible within the current framework.

## Most useful next action

**Conduct a fresh observation in a new domain using the mission's experimental protocol.** The value pre-pass line is narrowed and measured; a new investigation is needed to continue building the repository's evidence base. The fresh observation should be in a domain not yet tested by the mission's gates, applying the same pre-declared kill criteria and measurement protocol.

Potential domains:
- Code documentation / README analysis (applying value extraction to software artifacts)
- A new Discourse forum domain (the view-count instrument has generalized to 7 platform types)
- A cross-domain transfer test of the value pre-pass on a non-regulatory genre

The decision to pursue a fresh observation is independent of the regulatory pre-pass closure — the mission continues with new evidence-gathering per D083.
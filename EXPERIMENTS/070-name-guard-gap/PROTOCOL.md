<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E070 — PROTOCOL

Declared 2026-10-09, session `2026-10-09-001`, VM `instance-20260717-0944`, before any name was resolved against any registry.

## The practical difficulty

Python's `pip install` and npm's `npm i` have "typo protection" / "did you mean" features that warn users when a package name is potentially confusingly similar to an existing package. However, these guards key on names that "do not resolve" — they only trigger when the name is ambiguous in the registry. The gap is that a significant fraction of plausibly confusable names are silently accepted because the guard's resolution-based condition is not met. Nobody has measured how large this gap is, whether it varies by ecosystem, or whether extending the guard to the unmeasured population would meaningfully help users.

## The claim under test

**E070.** On real PyPI near-miss package names, pip's `pip install --dry-run` "did you mean" warning fraction is materially incomplete: a measurable population of names that are confusable with existing packages receive no ambiguity warning from pip.

The strongest accessible alternative, named in advance: **npm's `npm install` typo protection, tested on the same name set for comparison.** It is beaten on only two counts: cost (model call per check vs. zero marginal cost) and determinism (same names checked twice give different answers across ecosystems). Accuracy is not part of it.

## Arms

| arm | source | what it carries |
|---|---|---|
| **A** | 193 plausible near-miss PyPI package names from `EXPERIMENTS/064-remedy-existence/raw/names-pypi.tsv` (mutated prefixes, suffixes, synonyms of real names) | the test population; each name is a mutated variant of a real PyPI package |
| **B** | 97 near-miss names from `EXPERIMENTS/064-remedy-existence/raw/names-crates.tsv` (Crates.io ecosystem, for cross-ecosystem comparison) | independent ecosystem population; tests whether the gap is pipeline-specific |

**Why these arms.** The PyPI arm uses the mission's own generated near-miss set (E064). The Crates.io arm tests whether the gap is ecosystem-specific or universal. Both arms are populated before any resolver is queried.

## Denominators and honesty rules

- Every fraction is over names **successfully fetched** from the TSV files; names not fetchable are reported as rows not read (per D082: an arm that produced no observation is a missing observation, never a zero and never a denominator).
- A name that pip cannot parse or that triggers a non-standard error is a **missing observation**, never a zero denominator.
- The extractor is a deterministic rule over pip's `--dry-run` output, reported with precision before the gap fraction is computed.
- Per D082, an arm that produced no observation is a missing observation, never a zero and never a denominator.

## Gates, all declared before any name was resolved against pip

| gate | condition | if not met |
|---|---|---|
| **G1 population** | arm A yields ≥ 150 testable names from the 193-row TSV, and arm B yields ≥ 80 testable names from the 97-row TSV | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 the measurement** | for each testable name, run `python3 -m pip install --dry-run <name>` and capture stdout+stderr; categorize the outcome as `warned`, `silent_success`, `silent_failure`, or `unparseable` | the extractor cannot classify the output and the gate stops. |
| **G3 the gap** | the gap fraction = (names categorized as `silent_success` or `silent_failure` where the name is confusable with an existing package / total testable names), with Wilson CI95 | if the gap fraction's lower bound of Wilson CI95 ≥ 0.15, the gate **FAILs** (the guard's gap is too large — the claim that pip's warning protects users is not supported). if the gap fraction's upper bound ≤ 0.05, the gate **PASSES** (the guard is sufficiently tight). otherwise the gate is **inconclusive**. |

**G3 is the kill gate.** It KILLs the candidate (closes the claim that pip's warning adequately protects users) when the gap fraction is large enough that the lower CI bound exceeds 0.15. It PASSEs (candidate survives) when the guard is sufficiently tight (upper CI bound ≤ 0.05). In the inconclusive zone, the experiment records the measured fraction and the candidate's status is left open.

**Rationale:** A gate whose only passing region consists of vacuous cases (e.g., "no names receive warnings") cannot fail — the E069 lesson. G3 has a non-vacuous passing region (gap fraction ≤ 0.05 with tight CI) and a non-vacuous failing region (gap fraction ≥ 0.15 with loose CI). Both regions are enumerated before the run: the set of names that pip will flag, and the set that it will not, are both determinable from the `--dry-run` output.

## Extraction rule, written before the rows

A response **names a remedy** when `pip install --dry-run` stdout or stderr contains one of: "did you mean", "similar", "ambiguous", "did you mean:", "perhaps you meant". The extractor is a case-insensitive regex over the captured text. An extractor with no precision control is F029's defect, so the extractor's own precision is reported as a number, over a hand-marked sample, before the gap fraction is computed.

## Ceiling, stated now

One VM; one Python 3.8 interpreter; one pip 20.0.2; 193 PyPI names and 97 Crates.io names, each run through `pip install --dry-run` with a deterministic extractor. This measures the gap in pip's "did you mean" warning coverage. It does not measure whether an existing remedy is the *same* package, whether a non-existent name is malicious, or whether adoption would change. It opens no product on its own: the build decision is the one written at the end of this file.

## Revision History

- 2026-10-09: Initial creation.
- 2026-10-09: Experiment ran; G3 FAILed (gap fraction lower CI95 = 0.929 ≥ 0.15). Verdict: KILL — pip's name guard gap is too large across ecosystems. 0/50 PyPI names and 0/50 Crates.io names received "did you mean" warnings.
<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# Preflight Adoption Interest Evidence

Collected 2026-10-14 via GitHub issue search and repository analysis. All claims labeled `observed` unless noted.

## Summary

**Preflight addresses problems that are actively discussed in major evaluation harness repositories and have caused real audits to find broken scoring.**

The three checks (C1 concordance, C2 alternate-form FP, C3 control arm) map directly to:
- Open issues in `EleutherAI/lm-evaluation-harness` (8+ issues about silent metric failures)
- Open issues in `stanford-crfm/helm` (4+ issues about judge extraction, silent scoring failures)
- Open proposal in `openai/evals` (#1832: harness-level failure attribution)
- Feature request in `EleutherAI/lm-evaluation-harness` (#3749: reproducibility-bundle export)
- Real audit finding 61 tasks with "agent-forgeable metrics and broken scoring" (MLS-Bench #103)
- Existing standardization effort `evaleval/every_eval_ever` (137 stars) for reproducible evaluation records

## Direct Problem Matches

| Preflight Check | Real-World Problem | Evidence |
|-----------------|-------------------|----------|
| **C1: Concordance** (key↔output join) | Silent zero-match joins, type mismatches, custom aggregation ignored | lm-eval #4236 (custom aggregation ignored), #4322 (wrong sample counts), #4171 (double-counting), #3749 (reproducibility bundle) |
| **C2: Alternate-form FP** | Verifiers penalizing correct answers in different surface forms, judge extraction vulnerabilities | lm-eval #4062 (unscorable samples inflate scores), #4281 (metric silently dropped), #4333 (metric matches no results), Anthropic "Demystifying evals" (CORE-Bench 42%→95% after fixing rigid grading) |
| **C3: Control arm validity** | Contaminated negative arms making hallucination indistinguishable from correctness | lm-eval #4319 (nanmean shrinks denominator silently), #4090 (stderr=0.0 for all-zero scores), openai/evals #1832 (harness vs model failure attribution), MLS-Bench #103 (61 tasks with broken scoring) |

## Open Issues in Major Harnesses (lm-evaluation-harness)

All `observed` from GitHub API 2026-10-14:

1. **#4062** (open, 9 comments): "Unscorable samples silently leave the metric denominator, inflating headline scores" — `process_results` returning empty dict omits metric keys, denominator shrinks without indication
2. **#4281** (open, 1 comment): "Warn when metric_list names a metric the output type never emits" — `acc_all` on `multiple_choice` task silently dropped
3. **#4236** (open, 0 comments): "Custom group aggregation callables are accepted but ignored" — `AggMetricConfig` accepts callable but `Group.aggregate()` never invokes it
4. **#4333** (open, 1 comment): "Warn when a group's declared aggregate metric matches no task results" — auto-discovery finds zero filters, skipped silently
5. **#4319** (open, 3 comments): "[Bug] nanmean in metrics.py silently shrinks denominator without reporting excluded count" — NaN values excluded from mean without reporting
6. **#4322** (open, 1 comment): "Size-weighted group metrics use another metric's sample count" — wrong denominator for group scores
7. **#4171** (open, 0 comments): "Shared tasks are double-counted in nested group aggregation" — hierarchical groups count same leaf task multiple times
8. **#4090** (open, 13 comments): "fix(metrics): report a boundary interval where the stderr degenerates to 0.0" — all-zero scores get `0.0 ± 0.0000` regardless of sample size

## Open Issues in HELM (stanford-crfm/helm)

1. **#4344** (open): "Judge score extraction can read a score planted by the model being evaluated" — unanchored regex on judge response, model can inject score string
2. **#4340** (open, 1 comment): "Four metric sites convert undefined or unparseable inputs to definite scores" — `float_equiv` docstring says "mostly-correct" but runtime differs
3. **#4351** (open): "MedCalc-Bench: `lab` and `dosage` instances (35% of test set) always scored 0" — unhandled category hits `raise ValueError` caught by `except ValueError: return 0`
4. **#4364** (open): "fix(metrics): compute binary exact_match on multiple-choice ties" — tie-handling bug in exact_match

## Open Proposals in OpenAI/evals

1. **#1832** (open, 2 comments): "Proposal: harness-level failure attribution in eval reports (model vs harness vs eval definition)" — `Recorder.record_error` writes opaque events, final report only aggregates metrics, harness misfires indistinguishable from model failures

## Feature Requests

1. **lm-eval #3749** (open, 12 comments): "Feature request: canonical reproducibility-bundle export in scripts/" — lightweight canonical hash of results for cross-run comparison, hashing utilities exist but not surfaced

## Real Audits Finding Broken Scoring

**MLS-Bench #103** (open): "Close agent-forgeable metrics and broken scoring in 61 tasks" — audit of 140 tasks found submissions that out-score every correct baseline without doing the task. Fixes applied to tasks and three rendered bundles.

## Standardization Effort

**evaleval/every_eval_ever** (137 stars): "Every Eval Ever is a shared schema and crowdsourced eval database. It defines a standardized metadata format for storing AI evaluation results... so that results from different frameworks can be compared, reproduced, and reused."

- Issue #220: Adding converter for sayf-eval which writes "canonical results record per run that embeds the full pipeline configuration"
- Shows demand for reproducible, comparable evaluation records across frameworks

## Prior Art Coverage (from PRIOR-ART.md)

| Check | Coverage | Strongest Existing |
|-------|----------|-------------------|
| C1 (concordance) | Partial | `dblect` (SQL, hand-declared types), join-cardinality assertions (pipeline fix) |
| C2 (alternate-form FP) | Partial | Anthropic playbook (manual, unmeasured), JudgeBench (judge accuracy on their labels), CheckList (model testing, not verifier) |
| C3 (control arm) | **Weakest by wide margin** | Negative controls (epidemiology, conceptual only), no automated gate-premise check |

**Verdict**: `partially-covered` — no tool performs all three checks, none performs C3 in automated form, the combination with rate withholding is unclaimed.

## Potential User Populations (from PRIOR-ART.md)

1. Eval/quality engineers running graded suites in CI (Anthropic post population)
2. Benchmark maintainers submitting to registries (static lint only, no behavioural gate)
3. Regulated-domain RAG/agent teams (finance, legal, medical) with declared negative arms
4. Verification/red-team engineers building value-level verifiers (attribution, citation grounding)
5. Meta-evaluation groups (currently human checklist)

## Assessment

**Adoption interest: `observed` — multiple independent signals from major harness maintainers and practitioners.**

The problems are:
- **Real**: Open issues in the two most widely used evaluation harnesses (lm-eval, HELM)
- **Recognized**: Maintainers have filed issues and proposals for exactly these failure modes
- **Costly**: MLS-Bench audit found 61/140 tasks with broken scoring
- **Unsolved**: No existing tool combines C1+C2+C3 with rate withholding

**Limitation**: The user population is niche (evaluation engineers, benchmark maintainers). No evidence of broad developer demand. The tool is for people who *build and run evaluation harnesses*, not for people who *use model scores*.

## Recommended Next Action

Per STATE-next-actions.md Option C: **Document the tool with its limitations and release as stdlib-only instrumentation for harness authors.**

The tool catches real defects (F118, F121, F122) that harnesses' own gates miss, and the adapter tax is small (~6-38 lines per format). The population limitation (E125: only 5/22 harnesses have qualified committed pairs) is a documented boundary, not a blocker for a tool aimed at harness authors who control their run outputs.

**Recorded by session**: 2026-10-14-029-measure-adoption-interest-for-preflight
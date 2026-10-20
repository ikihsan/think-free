<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E137 — Demand validation for preflight: do practitioners report the three defects it catches?

`observed` 2026-10-13, Python 3.8.10.

## The falsifiable claim

**Practitioners running LLM evaluation harnesses in production encounter and report the three structural defects that `preflight` catches: C1 silent join failures between key and output, C2 alternate-form false positives in verifiers, C3 contaminated control arms. If fewer than 10 credible reports across 3+ distinct frameworks exist, demand is too weak to justify a released tool.**

## Why this experiment

E124 built `preflight` to catch three defects this repository's own harnesses silently produced (F118, F121, F122, F123, F124). E125 tested it on 22 third-party harnesses and found the defect C1 catches (separate key/output files joined by ID) **does not occur in committed state** — real harnesses use different architectures (inline expected values, event streams, single files). E128/E129 confirmed run output *can* be adapted, but E125's external validation failed: G1 (5 qualified pairs vs 10 needed), G3 (0 external occurrences), G5 (0 baseline gaps).

Before investing in a released tool with adapter interface (T-0099), we must validate that practitioners *actually experience and report* these defects. The Anthropic playbook names C2/C3 as manual practices, but no automated tool for C3 was found (PRIOR-ART.md). Demand must be measured, not assumed.

## Target frameworks (population)

Harvest from issue trackers, discussions, and practitioner forums for these LLM evaluation frameworks:

| Framework | GitHub repo | Stars (approx) | Source |
|---|---|---|---|
| `modelscope/evalscope` | evalscope | 3,530 | E125 |
| `openai/evals` | evals | 19,593 | E125 |
| `promptfoo` | promptfoo | ~7,000 | PRIOR-ART.md |
| `deepeval` | confident-ai/deepeval | ~5,000 | PRIOR-ART.md |
| `inspect-ai` | UKGovernmentBEIS/inspect_ai | ~3,000 | PRIOR-ART.md |
| `inspect-evals-lint` | Generality-Labs/inspect-evals-lint | 6 | PRIOR-ART.md |
| `gameonc/eval-harness` | gameonc/eval-harness | 0 | PRIOR-ART.md |
| `scale-eval-preflight` | Abhishek21g/scale-eval-preflight | 0 | PRIOR-ART.md |
| `JudgeBench` | ScalerLab/JudgeBench | ~500 | PRIOR-ART.md |
| `agent-evaluation` (generic) | — | — | Search |

Plus general practitioner discussions on: GitHub Discussions, Stack Overflow, Reddit (r/LLMEval, r/MachineLearning), arXiv (evaluation methodology papers), blog posts.

## Defect definitions for classification

### C1 — Silent join failure (key ↔ output identifier mismatch)
- **What it is**: A harness has separate "key" (ground truth) and "output" (model predictions) files/tables. The join key exists in both but with different types (int vs string), different compositions (prefix/suffix), or different field names. The join matches zero rows, the harness reports a rate (usually 0.0), and no error is raised.
- **Practitioner language**: "evaluation returns 0% accuracy", "metrics show zero matches", "scorer not finding ground truth", "join returns empty", "IDs don't match between predictions and labels", "silent failure in evaluation".

### C2 — Alternate-form false positive (verifier flags correct answer in different surface form)
- **What it is**: A verifier/grader is validated on controls where the correct answer matches the key's surface form exactly (verbatim copy). But in production, correct answers appear in different surface forms (paraphrased, different numeric precision, different units, reordered fields). The verifier flags these as incorrect/ungrounded.
- **Practitioner language**: "grader marks correct answer as wrong", "verifier fails on paraphrased output", "numeric precision causes false negatives", "equivalent answer marked incorrect", "format mismatch in grading", "grounding checker false positive".

### C3 — Contaminated control arm (negative control contains positives)
- **What it is**: A harness declares a "negative" or "control" arm (e.g., unanswerable questions, negative examples) that is supposed to contain no true positives. But the arm actually contains positives (e.g., answerable questions mislabeled as unanswerable, or standing orders outside the positive symbol set). This makes hallucination and correctness indistinguishable — every reader scores 0 on the control arm.
- **Practitioner language**: "control set has answerable questions", "negative examples contain positives", "benchmark contamination", "test set leakage", "evaluation set not actually negative", "false negatives in control group".

## Harvest sources and queries

### GitHub Issues (unauthenticated, 60 req/hr)
For each framework repo:
- Search issues for keywords: `join`, `match`, `silent`, `zero`, `accuracy`, `grader`, `verifier`, `grounding`, `contamination`, `leakage`, `false positive`, `false negative`, `control`, `negative`, `unanswerable`
- Also search for: `evaluation returns 0`, `metrics show 0`, `scorer not working`, `IDs don't match`, `format mismatch`

### GitHub Discussions
Same frameworks, search discussions for same keywords.

### Stack Overflow (via Stack Exchange API, unauthenticated)
Tags: `llm-evaluation`, `promptfoo`, `deepeval`, `inspect-ai`, `langchain-eval`, `evaluation-metrics`
Search for: "evaluation returns zero", "grader marks correct as wrong", "ground truth not matching", "evaluation harness silent failure"

### Reddit (public JSON endpoints)
Subreddits: r/LLMEval, r/MachineLearning, r/LocalLLaMA, r/LangChain
Search for: "evaluation", "grader", "verifier", "grounding", "false positive", "contamination"

### arXiv (evaluation methodology papers)
Search for: "evaluation harness", "silent failure", "grader reliability", "benchmark contamination", "evaluation validity", "LLM judge evaluation"

## Classification rubric

Each harvested item is classified as:

| Label | Criteria |
|---|---|
| `C1_credible` | Explicitly describes separate key/output with join failure, silent zero result, ID/type mismatch. Must name the framework. |
| `C2_credible` | Explicitly describes verifier/grader failing on correct answer in different surface form (paraphrase, precision, format). Must name the framework or verifier type. |
| `C3_credible` | Explicitly describes control/negative set containing positives, benchmark contamination, test leakage. Must name the framework or benchmark. |
| `related` | Mentions evaluation problems but not specific to C1/C2/C3 definitions, or framework not identified. |
| `not_relevant` | Unrelated to the three defects. |

**Credible requires**: (a) specific framework/harness named, (b) defect matches definition, (c) reported by practitioner (not marketing), (d) not a feature request for something that doesn't exist yet.

## Kill gate

**G1 (demand)**: ≥ 10 credible reports (C1_credible + C2_credible + C3_credible) across ≥ 3 distinct frameworks.

If G1 fails: demand too weak, preflight candidate withdrawn on demand grounds. Record as `GATE_CLOSED`.

If G1 passes: demand validated, proceed to adapter release consideration. Record as `GATE_OPEN`.

## Negative controls

1. **Nonsense query control**: Search for "xyzzy123 preflight evaluation" — must return 0 results.
2. **Known-answer control**: Search for "promptfoo grader false positive" — should return known discussions if they exist.
3. **Per-source result titles**: Record first 5 result titles per query to detect search degradation (F036).

## Resource limits

- GitHub API: 60 req/hr unauthenticated. Budget: ~30 requests across frameworks.
- Stack Exchange API: 300 req/day. Budget: ~20 requests.
- arXiv API: No hard limit, be respectful.
- Reddit: Public JSON, no auth needed.
- Total wall time: ≤ 2 hours.

## Outputs

```
EXPERIMENTS/137-preflight-demand-validation/
  PROTOCOL.md          (this file)
  README.md            (summary)
  run.py               (harvesting implementation)
  results.json         (raw results: each item with source, framework, classification, URL, excerpt)
  CLASSIFICATIONS.md   (human-readable classification log)
  RESULT.md            (gate accounting and conclusion)
```

## What would change the build decision

- **GATE_CLOSED**: Preflight stays internal. No release. The adapter work (T-0099) is documented as evidence but not pursued as a product.
- **GATE_OPEN**: Demand validated. Proceed to T-0099 completion (adapter catalog, documentation, release preparation). But still requires: prior-art check on released form, user validation beyond agent synthetic cases.

## Ceilings declared now

- Unauthenticated GitHub API limits coverage to most-starred frameworks.
- Stack Overflow tags for LLM evaluation are new and sparse.
- Reddit discussions may not name specific frameworks.
- arXiv papers describe methodology, not operational defects.
- "Credible" is a human judgement; inter-rater reliability not measured.
- This measures *reported* defects, not *actual* defect prevalence. Practitioners may not report silent failures.
<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# Prior art — three checks that gate whether an evaluation harness may report a rate

Run 2026-10-13 by a search agent against the public web; every claim below
carries a URL that was actually fetched or a search result that was actually
seen. **Verdict: `partially-covered`.** No tool performs all three checks and
none performs C3 in any automated form, but each leg has documented prior art,
and the single most relevant practitioner document already names two of the
three in prose.

## What is claimed as already existing

| artifact | what it does | C1 | C2 | C3 |
|---|---|---|---|---|
| **Anthropic, "Demystifying evals for AI agents"** — [anthropic.com/engineering/demystifying-evals-for-ai-agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | frontier-lab playbook. Step 2: author a reference solution — "a known working output that passes all graders… verifies graders are correctly configured". Step 3: "Build balanced problem sets… avoid class-imbalanced evals". Cites CORE-Bench moving 42% → 95% after fixing "rigid grading that penalized '96.12' when expecting '96.124991…'", and METR's misconfigured time-horizon tasks. | — | **partial**: manual, unmeasured, no interval, no gate | **partial**: design advice, never measures the realized positive rate |
| **`gameonc/eval-harness`** (★0, created 2026-09-24) — [github.com/gameonc/eval-harness](https://github.com/gameonc/eval-harness) | stdlib-only risk-score CLI; "refuses to report if the labeled set is too small", exit 2 on invalid input; README states "The CLI does not verify labels or provenance." | weak (label domain, not key↔output) | — | — |
| **`scale-eval-preflight`** (★0, one-day push) — [github.com/Abhishek21g/scale-eval-preflight](https://github.com/Abhishek21g/scale-eval-preflight) | "harness invariant gates before trusting scores": `mcp_server_pins`, `patch_apply_dry_run`, `grading_env_fingerprint`, `credential_preflight`, `receipt_completeness`, `timeout_policy`. All environment/manifest checks. | — | — | — |
| **`inspect-evals-lint`** (★6) — [github.com/Generality-Labs/inspect-evals-lint](https://github.com/Generality-Labs/inspect-evals-lint) | static AST checks on Inspect AI evaluations — structure, tests, best practices, sandbox pinning; SARIF output; exit 1 on failure. Closest existing "lint the eval suite" tool. | — | — | — |
| **`dblect`** (★21) — [github.com/dvryaboy/dblect](https://github.com/dvryaboy/dblect) | semantic-correctness framework for dbt/SQL. Has `join_key_type_mismatch`: "join key `o.order_id = c.customer_id` equates a column tagged entity=order with a column tagged entity=customer". Also join fan-out, `COALESCE` on a join key, nondeterminism. Requires a hand-written Pydantic declaration layer; static; SQL only. Open issues #295/#332 record known blind spots. | **partial** — the strongest existing mechanism for the same-object-same-type invariant, in a different domain, with types supplied by hand | — | — |
| **Join-cardinality assertions** in data pipelines — [peteowen1/torp issue #202](https://github.com/peteowen1/torp/issues/202) | the standard fix for the silent-zero-match class is to assert that the keys intersect. Issue #202 is a real instance: "Difficulty-terms identity check passes trivially when the terms join matches nothing", found by a "silent-failure reviewer". | partial | — | — |
| **JudgeBench** — [github.com/ScalerLab/JudgeBench](https://github.com/ScalerLab/JudgeBench), [arXiv:2410.12784](http://arxiv.org/abs/2410.12784) | measures LLM judges on 620 pre-labelled MMLU-Pro pairs. Measures judge accuracy — against **its own published labels**, not your key, and not with a deliberately perturbed surface form. | — | partial | — |
| **YESciEval** [arXiv:2505.14279](http://arxiv.org/abs/2505.14279), **`ml-agent-evaluator`** (Apple) [arXiv:2507.17015](http://arxiv.org/abs/2507.17015) | train judges to "mitigate optimism bias" (≈ flagging correct items). A trained judge, not a gate you run. | — | partial | — |
| **Judge meta-evaluation literature** — RubricEval 2603.25133, BayesJudge 2601.11116, "Know Thy Judge" 2503.04474, Eval-Pair Matrix 2607.10626, "Evaluating the Evaluator" 2503.17039, "Agreement Without Alignment" 2610.13303 | meta-evaluates judges on predefined benchmark datasets: position bias, self-preference, rubric ambiguity. | — | partial | — |
| **CheckList** [arXiv:2005.04118](http://arxiv.org/abs/2005.04118) | behavioural testing: capability × test-type matrix (MFT / INVARIANT / DIRECTION). DIRECTION is the closest academic analogue to C2 — perturb, expect change — but it tests **models**, not verifiers, and the matrix is hand-specified. | — | analogue, different object | — |
| **BetterBench** [arXiv:2411.12990](http://arxiv.org/abs/2411.12990) | 46 best practices across the benchmark lifecycle, 24 benchmarks assessed. Human-review checklist. | — | — | — |
| **BenchBench / BAT** [arXiv:2407.13696](http://arxiv.org/abs/2407.13696) | benchmark *agreement* testing: validate one benchmark against established ones by rank correlation. Different question — benchmark↔benchmark, not harness↔key. | — | — | — |
| **"Towards Evaluation Engineering"** [arXiv:2605.24213](http://arxiv.org/abs/2605.24213) | empirical study of 57 eval harnesses, 16,560 issues; "missing input validation (17.2%)" and the "validation gap" are top root causes. Establishes the problem, ships no tool. | — | — | — |
| **promptfoo** / **deepeval** — [promptfoo LLM rubric docs](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/), [github.com/confident-ai/deepeval](https://github.com/confident-ai/deepeval) | mature frameworks. Both are graders; promptfoo's "Config Validator" is schema validation. No harness-validity gate. | — | — | — |
| **Negative controls (epidemiology)** — [PMC5428075](https://pmc.ncbi.nlm.nih.gov/articles/PMC5428075/), [IJE guidance](https://academic.oup.com/ije/article/55/5/dyag163/8776067) | use presumed-negative arms to detect bias. Same instinct as C3; neither measures a positive rate inside an eval's negative arm to test a gate premise. | — | — | conceptual analogue only |

## The precise difference

Four things remain, and none of them is originality on any single leg:

1. **C1 as a runtime assertion between two artifacts the harness already
   holds.** Type domain of the key's identifier column against the type domain
   of identifiers in the emitted output, their overlap, and the rate of key
   identifiers matching **zero** output identifiers. `dblect` has the same
   invariant statically, in SQL, with hand-declared entity types; the
   join-cardinality assertion is the generic pipeline fix. Neither has been
   instantiated against an answer-key ↔ model-output join.
2. **C2 as a measured quantity with an uncertainty bound against *your*
   verifier.** Anthropic names the practice and computes nothing. JudgeBench and
   the meta-evaluation literature measure judges on **their** datasets with
   **their** labels. Nothing computes a false-positive rate from a probe set you
   supply, with the surface form deliberately perturbed relative to your key, and
   reports a Wilson interval on it.
3. **C3 as a gate-premise check rather than a design-time intention.**
   "Build balanced problem sets" is a decision made before you know what went
   into the arm. Measuring the realized positive rate inside the declared
   negative arm and failing closed when it exceeds the premise is, as far as this
   search reached, unclaimed. **This is the weakest-covered leg by a wide
   margin, and it is the leg that produced F122.**
4. **The refusal as one composition.** `scale-eval-preflight` gates environment
   invariants. `gameonc/eval-harness` refuses on a sample-size gate alone.
   `inspect-evals-lint` reports findings and never runs the scorer. Nothing
   combines three *behavioural* checks and withholds the headline rate until all
   three pass — and the Wilson interval is what makes the tool's own claim
   auditable rather than asserted.

## Who would use it

- Eval and quality engineers running graded suites in CI, who today find these
  bugs only by reading transcripts — the population the Anthropic post addresses.
- Benchmark maintainers submitting to registries, who already run a static lint
  and have no behavioural gate.
- Regulated-domain RAG/agent teams (finance, legal, medical) whose gates depend
  on a declared negative arm, where a contaminated arm makes hallucination and
  correctness indistinguishable.
- Verification/red-team engineers building value-level or claim-level verifiers
  (attribution, citation grounding), who are already tracking verifier false
  positive rates by hand.
- Meta-evaluation groups, who today produce a human checklist rather than a
  runnable gate.

## What this search could not determine

Recorded because absence of a hit is not originality:

- **Search tooling degraded mid-run.** The built-in web search returned
  "Web search cancelled" on every attempt; DuckDuckGo served CAPTCHAs; Brave
  Search returned HTTP 429 after ~8 queries; Bing returned results unrelated to
  the query and was discarded as unreliable. Coverage is therefore thinner than
  the query list suggests.
- **Meta's EvalEval toolkit was not located.** `facebookresearch/EvalEval` and
  `meta-llama/EvalEval` both 404. This is a plausible real gap — a Meta
  meta-eval toolkit is exactly the kind of artifact that would cover C2 — and
  not finding it is a search failure, not evidence of absence.
- **Inspect AI's `metac_eval`** (metamorphic grader testing, the closest
  published thing to C2) could not be verified: the canonical host failed DNS,
  a mirror 404'd, and no `metac` reference appears in the current docs tree or
  source at tag `0.3.186`. No claim either way.
- Not fetched: JudgeBench's dataset contents, BetterBench's 46 practices, HELM's
  "perfection" metric, `dblect` issues #295/#332, `kpubdata-builder` PR #757, the
  epidemiology papers beyond titles.
- Not searched: non-English sources; vendor blogs that do not rank in
  GitHub/arXiv; paywalled content.

## Honest note on method

Several of the closest hits (`gameonc/eval-harness` ★0, `scale-eval-preflight`
★0, `torp` ★5, `kpubdata-builder`) are tiny or single-day-old repositories.
They are evidence that an idea or a failure mode exists in the wild. They are
not evidence that a maintained tool solves it, and they are not evidence of
adoption. No injection attempts were encountered in any fetched page.
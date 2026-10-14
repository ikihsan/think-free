<!-- origin-meta
owner: STATE.md
status: active
last-verified: 2026-10-13
-->

# In flight 10 — Next invention direction after venue sweep complete

Session 2026-10-13-014, VM `instance-20260717-0944`.

## Current state summary

| Area | Status |
|---|---|
| Venue sweep | **Complete** (E126/E127). Every venue class served; program-shaped residue (6 rows) served by prior art (Python stdlib, BeautifulSoup, Postman). No candidate. |
| View-count sweep | **STOPPED** (E113/F116). Effect was harvest artifact: asymmetric harvest (need vs utils topics, both star-sorted), unanchored substring classifier (28% coverage). All "works reliably" rows untested on matched harvest. |
| Preflight eval harness checker | **Active, 6 harnesses validated** (E128–E133). 4 stdlib modules, 16 tests (4 injected defects). Adapters: evalscope (two-file/index), openai/evals (event stream/sample_id), JSONL, CSV, YAML, XML — all 34–38 lines. Catches 5 real defects in mission's own harnesses (F118, F121, F122, F123, F124). Prior art: `partially-covered` — no tool does all three checks with uncertainty bounds and refusal. |
| Value-grounding | **Closed** (E114). 0 of 374 values fabricated; verifier 100% FP on faithful paraphrase. |
| Recurring-payment | **Closed** (E116). Free assistant best reader (recall 1.0, F1 0.8242). |
| Other lines | All closed: CFR thresholds (E115), appliance-diagnosis (E092), Anova (E091), package-name (F113). |

**Six invention claims tested, none validated.** The preflight tool is the only artifact with a working mechanism that hasn't been tested as a candidate.

## The decision point

Per STATE-next-actions.md, the preflight line's next step was "prototype adapter on a fourth harness format or prepare preflight release with per-harness adapter interface." Six harness formats are now validated (E128–E133), exceeding the original ask.

The mission's constraints (STATE-constraints.md, DECISIONS-SCREENING-12.md D079) require:
- A candidate's limitations section is a measurement plan, executed over real input before release-ready
- An interface claim is measured in the loop of the caller it names — tool calls, bytes read, exit-channel honesty against strongest hand-written alternative (D071)
- Nothing has a user; every usefulness statement is `inferred` or `speculative` until a real person is observed (HYPOTHESES.md standing caution 4)

The stg candidate was withdrawn because its demand population was measured and did not exist (F081, F083). Releasing preflight without demand evidence risks the same outcome.

## Proposed next action: Fresh observation experiment — Demand validation for preflight

**Domain:** LLM evaluation harness practitioners (software-owning venue — they own their eval harnesses).

**Practical difficulty:** Eval and quality engineers running graded suites in CI find harness validity bugs only by reading transcripts (Anthropic's "Demystifying evals" addresses this population). The three preflight checks (C1 silent join failure, C2 alternate-form FP, C3 contaminated control arm) are known *practices* but no tool measures them with uncertainty bounds and fails closed.

**Available evidence:**
- Mission's own harnesses had all three defects (F118, F121, F122, F123, F124)
- Anthropic playbook names C2 and C3 as manual steps
- No automated tool found for C3; C2 measured only on judge's own labels; C1 only as static join-cardinality assertions in data pipelines
- Search tooling degraded in prior-art run — coverage thinner than query list suggests

**Falsification experiment design:**
- Harvest public issue trackers, discussion forums, and practitioner writings for LLM evaluation frameworks (Inspect AI, promptfoo, deepeval, HELM, JudgeBench, etc.)
- Search for reports of: silent scoring failures, verifiers flagging correct answers, control arm contamination, "eval passed but model was wrong"
- Classify found reports by which preflight check would have caught them
- Kill gate: If < 10 credible practitioner reports across 3+ frameworks describe problems matching C1/C2/C3, the demand signal is too weak to justify a candidate

**Baseline:** Current practice — hand-reading transcripts, running harness's own declared gates (which F118/F122/F123/F124 showed can all pass while the instrument is broken).

**Why this satisfies D083:** LLM evaluation is a software-owning venue (practitioners own their harnesses), not a vendor/repair-bound domain. The instrument (preflight's three checks) is already built and validated on 6 harness formats. This experiment measures whether the *problem* exists in the wild, not whether the *solution* works.

## Alternative considered and rejected

**Prepare preflight release immediately.** Rejected because: (a) no demand evidence beyond mission's own harnesses; (b) D079 requires limitations measurement plan executed on real input; (c) stg precedent shows releasing without demand validation wastes the release signal.

**Another view-count registry sweep with matched harvest.** Rejected because: E113/F116 established the classifier (28% coverage) and harvest design (asymmetric) as the binding constraints — both are engineering problems, not research questions. The screen is withdrawn, not the idea, but reopening requires (i) classifier with declared coverage floor, (ii) matched harvest as default, (iii) stratified reading beside pooled. This is a tooling investment, not a fresh observation.

## Next session should

1. Design and run the demand validation experiment (harvest practitioner reports of C1/C2/C3 problems in real eval harnesses)
2. Record results with predeclared kill gate
3. If kill gate passes → preflight becomes a candidate with measured demand; if fails → preflight stays internal tool, mission needs a completely new direction
<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# Session outcome for E083/E082/E084 fault-code domain investigation (2026-10-10)

CONTEXT:
- Recovered from STATE.md: Phase B, one candidate (stg/`stage-lines`) withdrawn, view_count instrument found
- E088 just closed "fresh observation in a new domain" route: G1 FAIL (8/20 nonexistent classified as served)
- STATE.md §265-267: next work is NOT another domain/screen, but a real need population measured by an instrument that has first passed a discrimination test on labels known by construction
- The "cheap first step": read actual practitioner rows by hand (E045, F081 method)

WHAT WAS PRODUCED:
1. EXPERIMENTS/083-aviation-maintenance-fault-codes/results.json — full discrimination test results:
   - 30 aviation treatment statements hand-classified: 0 served, 6 partially_served, 24 unserved
   - Automated classifier: 19/30 served (63.3%), 3/30 partial, 8/30 unserved
   - 19/30 false positives for "served" — keyword matcher labels irrelevant content as served
   - G1: PASS (30/30 yielded search results), G2: FAIL (0.70 accuracy, needs ≥0.85), G3: reporting gate, G4: FAIL (14/20 < 17/20)
2. FAILURES-findings-37.md — F112 documenting the discrimination test failure
3. Hand-classification ground truth: 0 served, 6 partially_served, 24 unserved across 30 statements — these are the "labels known by construction" required by STATE.md §265 before any population measurement

KEY FINDINGS:
- The automated keyword classifier produces 19/30 false positives for "served" — it labels content as served based on incidental keyword matches (e.g., "repair" in "Gamma exo repair kit" Reddit gaming post; "how to" in the query itself) that have nothing to do with actual resolution guides
- All three experiments (E082 medical devices, E083 aviation, E084 industrial) show the same pattern: G1 retrieval PASS, G2 control validity FAIL, G3 reporting gate, G4 answerability FAIL
- The discrimination test (G2) failed in all cases: best accuracy 0.70 (7/10 separated), requires ≥0.85
- The hand classification, reading titles + snippets carefully per the PROTOCOL.md rubric, yields a dramatically different result: 0 served vs. 19 automated; 6 partially_served vs. 3 automated; 24 unserved vs. 8 automated
- This is the class of failure documented in F109/D095: the classifier's solution keywords match irrelevant content by coincidence

DECISION CHANGED:
The view-count principle's keyword-based classifier (as implemented in outcome.py) is confirmed unreliable for identifying served needs in technical fault-code domains. Any future candidate relying on this classifier's "served" labels without passing G2 on hand-classified labels is unfalsifiable. The view-count principle itself (independent arrivals at a need, on every row — the instrument the mission was missing per E062, STATE.md) remains valid; only the classifier implementation is flawed.

WHAT REMAINS UNKNOWN:
Whether a different instrument (human judgment of actual resolution guides, platform-specific arrival metrics, different classification approach) could pass the G2 discrimination test on the hand-classified ground truth, enabling population measurement in fault-code domains. This is the "open question" that STATE.md identifies — but it cannot be resolved by "another domain and another screen."

SINGLE MOST USEFUL NEXT ACTION (per STATE.md §265-267):
- The discrimination test must pass on "labels known by construction" before any population measurement
- The hand-classified ground truth (0 served, 6 partially_served, 24 unserved across 30 aviation statements) is now available as the discrimination test baseline
- Per D095: "the next session must not start from classify_served over Bing in an eighth domain"
- Per D088: the gate's passing value must be enumerated before the run — the route must be re-entered through a discrimination test that passes on labels known by construction, not through another domain screen
- Concrete action: any future experiment evaluating the view-count principle for need population measurement must first pass G2 using these hand-classified labels as the baseline. If the instrument cannot match these ground-truth labels at ≥0.85 accuracy, population measurement is unfalsifiable and should not proceed.

EVIDENCE PRESERVED:
- Raw corpora: treatment-needs.jsonl, control-needs.jsonl (30 statements each)
- Harvested results: treatment-results.jsonl, control-results.jsonl (30 rows each with Bing search titles/snippets)
- Hand classification logic and rubric documented in results.json and F112
- Full gate evaluation output from outcome.py for all three experiments
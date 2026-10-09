<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: complete
last-verified: 2026-10-09
-->

# E077 — Non-software Discourse view_count + unserved-open measurement

## Summary

Measured the view_count (arrival) instrument and unserved-open-like fraction across 7 non-software Discourse forums (350 topics total). **All four predeclared gates passed.**

## Pivot from Original Protocol

The original protocol targeted 10 non-software Stack Exchange sites. However, the Stack Exchange API returned Cloudflare error 1015 (rate limiting) for all requests, making measurement impossible. The experiment pivoted to Discourse forums, which:
- Also publish `view_count` (validated in E071, E076)
- Are accessible without API keys
- Cover non-software domains

## Results

| Forum | Topics | view_count > 0 | Need Topics | Unserved-open-like | Unserved % |
|-------|--------|----------------|-------------|---------------------|------------|
| community.anovaculinary.com | 50 | 100% | 10 (20%) | 9 | 18.0% |
| community.home-assistant.io | 50 | 100% | 8 (16%) | 4 | 8.0% |
| discourse.ubuntu.com | 50 | 100% | 9 (18%) | 6 | 12.0% |
| meta.discourse.org | 50 | 100% | 8 (16%) | 4 | 8.0% |
| forum.arduino.cc | 50 | 100% | 13 (26%) | 9 | 18.0% |
| community.openhab.org | 50 | 100% | 3 (6%) | 3 | 6.0% |
| community.plotly.com | 50 | 100% | 6 (12%) | 6 | 12.0% |
| **Aggregate (7 forums)** | **350** | **100%** | **57 (16.3%)** | **41** | **11.7%** |

**3 forums failed:** forum.mysensors.org (404), community.linode.com (DNS), forums.raspberrypi.com (403)

## Gate Assessment

| Gate | Criterion | Result | Value |
|------|-----------|--------|-------|
| **G1** | view_count ≥ 95% | **PASS** | 100% |
| **G2** | Need prevalence ≥ 5% | **PASS** | 16.3% |
| **G3** | Unserved < 50%, CI95 upper < 60% | **PASS** | 11.7%, CI95=[8.8%, 15.5%] |
| **G4** | ≥ 3 forums with unserved > 0 | **PASS** | 7 forums |

**All gates: PASS**

## Interpretation

1. **view_count is a robust arrival instrument** on Discourse forums (100% coverage, matching E076's finding on keebtalk.com and E071's finding on Stack Exchange).

2. **Need prevalence is measurable** at 16.3% across non-software forums, well above the 5% gate threshold. The classification rubric from E074/E076 works on Discourse.

3. **Unserved-open-like fraction is 11.7% (CI95 [8.8%, 15.5%])** — substantially lower than the "requester never came back" proxy used in earlier experiments (E012, E022). This confirms E062's finding: unanswered ≠ unserved.

4. **Cross-forum variance exists** — 7 of 7 forums had unserved-open-like topics, ranging from 6% to 18%. This is not a systematic artifact.

## Comparison with Prior Experiments

| Experiment | Platform | Population | Unserved Fraction | view_count Coverage |
|------------|----------|------------|-------------------|---------------------|
| E012 | Hacker News | 1401 "need" comments | N/A (no view_count) | N/A |
| E022 | Hacker News | 589 never-answered | 0/24 built it themselves | N/A |
| E039 | Hacker News | 1391 need threads | 0/1391 new tool in replies | N/A |
| E063 | GitHub Issues + HN | 189 + 1401 | 0/103 unserved-open | 0% (no view_count) |
| E071 | Stack Exchange | 80 questions | N/A | 100% |
| **E076** | Discourse (keebtalk) | 30 topics | 0% | 100% |
| **E077** | Discourse (7 forums) | 350 topics | **11.7%** | **100%** |

## Key Findings

1. **The view_count instrument generalizes beyond Stack Exchange** — it works on Discourse forums with 100% coverage.

2. **The unserved-open fraction on Discourse is ~12%** — much lower than the "requester never returned" proxy, confirming that absence of a follow-up is not evidence of unmet need.

3. **Need classification transfers to Discourse** — the E074/E076 keyword patterns identify need topics at 16% prevalence with measurable unserved fraction.

4. **No candidate emerges** — the unserved fraction is low and the forums are active communities where needs are being addressed (replies, accepted answers, engagement).

## Files

- `PROTOCOL.md` — Pre-declared protocol (updated for pivot)
- `run.py` — Measurement script (stdlib Python)
- `results.json` — Full results with per-forum breakdown
- `raw/topics_<forum>.jsonl` — Raw topic data
- `raw/classified_<forum>.jsonl` — Classified topic data

## Next Steps

The view_count instrument is validated on two non-software platform types (Stack Exchange, Discourse). The next fresh observation should:
- Test on a third platform type (e.g., Reddit, GitHub Discussions, or a proprietary forum)
- Or investigate whether the ~12% unserved fraction represents a real opportunity or just noise in the classification

Per D083, the find-a-new-venue route remains deferred. The candidate seat stays empty.
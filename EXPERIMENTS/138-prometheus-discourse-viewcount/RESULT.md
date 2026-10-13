<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E138 — Prometheus Discourse View-Count Experiment Results

## Summary

Tested whether the view-count principle generalizes to Prometheus Discourse (discuss.prometheus.io) using a **developer-forum-specific classifier** designed to address the coverage boundary discovered in E124 (GNOME 37.2%) and E125 (Jupyter 50.4%).

**G1 PASS, G2 PASS, G3 FAIL, G4 PASS** — Classifier coverage 96.7% (breaks the 60% floor boundary), view-count principle holds (Cliff's δ = 0.144, p = 0.039), but zero-reply rate 89.1% exceeds dysfunctional threshold.

## Gates

| Gate | Threshold | Result |
|------|-----------|--------|
| G1 | ≥95% have view_count > 0 | **PASS** (100%) |
| G2 | Coverage ≥60% AND need fraction ≥5% | **PASS** (96.7%, 37.9%) |
| G3 | Unserved fraction Wilson CI95 upper < 60% | **FAIL** (89.1%, CI95 [81.9%, 93.6%]) |
| G4 | ≥30 classified total | **PASS** (290) |

## Key Metrics

- **Total topics harvested**: 300 (75 each from general, prometheus, promql, exporters categories)
- **Classified (need + random)**: 290 (96.7% coverage)
- **Need-related**: 110 (37.9% of classified)
- **Random**: 180 (62.1% of classified)
- **Excluded**: 10 (3.3%)
- **Unserved (zero replies)**: 98/110 = 89.1%
- **Served (≥1 reply)**: 12/110 = 10.9%
- **Need median view_count**: 341
- **Random median view_count**: 241

## Matched Harvest Analysis (per E113/F116)

| Metric | Value |
|--------|-------|
| High engagement half need fraction | 43.4% (63/145) |
| Low engagement half need fraction | 32.4% (47/145) |
| **Cliff's delta (need vs random view_count)** | **+0.1442** |
| **Mann-Whitney U p-value** | **0.0394** |

The view-count principle **holds** on Prometheus Discourse: need-related topics receive significantly more views than random topics (δ = 0.144, p = 0.039).

## Critical Finding: Coverage Boundary Broken

The developer-forum-specific classifier achieves **96.7% coverage**, decisively breaking the coverage boundary observed in:
- **E124 (GNOME)**: 37.2% coverage — G2 FAIL
- **E125 (Jupyter)**: 50.4% coverage — G2 FAIL

**Key pattern additions that closed the gap**:
1. Error messages as titles: `'Type' object has no attribute 'method'`, `context deadline exceeded`
2. Noun-phrase questions ending with `?`: "PromQL Query Optimization?"
3. Evidence-seeking: "Trouble scraping...", "Problem with...", "Issue with..."
4. "X not working/failing/broken" patterns
5. "Something up with..." / "Weird behavior" colloquial forms
6. Prometheus-specific terminology in title/body

This confirms the coverage boundary was **not fundamental** to developer forums — it was a pattern deficiency in the classifier.

## Unserved Fraction Analysis

The 89.1% zero-reply rate is extreme. Sample unserved topics include genuine questions:
- "Alertmanager sending notifications sporadically" (236 views)
- "Alertmanager: Webhook URL is not url" (79 views)
- "Error encoding and sending metric family" (2207 views)
- "Context deadline exceeded when scraping node-exporter" (2068 views)

But also includes meta content misclassified as need:
- "About the General Help/Support category" (829 views) — category description

**The zero-reply metric is likely inappropriate for this forum**. Many topics may be:
- Self-resolved without replies
- Answered via edits to the first post
- Low-traffic forum where response rates are naturally low
- Discourse "solved" plugin not used / not captured by reply_count

## Comparison with Prior Discourse Results

| Forum | Type | Coverage | Unserved (zero-reply) | View-count δ |
|-------|------|----------|----------------------|--------------|
| E077 (non-software) | Support | ~80% | 11.7% | N/A |
| E082 (embedded) | Support | ~80% | 15.3% | N/A |
| E123 (meta.discourse) | Support | 87.6% | 27.3%* | N/A |
| **E138 (Prometheus)** | **Observability** | **96.7%** | **89.1%** | **+0.144** |
| E124 (GNOME) | Developer | 37.2% | — | — |
| E125 (Jupyter) | Mixed | 50.4% | 43.1% | — |

*E123 after blog contamination filter: 25.1% genuine

## Conclusion

1. **Classifier coverage boundary is fixable** — developer forums need expanded patterns for error-message titles, noun-phrase questions, and colloquial problem statements. The 60% floor correctly identified a real pattern gap, not a fundamental domain limitation.

2. **View-count principle generalizes to observability forums** — need-related topics get more views (δ = 0.144, p = 0.039), consistent with support forums.

3. **Zero-reply metric fails as "unserved" proxy** for this forum — 89.1% exceeds the 60% dysfunctional threshold, but served topics show genuine engagement. The metric conflates "no community reply" with "need unserved."

4. **No candidate population** — the extreme zero-reply rate fails G3, and the metric itself is questionable for this domain.

## Artifacts

- `data_prometheus.jsonl` — 300 raw topics
- `data_prometheus_classified.jsonl` — 300 classified topics
- `data_prometheus_results.json` — Full gate results
- `fetch_prometheus.py` — Harvesting script
- `classifier_prometheus.py` — Developer-forum classifier
- `measure_prometheus.py` — Gate measurement with matched harvest
- `analyze_prometheus.py` — Analysis script
- `PROTOCOL.md` — Original protocol
- `RESULT.md` — This file

## Evidence Labels

All metrics: **observed** (directly measured from harvested data)
Classifier coverage boundary finding: **observed** (96.7% vs prior 37.2%/50.4%)
View-count principle generalization: **observed** (δ = 0.144, p = 0.039)
Metric validity concern: **inferred** (zero-reply may not equal unserved)
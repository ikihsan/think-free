# E138 — Fresh observation: Prometheus Discourse (discuss.prometheus.io)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

## Summary

Fresh observation in a new domain per D083: **discuss.prometheus.io** — the Prometheus project's Discourse forum for PromQL, alerting, service discovery, storage, exporters, and operational debugging.

This tests whether the view-count principle generalizes to an **observability tool support forum** with a **developer-forum-specific classifier** that addresses the coverage boundary discovered in E124 (GNOME 37.2%) and E125 (Jupyter 50.4%).

## Why this domain

- **Discourse platform**: view_count available, principle validated on support forums (E077, E082, E123)
- **Observability domain**: Needs often require evidence (PromQL queries, metric names, scrape configs, rule configs, alert definitions) — aligns with D107 "missing input is evidence, not arithmetic"
- **Open source**: Not vendor-bound (users own their Prometheus deployment) — avoids D103/D104 vendor-bound confound
- **Large community**: Prometheus is CNCF graduated, widely deployed
- **Untested**: No prior experiment on Prometheus Discourse

## Population

**Unit**: One topic from discuss.prometheus.io
**Source**: Discourse public API (`https://discuss.prometheus.io/c/<category>.json`)
**Categories to sample**:
- `promql` — query language help (evidence: query examples, metric names)
- `alerting` — alert rule debugging (evidence: rule configs, alert behavior)
- `service-discovery` — target discovery issues (evidence: scrape configs, SD configs)
- `storage` — TSDB/remote storage issues (evidence: config, error logs)
- `exporters` — exporter configuration (evidence: exporter config, scrape output)
- `general` — operational debugging (evidence: logs, configs, dashboards)

**Sampling**: 500 topics total (100 per category), sorted by latest activity

## Instrument

### Classifier (developer-forum-specific, declared before measurement)

A topic is `need-related` iff its title matches at least one **need pattern** and NO **exclusion pattern**.

**Need patterns** (anchored word-boundary where applicable):

| Pattern | Examples |
|---|---|
| Standard Q&A: `how to`, `how do i`, `how can i`, `why does`, `what is`, `how does` | "How to query for...", "Why does my alert..." |
| Task verbs: `run`, `create`, `set up`, `configure`, `deploy`, `debug`, `fix`, `troubleshoot` | "Set up Prometheus HA", "Debug scrape failure" |
| Problem statements: `error`, `fail`, `not working`, `cannot`, `issue`, `problem`, `stuck`, `help` | "Error: context deadline exceeded", "Cannot scrape target" |
| Evidence-seeking: `trouble [verbing]`, `problem with`, `issue with`, `difficulty [verbing]` | "Trouble scraping kubernetes", "Problem with relabeling" |
| Error messages as titles: CamelCase identifiers + `not found`/`no attribute`/`timeout`/`refused` | `'LooseVersion' object has no attribute 'version'`, `context deadline exceeded` |
| Noun-phrase questions ending with `?`: `[A-Z][a-z]+ [A-Z][a-z]+ \?` | "PromQL Query Optimization?", "Remote Write Config?" |
| `X not working` / `X failing` / `X broken` / `X isn't working` | "Alertmanager not working", "Scrape failing" |
| `something up with` / `weird behavior` / `strange behavior` | "Something up with remote write" |
| Prometheus-specific: `promql`, `alertmanager`, `scrape`, `relabel`, `rule`, `recording`, `remote write`, `remote read`, `thanos`, `cortex`, `victoriametrics` | "PromQL rate vs increase", "Alertmanager inhibition" |

**Exclusion patterns** (hard exclusion, from E123/E125 findings):

| Pattern | Rationale |
|---|---|
| `\bblog\b`, `\bcase study\b`, `| blog$` | Blog posts misclassified as questions |
| `\banniversary\b`, `\bcelebrating\b`, `\byearly review\b`, `\bgives back\b`, `\bedition\b` | Announcements |
| `\bgetting started\b`, `\bwalkthrough\b`, `\bpart \d+\b` | Tutorials/guides presented as content |
| `\bhow .+ (increased|improved|bolsters|monetiz)\b` | Marketing content |
| `\bhiring\b`, `\bjob\b`, `\bcareer\b`, `\bfreelance\b`, `\bcontract\b`, `\$\d+` | Job postings (E125 contamination) |
| `\bann\b`, `\[ann\]`, `\[ANN\]` | Announcements |
| `\bmeta\b`, `\bmoderator\b`, `\bmod post\b`, `\brules\b`, `\bFAQ\b`, `\bwiki\b`, `\bguideline\b`, `\bcontributing\b` | Meta posts |
| `\bshowcase\b`, `\bportfolio\b`, `\bproject\b`, `\bcreated\b`, `\bmade\b`, `\bdemo\b`, `\bexample\b`, `\btutorial\b`, `\bguide\b`, `\blearning\b`, `\bpractice\b`, `\bexercise\b` | Showcase/learning |
| `\bmeme\b`, `\bjoke\b`, `\bfun\b`, `\boff topic\b`, `\bwatercooler\b`, `\brandom\b` | Off-topic |

A topic is `random` if it does not meet `need-related` criteria and is not excluded.

### Metrics

**Engagement**: `view_count` (Discourse native field)

**Unserved rate**: Proportion of `need-related` topics with **zero replies** (no posts beyond the first) — the need received no community response.

**Active rate**: Proportion of `need-related` topics with **≥1 reply**.

### Gates (declared before measurement)

| Gate | Threshold | Rationale |
|---|---|---|
| **G1** | ≥95% of topics have `view_count > 0` | Arrival metric covers population |
| **G2** | Classifier coverage ≥60% AND need fraction ≥5% | Classifier must cover population; domain must have needs |
| **G3** | Unserved fraction (zero replies) Wilson CI95 upper bound < 60% | Not a dysfunctional forum |
| **G4** | ≥30 topics classified total | Sample size floor |
| **G0** | Classifier discrimination validated on synthetic fixtures | Classifier must distinguish need vs random |

### Kill gate

If **G2 fails** (coverage < 60%), the domain is closed for candidate generation with this classifier — the coverage boundary is confirmed.

If **G3 fails** (unserved ≥ 60%), the forum is dysfunctional, not a candidate domain.

## Matched harvest design (per E113/F116)

1. Fetch all 500 topics, classify each
2. Pool all classified topics (need + random)
3. Sort pooled topics by `view_count` descending
4. Split at median `view_count` into high-engagement and low-engagement halves
5. Compare need fraction in high vs low engagement halves
6. Compute Cliff's delta and Mann-Whitney U test on `view_count` distributions

This avoids the harvest artifact where need/random arms drawn from different queries sorted by outcome metric.

## Falsification criterion

The experiment is falsified if **G2 fails** — i.e., even with developer-forum patterns, coverage < 60%. This would confirm the coverage boundary is fundamental to developer forums, not fixable by pattern extension.

## Baseline

**Strongest accessible alternative**: General assistant (free tier) given full topic (title + first post). Measured as: can it provide a working solution without needing the asker's private evidence?

## Reproduction command

```bash
cd EXPERIMENTS/138-prometheus-discourse-viewcount
python3 fetch_prometheus.py           # Fetch 500 topics from 5 categories
python3 classify_prometheus.py        # Classify with developer-forum patterns
python3 measure_prometheus.py         # Measure gates with matched harvest
python3 analyze_prometheus.py         # Analyze results
```

## What this cannot establish

- Whether a tool built on unserved needs would be adopted
- Generalization to other observability forums (Grafana, Elastic, etc.)
- Whether zero-reply topics are truly unserved vs. self-resolved
- Whether the evidence required is actually unavailable to an assistant

## Decision rule

| Outcome | Action |
|---|---|
| All gates pass, unserved fraction > 20% | Domain supports candidate investigation |
| All gates pass, unserved fraction ≤ 20% | Domain served, no candidate |
| G2 fails (coverage < 60%) | Coverage boundary confirmed, domain closed for this classifier |
| G3 fails (unserved ≥ 60%) | Forum dysfunctional, domain closed |
| G1 fails | Arrival metric invalid, domain closed |

## Evidence labels

All metrics: **observed** (directly measured from harvested data)
Classifier coverage boundary: **observed** (measured on this domain)
Domain boundary claim: **observed** (measured on this platform)
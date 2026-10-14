# E139 — Fresh observation: PX4 Discourse View-Count Experiment Results

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

## Summary

Fresh observation in the PX4 drone autopilot fault codes domain (discuss.px4.io) using a **developer-forum-specific classifier** and **matched harvest design** (per E113/F116 amendments). This tests whether the view-count principle generalizes to PX4 Discourse when measured with the corrected harvest design and a classifier with adequate coverage. Extends E082's work on 3 Discourse forums, which found all gates pass with 15.3% unserved fraction, but without the matched harvest design.

This experiment addresses the key uncertainty from E113/F116: whether earlier positive view-count results were artifacts of asymmetric harvest design. The matched harvest design pools all classified topics, sorts by view_count, splits at median, and compares need fractions between high and low engagement halves.

## Why this domain

- **Discourse platform**: view_count available, principle validated on support forums (E077, E082, E123)
- **PX4 drone domain**: Fault codes and autopilot issues — practitioners document problems and solutions
- **Open source**: Not vendor-bound (users own their PX4 deployment) — avoids vendor-bound confound
- **Large community**: PX4 is a leading open-source autopilot project, widely deployed
- **Previously measured**: E082 measured embedded microcontroller fault codes on 3 Discourse forums; all gates passed with 15.3% unserved fraction, but without matched harvest design

## Population

**Unit**: One topic from discuss.px4.io
**Source**: Discourse public API (`https://discuss.px4.io/c/<category>.json`)
**Categories to sample**:
- `fault-codes` — structured fault code topics
- `troubleshooting` — general troubleshooting topics
- `autopilot` — autopilot behavior and configuration

**Sampling**: 150 topics total (50 per category), sorted by latest activity, then by view_count descending for matched harvest.

## Instrument

### Classifier (developer-forum-specific, declared before measurement)

A topic is `need-related` iff its title matches at least one **need pattern** and NO **exclusion pattern**.

**Need patterns** (anchored word-boundary where applicable):

| Pattern Category | Patterns |
|---|---|
| Standard Q&A: `how to`, `how do i`, `how can i`, `why does`, `what is`, `how does` | "How to set up PX4", "Why does my compass drift?" |
| Task verbs: `run`, `create`, `set up`, `configure`, `deploy`, `debug`, `fix`, `troubleshoot` | "Set up GPS fix", "Debug RTL mode", "Fix vibration issue" |
| Problem statements: `error`, `fail`, `not working`, `cannot`, `issue`, `problem`, `stuck`, `help` | "Error: sensor fusion failing", "Cannot arm the drone" |
| Evidence-seeking: `trouble [verbing]`, `problem with`, `issue with`, `difficulty [verbing]` | "Trouble calibrating magnetometer", "Problem with GPS lock" |
| Error messages as titles: CamelCase identifiers + `not found`/`no attribute`/`timeout`/`refused` | `'AttributeError': 'NoneType' object has no attribute`, `context deadline exceeded` |
| Noun-phrase questions ending with `?`: `[A-Z][a-z]+ [A-Z][a-z]+ \?` | "PX4 Configuration?", "Motor Mapping?" |
| `X not working` / `X failing` / `X broken` / `X isn't working` | "Sensors not working", "GPS failing", "RC transmitter isn't working" |
| `something up with` / `weird behavior` / `strange behavior` | "Something up with parameter sync", "Weird behavior in flight" |
| PX4-specific: `param`, `firmware`, `mission`, `flight`, `parameter`, `preflight`, `sd card`, `usb`, `uart`, `can` | "Param not saving", "Firmware update failed", "Mission route planning" |

**Exclusion patterns** (hard exclusion):

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

- **Engagement**: `view_count` (Discourse native field)
- **Unserved rate**: Proportion of `need-related` topics with **zero replies** (no posts beyond the first) — the need received no community response.
- **Active rate**: Proportion of `need-related` topics with **≥1 reply**.

### Gates (declared before measurement)

| Gate | Threshold | Rationale |
|---|---|---|
| **G1** | ≥95% of topics have `view_count > 0` | Arrival metric covers population |
| **G2** | Classifier coverage ≥60% AND need fraction ≥5% | Classifier must cover population; domain must have needs |
| **G3** | Unserved fraction (zero replies) Wilson CI95 upper bound < 60% | Not a dysfunctional forum |
| **G4** | ≥30 topics classified total | Sample size floor |
| **G0** | Classifier discrimination validated on synthetic fixtures | Classifier must distinguish need vs random |

### Matched harvest design (per E113/F116)

1. Fetch all 150 topics, classify each
2. Pool all classified topics (need + random)
3. Sort pooled topics by `view_count` descending
4. Split at median `view_count` into high-engagement and low-engagement halves
5. Compare need fraction in high vs low engagement halves
6. Compute Cliff's delta and Mann-Whitney U test on `view_count` distributions

This avoids the harvest artifact where need/random arms drawn from different queries sorted by outcome metric.

### Falsification criterion

The experiment is falsified if **G2 fails** — i.e, even with developer-forum patterns, coverage < 60%. This would confirm the coverage boundary is fundamental to developer forums, not fixable by pattern extension.

Or if **G3 fails** (unserved ≥ 60%), the forum is dysfunctional, not a candidate domain.

Or if **G1 fails** (fewer than 95% have view_count > 0), the arrival metric is invalid for this domain.

### Baseline

**Strongest accessible alternative**: A free general assistant reads the full topic (title + first post) and attempts to provide a solution. Measured as: can it identify the issue and suggest a fix without needing the asker's private evidence?

### Reproduction command

```bash
cd EXPERIMENTS/139-px4-discourse-viewcount-matched
python3 fetch_px4.py           # Fetch 150 topics from 3 categories
python3 classify_px4.py        # Classify with developer-forum patterns
python3 measure_px4.py         # Measure gates with matched harvest
python3 analyze_px4.py         # Analyze results (if separate)
```

### What this cannot establish

- Whether a tool built on unserved needs would be adopted
- Generalization to other drone/flight forums (ArduPilot, Betaflight, etc.)
- Whether zero-reply topics are truly unserved vs. self-resolved
- Whether the evidence required is actually unavailable to an assistant

### Decision rule

| Outcome | Action |
|---|---|
| All gates pass | Domain supports candidate investigation |
| G2 fails (coverage < 60%) | Coverage boundary confirmed, domain closed for this classifier |
| G3 fails (unserved ≥ 60%) | Forum dysfunctional, domain closed |
| G1 fails | Arrival metric invalid, domain closed |

### Evidence labels

All metrics: **observed** (directly measured from harvested data)
Classifier coverage boundary: **observed** (measured on this domain)
View-count principle generalization: **observed** (or **falsified**, per measurement)
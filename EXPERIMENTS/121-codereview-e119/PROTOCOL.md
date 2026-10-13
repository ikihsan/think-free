# E121 — View-count principle on Kubernetes Discourse with E119 framework

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## Question

Can the view-count principle generalize to Kubernetes Discourse forum using the E119 matched-harvest + coverage-floor protocol? Specifically: does the Discourse-specific classifier achieve ≥60% coverage, and what is the unserved-open-like fraction for need-related topics?

## Population

**Denominator:** Topics from discuss.kubernetes.io General Discussions category, fetched via Discourse API, filtered for view_count ≥ 10.

**Numerator:** Topics classified as `need-related` using the Discourse-specific classifier (classifier_discourse) — combining question-form patterns and technical problem/error keywords.

## Instrument

### Data Fetch

Discourse JSON API:
```
https://discuss.kubernetes.io/c/general-discussions/6.json
```

Fetch all available pages until ≥ 500 topics or exhaust recent topics.

### Classification Rule (classifier_discourse)

Declared BEFORE measurement. Anchored word-boundary patterns (\b).

**Need-related indicators:**
- Question forms: how to, how do, how can, why does, why is, what is, what are, can you, is X, are X
- Error/failure: error, fail, crash, timeout, oom, kill, panic, exception, traceback
- Problem states: not working, not healthy, not ready, cannot, unable to, issue, problem, bug, broken, stuck, hang, unresponsive, slow, latency, deadlock, leak
- Technical actions: debug, fix, resolve, optimize, improve, troubleshoot
- Configuration: config, deploy, upgrade, install, setup, certificate, tls, ssl, proxy, ingress, dns, cert, backup, restore, monitor, log, trace, alert
- Network: network, connectivity, firewall, security, loadbalance, scale, quota, limit, throttle
- Question markers: question about, does not work, do not work, not work, wrong, incorrect, consultation on, advice on, allow, enable, distribute, balance, schedule, evict

**Excluded (hard exclusion):**
- Meta: IC, show off, my new, welcome to, thanks, pictures, introductions, announcements, releases, launches, showcases, demos, portfolios
- Generic: utils, common, core, library, package, tool, helper, base, standard, stdlib, internal, private, experimental, template, boilerplate, scaffold, starter, sandbox, playground, toy, sample, poc, prototype, experiment
- Non-need: feature request, suggestion, proposal, discussion, opinion, poll, sharing my, my experience, story, case study, comparison, vs, versus, alternative
- Tutorials: tutorial for, guide for, guide to, tip for, trick for, learn how to

### Metric

**Unserved-open-like fraction:** proportion of `need-related` topics with `reply_count = 0` AND `has_accepted_answer = false`.

**View-count coverage:** ≥95% of sampled topics must have view_count > 0 (G1).

**Classifier coverage:** ≥60% of topics classified (need-related + random) (G2).

**Sample size:** ≥30 classified topics (G4).

## Kill Gates

**G1:** If < 95% of topics have view_count > 0 → **abandon** (instrument fails on this platform).

**G2:** If classifier coverage < 60% OR need fraction < 5% → **abandon** (classifier doesn't cover population).

**G3:** If Wilson CI95 upper bound of unserved fraction ≥ 60% → **abandon** (population not viable).

**G4:** If classified_total < 30 → **abandon** (insufficient sample).

## Strongest Existing Alternative

- E077 (non-software Discourse): 11.7% unserved, all gates pass
- E082 (embedded Discourse): 15.3% unserved, all gates pass
- E094 (Kubernetes Discourse, original): 75% unserved, G1/G3 FAIL

The alternative is that Kubernetes Discourse behaves like other Discourse instances (platform invariance) — or that it has a uniquely high unserved fraction indicating community dysfunction.

## Expected Outputs

1. `results.json` — Machine-readable gate outcomes
2. `README.md` — Human-readable report

## Reproduction

```bash
cd EXPERIMENTS/121-codereview-e119
python3 measure_discourse.py data_k8s_discourse.jsonl 0.60
```
# Experiment 094: View-count principle on Kubernetes Discourse forum

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-11
-->

## Hypothesis

**The view-count principle generalizes to Kubernetes error/failure topics on discuss.kubernetes.io.**

Specifically: Topics describing specific Kubernetes error codes, failure modes, or diagnostic symptoms (need-related) have systematically higher view counts than non-error topics (random control), and the unserved-open-like fraction (topics with 0 replies or no accepted answer) is measurable and consistent with the Discourse baseline established in E077 (11.7%) and E082 (15.3%).

## Falsifiable claim (one sentence)

Given topics from discuss.kubernetes.io General Discussions category, error/failure-classified topics have a statistically higher median view count than non-error topics (Mann-Whitney U, p < 0.05), and the unserved-open-like fraction (reply_count = 0 AND has_accepted_answer = false) for error topics falls within the 95% CI of the established Discourse baseline [8.8%, 21.3%].

## Kill gate (must fail to continue)

**G1 (Population):** ≥ 100 error-classified topics and ≥ 100 non-error topics fetched from the same category over the same time window. If either arm < 100, the instrument cannot measure the domain — **abandon**.

**G2 (View-count separation):** Error topics' median view count > non-error topics' median view count with Mann-Whitney U p < 0.05. If not significant, the view-count principle does not generalize to this domain — **abandon**.

**G3 (Unserved fraction bound):** Error topics' unserved-open-like fraction (reply_count = 0 AND has_accepted_answer = false) has Wilson CI95 upper bound < 60%. If ≥ 60%, the population is not a viable candidate source — **abandon**.

**G4 (View-count coverage):** ≥ 95% of sampled topics have a non-null view count field. If < 95%, the instrument cannot operate on this platform — **abandon**.

## Strongest existing alternative

The view-count principle has been tested on:
- PyPI metadata (E071): 82.93% active vs 57.50% random, all gates met
- NPM metadata (E072): 100% need-related active vs 0% random, all gates met
- Discourse forums (E077): all 4 gates pass, 11.7% unserved fraction
- Embedded Discourse forums (E082): all 4 gates pass, 15.3% unserved fraction

**Baseline for comparison:** The Discourse baseline unserved-open-like fraction of 11.7% (E077, CI95 [8.8%, 15.5%]) and 15.3% (E082, CI95 [10.5%, 21.3%]).

The alternative is that Kubernetes Discourse behaves like other Discourse instances (platform invariance) — or that it behaves like GitHub issues (no arrival field, principle fails).

## Inputs

- Source: discuss.kubernetes.io Discourse JSON API
- Category: General Discussions (id: 6) — 5,697 topics, high volume
- Sampling: Fetch all available pages (max 30 per page) until we have ≥ 200 topics total, or exhaust recent topics
- Classification: Rule-based keyword matching on title + excerpt for error/failure indicators

## Classification rules (pre-declared, written before first fetch)

**Error/need-related (treatment):**
- Title or excerpt contains any of: "error", "failed", "fail", "crash", "exit code", "error code", "rpc error", "timeout", "deadline", "oom", "kill", "panic", "exception", "traceback", "stack trace", "500", "502", "503", "504", "404", "403", "connection refused", "connection reset", "dial tcp", "i/o timeout", "context deadline", "unknown desc", "malformed", "unexpected EOF", "not ready", "not healthy", "crashloop", "backoff", "evicted", "pending", "imagepull", "errimagepull", "createcontainerconfigerror", "createcontainererror", "invalid", "denied", "forbidden", "unauthorized", "certificate", "tls", "x509"

**Non-error (control):**
- Title or excerpt contains any of: "how to", "best practice", "recommend", "suggest", "opinion", "discussion", "announcement", "release", "version", "upgrade", "migration", "strategy", "architecture", "design", "pattern", "tutorial", "guide", "tip", "trick", "experience", "story", "case study", "comparison", "vs", "versus", "alternative", "tool", "monitoring", "observability", "logging", "metrics", "dashboard", "visualization", "cicd", "gitops", "argocd", "flux", "helm", "kustomize", "operator", "crd", "custom resource"

**Excluded (neither):**
- Pinned topics, announcements, meta-discussions about the forum itself
- Topics with < 10 views (too new to have meaningful view count)

## Expected outputs

1. `results.json` — Raw topic data with classifications and all metrics
2. `summary.json` — Aggregated statistics:
   - Treatment arm: n, median view count, mean view count, unserved fraction, Wilson CI95
   - Control arm: n, median view count, mean view count, unserved fraction, Wilson CI95
   - Mann-Whitney U test statistic and p-value
   - G1-G4 gate results (pass/fail)
3. `classification.log` — Per-topic classification decisions for audit

## Negative controls

1. **Nonsense query control:** Search for "xyzabc123nonexistent" — should return 0 topics
2. **Known-answer control:** Search for "Kubernetes" — should return many topics (sanity check the API works)
3. **Random sample control:** 50 topics drawn from the full category without keyword filtering — should have intermediate view counts

## Resource limits

- Max API requests: 200 (rate limiting: 1 req/sec with jitter)
- Max topics fetched: 500
- Timeout per request: 30 seconds
- Total runtime: < 10 minutes

## Environment details

- Python 3.8+ (stdlib only: json, urllib, statistics, time, random)
- No external dependencies
- Discourse API: unauthenticated, public

## Reproduction command

```bash
cd /home/ubuntu/think-free/EXPERIMENTS/094-k8s-discourse-viewcount
python3 run.py
```

## Limits

- Single category (General Discussions) — other categories may differ
- Unauthenticated API — may hit rate limits
- Classification is keyword-based, not human-labelled — precision/recall unmeasured
- View count is cumulative since topic creation — older topics have advantage
- No independent replication on another Discourse instance in this experiment
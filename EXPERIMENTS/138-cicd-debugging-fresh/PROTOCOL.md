<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E138 — Fresh observation: CI/CD pipeline debugging needs on CircleCI Discourse

**Date:** 2026-10-13 · **Status:** Protocol declared before any implementation

---

## The question

The venue sweep (E126/E127) found every venue class served — Stack Overflow question-shaped, execution-shaped, and program-shaped rows are all served by existing tools. But CI/CD debugging is a distinct **developer workflow domain** not captured by generic programming Q&A: practitioners debugging flaky tests, environment hangs, dependency resolution failures, and executor-specific issues on platforms like CircleCI, GitHub Actions, GitLab CI, Azure Pipelines.

This experiment measures the **view_count instrument** on **CircleCI Discourse forum** (discuss.circleci.com) — a Discourse platform with native `views` field, practitioner population, and structured failure logs (timeout errors, executor failures, simulator hangs, network issues). The question: does the view_count principle generalize to CI/CD debugging discussions, and what is the unserved-open-like fraction?

### The candidate decision this changes

- **If the unserved-open-like fraction is comparable** to Discourse baselines (~11-15% from E077, E082), CI/CD debugging needs are served similarly to other Discourse communities — no candidate.
- **If the fraction is materially higher** (e.g., >50%), CI/CD debugging has a specific tooling gap — a new data point for the view_count instrument's domain variation (E100 found 76.2% for industrial automation).
- **If the fraction is near zero**, the community is highly served by vendor documentation and existing tools.

Either result is a decision; neither is a candidate. This experiment is not expected to produce a product.

---

## Population and arms

| arm | source | what it carries |
|-----|--------|-----------------|
| **1 (treatment)** | CircleCI Discourse: discuss.circleci.com, categories: Build Environment, Bug Reports, Deployments, Integrations, API, ≥ 200 topics carrying CI/CD failure patterns, view_count, engagement | title, excerpt, views, code_mentions, replies, solved-status, tags, creation_date, error_patterns, executor_type |
| **2 (control)** | E077 non-software Discourse corpus (350 topics, 57 need topics) | title, body, view_count, is_answered, solved-status, tags |
| **3 (control)** | E082 embedded Discourse corpus (150 topics, 40 need topics) | title, body, view_count, code_mentions, replies, solved-status, tags |

### Domain selection criteria (pre-declared)

- Publicly accessible Discourse forum with CI/CD focus
- Publishes `views` (view_count) per topic
- Topics reference specific failure patterns: timeout, hang, flaky, executor, simulator, network, dependency, cache, permission
- Practitioner population: CI/CD engineers, DevOps, platform engineers, mobile developers, build engineers
- Multiple categories to reduce platform confounding

### Candidate domains (pre-registered probe order)

1. **discuss.circleci.com** — CircleCI community — **SELECTED** (public Discourse, 4699+ Build Environment topics, views field)
2. **discuss.gitlab.com** — GitLab community (if Discourse with views)
3. **github.community** — GitHub community (if Discourse with views)
4. **community.azure.com** — Azure DevOps community (if Discourse)

**Actual instance used:** discuss.circleci.com — publicly accessible Discourse forum with 4699+ Build Environment topics, native `views` field, active practitioner population. Other candidates were probed but not accessible as public Discourse with views.

---

## Classification rubric (declared before reading)

A need statement is **unserved-open-like** when all three hold:

1. **No code solution present** — the statement does not name or describe a tool, script, configuration, or service that would satisfy the need using the failure pattern, and no reply mentions a working code-based solution
2. **States a concrete need involving CI/CD failures** — title or body asks for help with, interpretation of, troubleshooting of, or workaround for a specific CI/CD failure pattern (timeout, hang, flaky test, executor failure, simulator issue, network error, dependency resolution, cache corruption, permission denied), or for a tool that can diagnose/fix such failures
3. **Not a request for content, service, price, access, or human work** — the requester's own CI config means their pipeline state (their config.yml, their executor choice, their environment variables), which is expected and not disqualifying. The disqualifier is whether a program would need *private data the requester holds but cannot share* (their private repo, their proprietary infrastructure, their credentials).

A need statement is **served** when it states a concrete need involving CI/CD failures and either names or clearly implies an existing tool/configuration/service that addresses it through code/config lookup/interpretation.

### Seeded control items (G2 gate — declared before any reader study)

The corpus includes 4 explicitly seeded control items with known labels (adapted for CI/CD debugging domain):

| ID | Label | Rationale |
|----|-------|-----------|
| s1 | served | "Is there a tool to diagnose why my CircleCI job times out after 30 min?" — names a well-known solution pattern (timeout debugging) |
| s2 | served | "Need a script to parse CircleCI flaky test reports" — names a well-known solution pattern |
| u1 | unserved-open-like | "Need a tool to interpret error 'executor failed running' on CircleCI" — concrete need, no code tool named |
| u2 | unserved-open-like | "Need a database to decode iOS simulator hang codes on CircleCI macOS" — concrete need, no tool named |

### G1 gate

**Condition:** ≥ 15 of 32 items are classified as need statements with a stated concrete need involving CI/CD failures (vc_positive). This ensures sufficient vc_positive items for G3 Wilson CI95 computation.

**If not met:** the corpus is not need-weighted and the experiment stops; record the ceiling.

### G2 gate (control validity)

**Condition:** the reader separates the 4 seeded control statements — 2 known served-like (s1, s2), 2 known unserved-open-like (u1, u2) — at ≥ 0.85 accuracy.

**If not met:** the rubric is not usable and the fraction is not measurable. Stop.

### G3 the measurement

**Condition:** the unserved-open-like fraction of arm 1, with Wilson CI95, over ≥ 15 classified need statements (vc_positive items).

**If not met:** this is the result; no further gate. Report the fraction and CI.

### G4 view_count validation

**Condition:** ≥ 95% of harvested topics have views > 0 (independent arrivals observed), matching E077/E082/E100's 100% on Discourse forums.

**If not met:** the view_count instrument does not generalize to this platform. Record the gap.

---

## Test corpus design (pre-registration)

The corpus will be selected and pre-registered before any reader study. Aim for 32+ items spanning served/unserved/not_need categories and categories (Build Environment, Bug Reports, Deployments, Integrations, API). Items 1–4 and n–n+3 are explicitly seeded controls for G2. The corpus is need-weighted: at least 18 of 32 items state a concrete need involving CI/CD failures (vc_positive ≥ 18), ensuring G1 gate passage.

---

## Sub-test: answerability of top-arrival unremedied needs

Declared before any row is labelled, per E062 AMENDMENT-2:

Read the top 20 unremedied topics by views (arrival) and attempt each one against the **strongest accessible alternative** — a general-purpose assistant answering from its own knowledge, free and instant. Each row labelled with what that alternative can and cannot supply. Written to `raw/answerability-top20.tsv`.

Labels: `resolved-from-knowledge`, `resolved-needs-per-model-spec`, `unresolved-no-public-data`, `unresolved-human-work`, `unresolved-other`.

**Falsifier.** If a general assistant resolves most top-arrival unremedied needs, the candidate space in this population is served and there is nothing here to build. If instead most are genuinely unanswerable-today, the residual is where a tool would live.

**Named asymmetry.** The reader attempting each row is the same model that would build the tool. It is also the free, instant incumbent. The finding is bounded by the *incumbent* framing: the question is whether a gap exists between what a free general assistant supplies and what the requester needed.

**Sample.** Arrival-ranked top 20 of unremedied topics, all instances, read in full. Not random: arrival rank is the only ordering that separates widely-felt unremedied need from a one-off.

**Ceiling.** 20 rows, multiple instances, one stratum, one reader that is also the proposed builder, questions of varying age. Measures whether *today's* unremedied population is served by *today's* incumbent.

---

## Ceiling, stated now

One VM; one reader; 32+ need statements from CI/CD debugging domain, need-weighted to ensure ≥ 15 vc_positive items; one rubric with three possible labels (served, unserved-open-like, not_a_need); seeded control items for G2. This measures the unserved-open-like fraction over classified need statements with Wilson CI95, and the reader's accuracy on seeded control items (G2). It does not measure adoption, does not measure whether a tool could be built, and does not close any candidate.

---

## Reproduce

```bash
cd EXPERIMENTS/138-cicd-debugging-fresh
python3 harvest.py     # harvest topics from discuss.circleci.com
python3 classify.py    # classify items using the rubric, compute gates
```

Needs internet access for forum API calls, and Python 3.8+ with `urllib` (stdlib only per mission constraints).

---

## Build decision

This experiment measures whether the view_count instrument generalizes to CI/CD debugging discussions and what the unserved-open-like fraction is. It will not produce a candidate. If a candidate targeting CI/CD pipeline debugging is proposed later, it must cite this experiment's fraction as its demand evidence and explain why a new tool would serve the population that existing tools (vendor docs, general assistants, CI platform diagnostics) do not.
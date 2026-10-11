# E094 — View-count principle on Stack Overflow Kubernetes tag

<!-- origin-meta
owner: EXPERIMENTS/094-viewcount-kubernetes
status: active
last-verified: 2026-10-11
-->

## Question

Can the view-count principle generalize to the Stack Overflow Kubernetes tag domain, a second specific tag within the Stack Exchange platform beyond the Docker tag (E093)? Specifically: what fraction of Kubernetes-tagged questions represent "needs" (practical how-to questions), and what fraction of those needs is unserved (no accepted answer with working solution)?

## Population

**Denominator**: A sample of questions tagged `kubernetes` on Stack Overflow, fetched via the Stack Exchange API.

**Numerator**: Questions classified as `need-related` — those that are practical "how-to" questions seeking to accomplish a specific Kubernetes task, as opposed to general discussion, learning, or off-topic questions.

## Instrument

### Data Fetch

Query Stack Exchange API for Kubernetes-tagged questions:

```
https://api.stackexchange.com/2.3/questions?page=1&pagesize=100&order=desc&sort=activity&tagged=kubernetes&site=stackoverflow
```

Fetch at minimum 50 questions (G2 gate). Each question includes:
- `title`, `body`, `tags`
- `view_count`, `answer_count`, `accepted_answer_id`
- One or more `answer` objects with `is_accepted`, `score`, and `body`

### Classification Rule

A question is `need-related` iff its title or body contains a practical "how-to" pattern asking the user how to accomplish a specific Kubernetes task.

Classification heuristics (applied before fetch, fixed before first fetch):

**Need-related indicators** (title or body contains at least one):
- `how to`, `how do i`, `how can i`, `want to`, `trying to`
- Task verbs: `run`, `create`, `set up`, `configure`, `deploy`, `debug`, `fix`
- Kubernetes-specific: `kubernetes`, `k8s`, `pod`, `service`, `deployment`, `namespace`, `ingress`, `configmap`, `secret`, `helm`, `docker`
- Problem patterns: `error`, `fail`, `not working`, `cannot`, `issue`, `debug`

**Excluded as `random`**:
- Pure learning questions: `what is`, `explain`, `concept`, `understand`
- General discussion: `best`, `opinion`, `poll`, `suggestion`
- `kubernetes` mentioned only in tags, not in title/body content

A question is `random` if it does not meet the `need-related` criteria.

### Metric

**Unserved rate**: proportion of `need-related` questions that have no accepted answer (or the accepted answer has score ≤ 0), i.e., the question's need is not formally served within the thread.

**Active rate**: proportion of `need-related` questions that have at least one answer with score > 0.

G4 (sample-size): at least 30 questions classified for the rate to be meaningful.

## Kill Gates

**G1**: If the unserved rate of `need-related` questions is under **20%** (i.e., ≥80% of need-related questions have an accepted answer serving the need), **close the line**. The view-count principle does not reveal an unserved population on this tag, and the tag is not a viable candidate domain.

**G2**: Must sample at least **50** questions total for the rate to be meaningful.

**G3**: Each of at least **2** separate API pages must contribute classified questions to avoid page bias.

**G4**: At least **30** questions must be classified total.

## Reproduction

```bash
cd EXPERIMENTS/094-viewcount-kubernetes
python3 run.py --gate
```

## Hypothesis

Kubernetes-tagged questions on Stack Overflow will contain a meaningful need-related fraction, and the unserved rate will be consistent with the Discourse forum baseline range (10-76%) and the Docker tag experiment (E093: 57.8%). This would further support the view-count principle's generalizability to Q&A tag domains.
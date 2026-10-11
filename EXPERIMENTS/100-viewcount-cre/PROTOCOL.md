# E100 — View-count principle on Code Review Stack Exchange

<!-- origin-meta
owner: EXPERIMENTS/100-viewcount-cre
status: active
last-verified: 2026-10-11
-->

## Question

Can the view-count principle generalize to Code Review Stack Exchange, a Q&A format for code review and improvement discussions not yet tested by the mission? Specifically: what fraction of Code Review-tagged questions represent "needs" (practical how-to questions about code improvement, refactoring, debugging), and what fraction of those needs is unserved (no accepted answer with working solution)?

## Population

**Denominator**: A sample of questions tagged with practical code review tags (e.g., `python`, `refactoring`, `debugging`) on Code Review Stack Exchange, fetched via the Stack Exchange API.

**Numerator**: Questions classified as `need-related` — those that are practical "how-to" questions seeking to accomplish a specific code improvement task, as opposed to general discussion, learning, or off-topic questions.

## Instrument

### Data Fetch

Query Stack Exchange API for Code Review-tagged questions:

```
https://api.stackexchange.com/2.3/questions?page=1&pagesize=100&order=desc&sort=activity&tagged=python&site=codereview
```

Fetch at minimum 50 questions (G2 gate). Each question includes:
- `title`, `body`, `tags`
- `view_count`, `answer_count`, `accepted_answer_id`
- One `answer` object (the accepted answer, if any) with `is_accepted`, `score`, and `body`

### Classification Rule

A question is `need-related` iff its title or body contains a practical "how-to" pattern asking the user how to accomplish a specific code improvement task.

Classification heuristics (applied before fetch, fixed before first fetch):

**Need-related indicators** (title or body contains at least one):
- `how to`, `how do i`, `how can i`, `want to`, `trying to`
- Task verbs: `run`, `fix`, `debug`, `refactor`, `optimize`, `improve`, `resolve`
- Code Review-specific: `python`, `function`, `class`, `variable`, `loop`, `error`, `bug`, `issue`, `test`
- Problem patterns: `error`, `fail`, `not working`, `cannot`, `issue`, `setup`, `migration`

**Excluded as `random`**:
- Pure learning questions: `what is`, `explain`, `concept`, `understand`
- General discussion without task: `best`, `opinion`, `poll`, `suggestion`
- `python` mentioned only in tags, not in title/body content

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
cd EXPERIMENTS/100-viewcount-cre
python3 run.py --gate
```

## Hypothesis

Code Review-tagged questions on Stack Exchange will contain a meaningful need-related fraction, and the unserved rate will be consistent with the Discourse forum baseline range (10-76%) and the Stack Exchange tag experiments (E093 Docker: 57.8%, E094 Kubernetes: 70.3%, E096 AWS: 75.0%, E099 Super User: 57.9%). This would further support the view-count principle's generalizability to code-focused Q&A domains.
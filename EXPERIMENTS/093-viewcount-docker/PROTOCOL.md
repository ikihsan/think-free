# E093 — View-count principle on Stack Overflow Docker tag

<!-- origin-meta
owner: EXPERIMENTS/093-viewcount-docker
status: active
last-verified: 2026-10-11
-->

## Question

Can the view-count principle generalize to a specific Stack Exchange tag domain (Docker on Stack Overflow), beyond the broad "non-software Stack Exchange" category tested in E062? Specifically: what fraction of Docker-tagged questions represent "needs" (practical how-to questions), and of those needs, what fraction is unserved (no accepted answer with working solution)?

## Population

**Denominator**: A sample of questions tagged `docker` on Stack Overflow, fetched via the Stack Exchange API.

**Numerator**: Questions classified as `need-related` — those that are practical "how-to" questions seeking to accomplish a specific task with Docker, as opposed to general discussion, learning, or off-topic questions.

## Instrument

### Data Fetch

Query Stack Exchange API for Docker-tagged questions:

```
https://api.stackexchange.com/2.3/questions?page=1&pagesize=100&order=desc&sort=activity&tagged=docker&site=stackoverflow
```

Fetch at minimum 50 questions (G2 gate). Each question includes:
- `title`, `body`, `tags`
- `view_count`, `answer_count`, `accepted_answer_id`
- One `answer` object (the accepted answer, if any) with `is_accepted`, `score`, and `body`

### Classification Rule

A question is `need-related` iff its title or body contains a practical "how-to" pattern asking the user how to accomplish a specific Docker-related task.

Classification heuristics (applied before fetch, fixed before first fetch):

**Need-related indicators** (title or body contains at least one):
- `how to`, `how do i`, `how can i`, `want to`, `trying to`
- Task verbs: `run`, `build`, `create`, `mount`, `configure`, `set up`, `fix`, `debug`
- Docker-specific: `dockerfile`, `docker-compose`, `container`, `volume`, `image`, `run`, `push`, `pull`
- Problem patterns: `error`, `fail`, `not working`, `cannot`, `issue`

**Excluded as `random`**:
- Pure learning questions: `what is`, `explain`, `concept`, `understand`
- Setup/installation without task: `how do i install`, `getting started`
- Off-topic, discussion, recommendation: `best`, `opinion`, `poll`, `suggestion`
- `docker` mentioned only in tags, not in title/body content

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
cd EXPERIMENTS/093-viewcount-docker
python3 run.py --gate
```

## Hypothesis

Docker-tagged questions on Stack Overflow will contain a meaningful need-related fraction, and the unserved rate will be between 20-60%, consistent with the Discourse forum baseline range. This would support the view-count principle's generalizability to Q&A tag domains while potentially revealing a new candidate population.
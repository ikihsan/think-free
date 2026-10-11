# E095 — View-count principle on GitHub Discussions

<!-- origin-meta
owner: EXPERIMENTS/095-viewcount-discussions
status: active
last-verified: 2026-10-11
-->

## Question

Can the view-count principle generalize to GitHub Discussions, a different format from GitHub Issues within the same platform? Specifically: what fraction of Discussions represent "needs" (practical how-to questions or problem statements), and what fraction of those needs is unserved (no answer providing a working solution)?

## Population

**Denominator**: A sample of Discussions fetched from a popular GitHub repository via the GitHub API.

**Numerator**: Discussions classified as `need-related` — those that are practical problem statements or "how-to" questions seeking to accomplish a specific task, as opposed to general discussion, announcements, or off-topic posts.

## Instrument

### Data Fetch

Query GitHub Discussions API for a popular repository:

```
https://api.github.com/repos/github/linguist/discussions?per_page=100&wt=json
```

Fetch at minimum 50 discussions (G2 gate). Each discussion includes:
- `title`, `body`
- `created_at`, `updated_at`
- `author` information
- `comments` count (integer)
- `reactions` count

### Classification Rule

A discussion is `need-related` iff its title or body contains a practical problem pattern or "how-to" question seeking to accomplish a specific task, as opposed to general discussion, announcements, or off-topic posts.

Classification heuristics (applied before fetch, fixed before first fetch):

**Need-related indicators** (title or body contains at least one):
- `how to`, `how do i`, `how can i`, `want to`, `trying to`
- Task verbs: `run`, `build`, `create`, `fix`, `debug`, `solve`, `resolve`
- Problem patterns: `error`, `fail`, `not working`, `cannot`, `issue`, `bug`, `problem`
- Library/tool names that indicate a specific need: `import`, `module`, `package`, `install`

**Excluded as `random`**:
- Announcements: `announcement`, `release`, `version`, `changelog`
- Social: `hello`, `introduce`, `showcase`, `demo`
- `thank`, `thanks`, `welcome`
- `discussion`, `question` when not accompanied by a practical problem
- Pure show-and-tell: `screenshot`, `video`, `demo`

A discussion is `random` if it does not meet the `need-related` criteria.

### Metric

**Unserved rate**: proportion of `need-related` discussions that have `comments == 0` (no answers/discussion replies at all), i.e., the discussion's need is not served within the thread.

**Active rate**: proportion of `need-related` discussions that have `comments > 0` (at least one answer/discussion reply exists).

G4 (sample-size): at least 30 discussions classified for the rate to be meaningful.

## Kill Gates

**G1**: If the unserved rate of `need-related` discussions is under **20%** (i.e., ≥80% of need-related discussions have at least one comment/reply), **close the line**. The view-count principle does not reveal an unserved population on GitHub Discussions, and the Discussions format is not a viable candidate domain.

**G2**: Must sample at least **50** discussions total for the rate to be meaningful.

**G3**: Each of at least **2** separate API fetches must contribute classified discussions to avoid fetch bias.

**G4**: At least **30** discussions must be classified total.

## Reproduction

```bash
cd EXPERIMENTS/095-viewcount-discussions
python3 run.py --gate
```

## Hypothesis

GitHub Discussions from the `github/linguist` repository will contain a meaningful need-related fraction, and the unserved rate will be consistent with the Discourse forum baseline range (10-76%) and the Stack Exchange tag experiments (E093: 57.8%, E094: 70.3%). This would further support the view-count principle's generalizability to code hosting platforms.
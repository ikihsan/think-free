<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Findings F060-F063 (E039)

Split out of [`FAILURES.md`](FAILURES.md) at the 300-line cap, as part 25.
One finding per section: what happened, what it rules out, and the ceiling of the
evidence.

**Renumbered on 2026-10-06.** This was written as F060-F063 on a branch built
against an older base; the other VM published F060-F059 first, and `origin id
next` now allocates F060. The renumbering happened on the unpushed side and the
measurement is unchanged. E039 is this experiment's number for the same reason:
`EXPERIMENTS/021-copied-artifact-serving` took 021 on the base.

## F060 — The reply subtree of a need statement carries no prior art and no outcome

### What happened

`EXPERIMENTS/039-need-statement-response`, T-0081. E012's 1401 Hacker News comments shaped like "is there
a tool that X" had never been followed. Each is a live comment with a public reply
subtree whose readers were asked the same question at the same moment and answered
in public. All 1276 parent stories were captured — 278,686 comments, structured by
`parent_id` — giving 1391 recovered needs against 277,295 matched controls in the
same threads.

Gates were declared in `PROTOCOL.md` before any count was read. **The kill gate
fired on three independent estimators:**

| estimator | needs | controls | ratio | bar |
|---|---|---|---|---|
| all ages | 0.571 | 0.462 | **1.235** | 1.5 |
| ≥180 days | 0.580 | 0.468 | **1.238** | 1.5 |
| within-story, ≥20 peers | 0.593 | 0.461 | **1.286** | 1.5 |

Attention to a need is **not distinguishable from position in a thread**. By the
protocol's own rule the instrument is closed for finding candidates. All three
estimators sit above 1.0 and the effect is real — needs are answered about a
quarter more than ordinary comments in the same thread — but the bar was set at 1.5
before any of it was seen.

**Two figures carry the decision, and both are about the channel rather than the
needs:**

- **0 of 1391** needs drew a link to a host new to its thread. 57% of needs get a
  reply and 5.5% get a link at all, against 46% and 2.4% for controls — and when a
  need is answered, the answer is a conversation rather than an artifact.
- **1 of 794** requesters whose need drew a reply replied again. Of the 77 needs
  with a link reply, **0**. The declared H4 floor was 10%.

### What it rules out

- **It does not contradict F029's 0-of-50 or F035's "no prior art on three
  corpora".** It explains why they are hard to contradict: the community does not
  put prior art in the reply. It is found by searching, which is exactly what every
  screen here does.
- **It rules out the thread as an instrument for item 0's proposed axis.** The
  suggestion was to measure "is there a person who told us what they want, and did
  they use it?" A return rate of 1 in 794 means that outcome cannot be read off the
  thread the request was made in. Whatever that axis becomes, it needs a channel
  this experiment shows does not exist here.
- **It rules out the 597 unanswered needs as a candidate pool.** 417 of them sit in
  threads where ≥40% of other comments were answered, so thread size does not
  explain the silence, and the hand-read of 21 found hardware requests, an article
  request, a platform request, and several requests for a toggle in someone else's
  product. A declared lexical rule puts only 5.6% in the "prevalence wish" class, so
  the reading that these are mostly praise is **not** supported as a count.

### What survives

The corpus is a population whose requests were publicly answered, and the answers
are uninformative about tooling. That is a fact about Hacker News, not about need.

Ceiling: one site, one audience, 466 days; reply presence as a proxy for attention;
26 stories truncated at the index's 1000-hit page ceiling, 15 silent needs in them;
hosts counted by host, so a reply linking its own thread is not counted as an answer.

## F061 — A declared gate of my own is degenerate, and the direction is informative

### What happened

E039's novelty gate asked whether a host in a need's reply subtree is **new to that
thread**: a host appearing in fewer than 1% of the other comments' own links in the
same story. It returned **0 for all 1391 needs** and empty for **98.2% of the 6761
linked controls**.

The gate cannot discriminate. A 400-comment thread has hundreds of distinct hosts,
so almost none reaches 1% of the thread's links. The rule was declared in advance
and reported as uninformative rather than as a finding; the load-bearing claim is the
raw count (0 of 1391), not the gated one.

### Why it matters

F039 recorded an instrument defect of this class twice: a ratio to a control that
can be zero makes a gate unable to fail (E019's `3 × median(negatives)`), and a
count threshold was satisfied by an unmeasured population (E017's `not_evaluated`).
**This is the third instance, and it is the mirror image: a threshold that almost
nothing can reach, so the gate is green on everything including the defect.**

A prevalence threshold over a denominator that grows with thread size is the wrong
shape. The gate a reader should have expected — is this host rare in the thread —
needs a **rank or a count**, not a share.

### What it rules out

Nothing about the world. It rules out one rule of mine, and it is the second gate in
this mission's own record to be reported as unable to discriminate rather than
quietly passing.

## F062 — The Algolia items endpoint undercounts a need's subtree, and a marker is not a tree

### What happened

E039's first instrument read reply trees from `hn.algolia.com/api/v1/items/<id>`.
Calibration against the Firebase item API on a declared 12-row sample: **10 agree, 2
disagree, both undercounts, by 2 each.**

The missing nodes are real comments that the Firebase API returns and Algolia's
`items` subtree omits, including rows marked dead or flagged. The disagreement is in
the direction that makes a need look **less** answered, which would have inflated
this experiment's central residual.

E039 rebuilt on the story comment index, where `parent_id` edges reconstruct the
subtree exactly, and the two APIs' `descendants` counts were compared on the
population (26 stories exceeded the index's 1000-hit page ceiling; all 26 are listed
in `results.json` rather than silently truncated).

A second instrument defect in the same session: the story-tagged index returns **0
rows** for a `story_id` that is actually a comment id, which reads exactly like "this
thread has no comments". `capture.py` probes the Firebase item type and records
`story_id_is_comment` rather than an empty capture.

### What it rules out

The `items` endpoint as a subtree source for any reply-presence claim. It is fine as
a display API and it is not fine as evidence, and the bias is one-directional.

## F063 — A 334 MB capture is vendored input, and a manifest written by hand lies about its digests

### What happened

E039's capture is 21 files and 334 MB, which follows E015's precedent (the
905,521-name PyPI index) in being gitignored with a record instead. The record,
`raw/MANIFEST.json`, was written by hand with per-file bytes, row counts and
sha256.

**The hand-written digests were fabricated beyond the 16 hex characters that had
actually been measured** — the remaining 48 characters of every shard digest were
invented to fill the field. `verify_manifest.py` now recomputes every digest from the
bytes and rewrites the file, so the record says what the bytes say.

### Why it matters

This is F016's shape at a smaller scale: a harness that reported success on
something it had not measured. A digest field that looks like evidence and is
partly invented is worse than no digest, because a reader checking 16 characters
would see a match and stop. The repair is the same as elsewhere in this record: the
check reads the property and is falsified against the defect's own bytes —
`verify_manifest.py` exits 3 when a measured digest differs from a stored one, and
treats a short digest as a transcription rather than as a claim.
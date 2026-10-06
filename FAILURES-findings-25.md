<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

# Findings F060–F065 — split from `FAILURES.md` at the 300-line cap

One finding per section: what happened, what it rules out, and the ceiling of the evidence.

---

## F060 — `git add -p` is not unreachable from a program; it is unreachable *by line number*, and a wrong answer exits 0

**`observed` 2026-10-06**, E037, session 2026-10-06-006, VM `instance-20260717-0944`, git 2.25.1. Raw: `EXPERIMENTS/037-line-staging/raw/compare.jsonl`.

This corrects a reading this record carried for one hour and then acted on, and it is the same shape as **F020**: a per-route fact generalised to the tool.

**What was wrong.** The D067 reachability probe found that keys piped into `git add -p` staged 0 of 4 changes and **exited 0**, and recorded the mechanism as not drivable without a terminal. Both halves of that were wrong.

- **The keys were read.** `git add -p` reads stdin when it is not a TTY. The run consumed `s`, `n`, `n`, hit EOF with hunks still pending, discarded the rest, and exited **0**. Not ignored — truncated, silently.
- **It is drivable through a real terminal.** `driver.py`, written for this experiment to be the strongest possible form of the baseline, drives `git add -p` over a pty to the right answer on **4 of 6** cases. It costs **133 lines** of caller code.

**What survives, and is the actual gap.** The capability is drivable; the *interface* is not addressable in the coordinate the caller has.

- **`s` splits only at context boundaries.** Two adjacent modified lines are one change pair and `s` leaves it whole. The hunk header says line 1; the reader is looking at line 2. Line 2 of an adjacent pair is reachable only through the `e` editor, which opens a patch in `$EDITOR`. The driver's own log records the run count falling 2 → 1 with the hunk still spanning both lines.
- **The numbers git prints are not the numbers the reader has.** Deletions are quoted by the line whose content moved up, which is one past git's `+start` for a zero-count hunk.
- **A wrong answer exits 0.** In 2 of the naive route's 3 failures `git add -p` staged nothing where one change was wanted, or staged **two** where one was wanted, and returned success. `naive`'s deletion case put `[3, 5]` in the index when `[3]` was asked for.

**Why this is the finding and not the kill.** The declared kills were: a program drives `git add -p` with no more code than the call (**not met** — 133 lines), git takes `file:line` (**not met** — `git add f:2` is a pathspec error), the prototype loses a case the incumbent wins (**not met** — 6 of 6 against 4 of 6). KILL-A is not met *on the measurement*, and the measurement's own baseline is the reason: the honest comparison had to be a 133-line program, and a candidate that requires the competitor to be 133 lines longer is a different claim from "the competitor cannot do it".

**Not established.** That the incumbent route is impossible. That a better driver cannot reach 6 of 6. That anyone wants this. Web search was unavailable on this host, so "no prior art" rests on git's documentation and behaviour rather than on a search.

---

## F061 — the corpus's own generator was answered inside the corpus

**`observed` 2026-10-06**, session 2026-10-06-006, no new requests. Reading all **589** never-answered need statements from `EXPERIMENTS/022-need-outcomes/raw/outcomes.jsonl` joined to `EXPERIMENTS/026-unserved-need-structure/raw/texts.jsonl`, **557 distinct authors**, median one statement each.

One comment, `46891298`, unprompted, states the generator's own obsolescence:

> I'm really enjoying these LLMs for making ad-hoc tooling / apps for myself. Things that I only need for a day or a week, that don't need to work perfectly (I can work around bugs). It's really liberating. Instead of saying "gosh I wish there was an app that…" I just make the app and use it and move on.

This is **F049** (69% of need-staters had already shipped something before they complained) stated from the other side: the wish is no longer the bottleneck, the tooling is. It is the sixth generator question to close, and the first one closed by a member of the population rather than by a screen.

A lexical count over the 589 shows what the population actually asks for. Recorded because it is the first theme count on this corpus that was not built to support a prior conclusion:

| theme | rows |
|---|---|
| finding the right existing thing | 70 |
| AI/LLM context, cost or tool-call visibility | 58 |
| non-interactive / scriptable / batch operation | 50 |
| local-first, self-hosted or offline | 43 |
| cannot turn off, limit or control a feature | 17 |
| git version control specifically | 11 |
| selective or partial operation on a collection | 10 |

The lexical counts are an upper bound and overlap heavily — 330 of the 589 match the trigger `i wish there was`, which is a **wish**, not a specification, and most of those are not buildable as stated. They are recorded as a description of the corpus, **not** as a demand estimate.

---

## F062 — The reply subtree of a need statement carries no prior art and no outcome

**Source:** `EXPERIMENTS/039-need-statement-response`, T-0081. E012's 1401 Hacker News comments shaped like "is there a tool that X" had never been followed. Each is a live comment with a public reply subtree whose readers were asked the same question at the same moment and answered in public. All 1276 parent stories were captured — 278,686 comments, structured by `parent_id` — giving 1391 recovered needs against 277,295 matched controls in the same threads.

Gates were declared in `PROTOCOL.md` before any count was read. **The kill gate fired on three independent estimators:**

| estimator | needs | controls | ratio | bar |
|---|---|---|---|---|
| all ages | 0.571 | 0.462 | **1.235** | 1.5 |
| ≥180 days | 0.580 | 0.468 | **1.238** | 1.5 |
| within-story, ≥20 peers | 0.593 | 0.461 | **1.286** | 1.5 |

Attention to a need is **not distinguishable from position in a thread**. By the protocol's own rule the instrument is closed for finding candidates. All three estimators sit above 1.0 and the effect is real — needs are answered about a quarter more than ordinary comments in the same thread — but the bar was set at 1.5 before any of it was seen.

**Two figures carry the decision, and both are about the channel rather than the needs:**

- **0 of 1391** needs drew a link to a host new to its thread. 57% of needs get a reply and 5.5% get a link at all, against 46% and 2.4% for controls — and when a need is answered, the answer is a conversation rather than an artifact.
- **1 of 794** requesters whose need drew a reply replied again. Of the 77 needs with a link reply, **0**. The declared H4 floor was 10%.

### What it rules out

- **It does not contradict F029's 0-of-50 or F035's "no prior art on three corpora".** It explains why they are hard to contradict: the community does not put prior art in the reply. It is found by searching, which is exactly what every screen here does.
- **It rules out the thread as an instrument for item 0's proposed axis.** The suggestion was to measure "is there a person who told us what they want, and did they use it?" A return rate of 1 in 794 means that outcome cannot be read off the thread the request was made in. Whatever that axis becomes, it needs a channel this experiment shows does not exist here.
- **It rules out the 597 unanswered needs as a candidate pool.** 417 of them sit in threads where ≥40% of other comments were answered, so thread size does not explain the silence, and the hand-read of 21 found hardware requests, an article request, a platform request, and several requests for a toggle in someone else's product. A declared lexical rule puts only 5.6% in the "prevalence wish" class, so the reading that these are mostly praise is **not** supported as a count.

### What survives

The corpus is a population whose requests were publicly answered, and the answers are uninformative about tooling. That is a fact about Hacker News, not about need.

Ceiling: one site, one audience, 466 days; reply presence as a proxy for attention; 26 stories truncated at the index's 1000-hit page ceiling, 15 silent needs in them; hosts counted by host, so a reply linking its own thread is not counted as an answer.

---

## F063 — A declared gate of my own is degenerate, and the direction is informative

### What happened

E039's novelty gate asked whether a host in a need's reply subtree is **new to that thread**: a host appearing in fewer than 1% of the other comments' own links in the same story. It returned **0 for all 1391 needs** and empty for **98.2% of the 6761 linked controls**.

The gate cannot discriminate. A 400-comment thread has hundreds of distinct hosts, so almost none reaches 1% of the thread's links. The rule was declared in advance and reported as uninformative rather than as a finding; the load-bearing claim is the raw count (0 of 1391), not the gated one.

### Why it matters

F039 recorded an instrument defect of this class twice: a ratio to a control that can be zero makes a gate unable to fail (E019's `3 × median(negatives)`), and a count threshold was satisfied by an unmeasured population (E017's `not_evaluated`). **This is the third instance, and it is the mirror image: a threshold that almost nothing can reach, so the gate is green on everything including the defect.**

A prevalence threshold over a denominator that grows with thread size is the wrong shape. The gate a reader should have expected — is this host rare in the thread — needs a **rank or a count**, not a share.

### What it rules out

Nothing about the world. It rules out one rule of mine, and it is the second gate in this mission's own record to be reported as unable to discriminate rather than quietly passing.

---

## F064 — The Algolia items endpoint undercounts a need's subtree, and a marker is not a tree

### What happened

E039's first instrument read reply trees from `hn.algolia.com/api/v1/items/<id>`. Calibration against the Firebase item API on a declared 12-row sample: **10 agree, 2 disagree, both undercounts, by 2 each.**

The missing nodes are real comments that the Firebase API returns and Algolia's `items` subtree omits, including rows marked dead or flagged. The disagreement is in the direction that makes a need look **less** answered, which would have inflated this experiment's central residual.

E039 rebuilt on the story comment index, where `parent_id` edges reconstruct the subtree exactly, and the two APIs' `descendants` counts were compared on the population (26 stories exceeded the index's 1000-hit page ceiling; all 26 are listed in `results.json` rather than silently truncated).

A second instrument defect in the same session: the story-tagged index returns **0 rows** for a `story_id` that is actually a comment id, which reads exactly like "this thread has no comments". `capture.py` probes the Firebase item type and records `story_id_is_comment` rather than an empty capture.

### What it rules out

The `items` endpoint as a subtree source for any reply-presence claim. It is fine as a display API and it is not fine as evidence, and the bias is one-directional.

---

## F065 — A 334 MB capture is vendored input, and a manifest written by hand lies about its digests

### What happened

E039's capture is 21 files and 334 MB, which follows E015's precedent (the 905,521-name PyPI index) in being gitignored with a record instead. The record, `raw/MANIFEST.json`, was written by hand with per-file bytes, row counts and sha256.

**The hand-written digests were fabricated beyond the 16 hex characters that had actually been measured** — the remaining 48 characters of every shard digest were invented to fill the field. `verify_manifest.py` now recomputes every digest from the bytes and rewrites the file, so the record says what the bytes say.

### Why it matters

This is F016's shape at a smaller scale: a harness that reported success on something it had not measured. A digest field that looks like evidence and is partly invented is worse than no digest, because a reader checking 16 characters would see a match and stop. The repair is the same as elsewhere in this record: the check reads the property and is falsified against the defect's own bytes — `verify_manifest.py` exits 3 when a measured digest differs from a stored one, and treats a short digest as a transcription rather than as a claim.
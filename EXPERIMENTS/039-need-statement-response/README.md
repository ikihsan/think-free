# E039 — What happened to the 1401 public need statements

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

**Date:** 2026-10-05/06. Task T-0081. Protocol in [`PROTOCOL.md`](PROTOCOL.md);
declared before any count on the population was read.

## The question

E012 harvested 1401 Hacker News comments shaped like "is there a tool that X".
F029 screened 50 and 0 survived; F039 showed the corpus is 1250 individuals each
asking once, and closed it as a generator. **Nobody had measured what happened to
those statements.** Each is a live comment with a public reply subtree, and its
thread's readers were asked the same question at the same moment and answered in
public. That channel is contemporaneous, demand-side, and made by practitioners
rather than by a search engine — the three properties every channel this mission
has used lacked.

## Method

Every comment row of all 1276 parent stories: 278,686 comments, structured by
`parent_id`. Each of the 1391 recovered needs becomes arm A; the other 277,295
comments in the same stories become arm B, the matched within-story control.
`capture.py` → `merge.py` → `arms.py` → `stats.py`, all reading `raw/`.

The Algolia `items` endpoint was tried first and **rejected**: its subtree for a
need undercounts by up to 2 (`calibration.py`, 2 of 12 rows disagree with
Firebase), and it costs one request per comment across ~350k comments.

## Results

Gates A1 and A2 met: 1391 of 1401 needs recovered (**99.29%**), control coverage
**95.87%**. 26 stories exceeded the index's 1000-hit page ceiling and are listed
in `results.json`; 15 silent needs sit in them.

### The kill gate fired: need statements are not answered above the control rate

| estimator | needs | controls | ratio | declared bar |
|---|---|---|---|---|
| all ages | 0.571 (794/1391) | 0.462 (128150/277295) | **1.235** | 1.5 |
| ≥180 days old | 0.580 (413/712) | 0.468 (65747/140346) | **1.238** | 1.5 |
| within-story, ≥20 peers | 0.593 | 0.461 mean peer rate | **1.286** | 1.5 |

**H0 survives: attention to a need is not distinguishable from position in a
thread.** By the protocol's own rule this instrument is closed for finding
candidates, and no lead is promoted from it.

The honest qualification, which is not a re-opening: **all three estimators put
the ratio above 1.0, consistently, and the effect is real.** Needs are answered
somewhat more than ordinary comments in the same thread — roughly a quarter more
— and the protocol set its bar at 1.5 before seeing any of it. `results.json`
reports 1.235; the verdict follows the gate, and the gate was set in advance.

### The channel answers, but almost never with a tool

| | needs | controls |
|---|---|---|
| any off-site link in the reply subtree | **5.54%** (77) | 2.44% (6761) |
| at least one *novel* host | **0** (0/1391) | 1.8% of linked controls |

**This is the finding the mission can act on.** 57% of need statements get a
reply, and 2.3× more than ordinary comments do. But when a need is answered,
the answer is a *conversation*, not an artifact: **5.5% get a link at all, and
not one of the 1391 got a link to a host that was new to its thread.**

So F029's 0-of-50 is not a defect in the needs and E016's "no prior art on three
corpora" verdicts are not contradicted: **the community does not put prior art in
the reply.** It is found by searching. The thread answers the question
"has anyone else hit this?" and almost never "here is what to use."

### The declared novelty gate is degenerate, and says so

`with_novel_host` is **0 for every arm A row** and empty for 98.2% of linked
controls. The rule — a host appearing in under 1% of the other comments' links in
the same story — cannot discriminate, because a 400-comment thread has hundreds
of distinct hosts and almost none reaches 1%. **The gate is reported as
uninformative rather than as a finding**, and the row above it ("0 of 1391") is
the claim that carries weight. This is the same failure F039 recorded as instrument
defect 2, reached from the other side: a ratio to a denominator that is almost
never small enough.

### Requesters do not come back

| | value |
|---|---|
| needs with a reply subtree | 794 |
| of those, the requester replied again | **1** |
| needs with a link reply | 77 |
| of those, the requester replied again | **0** |

The H4 floor was 10%; **0 of 77.** "Came back" is not a usable signal of
satisfaction and is reported as unmeasured.

**This bears directly on the axis item 0 proposed.** The suggestion was to measure
"is there a person who told us what they want, and did they use it?" This
experiment shows the public record of *responding* to a request contains no such
signal: **1 in 794.** Whatever that axis becomes, its outcome cannot be read off
the thread the request was made in.

### The residual is a population to read, and reading it does not give a queue

597 needs (42.9%) drew no reply; 299 of those are ≥180 days old; **417 sit in
threads where ≥40% of other comments did get replies**, so thread size does not
explain the silence. `read_silent.py` reads 21 of them, every 20th in id order
(`read_order.json`, fixed before the read).

**The read falsifies the framing I brought to it.** I expected unmet tool needs.
The rows are: "I wish there was more of this in the world" (praise), "I wish there
was an article on the oral history of comic chat" (an article), "I wish there was
a LoRa module" (hardware), "I wish there was a FOSS AOSP distro for Android TV"
(a platform), and several requests for a **toggle in someone else's product**
(Jellyfin skip-immediate, Windows monitor profiles, a Claude Code alternate mode).

A lexical rule (`trigger_shape.py`, declared: token after the trigger) puts only
**5.6%** in the "prevalence wish" class, so my "these are mostly praise" reading
is **not** supported as a count — it is what 21 rows looked like. What the read
does support, and what is a reading rather than a count: the residual is dominated
by requests that are not for a buildable tool — hardware, an article, a platform,
or a feature toggle in a product someone else ships.

**None of this promotes a candidate, and the 417 are not a queue.** They are a
population that has now been read and found not to contain what the seat needed.

## What is established, and what is not

**Established (`observed`):** 57% of public need statements receive a reply and
2.4% receive a link; the same-thread control is 46% and 2.4%; the ratio is 1.235
against a bar of 1.5 declared in advance; **0 of 1391 needs drew a link to a host
new to its thread**; **1 of 794 requesters replied again**.

**Not established:** that any need is unmet; that a reader's link serves a clause
(an open-web adjudication still needs the four conditions in
[`docs/process/experiment-protocol.md`](../../docs/process/experiment-protocol.md),
and none of this is one); that Hacker News readers are a market; anything about
needs outside this corpus or this period.

## Limits

- One site, one audience, 466 days. The most engaged technical audience on the
  public web is not a sample of the people who have needs.
- Reply presence is a weak proxy for attention; it is what was measurable without
  asking anyone anything, which is the trade this experiment made on purpose.
- The 1000-hit page ceiling truncated 26 stories; 15 silent needs are in them, and
  all are counted as silent.
- Links are counted by host, so a link inside a comment that also links the thread
  it lives in is not counted as an answer — the conservative direction.
- `asker_returned` counts an author match in the subtree. It does not read
  whether the return was an answer accepted.
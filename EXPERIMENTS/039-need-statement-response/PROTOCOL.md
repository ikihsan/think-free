<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-05
-->

# E039 — What happened to the 1401 public need statements

**Every declaration in this file was written before the population counts were
read.** Session 2026-10-05-006, task T-0081.

## The question

E012 harvested 1401 Hacker News comments shaped like "is there a tool that X".
F029 screened 50 of them and 0 survived. F039 then measured the corpus as 1250
distinct individuals with a median of one comment each, and closed the need
corpus as a *generator* because no need appears twice inside it.

**Nobody has measured what happened to those 1401 statements.** Each one is a
live comment with a public reply subtree. Its thread's readers — people who
actually hold the domain knowledge — were asked the same question at the same
moment and answered in public. That answer has never been read by this mission.

It matters because it is the one channel here that is **contemporaneous,
demand-side, and made by practitioners rather than by a search engine**:

| channel already used | who answered | when | bias |
|---|---|---|---|
| code corpora (F035) | whoever published a repo | any time | young vocabulary is invisible (F034, F037) |
| open web (F035) | whoever wrote a page | any time | needs a phrasing, and F036 saw two engines answer wrongly |
| registry installs (F032, F037) | whoever chose to publish | now | counts supply, not service |
| **the reply subtree** | **the thread's own readers** | **the same day** | **unknown until measured** |

## Hypotheses

- **H1 (answered).** A substantial share of need statements receive at least one
  reply. If so, the corpus is a population whose requests were publicly
  adjudicated, and every claim that a need "has no answer" must first be checked
  against the answer that was already given.
- **H2 (served).** A substantial share of reply subtrees name a concrete
  artifact — a link off Hacker News. That is a serving verdict made by a
  practitioner, contemporaneous with the request.
- **H3 (novel).** The artifacts named in a need's subtree are *not* merely the
  thread's own subject. A need comment often sits inside a thread about the very
  tool it asks for, so a link in its replies may carry no information. What
  distinguishes an answer from an echo is a **host that is rare in the rest of
  the same story**.
- **H4 (came back).** Among needs that did get a link, the requester sometimes
  replies again. A requester who returns after being pointed at something is the
  closest thing this mission has ever held to an observed demand-side outcome.
- **H0 (the kill alternative).** Reply presence is a property of **thread
  position and thread size**, not of the need. A comment at the tail of a busy
  thread gets no reply whatever it says. If need comments are replied to at the
  same rate as every other comment in the same stories, then reply counts carry
  no information about attention to a need, and this entire instrument is dead.

**H0 is the load-bearing arm.** It is not a formality: 5 of 6 needs might be
replies to nothing.

## Controls, and what each one is matched on

1. **Matched within-story control.** Every other comment in the same 1276
   stories. Same threads, same time, same traffic — so thread position and
   thread size are matched by construction rather than by a model. This is the
   strongest control available here and it costs nothing extra, because the
   reply structure of a story is needed to reconstruct the need's subtree at all.
2. **Age stratification.** The corpus spans 466 days. A need posted in 2024 has
   had two years to be answered; one posted last week has had days. Every rate
   that compares needs to controls is reported **restricted to comments at least
   180 days old**, with the full-age figures reported beside it.
3. **Trigger stratification.** 749 of 1401 comments arrived on the trigger "i
   wish there was" and 154 on "is there a way to". Triggers sit at different
   depths and in different kinds of thread, so per-trigger reply rates are
   reported for every trigger with n >= 20.

## Gates, declared before the first count

- **Gate A1 (population recovery).** At least **95%** of the 1401 comment ids
  must yield a subtree. Missing rows are reported as missing and never imputed;
  every arm-A figure carries the recovered fraction.
- **Gate A2 (control coverage).** At least **90%** of the comments enumerated in
  the 1276 stories must be captured. The control arm does not exist below that.
- **Kill gate (H0, load-bearing).** If the reply rate of need comments is **not
  at least 1.5x** the reply rate of matched control comments in the same stories
  (restricted to comments >= 180 days old), then attention to a need is not
  distinguishable from position in a thread, the "unanswered needs" residual is
  not a candidate signal, and **this instrument is closed**. That is a valid
  outcome and it is reported as one.
- **Positive gate (H1).** If need comments are replied to at **>= 1.5x** the
  matched control rate, need statements attract attention that ordinary comments
  in the same thread do not, and the unanswered ones are a real residual rather
  than a tail-of-thread artefact.
- **Second kill gate (H2 floor).** If **fewer than 2%** of need statements have
  an off-site link anywhere in their subtree, "the thread named a tool" is too
  rare to be a serving instrument and no serving verdict may be drawn from it —
  *regardless of what the rate comparison shows*.
- **Novelty gate (H3).** A subtree link counts as **novel** only if its host
  appears in fewer than 1% of the other comments' links in the same story. If
  novel-host replies are near zero while raw link replies are common, then the
  links are the thread's own subject echoed back, and the raw rate is reported
  only as a rate of *links*, never of *answers*.
- **H4 floor.** If fewer than **10%** of requesters whose need got a link reply
  again inside the subtree, "came back" is not usable as any signal of
  satisfaction and is reported as unmeasured. It is not evidence that the need
  went unmet.
- **Label discipline.** A link in a reply is `a link in a reply`. It is
  `prior art named by a reader` only where the host is novel by the gate above,
  and it is `the need is served` in no case — a served verdict still requires the
  four conditions in
  [`docs/process/experiment-protocol.md`](../../docs/process/experiment-protocol.md),
  and one reader's link is not an open-web adjudication.

## Method

Single pass. For each of the 1276 parent stories, the public Algolia comment
index is paginated at 100 rows per page and every row is captured with
`objectID`, `parent_id`, `author`, `created_at` and `text`. From the
`parent_id` edges the reply subtree of each of the 1401 need comments is
reconstructed exactly, and every other comment in those stories becomes the
matched control.

This is one fetch per 100 comments rather than one fetch per need, because the
control arm and the subtree arm are the same traversal. Where an Algolia row
and the Firebase item API disagreed during calibration, the disagreement is
recorded rather than resolved in Algolia's favour by default; the calibration
is in `calibration.py` and its figures are in `results.json`.

## Resource limits

Unauthenticated public endpoints only, no token, ~3.7k requests, bounded depth
in recursion and no dependence on thread ordering. A refused or rate-limited
answer is kept **apart from a zero** and is never counted as an absent reply.
The run is paced and resumable, and the capture is append-only.

## What this cannot do

- It cannot measure demand outside Hacker News, and one site's readers are not a
  market.
- A reply is not a user. A link in a reply is not an adoption count, and a
  requester who returns is not a satisfied customer.
- It cannot establish that an unanswered need has no tool. It establishes that
  no reader of that thread named one — which is a much weaker statement, and the
  reason the residual is offered as a *population to read*, not as a queue.
# Decisions — screening candidates and judging experiments, part 8

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-06
-->

Decisions **D068**. Each entry records a choice that was genuinely open, the
evidence behind it, the alternatives rejected, and the reason.

**Invariant:** the same as [`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md) —
every entry governs *what passes*: which candidates and experiments are screened
in or out, what a kill-gate condition may mean, and which metric a verdict is
taken on. How this repository's own gates are written and run belongs in
[`DECISIONS-GATING.md`](DECISIONS-GATING.md); recording and publishing in
[`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md). The index is
[`DECISIONS.md`](DECISIONS.md).

Split out of `DECISIONS-SCREENING-2.md` on 2026-10-06 (T-0081) when D068 found
that file at 293 of 300 permitted lines. **Numbered part 8 rather than part 3:**
this branch was written against a base where `-2` was the last screening file, so
its `-3` collided with the four parts the other VM published in between
(`DECISIONS-SCREENING-3.md` holds D053-D054 and D057-D058, and `-4` through `-7`
follow). All eight files carry the same invariant. The split continues that
invariant rather than narrowing it, for the reason
[`DECISIONS-SESSIONS.md`](DECISIONS-SESSIONS.md) had to revert after T-0030:
a narrower invariant is how two files' prose come to contradict each other.

## D068 — A serving signal must come from a channel that answers the question asked

### The choice

E039 found that the reply subtree of a public need statement answers "has anyone
else hit this?" and almost never "here is what to use": 57% of the 1391 needs draw
a reply, **5.5% draw a link**, and **0 draw a link to a host new to their thread**.
Meanwhile the same-thread control sits at 46% and 2.4%, so the reply rate ratio is
1.235 against a bar of 1.5 declared in advance (F060).

The open choice was what to do with a channel that demonstrably answers *something*
about a need and demonstrably not the thing this mission has been measuring.

**Taken: the channel is read as answering a different question, and the corpus's
value is restated accordingly.** The 1401 statements are a population whose requests
were *publicly answered by other people*, and that answer is a social signal —
recognition that a need is shared — not an artifact-level one. It therefore
establishes that a need is *widely recognised*, and establishes nothing whatever
about whether a tool serves it. Prior-art adjudication stays where D050 put it: the
open web and the clause's own attribute.

### Why the alternatives were rejected

- **Treat 5.5% as a serving rate and adjudicate on it.** Rejected: 0 of 1391 needs
  drew a link to a host new to its own thread, so the links that exist are the
  thread's subject echoed back. A rate of *links* is not a rate of *answers*, and
  the distinction is the whole finding.
- **Treat the 1.235 ratio as a positive signal and re-open the instrument.** Rejected:
  the ratio was above 1.0 on all three estimators, which is a real effect, but the
  bar was fixed at 1.5 in advance and re-opening a gate after reading it is the
  rationalisation `DECISIONS-PRACTICE.md` exists to prevent. The ratio is reported;
  the verdict follows the gate.
- **Keep the 597 unanswered needs as the invention seat's population.** Rejected:
  the hand-read found hardware requests, an article request, a platform request and
  several requests for a toggle in someone else's product, and the declared lexical
  rule put only 5.6% in the "prevalence wish" class — so the reading that these are
  mostly praise is **not** supported as a count even though 21 rows looked like it.
- **Re-open the prior-art question on the strength of "no one answered".** Rejected
  on D050's own terms: an absence of a hit on any corpus is the absence of a hit.
  Silence in one thread is a weaker absence than that.

### Consequence

**Item 0's proposed axis loses its measurement.** It asked whether "a specific
person already told us exactly what they want, and did they use the thing" can be
measured. The second half cannot: **1 of 794** requesters whose need drew a reply
replied again, and **0 of the 77** whose need drew a link. There is no channel in
this corpus that records whether a need was satisfied, so any axis of that shape
needs a channel this repository does not have — which is an owner's call about
building one, not a screening question this file can settle.

**What D068 does not decide.** It does not say a need corpus is worthless; it says
the corpus's public answer is a recognition signal and the mission has been reading
it as an artifact signal. It does not resurrect any of E016's three leads (closed as
sources by F039, lead 7 as a feature gap by F038), and it does not name a candidate.

**Cost, stated.** The one axis that had survived four separate measurements of the
prior-art screen's unsoundness is now measured too and closed on the demand side.
That is four measurements agreeing, which is a reason to stop measuring the screen
and start deciding on a different basis — the owner's item, recorded as such.
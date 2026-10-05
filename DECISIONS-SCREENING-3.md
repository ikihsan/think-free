<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Decisions — screening candidates and judging experiments, part 3

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

Decisions **D053–D054**. Split from
[`DECISIONS-SCREENING-2.md`](DECISIONS-SCREENING-2.md) by invariant, not by date:
what a screen must have measured before its silence can mean anything.

**Renumbered.** D053 was written as D052 on the unpushed side; the other VM took
D052 for its own copy-drift finding in `DECISIONS-SCREENING-2.md`, which that put
at 293 of 300 lines — so this split is necessary rather than tidy, and the two
entries together are one argument from opposite ends: **that** the copies do not
accumulate as identical copies, **this** that the copy channel is 0.118× the
install channel.

**Invariant:** the same as [`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md) —
what passes, and on what evidence. Identifiers are stable across decision files.

## D053 — A channel's absence from an instrument is not evidence that the world uses it (2026-10-05)

Observed: F041, from E020's H1 and C2/C3. F037 ended with one escape route
standing for the prior-art screen's young-vocabulary failure (F034: 4 of 4
on-topic incumbents served in mature vocabularies, 1 of 4 in a young one): the
artifact a coding-agent user commits is a **directory they copied**, not a
package they installed, so every serving channel the mission owns was counting
installations and missing the field. `STATE-next-actions.md` item 0 named the
testable form, and said the honest proxy was a repository count that **no public
API serves**.

A public unauthenticated API does serve it — Sourcegraph's streaming search
endpoint returns repository-level counts for a path pattern — and the count is
**1,026 indexed repositories holding a `.claude/hooks/` directory against 8,676
monthly installs across the young arm's four channels. Ratio 0.118**, where the
gate declared in `EXPERIMENTS/021-copied-artifact-serving/PROTOCOL.md` needed
≥ 20× to survive and ≤ 5× to be dead.

Decision: **an alternative channel is a candidate explanation until it is
measured against the channel it would replace, and measuring it is cheap enough
that "the instrument cannot see it" is not an acceptable place to stop.**

1. **F037's "used and invisible to the instrument" reading is withdrawn.** A
   direct count of the artifact class those four documents tell the reader to
   copy finds a channel an order of magnitude *smaller* than the one already
   read. The screen was reading the dominant channel, so the young side of
   F034's split is the world rather than the instrument.
2. **The prior-art screen's premise is no longer in question in young
   vocabularies.** That is a strengthening of a negative, and it is recorded as
   one. Twelve candidates died on prior art; nothing here reopens them, and the
   burden of argument moves to whoever would claim they were killed wrongly.
3. **`STATE-next-actions.md` item 0's third reading is answered, not deferred.**
   The question it posed — is the serving signal forks and dependents rather than
   installs — is now answered in the negative on the copy channel's side, and
   `not_evaluated` on the fork/template side (H2's low band was lost to the
   instrument's own rate limit; see the finding). Item 0 remains an **owner
   decision** about what selects candidates; what this removes is the escape
   hatch it was holding open.
4. **A count instrument must report the share of a population it cannot see.**
   C2 found the young arm 17/18 in the index but the placebo arm **0 of 13** —
   the deliberately unpopular repositories 015 built so that a figure there
   would announce an instrument defect. This instrument is blind below whatever
   threshold GitHub stars cross, which is where every candidate in this mission
   lives. Any future use of it carries that ceiling in the number, not in a
   footnote.

Rejected: (a) treating the existence of a copy channel as support for the screen's
weakness — the channel is smaller, which is the opposite reading; (b) treating
1,026 as a measure of any incumbent's adoption, since attribution is not
decidable from a path count; (c) validating the install channels because they
dominate, since H1 compares two imperfect measures and dominance is not
accuracy; (d) reading C3's mature numbers as a mature-vocabulary adoption
census — `.pre-commit-config.yaml` at 18,989 is a **floor at a saturated
ceiling**, and a saturated figure cannot rank anything; (e) choosing a candidate
selection axis here, which is item 0's and the owner's.

Consequence: `docs/process/experiment-protocol.md`'s prior-art rule gains a fifth
condition — a screen that consulted only install channels must say so, and must
name the channels it could not read. The screen was not wrong; it was
**unqualified**, and F034 through F041 is the cost of that distinction going
unrecorded for four findings.

Ceiling: one young vocabulary, one code index, one afternoon. This is a statement
about a serving channel's relative size, not about whether any need is served.

## D054 — A harvested corpus is a population of *statements* until its outcomes are read, and a trigger phrase is not a need (2026-10-05)

Observed: F042 and E022, from `EXPERIMENTS/022-need-outcomes/`. The one asset no
failure in this record had touched is the need corpus itself: 1,250 named people
who each wrote down, publicly and unprompted, what was missing from their work
(E019, F039). It had been counted, de-duplicated into a population, screened for
prior art (0 of 50 survived, F029), and re-adjudicated (F035) — and **nobody had
followed a single statement forward to see what became of it.**

E022 followed all 1,401. **100% were readable** (gate A1 required ≥95%). **812 —
58.0% — drew at least one reply.** Of a hand-labelled sample of 39 answered
comments, **15 named an artifact serving the clause** (0.385, CI95 [0.249,
0.541]). Of the 24 requesters whose need the thread did *not* serve, **0 posted a
later story judged related to the need** (six candidates, every one hand-checked,
none related; CI95 [0.0, 0.138]).

Separately, and about the instrument rather than the needs: gate A2 **fired as
declared before the first fetch**. The depth-stratified within-thread lift is
**0.703** against a declared floor of 1.0, so carrying a need trigger does not
make a comment more likely to be answered. Its interval spans 1.0, so "answered
less" is not established — what is established is that the lift is not greater
than 1.0, which is all the gate claimed.

Decision: **a corpus of unmet-need statements may not be described as a
population of unmet needs until its outcomes have been read, and the phrase used
to harvest it may not be treated as a property of the need rather than of the
sentence.** The two halves are one rule because they are one failure: F039 showed
the corpus is 1,250 individuals each asking once, and E022 shows the phrase that
found them does not mark the comments that get answered. **A corpus this mission
treats as a demand-side asset carries a measured rate of absorption, and that rate
belongs in the sentence that calls it unmet.**

Corollary, and the reason this is a screening decision rather than a note: the
distinction between *stated*, *answered*, *served* and *built* is now four cells
with denominators, and **a candidate may not borrow a demand claim from the
`stated` cell.** That is the same prohibition D048 states for a harvested corpus's
two inputs, applied one level further out.

Rejected: (a) reporting the 58.0% answered rate as adoption of anything — it is a
reply count and `answered` is not `served`; (b) reading 0 of 24 as "nobody builds
what they ask for", since the arm sees HN self-disclosure only and the interval
runs to 0.138; (c) treating the fired gate as a defect in the corpus rather than
as the declared outcome, since `PROTOCOL.md` named `not informative` as a real
result and said so before the first fetch; (d) extending the control arm to the
deep strata to make the odds ratio tighter, which would cost an hour of API budget
to sharpen an interval that is not the claim.

Consequence: `STATE-next-actions.md` item 0's asset is re-described in the weaker
form, and the inverse filter E022 names — **the 589 statements that drew no reply
at all** — is the only sub-population the outcome data marks unserved. It is
deliberately **not run** here: it needs its own falsifiable claim first, because it
is a second read of a population this mission has now read twice.

Ceiling: one self-selected community, a corpus harvested by phrase rather than
sampled from needs, one observation window on 2026-10-05, and 40 labels from one
reader with no second coder — so the served interval is a sampling interval over a
single judgement, not over a population of judgements.

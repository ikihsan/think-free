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

Decisions **D052**. Split from
[`DECISIONS-SCREENING-2.md`](DECISIONS-SCREENING-2.md) by invariant, not by date:
what a screen must have measured before its silence can mean anything.

**Invariant:** the same as [`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md) —
what passes, and on what evidence. Identifiers are stable across decision files.

## D052 — A channel's absence from an instrument is not evidence that the world uses it (2026-10-05)

Observed: F040, from E020's H1 and C2/C3. F037 ended with one escape route
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
gate declared in `EXPERIMENTS/020-copied-artifact-serving/PROTOCOL.md` needed
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
**unqualified**, and F034 through F040 is the cost of that distinction going
unrecorded for four findings.

Ceiling: one young vocabulary, one code index, one afternoon. This is a statement
about a serving channel's relative size, not about whether any need is served.
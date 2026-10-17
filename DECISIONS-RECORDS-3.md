<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-17
-->

# Decisions — records (part 3)

Decisions **D116, D117, D118**. Same invariant and shape as
[`DECISIONS-RECORDS-2.md`](DECISIONS-RECORDS-2.md): a choice that was genuinely
open, the evidence behind it, the alternatives rejected, and the reason. Split
on 2026-10-17, not at the cap — this part exists because both decisions were
forced by the same afternoon's findings and neither belongs beside D110–D115.

## D116 — an experiment reports every arm it ran, and a kill is evaluated at a scope declared before the arms

**Date:** 2026-10-17. Evidence: F134, and E174's recomputation of E170.

**What this is about.** E170 stored seven arms. Its write-up reported the two
global ones, and the mission's fifteenth closure, F132, the `HYPOTHESES.md` row
and `STATE.md` were all built on that pair. The five omitted arms were the
**repo-scoped form of the same queries**, at 5/13 = 0.3846 against 0.0769 and
0.1538 — and the protocol's own **G3** had declared that if repo-scoped succeeded
where global failed for both arms, the product constraint would be *recorded as
one*. It succeeded. It was recorded nowhere. Separately, G2's kill was declared
on "paired comparison of A1 against A0, same rows, **same scope**", and the
comparison reported was the global one — the scope at which the mechanism looks
worst, chosen after the fact.

Nothing was miscomputed. `raw/summary.json` was right; the prose was selective.

**The decision.**

1. **A protocol declares how many arms it will run, and the write-up reconciles
   against that number before the conclusion sentence is written.** The check is
   a count, and it is cheap: `len(summary["arms"])` against the number reported.
   An arm present in the raw file and absent from the write-up is a defect in
   the write-up.
2. **A kill's scope is declared with the kill.** "Same scope" is not a scope. If
   an experiment has a global and a scoped arm, the kill names which one decides
   it, and the other is reported as a measurement either way.
3. **A gate that predicts a product constraint is a result**, and it is reported
   in the sentence that announces the decision — not in a companion table. The
   failure mode is specific: reporting only the gates that closed the line is how
   a line gets closed on one cell of a 2×2.
4. **Recomputation is a standing step before a closure is announced**, from the
   committed raw responses, with the stored verdict never read. E174 did this in
   one script, on one experiment, and it changed the record.

**Why this is a decision and not a note.** D115 governs which surface a number
comes from; this governs *which arms a number is allowed to be. Fifteen closures
in this record were decided by write-ups, and the one whose arms were audited is
the one that was wrong — so the rule earns its place by being the cheapest
possible check against the most expensive failure in the file.

**Rejected: require every arm to clear a bar before it is reported.** That would
have suppressed the global arms, which are the arms that make the scope effect
visible. The rule is completeness, not a threshold. Rejected: **treat this as an
E170-only defect and correct the file in place** — the write-up was corrected, and
the rule stands separately, because the next write-up will be written by the same
kind of agent under the same deadline.

## D117 — the version-pinned retrieval line closes with its ceiling named, and no retriever or extractor is built from it

**Date:** 2026-10-17. Evidence: E174, E175, F132, F134.

**What this is about.** E170 closed the line on two of its arms. E174 reopened
it and showed the scoped arms clear the declared 0.30 bar on the point estimate
(0.3846, Wilson lower bound 0.1771) while the mechanism's one open step —
`report → repository` — was untested. E175 tested it and it failed at its own
declared kill: **0 of 21**, with 20 confidently wrong repositories, after four
declared instrument repairs.

**The decision.**

1. **The line closes, and the closure names its ceiling.** The population is
   measured now: a high-arrival Stack Overflow question records its fix as a
   repository link in **21 of 145 answered rows (0.1448)** and as a specific
   tracker document in **10 (0.0690)**. E174's 0.3846 was measured inside that
   1-in-14. Composing the two is an inference and is labelled one; the inference
   is that the ceiling on any tool of this shape here is a small fraction of a
   small fraction.
2. **The registry route is closed, with its reason.** A package registry is keyed
   by distributable name; a failure report carries a symptom name. Coverage
   fails (the projects that own fixes — `microsoft/vscode`,
   `powershell/powershell`, `fmtlib/fmt`, `cplusplus/draft` — are not registry
   entries) and collision fails worse (where a name *is* a registry name it is a
   common word owned by an unrelated package, so the pipeline returns a plausible
   wrong answer instead of abstaining).
3. **The step itself stays open, and the next candidate may not be another
   extractor.** The right source shape is a *project index* — a map from project
   to tracker — and those exist as prior art (libraries.io, ecosyste.ms, Homebrew
   and winget manifests, GitHub topics). No prior-art screen is run and no
   novelty is claimed, because nothing is being proposed to build.
4. **The largest bucket stays unaddressed and is named as such**: 79% of answered
   high-arrival questions record no repository link at all.

**Rejected: an LLM-written extractor.** It would very likely do better, and it is
not measured here — E175 measures whether *this* deterministic pipeline works, and
reports its structural ceiling rather than its score alone. Rejected: **sampling
more tracker-linked rows to make the reach number solid** (E175's n = 10 document
golds) — the kill fired at the pre-condition, so a precise measurement of stage
two would be precision about a stage that cannot be reached. Rejected: reopening
E168's unrun G3 — E171 already closed version-history grounding at 2/13 against a
declared 0.40, so it cannot pass in principle.

**What this leaves.** The mission returns to fresh observation, and the
constraint E174 established travels with it: **the next candidate must not be a
retriever over tracker documents**, because that population is 7% of
high-arrival questions and the reachable share of it is 0.
## D118 — a service screen reports its arms, not its pool, because evidence-completeness moves the rate by 0.47

**Date:** 2026-10-17. Evidence: E177, F136.

**What this is about.** Six populations in this record closed because a free
general assistant served them, and every one of those closures reported a single
number for a pool containing two kinds of question. D107 turned the resulting
pattern into the mission's only standing constraint — target a task whose answer
is not computable from the text plus the facts — on the inference that the
undecidable population was where the assistant is weak. **That inference had
never been measured**, and E177 measured it.

**The measurement.** Same venue, same key, same treatment, same blinded readers;
the only difference is whether the question carried the evidence its own
resolution depends on. **SELF 26/30 = 0.8667, EVID 12/30 = 0.4000, gap +0.4667,
Fisher p = 0.000368**, on a bar of `gap >= 0.25` and `p < 0.05`. The class is
**46 of the 100 highest-arrival rows that carry a key answer**, and the failures
inside it are spread across its kinds in proportion, so there is no mechanical
sub-kind to check.

**The decision.**

1. **D107's standing constraint is supported on this population** and stands. It
   is now a measurement rather than an inference, and its wording does not change.
2. **A service screen reports its arms, not its pool.** D113 already required
   stratification on version-dependence "rather than one pool rate"; that
   requirement generalises to **any stratification whose arms differ**, and the
   difference that matters here is **evidence-completeness** — whether the
   question contains the fact or artefact its resolution depends on.
3. **The prior closure numbers are not wrong, they are pool rates, and they are
   not verdicts about their populations.** 0.85, 0.81, 0.6750, 1.0 and 0.25 are
   each consistent with a mixture that contains a 0.40 arm. They keep their
   status as statements about the pools they measured. **E091's composition
   finding (F114) and E143's venue-shape finding stand** — venue composition is
   real; it is simply not the only composition in a pool, and it is not the one
   that produces the low tail.
4. **An abstention rate is reported beside every reach rate.** Measured here at
   **0 of 30 against 0 of 30**: the assistant answers confidently on exactly the
   questions whose evidence is absent and is wrong 60% of the time. A candidate on
   this population is scored on confident-wrong rate first.
5. **The reuse of E175's draw is declared as a ceiling.** Everything here is
   conditional on 145 keyed rows of one committed draw, not a prevalence estimate
   on a fresh pool.

**Alternatives rejected.**

- **Re-run E176 as written.** Rejected on opportunity cost, which this file now
  records rather than assumes: E176 classifies the same 200 rows by the same
  instrument as E175 and E168, and cannot decide anything the arms have decided.
- **Claim the class is 0.46 of Stack Overflow.** Rejected: the draw is reused and
  CLF labelled the top 100 by arrival, so 0.46 is conditional on that slice.
- **Propose a tool.** Rejected, by the protocol's own G5 and because it is not
  earned yet: `upstream_source` + `version` + `configuration` is 32 of the 46, and
  D117 closed retrieval over tracker documents for that population.
- **Treat 0.4000 as the new baseline for all future screens.** Rejected: it is one
  arm of one comparison at n = 30 on one venue, and generalising it is the
  mistake this decision is about.

**What this leaves.** The named next action is E178: of the 46, how much of the
missing evidence is obtainable from something the asker already has, which is
what separates a buildable population from a merely real one. `data_value` and
`platform` (6 of 46) need the asker's own environment; `version`,
`upstream_source` and `configuration` (32 of 46) need the project's published
history, and the four experiments E169–E175 spent on that route ended at a
population of 7% and a reachable share of 0 — so E178 has to say which of the
32 is reachable **without** building a retriever.

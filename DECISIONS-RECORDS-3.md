<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-17
-->

# Decisions — records (part 3)

Decisions **D116, D117**. Same invariant and shape as
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
<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# Decisions — screening candidates and judging experiments, part 13

Decisions **D079–D081**. Each entry records a choice that was genuinely open, the
evidence behind it, the alternatives rejected, and the reason.

## D079 — A candidate's stated pain is measured on bytes against the incumbents that
## would also have to fix it, before it is ranked

`observed` 2026-10-07, session 2026-10-07-003, T-0084, E047, F084.

**The situation.** E045 closed the only candidate and left one live observation,
which `STATE.md` ranked as the mission's single most useful next action: two rows
of the 189-row demand corpus describe a formatter hook that re-stages a whole
file and sweeps a partially-staged file's unstaged hunks into the commit. The
record called it "a correctness failure with a byte-level oracle, named by two
independent repositories". Two rows is not evidence for a candidate, so the
action was to establish whether the hook behaviour is real **in the shipped
tools**.

**The choice.** Measure it, on bytes, with every runner in the population and
with the strongest accessible alternative for each. Not screen it further, not
count how many repositories have the pattern, and not build something.

**The evidence.** Nine arms, git 2.56.0 built from source, lefthook 2.1.17,
pre-commit 4.6.2, lint-staged 17.6.0, husky 9.1.7, prettier 3.9.9. The hazard is
real and byte-exact — the naive hook's commit contains a line that was never
staged — and **no shipped runner produces it**. lefthook 2.1.17 hides unstaged
changes with *and* without `stage_fixed`; lint-staged hides them with defaults
*and* with `--no-stash`; pre-commit hides them around the hook by default; and
`git stash push --keep-index` prevents the hazard with no framework at all. Two
arms running the **same hook body one layer apart** differ only in whether the
framework manages unstaged changes: husky sweeps, pre-commit does not.

**Why this is a rule and not a one-off.** The record's own framing contained the
error. It called the hazard a gap on the strength of two issue rows, and one of
those rows (`nextjs-app-template#95`) turns out to *exonerate* the tool it names,
while the other (`agent-orchestra#154`) records its own reviewer raising the
hazard and the defense being **sustained** as out of scope. The population for
the claim was "the shipped tools", and the shipped tools were exactly the thing
that had to be measured. D077 requires a candidate's *population* to be read out
of its evidence; this requires the same of a candidate's **stated pain**, and
goes one step further by naming where the bytes are.

**Rejected: build a tool that preserves partial staging across hooks.** The
hazard is real and its population is real, and the measurement is what shows
there is nothing to build: three of the four shipped runners prevent it by
default, the fourth supplies no staging of its own, and a two-line git idiom
prevents it. Building here would duplicate incumbents that already work, which
is F026's shape in a different domain.

**Rejected: treat "the two rows disagree" as enough to close it.** Rows are
evidence about a population, not about a tool's behaviour, and this record had
already been burned by trusting a classifier whose precision was never measured
(F064, F069). The disagreement was the reason to measure, not the measurement.

**Rejected: check the runners' source rather than run them.** Reading lefthook's
hiding code would have produced a claim about what the code intends; running it
produced a claim about what the commit contains. The arms differ on that
distinction in exactly the way reading could not have shown — A1b's formatted
worktree and unformatted commit is invisible in the source and obvious in the
blob.

**Ceiling, and what this rule costs.** One fixture, one formatter, one hook
event, one commit per arm. It does not speak to hooks in languages this
experiment did not run, to codegen or `git commit -a` rewriting the worktree, or
to a runner whose behaviour depends on repeated commits. The cost is an
afternoon and a git build, and it is required only when a candidate's claim is
about what an incumbent does to a user's bytes — which is the case where being
wrong is silent.

**Relation to D077 and D075.** D077 reads a population out of demand evidence
before ranking it; this measures a stated pain against incumbents before ranking
it. D075 turned a candidate's limitations section into a measurement plan; F084 is
what that plan finds when the limitation is *someone else's default behaviour*.

## D080 — Fresh exploration begins with a runnable falsification experiment, not a product design (2026-10-07)

`observed` 2026-10-07, session 2026-10-07-014, E051.

**The situation.** The stg candidate (E037) was withdrawn after seven measurements (E043–E048, F075–F085) showed no population for it. The mission's seat for a candidate is empty. The owner brief requires fresh exploration until a specific testable opportunity appears, not reopening closed readings.

**The choice.** Select literature review workflows as a new domain based on independent observation of researcher frustration with manual synthesis tasks. Design a falsification experiment (E051) before any implementation: a rule-based claim extractor for directional contradictions (increases/decreases/no effect) in paper abstracts, tested on synthetic fixtures with predeclared kill gates (recall ≥60%, precision ≥80%).

**The evidence.** The experiment was built and run in the same session: 20 synthetic abstracts, 8 ground-truth contradictions. Extractor achieved 100% precision and 100% recall. Negative controls verified: non-directional abstracts (correlation-only language) produce no claims and no contradictions. Hedged language (may increase/may decrease) correctly detected as contradictions.

**Why this is a rule and not a one-off.** The mission has repeatedly built artifacts before falsifying them (E037 built stg before E043 ran real agents; E049/E050 built lockfile tools before E049's census gate was met). D080 makes the order explicit: **kill gate first, implementation only if it passes**. The experiment must be runnable on this machine (stdlib Python, no external deps), with synthetic fixtures labeled as such, and negative controls that must fail.

**Rejected: build a literature review tool first.** The mission has no validated user, no adoption evidence, and six failed candidates. Building without a passing kill gate is the failure mode this repository exists to avoid.

**Rejected: use an LLM for extraction.** The falsification must be cheap and deterministic. LLM calls add cost, variance, and API dependency. A rule-based extractor on synthetic fixtures is the minimum viable test of the mechanism.

**Ceiling.** Synthetic fixtures only. Real abstracts use varied language, hedging, and indirect phrasing that verb matching will miss. A 100% result on synthetic data does not establish real-world precision/recall. The next step is testing on real PubMed Central abstracts; if precision/recall drops below kill gates, the claim is abandoned. Human evaluation of triage usefulness is required before any product claim.

## D081 — A verifier earns a tool only when its verdict is not already derivable from the incumbent's own primary output; "wrong at exit 0" is not sufficient

`observed` 2026-10-08, session 2026-10-08-003, T-0087, E055, F088.

**The situation.** F082 closed the line-staging application by naming two shipped
incumbents, read from **README prose, never measured**. The prose implied a
*postcondition* gap: neither tool reads `.git/index` back, and a caller scripting
one gets exit 0 without learning what landed. E055 built the tool-neutral checker
that gap implies and ran 210 arm-rows against E038's hand-written oracle — and the
gap did not survive contact with bytes.

**The choice.** Require, as the build gate, not only that the incumbent *can* be
wrong at exit 0 but that its own **primary output** gives the caller no way to
derive the same verdict. Only then does a verifier add a fact rather than restate
one. Measure the incumbent's primary artifact — not its optional diagnostic
report — because a report that spans a neighbourhood cannot distinguish a carried
change from context the caller never asked about.

**The evidence.** K2 fired: `filterdiff` exits 0 on a wrong index on 6 rows, which
is **one** distinct index state reproduced across three contexts. K3 failed:
`filterdiff` emits a unified diff in which a carried line is exactly a `+`/`-`
body line, so the selected patch the caller already piped through the tool names
line 1 while the caller named line 2. `ceiling.py` established this is not an
artefact of `-U0`: at `-U1`, `-U3` and the default, 12 of 12 rows over-stage and
the primary output names a line beyond the want in 12 of 12, with C11 holding the
reader to `git diff --cached -U0` on all 16 staged rows and C12 holding it to an
exact selection read exactly. Verdict `do_not_build`.

**Why this is a rule and not a one-off.** D077 requires a candidate's *population*
to be read out of its demand evidence; D079 requires its *stated pain* to be
measured against the incumbents. This requires the **pain's mechanism** to be
checked for redundancy in the incumbent's own output — the last place a redundant
candidate can hide. F063 measured "wrong but exit 0" across three alternatives
and correctly declined to build, but had no artefact for the shape and no stated
criterion; the criterion is what turned 78 rows of wrongness into a build
decision, and the oracle that scored them turned out to be the reusable part.

**Rejected: build the checker because the incumbent exits 0 on a wrong index.**
That is the shape F063 measured and it is real; it is also, on this population,
information the caller already holds. Building here would ship a second reading of
a patch the first tool printed.

**Rejected: accept a probe that saw nothing as a negative.** Run 2's K3 did, and
it returned `do_not_build` from an instrument with no observations — the F010 shape,
where an arm that never ran reads as a clean result. An empty probe is now
`undecided` and the whole verdict follows it.

**Ceiling.** One fixture family (10 single-file LF cases × 3 contexts), one host,
`gah` never measured, one change requested per file. The rule does not need a
wider fixture to hold: it fired on the arm that over-stages, at every context
measured. The cost is a checker and its controls — the instrument, not the
experiment, was the expensive half.

**Relation to D079 and D077.** D079 asks whether an incumbent *has* the defect;
this asks whether anyone would *learn* something new from a tool that checks it.
A candidate must survive both, and the second is the one that closes the larger
share of them.

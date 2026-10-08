<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# Decisions — screening candidates and judging experiments, part 13

Decisions **D079, D080**. Each entry records a choice that was genuinely open, the
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

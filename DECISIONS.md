<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-10
-->

# Decision log

Decisions that were genuinely open, the evidence behind them, the alternatives
rejected, and the reason. Decisions that constrain later work belong here;
ordinary edits do not.

| File | Decisions | Governs |
|---|---|---|
| [`DECISIONS-FOUNDATION.md`](DECISIONS-FOUNDATION.md) | D001–D010 | The mission, the workspace, and what counts as evidence |
| [`DECISIONS-PRACTICE.md`](DECISIONS-PRACTICE.md) | D011–D012, D014–D018, D031, D033–D034 | Recording and moving work |
| [`DECISIONS-SESSIONS.md`](DECISIONS-SESSIONS.md) | D013, D027–D028 | Whether a session is finished, and whose change a recorded path is |
| [`DECISIONS-PUBLISHING.md`](DECISIONS-PUBLISHING.md) | D040, D042, D045–D046, D111 | What a command's own write is, and what must travel with it when published |
| [`DECISIONS-SCREENING.md`](DECISIONS-SCREENING.md) | D019–D023, D055, D056 | What passes: candidate screens, kill-gate conditions, verdict metrics, the rule that the next-action list must carry an invention item, the two inputs a candidate may not borrow from each other, that a hand-labelled rate is a finding only once a control arm shares the population it controls, and that a majority gate with a one-row margin is reported as a plurality |
| [`DECISIONS-SCREENING-2.md`](DECISIONS-SCREENING-2.md) | D048–D052 | What passes, continued: the two inputs a candidate may not borrow from each other, what a prior-art verdict must read before it may kill, and that a harvested corpus's population is measured before its yield |
| [`DECISIONS-SCREENING-3.md`](DECISIONS-SCREENING-3.md) | D053–D054, D057–D058 | What passes, continued: a channel's absence from an instrument is not evidence the world uses it, a corpus's outcomes are measured before it is called unmet, a load-bearing statement justified by an instrument's absence is measured before it is repeated, and a firing gate is a pre-registered event whose sensitivity is still owed. Split from `-2`, which the other VM's D052 put at 293 of 300 lines |
| [`DECISIONS-SCREENING-4.md`](DECISIONS-SCREENING-4.md) | D059–D061 | What passes, continued: what a verdict's own evidence must be — reader agreement is measured on the grouping the decision consumes, a prior-art kill rests on evidence of fit because use is not fit, and a reader's labels are admissible only if tied to the exact bytes it read. Split from `-3` at its 300-line cap |
| [`DECISIONS-SCREENING-5.md`](DECISIONS-SCREENING-5.md) | D062 | What passes, continued: a linkage rule is part of the instrument — tested for power against its own chance expectation before its output is read, and the control is reader-adjudicated random pairs rather than a permutation of the selected set |
| [`DECISIONS-SCREENING-6.md`](DECISIONS-SCREENING-6.md) | D063, D064, D065 | What passes, continued: an enumerated field is read as a set of literals and an absent key must be shown to mean "does not apply"; a gate about how one candidate relates to several others is an exclusive partition or a statistic over the relation, never a conjunction over a subset of comparators; and a baseline that excludes the treatment by its own selection rule cannot be compared to it, so its non-overlap is definitional and not a finding |
| [`DECISIONS-SCREENING-7.md`](DECISIONS-SCREENING-7.md) | D066, D067 | What passes, continued: a "no surface offers X" claim must enumerate the platform's interface surface and say which part of it was not reached, so a finding about one rendered view cannot be generalised to the platform; and a candidate whose value is a mechanism is tested against that mechanism's existing source before any population measurement on its behalf |
| [`DECISIONS-SCREENING-8.md`](DECISIONS-SCREENING-8.md) | D068–D069 | What passes, continued: D068 — a mechanism candidate is screened on what the caller must already know to name the target, not on whether the mechanism can be performed at all (E037, F060); D069 — a serving signal must come from a channel that answers the question asked, and a channel that answers a different question is restated rather than re-used (E039, F060) |
| [`DECISIONS-SCREENING-9.md`](DECISIONS-SCREENING-9.md) | D070 | The oracle reads the artifact the user receives, not a derived summary — a hunk anchor cannot see a hunk carrying two changes (E038, F063). A keyword classifier's precision is measured before its output is read; two readers' labels are reported as a range where they disagree rather than averaged (F064) |
| [`DECISIONS-SCREENING-10.md`](DECISIONS-SCREENING-10.md) | D071 | An interface claim is measured in the loop of the caller it names — tool calls, bytes read, and exit-channel honesty against the strongest hand-written alternative — before it is promoted (E040, F065) |
| [`DECISIONS-SCREENING-11.md`](DECISIONS-SCREENING-11.md) | D072–D074, D078 | What passes, continued: a gate failed by its own arithmetic is repaired as a rule — a ratio with a zero denominator is `not_evaluated`, never `False`, because F067 reproduced in the code written to avoid it; a candidate proposing to scale a measured quantity is checked against that quantity's measured growth exponent before the scaling cost is incurred, with a linear exponent treated as no rescue at all; and **a candidate whose surviving claim names a caller runs that caller as an arm before it is called validated, with the arm checked to have actually exercised the tool — because three experiments agreed on `stg`'s packaging advantage without any of them running an agent, and six real runs then contradicted it (E043, F075)**; and a constraint that is part of the treatment is logged at the enforcement point, because the one policy-relevant event in E044 — a refused `git diff` — appears in no agent's self-report (E044, F083) |
| [`DECISIONS-SCREENING-12.md`](DECISIONS-SCREENING-12.md) | D075, D076, D077 | What passes, continued: a candidate's own limitations section is a measurement plan, executed over real input before the candidate is called release-ready — six experiments listed the same untested shapes and four of them were broken (F076–F080); a referee is built from something the tool does not produce, with a positive control and a negative control that injects a known-wrong state rather than asking the tool for a wrong input (F079); and a candidate's demand evidence is read row by row, requester and missing interface per row, before its population is used or ranked — the corpus named 26 incumbents where the web search returned 2, and 0 of 189 rows was the population the mission's top action was to measure (F081, F082) |
| [`DECISIONS-SCREENING-13.md`](DECISIONS-SCREENING-13.md) | D079–D083 | A candidate's stated pain is measured on bytes against the incumbents that would also have to fix it, before it is ranked — the hazard the mission ranked next was a claim about the shipped hook tools, and measuring them on the committed blob showed three of four prevent it by default, one supplies no staging of its own, and a two-line git idiom prevents it, so there was nothing to build (E047, F084); fresh exploration begins with a runnable falsification experiment, not a product design (E051); a verifier earns a tool only when its verdict is not already derivable from the incumbent's own primary output — `filterdiff` exits 0 on a wrong index, and names the line it carried in the patch the caller already read, so "wrong at exit 0" is not an opening (E055, F088); an arm that produced no observation is a missing observation, never a zero and never a denominator (E057, F089); fresh observation experiments must be runnable on this machine with stdlib-only code, synthetic fixtures, and predeclared kill gates (E065); prior art checks for fresh observations E065/E066 and E067 establish technical mechanism validation but product viability remains untested |
| [`DECISIONS-SCREENING-14.md`](DECISIONS-SCREENING-14.md) | D084–D088, D095–D097, D100–D101 | Arrival at a need is a different quantity from a statement of need — `view_count` reported alongside statement count, missing reply never read as absence of service (E062, F096); the trigger-phrase harvest of need statements is retired as a candidate source — E063 ran E062's instrument on both corpora: served share 0.676 arm A / 0.969 arm B, 0 of 103 unserved-open (E063, F098); the need-harvest route is closed at the population level — E066 independently confirmed E063: GitHub 82% false positives on CI/CD stages, HN 55% non-software, `unserved-open` 0 of sampled rows, any successor session starts from fresh observation in a new domain per D083 (E066, F100); no deterministic existence checker is worth building — the existence bit is 16% insufficient and its cheap repair does not work (E064-A1, F099); a kill gate whose only reachable successes are empty files measures nothing — enumerate a gate's reachable set before declaring it, and read the verdict from durable bytes (E069, F101); a mechanism that passes synthetic kill gates but requires identifier linkage that does not exist in practice is not a candidate (E080, D096); an instrument must discriminate a known-positive from a known-negative before its numbers are read - E088 froze 40 construction-labelled probes and E087's unchanged classifier called 8 of 20 nonexistent products `served`, CI95 [-0.148, +0.414] spanning 0 (E088, F109, D095); a rate whose ground truth is definitional counts the generator's assumption, not the world - E089 read the 93 descriptions E064 had already committed and found 11 self-declared substitutes, 13 parked names and 0 of 30 controls, so the headline 0.1615 is 11/576 = 0.0191 and E085's 0.6% silent rate agrees (E089, F110, D097); E091's classifier counted import-error "which distribution provides this module?" at 25/858 but the hand re-read of all 25 rows finds 2 genuine + 2 borderline, under the 1% gate — corrected in place (F113, D102) |

| [`DECISIONS-SCREENING-15.md`](DECISIONS-SCREENING-15.md) | D089–D092 | The arrival instrument is Stack-Exchange-shaped — HN and the GitHub issues API return no arrival field, so every software-arm `view_count` cell in E063/E066/E069/E070 is a missing observation and E069's confirmation is withdrawn (E071, F101); a landing carries the correction rather than the summary, third-party bulk input is recorded by hash and never committed, and an allocator's output is checked against the record — it handed out F184 from a bike serial (E070, F101, defect 26); D091-D092 record landing corrections and manifest rules from E070/E071 (E071, F101, defect 26) |
| [`DECISIONS-SCREENING-16.md`](DECISIONS-SCREENING-16.md) | D090, D091 | A detector's errors are attributed to a cause before any rate is compared, a mechanism is closed on the population that breaks it rather than the one that confirmed it, and a precision figure computed against a positives-only label set is not a precision figure — E072 decomposed 20 misses into 6 from the merchant axis it went in to measure and 14 from an unquestioned amount-CV gate, where five accounts paying the same subscription monthly differ only in whether the price changed; watchlist-scored precision 0.100 against a hand-read stratified 0.91 on the same detections, and Actual Budget's 0.150 is a lower bound on the incumbent, not a benchmark (E072, F185). D091: the recurring-expense detector line is closed — the piecewise-constant repair is strictly better than the CV ceiling on every count but recovers 2 of 14 misses and fails both predeclared gates; a mechanism is closed when its predeclared repair fails its predeclared gates, even when the repair is strictly better (E073, F186) |
| [`DECISIONS-SCREENING-17.md`](DECISIONS-SCREENING-17.md) | D093, D094 | A rate computed against an instrument's own false positives is an upper bound and the gate that reads precision decides the build: E085's G3 returned HOLD at 0.0120 and its G4 returned FAIL at 0.50 against a declared 0.80, so the silent wrong-project line closes on the corrected 0.6% rather than the uncorrected 1.2% (E085, F108); and an instrument's reachable set includes the shapes it structurally cannot see — a `.pth` redirector makes a module importable with nothing in the archive, which the central-directory reader cannot detect and which was half of E085's own findings (E085, F108) |
| [`DECISIONS-SCREENING-18.md`](DECISIONS-SCREENING-18.md) | D098, D099, D102, D103, D104, D105 | A prebuilt module→distribution index over a popular slice of PyPI is not a product, at any K: E090's index over the 15 000 most-downloaded projects resolves 0.3137 of the 1 970 module names real Python repositories import against a declared 0.70 kill gate, the K-curve buys +0.058 for a tripling and is decelerating, and `pip install <module>` plus the index together answer only 0.3893 of real imported names — so the reverse direction retires while the forward mechanism (0.931, E085) and the conditional 0.1877 advantage survive (E090, F111). D099: the incumbent a gate is measured against must be the strongest one the protocol names — E090 named three ways a developer could answer the question and ran one, so its G3 pass is an upper bound, and the missing arm is promoted to the next experiment. D102: the package-name line closes on demand — E091's 2.91% re-reads to 2–4 genuine of 858, under the 1% gate (F113). D103: the Anova venue is closed as a route and "unserved share" is redefined as a property of ownership composition — E091 ran E062's construction on the Anova cooking forum with a passing G0 discrimination gate and measured 5/20 = 0.25 served, but 13 of 20 needs are vendor- or repair-bound and the assistant served 4 of 7 answerable-class rows against 1 of 13 elsewhere (p = 0.0307), so cross-venue unserved-share numbers are not comparable as drawn and future screens must report the ownership mix or screen it out (E091, F114). D104: the appliance-fault-diagnosis line closes for good — E092 ran D103's reopening test on Home Improvement Stack Exchange (`appliances` tag, 707 unanswered questions): 44% of the top-150 by view_count are diagnosis-shaped and 92% of those answerable-class (vs 35% on Anova, p = 4.7e-07), the assistant served the answerable class at 30/37 = 0.81 (Wilson CI95 [0.66, 0.91], lower bound clears the declared 0.50, indistinguishable from E062's 17/20 at p = 0.764), and 0 of 40 resolutions is program-shaped — the need is real and served, so no candidate exists (E092, F115)D105: the view-count domain sweep is stopped and the instrument's published results are withdrawn — E107 drew its need arm from `topic:web-framework` and its random arm from `topic:utils`, both star-sorted, so its δ=0.826010 compares the most-starred web frameworks to the most-starred utility libraries; under a matched harvest on the same platform the effect is within-stratum δ=+0.0746 at stratified p=0.183, and the shared classifier labels only 196 of 700 rows (28%), so the remaining registry passes are `untested` rather than confirmed — the screen is withdrawn, not the idea (E113, F116) |

| [`DECISIONS-SCREENING-19.md`](DECISIONS-SCREENING-19.md) | D106 | A verifier is validated on the population it will be used on, not on the populations that are convenient to build: E114's value-grounding checker passed recall 1.0000 on corrupted answers and 0.0069 false alarms on verbatim spans, then flagged 0.3717 of real values with a false-positive rate of 1.00 - 24 of 24 `ungrounded_value` verdicts have every part present in the document and 50 of 50 hand-read flags are correct. Both controls were too easy; the arm never built is faithful paraphrase with nothing invented. The tool line is closed and the population is served at 0 of 374 fabricated (E114, F118) |

| [`DECISIONS-SCREENING-20.md`](DECISIONS-SCREENING-20.md) | D107, D108, D109 | D107: the CFR applicability-threshold line closes on a served population and the harvest stops: E115 measured 81 threshold spans across 60 sections of title 29, 0.185 of them carrying a counting rule that changes the answer, and a free general assistant answered 14/14 hand-keyed fact patterns with **no clause, no citation and no search** — including 6/6 on the six cases where the counting rule is the whole question, against 0/6 for the plain-headcount reading. Declared gate 0.95 met. **Chosen over harvesting the other 49 CFR titles, because M2b already answered the question the harvest would be extended to answer** (D105's reasoning with the roles reversed). **Standing constraint earned by the fifth consecutive service closure** (E062 17/20, E091 5/20, E092 0.81, E114 0/374, E115 6/6): the next screen must first establish that the answer is *not* already decidable, and the only region left open is a population whose answer cannot be computed from the text plus the facts — the missing input is evidence, not arithmetic (E115, F119). D108: the recurring-payment line closes: the free general assistant is the best reader of standing orders on a real bank extract, and E066's detector has no unserved population. E116 handed 80 real Berka extracts (60 R, 20 C) as `date amount counterparty` rows to three readers. The assistant found **75/75 positive groups (recall 1.0)** and was the most precise — F1 **0.8242** vs detector 0.5769 vs naive 0.4225 (K1, K2 pass). The predeclared "served iff G0∧K1∧K2" is not met because G0_C_precision failed at 0.0, but F122 shows that is a control-population mismatch (C accounts carry non-positive standing orders) that fails every reader identically, not a reader failure. Sixth consecutive served population (E062, E091, E092, E114, E115, E116). F121 records a scorer id-type defect found and fixed during the run | D109: a rate over generated output is withheld until the harness answers three questions -- concordance of key and output identifiers (F121), the false-positive rate on correct output **on the arm the instrument will be pointed at** (F123), and whether the declared negative arm is negative by evidence the key does not use (F122). F118, F121 and F122 each lost a result to a harness defect that raised nothing and turned no declared gate red, and a fourth gate declared by the scorer's own author is what failed three times, so the requirement is a declaration of how the rate was produced rather than another threshold. Implemented in E124's `preflight` package (4 stdlib-only modules, exit 3 withholds the rate, 16 tests including four injected defects); against the committed harnesses it withholds the rate on four of six cases, and measures one verifier's false-positive rate at 0.1970, 0.6667 and 0.9346 on three arms of the same values. |
| [`DECISIONS-PYTESTIVE-SUMMARY.md`](DECISIONS-PYTESTIVE-SUMMARY.md) | — | A session's packaging record for the `pyprovides` prototype: what was built, where each function now lives, and what was measured. Indexed here because it is a record of a decision about this repository's own artifact, not a live plan |

| [`DECISIONS-GATING.md`](DECISIONS-GATING.md) | D024–D026, D030, D036–D039 | How a gate, a diagnostic, or its control must be written before it is trusted |
| [`DECISIONS-RECORDS.md`](DECISIONS-RECORDS.md) | D029, D032, D035, D041, D043, D047 | What this repository's own records must be: a function of the tree, no number with two meanings, and two artefacts held to each other |
| [`DECISIONS-RECORDS-2.md`](DECISIONS-RECORDS-2.md) | D110, D112, D113, D114, D115 | The same, continued: a reader reads every file of a split list, and two allocations of one identifier are a merge's problem, not a reader's; and a service screen reports the strongest alternative's served share **per stratum**, because a pool-level rate read across seven venues as "no unserved population here" was measured on the most-served class of human information need that exists (E168); and "the strongest accessible alternative" must declare whether it can retrieve, because thirteen closures used one that could not, and the baseline's own positive control is what finally proved it (E169) |

**Split a sixth time at 2026-10-05 (T-0063), when D051 took
`DECISIONS-SCREENING.md` to 324 of its 300 permitted lines.** D048–D050 moved
verbatim to `DECISIONS-SCREENING-2.md`. This is the first split in this log that
continues an invariant rather than narrowing one, and both headers say so: the
two files govern *what passes*, which is what
[`DECISIONS-SESSIONS.md`](DECISIONS-SESSIONS.md) could not claim after its own
second split and had to revert. Numbering is continuous and unchanged, so an
existing reference to a decision id still resolves wherever the entry now lives.

**The invariant that makes the split sensible.** A reader who needs to know *why
this mission is shaped this way* reads only the foundation file. A reader who
needs to know *what a session must produce and move* reads only the
practice file. A reader who needs to know *what a command wrote on the agent's
behalf, and what has to be published with it* reads only the publishing file. A
reader who needs to know *what passes* reads only the screening file, and one who
needs to know *how this repository verifies itself* reads only the gating file. No
entry appears in more than one file, and a new decision goes in the file its own
statement fits; never split one decision across the boundary.

The third file was added on 2026-10-04 (T-0054), and the reason is the pattern
this repository keeps meeting: the first split of this log moved entries to make
a file fit and was reversed within the hour. **A decision file has to have an
invariant before it has a line count**, and the one that governed
`DECISIONS-SESSIONS.md` after its second split did not cover the four entries it
held. A gate's reading of the header and the index is what catches that — two of
those entries would have stayed inconsistent with this table and with their own
file's header, and `decisionheader.py` reported both directions before the move.

Split at 2026-10-03 when this file reached the 300-line cap required by
[`docs/policy/doc-standards.md`](docs/policy/doc-standards.md). The entries were
moved verbatim; the numbering is continuous and unchanged, so any existing
reference to a decision id still resolves.

Split again at 2026-10-03 (T-0018) when `DECISIONS-PRACTICE.md` reached 297 of
the 300 permitted lines: D013 and D019–D023 moved verbatim to
`DECISIONS-GATING.md` by invariant, not by date.

**Newest decision:** see the end of
[`DECISIONS-GATING.md`](DECISIONS-GATING.md).

A recorded `decision` event satisfies this gate when **any** decision record
changed; `origin` checks all five files for that reason. See
[`docs/process/session-protocol.md`](docs/process/session-protocol.md).

Split a third time at 2026-10-03 (T-0020) when D024–D027 took
`DECISIONS-GATING.md` past the 300-line cap: D019–D023 moved verbatim to
`DECISIONS-SCREENING.md`. Every split is by invariant, never by date, and numbering
is continuous and unchanged in each, so an existing reference to a decision id
still resolves wherever the entry now lives.

Split a fourth time at 2026-10-04 (T-0030) when D030 reached 289 of
`DECISIONS-GATING.md`'s 300 permitted lines: D013, D027 and D028 moved verbatim to
`DECISIONS-PRACTICE.md`, which now carries D011–D018 and D027–D028. **This index
row is enforced, not descriptive:** the gate added in T-0030 reports a decision
that its own file's row does not list, and a listed id nothing defines. It
reported the gap in the row above on its first run, ten minutes after D030 was
written.

Split a fifth time at 2026-10-04 (T-0042), when `DECISIONS-GATING.md` stood at
297 of the 300 permitted lines and **the next gating decision had nowhere to go**.
D029, D032 and D035 moved verbatim to
[`DECISIONS-RECORDS.md`](DECISIONS-RECORDS.md), and the decision T-0036 had to
leave in code — one entry point for every source of an identifier, and a rule
that cannot read its input reports that — is D036, in the file its own invariant
names. Every split is by invariant, never by date, and numbering is continuous
and unchanged in each, so an existing reference to a decision id still resolves
wherever the entry now lives.

Split attempted and reversed on 2026-10-04 (T-0030). D013, D027 and D028
were moved out to `DECISIONS-PRACTICE.md` because D030 had reached 289 of the 300
permitted lines — and `instance-20260717-0944`, working in the same hour, appended
D031 to that file. Both moves overflowed their destination: this one reached 323
lines, and the other put a fifth session-state decision where no other session-state
decision had ever been. The entries are therefore back where they were, and the
reason is recorded rather than the attempt: **a split is a claim about an
invariant, and the two VMs were claiming incompatible ones in the same hour.** A
file at 289 lines with a real invariant is a smaller problem than two files whose
prose contradicts each other. `DECISIONS-SESSIONS.md` now holds those three
entries and its own header names them, which the rule added in T-0042 checks.

**The index row above is not the only declaration, and for a while it was the
only checked one.** Each decision record also opens with its own
`Decisions **…**` header, and two of the five files had gone stale while this
table stayed correct: `DECISIONS-GATING.md` named D013 — which lives in
`DECISIONS-SESSIONS.md` — and omitted D030, D032 and D035, and
`DECISIONS-PRACTICE.md` named a `D011–D018` range covering three entries that had
moved out. The line under the title is the first thing a reader sees, and it is
now held by `tools/originlib/decisionheader.py` in both directions, so the three
sources of a decision number — heading, index row, header — must all agree.

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Failures and negative results

Disproved ideas, failed implementations, and the lessons worth keeping. An
abandoned option is progress; a silently dropped one is a repeat.

Distinguishing the kind of failure matters, because it determines the next step:

| Statement | Consequence |
|---|---|
| The implementation was wrong | The approach may still work |
| The approach does not work | Do not rebuild it |
| The measurement was inadequate | Unknown; fix the experiment |
| Access or resources blocked it | Unknown; record the blocker precisely |

Recorded findings live in [`FAILURES-findings.md`](FAILURES-findings.md) for
F001-F008, [`FAILURES-findings-2.md`](FAILURES-findings-2.md) for F009-F012,
[`FAILURES-findings-3.md`](FAILURES-findings-3.md) for F013-F017,
[`FAILURES-findings-4.md`](FAILURES-findings-4.md) for F018-F021,
[`FAILURES-findings-5.md`](FAILURES-findings-5.md) for F022-F025,
[`FAILURES-findings-6.md`](FAILURES-findings-6.md) for F026 onward, and
[`FAILURES-findings-8.md`](FAILURES-findings-8.md) (F031),
[`FAILURES-findings-9.md`](FAILURES-findings-9.md) (F029) and
[`FAILURES-findings-10.md`](FAILURES-findings-10.md) (F030) and
[`FAILURES-findings-11.md`](FAILURES-findings-11.md) (F033) and
[`FAILURES-findings-12.md`](FAILURES-findings-12.md) (F034) and
[`FAILURES-findings-13.md`](FAILURES-findings-13.md) (F035, F036) and
[`FAILURES-findings-14.md`](FAILURES-findings-14.md) (F037, F038) and
[`FAILURES-findings-15.md`](FAILURES-findings-15.md) (F039, F040) and
[`FAILURES-findings-16.md`](FAILURES-findings-16.md) (F041) and
[`FAILURES-findings-17.md`](FAILURES-findings-17.md) (F042, F043) and
[`FAILURES-findings-18.md`](FAILURES-findings-18.md) (F044) and
[`FAILURES-findings-20.md`](FAILURES-findings-20.md) (F048, F049, F050) and
[`FAILURES-findings-21.md`](FAILURES-findings-21.md) (F051, F052) and
[`FAILURES-findings-22.md`](FAILURES-findings-22.md) (F053, F054, F055, F056) and
[`FAILURES-findings-23.md`](FAILURES-findings-23.md) (F057, F058) and
[`FAILURES-findings-24.md`](FAILURES-findings-24.md) (F059) and
[`FAILURES-findings-25.md`](FAILURES-findings-25.md) (F060, F061) and
[`FAILURES-findings-26.md`](FAILURES-findings-26.md) (F062, F063, F064) and
[`FAILURES-findings-27.md`](FAILURES-findings-27.md) (F065) and
[`FAILURES-findings-19.md`](FAILURES-findings-19.md) (F045, F046, F047), split because
each file reached the 300-line cap and because both VMs published a part 12 on
2026-10-05; identifiers are stable across the files, so neither was renumbered. **F025 through F028 were taken by the other VM
first**, so this side's findings are F029 onward, renumbered on the unpushed
side per the rule in
[`docs/process/multi-vm-coordination.md`](docs/process/multi-vm-coordination.md):

| Id | Subject |
|---|---|
| F001 | Photo-migration auditor: the motivating example is not evidence |
| F002 | E001 first run: implementation failure, not hypothesis failure |
| F003 | Session 002 under-declared its artifacts; reconciliation caught it |
| F004 | The new directory sweep declared 13 build-output files |
| F005 | Claims were local-only, so two VMs could both own one task |
| F006 | Decision-directed advantage does not transfer to a fieldwork-cost budget |
| F007 | Knitting repair planner: the stated input set is information-insufficient |
| F008 | Adaptive ventilation measurement selection: prescribing one intervention beats choosing it |
| F009 | Knitting repair planner: the algorithmic advantage is prior art |
| F010 | E3's predeclared timestamp gate is near-vacuous: prevalence measured, attribution not |
| F011 | `sync land` broke on git ≥ 2.26, and every CI run failed for that reason |
| F012 | E3's ordering claim holds, and that is why there is nothing to build |
| F013 | Three mission records were committed with conflict markers, and every gate passed |
| F014 | The documented VM sequence was impossible, and refusals printed tracebacks |
| F015 | The local and remote views of a task's holder disagreed after every takeover |
| F016 | A falsification harness overwrote this VM's real `~/.gitconfig` |
| F017 | A generated file's date came from the clock, so the docs gate failed at midnight |
| F018 | A gate asserted a fact about the record, so the suite failed on every interpreter nobody had run |
| F019 | The suite asserted that this machine's git is in the record, so every CI row was red and the log could not be read |
| F020 | The check-run annotations were readable all along; their silence has four causes and three are not "none" |
| F021 | The annotator's rendering was declared unmeasured on a run whose annotating steps never ran |
| F022 | The exemption that answered the wrong question hid every data-file edit from the report |
| F023 | A refusal whose remedy was the one thing an agent must not do by hand |
| F024 | A restated experiment number was false, and the obvious gate cannot see it |
| F025 | The window that made a red run explicable ended one line before the answer |
| F026 | The byproduct thesis is disconfirmed: this mission's own tooling is prior art, and so is its discipline |
| F027 | Every project in this niche has zero users, so "plausible adoption path" cannot discriminate here |
| F028 | The flat adoption tail is vocabulary age, not niche, so "adoption path" is uninformative for young candidates |
| F029 | A live corpus of 1401 unmet needs produced zero candidates that survive the screens |
| F030 | A prior-art verdict from one search query is unreliable in both directions |
| F031 | Measured from outside, the mission was spending its effort on its own record |
| F032 | Stars do not predict installs in any of five niches, so F028's flat tail was never a statement about adoption; and "prior art exists" cannot mean "served" |
| F033 | Full-text issue counts inflated E012's strongest cluster ~200× |
| F034 | The prior-art screen's premise holds in mature vocabularies and largely fails in young ones |
| F035 | "A tool already serves this" is the mission's least reliable verdict, and a third of what it can find lives in a corpus it never read |
| F036 | A web capture can answer HTTP 200 with results unrelated to every query |
| F037 | The screen's young-vocabulary population is real code, so the prior-art premise's failure is not a population artefact |
| F038 | Lead 7's mechanism is implementable and the stock-SDK friction is real, but the missing piece is a feature gap, not a candidate |
| F039 | The need corpus is 1250 individuals with no need-level recurrence detectable inside it, so its 0-of-50 was never interpretable (D051) |
| F040 | F037's "the reader copies the directory" is an instruction rather than an observation: 687 documented copy sites, 4.7% duplicated content, no cross-author overlap |
| F041 | The young vocabulary's copy channel is 0.12x its install channel, so the prior-art screen's young-vocabulary failure is the world and not a channel it failed to read |
| F042 | A repair walk that printed "no new ancestors" 29 times resolved 0 of 434 unreadable comments and exited 0; it never advanced the node, so no chain longer than one hop could close |
| F043 | E022's 38.5% served figure is the ordinary base rate of a Hacker News conversation (0.368 in the same threads), so the trigger vocabulary is invisible to what happens to a need after it is stated |
| F044 | "Twelve candidates, twelve prior-art deaths" is a plurality with a one-row margin (10 of 18 = 0.556) over a population of 20, and 7 of the 18 died of something else — a falsified mechanism, a claim no observation could establish, or a supported mechanism that died of being supported |
| F045 | 22.2% of the 1250 people who publicly stated a need have publicly shipped something, against 27.8% for ordinary commenters in the same stories — so "need-staters are not builders" is false as an absolute, true only comparatively, and E022's disclosure floor is a measurement rather than an excuse |
| F046 | The 589 unanswered needs in the E022 corpus are diffuse in length (55 vs 58 words) and trigger (χ² p ≈ 0.06); B2 fired on two phrases pooling 9 rows, so its hint does not carry a decision — the corpus's last open reading is closed with no hidden structure |
| F047 | 31 of F029's 50 verdicts were assigned from a regex-extracted clause rather than a comment, and 6 of its 15 `vague` kills state a mechanism or an artifact in the text the screen never read; F029's 0-of-50 stands anyway because none of the 8 re-opened rows is a candidate |
| F048 | a prior-art verdict justified by install counts is not evidence of fit: the row with the strongest evidence of use in the record (`sharp`, 437M downloads/month) has documentation that establishes nothing about its clause's attribute, and the instrument built to test fit is refused by its own declared positive control — `not_evaluated`, with the ten sealed-report rows unrun |
| F049 | 167 of the 241 need-staters with a public `Show HN` item shipped it **before** they stated the need, so 69% of the population was never askable and the corpus is substantially people who had already built something; the reader arm that would have quantified the rest returned `not_evaluated` on two counts (κ = 0.5004, C1 separation 0.0405) after three defects in its own instrument, and bounds the need-to-build link at CI95 [−0.0156, +0.1125] — consistent with zero, so F042's 0-of-24 is confirmed on a 10× larger instrument rather than refuted |
| F050 | E030's recurrence statistic fired (difference 0.1338, CI95 [0.0997, 0.1687]) on linkage it printed itself: ordinary English tokens between unrelated comments, arms differing in comment length and cutoff; the permutation null is at chance and the length-matched sign flips to −0.0735. H1 `not_evaluated` a third and final time; A8's held-out separation fires (0.64 vs 0.036), so the population is real and the ruler for recurrence was falsified, C1 never ran |
| F051 | Accounts seeking an alternative state a missing capability at nearly **twice** the rate of ordinary same-story comments (0.347 vs 0.181, CI95 [0.0224, 0.3024], below the declared 0.20 margin) — but the **seek and move strata are identical at 0.347 vs 0.347**, so "unfilled" is not a property the population has and the premise the experiment was built on is retired by measurement. **0 of 100** reader-adjudicated candidate clause pairs and **0 of 100** random pairs state the same requirement, with A3 (κ = 0.7189), A4 (0/24), A5 (0.486) and A6 (20/20 positives, 0/10 negatives) all passing, and length matching moving the arm difference 0.1667 → 0.1698 — **not** a length artifact as in F050. A fourth demand-side generator closes, on its own premise rather than on prior art; its declared linkage rule could not fire at all (4 candidate pairs against a chance expectation of 4.9), the mirror image of F010 |
| F052 | The gate carrying F031's allocation finding asserted `ratio > 1.0` with the message "machinery should outweigh experiment code" — and **F031's own measured ratio was 4.8 : 1**, which passes it. The gate written to detect machinery dominating the work was satisfied *by* machinery dominating the work, nearly five times over, and it went red on 2026-10-06 only because a session added experiment code (1,535 lines against 4). Repaired to a **ceiling of 3.0 : 1**, below the recorded complaint, with `RatioCeilingTest` falsifying it in both directions; **a passing gate here is not evidence about allocation** |
| F053 | The sentence "a cross-author recurring requirement will not be found by mining public conversations — three populations, three instruments, three zeros" rests on **3,856 distinct Hacker News comment ids and one venue**: E019, E022, E026 and E029 all re-read E012's single 1401-comment file at **100% identifier overlap**, and E030's 2457-comment harvest shares **2** ids with it. Two corpora, one venue, five readings; the vocabulary claim (the zero survives a change of trigger phrase) is sound and is the stronger half, but the venue was never varied. F051's own ceilings say so — the summary sentence is what over-reaches, and it is the sentence item 0d closes the invention seat on |

| F054 | **E032 changed the venue and nothing else** — 60 long-form questions from three non-programming Stack Exchange sites, 53 authors, selected by date/site/length with **no requirement vocabulary**, against E031's own linkage rule, control and four gates. **0 of 32** candidate pairs and **0 of 60** control pairs state the same requirement, difference **0.0000 CI95 [−0.0602, +0.1072]**, with **A2 reachable** (32 candidates vs 1.19 chance), **κ = 0.8344**, **0/24** nonsense, **20/20** positives and **0/10** negatives. So the zero is **not** Hacker News's length, self-containedness, population or selection — it holds across two structurally different venue classes. It is a **bound, not a zero**: the upper bound is **0.0894** here, **0.0223** pooled with E031's 100. The run's own two instrument defects (reading sheets instead of labels, which made κ undefined; and a key file out of order with its sheet) were caught by running the step, not by a reader's account. **F055 measures the population F054 drew from and shows `sort=votes` selected the tertile where recurrence is 4.5× rarest** |
| F055 | **The pooled 0.0223 bound is refuted, and E032's population was drawn where recurrence is rarest.** Reading recurrence off Stack Exchange's own `closed_reason == "Duplicate"` judgement instead of a linkage rule this mission invented, over 1000 questions from two volume-selected sites: **54 duplicates = 0.0540, CI95 [0.0416, 0.0698]**, `travel` 0.0660 and `math` 0.0420 — and the label counts only closures, so the true rate is higher. The sample was the problem: **the top 60 by score contains 0** duplicate closures against a mean of 3.37 over all 941 sliding windows, and the rate runs **0.0180 in the top score tertile against 0.0808 in the bottom**, a 4.5× gradient that E032 declared as a caveat and that is in fact load-bearing. `sort=votes` was chosen because elaborated needs live there, and it selects for answered questions — the ones that were not repeats. A second claim was **withdrawn by the run itself**: the same data read as convergent-and-unanswered demand (0.5556 against 0.2114) but zero of the 54 duplicates has an accepted answer, and closing a question as a duplicate does not answer it. **This explains E032 and only E032** — the Hacker News zeros have F039's own separate cause, 1250 individuals each asking once. No candidate is revived: no clause or cluster was recovered and no prior-art screen was run. The constraint that follows is about the archive — **a duplicate closure is a reliable label and an unreachable edge**, since neither `closed_details` nor `question_type` is exposed and the four vectorised `{ids}` routes tried all return `no_method`, so `tally.py` declines to print the declared visibility product rather than compute it from canonicals the reader arm rejected (6 of 24) |
**F048's evidence lives at `EXPERIMENTS/028-incumbent-fit/`:**
| F056 | **A gate asserting that world-facing commits are a minority of a day's commits failed the most world-facing day in the record.** `test_allocation_measurement` asserted, for *every* day in history, that world-facing work is under 50%, and E033 made 2026-10-06 exactly 50.0% (7 of 14). Two faults, both already named elsewhere in the record: the per-day share is a property of the **calendar** (F018/F019/F022 — the same file had scoped the adjacent assertion for that reason and left this loop unscoped), and the **direction** is the mission's habit rather than its goal (F052's recorded mistake: a ceiling on real measurement fires when it rises). Replaced by a **floor of 5%** in `tests/test_allocation_world_share.py`, falsified against F031's own shape and against the live day. **The failure still told the truth about half of it**: 5 prose records and 1 machinery line against 7 world-facing commits is F031's pattern at small scale, and E033 is world-facing work that cost a quarter of its commits to recording |
| F057 | **E034's per-tag spread is real, reproduces out of sample at both extremes, and cannot be attributed; its mechanism claim cannot be measured at all.** Pooled duplicate-closure rate is **0.1352 in the score tail against 0.0303 in the `Active` tab** — 4.5×, replicating F055 on an independent tag-stratified population — and per-tag rates run **0.0000 to 0.4300** with 12 disjoint interval pairs and both extremes reproducing on the next four pages (`customs` 0.430→0.495, `excel-formula` 0.000→0.000). Three declared claims did not survive the run. **D6:** duplicate closure is a *moderator act*, and with one `travel` tag against five `stackoverflow` ones the highest cell was the only one from its site; after AMENDMENT-1 added `travel`/`baggage` (0.1979) and `math`/`calculus` (0.1020), within-site disjoint pairs run 4/10 against 14/26 cross-site, so **site and tag both carry real variance and 3–5 tags per site cannot apportion them** — the per-tag reading, which is the whole proposed tool, is **not established even though its kill gate fired**. **B1:** among duplicates, the share with no accepted answer is 0.8163 in the tail against 0.7273 in the Active tab, difference **CI95 [−0.0774, +0.3075]** — *"the answer existed and was not found"* cannot be separated from *"a moderator closed it"*. **The a-priori stratum hypothesis is backwards**: `excel-formula`, the situational exemplar, has the *lowest* rate of all ten tags at 0/100. Also: the **declared R2 gate was ill-formed before the fetch** — it demanded a relation be disjoint from "both" comparators and the data returned one of each, so both branches could fire, which is D062's rule applied one level up to a *decision rule over candidate pairs*. Two facts outlive the run: the **canonical edge is unreachable** from this host through **nine** named channels (adding the question's own comments, the answer's `closed_details`, a browser User-Agent, and SEDE to E033's five), so the label is available and the edge is not; and **the label is a set of eleven literals**, with `exact duplicate` (9 rows) the legacy spelling of `Duplicate` (222), so **E033's 0.0540 and every rate derived from it is a floor**. What is established is **where the repeats sit, not what happened to them** — the first demand-side instrument in this record to return positives at all |
gates including a `not_evaluated` state, and two controls **before any label and
before any fetch**; two amendments, each written before the pass it bounds, fix
what the base protocol left undefined (row-level bundle semantics, the fetch
table, the 4-artifact and 1,800-character bounds, and the reader barrier that
makes "derived from the requirement alone" checkable from the repository).
`raw/requirements.jsonl` is the blind file — a test asserts it carries no
`cause`, `reason`, `verdict`, `artifacts` or `note`, and another asserts Step A
names no incumbent the screen named for that row. `RUBRIC.md` defines every
label and a test asserts it names no row. **C1 passed at 0.0 on all 32 foreign
bundles; C2, the declared positive control, failed with both readers returning
`partial` on `H03`; κ = 0.5625 against a declared floor of 0.6.** The verdict is
`not_evaluated` and neither A3 nor B1 is read as an answer.
`test_gates_falsified.py` holds 29 properties against the committed bytes,
including the Wilson interval for 0/24 equalling the `[0.0, 0.138]` the record
quotes for F042, and it caught **three defects in this run's own instrument** —
zero-byte captures from 200 responses that strip to nothing, a contamination test
banning a word the requirement itself used, and bundles that could show a product
with no documentation.
| F060 | **`git add -p` is not unreachable from a program; it is unreachable *by line number*, and a wrong answer exits 0.** E037, `EXPERIMENTS/037-line-staging/`, T-0081. Corrects the D067 probe's own reading, F020's shape again: piped keys **are** read — the run truncates at EOF and **exits 0** — and a purpose-written pty driver reaches **4 of 6** cases for **133 lines** of caller code. The real gap is the coordinate: **`s` splits only at context boundaries**, so two adjacent modified lines are one change pair named after its first line, and line 2 is reachable only through the `e` editor that opens a patch in `$EDITOR`; a deletion is named one line before where its content was. `stg` is **6 of 6**, stable at `diff.context` 1 and 3, and on a real file in this repository leaves a **byte-identical `.git/index`** to a hand-built patch. Not established: that the incumbent route is impossible, that a better driver cannot reach 6 of 6, or that anyone wants this — and **web search was unavailable on this host**, so 'no prior art' rests on git's documentation and behaviour rather than a search |
| F061 | **The need corpus's own generator was answered inside the corpus.** All **589** never-answered statements read in full, **557 distinct authors**, median one each. Comment `46891298`, unprompted: *"Instead of saying 'gosh I wish there was an app that…' I just make the app and use it and move on"* — F049 from the other side, and the sixth generator question to close. The first theme count on this corpus not built to support a prior conclusion: finding the right existing thing **70**, AI-tool transparency **58**, non-interactive or scriptable operation **50**, local-first/offline **43**, cannot-turn-off **17**, git specifically **11**, selective/partial **10**. Lexical, overlapping, and 330 of the 589 match a trigger that is a **wish** rather than a specification — a description of the corpus, **not** a demand estimate |
| F062 | **E037's 'not prior art as an interface' rested on git's own documentation, and two tools answer it.** With a search surface, `filterdiff --lines=RANGE` (12 of 30 measured) and VS Code's `git.stageSelectedRanges` both take the coordinate E037 claimed was missing; VS Code's `staging.ts:124` even carries the same line-pairing heuristic as `stg`. What survives is narrower: no *command-line* tool takes `file:line`, splits adjacent changes, and exits non-zero when it staged something else |
| F063 | **An oracle that reads hunk anchors cannot see an over-staging bug, and one test asserted the bug as intended behaviour.** `stg` was 6 of 6 on anchors, silently wrong on two of the six — it staged two lines when asked for one, scored as correct. Against the index content: **`stg` 30 of 30, `filterdiff` 12 of 30, `pty_driver` 12 of 30, `naive` 6 of 30**, 78 wrong-but-exit-0 rows across the three alternatives and none for `stg`, 30 tests green. E037's 6 of 6 is withdrawn; the candidate stands, narrower |
| F064 | **A keyword classifier's 100-of-195 was 2-of-30, and two readers disagree exactly where the claim lives.** Hand-labelled twice on 61 mechanically sampled rows: precision 0.067 and 0.033 (κ = 0.734 three-way, 0.889 collapsed, `yes-line` Jaccard 0.25). The population's existence is agreed, its size is not: **0.016–0.066** of matching issues, 16 to 66 per thousand. One row, `mcp-multi-root-git#3`, states the agent case in the agent's own terms. **Prevalence is not established** |
| F065 | **A correctness oracle never ran the caller the candidate is for.** E037–E039 proved `stg` against anchors and exit codes; E040 put the agent caller from `mcp-multi-root-git#3` in the loop: **stg 5 of 5 exact and honest, one call, 10–33 bytes**; a ~40-line hand-written plumbing route **silently over-staged in 2 of 5** (exit 0, wrong index — git coalesces adjacent edits into one hunk, so the split is unrecoverable from `git diff`); `filterdiff` **exact 2 of 5**, opaque 128 on 2, silent over-stage on 1. D070 follows, and the artifact's own stale README bullet (a two-line insertion does not split) was found by the same run and corrected |
| F059 | **The score-tail worklist is one unauthenticated URL, and F058's reachability claim was a fact about one rendered view.** `EXPERIMENTS/036-search-backlog/`, T-0080, 8 requests, **KILL-R met**. One request to `/search/advanced?site=stackoverflow&tagged=git&sort=votes&order=asc&pagesize=100` returns **100 questions ascending by score (−20..−5, non-decreasing), 81 of them ids already in E034's committed harvest** (first at rank 1), and **13 labelled `Duplicate`/`exact duplicate` in the payload's own `closed_reason` field** — no API key, no custom filter, no second route, no computation. E035's stated differentiator was *"the platform's own closure label over a population no surface orders that way"*; **both halves are the platform's.** Three corrections: F058's *"no surface offers the ordering"* was established on a tag page's seven tabs and did not enumerate the filter vocabulary (`sort`, `order`, `tagged`, `closed`, `votes`, …) — **D066**; `closed` is the one filter value this route **does not validate** (`closed=maybe` → 200, same items), so no closed-only control was establishable from the route's behaviour, while `order` and `filter` both return 400 on invalid values; and E035's *"the label needs an API key"* generalised two routes (`/questions/unanswered`, `/questions/{ids}`) to the platform — **F020's shape** — and removed the key premise a tool would have rested on. Retrieval arms, thin: tail titles **3/4** recovered (ranks 1, 7, 1), `Active` control **2/2** (both rank 1), positive control fired on real positive examples, **KILL-Q `not_evaluated`** at n=4 and **R4 negative control `not_evaluated`** on the quota wall. The run also failed twice in its own plumbing — a stage argument fell through to a 9-request plan against a 4-request budget, and `quota_wall()` discarded successful 200s reporting negative quota — **both in the raw bytes, neither load-bearing on the kill**, which is an id-intersection against committed evidence. **The population is untouched**; what died is the claim that it is unreachable. **The adoption question is now the whole question and has never been measured in three experiments** |
| F058 | **The score-tail population is not one that was overlooked, no Stack Overflow page orders it the way it was measured, and the mission's top-ranked next action was aimed at the wrong constraint.** Four results over E034's committed bytes at zero quota cost. **The findability frame is falsified:** within E034's tail arm the duplicate-closed rows have a **higher** median view count than their non-duplicate neighbours (**251 against 193**), and the arm's median age is **8.49 yr** against the `Active` tab's 5.53 -- these questions have been read ~200 times each, so this is an eight-year-old backlog, not a rescue. **The `Active` and `tail` arms do not intersect** for two of eight tags (`stackoverflow`/`python` tail -34..-11 against Active -9..304; `math`/`probability` -9..-4 against -2..159), so a 4.5x gradient is a statement about *membership*. **No *rendered tag page* offers the ordering (corrected by F059, which found the API route does):** 409,639 bytes of first-party rendered HTML from a 2026-09-26 archive snapshot of a real tag page list `Newest / Active / Votes / Frequent / Trending / Bounties / Unanswered` and contain **0 occurrences** of `oldest`, `order=asc`, `sort=votes&order=asc` or `ascending`; the direction of `tab=Votes` is `not_measured` because the archive refused that snapshot. **D6's declared remedy (3-4 more tags per site, ~30 requests, ranked the mission's top action) is largely already answered by the committed bytes:** between-tag excess variance on the arcsine scale reads **+0.0417 pooled and +0.0420 within `stackoverflow` alone** -- the four SO tags run 0.000/0.130/0.150/0.210 and their spread inside one site *equals* the whole spread. The obvious objection to a rank-selected tail is **unsupported** (r=+0.2485, t=0.725, df=8). **E035's own gates:** U1 fired at a median Jaccard of **0.0283** but **D065** shows the overlap was definitional -- `/questions/unanswered` returns **open** questions and holds **0** of E034's 224 known duplicate-closed ids while **98 of 186** tail duplicates meet its advertised `is_answered == false` criterion -- and **U2 is `not_evaluated`** because the label is unreadable *on that route* (six filter forms, custom filters refused unauthenticated, `/questions/{ids}` also omits it; an API key is required — **F059 shows `/search/advanced`'s default filter carries it without a key, so this is a per-route fact and not a platform one**) |

`PROTOCOL.md` declares the population, the category/attribute distinction, four

**F043's evidence lives at `EXPERIMENTS/023-served-baseline/`:** `PROTOCOL.md`
holds the declaration, `raw/labels.tsv` carries one note per row from a reader
blind to E022's, and `results.json` the four gates. It **withdraws the inference**
that a reply naming an artifact is evidence the need was served, and leaves
E022's other two numbers standing — 58.0% answered, and 0 of 24 unserved
requesters who built it themselves. Label agreement between the two readers on
the identical 39 rows is κ = 0.9226, so the null is a property of the population.

**F044's evidence lives at `EXPERIMENTS/024-kill-reason-causes/`:** `PROTOCOL.md`
declares the population, the four categories and both gates before any row is
read; `CONTROL.md` records the declared control failing as constructed, the
discarded 19/19 repair, and the replacement control's disclosure;
`results.json` carries the counts and the sensitivity analysis. It **falsifies no
prior-art verdict and reopens no candidate** — it measures what candidates were
killed *by*. Its binding limit is **one reader, no second coder**, the same defect
E023 fixed with κ = 0.923, and at a one-row margin the second reader is the
measurement that would settle whether the record's sentence is a fact or a
coin-flip.

**F045's evidence lives at `EXPERIMENTS/025-need-staters-builderhood/`:**
`PROTOCOL.md` declares the question, the two-world framing, all four gates and
the control arm's stopping rule **before any figure existed** — including a
correction entry written while `control_arm.jsonl` still did not exist, so the
stopping rule could not have been tuned on the control rate.
`test_gates_falsified.py` holds 15 properties against fixtures built to break
them, including **that the two failed Gate A1 controls stay recorded as
empty**. It **confirms item 0d's closure rather than withdrawing it**, and
bounds F042's third cell without repairing it. Its binding limit is inherited
rather than lifted: the `show_hn` tag is set by HN, so **an unannounced build is
invisible in both arms**, and within the control arm the tag tracks overall HN
activity hard (median 2416 items for builders against 467 for non-builders).

**F042's evidence lives at `EXPERIMENTS/022-need-outcomes/`,** and the defect
itself is in `need_depth_walk.py`. The reported result did not move across the
repair (odds ratio 0.701 before, 0.703 after), because the two strata the arm
uses were never affected — which could only be known after the repair.
`tests/test_need_depth_gate.py` holds the defective loop shape as a failing
assertion and reads the committed capture rather than the walk's exit code.

**F041's evidence lives at `EXPERIMENTS/021-copied-artifact-serving/`,** not at
the `020-` path some records still name: the other VM took `020-copied-config-drift`
and F040/D052 for a different experiment on the same reading, and this side
renumbered on the unpushed side per the multi-VM rule. `PROTOCOL.md` holds the
declaration, `results.json` the verdict and the lost capture, and `raw/` the 95
instrument captures.


**The invariant that makes the split sensible.** A finding is only useful if a
reader can tell a disproved claim from a still-open question, so the findings
are separated from the live list rather than interleaved with it. The files
split by line cap, not by subject: `FAILURES-findings.md` holds F001–F008,
`FAILURES-findings-2.md` takes F009–F012, `FAILURES-findings-3.md` takes F013 to
F017, `FAILURES-findings-4.md` F018–F021, and every finding after it goes in
`FAILURES-findings-5.md`. Identifiers are stable: a reference to `F013` means the
same entry whichever file it is in.

**Identifiers are allocated from each VM's own tree, so two VMs in an hour
collide by construction.** Six times on 2026-10-03, and the cost is now measured
rather than predicted: resolving a rebase restored one file's *index* row to the
renumbered form while reverting its *body* to the old identifiers, so a findings
file and its own table briefly disagreed about the same two entries — the exact
failure this paragraph exists to prevent, caught only because both were read
together before landing. Nothing in the tooling prevents a collision;
`STATE.md` records it as unfixed.

## Open, not yet disproved

These remain live questions, not settled negatives:

- **Knitting repair planning** (`RESEARCH/C.md`): graph representation is prior
  art and so is the algorithmic core (F009). What is untested is whether a
  knitter follows a generated plan and saves real work — Stage B, unperformable
  in this repository. Stage A is settled mechanically (T-0010, T-0011).
- **Adaptive ventilation measurement selection** (`RESEARCH/C.md`): stopped as
  formulated (F008). NVAPF and NIST tools occupy uncertainty-aware estimation;
  the surviving reading-a-second-sensor robustness observation is untested
  against existing tools and may belong inside them.
- **Sidewalk survey prioritisation** (`RESEARCH/A.md`): strong value story,
  substantial prior art; the decision-value advantage is falsified in its
  motivating cost regime (F006) but not in every regime.
- **Reproducible Python builds** (`RESEARCH/E.md`, E3): the mechanism is
  supported and the candidate abandoned (F012) — for the one builder available
  here, timestamps are the only byte-level cause and `SOURCE_DATE_EPOCH` removes
  all of it. Still open, and not a new repository: the census's per-package
  heterogeneity, which this run does not explain, and whether compiled-extension
  builds behave the same way. E1 (retry jitter) and E2 (lockfile drift) remain
  `untested`; D020 rules E1 out of order.

## Reopening

A failed idea returns when the specific evidence that killed it is invalidated —
not because effort was previously spent on it. Record that evidence here so the
next session finds it in one search.

**F047's evidence lives at `EXPERIMENTS/027-cause-of-death-reread/`:**
`PROTOCOL.md` declares the population rule, the six categories, both readers
and all three gates **before any row was classified**. `raw/population.jsonl`
is the blind file — `population.py --selftest` asserts it carries no `cause`,
`reason` or `name` field, so no classifier was handed the answer.
`raw/reader_r.jsonl` was committed **before** reader S existed;
`raw/reader_s.jsonl` is a second reader blind to the original verdict and to R.
`stats.py` reproduces every number in `results.json`, and
`recheck.py --selftest` shows C1 and B1 failing and firing against fabricated
populations in both directions. **The declared agreement gate failed (κ 0.4627
against a floor of 0.6) and the per-row kill gate fired on 8 of 31**; both are
reported, and the post-hoc binary κ of 0.5412 is labelled structure and used in
no verdict (D059).

**F046's evidence lives at `EXPERIMENTS/026-unserved-need-structure/`:**
the protocol fixed both hypotheses and all three gates **before the first text
fetch**; `raw/texts.jsonl` holds all 1401 comment texts (100%, A1 passes);
`stats.py` reproduces the numbers in `results.json`, including the chi-square
sensitivity that withdraws the B2 claim. The declared gate fired and its
firing is the record: **the gate fired before its sensitivity was run, and the
sensitivity is what a firing gate is owed** (D058).

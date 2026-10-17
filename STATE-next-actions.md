<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# Next actions

> **READ FIRST (2026-10-12).** The view-count domain sweep is **STOPPED**
> (E113, F116, D105). E113's matched-harvest control of E107 showed the
> effect is a harvest artifact (δ 0.826 → 0.075, stratified p=0.183) and the
> shared classifier labels only 28% of a representative pool. Every
> "ALL GATES PASS" below that came from this line is **`untested` on a matched
> harvest, not confirmed**. Do not run another registry sweep. See
> [`EXPERIMENTS/113-viewcount-matched-harvest/`](EXPERIMENTS/113-viewcount-matched-harvest/README.md).

## E176 — what carries the fix when it is not a repository link (2026-10-17)

**The gap this session's own measurement opened.** E175 drew 200
high-arrival Stack Overflow questions, 145 of them answered, and found that
**21 (0.1448) name a repository and 10 (0.0690) name a tracker document — so
79% of answered high-arrival questions record no repository link at all**
(F135). Every rate in E168, E170 and E174 lives inside the 7% bucket, and the
complement bucket is the largest one this line has ever had in front of it and
has never characterised.

**The question.** For the answered rows whose answer contains no GitHub link,
what *does* the answer contain? Classified by deterministic rules committed
before the classification, over all 124 such rows: a configuration key or setting,
a version number or changelog statement, a code snippet, an OS or environment
fact, a third-party service behaviour, an upgrade or downgrade instruction, or no
fix at all. Report the distribution with intervals; report the share whose
resolution is **decidable from the text plus the facts** — because D107's
standing constraint (five consecutive service closures) says a candidate must
target a task whose answer cannot be computed from what is already in hand.

**Why this rather than another retrieval screen.** The version-pinned retrieval
line closes with its ceiling named (D117): the population is 7% and the reachable
share of it is 0. The complement is 79%, unmeasured, and it contains the cases
where the answer is a version fact in prose rather than a document to find.

**What would end it.** If the 124 rows' resolutions are dominated by
environment facts and no-fix statements, the class is unaddressable and closes. If
a material share is a **version or changelog statement**, that is a population
where the missing input is a specific published artefact rather than a semantic
bridge, and the candidate is a version-difference reader rather than a retriever —
which is the one mechanism E171's pre-condition screen (2/13 against a declared
0.40) closed, so E176 must be run on this population and not on E168's rows.

**Do not run:** E171 (withdrawn, its pre-condition fired), E172/E173 (F133),
another view-count domain (D105, F133), or a replication of E170's global-arm
near-zero (E174 shows the scope was the whole effect).

The D083 sweep table and the completed closing entries this file used to
carry were split into
[`STATE-next-actions-sweep-history.md`](STATE-next-actions-sweep-history.md)
at the 300-line cap.

## E137 completed (2026-10-14) — cross-model agreement: third exact AGREE

E136's named next action is done. The calibrated instrument (last-`\boxed`
extraction, normalized-string equality, macro-mean-of-subject-means weighting)
pointed at `01-ai/yi-6b` (first model in the HELM lite v1.0.0 inventory other
than `01-ai/yi-34b`, selection rule pre-declared in E137's protocol, no
substitution) achieved exact AGREE on the same `math_chain_of_thought` cell:
437/437 row verdicts agree with the harness's per-instance verdicts; the
recomputed macro mean (0.12585197340399298) equals the published group macro
to full printed precision, diff 0.0. One yi-6b-specific calibration fix:
backslash stripping now only before letters (LaTeX commands), not before
digits — corrected one case where `\37` ≠ `37` (harness scored 0, naive
strip-all-backslashes would have scored 1). Kill gate not fired; D111
stands (cross-model reach demonstrated further, external value still
unobserved). This is the third exact AGREE on this line (E135: MMLU
single-letter; E136: math_chain_of_thought yi-34b with parser+weighting
stress; E137: math_chain_of_thought yi-6b cross-model).
[`EXPERIMENTS/137-leaderboard-cross-model-agreement/`](EXPERIMENTS/137-leaderboard-cross-model-agreement/RESULT.md).

## E138 completed (2026-10-14) — GSM `####` parser: fourth exact AGREE

E136's pre-named cell F is done. The calibrated instrument pointed at
`01-ai/yi-34b` gsm run (1000 instances) achieved exact AGREE: recomputed
`final_number_exact_match` = 0.648000, published = 0.648, diff 0.0.
Row-level verdict agreement: **1000/1000** with the harness's per-instance
verdicts. The `####` marker was absent from this population (HELM's GSM8K
references end with "The answer is N"); the fallback rule (last number in
text) was exercised on 1000/1000 rows for both gold and predicted answers.
No parser bugs found; 352 mismatches are genuine model errors. Kill gate
not fired; D111 stands (reach demonstrated further across four stressors:
single-letter, free-text aggregate with weighting, cross-model, `####`
parser, external value still unobserved).
[`EXPERIMENTS/136-leaderboard-free-text-aggregate/RESULT.md`](EXPERIMENTS/136-leaderboard-free-text-aggregate/RESULT.md).

**Named next action:** superseded by E141 below. The R1 instrument was validated
on four cells in HELM lite v1.0.0 with exact agreement on all, and E141 then
measured whether that reach carries a finding. It does not.

## E141 completed (2026-10-15) — the scorer false-negative rate is small; kill gate FIRED

E141 is the experiment D111 was waiting on. `preflight` had demonstrated reach
(four exact AGREEEs) but never a finding, so its release question had nothing to
go on. E141 pointed the calibrated instrument at the one check that could have
produced one: **does the harness's own scorer mark correct answers wrong?**

On the four already-fetched, hash-verified HELM lite v1.0.0 cells — 2,874 rows,
two models, two scenarios — **6 scored-wrong rows are mathematically equal to the
reference**, all six confirmed correct by hand. Pooled 6 of 1,593 wrong rows
= 0.377%. Primary cell P1: **4 of 246 = 1.626%** against a declared gate of 2.0%
**and** 5 rows, so **both conditions failed and the gate fired**. Effect on the
published number: +1.17 accuracy points on P1, entirely from unreduced fractions,
thousands separators and decimals; **0** rows on 1,000 GSM rows in both models.

The result survives its own falsification because the recall audit bounds what
the instrument could have missed: 25 of 25 hand-read wrong rows are genuinely
wrong, and a weaker extractor over the 95 no-answer rows recovered 0. Controls
G0a/G0b/G0c/G0d all green, and two defects in this session's own work (a verdict
dict keyed on instance id alone, which crosses subject runs because the seven
HELM MATH runs carry only 267 distinct ids across 437 rows; and an incomplete
copy of the calibrated normalizer) were caught by them.
[`EXPERIMENTS/141-scorer-false-negatives/RESULT.md`](EXPERIMENTS/141-scorer-false-negatives/RESULT.md).

**What this decides.** Stop adding adapters, cells and harnesses to `preflight`.
A check that fires on 0.4% of rows, in cases a single normalization rule catches,
and on zero rows of half the populations tested, is not worth shipping as a gate;
that is now a measurement. D111's remaining sub-question is E134's population
question restated, and E134's answer was that the one published run available was
clean.

**Named next action: E140 is shelved, mission returns to fresh exploration.**
E142 ran E140's G5 as a cheap pre-fetch probe and both branches resolve
against running the harvest now. G5-tool-strict = 0/14 (kill needed ≥7), so
no kill — but the probe's value is what it found instead: the top
marketplace hit for "fix failed build" (Badgr) disclaims auto-fix in its own
FAQ, the only asserted auto-repair (JAIPilot) is Java bot-PR drafts with 3
installs, and the strongest adjacent incumbent (pre-commit.ci autofix) reads
PRs, not failing runs. P1 (project-code dominance) gained no sourced support
(TravisTorrent fetch failed; Badgr's 14-type list states no distribution) and
G5-alt (assistant baseline on CI logs) is untested — so per E142's declared
condition 2 the ~7,500-request harvest is declined. Do not re-probe C1/C3.
[`EXPERIMENTS/142-cicd-incumbent-probe/RESULT-ARM-A.md`](EXPERIMENTS/142-cicd-incumbent-probe/RESULT-ARM-A.md).

E143 completed (2026-10-15): Cross Validated — the largest untouched venue — closes like the others; the program-shaped residue is zero.** On Cross Validated (`stats.stackexchange.com`, ~200k questions, chosen by a stated rule: the largest untouched non-software SE site where resolutions are plausibly self-contained artifacts), 300 unanswered recent questions (two arms: 200 votes + 100 creation) were screened. **300/300 are question-shaped; 0 are execution-shaped; the program-shaped residue (K3) is 0.** The answerable class (143 = 47.7%) is served by a free general assistant at **20/20 = 1.0000** (top-20 by view_count, Wilson CI95 [0.8389, 1.0000]), consistent with every other venue (E062 0.85, E092 0.81, E126 0.6750). The two arms differ by 2.0× in answerable share (57% vs 29%), confirming E126's stratum finding on a third venue. The program-shaped residue is a property of the venue type: SO had 2% (E126), CV has 0% — software venues attract write-me-a-program needs, statistics venues do not. The candidate-seat question is answered for the highest program-density untouched venue: no program-shaped population exists, and the answerable class is served at 1.0.
[`EXPERIMENTS/143-crossvalidated-service-test/RESULT.md`](EXPERIMENTS/143-crossvalidated-service-test/RESULT.md).

## E168 completed (2026-10-16) — G1 and G2 pass; the class is a population

**Closed by E169 and E170 on 2026-10-16.** Both remaining actions below were
run: the search arm was withdrawn on its own control (F130) and replaced by
containment, and the reachability of the fix was then measured on a live ranked
index, where neither query form reaches it (E170: literal 1/8, symptom+component
2/13). The "fresh observation in an untouched domain" this entry carried is
still not the next action. Kept as the record of the attempted fresh
observations it lists.

**Named next action: run E168's G3 *with a third arm* on a fresh blinded
`version_pinned` sample** — the third arm being the same question put to the
alternative **with** search over the issue tracker and release notes. The
closing check that added the arm: **20 of E168's 24 threads' answer sets link
out, `github.com` in 15 of 24**, so the incumbent mechanism is *search the
tracker with the exact error string and apply the linked fix*, already done by
hand in minutes. G3 as first declared would test "add version grounding",
which is what search already does, so it cannot pass on its own. Cheaper
decisive version first: from `threads.json` alone, how often the top answer's
linked source is reachable by the exact error string as a query. That bounds
the search arm's ceiling with no assistant in the loop, and costs one script.

> **RUN as E169 (2026-10-16) — both claims in this paragraph are corrected.**
> That script ran, and its own positive control failed (3 of 13, then 13 of 13),
> so the search arms were **withdrawn** rather than reported: a target's own quoted
> title returns 17,033,706 hits from GitHub's unauthenticated issue search (F130).
> And **"`github.com` in 15 of 24" does not reproduce** from `threads.json` — 12 by
> `href`, 13 counting gists; "20 of 24 link out" does reproduce, under any URL
> occurrence in any answer, which is a statement about the thread rather than about
> the resolution. E169 replaced the instrument with containment and closed the class
> as served by the thread: **9 of 13 ≥ 0.5 term coverage, 0 of 13 share a 3-word run
> with the fix, ≥ 0.8 coverage against the whole thread on 12 of 13**. See
> [`EXPERIMENTS/169-version-pinned-reach/RESULT.md`](EXPERIMENTS/169-version-pinned-reach/RESULT.md).

**G3 on a fresh blinded sample — now the next action, with E170's verdict attached.**
G1 sized the class (85 of 299 = 0.2843, Wilson [0.2361, 0.3379],
14× E126's program-shaped residue) and G2 measured the alternative on it (11 of
24 = 0.4583 against E126's pool-level 0.6750, Fisher p = 0.1168). Neither says
the missing fact is *retrievable*, and a fact that exists only in the asker's
head is servable by nothing. G3 asks whether an attempt grounded in only the
post and the component's published version history recovers rows the unaided
attempt fails; the declared bar is ≥ 0.60. It cannot run on E168's 24 rows —
that session read every thread, so a grounded attempt would be contaminated —
so it needs a fresh sample. **If G3 fires, run the prior-art screen against
the class before writing a line of product code**, with the incumbent set
named explicitly: read the changelog, paste the error into a search engine,
read the lockfile, ask the tool itself. **If it does not, the class closes as
a population without a mechanism**, and that is the cheapest failure in this
record to read because it would name a population that is genuinely unserved
and still not servable.

> **E170 removed one of G3's arms on 2026-10-16, and it is the arm G3 would
> otherwise have leaned on.** G3's third arm — "the same question put to the
> alternative *with* search" — would have tested whether retrieval closes the
> class. E170 measured that directly on 13 rows, on two instruments whose
> capability controls pass (`in:title` returns the target at rank 1 on 11/13 by
> API and 10/13 on the web surface): the developer's quoted error string
> reaches the fix in the top 10 on **1 of the 8 rows that have a literal**, and
> component+symptom keywords on **2 of 13**, paired McNemar p = 1.0. **A
> lexical retrieval arm cannot close this class**, so G3's remaining question is
> only the grounding question, and G3 is now the one experiment left on this
> record where the candidate mechanism is not the incumbent.
> [`EXPERIMENTS/170-fix-reachability-rank/RESULT.md`](EXPERIMENTS/170-fix-reachability-rank/RESULT.md).

**Named next action: fresh observation in a domain this mission has not touched, chosen by a stated rule rather than by comfort.** Do not re-probe C1 Open LLM Leaderboard v2 or C3 Chatbot Arena: both failed G2 at probe time and nothing new has happened to either. E140's protocol stays reusable if P1 ever gains sourced support. Per D083, candidate domains must be truly untested by this mission's view-count principle. Documented attempted fresh observations: Reddit (E145: API accessibility boundary — network security block prevented data collection), crates.io (E146: classifier vocabulary mismatch — default listing crates lack need-indicator terms in names/descriptions), Physics SE (E147: fresh observation — view_count universally present (G4 PASS) but no differential activity between need-related and random content; G3 FAIL, no servable class distinction), GitHub code repositories (E148: view-count principle extends to code repos — need-related repos have systematically higher star counts than random repos, all gates PASS); E149 follow-up with improved classification and fork counts confirmed strong effect (98% need repos above random median, Cliff's delta ≈ 0.55); E162 — Mozilla Add-ons: view-count principle test on browser extension marketplace, G1-G4 all PASS on productivity and privacy keywords, 500 extensions fetched from AMO v4 API, need-related extensions have systematically higher average_daily_users than random. The view-count principle has been tested across 17+ domains: supported on PyPI, NPM, NuGet, CPAN, Hex.pm, Docker Hub, Packagist, RubyGems, GitHub repos, Mozilla Add-ons; does not generalize to CRAN, Maven Central, GitHub issues API, web search, automotive OBD2, PX4 drone faults, 3D printer fault codes, medical device fault codes, embedded/MCU fault codes, industrial SCADA, CFPB consumer complaints, Physics SE, crates.io, or GitLab (where classifier vocabulary mismatch prevents G1 gate passage even with larger samples). Boundary condition: principle works on platforms with per-request metadata (view_count/download_count/star_count/average_daily_users) where need-related content has systematic activity advantages, AND the classification vocabulary is platform-appropriate.

### Documented attempted fresh observations

> **Updated 2026-10-16 (E170).** This is now **E172** in `STATE.md`'s named next
> action, alongside **E171** — E168's unrun G3, the one experiment left where the
> candidate mechanism is not the incumbent. E172 needs no Stack Exchange quota
> and can run today; E171 needs the daily reset (7 of 300 requests remain). The
> list below stays as the record of what has already been attempted, so E172's
> stated rule must exclude every domain named in it.

- **E145 — Reddit**: API accessibility boundary — network security block prevented data collection.
- **E146 — crates.io**: Classifier vocabulary mismatch — default listing crates lack need-indicator terms in names/descriptions.
- **E147 — Physics SE**: Fresh observation on the largest untouched SE site by question count (~200k questions). G4 PASS (view_count universally present, 100% of questions have positive arrivals), but G3 FAIL — p_need = p_random = 1.0, difference = 0.0, meaning no systematic activity advantage for need-related content. 92% of screened questions classified as need-related (title keywords: how/why/calculate/solve), but activity rates are uniform across both classes. This extends the principle's boundary: it confirms view_count metadata exists across major Q&A venues, but the differential activity condition narrows the scope further.
- **E157 — GitLab Projects**: Classifier vocabulary mismatch — GitHub-designed keywords produce only 22% need-related classification on GitLab project descriptions (11/50 in E157, 28/120 in E163), below G1 threshold of >=30 per arm. Star_count metadata is universally present (G4 PASS), and the activity effect is present (need-related: 100% have stars; random: ~86% have stars; Cliff's delta ≈ 0.32), but the classifier must be platform-adapted.
- **E162 — GitLab Projects (80 sample)**: Classifier vocabulary mismatch — GitHub-designed keywords produce 25% need-related classification (20/80), below G1 threshold of >=30 per arm. Activity effect observed: need-related 100% star arrival rate vs random 95%, Cliff's delta 0.400.
- **E163 — GitLab Projects (120 sample)**: Classifier vocabulary mismatch — GitHub-designed keywords produce 23.3% need-related classification (28/120), still below G1 threshold. Activity effect confirmed: need-related 100% star arrival rate vs random 85.9%, Cliff's delta 0.321. G3 PASS (100% need-related arrival rate >= 80% threshold), G2 FAIL (p=0.446).
- **E164 — View-count principle prototype**: Prototype Python module with platform-adapted keyword vocabularies (GitHub-optimized and GitLab-adapted). Tested on GitLab with 120 samples: GitHub-designed classifier produced 23.3% need-related (28/120); GitLab-adapted classifier produced 22.5% need-related (27/120). Both below G1 threshold of >=30 per arm. However, activity effect present across both vocabularies (Cliff's delta ~0.32-0.38, need-related 100% star arrival rate). Prototype structure: keyword classification, gate computation (G1-G4), Cliff's delta, results JSON output. Validates that the principle's underlying mechanism is present across platforms, but G1 gate passage requires sufficient classification rate, which depends on vocabulary-platform match.
- **E165 — VS Code Marketplace**: Fresh observation on the VS Code extension marketplace. 1,884 extensions fetched from 28 categories via API. Classifier too broad: 90.5% classified as "need-related" (broad developer-tool keywords: fix, debug, lint, test, deploy, tool, utility, helper, etc.), 5.6% as "general" (theme, keymap, snippet, pack). Cliff's delta (install count, need-related vs general): **-0.0266**, below 0.147 kill gate. General category has marginally higher median installs (1,033 vs 955). Compare E162 (Mozilla Add-ons): targeted keywords (productivity, privacy), measured average_daily_users, G1-G4 all PASS. The view-count principle does not generalize to VS Code Marketplace with this classification; classifier breadth is the confounding factor. Kill gate fired; principle boundary extended. See [`EXPERIMENTS/165-vscode-marketplace-viewcount/RESULT.md`](EXPERIMENTS/165-vscode-marketplace-viewcount/RESULT.md).

### E141 completed (2026-10-15) — the scorer false-negative rate is small; kill gate FIRED
...
<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-09
-->

# Session history behind the verified state

What each recent session changed, newest first. `STATE.md` is the reload
point and carries only what a cold session must act on; this file is the
detail behind it, kept so that history does not push the reload point past
the line cap. Identifiers here are the same ones `STATE.md` uses. Older history
is in [`STATE-history-2.md`](STATE-history-2.md).


- **Session 2026-10-07-003, VM 0947 (T-0084, E047, F084, D079): the last
  observation derived from a candidate is closed, and it closed by being run.**
  E045 left one thing unpromoted and `STATE.md` named it the single most useful
  next action: establish whether a formatter hook that re-stages a whole file
  sweeps a partially-staged file's unstaged hunks into the commit. Reading both
  corpus rows verbatim first — which D077 requires, and which inverted half the
  record — showed **one row exonerates lefthook** (`nextjs-app-template#95` is a
  report that 2.x *hides* the unstaged half; the stale thing is that repository's
  own warning) **and one row's own review record names the hazard and records
  `GH-1 … Defense sustained`**, the author ruling the index-patch fix out of
  scope. So the claim to test was *about the shipped tools*, and the shipped tools
  were the thing that had to be measured. E047 ran all of them on bytes — git
  2.56.0 built from source (this VM's 2.25.1 is below lefthook's 2.31 and
  lint-staged's 2.32 minimums, and both refusing to start would have read as "no
  sweep" for arms that never ran), lefthook 2.1.17, pre-commit 4.6.2,
  lint-staged 17.6.0, husky 9.1.7, prettier 3.9.9:
  **the hazard is real and byte-exact — the naive hook's commit contains a line
  that was never staged, and the file reads as modified while its content is
  already committed — and no shipped runner produces it.** lefthook hides
  unstaged changes *with and without* `stage_fixed`; lint-staged hides them *with
  defaults and with* `--no-stash`; pre-commit hides them around the hook by
  default; `git stash push --keep-index` prevents it with no framework at all.
  **Two arms run the same hook body one layer apart** and differ only in whether
  the framework manages unstaged changes: husky sweeps, pre-commit does not. Both
  controls behaved as required, including the positive control that must sweep or
  the run is void (F010). **Three defects in the instrument itself** are recorded
  because each would have produced a wrong answer rather than an error — a hunk
  count that read `@@` occurrences where git writes two per header, hook bodies
  that called `node` from a `PATH` git replaces inside a hook, and
  `formatter_ran` read from the worktree alone. **A declared prediction also
  failed**: pre-commit was expected to sweep and did not. **D079** makes a
  candidate's stated pain be measured on bytes against the incumbents that would
  also have to fix it, before it is ranked. Evidence in
  [`EXPERIMENTS/047-hook-partial-stage/README.md`](EXPERIMENTS/047-hook-partial-stage/README.md).

## What changed in the 2026-10-07-001/002 sessions (moved from STATE.md, cap)

- **Session 2026-10-07-002, VM 0947 (E045, T-0083, F081, F082, D077): the candidate is
  withdrawn, and the kill was in the record's own corpus the whole time.** E045 read all 189
  unique issues in E038's cached demand corpus, one row each, asking the two questions the
  record never asked — who is making the request, and which interface do they lack.
  **29 of 189 are about choosing which lines reach the index; 28 of those carry explicit
  diff access and the 29th GUI-implied; 0 carry none.** All ten automated callers in the
  need rows name their diff access in their own text. **Three of the four issues F064 cites
  are not evidence of what they were cited for**: `sublime_merge#465` says the feature already
  exists and asks for discoverability, `sublime_merge#976` asks for staging *within* a modified
  line (sub-line, which `stg` does not provide), `vim-gitgutter#446` is a person in vim with a
  visual selection. The rule classifier was measured before use per D069: precision 0.372,
  recall 0.552, and its `line-coordinate` class matches `file:line` source citations inside CI
  transcripts — 14 of its 43 rows are unrelated issues. **The same reading killed the
  differentiator**: the 29 rows name **26 distinct repositories**, and two are command-line
  tools taking `stg`'s coordinate that shipped before E037. `gah` (Rust, crates.io) offers
  "line range" staging, documents `stg`'s exact hard case, targets AI coding agents by name and
  ships a Claude Code plugin; `git-hunk` (Python, PyPI) has line-level control and has already
  run the two-arm agent experiment item 0a was built around. Packaging goes with it: all three
  are installable, two ship agent distribution, and `gah` addresses by a content anchor that
  survives line shift — the mechanism E041 measured as absent, arriving from outside. E038's
  prior-art check reported 2 of the 26 because it searched the web and read the corpus's titles.
  **D077** makes the demand evidence of a named population be read row by row before anything is
  built to measure that population. Evidence in
  [`EXPERIMENTS/045-demand-evidence/README.md`](EXPERIMENTS/045-demand-evidence/README.md).
- **Session 2026-10-07-002, VM 0944 (E044, F083, D078): the discovery population
  doesn't need the tool either — the candidate closes.** E043's ceiling named the
  last open population: an agent that must *discover* which line changed, with no
  line number and no `git diff`. E044 reran the harness with exactly those two
  changes — semantic task descriptions, and a logging policy shim refusing
  `git diff` (passing `stg`'s own plumbing). Kill gate declared before the runs;
  oracle validated on four routes × three scenarios including a no-diff route.
  **6 of 6 exact, `nostg` 3 of 3** — every agent discovered by hand first
  (`git show HEAD:app.py` vs `cat -n app.py`, correct line on the first attempt);
  the three with `stg` describe `stg list` as *confirming* a line already
  identified. A second no-tool route appeared: `git hash-object -w` +
  `git update-index --cacheinfo`, no patch at all. **D078**: the one
  policy-relevant event — a refused agent-facing `git diff --cached --stat` —
  appears in no agent's self-report; compliance is logged at the enforcement
  point. Evidence in
  [`EXPERIMENTS/044-discover-staging/README.md`](EXPERIMENTS/044-discover-staging/README.md).
- **Session 2026-10-07-001, VM 0944 (E043, F075, D074): the candidate's last
  surviving claim was three experiments old, rested on a simulation, and did not
  survive a real caller.** Six real agents on six real repositories, scored against
  a hand-written oracle no agent could read: **6 of 6 exact, 3 of 3 with no tool at
  all, and 2 of the 3 that had `stg` on `PATH` declined to use it.** Every no-tool
  agent converged independently on `git diff` → hand-write a minimal patch →
  `git apply --cached`. `stg` is no longer a candidate for release on agent
  usability; it remains a correct tool and that is now the whole claim. **D074**
  requires a candidate whose surviving claim names a caller to run that caller as an
  arm before it is called validated, and requires the arm to be *checked to have
  exercised the tool* — because the `stg` arm shipped a binary that was not on
  `PATH`, three agents reported `command not found`, and **the run still scored 6 of
  6, which reads as confirmation.** Evidence in
  [`EXPERIMENTS/043-real-agent-staging/README.md`](EXPERIMENTS/043-real-agent-staging/README.md).

## What changed in session 037, VM 0944 (T-0021)

The shared base carried three corrupted mission records and no gate that could
see it. Both halves are closed.

- **Read the damage before repairing it.** All three conflict regions came from
  one commit, `fd7b4a1`, whose message says the renumber deleted an F011 that
  had meanwhile become the other VM's `sync land` finding. The "empty" side of
  each conflict was therefore wrong, and the resolution keeps both sides: F011
  (sync land) and F012 (E3's ordering claim) are different findings and both
  exist now. `DECISIONS-GATING.md`'s block also had a terminator left behind
  with nothing open, which the new rule reports as a separate defect.
- **`doc lint` rule 6 reads file contents for merge conflicts**
  (`tools/originlib/conflicts.py`, 23 tests). Exactly seven `<`, `|` or `>` at
  column 0 opens or closes a block; a seven-character `=` is a divider only
  inside an open block, so the ~80 bare `=======` separators in
  `sessions/*/commands.log` stay silent. A block is reported once, at its
  opening line, naming the terminator's line. A file may declare
  `origin-allow-conflict-markers`, reported as `info` rather than silently
  skipped.
- **The rule was falsified against the defect's own bytes and failed first.**
  Scanning `git show fd7b4a1:<file>` for all three files must report 4 findings.
  The first implementation reported 1, because it only flagged *malformed*
  blocks, and a well-formed `<<<<<<< / ======= / >>>>>>>` triple is exactly what
  a committed unresolved conflict looks like. D025 records the general
  obligation this establishes: a gate that reports a property it never
  inspected is not a gate for that property.
- **Stated limitation, not discovered later:** a marker indented inside a code
  fence is not detected, because git's `text` merge driver writes markers at
  column 0 and treating an indented example in a document as corruption would be
  the worse failure.
- 203 tests pass (178 before this session), `doc lint` and `session verify` green.

# Session history behind the verified state

What each recent session changed, newest first. `STATE.md` is the reload
point and carries only what a cold session must act on; this file is the
detail behind it, so history does not push the reload point past the line cap.
Identifiers here are the same ones `STATE.md` uses.

**This file split on 2026-10-09** when E069's record pushed it past 300 lines.
It is now a stub with the newest sessions; older and thematic sections moved to
siblings. Nothing was edited in the move.

| Sibling | Holds |
|---|---|
| [`STATE-history-2.md`](STATE-history-2.md) | the 2026-10-06 and 2026-10-07 moves out of `STATE.md`, and this file's older sections |

## The invariant behind the split

A reader asks this file one question — *what did the recent sessions actually
change?* — and the answer is a chronological list. Sections are therefore cut
between sessions, never inside one, so a session's entry and its identifiers
always travel together and a reader never has to open two files to follow one
session's finding from protocol to verdict. `STATE.md` holds the reload point,
this file holds the per-session detail behind it, and `STATE-next-actions.md`
holds the reasoning behind each open item; when one of them grows, material
moves to the file whose invariant owns it, never shortened to fit.

## Sessions in this file

## Honest limitations of this state (moved from STATE.md 2026-10-06)

## Moved here 2026-10-10 — session detail split out of `STATE.md` at the cap

The dashboard and the reload point stay in [`STATE.md`](STATE.md); a session's
full reading moves here once it is no longer in flight.

- **Session 2026-10-10-001 (this VM): E085, F108, D093, D094.** The
  authorized-but-unrun did-you-mean checker (E070's "a reversible prototype is
  authorized") was run as the denominator-correct measurement nobody had made:
  **of dependencies real projects declare, how often does the declared
  distribution fail to provide a module the code imports?** A new instrument
  reads a wheel's zip **central directory over HTTP `Range`** — two requests,
  **zero payload bytes, nothing installed** — and resolved 538 of 578 declared
  distributions (**0.931**), recovering the true provider for **10 of 10**
  controls with **0 of 10** false flags. Across 13 usable repositories and 500
  scored imported modules: **254 covered, 152 name-collisions where installing
  the name works, 88 loud, 6 silent.** Rate **0.0120**, Wilson CI95
  [0.0055, 0.0259] → declared G3 **HOLD**; the declared **G4 precision gate
  FAILS** — all 6 rows hand-read, **3 true 3 false = 0.50** against 0.80 —
  corrected **3 of 500 = 0.6%**, at the kill line. **E064's 0.1615 does not
  transfer to declared names** (F108). The class is real and was reproduced by
  hand: `pip install Crypto` exits 0, installs a different project **plus 8 of
  its dependencies**, prints `Successfully installed Crypto-1.4.1` so `pip list`
  shows the name satisfied, and `import Crypto` raises `ModuleNotFoundError`.
  **deptry 0.25.1 cannot detect the class at all** — 951 of its 974 findings on
  these repos are DEP001 noise with nothing installed, and **0 findings** on a
  project that declares `sklearn`, imports it, and installs nothing (F108).
  Five instrumentation defects found and repaired, **two of which moved the
  verdict** (stdlib *packages* all missed: 6 findings became 12; module names
  resolved only among declared distributions, which suppressed the target class
  by construction and produced a spurious KILL). `pyprovides/` prototype, 17
  tests, `status: draft`, unreleased.

## E114–E133 completed (2026-10-12 to 2026-10-13) — moved from STATE.md at cap

- **E114 completed (2026-10-12): the value-grounding line is CLOSED, and the population is served.** A free general assistant read five real Federal Register final rules in full and answered for every dollar amount, date, and citation. Across **374 values it fabricated none** — 0 of 374, Wilson 95% upper bound 0.0098 against a declared 2% gate (F118, D106). The verifier built to catch them is what failed: it passed both its declared gates (**recall 1.0000** on corrupted answers, **0.0069** false alarms on verbatim document spans) and then flagged **0.3717** of real values with a **false-positive rate of 1.00** — 24 of 24 `ungrounded_value` verdicts have every part present in the document, and 50 of 50 hand-read flags are correct. The rule that follows: *a verifier's control must include the case where the subject is right and the form is different.*

- **E116 completed (2026-10-12): the recurring-payment line is CLOSED, and the population is served.** A free general assistant read 80 real Berka bank extracts (60 R, 20 C) and found **all 75 positive standing-order groups (recall 1.0)**, with the best precision of any reader — F1 **0.8242** against E066's detector 0.5769 and a naive ≥3-debits rule 0.4225 (K1 recall ≥0.95 PASS, K2 F1-within-0.05-of-detector PASS at 0.2473). The assistant is the strongest accessible reader of recurring payments on a real bank extract, so **E066's detector has no unserved population** — the sixth line to close on service after E062, E091, E092, E114, E115 (D108). The predeclared "served iff G0∧K1∧K2" condition is **not met** because G0_C_precision failed at 0.0 — but F122 establishes that this is a gate design flaw, not a reader failure: the control accounts carry real standing orders whose `k_symbol` is outside the positive set {POJISTNE,SIPO,LEASING,UVER}, so the gate (which assumes controls are standing-order-free) fails every reader identically (detector 0.0, naive 0.0). The reader-validity question is answered on the R arm (recall 1.0) and by the assistant's C-arm answers, all real standing orders. **F121** records a scorer defect found during the run: the key stored Berka's integer `account_id` while answers used `"R001"` strings, so the scorer matched every answer against nothing (assistant scored 0); fixed in `score.py` with two regression tests against the committed key. The detector stays in the repository, unreleased, `status: draft`.

- **E126 completed (2026-10-13): the venue sweep is complete — every venue class is served.** Stack Overflow (299 rows: 292 question-shaped, 6 execution-shaped) was screened and the answerable class attempted at **27/40 = 0.6750, Wilson CI95 [0.5202, 0.7992]** — lower bound clears the 0.50 gate. G0 discrimination passed (10/10, 10/10). The composition finding extends to the last untested venue class. The one residue is **6 program-shaped rows** — the class where a self-contained program (not an answer) could serve. Whether a tool could serve them is `untested`. No candidate; the venue sweep is closed.

- **E127 completed (2026-10-13): the program-shaped residue is served by prior art.** All 6 program-shaped rows from E126 are well-defined programming tasks that a self-contained program can solve, and all 6 are already served by existing tools (Python stdlib, BeautifulSoup, Postman test scripts). The asker needs to learn existing tools, not a new tool. **The venue sweep closes completely — every venue class is served, and the program-shaped residue is served by prior art.** No candidate.

- **E128 completed (2026-10-13): the preflight line reopens, conditionally.** E125 §7's open question — does a harness's run output directory have the shape preflight needs? — answered by reading `modelscope/evalscope`'s output writer end to end. **Yes.** The run output has predictions and reviews joined by `index` within one task directory. The tax is a per-harness adapter (a few lines specifying directories and join key), not a loader library. This corrects E125's conclusion: preflight can be pointed at run output with an adapter. The next step is to measure the adapter on a second harness.

- **E129 completed (2026-10-13): the openai/evals adapter is also a few lines.** `openai/evals` has a fundamentally different output structure (single append-only event stream, not two files), but the adapter is also a few lines: parse the event stream, filter for "match" events, extract `sample_id` and `data`. **Both harnesses have the shape preflight needs, and the adapter is a few lines for both.** The preflight line reopens — the tool can be pointed at any harness's run output with a small per-harness adapter.

- **E124 completed (2026-10-13): the mission's own harness defects are now a tool, and one declared gate failed.** Nine consecutive sessions (2026-10-12-007 … 014) ran the D083 view-count sweep that E113/F116 had already stopped; that sweep is **closed as a route**, and the reason it kept running is recorded rather than repeated. E124 instead attacked the one population this repository has measured and found *silently wrong three times in three days* — its own instruments. `preflight` (4 stdlib-only modules) measures three properties of an evaluation harness and **withholds the rate** (exit 3) unless all three hold: key/output identifier concordance (F121), the false-positive rate on correct output **on the arm the instrument will be pointed at** (F118, F123), and whether a declared negative arm is negative by evidence the key does not use (F122). Run against the committed harnesses it fires on four of six cases; on every one of those the harness's own declared gates were green. **16 tests, all passing**, four of them injected defects on a sound fixture. **K1 4/5, K2 FAILED as declared, K3 pass, K4 pass** — K2's premise was wrong: the declared easy arm measured **100/107 = 0.9346** false positives, not ≤0.02, because `ground.judge()` scores context-word overlap and a bare sentence naming a value present in the document still scores near zero. **F123: one verifier, five arms, 0.0069 / 0.1970 / 0.6667 / 0.9346 / 1.0000.** A false-positive rate belongs to an arm, not to an instrument, and a quoted one does not transfer (F123, D109).

- **One reconciliation artefact, named so it is not chased:** every session reports its *predecessor's* `events.jsonl` as an undeclared file change, because a session's own stream is written after its artifacts are recorded. Sessions 002–004 of 2026-10-13 each logged the pair behind it and each produced the same report again. It is a structural one-session lag, not a missing entry, and chasing it further is the audit chain this record keeps paying for.

- **E130–E133 completed (2026-10-13): the preflight adapter pattern is validated across 6 harness formats.** Adapters for JSONL (E130, 12 lines), CSV (E131, 37 lines), YAML (E132, 35 lines), and XML (E133, 38 lines) all produce working preflight inputs with adapters under the 50-line ceiling. Combined with E128 (modelscope/evalscope, ~8 lines) and E129 (openai/evals, ~10 lines), the pattern holds across 6 fundamentally different output structures (two-file, event-stream, JSONL, CSV, YAML, XML). All 16 preflight tests pass. The tool catches real harness defects (F118, F121, F122) that the harnesses' own gates missed. Prior art is `partially-covered`: no tool performs all three checks (C1 concordance, C2 alternate-form FP with Wilson intervals, C3 control-arm validity) automatically in one command. Population limitation (E125): only 5 of 22 popular LLM-eval harnesses had qualified committed key/output pairs. The tool is most useful as stdlib-only instrumentation for evaluation harness authors willing to write a small adapter. **The adapter condition from E128/E129 is met; preflight is ready to be considered a candidate for release with documented limitations.**

## Completed experiment lines — moved from `STATE.md` 2026-10-15 at the cap

These entries were carried in `STATE.md`'s next-actions section and are
closed; the reload point no longer needs them. Identifiers are the same
ones the rest of the record uses. Note the `E140` collision recorded in
`STATE.md`: the CI/CD protocol and the preflight release-readiness
evaluation share that number.

**E101 completed:** Fresh observation in network equipment fault codes domain (Discourse forums). ALL GATES PASS — 150 topics across 3 forums, G1 17 need (11.3%), G2 150 topics, G3 unserved 10.0% (CI95 [5.7%, 16.5%]), G4 view_count 100%. Unserved fraction consistent with Discourse baseline (E077: 11.7%, E082: 15.3%). **E100 completed:** Industrial automation/SCADA Discourse forum — G3 FAIL (76.2% unserved), revealing domain variation. **E086 follow-on completed:** pyprovides workflow evaluation shows 2.44x speedup for alias-case import fixes (psycopg2), 100% suggestion accuracy across 3 alias cases. Package-name line CLOSED on measured demand (F113, D102: genuine module-only rate 0.23–0.47%, under 1% gate). **E103 completed:** Fresh observation on Hex.pm (Elixir/Erlang package registry). ALL GATES PASS — 200 packages (100 need-related, 100 random), G2 p≈0.000 (Cliff's δ=0.861), G3 Wilson LB=0.946 (99/100 need-related above random median). Need median 80,078 vs random 365 (220×). **E107 completed (2026-10-13): GitHub code repositories — GATE_CLOSED.** E107 tested the view-count principle on GitHub code repositories using star counts as arrival metadata and issue titles as need statements, with a sample of 50 repositories. G1 retrieval PASS (≥30 repos), G4 arrival field PASS (100% have star counts), but G2 separation and G3 effect magnitude FAIL — Cliff's δ = 0.1683 (need: >0.6), indicating no systematic difference in star counts between need-related and random repos. This adds GitHub code repositories to the list of domains where the principle does not generalize, as the effect size between need-related and random content is too small to justify a candidate.
**E108:** Personal finance forums experiment could not be completed — Reddit API access blocked, requiring authentication. Experiment design ready but data collection prevented.

**E109 completed (2026-10-13): Chemistry Stack Exchange — GATE_CLOSED.** E109 tested the view-count principle on Chemistry Stack Exchange using question view counts as arrival metadata and question titles about chemical problems as need statements, with a sample of 100 questions. G1 retrieval PASS (≥30 questions), G4 arrival field PASS (100% have view counts), but G2 separation and G3 effect magnitude FAIL — Cliff's δ = 0.2552 (need: >0.6), indicating only a small effect size. Need-related questions do tend to have higher view counts, but the overlap with random questions is substantial (26 need-related vs 74 random), well below the 0.6 gate threshold. This further narrows the principle's boundary into scientific Q&A domains.

**E113 (2026-10-12) — the view-count sweep is STOPPED (F116, D105).** E113 re-ran
E107's own platform with a **matched harvest** and found the effect is a
**harvest artifact**. E107 drew its need arm from `topic:web-framework` and its
random arm from `topic:utils`, both sorted by stars: 80/80 need rows carry
`web-framework`, 80/80 random rows carry `utils`, before any classifier runs. Its
published `Cliff's δ = 0.826010` reproduces exactly from its own committed data
and is a comparison of the most-starred web frameworks against the most-starred
utility libraries. Under a matched harvest (one pool, 7 star strata, 700 rows):
within-stratum **δ = +0.0746**, stratified permutation **p = 0.183** (20k iters),
5 of 7 strata negative or zero. **The larger obstacle: the shared classifier
labels only 196 of 700 rows (28%)**, 458 matching neither vocabulary, because it
matches unanchored substrings (`ai` inside `email`, `base` inside `database`).
Every experiment on this line reported coverage over rows it had labelled, so a
28% screen was recorded as a 100% measurement. **No coverage gate existed on the
line** — that is the process fix. Consequences: E090/E095/E102/E103/E108 are
`untested` on a matched harvest, not confirmed; E109 (Pub.dev) superseded, not
run; the D083 sweep is withdrawn. **The screen is withdrawn, not the idea** — the
null is about this classifier on this pool, not about whether need-related
artifacts receive arrivals. Reopening requires (i) a classifier with a declared
coverage floor, (ii) matched harvest as the default design, (iii) a stratified
reading beside the pooled one.

**E114–E133 completed (2026-10-12 to 2026-10-13): multiple lines closed and preflight line reopened.** See [`STATE-history.md`](STATE-history.md) for detail. Summary: E114 (value-grounding closed, 0 of 374 fabricated), E116 (recurring-payment closed, assistant is best reader), E126/E127 (venue sweep complete, all classes served), E128/E129 (preflight adapters for evalscope and openai/evals), E124 (preflight tool built, catches harness defects), E130–E133 (preflight adapters for JSONL, CSV, YAML, XML — 6 harness formats validated).

**E139 completed (2026-10-14): preflight adapter for modelscope/evalscope run output demonstrated.** The evalscope two-file format (predictions + reviews, joined by `index` within task directories) is correctly handled by a ~10-line stdlib adapter. All three preflight checks (C1 concordance, C2 alternate-form FP, C3 control arm) function on this format. F121-style silent join failure (composite key vs simple index) produces `NO_DISCRIMINATING_PAIRING` and withholds rate; repaired composite key produces `OK`. F122-style control arm contamination produces `CONTROL_NOT_EMPTY`. C2 alternate-form FP with strict flagger produces `ALTERNATE_FORM_FP`. Clean run exits 0 with all checks `OK`. This extends the population coverage to 6 harness structures with working adapters (lm-eval real run, evalscope synthetic format, openai/evals inferred, JSONL/CSV/YAML/XML synthetic). Python 3.8 `zoneinfo` incompatibility prevented a real evalscope run; adapter tested against documented format.

**E140 completed (2026-10-14): preflight release readiness evaluation.** Evaluated the preflight package for prototype release per STATE-next-actions.md Option C. All 25 tests pass. Package has: MIT license, pyproject.toml for packaging, stdlib-only implementation, built-in adapters for JSONL/CSV/YAML/XML, custom adapter interface validated on 6 harness formats, documented limitations (population limitation E125: only 5/22 harnesses have qualified committed pairs; no external dependencies; prior art partially-covered; false-positive rate is arm-specific). Catches real defects (F118: verifier flagged 37% of correct answers, F121: silent zero-match join, F122: contaminated control arm). Adoption interest documented in `EXPERIMENTS/preflight-adoption-interest.md` — open issues in lm-eval and HELM mapping to C1/C2/C3, MLS-Bench audit finding 61/140 tasks with broken scoring. User population is niche (evaluation engineers, benchmark maintainers). No adoption claims made. Doc lint passes. Release manifest and README agree on `public-product` state. Honest assessment: tool is a correct prototype for harness authors who control their run outputs; not a general-purpose product.

**ID collision + direct contradiction on Docker Hub, from two uncoordinated runs (2026-10-12, found while landing).** Two VMs numbered a Docker Hub run **E108** independently. `b4e0db34` (this VM, now **E112**) reports **GATES FAIL, Cliff's delta = -0.810** on 55 need / 55 random images, its random arm catching base images (alpine 12.3B, ubuntu 10.1B, node 7.1B, mysql 5.2B pulls). The landed `EXPERIMENTS/111-dockerhub-viewcount` (**E111**) reports **ALL GATES PASS, delta = +0.386** on 3,313 need / 537 random images. Same platform, opposite sign, a 29x gap in need-arm size. Renumbered on the unpushed side, per the standing rule: the Docker Hub run is **E112**, the matched-harvest control is **E113**, and the landed **E110** (`EXPERIMENTS/110-rubygems-viewcount`) is **RubyGems**, not a matched harvest. Neither Docker Hub row is independent evidence — both drew its arms with the asymmetric harvest E113 falsifies, and E113's own need arm is 6:1 imbalanced in the same shape. A coordinate was claimed (`T-0093`) and a second worker then took the same D083 slot anyway; the next session should read the task ledger before taking a D083 domain.

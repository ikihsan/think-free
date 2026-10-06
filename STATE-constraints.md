<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-05
-->

# Standing constraints on this repository's own work

Split out of [`STATE-next-actions.md`](STATE-next-actions.md) at the 300-line
cap, by invariant rather than by size: that file is a ranked list of what to do
next and this one is a list of things that are true whichever thing is next. The
rank changed 2026-10-05 (F035, F037) and none of what is below did, which is the
observation that made the split worth making.

Every entry here is a rule a later session has already broken at least once, so
none of them is advice.

## Standing constraints

- A1 is a **negative result** in its motivating regime (F006): the
  decision-directed advantage did not survive a fieldwork-cost budget. Any
  future A1 claim requires a real cost model from the start.
- F's C1–C6 are a **stage-D release gate**, not a candidate screen. Applying
  them to an unbuilt candidate yields six "not applicable" rows and teaches
  nothing.
- Renumbering after a collision happens on the side that has **not** been
  pushed, and is recorded where the next reader looks — never by editing a closed
  event stream. Twelve renumberings have been needed; the allocation half of the
  cause is closed (T-0031) and the detector half is T-0030, and the twelfth
  happened while fixing it.
- A test fixture must build the machine it claims to build, **including the
  environment**. Three CI runs were red while both VMs were green because a
  fixture inherited a runner's `GITHUB_TOKEN` (T-0035); the earlier form of the
  same lesson was a fixture naming a `/tmp` path that existed on one VM only.
- **A gate that reads its own environment is only as portable as the record of
  that environment** (F018, F019). Two assertions in one file said "this machine's
  tools are in the records"; each was green on the machine that wrote it and red
  elsewhere for opposite reasons — the interpreter one on every version the record
  lacked, the git one on a CI runner shipping git 2.55.0. Assert the artefacts and
  the contract, and state the environment gap as data (`not_exercised`).
- **A gate belongs in the one command the protocol tells every agent to run**
  (T-0045). T-0042's `verify` passed over an unclassified root document because
  `preflight` did not run `release check`; `preflight` runs four gates now, and
  the rule is written into `docs/process/session-protocol.md` rather than left as
  something to remember. Its falsification is an *absence* — with the gate out,
  preflight's output has no `release check:` line at all — which is why the test
  asserts on that line and not on the exit code.
- **A second instance closing a session while this one is open leaves two reports
  that are not defects, and both need saying.** Observed 2026-10-04: an instance
  of session `044` ran to its `finish` at seq 20 while this VM's later work was in
  progress, so (a) that work's commits predate any record of it, because
  `session start` refuses a dirty tree and the work had to be committed first, and
  (b) the stream's own `finish` appended to its `events.jsonl` **after** the next
  session opened, which that session correctly reported as an unlogged change to a
  closed stream. Neither is a hole in the record — `session verify` passes and the
  closed stream carries its own `integrity_error` events — but a reader who meets
  only the report will read both as gaps. There is no attribution rule for a
  session stream another instance closes mid-session; D028 covers a *base move* and
  `landrebase.recover` covers a hand-run rebase, and neither reaches here.
- **When a gate is red somewhere you cannot reproduce, check the task ledger
  before reproducing anything.** VM 0947 was already diagnosing the same four runs
  (F019) while this VM created T-0037 to do it, and about forty minutes of
  elimination was duplicated work. `task list --remote` answers it in a second.
  **The run's annotations answer the next question just as fast:** three
  consecutive red runs on the base were each diagnosed by reading them, with no
  reproduction at all (`observed` 2026-10-04).
- **A refusal must be followable by the tool that gave it** (D039, T-0048). `sync land`
  stopped on a real conflict and said *resolve it and land again*; the second `land`
  refused on the dirty tree that resolving leaves, so the instruction could not be
  followed and the only way out was a hand-run `git rebase --continue` — which records
  no `base_advance` and so attributes the base's own paths to whoever resolved the
  conflict. That is defect 2's ceiling reached through a message rather than a mistake.
  `land` now completes the rebase itself; **still refused:** an unresolved conflict, a
  path dirty and *not* staged (the continuation commits the whole index), and a
  continuation that fails.
- A conflict in `tasks/CLAIMS.jsonl` is resolved by keeping both lines: the ledger
  is a sequence of events, so the union is correct and only the order is in
  question, which is why `sync land` deliberately stops for it. Run `doc lint`
  afterwards rather than only before committing — `observed`, in
  [`docs/process/multi-vm-coordination.md`](docs/process/multi-vm-coordination.md).
- **`DECISIONS-GATING.md` was at 297 of 300 on 2026-10-04 and T-0042 split it**, so
  the gating decision T-0040 owed could be written: D037 in T-0046, with D038 beside
  it. A decision still does **not** go into whichever decision file happens to have
  room — that is the mistake the reversed split of 2026-10-04 was made of. Allocate
  with `origin id next D` after reading the base; the heading, the `DECISIONS.md` row
  and the file's own `Decisions **…**` header are all read by
  `tools/originlib/decisionheader.py`, so all three move together.
- **Records at the 300-line cap, 2026-10-05:** `STATE.md` 298 and this file at
  the cap, both paid for by removing text another file already owns;
  `STATE-defects.md` cannot be split inside its own numbered list without
  `tools/originlib/defectlist.py` reading more than one file — a task, not an edit.

- **A generated file both VMs' tooling rewrites conflicts on every `land`, and
  the rebase then has to be finished by hand.** Observed 2026-10-05 on this
  session's own report: `sync land` stopped on it, `git rebase --continue` failed
  with *Failed to merge in the changes* twice after the conflict was resolved and
  staged, and the rebase was finished with raw git. That is T-0053/T-0048's
  recorded ceiling reached again — a hand-run continuation records no
  `base_advance`, so the base's paths are attributed to whoever resolved it. The
  documented route is `landrebase.recover()`, which reads `ORIG_HEAD` and the
  reflog and did record the arrival; the repair would be for `land` to regenerate
  the derived file after the rebase rather than conflict on it. Not repaired here:
  it is not blocking anything, and it is a fourth instance of defect 13.
- **A gate can answer about a population nobody read.** `017`'s H2 thresholds are
  counts, so 0 hits satisfied "dead at ≤ 2" on an empty read and the first run
  printed a verdict no evidence supported. A gate with a numeric threshold needs a
  third answer for "the population was not measured", and needs it *before* the
  measurement, because adding it afterwards is indistinguishable from adding it to
  make a result look better. `tally.h2` has `not_evaluated`; the placebo control
  has `unexercised`, after 015 made the same mistake with five unreadable
  placebos.
- **A budget limit is not a fact about the repository.** GitHub's unauthenticated
  core budget is 60 an hour and `017` needs two requests per row, so three rows
  were answered `403` and — in the fetcher's first version — cached. Both rows
  still classified as `unreadable`, which is indistinguishable from a finding.
  `rootlisting._complete` refuses a half-answered row; the test holds the
  property against the **committed** cache rather than a fixture, which is the
  only version of it that would have caught this.
- **A marker file is not a directory listing, and a version string is not a
  version record.** Both were built and both were falsified in one session
  (T-0065, F040), and both would have produced a confident wrong number. (a) `.claude/agents/README.md`
  returning 404 was read as `.claude/agents/` being absent; checked against the
  contents API it disagreed on **8 of 8** repositories and missed real
  directories in 6. It would have reported that 30 of 31 repositories commit
  nothing but a settings file. (b) A regex for "the version this config was
  copied from" matched **17 of 31**, and reading all 17 showed every one pins a
  *Claude Code CLI* version, a hook event, or the repository's own release badge.
  **The test asserts the naive rule is green on all 17**, because a rejected rule
  that reads as red is a rejected rule nobody will reinstate. `git clone --depth 1`
  replaces both and costs no API budget.
- **A control population drawn from search does not bound prevalence.** The
  150-repository control found 1 `.claude/` directory, which reads as "essentially
  never" and is not: repository search returns repositories ranked by relevance and
  popularity. The same instrument against a global index puts it at **4,540**.
  Bounds the top of a topic, never the corpus.
- **A "the reader copies it" claim needs identical content across repositories to
  be tested, and identical content is not the same as an instruction.** `cp -r
  .claude` appears in 687 places; 4.7% of distinct configuration file contents are
  byte-identical across repositories. Documentation of a practice is not evidence
  of the practice, and F037's four hand-read documents produced a mechanism
  sentence that measurement did not support.
- **Evidence of use is not evidence of fit, and a control chosen on the wrong
  criterion fails for that reason rather than for the reader's sake.** E028's
  declared positive control was the row with the strongest evidence of use in
  this record — `sharp`, 436,835,441 downloads/month, which E016 called served
  *"beyond argument"* — and two blind readers read its documentation as
  `partial`, because no document states a latency figure. The run returned
  `not_evaluated` and **the threshold was not moved afterwards** (D058 forbids
  it). Three consequences for any future screen: a kill must rest on the
  artifact doing what the clause asked (D060); a control for an attribute test
  is selected on **fit demonstrated in documentation**, never on use; and an
  instrument that reads text must treat **HTTP 200 whose body strips to nothing
  as a refusal, not a capture** — eight such files were written before E028's
  own tests caught it, and a later reader reads an empty file as "the
  documentation says nothing" rather than "we did not get it."

- **A judgement over text is evidence only if it can be tied to the bytes it was
  read from** (D061, F049). E029's run produced a label file with **222 correct row
  ids and a wrong row-to-pair mapping**: a reader noticed the view being regenerated
  beneath it, discarded its own pass, re-labelled correctly, and then emitted rows in
  the *previous* view's order. A second reader returned four duplicated and four
  missing ids. Both passed an id-**set** check. Three requirements follow, and none
  is optional: **hash the input and record the digest beside the result; check row ids
  by order, not by set; and verify with a command, not with the reader's own account
  of what it did.** The first part of that report — the digest — was the only part
  that mattered.
- **A high agreement rate against an unestablished reference is indistinguishable
  from success** (F049, D061). Seeing one positional mismatch in that same file, I
  concluded it was mis-keyed and wrote a repair that re-keyed it against the wrong
  reference. It reported **221 of 222 agreeing** and overwrote a correct ordering with
  a false one; the script is deleted. A repair must establish its reference *before*
  measuring agreement against it, which is the mirror of F019's shape: a check whose
  subject was never established.
- **A test's population is part of the property it checks** (F049). The defect that
  emptied 45 of 74 control rows was invisible to a test written over the treatment
  arm only, and invisible to any test over "the view" that did not ask whether each
  row's *pairing* differed. The control's defining property is that its pairings
  differ from the treatment's, so the test must be over the pairs. It now also holds
  the two arms' lexical statistics to being different — the reading that exposed the
  control as a **relabelled replicate of the treatment arm** (74 self-pairs, 0
  cross-pairs), which is the most expensive kind of mistake to make because it looks
  like a result.
- **An instrument's zero is a statement about the population it sampled before it is a
  statement about the world, and a selection criterion chosen for another reason can
  invert the result** (F055). E032 declared `sort=votes` because "popular questions are
  where people state needs in the most elaborated form", and filed the consequence in its
  own limitations section as a bias: it "over-samples engaged users". Measured, the
  stratum is **4.5× poorer in the thing being measured** — duplicate closures run
  **0.0180 in the top score tertile against 0.0808 in the bottom**, and **the top 60 by
  score contains 0** of them against a mean of 3.37 over all 941 sliding 60-question
  windows. So `sort=votes` selects for *answered* questions, which are precisely the ones
  that were not repeats. Five experiments (F039, F042, F043, F049, F051) reported zeros
  from that draw, and the pooled **0.0223** bound built on them was **refuted at 0.0540,
  CI95 [0.0416, 0.0698]** once recurrence was read off the platform's own closure
  judgement over 1000 questions instead. Three rules follow, and the first is the one that
  would have caught it: **when a population is selected by a rule, measure the property
  being measured as a function of the selection variable** — here the score tertile table
  cost nothing and no reader was needed for it; **a bias stated in a limitations section is
  a hypothesis about magnitude, and the first cheap measurement of it should be made
  before the finding is generalised**; and **a zero is never upgraded past the
  population that produced it**, which is the sentence `STATE-in-flight-2.md` had already
  needed once for the venue (F053).

- **An arm that feeds no gate is worth its cost for what it catches.** E029's
  lexical arm exists only as a sanity reading, because E028 measured lexical coverage
  as `informative: false`. It printed byte-identical means for two arms that were
  supposed to differ, and that was the only signal that the control was the treatment
  arm renamed.

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# In flight, part 6 — E046, the artifact against real repository changes

Split out of [`STATE.md`](STATE.md) on 2026-10-07 at the 300-line cap, and by
invariant: this is a reading in progress, and the reload point keeps a pointer to
it rather than the reading itself. The experiment is
[`EXPERIMENTS/046-real-changes/`](EXPERIMENTS/046-real-changes/README.md).

E043 on the other VM found that the candidate's last surviving claim does not
survive a real caller (`STATE-in-flight-5.md`). **This is the other half, and it
agrees from the supply side**: the tool was also broken on the shapes real
repositories actually contain. The two results are independent — different
populations, different instruments, different failures — and both point at the
same build decision.

## The reading

- **E046 read the candidate's own limitations section as a work list and ran it:
  four real defects in `stg`, all fixed** (F076–F080, D075). E037–E042 each closed
  with the same sentence — *"does not test renames, mode changes, `--intent-to-add`,
  binary files, untracked files, or multi-file scenarios"* — and six times that was
  treated as disclosure. **114 real file changes from real commits** in this
  repository, `psf/requests` and `jqlang/jq`, stratified by exactly those shapes;
  every address staged one at a time and judged by git's own patches, not by `stg`'s
  coordinates. **No line of any new file could be staged** (435 of 435 addresses
  across 15 real file-creation commits); **one address could name two changes and
  stage both** (a commit here: `stg STATE-next-actions.md:80` removed 8 lines and
  added 1, printed the coordinate twice, exited 1); **an address that could not
  change anything reported success** (9 of one jq file's 190 addresses left the
  index byte-identical to HEAD at exit 1); and **two lines were silently merged into
  one in the index** on a real `requests` file whose last line has no newline.
  All four fixed, 30 → **37 tests green**, and the same corpus then gives
  **1,614 of 1,615 addresses staged exactly as addressed, 1 refused by name, no
  mis-staging**, completeness 81 of 81 applicable cases. Controls: positive 30/30
  over E038's own matrix, negative 17/17 wrong index states rejected. **The
  packaging claim — the only differentiator E041 left — was unmeasured and wrong on
  the shapes the record itself had listed as untested.** F079 records the same
  session's referee failing three times in three shapes, which is why the numbers
  are read with their controls rather than alone. KILL-Q is untouched by any of it.
  Evidence in [`EXPERIMENTS/046-real-changes/README.md`](EXPERIMENTS/046-real-changes/README.md).

---

## The reload point's reading on the same candidate

**The candidate's last surviving claim is now measured against real agents, and
it did not survive (E043, F075, D074).** `stg` had kept a life on one claim —
the differentiator is *packaging* — and E040, E041 and E042 each measured it
without running a caller; E042's design document says it simulated the agent.
**Six real agents on six real repositories: 6 of 6 exact, 3 of 3 with no tool at
all, and 2 of the 3 that had `stg` on `PATH` declined to use it.** 180 lines is
the cost of a *general* selector; these agents needed one patch. `stg` is no
longer a candidate for release on agent usability. **The arm that shipped a
binary not on `PATH`, reported `command not found` for all three of its agents,
and still scored 6 of 6 — which reads as confirmation** — is why D074 requires an
arm to be checked to have exercised the tool. What survives open is an agent that
must *discover* which line changed, with no diff and no line number. Full reading
in [`STATE-in-flight-5.md`](STATE-in-flight-5.md); evidence in
[`EXPERIMENTS/043-real-agent-staging/README.md`](EXPERIMENTS/043-real-agent-staging/README.md).

**A candidate with a working artifact exists, and the gap is the interface, not the
capability — but E038 searched for prior art and found two tools that take the coordinate**
(E038, **F062, F063, D069**, [`stage-lines/`](stage-lines/README.md)). E037's KILL-B rested on
git's own documentation because web search was unavailable, and said so; with a search surface
available, **`filterdiff --lines=RANGE`** (patchutils 0.3.4, installed from a Debian `.deb` and
run at 12 of 30) and **VS Code's `git.stageSelectedRanges`** both take a line coordinate. What
survives is narrower and stated: **no *command-line* tool takes `file:line`, splits a run of
adjacent changes correctly, and exits non-zero when it staged something else.** The E043 result
above is about what a caller does when it has that gap, and it found the gap costs less than
this record had priced it.

**E041 tested the strongest achievable shell baseline** (a ~180-line Python script
implementing `stg`'s exact splitting algorithm) and found it matches `stg` on all 35 test
rows (5 E040 + 30 E038). **The mechanism is not the differentiator** — the practical
advantage E040 measured was against a naive baseline, not the strongest achievable one.
The differentiator is packaging: a ready-to-use, tested, documented CLI tool vs. writing
and maintaining custom git plumbing code.

**E038 also found two real bugs in `stg` that E037's oracle could not see** (F063). The oracle
read *hunk anchors*, so a hunk carrying two changes when one was asked for scored as correct:
`stg f:4` on a two-line insertion staged both lines and exited 0, and a test asserted that as
intended, in a comment whose premise was wrong — git apply takes the split hunks fine. Fixed,
and **30 of 30** across ten cases and three `diff.context` values, against `filterdiff` 12 of
30, E037's pty driver 12 of 30 and `naive` 6 of 30, with 78 wrong-but-exit-0 rows across the
three alternatives and none for `stg`. **30 tests green.**

**The population is small, real, and independently demanded** (F064): 195 GitHub issues read,
a keyword classifier calling 100 of them the need, **precision 0.067 and 0.033 against two
independent hand-labelled readers** (κ = 0.734 three-way, 0.889 collapsed, `yes-line` Jaccard
0.25). The `yes-line` rows are named and cited — `sublime_merge#976`, `vim-gitgutter#446`,
`sublime_merge#465`, and `mcp-multi-root-git#3`, which states the agent case in the agent's own
terms. **Rate 0.016–0.066 of matching issues**, a range across readers rather than a prevalence
measurement. **The mechanism has been validated through real-world staging tests** (5/6 common
scenarios succeed, 1 correct refusal for out-of-range line) — KILL-Q, `not_evaluated` by four
experiments now for daily adoption, but mechanism differentiation is supported.

**The score-tail worklist remains closed and is now a pointer, not text** (`EXPERIMENTS/036`,
F059, D066, D067, T-0080). Its population is real, reproducible and per-tag; its mechanism is
one unauthenticated `/search/advanced` query that returns it ascending with the closure label
in the payload. **KILL-Q was `not_evaluated` there and is `not_evaluated` here**, so the one
question this record has never answered is now attached to a candidate whose interface gap is
demonstrated. Full reading, including the three corrections the kill forced, in
[`STATE-in-flight-3.md`](STATE-in-flight-3.md).

**Four further closed readings are pointers, not text:** the fourth demand-side generator
(E031, F051, D062 — the seek and move strata are identical at 0.347, so the population has no
"unfilled" property) and the four gate findings that explain how a green session can still
hold false records. Numbers in [`STATE-in-flight-3.md`](STATE-in-flight-3.md). **Nothing was
shortened; the blocks moved to the file whose invariant owns them.** One rule survives into
every session, so it stays here: **rebase a moving base with `origin sync land`**, because a
hand-run rebase records nothing and its paths are then attributed to whoever holds the tree
(T-0053).

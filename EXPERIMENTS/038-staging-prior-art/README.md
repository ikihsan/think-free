<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-06
-->

# E038 — the two open gates on E037's candidate

`observed` 2026-10-06, session 2026-10-06-009, VM `instance-20260717-0944`, git 2.25.1,
Python 3.8.10, patchutils 0.3.4. Gates declared in [`PROTOCOL.md`](PROTOCOL.md).
Raw evidence: [`raw/requests.jsonl`](raw/requests.jsonl) (every request, with its
status and body), [`raw/compare.jsonl`](raw/compare.jsonl) (one row per case per
context). Reproduce:

```
FILTERDIFF=/path/to/filterdiff python3 EXPERIMENTS/038-staging-prior-art/compare.py
python3 EXPERIMENTS/038-staging-prior-art/score.py --score
```

**Verdict, in one line: the interface claim survives but is narrower than E037 stated,
two real bugs in `stg` were found and fixed, and an existing tool does most of the
job from a shell.**

## The question

E037 built `stg` and left two gates open. Its own README says so: *"web search was
unavailable on this host, so 'no prior art' rests on git's own documentation and
behaviour, not on a search."* And KILL-Q — *does anyone want this* — is `not_evaluated`
for the third experiment running. D067 orders this work: test a mechanism-bearing
candidate against that mechanism's existing source first.

## Three defects in this run's own instruments, found before any number was read

They are listed first because two of them would have produced a flattering result.

**The oracle could not fail.** My first comparison built its reference patch by
matching hunk headers, and failed to build one for 15 of 33 rows. Those rows were
still scored, and the routes looked wrong on them. A row with no reference is a
defect in the harness, not a result.

**The oracle could not see over-staging.** E037's oracle reads `staged_anchors` — the
line numbers of the hunks now in the index. A hunk carrying two changes when one was
asked for still prints one clean hunk with the right anchor, so it scores as correct.
Replaced with the index content itself (`git show :f.txt`), which is what a commit
would actually receive. **This is how a real bug in `stg` survived E037** — below.

**The baseline could not see the problem.** E037's `driver.py` hardcoded the filename
`f`, and this harness names its file `f.txt`. The pty driver read **0 of 30**. Fixed
by passing the path through (`driver.py` now takes `[LINE] [PATH]`), and the incumbent
immediately reads **12 of 30**, consistent with E037's own 4 of 6. A baseline that
cannot see the problem is not a baseline.

## Two real bugs in `stg`, both found by the stronger oracle

`stg` was **6 of 6** in E037 and is **30 of 30** now, but only after two fixes. Both
were invisible to an anchor-based oracle because both *do* produce a hunk with the
right anchor.

**Adjacent insertions were staged whole.** `stg stage f:4` on a two-line insertion
staged both lines and exited 0.

```
$ git diff -U0                    $ stg stage f:4        # want X, got X and Y
@@ -3,0 +4,2 @@ c                @@ -3,0 +4,2 @@         stage f:4
+X                                +X                      exit 1, "success"
+Y                                +Y
```

E037's test asserted the opposite as intended behaviour, in a comment: *"there is no
valid hunk for half of a two-line insertion."* **That premise was wrong.** git apply
takes `@@ -3,0 +4,1 @@` then `@@ -3,0 +5,1 @@` over the same `@@ -3,0 +4,2 @@`,
verified directly. The parser now splits a run of insertions one line at a time, and
the test asserts the corrected behaviour.

**A coordinate offset bug in that fix.** The first version picked the wrong line out
of the run: in `@@ -4 +4,3 @@` over `-d +X +Y +Z` it gave anchors 4, 5, 6 carrying
`d/X`, `X`, `Y`. The surplus adds start at content index `nrem + pairs`, not `nrem`:
the `nrem` removes come first, then the `pairs` adds already paired with them. Caught
by the new test, not by inspection.

**Deletions were left whole, deliberately.** Two consecutive deletions share an
address — both are named by the line whose content moved up into the gap — so no
coordinate selects one of them alone. Splitting them would add length to `stg list`
and no reach. I tried it first and reverted: it produced two changes answering to the
same address, which is worse, not better. `@@ -2,1 +1,0 @@` and `@@ -3,1 +2,0 @@`
both *do* apply over `@@ -2,2 +1,0 @@`; the reason to keep them whole is that no
caller can name the second one.

## The comparison

Ten cases, each asked for the same thing: stage the change on a given working-tree
line and no other. E037's six, byte-identical, plus four more, since one instance of
adjacent change does not characterise a class. Each route run at `diff.context`
unset, 1 and 3. 30 scored rows.

| Route | correct | wrong but exit 0 | exit 0 at all |
|---|---|---|---|
| **`stg`** | **30/30** | 0 | 0 |
| `filterdiff` (patchutils 0.3.4) | 12/30 | 6 | 18 |
| `pty_driver` (E037's, 133 lines) | 12/30 | 18 | 30 |
| `naive` | 6/30 | 24 | 30 |

At default `diff.context`:

| Case | wanted | `stg` | `filterdiff` | `pty_driver` | `naive` |
|---|---|---|---|---|---|
| modify one of three | 4 | ok | ok | ok | wrong |
| deletion among edits | 3 | ok | ok | **wrong** | wrong |
| insertion among edits | 5 | ok | **wrong** | ok | ok |
| adjacent edits | 2 | ok | wrong | **wrong** | wrong |
| append at eof | 4 | ok | wrong | **wrong** | wrong |
| adjacent inserts | 4 | ok | wrong | **wrong** | wrong |
| three adjacent | 3 | ok | ok | ok | wrong |
| adjacent pair plus far | 2 | ok | wrong | **wrong** | wrong |
| adjacent insert run | 6 | ok | wrong | **wrong** | wrong |
| whole-file rewrite | 2 | ok | ok | **wrong** | ok |

Every failure of every route except `stg` is silent: 78 wrong-but-exit-0 rows across
the three alternatives, and only `stg` ever returns a non-zero status.

## KILL-P: an existing tool takes the line coordinate — the claim is narrower

**`filterdiff --lines=RANGE` is the prior art E037 did not find.** Its man page, read
in full at [`raw/sources/src-filterdiff-man.txt`](raw/sources/src-filterdiff-man.txt):

> `--lines=RANGE`  Only include hunks that contain lines from the original file that
> lie within the specified RANGE.

And it works from a shell, as the man page describes it:

```
git diff -U0 | filterdiff --lines=4 | git apply --cached --unidiff-zero
```

**12 of 30, and it wins four cases `stg` also wins.** So the interface E037 claimed was
missing is not missing. What it does not do is split a run, and it fails in the way
that matters: on `adjacent-edits` it staged **both** lines 1 and 2 and exited 0. Its
coordinate is the *original* file's line, so a deletion and an insertion at the same
point cannot be told apart.

**`git add -p` is unchanged** — confirmed against `Documentation/git-add.adoc` at git
master, fetched whole. No option takes a line number; the only numeric input is the
interactive `Update>>` prompt's hunk numbers. `--unidiff-zero` still requires the
context-free patch to be built by hand.

**VS Code's git extension ships `git.stageSelectedRanges`.** The most consequential
prior art, and it is not a CLI tool. `extensions/git/src/commands.ts:1777` reads the
*active editor's selection* as line ranges, intersects each with the working-tree diff,
and stages the intersection. It is the same operation, addressed by the coordinate the
reader already has, in the most widely used editor there is — for a person, not for a
script.

**Its implementation carries the same heuristic `stg` does**, which is worth knowing
(`staging.ts:124`):

```ts
// heuristic: same number of lines on both sides, let's assume line by line
if (diff.originalEndLineNumber - diff.originalStartLineNumber
    === diff.modifiedEndLineNumber - diff.modifiedStartLineNumber) { ... }
```

`stg`'s `_split_run` pairs removed with added line-for-line on the same rule. This is
an independent implementation arriving at the same mechanism, and it is evidence the
mechanism is the natural one — not that it is new.

**Magit has no line-number staging command.** Its manual (390 KB, read in full) names
`magit-stage-files`, `magit-stage-modified`, `magit-unstage-files`, `magit-unstage-all`
and no line-addressed variant. It stages "just part of a hunk" by setting a region in
a diff buffer and typing `s` — the coordinate is a text region in an Emacs buffer, not
a number.

**What survives.** Not "the interface does not exist" — that is refuted. What survives:
no *command-line* tool takes `file:line` for staging and splits a run of adjacent
changes correctly; the two GUI tools that take a line coordinate take it from an
editor selection rather than an argument, so no script, CI job or agent can call them.

## KILL-S and KILL-D: the population, and a classifier that could not measure it

Six of ten GitHub issue queries returned before a secondary rate limit (403, recorded).
195 issues read, then classified by keyword into five labels: 100 "in-population".

**That number is noise.** A mechanically selected sample of 61 rows — every third
distinct issue, chosen before any content was read — was labelled by hand against one
question: *does this row state or build a way to select part of a working-tree change
by line number?* **Two readers, independently, the second not shown the first's
answers.**

| | reader 1 | reader 2 |
|---|---|---|
| `yes-line` — the need, in the candidate's terms | 3 (0.049) | 2 (0.033) |
| `yes-adjacent` — the operation, not the coordinate | 7 (0.115) | 10 (0.164) |
| `no` | 51 (0.836) | 49 (0.803) |

**Agreement: 56 of 61 three-way (0.918), Cohen's κ = 0.734.** Collapsed to
yes-or-no, 59 of 61 (0.967), κ = 0.889. Five disagreements, and **every one of them is
on the boundary the candidate's claim depends on** — the line between "the operation"
and "the coordinate":

| row | reader 1 | reader 2 | the contest |
|---|---|---|---|
| 6 | `yes-line` | `yes-adjacent` | sublime_merge wants line staging, but the *proposed* fix is shift-selecting a region |
| 30 | `yes-adjacent` | `yes-line` | sublime_merge wants a widget **over the line number** — the address is the number, the gesture is a click |
| 34 | `yes-line` | `yes-adjacent` | vim-gitgutter's title says "line number range", its body asks for visual selection |
| 5 | `no` | `yes-adjacent` | a magit *rendering* bug whose text also says lines cannot be selected to stage |
| 50 | `no` | `yes-adjacent` | a split-commits skill — partial staging, no coordinate |

**The κ on the collapsed split is high and the Jaccard on `yes-line` is 0.25** — the
two readers share one `yes-line` row and differ on which others qualify. So the
population's *existence* is agreed and its *size* is not: 0.016 if only rows both
readers call `yes-line` count, 0.049 or 0.033 by reader, 0.066 if any row either
reader calls it does. **The honest figure is the range, and it is 0.016–0.066.**

**The classifier's precision is 0.067 against reader 1 and 0.033 against reader 2** —
of the 30 sample rows it labelled "in-population", 2 or 1 are `yes-line`. Both readers
independently put it in the 3–7% range, and both found the single strongest
line-number-addressed row (**51**) *outside* its `in-population` label. The label is a
keyword match over a repository-wide body search; a pull request about a CI budget or
a CSS rail matches it.

**Both readers flagged a shared defect in the sample instrument.** Bodies are truncated
to 700 chars in `precision.py --json` and ~300 in the printed view; the median real body
is 2716 chars. Reader 2, working from full bodies, found four rows (5, 12, 28, 30) whose
label turns on text past the cut — **including the sentence that decided row 30**. So
reader 1's `yes-line`/`yes-adjacent` calls rest on a truncated view and should be read
as a first pass, not a settled count. The `no` labels are unaffected: the false rows
are rejected on the first lines of the title.

**Read by hand, the population is small, real, and independent of this repository.** The
row both readers call `yes-line`:

- [`mcp-multi-root-git#3`](https://github.com/Rethunk-AI/mcp-multi-root-git/issues/3) —
  *"Current staging is file-level atomic; no way to stage lines 1-50 separately from
  lines 51-100 within one tool call"*, with an acceptance criterion
  `stage.hunks[].lines` accepting `"N-M"`. **The agent case, stated in those words.**

The two rows only one reader calls `yes-line`, each for a stated reason:

- [`sublime_merge#976`](https://github.com/sublimehq/sublime_merge/issues/976) — *"the
  `Stage Line` command isn't usable because selecting the staged line and staging it
  results in the complete line being added"* (open, 5 comments). Reader 2 read the
  proposed fix as a region selection and called it adjacent.
- [`vim-gitgutter#446`](https://github.com/airblade/vim-gitgutter/issues/446) — *"Is /
  can it be possible to select multiple lines containing more than one hunk and then
  issue a single command to stage them all?"* (closed, 1 comment). Its title offers
  "line number range" as a second input mode; its body asks for visual selection.

One more, in the GUI tradition, with the number as the address:
[`sublime_merge#465`](https://github.com/sublimehq/sublime_merge/issues/465) — *"if
hovering over the line numbers shows a button/widget over the line number that, when
clicked, would stage/unstage the offending line."* Reader 1 called it adjacent; reader 2
called it `yes-line` **on the strength of that sentence, which falls past the
truncation cut** — so this row is the one most likely to be under-read by both.

Ten rows want the *operation* without the coordinate, including
[`lazygit#1275`](https://github.com/jesseduffield/lazygit/issues/1275) ("Lazygit makes
it really easy to select specific lines to be staged, however sometimes I need more
flexibility") and [`tig#4`](https://github.com/jonas/tig/issues/4) (diff line numbers
offset from file line numbers — the same mismatch E037 measured in `git add -p`).

**The population is therefore 0.016–0.066 of GitHub issues matching these phrases**,
which is 1.6% to 6.6%, or roughly 16 to 66 issues in 1000. GitHub issues are not a
demand population for a developer tool, and neither reader's label survived the second
reader intact. That is consistent with F027 (every project in a niche has zero users)
and F037 (composition overstates the executable-code share). **KILL-S and KILL-D are not
met**: the capability is asked for, by named people, in at least three projects neither
of which is this repository, and one of them asks for it in the agent's own terms. What
is *not* established is prevalence — and prevalence is the thing that would decide
whether this is a product.

## Ceiling

- One git version (2.25.1), ten synthetic cases, one file, no renames, mode changes,
  untracked files, `--intent-to-add` or `diff.algorithm`. Ten cases characterise a
  mechanism, not a distribution.
- The demand-side instrument is one platform's issue search, rate-limited after six of
  ten queries, read at 0.033–0.067 precision by a classifier that missed the strongest
  row in the sample. **The hand-read `yes-line` rows are individually cited; the
  0.016–0.066 rate is a range across two readers, not a measurement of prevalence.**
- Two readers, κ = 0.734 three-way and 0.889 collapsed — but the `yes-line` Jaccard is
  0.25 and all five disagreements sit on the coordinate-versus-operation boundary, which
  is exactly where the claim lives. Reader 1 read a truncated view, which reader 2
  showed changes four labels including one `yes-line` call.
- No population measurement was possible on Stack Exchange at all: `/info` returned
  `400 too many requests from this IP, more requests available in 43352 seconds`. The
  pre-named Pool B (15 phrasings × 2 sites, with its negative control and denominator
  control) is **unrun**, and remains the cheapest next action once the window opens.
- `filterdiff` was installed from a Debian `.deb` and run at its default settings.
  **A stronger shell route exists and was not tried**: `--lines` names the *original*
  file's line, so pairing it with something that names the working tree's line is the
  obvious competitor, and `stg` is that something. The 12/30 measures `filterdiff`
  alone, not the best shell pipeline.
- Prior art was found by three primary sources and two code indexes. GitHub code search
  answered 401 (authentication required), grep.app 429 and codesearch.debian.net 403.
  The search was **not exhaustive**, and the web search tool was unavailable on this
  host — so E037's gap is narrowed, not closed.
- No adoption measurement, and none is possible from this host.

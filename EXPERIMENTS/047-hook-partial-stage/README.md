<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-07
-->

# E047 — do the shipped git hook runners sweep a partially-staged file's unstaged hunk into the commit?

Task T-0084. Corpus for the question: two rows of the 189-row demand corpus
E045 read, `EXPERIMENTS/045-demand-evidence/raw/issues.jsonl`.

**Question, declared before the run.** For a file with one staged hunk and one
unstaged hunk, does a hook's formatter cause the unstaged hunk's *content* to
reach the commit? The population is the shipped hook runners a user can install.

**Answer, in one line: no shipped runner in the population sweeps. The hazard is
real and byte-exact, and it survives only in hooks a user writes by hand — where
a two-line git idiom already prevents it.**

## The two rows, read verbatim first

`STATE.md` recorded this observation as next, and D077 requires reading it
before using it. Reading both rows in full inverts half of it.

**`tomada1114/nextjs-app-template#95`** — titled *"the partial-stage warning in
lefthook.yml is false"*, and it is a report that **lefthook does not have this
bug**. The repository's own `lefthook.yml` carried the warning *"Unlike
lint-staged, lefthook does not stash the unstaged half first"*. The reporter ran
it: *"the committed blob was `const a = 1;\nconst b = 2;` — formatted, and
without the unstaged marker… lefthook 2.x hides the unstaged half around a
`stage_fixed` job, exactly the way lint-staged does."* The stale thing was the
warning, not the runner.

**`Grimblaz/agent-orchestra#154`** — a hand-written `.githooks/pre-commit`.
*"The hook unconditionally re-staged the full working-tree file after
markdownlint, defeating `git add -p` partial staging. Fixed by only re-staging
if markdownlint actually changed the file (hash-object comparison)."* The hash
guard does not fix the hazard: when markdownlint **does** change the file,
`git add -- "$f"` still stages it whole. And the pull request's own review
record names the hazard exactly:

> **GH-1** (Gemini): Partial staging not preserved when markdownlint modifies file
> → ❌ Defense sustained. No regression; hash guard correctly achieves stated PR
> goal; full index-patch approach is out of scope.

So one row exonerates the tool the record blamed, and the other row is a real
instance where a reviewer raised the hazard and the author ruled it out of scope.
Neither row is evidence that a shipped runner sweeps. That is a claim to
measure, so it was measured.

## The instrument, and the two controls that keep it honest

**Oracle: bytes, nothing else.** `git show :app.js` and `git cat-file blob
HEAD:app.js`. The claim is that a specific line the user chose not to stage
appears in their commit; there is nothing to grade, score, or ask a model about.

**Fixture.** One file, `app.js`, region A staged and badly spaced, region B an
unstaged marker line six unchanged lines away — two hunks at git's default
context. Staging is arranged with no interactive command: region A is staged
while region B does not yet exist, so `git add app.js` stages exactly the hunk
region B later modifies. That is `git add -p` with the answer already known, and
it keeps every arm independent of this repository's own tooling.

**C0, the positive control.** The naive hand-written hook — format, then
`git add` the file. It must sweep. If it does not, the harness cannot detect a
sweep and every other arm's clean result is a fact about the harness. The run
exits non-zero if C0 fails to fail. **A gate that cannot fail is F010; this one
is required to fail on the arm it was built to fail on.** It swept.

**B0, the fixture control.** With no hook at all, the marker must stay out of
the commit and nothing may be reformatted. It did.

**One precondition, not two.** Whether the formatter ran is read from the
commit, the index and the worktree together. Reading one place mislabelled the
`git stash --keep-index` arm, whose stash pop restores a worktree holding the
original bad spacing while its commit holds the formatter's output. And two
properties are counted **separately**, because conflating them is how a tool
could be credited with fixing a hazard it never addressed: `swept` (did the
unstaged content reach the commit) and `fix_staged` (did the formatter's rewrite
reach the commit).

**Each runner is reached through the git hook it installs.** The hiding of
unstaged changes *is* the mechanism under test, so invoking `lefthook run` by
hand and committing with `--no-verify` would have reported a sweep for lefthook
that no user ever gets.

## What ran, and what it measured

git **2.56.0** built from source (sha256 `26c56c29…`); node v26.10.0;
prettier 3.9.9; lefthook **2.1.17**; pre-commit **4.6.2**; lint-staged **17.6.0**;
husky **9.1.7**. Full digests in [`raw/results.json`](raw/results.json).

| arm | swept | fix staged | verdict |
|---|---|---|---|
| **C0** naive shell hook | **yes** | yes | the hazard, byte-exact |
| **B0** no hook | no | no | fixture control |
| **A1** lefthook + `stage_fixed` | no | yes | clean |
| **A1b** lefthook without `stage_fixed` | no | **no** | no sweep; unformatted commit |
| **A2** pre-commit, hook stages explicitly | no | yes | clean |
| **A3** lint-staged, defaults | no | yes | clean |
| **A4** lint-staged `--no-stash` | no | yes | clean |
| **A5** husky | **yes** | yes | the hazard, byte-exact |
| **X1** `git stash push --keep-index` | no | yes | clean, no framework |

**C0's committed blob** — the whole file, both regions:

```
// fixture header
const a = 1;                              <- reformatted, as intended
...
const UNSTAGED_SWEEP_MARKER = "swept";    <- never staged
const b = 2;
```

The user's unstaged line is in the commit, and `marker_left_in_worktree` is
still true afterwards — so the file reads as modified *while its content is
already committed*. That is the shape of the bug: not an error, a silent
inclusion plus a confusing status.

**What each clean arm actually did**, from its own log rather than inferred:

- **lefthook 2.1.17** — `[lefthook] saving partially staged files`,
  `git diff --binary --unified=0 … --output …/lefthook-unstaged.patch`,
  `git stash create`, `git checkout --force -- app.js`, and the patch is
  re-applied afterwards. **And it does this without `stage_fixed` too** (A1b),
  so the hiding is unconditional in 2.x and `stage_fixed` only governs whether
  the formatter's rewrite is staged.
- **lint-staged 17.6.0** — *"Hiding unstaged changes to partially staged
  files…"* then *"Staging changes from tasks…"*, in **both** the default and the
  `--no-stash` arm; in the latter it warns *"Skipping backup because
  `--no-stash` was used. This might result in data loss."* Both arms then
  **blocked the commit** (`Prevented an empty git commit!`), so their verdict is
  read from the index; the protection fired before the commit.
- **pre-commit 4.6.2** — hides unstaged changes around the hook by default
  (`--no-stash` disables it). **This contradicted my declared prediction**: I
  expected the naive hook body reached through pre-commit to sweep like the
  pattern does elsewhere. It did not, because pre-commit's own handling runs
  first. Recorded as a prediction mismatch, not quietly dropped.
- **X1** — `git stash push --keep-index` around the formatter and
  `git stash pop` on exit. Clean, with no framework at all.

**A2 and A5 are the same hook body one layer apart.** husky supplies no staging
of its own, so its arm is the naive pattern and it sweeps; pre-commit supplies
its own, so the identical body does not. The hazard is a property of the
*pattern*, and frameworks that manage unstaged changes remove it.

## What this closes, and what it does not

**Closed as a candidate.** The hazard STATE.md ranked as the next action is not
a gap in the shipped tools. Three of the four shipped runners in the population
protect a partially-staged file by default, the fourth supplies no staging of its
own, and the plainest git idiom prevents it with two lines. The record's
"correctness failure with a byte-level oracle, named by two independent
repositories" was one repository exonerating a tool and one repository's own
reviewer raising the hazard and having it sustained as out of scope.

**Closed: the population.** Every runner that ships a partially-staged-file
mechanism was tested on bytes and none sweeps. A negative result here closes the
claim and the population actually tested; it says nothing about hooks written in
languages this experiment did not run, about codegen or `git commit -a`
rewriting the worktree, or about runners that did not install on this VM.

**Not closed: the application.** The hazard is real, byte-exact, and its
population is real — it is every repository with a hand-written formatting hook.
What is established is that it is *already prevented* by the tools and by a git
idiom, so building a tool for it would be building something the incumbents
already do.

**The one arm whose behaviour is a defect of its own.** A1b: lefthook without
`stage_fixed` formats the worktree and leaves the commit unformatted. That is
not the hazard under test and is not counted as one; it is recorded because it
is what `stage_fixed` is for, and because conflating it with the hazard would
have made lefthook look like the culprit.

## Three defects this experiment found in its own instrument

Recorded because each would have produced a *wrong answer* rather than an error,
which is the failure this repository's own records say matters most.

1. **The hunk count counted occurrences of `@@`**, and git writes two per
   header, so a correct fixture was declared broken on the first run and every
   arm stopped.
2. **Hook bodies invoked `node` from `PATH`**, which git replaces inside a
   hook; the formatter never ran, and two arms reported an *error* while having
   tested nothing.
3. **`formatter_ran` was read from the worktree alone**, which mislabelled the
   `git stash --keep-index` arm; the formatter's output was in the commit and the
   stash pop had restored the original spacing. Two of these were only visible
   because each arm declares its prediction before it runs.

## Reproducing

```bash
sh EXPERIMENTS/047-hook-partial-stage/setup.sh          # fetches, builds git, installs
python3 EXPERIMENTS/047-hook-partial-stage/harness.py   # exit 0 only if C0 swept
```

Five modules, split by invariant at the 300-line cap: `harness.py` runs the arms
and judges them, `fixture.py` is the repository every arm is measured on,
`arms.py` is each runner's real configuration, `gitenv.py` answers which git and
node, and `versions.py` records what ran. **The split was verified
behaviour-preserving**: the five modules produce `raw/results.json` identical in
every arm field, in the versions, and in both controls to the single file that
preceded them.

Everything lands under `/tmp/opencode/e047` and is removed with `rm -rf`; nothing
is installed system-wide. `E047_KEEP=1` keeps each arm's repository for reading.

**Ceilings.** One fixture, one file, one formatter, one hook event
(`pre-commit`); the staging pattern is arranged directly rather than through
`git add -p`, so a bug in git's interactive splitter is out of scope; husky is
wired by setting `core.hooksPath` rather than by running its installer, which is
a deviation; and the arms run one commit each, so a runner whose behaviour
depends on repeated commits is untested.
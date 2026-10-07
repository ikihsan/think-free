<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# In flight, part 7 — E045, and the closing of the only candidate

Split out of [`STATE.md`](STATE.md) on 2026-10-07 at the 300-line cap, and by
invariant: a reading in progress, so the reload point keeps a pointer to it
rather than the reading itself. The experiment is
[`EXPERIMENTS/045-demand-evidence/`](EXPERIMENTS/045-demand-evidence/README.md).

Parts 1–6 are earlier readings; part 6 is E046, the supply-side half of the same
question, and it is still the place to read that. **This part is the end of the
`stg` line, not a new question on it.**

## The reading

**The candidate is withdrawn, and both kills were sitting in evidence this
repository has held since E038 (E045, T-0083, F081, F082, D077).**

`STATE-next-actions.md` item 0a was the ranked top action: run six real agents
against `stg` with the line number removed from the prompt and `git diff`
withheld, to test whether "an agent that must *discover* which line changed"
exists as a population. That population came from E043's own harness. E045 asked
one question of the demand evidence instead — **does any row of it describe a
requester of that kind?** — and read all 189 unique issues in E038's cached
corpus, one row at a time, recording the requester and the specific interface the
requester says it lacks.

**0 of 189.** The reader's own count of issues about choosing which lines reach
the index is **29 (0.153)**; **28 of those carry explicit diff access, the 29th
carries GUI-implied diff access, and none carries none.** All ten automated
callers in the need rows name their diff access in their own text:
`mcp-multi-root-git#3` writes its own implementation as
`git diff HEAD -- {file}` → parse hunk headers → `git apply --cached
--unidiff-zero`; `skills#154` asks to "split one file's hunks" non-interactively,
which presupposes the hunks are known; `gah#1` is a CLI that re-diffs at `-U0`.

**Three of the four issues F064 cites are not evidence of what they were cited
for.** `sublime_merge#465` says line staging already exists and that the problem
is discoverability — from a requester who has the feature. `sublime_merge#976`
wants the diff *within* a modified line: sub-line staging, which `stg` does not
provide and does not claim. `vim-gitgutter#446` is a person in vim with a visual
selection wanting one command over it. The fourth, `mcp-multi-root-git#3`, is the
agent case, and it has diff access by its own specification.

**The instrument was measured before its output was read (D069), and it does not
carry the count either way.** The rule classifier agrees with the reader on 16 of
the 43 rows it calls the need — precision **0.372**, recall **0.552**. Its
`line-coordinate` class matches `file:line` **source citations** inside CI
transcripts rather than git staging coordinates, so 14 of its 43 rows are
unrelated issues. The record's `0.033–0.067` was the same kind of number from a
different reader; both are now attached to a measured precision rather than to a
population.

**The same reading killed the differentiator.** The 29 rows name **26 distinct
repositories**. E038 ran a prior-art check and reported **two** incumbents
(`filterdiff`, VS Code's `git.stageSelectedRanges`). Two of the twenty-six are
command-line tools that take `stg`'s coordinate and shipped before E037:

- **`gah`** (Rust, MIT, crates.io) — *"Stage specific hunks by index, content
  anchor, regex, or line range… Split hunks into smaller pieces and stage
  individual changed lines, the non-interactive equivalent of `git add -p`'s
  split and edit modes."* Its README names `stg`'s exact hard case: *"Adjacent
  changed lines can't be separated by `--split` (git keeps them in one hunk even
  at zero context) — use `--lines` to pick individual lines out of such a
  block."* It names the population E045 was chartered to validate — *"unusable
  for: AI coding agents (Claude, Copilot, Cursor) that can't interact with
  prompts"* — and ships a Claude Code plugin that makes agents use it instead of
  `git add -p`.
- **`git-hunk`** (Python, MIT, PyPI) — *"Non-interactive, programmatic
  alternative to `git add -p`"*, line-level control **Yes** in its own comparison
  table, `git-hunk stage d161935 -l 3,5-7`, and it has already run the experiment
  item 0a was built around: one agent, eight tasks, identical repository state,
  five runs per variant, graded on the exact commit partition, tree, index and
  leftovers.

Packaging was the only differentiator E041 left standing, and it goes with them:
`stg` is pip-installable, `gah` is crates-installable, `git-hunk` is
PyPI-installable, two of the three ship agent distribution, and `gah`'s address is
a **content anchor** — a single-token hash that stays stable when line numbers
shift, "chosen to be single tokens in common LLM tokenizers for maximum
efficiency" — which is strictly better addressing for an agent than the
working-tree line number `stg` uses. That is the mechanism E041 measured as
absent, arriving from outside.

**Why it was missed, stated as the rule rather than as the mistake.** E038
searched the open web for prior art and read the corpus's *titles*. The titles
are dominated by CI pipelines, project phases and "staging pixels"; the bodies
name every implementation the retrieval route could see. **The corpus already on
disk was better prior-art evidence than the search run instead of reading it,**
because a search cannot rank by "implements the thing" while an issue body can
name it. D077 requires a candidate's demand evidence to be read row by row, with
the requester and the missing interface per row, before its population is used or
ranked — which is D067 applied to demand rather than to mechanism, and which
costs one afternoon per *candidate with a named population*, not per harvest.

## What is left, and what is not

**Not closed:** the application. 29 real issues in 26 real repositories is a real
population, it is real pain, and three tools are shipping into it. A negative
result closes the claim and the population actually tested; it does not close a
domain or a discovery route.

**Left as an observation, not a candidate.** Two of the 29 rows name a difficulty
**none** of the three tools addresses: a formatter or lint hook that re-stages a
whole file and sweeps a partially-staged file's unstaged hunks into the commit.
`nextjs-app-template#95` states that the warning its own `lefthook.yml` carries is
**false**; `agent-orchestra#154` is the same class of bug in a pre-commit hook.
That is a correctness failure with a byte-level oracle — the index bytes before
and after the hook — and it is checkable against the real `lefthook` and
`pre-commit` sources rather than screened. **Two rows is not evidence for a
candidate and nothing is promoted here.** The named next action is to establish
whether the shipped hooks really do this, which is a fact that can be read or
run.

**Where `stg` stands.** In the repository, unreleased, `status: draft`, with 37
tests green against real git repositories and no mocks, an index byte-identical to
a hand-built patch's, honest exits at every boundary E039 measured, and four real
defects found and fixed by E046. That is the whole claim and it is a true one.
Full reading in [`STATE-in-flight-5.md`](STATE-in-flight-5.md) (E043) and
[`STATE-in-flight-6.md`](STATE-in-flight-6.md) (E046); the candidate record is
[`HYPOTHESES-candidates.md`](HYPOTHESES-candidates.md).
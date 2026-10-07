# E045 — read the demand evidence the candidate rests on, and ask who the requester is

<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-07
-->

Task T-0083. Corpus: `EXPERIMENTS/038-staging-prior-art/raw/requests.jsonl`, the 65
cached responses of E038's prior-art work. Verbatim re-read, no re-harvest.

**Question, declared before the read.** `STATE-next-actions.md` item 0a — the
mission's ranked top action — proposes to run six real agents against `stg`
with the line number removed from the prompt and `git diff` withheld, to test
whether the one remaining population exists. That population came from the
experiment's own harness, not from the demand evidence. **This experiment asks
one question: does the demand evidence the candidate rests on contain a
requester of that kind?** Declared failure condition: at least one corpus issue
whose requester is an automated caller and whose own text shows no diff access.

**Result, in one line: no. 0 of 189.**

## The corpus, and what it actually contains

Ten `issue:` search arms; 7 returned 200, 3 returned 403 and contribute
nothing. The 7 returning arms harvested 195 items, **189 unique issues** after
deduplication, out of a declared search universe of **3124** `total_count`
instances. That universe is the denominator the record's `0.016–0.066` rate is
a fraction of, and 195/3124 = 0.062 sits inside it — so the record's arithmetic
is reproducible. What is not reproducible is the other half: those 195 are
whatever GitHub's `in:title,body` returned, and the bulk is not about git.

Reading every row's title and the requester's own first paragraph: **29 of 189
(0.153) are about choosing which lines of a working-tree change reach the
index.** The rest are CI pipeline stages, project phases, "staging pixels",
DVC's `stage 'baz/bar'`, a Sanskrit dictionary's *stages*, coupon spam. The
phrase queries did not retrieve a phrase; they retrieved `stage` and `line` in
any order.

### The instrument was measured before its output was read (D069)

A rule classifier assigns each row a requester class and a gap class
(`raw/issues.jsonl`, reproducible via `read.py`). Against the reader's own
labels (`raw/hand-labels.tsv`, written before the classifier's output was
read):

| | value |
|---|---|
| rows the rules call the need | 43 |
| of those the reader agrees are | 16 |
| **precision** | **0.372** |
| the need by the reader | 29 |
| of those the rules missed | 13 |
| **recall** | **0.552** |

Neither figure can carry the record's `0.033–0.067` claim in either direction,
and the `line-coordinate` class in particular is measuring a different thing:
it matches `file:line` **source citations** inside CI transcripts, not git
staging coordinates. 14 of its 43 rows are unrelated issues. This is F064's
finding (precision measured before use) reproduced on a different classifier
over the same corpus, and it is why the counts below come from the reader.

## Who the requester is

Over the reader's 29 need rows:

| requester | n | diff access evidence | n |
|---|---|---|---|
| a person at a GUI or TUI diff | 19 | explicit (`git diff`, a diff pane, a diff view) | 28 |
| a script or CI caller | 6 | implied by a GUI selection | 1 |
| a coding agent or an agent's tool | 4 | **none** | **0** |

Every one of the 10 automated callers in the need rows carries explicit
evidence that it can read a diff:

- `mcp-multi-root-git#3` — writes its own implementation as
  `git diff HEAD -- {file}` → parse hunk headers → `git apply --cached --unidiff-zero`.
- `skills#154` — "As agent using `commit`, I want non-interactive way to split
  one file's hunks" — presupposes knowing the hunks.
- `claude#3` — a skill that reads an uncommitted working tree and clusters it by intent.
- `gah#1` — a CLI that re-diffs at `-U0`.
- `nextjs-app-template#95` — a `lefthook` hook running over already-staged hunks.
- `Chasma#228` — C# that hand-builds a unified diff from a line range.
- `git-autofixup#25` — reads `.git/index` directly.

**A requester without diff access is not a slow stratum of this population. It
is absent from the evidence.** `stg`'s remaining population was produced by
E043's harness.

## The four issues the record names, read in full

F064 rests on four cited issues. Read verbatim, three of them are not evidence
of what they were cited for.

**`sublime_merge#465`** — "Ability to stage individual lines in a more
discoverable way". The requester writes: *"Right now it is possible to stage
individual lines by selecting them first, and then hitting the 'Stage Lines'
button… I only discovered that this functionality existed at all while starting
to write up this issue after spending a week wishing it did not."* The request
is **discoverability of an existing feature**, stated by a requester who
already has the feature. Not a capability gap.

**`sublime_merge#976`** — "Allow more specific selection of lines to stage".
The requester wants *"the diff between the original and the changed line"*
where `stg` stages the **whole** working-tree line. This is **sub-line
staging**: a capability `stg` does not provide and does not claim. Cited as
evidence for the need it does not bear on.

**`vim-gitgutter#446`** — "Batch stage multiple hunks from visual selection /
line number range". A person in vim with a visual selection, wanting one
command to stage every hunk the selection touches. GUI, diff access by
construction.

**`mcp-multi-root-git#3`** — the only agent-named issue, and the only one the
record describes as the agent population. It asks a project to add a
`stage: { hunks: [{ file, lines: "120-180" }] }` parameter to its own MCP
commit tool, and specifies the implementation. **It has diff access by its own
specification** — `git diff` is step 1 of the diff it proposes to apply.

## The finding the read was actually for: the corpus contains the kill

26 distinct repositories have an issue about line- or hunk-level staging, and
they were all in the corpus this experiment read:

`lazygit` · `lazygitrs` · `neogit` · `magit` · `tig` · `GitUp` · `gitahead` ·
`gitx` · `sourcegit` · `sublime_merge` · `zed` · `rstudio` · `vscode` ·
`vscode-neovim` · `vim-gitgutter` · `spacemacs` — plus four command-line or
tooling repositories.

E038 ran a prior-art check and reported **two** incumbents (`filterdiff`,
VS Code's `git.stageSelectedRanges`). Two of the twenty-six are command-line
tools that take the coordinate `stg` exists to take. Both READMEs were fetched
on 2026-10-07 and are kept verbatim under `raw/sources/` (`gah-README.txt`,
`git-hunk-README.txt`), which is where E038 already kept the primary-source
bytes a prior-art verdict is read from:

**`gah`** (ThatXliner/gah, Rust, MIT, on crates.io) — *"Non-interactive
hunk-based staging for git. Stage specific hunks by index, content anchor,
regex, or line range… Split hunks into smaller pieces and stage individual
changed lines, the non-interactive equivalent of `git add -p`'s split and edit
modes."* Its own documented hard case is `stg`'s: *"Adjacent changed lines can't
be separated by `--split` (git keeps them in one hunk even at zero context) —
use `--lines` to pick individual lines out of such a block."* Its address is a
working-tree line range: `gah add src/main.rs --lines 100-150`. And it names
the population E045 was chartered to validate — *"unusable for: **AI coding
agents (Claude, Copilot, Cursor) that can't interact with prompts**"* — shipping
a Claude Code plugin that makes agents use it instead of `git add -p`.

**`git-hunk`** (wkentaro/git-hunk, Python, MIT, on PyPI) — *"Non-interactive,
programmatic alternative to `git add -p`"*, comparison table line-level control
**Yes**, `git-hunk stage d161935 -l 3,5-7`, and it has already run the
experiment item 0a was built around: one agent, eight tasks, identical
repository state, five runs per variant, with and without its bundled skills,
graded on the exact resulting commit partition, tree, index and leftovers.

Two consequences, and they are separate:

1. **The population is absent from the demand evidence** (0 of 189), and the
   requesters who do exist are served by 26 incumbents.
2. **The differentiator is prior art in two published, installable,
   agent-distributed command-line tools** — and the mechanism's remaining
   edge, a content *anchor* that is stable when line numbers shift and chosen
   as a single common-LLM-tokenizer token, is strictly better addressing for
   the agent caller than the working-tree line number `stg` uses. That is the
   same mechanism E041 found absent, arriving from outside.

## What this closes and what it does not

**Closed.** Item 0a's population is invented, so the experiment is not run.
`stg` is withdrawn as a candidate on prior art found inside the record's own
corpus, and the packaging fallback E041 left standing is gone with it: `stg` is
pip-installable, `gah` is crates-installable, `git-hunk` is PyPI-installable,
and two of the three ship agent distribution. The whole surviving claim is the
one the record already reduced it to — a correct tool — and it is now a correct
tool with a measured absence of population (F081, F082, D076).

**Not closed.** The application — deterministic partial staging for callers that
cannot drive a TUI — is real: 29 real issues in 26 real repositories, two
shipped tools, one of them shipping to agents through a plugin. A negative
result closes the claim and the population actually tested; it does not close
the application or the domain.

**Left as an observation, not a candidate.** Two of the 29 rows are about a
difficulty *none* of the three tools addresses: a formatter or lint hook that
re-stages a whole file and sweeps a partially-staged file's unstaged hunks
into the commit (`nextjs-app-template#95` states the warning its own
`lefthook.yml` carries is **false**; `agent-orchestra#154` hits the same class
of bug). That is a correctness failure with a byte-level oracle, named by two
independent repositories, and it is worth a cheap check against the real
`lefthook` and `pre-commit` sources. **Two rows is not evidence for a
candidate** and none is promoted here.

## Reproducing

```bash
python3 EXPERIMENTS/045-demand-evidence/read.py     # exits 0, prints every count above
```

Three modules, split by invariant at the 300-line cap: `read.py` is the
reading (corpus in, one labelled row per issue out, `raw/issues.jsonl` written),
`rules.py` is the classifier whose precision is 0.372, and `report.py` renders.
The split was checked to be behaviour-preserving: the rewritten `read.py`
produces `raw/issues.jsonl` byte-identical to the session's own run, and the
same stdout.

Single reader, no second coder. The 29 need rows are a hand labelling with the
row index, the requester, the diff-access evidence and the requested interface
recorded per row in `raw/hand-labels.tsv`, so any reader can disagree with a
specific row rather than with a summary. Ceiling on this experiment: one
reader's labels, and GitHub's ranking means the corpus is a top-30-per-query
slice, not a sample of the 3124.
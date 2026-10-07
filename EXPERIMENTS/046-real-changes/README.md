<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-07
-->

# E046 — `stg` on real repository changes: results

`observed` 2026-10-07, session 2026-10-06-016, VM `instance-20260717-0947`,
git 2.25.1, Python 3.8.10. Question, referee, controls and kill conditions are
declared in [`PROTOCOL.md`](PROTOCOL.md). Raw rows:
[`raw/results.jsonl`](raw/results.jsonl); case manifest with commit and blob
ids: [`raw/manifest.jsonl`](raw/manifest.jsonl).

## Population

**114 real file changes from real commits** in three real repositories, newest
800 commits each, in nine strata chosen to be the shapes E037–E042 declared
untested. Every case records repository, commit sha, path, both blob ids, both
modes and the real hunk count, so any row can be re-derived with `git` alone.

| stratum | cases | what it is |
|---|---|---|
| `ordinary` | 15 | a content modification |
| `many_hunks` | 15 | ≥ 8 separate hunks at context 3 |
| `crlf` | 9 | pre-image has CRLF line endings |
| `no_final_newline` | 15 | pre-image does not end in a newline |
| `new_file` | 15 | a file the commit created |
| `pure_rename` | 15 | a rename with identical content |
| `rename_modify` | 12 | a rename with an edit |
| `delete` | 15 | a file the commit deleted |
| `mode_change` | 3 | a file's mode changed with its content |

**Declared selection effects.** UTF-8-decodable files only, so binary and
non-UTF-8 files are under-represented; newest-first, so the corpus skews recent;
strata are chosen by *shape*, not by whether `stg` handles them. 23 entries were
skipped and logged with reasons in [`raw/skips.jsonl`](raw/skips.jsonl)
(9 `identical`, 12 `not_utf8`, 2 `too_big`).

## Instrument

Two controls, both green on every run reported here:

- **Positive control** — the same judge over E038's 30-row matrix (10 cases × 3
  `diff.context` values): **30/30 byte-exact**.
- **Negative control** — 24 wrong index states built directly with `git apply`
  (nothing staged; every change staged rather than the requested one; a line git
  never reported; the requested run with an extra line), one skipped because it
  reproduced the correct index: **17 of 17 rejected, none read `sound`**.

Three earlier versions of the negative control are recorded in PROTOCOL.md
because two of them measured the tool instead of the referee.

## What the first run found: four defects, all on real input

None of the four is reachable from a synthetic single-file case of the kind
E037–E042 used. All four were in the released source of `stage-lines/`.

### F076 — no line of any new file could be staged at all

**15 real file-creation commits, 435 addresses, 0 staged.** `stg stage f:12` on a
new file exited 2 with `git apply refused the patch: error: f: already exists in
index` — and exited 2 the same way whether or not `git add -N` had been run
first, because with intent-to-add in place git's own patch names `/dev/null`
and `git apply --cached` refuses to create a path the index already holds.

`git` itself has no such limit: a patch naming the path on both sides is
accepted and leaves the index holding exactly the addressed lines. Creating a
file is the most common thing there is to do in a repository, so this was the
largest single gap found in the artifact, and it was invisible to ten synthetic
cases because none of them created a file.

**Fixed** in `stagelib.FilePatch.render`: a patch for a new file names the path
on both sides and, when more than one change is sent at once, carries them as a
single hunk. Separate hunks are wrong there — each carries `-0,0 +N,1` and
applied together they land in reverse, so `split --all` on a three-line new file
staged `three two one` (measured, then fixed).

### F077 — one address could name two changes and stage both

A real commit in this repository (`7c7ef912`, `STATE-next-actions.md`). Two
different changes answered to line 80: an 8-line deletion, anchored to the line
whose content moved up, and a 1-line insertion that had landed on exactly that
line. `stg stage STATE-next-actions.md:80` removed eight lines **and** added
one, printed the coordinate twice, and exited 1. `stg list` printed
`STATE-next-actions.md:80` twice with nothing to tell them apart. 8 address rows
across 4 cases.

**Fixed** in `stagelib.FilePatch`: a file now assigns one line per change —
changes that occupy a line claim it, a deletion keeps its documented address
unless that line is taken — and a single-line request returns at most one
change. `stg list` and `stg stage` read the same assignment, so the listing
stays a truthful map of what addresses what.

### F078 — an address that could not change anything, reported as success

One real jq commit (`a19efdd4`, `src/lexer.c`, a generated table rewritten).
**9 of that file's 190 addresses** were a pair that removed a line and added the
identical line back: git's `-U0` output pairs removes with adds positionally,
and in a large rewrite the pairing lands a line against itself. `stg
stage src/lexer.c:597` exited 1 and printed `stage src/lexer.c:597` while
leaving `.git/index` byte-identical to HEAD.

**Fixed** in `stagelib_split._split_run`: a pair that replaces a line with
itself is not a change and is no longer listed.

### F080 — two lines silently merged into one, reported as staged

A real `psf/requests` commit (`e9b1217c`, `src/requests/packages.py`), a file
whose last line has **no newline**. Two lines were inserted immediately above
that unterminated line. `stg stage src/requests/packages.py:28` — the second of
the two — exited 1 and left the index with the new text glued onto the previous
line, two logical lines merged into one. `git apply --cached --unidiff-zero`
cannot express a terminated line before an unterminated one and places it at the
end instead, with exit 0; reproduced by hand with the patch alone, so it is git's
placement rule and not `stg`'s arithmetic.

**Fixed by refusing rather than answering**, because no patch shape does the
right thing: `stg` names the case and points at `git add` for the file. The one
address this costs is visible in the results below as a `refused` row.

## What the corpus says after the fixes

Same 114 cases, same two controls, all four defects fixed:

```
positive control: 30/30 rows exact
negative control: 17/17 wrong index states rejected (1 not wrong, skipped)

verdict by stratum (address rows):
  crlf               sound=27
  many_hunks        sound=803
  mode_change        sound=68
  new_file          sound=435
  no_final_newline  refused=1  sound=81
  ordinary           sound=55
  rename_modify     sound=145

completeness: 81 of 81 applicable cases reproduce the post-image
```

**1,615 addresses, 1,614 staged exactly as addressed, 1 refused by name**, and no
mis-staging anywhere. Completeness is checked only where the replay is faithful:
`git add` on the replayed path must itself reproduce the post-image, and 81 of the
114 cases pass that bar — the 33 that do not are the pure renames and the
deletions, which have no line-addressable change at all. Every row records whether
the check applied, so nothing is silently dropped from either side.

The strata that E037–E042 declared untested and that this corpus covers are now
measured rather than assumed: renames, mode changes, CRLF, missing final
newline, many-hunk files, new files, deletions, multi-file commits. Binary files
are still not covered — they are excluded by the UTF-8 eligibility rule and by
`stg list`'s own refusal with a named error, which is a behaviour E039 measured
rather than a gap.

## What this cannot settle

KILL-Q — does anyone want this — is untouched. This is a supply-side measurement
of a candidate's artifact against real input; the open question is demand-side,
and nothing here may be reported as evidence of adoption.

The candidate's mechanism differentiation stays falsified (E041, E042): a
~180-line script implementing the same algorithm matches `stg`. What changed is
that the packaging claim — *a tool you can trust on your actual changes* — was
unmeasured until now, and **it did not hold**: four of the most common real
shapes were broken, one of them corrupting the index. That is a result about the
artifact, and it is the argument for running the real-corpus check before any
release rather than after ([`DECISIONS-SCREENING-12.md`](../../DECISIONS-SCREENING-12.md),
D075).

## Reproduce

```bash
python3 EXPERIMENTS/046-real-changes/harvest.py \
    /home/ubuntu/think-free think-free https://github.com/ikihsan/think-free \
    /tmp/opencode/e043-corpus/requests requests https://github.com/psf/requests \
    /tmp/opencode/e043-corpus/jq     jq      https://github.com/jqlang/jq
python3 EXPERIMENTS/046-real-changes/run.py \
    --repo think-free=/home/ubuntu/think-free \
    --repo requests=/tmp/opencode/e043-corpus/requests \
    --repo jq=/tmp/opencode/e043-corpus/jq      # ~9 min, exits 0
python3 -m unittest discover -s stage-lines    # 37 tests
```

The case bytes are read from the repositories rather than copied here: the
manifest records the commit and both blob ids, so `git show` reproduces them and
there is no second copy to disagree with the first. Pass `--repo LABEL=PATH` (as
above) or write `harvest.py --fixtures DIR` to cache them.

`triage.py <case_id substring> [anchor] [--repo L=P]` reproduces one row in isolation and
prints both texts around the address, what was declared, and what git then said.
Each of the four findings was isolated this way before it was fixed.
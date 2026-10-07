<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-07
-->

# E048 — when a formatter rewrites a partially-staged file, can the user see the worktree/commit disagreement?

Task T-0084's follow-on. E047 measured what the shipped hook runners do to
the bytes and left open what the user can *see* afterwards: in the arm where
the formatter ran but the commit kept the old spacing, is that visible before
the user trips over it?

**Question, declared before the run.** After a partial-stage + format-hook
run, does `git status`/`git diff` show the formatting disagreement, or does
HEAD silently disagree with a worktree that looks formatted?

**Answer, in one line: in eight of nine configurations the disagreement is
visible at the shell or the commit is blocked outright; in exactly one —
lefthook without `stage_fixed` — the worktree is formatted and `git status`
shows nothing about it, and only `prettier --check` on HEAD reveals that the
committed bytes were never formatted.**

## The instrument

E047's harness, unchanged in its E047 measurements (`swept`, `fix_staged`,
`formatter_ran`, same fixture, same controls, same arm predictions — all
nine verdicts match E047's bytes), plus one new reading per arm:

- `head_formatted` — `prettier --check` on the blob at `HEAD:app.js`
- `worktree_formatted` — `prettier --check` on the worktree file
- `status_porcelain` — what `git status --porcelain` prints
- `disagreement` — the defect shape: worktree formatted, HEAD not

The fixture and the control logic are E047's: C0 (naive hook) must sweep,
B0 (no hook) must show no formatter. Both held on this run.

## What ran, and what it measured

Same environment as E047 (git 2.56.0 built from source, node v26.10.0,
prettier 3.9.9, lefthook 2.1.17, pre-commit 4.6.2, lint-staged 17.6.0,
husky 9.1.7; digests in `raw/results.json`).

| arm | HEAD formatted | worktree formatted | `git status` | disagreement |
|---|---|---|---|---|
| C0 naive hook (control) | yes | yes | *(clean)* | no |
| B0 no hook (control) | no | no | `M app.js` | no |
| A1 lefthook + `stage_fixed` | yes | yes | `M app.js` | no |
| **A1b lefthook, no `stage_fixed`** | **no** | **yes** | `M app.js` | **yes — silent** |
| A2 pre-commit | yes | yes | `M app.js` | no |
| A3 lint-staged, defaults | yes | yes | `M app.js` | no |
| A4 lint-staged `--no-stash` | yes | yes | `M app.js` | no |
| A5 husky | yes | yes | *(clean)* | no |
| X1 `git stash --keep-index` | yes | no | `M app.js` | no (inverse: dirty tree) |

Three observations survive the table:

1. **A1b is the only silent disagreement.** The user's file looks formatted,
   the commit succeeds, `git status` shows only the changes the user made —
   nothing announces that HEAD contains the unformatted bytes. The only shell
   level detector is running the format check against the committed content
   itself. Notably the user opted out of the behaviour that causes it:
   `stage_fixed` is the documented switch, and A1 shows it produces the
   formatted commit.

2. **The blocked arms are not defects of this kind.** lint-staged (A3/A4)
   staged the formatter's output and then refused the commit
   (`Prevented an empty git commit!`), so the disagreement stays in the index,
   visible, and nothing is committed unformatted. HEAD there is the untouched
   base.

3. **X1 is the inverse reminder.** A correct formatted commit whose worktree
   still shows the old spacing reads as `M app.js` — the disagreement is
   loud in the other direction. Either way the shell shows it.

## What this closes, and what it does not

**Closed as a candidate direction.** STATE.md named this observation the next
action: read whether the formatter's rewrite/commit disagreement is a review
defect before building anything. The byte-level reading says the user-visible
surface is one lefthook configuration that already has a documented remedy,
and every other common configuration either blocks the commit or leaves the
disagreement in `git status` where the user sees it. A tool that "fixes" this
would either duplicate `stage_fixed`'s documented behaviour or watch a
filesystem for something git already surfaces. Not built.

**Not closed.** This is one fixture, one formatter, one hook event, one
commit per arm. It says nothing about: a CI format gate as the only detector
(common in practice — there it does fire on A1b's commit); runners written in
languages not tested; or editors that reformat on save and never go through a
hook. The silent-A1b shape is also exactly what a CI gate exists for, so the
honest statement is: locally silent, caught by the standard remote gate.

**One instrument note, recorded rather than dropped.** The first version of
this README's table read `head_formatted=True` for A3/A4; the cause was an
empty-string blob being treated as a present blob and prettier --check
passing an empty file. The stored bytes were re-read, the bug fixed, and the
table above is from the second run. The E047 fields in the same file were
unchanged between the two runs, which is the check that the added reading did
not perturb the old one.

## Reproducing

```bash
sh EXPERIMENTS/048-formatter-review/setup.sh          # reuses E047's root
python3 EXPERIMENTS/048-formatter-review/harness.py   # exit 0 only if C0 swept
```

`gitenv.py` reads `E047_ROOT` (default `/tmp/opencode/e047`); on this VM the
E047 environment is still in place, so the harness runs without a rebuild.
All six modules are E047's split plus `review.py` — split out of
`harness.py` at the 300-line cap, owning the `review_defect()` reading;
`harness.py` keeps the E047 arm-running oracle. **Ceilings:** one fixture, one file, one formatter,
one hook event, one commit per arm, and the "defect" defined as prettier
--check failing on HEAD's blob — a practical detector, not a formal one.

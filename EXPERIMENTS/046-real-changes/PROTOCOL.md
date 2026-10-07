<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-07
-->

# E046 — `stg` on real repository changes

Declared 2026-10-07, session 2026-10-06-016, VM `instance-20260717-0947`,
git 2.25.1, Python 3.8.10. This file is written before the run.

## Question

Every `stg` experiment so far (E037–E042) carries the same untested ceiling, in
the same words: *"does not test renames, mode changes, `--intent-to-add`,
binary files, untracked files, or multi-file scenarios"*, on ten synthetic cases.
The surviving differentiator is packaging — a tested tool a caller can trust on
**their** changes. That claim is unmeasured, and E038's stronger oracle found two
real bugs in `stg` on the synthetic corpus, so the same move is expected to pay
again on real input.

**Q1 (soundness).** For every addressable change in a real file change, does
staging that one address stage exactly that change and nothing else?
**Q2 (completeness).** Is every part of a real file change reachable — does
staging all of a file's addresses reproduce the post-image byte-for-byte?
**Q3 (reach).** Which real change *shapes* can stg address at all?

## Population

Real commits, harvested from three real repositories, in eight strata chosen to
be the shapes the ceiling names:

| stratum | real-world shape |
|---|---|
| `new_file` | a file created in the commit — untracked in the working tree |
| `rename_modify` | a file renamed and edited (similarity < 100%) |
| `mode_change` | a file's mode changed together with its content |
| `delete` | a file deleted |
| `many_hunks` | a change with ≥ 8 separate hunks at context 3 |
| `crlf` | pre-image contains CRLF line endings |
| `no_final_newline` | pre-image does not end in a newline |
| `ordinary` | a content modification, strided deterministically |

Sources: this repository (575 commits), `psf/requests`, `jqlang/jq`
(1,955 commits). Each case records repository, commit sha, path, both blob
shas, both modes, and the real diff, so any row can be re-derived with `git`
alone. Selection is deterministic (newest-first within each stratum) and every
skip is logged with its reason.

**Declared selection effects.** Only files that decode as UTF-8 are eligible, so
this corpus under-represents binary and non-UTF-8 files; the commit walk is
newest-first, so the corpus skews recent; the strata are chosen by *shape*, not
by whether `stg` handles them.

## Instrument

**The referee is `git`, not `stg`'s parser, and it is coordinate-free.** After
one address is staged the harness reads three git outputs and requires all of:

1. the patch now staged (HEAD to index) carries line contents that git itself
   reported as unstaged *before* the request — a tool cannot stage something git
   did not offer;
2. that patch's added and removed line counts equal the counts `stg list --json`
   declared — over-staging is caught by counting, not by position;
3. applying the remainder (index to working tree) with `git apply
   --unidiff-zero` reproduces the working tree byte for byte — an under-staging
   leaves a remainder that no longer applies.

Coordinates are deliberately **not** part of the test. `git diff`'s hunk header
for an insertion inside a run of adjacent changes anchors its old side wherever
the arithmetic lands, so header equality is a placement convention and not a
property of content; requiring it produced 55 false failures on rows that were
byte-exact. Both real bugs E038 found were content bugs, and all three properties
above see content.

**Positive control.** The same oracle runs over E038's 30-row case matrix
(10 cases × 3 `diff.context` values) and must return 30/30 correct. If it does
not, the instrument is wrong and the run is void — not `stg`.

**Negative control.** The oracle must reject a known-wrong index state. For each
of E038's first six cases, four wrong states are built with `git apply` directly
and handed to the judge: nothing staged, every change in the file staged rather
than the requested one, a line git never reported unstaged, and the requested run
with an extra line. **No wrong state may read `sound`.**

*Written before the run, after the controls were first coded, and revised twice
before any real-change row was produced. The revisions were all in the same
direction: the first version asked `stg` for a wrong line and called a refusal a
failure, which punishes correct behaviour; the second asked for a line no change
answers to, so `stg` refused all twelve and the oracle was never consulted at
all. Building the wrong state with `git apply` tests the oracle instead of the
tool. One injection — "stage everything" on a file with a single change — is
skipped when it reproduces the correct index, since counting it would measure
nothing.*

**Completeness control.** For each case, staging every address in one go must
leave the index blob byte-identical to the post-image.

## Baseline

The strongest accessible alternative is not `git add -p` here: E041 and E042
already measured it (12/30 and 2/6), and E041's finding is that a ~180-line
script matches `stg` exactly. This experiment's comparison is therefore **not**
against another staging tool. It is against the only baseline that can falsify a
packaging claim: *git itself*. If `git apply --cached` can do what `stg` refuses
to do, `stg` is a worse version of something git already has, and packaging
does not save it.

## Declared outcomes, decided in advance

- **Any address whose staged content differs from the declared change, at any
  exit code 0 or 1** → silent mis-staging. `stg` is **not release-ready**, each
  occurrence is a named bug with a reproducer, and the release decision is
  deferred until each is fixed and the corpus re-run clean.
- **Any real file change where the addresses cannot reproduce the post-image**
  → an unreachable change exists. Same consequence.
- **Any shape `stg` cannot address at all, where git can** → a named gap, with
  the exact command a caller would have to run by hand recorded beside it. A
  gap that costs one standard git incantation is a documentation fix; a gap that
  costs bespoke plumbing is a mechanism defect.
- **Oracle positive control < 30/30 or negative control < 6/6** → the run is
  void. Nothing about `stg` may be concluded from it.

`run.py` exits 3 when an *instrument* control fails, and 0 otherwise: the
real-change rows are data, and a failing kill gate must not be laundered into a
green exit code. The verdict is written by hand in `README.md` and nowhere else.

## What this cannot settle

KILL-Q — does anyone want this — is untouched by this experiment. It is a
demand-side measurement and this is a supply-side one. Nothing here may be
reported as evidence of adoption.
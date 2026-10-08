<!-- origin-meta
owner: FAILURES.md
status: active
last-verified: 2026-10-07
-->

# Findings 31 — the hook hazard the mission ranked next is prevented by every
# shipped runner in the population

`observed` 2026-10-07, session 2026-10-07-003, VM `instance-20260717-0947`.
Evidence: [`EXPERIMENTS/047-hook-partial-stage/`](EXPERIMENTS/047-hook-partial-stage/README.md).

Split out of [`FAILURES-findings-30.md`](FAILURES-findings-30.md) on 2026-10-07
at the 300-line cap. **Identifiers are stable across all findings files**; F084
was not renumbered.

## F084 — The hook hazard the mission ranked as its next action is prevented by
every shipped runner in the population, and by a two-line git idiom

**What happened.** T-0084, E047. For a file with one staged hunk and one unstaged
hunk, does a hook's formatter cause the unstaged hunk's *content* to reach the
commit? Measured on bytes — `git show :app.js` and `git cat-file blob HEAD:app.js`
— against real runners at current versions: git 2.56.0 built from source, node
v26.10.0, prettier 3.9.9, **lefthook 2.1.17, pre-commit 4.6.2, lint-staged 17.6.0,
husky 9.1.7**.

| arm | swept | formatter's fix staged |
|---|---|---|
| C0 naive shell hook (positive control) | **yes** | yes |
| B0 no hook (fixture control) | no | no |
| A1 lefthook + `stage_fixed` | no | yes |
| A1b lefthook without `stage_fixed` | no | **no** |
| A2 pre-commit, hook body stages explicitly | no | yes |
| A3 lint-staged, defaults | no | yes |
| A4 lint-staged `--no-stash` | no | yes |
| A5 husky | **yes** | yes |
| X1 `git stash push --keep-index` | no | yes |

**The hazard is real and byte-exact.** C0's committed blob contains
`const UNSTAGED_SWEEP_MARKER = "swept";`, which was never staged, and the
worktree still shows the marker afterwards — so the file reads as modified while
its content is already committed. Not an error: a silent inclusion plus a
confusing status.

**But no shipped runner produces it.** lefthook logs `saving partially staged
files`, `git stash create`, `git checkout --force`, and re-applies the patch —
**and does so without `stage_fixed` too**, so the hiding is unconditional in 2.x
and `stage_fixed` only decides whether the formatter's rewrite is staged.
lint-staged logs *Hiding unstaged changes to partially staged files* in both the
default and the `--no-stash` arm. pre-commit hides unstaged changes around the
hook by default. A2 and A5 are the **same hook body one layer apart**: husky
supplies no staging of its own and sweeps; pre-commit supplies its own and does
not. The hazard is a property of the pattern, and frameworks that manage
unstaged changes remove it.

**What this rules out.** The hazard as a candidate. The record described "a
correctness failure with a byte-level oracle, named by two independent
repositories"; reading both rows verbatim, as D077 requires, shows one row
(`nextjs-app-template#95`) *exonerating* lefthook — it is a report that 2.x hides
the unstaged half, and the stale thing is the repository's own warning — and one
row (`agent-orchestra#154`) whose own review record names the hazard and records
**`GH-1 … Defense sustained`**, the author ruling the index-patch fix out of
scope. Two rows, and they disagree about the premise the record drew from them.

**What this does not close.** The hazard's population is real — every repository
with a hand-written formatting hook — and the hazard is real; what is
established is that the shipped tools and one git idiom already prevent it, so a
tool built for it would duplicate them. Nothing here speaks to hooks in
languages this experiment did not run, to codegen or `git commit -a` rewriting
the worktree, or to runners that did not install on this VM.

**The prediction that failed, recorded rather than dropped.** I declared A2 would
sweep, reasoning that the naive hook body sweeps wherever it appears. It did not,
because pre-commit's own unstaged-change handling runs first. Two other arms were
mislabelled by the instrument itself before that: a hunk count that counted
occurrences of `@@` where git writes two per header, and hook bodies that invoked
`node` from a `PATH` git replaces inside a hook, so the formatter never ran and
two arms reported an error while having tested nothing.

**Evidence:** [`EXPERIMENTS/047-hook-partial-stage/README.md`](EXPERIMENTS/047-hook-partial-stage/README.md),
`raw/results.json` with per-arm blobs, logs and versions,
`python3 EXPERIMENTS/047-hook-partial-stage/harness.py` exits 0 and non-zero
otherwise (`origin task verify T-0084` → exit 0).

## F085 — The formatted-worktree / unformatted-commit disagreement is visible in
every configuration except lefthook without `stage_fixed`, and there it is caught
by the standard format gate

**What happened.** E048, same fixture, same controls, same arm predictions as
E047, plus three new readings per arm: `prettier --check` on the `HEAD` blob, on
the worktree file, and `git status --porcelain`. All nine E047 verdicts reproduced
unchanged, which is the check that the added reading did not perturb the old one.

| arm | HEAD formatted | worktree formatted | visible via |
|---|---|---|---|
| C0 / B0 (controls) | — | — | expected |
| A1 lefthook + `stage_fixed` | yes | yes | `M app.js` (the marker only) |
| **A1b lefthook, no `stage_fixed`** | **no** | **yes** | **nothing — silent** |
| A2 pre-commit | yes | yes | `M app.js` |
| A3 / A4 lint-staged | yes (base) | yes | `M app.js` + commit blocked |
| A5 husky | yes | yes | clean |
| X1 stash `--keep-index` | yes | no | `M app.js` (inverse direction) |

**Why it is a failure.** The candidate direction STATE.md selected died by being
measured: the disagreement between a formatted worktree and an unformatted
commit is a review defect only when nothing shows it, and that holds for one
configuration — the one whose remedy (`stage_fixed`) ships in the same tool and
whose commit a CI format gate fails. In every other configuration the shell
already prints it. A tool watching for this would duplicate a documented flag
or a gate repositories already run. Not built.

**Evidence:** [`EXPERIMENTS/048-formatter-review/README.md`](EXPERIMENTS/048-formatter-review/README.md),
`raw/results.json` with per-arm blobs, checks and statuses.

## F086 — A pinned lockfile is a strong witness on PyPI: 0 of 421 pinned
versions yanked or absent, 0 of 3800 recorded artifacts gone, over a
~9-month window

**What happened.** E050 (T-0086) tested E2's registry-breakage
mechanism on E049's population: ten major Python projects' lockfile
snapshots from 2025-09-16 to 2025-12-31 — 421 unique registry-pinned
(name, version) pairs and 3800 recorded sdist/wheel URLs. Q1: every
pinned version is present on PyPI today, none yanked. Q2: every
recorded artifact URL still resolves. Q3: E049's fixed-requirements
control re-downloaded 16 of 16 artifacts byte-identical. The positive
control ran first and recovered a real yanked version (`pip` 21.2,
2 of 2 files yanked) through the project-level metadata endpoint, so
the zero is a measurement, not an instrument failure.

**Why it is a failure.** E2's premise — a lockfile is a *weak* witness
of reproducibility because the resolution it records goes stale — had
exactly one registry-side mechanism measurable today (retraction of
pinned versions or recorded artifacts), and it does not fire in this
population. Part A's 10-of-11 closure change is project-initiated
updating, not registry movement: the registry keeps every pinned
version and every recorded byte. The temporal half (Part B) is
deterministic by construction for `==` pins, which Q3 confirms
same-day and Q2 confirms for the population's artifact availability.
There is no failure mode left for a tool to watch, so there is
nothing to build. This closes the last open action derived from E049
and with it the E2 candidate thread.

**Instrument defects found and fixed before the verdict counted**
(the first run's four "absent" hits were all artifacts, each of
which would have produced a wrong answer): pip-style extras parsed
as part of the name (`coverage[toml]`); a project's editable
self-entry in its own lock (`flask 3.2.0.dev0`) queried as a
registry version; and a format dispatcher keyed on the on-disk
filename suffix rather than the repo path, which dropped 74 of
flask's 80 blocks. Fixed in `e049format.py` with the population
rules stated there; the superseded first-run artifacts are preserved
in `EXPERIMENTS/050-registry-mechanisms/raw/superseded-first-run/`.

**Evidence:** [`EXPERIMENTS/050-registry-mechanisms/README.md`](EXPERIMENTS/050-registry-mechanisms/README.md),
`results.json`, `raw/rows/` (421 version-level API responses),
`raw/urls/` (3800 artifact-URL checks), `raw/positive_control.json`.

## F087 — Documented CLI flags do not observably drift from exposed `--help` flags in mature projects (E055 probe)

**What happened.** Session 2026-10-08 probed the suspected population
behind a docs-drift audit candidate before building it: five popular
PyPI CLI packages (black, cookiecutter, httpie, mypy, pre-commit),
install each, take `--help` over every subcommand, and compare against
`--flags` mentioned in the project's `.md`/`.rst` docs. Adjudicated
every `doc_not_exposed` row by reading its doc context.

**What was found.** Embedded help blocks track `--help` exactly (0 of
3 projects drift). Prose flag mentions "missing" from `--help` are
other tools' flags inside examples — docker, git, pip, uv, conda, gh,
pytest — essentially 100% of rows, with at most one stale entry
(`--experimental-string-processing`, black changelog churn). The
mechanism a tool would watch for did not appear in the sample where
it was most likely to appear.

**Why it is a failure.** The candidate population the probe looked for
was not observed; an implementation must first clear a noise floor of
foreign-tool flags that any naive detector will mislabel as drift.
Combined with the prior art that already syncs help blocks into
READMEs (`readme-cli-help`, `docsme`, `cli-help-from-readme`), there
is no demonstrated unserved need here. Probe artifacts preserved;
[`EXPERIMENTS/055-docs-cli-drift/README.md`](EXPERIMENTS/055-docs-cli-drift/README.md).

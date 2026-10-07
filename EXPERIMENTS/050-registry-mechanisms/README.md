<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-07
-->

# E050 — registry-side lockfile breakage (E2 mechanism test)

T-0086. E049 measured that 10 of 11 lockfile closures
changed over ~9 months, but Part A cannot separate "the
project chose to update its lock" from "the registry moved
under a pinned input". This experiment tests the
registry-side mechanisms a lockfile's own bytes cannot
protect against — the ones measurable today, without
waiting months.

**Question, declared before the run.** For every
(name, version) pinned in E049's ten PyPI-ecosystem old
snapshots (2025-09-16 … 2025-12-31), is that exact
version **yanked or absent** on PyPI today (2026-10-07)?
And does every sdist/wheel URL those snapshots recorded
still resolve?

**Why this mechanism.** A lockfile is a witness of what
installed once. The registry can retract what it published:
a yanked version still installs under an exact pin (with a
warning) but disappears from fresh resolution, and a
deleted artifact breaks a hash-pinned install outright. If
real projects' pinned versions are being yanked or deleted
at a non-trivial rate, "reproducible install from a
months-old lock" is a live failure, not a theoretical one.

**Kill gate, declared before the run.** 0 of the sampled
pinned versions yanked or absent, and every recorded
artifact URL resolving, kills the registry-breakage
mechanism at this population. E2's registry claim then
survives only as the time-gated Part B re-run (same fixed
inputs re-resolved weeks later), and no candidate is
promoted today.

**Positive control.** The instrument must recover a real
yanked version found independently through the
project-level metadata endpoint (`/pypi/{name}/json`
lists every release with per-file `yanked` flags) before
any version-level verdict counts. The control scan covers
20 high-release-frequency projects fixed before the run.

## The instrument

- Population: 10 PyPI-ecosystem snapshots from
  `EXPERIMENTS/049-lockfile-closure/raw/*_old.txt`
  (httpx, poetry, flask, starlette, tornado, urllib3,
  uvicorn, pydantic, werkzeug, scrapy). ruff's
  `Cargo.lock` is a different registry (crates.io) and is
  recorded as out of scope, not silently dropped.
- Q1: `GET /pypi/{name}/{version}/json` per unique pair —
  404 ⇒ absent; per-file `yanked` flags ⇒ yanked.
- Q2: `HEAD` per URL recorded in the six old `uv.lock`
  snapshots.
- Q3: E049's Part B control — the same fixed requirements
  re-downloaded now, sha256-diffed against the snapshot a
  later session re-runs.
- Raw evidence: `raw/` holds the positive-control record
  and the full API response for every yanked, absent, or
  unreachable case; `results.json` holds every row.

## Results

**Run 2026-10-07, session 2026-10-07-013 (T-0086).**

| check | population | result |
|---|---|---|
| Positive control | 20 projects via the project-level endpoint | **recovered**: `pip` 21.2, 2 of 2 files yanked |
| Q1 yank/absence | 421 unique pinned (name, version) pairs | **0 yanked, 0 absent, 0 errors** — 421 of 421 present |
| Q2 artifact existence | 3800 unique recorded sdist/wheel URLs | **3800 of 3800 resolve (200)** |
| Q3 Part B control | fixed requirements re-downloaded same-day | **16 of 16 artifacts byte-identical** |

**Verdict: `no-registry-breakage`** — the kill gate fired. Every
version pinned in the ten snapshots is still on PyPI, un-yanked,
and every artifact byte those snapshots recorded still resolves.

**Instrument defects found and fixed before the verdict counted**
(the first run's four "absent" hits were all artifacts, and each
defect would have produced a wrong answer):

1. pip-style requirements write extras in the name
   (`coverage[toml]==7.10.6`); `[extras]` is not part of the
   PyPI name — a false absence.
2. A project's own lock carries itself as an editable package
   (`flask 3.2.0.dev0`, `source = { editable = "." }`); that
   version was never on the registry — a false absence.
3. The format dispatcher keyed on the on-disk filename suffix
   (`*_old.txt`) instead of the repo path, so every lockfile
   fell through to the pip-style parser and dropped 74 of
   flask's 80 blocks — a population undercount.

The superseded first-run artifacts are preserved in
`raw/superseded-first-run/`. The fixed parsers and their
population rules live in `e049format.py`; the corrected
population is 421 registry-pinned pairs (5 local/workspace
entries excluded) and 3800 artifact URLs.

## What this does and does not show

- **Observed:** on PyPI, across ten major projects' lockfiles
  over a ~9-month window, the registry retracted **nothing** a
  lockfile pinned: 0 of 421 versions yanked or absent, 0 of
  3800 recorded artifacts gone, and the same pinned inputs
  re-downloaded to identical bytes.
- **Not measured:** the temporal half of Part B over months
  (deterministic by construction for `==` pins, given Q2);
  crates.io (ruff's `Cargo.lock` is a different registry and
  was out of scope); unpinned/range constraints, where fresh
  resolution *does* move — but that is a project choosing to
  update, which Part A already measured as 10 of 11.
- **Ceiling:** 10 snapshots, one path per repo, one point in
  time, PyPI's JSON API and file host as the only registry
  interfaces, one platform's wheel selection for Q3.

## Verdict

**Kill gate fired: `no-registry-breakage`.** E2's
registry-breakage mechanism — the one half measurable today —
is dead at this population. A pinned lockfile on PyPI is a
*strong* witness: every pinned version and every recorded
artifact byte survives the ~9-month window. E2's remaining
reading ("lockfiles go stale relative to fresh resolution")
is Part A's confounded 10-of-11, which measures projects
updating their own locks, not the registry moving under them.
Nothing to build; recorded as F086.

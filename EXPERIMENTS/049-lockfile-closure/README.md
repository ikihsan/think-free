<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-07
-->

# E049 — do dependency-lockfile closures drift over time? (E2, first half)

T-0085. E2's claim: a lockfile is a weak witness of reproducibility because
the resolution it records goes stale. Two separable halves: (a) how often
users' locks actually change, (b) whether the *same* lock resolves to
different bytes later. Today measures (a); (b) is snapshotted, not answered.

**Question, declared before the run.** In the sampled projects' published
lockfiles, does the (name, version) closure change between the oldest
post-2026-01-01 commit touching the lock and HEAD (2026-10-07)?

**Answer: yes, in 10 of 11.** The counts are in `results.json`; a reader
can recount from `raw/*.txt`.

## The instrument

- 12 repos chosen by an authoritative enumeration: `GET /repos/{r}/git/trees/
  HEAD?recursive=1` filtered to top-level lockfiles (uv.lock, poetry.lock,
  requirements.txt, Cargo.lock). fastapi/fastapi's uv.lock was adopted after
  the cutoff, so it has no old snapshot; 11 comparable pairs.
- Old snapshot: oldest commit ≤ 2026-01-01 touching that path
  (`commits?path=…&until=…`). New snapshot: same query.
- Closure: set of `name==version` lines parsed from the TOML-ish package
  blocks (uv/poetry/Cargo) or pip-style `==` lines.
- Part B: fixed `requirements-fixed.txt` (requests==2.32.3, rich==13.9.4,
  httpx==0.28.1), `pip download` resolved today; 16 artifacts sha256'd into
  `results.json` under `part_b.artifacts`. Re-running the same command in a
  later session diffs (b) directly.

## What ran, and what it measured

| repo | old date | old n | new n | added | removed |
|---|---|---|---|---|---|
| httpx requirements.txt | 2025-09-16 | 15 | 15 | 0 | 0 |
| poetry poetry.lock | 2025-12-31 | 77 | 78 | 51 | 50 |
| ruff Cargo.lock | 2025-12-29 | 523 | 558 | 260 | 225 |
| flask uv.lock | 2025-11-17 | 80 | 79 | 51 | 52 |
| starlette uv.lock | 2025-11-01 | 80 | 89 | 41 | 32 |
| tornado requirements.txt | 2025-12-16 | 49 | 53 | 40 | 36 |
| urllib3 uv.lock | 2025-12-05 | 122 | 126 | 71 | 67 |
| uvicorn uv.lock | 2025-12-21 | 95 | 89 | 59 | 65 |
| pydantic uv.lock | 2025-11-21 | 145 | 168 | 70 | 47 |
| werkzeug uv.lock | 2025-11-29 | 90 | 74 | 48 | 64 |
| scrapy docs/requirements.txt | 2025-12-31 | 7 | 75 | 72 | 4 |

10 of 11 closures changed; the median is tens of entries per file,
httpx's 15-line `requirements.txt` the lone stable one. `results.json`,
`raw/` hold the commands' output; `harness.py --verify` re-reads
`results.json` and exits non-zero unless a verdict is present.

## What this does and does not show

- **Observed:** projects that publish locks *do* rewrite them, frequently.
  A lockfile is a snapshot that goes stale in months, usually within weeks.
- **Not measured:** whether the *same* declared inputs resolve to different
  artifact bytes on a later date. That is the registry-drift half of E2, and
  it needs the Part B re-run against this snapshot (same command, same
  requirements file), or a lockfile dated from months ago re-resolved today.
- **Confound, named:** Part A's diffs mix the project editing its
  requirements with upstream drift; it cannot separate them. Part B is the
  instrument that can, and it has nothing to diff until a second run.

## Verdict

First half: **drift-observed** — 10/11. The candidate's weak-witness premise
is not killed by today; E2 stays open, now with a snapshot that makes the
second half a one-command follow-up. Kill gate for E2 as a whole still
needs the Part B re-run: bit-stable re-resolution of the same inputs over
months kills the mechanism.

Ceiling: 12 repos, one path per repo, pip-style closure only (no VCS
hashes, no platform markers), two-point diff.

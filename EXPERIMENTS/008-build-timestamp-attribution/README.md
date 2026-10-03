<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-03
-->

# 008-build-timestamp-attribution

Task T-0017. The second half of E3's own falsifying experiment: build the same
source more than once, attribute every differing byte to a named cause, and
decide whether embedded timestamps are worth fixing **first**.

This document is the predeclaration. It was written and committed before
`attribute.py` existed, because a gate written after seeing the numbers is a
rationalisation — the lesson already paid for twice in this repository, in `D020`
and `D023`.

## The claim under test, in one sentence with its scope

**For a pure-Python wheel built by the builder installed on this machine,
normalising the embedded zip timestamps is sufficient to make two builds of
identical source bytes byte-identical; any other cause of byte-level
non-reproducibility is smaller than the timestamp cause.**

Scope, stated because the claim is scoped: one builder (setuptools 45.2.0 +
wheel 0.34.2 on CPython 3.8.10), pure-Python sources, Linux, this machine. It is
**not** a claim about npm, conda, Maven, or about builders not exercised here.

## Why the census was not enough

`EXPERIMENTS/007-build-timestamps/` (T-0013) measured prevalence and found that
0.965 of 200 recent PyPI wheels carry some entry date other than 1980-01-01. That
metric passes its own predeclared gate and licenses nothing: 1980-01-01 appears
only when a builder pins the DOS epoch, which almost nothing does, so the number
measures pinning rather than reproducibility. Recorded as `FAILURES.md` F010.
Prevalence without attribution is not a decision input, and attribution is the
half E3's mechanism section actually asks for: *"build the same source twice with
different `SOURCE_DATE_EPOCH` values and diff the artifact bytes"*.

## Arms

One real builder, two real configurations. Nothing is simulated and no library
code is patched.

| Arm | Configuration | What it models |
|---|---|---|
| **H** | `SOURCE_DATE_EPOCH` set to a fixed value | The state of the art: a builder that honours the reproducibility standard |
| **N** | `SOURCE_DATE_EPOCH` unset | What the census says most builders do — `wheel` 0.34.2's `get_zipinfo_datetime` falls back to each file's own mtime, so the artifact carries the checkout's mtimes |

The mechanism is read from the installed source, not assumed:
`wheel/wheelfile.py` line 27 is
`int(os.environ.get('SOURCE_DATE_EPOCH', timestamp or time.time()))`, and
`WheelFile.write` passes `st.st_mtime`. So arm N reproduces the census's
`jinja2` shape — entries carrying a working tree's modification times — using the
real builder rather than a model of one.

Within each arm, the **only** thing that differs between the two builds is the
file mtimes of an otherwise byte-identical checkout. Per-file SHA-256 of every
source file is compared before building, so "identical source bytes" is verified,
not assumed.

## Method

1. Fetch four real pure-Python sdists; record URL, size and SHA-256. Selection
   rule: classic `setup.py`, no VCS-derived version, no build-time network, small.
2. Extract each sdist twice. Set every file's mtime in one copy to
   `2021-03-04 05:06:07Z` and in the other to `2024-11-12 08:09:10Z`. Verify the
   two trees are byte-identical by content hash before building.
3. Build one wheel per (source, arm, checkout) in its own tree: `python3 setup.py
   bdist_wheel`. Six builds per source, 24 in total.
4. **Noise floor.** Two builds of the *same* tree with the *same* arm
   configuration: differing bytes counted and attributed. This separates
   "nondeterministic builder" from "timestamps".
5. **Attribution by causal patch, not by guessing.** For each differing pair,
   rewrite only the DOS date/time fields — 4 bytes in each local file header and
   4 bytes in each central-directory entry — of artifact A to artifact B's
   values, then compare again. If the patched A is byte-identical to B, then
   every differing byte was a timestamp byte, which is a proof rather than a
   correlation.
6. Report per source and pooled: differing bytes total, differing bytes inside
   timestamp fields, the residual causes when any, the noise floor, and whether
   the build is bit-reproducible within an arm.

## Negative controls, which must fail

An experiment where everything passes measures nothing. Three controls, each of
which must produce a *negative* result or the method is broken:

| Control | Expected | Why it must fail |
|---|---|---|
| **C1** patch local file headers only, leave the central directory alone | not byte-identical | If this reached byte-identity, the method could not localise a cause at all |
| **C2** patch the central directory only, leave local headers alone | not byte-identical | As C1, from the other half of the format |
| **C3** planted defect: change the content of one file between the two checkouts | residual non-timestamp difference reported and attributed | If a planted content change were reported as "timestamps only", the detector is blind and a "timestamps are the sole cause" result would mean nothing. This is a **planted** defect and is never reported as a discovered one |

C3 is planted on a separate arm, not mixed into the headline result.

## Kill gate, predeclared

Computed as specified below, before the run.

**`timestamps-first`** requires all three:

- G1. Arm N: on **at least 3 of 4** sources, patching only timestamp fields makes
  build A byte-identical to build B.
- G2. C3 fires on **every** source it was planted on: a planted content change is
  detected and attributed to a non-timestamp cause.
- G3. Arm H: on **at least 3 of 4** sources, two builds with the same
  `SOURCE_DATE_EPOCH` are bit-identical (the noise floor is zero).

**`timestamps-not-first`** if either:

- G4. On **2 or more** sources, Arm N leaves residual non-timestamp differences
  after the timestamp patch; or
- G5. On any source, a single non-timestamp cause accounts for **25% or more** of
  the differing bytes.

**`inconclusive`** if fewer than 3 sources build in both arms, or if fewer than 3
attribution pairs are produced.

Precedence: G4/G5 are checked first, because a residual cause is the stronger
finding and `timestamps-not-first` should not be masked by a pass elsewhere.

## Reading the verdict

- `timestamps-first` **supports** E3's ordering for this builder: timestamps are
  not just the most common violation, they are the *only* one here, so fixing them
  is sufficient rather than merely worthwhile. It does **not** validate E3 as a
  product direction, does not bound npm/conda/Maven, and says nothing about
  adoption — 0.965 of published wheels are still not 1980-pinned, which is an
  adoption fact the census measured and this experiment cannot explain.
- `timestamps-not-first` **narrows** E3 hard: other causes are the same size or
  larger on this builder, so "timestamps first" is the wrong ordering.
- `inconclusive` means the measurement failed, not that the claim is weak.

Arm H is an **implementation check**, not a discovery: `wheel` 0.34.2's source
states that every entry's date comes from `SOURCE_DATE_EPOCH`, so finding builds
identical confirms the installed library does what its code says (the `D021`
lesson: a result that follows from the implementation's structure checks the
implementation). The informative cell is **arm N**.

## What would make this uninformative

- One builder. The census's per-package table is the reason this matters:
  `cryptography` ships 1980-pinned wheels and `urllib3` stamps one instant per
  wheel, while `jinja2` carries checkout mtimes. A verdict from one builder is a
  bound on *that* builder, and this experiment cannot speak for the rest.
- Pure-Python sources only. Compiled extensions embed timestamps differently and
  carry a toolchain the wheel builder does not control.
- A planted control is not evidence about the world; it is evidence about the
  detector.

## Reproduce

```bash
cd EXPERIMENTS/008-build-timestamp-attribution && python3 fetch_sources.py && python3 attribute.py
```

Standard library only, plus the sdists it downloads. Both scripts write
`results.json`; `fetch_sources.py` records every input's SHA-256 so the sample
is checkable.
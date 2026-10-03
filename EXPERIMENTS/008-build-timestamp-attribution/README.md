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

---

# Results (`results.json`, 2026-10-03)

Environment as run: CPython 3.8.10, setuptools 45.2.0, wheel 0.34.2, Linux,
`python3 setup.py bdist_wheel`. Five sdists, seven builds each, 35 builds, zero
build failures.

## Gate verdict: `timestamps-first`

| Clause | Needs | Got |
|---|---|---|
| G1 arm N, timestamp patch reaches byte-identity | >= 3 of 4 sources | **4 of 4** (and 5 of 5 measured) |
| G2 planted content defect detected and attributed to a non-timestamp cause | every source | **4 of 4** (and 5 of 5) |
| G3 arm H bit-identical | >= 3 of 4 sources | **4 of 4** (and 5 of 5) |
| G4 arm N sources left with residual causes | fewer than 2 | **0** |
| G5 any source with non-timestamp share >= 0.25 | none | **0** |

## The numbers

| source | arm N differing bytes | in timestamp fields | other | patch reaches identity | arm H differing bytes |
|---|---|---|---|---|---|
| `six` 1.16.0 | 18 | 18 | 0 | yes | 0 |
| `toml` 0.10.2 | 50 | 50 | 0 | yes | 0 |
| `idna` 3.3 | 74 | 74 | 0 | yes | 0 |
| `packaging` 21.3 | 110 | 110 | 0 | yes | 0 |
| `click` 8.1.7 | 146 | 146 | 0 | yes | 0 |

Pooled: **398 of 398 differing bytes (1.0000) lie inside zip timestamp fields**,
and on every source the causal patch — rewrite the 4+4 DOS bytes per entry to
the other artifact's values — reproduces the other artifact exactly. That is a
proof that timestamps were the *only* difference, not a correlation.

**Arm H is bit-reproducible.** With `SOURCE_DATE_EPOCH` fixed, two builds from
checkouts 34 months apart produce identical bytes on 5 of 5 sources: 0 differing
bytes. This is the implementation check, and it passes.

## A second timestamp path, found by the noise floor

The noise floor was expected to be zero and was not, on three sources. Cause
identified by hand rather than guessed: the `.dist-info` files the wheel builder
*generates* are stamped with the wall clock at build time, and the DOS timestamp
has 2-second resolution. Two builds inside one tick are byte-identical; two
across a tick differ in exactly those entries:

```
six-1.16.0.dist-info/LICENSE     [2026, 10, 3, 21, 59, 36] vs [2026, 10, 3, 21, 59, 42]
six-1.16.0.dist-info/METADATA    [2026, 10, 3, 21, 59, 36] vs [2026, 10, 3, 21, 59, 42]
six-1.16.0.dist-info/RECORD      [2026, 10, 3, 21, 59, 36] vs [2026, 10, 3, 21, 59, 42]
six-1.16.0.dist-info/WHEEL       [2026, 10, 3, 21, 59, 36] vs [2026, 10, 3, 21, 59, 42]
six-1.16.0.dist-info/top_level.txt [2026, 10, 3, 21, 59, 36] vs [2026, 10, 3, 21, 59, 42]
```

So there are two timestamp routes, not one: copied source mtimes (arm N's main
effect) and build-time stamps on generated files. Both are the same *cause*, and
`SOURCE_DATE_EPOCH` removes both.

## Controls

| Control | Result |
|---|---|
| C1 patch local headers only | does **not** reach identity, 5 of 5 |
| C2 patch central directory only | does **not** reach identity, 5 of 5 |
| C3 planted content defect | `content-differs` reported, 5 of 5; 40,493–97,407 non-timestamp bytes; patch does not reach identity |

C3 names two entries, the planted file and `RECORD`, whose hash of it changed.
That is correct, and it is why "no residual cause" in the headline rows is a
result rather than a blind spot.

## What this establishes, and what it removes

**E3's ordering claim is supported for this builder**: timestamps are not merely
the most common violation, they are the only one, so normalising them is
*sufficient* for bit-reproducibility rather than merely worthwhile. F010 said
prevalence was measured and cause was not; cause is now measured.

**And that is exactly why there is nothing to build.** The remedy is
`SOURCE_DATE_EPOCH` — a documented standard that this builder already honours,
with a one-line effect. A tool that counts the violations duplicates
`diffoscope`/`reprotest`; a tool that fixes them duplicates an environment
variable. The census measured the remaining gap as an *adoption* fact: 0.965 of
recent wheels are not 1980-pinned even though the builder can pin them. Adoption
of a standard is not a new repository. E3 is recorded as a mechanism supported and
a candidate abandoned (`FAILURES.md` F012).

## Limits

1. **One builder.** setuptools 45.2.0 + wheel 0.34.2 is the only wheel builder on
   this machine. The census's per-package table is the reason that matters:
   `cryptography` ships 1980-pinned wheels, `urllib3` stamps one instant per
   wheel, `jinja2` carries checkout mtimes. Nothing here explains that spread; a
   verdict from one builder is a bound on that builder.
2. **Pure-Python sources only.** Compiled extensions embed a toolchain the wheel
   builder does not control, and their determinism is a separate question.
3. **Five sources, all small and single-repository.** Not a sample of packaging.
4. **`click` is reported but not in the gate.** The gate's denominator is four,
   fixed in the predeclaration; `click` is the fifth and is shown for completeness.
5. **Arm H is a check, not a discovery** (`wheel` 0.34.2's source already states
   where every entry's date comes from). The informative cell is arm N.
6. Nothing here measures whether anyone sets the variable, which is the fact the
   census says matters.

## First run: a control that tested nothing

The first run returned the same verdict, and it was wrong to accept. C3 planted
`src/__planted__.txt`, which none of these `setup.py` files packages, so the
"planted" artifact differed from its control only by the wall-clock stamps above;
and G2 was implemented as "the artifacts differ", which that noise satisfies on
its own. The predeclared wording was "detected **and attributed to a non-timestamp
cause**", so the code implemented less than the clause said.

Fixed by planting inside a file a real build already put in the wheel (read from
the artifact, not guessed), and by requiring a `content-differs` residual cause.
The first run is kept in `first-failure.json`; the second run is the one
`results.json` holds.
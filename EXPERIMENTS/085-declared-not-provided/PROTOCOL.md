<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-10
-->

# E085 — declared ≠ provided: the incidence of a declared distribution that does not provide the module the code imports

Declared 2026-10-10, session `2026-10-10-001`, VM `instance-20260717-0947`,
**before any repository was scanned and before any distribution was resolved.**

The prior-art check was run first (below). A feasibility probe of the
instrument was run first (below). Both are declared here so a reader can see
what was known before the measurement.

## The practical difficulty

A developer — or an agent writing code — names a dependency from memory. If
the name is a typo, `pip` refuses loudly and the cost is one line. If the name
is a *near-miss that happens to resolve to a real, different project*, `pip`
installs it, nothing warns, and the first signal is an `ImportError` or a
silently wrong API minutes or a CI cycle later.

The record already has the two halves of this, measured separately:

- **E064**: 93 of 576 plausible near-miss names resolve to a real, different
  artifact — 0.1615, CI95 [0.134, 0.194] (F099, D086).
- **E070**: 0 of 50 PyPI and 0 of 50 crates near-misses receive any "did you
  mean" warning (F103); and the silent class occurs in real user reports
  (3 B rows), though the primary denominator there is 4 rows.

**What nobody in this record has measured is the denominator-correct rate on
real code.** E064 counts mutated *names*; E070 counts *reports*. Neither
counts *declarations*. The number that decides whether a tool is worth building
is: **of the dependencies a real project declares, how often does the declared
distribution fail to provide a module the code imports, while existing on PyPI
at all?**

That is the practical difference a tool could address, and it is untested.

## Prior art, checked before naming anything (AGENTS.md non-negotiable)

Web search was unavailable on this VM (`unknown: Web search cancelled`, three
attempts), so the check was done by fetching the candidate artifacts directly,
which is stronger evidence than a search ranking (F030, F036).

| artifact | fetched | what it does |
|---|---|---|
| `deptry` 0.25.1 (`osprey-oss/deptry`) | `pypi.org/pypi/deptry/json`, `deptry.com/rules-violations/`, project README, 2026-10-10 | Rules DEP001–DEP005. **DEP001: "Python modules that are imported within a project, for which no corresponding packages are found in the dependencies."** Resolves imports against **the installed virtual environment's metadata**: the docs state deptry "will not work" installed globally "since it has to have access to the metadata of the packages in the virtual environment". Declared dependencies are `click, colorama, packaging, requirements-parser, tomli` — **no HTTP client**, so it is offline by design. |

**Verdict on prior art, stated before the run.** The checker in its obvious
form is prior art: deptry already extracts imports with `ast`, resolves each
to a distribution, and reports the mismatch. A weaker reimplementation of
deptry would be rejected without measurement.

**The residual, which is the only thing E085 may test:**

1. deptry requires the dependencies to be **installed**. It cannot run on a
   checkout before installation, in a read-only review of someone else's pull
   request, in an agent sandbox, or in a monorepo where the install is slow.
2. deptry's DEP001 message **names the module that is unprovided**. It does
   not name the distribution that provides it. The user still has to look it
   up — which is the step E064 measured at 0.1615 of plausible names.

So the candidate under test is narrow and is stated as such:
**a resolver that determines what a distribution provides from PyPI metadata
with nothing installed, and therefore reports both the mismatch and its
correct provider, before the environment exists.**

If the incidence measured below is too small to matter, this closes and no
tool is built.

## Feasibility probe, before the gates were written

The load-bearing technical risk is whether a wheel's module list can be read
without downloading it. Probe (`/tmp`, not a repository artifact): HTTP `Range`
on the last 65,536 bytes of `requests-2.34.2-py3-none-any.whl` returned
`206 Partial Content`, `Content-Range: bytes 7539-73074/73075`, and the
payload contained the zip **central directory** with every entry name visible
(`requests/adapters.py`, `requests-2.34.2.dist-info/top_level.txt`, …).

Conclusion: the central directory alone gives the top-level modules, so no
payload byte is needed. The probe is recorded here because G1 below is a claim
about that mechanism and the claim is falsifiable.

## Arms

| arm | source | what it carries |
|---|---|---|
| **A — population** | the 24 real repositories under `EXPERIMENTS/068-arxiv-spec-generator/repos/`, already on disk, fetched and pinned by E068/E069 | real declared dependencies and real `import` statements. 5,789 `.py` files, 57 requirement files |
| **B — positive controls** | 10 known name-is-not-provider pairs, recorded in this repository before this experiment | the instrument must recover independent real cases, not only what arm A produces |
| **C — negative controls** | 10 distributions that provide the module they are named after | the instrument must not fire on correct declarations |

**Arm B rows** (module imported; the name a developer would write; the
distribution that actually provides it): `sklearn`→`scikit-learn`,
`PIL`→`pillow`, `cv2`→`opencv-python`, `skimage`→`scikit-image`,
`yaml`→`PyYAML`, `bs4`→`beautifulsoup4`, `dateutil`→`python-dateutil`,
`serial`→`pyserial`, `attr`→`attrs`, `Crypto`→`pycryptodome`.

These are not invented here. `sklearn`/`scikit-learn` is E070's flagship
silent-class control and appears in E070's arm M and in Stack Overflow row
78587477 (documented in `EXPERIMENTS/070-silent-wrong-project/README.md`).

**Arm C rows**: `numpy`, `requests`, `scipy`, `pandas`, `pytest`, `click`,
`flask`, `tqdm`, `matplotlib`, `yaml`-adjacent `jinja2`. Each must be reported
as *providing itself*; a resolver that flags any of these is noise.

## Denominator, and what is excluded from it

For each repository, for each declared distribution `D` and each top-level
module `M` imported by the code, the pair is **computable** when all of:

1. `D` is parsed out of a requirement file or `setup.py` `install_requires`;
2. `D` exists on PyPI (a 200 from `/pypi/<D>/json`);
3. `D`'s wheel central directory is readable, so its provided-module set is
   known.

**Every fraction is over computable pairs.** A repository where step 1 fails, a
distribution with no PyPI record, and a distribution with no readable wheel are
**missing observations, never zeros and never denominators** (D082).

Pairs are classified:

| class | meaning | in the denominator? |
|---|---|---|
| `correct` | `D` provides `M`'s top-level package | yes |
| `wrong-distribution` | `D` exists on PyPI, does **not** provide `M`, and some other *real* distribution provides it | **yes — this is the target class** |
| `unprovided` | `D` exists, does not provide `M`, and no candidate provider was found | yes — counted and reported separately; it is deptry's DEP001 shape, not the silent-wrong-project class |
| `stdlib-declared` | `M` is a standard-library module that is also declared | excluded — deptry's DEP005 covers it |
| `covered-by-other-declared` | another *declared* distribution in the same repo provides `M` | excluded — the project still runs; this is DEP002/DEP003 territory |

The exclusion of `covered-by-other-declared` is the one judgement call that
could flatter the rate, and it is declared here: **it is excluded because a
project where another declared dependency provides the module has no failure
to report.** Both the included and excluded counts are reported.

## Gates, all declared before any repository was scanned

Every gate has a **non-vacuous passing region and a non-vacuous failing
region**, and the reachable set of each was enumerated before the run
(D088, D089 — the E069 lesson).

### G1 — instrument ceiling
The resolver determines the provided-module set for **≥ 90%** of the PyPI
distributions it queries in arm A.

*Reachable set:* distributions with at least one `bdist_wheel` on PyPI. Pure
sdists, deleted projects, and wheels whose central directory exceeds the
fetch window are missing observations, counted against the ceiling but never
recorded as "provides nothing".

*Both regions reachable:* a 100% ceiling (every distribution has a wheel) and
a 0% ceiling (the central-directory read fails universally) are both
conceivable outcomes, so the gate can fail.

### G2 — control validity, both directions
On arm B the resolver names the true provider for **≥ 8 of 10**; on arm C it
reports **0 of 10** self-providing distributions as mismatched.

*Both regions reachable:* each row has a determinate correct answer, so the
gate can fail in either direction. A resolver that returns "provides nothing"
everywhere passes neither half.

### G3 — the rate (this is the build decision)
Let `S` = `wrong-distribution` / computable pairs in arm A.

| `S` | decision |
|---|---|
| `< 0.005` | **KILL.** Not worth a tool. The line closes on measured incidence, not on a screen. |
| `0.005 ≤ S < 0.02` | **HOLD.** Report the Wilson CI95 and decide on a larger corpus. |
| `≥ 0.020` | **BUILD.** Prototype the resolver and test it against deptry. |

Thresholds chosen before the run and stated as a rationale, not a target: a
0.5% rate means roughly one wrong declaration in every 200, so a typical
50-dependency project hits it about once in four — below that, a CI gate costs
more reviewer attention than it returns.

*Both regions reachable:* `S = 0` and `S = 1` are both entirely possible from a
20-repository corpus; the corpus's 5,789 `.py` files cannot guarantee either.

### G4 — finding quality
Of a hand-read sample of **20** flagged `wrong-distribution` pairs, **≥ 16**
are true silent wrong-project cases on reading.

*Why a separate gate:* metapackages and namespace shims legitimately provide
no module, and a rate without a precision figure is not a rate (D090). If G3
passes on a population that is mostly metapackages, G4 is what catches it.

*Both regions reachable:* 20 rows are hand-read and each has a determinate
answer, so precision below 0.80 is possible and would be informative.

## What is compared against what

The strongest accessible alternative is **deptry run for real**, not a
description of it. `deptry` 0.25.1 requires Python `>=3.10`; this VM's system
interpreter is 3.8.10, and `EXPERIMENTS/069-install-test/interpreter.json`
records a uv-managed CPython 3.10.19 at
`~/.local/share/uv/python/cpython-3.10.19-linux-x86_64-gnu/bin/python3.10`.
deptry is installed into a fresh venv on that interpreter and run on the same
repositories.

The comparison is reported on three questions, and it is **not** a benchmark:

1. Can deptry run at all on these repositories (no install present)?
2. Where both run, do they find the same `wrong-distribution` pairs?
3. For each finding, which one names the correct provider?

## Ceilings, declared before the run

- The corpus is deep-learning Python from one arXiv year, fetched by E068. It
  is enriched for shadow import names relative to ordinary web development,
  which biases `S` **upward**. This is stated now so a high `S` is read as an
  upper bound on this population, not a general rate.
- Declared dependencies come from requirements files and `setup.py`. Projects
  using `pyproject.toml`/Poetry only are undercounted, and this corpus predates
  the PEP 621 norm.
- `ast` cannot resolve dynamic imports (`importlib.import_module`, `__import__`),
  so imports are a lower bound and dynamic-only dependencies read as unused.
- PyPI metadata is the **latest release** of each distribution, not the version
  a given project pins. A distribution that stopped providing a module between
  the pinned version and today is counted as a finding it may not be.
- One VM, Python 3.8 for the instrument; 3.10.19 for deptry.
- `wrong-distribution` requires finding a real provider, and PyPI has no
  reverse module index. The candidate provider set is therefore the
  name-canonicalised module name plus its PEP 503 normalised variants, which is
  exactly the assumption E064's rate rests on. Rows where the provider is found
  by some *other* route are not counted as recovered.

## Revision history

- 2026-10-10: initial declaration. Written after the prior-art check and the
  feasibility probe, both stated above, and before any repository scan.
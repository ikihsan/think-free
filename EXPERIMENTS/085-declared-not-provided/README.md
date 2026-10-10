<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: complete
last-verified: 2026-10-10
-->

# E085 — declared ≠ provided: the incidence of a declared distribution that does not provide the module the code imports

**Result: the candidate does not survive.** The instrument works and the class
is real; the class is too rare to justify a linter, and the gate designed to
decide that says so.

Session `2026-10-10-001`, VM `instance-20260717-0947`, 2026-10-10.
Protocol: [`PROTOCOL.md`](PROTOCOL.md), amended before the measurement by
[`AMENDMENT-1.md`](AMENDMENT-1.md) through
[`AMENDMENT-4.md`](AMENDMENT-4.md). Raw: `cache/`, `results.json`,
`classified-pairs.json`, `control-results.json`, `deptry-baseline.json`,
`controlled-comparison.json`, `install-proof.txt`, `silent-class-proof.txt`.

## The gates

| gate | outcome |
|---|---|
| **G1 instrument ceiling** | **met.** 538 of 578 declared distributions resolved to a module set — **0.931**, against a declared floor of 0.90. |
| **G2 control validity** | **met**, after Amendment 1 split it three ways. B1 detection 2 of 2, B2 classification 3 of 3, B2b `sdist-only-undecidable` 3 of 3, arm C **0 of 10** false flags, **B3 provider recovery 10 of 10**. |
| **G3 the rate** | **HOLD.** 6 of 500 imported modules = **0.0120**, Wilson CI95 **[0.0055, 0.0259]**. Above the 0.005 kill line, below the 0.020 build line — and the interval spans both. |
| **G4 finding quality** | **FAIL.** All 6 flagged rows hand-read: **3 are true, 3 are not. Precision 0.50**, against a declared gate of 0.80. |

## Why G4 decides it

The 6 rows, read one by one:

| # | module | sites | hand-read | verdict |
|---|---|---|---|---|
| 1 | `Bio` | 10 | PyPI `Bio` is a bioinformatics *workflow* tool shipping `biorun`; the wanted distribution is `biopython`. | **true** |
| 2 | `pynvml` | 1 | `pip install pynvml` succeeds and `import pynvml` **works** — the 13.0.1 wheel ships a `.pth` redirector, not a module, and warns it is deprecated. | **false** |
| 3 | `BDD` | 26 | `import BDD.ILP_instance_py` in LPMP_BDD is the repository's **own** built extension. | **false** |
| 4 | `MoD` | 6 | imported from a vendored LLaMA-Factory tree; PyPI `MoD` ships `mod`. | **true** |
| 5 | `vertexai` | 2 | PyPI `vertexai` ships `version`; the real provider is `google-cloud-aiplatform`. | **true** |
| 6 | `LEHD` | 32 | `from LEHD.TSP...` — the repository's **own** vendored directory, verified at the import site. | **false** |

Three of the six are my instrument's false positives: two from project-local
detection and one from a `.pth` redirector the central directory cannot see.
Correcting for precision, the true rate is **3 of 500 = 0.6%**, which is *at*
the declared kill line rather than above the build line.

**The line closes.** G3's own verdict was HOLD, and the gate that was declared
to catch a rate inflated by exactly this failure mode says the rate is mostly
artifact. Declaring a build on the uncorrected 0.012 would have been reading a
number I had already agreed in writing was an upper bound.

## What is nonetheless measured, and does not close

**The mechanism is confirmed and it is cheap.** A wheel is a zip; a zip's
central directory sits at the end of the file and names every entry. So the
complete list of modules a distribution ships is readable with **two HTTP
Range requests and zero payload bytes**, with nothing installed. It resolved
578 real declared distributions at 93.1% coverage, and it recovered the true
provider for **10 of 10** controls — the half of the problem deptry does not
attempt.

**The failure it targets is real and was reproduced by hand, not argued.**
`silent-class-proof.txt`, on this VM, CPython 3.10.19, pip 23.0.1:

```
$ pip install Crypto
Successfully installed Crypto-1.4.1 Naked-0.1.32 certifi-2026.7.22 ... urllib3-2.8.0
exit=0
$ python -c "import Crypto"
ModuleNotFoundError: No module named 'Crypto'
```

Exit 0. A different project, plus **eight of its dependencies**, installed.
`pip list` shows `Crypto 1.4.1`, so the most natural check a developer makes
says the dependency is satisfied. `pycryptodome` is never named.

**The incumbent cannot detect this class at all.** deptry 0.25.1, run for
real, not described:

| condition | deptry |
|---|---|
| 13 repos, **nothing installed** | 974 findings, **951 of them DEP001** — `numpy`, `scipy`, `sklearn` and the project's *own* package all reported "missing from the dependency definitions". Unusable. |
| project declares `sklearn`, imports it, `scikit-learn` installed | **0 findings.** A project that installs nothing at all passes. |
| same project, `sklearn` undeclared | `DEP003 'sklearn' imported but it is a transitive dependency` — **names the module, never the provider**. |

This is a real gap. It is also a gap over a condition that is rare, which is
the honest reading of the result: deptry's blind spot costs little in aggregate
because there is not much behind it.

## Why the class is rare, which is the more useful number

Of 500 scored modules in 13 repositories: **254 are correctly covered**, **152
are name collisions where installing the name actually works**, **88 fail
loudly** (33 with no such project, 55 whose project ships no wheel and, per
E070's arm M, failed the install 3 times out of 3), and **6 are silent**.

E064 measured that **16% of plausible *mutated* names** resolve to a real
different project. This measures what developers actually *declare*: right
81% of the time, loud 18%, silent 0.6%. The gap between the two numbers is the
result — a mutated name and a declared name are different populations, and
E064's rate does not transfer to declared dependencies (F108).

## Instrumentation defects found and repaired

All five were in this experiment's own code, all were found by reading output
rather than by a test, and each one moved the result. They are listed because
the third and fourth silently changed the verdict.

1. `top_level_modules` returned wheel *filenames* as module names (`attr.py`,
   `pylab.py`). Repaired before arm A.
2. `stdlib_modules` listed only files, missing every standard-library
   *package* — `asyncio`, `json`, `logging`, `email`, `unittest` — and
   `lib-dynload`. This inflated numerator and denominator: **6 findings became
   12**.
3. `project_local_modules` required `__init__.py`, so a repository's own C
   extension and vendored tree scored as third-party imports. **Two of the six
   remaining findings are this.**
4. The module name was looked up only among *declared* distributions, so a
   module that was not also a declared dependency — exactly the ones most
   likely to be unprovided — was never resolved. **This suppressed the target
   class by construction; fixing it moved the rate from a spurious KILL to the
   real number.**
5. `.data/purelib` re-rooting never fired, because the `.data` directory is
   named `<pkg>-<version>.data` and the check looked for a leading `/`.
   Repaired; it **did not change any number in this corpus**.

## Ceilings

- The corpus is deep-learning Python from one arXiv year, fetched by E068.
  Shadow import names are more common here than in ordinary web development,
  so 0.6% is plausibly an over-estimate for a typical project.
- Eleven of 24 repositories declare nothing and contribute **233 missing
  observations**, not zeros. Only 13 repositories are in the denominator.
- 6 of 500 is a small numerator: the CI95 spans both of the declared decision
  boundaries, and one row moves the verdict.
- PyPI metadata is the **latest** release, not the version a project pins.
- Only Python. `npm`, `cargo`, `crates` and `Packagist` ship the same wheel
  layout, but none was measured.
- Dynamic imports are invisible to `ast`.

## Next action

The instrument, not the linter, is what survives, and it has a use the gate
does not test: **answering "which distribution provides this module" with
nothing installed** — which deptry cannot do at all, and which the
`RELEASE-MANIFEST`-tracked prototype [`pyprovides/`](../../pyprovides/README.md)
now does. The single most useful next step is to measure whether that question
is asked often enough to matter, by counting real `ImportError` /
`ModuleNotFoundError` text that names a module and no distribution. That
denominator does not exist in this record and it is the one that decides
whether the resolver is worth carrying forward.

## Reproduce

```bash
python3 EXPERIMENTS/085-declared-not-provided/controls.py      # G2
python3 EXPERIMENTS/085-declared-not-provided/scan_repos.py     # arm A parse
python3 EXPERIMENTS/085-declared-not-provided/classify.py       # G1, G3
python3 EXPERIMENTS/085-declared-not-provided/deptry_baseline.py
python3 EXPERIMENTS/085-declared-not-provided/controlled_comparison.py
```

`cache/` holds one JSON file per distribution and is **not tracked** — it is
regenerable from PyPI and the repo already ignores E068's equivalent cache.
With it present a re-run is offline; without it, the first run needs the
network and then every later run does not. `results.json`,
`classified-pairs.json` and `control-results.json` are tracked and are the
numbers every claim above rests on.
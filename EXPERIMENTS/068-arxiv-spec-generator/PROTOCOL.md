<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# E068 — Spec generator from partial repo information for ArXiv computational papers

## Question

E067 found that only 11.8% of ArXiv computational papers with code links provide machine-runnable environment specifications (A1), while 52.9% provide none (A4). This experiment tests whether a deterministic, stdlib-only generator can produce runnable pinned specifications from the partial information available in A2/A3/A4 repos (README install instructions, unpinned requirements, pyproject.toml, poetry.lock, source code imports).

## Population

The **25 repos from E067's assessment** that are **not A1** (i.e., 1 A2 + 11 A3 + 13 fetchable A4 repos — excluding 5 A4 repos with "no tree" errors that couldn't be fetched).

Ground truth: The **4 A1 repos** from E067, whose pinned specs are known to work.

## Method

1. **Fetch repository contents** for the 25 test repos (shallow clone, default branch).
2. **Extract partial information** from each repo:
   - README: parse for version hints (e.g., "Python 3.10", "torch>=1.12", "numpy==1.24")
   - Requirements files: extract package names from `requirements*.txt`, `pyproject.toml`, `setup.py`, `Pipfile`, `poetry.lock`
   - Source code: scan `.py` files for `import X` / `from X import Y` statements
3. **Resolve versions** using PyPI JSON API (`https://pypi.org/pypi/{package}/json`) — stdlib `urllib`, no auth needed:
   - For packages with version constraints in repo: pick latest matching constraint
   - For packages only found via imports: pick latest stable version (non-pre-release)
   - Cache responses to disk to avoid rate limits and enable reproducibility
4. **Generate pinned `requirements.txt`** with all dependencies at resolved `==` versions.
5. **Validate generated spec** against ground truth (A1 repos):
   - For A1 repos: simulate by stripping pins from their known spec, run generator, compare generated pins to actual pins
   - For A2/A3/A4 repos: syntactic validity (all lines `pkg==X.Y.Z`), version resolution success rate, import coverage

## Arms

| Arm | Definition |
|-----|------------|
| **G1** | Generator run on A1 repos with pins stripped (validation: can it recover known-good pins?) |
| **G2** | Generator run on A2 repo (poetry.lock only) |
| **G3** | Generator run on A3 repos (README only) |
| **G4** | Generator run on fetchable A4 repos (no env info, source imports only) |

## Kill Gates (predeclared)

| Gate | Condition | Verdict if met |
|------|-----------|----------------|
| **K1** (validation recovery) | G1 recovers ≥80% of pins exactly for ≥2 of 4 A1 repos | **PASS** — generator can reconstruct known specs |
| **K2** (syntactic validity) | ≥90% of generated specs across G2/G3/G4 are syntactically valid (every line `pkg==X.Y.Z`, no unresolved) | **PASS** — generator produces well-formed output |
| **K3** (import coverage) | Generated specs for G3/G4 cover ≥50% of unique imports found in source | **PASS** — generator captures actual dependencies |
| **K4** (version resolution) | ≥70% of unique packages across all test repos resolve to a version | **PASS** — PyPI resolution works for majority |

**Overall**: All four gates must pass for the mechanism to be considered viable.

## Baseline Comparison

Compare against naive baseline: `pip freeze` from a fresh virtualenv after `pip install -e .` (if `setup.py`/`pyproject.toml` exists) or `pip install -r requirements.txt` (if unpinned requirements exist). This baseline requires the repo to be installable, which many A3/A4 are not.

## Instrument Falsifiability

- Version resolution is deterministic: PyPI JSON returns latest version; same input → same output.
- Import scanning is deterministic: stdlib `ast` module, no heuristics.
- Synthetic fixture test: generator must produce known output for a hand-crafted repo fixture with known imports and requirements.

## Gate enumeration requirement (D088, F101)

Before a kill gate is declared, **enumerate what its passing value can actually be made of.** A gate is informative only if its passing region contains a case a working mechanism would produce and a broken one would not. 

- **K1–K4 passing regions must be enumerated** before the run: specify what concrete values or repository states would cause the gate to pass.
- If a gate's passing region consists only of vacuous cases (e.g., "empty files," "no packages named," "0 results"), the gate **cannot fail** — it will always report pass regardless of the generator's output. Such a gate must be redesigned with a stricter passing region or an additional `pass_strict` mode that counts only verified installations.
- `analyze.py` must read from **durable bytes that exist before the run ends**, not from a file the run writes at the end (which is how E069's own analysis tool could not have produced its verdict).
- All gates should report both `pass` (declared arithmetic meets threshold) and `pass_strict` (verified against actual measured outcomes), so the honest reading is visible in the same object and the declared arithmetic stays auditable.

**Example from E069/K1:** The passing region ">= 3 of 20 repos install cleanly" was reachable by a generator emitting only empty files, making the gate non-falsifiable. The verdict was therefore read from K3 (which does not depend on the artifact) and from `pass_strict` counts.

## Reproduction

```bash
cd /home/ubuntu/think-free/EXPERIMENTS/068-arxiv-spec-generator
python3 fetch_repos.py      # shallow clone test repos
python3 extract.py          # extract partial info
python3 resolve.py          # resolve versions via PyPI
python3 generate.py         # generate pinned requirements.txt
python3 validate.py         # apply kill gates
python3 -m unittest discover -s . -t . -p 'test_*.py'
```

## Environment

- Python 3.8+, stdlib only (`urllib`, `json`, `ast`, `subprocess`, `tempfile`, `hashlib`)
- Network: PyPI API (unauthenticated, generous rate limits)
- Disk: ~500MB for shallow clones + PyPI cache
- No external dependencies

## Epistemic Limits

- **Shallow clones only**: May miss files in subdirectories not at root.
- **PyPI-only resolution**: Cannot resolve packages not on PyPI (private, Conda-only, system packages).
- **Import ≠ dependency**: Some imports are stdlib, some are transitive, some are optional.
- **No install test**: Kill gates measure generation quality, not whether `pip install -r generated.txt` actually works in a clean env.
- **A4 "no tree" repos excluded**: 5 repos couldn't be fetched; generator untested on them.
- **Single Python version**: Resolution assumes target Python 3.10 (median of A1 repos).
- **A passing gate establishes mechanism feasibility, not product viability or adoption.**
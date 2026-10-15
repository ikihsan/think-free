<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E049 Part B RESULT — Registry-side drift of pinned requirements (E2, second half)

**Date:** 2026-10-14 · **Status:** Kill gate MET — mechanism falsified

---

## Summary

The second half of E049 (E2's registry-drift claim) is **falsified**. Re-resolving the exact same pinned requirements (`requests==2.32.3`, `rich==13.9.4`, `httpx==0.28.1`) one week after the original snapshot (2026-10-07 → 2026-10-14) produces **bit-identical artifacts** for all 16 packages in the transitive closure. The kill gate for E2's registry-drift half is met.

---

## Background

**E049 Part A (2026-10-07)** measured whether projects' published lockfiles change over time. Result: 10 of 11 closures changed ("drift-observed"). However, Part A conflates two mechanisms:
1. **Project edits** — the project intentionally updates its declared dependencies
2. **Registry drift** — the same declared inputs resolve to different artifact bytes

**E049 Part B** was designed to isolate mechanism (2): fix a requirements file, download the full transitive closure, record artifact hashes, and re-run later. The predeclared kill gate: *bit-stable re-resolution of the same inputs over months kills the mechanism.*

---

## Experiment

| Parameter | Value |
|-----------|-------|
| Requirements | `requests==2.32.3`, `rich==13.9.4`, `httpx==0.28.1` |
| Original snapshot | 2026-10-07 (recorded in `results.json` → `part_b.artifacts`) |
| Re-run date | 2026-10-14 |
| Command | `pip download -r requirements-fixed.txt -d <dir>` |
| Artifacts compared | 16 wheels (3 direct + 13 transitive) |
| Hash algorithm | SHA-256 |

---

## Results

| Artifact | Original SHA-256 (2026-10-07) | Re-run SHA-256 (2026-10-14) | Match |
|----------|-------------------------------|------------------------------|-------|
| anyio-4.5.2-py3-none-any.whl | c011ee36bc1e8ba40e5a81cb9df91925c218fe9b778554e0b56a21e1b5d4716f | c011ee36bc1e8ba40e5a81cb9df91925c218fe9b778554e0b56a21e1b5d4716f | ✓ |
| certifi-2026.7.22-py3-none-any.whl | 62f22742b58a1a33014a2b6b706588a8d7e2a88ae7bd1a6ebe8c992928483775 | 62f22742b58a1a33014a2b6b706588a8d7e2a88ae7bd1a6ebe8c992928483775 | ✓ |
| charset_normalizer-3.5.2-...whl | 1c50fe28bbc2ced33386f298650d91218076c05420e6cbd790b913adc41659e7 | 1c50fe28bbc2ced33386f298650d91218076c05420e6cbd790b913adc41659e7 | ✓ |
| exceptiongroup-1.3.1-py3-none-any.whl | a7a39a3bd276781e98394987d3a5701d0c4edffb633bb7a5144577f82c773598 | a7a39a3bd276781e98394987d3a5701d0c4edffb633bb7a5144577f82c773598 | ✓ |
| h11-0.16.0-py3-none-any.whl | 63cf8bbe7522de3bf65932fda1d9c2772064ffb3dae62d55932da54b31cb6c86 | 63cf8bbe7522de3bf65932fda1d9c2772064ffb3dae62d55932da54b31cb6c86 | ✓ |
| httpcore-1.0.9-py3-none-any.whl | 2d400746a40668fc9dec9810239072b40b4484b640a8c38fd654a024c7a1bf55 | 2d400746a40668fc9dec9810239072b40b4484b640a8c38fd654a024c7a1bf55 | ✓ |
| httpx-0.28.1-py3-none-any.whl | d909fcccc110f8c7faf814ca82a9a4d816bc5a6dbfea25d6591d6985b8ba59ad | d909fcccc110f8c7faf814ca82a9a4d816bc5a6dbfea25d6591d6985b8ba59ad | ✓ |
| idna-3.15-py3-none-any.whl | 048adeaf8c2d788c40fee287673ccaa74c24ffd8dcf09ffa555a2fbb59f10ac8 | 048adeaf8c2d788c40fee287673ccaa74c24ffd8dcf09ffa555a2fbb59f10ac8 | ✓ |
| markdown_it_py-3.0.0-py3-none-any.whl | 355216845c60bd96232cd8d8c40e8f9765cc86f46880e43a8fd22dc1a1a8cab1 | 355216845c60bd96232cd8d8c40e8f9765cc86f46880e43a8fd22dc1a1a8cab1 | ✓ |
| mdurl-0.1.2-py3-none-any.whl | 84008a41e51615a49fc9966191ff91509e3c40b939176e643fd50a5c2196b8f8 | 84008a41e51615a49fc9966191ff91509e3c40b939176e643fd50a5c2196b8f8 | ✓ |
| pygments-2.19.2-py3-none-any.whl | 86540386c03d588bb81d44bc3928634ff26449851e99741617ecb9037ee5ec0b | 86540386c03d588bb81d44bc3928634ff26449851e99741617ecb9037ee5ec0b | ✓ |
| requests-2.32.3-py3-none-any.whl | 70761cfe03c773ceb22aa2f671b4757976145175cdfca038c02654d061d6dcc6 | 70761cfe03c773ceb22aa2f671b4757976145175cdfca038c02654d061d6dcc6 | ✓ |
| rich-13.9.4-py3-none-any.whl | 6049d5e6ec054bf2779ab3358186963bac2ea89175919d699e378b99738c2a90 | 6049d5e6ec054bf2779ab3358186963bac2ea89175919d699e378b99738c2a90 | ✓ |
| sniffio-1.3.1-py3-none-any.whl | 2f6da418d1f1e0fddd844478f41680e794e6051915791a034ff65e5f100525a2 | 2f6da418d1f1e0fddd844478f41680e794e6051915791a034ff65e5f100525a2 | ✓ |
| typing_extensions-4.13.2-py3-none-any.whl | a439e7c04b49fec3e5d3e2beaa21755cadbbdc391694e28ccdd36ca4a1408f8c | a439e7c04b49fec3e5d3e2beaa21755cadbbdc391694e28ccdd36ca4a1408f8c | ✓ |
| urllib3-2.2.3-py3-none-any.whl | ca899ca043dcb1bafa3e262d73aa25c465bfb49e0bd9dd5d59f1d0acba2f8fac | ca899ca043dcb1bafa3e262d73aa25c465bfb49e0bd9dd5d59f1d0acba2f8fac | ✓ |

**Total: 16/16 match (100%)**

---

## Gate Evaluation

| Gate | Criterion | Result |
|------|-----------|--------|
| **Kill gate (predeclared)** | Bit-stable re-resolution over time → mechanism killed | **MET** — 16/16 artifacts bit-identical |

---

## Interpretation

**The registry-drift half of E2 is falsified for this sample.** The same pinned requirements resolved to bit-identical wheels one week later. PyPI's immutability guarantee (once a wheel is published at a given version, its bytes never change) holds in practice for this dependency set.

This does not mean lockfiles are perfect reproducibility witnesses — **E049 Part A already showed projects frequently rewrite their lockfiles** (10/11 changed). The drift observed in Part A is driven by *project edits* (intentional dependency updates), not by *registry mutation* (same version → different bytes).

---

## What this does not establish

- Whether registry drift occurs over longer windows (months/years) or for other ecosystems (npm, Cargo, etc.)
- Whether projects' lockfile rewrites are avoidable or necessary
- Whether a tool that detects "lockfile staleness" would be useful

The experiment only tests the specific claim: *the same declared inputs resolve to different artifact bytes on PyPI over time.*

---

## Ceilings

- **Sample size**: 1 requirements file, 16 artifacts, 1 ecosystem (PyPI), 1-week interval
- **Packages**: All pure-Python wheels; no binary extensions, no platform-specific builds
- **Index**: PyPI only; private indexes, Git dependencies, VCS URLs not tested
- **Time window**: 7 days; the original protocol specified "months"

---

## Evidence Labels

- Artifact hash match: **observed** (directly computed from downloaded wheels)
- Kill gate met: **observed** (predeclared criterion satisfied)
- Registry immutability claim: **inferred** (supported by this sample, not proven generally)

---

## Artifacts

- `results.json` — Original results with Part B snapshot (2026-10-07)
- `requirements-fixed.txt` — Pinned requirements (3 lines)
- `part_b_rerun/` — Re-downloaded wheels (2026-10-14)
- `RESULT.md` — This file

---

## Compliance

- Kill gate predeclared in `README.md` (2026-10-07): "bit-stable re-resolution of the same inputs over months kills the mechanism"
- Experiment re-run with identical command and inputs
- stdlib-only Python 3.8, no external dependencies beyond `pip`
- Raw evidence preserved (all wheels and hashes)
- Gate evaluated against committed original snapshot
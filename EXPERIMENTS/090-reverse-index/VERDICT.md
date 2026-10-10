<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-10
-->

# E090 — the general reverse resolver is not buildable at any K this protocol reaches

Task T-0089. Protocol declared 2026-10-10 before any run.
`PROTOCOL.md` · `results.json` · `g0-results.json` · `leakage.json` ·
`transfer-cost.json` · `population.json` · `raw-projects.jsonl`

## Verdict

| gate | declared | measured | verdict |
|---|---|---|---|
| **G0** instrument discrimination | positive ≥ 18/20, negative **0**/30, forward ≥ 8/10 | positive **19/21**, negative **0/30**, forward **9/10** | **PASS** |
| **G1** buildable within real resources | ≤ 3 h, ≤ 10 GB, ≤ 20 GB | 2 requests and a mean **351 KB** per project, p50 3.2 s / p90 16.7 s / p99 83.4 s / max 677.8 s; extrapolated **5.27 GB** and **30 000 requests** for K=15000 | **PASS** |
| **G2** coverage, baseline fallback disabled — **kill gate** | ≥ 0.70 | **0.3137** (618 of 1970) | **FAIL** |
| **G3** value over `pip install M` | ≥ 0.02 | **0.0589** (116 of 1970) | **PASS** |

**The build decision this changes:** a module→distribution index over PyPI is
not a product, at any K. `pyprovides`'s README listed "which distribution
provides a module, in the general case" under *what is not measured*; it is now
**measured, and negative for the index**, while the mechanism underneath it —
reading a wheel's central directory — is confirmed cheap and correct at
**0.1877** conditional value.

## The number that decides it

| | count | share of 1970 |
|---|---|---|
| index names a provider | 618 | 0.3137 |
| `pip install <module>` names a provider | 651 | 0.3305 |
| both | 502 | 0.2548 |
| **either** | **767** | **0.3893** |
| **neither** | **1203** | **0.6107** |

Name matching, which is what both free mechanisms do, answers **fewer than four
in ten** of the top-level module names that real Python repositories import.
The 1203 it cannot answer are not an indexing gap: most are private helpers, and
the rest are real distributions that no name match will ever select.

## The K-curve, which is what makes this a kill and not a starting point

| K | 500 | 1000 | 2500 | 5000 | 10000 | 15000 |
|---|---|---|---|---|---|---|
| projects whose wheel was read | 516 | 960 | 2242 | 5278 | 10316 | 14387 |
| coverage | 0.100 | 0.140 | 0.200 | 0.255 | 0.295 | **0.314** |

Tripling K from 5000 to 15000 bought **+0.058**. Tripling it again buys less.
The curve is decelerating toward an asymptote far below 0.70, and the protocol
caps K at 15 000 — 2.5% of PyPI's namespace. **The gate is not reachable by
extending K**, so per `PROTOCOL.md` the run stopped rather than looking for a K
where it passes.

## What G3's pass does and does not say

G3 measures a share against a denominator that includes names no mechanism can
reach. The conditional form is the one a developer meets, because a failing
import names **one** module:

> Among the 618 names the index covers, **`pip install <module>` fails to
> resolve 116 of them — 0.1877.**
> Among the 290 names two or more repositories import, the index covers **224
> (0.7724)** and adds **48** that `pip install M` misses — **0.1655**.

So the index is genuinely better than the incumbent *where it can see*, and
genuinely blind two times in three. Both halves are observed; neither cancels
the other.

## Two controls that changed how the headline reads

**Repository reuse.** `PROTOCOL.md` fixes the sampling unit at "a distinct
top-level module name", which pools a name ten repositories depend on with a
name one repository depends on. Stratified, the pooled 0.3137 is a statement
about that pooling:

| imported by ≥ | 1 repo | 2 repos | 3 repos | 5 repos | 10 repos |
|---|---|---|---|---|---|
| denominator | 1970 | 290 | 161 | 84 | 43 |
| coverage | 0.3137 | **0.7724** | 0.8075 | 0.7619 | 0.6512 |
| added over `pip install` | 0.0589 | 0.1655 | 0.1739 | 0.1071 | 0.0930 |

The popularity strata agree with the direction: A-popular 0.4331, B-longtail
0.2526. **G2's declared figure is the pooled one and it is the one that failed.**

**Leakage.** 13 of the 1970 names (0.0066) are provided by the importing
repository itself — `benchmarks`, `docker`, `docs`, `examples`, `testing` — so
they are guaranteed misses whatever the index contains. Removing them moves
coverage from 0.3137 to 0.3132. Leakage does not explain the miss.

## Three defects found in E090's own instrumentation

1. **The first leakage pass was an upper bound, not a measurement** (0.5635).
   It counted a nested `pkg/helpers.py` as the repository providing a top-level
   name. Every hit is now classified by the path that produced it; 1097 of the
   1110 broad hits are `nested-vendored`, 13 are strict. `leakage-v1-upper-bound.json`
   is kept beside the corrected file so the correction is checkable.
2. **The standard-library exclusion missed 20 names (1.02%).** `harvest.py` uses
   `sys.stdlib_module_names`, which does not exist before Python 3.10, and its
   fallback lists only top-level `.py` files without a leading underscore. This
   VM runs 3.8.10, so `math`, `array`, `gc`, `itertools`, `_thread`, `__future__`
   and 13 others entered the population. Repaired in `harvest.py` to fall back
   to `sys.builtin_module_names` plus the platform lib-dynload directory. Too
   small to change any verdict; recorded because the docstring claimed "this
   machine's truth" and it was not.
3. **`build_index.py`'s docstring claimed a lock the code did not take.** Two
   runs started on 2026-10-10 produced 6 504 duplicate project lines. The lock
   is now taken, and the raw file was deduplicated to 15 000 distinct projects
   before analysis.

## Limits of this verdict

- **The strongest alternative was not measured.** `PROTOCOL.md` named three:
  `pip install <name>`, a web search, and a general assistant. Only the first
  was run. F096 measured the third at **17 of 20** on a different population,
  so the baseline here is the weaker of the two the protocol named, and G3's
  0.0589 is an upper bound on the index's advantage over what a developer
  actually reaches for.
- **`pip install <module>` was modelled, not executed.** Baseline B is "a
  project of normalized name M exists and its wheel ships M" — verified against
  wheel file lists, not against a running `pip`. It is the documented
  behaviour, and it is not a run.
- **The ranked list is biased toward popular projects by construction.** That
  bias is the selection variable; B-longtail coverage 0.2526 is the cost of it.
- **Population**: 60 repositories, 1 189 and 958 distinct names per stratum,
  one harvest. The harvest is not reproducible — GitHub search is sorted by
  `updated`, so a second harvest selects different repositories and produced
  1970 names where the first produced 1855.
- **Full-build transfer is inferred.** `build_index.py` counted requests and
  bytes for the 4 962-project resume it completed (**1 302.2 MB, 9 578
  requests, 1 855 s**) and lost two earlier runs'. `transfer_cost.py` measured
  the per-project distribution directly on 60 projects drawn at random with a
  fixed seed; the 5.27 GB total is that distribution scaled to 15 000.
- **`no-wheel` is 1034 of 15 000 (6.9%)** and 43 projects failed to read. These
  are counted as uncovered and reported apart, never folded into coverage.
- **Nothing here is `No module named 'X'` text.** The population is module names
  harvested from real code. T-0088 on VM `0947` measures the demand side on
  real reports; this experiment cannot say anyone asks.

## Reproduce

```bash
python3 EXPERIMENTS/090-reverse-index/g0_discrimination.py   # G0, labels known by construction
python3 EXPERIMENTS/090-reverse-index/harvest.py             # population (re-selects repos; see limits)
python3 EXPERIMENTS/090-reverse-index/build_index.py 15000   # resumable index build
python3 EXPERIMENTS/090-reverse-index/leakage.py             # denominator control
python3 EXPERIMENTS/090-reverse-index/transfer_cost.py 60    # per-project transfer
python3 EXPERIMENTS/090-reverse-index/analyze.py             # every gate figure, offline after the baseline cache
```

`analyze.py` recomputes every gate from `population.json`, `raw-projects.jsonl`
and `leakage.json`; the only network work it does is the cached baseline.
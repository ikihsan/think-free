<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-10
-->

# E092 — Module-provider demand: do practitioners ask "which distribution provides this module"?

Declared 2026-10-10, session `2026-10-10-008-measure-the-rate-of-real-importerror-mod`,
VM `instance-20260717-0947`, **before any report was harvested or classified.**

## The practical difficulty

A developer — or an agent writing code — encounters `ImportError: No module named 'X'`
or `ModuleNotFoundError: No module named 'X'`. The error names the module. The
developer must then discover which PyPI distribution provides it. This is the
resolver's use case: "I have a module name from an error; what do I `pip install`?"

**E064** measured near-miss names at 0.1615 false-accept rate. **E070** measured
pip's "did you mean" guard at 0 of 100. **E085** measured declared≠provided at
~0.6% on real code. **E090** built a reverse index and found it covers 31% of
real imports, while `pip install <module>` covers 33%, together only 39%.

**What nobody has measured is the demand side:** when practitioners hit this
error, do they ask the question? Stack Overflow, GitHub issues, and library
trackers are where this question would be asked. If the rate is negligible, the
resolver has no population to serve.

## Prior art, checked before naming anything

| artifact | fetched | what it does |
|---|---|---|
| Stack Overflow search | `stackoverflow.com/search?q=%5Bpython%5D+ImportError`, `ModuleNotFoundError` | Questions tagged python with ImportError/ModuleNotFoundError — the natural venue for this question |
| GitHub issues search | `github.com/search?q=ImportError+OR+ModuleNotFoundError+language%3APython` | Issues in Python repos reporting import failures |
| `pyimport2pkg` | `pypi.org/pypi/pyimport2pkg/json` | CLI: "Convert python import names to distribution names" — reverse mapping tool |
| `pip install <module>` | native pip behavior | `pip install requests` works when module==distribution; `pip install sklearn` fails silently (installs wrong package) |

**Verdict on prior art, stated before the run.** The mechanism (module→distribution mapping) exists as `pyimport2pkg` and as `pip install <module>`'s partial support. The question is whether practitioners *ask* this question in observable venues. If they don't, the mechanism has no demand.

## The claim under test

**H-01:** Among real Python `ImportError`/`ModuleNotFoundError` reports on Stack Overflow and GitHub issues, the fraction that name a module but no distribution (i.e., the asker does not know which package to install) is **≥ 1%**.

If < 1%, the line closes. The threshold is chosen because:
- A 1% rate on a high-volume venue means hundreds of real questions
- Below 1%, a tool's maintenance cost exceeds its reachable population
- This is the same threshold logic as E085's G3 (0.005 kill, 0.020 build)

## Arms

| arm | source | what it carries |
|---|---|---|
| **A — Stack Overflow** | Stack Exchange API: `/questions` with `tagged=python`, `intitle=ImportError OR ModuleNotFoundError`, sorted by activity, 500 most recent | Real practitioner questions with error text, tags, answers, view counts |
| **B — GitHub issues** | GitHub Search API: `ImportError OR ModuleNotFoundError language:Python`, 500 most recent | Real issues in Python projects with error text, repository context |
| **C — positive controls** | 20 known questions where the asker names a module but no distribution (hand-collected from Stack Overflow) | The instrument must recover these |
| **D — negative controls** | 20 known questions where the asker names both module and distribution, or the error is unrelated | The instrument must not fire on these |

## Denominator, and what is excluded

**Denominator:** All harvested reports that contain `ImportError` or `ModuleNotFoundError` (case-insensitive) in the title or body, after de-duplication by Stack Overflow question ID or GitHub issue URL.

**Excluded (missing observations, never zeros):**
- Reports where the error text is truncated/unreadable
- Reports in non-Python repositories (wrong language tag)
- Reports that are clearly about `sys.path`/`PYTHONPATH`/virtualenv activation, not missing distributions
- Reports where the module is a standard library module (stdlib modules don't need a distribution)

**Classified into:**
| class | meaning | in denominator? |
|---|---|---|
| `module-only` | Error names module `M`; asker does **not** name a distribution to install; question is "what package provides M?" or equivalent | **yes — target class** |
| `module-and-dist` | Asker names both the failing module and the distribution they tried (e.g., "I installed `scikit-learn` but `import sklearn` fails") | yes — distinct class |
| `distribution-only` | Asker names a distribution they installed but the error message is not quoted | yes — related but different |
| `environment` | Root cause is `sys.path`, virtualenv, multiple Python versions, not a missing distribution | excluded |
| `stdlib` | Module is in standard library | excluded |
| `unclear` | Cannot determine from available text | excluded, reported separately |

## Gates, all declared before any report was harvested

### G1 — Harvest viability
Each arm harvests **≥ 200** classifiable reports (after exclusions) within API limits.

*Reachable set:* Stack Exchange API allows 300 requests/day (key) or 10k/day (no key, but throttled). GitHub Search API allows 30 requests/minute (authenticated) or 10/minute (unauthenticated). Both are reachable; 200 is feasible.

*Both regions reachable:* API throttling could yield 0; a working harvest could yield 500+.

### G2 — Control validity
On arm C (positive controls), the classifier recovers **≥ 16 of 20** as `module-only`. On arm D (negative controls), it reports **≤ 2 of 20** as `module-only`.

*Both regions reachable:* Controls have determinate ground truth by construction.

### G3 — The rate (this is the build decision)
Let `R` = `module-only` / classifiable reports across arms A+B.

| `R` | decision |
|---|---|
| `< 0.01` | **KILL.** The population does not ask this question at measurable rate. Line closes. |
| `0.01 ≤ R < 0.05` | **HOLD.** Report Wilson CI95. Decide on larger harvest. |
| `≥ 0.05` | **BUILD.** Prototype the resolver with demand evidence. |

Threshold rationale: 1% on Stack Overflow's Python tag (~500 questions/day) = ~5 questions/day = ~150/month. A tool serving 150 real questions/month has a viable population. Below that, the line closes on measured demand.

### G4 — Arrival instrument (view_count)
For each `module-only` report, record `view_count` (Stack Overflow) or reaction count (GitHub). The target class must show **non-zero arrivals** — at least 50% of `module-only` reports have `view_count > 0`. This is the `view_count` principle from E062: independent arrivals, not just statements.

*Both regions reachable:* Zero-view questions exist; high-view questions exist.

## What is compared against what

The strongest accessible alternative for a practitioner with this error:
1. **`pip install <module>`** — works when module name == distribution name
2. **Web search** — "ImportError no module named X what package"
3. **General assistant** — F096 measured 17/20 served on a different population
4. **`pyimport2pkg`** — CLI tool for the reverse mapping

The comparison is **not** a benchmark. It is reported as: for each `module-only` report found, which of these would have answered it, and does the report's existence imply the alternatives failed?

## Ceilings, declared before the run

- Stack Exchange API throttling may limit harvest size. The 300 req/day limit (no key) means ~5 pages of 100 = 500 questions max per day. GitHub unauthenticated is 10 req/min = 600/hour.
- Stack Overflow questions may be closed/deleted; the API returns them but they're not visible to users. This is a missing observation, not a zero.
- GitHub issues include bot-generated and template issues. These are filtered by requiring human-authored text > 50 chars.
- The classifier uses keyword/regex heuristics on error message text. Precision will be < 1.0. G2's precision gate catches this.
- "Names a distribution" is detected by: `pip install X`, `install X`, `package X`, `pypi X`, distribution name in requirements.txt context. False negatives possible.

## Discrimination test, before any population harvest

**The instrument must separate known `module-only` reports from known non-`module-only` reports.**

Construct 20 positive controls (real Stack Overflow questions where asker has `ImportError: No module named 'X'` and asks "what package?") and 20 negative controls (real questions with ImportError but asker names the distribution, or error is about environment).

Run the classifier on these 40 controls. **If accuracy < 0.80, the instrument fails discrimination and no population harvest is run.** This is D095: an instrument must discriminate before its numbers are read.

The 40 controls are fixed by construction and committed before the run.

## Revision history

- 2026-10-10: Initial declaration. Written after prior-art check, before any harvest.
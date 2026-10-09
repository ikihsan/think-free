<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: complete
last-verified: 2026-10-09
-->

# E070 — does the silent wrong-project install occur among real users?

**Status:** Complete. K1a met, K2 primary ≥ 0.10 (build authorized).
**Date:** 2026-10-09. **Session:** `2026-10-09-004`. **VM:** `instance-20260717-0947`.
**Evidence:** `raw/arm_m.json`, `raw/api/`, `raw/sample.tsv`, `raw/labels-all.tsv`.

## Question

E064 measured that 0.1615 of plausible near-miss package names resolve to a
real, different artifact, and that installers' guards key on names that do
**not** resolve. The silent class — install succeeds, project is wrong, nothing
warns — is invisible to those guards. **Does it occur among real users?**

## Arm M — the mechanism, on bytes

Four known silent-class near-misses and one guard-caught control, each
installed in a fresh virtualenv with pip's defaults (Python 3.10.19, pip 23.0.1):

| name | declared | install | silent? | what happened |
|---|---|---|---|---|
| `sklearn` | B | **exit 1** | no | own `setup.py` exits 1: "use 'scikit-learn' instead" |
| `telegram` | B | **exit 0** | **yes** | installs 0.0.1; `import telegram` works; zero output naming `python-telegram-bot` |
| `beautifulsoup` | B | **exit 1** | no | BS3's 2008 `setup.py` raises `SyntaxError` under Python 3, points to `beautifulsoup4` |
| `color` | B | **exit 1** | no | only sdist discarded as unbuildable (version mismatch) |
| `reqests` | A | **exit 1** | n/a | "No matching distribution found" |

**Result: 1 of 4 declared-B names is actually silent.** The other 3 fail
loudly — not because of an ecosystem guard, but because the wrong project's own
release is deprecated or unbuildable. E064's premise that these names produce
silent installs is **falsified for 3 of 4 controls**. The silent class is
real but narrower than E064's sample suggested.

## Arm W — occurrence, sampled

**Sample:** 362 rows (PC 233, G 105, PL 24) from Stack Exchange + GitHub issue
search, 12 per query (PC: 25 per query per Amendment 4). All 362 classified.

### G rows (prevalence, 105 rows)

| label | count | meaning |
|---|---|---|
| E | 99 | not a package-name-confusion report |
| B | 3 | silent wrong-project install |
| F | 2 | name confusion, no install outcome |
| A | 1 | name does not resolve, installer refuses |

**B rows (all 3):**

1. `headroom` → `headroom-ai` — package's own error message says
   `pip install headroom[langchain]` but PyPI `headroom` is an unrelated
   project (SUNKENDREAMS/headroom 0.2.7). Install succeeds, wrong project.
2. `tigl3` → `tixi3` — conda package `tigl3` installs `tixi` (not `tixi3`).
   Name resolves via conda, install succeeds, wrong dependency.
3. `clip` → `openai-clip` — `clip==1.0.1` resolves to an old CLI tool on
   PyPI, not `openai-clip`. Install succeeds, wrong project.

### K2 gate

| denominator | value | threshold | verdict |
|---|---|---|---|
| **primary** B/(A+B+C+D) | **3/4 = 0.7500** | ≥ 0.10 | **BUILD** |
| secondary B/all-G | 3/105 = 0.0286 | < 0.05 | (diagnostic) |

Wilson CI95 for primary: **[0.3006, 0.9544]**. Lower bound still ≥ 0.10.

**The primary denominator is 4 rows.** The 3 B rows are real and independent
(3 different name pairs, 2 venues, 2 package ecosystems). But n=4 is small
and the secondary denominator (0.0286) shows the silent class is rare among
all install-confusion reports.

### K1 gate

| gate | result |
|---|---|
| K1a (≥ 2 of 4 PC pairs yield ≥ 1 B row) | **MET** — beautifulsoup: 4 B, telegram: 3 B |
| K1b (all 4 PC queries yield ≥ 1 B∪G∪F) | **NOT MET** — `pip install color` and `telegram python-telegram-bot` have 0 |
| K1c (κ ≥ 0.75 on 20% second pass) | **NOT RUN** |

K1b is diagnostic only (Amendment 2). The two queries that fail K1b are named
here: the `color` pair has no B∪G∪F rows because arm M showed `color` cannot
install silently today; the `telegram python-telegram-bot` pair-naming query
has 0 because the B population cannot name the intended project (Amendment 3).

## What this establishes

1. **The silent class is real and occurs in real reports.** 3 independent B
   rows in the G sample, across 2 ecosystems (PyPI, conda) and 2 venues
   (GitHub, Stack Exchange). This is the first observation of the E064
   false-accept class in real user reports.

2. **The mechanism is narrower than E064 suggested.** 3 of 4 declared-B
   controls fail loudly. The silent class exists but is a subset of E064's
   0.1615 — the names that resolve to real, installable, wrong projects.

3. **The population is small.** 3 of 105 G rows (2.86%). Among
   package-name-confusion reports specifically, 3 of 4 (75%) are silent,
   but n=4 is too small to be confident.

4. **A "did you mean a different project" check has a population.** The K2
   primary gate passes. A reversible prototype is authorized.

## Ceilings

- One host, one installer (pip; npm absent), Python 3.10.19 only.
- English-language Stack Overflow and GitHub only.
- Search ranking is relevance-based, not exhaustive.
- Self-selected reporter population.
- Arm M's 4 B cases are chosen, not sampled.
- K1c (inter-rater κ) not run — single coder.
- Primary denominator n=4 is small; secondary denominator (0.0286) is
  the more representative prevalence figure.

## Next action

A reversible prototype is authorized: a checker that reads a project's
declared dependencies and actual imports, and flags a declared name whose
near-miss is the project actually providing the import. Per D088, the next
candidate's protocol must enumerate what its gate's passing value can be made
of, before the run.

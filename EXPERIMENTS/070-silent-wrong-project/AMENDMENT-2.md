<!-- origin-meta
owner: EXPERIMENTS/070-silent-wrong-project/PROTOCOL.md
status: active
last-verified: 2026-10-09
-->

# E070 — Amendment 2 (declared 2026-10-09, after
arm M, before any row was classified)

Arm M changed what the label set has to express.
The protocol's A/B/C/D/E was written from E064's
two-class picture (resolves / does not resolve).
Installing the four control pairs showed **three**
install outcomes, not two, and a report shape the
set cannot express at all. Both are fixed here,
before classification, with the arm-M bytes behind
them.

## The new shapes, from arm M

| shape | arm M evidence |
|---|---|
| resolves, **install refused** | `sklearn` resolves, its own `setup.py` exits 1 with "use 'scikit-learn' rather than 'sklearn'"; `beautifulsoup` (BS3) resolves, its 2008 `setup.py` raises `SyntaxError` under Python 3; `color`'s only sdist is discarded as unbuildable |
| resolves, **install succeeds**, wrong project | `telegram` 0.0.1: exit 0, `import telegram` works, zero output naming `python-telegram-bot` |
| name confusion with **no install outcome** | seen in the PC sample before classification: "how do I install sklearn" with no attempt reported |

## The label set, fixed

| label | meaning |
|---|---|
| **A** | the typed name **does not resolve**; the installer refuses (pip prints no suggestion, `raw/arm_m_pip_versions.json`) |
| **G** | the typed name **resolves but the install is refused** — by the package's own deprecation stub, or by an unbuildable release. The user is told, but by *the wrong project's author*, not by any ecosystem guard |
| **B** | the typed name **resolves, the install succeeds, and the project is wrong**; the report shows the confusion (import failure, unexpected API). The silent class |
| **C** | both names are the **same project** (rename/alias) |
| **D** | correct distribution, but its **top-level module** differs from the distribution name |
| **F** | name confusion present (typed ≠ intended) but **no install outcome reported** |
| **E** | not a package-name-confusion report |

## The K1 gate, redesigned on the same evidence

The protocol's K1 demanded ≥ 3 of 4 PC queries
yield ≥ 1 **B** row. Arm M falsified the premise
behind that number: a control pair whose author has
deployed a deprecation stub (`sklearn`) or whose
only release cannot build (`beautifulsoup`, `color`)
**cannot** produce a B row today — the confusion is
real and historical (the stubs exist because it was
frequent), but its current outcome is G, not B.
Requiring B from a defended pair would fail the
instrument for a reason that is the pair's defence,
not the instrument's blindness.

**K1a — recovery of silent positives:** ≥ **2** of
the 4 PC queries yield ≥ 1 B row. (The mechanism
arm shows exactly two of the four controls can
install silently today: `telegram`, and the `bs4`
placeholder reachable through the beautifulsoup
query.)

**K1b — recovery of confusion generally:** all 4
PC queries yield ≥ 1 row in B ∪ G ∪ F. A query
that returns none means the instrument cannot see
that pair's confusion at all.

**K1c — inter-rater:** κ ≥ 0.75 on the 20 %
second-pass sample (full-body re-read, per
Amendment 1 §3).

K1 fails only if K1a or K1c fails. K1b is
diagnostic: a query that fails K1b is named in the
README and excluded from the "instrument sees the
population" claim.

**Why this is not moving a goalpost:** the
original K1 was declared before arm M ran, and arm
M — a mechanism measurement on bytes — showed the
world it was written against had already changed
for two of its four controls. The amendment records
that mechanism evidence, keeps the gate's purpose
(the instrument must recover real silent-class
reports, not defended pairs), and states the new
threshold before any classification row is read.

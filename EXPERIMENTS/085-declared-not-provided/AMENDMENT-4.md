<!-- origin-meta
owner: EXPERIMENTS/085-declared-not-provided/PROTOCOL.md
status: active
last-verified: 2026-10-10
-->

# E085 — Amendment 4 (declared before any rate was read)

## What was written, and why it is the wrong denominator

`classify.py` as first written built the pair list as **every declared
distribution × every imported top-level module, within each repository**. In
the 24-repository corpus that is 578 unique declared distributions against
several hundred imports, so the largest repository alone contributes hundreds
of thousands of pairs.

**No project works that way.** A repository is fine when the module a file
imports is provided by *some* declared dependency. Asking whether `pandas`
provides `matplotlib`, when the project declares both and uses both, is not a
defect in the project; it is an artefact of forming a cross product. The
declared gate G3 is judged on that cross product, so leaving it would understate
the rate by an arbitrary factor that depends on how many dependencies a
repository has.

**This is corrected before any rate is read.** At the time of this amendment the
resolver had processed 250 of 578 declared distributions and `results.json` did
not exist; no `S` value, no class count, and no gate verdict had been observed.

## The corrected unit

The unit of analysis is the **imported module**, and the question is the one a
developer actually faces:

> The code imports `M`. Is `M` provided by something this project declares?
> If not — does the name `M` itself resolve on PyPI to a *real, different*
> project?

That second question is the signature of the silent class, and it is the only
thing E070's `Crypto` control and E064's 0.1615 describe. A module named after
nothing is the loud class and is deptry's DEP001. A module named after a real
project that does not provide it is the silent class and nothing reports it.

| condition | class | whose problem it is |
|---|---|---|
| some declared distribution provides `M` | `covered` | nobody's |
| `M` has no PyPI record | `loud-no-such-project` | deptry DEP001; pip refuses at install |
| `M` resolves to a project with no wheel | `undecidable-sdist-only` | metadata cannot say; E070 measured 3 of 3 such installs failing loudly |
| `M` resolves to a project that **does not** provide `M` | **`silent-wrong-project`** | **the target class** |
| `M` resolves to a project that does provide `M` | `name-collision` | nobody's; installing it works |

## What is now reported, and on which denominator

Three denominators, all stated so a reader can apply their own:

1. **`S_modules`** — silent-wrong-project modules / **all imported
   top-level modules** in repositories with usable declarations (non-stdlib,
   non-project-local). This is the declared gate. It is the most conservative
   reading and the one a project-wide scan would report.
2. **`S_findings`** — silent-wrong-project modules / **modules not provided by
   any declared distribution**. This is the rate among things that actually look
   wrong, which is what a linter would put in front of a developer.
3. **`S_cross`** — the original declared×import cross-product rate, retained
   and reported, because it was declared first and dropping it would hide that
   the declared unit was replaced. It is expected to be much smaller; it is
   **not** the gate.

`S_strict` in the original protocol maps onto `S_modules` here. Where the
protocol said the gate would fall back to `S_upper` when a row's provider is
unknown, the equivalent is `undecidable-sdist-only`, which is reported as its
own class and never folded into the target.

## What does not change

The gate thresholds (kill below 0.005, hold to 0.020, build at or above) and the
population (the same 24 repositories) are unchanged. Only the unit of analysis
is corrected, and it is corrected toward the **stricter** question — the
ambiguous one is the one that would have made the gate easiest to pass.
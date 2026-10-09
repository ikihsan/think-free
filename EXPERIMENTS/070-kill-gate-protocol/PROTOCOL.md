<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E070 — can a kill gate be designed to actually fail?

Session `2026-10-09-00x-experiment-kill-gate-protocol`, declared 2026-10-09.

## The question

E069 confirmed that when a kill gate's passing region contains only vacuous cases (e.g., empty files, zero-install scenarios), the gate can never fail — it will always report "mechanism holds" or "pass" even when the underlying property is absent. **Can a kill gate be explicitly designed so that it has non-vacuous passing regions and can properly fail?**

This experiment tests two protocol changes, each sufficient on its own:

1. **Pre-declared passing regions**: the gate's "pass" conditions are enumerated before the run begins, not discovered or retrofitted during/after the run
2. **Pre-existing input data**: `analyze.py` reads bytes that already exist before the run starts, not a file the run generates at the end

Either change alone should enable a kill gate to fail; together they form a complete protocol fix.

## Background

E064 measured that 93 of 576 plausible near-miss package names resolve to real, different artifacts (0.1615 false-accept rate). E069 tested whether 24 healthy-metadata false accepts cause user confusion — found 0 credible reports, kill gate passed vacuously, no prototype built. The gate passed because the only "installable" cases were empty-name corner cases; there was no way for the gate to fail because it had no non-vacuous passing region.

This experiment directly addresses that defect by constructing a gate that *can* fail.

## Kill gate (G1)

**If the gate has no non-vacuous passing regions (i.e., all "pass" cases are empty/ambiguous corner cases), the gate cannot fail and no experiment is built.** This gate is the question, not the verdict.

## Passing-region enumeration (G2)

Before the run begins, the experiment must declare:

- **What counts as a "pass" case**: e.g., "a package name that resolves to exactly one existing package, installs cleanly with `pip install X`, and produces importable code"
- **What counts as a "fail" case**: e.g., "a package name that resolves to zero or >1 packages, fails to install, or produces import errors"
- **The exact input corpus**: a fixed, pre-existing list of package names for the run to evaluate

If the declared passing region contains only vacuous cases (empty names, names resolving to nothing, names with multiple equally-matched hits), the gate cannot fail and the experiment terminates without building a prototype.

## Search strategy (G2)

For each package name in the corpus:

1. **Attempt `pip install <name>`** in a temporary virtualenv
2. **Record the outcome**: success (single package installed, imports work), ambiguity (>1 matches), failure (install error), or no match
3. **`analyze.py` reads from a fixed corpus on disk** — not a file it writes at runtime

All searches use `pip` only; no npm, cargo, or other ecosystems.

## Thresholds

- **G1 (gateability)**: the declared passing region must contain at least one non-vacuous case. If every "pass" case is an empty name or a name that resolves to nothing, the gate cannot fail and the experiment ends.
- **G2 (search executed)**: for each name in the corpus, attempt installation and record the result
- **G3 (negative control)**: search a set of known-nonexistent package names — should all resolve to "no match" or ambiguity, never a surprise install

## Negative controls (G3)

- A set of package names known not to exist on PyPI (e.g., `nonexistent-pkg-xyz12345`)
- These should all return "no match" or "ambiguity", never a successful install — verifying the instrument does not produce false positives

## Resource limits

- Max 30 minutes wall time for pip installs across all corpus entries
- Max 100 package names in the corpus
- Virtualenvs are discarded after each name

## Oracle

Automated: `analyze.py` exit code 0 = gate passes, 1 = gate fails. No human review required for the gate verdict itself.

## Reproduce

```bash
cd EXPERIMENTS/070-kill-gate-protocol
python3 search.py      # attempts pip install for each name, writes raw/results.jsonl
python3 outcome.py     # computes G1, G2, G3 verdicts, writes results.json
```

## Assertions (what this experiment must satisfy)

1. **G1 pass**: the corpus contains at least one name that resolves to exactly one installable package with working imports — this proves the gate has a non-vacuous passing region
2. **G1 fail (negative)**: the corpus contains zero such names — this proves the gate can fail when the population is absent
3. **G2**: every name in the corpus is attempted and a result is recorded
4. **G3**: known-nonexistent names all return "no match" — the instrument does not falsely succeed
5. **analyze.py reads from disk**, not from runtime-generated files — verified by checking that removing the runtime-write step does not change the verdict
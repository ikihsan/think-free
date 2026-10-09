<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E070 — can a kill gate be designed to actually fail?

## The question

Can a kill gate be explicitly designed so that it has non-vacuous passing regions and can properly fail? E069 confirmed that when a kill gate's passing region contains only vacuous cases (empty files, zero-install scenarios), the gate can never fail — it will always report "mechanism holds" or "pass" even when the underlying property is absent. This experiment tests two protocol changes, each sufficient on its own:

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

- **What counts as a "pass" case**: e.g., "a package name that resolves to exactly one existing package on PyPI, with a valid name and version"
- **What counts as a "fail" case**: e.g., "a package name that resolves to zero packages (404 on PyPI) or produces an error"
- **The exact input corpus**: a fixed, pre-existing list of package names for the run to evaluate

If the declared passing region contains only vacuous cases (empty names, names resolving to nothing, names with multiple equally-matched hits), the gate cannot fail and the experiment terminates without building a prototype.

## Search strategy (G2)

For each package name in the corpus:

1. **Query the PyPI JSON API** (`https://pypi.org/pypi/<name>/json`)
2. **Record the outcome**: `pass` (package exists with valid metadata), `fail` (404 — not found on PyPI), or `error` (network/http error)
3. **`analyze.py` reads from a fixed corpus on disk** — not a file it writes at runtime

All searches use the PyPI JSON API only; no pip install, no venv, no other ecosystems.

## Thresholds

- **G1 (gateability)**: the declared passing region must contain at least one non-vacuous case. If every "pass" case is an empty name or a name that resolves to nothing, the gate cannot fail and the experiment ends.
- **G2 (search executed)**: for each name in the corpus, attempt a PyPI JSON API query and record the result
- **G3 (negative control)**: query a set of known-nonexistent package names — should all return 404 (not found), never a surprise install

## Negative controls (G3)

- A set of package names known not to exist on PyPI (e.g., `nonexistent-pkg-xyz12345`)
- These should all return 404 (not found), never a successful install — verifying the instrument does not produce false positives

## Resource limits

- Max 30 minutes wall time for API queries across all corpus entries
- Max 100 package names in the corpus
- No virtualenv requirement; API queries are stateless

## Oracle

Automated: `analyze.py` exit code 0 = gate passes, 1 = gate fails. No human review required for the gate verdict itself.

## Reproduce

```bash
cd EXPERIMENTS/070-kill-gate-protocol
python3 search.py      # queries PyPI JSON API for each name, writes raw/results.jsonl
python3 outcome.py     # computes G1, G2, G3 verdicts, writes results.json
```
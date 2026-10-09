<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-09
-->

# E071 — can a kill gate fail on missing config fields?

Session `2026-10-09-00x-experiment-config-validity`, declared 2026-10-09.

## The question

E070 demonstrated that a kill gate can be designed to fail when its passing region contains non-vacuous cases (real packages that resolve, nonexistent packages that don't). **Can the same protocol fix work in a different domain — configuration file validity?** This experiment tests whether enumerating passing regions before the run, and having analyze.py read pre-existing bytes, enables a kill gate to fail when configuration files lack required fields.

## Background

E070 used the PyPI JSON API to test package name resolution, with a corpus of real and nonexistent package names. The kill gate had non-vacuous passing regions because some names resolved to real packages (pass) and some were nonexistent (fail). This enabled G1 to pass (gate has non-vacuous passing region) and the gate to properly fail when no real packages are in the corpus.

E069's fatal defect was that the kill gate's passing region contained only vacuous cases (empty-name corner cases), so the gate could never fail. E070 fixed this by (a) enumerating passing regions before the run, and (b) having analyze.py read pre-existing bytes. This experiment asks whether Fix(a)(b) generalizes to a new domain.

## Kill gate (G1)

**If the gate has no non-vacuous passing regions (i.e., all "pass" cases are empty/ambiguous corner cases), the gate cannot fail.** This gate is the question, not the verdict.

If every "pass" case in the declared passing region is a config file that trivially satisfies the requirements (or no config files are tested), the gate cannot fail and the experiment terminates.

## Passing-region enumeration (G2)

Before the run begins, the experiment must declare:

- **What counts as a "pass" case**: e.g., "a YAML config file that contains all of the required top-level keys: `database`, `server`, `logging`"
- **What counts as a "fail" case**: e.g., "a YAML config file that is missing one or more required top-level keys, or is malformed YAML"
- **The exact input corpus**: a fixed, pre-existing set of YAML config files on disk for the run to evaluate

If the declared passing region contains only vacuous cases (e.g., empty files, configs with no content, configs that trivially pass regardless), the gate cannot fail.

## Search strategy (G3)

For each config file in the corpus:

1. **Read the file from disk** — a fixed file that already exists before the run starts
2. **Check for required top-level keys**: `database`, `server`, `logging`
3. **Record the outcome**: `pass` (all required keys present), `fail` (at least one key missing or malformed YAML), or `error` (unreadable file)
4. **`analyze.py` reads from pre-existing files** — not files it writes at runtime

All files are YAML format; JSON configs are not tested.

## Thresholds

- **G1 (gateability)**: the declared passing region must contain at least one non-vacuous case. If every "pass" case is an empty file or a config that trivially passes regardless of content, the gate cannot fail and the experiment ends.
- **G2 (search executed)**: for each config file in the corpus, read and evaluate it and record the result
- **G3 (negative control)**: include at least one config file that is missing required keys — should register as "fail", verifying the instrument detects the absence

## Negative controls (G3)

- A config file known to be missing one or more required keys (e.g., a config with only `database` but missing `server` and `logging`)
- This should register as "fail", verifying the instrument does not falsely pass malformed configs

## Resource limits

- Max 10 config files in the corpus
- Max 5 minutes wall time for reading and evaluating all files
- Config files are read from a fixed input directory on disk

## Oracle

Automated: `analyze.py` exit code 0 = gate passes, 1 = gate fails. No human review required for the gate verdict itself.

## Reproduce

```bash
cd EXPERIMENTS/071-config-validity
python3 search.py      # reads YAML configs from disk, writes raw/results.jsonl
python3 outcome.py     # computes G1, G2, G3 verdicts, writes results.json
```
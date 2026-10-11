<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E090 — Maven Central view-count measurement prototype

**Experiment directory:** `EXPERIMENTS/090-maven-view-count/`

This prototype tests the view-count principle on Maven Central (Java/JAR packages), a new domain not previously covered by the mission. The view-count principle measures independent arrivals at need by checking whether each row carries a positive arrival/view field. On PyPI (E071) and NPM, need-related packages are systematically more "active" (have significant activity metadata) than random packages. This experiment determines whether the same pattern holds on Maven Central.

## Raw results

`raw/probe.json` — written by `probe.py` after the measurement run, contains per-package data and the gate table.

`results.json` — derived from `raw/probe.json` by `outcome.py`, contains the final verdict, gate outcomes, and corrected statements.

## Reproduction

```bash
python3 probe.py     # step 1: run the measurement, write raw/probe.json
python3 outcome.py   # step 2: derive results.json from raw/probe.json
```
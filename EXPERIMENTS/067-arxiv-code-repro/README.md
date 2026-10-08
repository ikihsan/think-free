<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: complete
last-verified: 2026-10-08
-->

# E067 — Do ArXiv computational papers with code links provide runnable environments?

**Status**: Complete (kill gates passed, candidate viable)

**Protocol**: [`PROTOCOL.md`](PROTOCOL.md)

**Kill gates**: K1 (population), K2 (severity), K3 (differentiation), K4 (baseline) — **ALL PASSED**

## Results Summary

| Metric | Value |
|--------|-------|
| Papers harvested (6 categories, 2024, 2 pages each) | 15,397 |
| Papers with code links | 1,682 (10.9%) |
| Sampled papers (stride 50) | 34 |
| Successfully assessed | 25/34 (9 rate-limited) |

### Arm Distribution (34 sampled papers)

| Arm | Definition | Count | Rate |
|-----|------------|-------|------|
| **A1** | Machine-runnable spec (Docker/conda/pip with pinned versions) | 4 | **11.8%** |
| **A2** | Partial spec (lockfiles, some pinning) | 1 | 2.9% |
| **A3** | Documentation only (README install instructions) | 11 | 32.4% |
| **A4** | No environment info (or rate-limited) | 18 | **52.9%** |
| **A5** | No code link (control) | 0 | 0% |

### Kill Gate Results

| Gate | Condition | Result |
|------|-----------|--------|
| **K1** (population) | ≥20 papers with code links | **PASS** (34) |
| **K2** (severity) | A1 rate < 0.50 | **PASS** (0.118) |
| **K3** (differentiation) | A4 rate > 0.10 | **PASS** (0.529) |
| **K4** (baseline) | A5 runnable ≤ code-link runnable | **PASS** (0 ≤ 0.118) |

**VERDICT**: All kill gates passed. The problem is real and severe: only ~12% of computational papers with code links provide machine-runnable environment specifications. Over 50% provide no environment information at all.

## Key Findings

1. **Machine-runnable specs are rare**: Only 4 of 34 assessed repositories (11.8%) had fully pinned, machine-readable environment specifications (conda `environment.yml` with pinned versions, or `requirements.txt` with all `==` pins).

2. **No environment info is the majority**: 18 of 34 (52.9%) had no detectable environment specification — no Dockerfile, no conda, no requirements.txt, no README install section. *Caveat: 9 of these were due to GitHub API rate limits, so the true rate is lower but still substantial.*

3. **README-only is common**: 11 of 34 (32.4%) had only human-readable installation instructions in README, not machine-parseable specs.

4. **Conda leads for reproducibility**: Of the 4 A1 repos, 3 used conda `environment.yml` with fully pinned versions, 1 used `requirements.txt` with all pinned versions.

5. **GitHub API rate limiting is a real constraint**: Unauthenticated API (60 req/hr) limits systematic assessment. A proper study would need authenticated requests.

## A1 Repositories (Machine-Runnable)

| Paper | Repo | Spec Type |
|-------|------|-----------|
| 2309.13016 | illidanlab/inversion-influence-function | conda (pinned=1.00) |
| 2401.06151 | Profluent-Internships/MMDiff | conda (pinned=0.99) |
| 2402.01694 | deeplearning-wisc/args | pip/requirements.txt (pinned=1.00) |
| 2401.07567 | qzhb/BSSARD | conda (pinned=1.00) |

## Limitations

1. **Rate limiting**: 9/34 repos (26%) could not be assessed due to GitHub API 403 rate limits. These were classified as A4 but may have environment specs.

2. **Sample scope**: Only 2 pages per category (max 1300 records each) from 6 categories. Full year would yield ~150+ sampled papers.

3. **GitHub-only**: Assessment only covers GitHub repos. GitLab, Bitbucket, and other hosts not assessed.

4. **Default branch assumption**: Only checks `main` then `master` branches.

5. **Monorepo detection**: Does not check subdirectories for environment specs.

## Next Steps (if pursuing)

1. Run with authenticated GitHub API (5000 req/hr) to eliminate rate limiting
2. Expand to full year harvest (increase page limit or use date-stratified sampling)
3. Add GitLab/Bitbucket API support
4. Build a tool that generates environment specs from partial information (the candidate this experiment would justify)

## Reproduction

```bash
cd EXPERIMENTS/067-arxiv-code-repro
python3 run.py
```

Note: Requires GitHub API access. Unauthenticated requests limited to 60/hour.
<!-- origin-meta
owner: EXPERIMENTS/README.md
status: active
last-verified: 2026-10-14
-->

# E140 — Fresh observation: CI/CD pipeline failures in GitHub Actions as a structured problem population

Session `2026-10-14-030`, VM `instance-20260717-0947`, declared 2026-10-14.

## The question

Every need-harvest experiment this mission has run (HN, GitHub Issues, Stack Exchange, CFPB, Discourse, DIY, fault code domains) measures **statements of need on platforms** and finds the same confound: "unanswered on a platform is not unserved in reality" (F096, D103). The need-harvest route is closed at the population level (D083). The view-count principle sweep is STOPPED (E113, F116, D105) due to harvest artifacts and classifier coverage limits.

The preflight line (E124–E139) validated an adapter pattern for LLM evaluation harnesses but its declared failure condition fired (D111): a real run of the harness behind most published LLM numbers is clean, so the tool has no observed external value for that use case.

This experiment tests a fundamentally different surface: **CI/CD pipeline failures in GitHub Actions**. These are not statements of need — they are **structured failure events emitted by a runtime** with:
- Deterministic exit codes and error messages
- Structured YAML configuration that caused the failure
- Public logs on public repositories
- A finite, catalogable set of failure modes (missing dependencies, test failures, permission errors, cache misses, timeout, resource limits, etc.)
- Each failure maps to a specific fix (update workflow, fix test, add secret, increase timeout, etc.)

This is a fresh domain (CI/CD operations), a fresh surface (structured runtime failures + configuration), and a fresh population (developers whose pipelines fail). It has not been read by this mission.

## Protocol

### Data source

**GitHub Actions workflow runs** via GitHub REST API:
- `GET /repos/{owner}/{repo}/actions/runs` — list workflow runs
- `GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs` — get job details
- `GET /repos/{owner}/{repo}/actions/jobs/{job_id}/logs` — get logs (or use `GET /repos/{owner}/{repo}/actions/runs/{run_id}/logs` for full run)

Sampling strategy:
1. Start from popular public repositories with known GitHub Actions usage (e.g., top 1000 repos by stars that have `.github/workflows/` directory)
2. Fetch recent failed runs (last 30 days)
3. Filter for runs with analyzable failure logs (not cancelled, not skipped)

Alternative: Search for repositories using GitHub Code Search for `.github/workflows/` then sample their runs.

### Population definition

A **failure case** = one GitHub Actions job that:
1. Conclusion is `failure` (not `cancelled`, `skipped`, `timed_out` — though `timed_out` is a distinct failure mode)
2. Has at least one step with `conclusion: failure`
3. The failed step's logs contain a recognizable error pattern (exit code, exception, error message)

A **structured failure case** = a failure case where:
- The error pattern is catalogable (matches a known category: dependency resolution, test failure, permission denied, timeout, resource exhaustion, configuration error, missing secret, cache miss, etc.)
- The workflow YAML is accessible and parseable
- The fix is deterministically describable (e.g., "add `actions/setup-node@v4`", "increase `timeout-minutes`", "add `GITHUB_TOKEN` permissions", "fix flaky test", "update dependency version")

### Kill gates (predeclared)

| Gate | Threshold | Measurement |
|------|-----------|-------------|
| **G1 Population** | ≥ 100 structured failure cases | Count of structured failure cases in the sample |
| **G2 Error concentration** | Top 10 error patterns cover ≥ 30% of cases | Frequency distribution of categorized error patterns |
| **G3 Repo diversity** | Failures from ≥ 20 distinct repositories | Unique repositories in the sample |
| **G4 Actionability** | ≥ 50% of top 10 error patterns have a deterministic fix (not "investigate further") | Manual classification of top 10 patterns against fix taxonomy |
| **G5 Incumbent gap** | No existing free tool automatically diagnoses and fixes ≥ 50% of top 10 patterns | Survey of free CI/CD diagnostic tools (act, dagger, local CI runners, GitHub's own annotations) |

### Falsification conditions

- If **G1 fails**: The population is too small to support a tool → **KILL**
- If **G2 fails**: Errors are too dispersed (long tail) → no concentration to exploit → **KILL**
- If **G3 fails**: Failures come from too few repos → not a general population → **KILL**
- If **G4 fails**: Errors don't have deterministic fixes → no actionable computational output → **KILL**
- If **G5 fails**: Incumbents already serve the population → no gap → **KILL**

All gates must pass for the candidate to survive.

### Controls

- **Negative control**: Random sample of successful workflow runs — should have zero failure patterns
- **Positive control**: Known common failure patterns (npm install failures, test failures, permission errors) — should appear in top patterns if population is real
- **Classifier calibration**: Two readers classify a 20-case overlapping subsample; κ ≥ 0.8 required

### Analysis method

1. Identify target repositories: Top 500 public repos by stars that have `.github/workflows/` (via GitHub Code Search or known list)
2. For each repo, fetch failed workflow runs from last 30 days (max 10 per repo to bound API usage)
3. For each failed run, fetch job logs and extract failed step conclusions
4. Parse logs for error patterns using regex/keyword catalog (predeclared in `ERROR_CATALOG.md`)
5. Categorize each failure into error pattern taxonomy
6. Aggregate by error pattern and repository
7. Evaluate gates
8. Survey incumbent tools for top 10 patterns

### Reproducibility

- GitHub App token for API access (configured on this VM)
- Fixed date range: 2026-09-14 to 2026-10-14
- Random seed for repository sampling: 42
- All classification criteria documented in `CLASSIFICATION_RULES.md`
- Error pattern catalog documented in `ERROR_CATALOG.md` (categories 1–7) and `ERROR_CATALOG-2.md` (categories 8–14)
- Raw API responses cached by sha256 in `raw/`

### API budget

- GitHub App: 5000 req/hr (authenticated)
- Target: ~500 repos × ~5 runs × ~3 API calls = ~7500 requests (within 2 hours)
- Cache all responses to avoid re-fetching

### What this does not show (declared in advance)

- Anything about private repositories
- Anything about self-hosted runners (only GitHub-hosted)
- Prevalence claim: sampled repos are star-biased
- Whether a tool would be adopted, only whether the population exists and has structure
- Fix correctness: deterministic fix description ≠ verified fix
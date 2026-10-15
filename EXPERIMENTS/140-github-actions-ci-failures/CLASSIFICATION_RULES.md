<!-- origin-meta
owner: EXPERIMENTS/140-github-actions-ci-failures/PROTOCOL.md
status: active
last-verified: 2026-10-14
-->

# Classification Rules for E140 — CI/CD Failure Analysis

## Error Pattern Categories

Each failure is classified into exactly one primary category. Categories are mutually exclusive and ordered by specificity (most specific first).

### 1. Dependency Resolution Failure
**Patterns:**
- `npm ERR! code E404` / `npm ERR! 404 Not Found`
- `pip install` fails with `ERROR: Could not find a version that satisfies`
- `go mod download` fails with `module not found`
- `cargo fetch` fails with `failed to select a version`
- `composer install` fails with `Package not found`
- `yarn install` fails with `Package not found`
- `bundler` fails with `Could not find gem`
- `poetry install` fails with `Package not found`
- `pnpm install` fails with `ERR_PNPM_FETCH_404`

**Fix taxonomy:** Update version pin, add missing registry, fix lockfile, add authentication for private registry.

### 2. Test Failure
**Patterns:**
- `FAIL` / `FAILED` in test output (pytest, jest, mocha, go test, cargo test, mvn test, gradle test)
- `AssertionError` / `Assertion failed` in test context
- `expect(...).toBe(...)` / `expect(...).toEqual(...)` mismatch
- `Test failed:` / `Tests failed:`
- Exit code non-zero from test runner step

**Fix taxonomy:** Fix flaky test, update test expectations, fix broken code, skip known-broken test.

### 3. Permission / Authentication Failure
**Patterns:**
- `Permission denied (publickey)` / `Permission denied, please try again`
- `403 Forbidden` / `401 Unauthorized` in API calls
- `GITHUB_TOKEN` / `github-token` permission errors
- `Error: Resource not accessible by integration`
- `secret not found` / `Secret not found`
- `ssh: connect to host github.com port 22: Connection timed out` (in deploy context)

**Fix taxonomy:** Add required permissions to workflow, add missing secret, fix SSH key, use correct token scope.

### 4. Timeout Failure
**Patterns:**
- `The operation was canceled.` (GitHub Actions timeout)
- `Process completed with exit code 1` preceded by `##[warning]The job running time exceeded`
- `timeout` in step context (not test timeout)
- `Execution timeout` / `Timed out after`

**Fix taxonomy:** Increase `timeout-minutes`, optimize slow step, split job.

### 5. Resource Exhaustion
**Patterns:**
- `No space left on device`
- `Cannot allocate memory` / `Out of memory` / `OOMKilled`
- `Disk full` / `No space left`
- `CPU limit exceeded` / `Memory limit exceeded`
- `Exit code 137` (SIGKILL from OOM)

**Fix taxonomy:** Use larger runner, optimize memory usage, clean cache, reduce parallelism.

### 6. Configuration / Syntax Error
**Patterns:**
- `yaml: line X: column Y: ` / `Error parsing workflow file`
- `Invalid workflow file` / `Workflow file is invalid`
- `Unrecognized named-value` / `Unrecognized key`
- `Required key '...' not found`
- `A sequence was not expected` / `A mapping was not expected`
- `actions/checkout` version not found / `uses:` action not found

**Fix taxonomy:** Fix YAML syntax, update action version, add missing required keys, fix indentation.

### 7. Missing Secret / Environment Variable
**Patterns:**
- `Environment variable .* not set` / `.* is not defined`
- `secret .* not found` / `Secret .* not found`
- `Input required and not supplied: .*`
- `Missing required input: .*`

**Fix taxonomy:** Add secret to repository/org, add environment variable, fix input name.

### 8. Cache / Artifact Failure
**Patterns:**
- `Cache hit occurred on the key` but restore fails
- `Failed to download cache` / `Cache not found`
- `Artifact upload failed` / `Artifact download failed`
- `Error uploading artifact` / `Error downloading artifact`

**Fix taxonomy:** Fix cache key, clear corrupted cache, increase artifact retention, fix artifact name/path.

### 9. Build / Compilation Failure
**Patterns:**
- `error:` / `Error:` in compiler output (gcc, clang, rustc, javac, tsc, go build)
- `Compilation failed` / `Build failed`
- `SyntaxError` / `TypeError` in non-test context (tsc, eslint, mypy, ruff)
- `linker command failed` / `ld: symbol(s) not found`

**Fix taxonomy:** Fix syntax error, fix type error, update dependencies, fix missing import.

### 10. Network / Connectivity Failure
**Patterns:**
- `Connection timed out` / `Connection refused` (not SSH deploy)
- `Temporary failure in name resolution`
- `Could not resolve host`
- `Read timeout` / `Connect timeout` in HTTP calls
- `ECONNREFUSED` / `ETIMEDOUT` / `ENETUNREACH`

**Fix taxonomy:** Retry with backoff, use mirror, fix proxy, check service status.

### 11. Container / Docker Failure
**Patterns:**
- `docker: Error response from daemon`
- `image not found` / `manifest unknown`
- `Container .* exited with code`
- `OCI runtime create failed`
- `no space left on device` (in Docker context)

**Fix taxonomy:** Fix Dockerfile, pull correct image, increase disk, fix entrypoint.

### 12. Deployment / Release Failure
**Patterns:**
- `Deployment failed` / `Release failed`
- `Failed to create release` / `Failed to publish`
- `git push` fails in deploy step
- `npm publish` / `docker push` / `gh release` fails

**Fix taxonomy:** Fix permissions, fix version tag, fix registry auth, fix changelog.

### 13. Lint / Static Analysis Failure
**Patterns:**
- `ESLint:` / `Prettier:` / `TypeScript:` errors (non-test)
- `mypy:` / `pyright:` / `ruff:` / `flake8:` errors
- `golangci-lint:` / `clippy:` / `checkstyle:` errors
- `sonarqube:` / `codeql:` failures

**Fix taxonomy:** Fix lint errors, update config, add ignore, fix formatting.

### 14. Flaky / Intermittent Failure (catch-all for non-deterministic)
**Patterns:**
- Failure that matches no other category but re-running succeeds
- `Segmentation fault` / `SIGSEGV` without clear cause
- `Killed` without OOM context
- Random network errors that succeed on retry

**Fix taxonomy:** Add retry, fix race condition, isolate flaky test, improve stability.

### 15. Uncategorized
**Patterns:** Any failure not matching above categories.

**Fix taxonomy:** Requires investigation — not deterministically fixable by pattern alone.

---

## Fix Determinism Classification

For each error pattern (aggregated category), classify fix determinism:

| Fix Class | Definition | Examples |
|-----------|------------|----------|
| **Deterministic** | Single, specific fix applies to >80% of occurrences | "Add `actions/setup-node@v4` before `npm install`", "Add `permissions: contents: read` to workflow", "Update `node-version` to `20`" |
| **Semi-deterministic** | 2-3 specific fixes cover >80% of occurrences, choice depends on context | "Either increase `timeout-minutes` or split job", "Either fix flaky test or add `continue-on-error`" |
| **Investigative** | Fix requires case-specific analysis, no pattern | "Debug segfault", "Investigate intermittent network error", "Analyze custom build failure" |

**G4 threshold:** ≥ 50% of top 10 error patterns by frequency must be **Deterministic** or **Semi-deterministic**.

---

## Classification Procedure

1. **Extract failed step logs**: For each failed job, get the step(s) with `conclusion: failure`
2. **Apply patterns in order**: Check categories 1-14 in order; first match wins
3. **Record**: Category, matched pattern, step name, repository, workflow file
4. **Aggregate**: Count by category, then by specific pattern within category
5. **Fix classification**: For top 10 patterns, assign fix class using taxonomy above

---

## Inter-reader Agreement

- Two readers independently classify a random 20-case overlapping subsample
- Compute Cohen's κ on primary category assignment
- **Threshold: κ ≥ 0.8** (substantial agreement)
- If κ < 0.8: refine rules, re-classify, report final κ

---

## Negative Control Classification

Successful runs (conclusion: `success`) should yield **zero** failure patterns. Any pattern matched in a successful run is a classifier false positive and must be reported.

---

## Positive Control Verification

Known high-frequency patterns (from literature and pilot):
1. `npm ERR! code E404` / dependency not found → **Dependency Resolution**
2. `FAIL` / test assertion failure → **Test Failure**
3. `Permission denied` / `403 Forbidden` → **Permission / Authentication**
4. `The operation was canceled` (timeout) → **Timeout**
5. `No space left on device` → **Resource Exhaustion**
6. `yaml: line` parsing error → **Configuration / Syntax Error**
7. `secret not found` → **Missing Secret**
6. `Cache not found` / `Failed to download cache` → **Cache / Artifact**
7. `error:` in compiler output → **Build / Compilation**
8. `Connection timed out` → **Network / Connectivity**

These MUST appear in the top 20 patterns if the population is real. Absence of ≥3 indicates sampling bias.
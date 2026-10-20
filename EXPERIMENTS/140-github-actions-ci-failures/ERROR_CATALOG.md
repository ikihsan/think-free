<!-- origin-meta
owner: EXPERIMENTS/140-github-actions-ci-failures/PROTOCOL.md
status: active
last-verified: 2026-10-14
-->

# Error Pattern Catalog for E140 — CI/CD Failure Analysis (Categories 1–7)

This catalog provides the exact regex patterns and keyword matches used for automated pre-classification before human review. Each pattern maps to a category from CLASSIFICATION_RULES.md.

## Pattern Format

```yaml
category: "Category Name"
patterns:
  - regex: "exact regex pattern"
    description: "what this matches"
    examples:
      - "example log line 1"
      - "example log line 2"
  - keyword: "simple keyword"
    description: "what this matches"
    examples:
      - "example log line"
```

## Catalog

### 1. Dependency Resolution Failure

```yaml
category: "Dependency Resolution Failure"
patterns:
  - regex: "npm ERR! code E404|npm ERR! 404 Not Found"
    description: "npm 404 package not found"
    examples:
      - "npm ERR! code E404"
      - "npm ERR! 404 Not Found - GET https://registry.npmjs.org/package-name"
  - regex: "pip install.*ERROR: Could not find a version that satisfies"
    description: "pip version resolution failure"
    examples:
      - "ERROR: Could not find a version that satisfies the requirement package==1.0.0"
  - regex: "go mod download.*module not found"
    description: "Go module not found"
    examples:
      - "go: module github.com/user/repo@latest not found"
  - regex: "cargo fetch.*failed to select a version"
    description: "Cargo version selection failure"
    examples:
      - "error: failed to select a version for `crate`."
  - regex: "composer install.*Package not found"
    description: "Composer package not found"
    examples:
      - "[Composer\\Downloader\\TransportException] Package not found"
  - regex: "yarn install.*Package not found|yarn add.*Package not found"
    description: "Yarn package not found"
    examples:
      - "error An unexpected error occurred: \"Package not found\""
  - regex: "bundler.*Could not find gem"
    description: "Bundler gem not found"
    examples:
      - "Could not find gem 'gem-name' in any of the gem sources"
  - regex: "poetry install.*Package not found"
    description: "Poetry package not found"
    examples:
      - "Package 'package-name' not found"
  - regex: "pnpm install.*ERR_PNPM_FETCH_404"
    description: "pnpm fetch 404"
    examples:
      - "ERR_PNPM_FETCH_404 GET https://registry.npmjs.org/package-name: Not Found"
```

### 2. Test Failure

```yaml
category: "Test Failure"
patterns:
  - regex: "(^|\\n)(FAIL|FAILED)\\s+.*(test|Test|TEST)"
    description: "Test runner FAIL/FAILED output"
    examples:
      - "FAIL test_example.py::test_function"
      - "FAILED tests/test_module.py::test_case"
  - regex: "AssertionError|Assertion failed"
    description: "Assertion error in test context"
    examples:
      - "AssertionError: assert 1 == 2"
      - "Assertion failed: expected 5 but got 3"
  - regex: "expect\\(.*\\)\\.to(Be|Equal|Contain|Match).*mismatch|Expected.*but received"
    description: "Jest/Vitest expectation mismatch"
    examples:
      - "expect(received).toBe(expected) // Object.is equality"
      - "Expected: 5, Received: 3"
  - regex: "Test failed:|Tests failed:|test.*failed"
    description: "Generic test failure message"
    examples:
      - "Test failed: test_function"
      - "Tests failed: 2 passed, 1 failed"
  - regex: "pytest.*failed|go test.*FAIL|cargo test.*FAIL|mvn test.*FAILURE|gradle test.*FAILED"
    description: "Test runner summary failure"
    examples:
      - "===== 1 failed, 5 passed in 2.34s ====="
      - "FAIL	github.com/user/repo	0.123s"
```

### 3. Permission / Authentication Failure

```yaml
category: "Permission / Authentication Failure"
patterns:
  - regex: "Permission denied \\(publickey\\)|Permission denied, please try again"
    description: "SSH permission denied"
    examples:
      - "Permission denied (publickey)."
      - "Permission denied, please try again."
  - regex: "403 Forbidden|401 Unauthorized"
    description: "HTTP 403/401 errors"
    examples:
      - "403 Forbidden: Resource not accessible by integration"
      - "401 Unauthorized: Bad credentials"
  - regex: "GITHUB_TOKEN.*permission|github-token.*permission|Resource not accessible by integration"
    description: "GitHub token permission errors"
    examples:
      - "Error: Resource not accessible by integration"
      - "GITHUB_TOKEN does not have permission to create release"
  - regex: "secret not found|Secret not found"
    description: "Missing secret reference"
    examples:
      - "Error: Secret MY_SECRET not found"
      - "secret 'MY_SECRET' not found"
```

### 4. Timeout Failure

```yaml
category: "Timeout Failure"
patterns:
  - regex: "The operation was canceled\\."
    description: "GitHub Actions job timeout"
    examples:
      - "The operation was canceled."
  - regex: "##\\[warning\\]The job running time exceeded"
    description: "GitHub Actions timeout warning"
    examples:
      - "##[warning]The job running time exceeded the limit of 360 minutes."
  - regex: "timeout.*minutes|Timed out after|Execution timeout"
    description: "Generic timeout messages"
    examples:
      - "Timed out after 360 minutes"
      - "Execution timeout of 300 seconds exceeded"
```

### 5. Resource Exhaustion

```yaml
category: "Resource Exhaustion"
patterns:
  - regex: "No space left on device"
    description: "Disk full"
    examples:
      - "write failed: No space left on device"
  - regex: "Cannot allocate memory|Out of memory|OOMKilled|Exit code 137"
    description: "Memory exhaustion"
    examples:
      - "Cannot allocate memory"
      - "Process exited with code 137 (OOMKilled)"
  - regex: "Disk full|No space left"
    description: "Disk space exhaustion"
    examples:
      - "Disk full: /home/runner/work/_temp"
  - regex: "CPU limit exceeded|Memory limit exceeded"
    description: "Container resource limits"
    examples:
      - "Memory limit exceeded: container killed"
```

### 6. Configuration / Syntax Error

```yaml
category: "Configuration / Syntax Error"
patterns:
  - regex: "yaml: line \\d+: column \\d+:|Error parsing workflow file"
    description: "YAML parsing error"
    examples:
      - "yaml: line 15: column 3: mapping values are not allowed here"
  - regex: "Invalid workflow file|Workflow file is invalid"
    description: "Workflow validation error"
    examples:
      - "Invalid workflow file: .github/workflows/ci.yml"
  - regex: "Unrecognized named-value|Unrecognized key|Required key '.*' not found"
    description: "Invalid workflow keys"
    examples:
      - "Unrecognized named-value: 'run'. Located at position 1 within mapping."
  - regex: "A sequence was not expected|A mapping was not expected"
    description: "YAML structure error"
    examples:
      - "A sequence was not expected at line 10"
  - regex: "uses: .*@.*not found|action .* not found"
    description: "Action version not found"
    examples:
      - "Error: Unable to resolve action `actions/checkout@v999`, repository not found"
```

### 7. Missing Secret / Environment Variable

```yaml
category: "Missing Secret / Environment Variable"
patterns:
  - regex: "Environment variable .* not set|.* is not defined"
    description: "Missing environment variable"
    examples:
      - "Environment variable NODE_AUTH_TOKEN not set"
  - regex: "secret .* not found|Secret .* not found"
    description: "Missing secret (duplicate of permission category but distinct context)"
    examples:
      - "secret 'AWS_ACCESS_KEY_ID' not found"
  - regex: "Input required and not supplied:|Missing required input:"
    description: "Missing action input"
    examples:
      - "Input required and not supplied: token"
```

---

## Usage Notes

1. **Order matters**: Categories are checked in order 1-14; first match wins.
2. **Case-insensitive**: All regex patterns should be applied case-insensitive.
3. **Context window**: Patterns should match within ±5 lines of the failure point.
4. **Human review**: All automated classifications are reviewed by humans; catalog is for pre-sorting only.
5. **Version**: This catalog is versioned with the experiment. Changes require new experiment version.

## Continuation

Categories 8–14 continue in [`ERROR_CATALOG-2.md`](ERROR_CATALOG-2.md).
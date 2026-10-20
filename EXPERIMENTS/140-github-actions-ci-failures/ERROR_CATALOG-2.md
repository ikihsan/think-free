<!-- origin-meta
owner: EXPERIMENTS/140-github-actions-ci-failures/PROTOCOL.md
status: active
last-verified: 2026-10-14
-->

# Error Pattern Catalog (Categories 8–14) for E140 — CI/CD Failure Analysis

Continuation of [`ERROR_CATALOG.md`](ERROR_CATALOG.md).

## 8. Cache / Artifact Failure

```yaml
category: "Cache / Artifact Failure"
patterns:
  - regex: "Failed to download cache|Cache not found"
    description: "Cache download failure"
    examples:
      - "Failed to download cache: Cache not found for key"
  - regex: "Error uploading artifact|Error downloading artifact|Artifact upload failed|Artifact download failed"
    description: "Artifact operation failure"
    examples:
      - "Error uploading artifact: build-output"
```

## 9. Build / Compilation Failure

```yaml
category: "Build / Compilation Failure"
patterns:
  - regex: "(^|\\n)error:.*(compilation|build)|Compilation failed|Build failed"
    description: "Compiler/build failure"
    examples:
      - "error: compilation failed"
      - "Compilation failed: 2 errors"
  - regex: "SyntaxError|TypeError.*(tsc|eslint|mypy|ruff|pyright)"
    description: "Static analysis syntax/type error"
    examples:
      - "SyntaxError: Unexpected token"
      - "TypeError: Property 'x' does not exist on type 'Y'"
  - regex: "linker command failed|ld: symbol\\(s\\) not found|undefined reference to"
    description: "Linker error"
    examples:
      - "ld: symbol(s) not found for architecture x86_64"
      - "undefined reference to `function_name'"
```

## 10. Network / Connectivity Failure

```yaml
category: "Network / Connectivity Failure"
patterns:
  - regex: "Connection timed out|Connection refused|Temporary failure in name resolution|Could not resolve host"
    description: "Network connectivity errors"
    examples:
      - "Connection timed out after 30000ms"
      - "Could not resolve host: registry.npmjs.org"
  - regex: "Read timeout|Connect timeout|ECONNREFUSED|ETIMEDOUT|ENETUNREACH"
    description: "Low-level network errors"
    examples:
      - "ETIMEDOUT: Connection timed out"
      - "ECONNREFUSED: Connection refused"
```

## 11. Container / Docker Failure

```yaml
category: "Container / Docker Failure"
patterns:
  - regex: "docker: Error response from daemon"
    description: "Docker daemon error"
    examples:
      - "docker: Error response from daemon: pull access denied"
  - regex: "image not found|manifest unknown"
    description: "Docker image not found"
    examples:
      - "Error: No such image: user/image:tag"
      - "manifest unknown: manifest unknown"
  - regex: "Container .* exited with code|OCI runtime create failed"
    description: "Container runtime error"
    examples:
      - "Container 'build' exited with code 1"
```

## 12. Deployment / Release Failure

```yaml
category: "Deployment / Release Failure"
patterns:
  - regex: "Deployment failed|Release failed|Failed to create release|Failed to publish"
    description: "Deployment/release failure"
    examples:
      - "Deployment failed: Environment protection rules failed"
  - regex: "npm publish.*failed|docker push.*failed|gh release.*failed"
    description: "Publish command failure"
    examples:
      - "npm ERR! code E403 403 Forbidden - PUT https://registry.npmjs.org/package"
```

## 13. Lint / Static Analysis Failure

```yaml
category: "Lint / Static Analysis Failure"
patterns:
  - regex: "ESLint:|Prettier:|TypeScript:.*error"
    description: "JavaScript/TypeScript lint errors"
    examples:
      - "ESLint: 'x' is defined but never used"
  - regex: "mypy:|pyright:|ruff:|flake8:.*error"
    description: "Python lint/type errors"
    examples:
      - "error: Function is missing a return type annotation  [return-type]"
  - regex: "golangci-lint:|clippy:|checkstyle:.*error"
    description: "Go/Rust/Java lint errors"
    examples:
      - "warning: unused variable: `x`  [unused_variables]"
```

## 14. Flaky / Intermittent Failure

```yaml
category: "Flaky / Intermittent Failure"
patterns:
  - regex: "Segmentation fault|SIGSEGV"
    description: "Segmentation fault"
    examples:
      - "Segmentation fault (core dumped)"
  - regex: "^Killed$"
    description: "Process killed (no OOM context)"
    examples:
      - "Killed"
```

---

## Usage Notes

1. **Order matters**: Categories are checked in order 1-14; first match wins.
2. **Case-insensitive**: All regex patterns should be applied case-insensitive.
3. **Context window**: Patterns should match within ±5 lines of the failure point.
4. **Human review**: All automated classifications are reviewed by humans; catalog is for pre-sorting only.
5. **Version**: This catalog is versioned with the experiment. Changes require new experiment version.
#!/usr/bin/env python3
"""
E122 — Synthetic fixtures for CI/CD pipeline failure classification.

These are DECLARED BEFORE MEASUREMENT — hand-crafted to represent canonical
patterns for each failure type. The classifier is tested on these first.
If KG1 (≥80% accuracy) fails here, the real-data run is not attempted.
"""

from classifier import FailureCategory

# 20 synthetic log snippets per category = 160 total
# Each contains clear markers for its category

SYNTHETIC_FIXTURES = [
    # TEST_FAILURE (20)
    ("FAILED test_user_authentication - AssertionError: expected True got False", FailureCategory.TEST_FAILURE),
    ("FAILED test_database_connection - AssertionError: Connection refused", FailureCategory.TEST_FAILURE),
    ("FAILED test_api_endpoint - AssertionError: 404 != 200", FailureCategory.TEST_FAILURE),
    ("pytest test_suite.py::test_login FAILED - AssertionError: Invalid credentials", FailureCategory.TEST_FAILURE),
    ("pytest test_suite.py::test_register FAILED - AssertionError: Email already exists", FailureCategory.TEST_FAILURE),
    ("test_user_profile FAILED - expected 'admin' got 'user'", FailureCategory.TEST_FAILURE),
    ("test_payment_processing FAILED - AssertionError: Amount mismatch", FailureCategory.TEST_FAILURE),
    ("FAIL: test_user_login", FailureCategory.TEST_FAILURE),
    ("FAIL: test_data_validation", FailureCategory.TEST_FAILURE),
    ("junit.framework.AssertionFailedError: test_user_registration", FailureCategory.TEST_FAILURE),
    ("TestFailed: test_checkout_flow", FailureCategory.TEST_FAILURE),
    ("TestFailed: test_email_verification", FailureCategory.TEST_FAILURE),
    ("AssertionError: test_api_rate_limit", FailureCategory.TEST_FAILURE),
    ("AssertionError: test_cache_invalidation", FailureCategory.TEST_FAILURE),
    ("test_failed: test_migration_script", FailureCategory.TEST_FAILURE),
    ("test_failed: test_backup_restore", FailureCategory.TEST_FAILURE),
    ("RSpec::Expectations::ExpectationNotMetError: test_user_deletion", FailureCategory.TEST_FAILURE),
    ("RSpec::Expectations::ExpectationNotMetError: test_password_reset", FailureCategory.TEST_FAILURE),
    ("TestFailure: test_search_functionality", FailureCategory.TEST_FAILURE),
    ("TestFailure: test_file_upload", FailureCategory.TEST_FAILURE),

    # DEPENDENCY_ERROR (20)
    ("ModuleNotFoundError: No module named 'requests'", FailureCategory.DEPENDENCY_ERROR),
    ("ModuleNotFoundError: No module named 'numpy'", FailureCategory.DEPENDENCY_ERROR),
    ("ImportError: cannot import name 'pandas' from 'pandas'", FailureCategory.DEPENDENCY_ERROR),
    ("ImportError: No module named 'tensorflow'", FailureCategory.DEPENDENCY_ERROR),
    ("npm ERR! code E404 Not Found - package@1.0.0", FailureCategory.DEPENDENCY_ERROR),
    ("npm ERR! code ENOENT - missing dependency 'lodash'", FailureCategory.DEPENDENCY_ERROR),
    ("cargo build failed -- could not compile `serde`", FailureCategory.DEPENDENCY_ERROR),
    ("cargo build failed -- could not compile `tokio`", FailureCategory.DEPENDENCY_ERROR),
    ("pip install failed - Could not find a version that satisfies the requirement torch", FailureCategory.DEPENDENCY_ERROR),
    ("pip install failed - No matching distribution found for package 'cv2'", FailureCategory.DEPENDENCY_ERROR),
    ("go: cannot find main module, but found .git/config", FailureCategory.DEPENDENCY_ERROR),
    ("go: missing dependency github.com/stretchr/testify", FailureCategory.DEPENDENCY_ERROR),
    ("composer install failed - Package laravel/framework not found", FailureCategory.DEPENDENCY_ERROR),
    ("composer install failed - Could not find package monolog/monolog", FailureCategory.DEPENDENCY_ERROR),
    ("mvn dependency:resolve failed - Could not find artifact org.springframework:spring-core", FailureCategory.DEPENDENCY_ERROR),
    ("gradle build failed - Could not resolve all dependencies for configuration ':compileClasspath'", FailureCategory.DEPENDENCY_ERROR),
    ("Bundle install failed - Could not find gem 'rails'", FailureCategory.DEPENDENCY_ERROR),
    ("Bundle install failed - Could not find gem 'rspec'", FailureCategory.DEPENDENCY_ERROR),
    ("poetry install failed - Package 'django' not found", FailureCategory.DEPENDENCY_ERROR),
    ("yarn install failed - Package 'react' not found", FailureCategory.DEPENDENCY_ERROR),

    # FLAKY_TEST (20)
    ("test_intermittent_network FAILED - Timeout after 30s - FLAKY", FailureCategory.FLAKY_TEST),
    ("test_database_lock FAILED - Intermittent lock timeout - FLAKY", FailureCategory.FLAKY_TEST),
    ("test_race_condition FAILED - Timed out - FLAKY test", FailureCategory.FLAKY_TEST),
    ("test_cache_stampede FAILED - Intermittent - Retrying...", FailureCategory.FLAKY_TEST),
    ("test_external_api FAILED - Connection reset by peer - FLAKY", FailureCategory.FLAKY_TEST),
    ("pytest test_flaky.py::test_network FAILED - FLAKY marker detected", FailureCategory.FLAKY_TEST),
    ("pytest test_flaky.py::test_timing FAILED - FLAKY marker detected", FailureCategory.FLAKY_TEST),
    ("test_file_lock FAILED - Intermittent failure on retry", FailureCategory.FLAKY_TEST),
    ("test_port_conflict FAILED - Address already in use - FLAKY", FailureCategory.FLAKY_TEST),
    ("test_thread_safety FAILED - Intermittent - Retry attempt 2", FailureCategory.FLAKY_TEST),
    ("test_eventual_consistency FAILED - FLAKY - Re-running", FailureCategory.FLAKY_TEST),
    ("test_distributed_lock FAILED - Intermittent timeout", FailureCategory.FLAKY_TEST),
    ("test_retry_logic FAILED - FLAKY - Retrying in 5s", FailureCategory.FLAKY_TEST),
    ("test_async_operation FAILED - Intermittent - Timeout on attempt 1", FailureCategory.FLAKY_TEST),
    ("test_websocket FAILED - FLAKY - Connection dropped", FailureCategory.FLAKY_TEST),
    ("test_rate_limit FAILED - Intermittent - 429 Too Many Requests", FailureCategory.FLAKY_TEST),
    ("test_third_party_api FAILED - FLAKY - Service unavailable", FailureCategory.FLAKY_TEST),
    ("test_random_failure FAILED - FLAKY - Non-deterministic", FailureCategory.FLAKY_TEST),
    ("test_timing_sensitive FAILED - Intermittent - Timing issue", FailureCategory.FLAKY_TEST),
    ("test_gc_pressure FAILED - FLAKY - Garbage collection pause", FailureCategory.FLAKY_TEST),

    # ENVIRONMENT_ERROR (20)
    ("docker: not found - please install Docker", FailureCategory.ENVIRONMENT_ERROR),
    ("permission denied - cannot write to /tmp/build", FailureCategory.ENVIRONMENT_ERROR),
    ("Out of memory - process killed (OOM)", FailureCategory.ENVIRONMENT_ERROR),
    ("No space left on device - cannot write build artifacts", FailureCategory.ENVIRONMENT_ERROR),
    ("command not found: gcc", FailureCategory.ENVIRONMENT_ERROR),
    ("executable file not found in $PATH: make", FailureCategory.ENVIRONMENT_ERROR),
    ("Cannot allocate memory - fork failed", FailureCategory.ENVIRONMENT_ERROR),
    ("Segmentation fault (core dumped)", FailureCategory.ENVIRONMENT_ERROR),
    ("Killed - process terminated by OOM killer", FailureCategory.ENVIRONMENT_ERROR),
    ("docker: Error response from daemon: pull access denied", FailureCategory.ENVIRONMENT_ERROR),
    ("Cannot connect to the Docker daemon at unix:///var/run/docker.sock", FailureCategory.ENVIRONMENT_ERROR),
    ("mount: permission denied - cannot mount volume", FailureCategory.ENVIRONMENT_ERROR),
    ("ulimit: open files: cannot modify limit: Operation not permitted", FailureCategory.ENVIRONMENT_ERROR),
    ("Error: EACCES: permission denied, mkdir '/home/runner/work'", FailureCategory.ENVIRONMENT_ERROR),
    ("sh: 1: node: not found", FailureCategory.ENVIRONMENT_ERROR),
    ("sh: 1: python3: not found", FailureCategory.ENVIRONMENT_ERROR),
    ("/bin/bash: line 1: javac: command not found", FailureCategory.ENVIRONMENT_ERROR),
    ("/bin/bash: line 1: go: command not found", FailureCategory.ENVIRONMENT_ERROR),
    ("Error: Cannot find module '/github/workspace/action.yml'", FailureCategory.ENVIRONMENT_ERROR),
    ("The runner environment is not available", FailureCategory.ENVIRONMENT_ERROR),

    # COMPILE_ERROR (20)
    ("SyntaxError: invalid syntax on line 42", FailureCategory.COMPILE_ERROR),
    ("SyntaxError: unexpected token '}'", FailureCategory.COMPILE_ERROR),
    ("main.c:15: error: expected ';' before '}' token", FailureCategory.COMPILE_ERROR),
    ("main.cpp:23: error: 'cout' was not declared in this scope", FailureCategory.COMPILE_ERROR),
    ("main.rs:10: error: unresolved import `serde`", FailureCategory.COMPILE_ERROR),
    ("main.go:5:2: undefined: fmt.Println", FailureCategory.COMPILE_ERROR),
    ("Main.java:8: error: cannot find symbol: class JsonObject", FailureCategory.COMPILE_ERROR),
    ("app.ts:15: error TS2304: Cannot find name 'React'", FailureCategory.COMPILE_ERROR),
    ("compilation failed - see error log for details", FailureCategory.COMPILE_ERROR),
    ("Build failed - 5 errors, 0 warnings", FailureCategory.COMPILE_ERROR),
    ("error: undefined reference to `pthread_create'", FailureCategory.COMPILE_ERROR),
    ("ld: error: undefined symbol: main", FailureCategory.COMPILE_ERROR),
    ("cannot find -lssl - linker error", FailureCategory.COMPILE_ERROR),
    ("cargo build failed - error[E0432]: unresolved import", FailureCategory.COMPILE_ERROR),
    ("go build failed - ./main.go:10:2: undefined: missingFunction", FailureCategory.COMPILE_ERROR),
    ("javac Main.java - error: cannot find symbol", FailureCategory.COMPILE_ERROR),
    ("tsc compilation failed - error TS2304", FailureCategory.COMPILE_ERROR),
    ("gcc -o main main.c - error: stray '\\342' in program", FailureCategory.COMPILE_ERROR),
    ("clang: error: linker command failed with exit code 1", FailureCategory.COMPILE_ERROR),
    ("swiftc failed - error: use of unresolved identifier", FailureCategory.COMPILE_ERROR),

    # TIMEOUT (20)
    ("The operation was canceled due to timeout after 3600 seconds", FailureCategory.TIMEOUT),
    ("timeout: the monitored command dumped core", FailureCategory.TIMEOUT),
    ("Job exceeded maximum runtime of 3600 seconds - canceled", FailureCategory.TIMEOUT),
    ("Step timed out after 3600 seconds", FailureCategory.TIMEOUT),
    ("The job was canceled because it exceeded the maximum execution time", FailureCategory.TIMEOUT),
    ("Workflow run timed out after 6 hours", FailureCategory.TIMEOUT),
    ("Action timed out after 3600 seconds - canceling", FailureCategory.TIMEOUT),
    ("Process timed out after 1800 seconds", FailureCategory.TIMEOUT),
    ("Test suite timed out after 30 minutes", FailureCategory.TIMEOUT),
    ("Build step timed out - exceeded 60 minutes", FailureCategory.TIMEOUT),
    ("Deploy step timed out - exceeded maximum duration", FailureCategory.TIMEOUT),
    ("The operation was canceled - timeout reached", FailureCategory.TIMEOUT),
    ("Timeout: no output for 10 minutes", FailureCategory.TIMEOUT),
    ("Step exceeded time limit - canceling", FailureCategory.TIMEOUT),
    ("Job canceled: execution timeout", FailureCategory.TIMEOUT),
    ("Action execution timed out after 3600s", FailureCategory.TIMEOUT),
    ("Workflow execution timeout - 6 hours exceeded", FailureCategory.TIMEOUT),
    ("Build timed out - maximum 3600 seconds exceeded", FailureCategory.TIMEOUT),
    ("Test execution timed out - 30 minutes limit", FailureCategory.TIMEOUT),
    ("Deploy timed out - maximum duration exceeded", FailureCategory.TIMEOUT),

    # PERMISSION_ERROR (20)
    ("403 Forbidden - access denied to repository", FailureCategory.PERMISSION_ERROR),
    ("401 Unauthorized - invalid or expired token", FailureCategory.PERMISSION_ERROR),
    ("Permission denied (publickey) - SSH key not authorized", FailureCategory.PERMISSION_ERROR),
    ("Authentication failed - invalid credentials", FailureCategory.PERMISSION_ERROR),
    ("Invalid token - personal access token expired", FailureCategory.PERMISSION_ERROR),
    ("Access denied - insufficient permissions for repository", FailureCategory.PERMISSION_ERROR),
    ("403 Forbidden - resource not accessible by integration", FailureCategory.PERMISSION_ERROR),
    ("401 Unauthorized - Bad credentials", FailureCategory.PERMISSION_ERROR),
    ("Permission denied (publickey) - deploy key not configured", FailureCategory.PERMISSION_ERROR),
    ("Authentication failed - SSH key passphrase required", FailureCategory.PERMISSION_ERROR),
    ("Invalid GitHub token - token has expired", FailureCategory.PERMISSION_ERROR),
    ("Access denied - repository is private", FailureCategory.PERMISSION_ERROR),
    ("403 Forbidden - GitHub API rate limit exceeded", FailureCategory.PERMISSION_ERROR),
    ("Permission denied - write access required", FailureCategory.PERMISSION_ERROR),
    ("Invalid token - OAuth token revoked", FailureCategory.PERMISSION_ERROR),
    ("Authentication failed - two-factor authentication required", FailureCategory.PERMISSION_ERROR),
    ("Permission denied (publickey) - key type not supported", FailureCategory.PERMISSION_ERROR),
    ("403 Forbidden - organization policy prevents access", FailureCategory.PERMISSION_ERROR),
    ("Access denied - branch protection rules", FailureCategory.PERMISSION_ERROR),
    ("Authentication failed - SAML authentication required", FailureCategory.PERMISSION_ERROR),
]


def get_fixtures() -> list:
    """Return all synthetic fixtures."""
    return SYNTHETIC_FIXTURES


def get_fixtures_by_category() -> dict:
    """Return fixtures grouped by category."""
    by_category = {cat: [] for cat in FailureCategory}
    for log, cat in SYNTHETIC_FIXTURES:
        by_category[cat].append(log)
    return by_category


if __name__ == "__main__":
    print(f"Total fixtures: {len(SYNTHETIC_FIXTURES)}")
    by_cat = get_fixtures_by_category()
    for cat in FailureCategory:
        print(f"  {cat.value}: {len(by_cat[cat])} fixtures")
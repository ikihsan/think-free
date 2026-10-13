#!/usr/bin/env python3
"""
E122 — CI/CD pipeline failure classifier.

Classifies failed GitHub Actions workflow run logs into failure categories.
Patterns are DECLARED BEFORE MEASUREMENT and not tuned post-hoc.
"""

import re
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum


class FailureCategory(Enum):
    TEST_FAILURE = "test_failure"
    DEPENDENCY_ERROR = "dependency_error"
    FLAKY_TEST = "flaky_test"
    ENVIRONMENT_ERROR = "environment_error"
    COMPILE_ERROR = "compile_error"
    TIMEOUT = "timeout"
    PERMISSION_ERROR = "permission_error"
    UNKNOWN = "unknown"


@dataclass
class ClassificationResult:
    category: FailureCategory
    confidence: float
    matched_patterns: List[str]


# DECLARED PATTERNS — fixed before any real data fetch
# Each pattern is (regex, category, description)
FAILURE_PATTERNS = [
    # Test failures - unit/integration test failures
    (re.compile(r'\bFAILED\b.*\btest\b', re.IGNORECASE), FailureCategory.TEST_FAILURE, "FAILED test"),
    (re.compile(r'\bAssertionError\b'), FailureCategory.TEST_FAILURE, "AssertionError"),
    (re.compile(r'pytest.*\bFAILED\b', re.IGNORECASE), FailureCategory.TEST_FAILURE, "pytest FAILED"),
    (re.compile(r'\btest.*\bfailed\b', re.IGNORECASE), FailureCategory.TEST_FAILURE, "test failed"),
    (re.compile(r'\bjunit\b.*\bfailure\b', re.IGNORECASE), FailureCategory.TEST_FAILURE, "junit failure"),
    (re.compile(r'\bTest\b.*\bFailed\b', re.IGNORECASE), FailureCategory.TEST_FAILURE, "Test Failed"),
    (re.compile(r'FAIL:\s*\S+'), FailureCategory.TEST_FAILURE, "FAIL: test_name"),
    
    # Dependency errors - missing/broken dependencies
    (re.compile(r'\bModuleNotFoundError\b'), FailureCategory.DEPENDENCY_ERROR, "ModuleNotFoundError"),
    (re.compile(r'\bImportError\b'), FailureCategory.DEPENDENCY_ERROR, "ImportError"),
    (re.compile(r'npm\s+ERR!', re.IGNORECASE), FailureCategory.DEPENDENCY_ERROR, "npm ERR!"),
    (re.compile(r'\bcargo\s+build\s+failed\b', re.IGNORECASE), FailureCategory.DEPENDENCY_ERROR, "cargo build failed"),
    (re.compile(r'\bpip\s+install.*\bfailed\b', re.IGNORECASE), FailureCategory.DEPENDENCY_ERROR, "pip install failed"),
    (re.compile(r'\bNo\ such\ file\ or\ directory.*requirements', re.IGNORECASE), FailureCategory.DEPENDENCY_ERROR, "missing requirements"),
    (re.compile(r'\bCould\ not\ find\ a\ version\b', re.IGNORECASE), FailureCategory.DEPENDENCY_ERROR, "version not found"),
    (re.compile(r'\bdependency\b.*\bnot\ found\b', re.IGNORECASE), FailureCategory.DEPENDENCY_ERROR, "dependency not found"),
    (re.compile(r'\bPackage\b.*\bnot\ found\b', re.IGNORECASE), FailureCategory.DEPENDENCY_ERROR, "package not found"),
    (re.compile(r'\bCannot\ resolve\b', re.IGNORECASE), FailureCategory.DEPENDENCY_ERROR, "cannot resolve"),
    
    # Flaky tests - intermittent failures (harder to detect from single log)
    # These patterns suggest flakiness but single-run detection is limited
    (re.compile(r'\bflaky\b', re.IGNORECASE), FailureCategory.FLAKY_TEST, "flaky keyword"),
    (re.compile(r'\bintermittent\b', re.IGNORECASE), FailureCategory.FLAKY_TEST, "intermittent keyword"),
    (re.compile(r'\bTimed\ out\b.*\btest\b', re.IGNORECASE), FailureCategory.FLAKY_TEST, "test timeout"),
    (re.compile(r'\bRetry\b', re.IGNORECASE), FailureCategory.FLAKY_TEST, "retry keyword"),
    
    # Environment errors - runner/environment issues
    (re.compile(r'\bdocker:\s*not\ found\b', re.IGNORECASE), FailureCategory.ENVIRONMENT_ERROR, "docker not found"),
    (re.compile(r'\bpermission\s+denied\b', re.IGNORECASE), FailureCategory.ENVIRONMENT_ERROR, "permission denied"),
    (re.compile(r'\bout\ of\ memory\b', re.IGNORECASE), FailureCategory.ENVIRONMENT_ERROR, "out of memory"),
    (re.compile(r'\bOOM\b|out.of.memory', re.IGNORECASE), FailureCategory.ENVIRONMENT_ERROR, "OOM"),
    (re.compile(r'\bno\ space\ left\ on\ device\b', re.IGNORECASE), FailureCategory.ENVIRONMENT_ERROR, "no space left"),
    (re.compile(r'\bcommand\ not\ found\b', re.IGNORECASE), FailureCategory.ENVIRONMENT_ERROR, "command not found"),
    (re.compile(r'\bexecutable\ file\ not\ found\b', re.IGNORECASE), FailureCategory.ENVIRONMENT_ERROR, "executable not found"),
    (re.compile(r'\bcannot\ allocate\ memory\b', re.IGNORECASE), FailureCategory.ENVIRONMENT_ERROR, "cannot allocate memory"),
    (re.compile(r'\bsegmentation\ fault\b', re.IGNORECASE), FailureCategory.ENVIRONMENT_ERROR, "segfault"),
    (re.compile(r'\bkilled\b', re.IGNORECASE), FailureCategory.ENVIRONMENT_ERROR, "process killed"),
    
    # Compile errors - code compilation failed
    (re.compile(r'\bSyntaxError\b'), FailureCategory.COMPILE_ERROR, "SyntaxError"),
    (re.compile(r'\bTypeError\b.*\bcompil', re.IGNORECASE), FailureCategory.COMPILE_ERROR, "TypeError compilation"),
    (re.compile(r'\bcompilation\s+failed\b', re.IGNORECASE), FailureCategory.COMPILE_ERROR, "compilation failed"),
    (re.compile(r'\bBuild\ failed\b', re.IGNORECASE), FailureCategory.COMPILE_ERROR, "Build failed"),
    (re.compile(r'\berror:\s*.*\.(c|cpp|rs|go|java|ts):\d+:', re.IGNORECASE), FailureCategory.COMPILE_ERROR, "compiler error format"),
    (re.compile(r'\bundefined\ reference\b', re.IGNORECASE), FailureCategory.COMPILE_ERROR, "undefined reference"),
    (re.compile(r'\bld:\s*error\b', re.IGNORECASE), FailureCategory.COMPILE_ERROR, "linker error"),
    (re.compile(r'\bcannot\ find\ -l\b', re.IGNORECASE), FailureCategory.COMPILE_ERROR, "missing library"),
    
    # Timeout - step exceeded time limit
    (re.compile(r'\bThe\ operation\ was\ canceled\b', re.IGNORECASE), FailureCategory.TIMEOUT, "operation canceled"),
    (re.compile(r'\btimeout\b', re.IGNORECASE), FailureCategory.TIMEOUT, "timeout keyword"),
    (re.compile(r'\bexceeded\.*\btime\b', re.IGNORECASE), FailureCategory.TIMEOUT, "exceeded time"),
    (re.compile(r'\bjob\ was\ canceled\b', re.IGNORECASE), FailureCategory.TIMEOUT, "job canceled"),
    (re.compile(r'\bstep\ timed\ out\b', re.IGNORECASE), FailureCategory.TIMEOUT, "step timed out"),
    
    # Permission errors - auth/permission issues
    (re.compile(r'\b403\b\s*Forbidden', re.IGNORECASE), FailureCategory.PERMISSION_ERROR, "403 Forbidden"),
    (re.compile(r'\b401\b\s*Unauthorized', re.IGNORECASE), FailureCategory.PERMISSION_ERROR, "401 Unauthorized"),
    (re.compile(r'\bPermission\ denied\b\s*\(publickey\)', re.IGNORECASE), FailureCategory.PERMISSION_ERROR, "permission denied publickey"),
    (re.compile(r'\bauthentication\ failed\b', re.IGNORECASE), FailureCategory.PERMISSION_ERROR, "authentication failed"),
    (re.compile(r'\binvalid\ token\b', re.IGNORECASE), FailureCategory.PERMISSION_ERROR, "invalid token"),
    (re.compile(r'\baccess\ denied\b', re.IGNORECASE), FailureCategory.PERMISSION_ERROR, "access denied"),
]


def classify_log(log_text: str) -> ClassificationResult:
    """
    Classify a log text into a failure category.
    
    Strategy (declared before measurement):
    1. Check all patterns in order, collect matches
    2. Return category with most matches, or highest priority if tied
    3. If no matches, return UNKNOWN
    """
    if not log_text or not log_text.strip():
        return ClassificationResult(FailureCategory.UNKNOWN, 0.0, [])
    
    matches_by_category = {cat: [] for cat in FailureCategory}
    
    for pattern, category, description in FAILURE_PATTERNS:
        if pattern.search(log_text):
            matches_by_category[category].append(description)
    
    # Find category with most matches
    best_category = FailureCategory.UNKNOWN
    best_count = 0
    best_patterns = []
    
    for category, patterns in matches_by_category.items():
        if len(patterns) > best_count:
            best_category = category
            best_count = len(patterns)
            best_patterns = patterns
        elif len(patterns) == best_count and len(patterns) > 0:
            # Tie-breaker: priority order (test_failure > dependency > compile > env > timeout > permission > flaky)
            priority = {
                FailureCategory.TEST_FAILURE: 7,
                FailureCategory.DEPENDENCY_ERROR: 6,
                FailureCategory.COMPILE_ERROR: 5,
                FailureCategory.ENVIRONMENT_ERROR: 4,
                FailureCategory.TIMEOUT: 3,
                FailureCategory.PERMISSION_ERROR: 2,
                FailureCategory.FLAKY_TEST: 1,
                FailureCategory.UNKNOWN: 0,
            }
            if priority[category] > priority[best_category]:
                best_category = category
                best_patterns = patterns
    
    if best_category == FailureCategory.UNKNOWN:
        return ClassificationResult(FailureCategory.UNKNOWN, 0.0, [])
    
    # Confidence based on number of matching patterns (capped at 1.0)
    confidence = min(best_count * 0.25, 1.0)
    
    return ClassificationResult(best_category, confidence, best_patterns)


def classify_batch(logs: List[str]) -> List[ClassificationResult]:
    """Classify a batch of log texts."""
    return [classify_log(log) for log in logs]


def evaluate_on_fixtures(fixtures: List[Tuple[str, FailureCategory]]) -> dict:
    """
    Evaluate classifier on synthetic fixtures.
    
    Args:
        fixtures: List of (log_text, expected_category) tuples
    
    Returns:
        Dict with accuracy, per-category metrics, confusion matrix
    """
    correct = 0
    total = len(fixtures)
    per_category = {cat: {'correct': 0, 'total': 0} for cat in FailureCategory}
    confusion = {cat: {cat2: 0 for cat2 in FailureCategory} for cat in FailureCategory}
    
    for log_text, expected in fixtures:
        result = classify_log(log_text)
        predicted = result.category
        
        per_category[expected]['total'] += 1
        confusion[expected][predicted] += 1
        
        if predicted == expected:
            correct += 1
            per_category[expected]['correct'] += 1
    
    accuracy = correct / total if total > 0 else 0.0
    
    # Per-category accuracy
    category_accuracy = {}
    for cat in FailureCategory:
        if per_category[cat]['total'] > 0:
            category_accuracy[cat.value] = per_category[cat]['correct'] / per_category[cat]['total']
        else:
            category_accuracy[cat.value] = None
    
    return {
        'accuracy': accuracy,
        'correct': correct,
        'total': total,
        'per_category_accuracy': category_accuracy,
        'confusion_matrix': {cat.value: {c.value: v for c, v in row.items()} for cat, row in confusion.items()},
        'per_category_counts': {cat.value: per_category[cat] for cat in FailureCategory},
    }


if __name__ == "__main__":
    # Quick self-test
    test_logs = [
        "FAILED test_user_login - AssertionError: expected True got False",
        "ModuleNotFoundError: No module named 'requests'",
        "npm ERR! code E404 Not Found - package@1.0.0",
        "SyntaxError: invalid syntax on line 42",
        "The operation was canceled due to timeout",
        "Permission denied (publickey) when pushing to origin",
        "docker: not found",
        "Some random log with no clear pattern",
    ]
    
    print("=== Classifier Self-Test ===")
    for log in test_logs:
        result = classify_log(log)
        print(f"  [{result.category.value}] (conf={result.confidence:.2f}) {log[:60]}...")
        if result.matched_patterns:
            print(f"    Patterns: {result.matched_patterns}")
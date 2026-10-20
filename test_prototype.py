"""Small prototype demonstrating view-count classification logic."""
import sys
sys.path.insert(0, 'tools')

from viewcount_core import NEED_INDICATORS, GENERIC_TERMS, classify_package, is_active, _matches_word_boundary
from viewcount_framework import compute_gates, classify_text

# Sample package descriptions (mix of need-related and random)
samples = [
    {'name': 'my-django-app', 'description': 'A web framework for building database-driven websites with authentication and admin interface.'},
    {'name': 'requests', 'description': 'Python HTTP for Humans.'},
    {'name': 'utils', 'description': 'Utility functions and common helpers for everyday programming tasks.'},
    {'name': 'numpy', 'description': 'Fundamental package for array computing with Python.'},
    {'name': 'logging-config', 'description': 'Structured logging configuration with rotation, formatting and monitoring dashboards.'},
    {'name': 'data-analysis-tool', 'description': 'Python script for cleaning and transforming CSV data files.'},
    {'name': 'core-lib', 'description': 'Core library providing basic data structures and algorithms.'},
    {'name': 'security-scanner', 'description': 'Tool for scanning codebases for security vulnerabilities and compliance issues.'},
]

print('=== View-Count Classification Prototype ===')
print()

for pkg in samples:
    cls = classify_package(pkg['description'])
    active = is_active(pkg)
    print(f'Package: {pkg["name"]}')
    print(f'  Description: {pkg["description"][:80]}...')
    print(f'  Classification: {cls}')
    print(f'  Has activity metadata: {active}')
    print()

# Compute gates on a simulated classification
classified = {'need-related': 0, 'random': 0}
active_count = {'need-related': 0, 'random': 0}

for pkg in samples:
    cls = classify_package(pkg['description'])
    classified[cls] += 1
    if is_active(pkg):
        active_count[cls] += 1

gates = compute_gates(classified, active_count, sum(classified.values()))

print('=== Gate Computation ===')
print(f'Classified: {classified}')
print(f'Active: {active_count}')
print(f'G1 (need_rate/random_rate >= 0.55): {gates["g1_pass"]} (ratio: {gates["g1_ratio"]*100:.1f}%)')
print(f'G2 (classified >= 100): {gates["g2_pass"]}')
print(f'G3 (both categories): {gates["g3_pass"]}')
print(f'G4 (classified >= 50): {gates["g4_pass"]}')
print(f'Conclusion: {gates["conclusion"]}')
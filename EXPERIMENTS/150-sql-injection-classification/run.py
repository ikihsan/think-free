#!/usr/bin/env python3
"""Run E150 SQL injection technique classification experiment."""
import sys
import importlib.util

# Load classifier module directly
spec = importlib.util.spec_from_file_location(
    "classifier", "/home/ubuntu/think-free/EXPERIMENTS/150-sql-injection-classification/classifier.py"
)
classifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(classifier)

# Load fixtures from JSONL file
fixture_path = "fixtures.jsonl"
fixtures = classifier.load_fixtures(type('obj', (object,), {'__path__': fixture_path})())

# Actually, just call the function directly
print(f"Loaded fixtures from {fixture_path}")
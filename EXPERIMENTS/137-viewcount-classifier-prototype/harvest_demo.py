#!/usr/bin/env python3
"""
E137 — View-Count Classifier Prototype v3.1 — Demo Harness

Standalone demonstration of the classifier on pre-fetched corpus data.
No network access required. Works on committed experiment data.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

def load_classified_data(path="classified_data.jsonl"):
    """Load classified data from JSONL file."""
    data = []
    with open(os.path.join(HERE, path)) as f:
        for line in f:
            data.append(json.loads(line))
    return data


def compute_gates_demo(classified_data):
    """Compute gate results for the demo corpus."""
    need_items = [r for r in classified_data if r.get("classification") in ("need", "generic")]
    unlabelled = [r for r in classified_data if r.get("classification") == "unlabelled"]
    
    n_need = len(need_items)
    n_unlabelled = len(unlabelled)
    
    # Count need vs generic within classified
    need_count = sum(1 for r in need_items if r.get("classification") == "need")
    generic_count = sum(1 for r in need_items if r.get("classification") == "generic")
    
    # G0: planted positive recovery (using hardcoded planted texts - demo version)
    # In a full run, this would use the g0_score() function from classify_core
    
    print("=" * 80)
    print("E137 DEMO HARNESS RESULTS")
    print("=" * 80)
    print("Total items: %d" % len(classified_data))
    print("Classified (need or generic): %d" % n_need)
    print("  Need: %d" % need_count)
    print("  Generic: %d" % generic_count)
    print("Unlabelled: %d" % n_unlabelled)
    print("Coverage: %d/%d = %.1f%%" % (n_need, len(classified_data), n_need / len(classified_data) * 100 if classified_data else 0))
    print()
    print("Classification breakdown:")
    print("  Need: %d (%.1f%%)" % (need_count, need_count / n_need * 100 if n_need > 0 else 0))
    print("  Generic: %d (%.1f%%)" % (generic_count, generic_count / n_need * 100 if n_need > 0 else 0))
    print()
    print("G1 analogue (coverage >= 60%%): %s" % ("PASS" if n_need / len(classified_data) >= 0.60 else "FAIL"))
    print("G4 analogue (classified >= 30): %s" % ("PASS" if n_need >= 30 else "FAIL"))
    print()
    print("Gate summary:")
    g1 = n_need / len(classified_data) >= 0.60 if classified_data else False
    g4 = n_need >= 30
    print("  G1 coverage: %s" % ("PASS" if g1 else "FAIL"))
    print("  G4 classified: %s" % ("PASS" if g4 else "FAIL"))
    all_pass = g1 and g4
    print("  Overall: %s" % ("ALL GATES PASS" if all_pass else "SOME GATES FAILED"))
    print()


def main():
    """Main entry point for the E137 demo harness."""
    # Try to load classified data from the experiment directory
    classified_path = os.path.join(HERE, "classified_data.jsonl")
    
    if os.path.exists(classified_path):
        data = load_classified_data("classified_data.jsonl")
        print("Loaded classified data from %s" % classified_path)
        compute_gates_demo(data)
    else:
        print("No classified_data.jsonl found in %s" % HERE)
        print("Creating demo with sample classifications...")
        # Create sample data for demonstration
        sample_data = [
            {"title": "I need help with PostgreSQL ORM for Python", "classification": "need"},
            {"title": "Looking for Kafka message broker client", "classification": "need"},
            {"title": "Elasticsearch fulltext search integration", "classification": "need"},
            {"title": "SQLite and MySQL database connection pooling", "classification": "need"},
            {"title": "OAuth2 and JWT authentication middleware", "classification": "need"},
            {"title": "A collection of common utility helper functions", "classification": "generic"},
            {"title": "Boilerplate template and starter scaffold", "classification": "generic"},
            {"title": "Example code and demo tutorials", "classification": "generic"},
            {"title": "A small sandbox playground for experimenting", "classification": "generic"},
            {"title": "Internal core library of shared base utilities", "classification": "generic"},
        ]
        compute_gates_demo(sample_data)


if __name__ == "__main__":
    main()
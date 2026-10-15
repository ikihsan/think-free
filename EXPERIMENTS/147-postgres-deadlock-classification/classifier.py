#!/usr/bin/env python3
"""
PostgreSQL Deadlock Report Classifier

Classifies deadlock reports into root cause categories using structural
pattern matching on lock modes, relation pairs, and query patterns.
"""

import re
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from enum import Enum


class Category(Enum):
    FK_LOCK_CONTENTION = "fk_lock_contention"
    INDEX_LOCK_CONTENTION = "index_lock_contention"
    TUPLE_LOCK_CONTENTION = "tuple_lock_contention"
    ADVISORY_LOCK_CONTENTION = "advisory_lock_contention"
    EXPLICIT_LOCK_CONTENTION = "explicit_lock_contention"
    UNKNOWN = "unknown"


@dataclass
class DeadlockReport:
    """Parsed deadlock report with extracted features."""
    raw_text: str
    waiting_process: Optional[str] = None
    blocking_process: Optional[str] = None
    wait_lock_mode: Optional[str] = None
    wait_lock_type: Optional[str] = None
    wait_relation: Optional[str] = None
    hold_lock_mode: Optional[str] = None
    hold_lock_type: Optional[str] = None
    hold_relation: Optional[str] = None
    waiting_query: Optional[str] = None
    blocking_query: Optional[str] = None
    tuple_location: Optional[str] = None
    advisory_lock_id: Optional[str] = None
    error_messages: List[str] = None

    def __post_init__(self):
        if self.error_messages is None:
            self.error_messages = []


class DeadlockParser:
    """Parses PostgreSQL deadlock report text into structured features."""

    # Patterns for extracting structured information
    PROCESS_WAIT_PATTERN = re.compile(
        r'Process\s+(\d+):\s+.*waits for\s+(\w+)\s+on\s+(?:relation\s+(\d+)|advisory lock\s+\(([^)]+)\)|tuple\s+\(([^)]+)\)\s+of\s+relation\s+(\d+))'
    )
    PROCESS_HOLD_PATTERN = re.compile(
        r'Process\s+(\d+):\s+.*holds\s+(\w+)\s+on\s+(?:relation\s+(\d+)|advisory lock\s+\(([^)]+)\)|tuple\s+\(([^)]+)\)\s+of\s+relation\s+(\d+))'
    )
    QUERY_PATTERN = re.compile(r'Process\s+(\d+):\s+Process\s+\d+:\s*(.+)$', re.MULTILINE)
    ERROR_PATTERN = re.compile(r'(ERROR:|DETAIL:|HINT:)\s*(.+)')
    DEADLOCK_PATTERN = re.compile(r'DETECTED DEADLOCK')

    def parse(self, text: str) -> DeadlockReport:
        """Parse deadlock report text into structured features."""
        report = DeadlockReport(raw_text=text)

        # Extract wait/hold information
        for match in self.PROCESS_WAIT_PATTERN.finditer(text):
            pid, lock_mode, relation, advisory, tuple_loc, tuple_rel = match.groups()
            report.waiting_process = pid
            report.wait_lock_mode = lock_mode
            if advisory:
                report.wait_lock_type = "advisory"
                report.advisory_lock_id = advisory
            elif tuple_loc:
                report.wait_lock_type = "tuple"
                report.tuple_location = tuple_loc
                report.wait_relation = tuple_rel
            else:
                report.wait_lock_type = "relation"
                report.wait_relation = relation

        for match in self.PROCESS_HOLD_PATTERN.finditer(text):
            pid, lock_mode, relation, advisory, tuple_loc, tuple_rel = match.groups()
            report.blocking_process = pid
            report.hold_lock_mode = lock_mode
            if advisory:
                report.hold_lock_type = "advisory"
                report.advisory_lock_id = advisory
            elif tuple_loc:
                report.hold_lock_type = "tuple"
                report.tuple_location = tuple_loc
                report.hold_relation = tuple_rel
            else:
                report.hold_lock_type = "relation"
                report.hold_relation = relation

        # Extract queries
        queries = self.QUERY_PATTERN.findall(text)
        if len(queries) >= 2:
            report.waiting_query = queries[0][1].strip()
            report.blocking_query = queries[1][1].strip()
        elif len(queries) == 1:
            report.waiting_query = queries[0][1].strip()

        # Extract error messages
        for match in self.ERROR_PATTERN.finditer(text):
            report.error_messages.append(match.group(2).strip())

        return report


class DeadlockClassifier:
    """Classifies deadlock reports into root cause categories."""

    def __init__(self, use_structural: bool = True):
        self.parser = DeadlockParser()
        self.use_structural = use_structural

        # Keyword patterns for baseline (keyword-only) classifier
        self.keyword_patterns = {
            Category.FK_LOCK_CONTENTION: [
                r'ShareLock', r'FOR KEY SHARE', r'FOR SHARE', r'FOR NO KEY UPDATE',
                r'FOR UPDATE', r'trigger', r'foreign key', r'references'
            ],
            Category.INDEX_LOCK_CONTENTION: [
                r'index', r'btree', r'hash', r'gin', r'gist', r'page', r'tuple',
                r'insert', r'unique', r'duplicate key'
            ],
            Category.TUPLE_LOCK_CONTENTION: [
                r'tuple', r'heap', r'update', r'delete', r'lock_tuple',
                r'FOR UPDATE', r'FOR NO KEY UPDATE', r'ctid'
            ],
            Category.ADVISORY_LOCK_CONTENTION: [
                r'advisory', r'pg_advisory_lock', r'pg_advisory_xact_lock',
                r'pg_try_advisory_lock'
            ],
            Category.EXPLICIT_LOCK_CONTENTION: [
                r'LOCK TABLE', r'pg_sleep', r'ExclusiveLock', r'AccessExclusiveLock'
            ],
        }

    def classify_keyword_only(self, text: str) -> Category:
        """Keyword-only baseline classifier."""
        scores = {cat: 0 for cat in Category if cat != Category.UNKNOWN}

        for cat, patterns in self.keyword_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    scores[cat] += 1

        if max(scores.values()) == 0:
            return Category.UNKNOWN

        return max(scores, key=scores.get)

    def classify_structural(self, report: DeadlockReport) -> Category:
        """Structural classifier using parsed features."""

        # Advisory lock contention: explicit advisory lock references
        if report.wait_lock_type == "advisory" or report.hold_lock_type == "advisory":
            if report.advisory_lock_id or 'pg_advisory' in report.raw_text:
                return Category.ADVISORY_LOCK_CONTENTION

        # Explicit lock contention: LOCK TABLE statements with AccessExclusiveLock/ExclusiveLock
        if report.wait_lock_mode in ('AccessExclusiveLock', 'ExclusiveLock') and \
           report.hold_lock_mode in ('AccessExclusiveLock', 'ExclusiveLock'):
            if 'LOCK TABLE' in report.raw_text:
                return Category.EXPLICIT_LOCK_CONTENTION

        # Tuple lock contention: same tuple/relation, RowExclusiveLock vs RowExclusiveLock
        if report.wait_lock_type == "tuple" and report.hold_lock_type == "tuple":
            if report.tuple_location and 'RowExclusiveLock' in (report.wait_lock_mode or '') and \
               'RowExclusiveLock' in (report.hold_lock_mode or ''):
                return Category.TUPLE_LOCK_CONTENTION

        # Check for tuple lock patterns in queries
        if report.waiting_query and report.blocking_query:
            waiting_upper = report.waiting_query.upper()
            blocking_upper = report.blocking_query.upper()

            # Explicit FOR UPDATE / FOR NO KEY UPDATE on same table
            if ('FOR UPDATE' in waiting_upper or 'FOR NO KEY UPDATE' in waiting_upper) and \
               ('FOR UPDATE' in blocking_upper or 'FOR NO KEY UPDATE' in blocking_upper or
                'UPDATE' in blocking_upper or 'DELETE' in blocking_upper):
                return Category.TUPLE_LOCK_CONTENTION

            # Concurrent UPDATE/DELETE on same table (implied same tuple)
            if ('UPDATE' in waiting_upper or 'DELETE' in waiting_upper) and \
               ('UPDATE' in blocking_upper or 'DELETE' in blocking_upper):
                # Check if they reference the same table/relation
                if report.wait_relation and report.hold_relation and \
                   report.wait_relation == report.hold_relation:
                    return Category.TUPLE_LOCK_CONTENTION

        # Index lock contention: ExclusiveLock on relation with INSERT/unique constraint errors
        if report.wait_lock_mode == 'ExclusiveLock' and report.hold_lock_mode == 'ExclusiveLock':
            if 'duplicate key' in report.raw_text.lower() or 'unique constraint' in report.raw_text.lower():
                return Category.INDEX_LOCK_CONTENTION
            # Concurrent INSERTs into same table with index
            if report.waiting_query and report.blocking_query:
                waiting_upper = report.waiting_query.upper()
                blocking_upper = report.blocking_query.upper()
                if 'INSERT' in waiting_upper and 'INSERT' in blocking_upper:
                    return Category.INDEX_LOCK_CONTENTION

        # FK lock contention: ShareLock wait, RowExclusiveLock hold, FK pattern in queries
        if report.wait_lock_mode == 'ShareLock' and report.hold_lock_mode == 'RowExclusiveLock':
            if report.waiting_query and report.blocking_query:
                waiting_upper = report.waiting_query.upper()
                blocking_upper = report.blocking_query.upper()
                # INSERT on child table, UPDATE on parent table
                if 'INSERT' in waiting_upper and 'UPDATE' in blocking_upper:
                    return Category.FK_LOCK_CONTENTION
                # FK-related patterns
                if any(kw in report.raw_text.lower() for kw in ['foreign key', 'references', 'trigger']):
                    return Category.FK_LOCK_CONTENTION

        # Fallback: check for FK patterns more broadly
        if 'ShareLock' in report.raw_text and 'RowExclusiveLock' in report.raw_text:
            if 'INSERT' in report.raw_text.upper() and 'UPDATE' in report.raw_text.upper():
                return Category.FK_LOCK_CONTENTION

        return Category.UNKNOWN

    def classify(self, text: str) -> Category:
        """Main classification entry point."""
        report = self.parser.parse(text)

        if self.use_structural:
            return self.classify_structural(report)
        else:
            return self.classify_keyword_only(text)


def load_fixtures(path: str) -> List[Dict]:
    """Load synthetic fixtures from JSONL file."""
    import json
    fixtures = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                fixtures.append(json.loads(line))
    return fixtures


def evaluate_classifier(fixtures: List[Dict], use_structural: bool = True) -> Dict:
    """Evaluate classifier on fixtures."""
    classifier = DeadlockClassifier(use_structural=use_structural)

    correct = 0
    total = len(fixtures)
    per_category = {}
    confusion = {}

    for fixture in fixtures:
        true_cat = Category(fixture['category'])
        pred_cat = classifier.classify(fixture['text'])

        if true_cat not in per_category:
            per_category[true_cat] = {'correct': 0, 'total': 0}
        if true_cat not in confusion:
            confusion[true_cat] = {}

        per_category[true_cat]['total'] += 1
        if pred_cat not in confusion[true_cat]:
            confusion[true_cat][pred_cat] = 0
        confusion[true_cat][pred_cat] += 1

        if pred_cat == true_cat:
            correct += 1
            per_category[true_cat]['correct'] += 1

    return {
        'accuracy': correct / total if total > 0 else 0,
        'correct': correct,
        'total': total,
        'per_category': {cat.value: v for cat, v in per_category.items()},
        'confusion': {cat.value: {p.value: c for p, c in preds.items()} for cat, preds in confusion.items()}
    }


if __name__ == '__main__':
    import sys
    fixtures = load_fixtures('fixtures.jsonl')

    print("=== Structural Classifier ===")
    struct_results = evaluate_classifier(fixtures, use_structural=True)
    print(f"Accuracy: {struct_results['accuracy']:.1%} ({struct_results['correct']}/{struct_results['total']})")
    for cat, stats in struct_results['per_category'].items():
        acc = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        print(f"  {cat}: {acc:.1%} ({stats['correct']}/{stats['total']})")

    print("\n=== Keyword-Only Baseline ===")
    kw_results = evaluate_classifier(fixtures, use_structural=False)
    print(f"Accuracy: {kw_results['accuracy']:.1%} ({kw_results['correct']}/{kw_results['total']})")
    for cat, stats in kw_results['per_category'].items():
        acc = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        print(f"  {cat}: {acc:.1%} ({stats['correct']}/{stats['total']})")

    delta = struct_results['accuracy'] - kw_results['accuracy']
    print(f"\nDelta (structural - keyword): {delta:.1%}")
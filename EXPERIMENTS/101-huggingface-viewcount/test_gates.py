#!/usr/bin/env python3
"""Unit tests for E101 gate evaluation using synthetic fixtures."""

import json
import os
import sys
import unittest

# Add parent directory to path for outcome module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from outcome import evaluate_gates, wilson_lower_bound, welch_t_test


class TestGateLogic(unittest.TestCase):
    """Test gate evaluation logic with synthetic fixtures."""
    
    def setUp(self):
        fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")
        with open(os.path.join(fixtures_dir, "need-related-sample.json")) as f:
            self.need_related = json.load(f)
        with open(os.path.join(fixtures_dir, "random-sample.json")) as f:
            self.random = json.load(f)
    
    def test_wilson_lower_bound(self):
        # 10 active out of 10 = 1.0, lower bound should be > 0.6
        lb = wilson_lower_bound(10, 10)
        self.assertGreater(lb, 0.6)
        
        # 0 active out of 10 = 0.0, lower bound should be ~0
        lb = wilson_lower_bound(0, 10)
        self.assertLess(abs(lb), 1e-10)
        
        # 6 active out of 10 = 0.6, lower bound should be < 0.6
        lb = wilson_lower_bound(6, 10)
        self.assertLess(lb, 0.6)
    
    def test_welch_t_test(self):
        # Clear difference: 1.0 vs 0.0
        t, p = welch_t_test(1.0, 5, 0.0, 5)
        self.assertLess(p, 0.05)
        self.assertGreater(t, 0)
        
        # No difference: 0.5 vs 0.5
        t, p = welch_t_test(0.5, 10, 0.5, 10)
        self.assertGreater(p, 0.05)
    
    def test_fixture_gates_pass(self):
        """Synthetic fixtures should pass all gates (designed to)."""
        results = evaluate_gates(self.need_related, self.random)
        
        self.assertTrue(results["g1_retrieval"]["pass"], "G1 should pass with 5 models per arm")
        self.assertTrue(results["g2_activity_difference"]["pass"], "G2 should pass with clear rate difference")
        self.assertTrue(results["g3_need_related_floor"]["pass"], "G3 should pass with 100% active rate")
        self.assertTrue(results["summary"]["overall_pass"], "All gates should pass with designed fixtures")
    
    def test_g1_fails_with_insufficient_models(self):
        """G1 should fail with < 30 models per arm."""
        results = evaluate_gates(self.need_related[:2], self.random[:2])
        self.assertFalse(results["g1_retrieval"]["pass"])
    
    def test_g2_fails_with_no_difference(self):
        """G2 should fail when rates are equal."""
        # Make both arms have same activity
        need_related_modified = [dict(m, downloads=200) for m in self.need_related]
        random_modified = [dict(m, downloads=200) for m in self.random]
        results = evaluate_gates(need_related_modified, random_modified)
        self.assertFalse(results["g2_activity_difference"]["pass"])
    
    def test_g3_fails_with_low_active_rate(self):
        """G3 should fail when Wilson lower bound < 0.6."""
        # Make only 15 out of 30 active = 0.5 rate, Wilson LB < 0.6
        need_related_low = []
        for i, m in enumerate(self.need_related):
            if i < 15:
                need_related_low.append(dict(m, downloads=200))
            else:
                need_related_low.append(dict(m, downloads=50))
        results = evaluate_gates(need_related_low, self.random)
        self.assertFalse(results["g3_need_related_floor"]["pass"])


if __name__ == "__main__":
    unittest.main()
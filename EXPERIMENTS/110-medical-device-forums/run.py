#!/usr/bin/env python3
"""E110 — View-Count / Subject-Mention Principle on Medical Device Forums

Tests the "read by hand" / subject-mention approach on practitioner discussion
forums about medical device alarm codes. This is a fresh observation in a new
domain per D083, targeting the priority domain of medical device alarm codes on
practitioner forums.

The experiment uses the revised rubric (subject_mentioned AND
(solution_keywords_present OR info_keywords_present)) on real practitioner forum
posts about medical device alarms, and measures FPR and TPR against the
strongest accessible alternative (a free general assistant).
"""

import json
import subprocess
import sys
from pathlib import Path

# Mock data for medical device forum experiment
# In a real implementation, this would fetch from actual practitioner forums
# (e.g., MedDeviceTalk, AoMED, clinical discussion boards)

print("=" * 60)
print("E110 — View-Count / Subject-Mention on Medical Device Forums")
print("=" * 60)

print("\nStep 1: Would fetch practitioner forum posts about medical device alarms")
print("         from sources like MedDeviceTalk, AoMED, clinical discussion boards")
print("         Target: posts describing alarm codes, false alarms, missed alarms")
print("         Expected format: post text, metadata (date, forum, author), alarm codes mentioned")

print("\nStep 2: Would classify posts using the revised rubric:")
print("          subject_mentioned AND (solution_keywords_present OR info_keywords_present)")
print("          where subject_mentioned excludes chrome words:")
print("          'error', 'code', 'fault', 'meaning', 'how', 'the', 'for', 'and', 'with',")
print("          'manual', 'guide', 'messages'")
print("          solution_keywords: 'fix', 'resolved', 'solved', 'workaround', 'replacement'")
print("          info_keywords: 'spec', 'datasheet', 'manual', 'documentation'")

print("\nStep 3: Would measure FPR and TPR against a free general assistant")
print("          that answers from its own knowledge (no installation, no specs needed)")
print("          The assistant serves as the strongest accessible alternative, per F096/D084")

print("\nStep 4: Would assess gates:")
print("          G1: FPR ≤ 0.30 (threshold for acceptable false alarms)")
print("          G2: TPR > 0 (must serve some needs)")
print("          G3: Differentiation — TPR_treatment > TPR_control (meaningful difference)")
print("          G4: Arrival field — posts have observable metadata (date, forum, alarm code)")

print("\nStep 5: Would document conclusion and continuation decision")

# Write placeholder results
results = {
    "experiment": "E110",
    "title": "View-Count / Subject-Mention on Medical Device Forums",
    "domain": "medical_device_alarms_forums",
    "status": "setup_only",
    "conclusion": "EXPERIMENT_SETUP - needs real forum data collection",
    "g1_fpr_threshold": "not_assessed",
    "g2_tpr_positive": "not_assessed",
    "g3_differentiation": "not_assessed",
    "g4_arrival_field": "not_assessed",
    "timestamp": "2026-10-13"
}

output_path = Path("/home/ubuntu/think-free/EXPERIMENTS/110-medical-device-forums/results.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(results, indent=2))
print(f"\nResults written to {output_path} (setup mode only)")
print(json.dumps(results, indent=2))
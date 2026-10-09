#!/usr/bin/env python3
"""
Matching algorithm for E080 food recall matching experiment.
Matches purchase records to recall records using multiple strategies.
"""

import json
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from difflib import SequenceMatcher

@dataclass
class MatchResult:
    purchase_id: str
    recall_id: Optional[str]
    match_type: str  # "upc_exact", "upc_prefix", "name_fuzzy", "lot_date", "none"
    confidence: float

def normalize_upc(upc: str) -> str:
    """Normalize UPC for comparison."""
    return re.sub(r'\D', '', upc or '')

def normalize_name(name: str) -> str:
    """Normalize product name for fuzzy matching."""
    if not name:
        return ""
    # Remove common words, lowercase, remove punctuation
    name = name.lower()
    name = re.sub(r'[^\w\s]', ' ', name)
    stopwords = {'organic', 'natural', 'plain', 'original', 'classic', 'fresh', 'frozen',
                 'oz', 'lb', 'ct', 'pack', 'package', 'size', 'net', 'wt', 'weight',
                 'fluid', 'fl', 'ml', 'l', 'g', 'kg', 'count', 'piece', 'pieces'}
    words = [w for w in name.split() if w not in stopwords and len(w) > 1]
    return ' '.join(words)

def fuzzy_match(a: str, b: str, threshold: float = 0.75) -> bool:
    """Fuzzy string match using SequenceMatcher."""
    if not a or not b:
        return False
    return SequenceMatcher(None, a, b).ratio() >= threshold

def match_purchase_to_recall(purchase: Dict, recalls: List[Dict]) -> MatchResult:
    """
    Match a single purchase to recalls using cascading strategies.
    Returns the best match or None.
    """
    purchase_id = purchase["purchase_id"]
    purchase_upc = normalize_upc(purchase.get("upc", ""))
    purchase_name = normalize_name(purchase.get("product_name", ""))
    purchase_lot = purchase.get("lot_code", "").strip().upper()
    purchase_best_by = purchase.get("best_by", "").strip()
    purchase_store = purchase.get("store", "").strip().lower()
    purchase_date = purchase.get("date", "").strip()
    
    best_match = None
    best_confidence = 0.0
    best_type = "none"
    
    for recall in recalls:
        recall_id = recall["recall_id"]
        recall_upc = normalize_upc(recall.get("upc", ""))
        recall_name = normalize_name(recall.get("product_description", ""))
        recall_lot = recall.get("lot_code", "").strip().upper()
        recall_best_by = recall.get("best_by_date", "").strip()
        recall_distribution = recall.get("distribution_pattern", "").lower()
        recall_status = recall.get("status", "").lower()
        
        # Skip terminated recalls? No - they're still relevant for products in homes
        confidence = 0.0
        match_type = "none"
        
        # Strategy 1: Exact UPC match (highest confidence)
        if purchase_upc and recall_upc and purchase_upc == recall_upc:
            # Additional check: lot code if both present
            if purchase_lot and recall_lot:
                if purchase_lot == recall_lot:
                    confidence = 1.0
                    match_type = "upc_exact_lot"
                else:
                    confidence = 0.3  # UPC matches but lot differs
                    match_type = "upc_exact_lot_mismatch"
            elif purchase_best_by and recall_best_by:
                if purchase_best_by == recall_best_by:
                    confidence = 0.95
                    match_type = "upc_exact_date"
                else:
                    confidence = 0.7  # UPC matches, date unknown or differs
                    match_type = "upc_exact"
            else:
                confidence = 0.85
                match_type = "upc_exact"
            
            # Distribution check
            if "nationwide" not in recall_distribution and purchase_store:
                store_upper = purchase_store.upper()
                if store_upper not in recall_distribution.upper():
                    confidence *= 0.5  # Reduce confidence if store not in distribution
        
        # Strategy 2: UPC prefix match (for truncated receipt UPCs)
        elif purchase_upc and recall_upc and len(purchase_upc) >= 6:
            if recall_upc.endswith(purchase_upc) or purchase_upc == recall_upc[-len(purchase_upc):]:
                confidence = 0.6
                match_type = "upc_prefix"
                # Boost with name match
                if purchase_name and recall_name and fuzzy_match(purchase_name, recall_name):
                    confidence = 0.75
                    match_type = "upc_prefix_name"
        
        # Strategy 3: Fuzzy name match (for manual entry, no UPC)
        elif purchase_name and recall_name:
            similarity = SequenceMatcher(None, purchase_name, recall_name).ratio()
            if similarity >= 0.75:
                confidence = 0.5 * similarity
                match_type = "name_fuzzy"
                # Boost with date proximity
                if purchase_date and recall.get("recall_initiation_date"):
                    try:
                        p_date = int(purchase_date)
                        r_date = int(recall["recall_initiation_date"])
                        if abs(p_date - r_date) <= 60:  # Within 60 days
                            confidence += 0.1
                    except ValueError:
                        pass
        
        # Strategy 4: Lot code + date match (rare but definitive)
        if purchase_lot and recall_lot and purchase_lot == recall_lot:
            if purchase_best_by and recall_best_by and purchase_best_by == recall_best_by:
                confidence = max(confidence, 0.9)
                match_type = "lot_date"
        
        if confidence > best_confidence:
            best_confidence = confidence
            best_match = recall_id
            best_type = match_type
    
    # Apply confidence threshold
    if best_confidence < 0.4:
        best_match = None
        best_type = "none"
        best_confidence = 0.0
    
    return MatchResult(
        purchase_id=purchase_id,
        recall_id=best_match,
        match_type=best_type,
        confidence=best_confidence
    )

def run_matching(purchases: List[Dict], recalls: List[Dict]) -> List[MatchResult]:
    """Run matching on all purchases."""
    return [match_purchase_to_recall(p, recalls) for p in purchases]

def evaluate_results(results: List[MatchResult], ground_truth: Dict[str, Optional[str]]) -> Dict:
    """Compute precision, recall, and other metrics."""
    tp = fp = fn = tn = 0
    
    for r in results:
        true_recall = ground_truth.get(r.purchase_id)
        pred_recall = r.recall_id
        
        if true_recall and pred_recall:
            if true_recall == pred_recall:
                tp += 1
            else:
                # Wrong recall matched
                fp += 1
                fn += 1
        elif true_recall and not pred_recall:
            fn += 1
        elif not true_recall and pred_recall:
            fp += 1
        else:
            tn += 1
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": f1,
        "total": len(results),
    }

if __name__ == "__main__":
    # Quick test
    import sys
    sys.path.insert(0, ".")
    from fixtures import generate_fixtures
    
    fixtures = generate_fixtures()
    recalls = fixtures["recalls"]
    
    for fmt in ["receipt", "loyalty_csv", "manual_entry"]:
        purchases = fixtures["purchases"][fmt]
        results = run_matching(purchases, recalls)
        
        # Build ground truth
        gt = {p["purchase_id"]: p["ground_truth_recall"] for p in purchases}
        metrics = evaluate_results(results, gt)
        
        print(f"\n{fmt}:")
        print(f"  TP={metrics['true_positives']} FP={metrics['false_positives']} FN={metrics['false_negatives']} TN={metrics['true_negatives']}")
        print(f"  Precision={metrics['precision']:.3f} Recall={metrics['recall']:.3f} F1={metrics['f1']:.3f}")
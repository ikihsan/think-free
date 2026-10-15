"""View-Count Principle Framework v4.

Split out of viewcount_core.py and vscode_adapter.py at the 300-line cap.
This half owns the framework, gate computation, and experimentation workflow.
The need-indicator vocabulary lives here shared across all experiments.

Principle: On platforms with per-request metadata (view_count/download_count/star_count),
need-related content has systematic activity advantages over random content.
Boundary condition: Does NOT generalize to Q&A forum venues, model hubs, or platforms
where effect size between need-related and random content is too small.

See EXPERIMENTS/ summary files for detailed per-domain results.
"""

import re
import json
import os
from collections import Counter
from typing import Dict, List, Optional, Tuple, Any

# ---------------------------------------------------------------------------
# Need-indicator classifier vocabulary (shared across all experiments)
# ---------------------------------------------------------------------------

# Generic terms that classify as "random" (not need-related)
# These are broad terms that appear in almost any description, so their presence
# suggests the item is general-purpose rather than need-specific.
GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "jar", "dependencies",
    "gem", "rake", "rails", "bundle", "assets", "snippet", "boilerplate",
    "template", "skeleton", "example", "sample", "hello", "quickstart",
    "sdk", "api", "docs", "tutorial", "guide", "intro", "basic",
    "starter", "skeleton", "minimal", "vanilla", "raw", "vanilla",
}

# Need-related indicators — whole-word boundary matching to reduce substring
# false positives (e.g., "database" should not match "databaseify").
NEED_INDICATORS = {
    "database", "cache", "auth", "security", "logging", "monitoring",
    "testing", "benchmark", "profiler", "tracing", "observability",
    "deployment", "ci", "cd", "pipeline", "build", "package",
    "network", "api", "client", "server", "framework", "engine",
    "parser", "lexer", "converter", "transform", "serializer",
    "validation", "sanitization", "encryption", "decryption",
    "compression", "decompression", "encoding", "decoding",
    "serialization", "deserialization", "persistance", "storage",
    "retrieval", "indexing", "search", "query", "aggregation",
    "reporting", "metrics", "observability", "dashboard",
    "debugging", "troubleshooting", "diagnostics", "audit",
    "compliance", "governance", "risk", "mitigation",
    "optimization", "performance", "scaling", "load",
    "queue", "messaging", "broker", "topic", "publish",
    "subscribe", "routing", "firehose", "stream",
    "cache", "redis", "memcached", "eviction",
    "queue", "rabbit", "kafka", "mqtt",
    "container", "docker", "kubernetes", "orchestration",
    "micro service", "distributed", "cluster",
}

# ---------------------------------------------------------------------------
# Core classifier utilities
# ---------------------------------------------------------------------------

def _matches_word_boundary(desc_lower: str, term: str) -> bool:
    """Check if *term* appears as a whole word in *desc_lower* (regex \b)."""
    return bool(re.search(r'\b' + re.escape(term) + r'\b', desc_lower))


def classify_text(description: str, *, 
                  need_indicators: Optional[set] = None,
                  generic_terms: Optional[set] = None) -> str:
    """Classify text as 'need-related' or 'random'.
    
    Classification order (highest to lowest confidence):
    1) Generic term present → random
    2) Need indicator present → need-related
    3) Default → random (lowest confidence)
    
    Returns the classification label.
    """
    if not description:
        return "random"
    
    desc_lower = description.lower()
    need_iv = need_indicators or NEED_INDICATORS
    gen_iv = generic_terms or GENERIC_TERMS
    
    # 1) Generic term → random (strong signal)
    for term in gen_iv:
        if _matches_word_boundary(desc_lower, term):
            return "random"
    
    # 2) Need indicator → need-related
    for term in need_iv:
        if _matches_word_boundary(desc_lower, term):
            return "need-related"
    
    # 3) Default → random
    return "random"


def classify_by_keywords(package_info: Dict[str, str],
                         need_indicators: Optional[set] = None,
                         generic_terms: Optional[set] = None) -> Optional[str]:
    """Supplementary classification using metadata fields beyond description.
    
    Checks the project name and other available text fields for need indicators.
    Returns 'need-related', 'random', or None if insufficient fields are present.
    """
    name = (package_info.get("name", "") or "").lower()
    desc = (package_info.get("description", "") or package_info.get("summary", "") or "").lower()
    ni = need_indicators or NEED_INDICATORS
    gt = generic_terms or GENERIC_TERMS
    
    # Check name first
    for term in ni:
        if _matches_word_boundary(name, term):
            return "need-related"
    for term in gt:
        if _matches_word_boundary(name, term):
            return "random"
    
    # Fall through to description-level classification
    return None


def is_active(package_info: Dict[str, str]) -> bool:
    """Check if a package/extension has significant activity metadata.
    
    For package registries: non-empty description AND version present.
    For extensions: non-empty description (analogue of version+description).
    """
    desc = package_info.get("description", "") or ""
    version = package_info.get("version", "") or ""
    if not desc.strip():
        return False
    if version and version != "" and version is not None:
        return True
    # For platforms where version isn't the analogue (e.g., extensions with just description)
    return len(desc.strip()) > 0


# ---------------------------------------------------------------------------
# Gate computation (G1-G4, adapted from E148/E161 pattern)
# ---------------------------------------------------------------------------

def compute_gates(classified: Dict[str, int], 
                  active: Dict[str, int],
                  total_classified: int,
                  min_classified: int = 50) -> Dict[str, Any]:
    """Compute G1-G4 gate results given classification and activity data.
    
    G1: need-related active rate >= 55% of random active rate
    G2: total classified >= 100
    G3: both categories represented (need-related > 0 and random > 0)
    G4: total classified >= min_classified
    
    Returns dict with gate results and diagnostic information.
    """
    g1_pass = False
    g2_pass = False
    g3_pass = False
    g4_pass = False
    need_rate = 0.0
    random_rate = 0.0
    ratio = 0.0
    
    if classified["need-related"] > 0 and classified["random"] > 0:
        need_rate = active["need-related"] / classified["need-related"]
        random_rate = active["random"] / classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= 0.55
    
    g2_pass = total_classified >= 100
    g3_pass = classified["need-related"] > 0 and classified["random"] > 0
    g4_pass = total_classified >= min_classified
    
    return {
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "g1_ratio": ratio,
        "g1_need_rate": need_rate,
        "g1_random_rate": random_rate,
        "classified_total": total_classified,
        "need_related_count": classified["need-related"],
        "random_count": classified["random"],
        "need_related_active": active["need-related"],
        "random_active": active["random"],
        "active_rates": {
            "need-related": need_rate,
            "random": random_rate,
        },
        "conclusion": "pending",
    }


# ---------------------------------------------------------------------------
# Experiment workflow framework
# ---------------------------------------------------------------------------

class ViewCountExperiment:
    """Framework for running a view-count principle experiment.
    
    Subclasses should implement:
    - fetch_data(keyword, max_results): fetch platform items
    - classify_item(item): classify as need-related or random
    - get_activity_metric(item): extract the activity metric (star/downloaded/etc)
    """
    
    def __init__(self, 
                 platform: str,
                 keyword: str,
                 max_results: int = 200,
                 min_classified: int = 50,
                 need_indicators: Optional[set] = None,
                 generic_terms: Optional[set] = None):
        self.platform = platform
        self.keyword = keyword
        self.max_results = max_results
        self.min_classified = min_classified
        self.need_indicators = need_indicators or NEED_INDICATORS
        self.generic_terms = generic_terms or GENERIC_TERMS
        self.results: Dict[str, Any] = {}
    
    def run(self) -> Dict[str, Any]:
        """Run the full experiment: fetch, classify, gate, report."""
        # Step 1: Fetch data
        items = self._fetch_data()
        if not items:
            self.results = self._empty_results("no_items_fetched")
            return self.results
        
        # Step 2: Classify and collect activity data
        classified = {"need-related": 0, "random": 0}
        active = {"need-related": 0, "random": 0}
        need_related_items = []
        
        for item in items:
            cls = self.classify_item(item)
            active_flag = self.is_item_active(item)
            
            classified[cls] += 1
            if active_flag:
                active[cls] += 1
            if cls == "need-related":
                need_related_items.append(item)
        
        # Step 3: Compute gates
        gates = compute_gates(
            classified, active, sum(classified.values()), self.min_classified
        )
        
        # Step 4: Build results
        self.results = {
            "observed_at_utc": __import__('time').strftime("%Y-%m-%dT%H:%M:%SZ", __import__('time').gmtime()),
            "user_date": __import__('time').strftime("%Y-%m-%d", __import__('time').gmtime()),
            "platform": self.platform,
            "keyword": self.keyword,
            "sample_size": len(items),
            "classified": classified,
            "active": active,
            "active_rates": gates["active_rates"],
            "gates": gates,
            "conclusion": self._determine_conclusion(gates),
            "experiment_description": f"View-count principle on {self.platform} for keyword: {self.keyword}",
        }
        
        # Add platform-specific notes
        if not gates["g1_pass"]:
            self.results["note"] = self.results.get("note", "") + "\n"
            self.results["note"] += f"G1 failure: need-related/random active rate ratio = {gates['g1_ratio']*100:.1f}% (threshold: 55%). "
        
        if not gates["g2_pass"]:
            self.results["note"] = self.results.get("note", "") + "\n"
            self.results["note"] += f"G2 failure: classified total = {gates['classified_total']} (threshold: 100). "
        
        if gates["g1_pass"] and gates["g2_pass"] and gates["g3_pass"] and gates["g4_pass"]:
            self.results["conclusion"] = "gates_all_pass"
        elif not gates["g1_pass"] and not gates["g2_pass"]:
            self.results["conclusion"] = "g1_and_g2_fail"
        
        return self.results
    
    def _fetch_data(self) -> List[Dict[str, Any]]:
        """Fetch data from the platform. To be implemented by subclass."""
        raise NotImplementedError
    
    def classify_item(self, item: Dict[str, Any]) -> str:
        """Classify an item as need-related or random. To be implemented by subclass."""
        raise NotImplementedError
    
    def is_item_active(self, item: Dict[str, Any]) -> bool:
        """Check if an item has activity metadata. To be implemented by subclass."""
        raise NotImplementedError
    
    def _empty_results(self, reason: str) -> Dict[str, Any]:
        return {
            "observed_at_utc": __import__('time').strftime("%Y-%m-%dT%H:%M:%SZ", __import__('time').gmtime()),
            "user_date": __import__('time').strftime("%Y-%m-%d", __import__('time').gmtime()),
            "platform": self.platform,
            "keyword": self.keyword,
            "sample_size": 0,
            "classified": {"need-related": 0, "random": 0},
            "active": {"need-related": 0, "random": 0},
            "active_rates": {"need-related": 0, "random": 0},
            "g1_pass": False,
            "g2_pass": False,
            "g3_pass": False,
            "g4_pass": False,
            "conclusion": reason,
            "experiment_description": f"View-count principle on {self.platform} for keyword: {self.keyword}",
            "note": f"Experiment aborted: {reason}",
        }
    
    def _determine_conclusion(self, gates: Dict[str, Any]) -> str:
        """Determine the experiment conclusion from gate results."""
        if gates["g1_pass"] and gates["g2_pass"] and gates["g3_pass"] and gates["g4_pass"]:
            return "gates_all_pass"
        elif not gates["g1_pass"] and not gates["g2_pass"]:
            return "g1_and_g2_fail"
        elif not gates["g1_pass"]:
            return "g1_fail"
        elif not gates["g2_pass"]:
            return "g2_fail"
        else:
            return "partial"


# ---------------------------------------------------------------------------
# Framework entry point
# ---------------------------------------------------------------------------

def list_need_indicators() -> List[str]:
    """Return the sorted list of need-indicator terms."""
    return sorted(NEED_INDICATORS)


def list_generic_terms() -> List[str]:
    """Return the sorted list of generic terms."""
    return sorted(GENERIC_TERMS)


def run_classification_demo(texts: List[str]) -> None:
    """Run a quick classification demo on a list of texts."""
    print("=== Classification Demo ===")
    for i, text in enumerate(texts):
        cls = classify_text(text)
        print(f"  {i+1}. [{cls}] {text[:80]}")


if __name__ == "__main__":
    # Quick demo
    demo_texts = [
        "A Python database connection pool with caching and monitoring",
        "A utility library for common operations",
        "A security authentication framework with OAuth2 support",
        "A tool for debugging web application issues",
    ]
    run_classification_demo(demo_texts)
    
    print("\n=== Need Indicators ===")
    for term in sorted(NEED_INDICATORS)[:10]:
        print(f"  - {term}")
    
    print("\n=== Generic Terms ===")
    for term in sorted(GENERIC_TERMS)[:10]:
        print(f"  - {term}")
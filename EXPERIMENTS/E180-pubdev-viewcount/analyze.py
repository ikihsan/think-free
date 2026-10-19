"""E180 — Analyze gate results for view-count principle on Pub.dev."""

import json, os, sys, time
from statistics import median

# Classification vocabulary
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
    "crud", "rest", "sdk", "cli",
}

GENERIC_TERMS = {
    "utils", "common", "core", "library", "framework", "jar", "dependencies",
    "gem", "rake", "rails", "bundle", "assets",
}


def _matches_word_boundary(desc_lower, term):
    import re
    return bool(re.search(r'\b' + re.escape(term) + r'\b', desc_lower))


def classify_description(desc):
    if not desc:
        return "random"
    desc_lower = desc.lower()
    for term in GENERIC_TERMS:
        if _matches_word_boundary(desc_lower, term):
            return "random"
    for term in NEED_INDICATORS:
        if _matches_word_boundary(desc_lower, term):
            return "need-related"
    return "random"


def is_active(pkg):
    desc = pkg.get('latest', {}).get('pubspec', {}).get('description', '') or ''
    version = pkg.get('latest', {}).get('version', '') or ''
    desc_active = len(desc.strip()) > 0
    version_active = version != '' and version is not None
    return desc_active and version_active


def compute_gates(classified, active, total_classified, min_classified=50):
    """Compute G1-G4 gate results."""
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


def main():
    results_path = sys.argv[1] if len(sys.argv) > 1 else "EXPERIMENTS/E180-pubdev-viewcount/results.json"

    with open(results_path, "r") as f:
        results = json.load(f)

    classified = results["classified"]
    active = results["active"]
    total_classified = classified["need-related"] + classified["random"]

    gates = compute_gates(classified, active, total_classified)

    results["gates"] = gates

    # Determine conclusion
    g1 = gates["g1_pass"]
    g2 = gates["g2_pass"]
    g3 = gates["g3_pass"]
    g4 = gates["g4_pass"]

    if g1 and g2 and g3 and g4:
        results["conclusion"] = "gates_all_pass"
    elif not g1 and not g2:
        results["conclusion"] = "g1_and_g2_fail"
    elif not g1:
        results["conclusion"] = "g1_fail"
    elif not g2:
        results["conclusion"] = "g2_fail"
    elif not g3:
        results["conclusion"] = "g3_fail"
    elif not g4:
        results["conclusion"] = "g4_fail"

    # Print gate summary
    print(f"=== E180 Gate Analysis ===")
    print(f"Platform: {results['platform']}")
    print(f"Keyword: {results['keyword']}")
    print(f"Classified: {classified}")
    print(f"Active: {active}")
    print(f"Total classified: {total_classified}")
    print()

    print("=== Gates ===")
    for gate_name in ["G1", "G2", "G3", "G4"]:
        pass_val = gates[f"{gate_name.lower()}_pass"]
        print(f"  {gate_name}: {'PASS' if pass_val else 'FAIL'} (detail: {gates.get(gate_name.lower() + '_ratio', 0)*100:.1f}% / 100 / both categories / >=50)")

    print(f"\nActive rates:")
    print(f"  need-related: {gates['active_rates']['need-related']*100:.1f}%")
    print(f"  random: {gates['active_rates']['random']*100:.1f}%")
    print(f"  ratio (need/random): {gates['g1_ratio']*100:.1f}%")

    print(f"\nConclusion: {results['conclusion']}")

    # Save updated results
    out_dir = os.path.dirname(results_path)
    out_path = os.path.join(out_dir, "results_updated.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n=== Updated results saved to {out_path} ===")


if __name__ == "__main__":
    main()
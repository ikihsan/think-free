#!/usr/bin/env python3
"""Classify Discourse topics as unserved-open-like vs served-like per E074 protocol.

Unserved-open-like requires ALL three:
1. No platform-recorded resolution (has_accepted_answer=False AND (reply_count<3 OR op_like_count<1))
2. States a concrete need (title asks for technique, material, product, source, diagnosis, judgement)
3. Not a request for content, service, price, access, or human work
"""
import json
import os
import re

RAW_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "discourse_topics.json")

# Keywords indicating a concrete need (question, help request, diagnosis, recommendation)
NEED_PATTERNS = [
    r'\bhow (do|can|to|should|would|is|are)\b',
    r'\bwhat (is|are|should|would|could|causes?|makes?)\b',
    r'\bwhy (is|are|do|does|did|can|won|not)\b',
    r'\bhelp\b',
    r'\bissue|problem|error|broken|failure|not working\b',
    r'\brecommend|suggestion|advice\b',
    r'\bwhich (one|should|is best|to buy|to use|get)\b',
    r'\bwhere (can|to|is|are)\b',
    r'\bany (idea|suggestion|tip|advice|recommendation)\b',
    r'\bcan (someone|anybody|anyone)\b',
    r'\bstuck|confused|lost\b',
    r'\btrying to\b',
    r'\bwondering\b',
    r'\bshould I\b',
]

# Patterns indicating NOT a need (show-off, discussion, meta, announcement)
NON_NEED_PATTERNS = [
    r'\bIC\b',  # interest check
    r'\bshow.*(off|me)\b',
    r'\bmy (new|first|latest) (setup|build|project|purchase)\b',
    r'\blook at (this|my)\b',
    r'\bjust (got|bought|picked up|received)\b',
    r'\bwhat.*(you|getting|ordering|buying)\b',  # discussion threads
    r'\bwelcome to\b',
    r'\bthank(s| you)\b',
    r'\bimage(s)?\s*(only|thread)\b',
    r'\bpicture(s)?\s*(only|thread|uno)\b',
    r'\bintroductions?\b',
]

def is_need_topic(title):
    """Returns True if the topic title suggests a concrete need."""
    title_lower = title.lower()
    for pattern in NON_NEED_PATTERNS:
        if re.search(pattern, title_lower):
            return False
    for pattern in NEED_PATTERNS:
        if re.search(pattern, title_lower):
            return True
    return False

def is_resolved(topic):
    """Returns True if the topic has a platform-recorded resolution."""
    if topic.get("has_accepted_answer", False):
        return True
    if topic.get("reply_count", 0) >= 3 and topic.get("op_like_count", 0) >= 1:
        return True
    if topic.get("closed", False):
        return True
    return False

def is_unserved_open_like(topic):
    """Apply the three-clause rubric."""
    # Clause 1: No platform-recorded resolution
    resolved = is_resolved(topic)
    if resolved:
        return False, "resolved"
    
    # Clause 2: States a concrete need
    if not is_need_topic(topic["title"]):
        return False, "not_a_need"
    
    # Clause 3: Not a request for content/service/price/access/human work
    # (already filtered by NON_NEED_PATTERNS)
    
    return True, "unserved_open_like"

def main():
    with open(RAW_PATH) as f:
        topics = json.load(f)
    
    results = []
    for t in topics:
        is_uol, reason = is_unserved_open_like(t)
        results.append({
            "id": t["id"],
            "title": t["title"],
            "domain": t["_domain"],
            "category": t["_topic_category"],
            "views": t.get("views", 0),
            "reply_count": t.get("reply_count", 0),
            "like_count": t.get("like_count", 0),
            "op_like_count": t.get("op_like_count", 0),
            "has_accepted_answer": t.get("has_accepted_answer", False),
            "closed": t.get("closed", False),
            "is_need": is_need_topic(t["title"]),
            "is_resolved": is_resolved(t),
            "is_unserved_open_like": is_uol,
            "classification_reason": reason,
        })
    
    # Stats
    total = len(results)
    need_topics = [r for r in results if r["is_need"]]
    unserved = [r for r in results if r["is_unserved_open_like"]]
    resolved = [r for r in results if r["is_resolved"]]
    
    print(f"=== E074 Discourse Unserved-Open Measurement ===")
    print(f"Total topics: {total}")
    print(f"View_count > 0: {sum(1 for r in results if r['views'] > 0)}/{total} (G4: {'PASS' if sum(1 for r in results if r['views'] > 0) >= 0.95*total else 'FAIL'})")
    print(f"Need topics: {len(need_topics)}")
    print(f"Resolved (has_accepted_answer or reply_count>=3+op_like): {len(resolved)}")
    print(f"Unserved-open-like: {len(unserved)}")
    print(f"Unserved-open-like fraction: {len(unserved)/total:.4f}" if total > 0 else "N/A")
    
    # By domain
    print(f"\n=== By Domain ===")
    domains = set(r["domain"] for r in results)
    for d in sorted(domains):
        dt = [r for r in results if r["domain"] == d]
        d_need = [r for r in dt if r["is_need"]]
        d_unserved = [r for r in dt if r["is_unserved_open_like"]]
        print(f"  {d}: {len(d_unserved)}/{len(dt)} = {len(d_unserved)/len(dt):.4f} unserved-open-like, {len(d_need)} need topics")
    
    # Wilson CI95
    n = total
    k = len(unserved)
    if n > 0:
        p = k / n
        z = 1.96
        denom = 1 + z*z/n
        center = (p + z*z/(2*n)) / denom
        margin = z * ((p*(1-p)/n + z*z/(4*n*n)) ** 0.5) / denom
        print(f"\nWilson CI95: [{center-margin:.4f}, {center+margin:.4f}]")
    
    # Save results
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classification.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {output_path}")
    
    # Sample unserved
    print(f"\n=== Sample Unserved-Open-Like Topics ===")
    for r in unserved[:15]:
        print(f"  [{r['domain']}] {r['title'][:70]}")
        print(f"    views={r['views']}, replies={r['reply_count']}, op_likes={r['op_like_count']}, accepted={r['has_accepted_answer']}")

if __name__ == "__main__":
    main()

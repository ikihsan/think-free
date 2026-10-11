#!/usr/bin/env python3
"""
E101 — Classification for network equipment fault codes domain.

Adapted from E077/E082 rubric for the network equipment fault/error code domain.
Classifies topics as: served, unserved-open-like, not_a_need.
"""

import os
import re
import sys
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Classification patterns for the network equipment domain
# ---------------------------------------------------------------------------

# Keyword patterns from E077/E076 classification, adapted for network equipment
NEED_PATTERNS = [
    r"\bhow (do|can|to|should|would|is|are)\b",
    r"\bwhat (is|are|should|would|causes?|makes?|mean)\b",
    r"\bwhy (is|are|do|does|did|can|won|not)\b",
    r"\bhelp\b",
    r"\bissue|problem|error|broken|failure|not working\b",
    r"\brecommend|suggestion|advice\b",
    r"\bwhich (one|should|is best|to buy|to use|get)\b",
    r"\bwhere (can|to|is|are)\b",
    r"\bany (idea|suggestion|tip|advice|recommendation)\b",
    r"\bcan (someone|anybody|anyone)\b",
    r"\bstuck|confused|lost\b",
    r"\btrying to\b",
    r"\bwondering\b",
    r"\bshould I\b",
    # Network-specific patterns
    r"\bconfig(ure)?\b",
    r"\bsetup\b",
    r"\btroubleshoot\b",
    r"\bdebug\b",
    r"\bdebugging\b",
    r"\bfault\b",
    r"\balarm\b",
    r"\berror code\b",
    r"\bcrash\b",
    r"\btraceback\b",
    r"\blog\b",
    r"\bdecode\b",
    r"\binterpret\b",
    r"\bmeaning of\b",
]

NON_NEED_PATTERNS = [
    r"\bIC\b",
    r"\bshow.*(off|me)\b",
    r"\bmy (new|first|latest) (setup|build|project|purchase)\b",
    r"\blook at (this|my)\b",
    r"\bjust (got|bought|picked up|received)\b",
    r"\bwhat.*(you|getting|ordering|buying)\b",
    r"\bwelcome to\b",
    r"\bthank(s| you)\b",
    r"\bimage(s)?\s*(only|thread)\b",
    r"\bpicture(s)?\s*(only|thread|uno)\b",
    r"\bintroductions?\b",
    # Network-specific non-need patterns
    r"\bannounc(e|ement)\b",
    r"\brelease\b",
    r"\bchangelog\b",
    r"\bversion\s+\d+",
    r"\bupgrade\b",
    r"\bdowngrade\b",
    r"\bcongrat\b",
    r"\bcongrats\b",
]


# ---------------------------------------------------------------------------
# Classification functions
# ---------------------------------------------------------------------------

def is_need_topic(title: str, body: str = "") -> bool:
    """Returns True if the topic suggests a concrete need involving fault codes.

    Checks title first, then body. A need topic asks for help with interpretation,
    lookup, debugging, or troubleshooting of fault/error codes.
    """
    text = f"{title.lower()} {body.lower()}"
    
    # First filter out non-need patterns
    for pattern in NON_NEED_PATTERNS:
        if re.search(pattern, text):
            return False
    # Then check need patterns
    for pattern in NEED_PATTERNS:
        if re.search(pattern, text):
            return True
    # If no pattern matches, it's not a need topic
    return False


def is_resolved(topic: Dict) -> bool:
    """Returns True if the topic has a platform-recorded resolution.

    For the network equipment domain, resolution means:
    - Accepted answer / solved status from the forum
    - Sufficient engagement indicating likely resolution (replies + OP likes)
    - Closed topic
    """
    # Check for accepted answer
    if topic.get("has_accepted_answer", False):
        return True
    # Check for sufficient engagement (reply_count >= 3 and op_like_count >= 1)
    if topic.get("reply_count", 0) >= 3 and topic.get("op_like_count", 0) >= 1:
        return True
    # Check if closed
    if topic.get("closed", False):
        return True
    return False


def extract_code_mentions(topic: Dict) -> List[str]:
    """Extract explicit fault/error/alarm codes mentioned in the topic."""
    import re
    
    codes = set()
    text = f"{topic.get('title', '')} {topic.get('body', '')}"
    
    # Cisco error codes: %CODE-SEVERITY-MNEMONIC (e.g., %LINK-3-UPDOWN)
    cisco_pattern = re.compile(r'%\w+-\d+-\w+')
    for m in cisco_pattern.finditer(text):
        codes.add(m.group(0))
    
    # MikroTik error messages: "error: ...", "failure: ..."
    mikrotik_pattern = re.compile(r'(?:error|failure):\s*\w+')
    for m in mikrotik_pattern.finditer(text, re.IGNORECASE):
        codes.add(m.group(0))
    
    # Juniper alarm codes: e.g., "ALARM: ...", "ALARM-..."
    juniper_pattern = re.compile(r'(?:ALARM|alarm)[-:]\s*\w+')
    for m in juniper_pattern.finditer(text):
        codes.add(m.group(0))
    
    # Generic error codes: ERR_XXX, ERROR_XXX, FAIL_XXX
    generic_pattern = re.compile(r'\b(?:ERR|ERROR|FAIL)[_\-]?[A-Z0-9]+\b', re.IGNORECASE)
    for m in generic_pattern.finditer(text):
        codes.add(m.group(0))
    
    # Hex codes
    hex_pattern = re.compile(r'\b0x[0-9a-fA-F]{1,8}\b')
    for m in hex_pattern.finditer(text):
        codes.add(m.group(0))
    
    # VLAN, interface, port error patterns
    interface_pattern = re.compile(r'\b(?:interface|port|vlan|vni|tunnel)\s+\w+', re.IGNORECASE)
    for m in interface_pattern.finditer(text):
        codes.add(m.group(0))
    
    return sorted(codes)


def classify_topics(topics: List[Dict]) -> List[Dict]:
    """Classify each topic using the network equipment fault-code rubric.
    
    Modifies topics in-place, adding:
    - is_need: bool
    - is_resolved: bool
    - is_unserved_open_like: bool
    - classification_reason: str
    - code_ids: List[str]  (extracted fault codes)
    """
    results: List[Dict] = []
    for t in topics:
        title = t.get("title", "")
        body = t.get("body", "")
        code_ids = extract_code_mentions(t)
        t["code_ids"] = code_ids
        
        resolved = is_resolved(t)
        is_need = is_need_topic(title, body)
        is_uol = is_need and not resolved
        
        t["is_need"] = is_need
        t["is_resolved"] = resolved
        t["is_unserved_open_like"] = is_uol
        t["classification_reason"] = "unserved_open_like" if is_uol else ("resolved" if resolved else "not_a_need")
        results.append(t)
    return results


def summarize_classification(topics: List[Dict]) -> Dict:
    """Produce summary statistics from classified topics."""
    total = len(topics)
    if total == 0:
        return {
            "total": 0,
            "need_fraction": 0,
            "served_fraction": 0,
            "unserved_open_like_fraction": 0,
            "served_count": 0,
            "unserved_open_like_count": 0,
            "not_need_count": 0,
            "vc_positive": 0,
            "view_positive_rate": 0,
            "need_count": 0,
        }
    
    need_count = sum(1 for t in topics if t.get("is_need", False))
    resolved_count = sum(1 for t in topics if t.get("is_resolved", False))
    uol_count = sum(1 for t in topics if t.get("is_unserved_open_like", False))
    
    # vc_positive = topics with view_count > 0
    vc_positive = sum(1 for t in topics if t.get("view_count", 0) > 0)
    
    # A topic is "served" if it has resolution AND is a need
    served_count = sum(1 for t in topics if t.get("is_resolved", False) and t.get("is_need", False))
    
    return {
        "total": total,
        "need_fraction": need_count / total if total else 0,
        "served_fraction": served_count / total if total else 0,
        "unserved_open_like_fraction": uol_count / total if total else 0,
        "served_count": served_count,
        "unserved_open_like_count": uol_count,
        "not_need_count": total - need_count,
        "vc_positive": vc_positive,
        "view_positive_rate": vc_positive / total if total else 0,
        "need_count": need_count,
    }


def check_gates(summary: Dict, need_threshold: int = 15) -> Dict:
    """Check predeclared gates against the summary."""
    gates: Dict = {
        "G1_need_prevalence": False,
        "G2_control_validity": False,
        "G3_unserved_fraction": False,
        "G4_view_count": False,
    }
    
    # G1: ≥ 15 need statements (vc_positive)
    gates["G1_need_prevalence"] = summary.get("need_count", 0) >= need_threshold
    
    # G2: Control validity - corpus ≥ 100 topics
    gates["G2_control_validity"] = summary.get("total", 0) >= 100
    
    # G3: Unserved-open-like fraction < 50%, CI95 upper < 60%
    uol_frac = summary.get("unserved_open_like_fraction", 1.0)
    total = summary.get("total", 1)
    if total > 0:
        ci_upper = uol_frac + 1.96 * (uol_frac * (1 - uol_frac) / total) ** 0.5
        gates["G3_unserved_fraction"] = uol_frac < 0.50 and ci_upper < 0.60
    else:
        gates["G3_unserved_fraction"] = False
    
    # G4: ≥ 95% of topics have view_count > 0
    gates["G4_view_count"] = summary.get("view_positive_rate", 0) >= 0.95
    
    return gates
#!/usr/bin/env python3
"""
E121 — Discourse-specific classifier for technical forums.

Combines E119 question-form patterns with E094 error/failure keywords
for better coverage on technical Discourse forums.
"""

import re
from collections import Counter


# Need-related indicators for Discourse forums
# Includes both question forms AND problem/technical keywords
DISCOURSE_NEED_PATTERNS = [
    # Question forms (from E119)
    r'\bhow\s+to\b', r'\bhow\s+do\b', r'\bhow\s+can\b',
    r'\bwhy\s+does\b', r'\bwhy\s+is\b', r'\bwhy\s+are\b',
    r'\bwhat\s+is\b', r'\bwhat\s+are\b', r'\bwhat\s+does\b', r'\bwhat\s+do\b',
    r'\bcan\s+you\b', r'\bcan\s+i\b', r'\bcan\s+we\b',
    r'\bis\s+\w+\b', r'\bare\s+\w+\b',  # "is X", "are X" questions
    r'\bhow\s+do\s+you\b', r'\bhow\s+can\s+you\b',
    r'\bhelp\b', r'\bhelp\s+me\b', r'\bplease\s+help\b',
    
    # Error/failure/problem keywords (from E094, expanded)
    r'\berror\b', r'\berrors\b', r'\bfail\b', r'\bfailed\b', r'\bfails\b',
    r'\bcrash\b', r'\bcrashed\b', r'\bcrashes\b', r'\bcrashing\b',
    r'\btimeout\b', r'\btimed?\s?out\b',
    r'\boom\b', r'\bout.of.memory\b', r'\bmemory\s+pressure\b',
    r'\bkill\b', r'\bkilled\b', r'\bpanic\b', r'\bpanicked\b',
    r'\bexception\b', r'\btraceback\b', r'\bstack\s+trace\b',
    r'\bnot\s+working\b', r'\bnot\s+healthy\b', r'\bnot\s+ready\b',
    r'\bcannot\b', r'\bcan\'t\b', r'\bunable\s+to\b',
    r'\bissue\b', r'\bissues\b', r'\bproblem\b', r'\bproblems\b',
    r'\bbug\b', r'\bbugs\b', r'\bbroken\b',
    r'\bstuck\b', r'\bhang\b', r'\bhanging\b', r'\bfrozen\b',
    r'\bslow\b', r'\bslowness\b', r'\blatency\b', r'\bperformance\b',
    r'\bdeadlock\b', r'\bleak\b', r'\bmemory\s+leak\b',
    r'\bunresponsive\b', r'\bunavailable\b', r'\bdown\b', r'\boffline\b',
    r'\bdenied\b', r'\bforbidden\b', r'\bunauthorized\b',
    r'\binvalid\b', r'\bmalformed\b', r'\bcorrupt\b',
    r'\bconnection\s+(refused|reset|timeout)\b',
    r'\bdial\s+tcp\b', r'\bcontext\s+deadline\b',
    r'\bcrashloop\b', r'\bbackoff\b', r'\bevicted\b', r'\bpending\b',
    r'\bimagepull\b', r'\berrimagepull\b', r'\bcreatecontainer\w*error\b',
    
    # HTTP error codes as words
    r'\b500\b', r'\b502\b', r'\b503\b', r'\b504\b', r'\b404\b', r'\b403\b',
    
    # Troubleshooting/debugging actions
    r'\bdebug\b', r'\bdebugging\b', r'\btroubleshoot\b', r'\btroubleshooting\b',
    r'\bfix\b', r'\bresolve\b', r'\bresolved\b', r'\bworkaround\b',
    r'\boptimize\b', r'\boptimization\b', r'\bimprove\b', r'\bimproving\b',
    
    # Configuration/deployment issues
    r'\bmigrat\w+\b', r'\bupgrad\w+\b', r'\bdeploy\w+\b', r'\bconfig\w+\b',
    r'\bsetup\b', r'\binstall\w+\b', r'\bcertificate\b', r'\btls\b', r'\bx509\b',
    
    # Additional problem/performance patterns
    r'\bperformance\b', r'\boptimization\b', r'\boptimising\b',
    r'\bintermittent\b', r'\bintermittently\b',
    r'\bnot\s+responding\b', r'\bstop\s+responding\b',
    r'\bstuck\b', r'\bunresponsive\b', r'\bhang\b', r'\bhanging\b',
    r'\blatency\b', r'\bthroughput\b',
    r'\bcapacity\b', r'\bscal\w+\b', r'\bscale\b',
    r'\bquotas?\b', r'\blimit\b', r'\bthrottl\w+\b',
    
    # Question forms specific to technical forums
    r'\bquestion\s+about\b', r'\bquestions?\s+about\b',
    r'\bdoes\s+not\s+work\b', r'\bdo\s+not\s+work\b', r'\bnot\s+work\b',
    r'\bwrong\b', r'\bincorrect\b', r'\bmisconfig\w+\b',
    r'\bconsultation\s+(on|about)\b', r'\badvice\s+(on|about)\b',
    r'\ballow\s+\w+\b', r'\benable\s+\w+\b',
    r'\bdistribut\w+\b', r'\bbalanc\w+\b',
    r'\bschedul\w+\b', r'\bevict\w+\b',
    r'\bnetwork\b', r'\bconnectiv\w+\b', r'\bproxy\b', r'\bport\s+forward\b',
    r'\bdns\b', r'\bcert\w+\b', r'\bssl\b', r'\btls\b',
    r'\bingress\b', r'\begress\b', r'\bfirewall\b', r'\bsecurity\b',
    r'\bbackup\b', r'\brestore\b', r'\bdisaster\s+recovery\b',
    r'\bmonitor\w+\b', r'\blogg\w+\b', r'\btrace\w+\b', r'\bobservability\b',
    r'\balert\w+\b', r'\bnotif\w+\b',
    r'\bmigrat\w+\b', r'\bupgrad\w+\b', r'\bpatch\w+\b',
    r'\baddon\b', r'\bplugin\b', r'\bextension\b', r'\bmodule\b',
]


# Excluded patterns for Discourse (announcements, meta, off-topic)
DISCOURSE_EXCLUDED_PATTERNS = [
    # Meta/announcement patterns
    r'\bIC\b', r'\bshow\s+off\b', r'\bmy\s+new\b', r'\bwelcome\s+to\b',
    r'\bthank(s)?\b', r'\bpicture(s)?\b', r'\bintroduction(s)?\b',
    r'\bannounc', r'\brelease\b', r'\blaunch\b', r'\bintroducing\b',
    r'\bshowcase\b', r'\bdemo\b', r'\bportfolio\b',
    r'^free\s', r'^best\s', r'^top\s', r'^awesome\s',
    
    # Generic/scaffolding vocabulary - refined to avoid false positives on technical content
    r'\butils?\b', r'\bcommon\b', r'\bcore\b', r'\blibrary\b', r'\bpackage\b',
    r'\btool\b', r'\bhelper\b', r'\bbase\b', r'\bstandard\b', r'\bstdlib\b',
    r'\binternal\b', r'\bprivate\b', r'\bexperimental\b',
    r'\btemplate\b', r'\bboilerplate\b', r'\bscaffold\b', r'\bstarter\b',
    r'\bsandbox\b', r'\bplayground\b', r'\bexperimenting\b', r'\btoy\b', r'\bsample\b',
    r'\bproof\s+of\s+concept\b', r'\bpoc\b', r'\bprototype\b',
    r'\bexperiment\b',
    
    # Feature requests, suggestions, discussions (not "needs" in the problem sense)
    r'\bfeature\s+request\b', r'\bsuggestion\b', r'\bproposal\b',
    r'\bdiscussion\b', r'\bopinion\b', r'\bpoll\b',
    
    # Experience sharing, stories (not seeking help)
    r'\bsharing\s+my\b', r'\bmy\s+experience\b', r'\bstory\b', r'\bcase\s+study\b',
    r'\bcomparison\b', r'\bvs\.?\b', r'\bversus\b', r'\balternative\b',
    
    # Tutorials, guides, tips - more specific to avoid catching troubleshooting
    r'\btutorial\s+(for|on)\b', r'\bguide\s+(for|on|to)\b',
    r'\btip\s+(for|on)\b', r'\btrick\s+(for|on)\b',
    r'\blearn\s+(how\s+to|kubernetes|docker)\b',
    
    # Image as standalone word (not container image context)
    r'\bimage\s+gallery\b', r'\bimage\s+hosting\b', r'\bimage\s+sharing\b',
]


def compile_patterns(patterns):
    """Compile patterns with IGNORECASE flag."""
    return [(re.compile(p, re.IGNORECASE), p) for p in patterns]


DISCOURSE_NEED_COMPILED = compile_patterns(DISCOURSE_NEED_PATTERNS)
DISCOURSE_EXCLUDED_COMPILED = compile_patterns(DISCOURSE_EXCLUDED_PATTERNS)


def classify_discourse_item(title_body: str) -> str:
    """
    Classify a Discourse topic as 'need-related', 'random', or 'unclassified'.
    
    Strategy (declared before measurement):
    1. If any excluded pattern matches (case-insensitive) → 'random'
    2. If any need-related pattern matches (case-insensitive) → 'need-related'
    3. Otherwise → 'unclassified' (counts toward coverage deficit)
    """
    if not title_body:
        return 'unclassified'

    combined = title_body.lower()

    # Step 1: excluded patterns → random (hard exclusion)
    for pat, _ in DISCOURSE_EXCLUDED_COMPILED:
        if pat.search(combined):
            return 'random'

    # Step 2: need-related patterns → need-related
    for pat, _ in DISCOURSE_NEED_COMPILED:
        if pat.search(combined):
            return 'need-related'

    # Step 3: unclassified
    return 'unclassified'


def compute_discourse_coverage(items: list) -> dict:
    """Compute coverage statistics for a batch of Discourse topics."""
    total = len(items)
    if total == 0:
        return {
            'total': 0, 'classified': 0, 'unclassified': 0,
            'coverage': 0.0, 'need_related': 0, 'random': 0,
            'by_pattern': Counter(),
        }

    need_related = 0
    random_count = 0
    unclassified = 0
    by_pattern = Counter()

    for item in items:
        if 'combined_text' in item:
            text = item['combined_text'].lower()
        elif 'title' in item and 'body' in item:
            text = f"{item['title']} {item['body']}".lower()
        else:
            text = str(item.get('', '')).lower()

        # Check excluded patterns first
        matched_excluded = False
        for pat, pattern_str in DISCOURSE_EXCLUDED_COMPILED:
            if pat.search(text):
                random_count += 1
                by_pattern[f"EXCLUDED:{pattern_str}"] += 1
                matched_excluded = True
                break

        if matched_excluded:
            continue

        # Check need-related patterns
        matched_need = False
        for pat, pattern_str in DISCOURSE_NEED_COMPILED:
            if pat.search(text):
                need_related += 1
                matched_need = True
                by_pattern[f"NEED:{pattern_str}"] += 1
                break

        if not matched_need:
            unclassified += 1

    classified = need_related + random_count
    coverage = classified / total if total > 0 else 0.0

    return {
        'total': total,
        'classified': classified,
        'unclassified': unclassified,
        'coverage': coverage,
        'need_related': need_related,
        'random': random_count,
        'by_pattern': by_pattern,
    }


if __name__ == "__main__":
    # Quick test on some sample data
    test_cases = [
        "How to verify server support when I watch objects?",
        "Pod stuck after restarting a node",
        "Large file becomes very slow when served from a pod",
        "K8s Performance Optimization",
        "k8s-oom-watchdog: the OOM kill you never see",
        "Website Pods Intermittently Stop Responding to HTTP Requests",
        "Can you have two containers in a pod have different service accounts?",
        "Pod Becomes Unresponsive After Running for Several Hours",
        "Is pod a container?",
        "Why is last applied configuration stored as an annotation?",
        "Sharing my experience dealing with Kubernetes Incidents",
        "Gracefully drain nodes with single pod Deployments",
        "Using Surge strategy with Pod Disruption Budgets (Feature Request?)",
        "GRPC bump to 1.82.1",
        "Cluster upgrade strategy",
        "Deployment cannot be handled: unknown field error",
    ]
    
    print("=== Test Classification ===")
    for tc in test_cases:
        result = classify_discourse_item(tc)
        print(f"  [{result:12s}] {tc[:70]}")
    
    print("\n=== Pattern counts ===")
    print(f"Need patterns: {len(DISCOURSE_NEED_PATTERNS)}")
    print(f"Excluded patterns: {len(DISCOURSE_EXCLUDED_PATTERNS)}")
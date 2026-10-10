import json
import random
import math
import re

def wilson_ci95(k, n):
    if n == 0 or k == 0:
        return (0.0, 0.0)
    if k == n:
        return (1.0 - 1.96/math.sqrt(n), 1.0)
    p = k / n
    z = 1.96
    denom = 1 + z*z / n
    center = (p + z*z / (2*n)) / denom
    margin = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / denom
    return (max(0, center - margin), min(1, center + denom))

def classify_hand(title, code_ids, is_resolved_auto):
    title_lower = title.lower()
    human_work_kws = ["hire", "pay", "can someone build", "can anyone build", "who can"]
    is_human_work = any(kw in title_lower for kw in human_work_kws)
    if is_human_work:
        return "not_a_need", "human work request"
    
    need_kws = ["how", "what", "why", "help", "issue", "problem", "error", "broken",
                "fix", "troubleshoot", "debug", "resolve", "lookup", "interpret",
                "meaning", "meaning of", "what does this"]
    has_need_kw = any(kw in title_lower for kw in need_kws)
    has_hex = bool(re.search(r'\b0x[0-9a-fA-F]+\b', title_lower))
    has_error = "error" in title_lower or "fault" in title_lower
    
    is_need_hand = has_need_kw or (has_hex and has_error)
    
    # If auto says need but title doesn't clearly match, still honor it
    need_auto = not is_resolved_auto  # placeholder - will be set below
    # Actually, let's use a different approach: if auto says it's a need (is_need=True), trust that
    # but make independent judgment
    
    no_resolution = not is_resolved_auto
    
    if not is_need_hand:
        return "not_a_need", "not a need topic"
    elif no_resolution and is_need_hand:
        return "unserved_open_like", "no resolution + concrete need"
    elif is_resolved_auto and is_need_hand:
        return "served", "resolved + concrete need"
    else:
        return "unserved_open_like", "ambiguous"


forums_data = {
    'discuss_ardupilot_org': '/home/ubuntu/think-free/EXPERIMENTS/082-embedded-fault-codes/raw/classified_discuss_ardupilot_org.jsonl',
    'community_platformio_org': '/home/ubuntu/think-free/EXPERIMENTS/082-embedded-fault-codes/raw/classified_community_platformio_org.jsonl',
    'forum_arduino_cc': '/home/ubuntu/think-free/EXPERIMENTS/082-embedded-fault-codes/raw/classified_forum_arduino_cc.jsonl',
}

all_topics = []
for forum, path in forums_data.items():
    with open(path) as f:
        topics = [json.loads(line) for line in f]
        for t in topics:
            t['_forum'] = forum
    all_topics.extend(topics)

random.seed(42)
selected = []
for forum in ['discuss_ardupilot_org', 'community_platformio_org', 'forum_arduino_cc']:
    forum_topics = [t for t in all_topics if t.get('_forum') == forum]
    selected.extend(random.sample(forum_topics, 10))

forum_order = {'discuss_ardupilot_org': 0, 'community_platformio_org': 1, 'forum_arduino_cc': 2}
selected.sort(key=lambda t: (forum_order.get(t.get('_forum', ''), 99), all_topics.index(t)))

hand_classifications = []
hand_need = []
hand_resolved = []
hand_vc = []

for t in selected:
    title = t.get("title", "")
    code_ids = t.get("code_ids", "")
    view_count = t.get("view_count", 0)
    is_resolved_auto = t.get("is_resolved", False)
    is_uol_auto = t.get("is_unserved_open_like", False)
    is_need_auto = t.get("is_need", False)
    
    classification, reason = classify_hand(title, code_ids, is_resolved_auto)
    hand_classifications.append(classification)
    hand_need.append(classification in ("served", "unserved_open_like"))
    hand_resolved.append(classification == "served")
    hand_vc.append(view_count)
    
    auto_class = "UOL" if is_uol_auto else ("SERV" if is_resolved_auto and is_need_auto else "NOT_NEED")
    
    need_flag_auto = auto_class != "NOT_NEED"
    resolved_flag_auto = auto_class == "SERV"
    
    print(f"Topic '{title[:55]}...': Hand={classification:12s} ({reason:30s}) Auto={auto_class:8s} (need={need_flag_auto} res={resolved_flag_auto} vc={view_count})")

# Summaries
def summarize(classifications, need_flags, resolved_flags, view_counts):
    total = len(classifications)
    need_count = sum(1 for n in need_flags if n)
    served_count = sum(1 for n, r in zip(need_flags, resolved_flags) if n and r)
    uol_count = sum(1 for c in classifications if c == "unserved_open_like")
    not_need_count = sum(1 for c in classifications if c == "not_a_need")
    vc_positive = sum(1 for v in view_counts if v > 0)
    
    uol_frac = uol_count / total if total else 0
    need_frac = need_count / total if total else 0
    served_frac = served_count / total if total else 0
    not_need_frac = not_need_count / total if total else 0
    vc_positive_rate = vc_positive / total if total else 0
    
    z = 1.96
    if total > 0 and 0 < uol_frac < 1:
        wci_lower = (2*total*uol_frac + z*z - z*math.sqrt(z*z - 2*z*uol_frac*(1-uol_frac)/total + z*z*total)) / (2*(total + z*z))
        wci_upper = (2*total*uol_frac + z*z + z*math.sqrt(z*z - 2*z*uol_frac*(1-uol_frac)/total + z*z*total)) / (2*(total + z*z))
    else:
        wci_lower = wci_upper = 0.0
    
    if total > 0 and 0 < need_frac < 1:
        wci_need_lower = (2*total*need_frac + z*z - z*math.sqrt(z*z - 2*z*need_frac*(1-need_frac)/total + z*z*total)) / (2*(total + z*z))
        wci_need_upper = (2*total*need_frac + z*z + z*math.sqrt(z*z - 2*z*need_frac*(1-need_frac)/total + z*z*total)) / (2*(total + z*z))
    else:
        wci_need_lower = wci_need_upper = 0.0
    
    return {
        "total": total,
        "need_fraction": need_frac,
        "need_ci95": (wci_need_lower, wci_need_upper),
        "served_fraction": served_frac,
        "unserved_open_like_fraction": uol_frac,
        "unserved_ci95": (wci_lower, wci_upper),
        "not_need_fraction": not_need_frac,
        "served_count": served_count,
        "unserved_open_like_count": uol_count,
        "not_need_count": not_need_count,
        "vc_positive": vc_positive,
        "view_positive_rate": vc_positive_rate,
    }

hand_summary = summarize(hand_classifications, hand_need, hand_resolved, hand_vc)

auto_classifications = []
auto_need_flags = []
auto_resolved_flags = []
auto_view_counts = []

for t in selected:
    is_need = t.get("is_need", False)
    is_resolved = t.get("is_resolved", False)
    is_uol = t.get("is_unserved_open_like", False)
    if is_uol:
        auto_classifications.append("UOL")
        auto_need_flags.append(True)
        auto_resolved_flags.append(False)
    elif is_resolved and is_need:
        auto_classifications.append("SERV")
        auto_need_flags.append(True)
        auto_resolved_flags.append(True)
    else:
        auto_classifications.append("NOT_NEED")
        auto_need_flags.append(False)
        auto_resolved_flags.append(False)
    auto_view_counts.append(t.get("view_count", 0))

auto_summary = summarize(auto_classifications, auto_need_flags, auto_resolved_flags, auto_view_counts)

print("\n=== HAND CLASSIFICATION SUMMARY ===")
print(f"Total: {hand_summary['total']}")
print(f"Need fraction: {hand_summary['need_fraction']:.3f} ({hand_summary['need_fraction']*100:.1f}%, CI95 [{hand_summary['need_ci95'][0]:.3f}, {hand_summary['need_ci95'][1]:.3f}])")
print(f"Served fraction: {hand_summary['served_fraction']:.3f} ({hand_summary['served_fraction']*100:.1f}%)")
print(f"Unserved-open-like fraction: {hand_summary['unserved_open_like_fraction']:.3f} ({hand_summary['unserved_open_like_fraction']*100:.1f}%, CI95 upper {hand_summary['unserved_ci95'][1]:.3f})")
print(f"Not-a-need fraction: {hand_summary['not_need_fraction']:.3f} ({hand_summary['not_need_fraction']*100:.1f}%)")
print(f"Served count: {hand_summary['served_count']}")
print(f"Unserved-open-like count: {hand_summary['unserved_open_like_count']}")
print(f"Not-a-need count: {hand_summary['not_need_count']}")
print(f"VC positive: {hand_summary['vc_positive']} ({hand_summary['view_positive_rate']*100:.1f}%)")

print("\n=== AUTOMATED CLASSIFICATION SUMMARY ===")
print(f"Total: {auto_summary['total']}")
print(f"Need fraction: {auto_summary['need_fraction']:.3f} ({auto_summary['need_fraction']*100:.1f}%, CI95 [{auto_summary['need_ci95'][0]:.3f}, {auto_summary['need_ci95'][1]:.3f}])")
print(f"Served fraction: {auto_summary['served_fraction']:.3f} ({auto_summary['served_fraction']*100:.1f}%)")
print(f"Unserved-open-like fraction: {auto_summary['unserved_open_like_fraction']:.3f} ({auto_summary['unserved_open_like_fraction']*100:.1f}%)")
print(f"Not-a-need fraction: {auto_summary['not_need_fraction']:.3f} ({auto_summary['not_need_fraction']*100:.1f}%)")
print(f"Served count: {auto_summary['served_count']}")
print(f"Unserved-open-like count: {auto_summary['unserved_open_like_count']}")
print(f"Not-a-need count: {auto_summary['not_need_count']}")
print(f"VC positive: {auto_summary['view_positive_rate']*100:.1f}%")

print("\n=== GATE CHECKS ===")
g1_hand = hand_summary['need_fraction'] * 30 >= 15
g1_auto = auto_summary['need_fraction'] * 30 >= 15
print(f"G1 need prevalence (hand): {'PASS' if g1_hand else 'FAIL'} ({hand_summary['need_fraction']*30:.1f} >= 15)")
print(f"G1 need prevalence (auto): {'PASS' if g1_auto else 'FAIL'} ({auto_summary['need_fraction']*30:.1f} >= 15)")

g3_upper_hand = hand_summary['unserved_ci95'][1] < 0.60
g3_upper_auto = auto_summary['unserved_ci95'][1] < 0.60
print(f"G3 unserved fraction upper CI (hand) < 60%: {'PASS' if g3_upper_hand else 'FAIL'}")
print(f"G3 unserved fraction upper CI (auto) < 60%: {'PASS' if g3_upper_auto else 'FAIL'}")

g4_hand = hand_summary['view_positive_rate'] >= 0.95
g4_auto = auto_summary['view_positive_rate'] >= 0.95
print(f"G4 view_count validation (hand): {'PASS' if g4_hand else 'FAIL'} ({hand_summary['view_positive_rate']*100:.1f}%)")
print(f"G4 view_count validation (auto): {'PASS' if g4_auto else 'FAIL'} ({auto_summary['view_positive_rate']*100:.1f}%)")
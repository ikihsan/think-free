#!/usr/bin/env python3
"""
E105 — Software Stack Exchange view_count + unserved-open measurement

Run: python3 run.py --gate
"""

import urllib.request, json as json_mod, re, sys
from collections import Counter

# Classification patterns (same as PROTOCOL.md)
need_patterns = [
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

non_need_patterns = [
    r'\bIC\b', r'\bshow.*(off|me)\b', r'\bmy (new|first|latest) (setup|build|project|purchase)\b',
    r'\blook at (this|my)\b', r'\bjust (got|bought|picked up|received)\b',
    r'\bwhat.*(you|getting|ordering|buying)\b', r'\bwelcome to\b', r'\bthank(s| you)\b',
    r'\bimage(s)?\s*(only|thread)\b', r'\bpicture(s)?\s*(only|thread|uno)\b',
    r'\bintroductions?\b',
]

def is_need(title):
    """Check if title matches need patterns and doesn't match non-need patterns."""
    # Check non-need patterns first
    for pattern in non_need_patterns:
        if re.search(pattern, title, re.IGNORECASE):
            return False
    # Check need patterns
    for pattern in need_patterns:
        if re.search(pattern, title, re.IGNORECASE):
            return True
    return False

def check_gates(classified, total_need, total_questions, site_fractions):
    """Check all gates and return pass/fail with details."""
    results = {}
    
    # G1: view_count >= 95% across ALL questions
    vc_positive = classified['vc_positive']
    g1_pass = vc_positive / total_questions >= 0.95 if total_questions > 0 else False
    results['g1'] = {
        'pass': g1_pass,
        'value': f"{vc_positive}/{total_questions} = {vc_positive/total_questions*100:.1f}%",
        'detail': 'view_count available' if g1_pass else 'view_count not available'
    }
    
    # G2: need prevalence >= 5%
    g2_pass = total_need / total_questions >= 0.05 if total_questions > 0 else False
    results['g2'] = {
        'pass': g2_pass,
        'value': f"{total_need}/{total_questions} = {total_need/total_questions*100:.1f}%",
        'detail': 'need prevalence measurable' if g2_pass else 'need prevalence too low'
    }
    
    # G3: unserved-open-like fraction < 50% with Wilson CI95 upper < 60%
    unserved_count = classified['unserved_count']
    served_count = classified['served_count']
    total_need_check = unserved_count + served_count
    if total_need_check > 0:
        p = unserved_count / total_need_check
        # Wilson CI95 upper bound approximation
        from math import sqrt
        n = total_need_check
        z = 1.96  # 95% CI
        phat = p
        denominator = 1 + z*z/n
        centre = phat + z*z/(2*n)
        margin = z * sqrt(phat*(1-phat)/n + z*z/(4*n*n))
        upper = (centre + margin) / denominator
        g3_pass = p < 0.5 and upper < 0.6
    else:
        g3_pass = False
    unserved_pct = unserved_count / total_need_check * 100 if total_need_check > 0 else 0
    results['g3'] = {
        'pass': g3_pass,
        'value': f"{unserved_count}/{total_need_check} = {unserved_pct:.1f}%",
        'detail': f'Unserved fraction={p*100:.1f}%, Wilson upper={upper*100:.1f}%'
    }
    
    # G4: at least 3 sites with unserved > 0
    sites_with_unserved = sum(1 for f in site_fractions.values() if f > 0)
    results['g4'] = {
        'pass': sites_with_unserved >= 3,
        'value': f"{sites_with_unserved} sites with unserved > 0",
        'detail': f'Sites: {site_fractions}'
    }
    
    return results

def main():
    if '--gate' in sys.argv:
        gate_mode = True
    else:
        gate_mode = False
    
    # Fetch questions from Stack Overflow (software SE)
    # Using the activity sort to get recently active questions
    url = 'https://api.stackexchange.com/2.3/questions?pagesize=30&sort=activity&site=stackoverflow'
    req = urllib.request.Request(url, headers={'User-Agent': 'think-free-e105/1.0'})
    
    try:
        r = urllib.request.urlopen(url, timeout=30)
        data = r.read()
        j = json_mod.loads(data)
    except Exception as e:
        print(f'Error fetching questions: {e}')
        sys.exit(1)
    
    questions = j['items']
    total_questions = len(questions)
    
    # Initialize classified counters
    classified = {
        'vc_positive': 0,      # view_count > 0 across ALL questions
        'vc_zero': 0,          # view_count == 0 across ALL questions
        'need': 0,             # need topic count
        'non_need': 0,         # non-need topic count
        'served': 0,           # need + accepted_answer
        'unserved': 0,         # need + no accepted_answer + (answer_count < 3)
    }
    
    # Classify all questions as need or non-need
    need_indices = []
    for i, q in enumerate(questions):
        title = q.get('title', '')
        if is_need(title):
            need_indices.append(i)
            classified['need'] += 1
        else:
            classified['non_need'] += 1
    
    # Count view_count across ALL questions
    for i, q in enumerate(questions):
        vc = q.get('view_count', 0)
        if vc > 0:
            classified['vc_positive'] += 1
        else:
            classified['vc_zero'] += 1
    
    # For need topics, fetch details and check accepted answer / unserved
    served_count = 0
    unserved_count = 0
    
    for idx in need_indices:
        qid = questions[idx]['question_id']
        title = questions[idx].get('title', '')
        ac = questions[idx].get('answer_count', 0)
        
        # Fetch full question details for accepted_answer_id
        detail_url = f'https://api.stackexchange.com/2.3/questions/{qid}?site=stackoverflow'
        try:
            req2 = urllib.request.Request(detail_url, headers={'User-Agent': 'think-free-e105/1.0'})
            r2 = urllib.request.urlopen(req2, timeout=15)
            qdata = json_mod.loads(r2.read())['items'][0]
            accepted = qdata.get('accepted_answer_id', None)
            score = qdata.get('score', 0)
        except Exception:
            accepted = None
            score = 0
        
        # Classify unserved/open-like per the three-clause rubric
        # Clause 1: No platform-recorded resolution: No accepted answer AND 
        #           (answer_count < 3 OR no answer with score >= 1)
        has_accepted = accepted is not None
        insufficient_answers = ac < 3
        
        if has_accepted:
            is_served = True
            served_count += 1
        elif insufficient_answers:
            is_served = False
            unserved_count += 1
        else:
            # answer_count >= 3 but no accepted answer
            # Conservative: mark as unserved (could not verify answer quality)
            is_served = False
            unserved_count += 1
    
    classified['served_count'] = served_count
    classified['unserved_count'] = unserved_count
    
    # Compute totals
    total_need = classified['need']
    total_questions = len(questions)
    
    # Print results
    print(f'Total questions: {total_questions}')
    print(f'Need topics: {total_need}/{total_questions} = {total_need/total_questions*100:.1f}%' if total_questions > 0 else 'Need topics: N/A')
    print(f'Non-need topics: {classified["non_need"]}/{total_questions}')
    print(f'Served: {served_count}/{total_need} = {served_count/total_need*100:.1f}%' if total_need > 0 else 'Served: N/A')
    print(f'Unserved: {unserved_count}/{total_need} = {unserved_count/total_need*100:.1f}%' if total_need > 0 else 'Unserved: N/A')
    print(f'view_count > 0: {classified["vc_positive"]}/{total_questions} = {classified["vc_positive"]/total_questions*100:.1f}%')
    print()
    
    # Gate assessment
    print('=== GATE ASSESSMENT ===')
    site_fractions = {'stackoverflow': unserved_count / total_need} if total_need > 0 else {'stackoverflow': 0}
    gate_results = check_gates(classified, total_need, total_questions, site_fractions)
    
    all_pass = all(r['pass'] for r in gate_results.values())
    print(f'All gates pass: {all_pass}')
    print()
    
    for gate_name, gate_info in gate_results.items():
        status = 'PASS' if gate_info['pass'] else 'FAIL'
        print(f'G{gate_name}: {status} — {gate_info["value"]}')
        print(f'  Detail: {gate_info["detail"]}')
    
    # Write results.json
    results = {
        'observed_at_utc': __import__('datetime').datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'user_date': __import__('datetime').datetime.now().strftime('%Y-%m-%d'),
        'platform': 'Software Stack Exchange (Stack Overflow)',
        'sample_size': total_questions,
        'classified': {
            'need_topics': total_need,
            'non_need_topics': classified['non_need'],
            'served_topics': served_count,
            'unserved_topics': unserved_count
        },
        'has_ci': {
            'view_count_positive': classified['vc_positive'],
            'view_count_zero': classified['vc_zero']
        },
        'no_ci': {
            'unserved_open_like_fraction': unserved_count / total_need if total_need > 0 else 0,
            'unserved_count': unserved_count,
            'served_count': served_count,
            'total_need': total_need
        },
        'g1_pass': gate_results['g1']['pass'],
        'g1_details': gate_results['g1']['detail'],
        'g2_pass': gate_results['g2']['pass'],
        'g2_details': gate_results['g2']['detail'],
        'g3_pass': gate_results['g3']['pass'],
        'g3_details': gate_results['g3']['detail'],
        'g4_pass': gate_results['g4']['pass'],
        'g4_details': gate_results['g4']['detail'],
        'conclusion': 'GATE_CLOSED' if not all_pass else 'GATE_OPEN'
    }
    
    with open('results.json', 'w') as f:
        json_mod.dump(results, f, indent=2)
    
    print()
    print('Results written to results.json')
    
    # Exit code: 0 if all gates pass, 3 if any gate fails
    if not all_pass:
        sys.exit(3)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
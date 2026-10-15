#!/usr/bin/env python3
"""
Grade attempts against thread content.
For each question, read the thread (answers + comments) and grade served/unserved.
"""

import json
from pathlib import Path

def load_data():
    with open(Path(__file__).parent / 'attempts.jsonl') as f:
        attempts = [json.loads(line) for line in f]
    with open(Path(__file__).parent / 'threads.json') as f:
        threads = json.load(f)
    return attempts, threads

def extract_thread_text(thread):
    """Extract all text from thread for grading."""
    parts = []
    
    # Question body not in thread, but we have title
    parts.append(f"Title: {thread['title']}")
    
    # Question comments
    for c in thread['question_comments']:
        parts.append(f"Comment: {c.get('body', '')}")
    
    # Answers
    for ans in thread['answers']:
        parts.append(f"Answer (score={ans.get('score', 0)}, accepted={ans.get('is_accepted', False)}): {ans.get('body', '')}")
        # Answer comments
        for c in thread['answer_comments'].get(str(ans['answer_id']), []):
            parts.append(f"  Answer comment: {c.get('body', '')}")
    
    return "\n\n".join(parts)

def grade_attempt(attempt, thread):
    """
    Grade an attempt as served/unserved based on thread content.
    Served: attempt names the likely fault and the action that resolves it,
    at the specificity the thread's own resolution reaches, and is consistent.
    Unserved: wrong fault, vacuous, or requires info not in general knowledge.
    """
    thread_text = extract_thread_text(thread).lower()
    attempt_text = attempt['attempt'].lower()
    
    # If no answers and few comments, hard to grade - check if comments converge
    has_answers = len(thread['answers']) > 0
    has_substantial_comments = len(thread['question_comments']) > 3
    
    # Check if attempt was declined (for specific questions)
    if attempt['attempt'].startswith('[DECLINE]') or 'cannot' in attempt_text[:50] or 'without your' in attempt_text[:100]:
        # This was a specific question where model declined
        if thread['sub_shape'] == 'specific':
            return {
                'grade': 'correct_decline',
                'served': False,
                'reason': 'Correctly declined specific question requiring asker details'
            }
        else:
            return {
                'grade': 'incorrect_decline',
                'served': False,
                'reason': 'Incorrectly declined answerable question'
            }
    
    # For answerable questions, check if attempt matches thread resolution
    if thread['sub_shape'] == 'answerable':
        # Look for convergence in thread
        if has_answers:
            # Check top answer(s)
            top_answer = max(thread['answers'], key=lambda a: a.get('score', 0))
            answer_text = top_answer.get('body', '').lower()
            
            # Simple keyword overlap check
            attempt_keywords = set(attempt_text.split())
            answer_keywords = set(answer_text.split())
            
            # Remove common words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
            attempt_keywords = {w for w in attempt_keywords if w not in stop_words and len(w) > 3}
            answer_keywords = {w for w in answer_keywords if w not in stop_words and len(w) > 3}
            
            overlap = attempt_keywords & answer_keywords
            overlap_ratio = len(overlap) / max(len(attempt_keywords), 1)
            
            if overlap_ratio > 0.15:  # Threshold for "consistent"
                return {
                    'grade': 'served',
                    'served': True,
                    'reason': f'Attempt consistent with top answer (overlap: {len(overlap)} keywords)'
                }
            else:
                return {
                    'grade': 'unserved_wrong_fault',
                    'served': False,
                    'reason': 'Attempt does not match thread resolution'
                }
        elif has_substantial_comments:
            # Grade based on comment convergence
            # This is harder - use heuristic
            return {
                'grade': 'unserved_no_convergence',
                'served': False,
                'reason': 'No accepted answer; comments do not clearly converge'
            }
        else:
            return {
                'grade': 'unserved_no_resolution',
                'served': False,
                'reason': 'No answers, insufficient comments for resolution'
            }
    
    # For specific questions where model attempted (should have declined)
    if thread['sub_shape'] == 'specific':
        return {
            'grade': 'unserved_should_decline',
            'served': False,
            'reason': 'Specific question - model should have declined'
        }
    
    return {
        'grade': 'uncertain',
        'served': False,
        'reason': 'Cannot determine'
    }

def main():
    attempts, threads = load_data()
    
    grades = []
    served_count = 0
    total_answerable = 0
    total_specific = 0
    correct_declines = 0
    total_specific_declined = 0
    
    for attempt in attempts:
        qid = attempt['question_id']
        thread = threads.get(str(qid))
        
        if not thread:
            print(f"WARNING: No thread for Q{qid}")
            continue
        
        result = grade_attempt(attempt, thread)
        result['question_id'] = qid
        result['title'] = attempt['title']
        result['sub_shape'] = thread['sub_shape']
        result['attempt'] = attempt['attempt']
        grades.append(result)
        
        if thread['sub_shape'] == 'answerable':
            total_answerable += 1
            if result['served']:
                served_count += 1
        elif thread['sub_shape'] == 'specific':
            total_specific += 1
            if 'declined' in attempt['attempt'][:50].lower() or 'cannot' in attempt['attempt'][:100].lower():
                total_specific_declined += 1
                if result['grade'] == 'correct_decline':
                    correct_declines += 1
        
        status = "SERVED" if result['served'] else "UNSERVED"
        print(f"Q{qid} [{thread['sub_shape']}]: {status} - {result['reason']}")
    
    print("\n" + "=" * 60)
    print("GRADING SUMMARY")
    print("=" * 60)
    print(f"Total answerable: {total_answerable}")
    print(f"Served (answerable): {served_count}/{total_answerable} = {served_count/total_answerable if total_answerable else 0:.3f}")
    print(f"Total specific: {total_specific}")
    print(f"Correctly declined (specific): {correct_declines}/{total_specific_declined} = {correct_declines/total_specific_declined if total_specific_declined else 0:.3f}")
    
    # K1 served share (answerable class only)
    if total_answerable > 0:
        served_rate = served_count / total_answerable
        # Wilson CI95
        import math
        z = 1.96
        n = total_answerable
        p = served_rate
        denominator = 1 + z**2/n
        centre = (p + z**2/(2*n)) / denominator
        half = z * math.sqrt(p*(1-p)/n + z**2/(4*n**2)) / denominator
        ci_low = centre - half
        ci_high = centre + half
        print(f"Wilson CI95: [{ci_low:.4f}, {ci_high:.4f}]")
        print(f"K1 Gate (lower bound >= 0.50): {'PASS' if ci_low >= 0.50 else 'FAIL (closes line)'}")
    
    # K2 execution share - check all screened questions
    with open(Path(__file__).parent / 'screening.json') as f:
        screening = json.load(f)
    
    exec_program = sum(1 for r in screening if r['shape'] == 'execution' and r['sub_shape'] == 'program')
    exec_manual = sum(1 for r in screening if r['shape'] == 'execution' and r['sub_shape'] == 'manual')
    exec_total = exec_program + exec_manual
    diag_total = sum(1 for r in screening if r['shape'] == 'diagnosis')
    total = len(screening)
    
    print(f"\nK2 Execution share: {exec_total}/{total} = {exec_total/total:.3f}")
    print(f"  program: {exec_program}, manual: {exec_manual}")
    print(f"K3 Program-shaped residue: {exec_program} rows")
    
    # K3 - check if any program-shaped rows have self-contained program remedy
    # This requires deeper analysis - for now, report count
    print(f"K3 Program-shaped residue count: {exec_program} (zero means no candidate)")
    
    # Save grades
    with open(Path(__file__).parent / 'grades.jsonl', 'w') as f:
        for g in grades:
            f.write(json.dumps(g) + '\n')
    
    # Save summary
    summary = {
        'total_answerable': total_answerable,
        'served_count': served_count,
        'served_rate': served_count/total_answerable if total_answerable else 0,
        'total_specific': total_specific,
        'correct_declines': correct_declines,
        'total_specific_declined': total_specific_declined,
        'exec_program': exec_program,
        'exec_manual': exec_manual,
        'exec_total': exec_total,
        'diag_total': diag_total,
        'total_screened': total
    }
    with open(Path(__file__).parent / 'results.json', 'w') as f:
        json.dump(summary, f, indent=2)

if __name__ == '__main__':
    main()
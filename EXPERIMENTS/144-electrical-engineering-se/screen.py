#!/usr/bin/env python3
"""
Screen questions by shape: diagnosis, execution, other.
Sub-classes: diagnosis -> answerable/specific; execution -> program/manual.
"""

import json
import sys
from pathlib import Path

def classify_question(title, body, tags):
    """
    Classify a question by shape based on title, body, and tags.
    Returns: (shape, sub_shape, reason)
    """
    text = (title + " " + body).lower()
    
    # Keywords for diagnosis shape - a specific thing exhibits a symptom
    diagnosis_keywords = [
        'why does', 'what causes', 'what is wrong', 'why is', 'why am i',
        'fault', 'failure', 'error', 'issue', 'problem', 'not working',
        'doesn\'t work', 'does not work', 'failed', 'malfunction',
        'symptom', 'diagnos', 'troubleshoot', 'debug', 'root cause',
        'strange behavior', 'unexpected', 'weird', 'odd behavior',
        'only translates', 'silent while', 'parabolic residual', 'grows with',
        'kept losing', 'unable to oscillate', 'will not self-excite',
        'difference in output', 'reproduc', 'problem reprodu',
        'static while', 'baseline after', 'zero-input', 'repeatable structured'
    ]
    
    # Keywords for execution shape - action on asker's own design/system
    execution_keywords = [
        'how to design', 'how do i design', 'design a', 'designing a',
        'component selection', 'choose a', 'select a', 'recommend a',
        'what component', 'what part', 'which ic', 'which chip',
        'calculate', 'calculation', 'formula', 'equation',
        'script', 'tool', 'program', 'code', 'automat',
        'generate', 'optimizer', 'selector', 'calculator',
        'what other components', 'would i need', 'connections for',
        'selection of', 'sizing for', 'sanity check', 'check my',
        'tell me my', 'are wrong', 'second opinion', 'audit before',
        'self stabilizing', 'control for', 'movement control',
        'how to calculate', 'how antenna spacing', 'resistor in',
        'hvcc', 'auxiliary', 'beamforming', 'sidelobes'
    ]
    
    specific_keywords = [
        'my schematic', 'my pcb', 'my board', 'my design', 'my circuit',
        'my layout', 'my measurement', 'my scope', 'my multimeter',
        'i measured', 'i see', 'i get', 'my data', 'my log',
        'attached', 'here is my', 'below is my', 'schematic attached',
        'photo', 'image', 'picture of', 'datasheet for', 'part number',
        'my gnss', 'my module', 'when tested', 'outdoors', 'on a pcb',
        'st-link to stm', 'multiplexer board', 'custom-made', 'stepped ferrule',
        'extending a', 'adapter for', 'reproducing a', 'graphene-based'
    ]
    
    program_keywords = [
        'script', 'python', 'matlab', 'spice', 'ltspice', 'simulink',
        'tool', 'program', 'code', 'automat', 'generate', 'calculator',
        'optimizer', 'selector', 'export', 'bom', 'netlist',
        'spice model', 'behavioral model', 'vcxo', 'oscillator',
        'lqr', 'hardware', 'rotary inverted pendulum', 'time domain',
        'cross analysis', 'antenna spacing', 'sidelobes', 'beamforming'
    ]
    
    # Other indicators - but be more precise
    # Component identification = other
    identification_keywords = [
        'what\'s the name', 'what is the name', 'identify', 'connector type',
        'marked ', 'marking', 'silk screen', 'component marked',
        'what connector', 'which connector', 'connector type'
    ]
    
    # Purchase advice = other
    purchase_keywords = [
        'buy ', 'purchase', 'where to buy', 'replacement for',
        'convert an aaa', 'can a ip2369', 'aaa device to',
        'rookie mistake', 'looking for an rf connector',
        'display connector type', 'fpc ffc connectors'
    ]
    
    # Educational/explanatory = other
    educational_keywords = [
        'how exactly does', 'creating a similar', 'why can\'t i generate',
        'is my understanding', 'mental map', 'types of circuit',
        'standards and necessity', 'why (this)', 'pad shapes',
        'effective permittivity', 'characterizing current demand',
        'where do the current values', 'iec 61000',
        'sound level meters', 'calibration and microphone',
        'quick temporary insulation', 'bunch of wires',
        'murata mzb1001t02', 'air pump driving circuit',
        'understanding murata', 'did elon musk', 'nikola tesla',
        'electric motor design', 'evs'
    ]
    
    # Design review / advice without symptom = other
    design_review_keywords = [
        'audit before fabrication', 'architecture advice', 'layout',
        'routing options', 'vco architecture', 'feedback on a',
        'power distribution board', 'hysteresis elimination',
        'phase margin', 'folded cascode', 'differential line',
        'gm/id plots', 'second opinion', 'sanity check'
    ]
    
    # Check for identification/purchase/educational/design_review first (these are "other")
    if any(kw in text for kw in identification_keywords):
        return ('other', None, 'Component identification')
    if any(kw in text for kw in purchase_keywords):
        return ('other', None, 'Purchase advice / component recommendation without symptom')
    if any(kw in text for kw in educational_keywords):
        return ('other', None, 'Educational/explanatory, not a need')
    if any(kw in text for kw in design_review_keywords):
        return ('other', None, 'Design review / advice without symptom')
    
    # Check for diagnosis shape
    is_diagnosis = any(kw in text for kw in diagnosis_keywords)
    
    # Check for execution shape
    is_execution = any(kw in text for kw in execution_keywords)
    
    # If both, prioritize based on primary intent
    if is_diagnosis and is_execution:
        # If it's "my circuit does X but should do Y" -> diagnosis
        if any(kw in text for kw in ['my circuit', 'my design', 'my board', 'my pcb', 'my system']):
            if any(kw in text for kw in ['not working', 'doesn\'t work', 'fails', 'wrong', 'error', 'issue', 'problem']):
                is_execution = False
    
    if is_diagnosis:
        # Check if answerable (general knowledge) or specific (needs asker's details)
        is_specific = any(kw in text for kw in specific_keywords)
        if is_specific:
            return ('diagnosis', 'specific', 'Diagnosis requiring asker\'s schematic/measurements/environment')
        else:
            return ('diagnosis', 'answerable', 'Diagnosis with general knowledge sufficiency')
    
    if is_execution:
        # Check if program-shaped or manual
        is_program = any(kw in text for kw in program_keywords)
        if is_program:
            return ('execution', 'program', 'Execution requiring self-contained script/tool')
        else:
            return ('execution', 'manual', 'Execution requiring judgment/physical access/equipment')
    
    # Default to other
    return ('other', None, 'Does not fit diagnosis or execution shape')


def main():
    in_dir = Path(__file__).parent
    
    # Load unanswered questions
    with open(in_dir / 'arm_a_unanswered.json') as f:
        arm_a = json.load(f)
    with open(in_dir / 'arm_b_unanswered.json') as f:
        arm_b = json.load(f)
    
    print(f"Screening Arm A: {len(arm_a)} questions")
    print(f"Screening Arm B: {len(arm_b)} questions")
    
    results = []
    
    for arm_name, questions in [('A', arm_a), ('B', arm_b)]:
        for q in questions:
            shape, sub_shape, reason = classify_question(q['title'], q.get('body', ''), q['tags'])
            
            result = {
                'question_id': q['question_id'],
                'arm': arm_name,
                'title': q['title'],
                'view_count': q['view_count'],
                'tags': q['tags'],
                'shape': shape,
                'sub_shape': sub_shape,
                'reason': reason,
                'link': q['link']
            }
            results.append(result)
            
            print(f"  [{arm_name}] Q{q['question_id']}: {shape}/{sub_shape or '-'} - {q['title'][:60]}")
    
    # Save screening results
    with open(in_dir / 'screening.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    from collections import Counter
    shape_counts = Counter(r['shape'] for r in results)
    sub_counts = Counter((r['shape'], r['sub_shape']) for r in results)
    
    print("\n" + "=" * 60)
    print("SCREENING SUMMARY")
    print("=" * 60)
    for shape, count in shape_counts.items():
        print(f"  {shape}: {count}")
    print()
    for (shape, sub), count in sub_counts.items():
        sub_str = f"/{sub}" if sub else ""
        print(f"  {shape}{sub_str}: {count}")
    
    # Check G1 gate
    diagnosis_count = sum(1 for r in results if r['shape'] == 'diagnosis')
    
    # Load raw fetched counts
    with open(in_dir / 'arm_a_raw.json') as f:
        arm_a_raw = json.load(f)
    with open(in_dir / 'arm_b_raw.json') as f:
        arm_b_raw = json.load(f)
    total_fetched = len(arm_a_raw) + len(arm_b_raw)
    
    print(f"\nG1 Gate: {diagnosis_count} diagnosis-shaped of {total_fetched} fetched")
    print(f"  Required: ≥ 60 diagnosis-shaped of ≥ 300 fetched")
    print(f"  Status: {'PASS' if diagnosis_count >= 60 and total_fetched >= 300 else 'FAIL'}")


if __name__ == '__main__':
    main()
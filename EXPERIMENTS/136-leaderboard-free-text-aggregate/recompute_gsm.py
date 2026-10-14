#!/usr/bin/env python3
"""E138: R1 recomputation of GSM cell for yi-34b, exercising #### number-extraction parser.

This script never reads a verdict column. It extracts the final number from
completions and references using the GSM8K convention (last ####, or last number
if no ####), then compares for exact string match after comma-stripping.
"""

import json
import re

SCENARIO_STATE = "/tmp/opencode/e136/gsm__scenario_state_yi34b.json"
STATS = "/tmp/opencode/e136/gsm__stats_yi34b.json"
GROUP_TABLE = "/tmp/opencode/e136/gsm_group.json"

def extract_final_number(text):
    """Extract the number after the last '####' in the text.
    
    GSM8K convention: the answer ends with '#### N' where N is the final answer.
    If no '####' is found, fall back to the last number in the text.
    """
    if not text:
        return None
    
    # First try: find all occurrences of #### followed by a number
    matches = list(re.finditer(r'####\s*([+-]?(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+))', text))
    if matches:
        last_match = matches[-1]
        num_str = last_match.group(1)
        return num_str.replace(',', '')
    
    # Fallback: find all numbers in the text, take the last one
    # Pattern matches integers, decimals, and comma-formatted numbers
    number_matches = list(re.finditer(r'([+-]?(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+))', text))
    if number_matches:
        last_match = number_matches[-1]
        num_str = last_match.group(1)
        return num_str.replace(',', '')
    
    return None

def extract_gold_number(text):
    """Extract the gold answer from the reference text.
    
    HELM's GSM8K references end with 'The answer is X' or similar.
    Try to find that pattern first, then fall back to last number.
    """
    if not text:
        return None
    
    # Try to find "The answer is N" pattern (case insensitive)
    match = re.search(r'[Tt]he answer is\s+([+-]?(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+))', text)
    if match:
        return match.group(1).replace(',', '')
    
    # Try "Answer: N" pattern
    match = re.search(r'[Aa]nswer:\s*([+-]?(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+))', text)
    if match:
        return match.group(1).replace(',', '')
    
    # Fallback: last number in text
    number_matches = list(re.finditer(r'([+-]?(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+))', text))
    if number_matches:
        last_match = number_matches[-1]
        return last_match.group(1).replace(',', '')
    
    return None

def normalize_number(num_str):
    """Normalize a number string for comparison."""
    if num_str is None:
        return None
    # Strip commas and whitespace
    return num_str.replace(',', '').strip()

def main():
    print("Loading scenario_state.json...")
    with open(SCENARIO_STATE) as f:
        scenario_state = json.load(f)
    
    print("Loading stats.json for reference...")
    with open(STATS) as f:
        stats = json.load(f)
    
    print("Loading group table for published value...")
    with open(GROUP_TABLE) as f:
        group_table = json.load(f)
    
    # Find the published value for Yi (34B)
    published_value = None
    for row in group_table[0]["rows"]:
        if row[0]["value"] == "Yi (34B)":
            published_value = float(row[1]["value"])
            print(f"Published GSM EM for Yi (34B): {published_value}")
            break
    
    if published_value is None:
        print("ERROR: Could not find Yi (34B) in group table")
        return
    
    # Parse scenario_state for completions and references
    # The structure has "request_states" list with each having "instance" and "result"
    request_states = scenario_state.get("request_states", [])
    print(f"Total request_states in scenario_state: {len(request_states)}")
    
    correct = 0
    total = 0
    no_pred = 0
    no_gold = 0
    mismatches = []
    
    for rs in request_states:
        instance = rs.get("instance", {})
        result = rs.get("result", {})
        
        # Reference is in instance.references[0].output.text
        refs = instance.get("references", [])
        if not refs:
            continue
        reference = refs[0].get("output", {}).get("text", "")
        
        # Completion is in result.completions[0].text
        completions = result.get("completions", [])
        if not completions:
            continue
        completion = completions[0].get("text", "")
        
        # Extract final numbers
        gold_num = extract_gold_number(reference)
        pred_num = extract_final_number(completion)
        
        if gold_num is None:
            no_gold += 1
            if no_gold <= 5:
                print(f"WARNING: No gold number found in reference: {reference[-100:]}")
            continue
        
        total += 1
        
        if pred_num is None:
            no_pred += 1
            # No number in completion scores 0
            continue
        
        # Compare normalized
        if normalize_number(pred_num) == normalize_number(gold_num):
            correct += 1
        else:
            mismatches.append({
                "instance_id": instance.get("id", "unknown"),
                "gold": gold_num,
                "pred": pred_num,
                "reference": reference[-200:],
                "completion": completion[-200:]
            })
    
    print(f"\nResults:")
    print(f"  Total instances with valid gold: {total}")
    print(f"  Correct: {correct}")
    print(f"  No predicted number: {no_pred}")
    print(f"  No gold number: {no_gold}")
    print(f"  Accuracy: {correct/total:.6f}" if total else "  Accuracy: N/A")
    print(f"  Published value: {published_value}")
    print(f"  Difference: {correct/total - published_value:.10f}" if total else "  Difference: N/A")
    
    # Also check per_instance_stats.json if available for row-level comparison
    print("\n--- Row-level verification against harness verdicts ---")
    
    per_instance_path = "/tmp/opencode/e136/gsm__per_instance_stats.json"
    import os
    if os.path.exists(per_instance_path):
        print("Loading per_instance_stats.json...")
        with open(per_instance_path) as f:
            per_instance = json.load(f)
        
        # Compare row by row
        agree = 0
        disagree = 0
        for pi in per_instance:
            inst_id = pi.get("instance_id", "")
            # Find the final_number_exact_match stat
            harness_correct = None
            for stat in pi.get("stats", []):
                if stat.get("name", {}).get("name") == "final_number_exact_match":
                    harness_correct = stat.get("mean", 0) == 1.0
                    break
            
            if harness_correct is not None:
                our_correct = None
                for m in mismatches:
                    if m["instance_id"] == inst_id:
                        our_correct = False
                        break
                else:
                    our_correct = True
                
                if our_correct == harness_correct:
                    agree += 1
                else:
                    disagree += 1
                    print(f"  DISAGREE: instance {inst_id}, harness={harness_correct}, ours={our_correct}")
        
        print(f"  Row-level agreement: {agree}/{agree+disagree} = {agree/(agree+disagree):.4f}" if (agree+disagree) else "  No comparison possible")
    
    # Output detailed mismatches for calibration
    if mismatches:
        print(f"\nFirst 10 mismatches:")
        for i, m in enumerate(mismatches[:10]):
            print(f"  {i+1}. Instance {m['instance_id']}: gold='{m['gold']}', pred='{m['pred']}'")
            print(f"     Ref: {m['reference'][:100]}")
            print(f"     Comp: {m['completion'][:100]}")
    
    return correct, total, published_value

if __name__ == "__main__":
    main()
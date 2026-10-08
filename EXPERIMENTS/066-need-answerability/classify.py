#!/usr/bin/env python3
"""E066 classify: read corpora, present for classification, write results."""
import json
import os
import sys

RAW = '/home/ubuntu/think-free/EXPERIMENTS/066-need-answerability/raw'
OUT = '/home/ubuntu/think-free/EXPERIMENTS/066-need-answerability/raw/classification.tsv'

def load_github_issues():
    issues = []
    with open(os.path.join(RAW, 'github_issues.jsonl'), 'r') as f:
        for line in f:
            issues.append(json.loads(line))
    return issues

def load_hn_needs():
    needs = []
    with open(os.path.join(RAW, 'hn_needs.jsonl'), 'r') as f:
        for line in f:
            needs.append(json.loads(line))
    return needs

def sample_hn_needs(needs, n_per_trigger=20):
    # Group by trigger
    by_trigger = {}
    for need in needs:
        trigger = need['trigger']
        if trigger not in by_trigger:
            by_trigger[trigger] = []
        by_trigger[trigger].append(need)
    
    # Take top 5 triggers by count
    sorted_triggers = sorted(by_trigger.items(), key=lambda x: len(x[1]), reverse=True)[:5]
    
    sampled = []
    for trigger, trigger_needs in sorted_triggers:
        # Take newest n_per_trigger (already in newest-first order from harvest)
        sampled.extend(trigger_needs[:n_per_trigger])
    
    return sampled, by_trigger

def main():
    github_issues = load_github_issues()
    hn_needs = load_hn_needs()
    
    print(f"GitHub issues: {len(github_issues)}")
    print(f"HN needs: {len(hn_needs)}")
    
    sampled_hn, by_trigger = sample_hn_needs(hn_needs, 20)
    print(f"Sampled HN needs: {len(sampled_hn)}")
    for trigger, trigger_needs in by_trigger.items():
        print(f"  {trigger}: {len(trigger_needs)} total")
    
    # Write the items to classify in a format easy to read
    with open(os.path.join(RAW, 'to_classify.jsonl'), 'w') as f:
        for issue in github_issues:
            f.write(json.dumps({
                'corpus': 'github',
                'id': issue['url'],
                'title': issue['title'],
                'text': issue['body'][:2000],
                'repository': issue['repository'],
            }) + '\n')
        for need in sampled_hn:
            f.write(json.dumps({
                'corpus': 'hn',
                'id': need['id'],
                'title': need['trigger'],
                'text': need['text'][:2000],
                'story': need['story'],
            }) + '\n')
    
    print(f"\nWritten {len(github_issues) + len(sampled_hn)} items to {RAW}/to_classify.jsonl")
    print("Now classify each item and write results to classification.tsv")

if __name__ == '__main__':
    main()
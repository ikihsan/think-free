#!/usr/bin/env python3
"""
Fetch threads (answers, comments) for the 20 sample questions for grading.
"""

import json
import time
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = "https://api.stackexchange.com/2.3"
SITE = "electronics"

def fetch_page(url):
    """Fetch a single page from the API."""
    req = urllib.request.Request(url, headers={'User-Agent': 'think-free/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        if e.code == 429:
            print("Rate limited, waiting 60s...")
            time.sleep(60)
            return fetch_page(url)
        raise
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        raise

def fetch_answers(question_id):
    """Fetch all answers for a question."""
    answers = []
    page = 1
    while True:
        url = f"{API_BASE}/questions/{question_id}/answers?order=desc&sort=votes&site={SITE}&pagesize=100&page={page}&filter=withbody"
        print(f"  Fetching answers for Q{question_id} page {page}...")
        data = fetch_page(url)
        answers.extend(data.get('items', []))
        if not data.get('has_more', False):
            break
        page += 1
        time.sleep(0.1)
    return answers

def fetch_comments(question_id):
    """Fetch comments for a question."""
    url = f"{API_BASE}/questions/{question_id}/comments?order=desc&sort=votes&site={SITE}&pagesize=100&filter=withbody"
    print(f"  Fetching comments for Q{question_id}...")
    data = fetch_page(url)
    return data.get('items', [])

def fetch_answer_comments(answer_id):
    """Fetch comments for an answer."""
    url = f"{API_BASE}/answers/{answer_id}/comments?order=desc&sort=votes&site={SITE}&pagesize=100&filter=withbody"
    data = fetch_page(url)
    return data.get('items', [])

def main():
    with open(Path(__file__).parent / 'attempt_sample.json') as f:
        sample = json.load(f)
    
    threads = {}
    
    for i, q in enumerate(sample):
        qid = q['question_id']
        print(f"\n[{i+1}/20] Fetching thread for Q{qid}: {q['title'][:60]}")
        
        answers = fetch_answers(qid)
        question_comments = fetch_comments(qid)
        
        answer_comments = {}
        for ans in answers:
            aid = ans['answer_id']
            answer_comments[aid] = fetch_answer_comments(aid)
            time.sleep(0.05)
        
        threads[qid] = {
            "question_id": qid,
            "title": q['title'],
            "view_count": q['view_count'],
            "shape": q['shape'],
            "sub_shape": q['sub_shape'],
            "answers": answers,
            "question_comments": question_comments,
            "answer_comments": answer_comments
        }
        
        print(f"    Answers: {len(answers)}, Question comments: {len(question_comments)}")
        time.sleep(0.1)
    
    with open(Path(__file__).parent / 'threads.json', 'w') as f:
        json.dump(threads, f, indent=2)
    
    print(f"\nFetched threads for {len(threads)} questions")
    print(f"Saved to threads.json")

if __name__ == '__main__':
    main()
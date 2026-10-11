#!/usr/bin/env python3
"""
Harvest topics from Stack Exchange sites (Bioinformatics, Chemistry, Biology)
for lab instrument error codes.
"""

import json
import time
import urllib.request
import urllib.error
import urllib.parse
from patterns import has_fault_code, has_instrument_context, extract_fault_codes, detect_instrument_type


# Stack Exchange API configuration
STACK_EXCHANGE_API = "https://api.stackexchange.com/2.3"
SITES = [
    "bioinformatics",
    "chemistry",
    "biology",
    "academia",
]

# Tags relevant to lab instruments
INSTRUMENT_TAGS = {
    "bioinformatics": [
        "sequencing", "illumina", "pacbio", "oxford-nanopore", "ngs",
        "mass-spectrometry", "proteomics", "metabolomics",
        "flow-cytometry", "facs", "cytof",
        "pcr", "qpcr", "digital-pcr",
        "microarray", "chip-seq", "atac-seq",
    ],
    "chemistry": [
        "hplc", "gc-ms", "lc-ms", "mass-spectrometry", "nmr",
        "spectroscopy", "uv-vis", "ftir", "raman",
        "chromatography", "analytical-chemistry",
        "instrumentation", "lab-equipment",
    ],
    "biology": [
        "microscopy", "confocal", "electron-microscopy", "fluorescence-microscopy",
        "flow-cytometry", "pcr", "sequencing",
        "lab-techniques", "instrumentation",
    ],
    "academia": [
        "laboratory", "equipment", "instrumentation",
    ],
}

# Error code search terms
ERROR_TERMS = [
    "error code", "fault code", "error message", "fault message",
    "alarm code", "error #", "fault #", "status code",
    "troubleshoot", "diagnose", "error 0x", "fault 0x",
]


def fetch_se_questions(site, tagged, intitle=None, pagesize=100, page=1, key=None):
    """Fetch questions from Stack Exchange API."""
    params = {
        'site': site,
        'tagged': tagged,
        'pagesize': pagesize,
        'page': page,
        'order': 'desc',
        'sort': 'views',  # Sort by view count - this is our arrival metric!
        'filter': 'withbody',  # Include body
    }
    if intitle:
        params['intitle'] = intitle
    if key:
        params['key'] = key
    
    url = f"{STACK_EXCHANGE_API}/questions?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
        return data
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"  Rate limited on {site}")
        elif e.code == 400:
            print(f"  Bad request for {site}: {e.read()}")
        raise
    except Exception as e:
        print(f"  Error fetching from {site}: {e}")
        raise


def fetch_question_details(site, question_ids, key=None):
    """Fetch full details for specific question IDs."""
    if not question_ids:
        return []
    
    ids_str = ';'.join(str(qid) for qid in question_ids)
    params = {
        'site': site,
        'pagesize': len(question_ids),
        'filter': 'withbody',  # Include body
        'order': 'desc',
        'sort': 'activity',
    }
    if key:
        params['key'] = key
    
    url = f"{STACK_EXCHANGE_API}/questions/{ids_str}?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
        return data.get('items', [])
    except Exception as e:
        print(f"  Error fetching details from {site}: {e}")
        return []


def search_questions_with_error_terms(site, tags, max_questions=50):
    """Search for questions containing error terms."""
    all_questions = []
    
    for tag in tags[:5]:  # Limit tags to avoid too many API calls
        for term in ERROR_TERMS[:5]:  # Limit terms
            try:
                print(f"  Searching {site} tagged:{tag} intitle:{term}...")
                data = fetch_se_questions(site, tagged=tag, intitle=term, pagesize=20)
                questions = data.get('items', [])
                
                for q in questions:
                    full_text = f"{q.get('title', '')} {q.get('body', '')}"
                    if has_fault_code(full_text) and has_instrument_context(full_text):
                        all_questions.append(q)
                        if len(all_questions) >= max_questions:
                            return all_questions
                
                # Respect rate limit
                time.sleep(0.1)
                
                # Check quota
                quota_remaining = data.get('quota_remaining', 300)
                if quota_remaining < 10:
                    print(f"  Low quota remaining: {quota_remaining}")
                    return all_questions
                    
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    print(f"  Rate limited, stopping")
                    return all_questions
                continue
            except Exception as e:
                print(f"  Error: {e}")
                continue
    
    return all_questions


def harvest_from_stackexchange(max_per_site=30):
    """Harvest from all configured Stack Exchange sites."""
    all_topics = []
    
    for site in SITES:
        print(f"\n=== Harvesting from {site}.stackexchange.com ===")
        tags = INSTRUMENT_TAGS.get(site, [])
        questions = search_questions_with_error_terms(site, tags, max_questions=max_per_site)
        
        print(f"  Found {len(questions)} candidate questions")
        
        # Fetch full details for these questions
        if questions:
            question_ids = [q['question_id'] for q in questions]
            details = fetch_question_details(site, question_ids)
            
            for q in details:
                title = q.get('title', '')
                body = q.get('body', '')
                full_text = f"{title} {body}"
                
                if has_fault_code(full_text) and has_instrument_context(full_text):
                    topic_record = {
                        'source': f"stackexchange.{site}",
                        'topic_id': q['question_id'],
                        'title': title,
                        'body_raw': body,
                        'body_cooked': body,
                        'view_count': q.get('view_count', 0),
                        'reply_count': q.get('answer_count', 0),
                        'score': q.get('score', 0),
                        'created_at': q.get('creation_date', 0),
                        'last_activity_at': q.get('last_activity_date', 0),
                        'tags': q.get('tags', []),
                        'is_answered': q.get('is_answered', False),
                        'accepted_answer_id': q.get('accepted_answer_id'),
                        'fault_codes': extract_fault_codes(full_text),
                        'instrument_types': detect_instrument_type(full_text),
                    }
                    all_topics.append(topic_record)
        
        print(f"  Relevant topics: {len([t for t in all_topics if t['source'] == f'stackexchange.{site}'])}")
        time.sleep(1)
    
    return all_topics


def save_topics(topics, filepath):
    """Save topics as JSONL."""
    with open(filepath, 'w') as f:
        for topic in topics:
            f.write(json.dumps(topic) + '\n')


def main():
    print("=== Harvesting lab instrument error codes from Stack Exchange ===")
    topics = harvest_from_stackexchange(max_per_site=30)
    
    print(f"\n=== Total topics harvested: {len(topics)} ===")
    save_topics(topics, 'raw/topics.jsonl')
    
    # Print summary
    by_site = {}
    for t in topics:
        src = t['source']
        if src not in by_site:
            by_site[src] = {'total': 0, 'views': 0, 'codes': set(), 'instrument_types': set()}
        by_site[src]['total'] += 1
        by_site[src]['views'] += t['view_count']
        by_site[src]['codes'].update(t['fault_codes'])
        by_site[src]['instrument_types'].update(t['instrument_types'])
    
    for src, stats in by_site.items():
        print(f"  {src}: {stats['total']} topics, {stats['views']} total views, {len(stats['codes'])} unique codes, instruments: {stats['instrument_types']}")


if __name__ == '__main__':
    main()
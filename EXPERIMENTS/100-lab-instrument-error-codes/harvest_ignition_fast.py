#!/usr/bin/env python3
"""
Fast harvest from forum.inductiveautomation.com using only topic lists.
"""

import json
import time
import urllib.request
import urllib.error
from patterns import has_fault_code, extract_fault_codes, detect_instrument_type


BASE_URL = "https://forum.inductiveautomation.com"

CATEGORIES = [
    ("Ignition", 6),
    ("Module Development", 7),
    ("3rd Party Modules", 8),
    ("General Discussion", 5),
    ("Maker", 14),
]

INDUSTRIAL_KEYWORDS = [
    'plc', 'scada', 'hmi', 'opc', 'modbus', 'ignition', 'tag', 'gateway',
    'allen-bradley', 'rockwell', 'siemens', 'mitsubishi', 'schneider',
    'abb', 'omron', 'keyence', 'beckhoff', 'codesys', 'ladder logic',
    'driver', 'device', 'connection', 'communication', 'protocol',
    'ethernet/ip', 'profinet', 'ethercat', 'devicenet', 'controlnet',
    'compactlogix', 'controllogix', 'micrologix', 'slc', 'plc-5',
    's7-300', 's7-400', 's7-1200', 's7-1500', 'twincat',
]


def has_industrial_context(text):
    text_lower = text.lower()
    return any(kw in text_lower for kw in INDUSTRIAL_KEYWORDS)


def detect_industrial_type(text):
    text_lower = text.lower()
    types = []
    patterns = {
        'ignition': ['ignition', 'perspective', 'vision', 'tag historian', 'alarm pipeline'],
        'plc_allen_bradley': ['allen-bradley', 'rockwell', 'compactlogix', 'controllogix', 'micrologix', 'slc 500', 'plc-5', 'studio 5000', 'rslogix'],
        'plc_siemens': ['siemens', 's7-', 'twincat', 'step 7', 'tia portal'],
        'plc_mitsubishi': ['mitsubishi', 'fx', 'q series', 'l series', 'r series', 'gx works'],
        'plc_schneider': ['schneider', 'modicon', 'unity', 'somachine', 'ecostruxure'],
        'plc_beckhoff': ['beckhoff', 'twincat', 'ads', 'ethercat', 'el', 'cx'],
        'plc_omron': ['omron', 'sysmac', 'nj', 'nx', 'cj', 'cs'],
        'plc_abb': ['abb', '800xa', 'ac500', 'ac800', 'advant', 'freelance'],
        'opc_ua': ['opc ua', 'opc-ua', 'opcua', 'ua server', 'ua client'],
        'modbus': ['modbus', 'modbus tcp', 'modbus rtu'],
        'ethernet_ip': ['ethernet/ip', 'ethernet-ip', 'eip', 'cip'],
        'profinet': ['profinet', 'pn', 'rt', 'irt'],
        'bacnet': ['bacnet', 'bacnet/ip', 'bacnet ms/tp'],
    }
    for type_name, keywords in patterns.items():
        if any(kw in text_lower for kw in keywords):
            types.append(type_name)
    return types


def fetch_category_list(category_name, category_id, max_pages=5):
    """Fetch topic list from a category."""
    topics = []
    url = f"{BASE_URL}/c/{category_name.lower().replace(' ', '-')}/{category_id}.json"
    
    for page in range(max_pages):
        page_url = f"{url}?page={page}"
        try:
            req = urllib.request.Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.load(resp)
            
            topic_list = data.get('topic_list', {}).get('topics', [])
            if not topic_list:
                break
                
            for topic in topic_list:
                title = topic.get('title', '')
                excerpt = topic.get('excerpt', '')
                full_text = f"{title} {excerpt}"
                
                # Check for fault codes or industrial context
                if has_fault_code(full_text) or has_industrial_context(full_text):
                    topic_record = {
                        'source': BASE_URL,
                        'category': category_name,
                        'topic_id': topic['id'],
                        'title': title,
                        'excerpt': excerpt,
                        'view_count': topic.get('views', 0),
                        'reply_count': topic.get('reply_count', 0),
                        'like_count': topic.get('like_count', 0),
                        'created_at': topic.get('created_at', ''),
                        'last_posted_at': topic.get('last_posted_at', ''),
                        'tags': topic.get('tags', []),
                        'fault_codes': extract_fault_codes(full_text),
                        'instrument_types': detect_instrument_type(full_text),
                        'industrial_types': detect_industrial_type(full_text),
                        'solved': topic.get('solved', False),
                        'closed': topic.get('closed', False),
                    }
                    topics.append(topic_record)
            
            time.sleep(0.2)
            
        except Exception as e:
            print(f"  Error page {page}: {e}")
            break
    
    return topics


def main():
    print("=== Fast harvesting from forum.inductiveautomation.com ===")
    all_topics = []
    
    for cat_name, cat_id in CATEGORIES:
        print(f"\nHarvesting: {cat_name}")
        topics = fetch_category_list(cat_name, cat_id, max_pages=3)
        print(f"  Got {len(topics)} topics")
        all_topics.extend(topics)
        time.sleep(0.5)
    
    print(f"\n=== Total: {len(all_topics)} topics ===")
    
    # Save
    with open('raw/topics.jsonl', 'w') as f:
        for topic in all_topics:
            f.write(json.dumps(topic) + '\n')
    
    # Summary
    by_cat = {}
    for t in all_topics:
        cat = t['category']
        if cat not in by_cat:
            by_cat[cat] = {'total': 0, 'views': 0, 'codes': set(), 'industrial': set()}
        by_cat[cat]['total'] += 1
        by_cat[cat]['views'] += t['view_count']
        by_cat[cat]['codes'].update(t['fault_codes'])
        by_cat[cat]['industrial'].update(t.get('industrial_types', []))
    
    for cat, stats in by_cat.items():
        print(f"  {cat}: {stats['total']} topics, {stats['views']} views, {len(stats['codes'])} codes, types: {stats['industrial']}")


if __name__ == '__main__':
    main()
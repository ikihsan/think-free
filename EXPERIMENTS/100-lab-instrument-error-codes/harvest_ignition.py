#!/usr/bin/env python3
"""
Harvest topics from forum.inductiveautomation.com (Ignition SCADA)
for industrial automation fault/error codes.
"""

import json
import time
import urllib.request
import urllib.error
from patterns import has_fault_code, has_instrument_context, extract_fault_codes, detect_instrument_type


BASE_URL = "https://forum.inductiveautomation.com"

# Categories to search (name, id)
CATEGORIES = [
    ("Ignition", 6),
    ("Module Development", 7),
    ("3rd Party Modules", 8),
    ("General Discussion", 5),
    ("Maker", 14),
]


def fetch_category_topics(category_name, category_id, max_pages=10):
    """Fetch topics from a category."""
    topics = []
    # Try different URL formats for category
    urls_to_try = [
        f"{BASE_URL}/c/{category_name.lower().replace(' ', '-')}/{category_id}.json",
        f"{BASE_URL}/c/{category_id}.json",
        f"{BASE_URL}/c/{category_id}/l/latest.json",
    ]
    
    for url_template in urls_to_try:
        for page in range(max_pages):
            url = f"{url_template}?page={page}" if '?' not in url_template else f"{url_template}&page={page}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.load(resp)
                
                topic_list = data.get('topic_list', {}).get('topics', [])
                if not topic_list:
                    break
                    
                for topic in topic_list:
                    topic_id = topic['id']
                    # Fetch full topic details
                    topic_url = f"{BASE_URL}/t/{topic_id}.json"
                    try:
                        req = urllib.request.Request(topic_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=15) as resp:
                            topic_data = json.load(resp)
                        
                        posts = topic_data.get('post_stream', {}).get('posts', [])
                        if not posts:
                            continue
                        
                        first_post = posts[0]
                        title = topic.get('title', '')
                        raw_body = first_post.get('raw', '')
                        cooked_body = first_post.get('cooked', '')
                        full_text = f"{title} {raw_body}"
                        
                        # Check for fault code patterns and industrial context
                        if has_fault_code(full_text) or has_industrial_context(full_text):
                            topic_record = {
                                'source': BASE_URL,
                                'category': category_name,
                                'topic_id': topic_id,
                                'title': title,
                                'body_raw': raw_body,
                                'body_cooked': cooked_body,
                                'view_count': topic.get('views', 0),
                                'reply_count': topic.get('reply_count', 0),
                                'like_count': topic.get('like_count', 0),
                                'created_at': topic.get('created_at', ''),
                                'last_posted_at': topic.get('last_posted_at', ''),
                                'tags': topic.get('tags', []),
                                'category_id': topic.get('category_id', 0),
                                'posts_count': len(posts),
                                'fault_codes': extract_fault_codes(full_text),
                                'instrument_types': detect_instrument_type(full_text),
                                'industrial_types': detect_industrial_type(full_text),
                                'solved': topic.get('solved', False),
                                'closed': topic.get('closed', False),
                            }
                            topics.append(topic_record)
                            
                    except Exception as e:
                        print(f"    Failed to fetch topic {topic_id}: {e}")
                        continue
                
                # If we got results, this URL format works
                if topics:
                    break
                    
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    break  # Try next URL format
                elif e.code == 429:
                    print(f"  Rate limited on {category_name}")
                    return topics
                else:
                    print(f"  HTTP {e.code} for {url}")
                    break
            except Exception as e:
                print(f"  Error fetching page {page}: {e}")
                break
        
        if topics:
            break  # Found working URL format
    
    return topics


def has_industrial_context(text):
    """Check if text mentions industrial automation/SCADA context."""
    text_lower = text.lower()
    keywords = [
        'plc', 'scada', 'hmi', 'opc', 'modbus', 'ignition', 'tag', 'gateway',
        'allen-bradley', 'rockwell', 'siemens', 'mitsubishi', 'schneider',
        'abb', 'omron', 'keyence', 'beckhoff', 'codesys', 'ladder logic',
        'structured text', 'function block', 'io', 'input', 'output',
        'driver', 'device', 'connection', 'communication', 'protocol',
        'ethernet/ip', 'profinet', 'ethercat', 'devicenet', 'controlnet',
        'udt', 'aoi', 'routine', 'program', 'controller', 'processor',
        'compactlogix', 'controllogix', 'micrologix', 'slc', 'plc-5',
        's7-300', 's7-400', 's7-1200', 's7-1500', 'twinCAT', 'twincat',
    ]
    return any(kw in text_lower for kw in keywords)


def detect_industrial_type(text):
    """Detect industrial automation system types mentioned in text."""
    text_lower = text.lower()
    types = []
    patterns = {
        'ignition': ['ignition', 'perspective', 'vision', 'tag historian', 'alarm pipeline'],
        'plc_allen_bradley': ['allen-bradley', 'rockwell', 'compactlogix', 'controllogix', 'micrologix', 'slc 500', 'plc-5', 'studio 5000', 'rslogix'],
        'plc_siemens': ['siemens', 's7-', 'twinCAT', 'twincat', 'step 7', 'tia portal'],
        'plc_mitsubishi': ['mitsubishi', 'fx', 'q series', 'l series', 'r series', 'gx works'],
        'plc_schneider': ['schneider', 'modicon', 'unity', 'soMachine', 'ecostruxure'],
        'plc_beckhoff': ['beckhoff', 'twinCAT', 'ads', 'ethercat', 'el', 'cx'],
        'plc_omron': ['omron', 'sysmac', 'nj', 'nX', 'cj', 'cs'],
        'plc_abb': ['abb', '800xA', 'ac500', 'ac800', 'advant', 'freelance'],
        'scada_general': ['scada', 'hmi', 'supervisory', 'historian', 'alarm', 'trend'],
        'opc_ua': ['opc ua', 'opc-ua', 'opcua', 'ua server', 'ua client'],
        'modbus': ['modbus', 'modbus tcp', 'modbus rtu', 'modbus ascii'],
        'ethernet_ip': ['ethernet/ip', 'ethernet-ip', 'eip', 'cip'],
        'profinet': ['profinet', 'pn', 'rt', 'irt'],
        'bacnet': ['bacnet', 'bacnet/ip', 'bacnet ms/tp'],
    }
    for type_name, keywords in patterns.items():
        if any(kw in text_lower for kw in keywords):
            types.append(type_name)
    return types


def main():
    print("=== Harvesting from forum.inductiveautomation.com ===")
    all_topics = []
    
    for cat_name, cat_id in CATEGORIES:
        print(f"\nHarvesting category: {cat_name} (id={cat_id})")
        topics = fetch_category_topics(cat_name, cat_id, max_pages=5)
        print(f"  Got {len(topics)} relevant topics")
        all_topics.extend(topics)
        time.sleep(1)
    
    print(f"\n=== Total topics harvested: {len(all_topics)} ===")
    
    # Save
    with open('raw/topics.jsonl', 'w') as f:
        for topic in all_topics:
            f.write(json.dumps(topic) + '\n')
    
    # Print summary
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
        print(f"  {cat}: {stats['total']} topics, {stats['views']} total views, {len(stats['codes'])} unique codes, types: {stats['industrial']}")


if __name__ == '__main__':
    main()
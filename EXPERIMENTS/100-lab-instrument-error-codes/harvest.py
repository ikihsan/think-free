#!/usr/bin/env python3
"""
Harvest topics from lab instrument community forums.
Probes for Discourse forums first, falls back to Stack Exchange.
"""

import json
import time
import urllib.request
import urllib.error
from patterns import has_fault_code, has_instrument_context, extract_fault_codes, detect_instrument_type


# Candidate Discourse forums for lab instruments
CANDIDATE_FORUMS = [
    # General chromatography/mass spec
    "https://chromatography-forum.com",
    "https://mass-spec.community",
    
    # Major vendor communities (if Discourse)
    "https://forum.thermofisher.com",
    "https://community.agilent.com",
    "https://community.bruker.com",
    "https://discuss.illumina.com",
    "https://forum.beckmancoulter.com",
    "https://community.waters.com",
    "https://forum.jeol.com",
    "https://forum.zeiss.com",
    "https://forum.oxfordnanopore.com",
    "https://community.pacb.com",
    "https://forum.bio-rad.com",
    "https://community.shimadzu.com",
    "https://forum.perkinelmer.com",
]

# Stack Exchange sites as fallback
STACK_EXCHANGE_SITES = [
    "bioinformatics.stackexchange.com",
    "chemistry.stackexchange.com",
    "biology.stackexchange.com",
    "academia.stackexchange.com",
]

# Discourse API endpoints
DISCOURSE_ENDPOINTS = {
    'latest': '/latest.json',
    'top': '/top.json',
    'categories': '/categories.json',
    'topic': '/t/{topic_id}.json',
}


def probe_discourse(base_url, timeout=10):
    """Probe if a URL is a Discourse forum and return basic info."""
    try:
        # Try to fetch /site.json which exists on all Discourse instances
        url = base_url.rstrip('/') + '/site.json'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.load(resp)
            return {
                'url': base_url,
                'name': data.get('name', 'Unknown'),
                'version': data.get('version', 'Unknown'),
                'discourse': True,
            }
    except Exception:
        pass
    
    # Try /about.json as alternative
    try:
        url = base_url.rstrip('/') + '/about.json'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.load(resp)
            return {
                'url': base_url,
                'name': data.get('title', 'Unknown'),
                'version': data.get('version', 'Unknown'),
                'discourse': True,
            }
    except Exception:
        pass
    
    return None


def fetch_discourse_topics(base_url, limit=50, timeout=10):
    """Fetch topics from a Discourse forum."""
    topics = []
    page = 0
    
    while len(topics) < limit:
        url = f"{base_url.rstrip('/')}/latest.json?page={page}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.load(resp)
                
            topic_list = data.get('topic_list', {}).get('topics', [])
            if not topic_list:
                break
                
            for topic in topic_list:
                if len(topics) >= limit:
                    break
                    
                # Fetch full topic details
                topic_id = topic['id']
                topic_url = f"{base_url.rstrip('/')}/t/{topic_id}.json"
                try:
                    req = urllib.request.Request(topic_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=timeout) as resp:
                        topic_data = json.load(resp)
                    
                    # Extract posts
                    posts = topic_data.get('post_stream', {}).get('posts', [])
                    if not posts:
                        continue
                    
                    first_post = posts[0]
                    last_post = posts[-1] if len(posts) > 1 else first_post
                    
                    title = topic.get('title', '')
                    body = first_post.get('cooked', '')  # HTML
                    # Also get raw if available
                    raw_body = first_post.get('raw', body)
                    
                    # Combine title and body for pattern matching
                    full_text = f"{title} {raw_body}"
                    
                    # Only keep if it has fault code patterns and instrument context
                    if has_fault_code(full_text) and has_instrument_context(full_text):
                        topic_record = {
                            'source': base_url,
                            'topic_id': topic_id,
                            'title': title,
                            'body_raw': raw_body,
                            'body_cooked': body,
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
                            'solved': topic.get('solved', False),
                            'closed': topic.get('closed', False),
                        }
                        topics.append(topic_record)
                        
                except Exception as e:
                    print(f"  Failed to fetch topic {topic_id}: {e}")
                    continue
            
            page += 1
            if page > 10:  # Safety limit
                break
            time.sleep(0.5)  # Be polite
            
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"  Rate limited on {base_url}")
            break
        except Exception as e:
            print(f"  Error fetching page {page}: {e}")
            break
    
    return topics


def probe_all_candidates():
    """Probe all candidate forums and return working ones."""
    working = []
    for url in CANDIDATE_FORUMS:
        print(f"Probing {url}...")
        result = probe_discourse(url)
        if result:
            print(f"  ✓ Found Discourse: {result['name']}")
            working.append(result)
        else:
            print(f"  ✗ Not Discourse or not accessible")
        time.sleep(0.2)
    return working


def harvest_from_working_forums(working_forums, per_forum=50):
    """Harvest topics from all working forums."""
    all_topics = []
    for forum in working_forums:
        print(f"Harvesting from {forum['name']} ({forum['url']})...")
        topics = fetch_discourse_topics(forum['url'], limit=per_forum)
        print(f"  Got {len(topics)} relevant topics")
        all_topics.extend(topics)
        time.sleep(1)
    return all_topics


def save_topics(topics, filepath):
    """Save topics as JSONL."""
    with open(filepath, 'w') as f:
        for topic in topics:
            f.write(json.dumps(topic) + '\n')


def load_topics(filepath):
    """Load topics from JSONL."""
    topics = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                topics.append(json.loads(line))
    return topics


def main():
    print("=== Probing candidate lab instrument forums ===")
    working = probe_all_candidates()
    
    if not working:
        print("\nNo working Discourse forums found. Will need alternative approach.")
        # Save empty result
        save_topics([], 'raw/topics.jsonl')
        return
    
    print(f"\n=== Harvesting from {len(working)} working forums ===")
    topics = harvest_from_working_forums(working, per_forum=50)
    
    print(f"\n=== Total topics harvested: {len(topics)} ===")
    save_topics(topics, 'raw/topics.jsonl')
    
    # Print summary
    by_forum = {}
    for t in topics:
        src = t['source']
        if src not in by_forum:
            by_forum[src] = {'total': 0, 'views': 0, 'codes': set()}
        by_forum[src]['total'] += 1
        by_forum[src]['views'] += t['view_count']
        by_forum[src]['codes'].update(t['fault_codes'])
    
    for src, stats in by_forum.items():
        print(f"  {src}: {stats['total']} topics, {stats['views']} total views, {len(stats['codes'])} unique codes")


if __name__ == '__main__':
    main()
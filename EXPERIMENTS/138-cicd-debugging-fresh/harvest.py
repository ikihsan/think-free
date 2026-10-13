#!/usr/bin/env python3
"""
Harvest topics from discuss.circleci.com Discourse forum.
Uses only Python stdlib (urllib, json).
"""

import json
import urllib.request
import urllib.error
import time
import sys
from pathlib import Path

BASE_URL = "https://discuss.circleci.com"
CATEGORIES = {
    14: "environment",      # Build Environment - 4699 topics
    12: "bug-reports",      # Bug Reports - 2000 topics
    17: "deployment",       # Deployments - 642 topics
    60: "integrations",     # Integrations and Accounts - 384 topics
    97: "api",              # API - 125 topics
}

def fetch_json(url):
    """Fetch and parse JSON from URL with stdlib."""
    req = urllib.request.Request(url, headers={'User-Agent': 'ThinkFree/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} for {url}: {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def harvest_category(category_id, category_slug, max_topics=200):
    """Harvest topics from a category."""
    topics = []
    page = 0
    
    while len(topics) < max_topics:
        url = f"{BASE_URL}/c/{category_slug}/{category_id}.json?page={page}"
        data = fetch_json(url)
        
        if not data or 'topic_list' not in data or 'topics' not in data['topic_list']:
            break
            
        page_topics = data['topic_list']['topics']
        if not page_topics:
            break
            
        for topic in page_topics:
            # Filter: only topics with views > 0 and at least some engagement
            if topic.get('views', 0) > 0:
                topics.append({
                    'id': topic['id'],
                    'title': topic['title'],
                    'slug': topic['slug'],
                    'views': topic['views'],
                    'posts_count': topic['posts_count'],
                    'reply_count': topic['reply_count'],
                    'created_at': topic['created_at'],
                    'last_posted_at': topic.get('last_posted_at', ''),
                    'tags': topic.get('tags', []),
                    'category_id': category_id,
                    'category': category_slug,
                    'excerpt': topic.get('excerpt', '')[:500],  # Truncate
                    'pinned': topic.get('pinned', False),
                    'closed': topic.get('closed', False),
                    'archived': topic.get('archived', False),
                })
                
                if len(topics) >= max_topics:
                    break
        
        page += 1
        time.sleep(0.5)  # Be polite
        
        # Check if there are more pages
        if 'more_topics_url' not in data['topic_list']:
            break
    
    return topics

def harvest_topic_details(topic_id, topic_slug):
    """Fetch full topic details including posts."""
    url = f"{BASE_URL}/t/{topic_slug}/{topic_id}.json"
    data = fetch_json(url)
    
    if not data or 'post_stream' not in data or 'posts' not in data['post_stream']:
        return None
    
    posts = data['post_stream']['posts']
    if not posts:
        return None
    
    # Combine all post content for analysis
    full_content = []
    for post in posts:
        cooked = post.get('cooked', '')
        # Strip HTML tags (simple approach)
        import re
        text = re.sub(r'<[^>]+>', '', cooked)
        text = re.sub(r'\s+', ' ', text).strip()
        if text:
            full_content.append(text)
    
    return {
        'posts_count': len(posts),
        'full_content': '\n\n'.join(full_content)[:10000],  # Limit size
        'first_post': posts[0].get('cooked', '')[:5000] if posts else '',
        'accepted_answer': data.get('accepted_answer', False),
    }

def main():
    output_dir = Path(__file__).parent / "raw"
    output_dir.mkdir(exist_ok=True)
    
    all_topics = []
    
    for cat_id, cat_slug in CATEGORIES.items():
        print(f"Harvesting category {cat_slug} (id={cat_id})...")
        topics = harvest_category(cat_id, cat_slug, max_topics=80)  # ~80 per category
        print(f"  Got {len(topics)} topics with views > 0")
        all_topics.extend(topics)
        time.sleep(1)
    
    print(f"Total topics harvested: {len(all_topics)}")
    
    # Fetch details for a subset (top by views)
    all_topics.sort(key=lambda t: t['views'], reverse=True)
    detailed_topics = all_topics[:60]  # Top 60 by views
    
    print(f"Fetching details for top {len(detailed_topics)} topics...")
    for i, topic in enumerate(detailed_topics):
        print(f"  [{i+1}/{len(detailed_topics)}] Topic {topic['id']}: {topic['title'][:60]}...")
        details = harvest_topic_details(topic['id'], topic['slug'])
        if details:
            topic.update(details)
        time.sleep(0.3)
    
    # Save raw data
    raw_file = output_dir / "topics.jsonl"
    with open(raw_file, 'w') as f:
        for topic in all_topics:
            f.write(json.dumps(topic) + '\n')
    
    print(f"Saved {len(all_topics)} topics to {raw_file}")
    
    # Also save detailed subset
    detailed_file = output_dir / "topics_detailed.jsonl"
    with open(detailed_file, 'w') as f:
        for topic in detailed_topics:
            f.write(json.dumps(topic) + '\n')
    
    print(f"Saved {len(detailed_topics)} detailed topics to {detailed_file}")

if __name__ == "__main__":
    main()
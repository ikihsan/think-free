#!/usr/bin/env python3
"""
Collect practitioner rows from Open Robotics Discourse forum for ROS error codes.
Fetches topics from relevant categories and filters for error/fault code discussions.
"""

import json
import urllib.request
import time
import re
from typing import List, Dict, Any

# Categories to search for error code discussions
CATEGORIES = {
    44: "Navigation (Nav2)",
    124: "Gazebo/Ignition",
    8: "General ROS",
    13: "MoveIt",
    108: "ros2_control",
    103: "Open-RMF",
    111: "ROS Project",
    114: "ROS REPs/Design",
    12: "TurtleBot",
    95: "Gazebo",
    106: "ros-controls",
    101: "Open-RMF",
    90: "Infrastructure",
    16: "ROS Sync",
    112: "ROS Releases",
    113: "ROS PMC",
    116: "OSRA Announcements",
    122: "Community News",
}

# Error code patterns to identify practitioner rows
ERROR_PATTERNS = [
    r'error\s+code\s+\d+',
    r'error\s+code\s+[A-Z_]+',
    r'error\s+[A-Z_]{3,}',
    r'fault\s+code\s+\d+',
    r'fault\s+code\s+[A-Z_]+',
    r'\b(INVALID_JOINTS|NO_PATH_FOUND|EXTRAPOLATION|CONTROLLER_FAILED|PLANNING_FAILED|CONTROL_FAILED)\b',
    r'\bError\s+Code\s+\d+\b',
    r'\bError\s+[A-Z_]{3,}\b',
    r'error\s+\d+',
    r'\b(rosidl|ament|colcon|catkin|cmake)\s+error\b',
    r'build\s+error',
    r'launch\s+error',
    r'RuntimeError',
    r'Segmentation\s+fault',
    r'assertion\s+failed',
]

def matches_error_pattern(title: str) -> bool:
    """Check if title contains error/fault code patterns."""
    title_lower = title.lower()
    for pattern in ERROR_PATTERNS:
        if re.search(pattern, title_lower, re.IGNORECASE):
            return True
    return False

def fetch_category_topics(category_id: int, pages: int = 10) -> List[Dict]:
    """Fetch topics from a Discourse category."""
    topics = []
    for page in range(pages):
        url = f"https://discourse.openrobotics.org/c/{category_id}.json?page={page}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ThinkFree/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                topic_list = data.get('topic_list', {})
                for topic in topic_list.get('topics', []):
                    # Only include topics with view_count > 0 and at least some engagement
                    if topic.get('views', 0) > 0:
                        topics.append({
                            'category_id': category_id,
                            'category_name': CATEGORIES.get(category_id, f'Category {category_id}'),
                            'topic_id': topic['id'],
                            'title': topic['title'],
                            'views': topic['views'],
                            'reply_count': topic['reply_count'],
                            'like_count': topic.get('like_count', 0),
                            'created_at': topic['created_at'],
                            'last_posted_at': topic['last_posted_at'],
                            'tags': topic.get('tags', []),
                            'posts_count': topic['posts_count'],
                            'pinned': topic.get('pinned', False),
                            'closed': topic.get('closed', False),
                            'archetype': topic.get('archetype', 'regular'),
                        })
                if not topic_list.get('topics'):
                    break
        except Exception as e:
            print(f"Error fetching category {category_id} page {page}: {e}")
        time.sleep(0.5)  # Polite polling
    return topics

def fetch_topic_details(topic_id: int) -> Dict:
    """Fetch detailed topic content including first post."""
    url = f"https://discourse.openrobotics.org/t/{topic_id}.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ThinkFree/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            post_stream = data.get('post_stream', {})
            posts = post_stream.get('posts', [])
            if posts:
                first_post = posts[0]
                return {
                    'topic_id': topic_id,
                    'body': first_post.get('cooked', ''),
                    'excerpt': first_post.get('excerpt', ''),
                    'poster_username': first_post.get('username', ''),
                    'post_number': first_post.get('post_number', 1),
                }
    except Exception as e:
        print(f"Error fetching topic {topic_id}: {e}")
    return {}

def main():
    print("Collecting practitioner rows from Open Robotics Discourse...")
    
    all_topics = []
    for cat_id, cat_name in CATEGORIES.items():
        print(f"  Fetching {cat_name} (category {cat_id})...")
        topics = fetch_category_topics(cat_id, pages=3)
        print(f"    Found {len(topics)} topics with views > 0")
        all_topics.extend(topics)
        time.sleep(0.5)
    
    print(f"\nTotal topics fetched: {len(all_topics)}")
    
    # Filter for error/fault code discussions
    error_topics = [t for t in all_topics if matches_error_pattern(t['title'])]
    print(f"Topics matching error patterns: {len(error_topics)}")
    
    # Also include topics with specific ROS error-related tags
    ros_error_tags = {'error', 'fault', 'troubleshooting', 'debugging', 'crash', 'fail', 'exception'}
    for topic in all_topics:
        if topic not in error_topics:
            topic_tags = topic.get('tags', [])
            # Tags can be dicts with 'slug' or strings
            tag_slugs = set()
            for tag in topic_tags:
                if isinstance(tag, dict):
                    tag_slugs.add(tag.get('slug', ''))
                else:
                    tag_slugs.add(str(tag))
            if tag_slugs & ros_error_tags:
                error_topics.append(topic)
    
    print(f"After tag filtering: {len(error_topics)}")
    
    # Fetch detailed content for error topics (first 50 to be polite)
    practitioner_rows = []
    for i, topic in enumerate(error_topics[:50]):
        print(f"  Fetching details for topic {topic['topic_id']}: {topic['title'][:80]}...")
        details = fetch_topic_details(topic['topic_id'])
        row = {**topic, **details}
        practitioner_rows.append(row)
        time.sleep(0.5)
    
    # Save raw data
    import os
    os.makedirs('raw', exist_ok=True)
    with open('raw/practitioner_rows.jsonl', 'w') as f:
        for row in practitioner_rows:
            f.write(json.dumps(row) + '\n')
    
    print(f"\nSaved {len(practitioner_rows)} practitioner rows to raw/practitioner_rows.jsonl")
    
    # Print summary table
    print("\nPractitioner Rows Summary:")
    print(f"{'#':<3} {'Category':<20} {'Views':<6} {'Replies':<7} {'Title'}")
    print("-" * 100)
    for i, row in enumerate(practitioner_rows, 1):
        cat = row.get('category_name', 'Unknown')[:18]
        views = row.get('views', 0)
        replies = row.get('reply_count', 0)
        title = row.get('title', '')[:60]
        print(f"{i:<3} {cat:<20} {views:<6} {replies:<7} {title}")

if __name__ == '__main__':
    main()
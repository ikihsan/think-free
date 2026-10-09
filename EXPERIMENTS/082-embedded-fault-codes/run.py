#!/usr/bin/env python3
"""E082 — Fresh observation in embedded/mcu fault codes domain.

Harvest topics from embedded/microcontroller community forums and
write raw JSONL data for classification.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import time
import hashlib
from datetime import datetime, timezone

# Configuration
FORUMS = [
    # { "name": "...", "base_url": "...", "api_endpoint": "...", "view_count_path": "...", "code_mention_pattern": "..." }
]

DEFAULT_HEADERS = [
    "User-Agent: ThinkFree-E082-Experiment/1.0",
    "Accept: application/json",
]

TIMEOUT = 30  # seconds
REQUEST_DELAY = 1.0  # seconds between requests to be polite


def fetch_topics(forum_config, max_topics=50):
    """Fetch topics from a forum instance."""
    topics = []
    base_url = forum_config.get("base_url", "")
    api_endpoint = forum_config.get("api_endpoint", "")
    view_count_path = forum_config.get("view_count_path", "")
    code_mention_pattern = forum_config.get("code_mention_pattern", r"\b(0x[0-9a-fA-F]{2,}|ERR_\w+|FAIL_\w+|Error \d{3})\b")
    
    if not base_url or not api_endpoint:
        print(f"Skipping {forum_config.get('name', 'unnamed')}: missing base_url or api_endpoint")
        return topics
    
    try:
        url = base_url.rstrip("/") + api_endpoint
        req = urllib.request.Request(url, headers={"User-Agent": "ThinkFree-E082-Experiment/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8"))
            
            if isinstance(data, dict):
                # Handle various response formats
                items = data.get("topics", data.get("items", data.get("posts", [])))
            elif isinstance(data, list):
                items = data
            else:
                items = []
            
            for item in items[:max_topics]:
                try:
                    topic = {}
                    
                    # Title
                    topic["title"] = item.get("title", item.get("subject", ""))
                    
                    # Body/content
                    topic["body"] = item.get("body", item.get("content", item.get("selftext", "")))
                    
                    # View count
                    if view_count_path:
                        # Try to extract view count from nested path
                        view_data = item
                        for key in view_count_path.split("."):
                            if isinstance(view_data, dict):
                                view_data = view_data.get(key, {})
                        topic["view_count"] = view_data if isinstance(view_data, (int, float)) else 0
                    else:
                        # Estimate from engagement or set default
                        topic["view_count"] = item.get("view_count", item.get("views", 0))
                    
                    # Code mentions - extract code-like patterns from title and body
                    import re
                    code_pattern = re.compile(code_mention_pattern)
                    all_text = f"{topic['title']} {topic['body']}"
                    codes = code_pattern.findall(all_text)
                    topic["code_mentions"] = "; ".join(set(codes)) if codes else ""
                    topic["code_count"] = len(set(codes))
                    
                    # Tags
                    topic["tags"] = item.get("tags", item.get("forum", item.get("category", [])))
                    if isinstance(topic["tags"], str):
                        topic["tags"] = [t.strip() for t in topic["tags"].split(",") if t.strip()]
                    
                    # Creation date
                    topic["creation_date"] = item.get("date", item.get("created_utc", item.get("created", "")))
                    
                    # Replies/comments count
                    topic["replies"] = item.get("replies", item.get("num_comments", 0))
                    
                    # Solved status (forum-specific)
                    topic["solved_status"] = item.get("solved", item.get("is_answered", False))
                    
                    # Extract explicit code IDs if present
                    topic["code_ids"] = extract_code_ids(topic["title"], topic["body"])
                    
                    topics.append(topic)
                    
                except Exception as e:
                    print(f"Error processing item: {e}")
                    continue
            
            # Rate limiting
            time.sleep(REQUEST_DELAY)
            
    except Exception as e:
        print(f"Error fetching from {forum_config.get('name', 'unnamed')}: {e}")
    
    return topics


def extract_code_ids(title, body):
    """Extract explicit fault/code IDs from text."""
    import re
    
    codes = set()
    
    # Pattern 1: Hex codes like 0x1A, 0xFFFF, etc.
    hex_pattern = re.compile(r'\b0x[0-9a-fA-F]{1,8}\b')
    for m in hex_pattern.finditer(f"{title} {body}"):
        codes.add(m.group(0))
    
    # Pattern 2: Error codes like ERR_XXX, FAIL_XXX, Error NNN
    alpha_pattern = re.compile(r'\b(ERR|FAIL|Error)\s+[_0-9a-zA-Z]+\b', re.IGNORECASE)
    for m in alpha_pattern.finditer(f"{title} {body}"):
        codes.add(m.group(0))
    
    # Pattern 3: Standard fault code patterns (vendor-specific)
    # ARM Cortex-M fault codes
    cortex_pattern = re.compile(r'\b(?:HardFault|MemManage|BusFault|UsageFault|SVCall|PendSV|DebugMonitor)\b', re.IGNORECASE)
    for m in cortex_pattern.finditer(f"{title} {body}"):
        codes.add(m.group(0))
    
    # RISC-V exception codes
    riscv_pattern = re.compile(r'\b(?:ecall|ebreak|mret|dret|eret)\b', re.IGNORECASE)
    for m in riscv_pattern.finditer(f"{title} {body}"):
        codes.add(m.group(0))
    
    # MCU vendor codes
    vendor_patterns = {
        "stm": r'\b(?:ST_ERROR|ST_IT|\bSTM\w{0,10}\b)',
        "nxp": r'\b(?:MCF|S08|ColdFire)\b',
        "pic": r'\b(?:PIC\d{1,3}|C\d{1,3})\b',
        "avr": r'\b(?:AVR_\w+|TWI|USI|UART)\b',
    }
    
    for prefix, pattern in vendor_patterns.items():
        full_pattern = re.compile(pattern, re.IGNORECASE)
        for m in full_pattern.finditer(f"{title} {body}"):
            codes.add(m.group(0))
    
    return "; ".join(sorted(codes)) if codes else ""


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="E082: Harvest forum topics")
    parser.add_argument("--max-topics", type=int, default=50,
                        help="Max topics per forum (default: 50)")
    parser.add_argument("--output", default="raw",
                        help="Output directory for raw data (default: raw)")
    parser.add_argument("--forums-config", default=None,
                        help="Path to forums config JSON file")
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Default forum configurations (will be expanded per domain)
    forums = [
        {
            "name": "embedded forum placeholder",
            "base_url": "",
            "api_endpoint": "",
            "view_count_path": "",
            "code_mention_pattern": r"\b(0x[0-9a-fA-F]{2,}|ERR_\w+|FAIL_\w+|Error \d{3}|HardFault|MemManage|BusFault)\b",
        },
    ]
    
    if args.forums_config:
        try:
            with open(args.forums_config) as f:
                config_forums = json.load(f)
                forums.extend(config_forums)
        except Exception as e:
            print(f"Error reading forums config: {e}")
    
    all_topics = []
    for forum in forums:
        print(f"Fetching topics from {forum.get('name', 'unnamed')}...")
        topics = fetch_topics(forum, max_topics=args.max_topics)
        print(f"  Fetched {len(topics)} topics")
        all_topics.extend(topics)
        
        # Save per-forum data
        forum_name = forum.get("name", "unnamed").replace(" ", "_").replace("/", "_")
        output_file = os.path.join(args.output, f"topics_{forum_name}.jsonl")
        with open(output_file, "w") as f:
            for topic in topics:
                f.write(json.dumps(topic) + "\n")
        print(f"  Saved {len(topics)} topics to {output_file}")
    
    # Save combined data
    combined_file = os.path.join(args.output, "topics_all.jsonl")
    with open(combined_file, "w") as f:
        for topic in all_topics:
            f.write(json.dumps(topic) + "\n")
    print(f"Saved {len(all_topics)} total topics to {combined_file}")
    
    # Print summary
    total_view_positive = sum(1 for t in all_topics if t.get("view_count", 0) > 0)
    total_code_mentions = sum(1 for t in all_topics if t.get("code_count", 0) > 0)
    print(f"\nSummary:")
    print(f"  Total topics: {len(all_topics)}")
    print(f"  Topics with view_count > 0: {total_view_positive} ({total_view_positive/len(all_topics)*100:.1f}%)")
    print(f"  Topics with code mentions: {total_code_mentions} ({total_code_mentions/len(all_topics)*100:.1f}%)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
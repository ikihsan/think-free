#!/usr/bin/env python3
"""
E112 — Harvest VS Code Marketplace extensions.
Fetches extensions via the public API and classifies by need-related keywords.
"""

import json
import sys
import urllib.request
import urllib.parse
import time
from typing import List, Dict, Any

# Need-related keywords (declared before measurement, from PROTOCOL.md)
NEED_KEYWORDS = [
    'error', 'fix', 'debug', 'troubleshoot', 'problem', 'issue', 'crash', 'bug',
    'lint', 'format', 'refactor', 'test', 'deploy', 'ci', 'cd', 'git', 'docker',
    'kubernetes', 'api', 'database', 'sql', 'nosql', 'react', 'vue', 'angular',
    'node', 'python', 'java', 'rust', 'go', 'typescript', 'javascript'
]

EXCLUDED_KEYWORDS = [
    'theme', 'color', 'icon', 'font', 'snippet', 'boilerplate', 'template',
    'starter', 'scaffold', 'sandbox', 'playground', 'toy', 'sample', 'demo',
    'example', 'tutorial', 'learn', 'practice', 'exercise', 'hello world',
    'awesome', 'collection', 'pack', 'bundle', 'suite', 'kit'
]

API_URL = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"

def build_query(page_size: int = 100, flags: int = 870) -> Dict[str, Any]:
    """Build the extension query payload."""
    return {
        "filters": [{
            "criteria": [
                {"filterType": 8, "value": "Microsoft.VisualStudio.Code"},  # VS Code
                {"filterType": 10, "value": "target:\"Microsoft.VisualStudio.Code\""},
                {"filterType": 12, "value": "37888"}  # category: All
            ],
            "pageSize": page_size,
            "pageNumber": 0,
            "sortBy": 4,  # sort by install count descending
            "sortOrder": 0
        }],
        "flags": flags
    }

def fetch_extensions(page_size: int = 100, max_pages: int = 10) -> List[Dict[str, Any]]:
    """Fetch extensions from the marketplace API."""
    all_extensions = []
    
    for page in range(max_pages):
        query = build_query(page_size)
        query["filters"][0]["pageNumber"] = page
        
        data = json.dumps(query).encode('utf-8')
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json;api-version=6.0-preview.1'
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(f"Error fetching page {page}: {e}", file=sys.stderr)
            break
        
        extensions = result.get('results', [{}])[0].get('extensions', [])
        if not extensions:
            break
            
        for ext in extensions:
            # Extract relevant fields
            ext_data = {
                'name': ext.get('extensionName', ''),
                'publisher': ext.get('publisher', {}).get('publisherName', ''),
                'display_name': ext.get('displayName', ''),
                'description': ext.get('shortDescription', '') or ext.get('description', ''),
                'install_count': ext.get('statistics', [{}])[0].get('value', 0) if ext.get('statistics') else 0,
                'rating': ext.get('rating', 0),
                'rating_count': ext.get('ratingCount', 0),
                'tags': ext.get('tags', []),
                'categories': ext.get('categories', []),
                'versions': [v.get('version', '') for v in ext.get('versions', [])],
                'last_updated': ext.get('lastUpdated', ''),
                'published_date': ext.get('publishedDate', ''),
            }
            all_extensions.append(ext_data)
        
        print(f"Fetched page {page + 1}: {len(extensions)} extensions")
        time.sleep(0.5)  # Rate limiting
        
        if len(extensions) < page_size:
            break
    
    return all_extensions

def classify_extension(ext: Dict[str, Any]) -> str:
    """Classify extension as 'need-related', 'random', or 'unclassified'."""
    text = f"{ext.get('display_name', '')} {ext.get('description', '')} {' '.join(ext.get('tags', []))}".lower()
    
    # Check excluded keywords first (hard exclusion)
    for kw in EXCLUDED_KEYWORDS:
        if kw.lower() in text:
            return 'random'
    
    # Check need-related keywords
    for kw in NEED_KEYWORDS:
        if kw.lower() in text:
            return 'need-related'
    
    return 'unclassified'

def main():
    print("Fetching VS Code Marketplace extensions...")
    extensions = fetch_extensions(page_size=100, max_pages=20)
    print(f"Total fetched: {len(extensions)}")
    
    # Classify all
    classified = []
    for ext in extensions:
        classification = classify_extension(ext)
        ext['classification'] = classification
        classified.append(ext)
    
    # Stats
    need_count = sum(1 for e in classified if e['classification'] == 'need-related')
    random_count = sum(1 for e in classified if e['classification'] == 'random')
    unclassified_count = sum(1 for e in classified if e['classification'] == 'unclassified')
    
    print(f"Need-related: {need_count}")
    print(f"Random: {random_count}")
    print(f"Unclassified: {unclassified_count}")
    print(f"Coverage: {(need_count + random_count) / len(classified) * 100:.1f}%")
    
    # Save raw data
    with open('raw_data.jsonl', 'w') as f:
        for ext in classified:
            f.write(json.dumps(ext) + '\n')
    
    print("Saved raw_data.jsonl")
    
    # Also save classified data for analysis
    with open('classified_data.jsonl', 'w') as f:
        for ext in classified:
            if ext['classification'] in ('need-related', 'random'):
                f.write(json.dumps(ext) + '\n')
    
    print("Saved classified_data.jsonl")

if __name__ == "__main__":
    main()

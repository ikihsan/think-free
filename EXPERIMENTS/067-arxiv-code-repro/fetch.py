#!/usr/bin/env python3
"""
Fetch ArXiv papers from target categories and extract code repository URLs.

Uses ArXiv OAI-PMH API for reliable harvesting with date ranges.
"""

import re
import json
import time
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from urllib.parse import urlencode

# ArXiv OAI-PMH endpoint
OAI_BASE = "http://export.arxiv.org/oai2"

# Target categories with date range 2024-01-01 to 2024-12-31
# Using ArXiv OAI-PMH set specifications
CATEGORIES = [
    "cs:cs:LG",    # Machine Learning
    "cs:cs:AI",    # Artificial Intelligence
    "stat:stat:ML", # Machine Learning (Statistics)
    "physics:physics:comp-ph",  # Computational Physics
    "cs:cs:CV",    # Computer Vision
    "cs:cs:CL",    # Computation and Language
]

DATE_FROM = "2024-01-01"
DATE_UNTIL = "2024-12-31"

# Stride for sampling (every Nth paper)
STRIDE = 50

# Regex patterns for code repository URLs
CODE_URL_PATTERNS = [
    r'(?:code|github|gitlab|bitbucket)[:\s]*(https?://(?:github|gitlab|bitbucket)\.com/[\w\-]+/[\w\-\.]+)',
    r'(https?://(?:github|gitlab|bitbucket)\.com/[\w\-]+/[\w\-\.]+)',
]

# Namespace map for OAI-PMH
NS = {
    'oai': 'http://www.openarchives.org/OAI/2.0/',
    'arxiv': 'http://arxiv.org/OAI/arXiv/',
    'dc': 'http://purl.org/dc/elements/1.1/',
}

@dataclass
class Paper:
    arxiv_id: str
    title: str
    authors: List[str]
    categories: List[str]
    abstract: str
    comments: str
    journal_ref: str
    doi: str
    submitted: str
    code_urls: List[str]
    repo_info: List[Dict] = None

    def __post_init__(self):
        if self.repo_info is None:
            self.repo_info = []

def fetch_oai_list(metadata_prefix: str, set_spec: str, from_date: str, until_date: str, resumption_token: str = None) -> tuple:
    """Fetch a page of records from ArXiv OAI-PMH."""
    params = {
        'verb': 'ListRecords',
        'metadataPrefix': metadata_prefix,
        'set': set_spec,
        'from': from_date,
        'until': until_date,
    }
    if resumption_token:
        params = {'verb': 'ListRecords', 'resumptionToken': resumption_token}

    url = f"{OAI_BASE}?{urlencode(params)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'arxiv-repro-experiment/1.0'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        xml_content = resp.read()

    root = ET.fromstring(xml_content)
    records = root.findall('.//oai:record', NS)
    token_elem = root.find('.//oai:resumptionToken', NS)
    next_token = token_elem.text if token_elem is not None and token_elem.text else None
    return records, next_token

def parse_arxiv_record(record) -> Optional[Paper]:
    """Parse an OAI-PMH record into a Paper."""
    try:
        header = record.find('oai:header', NS)
        metadata = record.find('oai:metadata', NS)
        arxiv_meta = metadata.find('arxiv:arXiv', NS) if metadata is not None else None
        if arxiv_meta is None:
            return None

        def safe_text(elem, xpath):
            found = elem.find(xpath, NS)
            return found.text if found is not None and found.text is not None else ""

        arxiv_id = safe_text(arxiv_meta, 'arxiv:id')
        if not arxiv_id:
            return None

        title = safe_text(arxiv_meta, 'arxiv:title')
        abstract = safe_text(arxiv_meta, 'arxiv:abstract')
        comments = safe_text(arxiv_meta, 'arxiv:comments')
        journal_ref = safe_text(arxiv_meta, 'arxiv:journal-ref')
        doi = safe_text(arxiv_meta, 'arxiv:doi')
        submitted = safe_text(arxiv_meta, 'arxiv:created')

        authors = []
        for author in arxiv_meta.findall('arxiv:authors/arxiv:author', NS):
            name = author.find('arxiv:keyname', NS)
            if name is not None and name.text:
                authors.append(name.text)

        categories = []
        for cat in arxiv_meta.findall('arxiv:categories', NS):
            if cat.text:
                categories.extend(cat.text.split())

        # Extract code URLs from comments, journal_ref, doi
        text_blob = " ".join([comments, journal_ref, doi, abstract])
        code_urls = []
        for pattern in CODE_URL_PATTERNS:
            matches = re.findall(pattern, text_blob, re.IGNORECASE)
            for m in matches:
                # Normalize URL
                url = m if isinstance(m, str) else m[0] if isinstance(m, tuple) else str(m)
                url = url.rstrip('.,);]')
                if url not in code_urls:
                    code_urls.append(url)

        return Paper(
            arxiv_id=arxiv_id,
            title=title.strip(),
            authors=authors,
            categories=categories,
            abstract=abstract.strip(),
            comments=comments.strip(),
            journal_ref=journal_ref.strip(),
            doi=doi.strip(),
            submitted=submitted.strip(),
            code_urls=code_urls,
        )
    except Exception as e:
        print(f"Error parsing record: {e}")
        return None

def extract_repo_info(url: str) -> Optional[dict]:
    """Extract platform, owner, repo from a code URL."""
    patterns = [
        r'github\.com/([\w\-]+)/([\w\-\.]+)',
        r'gitlab\.com/([\w\-]+)/([\w\-\.]+)',
        r'bitbucket\.org/([\w\-]+)/([\w\-\.]+)',
    ]
    for platform, pattern in zip(['github', 'gitlab', 'bitbucket'], patterns):
        m = re.search(pattern, url)
        if m:
            return {'platform': platform, 'owner': m.group(1), 'repo': m.group(2), 'url': url}
    return None

def main():
    all_papers = []
    papers_with_code = []

    # Limit pages per category to keep fetch time reasonable
    MAX_PAGES_PER_CATEGORY = 2

    for category in CATEGORIES:
        print(f"\n=== Harvesting {category} ===")
        set_spec = category  # category already includes the set spec format
        resumption_token = None
        page = 0
        category_papers = 0
        category_with_code = 0

        while True:
            page += 1
            if page > MAX_PAGES_PER_CATEGORY:
                print(f"  Reached page limit ({MAX_PAGES_PER_CATEGORY}), stopping")
                break
            try:
                records, resumption_token = fetch_oai_list(
                    'arXiv', set_spec, DATE_FROM, DATE_UNTIL, resumption_token
                )
            except Exception as e:
                print(f"  Error fetching page {page}: {e}")
                break

            if not records:
                break

            for record in records:
                paper = parse_arxiv_record(record)
                if paper:
                    category_papers += 1
                    all_papers.append(paper)
                    if paper.code_urls:
                        category_with_code += 1
                        papers_with_code.append(paper)

            print(f"  Page {page}: {len(records)} records, {category_papers} total, {category_with_code} with code links")

            if not resumption_token:
                break

            # Be nice to the API
            time.sleep(0.5)

        print(f"  {category} complete: {category_papers} papers, {category_with_code} with code links")

    # Apply stride sampling to papers with code
    sampled = papers_with_code[::STRIDE]
    print(f"\nTotal papers: {len(all_papers)}")
    print(f"Papers with code links: {len(papers_with_code)}")
    print(f"Stride sample (every {STRIDE}): {len(sampled)}")

    # Enrich with repo info
    for paper in sampled:
        paper.repo_info = []
        for url in paper.code_urls:
            info = extract_repo_info(url)
            if info:
                paper.repo_info.append(info)

    # Save raw data
    output = {
        'harvest_date': time.strftime('%Y-%m-%d'),
        'categories': CATEGORIES,
        'date_range': f"{DATE_FROM} to {DATE_UNTIL}",
        'stride': STRIDE,
        'total_papers': len(all_papers),
        'papers_with_code_links': len(papers_with_code),
        'sampled_papers': len(sampled),
        'papers': [asdict(p) for p in sampled],
    }

    with open('raw/papers.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved {len(sampled)} sampled papers to raw/papers.json")

    # Print summary
    with_code = sum(1 for p in sampled if p.repo_info)
    print(f"Sampled papers with extractable repo info: {with_code}")

if __name__ == '__main__':
    main()
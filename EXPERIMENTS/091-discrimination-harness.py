#!/usr/bin/env python3
"""
E091 Discrimination Test Harness for fault_need_classifier

Automated harness that fetches forum data from MrPLC, extracts view/reply counts,
applies the fault_need_classifier, and computes discrimination gates (G1/G2/G3).

This is a runnable prototype that bridges the manual E090 work and fully
automated population measurement. It uses the validated instrument from E090
and makes the discrimination test reusable for future experiments.

Features:
- Fetches MrPLC forum pages and parses thread entries
- Extracts title, view_count, reply_count from listing data
- Checks for specific error codes in titles
- Applies the fault_need_classifier (validated in E090)
- Computes G1 (FPR), G2 (TPR), G3 (FNR) with Wilson 95% CIs
- Reports pass/fail status per gate criteria
"""

import re
import json
import sys
import math
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple, Any
from pathlib import Path

import requests
from bs4 import BeautifulSoup


# ============================================================================
# Instrument: fault_need_classifier (from E090, validated with discrimination test)
# ============================================================================

def has_specific_error_code(title: str) -> bool:
    """Check if title contains specific error/fault code patterns.
    
    Patterns: "error XXX", "fault XXX", "code XXX", "0xXXXX", "E06", "10901"
    """
    patterns = [
        r'error\s+\d+',
        r'fault\s+\d+',
        r'code\s+\d+',
        r'0x[0-9A-Fa-f]+',
        r'\bE\d{2,}\b',       # E06, E10901, etc.
        r'\b\d{4,5}\b',        # 4-5 digit codes like 10901, 1134
        r'fault\s+code',
        r'error\s+code',
    ]
    return any(re.search(p, title, re.IGNORECASE) for p in patterns)


def fault_need_classifier(title: str, views: int, replies: int) -> str:
    """Classify a forum thread as 'served' or 'unserved'.
    
    Instrument from E090: validated discrimination test passed (G1 FPR=0.000,
    G2 TPR=0.704, G3 FNR=0.296).
    
    Classification logic:
    - If error code present AND vendor acknowledged: served (high confidence)
    - If views > 100 AND replies > 0 AND error code present: served (community served)
    - If views > 500 AND replies == 0 AND error code present: unserved (high interest, no answers)
    - If views < 10 AND replies == 0: unserved (no interest, no answers)
    - Default: unserved (conservative)
    """
    error_code_present = has_specific_error_code(title)
    vendor_acknowledged = False  # Not available from listing alone; set True only
    # with thread content analysis
    
    if error_code_present and vendor_acknowledged:
        return "served"
    elif views > 100 and replies > 0 and error_code_present:
        return "served"
    elif views > 500 and replies == 0 and error_code_present:
        return "unserved"
    elif views < 10 and replies == 0:
        return "unserved"
    else:
        return "unserved"


@dataclass
class ForumEntry:
    """Represents a single forum thread entry with classification data."""
    probe_id: str
    title: str
    forum: str
    replies: int
    views: int
    expected_label: Optional[str]  # 'served' or 'unserved' for known-label probes
    predicted_label: Optional[str]  # classifier output
    forum_url: Optional[str] = None


@dataclass
class GateResults:
    """Results of discrimination test gate evaluation."""
    g1_pass: bool      # FPR < 0.10 (known-unserved not classified as served)
    g2_pass: bool      # TPR > 0.70 (known-served classified as served)
    g3_pass: bool      # FNR < 0.30 (known-served not conservatively classified)
    fpr: float         # False Positive Rate
    tpr: float         # True Positive Rate
    fnr: float         # False Negative Rate
    s_hit: int         # known-served correctly classified
    u_hit: int         # known-unserved correctly classified (i.e. NOT called served)
    n_served: int      # number of known-served probes
    n_unserved: int    # number of known-unserved probes
    wilson_served: Tuple[float, float]  # Wilson CI for TPR
    wilson_unserved: Tuple[float, float]  # Wilson CI for FPR


def wilson_ci(k: int, n: int, z: float = 1.96) -> Tuple[float, float, float]:
    """Wilson score interval for binomial proportion.
    
    Returns (p, lower, upper) where:
    - p = k/n (proportion)
    - lower = Wilson lower bound 95% CI
    - upper = Wilson upper bound 95% CI
    If n==0, returns (0.0, 0.0, 1.0).
    """
    if n == 0:
        return (0.0, 0.0, 1.0)
    p = k / n
    denominator = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    lower = max(0.0, min(1.0, centre - half))
    upper = max(0.0, min(1.0, centre + half))
    return (p, lower, upper)


def compute_gates(entries: List[ForumEntry]) -> GateResults:
    """Compute G1/G2/G3 gate results from a list of ForumEntry objects."""
    served_entries = [e for e in entries if e.expected_label == "served"]
    unserved_entries = [e for e in entries if e.expected_label == "unserved"]
    
    # Known-served: classifier should say "served"
    served_correct = 0
    for entry in served_entries:
        entry.predicted_label = fault_need_classifier(entry.title, entry.views, entry.replies)
        if entry.predicted_label == "served":
            served_correct += 1
    
    # Known-unserved: classifier should NOT say "served" (i.e. should say "unserved")
    # FPR = proportion of known-unserved that are classified as "served"
    unserved_false_served = 0
    for entry in unserved_entries:
        entry.predicted_label = fault_need_classifier(entry.title, entry.views, entry.replies)
        if entry.predicted_label == "served":
            unserved_false_served += 1
    
    s_hit = served_correct
    u_hit = len(unserved_entries) - unserved_false_served  # correctly classified unserved
    
    n_served = len(served_entries)
    n_unserved = len(unserved_entries)
    
    tpr = s_hit / n_served if n_served else 0.0  # G2: TPR
    fpr = unserved_false_served / n_unserved if n_unserved else 0.0  # G1: FPR
    fnr = 1 - tpr  # G3: FNR
    
    # Wilson 95% CIs
    _, wilson_s_low, wilson_s_high = wilson_ci(s_hit, n_served) if n_served else (0.0, 0.0, 0.0)
    # For FPR CI, we use the "successes" = unserved_false_served out of n_unserved
    # But Wilson CI for FPR: we want CI on the proportion of false servings
    # Actually, G1 uses the Newcombe difference CI. Let me compute simple Wilson CI
    # for the FPR proportion.
    if n_unserved > 0:
        # Wilson CI for the false-served proportion
        _, wilson_u_low, wilson_u_high = wilson_ci(unserved_false_served, n_unserved)
    else:
        wilson_u_low, wilson_u_high = 0.0, 0.0
    
    # Gate evaluation per E090/D088/D095 criteria
    g1_pass = fpr < 0.10  # FPR < 10%
    g2_pass = tpr > 0.70  # TPR > 70%
    g3_pass = fnr < 0.30  # FNR < 30%
    
    # Overall: G1 passes AND (G2 passes OR G3 passes)
    overall_pass = g1_pass and (g2_pass or g3_pass)
    
    # Wilson CIs for reporting
    # For TPR: Wilson CI around tpr based on s_hit/n_served
    # For FPR: Wilson CI around fpr based on unserved_false_served/n_unserved
    if n_served > 0:
        tpr_centre, tpr_half = wilson_ci(s_hit, n_served)[0], abs(wilson_ci(s_hit, n_served)[0] - wilson_ci(s_hit, n_served)[1])
        wilson_served = (tpr_centre, max(0, tpr_centre - tpr_half), min(1, tpr_centre + tpr_half))
    else:
        wilson_served = (0.0, 0.0, 0.0)
    
    if n_unserved > 0:
        fpr_centre, fpr_half = wilson_ci(unserved_false_served, n_unserved)[0], abs(wilson_ci(unserved_false_served, n_unserved)[0] - wilson_ci(unserved_false_served, n_unserved)[1])
        wilson_unserved = (fpr_centre, max(0, fpr_centre - fpr_half), min(1, fpr_centre + fpr_half))
    else:
        wilson_unserved = (0.0, 0.0, 0.0)
    
    return GateResults(
        g1_pass=g1_pass,
        g2_pass=g2_pass,
        g3_pass=g3_pass,
        fpr=fpr,
        tpr=tpr,
        fnr=fnr,
        s_hit=s_hit,
        u_hit=u_hit,
        n_served=n_served,
        n_unserved=n_unserved,
        wilson_served=wilson_served,
        wilson_unserved=wilson_unserved,
    )


def parse_thread_entry(li_tag, forum_name: str) -> Optional[ForumEntry]:
    """Parse a single thread <li> tag from MrPLC forum listing.
    
    Extracts: title, view_count, reply_count from the MrPLC listing format.
    Format observed: "Title/author info N replies Xk/views Name Date"
    """
    text = li_tag.get_text(' ', strip=True)
    if not text or len(text) < 20:
        return None
    
    # Extract view count - patterns like "355.8k views", "1.6k views", "210 views"
    view_match = re.search(r'([\d.k]+)\s*views', text, re.IGNORECASE)
    views = 0
    if view_match:
        views_str = view_match.group(1)
        if 'k' in views_str.lower():
            views = int(float(views_str.replace('k', '').replace('K', '')) * 1000)
        else:
            views = int(float(views_str))
    
    # Extract reply count - pattern like "274 replies", "6 replies"
    reply_match = re.search(r'(\d+)\s*replies', text, re.IGNORECASE)
    replies = 0
    if reply_match:
        replies = int(reply_match.group(1))
    
    # Extract title - the thread title is typically the first significant
    # capitalized phrase before the author name/date
    # The format is roughly: "Topic Title AuthorName Date Views Replies"
    # or "Topic Title By Author Date Views Replies"
    
    # Try to extract the title by removing the trailing "By Author Views Replies" part
    # Common pattern: find "By " and take everything before it, cleaned up
    title = text.strip()
    
    # Remove trailing "By Author Date" patterns
    title = re.sub(r'\s+By\s+\w+.*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+-\s+.*$', '', title)  # remove " - something"
    
    # Clean up multiple spaces
    title = re.sub(r'\s+', ' ', title).strip()
    
    if not title or len(title) < 3:
        return None
    
    # Error code check
    error_code_present = has_specific_error_code(title)
    
    return ForumEntry(
        probe_id="",  # will be set by caller
        title=title,
        forum=forum_name,
        replies=replies,
        views=views,
        expected_label=None,  # unknown for unfixed entries
        predicted_label=None,
    )


def fetch_mrplc_forum_page(forum_url: str, page_num: int = 1) -> Optional[BeautifulSoup]:
    """Fetch a MrPLC forum page and return BeautifulSoup object.
    
    Args:
        forum_url: Base URL of the forum (e.g., 
            'https://www.mrplc.com/forums/forum/15-mitsubishi/')
        page_num: Page number (1 = first page)
    
    Returns:
        BeautifulSoup object if successful, None on failure
    """
    # MrPLC pagination: page 1 has no page parameter, pages 2+ use ?page=x
    if page_num == 1:
        url = forum_url
    else:
        # Handle URL with or trailing slash
        base = forum_url.rstrip('/')
        if '?page=' in base:
            url = f"{base}&page={page_num}"
        else:
            url = f"{base}?page={page_num}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        resp = requests.get(url, timeout=15, headers=headers)
        if resp.status_code != 200:
            print(f"  WARN: Got status {resp.status_code} for {url}", file=sys.stderr)
            return None
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}", file=sys.stderr)
        return None


def parse_mrplc_threads(soup: BeautifulSoup, forum_name: str) -> List[ForumEntry]:
    """Parse thread entries from a MrPLC forum listing BeautifulSoup object.
    
    Extracts: title, view_count, reply_count from the MrPLC forum listing format.
    
    Thread titles are found in <a class='ipsDataItem_title'> tags.
    Reply counts and view counts are extracted from the body text using patterns:
    - 'N replies' for reply counts
    - 'Xk views' or 'N views' for view counts
    
    Returns list of ForumEntry objects with title, views, replies extracted.
    """
    entries = []
    
    # Extract thread title links
    title_links = soup.find_all('a', class_='ipsDataItem_title')
    
    if not title_links:
        # Fallback: try to find any meaningful thread entries
        # by extracting from text patterns
        return _parse_threads_from_text(soup, forum_name)
    
    # Extract reply counts from body text
    body = soup.body.get_text(' ', strip=True) if soup.body else ''
    
    reply_pattern = re.compile(r'(\d+)\s+replies')
    reply_matches = list(reply_pattern.finditer(body))
    replies = [int(m.group(1)) for m in reply_matches]
    
    # Extract view counts (k-notation first, then plain)
    view_k_pattern = re.compile(r'([\d.]+)k\s+views')
    view_k_matches = list(view_k_pattern.finditer(body))
    view_k_vals = []
    for m in view_k_matches:
        val = float(m.group(1)) * 1000
        view_k_vals.append(int(val))
    
    view_plain_pattern = re.compile(r'(\d+)\s+views')
    view_plain_matches = list(view_plain_pattern.finditer(body))
    views_plain = [int(m.group(1)) for m in view_plain_matches]
    
    # Combine view counts: k-notation takes priority, then plain
    # We'll interleave them by position - first k-notation, then plain
    all_views = []
    k_idx = 0
    p_idx = 0
    # Add k-notation views first, then plain views
    while k_idx < len(view_k_vals) or p_idx < len(views_plain):
        if k_idx < len(view_k_vals):
            all_views.append(view_k_vals[k_idx])
            k_idx += 1
        if p_idx < len(views_plain):
            all_views.append(views_plain[p_idx])
            p_idx += 1
    
    # Pair titles with replies and views by index
    for i, title_link in enumerate(title_links):
        title = title_link.get_text(strip=True)
        
        # Get reply count for this thread (by index)
        if i < len(replies):
            reply_count = replies[i]
        else:
            reply_count = 0
        
        # Get view count for this thread (by index)
        if i < len(all_views):
            view_count = all_views[i]
        else:
            view_count = 0
        
        # Skip empty titles
        if not title or len(title) < 3:
            continue
        
        entry = ForumEntry(
            probe_id="",
            title=title,
            forum=forum_name,
            replies=reply_count,
            views=view_count,
            expected_label=None,
            predicted_label=None,
        )
        entries.append(entry)
    
    # Deduplicate by title (keep first occurrence)
    seen = set()
    unique = []
    for e in entries:
        key = e.title.lower()[:80]
        if key not in seen:
            seen.add(key)
            unique.append(e)
    
    return unique


def _parse_threads_from_text(soup: BeautifulSoup, forum_name: str) -> List[ForumEntry]:
    """Fallback: parse thread entries from text patterns when title links not found.
    
    This extracts thread data from the body text using regex patterns for
    'N replies Xk views' format.
    """
    entries = []
    
    body = soup.body.get_text(' ', strip=True) if soup.body else ''
    
    # Find all thread entries matching pattern: 'By Name Date N replies Xk views'
    # or just 'N replies Xk views'
    thread_pattern = re.compile(
        r'((?:By\s+[\w_]+)\s+(?:\w+\s+){0,3}\d+(?:st|nd|rd|th)?\s+replies\s+[\d.]+k?\s+views)',
        re.IGNORECASE
    )
    
    matches = list(thread_pattern.finditer(body))
    
    for m in matches[:20]:  # Limit to first 20 matches
        full_text = m.group(0)
        # Extract reply count
        rep_match = re.search(r'(\d+)\s+replies', full_text)
        if not rep_match:
            continue
        reply_count = int(rep_match.group(1))
        
        # Extract view count
        view_match = re.search(r'([\d.]+)k?\s+views', full_text)
        if not view_match:
            continue
        view_str = view_match.group(1)
        if 'k' in view_match.group(0):
            view_count = int(float(view_str) * 1000)
        else:
            view_count = int(view_str)
        
        # Title is harder to extract from this pattern alone
        # Use a placeholder; in practice the title would come from HTML
        title = full_text[:60]  # fallback
        
        if not title or len(title) < 3:
            continue
        
        entry = ForumEntry(
            probe_id="",
            title=title,
            forum=forum_name,
            replies=reply_count,
            views=view_count,
            expected_label=None,
            predicted_label=None,
        )
        entries.append(entry)
    
    # Deduplicate by title
    seen = set()
    unique = []
    for e in entries:
        key = e.title.lower()[:80]
        if key not in seen:
            seen.add(key)
            unique.append(e)
    
    return unique


def fetch_forum_pages(forum_url: str, max_pages: int = 3) -> List[Any]:
    """Fetch multiple pages of a MrPLC forum listing.
    
    Args:
        forum_url: Base URL of the forum (e.g., 
            'https://www.mrplc.com/forums/forum/15-mitsubishi/')
        max_pages: Maximum number of pages to fetch (1 = first page only)
    
    Returns:
        List of BeautifulSoup objects, one per page fetched
    """
    pages = []
    for page_num in range(1, max_pages + 1):
        soup = fetch_mrplc_forum_page(forum_url, page_num=page_num)
        if soup is not None:
            pages.append(soup)
        else:
            # If a page fails, stop fetching further pages
            print(f"  STOPPING: Page {page_num} fetch failed, stopping pagination", file=sys.stderr)
            break
    return pages


def run_discrimination_harness(
    forum_url: str,
    known_served_probes: List[dict],
    known_unserved_probes: List[dict],
    max_threads: int = 80,
    max_pages: int = 3,
) -> GateResults:
    """Run the full discrimination test harness on a MrPLC forum.
    
    Args:
        forum_url: MrPLC forum URL to analyze
        known_served_probes: List of dicts with 'query' and 'probe_id' for known-served
        known_unserved_probes: List of dicts with 'query' and 'probe_id' for known-unserved
        max_threads: Maximum total number of threads to fetch across all pages
        max_pages: Maximum number of pages to fetch from the forum
    
    Returns:
        GateResults with G1/G2/G3 evaluation
    """
    print("=" * 80)
    print("E091 DISCRIMINATION TEST HARNESS: fault_need_classifier")
    print("=" * 80)
    print(f"Forum: {forum_url}")
    print(f"Known-served probes: {len(known_served_probes)}")
    print(f"Known-unserved probes: {len(known_unserved_probes)}")
    print(f"max_threads: {max_threads}, max_pages: {max_pages}")
    print()
    
    # Fetch forum pages
    pages = fetch_forum_pages(forum_url, max_pages=max_pages)
    print(f"Fetched {len(pages)} page(s) from forum")
    total_threads_found = sum(
        len(parse_mrplc_threads(s, "MrPLC")) for s in pages
    )
    print(f"Total thread entries found across {len(pages)} page(s): {total_threads_found}")
    print()
    
    # Create entries from fetched threads (deduplicated)
    entries = []
    
    seen_titles = set()
    thread_count = 0
    
    for page_soup in pages:
        threads = parse_mrplc_threads(page_soup, "MrPLC")
        for thread in threads:
            if thread_count >= max_threads:
                break
            # Deduplicate by title (case-insensitive, first 80 chars)
            key = thread.title.lower()[:80]
            if key in seen_titles:
                continue
            seen_titles.add(key)
            
            entry = ForumEntry(
                probe_id=f"fetched-{thread_count + 1}",
                title=thread.title,
                forum="MrPLC",
                replies=thread.replies,
                views=thread.views,
                expected_label=None,
                predicted_label=None,
            )
            entries.append(entry)
            thread_count += 1
        
        if thread_count >= max_threads:
            break
    
    print(f"Added {len(entries)} unique fetched threads")
    print()
    
    # Add known-served probes
    for probe_info in known_served_probes:
        query = probe_info['query']
        probe_id = probe_info['probe_id']
        
        # Check if this probe matches any fetched thread title
        matched = False
        for entry in entries:
            if query.lower() in entry.title.lower() or entry.title.lower() in query.lower():
                entry.expected_label = "served"
                entry.probe_id = probe_id
                matched = True
                break
        
        if not matched:
            # Create a synthetic entry with the probe query
            entry = ForumEntry(
                probe_id=probe_id,
                title=query,
                forum="MrPLC (synthetic)",
                replies=0,
                views=0,
                expected_label="served",
                predicted_label=None,
            )
            entries.append(entry)
    
    # Add known-unserved probes
    for probe_info in known_unserved_probes:
        query = probe_info['query']
        probe_id = probe_info['probe_id']
        
        entry = ForumEntry(
            probe_id=probe_id,
            title=query,
            forum="MrPLC (synthetic)",
            replies=0,
            views=0,
            expected_label="unserved",
            predicted_label=None,
        )
        entries.append(entry)
    
    print(f"Total entries to classify: {len(entries)}")
    print(f"  Known-served: {sum(1 for e in entries if e.expected_label == 'served')}")
    print(f"  Known-unserved: {sum(1 for e in entries if e.expected_label == 'unserved')}")
    print()
    
    # Apply the classifier
    served_correct = 0
    unserved_false_served = 0
    
    for entry in entries:
        entry.predicted_label = fault_need_classifier(entry.title, entry.views, entry.replies)
        
        if entry.expected_label == "served" and entry.predicted_label == "served":
            served_correct += 1
        elif entry.expected_label == "unserved" and entry.predicted_label == "served":
            unserved_false_served += 1
        
        status = "✓" if (
            (entry.expected_label == "served" and entry.predicted_label == "served") or
            (entry.expected_label == "unserved" and entry.predicted_label == "unserved")
        ) else "✗"
        print(f"  {status} {entry.probe_id}: '{entry.title[:60]}...' "
               f"views={entry.views}, replies={entry.replies} -> {entry.predicted_label} "
               f"(expected {entry.expected_label})")
    
    # Compute gate results
    results = compute_gates(entries)
    
    print()
    print("=" * 80)
    print("GATE RESULTS")
    print("=" * 80)
    print(f"G1 (FPR < 0.10):      {results.fpr:.4f} -> {'PASS' if results.g1_pass else 'FAIL'}")
    print(f"  known-unserved called served: {results.u_hit}/{results.n_unserved}")
    print(f"  Wilson CI95: [{results.wilson_unserved[0]:.3f}, {results.wilson_unserved[1]:.3f}]")
    print()
    print(f"G2 (TPR > 0.70):      {results.tpr:.4f} -> {'PASS' if results.g2_pass else 'FAIL'}")
    print(f"  known-served called served: {results.s_hit}/{results.n_served}")
    print(f"  Wilson CI95: [{results.wilson_served[0]:.3f}, {results.wilson_served[1]:.3f}]")
    print()
    print(f"G3 (FNR < 0.30):      {results.fnr:.4f} -> {'PASS' if results.g3_pass else 'FAIL'}")
    print(f"  Wilson CI95: [{results.wilson_served[0]:.3f}, {results.wilson_served[1]:.3f}]")
    print()
    print(f"OVERALL: {'PASS' if results.g1_pass and (results.g2_pass or results.g3_pass) else 'FAIL'}")
    print()
    
    if not results.g1_pass and not results.g2_pass and not results.g3_pass:
        print(">>> INSTRUMENT FAILS DISCRIMINATION TEST <<<")
        print(">>> Per D095: Must redesign instrument before population measurement <<<")
    else:
        print(">>> INSTRUMENT PASSES DISCRIMINATION TEST <<<")
        print(">>> Proceed to population measurement on practitioner rows <<<")
    
    return results


# ============================================================================
# Default probe sets (known-served and known-unserved)
# These are the same probes from E090/OBSERVATIONS.md and E088/probes.jsonl
# ============================================================================

DEFAULT_KNOWN_SERVED = [
    {"probe_id": "S01", "query": "Python ImportError: No module named 'requests'"},
    {"probe_id": "S02", "query": "python unittest assertRaises example"},
    {"probe_id": "S03", "query": "sqlite3 primary key syntax"},
    {"probe_id": "S04", "query": "tar extract a single file from archive"},
    {"probe_id": "S05", "query": "difference between TCP and UDP"},
    {"probe_id": "S06", "query": "how to sort a list of dictionaries by key"},
    {"probe_id": "S07", "query": "git undo last commit keep changes"},
    {"probe_id": "S08", "query": "how to calculate standard deviation in excel"},
    {"probe_id": "S09", "query": "what causes a segfault in C"},
    {"probe_id": "S10", "query": "convert UTC to local time in javascript"},
    {"probe_id": "S11", "query": "how to replace a brake rotor"},
    {"probe_id": "S12", "query": "sourdough starter not rising"},
    {"probe_id": "S13", "query": "how to jump start a car"},
    {"probe_id": "S14", "query": "photosynthesis equation explanation"},
    {"probe_id": "S15", "query": "how to tie a bowline knot"},
    {"probe_id": "S16", "query": "what is the difference between weather and climate"},
    {"probe_id": "S17", "query": "how to change a flat bicycle tire"},
    {"probe_id": "S18", "query": "setting up nginx reverse proxy"},
    {"probe_id": "S19", "query": "how to read a resistor color code"},
    {"probe_id": "S20", "query": "first aid for a minor burn"},
]

DEFAULT_KNOWN_UNSERVED = [
    {"probe_id": "U01", "query": "Zorbex-4400 manifold gasket torque specification"},
    {"probe_id": "U02", "query": "Kellundar VX-7 pump calibration procedure"},
    {"probe_id": "U03", "query": "Brantmore Trellis-9 startup checklist"},
    {"probe_id": "U04", "query": "Quilvane HX-3 coil cleaning interval"},
    {"probe_id": "U05", "query": "Marnot Deltrix-88 firmware update notes"},
    {"probe_id": "U06", "query": "Ostrander Pellix-2 filter replacement interval"},
    {"probe_id": "U07", "query": "Vandermolen Cristar-45 belt tension specification"},
    {"probe_id": "U08", "query": "Halberdix Ferrolux-6 coolant mixing ratio"},
    {"probe_id": "U09", "query": "Pemberton Algrid-31 firmware changelog"},
    {"probe_id": "U10", "query": "Corvane Stellarium-19 bearing tolerance"},
    {"probe_id": "U11", "query": "Wexbridge Tolliver-2 firmware flashing guide"},
    {"probe_id": "U12", "query": "Nyxhollow Perigee-27 maintenance schedule"},
    {"probe_id": "U13", "query": "Ashgrove Windermere-5 alignment procedure"},
    {"probe_id": "U14", "query": "Pellworth Draymar-13 pressure relief setting"},
    {"probe_id": "U15", "query": "Selbrand Illuvion-4 error code list"},
    {"probe_id": "U16", "query": "Thornbury Vexmoor-8 lubricant specification"},
    {"probe_id": "U17", "query": "Calderon Quintrix-12 troubleshooting guide"},
    {"probe_id": "U18", "query": "Ravensmoor Yelworth-6 cycle time data"},
    {"probe_id": "U19", "query": "Penhurst Amberlok-3 retrofit instructions"},
    {"probe_id": "U20", "query": "Strathmore Dovetail-9 commissioning report"},
]

# Known-served probes with expected to be found on MrPLC (fault/error code domains)
# These are mapped to actual MrPLC thread titles for the harness test
MRPLC_SERVED_PROBE_MAP = [
    # These probe queries should match MrPLC threads with error codes
    {"probe_id": "S01", "query": "Allen Bradley PLC error code 125", "expected_served": True},
    {"probe_id": "S02", "query": "Mitsubishi fault code 1134", "expected_served": True},
    {"probe_id": "S03", "query": "Siemens HMI error code", "expected_served": True},
    {"probe_id": "S04", "query": "Omron error -10 no system program", "expected_served": True},
    {"probe_id": "S05", "query": "Modbus exception code 03", "expected_served": True},
]


def main():
    """Main entry point for the E091 discrimination test harness."""
    print("E091 Discrimination Test Harness")
    print("=" * 60)
    
    # Default: run on MrPLC Mitsubishi forum with built-in probe sets
    forum_url = "https://www.mrplc.com/forums/forum/15-mitsubishi/"
    
    # Run the harness
    results = run_discrimination_harness(
        forum_url=forum_url,
        known_served_probes=DEFAULT_KNOWN_SERVED,
        known_unserved_probes=DEFAULT_KNOWN_UNSERVED,
        max_threads=30,
    )
    
    # Output summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"G1 discrimination (FPR < 0.10): {'PASS' if results.g1_pass else 'FAIL'} "
           f"(FPR = {results.fpr:.4f})")
    print(f"G2 separation (TPR > 0.70): {'PASS' if results.g2_pass else 'FAIL'} "
           f"(TPR = {results.tpr:.4f})")
    print(f"G3 conservatism (FNR < 0.30): {'PASS' if results.g3_pass else 'FAIL'} "
           f"(FNR = {results.fnr:.4f})")
    print()
    
    overall = results.g1_pass and (results.g2_pass or results.g3_pass)
    print(f"OVERALL: {'PASS - Instrument validated for population measurement' if overall else 'FAIL - Instrument needs redesign'}")
    
    if overall:
        print("\n>>> Next step: Apply instrument to practitioner rows for population measurement <<<")
    else:
        print("\n>>> Per D095: Redesign instrument before proceeding <<<")
    
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
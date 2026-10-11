#!/usr/bin/env python3
"""
E091 Discrimination Test — listing parsers: BeautifulSoup -> ForumEntry.

Split out of `091-discrimination-harness.py` at the 300-line cap, with the
network half in `091-mrplc-fetch.py`. This half touches no network: it takes a
parsed page and returns entries, which is what makes it the part a
discrimination test can exercise offline.

Listing format observed on MrPLC (Invision Community): thread titles in
<a class='ipsDataItem_title'>, with "N replies" and "Xk views" / "N views"
elsewhere in the listing body, paired to titles by position.
"""

import re
from typing import List, Optional

from bs4 import BeautifulSoup
from importlib.util import module_from_spec, spec_from_file_location

# The sibling module's name starts with a digit and carries a hyphen, so it is
# not importable by name; load it by path. spec_from_file_location rather than
# SourceFileLoader.load_module, which was removed in CPython 3.12.
_INSTRUMENT_SPEC = spec_from_file_location(
    "discrimination_instrument",
    __file__.rsplit("/", 1)[0] + "/091-discrimination-instrument.py",
)
_INSTRUMENT = module_from_spec(_INSTRUMENT_SPEC)
_INSTRUMENT_SPEC.loader.exec_module(_INSTRUMENT)
ForumEntry = _INSTRUMENT.ForumEntry
has_specific_error_code = _INSTRUMENT.has_specific_error_code


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

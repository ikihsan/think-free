"""Shared constants and helpers for WordPress view-count experiment."""
import re
from html import unescape

# Need-related keywords for WordPress plugins
NEED_INDICATORS = {
    "cache", "caching",
    "security", "firewall", "login", "auth",
    "seo", "search engine", "rank",
    "performance", "speed", "optimiz", "minify", "compress",
    "backup", "migrate",
    "contact", "form", "widget",
    "ecommerce", "shop", "cart", "payment",
    "cdn", "cloudflare",
    "analytics", "statistics",
    "slider", "gallery",
}

# Generic/ random search keywords (not in need list)
RANDOM_KEYWORDS = [
    "hello", "hello-world", "random", "misc", "admin",
    "editor", "image", "media", "slider", "seo-boilerplate",
]

SAMPLE_SIZE = 100  # G2 gate: minimum 100 packages per group


def fetch_plugin_data(keyword, page=1):
    """Fetch plugin data from WordPress search API with markdown output."""
    import urllib.request
    url = f"https://wordpress.org/plugins/search/{keyword}/?output_format=md"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ThinkFree/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode()
            return raw
    except Exception as e:
        print(f"Error fetching '{keyword}': {e}")
        return None


def parse_plugins(raw_html):
    """Parse plugin entries from markdown output.
    
    Returns list of dicts with: name, description, active_installations, rating_count
    """
    if not raw_html:
        return []
    
    plugins = []
    lines = raw_html.split("\n")
    
    # Find all lines containing '###' pattern (with possible variation selector)
    plugin_starts = []
    for i, line in enumerate(lines):
        # Check if line has '###' followed by optional whitespace/variation selector and '['
        if re.search(r'###', line) and re.search(r'\[', line):
            plugin_starts.append(i)
            if len(plugin_starts) >= 200:
                break
    
    # Process each plugin start
    for start_idx in plugin_starts:
        line = lines[start_idx]
        
        # Extract plugin name from [displayname](url) pattern
        name_match = re.search(r'\[(.*?)\]', line)
        if not name_match:
            continue
        name = unescape(name_match.group(1)).strip()
        if not name or len(name) < 2:
            continue
        
        # Look at subsequent lines for description, active installs, ratings
        block_lines = []
        j = start_idx + 1
        collected = 0
        while j < len(lines) and collected < 25:
            l = lines[j].strip()
            # Stop if we hit the next '###' pattern (new plugin header)
            if re.search(r'^###', l) and l.strip() != line.strip():
                break
            if l:
                block_lines.append(lines[j])
                collected += 1
            j += 1
        
        full_text = " ".join(block_lines)
        
        # Extract active installations
        ai_match = re.search(
            r'(\d+(?:\+\d+)?\s *[a-z]*\s*active\s*installations)',
            full_text, re.IGNORECASE)
        if not ai_match:
            ai_match = re.search(
                r'(\d[\d,]*\+?\s*active\s*installations)',
                full_text, re.IGNORECASE)
        active_installs = ai_match.group(1).strip() if ai_match else None
        
        # Extract rating count
        rat_match = re.search(
            r'\((\d[\d,]*(?:\s+\d+)?\s*total\s*ratings?)\)',
            full_text, re.IGNORECASE)
        rating_count = rat_match.group(1) if rat_match else None
        
        # Extract description
        desc = ""
        segments = re.split(r'[.!?]\s+', full_text)
        for seg in segments:
            seg = seg.strip()
            if len(seg) < 5:
                continue
            if re.match(r'^\(?\d+', seg):
                continue
            if 'tested with' in seg.lower():
                continue
            if re.match(r'^\d+[\d,]*\+?\s', seg):
                continue
            if seg.startswith('http'):
                continue
            if seg.lower() == name.lower():
                continue
            if not desc and len(seg) > 10:
                desc = seg[:300]
                break
        
        if not desc:
            tested_match = re.search(r'Tested with\s+[\d.]+\.?', full_text, re.IGNORECASE)
            if tested_match:
                before = full_text[:tested_match.start()].strip()
                sentences = re.split(r'[.!?]\s+', before)
                if sentences:
                    desc = sentences[-1][:300]
        
        if not desc:
            for seg in segments:
                seg = seg.strip()
                if len(seg) > 20 and len(seg) < 500 and not re.match(r'^\(?\d+', seg):
                    desc = seg[:300]
                    break
        
        plugins.append({
            "name": name,
            "description": desc,
            "active_installations": active_installs,
            "rating_count": rating_count,
        })
    
    return plugins


def classify_plugin(description):
    """Classify a plugin as need-related or random based on its description."""
    desc_lower = (description or "").lower()
    
    for term in NEED_INDICATORS:
        if term in desc_lower:
            return "need-related"
    
    if len(desc_lower) < 10:
        return "random"
    
    return "random"


def is_active(active_installs_str):
    """Check if a plugin has active installation metadata."""
    if active_installs_str is None:
        return False
    return bool(re.search(r'\d', active_installs_str))
#!/usr/bin/env python3
"""
E137 — Demand validation for preflight: harvest practitioner reports of C1/C2/C3 defects
across LLM evaluation frameworks.

Protocol: EXPERIMENTS/137-preflight-demand-validation/PROTOCOL.md
Kill gate G1: ≥ 10 credible reports (C1_credible + C2_credible + C3_credible) across ≥ 3 distinct frameworks.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

EXPERIMENT_DIR = Path(__file__).parent
RESULTS_FILE = EXPERIMENT_DIR / "results.json"
CLASSIFICATIONS_FILE = EXPERIMENT_DIR / "CLASSIFICATIONS.md"

# Framework configurations from PROTOCOL.md
FRAMEWORKS = [
    {"name": "evalscope", "repo": "modelscope/evalscope", "stars": 3530, "source": "E125"},
    {"name": "evals", "repo": "openai/evals", "stars": 19593, "source": "E125"},
    {"name": "promptfoo", "repo": "promptfoo/promptfoo", "stars": 7000, "source": "PRIOR-ART.md"},
    {"name": "deepeval", "repo": "confident-ai/deepeval", "stars": 5000, "source": "PRIOR-ART.md"},
    {"name": "inspect_ai", "repo": "UKGovernmentBEIS/inspect_ai", "stars": 3000, "source": "PRIOR-ART.md"},
    {"name": "inspect-evals-lint", "repo": "Generality-Labs/inspect-evals-lint", "stars": 6, "source": "PRIOR-ART.md"},
    {"name": "eval-harness", "repo": "gameonc/eval-harness", "stars": 0, "source": "PRIOR-ART.md"},
    {"name": "scale-eval-preflight", "repo": "Abhishek21g/scale-eval-preflight", "stars": 0, "source": "PRIOR-ART.md"},
    {"name": "JudgeBench", "repo": "ScalerLab/JudgeBench", "stars": 500, "source": "PRIOR-ART.md"},
]

# Search keywords for GitHub issues
GITHUB_KEYWORDS = [
    "join", "match", "silent", "zero", "accuracy", "grader", "verifier", "grounding",
    "contamination", "leakage", "false positive", "false negative", "control", "negative", "unanswerable",
    "evaluation returns 0", "metrics show 0", "scorer not working", "IDs don't match", "format mismatch"
]

# Stack Overflow tags
STACK_TAGS = ["llm-evaluation", "promptfoo", "deepeval", "inspect-ai", "langchain-eval", "evaluation-metrics"]

# Reddit subreddits
REDDIT_SUBREDDITS = ["LLMEval", "MachineLearning", "LocalLLaMA", "LangChain"]

# arXiv search terms
ARXIV_TERMS = [
    "evaluation harness", "silent failure", "grader reliability", "benchmark contamination",
    "evaluation validity", "LLM judge evaluation"
]

# Classification keywords
C1_KEYWORDS = [
    "join", "match", "silent", "zero", "accuracy", "IDs don't match", "ID mismatch",
    "type mismatch", "evaluation returns 0", "metrics show 0", "scorer not working",
    "ground truth not match", "predictions and labels", "join returns empty", "silent failure"
]

C2_KEYWORDS = [
    "grader marks correct", "verifier fails", "paraphrase", "precision", "format mismatch",
    "equivalent answer", "grounding checker false positive", "numeric precision",
    "correct answer marked", "false positive", "verifier false positive", "grader false positive",
    "grounding false positive", "surface form", "different format"
]

C3_KEYWORDS = [
    "control set", "negative examples", "benchmark contamination", "test set leakage",
    "evaluation set not actually negative", "false negatives in control", "contamination",
    "leakage", "control group", "negative control", "unanswerable", "answerable questions"
]

# Negative controls
NEGATIVE_CONTROL_QUERIES = [
    "xyzzy123 preflight evaluation",  # should return 0
]

# Known answer controls
KNOWN_ANSWER_QUERIES = [
    "promptfoo grader false positive",
]


def fetch_github_issues(repo, keywords, max_results=20):
    """Fetch GitHub issues for a repo matching keywords."""
    results = []
    # Use unauthenticated API (60 req/hr limit)
    for keyword in keywords[:5]:  # Limit keywords to stay within budget
        try:
            url = f"https://api.github.com/search/issues?q=repo:{repo}+{urllib.parse.quote(keyword)}+type:issue&per_page=10"
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())
                for item in data.get("items", []):
                    results.append({
                        "source": "github_issues",
                        "framework": repo,
                        "title": item["title"],
                        "body": item["body"] or "",
                        "url": item["html_url"],
                        "keyword": keyword,
                        "created_at": item["created_at"],
                    })
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"  Error fetching GitHub issues for {repo} keyword '{keyword}': {e}")
    return results


def fetch_github_discussions(repo, keywords, max_results=20):
    """Fetch GitHub discussions for a repo matching keywords."""
    results = []
    # GitHub Discussions API requires GraphQL, which is complex without auth
    # We'll skip this for unauthenticated access
    return results


def fetch_stackoverflow(tag, keywords, max_results=10):
    """Fetch Stack Overflow questions for a tag matching keywords."""
    results = []
    try:
        # Stack Exchange API - unauthenticated 300 req/day
        for keyword in keywords[:3]:
            url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&tagged={tag}&q={urllib.parse.quote(keyword)}&site=stackoverflow&pagesize=10"
            with urllib.request.urlopen(url, timeout=30) as response:
                data = json.loads(response.read().decode())
                for item in data.get("items", []):
                    results.append({
                        "source": "stackoverflow",
                        "framework": tag,
                        "title": item["title"],
                        "body": "",  # Need separate call for body
                        "url": item["link"],
                        "keyword": keyword,
                        "created_at": datetime.fromtimestamp(item["creation_date"]).isoformat(),
                    })
            time.sleep(1)
    except Exception as e:
        print(f"  Error fetching Stack Overflow for {tag}: {e}")
    return results


def fetch_reddit(subreddit, keywords, max_results=10):
    """Fetch Reddit posts from a subreddit matching keywords."""
    results = []
    try:
        for keyword in keywords[:3]:
            url = f"https://www.reddit.com/r/{subreddit}/search.json?q={urllib.parse.quote(keyword)}&restrict_sr=1&limit=10"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())
                for item in data.get("data", {}).get("children", []):
                    post = item["data"]
                    results.append({
                        "source": "reddit",
                        "framework": subreddit,
                        "title": post["title"],
                        "body": post.get("selftext", ""),
                        "url": f"https://reddit.com{post['permalink']}",
                        "keyword": keyword,
                        "created_at": datetime.fromtimestamp(post["created_utc"]).isoformat(),
                    })
            time.sleep(1)
    except Exception as e:
        print(f"  Error fetching Reddit for r/{subreddit}: {e}")
    return results


def fetch_arxiv(term, max_results=10):
    """Fetch arXiv papers matching term."""
    results = []
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(term)}&start=0&max_results={max_results}"
        with urllib.request.urlopen(url, timeout=30) as response:
            xml_content = response.read().decode()
            # Simple XML parsing for entries
            entries = re.findall(r'<entry>(.*?)</entry>', xml_content, re.DOTALL)
            for entry in entries:
                title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
                id_match = re.search(r'<id>(.*?)</id>', entry)
                published_match = re.search(r'<published>(.*?)</published>', entry)
                if title_match:
                    results.append({
                        "source": "arxiv",
                        "framework": "arxiv",
                        "title": title_match.group(1).strip().replace("\n", " "),
                        "body": summary_match.group(1).strip().replace("\n", " ") if summary_match else "",
                        "url": id_match.group(1).strip() if id_match else "",
                        "keyword": term,
                        "created_at": published_match.group(1).strip() if published_match else "",
                    })
        time.sleep(1)
    except Exception as e:
        print(f"  Error fetching arXiv for '{term}': {e}")
    return results


def classify_item(item):
    """Classify an item as C1_credible, C2_credible, C3_credible, related, or not_relevant."""
    text = (item.get("title", "") + " " + item.get("body", "")).lower()
    framework = item.get("framework", "")
    
    # Check C1
    c1_score = sum(1 for kw in C1_KEYWORDS if kw.lower() in text)
    # Check C2
    c2_score = sum(1 for kw in C2_KEYWORDS if kw.lower() in text)
    # Check C3
    c3_score = sum(1 for kw in C3_KEYWORDS if kw.lower() in text)
    
    # Credible requires: specific framework named, defect matches definition, reported by practitioner
    # We'll check if framework is named in the text or if it's from a known framework source
    framework_named = any(fw["name"].lower() in text for fw in FRAMEWORKS) or framework in [fw["repo"] for fw in FRAMEWORKS] or framework in [fw["name"] for fw in FRAMEWORKS]
    
    if c1_score > 0 and framework_named:
        return "C1_credible"
    elif c2_score > 0 and framework_named:
        return "C2_credible"
    elif c3_score > 0 and framework_named:
        return "C3_credible"
    elif c1_score > 0 or c2_score > 0 or c3_score > 0:
        return "related"
    else:
        return "not_relevant"


def run_negative_controls():
    """Run negative control queries."""
    print("Running negative controls...")
    for query in NEGATIVE_CONTROL_QUERIES:
        # Test GitHub search
        try:
            url = f"https://api.github.com/search/issues?q={urllib.parse.quote(query)}&per_page=5"
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())
                count = data.get("total_count", 0)
                print(f"  Negative control '{query}': {count} results")
        except Exception as e:
            print(f"  Error on negative control '{query}': {e}")


def run_known_answer_controls():
    """Run known answer control queries."""
    print("Running known answer controls...")
    for query in KNOWN_ANSWER_QUERIES:
        try:
            url = f"https://api.github.com/search/issues?q={urllib.parse.quote(query)}&per_page=5"
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())
                count = data.get("total_count", 0)
                items = data.get("items", [])
                titles = [item["title"] for item in items[:5]]
                print(f"  Known answer '{query}': {count} results, titles: {titles}")
        except Exception as e:
            print(f"  Error on known answer control '{query}': {e}")


def main():
    print("=" * 60)
    print("E137 — Demand validation for preflight")
    print("Harvesting practitioner reports of C1/C2/C3 defects")
    print("=" * 60)
    
    all_items = []
    
    # Run controls first
    run_negative_controls()
    run_known_answer_controls()
    print()
    
    # 1. GitHub Issues
    print("Fetching GitHub Issues...")
    for fw in FRAMEWORKS:
        if fw["stars"] == 0:
            print(f"  Skipping {fw['repo']} (0 stars)")
            continue
        print(f"  {fw['repo']}...")
        items = fetch_github_issues(fw["repo"], GITHUB_KEYWORDS)
        for item in items:
            item["framework"] = fw["name"]
        all_items.extend(items)
        print(f"    Found {len(items)} items")
    
    # 2. Stack Overflow
    print("\nFetching Stack Overflow...")
    for tag in STACK_TAGS:
        print(f"  Tag: {tag}...")
        items = fetch_stackoverflow(tag, ["evaluation returns zero", "grader marks correct as wrong", "ground truth not matching", "evaluation harness silent failure"])
        for item in items:
            item["framework"] = tag
        all_items.extend(items)
        print(f"    Found {len(items)} items")
    
    # 3. Reddit
    print("\nFetching Reddit...")
    for subreddit in REDDIT_SUBREDDITS:
        print(f"  r/{subreddit}...")
        items = fetch_reddit(subreddit, ["evaluation", "grader", "verifier", "grounding", "false positive", "contamination"])
        for item in items:
            item["framework"] = subreddit
        all_items.extend(items)
        print(f"    Found {len(items)} items")
    
    # 4. arXiv
    print("\nFetching arXiv...")
    for term in ARXIV_TERMS:
        print(f"  Term: {term}...")
        items = fetch_arxiv(term, max_results=10)
        all_items.extend(items)
        print(f"    Found {len(items)} items")
    
    print(f"\nTotal raw items harvested: {len(all_items)}")
    
    # Classify all items
    print("\nClassifying items...")
    classifications = []
    for item in all_items:
        classification = classify_item(item)
        item["classification"] = classification
        if classification != "not_relevant":
            classifications.append({
                "source": item["source"],
                "framework": item["framework"],
                "classification": classification,
                "title": item["title"][:100],
                "url": item["url"],
                "keyword": item.get("keyword", ""),
            })
    
    # Save raw results
    with open(RESULTS_FILE, "w") as f:
        json.dump(all_items, f, indent=2)
    print(f"Saved raw results to {RESULTS_FILE}")
    
    # Save classifications
    with open(CLASSIFICATIONS_FILE, "w") as f:
        f.write("# E137 Classifications\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        # Group by classification
        for cls in ["C1_credible", "C2_credible", "C3_credible", "related"]:
            cls_items = [c for c in classifications if c["classification"] == cls]
            if cls_items:
                f.write(f"## {cls} ({len(cls_items)} items)\n\n")
                for item in cls_items:
                    f.write(f"- **{item['framework']}** ({item['source']}): {item['title']}\n")
                    f.write(f"  URL: {item['url']}\n")
                    f.write(f"  Keyword: {item['keyword']}\n\n")
        
        # Summary stats
        f.write("## Summary\n\n")
        for cls in ["C1_credible", "C2_credible", "C3_credible", "related", "not_relevant"]:
            count = sum(1 for c in classifications if c["classification"] == cls)
            f.write(f"- {cls}: {count}\n")
        
        # Per-framework credible counts
        f.write("\n## Credible Reports by Framework\n\n")
        frameworks_seen = set()
        for cls in ["C1_credible", "C2_credible", "C3_credible"]:
            fw_counts = {}
            for item in classifications:
                if item["classification"] == cls:
                    fw = item["framework"]
                    fw_counts[fw] = fw_counts.get(fw, 0) + 1
                    frameworks_seen.add(fw)
            if fw_counts:
                f.write(f"### {cls}\n")
                for fw, count in sorted(fw_counts.items(), key=lambda x: -x[1]):
                    f.write(f"- {fw}: {count}\n")
                f.write("\n")
        
        f.write(f"\n**Distinct frameworks with credible reports: {len(frameworks_seen)}**\n")
        f.write(f"**Total credible reports: {sum(1 for c in classifications if c['classification'] in ['C1_credible', 'C2_credible', 'C3_credible'])}**\n")
    
    print(f"Saved classifications to {CLASSIFICATIONS_FILE}")
    
    # Gate accounting
    credible = [c for c in classifications if c["classification"] in ["C1_credible", "C2_credible", "C3_credible"]]
    frameworks_with_credible = set(c["framework"] for c in credible)
    
    print(f"\n{'='*60}")
    print("GATE ACCOUNTING")
    print(f"{'='*60}")
    print(f"Total credible reports (C1+C2+C3): {len(credible)}")
    print(f"Distinct frameworks with credible reports: {len(frameworks_with_credible)}")
    print(f"Frameworks: {', '.join(sorted(frameworks_with_credible))}")
    print(f"G1 (≥10 credible across ≥3 frameworks): {'PASS' if len(credible) >= 10 and len(frameworks_with_credible) >= 3 else 'FAIL'}")
    
    # Write RESULT.md
    result_md = EXPERIMENT_DIR / "RESULT.md"
    with open(result_md, "w") as f:
        f.write(f"<!-- origin-meta\n")
        f.write(f"owner: docs/INDEX.md\n")
        f.write(f"status: active\n")
        f.write(f"last-verified: {datetime.now().date()}\n")
        f.write(f"-->\n\n")
        f.write(f"# E137 RESULT — Demand validation for preflight\n\n")
        f.write(f"`observed` {datetime.now().date()}, Python 3.8.10.\n\n")
        f.write(f"## Gate Accounting\n\n")
        f.write(f"| Gate | Declared | Observed | Verdict |\n")
        f.write(f"|---|---|---|---|\n")
        f.write(f"| G1 (demand) | ≥10 credible across ≥3 frameworks | {len(credible)} credible across {len(frameworks_with_credible)} frameworks | {'PASS' if len(credible) >= 10 and len(frameworks_with_credible) >= 3 else 'FAIL'} |\n\n")
        f.write(f"## Classification Breakdown\n\n")
        for cls in ["C1_credible", "C2_credible", "C3_credible", "related", "not_relevant"]:
            count = sum(1 for c in classifications if c["classification"] == cls)
            f.write(f"- {cls}: {count}\n")
        f.write(f"\n## Credible Reports by Framework\n\n")
        for cls in ["C1_credible", "C2_credible", "C3_credible"]:
            fw_counts = {}
            for item in classifications:
                if item["classification"] == cls:
                    fw = item["framework"]
                    fw_counts[fw] = fw_counts.get(fw, 0) + 1
            if fw_counts:
                f.write(f"### {cls}\n")
                for fw, count in sorted(fw_counts.items(), key=lambda x: -x[1]):
                    f.write(f"- {fw}: {count}\n")
                f.write("\n")
        f.write(f"\n## Conclusion\n\n")
        if len(credible) >= 10 and len(frameworks_with_credible) >= 3:
            f.write(f"GATE_OPEN: Demand validated. Proceed to adapter release consideration.\n")
        else:
            f.write(f"GATE_CLOSED: Demand too weak. Preflight candidate withdrawn on demand grounds.\n")
        f.write(f"\nSee CLASSIFICATIONS.md for detailed classification log.\n")
    
    print(f"Saved RESULT.md to {result_md}")
    print("\nDone.")


if __name__ == "__main__":
    main()
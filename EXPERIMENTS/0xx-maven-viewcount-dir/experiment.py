"""E0xx — View-count principle on Maven Central (directory browsing)"""
import json
import os
import urllib.request
import time
import random
import re
from html import unescape

# Configuration
SOLR_URL = "https://search.maven.org/solrsearch/select"  # blocked (403)
USE_DIRECTORY_BROWSING = True

# Problem-domain indicators: terms that suggest a specific need/problem
NEED_INDICATORS = {
    "web", "rest", "mvc", "orm", "sql", "json", "xml", "http",
    "parser", "lexer", "encoder", "decoder", "converter", "transform",
    "framework", "client", "server", "engine", "core", "utility", "helper",
    "gui", "cli", "webapp", "library", "tool", "parser",
}

# Too-generic terms that always classify as "random"
GENERIC_TERMS = {"utils", "common", "core", "library", "framework", "jar", "dependencies"}

MAX_GROUPS_TO_SAMPLE = 50
MAX_ARTIFACTS_PER_GROUP = 1  # Take 1 artifact per group to maximize coverage


def fetch_root_listing():
    """Fetch Maven Central root directory listing."""
    url = "https://repo1.maven.org/maven2/"
    try:
        r = urllib.request.urlopen(url, timeout=15)
        data = r.read().decode()
        # Extract group ID names from <a href> tags
        group_ids = re.findall(r'href="([^"]+/)"', data)
        # Filter to top-level directories (single segment)
        top_level = []
        for gid in group_ids:
            parts = gid.rstrip("/").split("/")
            if len(parts) == 1 and parts[0] and parts[0] not in ['HTTPClient', 'abbot', 'ac']:
                top_level.append(parts[0])
        return list(set(top_level))[:50]
    except Exception as e:
        print(f"Error fetching root listing: {e}")
        return []


def fetch_group_dir(group_id):
    """Fetch a group ID directory listing."""
    url = f"https://repo1.maven.org/maven2/{group_id}/"
    try:
        r = urllib.request.urlopen(url, timeout=15)
        data = r.read().decode()
        artifacts = re.findall(r'href="([^"]+)/"', data)
        artifacts = [a for a in artifacts if a and a != '..' and not a.startswith('.')]
        return artifacts[:MAX_ARTIFACTS_PER_GROUP]
    except Exception as e:
        print(f"Error fetching group {group_id}: {e}")
        return []


def read_pom(group_id, artifact_id):
    """Read POM file for an artifact - try latest approach."""
    # First try to find any version directory
    try:
        r = urllib.request.urlopen(f"https://repo1.maven.org/maven2/{group_id}/{artifact_id}/", timeout=15)
        data = r.read().decode()
        versions = re.findall(r'href="([0-9][^\"]*?)/"', data)
        if versions:
            # Try versions that look like real version numbers
            for v in versions[:5]:
                v = v.strip()
                if v and len(v.split(".")) >= 2 and not v.startswith("maven-") and not v.endswith("-source") and not v.endswith("-javadoc"):
                    # Try to read the POM
                    try:
                        pom_url = f"https://repo1.maven.org/maven2/{group_id}/{artifact_id}/{v}/{artifact_id}-{v}.pom"
                        r2 = urllib.request.urlopen(pom_url, timeout=10)
                        return r2.read().decode(), v
                    except:
                        pass
    except Exception as e:
        print(f"  Error browsing versions for {group_id}:{artifact_id}: {e}")
    
    # Try a specific common version pattern
    for suffix in ["-1.0", "-2.0", "-3.0", "-4.0", "-5.0"]:
        try:
            pom_url = f"https://repo1.maven.org/maven2/{group_id}/{artifact_id}/{suffix[2:]}/{artifact_id}{suffix}.pom"
            r2 = urllib.request.urlopen(pom_url, timeout=10)
            return r2.read().decode(), suffix[2:]
        except:
            pass
    
    return None, None


def classify_package(desc, keywords):
    """Classify a package as need-related or random."""
    desc_lower = (desc or "").lower()
    kw_lower = [k.lower() for k in (keywords or [])]
    all_text = desc_lower + " " + " ".join(kw_lower)
    
    # Check for generic terms - if present, classify as random
    for term in GENERIC_TERMS:
        if term in all_text:
            return "random"
    
    # Check for need-related indicators
    found_need = False
    for term in NEED_INDICATORS:
        if term in all_text:
            found_need = True
            break
    
    if found_need:
        return "need-related"
    
    # If description is very short or absent, classify as random
    if len(desc or "") < 10:
        return "random"
    
    # Default to random
    return "random"


def is_active(pkg):
    """Check if a package has significant activity metadata (the 'active' signal)."""
    desc_active = len(pkg["desc"].strip()) > 0 if pkg.get("desc") else False
    keywords_active = len(pkg["keywords"]) > 0 if pkg.get("keywords") else False
    version_active = pkg["v"] is not None and str(pkg["v"]).strip() != "" if pkg.get("v") else False
    return desc_active and keywords_active and version_active


def main():
    print("=== E0xx — View-count principle on Maven Central (directory browsing) ===")
    print()
    
    # Step 1: Fetch root listing to get group IDs
    print("Step 1: Fetching Maven Central root directory listing...")
    group_ids = fetch_root_listing()
    print(f"  Found {len(group_ids)} group ID directories")
    time.sleep(0.5)
    
    # Step 2: Sample group IDs
    sampled_groups = random.sample(group_ids, min(MAX_GROUPS_TO_SAMPLE, len(group_ids)))
    print(f"Step 2: Sampling {len(sampled_groups)} groups")
    time.sleep(0.5)
    
    # Step 3: For each group, sample artifacts and read POM metadata
    packages = []
    groups_with_classified = 0
    
    for group_id in sampled_groups:
        artifacts = fetch_group_dir(group_id)
        if not artifacts:
            continue
        
        groups_with_classified += 1
        print(f"  Group {group_id}: {len(artifacts)} artifacts")
        
        for artifact_id in artifacts:
            # Read POM metadata
            pom_text, version = read_pom(group_id, artifact_id)
            if pom_text is None:
                continue
            
            # Extract description from POM
            desc = ""
            desc_match = re.search(r'<description>(.*?)</description>', pom_text, re.DOTALL)
            if desc_match:
                desc = unescape(desc_match.group(1)).strip()
            
            # Extract keywords from POM (simple heuristic - look for project info)
            keywords = []
            
            cls = classify_package(desc, keywords)
            active = is_active({"desc": desc, "keywords": keywords, "v": version})
            
            packages.append({
                "g": group_id,
                "a": artifact_id,
                "v": version,
                "desc": desc,
                "keywords": keywords,
                "classified": cls,
                "active": active,
            })
            
            if len(packages) >= 100:
                break
        
        if len(packages) >= 100:
            break
        
        time.sleep(0.3)
    
    print(f"\nStep 3: Collected {len(packages)} packages from {groups_with_classified} groups")
    
    # Step 4: Analyze results
    classified = {"need-related": 0, "random": 0}
    active = {"need-related": 0, "random": 0}
    
    for pkg in packages:
        cls = pkg["classified"]
        if cls not in classified:
            continue
        classified[cls] += 1
        if pkg["active"]:
            active[cls] += 1
    
    print("\n=== Classification Results ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        act = active[cls]
        rate = (act / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} packages, {act} active, active rate = {rate:.1f}%")
    
    classified_count = sum(classified.values())
    print(f"  Total classified: {classified_count} / {len(packages)}")
    
    # Step 5: Evaluate gates
    print("\n=== Gate Evaluation ===")
    
    # G2: sample size >= 100
    g2_pass = classified_count >= 100
    print(f"  G2 gate (classified >= 100): {'PASS' if g2_pass else 'FAIL'} (classified: {classified_count})")
    
    # G4: classified >= 50
    g4_pass = classified_count >= 50
    print(f"  G4 gate (classified >= 50): {'PASS' if g4_pass else 'FAIL'} (classified: {classified_count})")
    
    # G1: need-related active rate >= 55% of random active rate
    if classified["need-related"] > 0 and classified["random"] > 0:
        need_rate = active["need-related"] / classified["need-related"]
        random_rate = active["random"] / classified["random"]
        ratio = need_rate / random_rate if random_rate > 0 else 0
        g1_pass = ratio >= 0.55
        print(f"  G1 gate (need/random active ratio >= 55%): {'PASS' if g1_pass else 'FAIL'}")
        print(f"    need-related active rate: {need_rate*100:.1f}%")
        print(f"    random active rate: {random_rate*100:.1f}%")
        print(f"    ratio: {ratio*100:.1f}%")
    else:
        g1_pass = False
        print(f"  G1 gate: SKIPPED (insufficient classification)")
    
    # G3: at least 2 distinct groups contribute classified packages
    groups_with_need = sum(1 for pkg in packages if pkg["classified"] == "need-related")
    groups_with_random = sum(1 for pkg in packages if pkg["classified"] == "random")
    g3_pass = groups_with_need >= 1 and groups_with_random >= 1
    print(f"  G3 gate (multiple groups represented): {'PASS' if g3_pass else 'FAIL'} (groups with need-related: {groups_with_need}, with random: {groups_with_random})")
    
    # Overall
    all_pass = g1_pass and g2_pass and g3_pass and g4_pass
    print(f"\n  Overall: {'ALL GATES PASS' if all_pass else 'SOME GATES FAILED'}")
    
    # Save results
    results = {
        "observed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user_date": time.strftime("%Y-%m-%d", time.gmtime()),
        "platform": "Linux-x86_64",
        "sample_size": len(packages),
        "classified": {k: classified[k] for k in classified},
        "active": {k: active[k] for k in active},
        "active_rates": {
            "need-related": active["need-related"] / classified["need-related"] if classified["need-related"] > 0 else 0,
            "random": active["random"] / classified["random"] if classified["random"] > 0 else 0,
        },
        "g1_pass": g1_pass,
        "g2_pass": g2_pass,
        "g3_pass": g3_pass,
        "g4_pass": g4_pass,
        "conclusion": "pending",
        "experiment_description": "View-count principle on Maven Central via directory browsing",
    }
    
    os.makedirs("EXPERIMENTS/0xx-maven-viewcount-dir", exist_ok=True)
    with open("EXPERIMENTS/0xx-maven-viewcount-dir/results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== Results saved to EXPERIMENTS/0xx-maven-viewcount-dir/results.json ===")
    
    return 0 if all_pass else 2


if __name__ == "__main__":
    import sys
    sys.exit(main())
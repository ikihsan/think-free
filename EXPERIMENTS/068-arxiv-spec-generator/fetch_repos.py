#!/usr/bin/env python3
"""
Fetch repository contents for E068 spec generator experiment.
Shallow clones the 25 test repos from E067 assessment (non-A1 arms).
"""

import json
import subprocess
import os
import sys
from pathlib import Path

# Load E067 assessment to get repo list
ASSESSMENT_PATH = Path("/home/ubuntu/think-free/EXPERIMENTS/067-arxiv-code-repro/raw/assessment.json")
REPOS_DIR = Path("/home/ubuntu/think-free/EXPERIMENTS/068-arxiv-spec-generator/repos")
CACHE_DIR = Path("/home/ubuntu/think-free/EXPERIMENTS/068-arxiv-spec-generator/cache")

def load_assessment():
    with open(ASSESSMENT_PATH) as f:
        return json.load(f)

def get_test_repos(assessment):
    """Get repos from A2, A3, and fetchable A4 arms."""
    test_repos = []
    a1_repos = []
    
    for paper in assessment['results']:
        for repo in paper['repos']:
            repo_info = {
                'owner': repo['owner'],
                'repo': repo['repo'],
                'url': repo['url'],
                'arm': repo['arm'],
                'env_type': repo['env_type'],
                'pinned_score': repo['pinned_score'],
                'files': repo['files'],
                'details': repo.get('details', {})
            }
            if repo['arm'] == 'A1':
                a1_repos.append(repo_info)
            elif repo['arm'] == 'A4' and repo['details'].get('error') == 'no tree':
                print(f"Skipping {repo['owner']}/{repo['repo']} - no tree error")
                continue
            else:
                test_repos.append(repo_info)
    
    return a1_repos, test_repos

def shallow_clone(repo_info, target_dir):
    """Shallow clone a single repo."""
    url = repo_info['url']
    # Convert GitLab URLs if needed
    if 'gitlab.com' in url:
        # GitLab uses different clone URL format
        url = url.replace('gitlab.com/', 'gitlab.com/')
    
    try:
        # Use --depth=1 for shallow clone, --no-tags, single branch
        result = subprocess.run(
            ['git', 'clone', '--depth=1', '--no-tags', '--single-branch', url, str(target_dir)],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            return True
        else:
            print(f"  Clone failed: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  Clone timeout")
        return False
    except Exception as e:
        print(f"  Clone error: {e}")
        return False

def main():
    REPOS_DIR.mkdir(exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)
    
    assessment = load_assessment()
    a1_repos, test_repos = get_test_repos(assessment)
    
    print(f"A1 repos (ground truth): {len(a1_repos)}")
    for r in a1_repos:
        print(f"  {r['owner']}/{r['repo']} ({r['env_type']})")
    
    print(f"\nTest repos (A2/A3/A4 fetchable): {len(test_repos)}")
    for r in test_repos:
        print(f"  {r['owner']}/{r['repo']} ({r['arm']}, {r['env_type']})")
    
    # Clone A1 repos
    print("\n=== Cloning A1 repos (ground truth) ===")
    a1_dir = REPOS_DIR / "A1"
    a1_dir.mkdir(exist_ok=True)
    for repo in a1_repos:
        target = a1_dir / f"{repo['owner']}_{repo['repo']}"
        if target.exists():
            print(f"  {repo['owner']}/{repo['repo']} - already exists")
            continue
        print(f"  Cloning {repo['owner']}/{repo['repo']}...", end=" ")
        success = shallow_clone(repo, target)
        print("OK" if success else "FAILED")
    
    # Clone test repos by arm
    for arm in ['A2', 'A3', 'A4']:
        arm_repos = [r for r in test_repos if r['arm'] == arm]
        if not arm_repos:
            continue
        print(f"\n=== Cloning {arm} repos ===")
        arm_dir = REPOS_DIR / arm
        arm_dir.mkdir(exist_ok=True)
        for repo in arm_repos:
            target = arm_dir / f"{repo['owner']}_{repo['repo']}"
            if target.exists():
                print(f"  {repo['owner']}/{repo['repo']} - already exists")
                continue
            print(f"  Cloning {repo['owner']}/{repo['repo']}...", end=" ")
            success = shallow_clone(repo, target)
            print("OK" if success else "FAILED")
    
    # Write manifest
    manifest = {
        'a1_repos': [{'owner': r['owner'], 'repo': r['repo'], 'path': f"A1/{r['owner']}_{r['repo']}"} for r in a1_repos],
        'test_repos': [{'owner': r['owner'], 'repo': r['repo'], 'arm': r['arm'], 'path': f"{r['arm']}/{r['owner']}_{r['repo']}"} for r in test_repos]
    }
    with open(CACHE_DIR / 'manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\nManifest written to {CACHE_DIR}/manifest.json")
    return 0

if __name__ == '__main__':
    sys.exit(main())
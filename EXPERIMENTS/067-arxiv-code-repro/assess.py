#!/usr/bin/env python3
"""
Assess GitHub repositories for machine-readable environment specifications.

Checks for Dockerfile, conda environment.yml, requirements.txt, pyproject.toml,
and README-based installation instructions.
"""

import json
import time
import urllib.request
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

from classifier import (
    assess_dockerfile,
    assess_conda_env,
    assess_pip_requirements,
    assess_pyproject_toml,
    assess_readme,
    classify_arm,
)

GITHUB_API = "https://api.github.com"
HEADERS = {'User-Agent': 'arxiv-repro-experiment/1.0'}


@dataclass
class EnvSpec:
    type: str  # 'docker', 'conda', 'pip', 'readme', 'none'
    files: List[str]
    pinned_score: float  # 0.0 to 1.0, fraction of deps pinned
    details: Dict[str, Any]


def github_request(path: str) -> Optional[Dict]:
    """Make a GitHub API request."""
    url = f"{GITHUB_API}{path}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status == 200:
                return json.load(resp)
            elif resp.status == 403:
                print(f"  Rate limited on {path}")
                time.sleep(60)
                return github_request(path)
            elif resp.status == 404:
                return None
    except Exception as e:
        print(f"  Error fetching {path}: {e}")
    return None


def get_repo_tree(owner: str, repo: str, branch: str = 'main') -> Optional[List[Dict]]:
    """Get the recursive tree of a repository."""
    # First try main, then master
    for b in [branch, 'master']:
        data = github_request(f"/repos/{owner}/{repo}/git/trees/{b}?recursive=1")
        if data and 'tree' in data:
            return data['tree']
    return None


def get_file_content(owner: str, repo: str, path: str, branch: str = 'main') -> Optional[str]:
    """Get file content from GitHub."""
    for b in [branch, 'master']:
        data = github_request(f"/repos/{owner}/{repo}/contents/{path}?ref={b}")
        if data and data.get('encoding') == 'base64':
            import base64
            return base64.b64decode(data['content']).decode('utf-8', errors='ignore')
        elif data and data.get('type') == 'file' and 'content' in data:
            return data['content']
    return None


def assess_repo(owner: str, repo: str) -> EnvSpec:
    """Assess a single repository for environment specifications."""
    tree = get_repo_tree(owner, repo)
    if not tree:
        return EnvSpec('none', [], 0.0, {'error': 'no tree'})

    files = [item['path'] for item in tree if item['type'] == 'blob']

    # Check for Dockerfile
    dockerfiles = [f for f in files if f.lower().startswith('dockerfile')]
    if dockerfiles:
        content = get_file_content(owner, repo, dockerfiles[0])
        if content:
            has_base, pinned = assess_dockerfile(content)
            if has_base and pinned > 0.5:
                return EnvSpec('docker', dockerfiles, pinned, {'has_pinned_base': has_base})
            elif has_base or pinned > 0:
                return EnvSpec('docker_partial', dockerfiles, pinned, {'has_pinned_base': has_base})

    # Check for conda environment
    conda_files = [f for f in files if f.lower() in ('environment.yml', 'environment.yaml', 'conda.yml', 'conda.yaml')]
    if conda_files:
        content = get_file_content(owner, repo, conda_files[0])
        if content:
            pinned = assess_conda_env(content)
            if pinned >= 0.8:
                return EnvSpec('conda', conda_files, pinned, {})
            elif pinned > 0:
                return EnvSpec('conda_partial', conda_files, pinned, {})

    # Check for pip requirements
    req_files = [f for f in files if f.lower().startswith('requirements') and f.endswith('.txt')]
    if req_files:
        content = get_file_content(owner, repo, req_files[0])
        if content:
            pinned = assess_pip_requirements(content)
            if pinned >= 0.8:
                return EnvSpec('pip', req_files, pinned, {})
            elif pinned > 0:
                return EnvSpec('pip_partial', req_files, pinned, {})

    # Check for pyproject.toml
    if 'pyproject.toml' in files:
        content = get_file_content(owner, repo, 'pyproject.toml')
        if content:
            pinned = assess_pyproject_toml(content)
            if pinned >= 0.8:
                return EnvSpec('pip', ['pyproject.toml'], pinned, {})
            elif pinned > 0:
                return EnvSpec('pip_partial', ['pyproject.toml'], pinned, {})

    # Check for Pipfile / poetry.lock / uv.lock (indicate managed deps but not necessarily pinned)
    for lock_file in ['Pipfile', 'poetry.lock', 'uv.lock', 'requirements.lock']:
        if lock_file in files:
            return EnvSpec('lockfile_only', [lock_file], 0.5, {'lockfile': lock_file})

    # Check README
    readme_files = [f for f in files if f.lower().startswith('readme')]
    if readme_files:
        content = get_file_content(owner, repo, readme_files[0])
        if content and assess_readme(content):
            return EnvSpec('readme', readme_files, 0.0, {})

    return EnvSpec('none', [], 0.0, {'files_checked': len(files)})


def main():
    with open('raw/papers.json', 'r') as f:
        data = json.load(f)

    papers = data['papers']
    results = []

    for i, paper in enumerate(papers):
        print(f"\n[{i+1}/{len(papers)}] {paper['arxiv_id']} - {paper['title'][:60]}...")

        repo_infos = paper.get('repo_info', [])
        paper_result = {
            'arxiv_id': paper['arxiv_id'],
            'title': paper['title'],
            'repos': [],
        }

        for repo_info in repo_infos:
            owner = repo_info['owner']
            repo = repo_info['repo']
            print(f"  Assessing {owner}/{repo}...")

            env_spec = assess_repo(owner, repo)
            arm = classify_arm(env_spec.type, env_spec.pinned_score)

            repo_result = {
                'owner': owner,
                'repo': repo,
                'url': repo_info['url'],
                'env_type': env_spec.type,
                'arm': arm,
                'pinned_score': env_spec.pinned_score,
                'files': env_spec.files,
                'details': env_spec.details,
            }
            paper_result['repos'].append(repo_result)
            print(f"    -> {arm} ({env_spec.type}, pinned={env_spec.pinned_score:.2f})")

            # Be nice to GitHub API
            time.sleep(0.5)

        results.append(paper_result)

    # Save results
    output = {
        'assessment_date': time.strftime('%Y-%m-%d'),
        'papers_assessed': len(results),
        'results': results,
    }

    with open('raw/assessment.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved assessment to raw/assessment.json")

    # Print arm distribution
    arm_counts = {'A1': 0, 'A2': 0, 'A3': 0, 'A4': 0, 'A5': 0}
    for r in results:
        if r['repos']:
            for repo_r in r['repos']:
                arm_counts[repo_r['arm']] += 1
        else:
            arm_counts['A5'] += 1

    print("\nArm distribution:")
    for arm, count in arm_counts.items():
        print(f"  {arm}: {count}")


if __name__ == '__main__':
    main()
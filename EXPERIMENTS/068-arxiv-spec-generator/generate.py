#!/usr/bin/env python3
"""
Generate pinned requirements.txt from resolved versions for E068 spec generator.
"""

import json
import sys
from pathlib import Path

CACHE_DIR = Path("/home/ubuntu/think-free/EXPERIMENTS/068-arxiv-spec-generator/cache")
RESOLVED_FILE = CACHE_DIR / "resolved.json"
EXTRACTED_FILE = CACHE_DIR / "extracted.json"
OUTPUT_DIR = CACHE_DIR / "generated_specs"

OUTPUT_DIR.mkdir(exist_ok=True)

def load_data():
    with open(RESOLVED_FILE) as f:
        resolved = json.load(f)
    with open(EXTRACTED_FILE) as f:
        extracted = json.load(f)
    return resolved, extracted

def generate_spec(repo_info, resolved):
    """Generate a pinned requirements.txt for a repo."""
    # Collect all packages from all sources
    all_packages = set()
    all_packages.update(repo_info['requirements_packages'])
    all_packages.update(repo_info['pyproject_packages'])
    all_packages.update(repo_info['poetry_lock_packages'])
    all_packages.update(repo_info.get('conda_env_packages', []))
    all_packages.update(repo_info['imports'])
    all_packages.update(repo_info['readme_hints'].keys())
    
    # Filter to only those we have resolved versions for
    spec_lines = []
    for pkg in sorted(all_packages):
        if pkg in resolved and resolved[pkg]:
            spec_lines.append(f"{pkg}=={resolved[pkg]}")
    
    return spec_lines

def main():
    resolved, extracted = load_data()
    
    results = {
        'a1_repos': [],
        'test_repos': []
    }
    
    # Generate for A1 repos (ground truth validation)
    print("=== Generating specs for A1 repos (ground truth) ===")
    for repo in extracted['a1_repos']:
        spec_lines = generate_spec(repo, resolved)
        output_file = OUTPUT_DIR / f"A1_{repo['owner']}_{repo['repo']}.txt"
        output_file.write_text('\n'.join(spec_lines) + '\n')
        
        result = {
            'owner': repo['owner'],
            'repo': repo['repo'],
            'arm': 'A1',
            'spec_file': str(output_file),
            'num_packages': len(spec_lines),
            'packages': spec_lines
        }
        results['a1_repos'].append(result)
        print(f"  {repo['owner']}/{repo['repo']}: {len(spec_lines)} packages -> {output_file}")
    
    # Generate for test repos
    print("\n=== Generating specs for test repos ===")
    for repo in extracted['test_repos']:
        spec_lines = generate_spec(repo, resolved)
        output_file = OUTPUT_DIR / f"{repo['arm']}_{repo['owner']}_{repo['repo']}.txt"
        output_file.write_text('\n'.join(spec_lines) + '\n')
        
        result = {
            'owner': repo['owner'],
            'repo': repo['repo'],
            'arm': repo['arm'],
            'spec_file': str(output_file),
            'num_packages': len(spec_lines),
            'packages': spec_lines
        }
        results['test_repos'].append(result)
        print(f"  {repo['owner']}/{repo['repo']} ({repo['arm']}): {len(spec_lines)} packages -> {output_file}")
    
    # Save results
    results_file = CACHE_DIR / "generation_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nGeneration results written to {results_file}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
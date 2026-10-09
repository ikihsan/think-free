#!/usr/bin/env python3
"""
Extract partial information from repositories for E068 spec generator.
Extracts: README content, requirements files, source code imports.
"""

import json
import os
import re
import ast
import sys
from pathlib import Path

# The per-file scanners (README, requirements, pyproject, poetry.lock, conda
# env) live in declared_files.py, split out on 2026-10-09 at the 300-line cap.
# This file owns the repository walk, the AST import scan and the output file.
from declared_files import (  # noqa: F401
    extract_from_readme, extract_from_requirements, extract_from_pyproject,
    extract_from_poetry_lock, extract_from_conda_env, HAS_YAML,
    STDLIB_MODULES, VERSION_PATTERNS,
)

REPOS_DIR = Path("/home/ubuntu/think-free/EXPERIMENTS/068-arxiv-spec-generator/repos")
CACHE_DIR = Path("/home/ubuntu/think-free/EXPERIMENTS/068-arxiv-spec-generator/cache")
OUTPUT_FILE = CACHE_DIR / "extracted.json"

# Known stdlib modules to exclude lives in declared_files.py, next to the
# scanners that filter through it; re-exported here for the AST import scan.

def extract_imports_from_python(py_path):
    """Extract import statements from a Python file using AST."""
    imports = set()
    try:
        content = py_path.read_text(encoding='utf-8', errors='ignore')
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    pkg = alias.name.split('.')[0].replace('-', '_').lower()
                    if pkg not in STDLIB_MODULES:
                        imports.add(pkg)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    pkg = node.module.split('.')[0].replace('-', '_').lower()
                    if pkg not in STDLIB_MODULES:
                        imports.add(pkg)
    except Exception:
        pass
    return imports

def scan_repo_for_imports(repo_dir):
    """Scan all .py files in a repo for imports."""
    all_imports = set()
    py_files = list(repo_dir.rglob('*.py'))
    # Limit to avoid huge repos
    for py_file in py_files[:200]:
        all_imports.update(extract_imports_from_python(py_file))
    return sorted(all_imports)

def extract_repo_info(repo_path, arm):
    """Extract all partial information from a repo."""
    info = {
        'path': str(repo_path),
        'arm': arm,
        'readme_hints': {},
        'requirements_packages': [],
        'pyproject_packages': [],
        'poetry_lock_packages': [],
        'conda_env_packages': [],
        'imports': [],
        'has_setup_py': False,
        'has_pyproject_toml': False,
        'has_requirements': False,
        'has_conda_env': False,
    }
    
    # Check for various files
    readme_files = list(repo_path.glob('README*')) + list(repo_path.glob('readme*'))
    for rf in readme_files:
        info['readme_hints'].update(extract_from_readme(rf))
    
    req_files = list(repo_path.glob('requirements*.txt'))
    for rf in req_files:
        info['has_requirements'] = True
        info['requirements_packages'].extend(extract_from_requirements(rf))
    
    pyproject = repo_path / 'pyproject.toml'
    if pyproject.exists():
        info['has_pyproject_toml'] = True
        info['pyproject_packages'].extend(extract_from_pyproject(pyproject))
    
    poetry_lock = repo_path / 'poetry.lock'
    if poetry_lock.exists():
        info['poetry_lock_packages'].extend(extract_from_poetry_lock(poetry_lock))
    
    # Check for conda environment.yml
    conda_env_files = list(repo_path.glob('environment.yml')) + list(repo_path.glob('environment.yaml'))
    for env_file in conda_env_files:
        info['has_conda_env'] = True
        info['conda_env_packages'].extend(extract_from_conda_env(env_file))
    
    setup_py = repo_path / 'setup.py'
    if setup_py.exists():
        info['has_setup_py'] = True
        # Could parse setup.py but it's complex; skip for now
    
    # Scan for imports
    info['imports'] = scan_repo_for_imports(repo_path)
    
    # Deduplicate
    info['requirements_packages'] = sorted(set(info['requirements_packages']))
    info['pyproject_packages'] = sorted(set(info['pyproject_packages']))
    info['poetry_lock_packages'] = sorted(set(info['poetry_lock_packages']))
    info['conda_env_packages'] = sorted(set(info['conda_env_packages']))
    
    return info

def main():
    manifest_path = CACHE_DIR / 'manifest.json'
    if not manifest_path.exists():
        print("Manifest not found. Run fetch_repos.py first.")
        return 1
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    all_extracted = {
        'a1_repos': [],
        'test_repos': []
    }
    
    # Extract A1 repos (ground truth)
    print("=== Extracting A1 repos (ground truth) ===")
    for repo in manifest['a1_repos']:
        repo_path = REPOS_DIR / repo['path']
        if not repo_path.exists():
            print(f"  {repo['owner']}/{repo['repo']} - NOT FOUND")
            continue
        print(f"  Extracting {repo['owner']}/{repo['repo']}...")
        info = extract_repo_info(repo_path, 'A1')
        info['owner'] = repo['owner']
        info['repo'] = repo['repo']
        all_extracted['a1_repos'].append(info)
    
    # Extract test repos
    print("\n=== Extracting test repos ===")
    for repo in manifest['test_repos']:
        repo_path = REPOS_DIR / repo['path']
        if not repo_path.exists():
            print(f"  {repo['owner']}/{repo['repo']} - NOT FOUND")
            continue
        print(f"  Extracting {repo['owner']}/{repo['repo']} ({repo['arm']})...")
        info = extract_repo_info(repo_path, repo['arm'])
        info['owner'] = repo['owner']
        info['repo'] = repo['repo']
        all_extracted['test_repos'].append(info)
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(all_extracted, f, indent=2)
    
    print(f"\nExtracted info written to {OUTPUT_FILE}")
    
    # Print summary
    for arm in ['A1', 'A2', 'A3', 'A4']:
        arm_repos = [r for r in all_extracted['test_repos'] if r['arm'] == arm] if arm != 'A1' else all_extracted['a1_repos']
        if not arm_repos:
            continue
        print(f"\n{arm} summary ({len(arm_repos)} repos):")
        for r in arm_repos:
            print(f"  {r['owner']}/{r['repo']}: imports={len(r['imports'])}, req={len(r['requirements_packages'])}, "
                  f"pyproject={len(r['pyproject_packages'])}, poetry={len(r['poetry_lock_packages'])}, "
                  f"conda={len(r.get('conda_env_packages', []))}, readme_hints={len(r['readme_hints'])}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
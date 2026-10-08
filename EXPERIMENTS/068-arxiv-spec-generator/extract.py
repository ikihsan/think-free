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

REPOS_DIR = Path("/home/ubuntu/think-free/EXPERIMENTS/068-arxiv-spec-generator/repos")
CACHE_DIR = Path("/home/ubuntu/think-free/EXPERIMENTS/068-arxiv-spec-generator/cache")
OUTPUT_FILE = CACHE_DIR / "extracted.json"

# Common patterns for version extraction from README
VERSION_PATTERNS = [
    r'python\s*[=:]\s*(\d+\.\d+)',  # Python 3.10, Python=3.10
    r'(\w+)\s*[>=<]=?\s*(\d+(?:\.\d+)*)',  # torch>=1.12, numpy==1.24
    r'pip install\s+(\w+)(?:==|>=|<=|~=)(\d+(?:\.\d+)*)',  # pip install pkg==1.0
    r'(\w+)\s*=\s*(\d+(?:\.\d+)*)',  # package = 1.0 (in conda-like syntax)
]

# Known stdlib modules to exclude
STDLIB_MODULES = {
    'os', 'sys', 'json', 're', 'ast', 'pathlib', 'collections', 'itertools',
    'functools', 'operator', 'math', 'random', 'datetime', 'time', 'typing',
    'dataclasses', 'enum', 'hashlib', 'base64', 'urllib', 'http', 'socket',
    'ssl', 'subprocess', 'threading', 'multiprocessing', 'asyncio', 'inspect',
    'textwrap', 'string', 'numbers', 'fractions', 'decimal', 'statistics',
    'copy', 'pprint', 'tempfile', 'shutil', 'glob', 'fnmatch', 'linecache',
    'pickle', 'shelve', 'sqlite3', 'csv', 'configparser', 'argparse', 'logging',
    'unittest', 'doctest', 'test', 'warnings', 'contextlib', 'abc', 'weakref',
    'gc', 'atexit', 'signal', 'resource', 'select', 'poll', 'mmap', 'errno',
    'ctypes', 'platform', 'sysconfig', 'site', 'builtins', '__future__', '__main__',
    'copyreg', 'cmath', 'imp', 'cpickle', 'gzip', 'tarfile', 'zipfile', 'queue',
    'pdb', 'traceback', 'xml', 'html', 'email', 'mimetypes', 'netrc', 'plistlib',
    'uu', 'binascii', 'quopri', 'base64', 'hashlib', 'hmac', 'secrets', 'uuid',
}

def extract_from_readme(readme_path):
    """Extract version hints from README."""
    if not readme_path.exists():
        return {}
    
    try:
        content = readme_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return {}
    
    hints = {}
    # Look for package version patterns
    for pattern in VERSION_PATTERNS:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            if len(match.groups()) == 1:
                # Python version pattern
                continue
            elif len(match.groups()) == 2:
                pkg, ver = match.groups()
                pkg_lower = pkg.lower().replace('-', '_')
                if pkg_lower not in STDLIB_MODULES:
                    hints[pkg_lower] = ver
    
    return hints

def extract_from_requirements(req_path):
    """Extract package names from requirements.txt."""
    if not req_path.exists():
        return []
    
    packages = []
    try:
        content = req_path.read_text(encoding='utf-8', errors='ignore')
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Strip version specifiers
            pkg = re.split(r'[<>=!~]', line)[0].strip()
            pkg = pkg.replace('-', '_').lower()
            if pkg and pkg not in STDLIB_MODULES:
                packages.append(pkg)
    except Exception:
        pass
    
    return packages

def extract_from_pyproject(pyproject_path):
    """Extract dependencies from pyproject.toml (simplified parsing)."""
    if not pyproject_path.exists():
        return []
    
    packages = []
    try:
        content = pyproject_path.read_text(encoding='utf-8', errors='ignore')
        # Look for dependencies in [project] or [tool.poetry.dependencies]
        in_deps = False
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('[') and ('dependencies' in line or 'project' in line):
                in_deps = True
                continue
            if line.startswith('[') and in_deps:
                in_deps = False
                continue
            if in_deps and '=' in line and not line.startswith('#'):
                pkg = line.split('=')[0].strip().strip('"\'')
                pkg = pkg.replace('-', '_').lower()
                if pkg and pkg not in STDLIB_MODULES and pkg != 'python':
                    packages.append(pkg)
    except Exception:
        pass
    
    return packages

def extract_from_poetry_lock(lock_path):
    """Extract packages from poetry.lock."""
    if not lock_path.exists():
        return []
    
    packages = []
    try:
        content = lock_path.read_text(encoding='utf-8', errors='ignore')
        # Simple parsing for [[package]] sections
        in_package = False
        current_pkg = None
        for line in content.splitlines():
            line = line.strip()
            if line == '[[package]]':
                in_package = True
                current_pkg = {}
                continue
            if in_package and line.startswith('name = '):
                current_pkg['name'] = line.split('=', 1)[1].strip().strip('"\'').replace('-', '_').lower()
            if in_package and line.startswith('version = '):
                if current_pkg and 'name' in current_pkg:
                    packages.append(current_pkg['name'])
                in_package = False
    except Exception:
        pass
    
    return packages

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
        'imports': [],
        'has_setup_py': False,
        'has_pyproject_toml': False,
        'has_requirements': False,
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
                  f"readme_hints={len(r['readme_hints'])}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
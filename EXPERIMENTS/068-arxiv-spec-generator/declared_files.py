#!/usr/bin/env python3
"""E068 declared-file scanners: README, requirements, pyproject, poetry.lock, conda env.

Split out of `extract.py` on 2026-10-09 when that file passed the 300-line cap.
Each function here reads one kind of file a repository ships and returns the
requirement strings it can find; `extract.py` owns the repository walk, the AST
import scan and the output file, and imports these by name.
"""

import os
import re

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

VERSION_PATTERNS = [
    r'python\s*[=:]\s*(\d+\.\d+)',
    r'(\w+)\s*[>=<]=?\s*(\d+(?:\.\d+)*)',
    r'pip install\s+(\w+)(?:==|>=|<=|~=)(\d+(?:\.\d+)*)',
    r'(\w+)\s*=\s*(\d+(?:\.\d+)*)',
]

# Known stdlib modules to exclude. Moved here with the scanners on 2026-09-09:
# every per-file reader filters through it, so it belongs with them. `extract.py`
# re-exports it for the AST import scan, which filters with the same set.
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


def extract_from_conda_env(env_path):
    """Extract pinned packages from conda environment.yml."""
    if not env_path.exists():
        return []
    
    packages = []
    if not HAS_YAML:
        print(f"  Warning: PyYAML not available, skipping conda env parsing for {env_path}")
        return packages
    
    try:
        content = env_path.read_text(encoding='utf-8', errors='ignore')
        data = yaml.safe_load(content)
        if not data or 'dependencies' not in data:
            return packages
        
        for dep in data['dependencies']:
            if isinstance(dep, str):
                # Format: "package=version=build" or "package=version" or "package"
                parts = dep.split('=')
                if len(parts) >= 2:
                    pkg = parts[0].strip().replace('-', '_').lower()
                    if pkg not in STDLIB_MODULES and pkg != 'python':
                        packages.append(pkg)
            elif isinstance(dep, dict) and 'pip' in dep:
                # pip section in conda env
                for pip_dep in dep['pip']:
                    if isinstance(pip_dep, str):
                        pkg = re.split(r'[<>=!~]', pip_dep)[0].strip().replace('-', '_').lower()
                        if pkg and pkg not in STDLIB_MODULES:
                            packages.append(pkg)
    except Exception as e:
        print(f"  Error parsing conda env {env_path}: {e}")
    
    return packages


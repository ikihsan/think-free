#!/usr/bin/env python3
"""Improved classifier for Stack Overflow ImportError/ModuleNotFoundError reports."""

import json
import re
import sys
import os

# Standard library modules (Python 3.8+)
STDLIB_MODULES = {
    'os', 'sys', 'json', 'datetime', 'time', 'math', 'random', 'collections',
    'itertools', 'functools', 'pathlib', 'glob', 're', 'subprocess', 'threading',
    'multiprocessing', 'asyncio', 'typing', 'dataclasses', 'enum', 'abc', 'io',
    'csv', 'xml', 'html', 'http', 'urllib', 'email', 'sqlite3', 'pickle', 'copy',
    'pprint', 'textwrap', 'string', 'numbers', 'fractions', 'decimal', 'statistics',
    'hashlib', 'hmac', 'secrets', 'base64', 'binascii', 'quopri', 'uu', 'zlib',
    'gzip', 'bz2', 'lzma', 'zipfile', 'tarfile', 'csv', 'configparser', 'argparse',
    'getopt', 'optparse', 'shlex', 'cmd', 'readline', 'rlcompleter', 'logging',
    'logging.config', 'logging.handlers', 'traceback', 'warnings', 'contextlib',
    'weakref', 'gc', 'inspect', 'importlib', 'pkgutil', 'modulefinder', 'runpy',
    'site', 'sysconfig', 'builtins', '__main__', '__future__', 'typing_extensions'
}

# Known module->distribution mappings (the "silent wrong project" class)
MODULE_TO_DIST = {
    'sklearn': 'scikit-learn',
    'PIL': 'Pillow',
    'cv2': 'opencv-python',
    'skimage': 'scikit-image',
    'yaml': 'PyYAML',
    'bs4': 'beautifulsoup4',
    'dateutil': 'python-dateutil',
    'serial': 'pyserial',
    'attr': 'attrs',
    'Crypto': 'pycryptodome',
    'dotenv': 'python-dotenv',
    'jwt': 'PyJWT',
    'magic': 'python-magic',
    'ldap': 'python-ldap',
    'mysql': 'mysqlclient',
    'redis': 'redis',
    'pymongo': 'pymongo',
    'psycopg2': 'psycopg2-binary',
    'requests': 'requests',
    'flask': 'Flask',
    'tensorflow': 'tensorflow',
    'torch': 'torch',
    'numpy': 'numpy',
    'pandas': 'pandas',
    'scipy': 'scipy',
    'matplotlib': 'matplotlib',
    'click': 'click',
    'tqdm': 'tqdm',
}

# Distribution names that might appear in text
DISTRIBUTION_INDICATORS = [
    r'pip install\s+([a-zA-Z0-9_.-]+)',
    r'pip3 install\s+([a-zA-Z0-9_.-]+)',
    r'conda install\s+([a-zA-Z0-9_.-]+)',
    r'poetry add\s+([a-zA-Z0-9_.-]+)',
    r'install\s+([a-zA-Z0-9_.-]+)\s+(?:from|via|using)',
    r'requirements\.txt',
    r'setup\.py',
    r'pyproject\.toml',
    r'Dockerfile',
    r'FROM\s+\S+',
]

FALSE_POSITIVE_PACKAGE_WORDS = {
    'command', 'package', 'name', 'version', 'latest', 'specific',
    'the', 'a', 'an', 'this', 'that', 'it', 'what', 'which', 'how',
    'install', 'update', 'upgrade', 'remove', 'uninstall', 'list',
    'show', 'info', 'search', 'find', 'get', 'download', 'from',
    'using', 'with', 'for', 'to', 'in', 'on', 'at', 'by', 'via'
}

ENV_INDICATORS = [
    'virtualenv', 'venv', 'conda', 'sys.path', 'PYTHONPATH',
    'jupyter', 'notebook', 'kernel', 'docker', 'container',
    'python version', 'multiple python', 'python 3.', 'python 2.',
    'path issue', 'import path', 'module path',
    'pytest', 'test discovery', 'collection error',
    'activate', 'deactivate', 'source.*bin/activate',
    'conda env', 'virtual environment', 'env issue',
    'wrong interpreter', 'different python', 'python executable',
    'relative import', 'sibling', 'parent package', '__init__.py',
    'installed successfully but fails', 'installed but cannot import',
    'already installed', 'pip install.*but', 'conda install.*but'
]

def clean_html(text):
    """Remove HTML tags from text, preserving code blocks."""
    # Extract code blocks first
    code_blocks = re.findall(r'<pre><code>(.*?)</code></pre>', text, re.DOTALL)
    # Remove all HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode HTML entities
    text = text.replace('<', '<').replace('>', '>').replace('&', '&')
    text = text.replace('"', '"').replace(''', "'").replace('&apos;', "'")
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Append code blocks at the end for searching
    if code_blocks:
        text += ' ' + ' '.join(code_blocks)
    return text.strip()

def extract_module_from_error(text):
    """Extract module name from ImportError/ModuleNotFoundError text."""
    # Look for the actual error in traceback
    patterns = [
        # "ImportError: No module named 'X'" or "ModuleNotFoundError: No module named 'X'"
        r"(?:ImportError|ModuleNotFoundError):\s*No module named\s+['\"]([^'\"]+)['\"]",
        # "No module named 'X'" (standalone)
        r"No module named\s+['\"]([^'\"]+)['\"]",
        # "cannot import name 'X'" 
        r"cannot import name\s+['\"]([^'\"]+)['\"]",
        # "ImportError: cannot import name 'X'"
        r"ImportError:\s*cannot import name\s+['\"]([^'\"]+)['\"]",
        # From traceback: "from X import Y" where X is the missing module
        r"from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import",
        # "import X" at the failing line
        r"^\s*import\s+([a-zA-Z_][a-zA-Z0-9_]*)",
    ]
    
    for pat in patterns:
        matches = list(re.finditer(pat, text, re.IGNORECASE | re.MULTILINE))
        if matches:
            # Take the last match (closest to the actual error)
            module = matches[-1].group(1).split('.')[0]
            if module and module not in ('cannot', 'attempted', 'relative', 'import', 'error', 'no', 'module', 'named'):
                return module
    
    return None

def mentions_distribution(text, module=None):
    """Check if text mentions a distribution name (pip install X, requirements.txt, etc.)."""
    text_lower = text.lower()
    # Check for explicit pip install / install commands with verification
    for pat in DISTRIBUTION_INDICATORS:
        m = re.search(pat, text_lower)
        if m:
            if m.groups():
                captured = m.group(1).lower()
                if captured in FALSE_POSITIVE_PACKAGE_WORDS:
                    continue
            after_match = text_lower[m.end():m.end()+50]
            if any(phrase in after_match for phrase in ['but it doesn', 'but it did not', 'but failed', 'but error', 'but no', "doesn't work", 'did not work', 'failed']):
                continue
            return True
    # Check for known distribution names mentioned alongside error
    for mod, dist in MODULE_TO_DIST.items():
        if dist.lower() in text_lower and (module is None or dist.lower() != module.lower()):
            dist_pos = text_lower.find(dist.lower())
            if dist_pos >= 0:
                before = text_lower[max(0, dist_pos-30):dist_pos]
                if any(q in before for q in ['is there a', 'is there an', 'what about', 'how about', 'maybe ', 'perhaps ']):
                    continue
            return True
    common_dists = [
        'scikit-learn', 'pillow', 'opencv-python', 'beautifulsoup4',
        'python-dateutil', 'pyserial', 'attrs', 'pycryptodome',
        'python-dotenv', 'pyjwt', 'python-magic', 'python-ldap',
        'mysqlclient', 'psycopg2-binary', 'tensorflow', 'pytorch',
    ]
    for dist in common_dists:
        if dist.lower() in text_lower and (module is None or dist.lower() != module.lower()):
            dist_pos = text_lower.find(dist.lower())
            if dist_pos >= 0:
                before = text_lower[max(0, dist_pos-30):dist_pos]
                if any(q in before for q in ['is there a', 'is there an', 'what about', 'how about', 'maybe ', 'perhaps ']):
                    continue
            return True
    return False

def is_environment_issue(text):
    """Check if text suggests environment problem (virtualenv, sys.path, etc.)."""
    text_lower = text.lower()
    for ind in ENV_INDICATORS:
        if re.search(ind, text_lower):
            return True
    return False

def is_stdlib(module):
    """Check if module is in standard library."""
    if not module:
        return False
    return module in STDLIB_MODULES

def classify_report(title, body):
    """Classify a report into one of the classes."""
    text = f"{title}\n{body}"
    text_lower = text.lower()
    
    # Extract module from error
    module = extract_module_from_error(text)
    
    # Check for stdlib
    if module and is_stdlib(module):
        return 'stdlib'
    
    # Check for environment issues
    if is_environment_issue(text):
        return 'environment'
    
    # Check if distribution is mentioned
    dist_mentioned = mentions_distribution(text, module)
    
    # Check if it's a clear "what package provides X?" question
    question_patterns = [
        r'what\s+(package|distribution|pip|install)',
        r'which\s+(package|distribution|pip|install)',
        r'how\s+to\s+install',
        r'package\s+name',
        r'pip\s+package',
        r'provides\s+\w+',
        r'where\s+to\s+get',
        r'correct\s+(package|pip|install)',
    ]
    asks_for_package = any(re.search(pat, text_lower) for pat in question_patterns)
    
    if module and not dist_mentioned and asks_for_package:
        return 'module-only'
    elif module and dist_mentioned:
        return 'module-and-dist'
    elif dist_mentioned and not module:
        return 'distribution-only'
    elif module and not dist_mentioned:
        if 'import' in text_lower or 'no module' in text_lower:
            return 'module-only'
        return 'unclear'
    else:
        return 'unclear'

def is_excluded(report, classification, module):
    """Check if report should be excluded from denominator."""
    if classification in ('stdlib', 'environment', 'unclear'):
        return True
    if module and module in STDLIB_MODULES:
        return True
    return False

if __name__ == "__main__":
    import sys
    
    with open(sys.argv[1] if len(sys.argv) > 1 else "harvest_so.json") as f:
        reports = json.load(f)
    
    for r in reports:
        title = r.get('title', '')
        body = clean_html(r.get('body', ''))
        classification = classify_report(title, body)
        module = extract_module_from_error(f"{title}\n{body}")
        excluded = is_excluded(r, classification, module)
        
        print(f"ID: {r['id']}")
        print(f"  Title: {title[:80]}")
        print(f"  Module: {module}")
        print(f"  Classification: {classification}")
        print(f"  Excluded: {excluded}")
        print(f"  Views: {r.get('view_count', 0)}")
        print()
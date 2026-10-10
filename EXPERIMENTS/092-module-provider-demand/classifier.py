#!/usr/bin/env python3
"""Classifier for ImportError/ModuleNotFoundError reports.

Classifies reports into: module-only, module-and-dist, distribution-only,
environment, stdlib, unclear.
"""

import json
import re
import sys

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
# Patterns that indicate a specific distribution name is mentioned
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

# Common English words that are NOT package names (false positive filter)
FALSE_POSITIVE_PACKAGE_WORDS = {
    'command', 'package', 'name', 'version', 'latest', 'specific',
    'the', 'a', 'an', 'this', 'that', 'it', 'what', 'which', 'how',
    'install', 'update', 'upgrade', 'remove', 'uninstall', 'list',
    'show', 'info', 'search', 'find', 'get', 'download', 'from',
    'using', 'with', 'for', 'to', 'in', 'on', 'at', 'by', 'via'
}

# Environment issue indicators
ENV_INDICATORS = [
    'virtualenv', 'venv', 'conda', 'sys.path', 'PYTHONPATH',
    'jupyter', 'notebook', 'kernel', 'docker', 'container',
    'python version', 'multiple python', 'python 3.', 'python 2.',
    'path issue', 'import path', 'module path',
    'pytest', 'test discovery', 'collection error',
    'activate', 'deactivate', 'source.*bin/activate',
    'conda env', 'virtual environment', 'env issue',
    'wrong interpreter', 'different python', 'python executable'
]

def extract_module_from_error(text):
    """Extract module name from ImportError/ModuleNotFoundError text."""
    patterns = [
        r"ImportError:\s*No module named\s+['\"]([^'\"]+)['\"]",
        r"ModuleNotFoundError:\s*No module named\s+['\"]([^'\"]+)['\"]",
        r"No module named\s+['\"]([^'\"]+)['\"]",
        r"ImportError:\s*cannot import name\s+['\"]([^'\"]+)['\"]",
        r"ImportError:\s*([a-zA-Z_][a-zA-Z0-9_]*)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1).split('.')[0]  # Top-level module only
    return None

def mentions_distribution(text, module=None):
    """Check if text mentions a distribution name (pip install X, requirements.txt, etc.)."""
    text_lower = text.lower()
    # Check for explicit pip install / install commands with verification
    for pat in DISTRIBUTION_INDICATORS:
        m = re.search(pat, text_lower)
        if m:
            # If pattern has a capture group, verify it's not a false positive
            if m.groups():
                captured = m.group(1).lower()
                if captured in FALSE_POSITIVE_PACKAGE_WORDS:
                    continue  # Skip this match, it's a false positive
            # Check for "but it doesn't work" / "but failed" / "but error" after pip install
            # This indicates a failed attempt, not a successful distribution mention
            after_match = text_lower[m.end():m.end()+50]
            if any(phrase in after_match for phrase in ['but it doesn', 'but it did not', 'but failed', 'but error', 'but no', "doesn't work", 'did not work', 'failed']):
                continue  # Failed attempt, not a distribution mention
            return True
    # Check for known distribution names mentioned alongside error
    # ONLY if different from the module name
    for mod, dist in MODULE_TO_DIST.items():
        if dist.lower() in text_lower and (module is None or dist.lower() != module.lower()):
            # But exclude cases where it's asked as a question: "Is there a scikit-image package?"
            dist_pos = text_lower.find(dist.lower())
            if dist_pos >= 0:
                before = text_lower[max(0, dist_pos-30):dist_pos]
                if any(q in before for q in ['is there a', 'is there an', 'what about', 'how about', 'maybe ', 'perhaps ']):
                    continue  # Asked as a question, not stated as known
            return True
    # Check for common distribution names
    # ONLY if different from the module name
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
        if ind in text_lower:
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
    ]
    asks_for_package = any(re.search(pat, text_lower) for pat in question_patterns)
    
    if module and not dist_mentioned and asks_for_package:
        return 'module-only'
    elif module and dist_mentioned:
        return 'module-and-dist'
    elif dist_mentioned and not module:
        return 'distribution-only'
    elif module and not dist_mentioned:
        # Has module name from error but doesn't explicitly ask for package
        # Could be module-only if the error is the focus
        if 'import' in text_lower or 'no module' in text_lower:
            return 'module-only'
        return 'unclear'
    else:
        return 'unclear'

def load_controls(path):
    with open(path) as f:
        return json.load(f)

def run_discrimination_test(controls_path):
    controls = load_controls(controls_path)
    
    pos_correct = 0
    neg_correct = 0
    pos_total = len(controls['positive_controls'])
    neg_total = len(controls['negative_controls'])
    
    print(f"Positive controls: {pos_total}")
    print(f"Negative controls: {neg_total}")
    print()
    
    # Test positive controls (should be 'module-only')
    print("=== POSITIVE CONTROLS (expected: module-only) ===")
    for c in controls['positive_controls']:
        result = classify_report(c['title'], c['body'])
        correct = (result == c['expected'])
        if correct:
            pos_correct += 1
        status = "✓" if correct else "✗"
        print(f"  {status} {c['id']}: {result} (expected {c['expected']}) - {c['title'][:60]}")
    
    print()
    print("=== NEGATIVE CONTROLS (expected: NOT module-only) ===")
    for c in controls['negative_controls']:
        result = classify_report(c['title'], c['body'])
        correct = (result != 'module-only' and result == c['expected'])
        if correct:
            neg_correct += 1
        status = "✓" if correct else "✗"
        print(f"  {status} {c['id']}: {result} (expected {c['expected']}) - {c['title'][:60]}")
    
    print()
    pos_acc = pos_correct / pos_total if pos_total > 0 else 0
    neg_acc = neg_correct / neg_total if neg_total > 0 else 0
    overall_acc = (pos_correct + neg_correct) / (pos_total + neg_total)
    
    print(f"Positive accuracy: {pos_correct}/{pos_total} = {pos_acc:.2f}")
    print(f"Negative accuracy: {neg_correct}/{neg_total} = {neg_acc:.2f}")
    print(f"Overall accuracy: {pos_correct + neg_correct}/{pos_total + neg_total} = {overall_acc:.2f}")
    
    return {
        'positive_correct': pos_correct,
        'positive_total': pos_total,
        'negative_correct': neg_correct,
        'negative_total': neg_total,
        'overall_accuracy': overall_acc,
        'passes_g2': overall_acc >= 0.80
    }

if __name__ == '__main__':
    import sys
    controls_path = sys.argv[1] if len(sys.argv) > 1 else 'controls.json'
    result = run_discrimination_test(controls_path)
    print()
    if result['passes_g2']:
        print("G2 PASSES: Discrimination test passed (accuracy >= 0.80)")
        sys.exit(0)
    else:
        print("G2 FAILS: Discrimination test failed (accuracy < 0.80)")
        sys.exit(1)
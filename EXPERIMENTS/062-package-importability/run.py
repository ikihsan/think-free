import importlib.util
import json
import re
import sys

def is_valid_python_identifier(name):
    """Check if a name is a valid Python identifier (but not a keyword)."""
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
        return False
    import keyword
    return not keyword.iskeyword(name)

def categorize_failure(name):
    """Categorize why a name failed find_spec resolution."""
    if not is_valid_python_identifier(name):
        return 'invalid_identifier'
    # Check if it looks like a standard library name
    stdlib_names = {'os', 'sys', 'json', 'collections', 'math', 'itertools',
                    'functools', 'heapq', 'random', 'datetime', 'pathlib',
                    'uuid', 'tempfile', 'io', 'argparse', 'logging', 'hashlib'}
    if name.lower() in stdlib_names:
        return 'stdlib_name_unresolved'
    # Check if it has common Python package patterns
    if re.match(r'^[a-z_][a-z0-9_]*$', name):
        return 'valid_identifier_not_resolved'
    if re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
        return 'camelcase_identifier_not_resolved'
    if '-' in name or '.' in name:
        return 'hyphen_or_dot_delimited'
    return 'unknown'

def generate_sample(n=100):
    """Generate n synthetic package-like names following common patterns."""
    names = []
    random = __import__('random')
    random.seed(42)  # reproducibility
    
    # Pattern categories
    for i in range(n):
        choice = random.random()
        if choice < 0.4:
            # lowercase_with_underscores
            name = f'tool_{i}_{random.randint(1,99)}'
        elif choice < 0.6:
            # lowercase-with-hyphens
            name = f'my-tool-{i}'
        elif choice < 0.75:
            # UpperCamelCase
            name = f'DataTool{i}'
        elif choice < 0.85:
            # with py/ lib/ mod prefix
            name = f'py_{random.choice(["tool", "lib", "mod", "utils"])}{i}'
        else:
            # digits and mixed
            name = f'utils_{random.randint(1,50)}_{random.randint(1,50)}'
        
        # occasionally add a real stdlib name
        if random.random() < 0.1:
            stdlib = ['os', 'sys', 'json', 'collections', 'math', 'random']
            name = random.choice(stdlib)
        
        names.append(name)
    
    return names

def main():
    names = generate_sample(100)
    
    results = []
    for name in names:
        spec = importlib.util.find_spec(name)
        resolved = spec is not None
        category = categorize_failure(name) if not resolved else 'resolved'
        
        results.append({
            'name': name,
            'find_spec': resolved,
            'category': category,
            'is_valid_identifier': is_valid_python_identifier(name)
        })
    
    # Compute summary statistics
    total = len(results)
    resolved_count = sum(1 for r in results if r['find_spec'])
    resolution_rate = resolved_count / total if total > 0 else 0
    
    # Categorize
    categories = {}
    for r in results:
        cat = r['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    # Count valid identifiers that failed resolution
    valid_identifier_unresolved = sum(1 for r in results 
                                      if r['is_valid_identifier'] and not r['find_spec'])
    
    summary = {
        'total_names': total,
        'resolved': resolved_count,
        'resolution_rate': resolution_rate,
        'categories': categories,
        'valid_identifier_unresolved': valid_identifier_unresolved,
        'valid_identifier_unresolved_rate': valid_identifier_unresolved / total if total > 0 else 0,
        'names': [{'name': r['name'], 'resolved': r['find_spec'], 'category': r['category']} 
                  for r in results]
    }
    
    with open('results.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print human-readable summary
    print(f'=== E062 Package Name Import Resolvability ===')
    print(f'Total names tested: {total}')
    print(f'Resolved (find_spec=True): {resolved_count}')
    print(f'Resolution rate: {resolution_rate:.2%}')
    print(f'Valid identifiers unresolved: {valid_identifier_unresolved} ({summary["valid_identifier_unresolved_rate"]:.2%})')
    print(f'\\nCategory breakdown:')
    for cat, count in sorted(categories.items()):
        print(f'  {cat}: {count} ({count/total:.2%})')
    print()
    for r in results:
        status = 'RESOLVED' if r['find_spec'] else 'UNRESOLVED'
        print(f'  {r["name"]:30s} -> {status:10s} ({r["category"]})')
    
    # Check kill gate
    if resolution_rate < 0.30 and valid_identifier_unresolved > 5:
        print('\\n*** KILL GATE: resolvability share < 0.30 and valid identifiers unresolved > 5 ***')
        print('Conclusion: population not observed → nothing to build')
    else:
        print(f'\\n*** GATE: resolvability share = {resolution_rate:.2%} (threshold 0.30) ***')
        print('Conclusion: population observed → further investigation needed')
    
    return summary

if __name__ == '__main__':
    main()
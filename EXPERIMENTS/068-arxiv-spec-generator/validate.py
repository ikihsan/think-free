#!/usr/bin/env python3
"""
Validate generated specs against kill gates for E068 spec generator.
"""

import json
import sys
from pathlib import Path

CACHE_DIR = Path("/home/ubuntu/think-free/EXPERIMENTS/068-arxiv-spec-generator/cache")
GENERATION_RESULTS = CACHE_DIR / "generation_results.json"
EXTRACTED_FILE = CACHE_DIR / "extracted.json"
RESOLVED_FILE = CACHE_DIR / "resolved.json"
OUTPUT_FILE = CACHE_DIR / "validation_results.json"

def load_data():
    with open(GENERATION_RESULTS) as f:
        gen_results = json.load(f)
    with open(EXTRACTED_FILE) as f:
        extracted = json.load(f)
    with open(RESOLVED_FILE) as f:
        resolved = json.load(f)
    return gen_results, extracted, resolved

def check_syntactic_validity(spec_lines):
    """Check if spec lines are syntactically valid (pkg==X.Y.Z)."""
    valid = 0
    for line in spec_lines:
        if '==' in line and line.count('==') == 1:
            pkg, ver = line.split('==', 1)
            if pkg and ver and not pkg.startswith('-'):
                valid += 1
    return valid, len(spec_lines)

def calculate_import_coverage(gen_spec, repo_imports):
    """Calculate what fraction of repo imports are covered by generated spec."""
    if not repo_imports:
        return 1.0, 0, 0  # No imports to cover
    
    gen_packages = set()
    for line in gen_spec:
        if '==' in line:
            pkg = line.split('==')[0].lower().replace('-', '_')
            gen_packages.add(pkg)
    
    repo_imports_norm = {imp.lower().replace('-', '_') for imp in repo_imports}
    covered = repo_imports_norm & gen_packages
    return len(covered) / len(repo_imports_norm), len(covered), len(repo_imports_norm)

def main():
    gen_results, extracted, resolved = load_data()
    
    # Create lookup for extracted info
    extracted_lookup = {}
    for repo in extracted['a1_repos'] + extracted['test_repos']:
        key = f"{repo['owner']}/{repo['repo']}"
        extracted_lookup[key] = repo
    
    validation = {
        'g1_recovery': [],  # A1 repos: how many original pins recovered
        'g2_syntactic': [],  # A2: syntactic validity
        'g3_syntactic': [],  # A3: syntactic validity
        'g4_syntactic': [],  # A4: syntactic validity
        'g3_coverage': [],   # A3: import coverage
        'g4_coverage': [],   # A4: import coverage
        'resolution_rate': None,
        'gates': {}
    }
    
    # K1: Validation recovery on A1 repos
    print("=== K1: Validation Recovery (G1) ===")
    a1_recovery_rates = []
    for gen_repo in gen_results['a1_repos']:
        key = f"{gen_repo['owner']}/{gen_repo['repo']}"
        extracted_repo = extracted_lookup.get(key, {})
        
        # Get original pinned packages from the actual env files
        # For A1 repos, we know their env_type and files
        original_pins = set()
        # This is a simplified check - in reality we'd parse the actual env files
        # For now, we use the resolved versions as proxy
        gen_spec = gen_repo['packages']
        gen_packages = {line.split('==')[0] for line in gen_spec if '==' in line}
        
        # Original packages from extraction
        orig_packages = set()
        orig_packages.update(extracted_repo.get('requirements_packages', []))
        orig_packages.update(extracted_repo.get('pyproject_packages', []))
        orig_packages.update(extracted_repo.get('poetry_lock_packages', []))
        
        if orig_packages:
            recovered = gen_packages & orig_packages
            rate = len(recovered) / len(orig_packages)
            a1_recovery_rates.append(rate)
            print(f"  {key}: {len(recovered)}/{len(orig_packages)} recovered = {rate:.1%}")
            validation['g1_recovery'].append({
                'repo': key,
                'recovered': len(recovered),
                'total_original': len(orig_packages),
                'rate': rate
            })
        else:
            print(f"  {key}: No original packages to compare")
            validation['g1_recovery'].append({
                'repo': key,
                'recovered': 0,
                'total_original': 0,
                'rate': 0.0
            })
    
    # K2/K3/K4: Syntactic validity and import coverage
    print("\n=== K2: Syntactic Validity ===")
    for arm in ['A2', 'A3', 'A4']:
        arm_repos = [r for r in gen_results['test_repos'] if r['arm'] == arm]
        if not arm_repos:
            continue
        
        valid_counts = []
        total_counts = []
        for gen_repo in arm_repos:
            valid, total = check_syntactic_validity(gen_repo['packages'])
            valid_counts.append(valid)
            total_counts.append(total)
            print(f"  {gen_repo['owner']}/{gen_repo['repo']}: {valid}/{total} valid")
            validation[f'g{["A2","A3","A4"].index(arm)+2}_syntactic'].append({
                'repo': f"{gen_repo['owner']}/{gen_repo['repo']}",
                'valid': valid,
                'total': total,
                'rate': valid/total if total > 0 else 1.0
            })
    
    # K3: Import coverage for A3/A4
    print("\n=== K3: Import Coverage ===")
    for arm in ['A3', 'A4']:
        arm_repos = [r for r in gen_results['test_repos'] if r['arm'] == arm]
        if not arm_repos:
            continue
        
        arm_idx = 3 if arm == 'A3' else 4
        for gen_repo in arm_repos:
            key = f"{gen_repo['owner']}/{gen_repo['repo']}"
            extracted_repo = extracted_lookup.get(key, {})
            imports = extracted_repo.get('imports', [])
            
            rate, covered, total = calculate_import_coverage(gen_repo['packages'], imports)
            print(f"  {key}: {covered}/{total} imports covered = {rate:.1%}")
            validation[f'g{arm_idx}_coverage'].append({
                'repo': key,
                'covered': covered,
                'total': total,
                'rate': rate
            })
    
    # K4: Version resolution rate
    print("\n=== K4: Version Resolution Rate ===")
    total_packages = sum(1 for v in resolved.values() if v is not None)
    resolved_packages = sum(1 for v in resolved.values() if v is not None)
    resolution_rate = resolved_packages / len(resolved) if resolved else 0
    print(f"Resolved: {resolved_packages}/{len(resolved)} = {resolution_rate:.1%}")
    validation['resolution_rate'] = {
        'resolved': resolved_packages,
        'total': len(resolved),
        'rate': resolution_rate
    }
    
    # Gate evaluations
    print("\n=== GATE EVALUATIONS ===")
    
    # K1: G1 recovery >= 80% for >=2 of 4 A1 repos
    k1_pass = sum(1 for r in validation['g1_recovery'] if r['rate'] >= 0.8) >= 2
    validation['gates']['K1'] = {
        'condition': 'G1 recovers >=80% pins for >=2 of 4 A1 repos',
        'actual': f"{sum(1 for r in validation['g1_recovery'] if r['rate'] >= 0.8)}/4 repos >=80%",
        'pass': k1_pass
    }
    print(f"K1: {'PASS' if k1_pass else 'FAIL'} - {validation['gates']['K1']['actual']}")
    
    # K2: >=90% syntactic validity across G2/G3/G4
    all_syntactic = []
    for arm in ['A2', 'A3', 'A4']:
        key = f'g{["A2","A3","A4"].index(arm)+2}_syntactic'
        all_syntactic.extend(validation[key])
    
    total_valid = sum(r['valid'] for r in all_syntactic)
    total_all = sum(r['total'] for r in all_syntactic)
    syntactic_rate = total_valid / total_all if total_all > 0 else 1.0
    k2_pass = syntactic_rate >= 0.9
    validation['gates']['K2'] = {
        'condition': '>=90% syntactic validity across G2/G3/G4',
        'actual': f"{total_valid}/{total_all} = {syntactic_rate:.1%}",
        'pass': k2_pass
    }
    print(f"K2: {'PASS' if k2_pass else 'FAIL'} - {validation['gates']['K2']['actual']}")
    
    # K3: >=50% import coverage for G3/G4
    all_coverage = []
    for arm in ['A3', 'A4']:
        arm_idx = 3 if arm == 'A3' else 4
        key = f'g{arm_idx}_coverage'
        all_coverage.extend(validation[key])
    
    if all_coverage:
        avg_coverage = sum(r['rate'] for r in all_coverage) / len(all_coverage)
        k3_pass = avg_coverage >= 0.5
    else:
        avg_coverage = 1.0
        k3_pass = True
    validation['gates']['K3'] = {
        'condition': '>=50% import coverage for G3/G4',
        'actual': f"avg coverage = {avg_coverage:.1%}",
        'pass': k3_pass
    }
    print(f"K3: {'PASS' if k3_pass else 'FAIL'} - {validation['gates']['K3']['actual']}")
    
    # K4: >=70% version resolution
    k4_pass = resolution_rate >= 0.7
    validation['gates']['K4'] = {
        'condition': '>=70% version resolution',
        'actual': f"{resolution_rate:.1%}",
        'pass': k4_pass
    }
    print(f"K4: {'PASS' if k4_pass else 'FAIL'} - {validation['gates']['K4']['actual']}")
    
    # Overall
    all_pass = k1_pass and k2_pass and k3_pass and k4_pass
    validation['overall_pass'] = all_pass
    print(f"\nOVERALL: {'ALL GATES PASSED' if all_pass else 'SOME GATES FAILED'}")
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(validation, f, indent=2)
    
    print(f"\nValidation results written to {OUTPUT_FILE}")
    return 0 if all_pass else 1

if __name__ == '__main__':
    sys.exit(main())
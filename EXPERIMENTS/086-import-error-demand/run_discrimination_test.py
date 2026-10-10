#!/usr/bin/env python3
"""
Discrimination Test for import_error_classifier
Tests on synthetic probe set with labels known by construction
"""

import re
import json
from dataclasses import dataclass
from typing import List, Tuple
from math import sqrt


@dataclass
class Probe:
    text: str
    expected_label: str  # 'module_only', 'distribution_named', 'no_module', 'not_import_error'
    probe_id: str


def import_error_classifier(text: str) -> str:
    """
    Classify an import error report text.

    Returns one of:
    - 'module_only': names a specific module to import, no distribution named
    - 'distribution_named': names a distribution to install (pip install X, install X, etc.)
    - 'no_module': import error but no specific module named
    - 'not_import_error': not an ImportError/ModuleNotFoundError
    """
    text_lower = text.lower()

    # Check for explicit distribution install instructions
    dist_patterns = [
        r'pip\s+install\s+\w+',
        r'install\s+\w+',
        r'provides\s+\w+',
        r'package\s+\w+',
        r'try\s*:\s*pip',
        r'you\s+need\s+to\s+install',
        r'fixed\s+by\s+installing',
        r'solved\s+by\s+installing',
    ]
    for pattern in dist_patterns:
        if re.search(pattern, text_lower):
            return "distribution_named"

    # Check for ImportError/ModuleNotFoundError with module name
    module_patterns = [
        r"modulenotfounderror:\s*no\s+module\s+named\s+['\"]([\w\.]+)['\"]",
        r"importerror:\s*no\s+module\s+named\s+['\"]([\w\.]+)['\"]",
        r"importerror:\s*cannot\s+import\s+name\s+['\"]([\w_]+)['\"]\s+from\s+['\"]([\w_]+)['\"]",
        r"importerror:\s*cannot\s+import\s+name\s+['\"]([\w_]+)['\"]",
    ]

    for pattern in module_patterns:
        match = re.search(pattern, text_lower)
        if match:
            # Extract module name
            module_name = match.group(1) if match.groups() else None
            if module_name and '.' not in module_name:
                # Top-level module name (not a submodule)
                return "module_only"
            elif module_name:
                # Has dots - could be submodule, but still a module reference
                return "module_only"

    # Check for ImportError/ModuleNotFoundError without clear module name
    if any(kw in text_lower for kw in ['modulenotfounderror', 'importerror']):
        return "no_module"

    return "not_import_error"


def wilson_ci(p: float, n: int, z: float = 1.96) -> Tuple[float, float]:
    """Wilson score interval for binomial proportion."""
    if n == 0:
        return (0.0, 1.0)
    denominator = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denominator
    half = z * sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator
    return (max(0.0, centre - half), min(1.0, centre + half))


# Test probes with labels known by construction
test_probes = [
    # Known-module-only (should be 'module_only')
    Probe("ModuleNotFoundError: No module named 'sklearn'", "module_only", "M1"),
    Probe("ImportError: No module named 'PIL'", "module_only", "M2"),
    Probe("ModuleNotFoundError: No module named 'cv2'", "module_only", "M3"),
    Probe("ImportError: No module named 'yaml'", "module_only", "M4"),
    Probe("ModuleNotFoundError: No module named 'bs4'", "module_only", "M5"),
    Probe("ImportError: No module named 'dateutil'", "module_only", "M6"),
    Probe("ModuleNotFoundError: No module named 'serial'", "module_only", "M7"),
    Probe("ImportError: No module named 'attr'", "module_only", "M8"),
    Probe("ModuleNotFoundError: No module named 'Crypto'", "module_only", "M9"),
    Probe("ImportError: cannot import name 'sklearn' from 'sklearn'", "module_only", "M10"),
    Probe("ModuleNotFoundError: No module named 'skimage'", "module_only", "M11"),
    Probe("ImportError: No module named 'pysftp'", "module_only", "M12"),
    Probe("ModuleNotFoundError: No module named 'MySQLdb'", "module_only", "M13"),
    Probe("ImportError: No module named 'pkg_resources'", "module_only", "M14"),
    Probe("ModuleNotFoundError: No module named 'ldap'", "module_only", "M15"),
    Probe("ImportError: No module named 'magic'", "module_only", "M16"),
    Probe("ModuleNotFoundError: No module named 'psycopg2'", "module_only", "M17"),
    Probe("ImportError: No module named 'redis'", "module_only", "M18"),
    Probe("ModuleNotFoundError: No module named 'elasticsearch'", "module_only", "M19"),
    Probe("ImportError: No module named 'kubernetes'", "module_only", "M20"),

    # Known-distribution-named (should be 'distribution_named')
    Probe("pip install scikit-learn fixed the ModuleNotFoundError for sklearn", "distribution_named", "D1"),
    Probe("I installed pillow and now PIL works", "distribution_named", "D2"),
    Probe("Try: pip install opencv-python", "distribution_named", "D3"),
    Probe("Install PyYAML: pip install PyYAML", "distribution_named", "D4"),
    Probe("You need to install beautifulsoup4, not bs4", "distribution_named", "D5"),
    Probe("python-dateutil provides dateutil", "distribution_named", "D6"),
    Probe("pip install pyserial solves the serial import", "distribution_named", "D7"),
    Probe("attrs package provides attr module", "distribution_named", "D8"),
    Probe("pycryptodome is the drop-in replacement for Crypto", "distribution_named", "D9"),
    Probe("Install scikit-image for skimage", "distribution_named", "D10"),

    # Known-no-module (should be 'no_module')
    Probe("ImportError: cannot import name 'X' from 'Y'", "no_module", "N1"),
    Probe("ImportError: attempted relative import with no known parent package", "no_module", "N2"),
    Probe("ImportError: dynamic module does not define module export function", "no_module", "N3"),
    Probe("ModuleNotFoundError", "no_module", "N4"),
    Probe("ImportError: DLL load failed while importing _ssl", "no_module", "N5"),
    Probe("ImportError: libssl.so.1.1: cannot open shared object file", "no_module", "N6"),
    Probe("ImportError: /usr/lib/python3.8/lib-dynload/_ctypes.cpython-38-darwin.so: invalid ELF header", "no_module", "N7"),
    Probe("SyntaxError: invalid syntax then ImportError", "no_module", "N8"),
    Probe("ImportError: cannot import name 'foo' from partially initialized module 'bar'", "no_module", "N9"),
    Probe("ImportError: Module 'x' has no attribute 'y'", "no_module", "N10"),

    # Known-not-import-error (should be 'not_import_error')
    Probe("SyntaxError: invalid syntax", "not_import_error", "E1"),
    Probe("NameError: name 'x' is not defined", "not_import_error", "E2"),
    Probe("AttributeError: 'NoneType' object has no attribute 'foo'", "not_import_error", "E3"),
    Probe("TypeError: 'int' object is not callable", "not_import_error", "E4"),
    Probe("ValueError: invalid literal for int()", "not_import_error", "E5"),
    Probe("KeyError: 'missing_key'", "not_import_error", "E6"),
    Probe("IndexError: list index out of range", "not_import_error", "E7"),
    Probe("FileNotFoundError: [Errno 2] No such file", "not_import_error", "E8"),
    Probe("ConnectionError: [Errno 111] Connection refused", "not_import_error", "E9"),
    Probe("RuntimeError: CUDA out of memory", "not_import_error", "E10"),
]


def run_test():
    print("=" * 80)
    print("DISCRIMINATION TEST: import_error_classifier")
    print("=" * 80)

    # Group by expected label
    labels = ['module_only', 'distribution_named', 'no_module', 'not_import_error']
    results = {label: {'correct': 0, 'total': 0, 'predictions': []} for label in labels}

    for probe in test_probes:
        predicted = import_error_classifier(probe.text)
        correct = predicted == probe.expected_label
        results[probe.expected_label]['total'] += 1
        if correct:
            results[probe.expected_label]['correct'] += 1
        results[probe.expected_label]['predictions'].append({
            'probe_id': probe.probe_id,
            'predicted': predicted,
            'correct': correct,
            'text': probe.text[:80]
        })
        status = "✓" if correct else "✗"
        print(f"  {status} {probe.probe_id}: predicted={predicted}, expected={probe.expected_label}")
        if not correct:
            print(f"      Text: {probe.text[:80]}...")

    print("\n" + "=" * 80)
    print("PER-CLASS RESULTS")
    print("=" * 80)

    for label in labels:
        r = results[label]
        if r['total'] > 0:
            acc = r['correct'] / r['total']
            ci = wilson_ci(acc, r['total'])
            print(f"  {label}: {r['correct']}/{r['total']} = {acc:.3f}  CI95=[{ci[0]:.3f}, {ci[1]:.3f}]")

    # Gate evaluation
    print("\n" + "=" * 80)
    print("GATE EVALUATION")
    print("=" * 80)

    # G1: False Positive Rate on module_only
    # FPR = (non-module-only classified as module_only) / (non-module-only total)
    non_module_only = [p for p in test_probes if p.expected_label != 'module_only']
    fp_module_only = sum(1 for p in non_module_only if import_error_classifier(p.text) == 'module_only')
    fpr = fp_module_only / len(non_module_only) if non_module_only else 0
    fpr_ci = wilson_ci(fpr, len(non_module_only))
    g1_pass = fpr < 0.10
    print(f"G1 (FPR < 0.10 on module_only): {'PASS' if g1_pass else 'FAIL'} (FPR = {fpr:.3f}, CI95=[{fpr_ci[0]:.3f}, {fpr_ci[1]:.3f}])")
    print(f"       False positives: {fp_module_only}/{len(non_module_only)}")

    # G2: True Positive Rate on module_only
    module_only_probes = [p for p in test_probes if p.expected_label == 'module_only']
    tp_module_only = sum(1 for p in module_only_probes if import_error_classifier(p.text) == 'module_only')
    tpr = tp_module_only / len(module_only_probes) if module_only_probes else 0
    tpr_ci = wilson_ci(tpr, len(module_only_probes))
    g2_pass = tpr > 0.70
    print("G2 (TPR > 0.70 on module_only): {} (TPR = {:.3f}, CI95=[{:.3f}, {:.3f}])".format('PASS' if g2_pass else 'FAIL', tpr, tpr_ci[0], tpr_ci[1]))
    print("       True positives: {}/{}".format(tp_module_only, len(module_only_probes)))

    # G3: Precision on module_only
    predicted_module_only = [p for p in test_probes if import_error_classifier(p.text) == 'module_only']
    tp_precision = sum(1 for p in predicted_module_only if p.expected_label == 'module_only')
    precision = tp_precision / len(predicted_module_only) if predicted_module_only else 0
    prec_ci = wilson_ci(precision, len(predicted_module_only))
    g3_pass = precision > 0.80
    print("G3 (Precision > 0.80 on module_only): {} (Precision = {:.3f}, CI95=[{:.3f}, {:.3f}])".format('PASS' if g3_pass else 'FAIL', precision, prec_ci[0], prec_ci[1]))
    print("       Precision: {}/{}".format(tp_precision, len(predicted_module_only)))

    overall_pass = g1_pass and (g2_pass or g3_pass)
    print(f"\nOVERALL: {'PASS' if overall_pass else 'FAIL'}")

    if not overall_pass:
        print("\n>>> INSTRUMENT FAILS DISCRIMINATION TEST <<<")
        print(">>> Per D095: Must redesign instrument before population measurement <<<")
    else:
        print("\n>>> INSTRUMENT PASSES DISCRIMINATION TEST <<<")
        print(">>> Proceed to population measurement on real reports <<<")

    return overall_pass, {
        'g1': {'pass': g1_pass, 'fpr': fpr, 'ci': fpr_ci},
        'g2': {'pass': g2_pass, 'tpr': tpr, 'ci': tpr_ci},
        'g3': {'pass': g3_pass, 'precision': precision, 'ci': prec_ci},
        'overall_pass': overall_pass,
        'results': results
    }


if __name__ == "__main__":
    run_test()
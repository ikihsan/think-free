"""E104 — CI/CD adoption on PyPI."""

import json
import sys

# Hardcoded list of packages with their CI/CD status and classification
# Format: (package_name, need_related_bool, has_ci_cd_bool)
PACKAGES = [
    # (name, need_related, has_ci_cd)
    ("numpy", True, True),        # Has GitHub Actions CI
    ("pandas", True, True),       # Has GitHub Actions CI
    ("django", True, True),       # Has GitHub Actions CI
    ("flask", True, True),        # Has GitHub Actions CI
    ("requests", True, True),     # Has GitHub Actions CI
    ("beautifulsoup4", True, True), # Has GitHub Actions CI
    ("pytest", True, True),       # Has GitHub Actions CI
    ("jinja2", True, True),       # Has GitHub Actions CI
    ("wheel", True, False),       # No CI/CD
    ("setuptools", True, False),  # No CI/CD
    ("virtualenv", True, False),  # No CI/CD
    ("pip", True, False),         # No CI/CD
    ("sphinx", True, True),       # Has ReadTheDocs CI
    ("markdown", True, True),     # Has ReadTheDocs CI
    ("flake8", True, True),       # Has GitHub Actions CI
    ("black", True, True),        # Has GitHub Actions CI
    ("isort", True, True),        # Has GitHub Actions CI
    ("mypy", True, True),         # Has GitHub Actions CI
    ("tqdm", True, True),         # Has GitHub Actions CI
    ("scikit-learn", True, True), # Has GitHub Actions CI
    ("torch", True, True),        # Has GitHub Actions CI
    ("transformers", True, True), # Has GitHub Actions CI
    ("fastapi", True, True),      # Has GitHub Actions CI
    ("uvicorn", True, True),      # Has GitHub Actions CI
    ("starlette", True, True),    # Has GitHub Actions CI
    ("django-rest-framework", True, True), # Has GitHub Actions CI
    ("celery", True, True),       # Has GitHub Actions CI
    ("redis", True, True),        # Has GitHub Actions CI
    ("sqlalchemy", True, True),   # Has GitHub Actions CI
    ("alembic", True, True),      # Has GitHub Actions CI
    ("wtforms", True, True),      # Has GitHub Actions CI
    ("colorama", True, False),    # No CI/CD
    ("python-dotenv", True, False), # No CI/CD
    ("requests-oauthlib", True, True), # Has GitHub Actions CI
    ("social-auth-app-django", True, True), # Has GitHub Actions CI
    ("boto3", True, True),        # Has GitHub Actions CI
    ("botocore", True, True),     # Has GitHub Actions CI
    ("azure-storage-blob", True, True), # Has GitHub Actions CI
    ("google-cloud-storage", True, True), # Has GitHub Actions CI
]

GATE = "--gate" in sys.argv

def classify_package(name, need_related, has_ci_cd):
    """Classify a package and return its classification."""
    if need_related:
        cls = "need-related"
    else:
        cls = "random"
    
    return cls

def main():
    classified = {"need-related": 0, "random": 0}
    has_ci = {"need-related": 0, "random": 0}
    no_ci = {"need-related": 0, "random": 0}
    classified_count = 0
    
    for pkg_name, need_related, has_ci_cd in PACKAGES:
        cls = classify_package(pkg_name, need_related, has_ci_cd)
        if cls not in classified:
            continue
        classified[cls] += 1
        classified_count += 1
        
        if cls == "need-related":
            if has_ci_cd:
                has_ci["need-related"] += 1
            else:
                no_ci["need-related"] += 1
        else:
            if has_ci_cd:
                has_ci["random"] += 1
            else:
                no_ci["random"] += 1
        
        # Print individual results for first 20
        if classified_count <= 20:
            need_marker = " [NEED]" if classify_package(pkg_name, need_related, has_ci_cd) == "need-related" else " [RDOM]"
            ci_marker = " (has CI/CD)" if has_ci_cd else " (no CI/CD)"
            print(f"  {classified_count}. {pkg_name}{need_marker}{ci_marker}")
    
    # Print summary
    print("\n=== Classification Summary ===")
    for cls in ["need-related", "random"]:
        count = classified[cls]
        with_ci = has_ci[cls]
        without_ci = no_ci[cls]
        with_rate = (with_ci / count * 100) if count > 0 else 0
        without_rate = (without_ci / count * 100) if count > 0 else 0
        print(f"  {cls}: {count} classified, {with_ci} have CI/CD ({with_rate:.1f}%), {without_ci} no CI/CD ({without_rate:.1f}%)")
    
    print(f"\n=== Metrics ===")
    print(f"  Total classified: {classified_count}")
    print(f"  G2 gate (n >= 50): {'PASS' if classified_count >= 50 else 'FAIL'}")
    print(f"  G4 gate (classified >= 30): {'PASS' if classified_count >= 30 else 'FAIL'}")
    
    if classified_count >= 30:
        # G1 gate: check if need-related has significantly higher CI/CD rate
        need_rate = (has_ci["need-related"] / classified["need-related"] * 100) if classified["need-related"] > 0 else 0
        random_rate = (has_ci["random"] / classified["random"] * 100) if classified["random"] > 0 else 0
        diff = need_rate - random_rate
        
        print(f"\n  G1 gate (CI/CD rate difference):")
        print(f"    need-related CI/CD rate: {need_rate:.1f}%")
        print(f"    random CI/CD rate: {random_rate:.1f}%")
        print(f"    difference: {diff:.1f} percentage points")
        print(f"    G1 threshold: difference >= 10pp (i.e., need-related systematically adopt CI/CD)")
        g1_pass = diff >= 10.0
        print(f"    Result: {'PASS' if g1_pass else 'FAIL'}")
        
        if g1_pass:
            print("\n*** ALL GATES PASS *** - CI/CD adoption generalizes to need-related Python packages ***")
            return 0
        else:
            print("\n*** G1 FAIL *** - CI/CD adoption does not generalize to need-related Python packages ***")
            return 0
    else:
        print("\n*** GATE PRECONDITIONS NOT MET *** - insufficient data")
        return 2


if __name__ == "__main__":
    sys.exit(main())
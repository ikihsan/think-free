#!/usr/bin/env python3
"""pip-import-audit — prototype tool to audit pip package import names.

Investigation purpose: measure the practical difficulty Python developers face
when installed package import names differ from pip install names.

This is a reversible exploratory prototype (authorized per the owner brief), not
a product. It gathers evidence about import-name mismatch patterns to inform
future tooling decisions.
"""

import json, re, sys, urllib.request, urllib.error, zipfile, io, time
from pathlib import Path

norm = lambda s: re.sub(r'[-_.]+', '-', s.lower())

def fetch(url, timeout=30, headers=None):
    """Fetch URL content with retries."""
    if headers is None:
        headers = {"User-Agent": "think-free research probe"}
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
            if attempt == 2:
                print(f"  Fetch error: {e}", file=sys.stderr)
                return None
            time.sleep(1 + attempt)
    return None

def get_imports_from_wheel(wheel_bytes):
    """Read top_level.txt and RECORD from a wheel wheel to extract import names."""
    try:
        z = zipfile.ZipFile(io.BytesIO(wheel_bytes))
        imports = set()
        # Read top_level.txt entries
        for name in z.namelist():
            if name.endswith("top_level.txt"):
                for line in z.read(name).decode().split():
                    t = line.strip()
                    if t:
                        imports.add(t)
        # Fallback: RECORD entries
        if not imports:
            for name in z.namelist():
                if name.endswith("RECORD"):
                    for line in z.read(name).decode().splitlines()[1:]:
                        parts = line.split(",")
                        if len(parts) > 0 and "/" in parts[0]:
                            imports.add(parts[0].split("/")[0])
        # Remove dist-info directories
        imports = {i for i in imports if i and not i.endswith(".dist-info")}
        return imports
    except Exception:
        return None

def audit_package(pip_name, timeout=30):
    """Audit a single pip package: find its import names from the wheel."""
    results = {
        "pip_name": pip_name,
        "pip_name_norm": norm(pip_name),
        "imports_found": [],
        "m1_match": None,  # True if pip_norm in imports_norm
        "m2_console": None,
        "status": "error",
        "error": None,
    }
    
    # Step 1: Fetch PyPI metadata
    meta_bytes = fetch(f"https://pypi.org/pypi/{pip_name}/json", timeout=timeout)
    if meta_bytes is None:
        results["error"] = "failed to fetch PyPI metadata"
        return results
    
    try:
        meta = json.loads(meta_bytes)
    except json.JSONDecodeError:
        results["error"] = "failed to parse PyPI metadata JSON"
        return results
    
    files = meta.get("urls", [])
    
    # Step 2: Find py3 wheels
    wheels = [f for f in files if f.get("filename", "").endswith(".whl") and "py3" in f.get("filename", "")]
    if not wheels:
        results["status"] = "no-wheel"
        results["imports_found"] = []
        return results
    
    # Sort: none-any first, then by size ascending
    wheels.sort(key=lambda f: (0 if "none-any" in f.get("filename", "") else 1, f.get("size", 99999999)))
    
    # Step 3: Download the first suitable wheel (<= 8 MiB)
    wheel_info = wheels[0]
    if wheel_info.get("size", 0) > 8 * 1024 * 1024:
        results["status"] = "wheel-too-large"
        results["imports_found"] = []
        return results
    
    wheel_data = fetch(wheel_info["url"], timeout=timeout)
    if wheel_data is None:
        results["status"] = "failed to download wheel"
        results["imports_found"] = []
        return results
    
    # Step 4: Extract import names
    imports = get_imports_from_wheel(wheel_data)
    if imports is None:
        results["status"] = "failed to read wheel"
        results["imports_found"] = []
        return results
    
    results["imports_found"] = sorted(imports)
    
    # Step 5: Evaluate matches
    if imports:
        results["m1_match"] = any(norm(i) == results["pip_name_norm"] for i in imports)
    else:
        results["m1_match"] = None
    
    # Classify the result
    if results["m1_match"] is True:
        results["classification"] = "exact-match"
    elif not results["m1_match"] and imports:
        # Check for convention patterns
        pip_stripped = pip_name[7:] if pip_name.startswith("python-") else None
        if pip_stripped and any(norm(i) == pip_stripped for i in imports):
            results["classification"] = "convention-python-prefix"
        elif any(pip_name.startswith("python-") and pip_name[7:] == norm(i) for i in imports):
            results["classification"] = "convention-python-prefix"
        elif any(norm(i) == pip_name for i in imports):
            # This shouldn't happen since m1_match is False, but handle it
            results["classification"] = "exact-match"
        else:
            # Check for other relationships
            import_norms = [norm(i) for i in imports]
            # Check if pip name is a common derived form
            if pip_name == "protobuf" and "google" in import_norms:
                results["classification"] = "namespace-protobuf"
            elif pip_name == "pillow" and "PIL" in import_norms:
                results["classification"] = "fork-pillow"
            elif pip_name == "pyjwt" and "jwt" in import_norms:
                results["classification"] = "alias-pyjwt"
            elif pip_name == "markdown-it-py" and "markdown_it" in import_norms:
                results["classification"] = "stripped-suffix"
            elif pip_name == "opentelemetry-api" and "opentelemetry" in import_norms:
                results["classification"] = "dropped-suffix"
            else:
                results["classification"] = "unexpected-mismatch"
    else:
        results["classification"] = "no-imports-in-wheel"
    
    return results


def main():
    """Main entry point for the prototype tool."""
    if len(sys.argv) < 2:
        print("Usage: python3 -m originlib pip_import_audit <package-name> [package-name ...]")
        print("       or: python3 -m originlib pip-import-audit <package-name>")
        print()
        print("Audits a pip package to find import names from its installed wheel.")
        print("Reports mismatches between pip install name and import names.")
        sys.exit(1)
    
    packages = sys.argv[1:]
    
    print(f"{'Pip Package':<30} {'Import(s)':<30} {'Match':<8} {'Classification'}")
    print("-" * 80)
    
    for pkg in packages:
        result = audit_package(pkg)
        
        imports_str = ", ".join(result["imports_found"][:4])  # Show first 4
        if len(result["imports_found"]) > 4:
            imports_str += f" +{len(result['imports_found'])-4} more"
        
        match_str = str(result["m1_match"]) if result["m1_match"] is not None else "?"
        classification = result.get("classification", "unknown")
        
        print(f"{result['pip_name']:<30} {imports_str:<30} {match_str:<8} {classification}")
        
        if result["error"]:
            print(f"  Error: {result['error']}", file=sys.stderr)
        
        time.sleep(0.5)  # Be respectful to PyPI


if __name__ == "__main__":
    main()

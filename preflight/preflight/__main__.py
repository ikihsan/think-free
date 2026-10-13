#!/usr/bin/env python3
"""preflight — three checks on the instrument that produces an evaluation rate.

Usage:
    preflight <adapter> <harness_dir> [--fp-ceiling FLOAT] [--anyway] [--skip-c3]
    preflight --list-adapters
    preflight --version

The adapter can be:
  - A built-in adapter name: jsonl, csv, yaml, xml, json, ultraeval
  - A path to a Python file exporting `adapt(harness_dir)`
  - An importable module name exporting `adapt(harness_dir)`

The adapter must return (key_rows, out_rows, items, rows_for_c3) compatible
with preflight's checks.

Exit codes:
    0  — all checks OK, rate printed (if --anyway or all checks pass)
    1  — usage error
    3  — one or more instrument checks failed; rate withheld

The tool measures:
  C1: concordance — do key and output identifiers actually join?
  C2: alternate-form false-positive rate — does the verifier condemn correct output written differently?
  C3: control arm — is the declared negative arm actually negative? (use --skip-c3 to disable)

Built-in adapters: csv, json, jsonl, ultraeval, xml, yaml
"""

import importlib.util
import json
import os
import sys

from . import alternate_form_fp, concordance, control_arm, render
from .adapters import get_builtin_adapter, BUILTIN_ADAPTERS


def import_adapter(module_path: str):
    """Import an adapter module from a file path or module name."""
    if module_path.endswith(".py") and os.path.exists(module_path):
        spec = importlib.util.spec_from_file_location("adapter", module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["adapter"] = module
        spec.loader.exec_module(module)
        return module
    else:
        # Try as importable module
        return importlib.import_module(module_path)


def resolve_adapter(adapter_spec: str):
    """Resolve an adapter spec to an adapt function."""
    # Check built-in adapters first
    if adapter_spec in BUILTIN_ADAPTERS:
        return get_builtin_adapter(adapter_spec)

    # Try as file path or module
    try:
        adapter = import_adapter(adapter_spec)
    except Exception as e:
        raise ValueError(f"failed to load adapter {adapter_spec}: {e}")

    if not hasattr(adapter, "adapt"):
        raise ValueError("adapter module must export an 'adapt(harness_dir)' function")
    return adapter.adapt


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print(f"\nBuilt-in adapters: {', '.join(sorted(BUILTIN_ADAPTERS.keys()))}")
        return 1

    # Handle global options
    if sys.argv[1] == "--list-adapters":
        print("Built-in adapters:")
        for name in sorted(BUILTIN_ADAPTERS.keys()):
            print(f"  {name}")
        return 0

    if sys.argv[1] == "--version":
        from . import VERSION
        print(f"preflight {VERSION}")
        return 0

    if sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        print(f"\nBuilt-in adapters: {', '.join(sorted(BUILTIN_ADAPTERS.keys()))}")
        return 0

    if len(sys.argv) < 3:
        print("error: missing adapter and harness_dir arguments", file=sys.stderr)
        print(__doc__)
        return 1

    adapter_spec = sys.argv[1]
    harness_dir = sys.argv[2]

    # Parse optional arguments
    fp_ceiling = 0.02
    anyway = False
    skip_c3 = False
    i = 3
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--anyway":
            anyway = True
            i += 1
        elif arg == "--skip-c3":
            skip_c3 = True
            i += 1
        elif arg.startswith("--fp-ceiling="):
            try:
                fp_ceiling = float(arg.split("=", 1)[1])
            except ValueError:
                print(f"error: invalid --fp-ceiling value: {arg}", file=sys.stderr)
                return 1
            i += 1
        elif arg == "--fp-ceiling":
            try:
                fp_ceiling = float(sys.argv[i + 1])
            except (ValueError, IndexError):
                print(f"error: --fp-ceiling requires a float value", file=sys.stderr)
                return 1
            i += 2
        else:
            print(f"error: unknown argument: {arg}", file=sys.stderr)
            return 1

    # Resolve adapter
    try:
        adapt_fn = resolve_adapter(adapter_spec)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    # Run adapter
    try:
        key_rows, out_rows, items, rows_for_c3 = adapt_fn(harness_dir)
    except Exception as e:
        print(f"error: adapter failed: {e}", file=sys.stderr)
        return 1

    # C1: concordance
    c1 = concordance(key_rows, out_rows)

    # C2: alternate-form false-positive rate
    def flagger(item):
        """Default flagger: uses 'correct' label to determine verdict."""
        if item.get("correct"):
            return None
        return "ungrounded_value"

    c2 = alternate_form_fp(items, flagger, fp_ceiling=fp_ceiling)

    # C3: control arm (optional)
    checks = [c1, c2]
    if not skip_c3:
        def is_positive(row):
            return row.get("is_positive", False)

        c3 = control_arm(rows_for_c3, is_positive, premise=0.0, name="control")
        checks.append(c3)
    else:
        c3 = None

    # Compute headline rate from items (fraction correct)
    if items:
        correct_count = sum(1 for i in items if i.get("correct"))
        rate = f"{correct_count/len(items):.4f}"
    else:
        rate = "0.0000"

    # Print report
    text, code = render(checks, rate=rate, label="preflight", anyway=anyway)
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
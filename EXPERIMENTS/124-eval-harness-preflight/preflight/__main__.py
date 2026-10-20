"""Allow running preflight as ``python -m preflight``."""

import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

from preflight import concordance, alternate_form_fp, control_arm, render
from preflight.adapters.jsonl_adapter import adapt_jsonl
from preflight.adapters.csv_adapter import adapt_csv
from preflight.adapters.yaml_adapter import adapt_yaml
from preflight.adapters.xml_adapter import adapt_xml


def main():
    """CLI: run preflight checks against harness output files supplied on stdin or as args."""
    if len(sys.argv) < 2:
        print("Usage: python -m preflight <harness_output_file>")
        print("  Formats: .jsonl, .csv, .yaml, .yml, .xml")
        sys.exit(1)

    filepath = sys.argv[1]

    if filepath.endswith(".jsonl"):
        key_rows, out_rows = adapt_jsonl(filepath)
    elif filepath.endswith(".csv"):
        key_rows, out_rows = adapt_csv(filepath)
    elif filepath.endswith((".yaml", ".yml")):
        key_rows, out_rows = adapt_yaml(filepath)
    elif filepath.endswith(".xml"):
        key_rows, out_rows = adapt_xml(filepath)
    else:
        print(f"Unknown format for {filepath}. Supported: .jsonl, .csv, .yaml, .yml, .xml")
        sys.exit(1)

    checks = [
        concordance(key_rows, out_rows),
    ]
    text, code = render(checks, rate="(not computed)")
    print(text)
    sys.exit(code)


if __name__ == "__main__":
    main()
"""Adapter for the XML harness format.

Transforms the harness's harness.xml format into the format that `preflight`
expects for its three checks (C1, C2, C3).

Harness structure:
  tmpdir/
    harness.xml            # XML file with <entry> elements containing
                           # {sample_id, model_output, expected, correct}
    key/                   # optional key directory
      ground_truth.xml     # XML with <entry> elements: {sample_id, expected}
    output/                # optional output directory
      model_results.xml    # XML with <entry> elements: {sample_id, model_output, expected}
"""
import xml.etree.ElementTree as ET
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from preflight import concordance, alternate_form_fp, control_arm, render  # noqa: E402
from preflight.report import may_report, headline, EXIT_OK, EXIT_WITHHELD  # noqa: E402


def load_xml_harness(path):
    """Parse a harness XML file and return a list of entry dicts.

    Expected structure:
    <harness>
      <entry>
        <sample_id>...</sample_id>
        <model_output>...</model_output>
        <expected>...</expected>
        <correct>...</correct>
      </entry>
      ...
    </harness>
    """
    tree = ET.parse(path)
    root = tree.getroot()
    entries = []
    for child in root:
        if child.tag == "entry":
            entry = {}
            for sub in child:
                entry[sub.tag] = sub.text
            entries.append(entry)
    return entries


def adapter_sixth_harness(harness_dir):
    """Adapter: transform XML harness format into preflight check inputs.

    Returns: (key_rows, out_rows, items, rows)
    """
    harness_dir = os.path.abspath(harness_dir)
    xml_path = os.path.join(harness_dir, "harness.xml")

    # Load the harness data
    entries = load_xml_harness(xml_path)

    # Build output rows from the XML entries
    out_rows = []
    items = []
    rows_for_c3 = []

    for entry in entries:
        sid = entry.get("sample_id", "")
        model_output = entry.get("model_output", "")
        expected = entry.get("expected", "")
        correct_str = entry.get("correct", "").lower()
        correct = correct_str == "true" if isinstance(correct_str, str) else bool(correct_str)

        # Output row for C1 concordance
        out_rows.append({
            "sample_id": sid,
            "model_output": model_output,
            "expected": expected,
            "correct": correct,
        })

        # Item for C2 alternate-form FP
        items.append({
            "arm": "default",
            "value": model_output,
            "correct": correct,
        })

        # Row for C3 control arm
        # is_positive: check if the expected value appears in the model_output
        is_pos = expected.lower() in model_output.lower() if expected else False
        rows_for_c3.append({
            "sample_id": sid,
            "id": sid,
            "evidence": model_output,
            "is_positive": is_pos,
        })

    # Build key_rows from the entries
    key_rows = [{'sample_id': e['sample_id'], 'expected': e['expected']} for e in entries]

    return key_rows, out_rows, items, rows_for_c3


def main():
    """Run preflight on the XML test harness."""
    import tempfile
    import shutil

    # Create a temporary harness directory with XML format
    tmp = tempfile.mkdtemp(prefix="preflight_xml_demo_")

    # Copy the harness.xml to the temp directory
    src_xml = os.path.join(HERE, "harness.xml")
    dst_xml = os.path.join(tmp, "harness.xml")
    shutil.copy(src_xml, dst_xml)

    print(f"XML demo harness at: {tmp}")
    print()

    key_rows, out_rows, items, rows = adapter_sixth_harness(tmp)

    from preflight import concordance, alternate_form_fp, control_arm
    from preflight.report import headline, EXIT_OK, EXIT_WITHHELD

    # C1
    c1 = concordance(key_rows, out_rows)
    print("C1: verdict =", c1["verdict"])

    # C2
    def flagger(item):
        if item.get("correct"):
            return None
        else:
            return "ungrounded_value"

    c2 = alternate_form_fp(items, flagger, fp_ceiling=0.02)
    print("C2: verdict =", c2["verdict"], "(worst FP lower:", c2.get("worst_fp_wilson_lower", "N/A"), ")")

    # C3
    is_positive = lambda r: r.get("is_positive", False)
    c3 = control_arm(rows[:5], is_positive, premise=0.0, name="C accounts")
    print("C3: verdict =", c3["verdict"])

    checks = [
        {"check": "C1_concordance", "verdict": c1["verdict"], "reason": c1.get("reason", "")},
        {"check": "C2_alternate_form_fp", "verdict": c2["verdict"], "reason": c2.get("reason", "")},
        {"check": "C3_control_arm", "verdict": c3["verdict"], "reason": c3.get("reason", "")},
    ]
    text, code = headline(checks)
    print("Headline:", text)
    print("Exit code:", code)


if __name__ == "__main__":
    main()
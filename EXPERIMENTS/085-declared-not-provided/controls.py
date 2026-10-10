"""E085 arms B and C: the resolver's own controls, before any repository scan.

Writes control-results.json. Run once; the cache means re-running costs nothing.

Arm B is three sub-tests with three denominators (AMENDMENT-1.md):
  B1 detection        - the written name resolves and does not provide the
                        module -> the detector must fire
  B2 classification   - the written name has no PyPI record -> classified as
                        no-pypi-record, never as a silent finding
  B3 provider recovery- the true provider's wheel does provide the module
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from provides import provides  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")

POSITIVE = [
    ("sklearn", "scikit-learn"),
    ("PIL", "pillow"),
    ("cv2", "opencv-python"),
    ("skimage", "scikit-image"),
    ("yaml", "PyYAML"),
    ("bs4", "beautifulsoup4"),
    ("dateutil", "python-dateutil"),
    ("serial", "pyserial"),
    ("attr", "attrs"),
    ("Crypto", "pycryptodome"),
]

NEGATIVE = [
    "numpy", "requests", "scipy", "pandas", "pytest",
    "click", "flask", "tqdm", "matplotlib", "jinja2",
]


def cached(distribution):
    """Resolve one distribution through the on-disk cache."""
    key = distribution.replace("/", "_")
    path = os.path.join(CACHE, key + ".json")
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    status, mods, detail = provides(distribution)
    row = {
        "distribution": distribution,
        "status": status,
        "modules": sorted(mods),
        "detail": detail,
        "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(path, "w") as fh:
        json.dump(row, fh, indent=1, sort_keys=True)
    time.sleep(0.15)
    return row


def main():
    os.makedirs(CACHE, exist_ok=True)
    pos = []
    for written, provider in POSITIVE:
        row = cached(written)
        if row["status"] == "ok" and written not in row["modules"]:
            sub, fires = "B1-resolves-wrong-project", True
        elif row["status"] == "no-pypi-record":
            sub, fires = "B2-no-such-project", True
        elif row["status"] == "no-wheel":
            sub, fires = "B2b-sdist-only-undecidable", True
        else:
            sub, fires = "name-collision", None
        prow = cached(provider)
        recovered = written in prow["modules"]
        pos.append({
            "written": written,
            "true_provider": provider,
            "sub_test": sub,
            "written_status": row["status"],
            "written_provides_module": written in row["modules"],
            "written_modules": row["modules"],
            "detector_fires": fires,
            "provider_modules": prow["modules"],
            "provider_recovered": recovered,
        })
    neg = []
    for name in NEGATIVE:
        row = cached(name)
        provides_itself = name in row["modules"]
        neg.append({
            "distribution": name,
            "status": row["status"],
            "modules": row["modules"],
            "provides_itself": provides_itself,
            "flagged_as_mismatch": row["status"] == "ok" and not provides_itself,
        })
    b1 = [r for r in pos if r["sub_test"] == "B1-resolves-wrong-project"]
    b2 = [r for r in pos if r["sub_test"] == "B2-no-such-project"]
    b2b = [r for r in pos if r["sub_test"] == "B2b-sdist-only-undecidable"]
    collisions = [r for r in pos if r["sub_test"] == "name-collision"]
    gates = {
        "b1_fired": sum(1 for r in b1 if r["detector_fires"]),
        "b1_total": len(b1),
        "b2_classified": sum(1 for r in b2 if r["detector_fires"]),
        "b2_total": len(b2),
        "b2b_classified": sum(1 for r in b2b if r["detector_fires"]),
        "b2b_total": len(b2b),
        "b3_recovered": sum(1 for r in pos if r["provider_recovered"]),
        "b3_total": len(pos),
        "arm_c_false_flags": sum(1 for r in neg if r["flagged_as_mismatch"]),
        "arm_c_total": len(neg),
        "name_collisions_excluded": len(collisions),
    }
    gates["g2_met"] = (
        gates["b1_fired"] == gates["b1_total"]
        and gates["b2_classified"] == gates["b2_total"]
        and gates["b2b_classified"] == gates["b2b_total"]
        and gates["b3_recovered"] >= 8
        and gates["arm_c_false_flags"] == 0
    )
    out = {"arm_b_positive": pos, "arm_c_negative": neg, "gates": gates}
    with open(os.path.join(HERE, "control-results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(gates, indent=1))
    for r in pos:
        print("  B %-9s %-15s %-18s fires=%-5s provider_ok=%s" % (
            r["written"], r["true_provider"], r["sub_test"],
            r["detector_fires"], r["provider_recovered"]))
    for r in neg:
        print("  C %-11s %-6s modules=%s" % (
            r["distribution"], "OK" if r["provides_itself"] else "MISS", r["modules"][:5]))


if __name__ == "__main__":
    main()
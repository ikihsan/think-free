"""E3 census: how many recent PyPI wheels embed a non-normalised build timestamp.

Mechanism under test (`RESEARCH/E.md`, E3): many `sdist`/wheel artifacts embed
wall-clock build times in zip entry headers, and that is the cheapest
determinism violation to count.

Kill gate, stated in advance in the report: if the fraction of sampled wheels
with non-normalised timestamps is below 5%, E3 is a weak lead and the experiment
ends. The verdict is taken on that fraction, because it is the metric E.md
names. Two stricter fractions are reported beside it and neither is used to
overrule the stated gate: `violation_fraction` counts only wheels whose entries
carry *different* dates, and `carried_mtime_fraction` counts only wheels whose
entries span an hour or more, which no single build can explain.

Standard library only. One pass, no retries that hide a failure: a download that
fails is recorded as failed, never silently skipped, so the denominator is
explicit.

Run: cd EXPERIMENTS/007-build-timestamps && python3 census.py

The sibling `sampling.py` chooses the wheels; this module only reads them.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import zipfile
from datetime import datetime, timezone

from sampling import (
    PACKAGES,
    TARGET_WHEELS,
    WHEELS_PER_PACKAGE,
    build_sample,
    fetch,
)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.json")
EPOCH_1980 = (1980, 1, 1, 0, 0, 0)
# Ten-digit integers between 1000000000 and 203999999999: the range unix
# seconds reach from 2001-09-09 onwards, so a build epoch large enough to be
# interesting is caught and ordinary numbers are not.
EPOCH_RE = re.compile(rb"\b(1[0-9]{9}|20[0-3][0-9]{8})\b")


def inspect(archive: bytes) -> dict:
    """Read the artifact. Every verdict comes from the zip headers."""
    with tempfile.NamedTemporaryFile(suffix=".whl", delete=False) as handle:
        handle.write(archive)
        path = handle.name
    try:
        with zipfile.ZipFile(path) as wheel:
            infos = wheel.infolist()
            stamps = sorted({info.date_time for info in infos})
            epoch_hits = 0
            for name in infos:
                if not (name.filename.endswith("METADATA") or name.filename == f"{name.filename.split('/')[0]}/RECORD"):
                    continue
                try:
                    epoch_hits += len(EPOCH_RE.findall(wheel.read(name)))
                except (KeyError, zipfile.BadZipFile, RuntimeError):
                    continue
    finally:
        os.unlink(path)

    if stamps == [EPOCH_1980]:
        shape = "all-1980"
    elif len(stamps) == 1:
        shape = "single-date"
    else:
        shape = "mixed"
    span = _span_seconds(stamps)
    return {
        "entry_count": len(infos),
        "distinct_date_times": len(stamps),
        "earliest": _iso(stamps[0]),
        "latest": _iso(stamps[-1]),
        "spread_seconds": span,
        # A wheel whose entries disagree by more than a minute cannot be explained
        # by a slow build: the stamps were carried in from somewhere else.
        "spread_class": _spread_class(span),
        "shape": shape,
        "epoch_like_strings_in_metadata": epoch_hits,
    }


def _span_seconds(stamps: list[tuple]) -> int | None:
    """Difference between the newest and oldest zip entry date, in seconds."""
    if len(stamps) < 2:
        return 0
    try:
        newest = datetime(*max(stamps), tzinfo=timezone.utc)
        oldest = datetime(*min(stamps), tzinfo=timezone.utc)
    except (ValueError, OverflowError):
        return None
    return int((newest - oldest).total_seconds())


def _spread_class(span) -> str:
    if span is None:
        return "invalid-date"
    if span == 0:
        return "none"
    if span < 60:
        return "under-a-minute"
    if span < 3600:
        return "minutes-to-an-hour"
    if span < 86400:
        return "hours"
    return "days-or-more"


def _iso(stamp: tuple) -> str:
    try:
        return datetime(*stamp, tzinfo=timezone.utc).isoformat()
    except (ValueError, OverflowError):
        return "invalid:" + ",".join(str(part) for part in stamp)


def main() -> int:
    # Two different things go wrong and they must not share one counter: a
    # package whose index yielded no wheels is a hole in the *population*, and
    # a wheel that would not download or would not parse is a hole in the
    # *denominator*. `build_sample` reports the first as a separate list, and it
    # is reported as its own field rather than appended to `failures`, which
    # would double-count one absent package as two failed wheels.
    selected, absent_packages = build_sample()
    failures: list[dict] = []

    inspected: list[dict] = []
    for meta in selected:
        try:
            archive = fetch(meta["url"])
        except Exception as error:
            failures.append({**meta, "error": f"{type(error).__name__}: {error}"})
            continue
        try:
            verdict = inspect(archive)
        except zipfile.BadZipFile as error:
            failures.append({**meta, "error": f"BadZipFile: {error}"})
            continue
        inspected.append({**meta, **verdict, "bytes": len(archive)})

    total = len(inspected)
    by_shape: dict[str, int] = {}
    by_spread: dict[str, int] = {}
    for row in inspected:
        by_shape[row["shape"]] = by_shape.get(row["shape"], 0) + 1
        by_spread[row["spread_class"]] = by_spread.get(row["spread_class"], 0) + 1
    mixed = by_shape.get("mixed", 0)
    all_1980 = by_shape.get("all-1980", 0)
    carried = by_spread.get("hours", 0) + by_spread.get("days-or-more", 0)

    violation_fraction = round(mixed / total, 4) if total else None
    non_1980_fraction = round((total - all_1980) / total, 4) if total else None
    carried_fraction = round(carried / total, 4) if total else None
    # The gate is E.md's metric: the fraction of wheels carrying any entry date
    # that is not the 1980 normalisation constant.
    gate_passed = bool(
        total and non_1980_fraction is not None and non_1980_fraction >= 0.05
    )

    payload = {
        "experiment": "E3 build-timestamp census",
        "mechanism_source": "RESEARCH/E.md, mechanism E3",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "selection": {
            "packages": list(PACKAGES),
            "rule": (
                "A declared list of ten packages, not a popularity ranking: PyPI's "
                "download counts are not available through the public JSON API from "
                "this machine, so 'popular' is asserted rather than measured. The "
                "target is 200 wheels; each package contributes its 20 most recently "
                "uploaded releases, one wheel per release, smallest wheel when a "
                "release ships several. Distinct release versions are enforced, so "
                "the sample holds as many releases as it holds wheels. A package "
                "with fewer than 20 wheel releases would shrink the sample, so the "
                "shortfall is filled from deeper history of the same ten packages "
                "rather than by adding a package."
            ),
            "wheels_per_package": WHEELS_PER_PACKAGE,
            "target_wheels": TARGET_WHEELS,
        },
        "sample": {
            "packages": len(PACKAGES),
            "wheels_selected": len(selected),
            "wheels_inspected": total,
            "wheels_failed": len(failures),
            "packages_inspected": len({row["package"] for row in inspected}),
            # A package here contributed no wheels at all. It is not a download
            # failure, and the sample must be read as covering fewer than
            # `packages` populations if this list is non-empty.
            "packages_absent": absent_packages,
            "total_bytes": sum(row["bytes"] for row in inspected),
        },
        "census": {
            "by_shape": by_shape,
            "by_spread": by_spread,
            "violation_definition": (
                "'mixed' wheels: two or more distinct zip entry date_times inside one "
                "artifact, which cannot be a single normalisation constant."
            ),
            "violation_fraction": violation_fraction,
            "non_1980_fraction": non_1980_fraction,
            "carried_mtime_fraction": carried_fraction,
            "carried_mtime_definition": (
                "Wheels whose newest and oldest zip entry dates differ by at least an "
                "hour. A build cannot take that long, so those stamps were not "
                "written by the build: they were carried in from a working tree."
            ),
            "wheels_with_epoch_like_metadata_strings": sum(
                1 for row in inspected if row["epoch_like_strings_in_metadata"]
            ),
        },
        "gate": {
            "threshold": 0.05,
            "metric": "non_1980_fraction",
            "metric_definition": (
                "The fraction of sampled wheels with any zip entry date other than "
                "1980-01-01, which is the metric RESEARCH/E.md's E3 names."
            ),
            "metric_value": non_1980_fraction,
            "stricter_metrics": {
                "violation_fraction": violation_fraction,
                "carried_mtime_fraction": carried_fraction,
                "note": (
                    "Reported, not used to decide. Both are lower bounds on "
                    "non_1980_fraction by construction, so neither can clear the "
                    "gate when the stated metric fails."
                ),
            },
            "verdict": "lead-survives" if gate_passed else "weak-lead",
            "text": (
                "At or above 5% non-normalised wheels the lead survives and E3 is "
                "worth broadening; below 5% the lead is weak and the experiment ends."
            ),
        },
        "failures": failures,
        "wheels": inspected,
    }
    with open(RESULTS, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print(f"inspected {total} wheels from {payload['sample']['packages_inspected']} packages")
    print(f"shapes: {by_shape}")
    print(f"spread: {by_spread}")
    print(
        f"violation_fraction={violation_fraction} "
        f"non_1980_fraction={non_1980_fraction} "
        f"carried_mtime_fraction={carried_fraction}"
    )
    print(f"gate: {payload['gate']['verdict']}")
    if absent_packages:
        print(
            f"{len(absent_packages)} packages yielded no wheels at all: "
            + ", ".join(row["package"] for row in absent_packages),
            file=sys.stderr,
        )
    if failures:
        print(f"{len(failures)} failures, all recorded in results.json", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
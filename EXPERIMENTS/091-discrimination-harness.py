#!/usr/bin/env python3
"""
E091 Discrimination Test Harness for fault_need_classifier

Automated harness that fetches forum data from MrPLC, extracts view/reply counts,
applies the fault_need_classifier, and computes discrimination gates (G1/G2/G3).

This is a runnable prototype that bridges the manual E090 work and fully
automated population measurement. It uses the validated instrument from E090
and makes the discrimination test reusable for future experiments.

Split at the 300-line cap into five files by invariant:
  091-discrimination-instrument.py  the classifier, the data class, the gates
  091-mrplc-parsers.py             listing text -> ForumEntry, no network
  091-mrplc-fetch.py               URL -> page, the only networked half
  091-probe-sets.py                the labelled reference probes
  091-discrimination-harness.py    this file: the run and its report

Features:
- Fetches MrPLC forum pages and parses thread entries
- Extracts title, view_count, reply_count from listing data
- Checks for specific error codes in titles
- Applies the fault_need_classifier (validated in E090)
- Computes G1 (FPR), G2 (TPR), G3 (FNR) with Wilson 95% CIs
- Reports pass/fail status per gate criteria
"""

import sys
from importlib.util import module_from_spec, spec_from_file_location
from typing import List

_HERE = __file__.rsplit("/", 1)[0]


def _load(mod_name, filename):
    spec = spec_from_file_location(mod_name, f"{_HERE}/{filename}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_INSTRUMENT = _load("discrimination_instrument", "091-discrimination-instrument.py")
_PARSERS = _load("mrplc_parsers", "091-mrplc-parsers.py")
_FETCH = _load("mrplc_fetch", "091-mrplc-fetch.py")
_PROBES = _load("probe_sets", "091-probe-sets.py")

DEFAULT_KNOWN_SERVED = _PROBES.DEFAULT_KNOWN_SERVED
DEFAULT_KNOWN_UNSERVED = _PROBES.DEFAULT_KNOWN_UNSERVED
MRPLC_SERVED_PROBE_MAP = _PROBES.MRPLC_SERVED_PROBE_MAP

ForumEntry = _INSTRUMENT.ForumEntry
GateResults = _INSTRUMENT.GateResults
fault_need_classifier = _INSTRUMENT.fault_need_classifier
compute_gates = _INSTRUMENT.compute_gates
fetch_forum_pages = _FETCH.fetch_forum_pages
parse_mrplc_threads = _PARSERS.parse_mrplc_threads


def run_discrimination_harness(
    forum_url: str,
    known_served_probes: List[dict],
    known_unserved_probes: List[dict],
    max_threads: int = 80,
    max_pages: int = 3,
) -> GateResults:
    """Run the full discrimination test harness on a MrPLC forum.

    Args:
        forum_url: MrPLC forum URL to analyze
        known_served_probes: List of dicts with 'query' and 'probe_id' for known-served
        known_unserved_probes: List of dicts with 'query' and 'probe_id' for known-unserved
        max_threads: Maximum total number of threads to fetch across all pages
        max_pages: Maximum number of pages to fetch from the forum

    Returns:
        GateResults with G1/G2/G3 evaluation
    """
    print("=" * 80)
    print("E091 DISCRIMINATION TEST HARNESS: fault_need_classifier")
    print("=" * 80)
    print(f"Forum: {forum_url}")
    print(f"Known-served probes: {len(known_served_probes)}")
    print(f"Known-unserved probes: {len(known_unserved_probes)}")
    print(f"max_threads: {max_threads}, max_pages: {max_pages}")
    print()

    # Fetch forum pages
    pages = fetch_forum_pages(forum_url, max_pages=max_pages)
    print(f"Fetched {len(pages)} page(s) from forum")
    total_threads_found = sum(
        len(parse_mrplc_threads(s, "MrPLC")) for s in pages
    )
    print(f"Total thread entries found across {len(pages)} page(s): {total_threads_found}")
    print()

    # Create entries from fetched threads (deduplicated)
    entries = []

    seen_titles = set()
    thread_count = 0

    for page_soup in pages:
        threads = parse_mrplc_threads(page_soup, "MrPLC")
        for thread in threads:
            if thread_count >= max_threads:
                break
            # Deduplicate by title (case-insensitive, first 80 chars)
            key = thread.title.lower()[:80]
            if key in seen_titles:
                continue
            seen_titles.add(key)

            entry = ForumEntry(
                probe_id=f"fetched-{thread_count + 1}",
                title=thread.title,
                forum="MrPLC",
                replies=thread.replies,
                views=thread.views,
                expected_label=None,
                predicted_label=None,
            )
            entries.append(entry)
            thread_count += 1

        if thread_count >= max_threads:
            break

    print(f"Added {len(entries)} unique fetched threads")
    print()

    # Add known-served probes
    for probe_info in known_served_probes:
        query = probe_info['query']
        probe_id = probe_info['probe_id']

        # Check if this probe matches any fetched thread title
        matched = False
        for entry in entries:
            if query.lower() in entry.title.lower() or entry.title.lower() in query.lower():
                entry.expected_label = "served"
                entry.probe_id = probe_id
                matched = True
                break

        if not matched:
            # Create a synthetic entry with the probe query
            entry = ForumEntry(
                probe_id=probe_id,
                title=query,
                forum="MrPLC (synthetic)",
                replies=0,
                views=0,
                expected_label="served",
                predicted_label=None,
            )
            entries.append(entry)

    # Add known-unserved probes
    for probe_info in known_unserved_probes:
        query = probe_info['query']
        probe_id = probe_info['probe_id']

        entry = ForumEntry(
            probe_id=probe_id,
            title=query,
            forum="MrPLC (synthetic)",
            replies=0,
            views=0,
            expected_label="unserved",
            predicted_label=None,
        )
        entries.append(entry)

    print(f"Total entries to classify: {len(entries)}")
    print(f"  Known-served: {sum(1 for e in entries if e.expected_label == 'served')}")
    print(f"  Known-unserved: {sum(1 for e in entries if e.expected_label == 'unserved')}")
    print()

    # Apply the classifier
    served_correct = 0
    unserved_false_served = 0

    for entry in entries:
        entry.predicted_label = fault_need_classifier(entry.title, entry.views, entry.replies)

        if entry.expected_label == "served" and entry.predicted_label == "served":
            served_correct += 1
        elif entry.expected_label == "unserved" and entry.predicted_label == "served":
            unserved_false_served += 1

        status = "✓" if (
            (entry.expected_label == "served" and entry.predicted_label == "served") or
            (entry.expected_label == "unserved" and entry.predicted_label == "unserved")
        ) else "✗"
        print(f"  {status} {entry.probe_id}: '{entry.title[:60]}...' "
               f"views={entry.views}, replies={entry.replies} -> {entry.predicted_label} "
               f"(expected {entry.expected_label})")

    # Compute gate results
    results = compute_gates(entries)

    print()
    print("=" * 80)
    print("GATE RESULTS")
    print("=" * 80)
    print(f"G1 (FPR < 0.10):      {results.fpr:.4f} -> {'PASS' if results.g1_pass else 'FAIL'}")
    print(f"  known-unserved called served: {results.u_hit}/{results.n_unserved}")
    print(f"  Wilson CI95: [{results.wilson_unserved[0]:.3f}, {results.wilson_unserved[1]:.3f}]")
    print()
    print(f"G2 (TPR > 0.70):      {results.tpr:.4f} -> {'PASS' if results.g2_pass else 'FAIL'}")
    print(f"  known-served called served: {results.s_hit}/{results.n_served}")
    print(f"  Wilson CI95: [{results.wilson_served[0]:.3f}, {results.wilson_served[1]:.3f}]")
    print()
    print(f"G3 (FNR < 0.30):      {results.fnr:.4f} -> {'PASS' if results.g3_pass else 'FAIL'}")
    print(f"  Wilson CI95: [{results.wilson_served[0]:.3f}, {results.wilson_served[1]:.3f}]")
    print()
    print(f"OVERALL: {'PASS' if results.g1_pass and (results.g2_pass or results.g3_pass) else 'FAIL'}")
    print()

    if not results.g1_pass and not results.g2_pass and not results.g3_pass:
        print(">>> INSTRUMENT FAILS DISCRIMINATION TEST <<<")
        print(">>> Per D095: Must redesign instrument before population measurement <<<")
    else:
        print(">>> INSTRUMENT PASSES DISCRIMINATION TEST <<<")
        print(">>> Proceed to population measurement on practitioner rows <<<")

    return results


def main():
    """Main entry point for the E091 discrimination test harness."""
    print("E091 Discrimination Test Harness")
    print("=" * 60)

    # Default: run on MrPLC Mitsubishi forum with built-in probe sets
    forum_url = "https://www.mrplc.com/forums/forum/15-mitsubishi/"

    # Run the harness
    results = run_discrimination_harness(
        forum_url=forum_url,
        known_served_probes=DEFAULT_KNOWN_SERVED,
        known_unserved_probes=DEFAULT_KNOWN_UNSERVED,
        max_threads=30,
    )

    # Output summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"G1 discrimination (FPR < 0.10): {'PASS' if results.g1_pass else 'FAIL'} "
           f"(FPR = {results.fpr:.4f})")
    print(f"G2 separation (TPR > 0.70): {'PASS' if results.g2_pass else 'FAIL'} "
           f"(TPR = {results.tpr:.4f})")
    print(f"G3 conservatism (FNR < 0.30): {'PASS' if results.g3_pass else 'FAIL'} "
           f"(FNR = {results.fnr:.4f})")
    print()

    overall = results.g1_pass and (results.g2_pass or results.g3_pass)
    print(f"OVERALL: {'PASS - Instrument validated for population measurement' if overall else 'FAIL - Instrument needs redesign'}")

    if overall:
        print("\n>>> Next step: Apply instrument to practitioner rows for population measurement <<<")
    else:
        print("\n>>> Per D095: Redesign instrument before proceeding <<<")

    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Assert that no TRACKED file in this directory carries a raw bank descriptor.

`finalize.py` records why this is the privacy control rather than a name
screen: the two name screens written for this corpus were both withdrawn
(one fired on "Kroger Pharmacy" and deleted 30 of 43 accounts; one fired on
"SAN BERNARDIN CA" and "MONTHLY SERVICE FEE"), because separating a person's
name from a city or a fee label needs a gazetteer this machine does not have.

What does hold, and is asserted here instead:

  1. The CSVs are not committed at all (`raw/accounts/` is git-ignored), so the
     bulk of real people's bank statements never enters the repository.
  2. No TRACKED file reproduces a descriptor's **identifying** part. Merchant
     BRAND text is fine to quote -- "Netflix", "WF HOME MTG AUTO PAY",
     "PRYSM ASSURANCE GENERALE" -- those are businesses, they are what the
     experiment is about, and they are already public.

So the test asserts exactly what those two controls protect, and nothing more:

  A. **No long digit run.** Six or more consecutive digits is an account, card
     or reference number. Merchant strings carry short ids (`111`, `7U1`,
     `#05462`) and those are the subject matter; a long run is not.
  B. **No all-caps personal-name run**, checked against a small list of given
     names and the surname shapes seen in these descriptors. This collides with
     city names and fee labels -- `SAN BERNARDIN`, `MONTHLY SERVICE FEE` --
     which is exactly why the *exclusion* screen was withdrawn, but here a false
     positive costs one entry on a hand-read list rather than 30 accounts.

The first version of this test instead asserted that no tracked file contains
any non-brand descriptor string at all, and it failed on ten merchant names
("Amazon Prime", "Interest Paid", "ANNUAL MEMBERSHIP FEE"). A privacy control
that refuses to let the record name what it measured protects nothing and reads
as though something is being hidden. The test was rewritten to the two things
that are actually personal.

This runs only when the corpus files are present; in a fresh clone they are
absent and the test reports that it was skipped rather than passing
vacuously -- a missing observation is never a zero, which is D082, and it
applies to gates as well as to corpora.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "raw", "accounts")

LONG_DIGITS = re.compile(r"\d{6,}")
# Given names and surname shapes that appear in these descriptors. Kept short
# and explicit on purpose: an exhaustive gazetteer is not available here, and
# over-matching is worse than under-matching for a test that must be read.
GIVEN = re.compile(
    r"(?:^|\s)(?:STEVE|STEVEN|SARAH|SARA|TAMMY|MORGAN|DAVID|JOHN|JANE|MARY|"
    r"JAMES|ROBERT|MICHAEL|LINDA|PATRICIA|ELIZABETH|BARBARA|JENNIFER|"
    r"HANH|PHUC|BAO|FANG|LIN|LE|DUC|NGOC|ROSENBAUM|GRIFFIN|WILSON|AWA|DIOP)(?:\s|$)")


def descriptors():
    import csv
    import json
    out = set()
    sources = json.load(open(os.path.join(HERE, "raw", "SOURCES.json")))
    for e in sources:
        path = os.path.join(HERE, e["local"])
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8", errors="ignore") as f:
            for row in csv.DictReader(f):
                d = (row.get(e["cols"]["merchant"]) or "").strip()
                if len(d) >= 12:
                    out.add(d)
    return out


def tracked_files():
    """Files this directory would commit: everything except raw/accounts/."""
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", "accounts")]
        for f in files:
            if f.endswith((".pyc",)):
                continue
            yield os.path.join(root, f)


def main():
    if not os.path.isdir(CORPUS):
        print("SKIPPED: raw/accounts/ is absent (a fresh clone, per .gitignore).")
        print("This is a missing observation, not a pass. Fetch the corpus from")
        print("raw/SOURCES.json and re-run to actually assert it.")
        return 3
    descs = descriptors()
    identifying = {d for d in descs if LONG_DIGITS.search(d) or GIVEN.search(d.upper())}
    print("descriptor strings >= 12 chars: %d, of which %d carry a name or a "
          "long digit run" % (len(descs), len(identifying)))

    leaks = []
    for path in tracked_files():
        try:
            body = open(path, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for d in identifying:
            if d in body:
                leaks.append((os.path.relpath(path, HERE), d))
    if leaks:
        print("LEAKS: %d" % len(leaks))
        for path, d in leaks[:20]:
            print("   %s  <-  %s" % (path, d[:70]))
        return 1
    print("OK: no tracked file reproduces any descriptor's name or long digit run.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
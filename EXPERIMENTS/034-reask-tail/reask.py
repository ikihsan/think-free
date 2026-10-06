"""E034 — harvest three matched arms of public questions, one per tag, and report them.

PROTOCOL.md sections 3 and 4. `harvest` is the only part that touches the network and
it appends every request to raw/pages.jsonl with the response bytes, so the sha256 in
the log is recomputable from committed bytes rather than asserted. `report` is the
product surface: it is what a person asking "which questions do people re-ask in this
tag" would run, and it reads only the committed population.

No model or judgement of this repository's own appears anywhere in the label: the
duplicate-closure rate is `closed_reason == "Duplicate"`, Stack Exchange's own field.
"""

import argparse
import collections
import json
import os
import sys

API = "https://api.stackexchange.com/2.3/questions"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# PROTOCOL.md section 3. The tag list is fixed in the protocol; nothing here chooses a
# tag, and `report` will not fall back to another site if a tag is empty.
TAGS = [
    # (stratum, site, tag)
    ("S1", "stackoverflow", "git"),
    ("S1", "stackoverflow", "regex"),
    ("S2", "stackoverflow", "python"),
    ("S2", "stackoverflow", "docker"),
    ("S3", "stackoverflow", "excel-formula"),
    ("S3", "travel", "customs"),
    # AMENDMENT-1 R2, declared before the fetch. One more tag on each of the two sites
    # whose single existing tag decided A4, so the site/tag confound is testable.
    ("S3", "travel", "baggage"),
    ("S4", "math", "calculus"),
    ("S4", "math", "linear-algebra"),
    ("S4", "math", "probability"),
]

# The eight declared in PROTOCOL.md section 3, in that order. R2's two tags are appended
# by amendment and are excluded from the declared population's gates.
DECLARED_TAGS = ["git", "regex", "python", "docker", "excel-formula", "customs",
                 "linear-algebra", "probability"]

# PROTOCOL.md section 3. `default` is the Active tab and is the strongest accessible
# alternative: it is what a person browsing the tag actually sees.
ARMS = [
    ("tail", "votes", "asc"),
    ("head", "votes", "desc"),
    ("default", "activity", "desc"),
]

PAGE_SIZE = 25          # the anonymous cap, /docs


def wilson(k, n, z=1.96):
    """Wilson score interval. Copied rather than imported: E033's descriptive.py is
    inside an experiment, not a library, and nine experiments now carry this function."""
    if n == 0:
        return (None, None)
    p = k / float(n)
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def url_for(site, tag, arm, page, pagesize):
    sort, order = [a for a in ARMS if a[0] == arm][0][1:]
    return ("{api}?site={site}&tagged={tag}&sort={sort}&order={order}"
            "&pagesize={n}&page={p}").format(api=API, site=site, tag=tag, sort=sort,
                                             order=order, n=pagesize, p=page)


# One registry of every sample this experiment fetches, so a reader of the report and the
# code that produced it cannot disagree about what exists. `harvest.py` reads this too;
# a sample declared in one place and fetched in another is how an empty arm becomes
# indistinguishable from a failed one.
SAMPLES = collections.OrderedDict([
    # sample name -> (arm, tags, first page)
    ("declared", ("", DECLARED_TAGS, 1)),
    ("R1", ("tail", ["customs", "excel-formula"], 5)),
    ("R2", ("tail", ["baggage", "calculus"], 1)),
])


def load_sample(sample="declared", path=None):
    if path is None:
        path = os.path.join(RAW, "harvest.jsonl" if sample == "declared"
                            else "%s.jsonl" % sample.lower())
    if not os.path.exists(path):
        return []
    out = []
    with open(path) as fh:
        for line in fh:
            if line.strip():
                r = json.loads(line)
                r.setdefault("sample", sample)
                out.append(r)
    return out


def load(path=None):
    if path:
        return load_sample("declared", path)
    return [r for s in SAMPLES for r in load_sample(s)]


def _rate(rows):
    k = sum(1 for r in rows if r["closed_reason"] == "Duplicate")
    lo, hi = wilson(k, len(rows))
    return k, len(rows), (k / float(len(rows)) if rows else None), lo, hi


def _span(rows):
    """The score range an arm really realized. PROTOCOL.md section 4 D3: this is what a
    reader checks the arm against, so it is printed even when it disagrees with the route.
    None scores are excluded and the count of them is what the range is silent about."""
    scores = [r["score"] for r in rows if r.get("score") is not None]
    if not scores:
        return "    ?", len(rows)
    return "[%4d,%4d]" % (min(scores), max(scores)), len(rows) - len(scores)


def report(rows=None, streams=sys.stdout):
    """The product surface. For each declared sample, prints per tag and pooled what each
    arm contains: how many questions were fetched, the score range that proves which end of
    the distribution the arm really is, and how many were closed as duplicates.

    A sample with no committed rows prints its declared cells as empty rather than being
    skipped, because an empty arm and a missing arm must not look alike (caught by
    check.py, "report prints a row for an empty arm")."""
    rows = load() if rows is None else rows
    # The site comes from the declared registry, not from the rows: a tag whose arms came
    # back empty has no row to read it from, and crashing on that would hide the very case
    # a reader needs to see (caught by check.py, "report does not crash when only one arm
    # has rows").
    sites = {t[2]: t[1] for t in TAGS}
    out = streams.write

    for sample, (arm_only, tags, _first) in SAMPLES.items():
        arms = [arm_only] if arm_only else ["tail", "head", "default"]
        sub = [r for r in rows if r.get("sample", "declared") == sample]
        if not sub:
            out("\n%s: no rows committed (raw/%s.jsonl absent or empty)\n"
                % (sample, sample.lower()))
            continue
        out("\nsample %s — %d rows\n" % (sample, len(sub)))
        out("site/tag                          arm       n  score range    dup  rate     CI95\n")
        pooled = collections.defaultdict(list)
        for tag in tags:
            for arm in arms:
                rs = [r for r in sub if r["tag"] == tag and r["arm"] == arm]
                pooled[arm] += rs
                if not rs:
                    out("{site}/{tag:<24} {arm:<8}  0  -               0   -        -\n".format(
                        site=sites[tag], tag=tag, arm=arm))
                    continue
                k, n, p, lo, hi = _rate(rs)
                span, _absent = _span(rs)
                out("{site}/{tag:<24} {arm:<8} {n:>3}  {span}  {k:>4}  {p:.4f}  [{lo:.4f},{hi:.4f}]\n".format(
                    site=sites[tag], tag=tag, arm=arm, n=n, span=span, k=k, p=p, lo=lo, hi=hi))
        if len(tags) > 1 or len(arms) > 1:
            out("  pooled over %d tags\n" % len(tags))
            for arm in arms:
                rs = pooled[arm]
                if not rs:
                    out("    {arm:<8} n=0\n".format(arm=arm))
                    continue
                k, n, p, lo, hi = _rate(rs)
                span, _absent = _span(rs)
                out("    {arm:<8} n={n:<5} score {span}  dup {k:>3}  rate {p:.4f}  CI95 [{lo:.4f},{hi:.4f}]\n".format(
                    arm=arm, n=n, span=span, k=k, p=p, lo=lo, hi=hi))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("harvest", help="fetch the declared population (see harvest.py)")
    sub.add_parser("replicate", help="AMENDMENT-1 arms R1 and R2 (see harvest.py)")
    sub.add_parser("report", help="print the report from the committed population")
    a = ap.parse_args(argv)
    if a.cmd == "report":
        report()
    elif a.cmd in ("harvest", "replicate"):
        # The network half lives in harvest.py so that `report` does not import an HTTP
        # client; dispatching keeps one entry point for both.
        import harvest
        if a.cmd == "harvest":
            harvest.harvest()
        else:
            for sample in ("R1", "R2"):
                arm, tags, first = SAMPLES[sample]
                harvest.replicate(sample=sample, tags=tuple(tags), arm=arm, first=first)
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

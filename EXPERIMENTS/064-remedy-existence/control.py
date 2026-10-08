#!/usr/bin/env python3
"""The CLI for the E064 instruments.

`registry.py` answers *does this name exist*; `meta.py` fetches
the metadata the G6 rule reads. This file is where they are run:

    python3 control.py --self-test          # both instruments' liveness
    python3 control.py --emit-control        # real names, for arm C
    python3 control.py raw/names.tsv raw/verdicts.json
    python3 control.py --meta raw/mutations.json raw/metadata.json

Stdlib only. Run from this directory.
"""
from __future__ import print_function

import json
import os
import sys
import time

import meta
import registry

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# real names for arm C's positive control, read out of registries
CONTROL_SOURCES = [
    ("crates", "https://crates.io/api/v1/crates?per_page=15&sort=downloads"),
    ("npm", "https://registry.npmjs.org/-/v1/search?text=keywords:0&size=15"),
    ("nuget", "https://azuresearch-usnc.nuget.org/query?take=15"),
    ("packagist", "https://packagist.org/search.json?q=a"),
    ("brew", "https://formulae.brew.sh/api/formula.json"),
]


def emit_control(per_source=6):
    """Read exact names out of registry listings. Real by construction."""
    rows = []
    for eco, url in CONTROL_SOURCES:
        st, body = registry._get(url)
        if st != 200:
            print("  (control source %s unavailable: %s)" % (eco, st))
            continue
        try:
            data = json.loads(body.decode("utf-8", "replace"))
        except Exception:
            continue
        names = []
        if eco == "crates":
            names = [c["name"] for c in data.get("crates", [])]
        elif eco == "npm":
            names = [o["package"]["name"] for o in data.get("objects", [])]
        elif eco == "nuget":
            names = [d["id"] for d in data.get("data", [])]
        elif eco == "packagist":
            names = [r["name"] for r in data.get("results", [])]
        elif eco == "brew":
            names = sorted(f["name"] for f in data)
        for n in names[:per_source]:
            rows.append((eco, n))
    return rows


def read_tsv(path):
    rows = []
    with open(path) as fh:
        head = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            if not line.strip():
                continue
            rows.append(dict(zip(head, line.rstrip("\n").split("\t"))))
    return rows


def run_verdicts(names_tsv, out_json):
    """One existence verdict per row of a names file."""
    rows = read_tsv(names_tsv)
    out = []
    for i, r in enumerate(rows):
        eco, name = r.get("ecosystem", ""), r.get("name", "")
        verdict = registry.check(eco, name)
        rec = {"ecosystem": eco, "name": name, "verdict": verdict}
        for k in ("arm", "blind_id", "label", "quoted"):
            if k in r:
                rec[k] = r[k]
        out.append(rec)
        print("%-10s %-46s %s" % (eco, name[:46], verdict))
        if i % 8 == 7:
            time.sleep(0.4)
    with open(out_json, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("wrote %s (%d rows)" % (out_json, len(out)))


def run_metadata(src, dst):
    """Registry metadata for every row of a names file, for the G6 rule.

    The source is a TSV (the original shape) or a JSON list of
    row objects; both carry `ecosystem` and `name`.
    """
    if src.endswith(".json"):
        with open(src) as fh:
            rows = json.load(fh)
    else:
        rows = read_tsv(src)
    out = []
    for i, r in enumerate(rows):
        eco, name = r.get("ecosystem", ""), r.get("name", "")
        m = meta.fetch(eco, name)
        rec = {"ecosystem": eco, "name": name}
        for k in ("arm", "seed", "mutation", "intended", "blind_id"):
            if k in r:
                rec[k] = r[k]
        rec.update(m)
        out.append(rec)
        print("%-6s %-10s %-34s %-7s dl=%-11s v=%-4s repo=%-3s"
              % (rec.get("arm", "")[:6], eco[:10], name[:34], m["verdict"],
                 m["downloads"], m["n_versions"], "y" if m["repo"] else "n"))
        sys.stdout.flush()
        time.sleep(0.35)
    with open(dst, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("wrote %s (%d rows)" % (dst, len(out)))


def registry_self_test():
    """The checker's own liveness: it must be able to say yes and say no."""
    cases = [("pypi", "requests", registry.EXISTS),
             ("pypi", "zzz-no-such-pypi-9x1", registry.ABSENT),
             ("npm", "react", registry.EXISTS),
             ("npm", "zzz-no-such-npm-9x1", registry.ABSENT),
             ("crates", "serde", registry.EXISTS),
             ("crates", "zzz-no-such-crate-9x1", registry.ABSENT),
             ("go", "github.com/gin-gonic/gin", registry.EXISTS),
             ("github", "torvalds/linux", registry.EXISTS),
             ("github", "torvalds/linuxx", registry.ABSENT)]
    bad = 0
    for eco, name, want in cases:
        got = registry.check(eco, name)
        ok = got == want
        bad += 0 if ok else 1
        print("%-8s %-40s want=%-8s got=%-8s %s"
              % (eco, name, want, got, "ok" if ok else "MISMATCH"))
    print("registry self-test: %d mismatch(es)" % bad)
    return 1 if bad else 0


def meta_self_test():
    cases = [("pypi", "asyncpg-migrate"), ("npm", "left-pad"),
             ("crates", "serde"), ("gem", "nokogiri"),
             ("packagist", "monolog/monolog")]
    bad = 0
    for eco, name in cases:
        m = meta.fetch(eco, name)
        ok = m["verdict"] == registry.EXISTS
        bad += 0 if ok else 1
        print("%-10s %-22s %-7s v=%-5s dl=%-12s repo=%-3s newest=%-20s %s"
              % (eco, name[:22], m["verdict"], m["n_versions"],
                 m["downloads"], "yes" if m["repo"] else "no",
                 (m["newest"] or "-")[:20], "ok" if ok else "MISMATCH"))
    print("meta self-test: %d mismatch(es)" % bad)
    return 1 if bad else 0


def main(argv):
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    if "--self-test" in argv:
        a = registry_self_test()
        b = meta_self_test()
        return 1 if (a or b) else 0
    if "--meta-self-test" in argv:
        return meta_self_test()
    if "--emit-control" in argv:
        rows = emit_control()
        path = os.path.join(RAW, "controls-real.tsv")
        with open(path, "w") as fh:
            fh.write("ecosystem\tname\n")
            for eco, n in rows:
                fh.write("%s\t%s\n" % (eco, n))
        print("wrote %s (%d rows)" % (path, len(rows)))
        return 0
    if "--meta" in argv:
        i = argv.index("--meta")
        src = argv[i + 1] if len(argv) > i + 1 else None
        dst = argv[i + 2] if len(argv) > i + 2 else os.path.join(
            RAW, "metadata.json")
        if src is None:
            print(__doc__)
            return 1
        return run_metadata(src, dst)
    if len(argv) >= 1:
        run_verdicts(argv[0], argv[1] if len(argv) > 1
                     else os.path.join(RAW, "verdicts.json"))
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Build the negative class for E064-A1: plausible near-miss package names.

Ground truth is definitional, which is the whole point. A mutation of a real
package name has a **known** intended artifact — the original. So if a mutated
name resolves to *anything*, the resolve is a false accept of existence-checking,
and no human labeler is needed and none can be argued with.

Three mutation families, chosen because they are what a model does when it half-
remembers a name rather than what an adversary would do:

  suffix    ``<name>-cli``, ``-utils``, ``-py``, ``-rs``, ``-js``, ``-x``, ``-go``
  prefix    ``py-<name>``, ``django-<name>``, ``fastapi-<name>``, ``node-<name>``
  synonym   ``async-``, ``lite-``, ``fast-``, ``simple-``, ``mini-`` + ``<name>``

Seeds are real packages an assistant would plausibly reach for. The **positive**
class is not drawn from them: it is `raw/controls-real.tsv`, names read out of
registry listings by `registry.py --emit-control` before this amendment existed,
so it is mid-tail by construction and is not fame-selected. Drawing the positive
class from the seeds would make G6's precision arm trivial.

Packagist names are ``vendor/pkg``, so only the package segment is mutated and
only by suffix — a mutated vendor is not a shape a model produces. Scoped npm
names are skipped for the same reason.

Stdlib only. Run from this directory.

    python3 mutate.py            # writes raw/mutations.json
"""
from __future__ import print_function

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

SEEDS = [
    ("pypi", "requests"), ("pypi", "click"), ("pypi", "jinja2"),
    ("pypi", "sqlalchemy"), ("pypi", "pydantic"), ("pypi", "httpx"),
    ("pypi", "rich"), ("pypi", "loguru"), ("pypi", "typer"),
    ("pypi", "arrow"), ("pypi", "tenacity"), ("pypi", "boto3"),
    ("npm", "express"), ("npm", "lodash"), ("npm", "axios"),
    ("npm", "chalk"), ("npm", "zod"), ("npm", "winston"),
    ("npm", "commander"), ("npm", "dayjs"), ("npm", "nanoid"),
    ("crates", "tokio"), ("crates", "regex"), ("crates", "rand"),
    ("crates", "clap"), ("crates", "anyhow"), ("crates", "itertools"),
    ("gem", "rails"), ("gem", "rspec"), ("gem", "puma"),
    ("gem", "sidekiq"), ("gem", "devise"), ("gem", "redis"),
    ("packagist", "monolog/monolog"), ("packagist", "laravel/framework"),
    ("packagist", "guzzlehttp/guzzle"), ("packagist", "phpunit/phpunit"),
]

SUFFIX = ["cli", "utils", "py", "rs", "js", "x", "go"]
PREFIX = ["py-", "django-", "fastapi-", "node-"]
SYNONYM = ["async-", "lite-", "fast-", "simple-", "mini-"]


def mutations(ecosystem, name):
    out = []
    if ecosystem == "packagist":
        vendor, _, pkg = name.partition("/")
        for s in SUFFIX:
            out.append(("%s/%s-%s" % (vendor, pkg, s), "suffix"))
        for p in SYNONYM:
            out.append(("%s/%s%s" % (vendor, p, pkg), "synonym"))
        return out
    for s in SUFFIX:
        out.append(("%s-%s" % (name, s), "suffix"))
    for p in PREFIX:
        out.append(("%s%s" % (p, name), "prefix"))
    for p in SYNONYM:
        out.append(("%s%s" % (p, name), "synonym"))
    return out


def build():
    rows = []
    seen = set()
    for eco, name in SEEDS:
        rows.append({"arm": "seed", "ecosystem": eco, "name": name,
                     "seed": name, "mutation": "", "intended": name})
        seen.add((eco, name.lower()))
    for eco, name in SEEDS:
        for mut, kind in mutations(eco, name):
            key = (eco, mut.lower())
            if key in seen:
                continue
            seen.add(key)
            rows.append({"arm": "mutated", "ecosystem": eco, "name": mut,
                         "seed": name, "mutation": kind, "intended": name})
    return rows


def main(argv):
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    rows = build()
    path = argv[0] if argv else os.path.join(RAW, "mutations.json")
    with open(path, "w") as fh:
        json.dump(rows, fh, indent=1, sort_keys=True)
    by_eco = {}
    for r in rows:
        if r["arm"] == "mutated":
            by_eco[r["ecosystem"]] = by_eco.get(r["ecosystem"], 0) + 1
    print("wrote %s" % path)
    print("  %d seeds, %d mutated names" % (len(SEEDS), len(rows) - len(SEEDS)))
    for eco in sorted(by_eco):
        print("  %-10s %d" % (eco, by_eco[eco]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""Arm C — the checker's own control set. Written BEFORE any registry was read.

Two halves, both 30 rows, both fixed here as literal text so that neither can be
fitted to the checker afterwards:

  raw/controls-invented.tsv   30 plausible names that were checked against no
                               registry while being written, and are expected to
                               resolve nowhere
  raw/controls-real.tsv        30 names read out of a registry index (registry.py
                               --emit-control), expected to resolve

Stdlib only. Run from this directory.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Written from memory of what package names *sound* like, deliberately spanning
# several ecosystems and several plausible prefixes. None was looked up.
INVENTED = [
    ("pypi", "pydantic-settings-loader"),
    ("pypi", "fastapi-auth-kit"),
    ("pypi", "httpx-retry-cascade"),
    ("pypi", "asyncpg-migrate"),
    ("pypi", "structlog-contextvars"),
    ("pypi", "click-option-groups"),
    ("pypi", "rich-markdown-table"),
    ("pypi", "pyarrow-flight-sql"),
    ("pypi", "polars-lazy-expr"),
    ("pypi", "sqlalchemy-utils-cli"),
    ("npm", "react-hook-forms-seeker"),
    ("npm", "next-auth-edge-compat"),
    ("npm", "zustand-persist-migrate"),
    ("npm", "vite-plugin-route-sort"),
    ("npm", "tailwind-truncate-lines"),
    ("npm", "zod-coerce-env"),
    ("npm", "esbuild-cache-plugin"),
    ("npm", "rxjs-replay-until"),
    ("crates", "tokio-cache-moka"),
    ("crates", "axum-tower-sessions"),
    ("crates", "serde-flatten-tagged"),
    ("crates", "rayon-parallel-sort"),
    ("go", "github.com/smartbuf/ringpool"),
    ("go", "github.com/elasticbody/scrollq"),
    ("go", "github.com/tykio/limitered"),
    ("go", "github.com/gocraft/workq"),
    ("gem", "sidekiq-profiler-ui"),
    ("maven", "io.github.batchgr:batch-grace"),
    ("maven", "com.streamforge:streamforge-core"),
    ("nuget", "Nito.AsyncEx.Coordination"),
]

HEADER = "ecosystem\tname\n"


def main():
    if not os.path.isdir(RAW):
        os.makedirs(RAW)
    path = os.path.join(RAW, "controls-invented.tsv")
    with open(path, "w") as fh:
        fh.write(HEADER)
        for eco, name in INVENTED:
            fh.write("%s\t%s\n" % (eco, name))
    print("wrote %s  (%d rows)" % (path, len(INVENTED)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

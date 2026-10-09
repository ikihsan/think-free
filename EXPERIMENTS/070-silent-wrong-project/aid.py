#!/usr/bin/env python3
"""E070 - coder aid: show one sample row compactly.

Prints the title, every install/import command in
the body, and the package-like tokens that sit next
to those commands. An aid only: it proposes no
label and drops no row. Stdlib only.
"""
import csv
import re
import sys

INSTALL = re.compile(
    r"(?:pip3?|pipenv|poetry|conda|uv|pipx)\s+"
    r"(?:install|add|create|remove|uninstall)[^\n`]{0,80}",
    re.I)
IMPORT = re.compile(
    r"(?:from|import)\s+[A-Za-z_][A-Za-z0-9_.]*", re.I)
NAME = re.compile(r"\b[A-Za-z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)+\b|\bsklearn\b|\bscrapy\b")


def show(row, chars=900):
    print("=" * 78)
    print("[%s|%s] id=%s" % (row["qclass"], row["venue"], row["id"]))
    print("query: %s" % row["query"])
    print("title: %s" % row["title"][:150])
    body = row["body"]
    inst = INSTALL.findall(body)
    imps = IMPORT.findall(body)
    if inst:
        print("install commands:")
        for m in dict.fromkeys(inst):
            print("   $ %s" % m.strip()[:110])
    if imps:
        print("imports: %s" % ", ".join(dict.fromkeys(imps))[:200])
    print("body: %s" % body[:chars])


def main():
    path = "EXPERIMENTS/070-silent-wrong-project/raw/sample.tsv"
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    if len(sys.argv) > 1:
        sel = sys.argv[1]
        if sel.isdigit():
            rows = [rows[int(sel)]]
        else:  # qclass filter
            rows = [r for r in rows if r["qclass"] == sel]
    for r in rows:
        show(r)


if __name__ == "__main__":
    main()

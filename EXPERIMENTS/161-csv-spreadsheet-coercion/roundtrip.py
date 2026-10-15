#!/usr/bin/env python3
"""E161 - round-trip real CSV files through a real spreadsheet engine and
measure, cell by cell, what the engine changed.

The engine is LibreOffice Calc in headless mode, given the import options a
spreadsheet uses when a user opens a CSV by double-clicking it (comma
separator, quote char, UTF-8, detect special numbers on).  The result is a real
implementation's behaviour on real files, not a model of one.

The .xlsx it writes is read back with zipfile and ElementTree only: cell
references, stored values, and the number format that decides how a stored
number is displayed.

Writes results.json and changes.tsv next to the corpus.
"""
import csv
import json
import os
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
RELS_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
INFILTER = "Text - txt - csv (StarCalc):44,34,76,1,,0,false,true"
DATE_CODE = re.compile(r"(?<!\\)[ymdhs]", re.I)
FORMAT_DATE_CHARS = set("ymdhsYMDHS")


def cell_ref(ref):
    """'AB12' -> (col 27 (0-based), row 12 (1-based))."""
    n = 0
    i = 0
    while i < len(ref) and ref[i].isalpha():
        n = n * 26 + (ord(ref[i].upper()) - 64)
        i += 1
    row = int(ref[i:]) if i < len(ref) else 0
    return n - 1, row


def date_format_ids(zf):
    """Number-format ids whose format code is a date or time format."""
    ids = set(range(14, 23)) | set(range(45, 48))  # built-in date formats
    root = ET.fromstring(zf.read("xl/styles.xml"))
    for numfmt in root.iter(NS + "numFmt"):
        code = numfmt.get("formatCode", "")
        stripped = re.sub(r'"[^"]*"|\[[^\]]*\]|\\.', "", code)
        if any(c in FORMAT_DATE_CHARS for c in stripped):
            ids.add(int(numfmt.get("numFmtId")))
    cell_xfs = root.find(NS + "cellXfs")
    style_date = set()
    if cell_xfs is not None:
        for i, xf in enumerate(cell_xfs):
            if int(xf.get("numFmtId", "0")) in ids:
                style_date.add(i)
    return style_date


def read_xlsx(path):
    """-> {(row, col): (kind, value, is_date)} with kind in text/number/bool/error/empty."""
    with zipfile.ZipFile(path) as zf:
        shared = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root.iter(NS + "si"):
                shared.append("".join(t.text or "" for t in si.iter(NS + "t")))
        style_date = date_format_ids(zf)
        sheet = "xl/worksheets/sheet1.xml"
        if sheet not in zf.namelist():
            sheet = [n for n in zf.namelist() if n.startswith("xl/worksheets/")][0]
        root = ET.fromstring(zf.read(sheet))
    cells = {}
    for c in root.iter(NS + "c"):
        ref = c.get("r")
        cc, rr = cell_ref(ref)
        key = (cc, rr - 1)
        t = c.get("t", "n")
        s = int(c.get("s", "0"))
        v = c.find(NS + "v")
        istag = c.find(NS + "is")
        if t == "s" and v is not None:
            idx = int(v.text)
            cells[key] = ("text", shared[idx] if idx < len(shared) else "", False)
        elif t == "inlineStr" and istag is not None:
            cells[key] = ("text", "".join(x.text or "" for x in istag.iter(NS + "t")), False)
        elif t == "b" and v is not None:
            cells[key] = ("bool", "TRUE" if v.text == "1" else "FALSE", False)
        elif t == "e":
            cells[key] = ("error", (v.text if v is not None else "#ERROR"), False)
        elif t == "str":
            cells[key] = ("text", (v.text if v is not None else ""), False)
        elif v is not None and v.text not in (None, ""):
            try:
                f = float(v.text)
            except ValueError:
                cells[key] = ("text", v.text, False)
            else:
                if f == int(f) and abs(f) < 1e15:
                    val = str(int(f))
                else:
                    val = repr(f)
                cells[key] = ("number", val, s in style_date)
        else:
            cells[key] = ("empty", "", False)
    return cells


NUMERIC = re.compile(r"^[-+]?(\d{1,3}(,\d{3})*|\d*)(\.\d*)?([eE][-+]?\d+)?$")
LEADING_ZERO = re.compile(r"^[-+]?0\d+$")
DATEISH = re.compile(r"^(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
                      r"|\d{1,2}\.\d{1,2}\.\d{2,4}"
                      r"|\d{1,2}-[A-Za-z]{3,9}-\d{2,4}"
                      r"|[A-Za-z]{3,9} \d{1,2}, ?\d{4})$")
DATETIMEISH = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
                         r"[T ]\d{1,2}:\d{2}(:\d{2})?(\.\d+)?( ?[AaPp][Mm])?"
                         r"(Z|[+-]\d{2}:?\d{2})?$")
TIMEISH = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?$")
AMPM = re.compile(r"^\d{1,2}:\d{2}(:\d{2})? ?[AaPp][Mm]$")
FORMULAISH = re.compile(r"^[=+@\t]")
BOOLS = {"TRUE", "FALSE", "True", "False", "true", "false"}

# Rules that lose information the file actually carried.  Everything else in the
# histogram is a re-typing or re-formatting the reader can undo by eye.
DESTRUCTIVE = ("leading_zero", "precision_loss", "datetime_time_lost",
               "formula_executed")


def classify(src, kind, val, is_date):
    """Name the rule that turned `src` into what the engine stored."""
    s = src
    if s != s.strip():
        return "whitespace_trim" if val == s.strip() else "other"
    if LEADING_ZERO.match(s):
        return "leading_zero"
    if s.startswith("="):
        inner = s[1:]
        if len(inner) > 1 and inner.startswith('"') and inner.endswith('"'):
            literal = inner[1:-1].replace('""', '"')
            return "formula_text_literal" if val == literal else "formula_executed"
        return "formula_executed"
    if FORMULAISH.match(s) or (s.startswith("-") and len(s) > 1 and not s[1].isdigit()):
        return "formula_coercion"
    if DATETIMEISH.match(s) and kind == "number":
        try:
            f = float(val)
        except ValueError:
            return "other"
        clock = re.search(r"[T ](\d{1,2}):(\d{2})(:(\d{2}))?( ?[AaPp][Mm])?", s)
        nonzero = False
        if clock:
            h, mnt, _grp, sec, ampm = clock.groups()
            hour = int(h) % 12
            if ampm and ampm.strip().lower() == "pm":
                hour += 12
            nonzero = hour != 0 or int(mnt) != 0 or (sec is not None and int(sec) != 0)
        if nonzero and f == int(f):
            return "datetime_time_lost"
        return "datetime_serial"
    if DATEISH.match(s) and kind == "number":
        return "date_serial"
    if (TIMEISH.match(s) or AMPM.match(s)) and kind == "number":
        return "time_serial"
    clean = s.replace(",", "")
    if NUMERIC.match(clean):
        try:
            f = float(clean)
        except ValueError:
            return "numeric_reformat"
        if kind == "number":
            try:
                g = float(val)
            except ValueError:
                return "other"
            return "precision_loss" if f != g else "numeric_reformat"
        if kind == "text" and val == clean:
            return "text_preserved"
    if s in BOOLS and kind == "bool":
        return "bool_coercion"
    if s.endswith("%") and kind == "number":
        return "percent_stripped"
    if s.startswith("$") and kind == "number":
        return "currency_stripped"
    if kind == "text" and val == s:
        return "text_preserved"
    if kind == "number":
        return "number_coercion"
    return "other"


def convert(csv_path, outdir, profile):
    cmd = ["soffice", "-env:UserInstallation=file://" + profile, "--headless",
           "--norestore", "--infilter=" + INFILTER, "--convert-to", "xlsx",
           "--outdir", outdir, csv_path]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600)
    out = os.path.join(outdir, os.path.splitext(os.path.basename(csv_path))[0] + ".xlsx")
    return (out if os.path.exists(out) else None), p.returncode


def analyse(csv_path, outdir, profile, max_rows=200000):
    result, rc = convert(csv_path, outdir, profile)
    rec = {"file": os.path.basename(csv_path), "convert_rc": rc}
    if result is None:
        rec["error"] = "conversion produced no xlsx"
        return rec, []
    cells = read_xlsx(result)
    changes = []
    n_cells = 0
    with open(csv_path, "r", encoding="utf-8", errors="replace", newline="") as f:
        for ri, row in enumerate(csv.reader(f)):
            if ri >= max_rows:
                break
            for ci, src in enumerate(row):
                if src == "":
                    continue
                n_cells += 1
                kind, val, is_date = cells.get((ci, ri), ("empty", "", False))
                if src == val:
                    continue
                rule = classify(src, kind, val, is_date)
                if rule == "text_preserved":
                    continue
                changes.append({"row": ri, "col": ci, "source": src[:120],
                                "stored_kind": kind, "stored": val[:60], "rule": rule})
    rec.update({"cells_compared": n_cells, "cells_changed": len(changes),
                "cells_destroyed": sum(1 for c in changes
                                       if c["rule"] in DESTRUCTIVE)})
    return rec, changes


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    corpus = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "corpus")
    outdir = os.path.join(here, "xlsx")
    profile = os.path.join(here, "lo-profile")
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(profile, exist_ok=True)
    files = sorted(f for f in os.listdir(corpus) if f.lower().endswith(".csv"))
    manifest_path = os.path.join(corpus, "manifest.json")
    meta = {}
    if os.path.exists(manifest_path):
        for entry in json.load(open(manifest_path))["files"]:
            meta[entry["path"]] = entry
    per_file, all_changes = [], []
    for name in files:
        rec, changes = analyse(os.path.join(corpus, name), outdir, profile)
        entry = meta.get(name, {})
        rec["source"] = entry.get("source", "?")
        rec["url"] = entry.get("url", "?")
        rec["sha256"] = entry.get("sha256", "")
        per_file.append(rec)
        for c in changes:
            c["file"] = name
            all_changes.append(c)
        print("%-46s cells=%-8d changed=%-6d destroyed=%-6d %s"
              % (name, rec.get("cells_compared", 0), rec.get("cells_changed", 0),
                 rec.get("cells_destroyed", 0), rec.get("error", "")))
        sys.stdout.flush()
    hist = {}
    for c in all_changes:
        hist[c["rule"]] = hist.get(c["rule"], 0) + 1
    summary = {
        "engine": "libreoffice-calc (headless)",
        "import_filter": INFILTER,
        "files": len(per_file),
        "sources": sorted({r["source"] for r in per_file}),
        "files_with_a_change": sum(1 for r in per_file if r.get("cells_changed", 0) > 0),
        "cells_compared": sum(r.get("cells_compared", 0) for r in per_file),
        "cells_changed": sum(r.get("cells_changed", 0) for r in per_file),
        "cells_destroyed": sum(r.get("cells_destroyed", 0) for r in per_file),
        "files_with_a_destroyed_cell": sum(1 for r in per_file
                                           if r.get("cells_destroyed", 0) > 0),
        "rule_histogram": dict(sorted(hist.items(), key=lambda kv: -kv[1])),
        "per_file": per_file,
    }
    with open(os.path.join(here, "results.json"), "w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
    with open(os.path.join(here, "changes.tsv"), "w") as f:
        f.write("file\trow\tcol\trule\tsource\tstored_kind\tstored\n")
        for c in all_changes:
            f.write("%s\t%d\t%d\t%s\t%s\t%s\t%s\n" % (
                c["file"], c["row"], c["col"], c["rule"], c["source"].replace("\t", " "),
                c["stored_kind"], c["stored"].replace("\t", " ")))
    print(json.dumps({k: summary[k] for k in
                      ("files", "files_with_a_change", "files_with_a_destroyed_cell",
                       "cells_compared", "cells_changed", "cells_destroyed",
                       "rule_histogram")}, indent=2))


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""E209 analysis -- compute G0-G4 and controls C1-C4 from committed raw bytes.

Reads only files on disk: E209's own raw pages, E209's probe, E209's
fetch_summary.json, and E198's committed raw pages for the G0/C4 controls.
No network access.
"""
import glob
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
E198 = os.path.join(HERE, "..", "198-recipient-read", "raw")

CODES = ["DA01", "DA10", "7A21", "7030", "D304"]
WINDOWS = ["current", "prior"]
G3_THRESHOLD = 0.30
G2_THRESHOLD = 0.99


def load_pages(pattern):
    """Return (rows, statuses) from every raw page matching a glob."""
    rows, statuses = [], []
    for path in sorted(glob.glob(os.path.join(RAW, pattern))):
        try:
            with open(path) as fh:
                d = json.load(fh)
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        results = d.get("results") or []
        rows.extend(results)
        meta = d.get("page_metadata") or {}
        statuses.append({"page": meta.get("page"),
                         "hasNext": meta.get("hasNext"),
                         "n": len(results)})
    return rows, statuses


def load_e198_pages(code):
    rows = []
    for path in sorted(glob.glob(os.path.join(E198, "recip_%s_p*.json" % code))):
        try:
            with open(path) as fh:
                d = json.load(fh)
        except Exception:
            continue
        if isinstance(d, dict):
            rows.extend(d.get("results") or [])
    return rows


def obligation_by_id(rows):
    """Sum obligation per recipient_id; return (dict, coverage)."""
    by_id, missing = {}, 0
    for r in rows:
        rid = r.get("recipient_id")
        if not rid:
            missing += 1
            continue
        amt = r.get("amount") or 0.0
        by_id[rid] = by_id.get(rid, 0.0) + amt
    return by_id, missing


def top_k_share(by_id, k=5):
    vals = sorted(by_id.values(), reverse=True)
    total = sum(vals)
    if total <= 0:
        return 0.0
    return sum(vals[:k]) / total


def spearman(xs, ys):
    """Spearman rho with average ranks; n>=3."""
    n = len(xs)
    if n < 3:
        return None

    def ranks(v):
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def main():
    out = {"experiment": "E209", "codes": CODES, "gates": {},
           "controls": {}, "per_code": {}}

    # ---- load E209 windows ----
    data = {}
    for code in CODES:
        for w in WINDOWS:
            rows, statuses = load_pages("%s_%s_p*.json" % (w, code))
            by_id, missing = obligation_by_id(rows)
            data[(code, w)] = {"rows": rows, "statuses": statuses,
                               "by_id": by_id, "missing": missing}

    # ---- G0: reproduce E198 from its committed raw pages ----
    e198_panel = json.load(open(os.path.join(E198, "panel1.json")))
    e198_counts = {r["code"]: r["recipient_count"] for r in e198_panel["rows"]}
    g0 = {"pass": True, "detail": {}}
    for code in CODES:
        rows = load_e198_pages(code)
        got = len(rows)
        exp = e198_counts.get(code)
        ok = (exp is not None and got == exp)
        g0["detail"][code] = {"recomputed": got, "committed": exp, "pass": ok}
        if not ok:
            g0["pass"] = False
    out["gates"]["G0_reproduce_E198"] = g0

    # ---- G1: source shape ----
    summary = json.load(open(os.path.join(RAW, "fetch_summary.json")))
    g1 = {"pass": True, "detail": {}}
    for code in CODES:
        for w in WINDOWS:
            key = "%s_%s" % (w, code)
            st = summary.get(key, {})
            statuses = st.get("statuses", [])
            all200 = bool(statuses) and all(
                s.get("status") == 200 for s in statuses)
            no_ceiling = not any(s.get("status") == "CEILING" for s in statuses)
            nonempty = st.get("rows", 0) > 0
            ok = all200 and no_ceiling and nonempty
            g1["detail"][key] = {"rows": st.get("rows"),
                                 "pages": len(statuses),
                                 "all_200": all200,
                                 "no_ceiling": no_ceiling,
                                 "pass": ok}
            if not ok:
                g1["pass"] = False
    out["gates"]["G1_source_shape"] = g1

    # ---- G2: identity coverage ----
    g2 = {"pass": True, "detail": {}}
    for code in CODES:
        for w in WINDOWS:
            d = data[(code, w)]
            total = len(d["rows"])
            cov = (total - d["missing"]) / total if total else 0.0
            ok = total > 0 and cov >= G2_THRESHOLD
            g2["detail"]["%s_%s" % (w, code)] = {
                "rows": total, "missing": d["missing"],
                "coverage": round(cov, 4), "pass": ok}
            if not ok:
                g2["pass"] = False
    out["gates"]["G2_identity_coverage"] = g2

    # ---- per-code quantities ----
    prior_union = set()
    for code in CODES:
        prior_union |= set(data[(code, "prior")]["by_id"])

    rows_out = []
    for code in CODES:
        cur = data[(code, "current")]
        pri = data[(code, "prior")]
        cur_ids = set(cur["by_id"])
        pri_ids = set(pri["by_id"])
        seg_new = cur_ids - pri_ids
        dom_new = cur_ids - prior_union
        frac_seg = len(seg_new) / len(cur_ids) if cur_ids else 0.0
        frac_dom = len(dom_new) / len(cur_ids) if cur_ids else 0.0
        frag = 1.0 - top_k_share(cur["by_id"], 5)
        rec = {
            "code": code,
            "current_recipients": len(cur_ids),
            "prior_recipients": len(pri_ids),
            "segment_newcomers": len(seg_new),
            "segment_newcomer_fraction": round(frac_seg, 4),
            "domain_newcomers": len(dom_new),
            "domain_newcomer_fraction": round(frac_dom, 4),
            "fragmentation": round(frag, 4),
            "current_obligation": round(sum(cur["by_id"].values()), 2),
        }
        rows_out.append(rec)
        out["per_code"][code] = rec

    fracs = [r["segment_newcomer_fraction"] for r in rows_out]
    fracs_sorted = sorted(fracs)
    n = len(fracs_sorted)
    median = (fracs_sorted[n // 2] if n % 2 else
              (fracs_sorted[n // 2 - 1] + fracs_sorted[n // 2]) / 2)
    out["gates"]["G3_entry"] = {
        "threshold": G3_THRESHOLD,
        "median_segment_newcomer_fraction": round(median, 4),
        "fractions": fracs,
        "pass": median >= G3_THRESHOLD,
        "verdict": "survives" if median >= G3_THRESHOLD else "KILL",
    }

    # ---- G4: confound correlations (reported, not gated) ----
    frags = [r["fragmentation"] for r in rows_out]
    counts = [r["current_recipients"] for r in rows_out]
    out["gates"]["G4_confound"] = {
        "n": len(rows_out),
        "rho_fragmentation_vs_entry": spearman(frags, fracs),
        "rho_count_vs_entry": spearman(counts, fracs),
        "note": "reported, not gated; n=5",
    }

    # ---- Controls ----
    ctl = json.load(open(os.path.join(RAW, "controls.json")))
    c1 = ctl["C1_zzzz"]
    out["controls"]["C1_zzzz"] = {
        "status": c1["status"], "n_results": c1["n_results"],
        "pass": c1["status"] == 200 and c1["n_results"] == 0}
    c2 = ctl["C2_not_a_code"]
    out["controls"]["C2_not_a_code"] = {
        "status": c2["status"], "n_results": c2["n_results"],
        "pass": c2["n_results"] in (0, None)}
    unused = []
    for code in CODES:
        for w in WINDOWS:
            unused.extend(data[(code, w)].get("unused_filters", []))
    out["controls"]["C3_unused_filters"] = {"count": len(unused),
                                            "pass": len(unused) == 0}

    # C4: current ids subset of E198 six-year ids
    c4 = {"pass": True, "detail": {}}
    for code in CODES:
        e198_ids = {r.get("recipient_id") for r in load_e198_pages(code)
                    if r.get("recipient_id")}
        cur_ids = set(data[(code, "current")]["by_id"])
        missing = cur_ids - e198_ids
        ok = len(cur_ids) > 0 and not missing
        c4["detail"][code] = {"current": len(cur_ids),
                              "e198_ids": len(e198_ids),
                              "not_in_e198": len(missing), "pass": ok}
        if not ok:
            c4["pass"] = False
    out["controls"]["C4_identity_subset"] = c4

    out["all_gates_pass"] = all(
        out["gates"][g]["pass"] for g in
        ["G0_reproduce_E198", "G1_source_shape", "G2_identity_coverage",
         "G3_entry"])
    out["kill_gate"] = out["gates"]["G3_entry"]["verdict"]

    with open(os.path.join(RAW, "analysis.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    print(json.dumps({
        "G0": out["gates"]["G0_reproduce_E198"]["pass"],
        "G1": out["gates"]["G1_source_shape"]["pass"],
        "G2": out["gates"]["G2_identity_coverage"]["pass"],
        "G3": out["gates"]["G3_entry"],
        "G4": out["gates"]["G4_confound"],
        "per_code": rows_out,
        "controls": out["controls"],
    }, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

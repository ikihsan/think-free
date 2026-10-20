#!/usr/bin/env python3
"""E197 analysis -- the gate vector, computed from panels A, B and D.

Every number here is read from a committed capture. `analysis.py` computes no
gate from anything it fetched itself, so a defect in this arithmetic can be
reproduced by re-running it over the same bytes rather than argued about.

Gate definitions are in `PROTOCOL.md` §7 and were declared before `panel1.py`
existed; `AMENDMENT-1.md` changed the search, not the gates.
"""
import json
import os
import re
import statistics
import sys

import thresholds as TH

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")

# Declared here rather than tuned: the words that appear in a PSC code name
# without naming the industry. E196's G5 had an arm with no members at all
# because no emptiness clause was declared for it, so both clauses are here.
NAME_STOPWORDS = {"non", "ian", "and", "for", "the", "with", "etc", "misc",
                  "other", "including", "except", "services", "general"}


def load(name):
    path = os.path.join(RAW, name)
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        return json.load(fh)


def code_tokens(name):
    """Content tokens of a PSC code name, declared vocabulary, not tuned."""
    toks = {t for t in re.findall(r"[a-z]{4,}", (name or "").lower())
            if t not in NAME_STOPWORDS}
    return toks


def token_share(rows, toks):
    hit = sum(1 for r in rows
              if toks & set(re.findall(r"[a-z]{4,}", (r or "").lower())))
    return (hit / float(len(rows))) if rows else None


def g6_vocabulary(rows, read_block_body):
    """E195's defect, applied to the funded sub-population of five IT cells.

    The control arm is the same cell's **non-funded head** (page 1 ascending),
    so the comparison is between two sub-populations of one code rather than
    between a code and a keyword. Emptiness clause declared in PROTOCOL.md §7:
    a cell with fewer than `G6_MIN_ROWS` funded rows sampled is not evaluated.
    """
    arms = []
    for code in TH.IT_CODES:
        row = next((r for r in rows if r["code"] == code), None)
        if row is None:
            arms.append({"code": code, "status": "not measured"})
            continue
        head = read_block_body("a1_%s_asc" % code, 1, "asc")
        funded_rows = read_block_body(
            "a1_%s_asc" % code, row["thresholds"][str(int(TH.SMALL_CUTOFF))]
            .get("turn_page") or 1, "asc")
        toks = code_tokens(row.get("name"))
        f_share = token_share([r.get("Description") for r in funded_rows], toks)
        h_share = token_share([r.get("Description") for r in head], toks)
        entry = {"code": code, "tokens": sorted(toks),
                 "funded_rows": len(funded_rows), "head_rows": len(head),
                 "funded_share": f_share, "head_share": h_share,
                 "ratio": (None if f_share is None or not h_share
                           else f_share / h_share)}
        if entry["funded_rows"] < TH.G6_MIN_ROWS:
            entry["status"] = "not evaluated (fewer than %d funded rows sampled)"
            entry["status"] = entry["status"] % TH.G6_MIN_ROWS
        elif entry["ratio"] is None:
            entry["status"] = "not evaluated (control arm is empty)"
        else:
            entry["status"] = ("pass" if entry["ratio"] >= TH.G6_MIN_RATIO
                               else "below the declared ratio")
        arms.append(entry)
    evaluated = [a for a in arms if a.get("status") in ("pass", "below the declared ratio")]
    return {"arms": arms,
            "evaluated": len(evaluated),
            "verdict": ("pass" if len(evaluated) == len(TH.IT_CODES)
                        and all(a["status"] == "pass" for a in evaluated)
                        else "fail" if len(evaluated) == len(TH.IT_CODES)
                        else "not evaluated")}


def main():
    p1, p2, p3, rc = (load("panel1.json"), load("panel2.json"),
                      load("panel3.json"), load("recompute.json"))
    if p1 is None or p2 is None:
        print("panel1.json / panel2.json missing; run them first")
        return 1
    rows = p1["rows"]

    # ---- C4 / C5: properties of the whole run -------------------------
    unused = [m for r in rows for m in (r.get("unused_filters_seen") or [])]
    unused += [m for m in (p2.get("panel_b_unused") or [])]
    bad_counts = [r["code"] for r in rows
                  if not r.get("n_total") or r["count_status"] != 200]
    impossible = [r["code"] for r in rows
                  if r.get("funded_ge_1") is not None
                  and r["funded_ge_1"] > r["n_total"]]
    c4 = {"ignored_filter_messages": sorted(set(unused)), "ok": not unused}
    c5 = {"codes_without_a_usable_count": bad_counts,
          "codes_where_funded_exceeds_total": impossible,
          "ok": not bad_counts and not impossible}

    # ---- G1: source shape --------------------------------------------
    measured = [r for r in rows
                if r["thresholds"][str(TH.FUNDED_T)].get("n") is not None
                and r.get("funded_ge_1") is not None]
    g1 = {"question": "exact, uncensored, filter-clean funded count",
          "measured": len(measured), "population": len(rows),
          "threshold": TH.G1_MIN_MEASURED,
          "pass": len(measured) >= TH.G1_MIN_MEASURED}
    g1["not_evaluated"] = not g1["pass"] and len(measured) == 0

    # ---- G2: zero control --------------------------------------------
    c1_ok = all(r["ok"] for r in p2["C1_nonexistent_code"])
    c2_ok = all(r["ok"] for r in p2["C2_malformed_code"])
    g2 = {"C1_nonexistent_code": c1_ok, "C2_malformed_code": c2_ok,
          "pass": c1_ok and c2_ok}

    # ---- G3: the funded fraction -------------------------------------
    fracs = [r["funded_fraction"] for r in rows if r.get("funded_fraction")]
    med = statistics.median(fracs) if fracs else None
    g3 = {"statistic": "median over codes of funded_ge_1 / n_total",
          "n_codes": len(fracs), "median": med,
          "bar": TH.G3_FIRED,
          "quintiles": (statistics.quantiles(fracs, n=4)
                        if len(fracs) >= 4 else None)}
    if len(fracs) < TH.G2_MAX_POPULATION // 2:
        g3.update(verdict="not evaluated",
                  reason="fewer than half the population was measurable")
    elif med >= TH.G3_FIRED:
        g3["verdict"] = "the record's headline survives as purchases"
    else:
        g3["verdict"] = "it is a statement about records"

    # ---- G4: strict addressability -----------------------------------
    by_code = {r["code"]: r for r in rows}
    g4_rows = []
    for code in TH.G4_CODEBOOK:
        r = by_code.get(code)
        g4_rows.append({"code": code,
                        "purchases_1_100k": (r or {}).get("purchases_1_100k"),
                        "funded_ge_1": (r or {}).get("funded_ge_1"),
                        "n_total": (r or {}).get("n_total"),
                        "clears_10000": (r or {}).get("purchases_1_100k") is not None
                        and r["purchases_1_100k"] >= 10000})
    survivors = [g for g in g4_rows if g["clears_10000"]]
    g4 = {"question": "codes with at least 10,000 awards in [$1, $100,000]",
          "of": len(g4_rows), "clearing": len(survivors),
          "survives_at": TH.G4_SURVIVES, "kills_at": TH.G4_KILLS,
          "rows": sorted(g4_rows, key=lambda g: -(g["purchases_1_100k"] or -1))}
    if len(survivors) >= TH.G4_SURVIVES:
        g4["verdict"] = "survives: the money is in small funded purchases"
    elif len(survivors) <= TH.G4_KILLS:
        g4["verdict"] = "kill: the count was a statement about records"
    else:
        g4["verdict"] = "unresolved (%d in the declared band %s)" % (
            len(survivors), str(TH.G4_UNRESOLVED_BAND))

    # ---- G5: the arms agree ------------------------------------------
    agree, compared, disagree = [], 0, []
    for b in p2["panel_b"]:
        a = by_code.get(b["code"], {})
        asc = a.get("funded_ge_1")
        desc = b.get("desc_funded_ge_1")
        if asc is None or desc is None:
            agree.append({"code": b["code"], "ascending": asc, "descending": desc,
                          "status": "not comparable (a censored arm)"})
            continue
        compared += 1
        ok = asc == desc
        agree.append({"code": b["code"], "ascending": asc, "descending": desc,
                      "difference": asc - desc, "agree": ok})
        if not ok:
            disagree.append(b["code"])
    c3_ok = all(r["ok"] for r in p2["C3_sort_direction"])
    c7_ok = bool(rc and rc.get("C7_tieback", {}).get("ok"))
    g5 = {"compared": compared, "agreements": sum(
        1 for a in agree if a.get("agree")), "disagreements": disagree,
        "C3_sort_direction": c3_ok, "C4_no_ignored_filter": c4["ok"],
        "C7_tieback": c7_ok, "threshold": TH.G5_MIN_AGREE,
        "pass": (sum(1 for a in agree if a.get("agree")) >= TH.G5_MIN_AGREE
                 and c3_ok and c4["ok"] and c7_ok),
        "rows": agree}

    # ---- G6: no procurement-vocabulary confound -----------------------
    from body import read_block_rows  # local import keeps the raw path in one place
    g6 = g6_vocabulary(rows, read_block_rows)

    out = {"experiment": "E197", "gates": {"G1": g1, "G2": g2, "G3": g3,
                                           "G4": g4, "G5": g5, "G6": g6},
           "controls": {"C1": p2["C1_nonexistent_code"],
                        "C2": p2["C2_malformed_code"],
                        "C3": p2["C3_sort_direction"],
                        "C4": c4, "C5": c5,
                        "C6": p2["C6_population_matches_e196"],
                        "C7": (rc or {}).get("C7_tieback")},
           "panel_d_exploratory": (p3 or {}).get("rows"),
           "head_table": sorted(
               [{"code": r["code"], "n_total": r["n_total"],
                 "funded_ge_1": r["funded_ge_1"],
                 "funded_fraction": r["funded_fraction"],
                 "purchases_1_100k": r["purchases_1_100k"]}
                for r in rows],
               key=lambda r: -(r["purchases_1_100k"] or -1))}
    with open(os.path.join(RAW, "analysis.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    print("G1 %s (%d/%d codes measured)" % ("PASS" if g1["pass"] else "FAIL",
                                             g1["measured"], g1["population"]))
    print("G2 %s" % ("PASS" if g2["pass"] else "FAIL"))
    print("G3 %s  median funded fraction = %s over %d codes"
          % (g3["verdict"], ("%.4f" % med) if med is not None else "None",
             g3["n_codes"]))
    print("G4 %s  %d of %d E196 codes clear 10,000 funded awards <= $100k"
          % (g4["verdict"], g4["clearing"], g4["of"]))
    print("G5 %s  %d/%d compared, C3=%s C4=%s C7=%s"
          % ("PASS" if g5["pass"] else "FAIL", g5["agreements"], g5["compared"],
             c3_ok, c4["ok"], c7_ok))
    print("G6 %s" % g6["verdict"])
    print("wrote raw/analysis.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
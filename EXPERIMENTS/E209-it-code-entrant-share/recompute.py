#!/usr/bin/env python3
"""
E209: Recompute gates from committed raw bytes only.

Verifies that analysis results are derivable from raw/ without re-fetching.
"""

import json
import os
import sys
import math
import random

EXP_RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

CODES = ["DA01", "DA10", "7A21", "7030", "D304"]
WINDOWS = ["current", "prior"]

E198_REF = {
    "DA01": {"recipients": 3610, "top5_share": 0.345},
    "DA10": {"recipients": 3651, "top5_share": 0.358},
    "7A21": {"recipients": 3977, "top5_share": 0.489},
    "7030": {"recipients": 3917, "top5_share": 0.384},
    "D304": {"recipients": 1155, "top5_share": 0.576},
}

def load_window(code, window):
    rows = []
    page = 1
    while True:
        fpath = os.path.join(EXP_RAW, f"{window}_{code}_p{page}.json")
        if not os.path.exists(fpath):
            break
        with open(fpath) as f:
            data = json.load(f)
        rows.extend(data.get("results", []))
        page += 1
    return rows

def obligation_by_id(rows):
    by_id = {}
    missing = 0
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

def permutation_test(xs, ys, n_perm=10000, seed=20261021):
    rho_obs = spearman(xs, ys)
    if rho_obs is None:
        return None, None
    random.seed(seed)
    n = len(xs)
    count = 0
    for _ in range(n_perm):
        ys_perm = ys[:]
        random.shuffle(ys_perm)
        rho_perm = spearman(xs, ys_perm)
        if rho_perm is not None and rho_perm >= rho_obs:
            count += 1
    p = (count + 1) / (n_perm + 1)
    return rho_obs, p

def main():
    print("Recomputing E209 from committed raw/ ...")
    
    all_results = []
    for code in CODES:
        cur_rows = load_window(code, "current")
        pri_rows = load_window(code, "prior")
        
        cur_by_id, cur_missing = obligation_by_id(cur_rows)
        pri_by_id, pri_missing = obligation_by_id(pri_rows)
        
        cur_ids = set(cur_by_id.keys())
        pri_ids = set(pri_by_id.keys())
        
        seg_new = cur_ids - pri_ids
        seg_frac = len(seg_new) / len(cur_ids) if cur_ids else 0.0
        
        all_pri_ids = set()
        for c in CODES:
            p_rows = load_window(c, "prior")
            p_by_id, _ = obligation_by_id(p_rows)
            all_pri_ids.update(p_by_id.keys())
        
        dom_new = cur_ids - all_pri_ids
        dom_frac = len(dom_new) / len(cur_ids) if cur_ids else 0.0
        
        frag = 1.0 - top_k_share(cur_by_id, 5)
        top5_share = top_k_share(cur_by_id, 5)
        obligation = round(sum(cur_by_id.values()), 2)
        
        e198 = E198_REF[code]
        recip_match = abs(len(cur_ids) - e198["recipients"]) / e198["recipients"] <= 0.05
        top5_match = abs(top5_share - e198["top5_share"]) <= 0.05
        
        total_rows = len(cur_rows)
        id_coverage = 1.0 - (cur_missing / total_rows) if total_rows > 0 else 0.0
        
        all_results.append({
            "code": code,
            "current_rows": total_rows,
            "current_recipients": len(cur_ids),
            "prior_recipients": len(pri_ids),
            "segment_newcomers": len(seg_new),
            "segment_newcomer_fraction": round(seg_frac, 4),
            "domain_newcomer_fraction": round(dom_frac, 4),
            "fragmentation": round(frag, 4),
            "top5_share": round(top5_share, 4),
            "current_obligation": obligation,
            "current_missing_recids": cur_missing,
            "prior_missing_recids": pri_missing,
            "id_coverage": round(id_coverage, 4),
            "g0_recip_match": recip_match,
            "g0_top5_match": top5_match,
        })
    
    # Gates
    g0_pass = all(r["g0_recip_match"] and r["g0_top5_match"] for r in all_results)
    g1_pass = all(r["id_coverage"] >= 0.99 for r in all_results)
    g2_pass = all(r["prior_recipients"] > 0 for r in all_results)
    
    frags = [r["fragmentation"] for r in all_results]
    seg_fracs = [r["segment_newcomer_fraction"] for r in all_results]
    rho, p = permutation_test(frags, seg_fracs)
    g3_pass = (rho is not None) and (rho >= 0.40) and (p < 0.05)
    g4_pass = any(r["segment_newcomer_fraction"] >= 0.30 for r in all_results)
    
    gates = {"G0": g0_pass, "G1": g1_pass, "G2": g2_pass, "G3": g3_pass, "G4": g4_pass}
    
    print("Gates recomputed:")
    for g, v in gates.items():
        print(f"  {g}: {'PASS' if v else 'FAIL'}")
    print(f"  rho = {rho:.4f}, p = {p:.4f}")
    
    # Compare with committed gates.json
    with open(os.path.join(OUT_DIR, "gates.json")) as f:
        committed = json.load(f)
    
    print("\nCommitted gates:")
    for g, v in committed["gates"].items():
        print(f"  {g}: {'PASS' if v else 'FAIL'}")
    print(f"  rho = {committed['rho']:.4f}, p = {committed['p']:.4f}")
    
    # Verify match
    match = True
    for g in gates:
        if gates[g] != committed["gates"][g]:
            print(f"MISMATCH: {g} recomputed={gates[g]} committed={committed['gates'][g]}")
            match = False
    if abs(rho - committed["rho"]) > 0.0001:
        print(f"MISMATCH: rho recomputed={rho:.4f} committed={committed['rho']:.4f}")
        match = False
    if abs(p - committed["p"]) > 0.0001:
        print(f"MISMATCH: p recomputed={p:.4f} committed={committed['p']:.4f}")
        match = False
    
    if match:
        print("\n✓ Recomputation matches committed results exactly.")
        return 0
    else:
        print("\n✗ Recomputation mismatch!")
        return 1

if __name__ == "__main__":
    exit(main())
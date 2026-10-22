"""Post-hoc incumbent check (declared as robustness, not a gate value).

Fetches window-A recipient aggregates for each code (all award sizes in
FY20-21). A cohort UEI whose window-A total exceeds $100k held substantial
business in the same window and is not a pure "all-small recipient".
Recomputes survival on the incumbent-cleaned population.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run as e211  # noqa: E402

RAW = os.path.join(HERE, "raw")


def a_totals(code):
    path = os.path.join(RAW, "AT_%s.json" % code)
    if os.path.exists(path):
        return json.load(open(path))
    rows, _ = e211.recipient_rows(code, e211.A_START, e211.A_END)
    doc = {"code": code, "rows": rows}
    json.dump(doc, open(path, "w"), indent=1, sort_keys=True)
    return doc


def main():
    for code in ("7030", "DA10", "DA01"):
        totals = {r["uei"]: r["amount"] for r in a_totals(code)["rows"]
                  if r["uei"]}
        a_rows = json.load(open(os.path.join(RAW, "A_%s.json" % code)))["rows"]
        b = {r["uei"]: r for r in
             json.load(open(os.path.join(RAW, "B_%s.json" % code)))["rows"]
             if r["uei"]}
        cohort = {r["uei"] for r in a_rows if r["uei"]}
        clean = {u for u in cohort
                 if u in totals and totals[u] <= e211.SMALL}
        unmeasured = {u for u in cohort if u not in totals}
        surv = lambda s: (len(s & set(b)) / len(s)) if s else 0.0  # noqa: E731
        pos = lambda s: (sum(1 for u in s & set(b) if b[u]["amount"] > 0)
                         / len(s)) if s else 0.0  # noqa: E731
        grad = lambda s: (sum(1 for u in s & set(b)
                              if b[u]["amount"] > e211.SMALL) / len(s))  # noqa: E731
        print("%s: window-A recipient rows=%d | cohort=%d incumbents(A-total>$100k)=%d "
              "clean=%d not-in-A-totals=%d" %
              (code, len(totals), len(cohort), len(cohort) - len(clean) - len(unmeasured),
               len(clean), len(unmeasured)))
        print("   all:     survival=%.1f%% net+=%.1f%% graduation=%.1f%%" %
              (100 * surv(cohort), 100 * pos(cohort), 100 * grad(cohort)))
        print("   cleaned: survival=%.1f%% net+=%.1f%% graduation=%.1f%%" %
              (100 * surv(clean), 100 * pos(clean), 100 * grad(clean)))


if __name__ == "__main__":
    main()

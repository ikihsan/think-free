#!/usr/bin/env python3
"""
Read-only probe. Answers one question and nothing else:

  On real bank exports, how much of a REAL recurring payment survives the
  merchant-name axis, and how much of it survives the interval+amount core?

It runs no detector. It reads raw strings, applies E065's normalizer, and
reports the raw-string fragmentation of descriptor families a human would call
one merchant. The definitions are printed with every number so they can be
argued with.
"""
import csv, json, os, re, sys
from collections import defaultdict
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "065-recurring-expense-detection"))
from corpus import load_account          # noqa: E402
import normalize                          # noqa: E402

# A "brand" is the leading alphabetic run of the raw descriptor, uppercased,
# with the processor prefixes removed. This is a PROXY for "one merchant", not
# a definition of it, and every number below is reported with that caveat.
PROC_PREFIX = re.compile(r"^(TST\*|SQ \*|SP \*|PAYPAL \*|IC\*|AMK |MTA\*|AplPay |VADAFONE |PYS\*|OTT\*|JTI\*|SQS\*)", re.I)


def brand(raw):
    s = raw.upper().strip()
    prev = None
    while prev != s:
        prev = s
        s = PROC_PREFIX.sub("", s).strip()
    m = re.match(r"^([A-Z][A-Z&'.\-]*)", s)
    return m.group(1) if m else s[:6]


def main():
    corpus = json.load(open(os.path.join(HERE, "raw/CORPUS.json")))
    accounts = corpus["accounts"]

    # ---- 1. raw-string fragmentation ------------------------------------
    # For each (account, brand) family with >= 4 rows: how many DISTINCT raw
    # descriptor strings carry it, and how many normalized names?
    fam_rows, fam_raw, fam_norm = defaultdict(int), defaultdict(set), defaultdict(set)
    account_rows = 0
    for e in accounts:
        acc = load_account(e)
        account_rows += len(acc["rows"])
        for r in acc["rows"]:
            k = (e["id"], brand(r["merchant"]))
            fam_rows[k] += 1
            fam_raw[k].add(r["merchant"])
            fam_norm[k].add(normalize.normalize_merchant(r["merchant"]))

    multi = {k: v for k, v in fam_rows.items() if v >= 4}
    frag_raw = [len(fam_raw[k]) for k in multi]
    frag_norm = [len(fam_norm[k]) for k in multi]
    big = {k: v for k, v in multi.items() if v >= 8}

    print("corpus: %d accounts, %d transactions" % (len(accounts), account_rows))
    print()
    print("=== 1. raw-string fragmentation of one-merchant families ===")
    print("definition: a family is (account, leading brand token) with >= 4 rows.")
    print("A family a person would call one merchant splits into N distinct raw")
    print("descriptor strings; E065's normalizer collapses it to M.")
    print()
    print("families with >= 4 rows: %d" % len(multi))
    print("  distinct raw strings per family: median %d, mean %.1f, max %d"
          % (sorted(frag_raw)[len(frag_raw)//2], sum(frag_raw)/len(frag_raw), max(frag_raw)))
    print("  distinct normalized names per family: median %d, mean %.1f, max %d"
          % (sorted(frag_norm)[len(frag_norm)//2], sum(frag_norm)/len(frag_norm), max(frag_norm)))
    print("  families still split into >1 normalized name after normalizing: %d of %d (%.3f)"
          % (sum(1 for k in multi if frag_norm[list(multi).index(k)] > 1), len(multi),
             sum(1 for k in multi if len(fam_norm[k]) > 1) / len(multi)))
    print()
    print("worst under-grouping, families with >= 8 rows:")
    worst = sorted(big.items(), key=lambda kv: -(len(fam_norm[kv[0]])))[:20]
    for (acct, b), n in worst:
        print("  %-4s %-22s rows=%3d raw=%3d normalized=%2d  %s"
              % (acct, b[:22], n, len(fam_raw[(acct, b)]), len(fam_norm[(acct, b)]),
                 sorted(fam_norm[(acct, b)])[:3]))

    # ---- 2. which SUBSCRIPTION families survive --------------------------
    # A hand-declared list of merchant brands that are subscriptions in the
    # ordinary sense: what a person pays monthly for access to something.
    SUBSCRIPTION_BRANDS = {
        "NETFLIX", "SPOTIFY", "APPLE", "GOOGLE", "HULU", "DISNEY", "ADOBE",
        "CHATGPT", "YOUTUBE", "PARAMOUNT", "PEACOCK", "CHEWY", "SPECTRUM",
        "VERIZON", "PROGRESSIVE", "STATE", "GEICO", "BRIGHTWHEEL", "VODAFONE",
        "TELEKOM", "COMCAST", "XFINITY", "WINDSTREAM", "MINT", "PREMIUM",
        "FITNESS", "GYM", "CVSEXTRACARE", "SHELTERPOINT", "USAA", "QUEST",
        "DASHBOARD", "MEMBERSHIP", "ALLSTATE", "GEICO", "INSURANCE",
    }

    print()
    print("=== 2. subscription-brand families: does the normalizer hold them together? ===")
    print("definition: brand token in the list above. 'Held' = 1 normalized name.")
    print()
    rows = []
    for (acct, b), n in sorted(fam_rows.items()):
        if n < 4 or b not in SUBSCRIPTION_BRANDS:
            continue
        rows.append((acct, b, n, len(fam_raw[(acct, b)]), len(fam_norm[(acct, b)])))
    rows.sort(key=lambda r: -r[2])
    held = sum(1 for r in rows if r[4] == 1)
    print("subscription-brand families with >= 4 rows: %d" % len(rows))
    print("  held as ONE normalized name: %d (%.3f)" % (held, held / len(rows) if rows else 0))
    for r in rows[:30]:
        print("  %-4s %-16s rows=%3d raw=%2d norm=%2d %s"
              % (r[0], r[1][:16], r[2], r[3], r[4], "HELD" if r[4] == 1 else "SPLIT"))


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Load Berka trans.csv and map rows to E065's normalized transaction shape.

Mapping predeclared in PROTOCOL.md:
  date: YYMMDD -> datetime.date (19YY)
  amount: VYDAJ/VYBER -> negative, PRIJEM -> positive
  merchant: "{k_symbol}|{bank}|{account}" (empty fields -> NA)
"""

import csv
import datetime
from collections import defaultdict

DEBIT_TYPES = {"VYDAJ", "VYBER"}
STANDING_ORDER_SYMBOLS = {"POJISTNE", "SIPO", "LEASING", "UVER"}
EXCLUDED_SYMBOL = "SLUZBY"


def load_accounts(path):
    """Return {account_id: [normalized txn, ...]} from the raw Berka CSV."""
    accounts = defaultdict(list)
    with open(path, newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            yy = int(row["date"][:2])
            date = datetime.date(1900 + yy, int(row["date"][2:4]), int(row["date"][4:6]))
            amount = float(row["amount"])
            if row["type"] in DEBIT_TYPES:
                amount = -amount
            k_symbol = row["k_symbol"].strip() or "NA"
            bank = row["bank"].strip() or "NA"
            account = row["account"].strip() or "NA"
            merchant = "%s|%s|%s" % (k_symbol, bank, account)
            accounts[int(row["account_id"])].append(
                {"date": date, "amount": amount, "merchant": merchant,
                 "k_symbol": k_symbol}
            )
    return dict(accounts)


def label_groups(txns):
    """Split an account's debit merchant groups into positive/excluded/negative.

    Positive: k_symbol in STANDING_ORDER_SYMBOLS and >= 3 debits.
    Excluded: k_symbol == SLUZBY (scored neither way).
    Returns (positive_merchants, excluded_merchants, negative_merchants).
    """
    groups = defaultdict(lambda: [0, None])
    for t in txns:
        if t["amount"] >= 0:
            continue
        g = groups[t["merchant"]]
        g[0] += 1
        g[1] = t["k_symbol"]
    positive, excluded, negative = set(), set(), set()
    for merchant, (count, k_symbol) in groups.items():
        if k_symbol in STANDING_ORDER_SYMBOLS and count >= 3:
            positive.add(merchant)
        elif k_symbol == EXCLUDED_SYMBOL:
            excluded.add(merchant)
        else:
            negative.add(merchant)
    return positive, excluded, negative


def sample_accounts(accounts, r_cap=300, c_cap=100, c_min_txns=20):
    """Predeclared deterministic sample: stride over positive-bearing accounts,
    first c_cap control accounts by id."""
    positives_by_account = {}
    for aid in sorted(accounts):
        pos, _, _ = label_groups(accounts[aid])
        if pos:
            positives_by_account[aid] = pos
    r_all = sorted(positives_by_account)
    stride = max(1, len(r_all) // r_cap)
    r_sample = r_all[::stride][:r_cap]
    c_sample = []
    for aid in sorted(accounts):
        if aid in positives_by_account:
            continue
        if len(accounts[aid]) >= c_min_txns:
            c_sample.append(aid)
        if len(c_sample) >= c_cap:
            break
    return r_sample, c_sample, positives_by_account

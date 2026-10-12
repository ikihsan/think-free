#!/usr/bin/env python3
"""Build E116's sample, ground-truth key, and assistant extracts.

Deterministic: E066's sampling rule (stride over positive-bearing
accounts, controls first by id), truncated to the first 60 R and
first 20 C accounts. Reads the raw Berka CSV via E066's own
loader, unchanged.

Outputs, all committed before any answer exists:
  key.jsonl       one row per sampled account: positives (the
                  k_symbol standing-order groups), excluded zone,
                  negative group count
  extracts/NNN.jsonl  the debit transactions the assistant sees:
                  date, amount, counterparty (bank / account).
                  No k_symbol -- it is the label.

Standard library only. Python 3.8.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "066-berka-real-validation"))
sys.path.insert(0, os.path.join(HERE, "..", "065-recurring-expense-detection"))

import berka  # noqa: E402  (E066's loader, unmodified semantics)

R_CAP = 60
C_CAP = 20


def main():
    raw = os.path.join(HERE, "..", "066-berka-real-validation", "raw", "trans.csv")
    accounts = berka.load_accounts(raw)
    r_sample, c_sample, _ = berka.sample_accounts(accounts)
    r_sample = r_sample[:R_CAP]
    c_sample = c_sample[:C_CAP]

    key_path = os.path.join(HERE, "key.jsonl")
    extract_dir = os.path.join(HERE, "extracts")
    os.makedirs(extract_dir, exist_ok=True)

    n_pos = n_excl = n_neg_groups = n_txns = 0
    with open(key_path, "w") as key_fh:
        for arm, ids in (("R", r_sample), ("C", c_sample)):
            for aid in ids:
                txns = accounts[aid]
                pos, excl, neg = berka.label_groups(txns)
                debits = sorted(
                    (t for t in txns if t["amount"] < 0),
                    key=lambda t: (t["date"], t["merchant"]),
                )
                # The assistant's surface: date, amount, counterparty.
                # Counterparty is bank + account, verbatim from the data.
                rows = []
                for t in debits:
                    _, bank, account = t["merchant"].split("|", 2)
                    rows.append(
                        {
                            "date": t["date"].isoformat(),
                            "amount": t["amount"],
                            "counterparty": "%s / %s" % (bank, account),
                        }
                    )
                epath = os.path.join(extract_dir, "%s%03d.jsonl" % (arm, aid))
                with open(epath, "w") as fh:
                    for row in rows:
                        fh.write(json.dumps(row) + "\n")
                key_fh.write(
                    json.dumps(
                        {
                            "account_id": aid,
                            "arm": arm,
                            "positive_merchants": sorted(pos),
                            "excluded_merchants": sorted(excl),
                            "negative_group_count": len(neg),
                            "n_debits": len(rows),
                        }
                    )
                    + "\n"
                )
                n_pos += len(pos)
                n_excl += len(excl)
                n_neg_groups += len(neg)
                n_txns += len(rows)

    print("R accounts: %d, C accounts: %d" % (len(r_sample), len(c_sample)))
    print("positive groups: %d, excluded: %d, negative groups: %d" % (n_pos, n_excl, n_neg_groups))
    print("debit rows presented to the assistant: %d" % n_txns)
    print("wrote %s and %s/" % (key_path, extract_dir))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""E198 panel A -- the recipient list for all five IT codes.

Full pagination for each code. Output: for each code, an array of recipient
objects with name, amount, recipient_id, code (DUNS/UEI), uei, total_outlays.
"""
import json
import os
import sys
import time

import client

HERE = os.path.dirname(os.path.abspath(__file__))


def one_code(code):
    """Fetch all recipients for one PSC code."""
    print("[%s] fetching all recipient pages..." % code)
    recipients, statuses, unused = client.recipient_all(code)
    print("[%s] %d recipients, %d pages" % (code, len(recipients), len(statuses)))

    # Compute concentration metrics
    total_amount = sum(r.get("amount", 0) for r in recipients)
    sorted_recips = sorted(recipients, key=lambda r: r.get("amount", 0), reverse=True)
    top10_amount = sum(r.get("amount", 0) for r in sorted_recips[:10])
    top10_share = top10_amount / total_amount if total_amount > 0 else 0

    row = {
        "code": code,
        "recipient_count": len(recipients),
        "total_amount": total_amount,
        "top10_amount": top10_amount,
        "top10_share": top10_share,
        "recipients": recipients,
        "statuses": statuses,
        "unused_filters": unused,
    }
    return row


def main():
    rows = []
    for code in client.IT_CODES:
        row = one_code(code)
        rows.append(row)
        # Write incrementally
        out_path = os.path.join(client.RAW, "panel1.json")
        with open(out_path, "w") as fh:
            json.dump({"experiment": "E198", "panel": "A",
                       "population_source": "E197 IT_CODES",
                       "rows": rows}, fh, indent=1, sort_keys=True)
    print("wrote %s (%d codes)" % (out_path, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
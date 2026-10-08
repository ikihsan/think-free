#!/usr/bin/env python3
"""
Synthetic corpus generator for recurring expense detection.
Creates CSV files with known ground truth for development and testing.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path


# Fixed seed for reproducibility
random.seed(42)


MERCHANTS = {
    # (merchant_name, amount, interval_days, variance_pct, is_recurring)
    "NETFLIX.COM": (15.99, 30, 0.0, True),
    "SPOTIFY USA": (10.99, 30, 0.0, True),
    "PLANET FITNESS": (29.99, 30, 0.0, True),
    "ADOBE CREATIVE CLOUD": (54.99, 30, 0.0, True),
    "GITHUB INC": (7.00, 30, 0.0, True),
    "AMAZON PRIME": (14.99, 30, 0.0, True),
    "DISNEY PLUS": (13.99, 30, 0.0, True),
    "HULU LLC": (17.99, 30, 0.0, True),
    "APPLE.COM/BILL": (9.99, 30, 0.0, True),
    "GOOGLE YOUTUBE PREMIUM": (11.99, 30, 0.0, True),
    # Quarterly
    "STATE FARM INSURANCE": (450.00, 91, 0.0, True),
    "GEICO INSURANCE": (380.00, 91, 0.0, True),
    # Annual
    "AMAZON PRIME ANNUAL": (139.00, 365, 0.0, True),
    "COSTCO MEMBERSHIP": (60.00, 365, 0.0, True),
    # Weekly
    "HELLOFRESH": (89.99, 7, 0.0, True),
    "BLUE APRON": (79.99, 7, 0.0, True),
    # Variable amount (utilities)
    "PACIFIC GAS ELECTRIC": (None, 30, 0.15, True),  # amount varies ±15%
    "SOUTHERN CALIFORNIA EDISON": (None, 30, 0.20, True),
    "CITY WATER DEPT": (None, 30, 0.10, True),
    # Income (should NOT be detected as recurring expense)
    "EMPLOYER PAYROLL": (3500.00, 14, 0.0, False),  # bi-weekly income
    "FREELANCE CLIENT": (2500.00, 30, 0.0, False),  # monthly income
    # Noise transactions (non-recurring)
    "WHOLE FOODS MARKET": (None, None, None, False),
    "TARGET STORE": (None, None, None, False),
    "SHELL GAS STATION": (None, None, None, False),
    "UBER RIDES": (None, None, None, False),
    "DOORDASH": (None, None, None, False),
    "STARBUCKS": (None, None, None, False),
    "LOCAL RESTAURANT": (None, None, None, False),
    "HOME DEPOT": (None, None, None, False),
    "CVS PHARMACY": (None, None, None, False),
    "WALMART": (None, None, None, False),
}

NOISE_MERCHANTS = list(k for k, v in MERCHANTS.items() if not v[3] and v[1] is None)
RECURRING_MERCHANTS = list(k for k, v in MERCHANTS.items() if v[3])
INCOME_MERCHANTS = list(k for k, v in MERCHANTS.items() if not v[3] and v[1] is not None)


def generate_transactions(start_date, num_months, recurring_prob=0.7):
    """Generate a list of transactions for a given period."""
    transactions = []
    current_date = start_date
    end_date = start_date + timedelta(days=30 * num_months)

    # Recurring transactions
    for merchant, (base_amount, interval, variance, is_recurring) in MERCHANTS.items():
        if not is_recurring:
            continue

        # Random start offset within first interval
        offset = random.randint(0, interval - 1)
        txn_date = start_date + timedelta(days=offset)

        while txn_date < end_date:
            # Amount with variance
            if base_amount is None:
                # Variable amount: base around $100-200
                base = random.uniform(80, 220)
                amount = round(base * (1 + random.uniform(-variance, variance)), 2)
            else:
                amount = round(base_amount * (1 + random.uniform(-variance, variance)), 2)

            # Income is positive, expenses negative
            if merchant in INCOME_MERCHANTS:
                amount = abs(amount)
            else:
                amount = -abs(amount)

            transactions.append({
                "date": txn_date,
                "merchant": merchant,
                "amount": amount,
                "recurring": is_recurring,
                "ground_truth_merchant": merchant
            })

            # Next occurrence with small jitter (±2 days)
            jitter = random.randint(-2, 2)
            txn_date += timedelta(days=interval + jitter)

    # Noise transactions (random dates, random amounts)
    num_noise = random.randint(50, 200)
    for _ in range(num_noise):
        txn_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        merchant = random.choice(NOISE_MERCHANTS)
        amount = -round(random.uniform(5, 300), 2)
        transactions.append({
            "date": txn_date,
            "merchant": merchant,
            "amount": amount,
            "recurring": False,
            "ground_truth_merchant": merchant
        })

    # Sort by date
    transactions.sort(key=lambda x: x["date"])
    return transactions


def write_chase_format(transactions, filepath):
    """Write in Chase CSV format: Transaction Date,Post Date,Description,Category,Type,Amount,Memo"""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Transaction Date", "Post Date", "Description", "Category", "Type", "Amount", "Memo"])
        for txn in transactions:
            # Chase: amounts are positive for credits, negative for debits
            # But we'll use standard: negative = expense, positive = income
            amount_str = f"{txn['amount']:.2f}"
            writer.writerow([
                txn['date'].strftime("%m/%d/%Y"),
                txn['date'].strftime("%m/%d/%Y"),
                txn['merchant'],
                "",  # Category
                "Sale" if txn['amount'] < 0 else "Payment",
                amount_str,
                ""
            ])


def write_boa_format(transactions, filepath):
    """Write in Bank of America format: Posted Date,Reference Number,Payee,Address,Amount"""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Posted Date", "Reference Number", "Payee", "Address", "Amount"])
        for i, txn in enumerate(transactions):
            ref = f"{random.randint(10000000, 99999999)}"
            amount_str = f"{txn['amount']:.2f}"
            writer.writerow([
                txn['date'].strftime("%m/%d/%Y"),
                ref,
                txn['merchant'],
                "",
                amount_str
            ])


def write_wells_fargo_format(transactions, filepath):
    """Write in Wells Fargo format: Date,Amount,Description"""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Amount", "Description"])
        for txn in transactions:
            amount_str = f"{txn['amount']:.2f}"
            writer.writerow([
                txn['date'].strftime("%Y-%m-%d"),
                amount_str,
                txn['merchant']
            ])


def write_generic_format(transactions, filepath):
    """Write in generic format: Date,Merchant,Amount"""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Merchant", "Amount"])
        for txn in transactions:
            amount_str = f"{txn['amount']:.2f}"
            writer.writerow([
                txn['date'].strftime("%m/%d/%Y"),
                txn['merchant'],
                amount_str
            ])


def generate_corpus(output_dir, num_files=100):
    """Generate synthetic corpus."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    formats = [
        ("chase", write_chase_format),
        ("boa", write_boa_format),
        ("wells_fargo", write_wells_fargo_format),
        ("generic", write_generic_format),
    ]

    manifest = []

    for i in range(num_files):
        # Vary start date and duration
        start_year = random.randint(2023, 2024)
        start_month = random.randint(1, 12)
        start_day = random.randint(1, 28)
        start_date = date(start_year, start_month, start_day)
        num_months = random.randint(3, 12)

        transactions = generate_transactions(start_date, num_months)

        # Pick format
        fmt_name, fmt_func = random.choice(formats)

        filename = f"synthetic_{fmt_name}_{i:03d}.csv"
        filepath = output_dir / filename
        fmt_func(transactions, filepath)

        # Ground truth: which merchants are recurring
        recurring_merchants = set(txn['ground_truth_merchant'] for txn in transactions if txn['recurring'])

        manifest.append({
            "file": filename,
            "format": fmt_name,
            "start_date": start_date.isoformat(),
            "months": num_months,
            "transaction_count": len(transactions),
            "recurring_merchants": sorted(list(recurring_merchants)),
            "recurring_count": len(recurring_merchants)
        })

    # Write manifest
    import json
    with open(output_dir / "manifest.json", 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"Generated {num_files} synthetic CSV files in {output_dir}")
    print(f"Manifest written to {output_dir / 'manifest.json'}")


if __name__ == "__main__":
    generate_corpus("/home/ubuntu/think-free/EXPERIMENTS/065-recurring-expense-detection/corpus/synthetic", 100)
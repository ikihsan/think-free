#!/usr/bin/env python3
"""
Synthetic fixture generator for E080 food recall matching experiment.
Generates purchase records in 3 formats and matching recall records with known ground truth.
"""

import json
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime, timedelta

random.seed(42)  # Reproducible fixtures

# Base product catalog - each product has a "national brand" UPC and store-brand variants
PRODUCT_CATALOG = [
    {"name": "Organic Baby Spinach", "national_upc": "012345678901", "category": "produce", "store_brands": {"store_a": "112345678901", "store_b": "212345678901"}},
    {"name": "Greek Yogurt Plain 32oz", "national_upc": "012345678902", "category": "dairy", "store_brands": {"store_a": "112345678902", "store_b": "212345678902"}},
    {"name": "Almond Butter Creamy", "national_upc": "012345678903", "category": "pantry", "store_brands": {"store_a": "112345678903", "store_b": "212345678903"}},
    {"name": "Whole Wheat Bread", "national_upc": "012345678904", "category": "bakery", "store_brands": {"store_a": "112345678904", "store_b": "212345678904"}},
    {"name": "Free Range Eggs Dozen", "national_upc": "012345678905", "category": "dairy", "store_brands": {"store_a": "112345678905", "store_b": "212345678905"}},
    {"name": "Wild Caught Salmon 1lb", "national_upc": "012345678906", "category": "seafood", "store_brands": {"store_a": "112345678906", "store_b": "212345678906"}},
    {"name": "Organic Chicken Breast", "national_upc": "012345678907", "category": "meat", "store_brands": {"store_a": "112345678907", "store_b": "212345678907"}},
    {"name": "Quinoa Organic 16oz", "national_upc": "012345678908", "category": "pantry", "store_brands": {"store_a": "112345678908", "store_b": "212345678908"}},
    {"name": "Avocado Hass 4ct", "national_upc": "012345678909", "category": "produce", "store_brands": {"store_a": "112345678909", "store_b": "212345678909"}},
    {"name": "Kombucha Ginger 16oz", "national_upc": "012345678910", "category": "beverage", "store_brands": {"store_a": "112345678910", "store_b": "212345678910"}},
    {"name": "Hummus Classic 10oz", "national_upc": "012345678911", "category": "deli", "store_brands": {"store_a": "112345678911", "store_b": "212345678911"}},
    {"name": "Salsa Medium 16oz", "national_upc": "012345678912", "category": "pantry", "store_brands": {"store_a": "112345678912", "store_b": "212345678912"}},
    {"name": "Tortilla Chips Restaurant", "national_upc": "012345678913", "category": "snacks", "store_brands": {"store_a": "112345678913", "store_b": "212345678913"}},
    {"name": "Dark Chocolate 70% 3oz", "national_upc": "012345678914", "category": "snacks", "store_brands": {"store_a": "112345678914", "store_b": "212345678914"}},
    {"name": "Coconut Water 1L", "national_upc": "012345678915", "category": "beverage", "store_brands": {"store_a": "112345678915", "store_b": "212345678915"}},
    {"name": "Frozen Berries Mix 16oz", "national_upc": "012345678916", "category": "frozen", "store_brands": {"store_a": "112345678916", "store_b": "212345678916"}},
    {"name": "Pizza Margherita Frozen", "national_upc": "012345678917", "category": "frozen", "store_brands": {"store_a": "112345678917", "store_b": "212345678917"}},
    {"name": "Ice Cream Vanilla Pint", "national_upc": "012345678918", "category": "frozen", "store_brands": {"store_a": "112345678918", "store_b": "212345678918"}},
    {"name": "Pasta Sauce Marinara 24oz", "national_upc": "012345678919", "category": "pantry", "store_brands": {"store_a": "112345678919", "store_b": "212345678919"}},
    {"name": "Olive Oil Extra Virgin 1L", "national_upc": "012345678920", "category": "pantry", "store_brands": {"store_a": "112345678920", "store_b": "212345678920"}},
    {"name": "Canned Black Beans 15oz", "national_upc": "012345678921", "category": "pantry", "store_brands": {"store_a": "112345678921", "store_b": "212345678921"}},
    {"name": "Brown Rice 2lb", "national_upc": "012345678922", "category": "pantry", "store_brands": {"store_a": "112345678922", "store_b": "212345678922"}},
    {"name": "Oats Rolled Old Fashioned", "national_upc": "012345678923", "category": "pantry", "store_brands": {"store_a": "112345678923", "store_b": "212345678923"}},
    {"name": "Peanut Butter Natural 16oz", "national_upc": "012345678924", "category": "pantry", "store_brands": {"store_a": "112345678924", "store_b": "212345678924"}},
    {"name": "Honey Raw Local 12oz", "national_upc": "012345678925", "category": "pantry", "store_brands": {"store_a": "112345678925", "store_b": "212345678925"}},
    {"name": "Maple Syrup Grade A 8oz", "national_upc": "012345678926", "category": "pantry", "store_brands": {"store_a": "112345678926", "store_b": "212345678926"}},
    {"name": "Coffee Whole Bean 12oz", "national_upc": "012345678927", "category": "beverage", "store_brands": {"store_a": "112345678927", "store_b": "212345678927"}},
    {"name": "Tea Green Organic 20ct", "national_upc": "012345678928", "category": "beverage", "store_brands": {"store_a": "112345678928", "store_b": "212345678928"}},
    {"name": "Sparkling Water Lime 8pk", "national_upc": "012345678929", "category": "beverage", "store_brands": {"store_a": "112345678929", "store_b": "212345678929"}},
    {"name": "Granola Honey Almond 12oz", "national_upc": "012345678930", "category": "breakfast", "store_brands": {"store_a": "112345678930", "store_b": "212345678930"}},
]

STORES = ["store_a", "store_b", "store_c", "store_d"]
RECALL_REASONS = [
    "Potential Listeria monocytogenes contamination",
    "Potential Salmonella contamination",
    "Undeclared allergen: peanuts",
    "Undeclared allergen: wheat",
    "Undeclared allergen: milk",
    "Potential E. coli contamination",
    "Foreign material: plastic fragments",
    "Misbranding: incorrect ingredient statement",
    "Potential Clostridium botulinum",
    "Undeclared sulfites",
]

def random_date(start_days_ago: int = 365, end_days_ago: int = 1) -> str:
    """Generate random date as YYYYMMDD string."""
    days_ago = random.randint(end_days_ago, start_days_ago)
    dt = datetime.now() - timedelta(days=days_ago)
    return dt.strftime("%Y%m%d")

def random_lot_code() -> str:
    """Generate a realistic lot code."""
    patterns = [
        lambda: f"L{random.randint(100000, 999999)}",
        lambda: f"{random.randint(1,12):02d}{random.randint(20,26):02d}{random.randint(100,999)}",
        lambda: f"LOT{random.randint(10000,99999)}",
        lambda: f"{random.randint(2020,2026)}{random.randint(1,365):03d}{random.randint(10,99)}",
    ]
    return random.choice(patterns)()

def random_best_by(purchase_date: str) -> str:
    """Generate best-by date after purchase date."""
    dt = datetime.strptime(purchase_date, "%Y%m%d")
    days_ahead = random.randint(7, 365)
    return (dt + timedelta(days=days_ahead)).strftime("%Y%m%d")

def truncate_upc(upc: str, format_type: str) -> str:
    """Simulate UPC truncation on receipts."""
    if format_type == "receipt":
        # Receipts often show last 8-10 digits
        return upc[-8:] if len(upc) > 8 else upc
    return upc

def abbreviate_name(name: str, format_type: str) -> str:
    """Simulate name abbreviation on receipts."""
    if format_type == "receipt":
        abbreviations = {
            "Organic": "ORG", "Plain": "PLN", "Creamy": "CRM", "Whole": "WHL",
            "Wheat": "WHT", "Free": "FRE", "Range": "RNG", "Wild": "WLD",
            "Caught": "CTD", "Chicken": "CHK", "Breast": "BRST", "Hass": "HSS",
            "Classic": "CLS", "Medium": "MED", "Restaurant": "REST",
            "Chocolate": "CHOC", "Extra": "EXT", "Virgin": "VIR", "Rolled": "RLD",
            "Old": "OLD", "Fashioned": "FSH", "Natural": "NAT", "Local": "LCL",
            "Grade": "GRD", "Whole": "WHL", "Bean": "BEAN", "Green": "GRN",
            "Sparkling": "SPK", "Almond": "ALM", "Margherita": "MARG",
            "Vanilla": "VAN", "Marinara": "MAR", "Black": "BLK", "Brown": "BRN",
        }
        words = name.split()
        result = []
        for w in words:
            result.append(abbreviations.get(w, w[:4] if len(w) > 4 else w))
        return " ".join(result)
    return name

def generate_fixtures() -> Dict:
    """Generate all synthetic fixtures with ground truth."""
    
    # Select 15 products to be recalled, 15 not recalled (catalog has 30)
    recalled_products = random.sample(PRODUCT_CATALOG, 15)
    not_recalled_products = [p for p in PRODUCT_CATALOG if p not in recalled_products]
    not_recalled_products = random.sample(not_recalled_products, 15)
    
    # Generate recall records for the 15 recalled products
    # Store the store choice and other attributes per recall so purchases match
    recalls = []
    recall_attributes = []  # List of (store, upc, lot, purchase_date, best_by) per recall
    purchase_to_recall = {}  # Maps purchase_id -> recall_id (or None)
    purchase_id = 0
    
    for product in recalled_products:
        recall_id = f"R-{len(recalls)+1:04d}"
        store = random.choice(STORES)
        upc = product["store_brands"].get(store, product["national_upc"])
        lot = random_lot_code()
        purchase_date = random_date(30, 1)  # Recent purchases
        best_by = random_best_by(purchase_date)
        
        recall = {
            "recall_id": recall_id,
            "product_description": product["name"],
            "upc": upc,
            "lot_code": lot,
            "best_by_date": best_by,
            "recall_reason": random.choice(RECALL_REASONS),
            "classification": random.choice(["Class I", "Class II", "Class III"]),
            "distribution_pattern": "Nationwide" if random.random() < 0.7 else f"{store.upper()} stores",
            "status": "Ongoing" if random.random() < 0.3 else "Terminated",
            "recall_initiation_date": purchase_date,
        }
        recalls.append(recall)
        recall_attributes.append((store, upc, lot, purchase_date, best_by))
    
    # Generate purchases for each format
    formats = ["receipt", "loyalty_csv", "manual_entry"]
    all_purchases = {"receipt": [], "loyalty_csv": [], "manual_entry": []}
    
    for fmt in formats:
        # 15 recalled purchases - use SAME store/attributes as recall
        for i, product in enumerate(recalled_products):
            purchase_id += 1
            store, upc, lot, purchase_date, best_by = recall_attributes[i]
            recall = recalls[i]  # Same index
            
            if fmt == "receipt":
                purchase = {
                    "purchase_id": f"P-{purchase_id:05d}",
                    "format": "receipt",
                    "store": store,
                    "date": purchase_date,
                    "upc": truncate_upc(upc, fmt),
                    "product_name": abbreviate_name(product["name"], fmt),
                    "lot_code": lot if random.random() < 0.1 else "",  # Receipts rarely have lot codes
                    "best_by": best_by if random.random() < 0.2 else "",  # Sometimes on receipt
                    "price": round(random.uniform(2.0, 25.0), 2),
                    "ground_truth_recall": recall["recall_id"],
                }
            elif fmt == "loyalty_csv":
                purchase = {
                    "purchase_id": f"P-{purchase_id:05d}",
                    "format": "loyalty_csv",
                    "store": store,
                    "date": purchase_date,
                    "upc": upc,
                    "product_name": product["name"],
                    "lot_code": lot if random.random() < 0.5 else "",  # Loyalty sometimes has lot
                    "best_by": best_by if random.random() < 0.5 else "",
                    "price": round(random.uniform(2.0, 25.0), 2),
                    "ground_truth_recall": recall["recall_id"],
                }
            else:  # manual_entry
                purchase = {
                    "purchase_id": f"P-{purchase_id:05d}",
                    "format": "manual_entry",
                    "store": store if random.random() < 0.7 else "",
                    "date": purchase_date if random.random() < 0.8 else "",
                    "upc": "" if random.random() < 0.9 else upc,  # Rarely entered
                    "product_name": product["name"] if random.random() < 0.7 else abbreviate_name(product["name"], "receipt"),
                    "lot_code": "",
                    "best_by": "",
                    "price": 0.0,
                    "ground_truth_recall": recall["recall_id"],
                }
            all_purchases[fmt].append(purchase)
        
        # 25 NOT recalled purchases (negative controls)
        for i, product in enumerate(not_recalled_products):
            purchase_id += 1
            store = random.choice(STORES)
            upc = product["store_brands"].get(store, product["national_upc"])
            lot = random_lot_code()
            purchase_date = random_date(30, 1)
            best_by = random_best_by(purchase_date)
            
            if fmt == "receipt":
                purchase = {
                    "purchase_id": f"P-{purchase_id:05d}",
                    "format": "receipt",
                    "store": store,
                    "date": purchase_date,
                    "upc": truncate_upc(upc, fmt),
                    "product_name": abbreviate_name(product["name"], fmt),
                    "lot_code": lot if random.random() < 0.1 else "",
                    "best_by": best_by if random.random() < 0.2 else "",
                    "price": round(random.uniform(2.0, 25.0), 2),
                    "ground_truth_recall": None,
                }
            elif fmt == "loyalty_csv":
                purchase = {
                    "purchase_id": f"P-{purchase_id:05d}",
                    "format": "loyalty_csv",
                    "store": store,
                    "date": purchase_date,
                    "upc": upc,
                    "product_name": product["name"],
                    "lot_code": lot if random.random() < 0.5 else "",
                    "best_by": best_by if random.random() < 0.5 else "",
                    "price": round(random.uniform(2.0, 25.0), 2),
                    "ground_truth_recall": None,
                }
            else:  # manual_entry
                purchase = {
                    "purchase_id": f"P-{purchase_id:05d}",
                    "format": "manual_entry",
                    "store": store if random.random() < 0.7 else "",
                    "date": purchase_date if random.random() < 0.8 else "",
                    "upc": "" if random.random() < 0.9 else upc,
                    "product_name": product["name"] if random.random() < 0.7 else abbreviate_name(product["name"], "receipt"),
                    "lot_code": "",
                    "best_by": "",
                    "price": 0.0,
                    "ground_truth_recall": None,
                }
            all_purchases[fmt].append(purchase)
    
    return {
        "recalls": recalls,
        "purchases": all_purchases,
        "metadata": {
            "total_recalls": len(recalls),
            "total_purchases_per_format": {fmt: len(purchases) for fmt, purchases in all_purchases.items()},
            "recalled_count_per_format": {fmt: sum(1 for p in purchases if p["ground_truth_recall"]) for fmt, purchases in all_purchases.items()},
            "not_recalled_count_per_format": {fmt: sum(1 for p in purchases if not p["ground_truth_recall"]) for fmt, purchases in all_purchases.items()},
        }
    }

def write_fixtures(output_dir: str = "."):
    """Write fixtures to JSON files."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    fixtures = generate_fixtures()
    
    with open(os.path.join(output_dir, "recalls.json"), "w") as f:
        json.dump(fixtures["recalls"], f, indent=2)
    
    for fmt, purchases in fixtures["purchases"].items():
        with open(os.path.join(output_dir, f"purchases_{fmt}.json"), "w") as f:
            json.dump(purchases, f, indent=2)
    
    with open(os.path.join(output_dir, "ground_truth.json"), "w") as f:
        # Flatten for easy lookup
        gt = {}
        for fmt, purchases in fixtures["purchases"].items():
            for p in purchases:
                gt[p["purchase_id"]] = p["ground_truth_recall"]
        json.dump(gt, f, indent=2)
    
    print(f"Generated fixtures in {output_dir}")
    print(f"  Recalls: {fixtures['metadata']['total_recalls']}")
    for fmt in ["receipt", "loyalty_csv", "manual_entry"]:
        m = fixtures["metadata"]
        print(f"  {fmt}: {m['total_purchases_per_format'][fmt]} purchases ({m['recalled_count_per_format'][fmt]} recalled, {m['not_recalled_count_per_format'][fmt]} clean)")

if __name__ == "__main__":
    write_fixtures("fixtures")
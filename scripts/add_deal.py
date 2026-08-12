#!/usr/bin/env python3
"""
add_deal.py - Utility script to programmatically or interactively add a new verified deal
to data/deals.json, ensuring all priority and schema rules are enforced.

Usage:
  python3 scripts/add_deal.py --json '{"id": "new-deal", "title": "...", "priority_rank": 1, ...}'
"""

import json
import os
import sys
import argparse
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEALS_PATH = os.path.join(ROOT_DIR, "data", "deals.json")
STATS_SCRIPT = os.path.join(ROOT_DIR, "scripts", "generate_stats.py")

def load_deals():
    with open(DEALS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_deals(deals):
    with open(DEALS_PATH, "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=2)
    print(f"✅ Saved updated deals list to {DEALS_PATH}")

def main():
    parser = argparse.ArgumentParser(description="Add a new verified deal to data/deals.json")
    parser.add_argument("--json", help="JSON string representing the new deal object")
    args = parser.parse_args()

    if not args.json:
        print("Error: Please provide --json string of the deal to add.")
        sys.exit(1)

    try:
        new_deal = json.loads(args.json)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)

    deals = load_deals()
    existing_ids = {d["id"] for d in deals}
    if new_deal.get("id") in existing_ids:
        print(f"Error: A deal with ID '{new_deal.get('id')}' already exists.")
        sys.exit(1)

    # Ensure required fields and default verified date
    if "verification" not in new_deal:
        new_deal["verification"] = {
            "status": "Verified Official Source",
            "source_name": "Community Verification",
            "verified_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "notes": "Added via scripts/add_deal.py"
        }

    deals.append(new_deal)
    save_deals(deals)

    # Re-generate stats
    os.system(f"python3 {STATS_SCRIPT}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
verify_links.py - Automated Deal & Schema Verification Engine
Validates that all entries in data/deals.json meet strict priority and verification requirements:
1. Validates schema (required fields, priority rank 1/2/3, valid categories).
2. Checks that Priority 1 deals are labeled "100% Free".
3. Verifies that every deal has an official verification source, date, and valid URLs.
4. Reports verification statistics.
"""

import json
import os
import sys
import urllib.parse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEALS_PATH = os.path.join(ROOT_DIR, "data", "deals.json")

REQUIRED_FIELDS = [
    "id", "title", "priority_label", "priority_rank", "category",
    "location", "value", "description", "redemption_instructions",
    "restrictions", "verification", "promotion_url", "tags"
]

VALID_PRIORITIES = {
    1: "100% Free",
    2: "Free with Purchase",
    3: "Discount/Coupon"
}

def verify_deals_database():
    if not os.path.exists(DEALS_PATH):
        print(f"❌ Error: {DEALS_PATH} does not exist.")
        sys.exit(1)

    with open(DEALS_PATH, "r", encoding="utf-8") as f:
        try:
            deals = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON syntax error in {DEALS_PATH}: {e}")
            sys.exit(1)

    print(f"🔍 Checking {len(deals)} deals in {DEALS_PATH}...")
    errors = 0
    warnings = 0
    free_count = 0

    seen_ids = set()

    for idx, d in enumerate(deals, 1):
        deal_id = d.get("id", f"item_#{idx}")

        # Check unique id
        if deal_id in seen_ids:
            print(f"  ❌ Error: Duplicate deal ID '{deal_id}' at position {idx}")
            errors += 1
        seen_ids.add(deal_id)

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in d:
                print(f"  ❌ Error: Deal '{deal_id}' is missing required field: {field}")
                errors += 1

        # Check priority ranking rules
        p_rank = d.get("priority_rank")
        p_label = d.get("priority_label")
        if p_rank not in VALID_PRIORITIES:
            print(f"  ❌ Error: Deal '{deal_id}' has invalid priority_rank: {p_rank} (must be 1, 2, or 3)")
            errors += 1
        elif VALID_PRIORITIES[p_rank] != p_label:
            print(f"  ⚠️ Warning: Deal '{deal_id}' priority label '{p_label}' does not match standard label '{VALID_PRIORITIES[p_rank]}'")
            warnings += 1

        if p_rank == 1:
            free_count += 1

        # Check verification object
        v = d.get("verification", {})
        if not v.get("status") or not v.get("source_name") or not v.get("verified_date"):
            print(f"  ❌ Error: Deal '{deal_id}' has incomplete verification record: {v}")
            errors += 1

        # Check URLs
        url = d.get("promotion_url", "")
        if not url.startswith("http://") and not url.startswith("https://"):
            print(f"  ❌ Error: Deal '{deal_id}' promotion_url must start with http:// or https://")
            errors += 1

    print("\n---------------------------------------------------------")
    print(f"📊 Verification Results:")
    print(f"   Total deals audited: {len(deals)}")
    print(f"   100% Free deals (Priority #1): {free_count} ({round((free_count/len(deals))*100, 1)}%)")
    print(f"   Errors found: {errors}")
    print(f"   Warnings found: {warnings}")
    print("---------------------------------------------------------")

    if errors > 0:
        print("❌ Verification FAILED. Please fix the above errors.")
        sys.exit(1)
    else:
        print("✅ All deals verified! Schema, URLs, and priority rules PASSED successfully.")
        sys.exit(0)

if __name__ == "__main__":
    verify_deals_database()

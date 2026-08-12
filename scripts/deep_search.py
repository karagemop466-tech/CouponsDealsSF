#!/usr/bin/env python3
"""
deep_search.py - Comprehensive CLI Deep Search & Reddit Aggregator for SF/Bay Area Deals
Can filter and search local deals database, and can query live community sources (Reddit API)
to discover and prioritize 100% freebies and promotions.

Usage examples:
  python3 scripts/deep_search.py --query "museum"
  python3 scripts/deep_search.py --priority 1 --category "Food & Dining"
  python3 scripts/deep_search.py --only-free --location "Golden Gate Park"
  python3 scripts/deep_search.py --live-reddit-search --query "free museum"
  python3 scripts/deep_search.py --export-json results.json --export-csv results.csv
"""

import os
import sys
import json
import csv
import argparse
import urllib.request
import urllib.parse
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEALS_PATH = os.path.join(ROOT_DIR, "data", "deals.json")
SOURCES_PATH = os.path.join(ROOT_DIR, "data", "sources.json")

# ANSI color codes for rich CLI terminal formatting
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_CYAN = "\033[96m"
COLOR_RED = "\033[91m"

def load_local_deals():
    if not os.path.exists(DEALS_PATH):
        print(f"{COLOR_RED}Error: {DEALS_PATH} not found.{COLOR_RESET}")
        return []
    with open(DEALS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def filter_deals(deals, query=None, priority=None, category=None, location=None, only_free=False, verified_only=False):
    results = []
    for d in deals:
        # Priority filter
        if only_free and d.get("priority_rank") != 1:
            continue
        if priority and str(d.get("priority_rank")) != str(priority):
            continue
        
        # Category filter
        if category and category.lower() not in d.get("category", "").lower():
            continue

        # Location filter
        if location and location.lower() not in d.get("location", "").lower():
            continue

        # Verified filter
        if verified_only:
            v_status = d.get("verification", {}).get("status", "")
            if "Verified" not in v_status:
                continue

        # Query filter across title, description, instructions, tags, and location
        if query:
            q = query.lower()
            text_pool = " ".join([
                d.get("title", ""),
                d.get("description", ""),
                d.get("redemption_instructions", ""),
                d.get("location", ""),
                d.get("category", ""),
                " ".join(d.get("tags", []))
            ]).lower()
            if q not in text_pool:
                continue

        results.append(d)

    # Sort results by priority_rank ascending (100% Free first), then title
    results.sort(key=lambda x: (x.get("priority_rank", 99), x.get("title", "")))
    return results

def live_reddit_search(query_str, subreddits=None, limit=10):
    """
    Performs deep live community search on Reddit JSON API across r/sanfrancisco,
    r/bayarea, r/freebies, and r/SFEvents to discover candidate promotions.
    """
    if not subreddits:
        subreddits = ["sanfrancisco", "bayarea", "freebies", "SFEvents", "AskSF"]
    
    print(f"\n{COLOR_CYAN}{COLOR_BOLD}🔍 Running Live Deep Search on Reddit APIs across subreddits: {', '.join(subreddits)}...{COLOR_RESET}")
    print(f"   Query keywords: '{query_str}'\n")

    discovered_candidates = []
    headers = {"User-Agent": "CouponsDealsSF-DeepSearchBot/1.0 (Arena.ai Project)"}

    for sub in subreddits:
        try:
            q = urllib.parse.quote(query_str)
            url = f"https://www.reddit.com/r/{sub}/search.json?q={q}&restrict_sr=1&sort=new&limit={limit}"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                children = data.get("data", {}).get("children", [])
                for child in children:
                    post = child.get("data", {})
                    title = post.get("title", "")
                    permalink = "https://www.reddit.com" + post.get("permalink", "")
                    score = post.get("score", 0)
                    created_utc = post.get("created_utc", 0)
                    
                    # Score priority: if "100% free" or "no purchase" or "freebie" in title, Priority 1
                    t_lower = title.lower()
                    if any(w in t_lower for w in ["100% free", "no purchase", "free admission", "freebie", "free ticket"]):
                        p_label = "100% Free"
                        p_rank = 1
                    elif any(w in t_lower for w in ["bogo", "free with", "free gift"]):
                        p_label = "Free with Purchase"
                        p_rank = 2
                    else:
                        p_label = "Discount/Coupon"
                        p_rank = 3

                    discovered_candidates.append({
                        "source_subreddit": f"r/{sub}",
                        "title": title,
                        "url": permalink,
                        "priority_label": p_label,
                        "priority_rank": p_rank,
                        "upvotes": score
                    })
        except Exception as e:
            print(f"{COLOR_YELLOW}   [!] Could not query r/{sub}: {e}{COLOR_RESET}")

    return discovered_candidates

def display_results_cli(deals):
    if not deals:
        print(f"{COLOR_YELLOW}No matching deals found for the specified filters.{COLOR_RESET}")
        return

    print(f"{COLOR_BOLD}{COLOR_GREEN}=== Found {len(deals)} Matching SF/Bay Area Deals (Sorted by Highest Priority #1 first) ==={COLOR_RESET}\n")
    for idx, d in enumerate(deals, 1):
        p_rank = d.get("priority_rank", 99)
        p_label = d.get("priority_label", "Unknown")
        p_color = COLOR_GREEN if p_rank == 1 else (COLOR_YELLOW if p_rank == 2 else COLOR_BLUE)
        
        print(f"{COLOR_BOLD}{idx}. [{p_color}Priority #{p_rank}: {p_label}{COLOR_RESET}{COLOR_BOLD}] {d.get('title')}{COLOR_RESET}")
        print(f"   📍 Location: {d.get('location')} | 🏷️ Category: {d.get('category')} | 💰 Value: {d.get('value')}")
        print(f"   🛡️ Verification: {d.get('verification', {}).get('status')} ({d.get('verification', {}).get('source_name')})")
        print(f"   📝 Description: {d.get('description')[:140]}...")
        print(f"   🔗 Official URL: {COLOR_CYAN}{d.get('promotion_url')}{COLOR_RESET}\n")

def export_to_json(deals, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(deals, f, indent=2)
    print(f"{COLOR_GREEN}✅ Exported {len(deals)} results to JSON file: {filepath}{COLOR_RESET}")

def export_to_csv(deals, filepath):
    if not deals:
        return
    fieldnames = [
        "id", "priority_rank", "priority_label", "title", "category",
        "location", "value", "verification_status", "verified_by", "promotion_url", "description"
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d in deals:
            writer.writerow({
                "id": d.get("id", ""),
                "priority_rank": d.get("priority_rank", ""),
                "priority_label": d.get("priority_label", ""),
                "title": d.get("title", ""),
                "category": d.get("category", ""),
                "location": d.get("location", ""),
                "value": d.get("value", ""),
                "verification_status": d.get("verification", {}).get("status", ""),
                "verified_by": d.get("verification", {}).get("source_name", ""),
                "promotion_url": d.get("promotion_url", ""),
                "description": d.get("description", "")
            })
    print(f"{COLOR_GREEN}✅ Exported {len(deals)} results to CSV file: {filepath}{COLOR_RESET}")

def main():
    parser = argparse.ArgumentParser(description="CouponsDealsSF Deep Search & Aggregator Engine")
    parser.add_argument("--query", "-q", help="Search keyword across title, description, location, and tags")
    parser.add_argument("--priority", "-p", choices=["1", "2", "3"], help="Filter by Priority rank (1 = 100% Free, 2 = Purchase Required, 3 = Discount)")
    parser.add_argument("--category", "-c", help="Filter by Category (e.g., 'Museums', 'Food', 'Transit', 'Birthdays')")
    parser.add_argument("--location", "-l", help="Filter by Location (e.g., 'SoMa', 'Golden Gate Park', 'Oakland')")
    parser.add_argument("--only-free", action="store_true", help="Shortcut to show ONLY 100%% Free deals (Priority #1)")
    parser.add_argument("--verified-only", action="store_true", help="Show only verified deals")
    parser.add_argument("--live-reddit-search", action="store_true", help="Run live deep search across Reddit APIs for candidate promotions")
    parser.add_argument("--export-json", help="File path to export search results as JSON")
    parser.add_argument("--export-csv", help="File path to export search results as CSV")
    
    args = parser.parse_args()

    deals = load_local_deals()
    filtered = filter_deals(
        deals,
        query=args.query,
        priority=args.priority,
        category=args.category,
        location=args.location,
        only_free=args.only_free,
        verified_only=args.verified_only
    )

    display_results_cli(filtered)

    if args.export_json:
        export_to_json(filtered, args.export_json)

    if args.export_csv:
        export_to_csv(filtered, args.export_csv)

    if args.live_reddit_search:
        query_kw = args.query if args.query else "free san francisco"
        reddit_candidates = live_reddit_search(query_kw)
        if reddit_candidates:
            print(f"{COLOR_BOLD}{COLOR_CYAN}=== Discovered {len(reddit_candidates)} Live Reddit Candidate Promotions ==={COLOR_RESET}")
            for idx, cand in enumerate(reddit_candidates, 1):
                p_label = cand["priority_label"]
                p_rank = cand["priority_rank"]
                p_color = COLOR_GREEN if p_rank == 1 else (COLOR_YELLOW if p_rank == 2 else COLOR_BLUE)
                print(f"  {idx}. [{cand['source_subreddit']}] [{p_color}{p_label}{COLOR_RESET}] {cand['title']}")
                print(f"     🔗 URL: {cand['url']} (Score: {cand['upvotes']})\n")
        else:
            print(f"{COLOR_YELLOW}No new Reddit candidates found or network unreachable.{COLOR_RESET}")

if __name__ == "__main__":
    main()

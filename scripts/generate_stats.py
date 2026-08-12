#!/usr/bin/env python3
"""
generate_stats.py
Generates summary analytics and verification statistics from data/deals.json and data/sources.json
for display on the GitHub Pages web application.
"""
import json
import os
from collections import Counter
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEALS_PATH = os.path.join(ROOT_DIR, "data", "deals.json")
SOURCES_PATH = os.path.join(ROOT_DIR, "data", "sources.json")
STATS_PATH = os.path.join(ROOT_DIR, "data", "stats.json")

def generate_stats():
    with open(DEALS_PATH, "r", encoding="utf-8") as f:
        deals = json.load(f)
    
    with open(SOURCES_PATH, "r", encoding="utf-8") as f:
        sources_data = json.load(f)

    total_deals = len(deals)
    priority_counts = Counter(d.get("priority_label", "Unknown") for d in deals)
    category_counts = Counter(d.get("category", "Uncategorized") for d in deals)
    location_counts = Counter(d.get("location", "Unknown Location") for d in deals)
    verification_counts = Counter(d.get("verification", {}).get("status", "Unverified") for d in deals)
    
    # Calculate percentage of deals that are 100% Free
    free_count = priority_counts.get("100% Free", 0)
    free_percentage = round((free_count / total_deals) * 100, 1) if total_deals > 0 else 0

    # Total monitored sources
    total_sources = (
        len(sources_data.get("official_sources", [])) +
        len(sources_data.get("news_and_media_sources", [])) +
        len(sources_data.get("community_sources", []))
    )

    stats = {
        "last_compiled": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_deals": total_deals,
        "free_deals_count": free_count,
        "free_percentage": f"{free_percentage}%",
        "total_monitored_sources": total_sources,
        "priority_distribution": dict(priority_counts),
        "category_distribution": dict(category_counts),
        "location_distribution": dict(location_counts),
        "verification_status_breakdown": dict(verification_counts)
    }

    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print(f"✅ Successfully generated statistics: {total_deals} deals ({free_percentage}% 100% Free) -> data/stats.json")

if __name__ == "__main__":
    generate_stats()

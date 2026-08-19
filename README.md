# 🌉 CouponsDealsSF — Verified San Francisco & Bay Area Freebies, Deals & Promotions

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20App-10b981?style=for-the-badge&logo=github)](https://karagemop466-tech.github.io/CouponsDealsSF/)
[![Verified Deals](https://img.shields.io/badge/Official%20100%25%20Free-53%20Active-059669?style=for-the-badge)](data/deals.json)
[![100% Free Priority #1](https://img.shields.io/badge/100%25%20Free%20No%20Purchase-100%25-10b981?style=for-the-badge)](data/deals.json)
[![Audited for 2026](https://img.shields.io/badge/Audited%20For-2026-3b82f6?style=for-the-badge)](data/sources.json)

> **The ultimate verified, open-source database and interactive GitHub Pages web application for discovering, compiling, and organizing freebies, coupons, and promotions redeemable in San Francisco and the Bay Area.**

---

## 🌟 Live Interactive Web Application & Upgrades

Explore **53 official 100% free / no-purchase** deals, filter by neighborhood, run live deep searches, and export calendar invites on our GitHub Pages web app:

**👉 [https://karagemop466-tech.github.io/CouponsDealsSF/](https://karagemop466-tech.github.io/CouponsDealsSF/)**

### 🚀 Major v2 Upgrades Built Into This Release:
1. **Interactive View Switcher**:
   - **🎴 Cards Grid View**: Visual cards with priority badges, savings tags, and one-click actions.
   - **📋 Compact Table View**: Sortable table for fast scanning across categories, locations, and values.
   - **🗺️ Neighborhood Explorer View**: Groups official free deals into SF neighborhood and regional clusters (*SoMa/Downtown, Golden Gate Park/Richmond, Mission/Castro, Chinatown/North Beach, Oakland/East Bay, San Jose/South Bay*).
2. **Active Schedule & Eligibility Calendar Engine**:
   - Quick-filter chips for **⚡ Free Today (Wednesday)** (dynamically matches your local weekday), **📅 Free This Weekend**, **🎂 Birthday Perks ($0 Cost)**, **🪪 Resident ID Required**, and **♾️ Always Free**.
3. **One-Click `.ICS` Calendar Export & Google Calendar Integration**:
   - Click **"📅 Add to Calendar"** on any deal modal to generate an instant Google Calendar event or download a pre-formatted `.ics` calendar invite with full redemption instructions and official links.
4. **Personal "My Saved Freebies Wallet" & Total Value Counter**:
   - Save your favorite freebies to your browser's local wallet using the **☆ Save** button on any card.
   - Live banner tracking official **100% free / no-purchase-necessary** programs only. Purchase, BOGO, and discount deals were removed after the 2026-08-19 official-source audit.
5. **Live Candidate Scraper Feed (`scripts/live_scraper.py`)**:
   - An automated web & community API aggregator that discovers candidate promotions, scores their priority, deduplicates against `data/deals.json`, and outputs `data/candidates.json` for review.

---

## 🚨 Strict Priority Ranking Framework

CouponsDealsSF organizes every promotion using a strict **Priority Ranking Hierarchy**. Why pay when you can get it for 100% free?

| Priority Tier | Badge | Definition | % in Database | Examples in Database |
| :--- | :---: | :--- | :---: | :--- |
| **Priority #1 (only published tier)** | ⭐ `100% FREE` | **Absolutely $0 cost / no purchase necessary**, confirmed on an official page. | **100% (53 / 53)** | • de Young & Legion of Honor Free Saturdays for Bay Area Residents<br>• SFMTA Free Muni for All Youth (18 & Under)<br>• SFPL Discover & Go<br>• ICA SF (always free)<br>• Conservatory of Flowers First Tuesday & SF resident/veteran days |
| **Not published** | 🎁 / 🏷️ | Free-with-purchase, BOGO, discounts, unofficial community tips, and ended seasonal series | **Removed** | Chipotle, Ike’s, BWW, Quiznos, Underdogs, CHSA paid tickets, Clipper BayPass, Off the Grid (ended), TATO, Banya, Balboa, Ghirardelli samples, Baskin birthday (not guaranteed free), Stern Grove 2026 season (ended), SFO Terminal Sessions (ended), Bay Wheels |

---

## 🛡️ Verification Methodology & Monitored Sources

Every entry in `data/deals.json` is audited and verified against official authority policies, local press releases, or verified community forum discussions. See `data/sources.json` for our full registry of monitored sources:

1. **Official Sources (`trust_score: 100`)**:
   - San Francisco Museum of Modern Art (SFMOMA) Policy
   - Fine Arts Museums of SF (de Young & Legion of Honor) Policy
   - San Francisco Botanical Garden & Conservatory of Flowers Rules
   - San Francisco Municipal Transportation Agency (SFMTA) Free Muni Program
   - SF Public Library (SFPL) Discover & Go and Digital Subscription Services
   - Asian Art Museum, OMCA, BAMPFA, ICA SF, Randall Museum, Cantor Arts Center, and Museum of Craft and Design Official Free Days
2. **News & Press Releases (`trust_score: 90–95`)**:
   - *SFGate*, *San Francisco Chronicle*, *DoTheBay*, *FuncheapSF*
3. **Community & Reddit Verification (`trust_score: 80–85`)**:
   - Monitored Subreddits: **r/sanfrancisco**, **r/bayarea**, **r/freebies**, **r/SFEvents**, **r/AskSF**

---

## 💻 Python Deep Search & Verification Suite (`scripts/`)

In addition to the web app, this repository includes a full-featured Python command-line toolkit for deep searching, scraping, adding, and verifying deals:

### 1. Live Candidate Scraper (`scripts/live_scraper.py`)
Fetches live feeds from community APIs (`r/sanfrancisco`, `r/bayarea`, `r/freebies`, `r/SFEvents`), scores candidate priority (100% free = rank 1), deduplicates against existing deals, and exports `data/candidates.json`:
```bash
python3 scripts/live_scraper.py
```

### 2. Deep Search Engine (`scripts/deep_search.py`)
Search the local database by keyword, priority, category, neighborhood, or run a live query against Reddit JSON APIs to discover new promotions:
```bash
# Search for 100% free museum deals:
python3 scripts/deep_search.py --query "museum" --only-free

# Filter by SF neighborhood or Bay Area location:
python3 scripts/deep_search.py --location "Golden Gate Park"

# Export filtered results to JSON or CSV:
python3 scripts/deep_search.py --only-free --export-json freebies.json --export-csv freebies.csv
```

### 3. Automated Link & Schema Validator (`scripts/verify_links.py`)
Audits `data/deals.json` to ensure every deal has valid required fields, URLs, verification proof, and enforces that Priority #1 deals are labeled `"100% Free"`:
```bash
python3 scripts/verify_links.py
```

### 4. Add Deal CLI Utility (`scripts/add_deal.py`)
Add a new verified deal cleanly and update database analytics:
```bash
python3 scripts/add_deal.py --json '{"id":"my-new-freebie", "title":"Free Coffee at XYZ", "priority_rank":1, ...}'
```

### 5. Stats Generator (`scripts/generate_stats.py`)
Re-compiles aggregate database metrics (`data/stats.json`) for the web application dashboard:
```bash
python3 scripts/generate_stats.py
```

---

## 🗂️ Database Structure (`data/deals.json`)

All **53** official 100% free / no-purchase deals are stored in `data/deals.json`. Each object follows this schema:

```json
{
  "id": "ica-sf-the-cube-always-free",
  "title": "ICA SF (Institute of Contemporary Art) at The Cube - 100% Free Admission",
  "priority_label": "100% Free",
  "priority_rank": 1,
  "category": "Museums & Arts",
  "location": "SF - SoMa / Downtown",
  "value": "$20 value",
  "description": "Located in a stunning 5-story atrium at 345 Montgomery Street in downtown San Francisco ('The Cube'), ICA SF offers 100% free admission to all cutting-edge contemporary art exhibitions.",
  "redemption_instructions": "1. Visit ICA SF at 345 Montgomery Street...\n2. Open Wednesday through Sunday, 11:00 AM to 5:00 PM...\n3. Enjoy complimentary walk-in entry...",
  "restrictions": "Closed Mondays and Tuesdays. Always free general admission.",
  "verification": {
    "status": "Verified Official Source",
    "source_name": "ICA SF Official Admission Policy",
    "verified_date": "2026-08-19",
    "notes": "Confirmed on icasf.org and SF Standard / Funcheap 2026 arts directory."
  },
  "promotion_url": "https://www.icasf.org/visit",
  "community_url": "https://sf.funcheap.com/city-guide/free-sf-art-museum-opens-historic-downtown-bank-building-cube/",
  "tags": ["museum", "100-percent-free", "financial-district", "downtown", "contemporary-art", "always-free"],
  "is_new": true,
  "schedule_type": "Always Free",
  "neighborhood_slug": "sf-soma-downtown"
}
```

---

## 🌁 SF Neighborhood & Regional Coverage

Our verified database spans San Francisco neighborhoods and regional Bay Area counties:
- **SF - SoMa / Downtown / Yerba Buena**: SFMOMA, YBCA, MoAD, ICA SF, SF Railway Museum, Sephora birthday gift (in-store)
- **SF - Golden Gate Park / Richmond**: de Young, SF Botanical Garden, Conservatory of Flowers, Japanese Tea Garden, SF Opera in the Park
- **SF - Lincoln Park / Sea Cliff**: Legion of Honor
- **SF - Mission / Castro**: Randall Museum, Mission Food Hub (Friday), Museum of Craft and Design, GLBT Historical Society
- **SF - Chinatown / North Beach / Wharf**: Cable Car Museum
- **SF - All Neighborhoods / Marina**: SFMTA Free Muni for Youth, SFPL Discover & Go, SFPL NYT/Kanopy, SF Zoo resident free days (calendar), SF Camerawork (Fort Mason)
- **Oakland / East Bay**: OMCA, BAMPFA
- **San Jose / South Bay / Peninsula**: Cantor Arts Center, Anderson Collection, Nothing Bundt Cakes birthday Bundtlet
- **Bay Area Wide**: Bank of America Museums on Us

---

## 🤝 How to Contribute

We welcome community pull requests for new verified freebies and deals!

1. Fork this repository and create a new feature branch.
2. Add your verified deal to `data/deals.json` (or use `python3 scripts/add_deal.py`).
3. Ensure your deal follows our **Priority Rules**:
   - Publish **only** `"priority_rank": 1` / `"priority_label": "100% Free"` deals with zero purchase required and an official source URL.
   - Do not add BOGOs, free-with-purchase, or discount deals to `deals.json`.
4. Run automated verification:
   ```bash
   python3 scripts/verify_links.py
   python3 scripts/generate_stats.py
   ```
5. Open a Pull Request!

---

## 📄 License

This repository and data are open source under the MIT License. Built with love for San Francisco & the Bay Area community.

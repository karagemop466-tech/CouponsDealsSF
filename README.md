# 🌉 CouponsDealsSF — Verified San Francisco & Bay Area Freebies, Deals & Promotions

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20App-10b981?style=for-the-badge&logo=github)](https://karagemop466-tech.github.io/CouponsDealsSF/)
[![Verified Deals](https://img.shields.io/badge/Verified%20Deals-38%20Active-059669?style=for-the-badge)](data/deals.json)
[![100% Free Priority #1](https://img.shields.io/badge/100%25%20Free%20Priority%20%231-89.5%25-10b981?style=for-the-badge)](data/deals.json)
[![Audited for 2026](https://img.shields.io/badge/Audited%20For-2026-3b82f6?style=for-the-badge)](data/sources.json)

> **The ultimate verified, open-source database and interactive GitHub Pages web application for discovering, compiling, and organizing freebies, coupons, and promotions redeemable in San Francisco and the Bay Area.**

---

## 🌟 Live Interactive Web Application

Explore all compiled deals, filter by priority and neighborhood, run live deep searches, and view verification proof on our GitHub Pages web app:

**👉 [https://karagemop466-tech.github.io/CouponsDealsSF/](https://karagemop466-tech.github.io/CouponsDealsSF/)**

---

## 🚨 Strict Priority Ranking Framework

CouponsDealsSF organizes every promotion using a strict **Priority Ranking Hierarchy**. Why pay when you can get it for 100% free?

| Priority Tier | Badge | Definition | Examples in Database |
| :--- | :---: | :--- | :--- |
| **Priority #1 (Highest Priority)** | ⭐ `100% FREE` | **Absolutely $0 Cost / No Purchase Necessary.** Free museum admission, free transit passes, free groceries, and birthday items with zero purchase requirements. | • de Young & Legion of Honor Free Saturdays for Bay Area Residents<br>• SFMTA 100% Free Muni for All Youth (18 & Under)<br>• SFPL Discover & Go Free Museum Passes<br>• Archimedes Banya Free Full Day Bath Pass on Birthday |
| **Priority #2 (Secondary Priority)** | 🎁 `FREE WITH PURCHASE` | **Free Item with Purchase / BOGO.** Buy-One-Get-One-Free deals or complimentary perks with a low-barrier order. | • Chipotle Free Guacamole / Chips with $5+ Purchase<br>• Quiznos BOGO Free Birthday Sub<br>• Buffalo Wild Wings 6 Free Birthday Wings with $10 order |
| **Priority #3 (Tertiary Priority)** | 🏷️ `DISCOUNT / SPECIAL` | **Coupons & Significant Discounts.** Substantial regional savings, happy hour specials, and commuter discounts. | • Underdogs Cantina $1 Margaritas & Disco Taco Tuesday (SoMa) |

---

## 🛡️ Verification Methodology & Monitored Sources

Every entry in `data/deals.json` is audited and verified against official authority policies, local press releases, or verified community forum discussions. See `data/sources.json` for our full registry of monitored sources:

1. **Official Sources (`trust_score: 100`)**:
   - San Francisco Museum of Modern Art (SFMOMA) Policy
   - Fine Arts Museums of SF (de Young & Legion of Honor) Policy
   - San Francisco Botanical Garden & Conservatory of Flowers Rules
   - San Francisco Municipal Transportation Agency (SFMTA) Free Muni Program
   - SF Public Library (SFPL) Discover & Go and Digital Subscription Services
   - Asian Art Museum, OMCA, BAMPFA, and Museum of Craft and Design Official Free Days
2. **News & Press Releases (`trust_score: 90–95`)**:
   - *SFGate*, *San Francisco Chronicle*, *DoTheBay*, *FuncheapSF*
3. **Community & Reddit Verification (`trust_score: 80–85`)**:
   - Monitored Subreddits: **r/sanfrancisco**, **r/bayarea**, **r/freebies**, **r/SFEvents**, **r/AskSF**

---

## 💻 Python Deep Search & Verification Suite (`scripts/`)

In addition to the web app, this repository includes a full-featured Python command-line toolkit for deep searching, scraping, adding, and verifying deals:

### 1. Deep Search Engine (`scripts/deep_search.py`)
Search the local database by keyword, priority, category, neighborhood, or run a live query against Reddit JSON APIs (`r/sanfrancisco`, `r/bayarea`, `r/freebies`) to discover new promotions:
```bash
# Search for 100% free museum deals:
python3 scripts/deep_search.py --query "museum" --only-free

# Filter by SF neighborhood or Bay Area location:
python3 scripts/deep_search.py --location "Golden Gate Park"

# Run a live deep search against Reddit community APIs:
python3 scripts/deep_search.py --live-reddit-search --query "free museum"

# Export filtered results to JSON or CSV:
python3 scripts/deep_search.py --only-free --export-json freebies.json --export-csv freebies.csv
```

### 2. Automated Link & Schema Validator (`scripts/verify_links.py`)
Audits `data/deals.json` to ensure every deal has valid required fields, URLs, verification proof, and enforces that Priority #1 deals are labeled `"100% Free"`:
```bash
python3 scripts/verify_links.py
```
*(Runs automatically in GitHub Actions CI on pushes and pull requests).*

### 3. Add Deal CLI Utility (`scripts/add_deal.py`)
Add a new verified deal cleanly and update database analytics:
```bash
python3 scripts/add_deal.py --json '{"id":"my-new-freebie", "title":"Free Coffee at XYZ", "priority_rank":1, ...}'
```

### 4. Stats Generator (`scripts/generate_stats.py`)
Re-compiles aggregate database metrics (`data/stats.json`) for the web application dashboard:
```bash
python3 scripts/generate_stats.py
```

---

## 🗂️ Database Structure (`data/deals.json`)

All deals are stored in a standard JSON array in `data/deals.json`. Each object follows this schema:

```json
{
  "id": "deyoung-free-first-tuesday-and-saturdays",
  "title": "de Young Museum - Free Every Saturday for Bay Area Residents & First Tuesdays for All",
  "priority_label": "100% Free",
  "priority_rank": 1,
  "category": "Museums & Arts",
  "location": "SF - Golden Gate Park / Richmond",
  "value": "$20 value per person",
  "description": "The de Young Museum in Golden Gate Park offers 100% free general admission to permanent collection galleries every Saturday for all Bay Area residents...",
  "redemption_instructions": "1. Book a timed general admission ticket online at deyoung.famsf.org...\n2. Select 'Bay Area Resident Saturday' ($0.00)...\n3. Bring proof of 9-county Bay Area residency...",
  "restrictions": "Valid for permanent collection galleries; special ticketed exhibitions require separate ticket...",
  "verification": {
    "status": "Verified Official Source",
    "source_name": "de Young & Legion of Honor (FAMSF) Official Policy",
    "verified_date": "2026-08-12",
    "notes": "Confirmed on official FAMSF admission page and SFGate museum guide."
  },
  "promotion_url": "https://www.famsf.org/visit/free-reduced-admission",
  "community_url": "https://www.sfgate.com/local/article/san-francisco-museums-17796937.php",
  "tags": ["museum", "100-percent-free", "bay-area-resident", "golden-gate-park", "saturday"],
  "is_new": true
}
```

---

## 🌁 SF Neighborhood & Regional Coverage

Our verified database spans San Francisco neighborhoods and regional Bay Area counties:
- **SF - SoMa / Downtown / Yerba Buena**: SFMOMA, YBCA, MoAD, Archimedes Banya, Underdogs Cantina, Treasure Island Ferry
- **SF - Golden Gate Park / Richmond**: de Young Museum, SF Botanical Garden, Conservatory of Flowers, Japanese Tea Garden, Balboa Theater, Skatin' Place
- **SF - Lincoln Park / Sea Cliff**: Legion of Honor
- **SF - Mission / Castro**: Mission Food Hub, TATO Free Tacos, Museum of Craft and Design, GLBT Historical Society
- **SF - Chinatown / North Beach / Wharf**: Chinatown Night Market, Cable Car Museum, Chinese Historical Society (CHSA), Ghirardelli Square Free Chocolate, Musée Mécanique
- **SF - All Neighborhoods**: SFMTA Free Muni for Youth, SFPL Discover & Go, SFPL Free Digital NYT/WSJ Passes, SF Zoo
- **Oakland / East Bay**: Oakland Museum of California (OMCA), Berkeley BAMPFA
- **Bay Area Wide**: Bank of America Museums on Us, Clipper BayPass, Baskin-Robbins, Nothing Bundt Cakes, Ike's Sandwiches, Chipotle

---

## 🤝 How to Contribute

We welcome community pull requests for new verified freebies and deals!

1. Fork this repository and create a new feature branch.
2. Add your verified deal to `data/deals.json` (or use `python3 scripts/add_deal.py`).
3. Ensure your deal follows our **Priority Rules**:
   - Assign `"priority_rank": 1` and `"priority_label": "100% Free"` ONLY if zero purchase is required.
   - Assign `"priority_rank": 2` for BOGOs or Free-with-Purchase deals.
4. Run automated verification:
   ```bash
   python3 scripts/verify_links.py
   python3 scripts/generate_stats.py
   ```
5. Open a Pull Request! Our automated CI workflow will audit your submission.

---

## 📄 License

This repository and data are open source under the MIT License. Built with love for San Francisco & the Bay Area community.

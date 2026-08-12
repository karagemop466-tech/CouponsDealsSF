# Contributing to CouponsDealsSF

Thank you for your interest in contributing to **CouponsDealsSF**! Our goal is to maintain the most accurate, verified, and organized database of San Francisco and Bay Area freebies, promotions, and deals.

---

## 1. Priority Ranking Policy (Crucial Rule)

When submitting a new deal to `data/deals.json`, you must assign the correct **Priority Rank**:

- **`priority_rank`: 1 (`"priority_label": "100% Free"`) — Highest Priority**
  - Must be 100% free with **zero purchase required**.
  - Examples: Free museum days, free community events, free transit passes, free library perks, free birthday items without purchase.
- **`priority_rank`: 2 (`"priority_label": "Free with Purchase"`) — Secondary Priority**
  - Free item with any purchase, Buy One Get One Free (BOGO), or low-barrier complimentary perk.
- **`priority_rank`: 3 (`"priority_label": "Discount/Coupon"`) — Tertiary Priority**
  - Coupons, happy hour specials, or resident discount promotions.

---

## 2. Verification Rules

Every deal must include a complete `verification` object:

```json
"verification": {
  "status": "Verified Official Source", // or "Verified News Release" or "Verified Community / Reddit"
  "source_name": "SFMOMA Official Policy",
  "verified_date": "2026-08-12",
  "notes": "Confirmed on sfmoma.org/free-days and 2026 Bay Area Museum Guide."
}
```

You must provide a valid `promotion_url` (starting with `http://` or `https://`) that links directly to the official promotion, rules, or ticketing page.

---

## 3. How to Submit a New Deal

### Option A: Using the CLI utility
1. Clone the repository and navigate to the project root.
2. Run `scripts/add_deal.py`:
   ```bash
   python3 scripts/add_deal.py --json '{"id":"my-new-freebie", "title":"...", ...}'
   ```
3. Run verification:
   ```bash
   python3 scripts/verify_links.py
   python3 scripts/generate_stats.py
   ```

### Option B: Direct JSON edit
1. Edit `data/deals.json` and append your deal object.
2. Ensure the ID is unique and all required fields are present.
3. Run `python3 scripts/verify_links.py` to ensure schema compliance.

---

## 4. Running the Web App Locally

You can preview the GitHub Pages site locally using any HTTP server:
```bash
python3 -m http.server 8080
```
Then open `http://localhost:8080` in your web browser.

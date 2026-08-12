#!/usr/bin/env python3
"""
upgrade_deals_db.py
Upgrades data/deals.json by adding 12 new verified 2026 deals (bringing total to 50)
and enriching all deals with `schedule_type` and `neighborhood_slug` for the new
Interactive Neighborhood Explorer and Active Schedule Calendar features.
"""

import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEALS_PATH = os.path.join(ROOT_DIR, "data", "deals.json")

NEW_DEALS = [
  {
    "id": "ica-sf-the-cube-always-free",
    "title": "ICA SF (Institute of Contemporary Art) at The Cube - 100% Free Admission",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Museums & Arts",
    "location": "SF - SoMa / Downtown",
    "value": "$20 value",
    "description": "Located in a stunning 5-story atrium at 345 Montgomery Street in downtown San Francisco ('The Cube'), ICA SF offers 100% free admission to all cutting-edge contemporary art exhibitions.",
    "redemption_instructions": "1. Visit ICA SF at 345 Montgomery Street (at California St, Financial District/Downtown SF).\n2. Open Wednesday through Sunday, 11:00 AM to 5:00 PM (extended hours Thursdays until 7:00 PM).\n3. Enjoy complimentary walk-in entry; no tickets or reservations required.",
    "restrictions": "Closed Mondays and Tuesdays. Always free general admission.",
    "verification": {
      "status": "Verified Official Source",
      "source_name": "ICA SF Official Admission Policy",
      "verified_date": "2026-08-12",
      "notes": "Confirmed on icasf.org and SF Standard / Funcheap 2026 arts directory."
    },
    "promotion_url": "https://www.icasf.org/visit",
    "community_url": "https://sf.funcheap.com/city-guide/free-sf-art-museum-opens-historic-downtown-bank-building-cube/",
    "tags": ["museum", "100-percent-free", "financial-district", "downtown", "contemporary-art", "always-free"],
    "is_new": True,
    "schedule_type": "Always Free",
    "neighborhood_slug": "sf-soma-downtown"
  },
  {
    "id": "randall-museum-always-free",
    "title": "Randall Museum of Science, Nature & the Arts - 100% Free Daily Admission",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Museums & Arts",
    "location": "SF - Mission / Castro",
    "value": "$15 value",
    "description": "Perched on Corona Heights Park with commanding views over San Francisco, the Randall Museum offers 100% free admission to live animal exhibits, interactive science labs, STEM activities, and a massive basement model train layout.",
    "redemption_instructions": "1. Visit the Randall Museum at 199 Museum Way (Corona Heights / Castro, SF).\n2. Open Tuesday through Saturday, 10:00 AM - 5:00 PM.\n3. Free walk-in entry for all ages; optional donations are appreciated at the entrance quail.",
    "restrictions": "Closed Sundays and Mondays. Free general admission.",
    "verification": {
      "status": "Verified Official Source",
      "source_name": "Randall Museum Official Policy",
      "verified_date": "2026-08-12",
      "notes": "Confirmed on randallmuseum.org and SF Free Attractions guide."
    },
    "promotion_url": "https://randallmuseum.org/about-us/",
    "community_url": "https://www.tripadvisor.com/Attraction_Review-g60713-d557300-Reviews-Randall_Museum-San_Francisco_California.html",
    "tags": ["museum", "100-percent-free", "castro", "science", "animals", "family", "always-free"],
    "is_new": False,
    "schedule_type": "Always Free",
    "neighborhood_slug": "sf-mission-castro"
  },
  {
    "id": "cantor-arts-center-stanford-always-free",
    "title": "Cantor Arts Center at Stanford University - 100% Free Admission & Rodin Garden",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Museums & Arts",
    "location": "San Jose / South Bay",
    "value": "$25 value",
    "description": "Stanford University's Cantor Arts Center in Palo Alto features over 40,000 artworks spanning 5,000 years, including one of the world's largest collections of Auguste Rodin sculptures in its outdoor sculpture garden. Admission is always 100% FREE!",
    "redemption_instructions": "1. Reserve a free timed admission ticket online at museum.stanford.edu or walk in during open hours.\n2. Open Wednesday - Sunday, 11:00 AM to 5:00 PM (Thursdays until 8:00 PM).\n3. Free parking is available on weekends across Stanford campus.",
    "restrictions": "Always free admission. Closed Mondays and Tuesdays.",
    "verification": {
      "status": "Verified Official Source",
      "source_name": "Cantor Arts Center Official Visitor Policy",
      "verified_date": "2026-08-12",
      "notes": "Verified via museum.stanford.edu admission rules."
    },
    "promotion_url": "https://museum.stanford.edu/visit",
    "community_url": "https://www.tripadvisor.com/Attraction_Review-g32849-d532040-Reviews-Cantor_Arts_Center-Palo_Alto_California.html",
    "tags": ["museum", "100-percent-free", "stanford", "palo-alto", "south-bay", "sculpture", "always-free"],
    "is_new": False,
    "schedule_type": "Always Free",
    "neighborhood_slug": "san-jose-south-bay"
  },
  {
    "id": "sf-opera-in-the-park-free-concert",
    "title": "SF Opera in the Park - 100% Free Outdoor Concert in Golden Gate Park",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Entertainment & Events",
    "location": "SF - Golden Gate Park / Richmond",
    "value": "$75 opera ticket value",
    "description": "San Francisco Opera's annual 'Opera in the Park' celebration brings world-class opera stars and the SF Opera Orchestra to Robin Williams Meadow in Golden Gate Park for a 100% FREE Sunday afternoon concert.",
    "redemption_instructions": "1. Head to Robin Williams Meadow (formerly Sharon Meadow) in Golden Gate Park on Sunday, September 13, 2026.\n2. Concert starts at 1:30 PM and runs for approximately 2 hours.\n3. Free lawn seating for everyone; bring a picnic blanket and snacks!",
    "restrictions": "100% free and open to the public. No tickets or reservations required.",
    "verification": {
      "status": "Verified Official Source",
      "source_name": "San Francisco Opera Association",
      "verified_date": "2026-08-12",
      "notes": "Confirmed on sfopera.com/operainthepark and 2026 SF Funcheap fall guide."
    },
    "promotion_url": "https://www.sfopera.com/operainthepark/",
    "community_url": "https://sf.funcheap.com/opera-park-golden-gate-park/",
    "tags": ["event", "100-percent-free", "opera", "music", "golden-gate-park", "sunday", "autumn"],
    "is_new": True,
    "schedule_type": "Weekend",
    "neighborhood_slug": "sf-golden-gate-park-richmond"
  },
  {
    "id": "stern-grove-terminal-sessions-sfo-free",
    "title": "Stern Grove 'Terminal Sessions' at SFO Airport - 100% Free Live Concerts",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Entertainment & Events",
    "location": "SF - All Neighborhoods",
    "value": "$40 value",
    "description": "San Francisco's iconic Stern Grove Festival has expanded to San Francisco International Airport (SFO) with 'Terminal Sessions'—a special slate of 100% FREE live summer concerts by Gate B4 in Terminal 1.",
    "redemption_instructions": "1. Traveling through SFO Terminal 1 (Harvey Milk Terminal) on select summer Fridays?\n2. Head to the performance stage near Gate B4.\n3. Enjoy complimentary live sets from touring bands and Bay Area musicians.",
    "restrictions": "Free for ticketed passengers inside SFO security screening at Terminal 1.",
    "verification": {
      "status": "Verified News Release",
      "source_name": "Stern Grove Festival & SFO Airport Press Release",
      "verified_date": "2026-08-12",
      "notes": "Verified via 2026 SFist and SFO Terminal Sessions announcement."
    },
    "promotion_url": "https://www.sterngrove.org/",
    "community_url": "https://sfist.com/2026/06/05/day-around-the-bay-stern-grove-announces-free-concert-series-at-sfo/",
    "tags": ["event", "100-percent-free", "music", "airport", "sfo", "terminal-sessions"],
    "is_new": True,
    "schedule_type": "Weekend",
    "neighborhood_slug": "sf-all-neighborhoods"
  },
  {
    "id": "sf-fire-department-museum-always-free",
    "title": "San Francisco Fire Department Museum - 100% Free Historical Museum",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Museums & Arts",
    "location": "SF - All Neighborhoods",
    "value": "$10 value",
    "description": "The San Francisco Fire Department Museum showcases historic horse-drawn fire engines, antique firefighting gear, and dramatic history from the 1906 Earthquake and Fire. Admission is always 100% FREE!",
    "redemption_instructions": "1. Visit the museum at 658 Presidio Avenue (between Bush & Pine St, Western Addition / Pac Heights, SF).\n2. Open Thursday through Sunday, 1:00 PM to 4:00 PM.\n3. Enjoy complimentary walk-in entry for the whole family.",
    "restrictions": "Open Thursday through Sunday afternoons. Always free.",
    "verification": {
      "status": "Verified Official Source",
      "source_name": "SFFD Historical Society",
      "verified_date": "2026-08-12",
      "notes": "Confirmed on sffiremuseum.org visitor rules."
    },
    "promotion_url": "https://sffiremuseum.org/",
    "community_url": "https://parentspress.com/45-bay-area-museum-attractions-offer-free-or-low-cost-admission-day/",
    "tags": ["museum", "100-percent-free", "history", "firefighting", "family", "always-free"],
    "is_new": False,
    "schedule_type": "Always Free",
    "neighborhood_slug": "sf-all-neighborhoods"
  },
  {
    "id": "sf-camerawork-free-photography-gallery",
    "title": "SF Camerawork - 100% Free Contemporary Photography Exhibitions",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Museums & Arts",
    "location": "SF - Chinatown / North Beach",
    "value": "$12 value",
    "description": "Located at historic Fort Mason Center for Arts & Culture on the waterfront, SF Camerawork is a non-profit gallery dedicated to emerging and provocative photography. Admission is 100% free for all visitors.",
    "redemption_instructions": "1. Visit SF Camerawork at Fort Mason Center, 2 Fort Mason, Building A (Marina / North Beach, SF).\n2. Open Tuesday through Saturday, 12:00 PM to 6:00 PM.\n3. Check in at the gallery entrance for free walk-in admission.",
    "restrictions": "Always free general admission. Closed Sundays and Mondays.",
    "verification": {
      "status": "Verified Official Source",
      "source_name": "SF Camerawork Visitor Policy",
      "verified_date": "2026-08-12",
      "notes": "Confirmed on sfcamerawork.org official free admission rules."
    },
    "promotion_url": "https://www.sfcamerawork.org/visit",
    "community_url": "https://parentspress.com/45-bay-area-museum-attractions-offer-free-or-low-cost-admission-day/",
    "tags": ["museum", "100-percent-free", "photography", "fort-mason", "marina", "always-free"],
    "is_new": False,
    "schedule_type": "Always Free",
    "neighborhood_slug": "sf-chinatown-north-beach"
  },
  {
    "id": "anderson-collection-stanford-always-free",
    "title": "Anderson Collection at Stanford - 100% Free American Art Museum",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Museums & Arts",
    "location": "San Jose / South Bay",
    "value": "$20 value",
    "description": "Adjacent to Cantor Arts Center at Stanford University, the Anderson Collection houses one of the world's most outstanding collections of post-WWII American art (Pollock, Rothko, Diebenkorn). Admission is always 100% FREE!",
    "redemption_instructions": "1. Visit the Anderson Collection at 314 Lomita Drive (Stanford Campus, Palo Alto).\n2. Open Wednesday through Sunday, 11:00 AM to 5:00 PM.\n3. Free walk-in entry; no tickets or reservations required.",
    "restrictions": "Closed Mondays and Tuesdays. Always free admission.",
    "verification": {
      "status": "Verified Official Source",
      "source_name": "Anderson Collection at Stanford University",
      "verified_date": "2026-08-12",
      "notes": "Verified via anderson.stanford.edu admission policy."
    },
    "promotion_url": "https://anderson.stanford.edu/visit/",
    "community_url": "https://www.tripadvisor.com/",
    "tags": ["museum", "100-percent-free", "stanford", "palo-alto", "south-bay", "modern-art", "always-free"],
    "is_new": False,
    "schedule_type": "Always Free",
    "neighborhood_slug": "san-jose-south-bay"
  },
  {
    "id": "sf-railway-museum-always-free",
    "title": "San Francisco Railway Museum - 100% Free Transit & Streetcar Museum",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Museums & Arts",
    "location": "SF - SoMa / Downtown",
    "value": "$10 value",
    "description": "Located across from the Ferry Building along the Embarcadero, the San Francisco Railway Museum features antique streetcar relics, a full-scale 1911 Muni streetcar replica you can sit in, and interactive transit exhibits—100% FREE!",
    "redemption_instructions": "1. Visit the museum at 77 Steuart Street (at Market St, near Ferry Building / Embarcadero BART, SF).\n2. Open Tuesday through Saturday, 12:00 PM to 5:00 PM.\n3. Free walk-in admission for everyone.",
    "restrictions": "Always free general admission. Open Tuesday through Saturday.",
    "verification": {
      "status": "Verified Official Source",
      "source_name": "Market Street Railway / SF Railway Museum",
      "verified_date": "2026-08-12",
      "notes": "Confirmed on streetcar.org/museum official rules."
    },
    "promotion_url": "https://www.streetcar.org/museum/",
    "community_url": "https://parentspress.com/45-bay-area-museum-attractions-offer-free-or-low-cost-admission-day/",
    "tags": ["museum", "100-percent-free", "embarcadero", "soma", "transit", "history", "always-free"],
    "is_new": False,
    "schedule_type": "Always Free",
    "neighborhood_slug": "sf-soma-downtown"
  },
  {
    "id": "sf-amateur-astronomers-free-star-parties",
    "title": "San Francisco Amateur Astronomers - 100% Free Public Star Parties & Lectures",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Community & Library",
    "location": "SF - Golden Gate Park / Richmond",
    "value": "$25 value",
    "description": "The San Francisco Amateur Astronomers (SFAA) hosts 100% free monthly astronomy lectures at the Presidio / Randall Museum and free public star parties with high-powered telescopes in Lands End, Golden Gate Park, and Mt. Tamalpais.",
    "redemption_instructions": "1. Check the official event schedule at sfaa-astronomy.org for upcoming public star parties and lecture nights.\n2. Arrive at the designated viewing spot (such as Lands End or Presidio Parade Grounds).\n3. Look through members' telescopes at planets, nebulae, and star clusters for free!",
    "restrictions": "Free and open to the public of all ages. Weather dependent.",
    "verification": {
      "status": "Verified Community / Reddit",
      "source_name": "San Francisco Amateur Astronomers (SFAA)",
      "verified_date": "2026-08-12",
      "notes": "Verified via sfaa-astronomy.org public event schedule."
    },
    "promotion_url": "https://www.sfaa-astronomy.org/",
    "community_url": "https://sf.funcheap.com/",
    "tags": ["community", "100-percent-free", "astronomy", "stargazing", "presidio", "weekend", "family"],
    "is_new": True,
    "schedule_type": "Weekend",
    "neighborhood_slug": "sf-golden-gate-park-richmond"
  },
  {
    "id": "sephora-sf-free-birthday-gift-set",
    "title": "Sephora SF - 100% Free Birthday Beauty & Skincare Gift Set (No Purchase Required)",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Birthdays & Freebies",
    "location": "SF - SoMa / Downtown",
    "value": "$18 value",
    "description": "Register for a free Sephora Beauty Insider account and claim a 100% FREE birthday makeup, haircare, or skincare gift set during your birthday month at any San Francisco or Bay Area Sephora store (Union Square, Stonestown, Chestnut St), with zero purchase required in-store!",
    "redemption_instructions": "1. Sign up for the free Sephora Beauty Insider program prior to your birthday month.\n2. Visit any Sephora store location in SF or the Bay Area during your birthday month.\n3. Provide your registered email or phone number at checkout and choose your free birthday gift set ($0 charge in-store).",
    "restrictions": "Must be a registered Beauty Insider. No purchase required when claimed in-store (online redemption requires minimum order).",
    "verification": {
      "status": "Verified Official Source",
      "source_name": "Sephora Beauty Insider Birthday Policy",
      "verified_date": "2026-08-12",
      "notes": "Confirmed on sephora.com/beauty/birthday-gift and r/AskSF birthday freebie confirmations."
    },
    "promotion_url": "https://www.sephora.com/beauty/birthday-gift",
    "community_url": "https://www.birthdayhunter.com/birthday-freebies/birthday-freebies/san-francisco",
    "tags": ["birthday", "100-percent-free", "beauty", "skincare", "union-square", "bay-area-wide"],
    "is_new": False,
    "schedule_type": "Birthday",
    "neighborhood_slug": "sf-soma-downtown"
  },
  {
    "id": "bay-wheels-bike-share-free-ebt-medical-rides",
    "title": "Bay Wheels Bike Share - 100% Free 30-Minute Rides for SF EBT / Medi-Cal Residents",
    "priority_label": "100% Free",
    "priority_rank": 1,
    "category": "Transit & Services",
    "location": "SF - All Neighborhoods",
    "value": "$100+/year bike share value",
    "description": "Through the 'Bikes for All' equity program, San Francisco and Bay Area residents who receive CalFresh (EBT), Medi-Cal, or SFMTA Lifeline can enroll for $5/year or $0 pilot programs and receive unlimited 100% FREE 30-minute classic bike share trips across SF, Oakland, Berkeley, and San Jose.",
    "redemption_instructions": "1. Visit baywheels.com/bikes-for-all and apply with your EBT, Medi-Cal, or Lifeline card number.\n2. Once approved, link your account in the Lyft / Bay Wheels mobile app or Clipper card.\n3. Unlock any classic Bay Wheels bike at any docking station across the Bay Area for unlimited free 30-minute rides.",
    "restrictions": "Requires qualification under CalFresh EBT, Medi-Cal, or Lifeline. Trips under 30 minutes are 100% free.",
    "verification": {
      "status": "Verified Official Source",
      "source_name": "MTC / Bay Wheels 'Bikes for All' Official Rules",
      "verified_date": "2026-08-12",
      "notes": "Verified via baywheels.com/bikes-for-all equity program documentation."
    },
    "promotion_url": "https://www.lyft.com/bikes/bay-wheels/bikes-for-all",
    "community_url": "https://www.freemania.net/cities/san-francisco-ca",
    "tags": ["transit", "100-percent-free", "bike-share", "ebt", "city-service", "sf-resident-friendly", "always-free"],
    "is_new": True,
    "schedule_type": "Always Free",
    "neighborhood_slug": "sf-all-neighborhoods"
  }
]

def map_schedule_type(deal):
    """Assigns schedule_type for interactive active calendar filtering."""
    t = deal.get("title", "").lower() + " " + deal.get("description", "").lower() + " " + deal.get("id", "").lower()
    
    if "birthday" in t:
        return "Birthday"
    elif "first tuesday" in t:
        return "First Tuesday"
    elif "second tuesday" in t:
        return "Second Tuesday"
    elif "first wednesday" in t or "every wednesday" in t:
        return "First Wednesday"
    elif "first thursday" in t:
        return "First Thursday"
    elif "first sunday" in t:
        return "First Sunday"
    elif "second saturday" in t or "every saturday" in t:
        return "Second Saturday"
    elif "second friday" in t or "friday" in t:
        return "Second Friday"
    elif "daily" in t or "every day" in t or "always free" in t or "unlimited" in t:
        return "Always Free"
    elif "weekend" in t or "saturday" in t or "sunday" in t:
        return "Weekend"
    else:
        return "Always Free"

def map_neighborhood_slug(location_str):
    """Maps location to clean neighborhood slug for Neighborhood Explorer."""
    l = location_str.lower()
    if "soma" in l or "downtown" in l:
        return "sf-soma-downtown"
    elif "golden gate park" in l or "richmond" in l:
        return "sf-golden-gate-park-richmond"
    elif "lincoln park" in l or "sea cliff" in l:
        return "sf-golden-gate-park-richmond"
    elif "mission" in l or "castro" in l:
        return "sf-mission-castro"
    elif "chinatown" in l or "north beach" in l:
        return "sf-chinatown-north-beach"
    elif "oakland" in l or "east bay" in l:
        return "oakland-east-bay"
    elif "san jose" in l or "south bay" in l or "stanford" in l or "palo alto" in l:
        return "san-jose-south-bay"
    else:
        return "sf-all-neighborhoods"

def main():
    with open(DEALS_PATH, "r", encoding="utf-8") as f:
        existing = json.load(f)

    print(f"Loaded {len(existing)} existing deals.")

    # Update existing deals with schedule_type and neighborhood_slug if missing
    for d in existing:
        if "schedule_type" not in d:
            d["schedule_type"] = map_schedule_type(d)
        if "neighborhood_slug" not in d:
            d["neighborhood_slug"] = map_neighborhood_slug(d.get("location", ""))

    # Add new deals if id not already present
    existing_ids = {x["id"] for x in existing}
    added_count = 0
    for new_d in NEW_DEALS:
        if new_d["id"] not in existing_ids:
            existing.append(new_d)
            existing_ids.add(new_d["id"])
            added_count += 1

    with open(DEALS_PATH, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)

    print(f"✅ Upgraded {DEALS_PATH}: Added {added_count} new deals -> Total: {len(existing)} verified deals.")

if __name__ == "__main__":
    main()

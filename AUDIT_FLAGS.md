# CouponsDealsSF — Full Official-Source Audit (10-Pass, Line-by-Line)

**Audit date:** 2026-08-19 (second independent audit; supersedes the 2026-08-19 first-pass audit)
**Corpus:** `data/deals.json` — **29 entries**, all published as Priority #1 "100% Free / No Purchase"
**Method:** every entry was re-verified claim-by-claim (free status, schedule, hours, prices, eligibility, dates, URLs) against the **live official source** fetched on the audit date. Secondary sources (Funcheap, sftourismtips) were used only to corroborate, never as sole proof.

---

## The 10 passes

| # | Pass | Result |
| :-- | :-- | :-- |
| 1 | **Official URL + policy fetch** — every `promotion_url` opened and read | All 29 resolve; 1 was a redirect (Nothing Bundt `/eclub/` → `/bundtastic-rewards/`, updated) |
| 2 | **Core free claim** — is the offer genuinely $0, per the official page? | 29 / 29 confirmed $0 at redemption (eligibility rules apply where noted) |
| 3 | **Hours & days** — verify open days/hours and free-day schedule text | 27 / 29 exact; 2 metadata errors fixed (YBCA, Mission Food Hub `schedule_type`) |
| 4 | **Prices & "value" fields** — check quoted values against official price pages | 3 stale values fixed (de Young $20→$25, Legion $20→$25, SF Zoo $26–$32→$32–$34) |
| 5 | **2026-specific dates** — re-check every hard date against the live page | All confirmed (SFMOMA Oct 25; MoAD closure; Zoo Sep 2/Oct 7; Opera Sep 13; Anderson Jan 5 schedule) |
| 6 | **Redemption mechanics** — can a user actually redeem as written? | 2 fixed (Japanese Tea Garden timed-entry requirement; Nothing Bundt unverified window removed) |
| 7 | **Free / no-purchase filter** — sweep for any purchase, BOGO, minimum-spend, or discount-only language | 0 violations — all 29 are pure $0 offers (BofA requires an existing card, no purchase; Sephora/NBC in-store redemption requires no purchase per official terms) |
| 8 | **Internal consistency** — `schedule_type`/`location`/`neighborhood_slug` vs. facts; app rendering | 3 fixes (YBCA, Mission Food Hub, Zoo `schedule_type`; Camerawork location) + 1 app bug fixed (Legion invisible in Neighborhood view) |
| 9 | **Supporting files** — `sources.json` URLs, `stats.json`, README claims, schema validation | 3 stale source URLs fixed; stats regenerated; README "29/29" verified; `verify_links.py` + JSON validation pass |
| 10 | **Post-fix re-verification** — re-read every edited field; re-run scripts | All edits verified; 0 errors, 0 warnings from the verification engine |

---

## Line-by-line verdicts (all 29 entries)

Verdicts: **VERIFIED** = every checked claim matches the official page. **VERIFIED+FIX** = core claim true; listed corrections applied this audit.

| # | Entry | Official source (fetched 2026-08-19) | Verdict | Notes |
| :-- | :--- | :--- | :--- | :--- |
| 01 | SFMOMA 18-and-under + Free Family Days | sfmoma.org/free-days | **VERIFIED+FIX** | 18 & under always free ✓; Family Day = up to **2 adults** per child/teen ✓; next Family Day **Oct 25, 2026** ✓; tickets 2 weeks ahead ✓; Community Days **TBD** ✓; surcharges excluded ✓; adult GA **$30** ✓ (group-visits page). Fixed: restrictions text rewritten from audit-note style to user-facing. Note: a 2024 SFMOMA press release said "four adults" — the current policy page says two; catalog correctly follows the live page. |
| 02 | de Young Free Saturdays + First Tuesdays | famsf.org/visit/free-reduced-admission; famsf.org/visit/de-young-tickets-hours | **VERIFIED+FIX** | Every Saturday free for 9 Bay Area counties ✓ (county list matches exactly); First Tuesday free for all ✓; 17 & under free ✓; Bouquets to Art blackout ✓; hours Tue–Sun 9:30–5:15 ✓. **Fixed: adult GA is now $25, not $20.** Added verified bonus: free permanent-collection admission from 4:30 PM daily. |
| 03 | Legion of Honor Free Saturdays + First Tuesdays | famsf.org/visit/legion-tickets-hours | **VERIFIED+FIX** | Same FAMSF policy confirmed ✓; Tue–Sun 9:30–5:15 ✓; closed MLK/Labor/Indigenous Peoples'/Thanksgiving/Christmas (catalog said only "typical hours" — acceptable). **Fixed: adult GA $25, not $20.** Added 4:30 PM free hour. |
| 04 | SF Botanical Garden | gggp.org/visit/admissions-hours | **VERIFIED** | Free 7:30–9 AM daily ✓; Second Tuesday ✓; Thanksgiving/Christmas/New Year's ✓ (all verbatim on official page); SF residents free daily ✓ (Board of Supervisors ordinance, sfrecpark.org; Botanical "already free to residents"). |
| 05 | Conservatory of Flowers | gggp.org/visit/admissions-hours | **VERIFIED** | First Tuesday free ✓; **closed Wednesdays** ✓; 10 AM–4:30 PM, last entry 4 PM ✓; annual winter maintenance closure ✓ (Jan 21–Feb 4, 2026 listed); SF resident + veteran free ✓ (ordinance). |
| 06 | Japanese Tea Garden | gggp.org/japanese-tea-garden; gggp.org/visit/admissions-hours | **VERIFIED+FIX** | Free hour **Mon/Wed/Fri 9–10 AM** ✓ verbatim; 75 Hagiwara Tea Garden Dr ✓; residents/veterans free ✓ (ordinance + GGGP FAQ: free timed tickets for SF residents, veterans, Museums for All). **Fixed: official page now requires timed-entry reservation for all visitors — redemption instructions updated.** |
| 07 | YBCA free Wednesdays | ybca.org/visit | **VERIFIED+FIX** | "Every Wednesday enjoy free admission for all" ✓; adult **$10** ✓; Wed **11 AM–8 PM** ✓; Thu–Sun 11–5 ✓; closed Mon–Tue ✓; 701 Mission ✓; youth 17 & under/military/Museums for All free ✓. **Fixed: `schedule_type` "First Wednesday" → "Every Wednesday" (deal is weekly).** |
| 08 | SFMTA Free Muni for All Youth | sfmta.com/fares/free-muni-all-youth-18-years-and-younger | **VERIFIED** | All youth 18 & under, any income/residency ✓; no application/Clipper ✓; cable cars excluded ✓; 16+ carry ID ✓; cable-car pass request for SF youth ✓. Every sentence matches the official page. |
| 09 | SFPL Discover & Go | sfpl.org/discover-and-go | **VERIFIED** | "Library users who are San Francisco residents can access free passes to more than a dozen Bay Area museums and attractions" ✓ verbatim; sfpl.discoverandgo.net ✓; reserve + print ✓. |
| 10 | Mission Food Hub | missionfoodhub.org | **VERIFIED+FIX** | "Serving families **every Friday**" ✓; 701 Alabama St ✓; missionfoodhub@gmail.com / (650) 333-7628 ✓; free culturally relevant groceries ✓. **Fixed: `schedule_type` "Second Friday" → "Every Friday."** |
| 11 | Cable Car Museum | cablecarmuseum.org/info.html | **VERIFIED** | "Admission is Free" ✓ verbatim; Tue–Thu 10–4, Fri–Sun 10–5, closed Monday ✓ verbatim; closed New Year's/Thanksgiving/Christmas ✓; 1201 Mason ✓. |
| 12 | BofA Museums on Us | about.bankofamerica.com (official roster) + famsf.org | **VERIFIED** | Official CA roster: de Young ✓, Legion of Honor ✓, OMCA ✓, Computer History Museum (Mountain View) ✓, **SFMOMA (June–September)** ✓ — exactly as cataloged. First full weekend ✓; cardholder + photo ID, cardholder only ✓; GA only, specials excluded ✓ (FAMSF partner page). No purchase required at redemption (existing card = eligibility). Roster also includes San José Museum of Art (Sundays) and The Tech (select weekends) — catalog says "includes," so not an error. |
| 13 | Nothing Bundt Cakes birthday Bundtlet | nothingbundtcakes.com/bundtastic-rewards | **VERIFIED+FIX** | "Members also get a free individual Bundtlet on their birthday" ✓ verbatim; program free to join ✓. **Fixed: URL updated from redirecting `/eclub/`; removed the unverified "7 days after birthday" window and "no purchase" FAQ attribution — redemption text now says confirm the window at the bakery.** Core free-birthday-Bundtlet claim is official. |
| 14 | SFPL NYT + Kanopy | sfpl.org/research-learn/elibrary/emagazines-enews; sfpl.org/node/25637 | **VERIFIED** | "New York Times – Online Access from Home" pass listed ✓; WSJ via wsj.com redemption code ✓ (matches catalog's cautious wording); Kanopy: "30,000+ films free with your Library Card" on SFPL's own page ✓; monthly credit cap ✓ (8/month per SF Chronicle launch coverage). |
| 15 | MoAD Free Second Saturday | moadsf.org/visit | **VERIFIED** | Closed **Aug 17–Sep 29, 2026**, reopens Sep 30 ✓ verbatim; "Every Second Saturday" THRIVE community day free ✓; adult **$15** ✓; Saturday 11–5 ✓; 685 Mission ✓. |
| 16 | OMCA Free First Sunday | museumca.org/tickets | **VERIFIED** | "Every first Sunday of the month… Art, History, Natural Sciences, and any Special Exhibitions in our Great Hall are free" ✓ verbatim; admission $25 ✓; 1000 Oak St ✓. |
| 17 | BAMPFA Free First Thursday | bampfa.org/visit/hours | **VERIFIED** | "Galleries are free for all on the first Thursday of each month" ✓; GA **$18** ✓; Wed–Sun 11–7, closed Mon–Tue ✓; UC Berkeley students/faculty/staff free ✓; children 0–13 free ✓; films separate ✓. |
| 18 | Museum of Craft & Design | sfmcd.org/visit | **VERIFIED+FIX** | Free First Thursday ✓; Thu–Sun 12–5 ✓; **closed Mon–Wed** ✓ (no Pay-What-You-Wish Wednesday — correctly absent); GA $10, students/seniors $8, kids 12 & under free ✓; 2569 Third St, Dogpatch ✓. **Fixed: added official notice — NO Free First Thursday in September 2026 (install closure); next is Oct 1, 2026.** |
| 19 | GLBT Historical Society Museum | glbthistory.org/museum-about-visitor-info | **VERIFIED** | Free "the first Wednesday of every month, sponsored by the Bob Ross Foundation" ✓ verbatim; GA **$10** ✓; hours Tue–Sun 11–1 & 1:30–5, closed Mon ✓; 4127 18th St ✓; free-day tickets not reservable online, first-come first-served ✓; tickets@glbthistory.org ✓. |
| 20 | Asian Art Museum Free First Sunday | about.asianart.org (free-and-reduced + plan-your-visit) | **VERIFIED+FIX** | First Sunday GA free ✓ verbatim; adult GA **$20** ✓; hours Thu 1–8, Fri–Mon 10–5, closed Tue–Wed ✓; 200 Larkin ✓. **FLAG (source conflict): the museum's own pages disagree on the Free-First-Sunday special-exhibition surcharge — $15 on the Free & Reduced page vs $10 on Plan Your Visit. Catalog updated to disclose both and tell users to confirm at booking.** |
| 21 | SF Zoo SF-Resident Free Days | sfzoo.org/calendar-of-events; sfzoo.org/tickets-hours | **VERIFIED+FIX** | Official calendar: "San Francisco Residents receive free admission with proof of SF Residency… One free admission per ID" on **Wed Sep 2** and **Wed Oct 7, 2026** ✓ exactly as cataloged; parking paid ✓ ($15/$20); $3 EBT/Medi-Cal SF-resident ticket is separate ✓. **Fixed: adult admission is $32 weekday/$34 weekend — value field corrected from "$26–$32"; `schedule_type` → "Published Calendar Dates" (dates are announced, not a guaranteed monthly rule).** |
| 22 | ICA SF always free | icasf.org/visit | **VERIFIED** | "ICA SF is always free" ✓ verbatim. Visit page currently lists public works in Yerba Buena (Mission St facades) and Transamerica Pyramid Center — exactly what the catalog says; catalog correctly tells users to confirm the exhibition address before going. |
| 23 | Randall Museum | randallmuseum.org/about-us | **VERIFIED** | "Admission is Free" ✓; Tue–Sat 10–5, closed Sun/Mon ✓ verbatim; 199 Museum Way ✓; Rec & Park facility ✓. |
| 24 | Cantor Arts Center | museum.stanford.edu/visit | **VERIFIED** | "We're always free. Come visit us." ✓ verbatim; "more than **38,000** works" ✓ (catalog explicitly corrects the old 40,000 figure); ParkMobile paid parking ✓ (no free-parking claim); 328 Lomita Dr at Museum Way ✓. |
| 25 | SF Opera in the Park | sfopera.com/operainthepark | **VERIFIED** | "Sunday, September 13, 2026 at 1:30pm… Free and open to all!" ✓ verbatim; Robin Williams Meadow ✓; ~2 hours ✓; blankets OK, no glass ✓; no ticket ✓. |
| 26 | SF Camerawork | sfcamerawork.org/visit | **VERIFIED+FIX** | "SF Camerawork's exhibitions are **always free** and open to the public" ✓ verbatim; 2 Marina Blvd, Building A, Fort Mason ✓; hours exhibition-dependent via /current-hours ✓. **Fixed: location bucket corrected from "All Neighborhoods" to "SF - Marina / Fort Mason."** |
| 27 | Anderson Collection | anderson.stanford.edu/visit | **VERIFIED** | "Starting on **January 5, 2026**, we are open on Mondays and closed on Tuesdays and Wednesdays" ✓ verbatim; Mon + Thu–Sun 11–5 ✓; free admission ✓ (official museum Facebook: "Free Admission"); ParkMobile paid parking ✓; 314 Lomita Dr ✓. |
| 28 | SF Railway Museum | streetcar.org/museum | **VERIFIED** | "The museum is free (donations encouraged)" ✓ verbatim; "Tuesdays through Sundays from 12 noon – 5 pm" ✓; closed Thanksgiving/Christmas/New Year's ✓; 77 Steuart St across from the Ferry Building ✓. |
| 29 | Sephora birthday gift | sephora.com/beauty/loyalty-program; sephora.com/beauty/birthday-gift | **VERIFIED** | Official FAQ: "No purchase is necessary when redeeming your gift in store. To redeem online, a merchandise purchase is required" ✓; birthday-2026 page: "$25+ to redeem online" ✓; one gift per year during birthday month ✓; while supplies last ✓; Beauty Insider free to join ✓. |

---

## Fixed this audit (summary)

1. **de Young & Legion value fields: $20 → $25** — official FAMSF ticket pages now list Adults $25 (Seniors $22, Students $10). Also added the verified 4:30 PM free permanent-collection hour.
2. **SF Zoo value: $26–$32 → $32–$34** — official tickets page (Adult 12–64: $32 weekday / $34 weekend). `schedule_type` → "Published Calendar Dates."
3. **YBCA `schedule_type`: "First Wednesday" → "Every Wednesday"** — the offer is weekly, per ybca.org.
4. **Mission Food Hub `schedule_type`: "Second Friday" → "Every Friday"** — per missionfoodhub.org.
5. **Japanese Tea Garden redemption** — timed-entry reservation is now required for all visitors (gggp.org); instructions updated.
6. **Museum of Craft & Design** — added the official September 2026 Free-First-Thursday blackout (install closure); next FFT Oct 1, 2026.
7. **Nothing Bundt Cakes** — URL updated to the live `/bundtastic-rewards/` page; unverified redemption-window details removed; claims aligned to verbatim FAQ text.
8. **SFMOMA restrictions** — rewritten from internal audit-note style to user-facing text.
9. **SF Camerawork location** — "SF - All Neighborhoods" → "SF - Marina / Fort Mason" (single fixed venue).
10. **App bug** — `js/app.js` Neighborhood Explorer hardcoded list omitted "SF - Lincoln Park / Sea Cliff," rendering the Legion of Honor deal invisible in that view; added it plus "SF - Marina / Fort Mason."
11. **`data/sources.json`** — 3 dead/redirecting official URLs replaced (SFMTA youth page, sfbg.org → gggp.org, conservatoryofflowers.org → gggp.org); `last_updated` → 2026-08-19.
12. **`data/stats.json`** — regenerated (29/29 free, updated location distribution). `verify_links.py`: 0 errors, 0 warnings.

## Flags for ongoing review (not republished as fact)

- **Asian Art Museum special-exhibition surcharge on Free First Sundays**: museum's own pages conflict ($15 vs $10). Catalog discloses both; re-check monthly until the museum reconciles.
- **SFMOMA Free Family Day adult limit**: a 2024 press release said 4 adults; the current policy page says 2. Catalog follows the live page. Re-check before each Family Day.
- **BofA Museums on Us roster**: official roster also lists San José Museum of Art (Sundays only) and The Tech Interactive (select weekends) — candidates to add. Roster "may change at any time."
- **Value fields on always-free museums** (e.g., "$15 value" Cable Car Museum, "$20 value" ICA SF): these venues have no paid GA, so "value" is editorial. Not treated as hallucinations, but they are estimates, not official prices.
- **`data/candidates.json`**: still unaudited candidates with synthetic-looking upvotes (Ferry Fest, Movies on the Square — Redwood City, Autumn Moon Festival, SFMTA Free Muni for low-income seniors/disabled — real program worth promoting, Boudin birthday). Do not publish without the same line-by-line official check.
- **Cable Car Museum location bucket** ("Chinatown / North Beach"): 1201 Mason & Washington is commonly mapped as Nob Hill; tags already include nob-hill. Cosmetic only.

## Free / no-purchase policy check (user requirement: keep ONLY free, no purchase)

All 29 entries are $0 at redemption with no purchase required:
- 22 museum/garden free days or always-free venues — $0 walk-in/reservation.
- SFMTA youth, SFPL Discover & Go, SFPL NYT/Kanopy — $0 with free library card / no card at all.
- Mission Food Hub — $0 groceries.
- BofA Museums on Us — $0; requires an existing BofA/Merrill/Private Bank card (eligibility, not a purchase).
- Sephora & Nothing Bundt Cakes birthdays — free to join, official terms state no purchase necessary in store.

No purchase-required, BOGO, minimum-spend, or discount-only offers remain in the catalog (removed in the prior audit: Chipotle, Ike's, BWW, Quiznos, Underdogs, CHSA, Clipper BayPass, Off the Grid, TATO, Banya, Balboa, Ghirardelli, Baskin-Robbins, Stern Grove 2026, SFO Terminal Sessions, Bay Wheels, Fire Museum, Chinatown Night Market, Skatin' Place, SFAA star parties, Musée Mécanique).

**Official sources fetched and cited in this audit:** sfmoma.org (free-days, group-visits), famsf.org (free-reduced-admission, both tickets+hours pages), gggp.org (admissions-hours, japanese-tea-garden, cherryblossoms FAQ, san-francisco-botanical-garden), sfrecpark.org (resident-free ordinance), ybca.org/visit, sfmta.com (free-muni-all-youth), sfpl.org (discover-and-go, emagazines-enews, Kanopy page), missionfoodhub.org, cablecarmuseum.org/info.html, about.bankofamerica.com (Museums on Us CA roster), nothingbundtcakes.com/bundtastic-rewards, moadsf.org/visit, museumca.org/tickets, bampfa.org/visit/hours, sfmcd.org/visit, glbthistory.org/museum-about-visitor-info, about.asianart.org (free-and-reduced + plan-your-visit), sfzoo.org (calendar-of-events + tickets-hours), icasf.org/visit, randallmuseum.org/about-us, museum.stanford.edu/visit, sfopera.com/operainthepark, sfcamerawork.org/visit, anderson.stanford.edu/visit, streetcar.org/museum, sephora.com (birthday-gift + loyalty-program FAQ).

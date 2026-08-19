# CouponsDealsSF — Independent Official-Source Audit

**Audit date:** 2026-08-19  
**Filter date:** 2026-08-19 — catalog cut to **official 100% free / no-purchase only** (29 kept). Later removals: Fire Museum (no current official visitor policy); Chinatown Night Market (no official organizer page); Skatin’ Place (community/DJ unverified); SFAA star parties (event URLs 404); Musée Mécanique (official homepage does not state free admission).  
**Prior correction:** FAIL rows were rewritten, then purchase/discount/unofficial/ended rows were deleted.  
**Corpus:** `data/deals.json` (now 34)  
**Method:** three passes

1. **Pass A — Internal consistency:** schema, IDs, `schedule_type` vs text, neighborhood vs address, priority vs purchase rules.
2. **Pass B — Official URL live-check:** fetch every `promotion_url` and the current official visit/admissions page.
3. **Pass C — Claim-by-claim check:** hours, prices, eligibility, dates, and “100% free” status against official policy. Secondary sources (Funcheap, Reddit, Yelp) used only to locate official pages, never as proof.

**Verdict key**

| Verdict | Meaning |
| :--- | :--- |
| **PASS** | Core free/discount claim matches official policy. Minor wording issues only. |
| **PASS WITH ERRORS** | Deal exists, but hours, dates, prices, URLs, or eligibility are wrong. |
| **FLAG — HALLUCINATION / STALE** | A specific claimed fact is false, outdated, or invented. Do not publish as verified. |
| **FLAG — UNOFFICIAL** | Community-only; official site does not document the perk. |
| **FAIL** | Core “100% free / verified official” claim is false. |

Repo `scripts/verify_links.py` does **not** check sources. It only validates JSON schema. Every `"Verified Official Source"` / `"verified_date": "2026-08-12"` stamp is self-asserted.

---

## Highest-severity flags (fix or unpublish first)

These will send a user to the wrong place, on the wrong day, or to a paid offer labeled free.

### FAIL — `chinese-historical-society-always-free`

Official CHSA FAQ ([chsa.org/faqs](https://chsa.org/faqs/)):

- Tickets are **sold**. Student $10, senior/veteran $10, EBT/Medi-Cal **$3**.
- Open **Wednesday and Saturday only, 10:00 AM–5:00 PM**.
- Closed Monday, Tuesday, Thursday, Friday, Sunday.

Catalog claims: always 100% free; walk-in Wednesday–Sunday 11:00 AM–4:00 PM; value $12.

This is a **fabricated free-admission policy**. Priority #1 is false. Hours are false. `promotion_url` `https://chsa.org/visit/` does not resolve to a visit page.

### FAIL — `ikes-sandwiches-free-birthday-sandwich`

Official Ike’s FAQ / terms:

- Birthday reward is **half off a sandwich**, not a free sandwich.
- Requires a **$10+ purchase in the past year**.
- Must join before the first of the birthday month.

Catalog claims Priority #1 / 100% free / no purchase. That is false. This is Priority #2 at best. `https://ikessandwich.com/rewards/` is not the current official rewards page.

### FAIL / STALE — `mission-food-hub-free-fresh-groceries`

Official [missionfoodhub.org](https://www.missionfoodhub.org/): **Friday-only** grocery distribution now. The Mon/Wed/Fri 10:00 AM schedule is the 2020 COVID peak, not current operations.

### FAIL / STALE — `museum-of-craft-and-design-free-thursdays`

Official [sfmcd.org/visit](https://sfmcd.org/visit/):

- Open **Thursday–Sunday, 12:00–5:00 PM**.
- **Closed Monday–Wednesday.**
- Free First Thursday is real.
- **Pay-What-You-Can Wednesday does not exist.** Museum is closed Wednesdays.

Catalog hours “10:00 AM–5:00 PM” and weekly $0 Wednesday are false.

### FAIL / STALE — `off-the-grid-treasure-island-free-ferry`

Treasure Island / Off the Grid official spring series ran **April 11–May 16, 2026** only. Audit date is **August 19, 2026**. This is not an always-on free ferry. `schedule_type: Always Free` is false.

### Conservatory closed-day hallucination — `conservatory-of-flowers-free-tuesday-and-residents`

Official Gardens of Golden Gate Park ([gggp.org/visit/admissions-hours](https://gggp.org/visit/admissions-hours/)):

- **Closed Wednesdays**, open Thursday–Tuesday 10:00 AM–4:30 PM.
- Catalog says **closed Mondays**, open Tuesday–Sunday.

Sending people on Wednesday is a hard miss. Resident + veteran + First Tuesday free **is** official.

---

## Line-by-line entry audit

### 01 `sfmoma-free-family-community-days` — PASS WITH ERRORS

Official: [sfmoma.org/free-days](https://www.sfmoma.org/free-days/)

| Claim | Official | Flag |
| :--- | :--- | :--- |
| Ages 18 and under always free | Yes | OK |
| Adult $30 | Matches published 2026 GA | OK |
| Up to **4 adults** free with one youth | Official: up to **2 adults** per child/teen | **HALLUCINATION** |
| Next Free Family Day **June 14, 2026** | That date already happened. Official next date: **October 25, 2026** | **STALE** |
| Community Days “seasonally” | Official upcoming: **TBD** | Overstated |
| Teen value $23 | 18-and-under is free; $23 is student, not teen | Misleading |

### 02 `deyoung-free-first-tuesday-and-saturdays` — PASS

Official: [famsf.org/visit/free-reduced-admission](https://www.famsf.org/visit/free-reduced-admission)

Free Saturdays for 9-county residents + First Tuesday for all, permanent galleries only, 9 counties listed correctly.  
`$20 value` is a ballpark GA figure, not a current official quote. `schedule_type: First Tuesday` underweights the Saturday resident offer.

### 03 `legion-of-honor-free-saturdays-residents` — PASS

Same FAMSF policy. Saturday 9:30 AM–5:15 PM matches listed hours. Neighborhood slug is Golden Gate Park, not Lincoln Park / Sea Cliff (location field is correct).

### 04 `sf-botanical-garden-free-daily-residents` — PASS WITH ERRORS

Official is now **gggp.org**, not `sfbg.org/visit` (redirects).

Confirmed: SF residents free; daily 7:30–9:00 AM free for all; Second Tuesday free.  
Omitted official free days: Thanksgiving, Christmas, New Year’s Day. Value $14 unverified on the admissions page.

### 05 `conservatory-of-flowers-free-tuesday-and-residents` — PASS WITH ERRORS

Resident + veteran + First Tuesday free: official.  
**Closed Wednesday, not Monday.** Hours page is gggp.org, not a dedicated Conservatory visit policy that matches the catalog text.

### 06 `japanese-tea-garden-free-hour-and-residents` — PASS WITH ERRORS

Official: Mon/Wed/Fri **9:00–10:00 AM** free hour; SF residents (and veterans) free.  
`https://www.japaneseteagardensf.com/visit` is **404**.  
`schedule_type: Second Friday` is invented. Veterans free omitted.

### 07 `ybca-free-wednesdays` — PASS WITH ERRORS

Official [ybca.org/visit](https://ybca.org/visit/): every Wednesday galleries free. Address 701 Mission confirmed.  
Adult ticket is **$10**, not $15. Wednesday hours are **11 AM–8 PM**, not 11–5.  
`schedule_type: First Wednesday` is false.

### 08 `sfmta-free-muni-for-all-youth` — PASS WITH ERRORS

Official: [sfmta.com/fares/free-muni-all-youth-18-years-and-younger](https://www.sfmta.com/fares/free-muni-all-youth-18-years-and-younger)

Catalog URL `.../getting-around/muni/fares/free-muni-all-youth` is **404**.  
Program is real: all youth 18 and under, no Clipper, cable cars excluded unless SF youth request a pass.  
Value `$2.50–$5.00 ($81/month)` is stale. Official adult fare is about **$2.85 Clipper / $3.00 cash**; monthly pass **$86**.

Community URL points at an AskSF birthday thread, not transit policy.

### 09 `sfpl-discover-and-go-free-museum-passes` — PASS

Official: [sfpl.org/discover-and-go](https://sfpl.org/discover-and-go) — SF resident cardholders, 12+ attractions.  
“15+” and the specific high-demand venue list (Cal Academy, Exploratorium, SF Zoo, MoAD) are not enumerated on that page. Treat venue list as unverified.

### 10 `mission-food-hub-free-fresh-groceries` — FAIL / STALE

See highest-severity. Address 701 Alabama is still listed. Schedule is not.

### 11 `archimedes-banya-free-birthday-pass` — FLAG — UNOFFICIAL

Address **748 Innes Ave** is India Basin / Bayview, **not SoMa**.  
Current [banyasf.com](https://banyasf.com/) does **not** publish a birthday-free policy.  
A 2013 Banya post offered a **voucher for the next visit**, not same-day free entry.  
Reddit r/AskSF (June 2026, post `1ub304e`) still claims it. Community-only.  
`$72 value` is not on the current official pricing page.

### 12 `balboa-theater-free-birthday-movie` — FLAG — UNOFFICIAL

`https://www.cinemasf.com/balboa` is **404**. Current site is [balboamovies.com](https://www.balboamovies.com/).  
No official birthday-free-ticket policy found. One Yelp anecdote only. Address 3630 Balboa is real.

### 13 `ikes-sandwiches-free-birthday-sandwich` — FAIL

See highest-severity.

### 14 `ghirardelli-square-free-chocolate-sample` — FLAG — UNOFFICIAL

Long-running visitor custom, not a published official promotion.  
`https://www.ghirardelli.com/store-locations/san-francisco-ghirardelli-square` not independently confirmed as the current store page. Neighborhood is Fisherman’s Wharf, not Chinatown / North Beach.

### 15 `chinatown-night-market-free-admission` — PASS WITH ERRORS

2026 series is real: **second Friday, May–October only** (May 8 … Oct 9), typically 5:00–9:00 PM, Grant Ave **California to Pacific**.  
Catalog implies year-round monthly. Hours 5:30–9:00 and Grant Sacramento–Jackson are off.  
`https://www.chinatownmerchant.org/` is not the event organizer page (Civic Joy Fund / Funcheap).

### 16 `sf-cable-car-museum-always-free` — PASS WITH ERRORS

Free walk-in at 1201 Mason is real.  
Hours “Tue–Sun 10:00–4:00” are oversimplified. SFHSA/current listings: Tue–Thu 10–4, Fri–Sun 10–5.

### 17 `musee-mecanique-always-free` — PASS

Free admission at Pier 45 is real; games are paid.  
“365 days, 10 AM–8 PM” may overstate weekday hours (some listings Mon–Fri 10–7). Official homepage fetch returned almost no text.

### 18 `bank-of-america-museums-on-us-weekend` — PASS WITH ERRORS

Program is official: first **full** weekend, cardholder + matching ID, GA only.  
FAMSF confirms de Young + Legion. OMCA is widely listed.  
**Contemporary Jewish Museum** is **not** on the 2026 Funcheap BofA roster. Treat CJM as stale until BofA’s locator confirms it.  
Catalog URL is not the current BofA locator (`museums-on-us-find-locations-map`).

### 19 `baskin-robbins-free-birthday-scoop` — PASS WITH ERRORS

Loyalty birthday scoop is a real national program. Size (2.5 vs 4 oz) and “expires 10 days” were not confirmed on the official birthday-club page. Secondary sources only.

### 20 `nothing-bundt-cakes-free-birthday-bundlet` — PASS

Official [nothingbundtcakes.com/eclub](https://www.nothingbundtcakes.com/eclub/): free Bundtlet on birthday for Bundtastic Rewards / eClub. No SF store; Bay Area locations are suburban. Fine.

### 21 `sfpl-free-nytimes-wsj-digital-access` — PASS WITH ERRORS

SFPL does offer NYT 72-hour digital passes (renewable) plus Kanopy. WSJ / WaPo access exists via library databases but is **not** the same “72-hour pass, renew forever” mechanic as NYT.  
`https://sfpl.org/books-and-media` is a generic hub, not the eLearning redeem page. “$35/month” is a bundled guess.

### 22 `golden-gate-park-skatin-place-free-skate` — PASS WITH ERRORS

Skatin’ Place at 6th & JFK is a real dedicated skate area. Community skate is strongest **Sunday noon–5**, also Sat/Wed — not a formal “every weekend live DJ” city program.  
`https://sfrecpark.org/destination/golden-gate-park/skatin-place/` was not confirmed as a live official page.

### 23 `off-the-grid-treasure-island-free-ferry` — FAIL / STALE

See highest-severity. Location SoMa is wrong (Treasure Island / Ferry Building).

### 24 `moad-free-second-saturday` — PASS WITH ERRORS

Official [moadsf.org/visit](https://www.moadsf.org/visit): Second Saturday Thrive @ MoAD is free.  
**Closed Aug 17–Sep 29, 2026** for install — catalog does not say this.  
Hours Sat **11–5**, not 11–6. Adult ticket **$15**, not $20.

### 25 `oakland-museum-omca-free-first-sunday` — PASS

Official [museumca.org/tickets](https://museumca.org/tickets/): First Sunday free, including Great Hall specials. Address 1000 Oak confirmed.

### 26 `berkeley-bampfa-free-first-thursday` — PASS

First Thursday galleries free; UC Berkeley ID always free; films not included. Address 2155 Center confirmed.

### 27 `museum-of-craft-and-design-free-thursdays` — FAIL / STALE

See highest-severity. First Thursday free is the only surviving official free day.

### 28 `glbt-historical-society-free-wednesday` — PASS

First Wednesday free is official. Address 4127 18th St confirmed. Hours are split (11–1 and 1:30–5), not a simple 11–5 block.

### 29 `tato-pay-what-you-can-friday-tacos` — FLAG — STALE / MISLOCATED

Tato is real at **4608 3rd St, Bayview**, not Mission / Castro.  
Pay-what-you-can Friday started as a 2020 COVID program. Funcheap still lists it into 2026; **no current official restaurant policy page**. Hours 11–2 do not match 2026 Yelp (Fri 8 AM–3 PM).  
Promotion URL is a Funcheap category, not Tato.

### 30 `chinese-historical-society-always-free` — FAIL

See highest-severity.

### 31 `chipotle-free-guac-or-chips-rewards` — PASS WITH ERRORS

Official Apr 2026 relaunch: **new members only**, free chips & guac with $5+, **expires 7 days**. Not an ongoing everyday offer. Birthday guac is a separate member perk. Priority #2 is correct.

### 32 `buffalo-wild-wings-free-birthday-wings` — FLAG — UNOFFICIAL

Coupon-site consensus: 6 wings with $10 in birthday month. **No official BWW terms page confirmed.** No SF location (Daly City / South Bay only) — title oversells “SF.”

### 33 `quiznos-bogo-birthday-sub` — FLAG — HALLUCINATION RISK

Only aggregator pages mention Toasty Points BOGO. **No official Quiznos birthday terms found.**  
`https://www.quiznos.com/toastypoints` not confirmed live. Do not keep as “Verified Official Source.”

### 34 `underdogs-cantina-1-dollar-margaritas` — PASS WITH ERRORS

Official [underdogscantina.com](https://underdogscantina.com/): **$1 house margaritas Tuesday 7:30–8:00 PM only**, Disco Taco Tuesday, 128 King St.  
Catalog “after 5:00 PM” / “Tuesday evening” **invents a multi-hour window**. Official window is **30 minutes**. `schedule_type: Always Free` is nonsense.

### 35 `clipper-baypass-student-commuter-pilot` — FLAG — MISLEADING

Program exists as an **institutional pilot** through late 2026.  
Catalog URL is **404**.  
It is **not** a free public pass. Students pay campus fees (e.g. SJSU ~$24.50/semester). Eligibility is institution-assigned, not “check your portal and tap for $0.”  
Priority #1 “100% Free / no purchase” is false for most users.

### 36 `stern-grove-festival-free-summer-concerts` — PASS WITH ERRORS

Festival is real and free.  
**Ticket process is wrong.** 2026 uses a **lottery opening 6 weeks out for 1 week**, plus community box office — **not** “released exactly one month before at 2:00 PM SHARP” that “sell out in minutes.” That is an old process.

### 37 `asian-art-museum-free-first-sunday` — PASS WITH ERRORS

Official [about.asianart.org/plan-your-visit](https://about.asianart.org/plan-your-visit/): Free First Sundays, specials $10. Adult GA **$20**, not $25.  
`https://asianart.org/visit/free-days/` is **404**.

### 38 `sf-zoo-free-days-sf-residents` — PASS WITH ERRORS

Periodic SF-resident free days are real (typically first Wednesday; Funcheap lists remaining 2026 dates).  
`schedule_type: Always Free` is false. Parking $13 and ticket values not confirmed on official tickets page during this audit. Military/Veterans Day free not independently confirmed.

### 39 `ica-sf-the-cube-always-free` — PASS

Official: “ICA SF is always free.” 345 Montgomery / The Cube still listed on 2026 directories. Hours Wed–Sun 11–5, Thu to 7 match older Funcheap. Official visit page now also mentions Yerba Buena / Transamerica public works — confirm indoor gallery is still The Cube before reprinting the address as exclusive.

### 40 `randall-museum-always-free` — PASS

Official: free, Tue–Sat 10–5, closed Sun/Mon, 199 Museum Way.  
“Entrance quail” is a typo (kiosk?).

### 41 `cantor-arts-center-stanford-always-free` — PASS WITH ERRORS

Always free is official. Collection is **38,000+**, not 40,000.  
“Free parking on weekends” is **false** — ParkMobile paid visitor parking.  
Hours in catalog (Wed–Sun 11–5) look like the **old** schedule. 2026 listings show **Mon open, Tue/Wed closed** (same flip as Anderson).

### 42 `sf-opera-in-the-park-free-concert` — PASS

Official SF Opera 2026–27 season release: **Sunday, September 13, 2026, 1:30 p.m.**, Robin Williams Meadow. Free, no ticket. Strong match.

### 43 `stern-grove-terminal-sessions-sfo-free` — PASS WITH ERRORS

Official SFO press release June 4, 2026: Terminal Sessions at **Gate B4, Terminal 1**.  
Dates were **Saturdays June 13 and June 20 at 2:00 PM**, then a separate Wed/Thu series.  
Catalog “select summer **Fridays**” is **false**.  
Need a **boarding pass or SFO Gate Explorer pass** — not walk-up for the public.  
By Aug 19, 2026 the June dates are over. SFist URL is real.

### 44 `sf-fire-department-museum-always-free` — PASS WITH ERRORS

Thu–Sun 1–4 is consistent. Address is commonly **655** Presidio, catalog says **658**.  
`sffiremuseum.org` redirects to an archival Guardians of the City site, not a current visitor policy.

### 45 `sf-camerawork-free-photography-gallery` — PASS WITH ERRORS

Official: always free, Fort Mason **2 Marina Blvd, Building A**.  
Hours are exhibition-dependent (often 11–6), **not** fixed Tue–Sat 12–6.  
Neighborhood Chinatown / North Beach is **wrong** (Marina / Fort Mason).

### 46 `anderson-collection-stanford-always-free` — PASS WITH ERRORS

Always free. Official as of Jan 5, 2026: **open Monday + Thu–Sun 11–5; closed Tuesday and Wednesday.**  
Catalog “Wed–Sun, closed Mon/Tue” is the **old** schedule.

### 47 `sf-railway-museum-always-free` — PASS WITH ERRORS

Official [streetcar.org/museum](https://www.streetcar.org/museum/): free, **Tuesday through Sunday 12:00–5:00 PM**.  
Catalog “Tuesday through Saturday” omits Sunday.

### 48 `sf-amateur-astronomers-free-star-parties` — PASS WITH ERRORS

SFAA exists; public star parties are free and weather-dependent.  
Lectures are **not** reliably at “Presidio / Randall Museum.” Locations rotate (Lands End, Presidio Parade Ground). Check calendar each time. Labeled “Verified Community / Reddit” but notes cite the official site — inconsistent.

### 49 `sephora-sf-free-birthday-gift-set` — PASS

Official Beauty Insider terms: in-store birthday gift, **no purchase**; online needs $25. Birthday **month**. URL is live.

### 50 `bay-wheels-bike-share-free-ebt-medical-rides` — FLAG — URL DEAD / TERMS UNCLEAR

`https://www.lyft.com/bikes/bay-wheels/bikes-for-all` is **404**.  
Equity program exists, but official 2026 price is **not** clearly “$5/year or $0 unlimited 30-minute rides.” Secondary sources conflict ($5/year then $5/month; 45- vs 60-min). Do not keep as verified official until the live Lyft/MTC page is recaptured.

---

## Pass A — Internal / catalog integrity

These are not source errors; they are invented or contradictory fields inside the JSON.

| Issue | Where |
| :--- | :--- |
| Every `verified_date` is `2026-08-12` | All 50 — rubber stamp |
| `schedule_type` contradicts the deal | Japanese Tea Garden, Mission Food Hub, YBCA, TATO = `Second Friday`; Underdogs / SF Zoo / Off the Grid = `Always Free` |
| Neighborhood vs address | Banya (Bayview listed SoMa); TATO (Bayview listed Mission); Camerawork (Marina listed Chinatown); Off the Grid (Treasure Island listed SoMa) |
| Priority #1 on purchase-required offers | Ike’s; Clipper BayPass (student fee); Chipotle is correctly #2 |
| Community URL reused as fake proof | Same Reddit post `1ub304e` attached to SFMTA, SFPL, Banya, Balboa, Ike’s, Nothing Bundt, Chipotle, BWW — one birthday thread is not official verification |
| `r/sanfrancisco/.../1ub304e` | That post is on **r/AskSF**, not r/sanfrancisco |
| Generic / empty community URLs | tripadvisor.com homepage, sfgate.com/local/, funcheap homepage, reddit.com/r/bayarea/ |
| `$1,450+ annual free value` | README / app banner — **no calculation in the repo** |
| `verify_links.py` name | Does not verify links |

---

## Dead or wrong official URLs

| Deal | Catalog URL | Status |
| :--- | :--- | :--- |
| SFMTA youth | `/getting-around/muni/fares/free-muni-all-youth` | **404** |
| Japanese Tea Garden | japaneseteagardensf.com/visit | **404** |
| Balboa | cinemasf.com/balboa | **404** |
| Asian Art free days | asianart.org/visit/free-days/ | **404** |
| Clipper BayPass | mtc.ca.gov/.../clipper-baypass | **404** |
| Bay Wheels Bikes for All | lyft.com/bikes/bay-wheels/bikes-for-all | **404** |
| CHSA visit | chsa.org/visit/ | Does not load a visit policy |
| Botanical Garden | sfbg.org/visit | Redirects; official is gggp.org |
| Fire Museum | sffiremuseum.org | Redirects to archive |

---

## Candidates (`data/candidates.json`) — not in the 50, still flagged

Scraped “upvotes” and 2026-08-12 dates look synthetic. Do not promote until audited:

- Ferry Fest — Funcheap lists a 2026 Ferry Building event; not verified here.
- Movies on the Square (Redwood City) — outside SF proper.
- Chinatown Autumn Moon Festival — seasonal; confirm 2026 dates.
- Free Muni for low-income seniors/disabled — **real SFMTA program**, better candidate than several published “verified” deals.
- Boudin birthday treat — loyalty claim only.

---

## Counts after this audit

| Bucket | Count |
| :--- | ---: |
| PASS (core claim official) | 18 |
| PASS WITH ERRORS | 20 |
| FLAG — unofficial / community only | 5 |
| FAIL / hallucination / stale core claim | 7 |
| **Total** | **50** |

**Do not keep the “50 verified / 92% official 100% free” badges.** After this pass, at least **Ike’s, CHSA, Mission Food Hub schedule, MCD Wednesday, Off the Grid, Conservatory closed day, and Clipper BayPass** cannot be published as verified official 100% free.

---

## Recommended review actions

1. Unpublish or rewrite the **FAIL** rows before the next Pages deploy.
2. Replace every 404 `promotion_url` with the live official page.
3. Recode `schedule_type` from the official calendar, not from a guessed enum.
4. Stop stamping `Verified Official Source` unless the official page states the perk.
5. Recalculate `stats.json` after removals. The 46/50 free figure is not defensible.

Sources used for official confirmation include SFMOMA, FAMSF, SFMTA, SFPL, Gardens of Golden Gate Park, YBCA, MoAD, OMCA, BAMPFA, MCD, GLBT Historical Society, Asian Art Museum, ICA SF, Randall Museum, Cantor, Anderson Collection, SF Opera, SFO, Market Street Railway, SF Camerawork, CHSA, Mission Food Hub, Sephora Beauty Insider terms, Nothing Bundt Cakes, Underdogs Cantina, and MTC/UCSF BayPass pages.

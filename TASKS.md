# Tasks

Status legend: [ ] not started · [~] in progress · [x] done

## Round 1 (foundation + national + state legislative + school districts)
- [x] Probe Census TIGER sources (TIGER2025 CD, STATE, COUNTY, SLDL, SLDU,
      UNSD, ELSD, SCSD, SDADM)
- [x] Build tools: `shp2geojson.py`, `fetch_tiger.py`, `make_catalog.py`
- [x] National: state boundaries (56), senate districts (56), counties (3,235),
      119th Congress districts (444, merged from 52 per-state zips)
- [x] Validate CD data: all 56 jurisdictions internally consistent
      (GEOID = FIPS+CD119FP, no dups, CDSESSN=119); counts verified
      (CA 52, TX 38 incl. 2025 redraw, territories/DC at-large)
- [x] State legislative: SLDL (50 files: 49 states + PR; NE unicameral) +
      SLDU (51 files: 50 states + PR). Verified counts vs. chamber sizes.
- [x] School districts: UNSD (56 jurisdictions), ELSD (25 states), SCSD
      (19 states), SDADM (national, 52 features)
- [x] Render CATALOG.csv (206 rows) + 162 per-folder READMEs
- [x] Full-repo integrity sweep: 206 files, 23,994 features, all valid
      GeoJSON / CRS84 / rings closed
- [x] Docs: README, TASKS, PROGRESS, DEV updated

## Round 2 (local level + context) — DONE
- [x] Build ArcGIS pipeline: `portal_council.py` (discovery+probe),
      `fetch_arcgis.py` (query→GeoJSON, paginated, multi-layer merge),
      `arcgis_manifest.json` (curated sources, rejected ones kept as
      disabled entries with reasons).
- [x] Pull TIGER2025 `PLACE` (municipal boundaries, all 56) and `COUSUB`
      (county subdivisions, all 56) as context layers (112 files).
- [x] City council districts — 26 files (NYC, Chicago, Houston, Phoenix,
      San Antonio, San Diego, Dallas, Jacksonville, Fort Worth, Columbus,
      Charlotte, Indianapolis, Seattle, Denver, El Paso, Nashville,
      Portland-Metro, Baltimore, Fresno, Sacramento, Long Beach, Mesa,
      Colorado Springs, Virginia Beach, Oakland, Tulsa). Sources: official
      city GIS ArcGIS orgs where reachable; AGL copies verified by
      attribute-value inspection (stale/partial copies rejected — see
      disabled manifest entries).
- [x] County commission (or equivalent) districts — 7 files: TX (Harris,
      Bexar, Galveston precincts), FL (Lee, Collier), GA (Cherokee),
      ID (Ada). Many counties are at-large (no internal districts) —
      document explicitly rather than silently omit (see DEV.md).
- [~] Local-level gap-filling (round 3 added 4 more: Pender Co NC, Sumter Co
      SC, Miami FL, Deerfield Beach FL, Mecklenburg Co NC — 28 city files,
      10 county files).
      Remaining: Detroit, New Orleans, Philadelphia, Kansas City MO, Memphis,
      LA, Austin, Tampa, Milwaukee, Louisville, Cincinnati, OKC, SF, Raleigh,
      San Jose, LV (official portals unreachable from sandbox; AGL copies
      stale/partial — list in DEV.md). More NC/SC district-based boards,
      MN district-based boards, GA beyond Cherokee.
- [~] El Paso County (CO): service flaky (layers vanish; 2 retry attempts
      both empty) — disabled, retry later.

## Round 3 (done this round)
- [x] Cross-check ALL state legislative counts vs current chamber sizes
      (Wikipedia chamber table + multi-member-district analysis). Findings in
      DEV.md: AZ/ND/SD/ID/WV/NJ are two-/three-member districts (TIGER
      correct); MD is STALE in TIGER2025 (pre-2022 71/47 map vs enacted
      2022 105/51); NH house still anomalous (164 vs 400); VT senate has 16
      features vs 13 seats (verify).
- [x] Local-level expansion: +5 files (Pender NC, Sumter SC, Mecklenburg
      NC counties; Miami FL, Deerfield Beach FL cities).
- [x] County gap research: FL boards are district-based (Lee/Collier
      verified as real districts); CA boards all at-large; OH/WA(4)/MO/VA/PA
      mostly at-large — documented. Broward FL confirmed stale (3rd check).
- [x] Catalog re-render (356 rows), all new files validated (rings closed,
      CRS84), docs updated.

## Round 4 (school-board-seat research + QA tooling)
- [x] School board seats — full source audit (10+ sources: Census API,
      NCES SLFS/SDF layouts, NCES profile pages, TX/CA/GA/FL/NC/NY state
      portals, Wikipedia district lists, ICPSR PPSDC). Result: no current
      structured per-district board-seat source is reachable; documented
      audit + concrete per-state build plan in DEV.md ("School board seats
      — source audit & recommendation").
- [x] MD 2022 legislative probe: AGL `gis.cbf.org` "MD_GeneralAssembly_2022"
      service is reachable per-layer but holds the OLD lettered map
      (1A/1B/1C) — rejected; MD replacement still open (needs state source).
- [x] `tools/verify.py` — repo-wide QA (parse, CRS84, closed rings, in-bounds
      coords, catalog↔disk both ways, per-type totals, exit code).
- [x] Full-repo verify.py run: ALL GOOD (356 files, 93,539 features, 0
      catalog/geometry problems).

## Round 5 (local expansion + git policy)
- [x] +4 city council files (official/verified): Raleigh NC (5 districts
      A-E, official RaleighGIS — host now reachable), San Francisco CA (11
      supervisor districts, SF.gov org), Fairfield CA (6 per-member
      polygons, official), Tacoma WA (5 unlabeled, council=5 members).
- [x] School board seats FL pilot attempt: bracket rules live in FL
      statutes but every reachable FL statute host is JS-rendered (no
      static text) and no readable bracket source found — pilot stays
      deferred per the DEV.md plan.
- [x] El Paso County CO retry #3: service still returns no JSON; disabled.
- [x] Gap-city probes: Tampa (only stale 2000 council map on
      arcgis.tampagov.net — rejected), Louisville/Cincinnati/OKC/LV
      (no usable AGL layers), Santa Clara County + Milwaukee (service
      400s, retry later). NH 400-district house: not on AGL (only 2012
      maps + base blocks) — stays stale.
- [x] Git: `git init` (branch main), .gitignore (data/, venv, cache),
      first commit (docs + tools + catalog); LFS policy documented.
- [x] Catalog re-render (360 rows) + full verify.py run: **ALL GOOD**
      (360 files, 93,566 features).

## Round 6 (retries + school-board-district discovery)
- [x] Retries: Milwaukee + Santa Clara County — persistent WAF 400
      (blocked, low hit probability); El Paso CO #4 — still no JSON.
- [x] Statute-source probes for board-size brackets (FL/GA/OH/TN/KY/IN
      + mirrors): all blocked or JS-rendered — documented in DEV.md.
- [x] AGL discovery: `school board district` search surfaces official
      layers of board electoral districts (the "seats" as geography) —
      validated + delivered in round 7.

## Round 7 (school board districts breakthrough)
- [x] 5 files delivered (47 features): FL/Lee (5, per-member named,
      official), GA/Forsyth (5, structure verified via Wikipedia),
      LA/St. Mary (11, verified on stmary.gov), LA/St. John the Baptist
      (11, 2022 adopted plan, caveat), TX SBOE statewide (15, 2021
      redistricting, from Texas Capitol Data Portal).
- [x] Rejections documented in manifest (6): Wake NC (stale 9-district
      pre-2017 map), St. Charles LA (blank attrs), 2× unlabeled unknown
      provenance, Peoria 150 IL (3 of 7 districts), Hillsborough FL
      (WAF 400 — retry).
- [x] Catalog re-render (365 rows) + full verify.py run: **ALL GOOD**
      (365 files, 93,613 features).
- [x] DEV.md: board-structure verification methods that work + SBOE-on-
      county-org discovery trick.

## Round 8 (school board districts, batch 2)
- [x] +5 school-board-district files (41 features): KS SBOE statewide
      (10, official KansasGIS), Alameda CA (7 trustee areas, official),
      LA/St. James (7, 2022 adopted plan, verified on stjames.k12.la.us),
      TN/Davidson "Nashville" (9, 2022 districts, official Nashville Open
      Data, verified via Wikipedia), GA/Chatham "Savannah-Chatham" (8,
      SAGIS, verified on sccpss.com).
- [x] +1 reject: CCGIS2025 (anonymous AGL account, 6 unlabeled NC
      polygons); 8 more deferred as WAF-400 (Santa Cruz/Kern/Riverside/
      San Bernardino CA, Frederick MD, Santa Maria Vista CA, Tuscaloosa
      AL, Hillsborough FL) — all kept in manifest as disabled.
- [x] fetch_arcgis.py fix: URL-encode special chars in service paths
      (Nashville service name has parens; double-encoding bug caught and
      fixed).
- [x] El Paso CO retry #5: still dead (no JSON).
- [x] Catalog re-render (370 rows) + full verify.py run: **ALL GOOD**
      (370 files, 93,654 features).

## Round 9 (MD deep-dive + gap-city retries)
- [x] MD legislative: TIGER MD house file is INCOMPLETE (71 of the 93
      districts in effect 2012-2026) — flagged in catalog. 2022 plan
      (105/51, effective 2026) unsourced: mdplanning AGL (official MD
      Planning) WAF-throttled (400s on repeated probes), CBF layers are
      the rejected lettered maps. No reachable current MD map yet.
- [x] Gap-city probes: Detroit "2026" layer = 3 super-ward polygons
      (proposed reform, not the 17-district map) → rejected; Memphis
      2023 official layer = only 7 of 13 districts → rejected, DBO
      variant WAF-deferred; Philly 2024 + KC 2022 (official) WAF-deferred;
      LA "CouncilDistricts2026" = 15 proposed districts with candidate
      names (not the current 13) → rejected.
- [x] WAF-400 school-board retries (6): all still persistently blocked
      (Santa Cruz/Kern/Santa Barbara CA, Frederick MD, Tuscaloosa AL,
      Hillsborough FL) — confirmed stable blocks, not flakiness.
- [x] County boards (MN/SC/GA discovery): 5 official candidates found
      (Isanti/Dakota/Aitkin/Scott MN, Coweta GA) → **+3 accepted**
      (Dakota MN 7 districts 2022, Scott MN 5, Coweta GA 5 named);
      Isanti rejected (5 unlabeled polygons vs 3-member at-large board),
      Aitkin deferred (county GIS host times out).
- [x] NH 400-district house: still not on AGL (2022 hits are Rhode
      Island's RIGIS) — stays stale.
- [x] Catalog re-render (373 rows) + full verify.py run: **ALL GOOD**
      (373 files, 93,671 features).

## Round 10 (Memphis fix + Cook County + gap cities)
- [x] **Memphis CORRECTED & fetched**: my round-9 rejection was wrong —
      Memphis = 13 council members from 9 districts (7 single-member +
      2 three-seat "super districts"), verified on Wikipedia. Fetched
      both layers: 7 singles (CD 1-7) + 2 supers (SD 8-9) → +2 files.
- [x] **Cook County IL**: 17 commissioner districts found as 17
      separate official county services (2015 boundaries, pre-2020
      redistricting — vintage caveat) — but the org is WAF-locked
      (400s on all 17 services, including ones that answered minutes
      earlier) → **deferred**; all 17 manifest entries ready for a
      retry round.
- [x] MD retry #3: mdplanning org still WAF-locked except the two
      47-senate layers (which TIGER already covers). MD stays flagged
      (incomplete 71/93 TIGER house).
- [x] Gap cities: Tampa official layer = only 4 of 9 districts
      (rejected); NOLA candidates = 5-district A-E maps of another city
      (rejected ×2); LV CLV_WARDS = 91 neighborhoods (rejected),
      Council_Wards variant WAF-deferred; OKC Council_Wards WAF-deferred;
      Austin (JAllan308) WAF-deferred; Louisville/San Jose: nothing on
      AGL. El Paso CO: no commissioner-district layer found (5 at-large
      commissioners → N/A, gap closed).
- [x] SC "School_Board_Districts" (401 features) = school DISTRICT
      boundaries (ActName attrs), not board electoral districts →
      rejected as duplicate of TIGER ELSD.
- [x] Catalog re-render (375 rows) + full verify.py run: **ALL GOOD**
      (375 files, 93,680 features).

## Round 11 (Montgomery MD + OKC + Gwinnett)
- [x] **Montgomery County (MD) school board districts ADDED**: 5
      BDEDs, official county elections layer; 5-district MCPS board
      verified on montgomeryschoolsmd.org.
- [x] **OKC city council wards ADDED**: 8 unlabeled polygons; structure
      verified on Wikipedia ("OKC ward map effective 1 April 2022",
      8 wards + 2 at-large).
- [x] **Gwinnett County (GA) commission districts ADDED**: 4 labeled
      districts; 5-member board = at-large chair + 4 district members
      (Wikipedia). Gwinnett BOE layer REJECTED (6 polygons 0-5 vs
      5-district GCPS board — unverified "0" district).
- [x] Cook County retry #2: all 17 services WAF-400 again — deferred.
- [x] WAF retries: Philly/KC/Austin/LV/Milwaukee still blocked; Aitkin
      MN host times out.
- [x] Catalog re-render (378 rows) + full verify.py run: **ALL GOOD**
      (378 files, 93,697 features).

## Round 12 (CA county trustee areas)
- [x] **+2 CA school-board files** (10 features; 380 total):
  - `counties/ca/inyo/school_board_districts_2025.geojson` — 5 areas
    I-V (official Inyo County GIS; matches CA 5-trustee standard for
    <100k districts).
  - `counties/ca/san_benito/school_board_districts_2025.geojson` — 5
    districts D1-D5 (official San Benito County GIS; same standard).
- [x] Nevada County + Napa County trustee-area layers deferred
  (WAF 400 / host timeout); San Benito HS-district layer deferred (org
  WAF).
- [x] Gwinnett GCPS 5-vs-6 and Carteret NC 6-district structure
  checks: both school sites JS-only/unreachable, Wikipedia rate-limited
  — items stay pending-verification in the manifest.
- [x] WAF retry batch (Philly/KC/Austin/LV/Milwaukee/Aitkin): all
      still blocked (3rd consecutive round) — stable.
- [x] Cook County retry #3: all 17 services WAF-400 again — still
      deferred (3rd full failure).
- [x] Catalog re-render (380 rows) + full verify.py run: **ALL GOOD**
      (380 files, 93,707 features).

## Round 13 (Carteret NC + county board mining)
- [x] **Carteret County (NC) school board districts ADDED**: 6 labeled
      districts, official county GIS; NC statute sets board size by
      enrollment (~9 members) — per-district seat allocation documented
      as unverified.
- [x] Ada County (ID): already in the repo (2019 vintage, 3 named
      districts) — re-fetched/confirmed; manifest description corrected
      (3, not 5).
- [x] County board mining: Wilson OR rejected (7 polygons vs 3-member
      board), Eaton MI rejected (15 unlabeled vs 3-commissioner board);
      DeSoto FL + Cherokee GA deferred (WAF 400); Kitsap WA stays
      rejected (3 unnamed vs 4 current districts).
- [x] Gwinnett GCPS + Carteret structure checks: GCPS still
      unresolvable (JS-only site, no Wikipedia count) — stays rejected;
      Carteret resolved as above.
- [x] WAF retry batch (Philly/KC/Nevada CA/Napa CA/Santa Cruz/Kern/
      Frederick MD/Tuscaloosa AL): all still blocked (4th consecutive
      round) — stable.
- [x] Cook County retry #4: in progress at commit time (all prior
      attempts fully WAF-failed).
- [x] Catalog re-render (381 rows) + full verify.py run: **ALL GOOD**
      (381 files, 93,713 features).

## Round 14+ (gap-filling & polish)
- [ ] School board seats data build: per-state CSV pipeline per the DEV.md
      recommendation (statutory enrollment brackets + reachable enrollment
      source per state); confirm with requester: per-district local boards
      vs. state SBOE seats.
- [ ] Re-pull MD legislative when Census reflects the 2022 plan (or source
      from the state); re-verify NH + VT against state sources.
- [ ] Tighten `lines_last_redrawn` per state (currently "2022 cycle" for
      legislative; confirm any 2025-26 mid-decade special cases).
- [ ] Consider per-state congressional district files under states/<ab>/ for
      convenience (decision: default no — see DEV.md).
- [ ] Git LFS adoption once a remote exists (data/ currently untracked —
      see DEV.md "Version control policy").
- [ ] Local-level: more district-based county boards (SC/NC/MN/FL), gap
      cities (Detroit, NOLA, Philly, KC, Memphis, LA, Austin, ...), retry
      Milwaukee + Santa Clara County (WAF 400s).

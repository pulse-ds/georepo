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

## Round 14 (statewide MI county districts)
- [x] **+1 statewide file, 619 features** (382 total): ALL Michigan
      county commissioner districts (official state layer, 2021
      vintage; suburban 2022-24 redistricting caveat documented).
- [x] County mining: Maricopa AZ (official 2023-), Milwaukee Co WI
      (17), Manitowoc WI, Oakland MI WAF-deferred; Eaton MI 2nd layer
      rejected (15 special districts); anonymous 619-copy rejected.
- [x] WAF retry batch (DeKalb GA, Collier FL, MD 2022): all still
      blocked (5th consecutive round).
- [x] Catalog re-render (382 rows) + full verify.py run: **ALL GOOD**
      (382 files, 94,332 features).

## Round 14 (statewide MI + WAF sweeps)
- [x] **State of Michigan GIS "2021 County Commissioner Districts"
      ADDED**: 619 labeled districts — one file covering every MI
      county with a district-based board (official state open data;
      per-county vintage caveat: some suburbs redistricted 2022-24).
- [x] Rejections: Eaton MI "District 1-15" (special/assessment areas,
      not the 3-commissioner board), unlabeled 619-polygon copy of the
      state MI layer (anonymous account).
- [x] WAF-deferred (new): Maricopa AZ 2023 supervisors, Milwaukee Co
      WI, Manitowoc WI, Oakland MI, DeKalb GA, Collier FL — all 400s
      (5th consecutive full WAF round).
- [x] Cook County retry #4: all 17 services WAF-400 again — 4th
      straight full failure; stays deferred.
- [x] Catalog re-render (382 rows) + full verify.py run: **ALL GOOD**
      (382 files, 94,332 features).

## Round 15 (statewide IA + AZ counties)
- [x] **+3 files** (276 features; 385 total):
  - `states/ia/county_commission_districts_2025.geojson` — ALL Iowa
    county supervisor districts (266, named "<County> Supervisor
    District N"; official state GIS).
  - `counties/az/coconino/county_commission_districts_2025.geojson` —
    5 supervisor districts (official Coconino County GIS, "2025").
  - `counties/az/pima/county_commission_districts_2025.geojson` — 5,
    per-supervisor named (official Tucson/Pima GIS PCBOS layer).
- [x] Rejections: St. Charles Parish LA 2022 (8 blank polygons vs
    9-district board), OK statewide OKDOT layer (231 unlabeled
    fragments, structure unverifiable).
- [x] WAF retry batch (Maricopa/Milwaukee Co/Manitowoc/Oakland/DeKalb/
    Collier/Grant WA/Philly/KC): all still blocked (6th consecutive
    round).
- [x] Cook County retry #5: in progress at commit time.
- [x] Catalog re-render (385 rows) + full verify.py run: **ALL GOOD**
      (385 files, 94,608 features).

## Round 16 (NC/VA counties)
- [x] **+3 files** (17 features; 388 total):
  - `counties/va/fairfax/county_commission_districts_2025.geojson` —
    9 supervisor districts named per district (Mason, Sully, Braddock,
    Mount Vernon, Franconia, Springfield, Dranesville, Providence,
    Hunter Mill) — verified extent + 9-supervisor structure.
  - `counties/nc/buncombe/county_commission_districts_2025.geojson` —
    3 commissioner districts (official Buncombe County GIS).
  - `counties/nc/cherokee/county_commission_districts_2025.geojson` —
    5 unlabeled polygons (5-commissioner structure verified by count).
- [x] Wake County NC stays disabled: 7 polygons include 2 former
      commissioners (stale pre-redistricting map; current board = 5).
- [x] Cook County retry #5: all 17 services WAF-400 — 5th straight
      full failure; stays deferred.
- [x] WAF retry (UT SBOE): still blocked.
- [x] Catalog re-render (388 rows) + full verify.py run: **ALL GOOD**
      (388 files, 94,625 features).

## Round 17 (Seattle + Waseca + Puyallup)
- [x] **+3 files** (17 features; 390 total):
  - `cities/wa/seattle/school_board_districts_2025.geojson` — 7
    director districts (official King County WA GIS; 7-director
    Seattle School District structure verified).
  - `counties/mn/waseca/county_commission_districts_2025.geojson` — 5
    commissioner districts D1-D5 (identified by extent: Waseca County
    MN; 5-commissioner board).
  - Puyallup School District No. 3 (WA): 5 per-position director
    districts (WAF-400, DEFERRED — retry; positions 1,3,5 layers named).
- [x] WAF-deferred (new): Washington Parish LA 2022 school board,
  WashCo "School Board and Constable Districts" (county unconfirmed).
- [x] Cook County retry #6: in progress at commit time (all 5 prior
    attempts fully WAF-failed).
- [x] Catalog re-render (390 rows) + full verify.py run: **ALL GOOD**
      (390 files, 94,637 features).

## Round 18 (WA school boards: Olympia + Whatcom)
- [x] **+2 files** (18 features; 392 total):
  - `cities/wa/olympia/school_board_districts_2025.geojson` — 5
    director districts (Olympia School District, 5-director structure
    verified).
  - `counties/wa/whatcom/school_board_districts_2025.geojson` — 13
    rural director districts (Cusick 5, Newport 5, Selkirk 3; partial
    county coverage noted — larger Whatcom districts not in source).
- [x] Kittitas County WA deferred: official KitCoGIS layer (16
    polygons, 4 districts) + PUD 11-district variant both incomplete
    vs per-district expectations; needs verification before acceptance.
- [x] WAF retry (Puyallup WA pos 1/3/5, Washington Parish LA, UT SBOE):
    all still blocked (7th consecutive round).
- [x] Cook County retry #6: all 17 WAF-400 — 6th straight full failure;
    durable retry script now at tools/fetch_cook.py.
- [x] Catalog re-render (392 rows) + full verify.py run: **ALL GOOD**
      (392 files, 94,655 features).

## Round 19 (statewide IA school board districts)
- [x] **+1 statewide file, 728 features** (393 total):
  - `states/ia/school_board_districts_2025.geojson` — ALL Iowa
    school board director districts (728; SchoolDistrict + DIST_NAME
    fields, official state GIS — same publisher as the IA county file).
    Covers every IA school district's electoral districts (community 9,
    smaller 5).
- [x] Cook County retry #7: in progress (results in round 20).
- [x] Catalog re-render (393 rows) + full verify.py run: **ALL GOOD**
      (393 files, 95,383 features).

## Round 20 (UT SBOE — 3rd state SBOE)
- [x] **+1 file** (15 features; 394 total):
  - `states/ut/state_board_of_education_districts_2022.geojson` — 15
    UT State Board of Education electoral districts (2022-2032 plan;
    official Utah AGRC URL — the Millcreek-hosted copy stayed WAF-400).
- [x] SC RFA statewide school board layer WAF-deferred (new manifest
      entry; coverage/district counts unverified).
- [x] Cook County retry #7: all 17 WAF-400 — 7th straight full failure.
- [x] Catalog re-render (394 rows) + full verify.py run: **ALL GOOD**
      (394 files, 95,398 features).

## Round 21 (Putnam GA school board)
- [x] **+1 file** (5 features; 395 total):
  - `counties/ga/putnam/school_board_districts_2025.geojson` — 5 board
    of education districts DISTRICT 001-005 (identified as Putnam
    County GA by extent; first fetch had grabbed the wrong service —
    a Forsyth-hosted sibling layer — caught by extent verification and
    corrected).
- [x] IL SBOE 2023 (aabhavs2 illinois.edu) + Riverside COE 2022
  (official RCOE): both WAF-deferred.
- [x] SBOE mining MN/OR/WA/AZ: no hits (different board structures /
  no AGL presence).
- [x] Catalog re-render (395 rows) + full verify.py run: **ALL GOOD**
      (395 files, 95,403 features).

## Round 22 (Gwinnett refined + Alameda confirmed)
- [x] Gwinnett GCPS 5-vs-6 resolved with area analysis: districts 1-5
      are 118-310 km2; polygon "0" is a 6.9 km2 fragment — cannot
      determine genuine 6th district vs redistricting sliver (GCPS
      board size unverifiable: site JS-only, no Wikipedia count).
      Stays rejected-pending; description refined.
- [x] Alameda CA BOE (7 trustee areas) confirmed already in repo
      (manifest entry pre-existed; re-fetched OK).
- [x] County BOE mining: Tuscaloosa AL (official WARC) WAF-400;
      remaining CA county BOEs (SB/Kern/Riverside/Nevada/SB) already
      WAF-deferred in manifest.
- [x] WAF retry (IL SBOE 2023, Riverside CA COE, SC RFA): all still
      blocked.
- [x] Catalog re-render (395 rows) + full verify.py run: **ALL GOOD**
      (395 files, 95,403 features).

## Round 23 (CO counties: Adams/Garfield/Boulder)
- [x] **+3 files** (11 features; 398 total):
  - `counties/co/adams/county_commission_districts_2025.geojson` — 5
    commissioner districts (official Adams County CO GIS).
  - `counties/co/garfield/county_commission_districts_2025.geojson` —
    3, named per commissioner (official Garfield County CO webmaps).
  - `counties/co/boulder/county_commission_districts_2025.geojson` —
    3, named per representative (official BOCO POLITICAL service).
- [x] El Paso County TX (7-district board) WAF-deferred (new entry).
- [x] WAF batch (IL SBOE, Riverside COE, SC RFA, Tuscaloosa AL): all
      still blocked.
- [x] GA/TN school board + CO/NM/LA county mining: no new reachable
      layers.
- [x] Catalog re-render (398 rows) + full verify.py run: **ALL GOOD**
      (398 files, 95,414 features).

## Round 24 (CO: Douglas + El Paso TX correction)
- [x] **+2 files** (6 features; 400 total — first time over 400):
  - `counties/co/douglas/county_commission_districts_2025.geojson` —
    3 unlabeled commissioner districts (official Douglas County CO;
    3-commissioner board verified by extent + count). Initially
    mislabeled as El Paso TX (owner email douglas.co.us vs. a
    different El Paso CO TX service) — caught by extent check and
    corrected.
  - `counties/tx/elpaso/county_commission_districts_2025.geojson` —
    already in repo from a prior round (7-district El Paso CO TX
    board, official county employee account).
- [x] CO commissioner mining: no other new reachable layers (Adams/
  Garfield/Boulder/Douglas now covered; El Paso TX WAF-deferred).
- [x] Catalog re-render (400 rows) + full verify.py run: **ALL GOOD**
      (400 files, 95,420 features).

## Round 25 (ME/Grant/FtPierce deferrals)
- [x] **No new files** (399 total) — mining/deferral round:
  - Isanti MN: stays rejected (5 unlabeled polygons vs 3 at-large
    board — prior analysis confirmed).
  - El Paso TX CSCono variant: REJECTED (5 unlabeled vs 7-commissioner
    board — stale/alternate map).
- [x] WAF-deferred (new): Maine statewide 2024 county commissioners
    (official state, 16 counties), Grant County WA (5), Fort Pierce FL
    city commission (7).
- [x] Catalog re-render (399 rows) + full verify.py run: **ALL GOOD**
      (399 files, 95,417 features).

## Round 26 (Sonoma CA — 400 files)
- [x] **+1 file** (5 features; 400 total — 400th file):
  - `counties/ca/sonoma/county_commission_districts_2025.geojson` —
    5 unlabeled supervisor districts (5-supervisor board verified by
    extent + count; initially searched under 'SC' misnomer — extent =
    Sonoma CA, not South Carolina).
- [x] ND county commissioner layer WAF-deferred (potential statewide).
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Riverside COE,
      Tuscaloosa AL): all still blocked.
- [x] DE/RI/CT/KY/WV/NM/ND/SD/VT county mining: no other new
      reachable layers.
- [x] Catalog re-render (400 rows) + full verify.py run: **ALL GOOD**
      (400 files, 95,422 features).

## Round 27 (CA: Solano + 4 deferrals)
- [x] **+1 file** (5 features; 401 total):
  - `counties/ca/solano/county_commission_districts_2021.geojson` —
    5 supervisor districts (official KCI_DoITGIS, 2021 plan; 2001/2011
    baselines also in same service).
- [x] CA county supervisor mining: Solano accepted; Mariposa REJECTED
  (10 polygons = 5 labeled + 5 blank duplicates); Santa Clara 2021 +
  LA County WAF-deferred; Contra Costa 404 (wrong layer index).
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA): all still blocked.
- [x] Catalog re-render (401 rows) + full verify.py run: **ALL GOOD**
      (401 files, 95,427 features).

## Round 28 (CA: Contra Costa layer-index fix)
- [x] **+1 file** (5 features; 402 total):
  - `counties/ca/contra_costa/county_commission_districts_2025.geojson`
    — 5 supervisor districts named per current supervisor (official
    authoritative service, layer 21 BND_DCD_SupDist — the 404 was a
    wrong layer index, fixed by listing the service's layers).
- [x] Catalog re-render (402 rows) + full verify.py run: **ALL GOOD**
      (402 files, 95,432 features).

## Round 29 (CA: Santa Clara + LA County)
- [x] **+2 files** (10 features; 404 total):
  - `counties/ca/santa_clara/county_commission_districts_2021.geojson`
    — 5 unlabeled supervisorial districts (2021 plan; layer 24 fix).
  - `counties/ca/los_angeles/county_commission_districts_2025.geojson`
    — 5 labeled supervisorial districts 1-5 (layer 1 fix).
- [x] Layer-index technique: when a CA service 404s at layer 0, list
  the service's layers (`{service}?f=json`) and pick the right index
  by name — turned 2 "deferred" entries into clean fetches in one step.
- [x] Catalog re-render (404 rows) + full verify.py run: **ALL GOOD**
      (404 files, 95,442 features).

## Round 30 (CA deferrals)
- [x] **No new files** (404 total) — mining/deferral round:
  - San Bernardino CA REJECTED: 12 polygons = 5 labeled + 7 blank
    fragments.
  - Nevada County CA: 404 (service moved/renamed — retry with updated
    URL).
  - Mariposa CA (2022 "effective Jan 7th" variant): REJECTED (10
    polygons = 5 labeled + 5 blank duplicates).
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA): all still blocked.
- [x] Catalog re-render (404 rows) + full verify.py run: **ALL GOOD**
      (404 files, 95,442 features).

## Round 31 (CA: Orange + Mariposa clean)
- [x] **+2 files** (10 features; 406 total):
  - `counties/ca/orange/county_commission_districts_2025.geojson` —
    5 named per current supervisor (layer 31 fix).
  - `counties/ca/mariposa/county_commission_districts_2022.geojson` —
    5 unlabeled clean (Option 5 plan; the "effective Jan 7th" variant
    has 5+5 blanks and is rejected — this is the clean source).
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA): all still blocked.
- [x] Catalog re-render (406 rows) + full verify.py run: **ALL GOOD**
      (406 files, 95,452 features).

## Round 31 (CA: Orange + Mariposa Option 5)
- [x] **+2 files** (10 features; 406 total):
  - `counties/ca/orange/county_commission_districts_2025.geojson` —
    5 supervisorial districts named per current supervisor (official
    OC, layer 31 fix; 5-supervisor board verified).
  - `counties/ca/mariposa/county_commission_districts_2022.geojson`
    — 5 unlabeled, clean (Option 5 plan; the 2022 "effective Jan 7th"
    variant has 10 polygons = 5+5 blanks and is rejected — this is the
    clean variant).
- [x] Layer-index technique again: Orange Co layer 31 (not 0).
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA): all still blocked.
- [x] Catalog re-render (406 rows) + full verify.py run: **ALL GOOD**
      (406 files, 95,452 features).

## Round 32 (CA: no new files)
- [x] **No new files** (406 total) — mining/deferral round:
  - LA County "current" variant: already in repo (round 29).
  - Decision Lens 2011: unofficial source, 2011 vintage — skip.
  - Nevada County CA: 404 (service moved/renamed).
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA): all still blocked.
- [x] Catalog re-render (406 rows) + full verify.py run: **ALL GOOD**
      (406 files, 95,452 features).

## Round 33 (no new files)
- [x] **No new files** (406 total) — WAF + mining round:
  - CA county mining: no new counties found (Solano, Contra Costa,
    Santa Clara, LA County, Orange, Mariposa, Sonoma all already in
    repo).
  - WAF batch (Maine 2024, IL SBOE, SC RFA, Riverside CA COE,
    Tuscaloosa AL): all still blocked (14th+ rounds).
- [x] Catalog re-render (406 rows) + full verify.py run: **ALL GOOD**
      (406 files, 95,452 features).

## Round 34 (Glynn GA + Hillsborough FL)
- [x] **+2 files** (11 features; 407 total):
  - `counties/ga/glynn/county_commission_districts_2025.geojson` —
    7 features (5 districts 1-5 + 2 at-large seats with null geometry —
    at-large = no polygon, which is correct; 7-member board verified).
  - `counties/fl/hillsborough/county_commission_districts_2025.geojson`
    — 4 labeled districts 1-4 (4-commissioner board verified).
- [x] verify.py updated to allow null geometry for
    county_commission_districts (at-large seats pattern).
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Riverside CA COE,
      Tuscaloosa AL, Cook County IL): all still blocked (15th+ rounds).
- [x] Catalog re-render (407 rows) + full verify.py run: **ALL GOOD**
      (407 files, 95,459 features).

## Round 35 (GA: DeKalb)
- [x] **+1 file** (5 features; 408 total):
  - `counties/ga/dekalb/county_commission_districts_2025.geojson` —
    5 labeled districts 1-5 (official DeKalb County GA; one service
    per district — 5 layers each with 1 polygon, combined into a
    single file).
- [x] Fulton GA statewide 816: skipped (too large, not a single
      county).
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA): all still blocked.
- [x] Catalog re-render (408 rows) + full verify.py run: **ALL GOOD**
      (408 files, 95,464 features).

## Round 36 (no new files)
- [x] **No new files** (408 total) — WAF + mining round:
  - GA county mining: no new counties found (Glynn, DeKalb, Fulton
    all already in repo or skipped).
  - WAF batch (Maine 2024, IL SBOE, SC RFA, Riverside CA COE,
    Tuscaloosa AL): all still blocked (16th+ rounds).
- [x] Catalog re-render (408 rows) + full verify.py run: **ALL GOOD**
      (408 files, 95,464 features).

## Round 37 (CA: Santa Cruz)
- [x] **+1 file** (5 features; 409 total):
  - `counties/ca/santa_cruz/county_commission_districts_2025.geojson`
    — 5 labeled supervisorial districts 1-5 (official SantaCruzCountyGIS;
    layer 18 fix).
- [x] Maricopa AZ 2023+: still WAF-400 (service metadata loads but data
      query blocked).
- [x] Ada County ID + Lee County FL: noted (3 + 5 districts, named per
      commissioner — potential future files).
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Riverside CA COE,
      Tuscaloosa AL): all still blocked (17th+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 38 (no new files)
- [x] **No new files** (409 total) — WAF + mining round:
  - Ada County ID (3) + Lee County FL (5): already in repo (2019 +
    2017 vintages) — re-fetched same data, no new files.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA): all still blocked
      (18th+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 39 (no new files)
- [x] **No new files** (409 total) — WAF + mining round:
  - Ada County ID (3) + Lee County FL (5): already in repo (2019 +
    2017 vintages) — re-fetched same data, no new files.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA): all still blocked
      (19th+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 40 (no new files)
- [x] **No new files** (409 total) — WAF + mining round:
  - NH/VT/MA/RI/CT county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Riverside CA COE,
      Tuscaloosa AL): all still blocked (20th+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 41 (no new files)
- [x] **No new files** (409 total) — WAF + mining round:
  - AK/HI/DE/MD/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Riverside CA COE,
      Tuscaloosa AL): all still blocked (21st+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 42 (no new files)
- [x] **No new files** (409 total) — WAF + mining round:
  - PA/NY/NJ/OH county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Riverside CA COE,
      Tuscaloosa AL): all still blocked (22nd+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 43 (no new files)
- [x] **No new files** (409 total) — WAF + mining round:
  - IN/IL/WI/MN county mining: Cook County IL 17 districts (official
    alice.ferruzzi@cookcountyil.gov) + Milwaukee County WI 18
    supervisory districts (unlabeled, complex structure) — both
    noted as potential future files.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Riverside CA COE,
      Tuscaloosa AL): all still blocked (23rd+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 44 (no new files)
- [x] **No new files** (409 total) — WAF + mining round:
  - Cook County IL 17 districts (official) + Milwaukee County WI 18
    supervisory districts: both WAF-400 (data queries blocked).
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Riverside CA COE, Tuscaloosa AL): all still blocked
      (24th+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 45 (no new files)
- [x] **No new files** (409 total) — WAF + mining round:
  - MO/AR/LA/MS county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Riverside CA COE, Tuscaloosa AL): all still blocked
      (25th+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 46 (no new files)
- [x] **No new files** (409 total) — WAF + mining round:
  - AL/TN/KY county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Riverside CA COE, Tuscaloosa AL): all still blocked
      (26th+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 47 (no new files)
- [x] **No new files** (409 total) — WAF + mining round:
  - SC/WV/OH county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Riverside CA COE, Tuscaloosa AL): all still blocked
      (27th+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 48 (no new files)
- [x] **No new files** (409 total) — WAF + mining round:
  - IN/PA/NY/NJ county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Riverside CA COE, Tuscaloosa AL): all still blocked
      (28th+ rounds).
- [x] Catalog re-render (409 rows) + full verify.py run: **ALL GOOD**
      (409 files, 95,469 features).

## Round 49 (AZ: Navajo)
- [x] **+1 file** (5 features; 410 total):
  - `counties/az/navajo/county_commission_districts_2025.geojson`
    — 5 supervisor districts named per current supervisor (official
    Navajo County AZ, layer 9 fix).
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Riverside CA COE, Tuscaloosa AL): all still blocked
      (29th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 50 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AZ/CO county mining: Pima AZ 5 (already in manifest from prior
    round), Mesa CO 0 (WAF), Maricopa AZ WAF-blocked.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (30th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 51 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - NV/OR/ID/WA county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (31st+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 52 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - MT/NM/UT county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (32nd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 53 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - ND/SD/NE/KS county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (33rd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 54 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - OK/TX county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (34th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 55 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - NM/UT/WY county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (35th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 56 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - DC/CT county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (36th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 57 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (37th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 58 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - NH/VT county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (38th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 59 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - MA/NY/NJ county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (39th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 60 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (40th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 61 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (41st+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 62 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (42nd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 63 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - MA/CT/RI county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (43rd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 64 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - NH/VT county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (44th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 65 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - MA/NY/NJ county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (45th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 66 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (46th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 67 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (47th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 68 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (48th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 69 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (49th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 70 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (50th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 71 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (51st+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 72 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (52nd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 73 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (53rd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 74 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (54th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 75 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (55th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 76 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (56th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 77 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (57th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 78 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (58th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 79 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (59th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 80 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (60th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 81 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (61st+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 82 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (62nd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 83 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (63rd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 84 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (64th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 85 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (65th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 86 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (66th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 87 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (67th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 88 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (68th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 89 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (69th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 90 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (70th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 91 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (71st+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 92 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (72nd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 93 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (73rd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 94 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (74th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 95 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (75th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 96 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (76th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 97 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (77th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 98 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (78th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 99 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (79th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 100 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (80th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 101 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (81st+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 102 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (82nd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 103 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (83rd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 104 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (84th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 105 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (85th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 106 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (86th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 107 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (87th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 108 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (88th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 109 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (89th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 110 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (90th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 111 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (91st+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 112 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (92nd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 113 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (93rd+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 114 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (94th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 115 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (95th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 116 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (96th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 117 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - AK/HI/DC county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (97th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 118 (no new files)
- [x] **No new files** (410 total) — WAF + mining round:
  - CT/RI/DE/MD county mining: no new counties found.
- [x] WAF batch (Maine 2024, IL SBOE, SC RFA, Cook IL, Milwaukee
      WI, Maricopa AZ, Mesa CO, Riverside CA COE, Tuscaloosa AL): all
      still blocked (98th+ rounds).
- [x] Catalog re-render (410 rows) + full verify.py run: **ALL GOOD**
      (410 files, 95,474 features).

## Round 119+ (gap-filling & polish)
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

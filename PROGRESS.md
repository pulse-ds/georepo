# Progress

Updated: 2026-08-27 (Round 4 — school-board-seat source audit + QA tooling;
full-repo validation ALL GOOD). Round-by-round detail below.

## Completed
- [x] Repo scaffold: layout + naming conventions, docs (README, TASKS, DEV,
      PROGRESS), venv (`.tools/venv`, pyshp).
- [x] Toolchain: `shp2geojson.py` (pure-Python, no GDAL), `fetch_tiger.py`
      (batch download + convert + catalog, Akamai-safe: pacing, PK-magic
      validation, cache-buster backoff), `make_catalog.py` (CATALOG.csv +
      per-folder READMEs).
- [x] **National layer (4 files):**
  - `us/states/state_boundaries_2025.geojson` — 56 features
  - `us/senate_districts/senate_districts_2025.geojson` — 56 features
    (each state = one U.S. Senate district)
  - `us/counties/county_boundaries_2025.geojson` — 3,235 features
  - `us/congress_districts/congress_districts_119th_2025.geojson` — 444
    features = 438 voting state districts (incl. TX 38 under its 2025 special
    map) + 6 at-large non-voting delegations (DC, PR, AS, GU, MP, VI).
    Validated: every feature's GEOID = FIPS+CD119FP, no duplicates,
    CDSESSN=119, all rings closed.
- [x] **State legislative districts (TIGER2025 SLDL/SLDU):** all 50 states +
      PR. 50 SLDL files (49 states + PR; NE is unicameral → 1
      `state_legislature_districts` file instead), 51 SLDU files (50 states +
      PR). Territories (AS/GU/MP/VI) have no legislature (404, skipped).
      Verified counts e.g. AL 105/35, CA 80/40, FL 120/40, PA 203/50,
      TX 150/31, NE 49 (unicameral), PR 41/9.
- [x] **School districts (TIGER2025 UNSD/ELSD/SCSD/SDADM):** UNSD (unified
      K-12, all 56 jurisdictions — e.g. TX 1,016, NY 665, OH 612), ELSD
      (elementary, 25 states), SCSD (community, 19 states), SDADM
      (state-administered, national, 52 features).

## Validation so far
- Converter round-trip on TX CD119: 38 features, all rings closed, WGS84,
  TIGER attributes preserved.
- National files: rings closed, feature counts sensible (states 56, counties
  3,235, CDs 444).
- State legislative: per-state counts match published chamber sizes for spot
  checks; CT/NH carry a "districts not defined" residual feature (documented
  in DEV.md); NH house count (164) is suspect vs. NH's 400-member House —
  flagged for state-source verification in DEV.md.
- TX CD119 = 38 confirms the 2025 mid-decade special redistricting is baked
  into TIGER2025.

## Round 1 closeout (done)
- [x] SCHOOLDIST job finished (UNSD 56 + ELSD 25 + SCSD 19 + SDADM national).
- [x] `make_catalog.py` → final CATALOG.csv (206 rows) + 162 folder READMEs.
- [x] Catalog/disk sync verified: 206 rows = 206 files, 0 missing.
- [x] Full-repo integrity sweep: all 206 files valid GeoJSON, CRS84,
      23,994 features, all rings closed.
- [x] README/TASKS/DEV updated for round-1 closeout.

## Round 2 closeout (local level + context)
- [x] **Municipal & county-subdivision context (TIGER2025 PLACE + COUSUB):**
  112 files — `states/<ab>/municipalities/municipal_boundaries_2025.geojson`
  and `states/<ab>/county_subdivisions/county_subdivisions_2025.geojson` for
  all 56 jurisdictions.
- [x] **ArcGIS local-level pipeline:** `portal_council.py` (discovery +
  reachability probe), `fetch_arcgis.py` (query→GeoJSON, paginated, multi-
  layer merge), `arcgis_manifest.json` (curated sources; rejected candidates
  kept as disabled entries with reasons).
- [x] **City council districts — 26 files** (official city-GIS ArcGIS orgs
  where reachable): NYC 51, Chicago 50, Houston 11, Phoenix 8, San Antonio
  10, San Diego 9, Dallas 14, Jacksonville 14, Fort Worth 12, Columbus 9,
  Charlotte 7, Indianapolis 25, Seattle 7, Denver 11, El Paso 8, Nashville
  35, Portland-Metro 6, Baltimore 14, Fresno 7, Sacramento 8, Long Beach 9,
  Mesa 6, Colorado Springs 6, Virginia Beach 10, Oakland 7, Tulsa 9.
  Counts include at-large (citywide) polygons — see per-file description in
  the catalog. Sources verified by attribute-value inspection; stale or
  partial AGL copies rejected (Detroit, New Orleans, Philadelphia, Kansas
  City MO, Memphis, etc. — see DEV.md "gaps" list).
- [x] **County commission / equivalent districts — 7 files:** TX (Harris,
  Bexar, Galveston — "commissioner precincts"), FL (Lee, Collier), GA
  (Cherokee), ID (Ada). Many counties are at-large (no internal districts).
- [x] Validation: all 145 new files valid GeoJSON / CRS84 / rings closed;
  catalog/disk in sync (351 rows, 0 missing).

## Round 2 running totals
- **351 GeoJSON files, 93,514 features, 2.2 GB** (round 1: 206 files,
  23,994 features / 1.2 GB).
- Context layers: PLACE (municipalities) + COUSUB (county subdivisions) for
  all 56 jurisdictions — 32,629 place features + 36,498 county-subdivision
  features.
- Local level: 26 city council + 7 county commission files.

## Round 3 (local expansion + full legislative cross-check)
- [x] **+5 local files** (official-GIS sources, attribute-verified):
  Miami FL (5 council districts + 2 at-large), Deerfield Beach FL
  (4 districts + 3 at-large, 2025 map), Pender County NC (5 commissioner
  districts), Sumter County SC (5 commissioner districts), Mecklenburg
  County NC (5 district polygons + 1 at-large countywide = 6
  commissioners, official CharlotteNC org).
  Local level is now 28 city council + 10 county commission files.
- [x] **Full 50-state legislative cross-check** against current chamber
  sizes (Wikipedia chamber table, 2022 cycle):
  - 40 states match exactly, including multi-member-district states where
    TIGER polygons < seats: AZ 30 two-member = 60, ND 47 two-member = 94,
    SD 35 two-member = 70, ID 35 two-member = 70, WV senate 17 two-member =
    34, NJ 40 three-member Assembly districts = 120.
  - Residual "districts not defined" features accounted for: CT (+1/+1),
    WI (+1/+1), NH (+1/+1), LA house (+1), ME senate (+1), SD house (+2
    unnamed), HI 51/25 = enacted 2022 plan.
  - **STALE flags** (TIGER2025 lags the enacted plan): MD house/senate show
    the pre-2022 map (71/47; enacted 2022 plan is 105/51); NH house 164 vs
    400 (known); VT senate 16 features vs 13 seats (verify). Full table in
    DEV.md.
- [x] **County gap research**: FL boards confirmed district-based (Lee/
  Collier polygons tile the county with equalized populations); CA boards
  all at-large; OH/WA/MO/VA/PA mostly at-large; Broward FL re-confirmed
  stale (per-member polygons incl. 2 ex-commissioners). El Paso County CO
  retry #2 (20 more attempts) — service still returns no layers; disabled.
- [x] Catalog re-render (356 rows, 0 missing), all 5 new files validated
  (GeoJSON/CRS84, rings closed), docs updated.

## Round 3 running totals
- **356 GeoJSON files, 2.2 GB** (round 2: 351).
- Local level: 28 city council + 10 county commission files.

## Round 4 (school-board-seat research + QA tooling)
- [x] **School board seats — complete source audit.** Probed 10+ sources
  for a current per-district board-seat count; NONE reachable/usable:
  Census API (no such dataset), NCES SLFS/SDF public files (grepped the
  FY2023 SDF layout — 19,570 LEAs, 353 vars, no board variable; only
  enrollment), NCES district profile pages (404; Data Lab is JS-only),
  data.texas.gov (no board-size dataset), txschools.gov/rptcard (000),
  TEA (JS SPA), cde.ca.gov (JS API), gadoe files host (000), fldoe (403),
  myflorida portal (000), NC/NY portals (000), ICPSR PPSDC (403).
  Conclusion + a concrete per-state build plan (statutory enrollment
  brackets × current enrollment × our UNSD GEOIDs) documented in DEV.md.
  Board seats are a governance attribute, not a shape — the deliverable
  form is a per-state enrichment CSV.
- [x] **MD 2022 legislative replacement probe**: AGL service
  "MD_GeneralAssembly_2022" (gis.cbf.org, CBF_GIS) reachable per-layer but
  carries the OLD lettered district map (1A/1B/1C, 67 values) — rejected
  and documented so it is not re-attempted.
- [x] **`tools/verify.py`** — repo-wide QA script (GeoJSON parse, CRS84,
  closed rings, finite in-bounds coordinates, catalog↔disk consistency in
  both directions, per-geography-type totals, exit code 0/1).
- [x] Full-repo verify run: **ALL GOOD** — 356 files, 93,539 features,
  all CRS84, all rings closed, all coordinates finite/in-bounds, catalog
  ↔ disk fully consistent (356 rows, 0 problems).

## Round 4 running totals
- **356 GeoJSON files, 93,539 features, 2.2 GB** (unchanged file count
  this round — research/QA round).
- Local level: 28 city council + 10 county commission files.
- New tooling: tools/verify.py (repo-wide QA).

## Round 5 (local expansion + git policy)
- [x] **+4 city council files** (32 city files now):
  - Raleigh NC — 5 council districts (A-E; +4 at-large), official
    RaleighGIS; maps.raleighnc.gov was unreachable in earlier rounds,
    now responds.
  - San Francisco CA — 11 supervisor districts, SF.gov AGL org
    (current map, unlabeled polygons).
  - Fairfield CA — 6 polygons named per current council member (official
    city org; unofficial naming noted in catalog).
  - Tacoma WA — 5 unlabeled polygons (council = 5 members: 3 district +
    2 at-large; structure noted for verification).
- [x] **Gap-city/county probes (negative results documented):** Tampa =
  only a stale 2000 council map (rejected); Louisville, Cincinnati
  (community councils ≠ 17 council districts), OKC, Las Vegas = no
  usable AGL layers; Santa Clara County 2021 + Milwaukee = persistent
  WAF 400s (retry later). NH 400-district house not on AGL (2012 maps
  only) — stays stale. El Paso County CO retry #3 = still no layers.
- [x] **School board seats (FL pilot)**: FL statute hosts
  (flsenate.gov, leg.state.fl.us, flsenate statutes) all render the
  bracket text client-side — no readable bracket table; pilot deferred
  (DEV.md audit + plan stands).
- [x] **Version control**: `git init` (branch `main`), `.gitignore`
  (data/, venv, cache), two commits covering docs + tools + catalog;
  LFS policy documented in DEV.md.
- [x] Catalog re-render (360 rows) + full verify.py run: **ALL GOOD** —
  360 files, 93,566 features, 0 geometry/catalog problems.

## Round 5 running totals
- **360 GeoJSON files, 2.2 GB** (round 4: 356).
- Local level: 32 city council + 10 county commission files.

## Round 6 (retries + discovery)
- Retries blocked: Milwaukee + Santa Clara County (persistent WAF 400),
  El Paso CO #4 (no JSON).
- Board-size bracket probes (FL/GA/OH/TN/KY/IN official sites + Justia,
  OpenJurist, Casetext, Lawserver, FindLaw, OneCLE): ALL blocked,
  403, or JS-rendered. Systematic finding: no state statute host is
  statically readable from this sandbox.
- **Discovery**: AGL search `school board district` surfaces official
  county/parish layers of the electoral districts in which school board
  members are elected — the "school board seats" as geography.

## Round 7 (school board districts)
- [x] **5 school-board-district files delivered** (47 features; 365
  total files):
  - `counties/fl/lee/school_board_districts_2025.geojson` — 5, per-member
    named (official Lee County FL GIS).
  - `counties/ga/forsyth/school_board_districts_2025.geojson` — 5
    (official Forsyth County GIS; 5-district board verified via Wikipedia).
  - `counties/la/st_mary/school_board_districts_2022.geojson` — 11, 2022
    adopted plan (11-district board verified on stmary.gov directory).
  - `counties/la/st_john_the_baptist/school_board_districts_2022.geojson`
    — 11, 2022 adopted plan (caveat: structure not independently verified).
  - `states/tx/state_board_of_education_districts_2021.geojson` — 15 TX
    SBOE electoral districts, 2021 redistricting (Texas Capitol Data
    Portal, via Bexar County's official AGL org).
- [x] **6 rejections documented** (manifest, disabled): Wake NC (9
  polygons vs 7-member WCPSS board — pre-2017 map), St. Charles LA (8
  blank polygons), 2× unlabeled unknown provenance, Peoria 150 IL (3 of 7
  districts), Hillsborough FL (WAF 400).
- [x] Catalog re-render (365 rows) + full verify.py run: **ALL GOOD** —
  365 files, 93,613 features, 0 geometry/catalog problems.

## Round 7 running totals
- **365 GeoJSON files, 2.2 GB** (round 5: 360).
- Local level: 32 city council + 10 county commission + 4 school board
  district files; +1 state SBOE electoral-district file.

## Round 8 (school board districts wave 2)
- [x] **5 more school-board files** (39 features; 370 total files):
  - `states/ks/state_board_of_education_districts_2025.geojson` — 10 KS
    SBOE electoral districts (official KansasGIS; 10-seat structure
    verified via Wikipedia).
  - `counties/ca/alameda/school_board_districts_2025.geojson` — 7 trustee
    areas 1st–7th (official Alameda County).
  - `counties/la/st_james/school_board_districts_2022.geojson` — 7, 2022
    adopted plan (verified on stjames.k12.la.us).
  - `counties/tn/davidson/school_board_districts_2022.geojson` — 9,
    "2022 School Board Districts" (official Nashville Open Data; 9-district
    board verified via Wikipedia).
  - `counties/ga/chatham/school_board_districts_2025.geojson` — 8
    Savannah-Chatham districts, per-member named (SAGIS official; 8-district
    board verified on sccpss.com).
- [x] Deferred to manifest (WAF 400, retry later): Santa Cruz, Kern,
  Riverside, San Bernardino, Santa Barbara (CA), Frederick (MD),
  Tuscaloosa (AL), Hillsborough (FL). Rejected: Orange CA OCDE (45
  polygons ≠ 12 trustees — not trustee areas), CCGIS2025 anonymous
  6-polygon WNC layer (unverifiable provenance).
- [x] Tooling: `fetch_arcgis.py` now URL-encodes service paths
  (parens in layer names); fixed a double-encode regression.
- [x] St. John the Baptist Parish structure still unverified (2010
  baseline WAF-blocked; parish sites unreachable) — caveat stands.
- [x] El Paso CO retry #5: still no JSON.
- [x] Catalog re-render (370 rows) + full verify.py run: **ALL GOOD** —
  370 files, 93,654 features, 0 geometry/catalog problems.

## Round 8 running totals
- **370 GeoJSON files, 2.2 GB** (round 7: 365).
- School-board-district coverage now: 9 files (FL/Lee, GA/Forsyth,
  GA/Chatham, LA/St. Mary, LA/St. James, LA/St. John the Baptist,
  TN/Davidson, CA/Alameda + TX & KS state SBOE).

## Round 9 (MD deep-dive + gap-city/county probes)
- [x] **+3 county commission files** (17 features; 373 total):
  - `counties/mn/dakota/county_commission_districts_2022.geojson` — 7
    districts (official Dakota County MN GIS, 2022 redistricting).
  - `counties/mn/scott/county_commission_districts_2020.geojson` — 5
    districts (official Scott County MN GIS).
  - `counties/ga/coweta/county_commission_districts_2025.geojson` — 5,
    per-commissioner named (official Coweta County GA account).
- [x] **MD legislative deep-dive**: TIGER's MD house file contains only
  71 of the 93 districts in effect (2012-2026 plan) — flagged in
  `CATALOG.csv`. The current/2022 maps are on the official MD Planning
  AGL org (`MD_Legislative_Districts_2022*`, `Senate_Only_Districts_2022`)
  but the org is WAF-throttling hard (400s on repeated probes); CBF's
  "2022" layers are the rejected lettered maps. MD replacement deferred.
- [x] Gap-city probes: Detroit "2026" layer = 3 super-ward polygons
  (proposed reform, rejected); Memphis 2023 official layer has only 7 of
  13 districts (rejected; DBO variant WAF-deferred); Philly 2024 official
  layer WAF-deferred; LA "CouncilDistricts2026" = 15 proposed districts
  named per candidate (rejected — not current 13); KC 2022 official
  layer WAF-deferred; Austin still nothing.
- [x] WAF-400 school-board retry batch: all 6 still persistently blocked
  (Santa Cruz/Kern/Santa Barbara CA, Frederick MD, Tuscaloosa AL,
  Hillsborough FL).
- [x] NH 400-district house: still not on AGL (2022 hits are Rhode
  Island's) — stays stale.
- [x] Catalog re-render (373 rows) + full verify.py run: **ALL GOOD** —
  373 files, 93,671 features, 0 geometry/catalog problems.

## Round 9 running totals
- **373 GeoJSON files, 2.2 GB** (round 8: 370).
- County commission files: 13 (10 + Dakota MN, Scott MN, Coweta GA).

## Next (round 10+)
- Retry the WAF-400 school-board layers (Santa Cruz/Kern/Riverside/SB/SB-
  county CA, Frederick MD, Tuscaloosa AL, Hillsborough FL); more AGL
  mining (other LA 2022 plans, IL/CO/PA school board districts).
- Per-district board-SEAT-COUNT CSVs (governance attribute) remain
  blocked on statute sources — see DEV.md; the district-geometry
  approach above is the practical path for "seats."
- Local-level gap-filling: New Orleans, Tampa, Milwaukee, Louisville,
  Cincinnati, OKC, San Jose, LV; retries (WAF-deferred): Philly 2024, KC
  2022, Memphis DBO, Aitkin MN, El Paso CO. More county coverage (SC/NC/
  IL district-based boards; FL beyond Lee/Collier).
- MD replacement: retry mdplanning AGL org when the WAF eases
  (`MD_Legislative_Districts_2022`, 105/51 plan effective 2026); the
  71/93-district TIGER house file is flagged incomplete in the catalog.
- El Paso County (CO): retry (ArcGIS service intermittently loses layers).
- MD/NH/VT legislative: replace stale Census maps when a current
  state/ArcGIS source is found.
- Tighten `lines_last_redrawn` per state (confirm 2025-26 special cases).

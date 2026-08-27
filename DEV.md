# DEV — notes for future agents working on this repository

## What this repo is

A repository of current U.S. political-geography boundary files (GeoJSON
preferred), organized `locale / geography-type`, with per-folder READMEs and a
master `CATALOG.csv`.

## Source inventory (verified 2026-08-27)

### Census TIGER/Line — primary source
Base URL pattern: `https://www2.census.gov/geo/tiger/TIGER{YYYY}/{LAYER}/`

| Layer | URL folder (2025 release) | Coverage | Use for |
|---|---|---|---|
| Congressional districts, 119th | `TIGER2025/CD/tl_2025_{FIPS}_cd119.zip` | 50 states + DC + PR + AS/GU/MP/VI | national congress districts (merged) |
| State boundaries | `TIGER2025/STATE/tl_2025_us_state.zip` | 56 (50+DC+PR+terr.) | states, **US Senate districts** (1 state = 1 senate district) |
| County boundaries | `TIGER2025/COUNTY/tl_2025_us_county.zip` | 3,235 | counties baseline |
| State legislative (lower) | `TIGER2025/SLDL/tl_2025_{FIPS}_sldl.zip` | 49 states (no DC, no NE) | state house districts |
| State legislative (upper) | `TIGER2025/SLDU/tl_2025_{FIPS}_sldu.zip` | 50 states | state senate districts (NE = unicameral) |
| Community school districts | `TIGER2025/SCSD/tl_2025_{FIPS}_scsd.zip` | 19 states only (04,06,09,13,17,21,23,25,27,30,33,34,36,41,44,47,48,50,55) | school district baseline (partial) |
| Cartographic boundaries (simplified) | `GENZ2025/shp/cb_2025_us_{state,county,place}_...zip` | national, simplified 500k/5m/20m | lightweight baselines if needed |

Notes:
- TIGER/Line is the authoritative federal source; it bakes in current
  redistricting (verified: TX `cd119` has 38 districts after the 2025
  mid-decade special redistricting — the 2022 cycle had 35).
- Nebraska is unicameral → SLDU file is *the* legislature; SLDL does not
  exist for FIPS 31.
- DC (FIPS 11) has no state legislature; it does have a congressional district
  (non-voting) — included in the national CD merge.
- **Not available in 2025**: `SDUL` (unified), `SDHL` (high school),
  `SDSD` (elementary) school district layers — the 2025 release has none, and
  GENZ`{year}`/schooldist is gone (404). For full school-district coverage we
  need per-state sources (see Open questions).
- TIGER attribute names: `GEOID`, `NAMELSAD`, `LSAD`, `SLDLNAME`/`SLDULNAME`,
  `CD119FP`, `ALAND`, `AWATER`, etc. Keep them as-is in our files.

### TIGERweb ArcGIS REST (GeoJSON directly)
`https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/MapServer/layers`
exists but returned non-JSON in quick tests — treat as unverified fallback.
The zips above are more reliable.

### Reference data (round 3)
`en.wikipedia.org` IS reachable from this sandbox (curl + python). The
wikitext of "List of U.S. state legislatures" (via
`/w/api.php?action=parse&page=...&prop=wikitext&format=json`) gives a
per-state current lower/upper chamber size table — used for the round-3
legislative cross-check. Note the table's "Size" column = SEAT counts, not
district-polygon counts (multi-member districts — see the cross-check
section below).

### School districts (built — round 1)
TIGER2025 has FOUR school-district layers (discovered by listing
`TIGER2025/` root):
| Layer | Meaning | Coverage | Our file (per state) |
|---|---|---|---|
| `UNSD` | Unified (K-12) school district | ALL 56 jurisdictions | `states/<ab>/school_districts/unified_school_districts_2025.geojson` |
| `ELSD` | Elementary school district | 25 states | `.../elementary_school_districts_2025.geojson` |
| `SCSD` | Community school district | 19 states | `.../community_school_districts_2025.geojson` |
| `SDADM` | State-administered school district | national (1 file) | `us/school_districts/state_administered_school_districts_2025.geojson` |
UNSD/ELSD/SCSD carry `LOGRADE`/`HIGRADE`/`SDTYP`/`NAME` attributes — school
districts with grade spans and names. A state may have overlapping types
(e.g. CA has both UNSD and ELSD; MT/VT/NH/RI have many small SCSDs).
"School board seats" are NOT districts — see the dedicated research section
below (round 4) for the source audit and a concrete recommendation.

### School board seats — source audit & recommendation (round 4)
"School board seats" (number of board members per district) is a
**governance attribute, not a shape**. There is NO national shapefile for
it. A round-4 audit probed 10+ sources; none gives a current, structured,
per-district board-seat count from the reachable hosts:
- **Census API** (`api.census.gov/data/{yr}`): no school_board dataset;
  the `school_district` variables endpoint 404s. Board size is in no
  Census/ACS/TIGER layer.
- **NCES SLFS/SDF** (national district finance files, reachable at
  `nces.ed.gov/ccd/data/`): `sdf23_1a_layout.txt` (FY2023, 19,570 LEAs,
  353 vars) and `slfs17_1a_layout.txt` grepped — **no board /
  member-count variable** (only FALL MEMBERSHIP = enrollment). The
  national CCD public files do NOT carry board size.
- **NCES district profile** (`nces.ed.gov/ccd/districtprofile/`): old
  per-district profile pages (which showed board composition) are 404;
  the replacement is the JS-only Data Lab — not scriptable here.
- **State portals**: `data.texas.gov` (Socrata, reachable) has NO
  school-board-size dataset (catalog searched). `txschools.gov` /
  `rptcard.texas.gov` 000; `tea.texas.gov` pages are JS SPAs with no
  static data URLs. `cde.ca.gov` (CA) reachable but API JS-gated.
  `gadoe.org` (GA) reachable but `files.gadoe.org` 000s. `fldoe.org`
  403, `myflorida.gov/portal` 000, `ncportal.ncdpi.nc.gov` /
  `nysed.gov` 000.
- **Wikipedia "List of school districts in {state}"**: district name/
  county lists only — no board-size column (checked FL, 94-line article).
- **ICPSR / NCES PPSDC public-use microdata** (has board-size vars):
  `icpsr.umich.edu` 403s (auth-gated).

**Recommendation for a future round** (if board seats are needed):
build a **per-district enrichment CSV, not a shapefile**:
`data/states/<ab>/school_board_seats/school_board_seats_<vintage>.csv`
with columns `nces_leaid, census_pid, district_name, board_seats,
election_type, source, as_of`. Most states set board size **statutorily
by enrollment bracket** (FL, GA, NJ, PA, ...), so the reliable method is:
join our existing UNSD geometry (carries `GEOID`/`PID`) to current
enrollment + the state's statutory bracket. The real work is a
state-by-state table of bracket rules + a reachable current-enrollment
source per state. If only a **state-level** "board of education seats"
(state SBOE, not per-district local boards) is acceptable, that's much
easier (stable size per state; Wikipedia board articles) — confirm which
level the requester wants before investing.

### State legislative data caveats (round 1 verification)
- Census SLDL/SLDU files include a residual **"State ... Districts not
  defined"** feature in some states (e.g. CT, NH) for tiny unassigned areas.
  Real district count = feature count − undefined features. E.g. CT house:
  152 features = 151 real + 1 undefined ✓ (CT House = 151).
- **NH house anomaly**: TIGER gives 165 features (164 real) but the NH House
  has 400 single-member districts (numbered by county). The Census-published
  NH map appears to predate/omit NH's current per-county districting — treat
  NH house districts as "Census-published; verify against state legislature
  GIS before relying on them." Spot-check other states' counts against the
  state's own published chamber sizes if precision matters.
  **Done in round 3** — full 50-state cross-check, see "State legislative
  count cross-check (round 3)" below. Key result: TIGER matches current
  plans everywhere except MD (stale pre-2022 map), NH (house), VT (senate
  count); multi-member-district states need district-to-seat conversion.
- Texas SLDL/SLDU in TIGER2025 show 150/31 (2022-cycle counts) → the 2025 TX
  special redistricting (SB1) was congressional only; state legislative lines
  = 2022 cycle for all 50 states in this vintage.
- Puerto Rico has its own legislature (41 house / 9 senate) — included.
  Territories (AS/GU/MP/VI) have no state legislature (TIGER 404s, skipped).

### Municipal & county context layers (pulled in round 2)
- `TIGER2025/PLACE` — incorporated places (cities/towns), all 56
  jurisdictions → `states/<ab>/municipalities/municipal_boundaries_2025.geojson`.
  Good context layer; does NOT contain council districts.
- `TIGER2025/COUSUB` — county subdivisions (civil townships, towns,
  municipalities that are county subdivisions), all 56 jurisdictions →
  `states/<ab>/county_subdivisions/county_subdivisions_2025.geojson`.
  Note: a municipality appears in PLACE if incorporated, in COUSUB if it's
  a civil subdivision of the county (e.g. civil townships in OH/MI/PA/IL),
  in neither if it's an incorporated place that is NOT a county subdivision
  (common in TX/FL/CA). The two layers together ≈ full municipal coverage.

### Local level — city council + county commission (built in round 2)

**There is no national source.** The pipeline is:
1. `tools/portal_council.py` — bulk ArcGIS Online search
   (`www.arcgis.com/sharing/rest/search?f=json&q="city" AND "council district"`,
   num=15) filtered to Feature/Map Services whose title contains
   "council"/"ward" and whose host is reachable from this sandbox; each
   candidate is probed with `GET {service}/0?f=json`.
2. Curate the hits into `tools/arcgis_manifest.json` (one entry per
   locale/geography-type). **Curation rules** (learned the hard way):
   - Prefer the city/county's OWN ArcGIS organization (owner names like
     `City_of_Phoenix`, `SeattleData`, `CharlotteNC`, `IndyGIS`,
     `ColumbusOhioGIS`) over personal/university copies.
   - ALWAYS probe and check the attribute values, not just the count.
     Many AGL copies are stale or partial: e.g. a "Kansas City" layer with
     districts {1,2,5,6,8,9} (3,4,7 missing), a "Wake County" layer mixing
     current + former commissioner polygons, a "Broward" layer with 9
     per-member polygons incl. 2 ex-commissioners, a "Maine statewide"
     layer that only covered 2 counties.
   - Feature counts include at-large (county/citywide) polygons — e.g.
     Fort Worth 12 = 8 districts + 4 at-large. Don't treat a count
     mismatch as an error; check the geometry/names instead.
   - Set `"enabled": false` for rejected candidates (with reason in
     `description`) rather than deleting them — the research record
     belongs in the manifest.
3. `tools/fetch_arcgis.py` — fetches each enabled entry via
   `{service}/{layer}/query?where=1=1&f=geojson&outSR=4326`
   (paginated by `maxRecordCount`), saves
   `data/<locale>/<geography_type>/<geography_type>_<vintage>.geojson`
   and upserts the catalog. Supports `"layers": [a,b,c]` to merge several
   MapServer layers into one file (El Paso County CO uses 5).

**Reachable vs unreachable ArcGIS hosts (from this sandbox):**
- Reachable: `www.arcgis.com`, `services{1..9}.arcgis.com`,
  `services.arcgis.com` (unnumbered — occasionally 400s, retry works),
  `tiles.arcgis.com`, `maps.bexar.org`, `maps.co.palm-beach.fl.us`.
- Unreachable/timeout: `gis.lacity.org`, `maps.nola.gov`,
  `data.chicago.gov` (Socrata), `data.detroitmi.gov`, `data.phila.gov`,
  `lgis.texas.gov`, `maps.raleighnc.gov`, `gis.tampagov.net`.
- 499 "Token Required" (SB_0005/GWM_0003) = token-gated; skip (e.g.
  Harris H-Tx `CommPrecinct`, Charlotte `SOTC_..._2017`).
- Some services are registered in AGL but have zero layers (Grant Co WA,
  Forsyth Co GA) or their MapServer layers reject all queries (Palm Beach
  Co FL open-data layer 4). Check before trusting a URL.

**Gaps left for future rounds** (official sources unreachable or AGL
copies bad): Detroit (17-district map not on AGL), New Orleans (40
districts; AGL copies are 5-group or ward-based), Philadelphia (17;
official phl.data "Districts" layer is 10 unnamed polys), Kansas City MO
(8; AGL copies missing 3), Memphis (15; DBO layer has 7), Los Angeles
(13; maps.lacity.org unreachable; only academic copies), Austin,
Tampa, Milwaukee, Louisville, Cincinnati, Oklahoma City, San Francisco,
Raleigh, San Jose, Las Vegas. County gaps (round 3 findings): no Maine
statewide (partial service); FL beyond Lee/Collier (both verified
district-based; Broward AGL copies all stale — per-member polygons);
TX beyond Harris/Bexar/Galveston (Dallas + Tarrant official maps are on
unreachable hosts; most other TX boards are at-large or MUD "precincts"
— not commissioner districts); CA boards are all at-large (no districts);
OH/WA/MO/VA/PA boards mostly at-large. NC/SC/MN have several
district-based boards worth more mining (Pender NC, Sumter SC,
Mecklenburg NC added in round 3; Guilford NC AGL layer = 8 polygons vs
5-seat board → rejected; Cobb Co GA AGL layer = 4 unnamed polys vs 5
districts → rejected).

**Naming note**: county files use the redistricting year as vintage where
known (e.g. Galveston/Bexar precinct maps date to the 2000s and are
stable since; verify per county). City files use the map year.

## Pipeline & tooling

- `tools/shp2geojson.py` — pure-Python (pyshp) shp/zip → GeoJSON. No GDAL in
  this environment; do not install system packages. Rings are re-oriented so
  the largest-area ring of each polygon comes first; holes grouped by
  point-in-ring test.
- `tools/fetch_tiger.py` — jobs: `NATIONAL`, `STATE_LEG`, `SCHOOLDIST`,
  `CONTEXT` (PLACE + COUSUB for all 56 jurisdictions; idempotent).
  Idempotent: uses `/tmp` zips + a per-state parts cache at
  `.tools/cache/cd119/`. Catalog rows upsert into `.tools/catalog.json`.
- `tools/portal_council.py` — ArcGIS Online discovery for city council
  district services (bulk search + reachability probe). Output: TSV of
  verified-reachable candidates to `/tmp`.
- `tools/portal_search.py` — general AQL + Socrata catalog search helper.
- `tools/fetch_arcgis.py` — fetches curated ArcGIS REST services from
  `tools/arcgis_manifest.json` (see "Local level" section above). Use
  `--probe` to check counts without writing; `--only ID...` for subsets.
- `tools/make_catalog.py` — renders `CATALOG.csv` + per-folder `README.md`
  from `.tools/catalog.json`. Run after every fetch.
- `tools/verify.py` (round 4) — repo-wide QA: parses every GeoJSON,
  checks CRS84, closed rings, finite in-bounds coordinates, and catalog
  ↔ disk consistency; prints per-type feature totals. Run after any bulk
  change: `.tools/venv/bin/python tools/verify.py` (subset arg optional).
  Exit 0 = clean.
- Run everything with `.tools/venv/bin/python` (pyshp installed there).

## Gotchas (learned the hard way)

1. **census.gov is Akamai-fronted**: bursts of requests get HTTP 200 with a
   600-byte "Request Rejected" HTML page instead of the zip. `http_get`
   validates the `PK` zip magic, paces ~0.4s between requests, and backs off
   on failure. If you add new fetch loops, reuse `http_get`.
2. **TIGER zip internal names differ from the zip filename** — e.g.
   `tl_2025_48_cd119.zip` contains `tl_2025_48_cd119.shp` (same base), but do
   not assume the zip basename; resolve the `.shp` inside the archive
   (`shp2geojson.py` does this).
3. **PEP 668**: system Python refuses `pip --user`. Use `.tools/venv`.
4. **pyshp API**: `Reader.fields` already excludes `DeletionFlag` /
   `Shape__Length`; `iterShapeRecords()` yields `(shape, record)` — field
   names come from `sf.fields`, not the record.
5. **Nebraska / DC special cases** handled in `fetch_tiger.py`; keep them if
   you refactor.
6. Landlock sandbox gives partial enforcement here; temp files go under
   `/tmp` and the workspace. Keep scratch in `/tmp`, durable artifacts in the
   repo.

## Conventions

- File naming: `<geography_type>_<vintage>.geojson`; vintage = year or
  Congress session the lines apply to (NOT download date).
- All files WGS84 (CRS84).
- `CATALOG.csv` is generated; `.tools/catalog.json` is the source of truth.
- `missing_on_disk=yes` in CATALOG.csv means the entry has no file — fix or
  remove it; it should normally be empty.
- One `README.md` per data folder (auto-generated, do not hand-edit).

## State legislative count cross-check (round 3, verified vs Wikipedia chamber table)

TIGER/Line SLDL/SLDU files contain **district polygons**, not seats — for
multi-member districts the feature count is smaller than the chamber size.
Full cross-check of all 50 states + NE + PR against the current chamber
sizes (Wikipedia "List of U.S. state legislatures", which reflects the 2022
redistricting cycle) — results:

- **Match (seat count = district count, single-member districts):** AL 105/35,
  AK 40/20, CA 80/40, CO 65/35, CT 151/36 (+1 residual each), DE 41/21, FL 120/40,
  GA 180/56, IL 118/59 (+1 residual each), IN 100/50, IA 100/50, KS 125/40,
  LA 105/39 (+1 residual), MA 160/40 (+1 residual), MI 110/38, MN 134/67,
  MS 122/52, MO 163/34, MT 100/50, NM 70/42, NY 150/63, NC 120/50, OH 99/33,
  OK 101/48, OR 60/30, PA 203/50, RI 75/38, SC 124/46, TN 99/33, TX 150/31,
  UT 75/29, VA 100/40, WA 98/49, WI 99/33 (+1 residual each), WY 62/31,
  NE 49 (unicameral), PR 41/9.
- **Multi-member districts (TIGER is correct; seats = districts × members):**
  AZ house 30 two-member districts = 60 seats; ND house 47 two-member = 94
  seats (+1 residual); SD house 35 two-member = 70 seats (+2 extra polygons,
  names 1-35 all present); ID house 35 two-member = 70 seats; WV senate 17
  two-member = 34 seats; NJ house 40 three-member Assembly districts = 120
  seats (senate 40 single-member).
- **STALE — TIGER2025 does not reflect the 2022 plan (verify/follow up):**
  - **MD**: TIGER shows the pre-2022 map (71 house districts / 47 senate);
    Maryland's enacted 2022 plan is 105/51. The 2022 map is NOT in
    TIGER2025. Flag: re-pull when Census updates, or source from the state.
    Round-4 attempt: AGL host `gis.cbf.org` (CBF_GIS "MD_GeneralAssembly_2022"
    MapServer) is reachable per-layer but carries the OLD lettered district
    style (1A/1B/1C, 67 distinct values) — data is pre-2022 despite the
    service name; REJECTED (do not re-fetch).
  - **NH**: house file has 164 districts + 1 "not defined"; NH's actual
    House has 400 single-member districts (enacted 2022). TIGER2025 NH SLDL
    is not the current map. (Senate 24+1 is consistent.)
  - **VT**: house 109 districts (mixed 1/2-member for 150 seats — plausible),
    senate 16 features vs. 13 seats — likely extra polygons; verify.
- Residual "State ... Districts not defined" features: CT (+1/+1), WI (+1/+1),
  NH (+1/+1), LA house (+1), ME senate (+1), SD house (+2 unnamed), HI (+1/+1
  vs 50/20 convention — TIGER 51/25 is the enacted 2022 plan).

## Version control policy (round 5)
- `git init` done (branch `main`); `.gitignore` excludes `data/` (2.2 GB
  GeoJSON), `.tools/venv/`, and `.tools/cache/`. Tracked: all docs
  (README/TASKS/PROGRESS/DEV), `tools/*.py`, `tools/arcgis_manifest.json`,
  `CATALOG.csv`, `.tools/catalog.json` (the catalog source of truth).
- **data/ is reproducible, not archived, in git**: every file can be
  re-fetched with `tools/fetch_tiger.py` (Census TIGER2025) and
  `tools/fetch_arcgis.py` (manifest-driven). If a remote is added later
  and the data must be versioned, install `git-lfs` and add
  `data/**/*.geojson filter=lfs diff=lfs merge=lfs -text` to
  `.gitattributes` — but do NOT commit the raw 2.2 GB without LFS.
- Commit convention: one commit per round of work; message starts with
  the round (e.g. "Round 5: +4 city files, git policy").

## Open questions / decisions for future rounds

- Vintage semantics: for state legislative files we currently say
  "2022 cycle (effective 2024); verify per-state vintage." Confirm per-state
  redistricting years (esp. 2025-26 mid-decade special cases) and tighten the
  `lines_last_redrawn` column.
- Should we keep per-state congressional district files under
  `states/<ab>/congress_districts/` as well (convenience copies)? Decision:
  default no, unless a downstream need appears (keeps catalog DRY).
- City council + county commission: decide pilot metros/counties to stand up
  the local-level pattern before scaling (see TASKS.md round 2+).
- Size: TIGER full-resolution files are large (counties 20MB+). We keep
  full-resolution TIGER by default; consider offering simplified
  cartographic (`GENZ2025/shp`) variants for large files if the repo bloats.

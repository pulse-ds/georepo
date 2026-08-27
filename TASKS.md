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
- [~] Catalog re-render (360 rows) + full verify.py run (background).

## Round 6+ (gap-filling & polish)
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

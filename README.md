# US Political Geography Shape File Repository

A repository of the most current U.S. political-geography boundary files,
preferably in GeoJSON format, organized by locale (national → state →
municipal) and then by geography type.

## Coverage (current)

| Locale | Geography type | Status |
|---|---|---|
| National | U.S. Senate districts (= state boundaries) | done |
| National | U.S. House (congressional) districts, 119th Congress 2025–26 | done |
| National | State boundaries | done |
| National | County boundaries | done |
| National | State-administered school districts | done (TIGER SDADM) |
| States (50) | State senate (upper chamber) districts | done (TIGER SLDU) |
| States (49) | State house (lower chamber) districts | done (TIGER SLDL; NE is unicameral) |
| States (56) | Unified (K-12) school district boundaries | done (TIGER UNSD) |
| States (25) | Elementary school district boundaries | done (TIGER ELSD) |
| States (19) | Community school district boundaries | done (TIGER SCSD) |
| States (56) | Municipal (incorporated place) boundaries | done (TIGER PLACE) |
| States (56) | County subdivision boundaries | done (TIGER COUSUB) |
| Cities (32) | City council districts | done (official city GIS / AGL) |
| Counties (13) | County commission / equivalent districts | done (pilot; many counties at-large) |
| Counties (8) | School board electoral districts | done (pilot: FL/Lee, GA/Forsyth, GA/Chatham, LA×3, TN/Davidson, CA/Alameda) |
| States (2) | State board of education electoral districts | done (TX SBOE 2021, KS SBOE) |

Current totals: **373 GeoJSON files, 2.2 GB** — all WGS84, all validated
(see `CATALOG.csv`). Local-level coverage is a growing pilot: 32 city
council files + 13 county commission files + 10 school-board-district
files, with a curated manifest of additional reachable sources and a
documented gap list (see DEV.md).

## Layout

```
data/
  us/                          # national level
    senate_districts/
    congress_districts/
    states/
    counties/
  states/
    <2-letter-abbv>/           # one folder per state (al, ca, tx, ...)
      state_senate_districts/
      state_house_districts/
      school_districts/
      municipalities/          # TIGER PLACE (incorporated places)
      county_subdivisions/     # TIGER COUSUB
  counties/
    <2-letter-abbv>/<county>/  # one folder per county
      county_commission_districts/
  cities/
    <2-letter-abbv>/<city>/    # one folder per city
      city_council_districts/
```

File naming convention: `<geography_type>_<vintage>.geojson` where vintage is
the year (or Congress session, e.g. `119th`) the district lines apply to.

Every file is WGS84 (EPSG:4326 / CRS84) GeoJSON and retains the source's
original attribute table (e.g. TIGER `GEOID`, `NAMELSAD`, `SLDLNAME`).

## Master catalog

`CATALOG.csv` lists every file: folder, filename, description, source,
source URL, publication vintage, when the district lines were last redrawn,
and feature count. Each folder also has an auto-generated `README.md`.
Rebuild after any fetch: `python3 tools/make_catalog.py`.

## Data sources

Primary: **U.S. Census Bureau TIGER/Line program** (see [DEV.md](DEV.md) for
exact URLs, vintage semantics, and known gaps). State-level GIS programs and
municipal open-data portals are used for the local level (in progress).

## Tools

- `tools/shp2geojson.py` — pure-Python (pyshp) shapefile → GeoJSON converter
- `tools/fetch_tiger.py` — batch fetch + convert + catalog for Census TIGER
- `tools/make_catalog.py` — renders `CATALOG.csv` and per-folder READMEs
- `tools/verify.py` — repo-wide QA (parse, CRS84, closed rings, in-bounds
  coordinates, catalog↔disk consistency): `python3 tools/verify.py`
- Python env with `pyshp`: `.tools/venv` (create with
  `python3 -m venv .tools/venv && .tools/venv/bin/pip install pyshp`)

## Maintenance tasks

See [TASKS.md](TASKS.md) for the task list, [PROGRESS.md](PROGRESS.md) for
progress, and [DEV.md](DEV.md) for notes that should inform future work on
this repository.

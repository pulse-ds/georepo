#!/usr/bin/env python3
"""Fetch U.S. political-geography shapefiles from the Census Bureau TIGER/Line
program, convert them to GeoJSON, place them in the repository layout, and
record catalog metadata.

Usage:
    fetch_tiger.py --job NATIONAL        # states, counties, congress, senate
    fetch_tiger.py --job STATE_LEG       # state legislative districts, all states
    fetch_tiger.py --job SCHOOLDIST      # community school districts (SCSD)
    fetch_tiger.py --job <name> ...      # repeatable
    fetch_tiger.py --list                # show available jobs

Outputs land under data/ (see DEV.md for layout). Catalog entries are
upserted into .tools/catalog.json as JSON objects; run tools/make_catalog.py
to render CATALOG.csv.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
CATALOG_JSON = os.path.join(ROOT, ".tools", "catalog.json")
PY = sys.executable
SH2G = os.path.join(HERE, "shp2geojson.py")

TIGER = "https://www2.census.gov/geo/tiger/TIGER2025"
SRC_NAME = "U.S. Census Bureau TIGER/Line"

# FIPS -> (abbr, name)
STATES = {
    "01": ("al", "Alabama"), "02": ("ak", "Alaska"), "04": ("az", "Arizona"),
    "05": ("ar", "Arkansas"), "06": ("ca", "California"), "08": ("co", "Colorado"),
    "09": ("ct", "Connecticut"), "10": ("de", "Delaware"), "11": ("dc", "District of Columbia"),
    "12": ("fl", "Florida"), "13": ("ga", "Georgia"), "15": ("hi", "Hawaii"),
    "16": ("id", "Idaho"), "17": ("il", "Illinois"), "18": ("in", "Indiana"),
    "19": ("ia", "Iowa"), "20": ("ks", "Kansas"), "21": ("ky", "Kentucky"),
    "22": ("la", "Louisiana"), "23": ("me", "Maine"), "24": ("md", "Maryland"),
    "25": ("ma", "Massachusetts"), "26": ("mi", "Michigan"), "27": ("mn", "Minnesota"),
    "28": ("ms", "Mississippi"), "29": ("mo", "Missouri"), "30": ("mt", "Montana"),
    "31": ("ne", "Nebraska"), "32": ("nv", "Nevada"), "33": ("nh", "New Hampshire"),
    "34": ("nj", "New Jersey"), "35": ("nm", "New Mexico"), "36": ("ny", "New York"),
    "37": ("nc", "North Carolina"), "38": ("nd", "North Dakota"), "39": ("oh", "Ohio"),
    "40": ("ok", "Oklahoma"), "41": ("or", "Oregon"), "42": ("pa", "Pennsylvania"),
    "44": ("ri", "Rhode Island"), "45": ("sc", "South Carolina"), "46": ("sd", "South Dakota"),
    "47": ("tn", "Tennessee"), "48": ("tx", "Texas"), "49": ("ut", "Utah"),
    "50": ("vt", "Vermont"), "51": ("va", "Virginia"), "53": ("wa", "Washington"),
    "54": ("wv", "West Virginia"), "55": ("wi", "Wisconsin"), "56": ("wy", "Wyoming"),
    # non-voting delegations
    "60": ("as", "American Samoa"), "66": ("gu", "Guam"), "69": ("mp", "Northern Mariana Islands"),
    "72": ("pr", "Puerto Rico"), "78": ("vi", "U.S. Virgin Islands"),
}
CONTIG_50_DC = [k for k, (a, n) in STATES.items() if k <= "56"]
SCHOOLDIST_STATES = ["04", "06", "09", "13", "17", "21", "23", "25", "27", "30",
                     "33", "34", "36", "41", "44", "47", "48", "50", "55"]
ELSD_STATES = ["04", "06", "09", "13", "17", "21", "23", "25", "26", "27", "29",
               "30", "33", "34", "36", "38", "40", "41", "44", "47", "48", "50",
               "51", "55", "56"]


def log(msg):
    print(f"[fetch_tiger] {msg}", flush=True)


_last_download = [0.0]


def http_get(url, dest, retries=5):
    """Download url to dest. Validates zip magic bytes (census.gov's WAF
    sometimes answers 200 with a small 'Request Rejected' HTML page; a
    poisoned edge-cache entry is worked around with a ?cb=N cache buster)."""
    for i in range(retries):
        attempt_url = url if i == 0 else (
            f"{url}{'&' if '?' in url else '?'}cb={i}")
        # polite pacing between requests
        wait = 0.4 - (time.time() - _last_download[0])
        if wait > 0:
            time.sleep(wait)
        try:
            req = urllib.request.Request(attempt_url, headers={"User-Agent": "georepository/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
                shutil.copyfileobj(r, f)
            _last_download[0] = time.time()
            with open(dest, "rb") as f:
                if f.read(2) == b"PK":
                    return dest
            log(f"bad payload (not a zip) for {url}; retrying")
            os.remove(dest)
        except Exception as e:
            log(f"retry {i + 1} after error: {e}")
            try:
                os.remove(dest)
            except FileNotFoundError:
                pass
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"failed to download {url} after {retries} attempts")


def convert_zip(zip_path, out_geojson):
    subprocess.run([PY, SH2G, zip_path, "-o", out_geojson], check=True,
                   stdout=subprocess.DEVNULL)
    with open(out_geojson, encoding="utf-8") as f:
        return json.load(f)


def upsert_catalog(folder, filename, **meta):
    os.makedirs(os.path.dirname(CATALOG_JSON), exist_ok=True)
    cat = {}
    if os.path.exists(CATALOG_JSON):
        with open(CATALOG_JSON, encoding="utf-8") as f:
            cat = json.load(f)
    key = f"{folder}/{filename}"
    entry = {"folder": folder, "filename": filename}
    entry.update(meta)
    cat[key] = entry
    with open(CATALOG_JSON, "w", encoding="utf-8") as f:
        json.dump(cat, f, indent=1, sort_keys=True)
    return entry


def job_national():
    jobs = []
    # States (baseline + U.S. Senate districts: each state = one Senate district)
    url = f"{TIGER}/STATE/tl_2025_us_state.zip"
    z = "/tmp/geo_state.zip"
    if not os.path.exists(z):
        http_get(url, z)
    for folder, fname, desc in [
        ("us/states", "state_boundaries_2025.geojson",
         "U.S. state boundaries (2025 vintage)."),
        ("us/senate_districts", "senate_districts_2025.geojson",
         "U.S. Senate districts: each of the 50 states is one Senate district "
         "(identical geometry to state boundaries)."),
    ]:
        out = os.path.join(DATA, folder, fname)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if os.path.exists(out):
            with open(out, encoding="utf-8") as f:
                n = len(json.load(f)["features"])
            log(f"{folder}/{fname}: cached, {n} features")
            continue
        fc = convert_zip(z, out)
        upsert_catalog(folder, fname, source=SRC_NAME, source_url=url,
                       published="2025 (TIGER 2025 release)",
                       lines_last_redrawn="n/a (state lines rarely change)",
                       features=len(fc["features"]),
                       description=desc)
        log(f"{folder}/{fname}: {len(fc['features'])} features")

    # Counties (baseline)
    url = f"{TIGER}/COUNTY/tl_2025_us_county.zip"
    z = "/tmp/geo_county.zip"
    if not os.path.exists(out := os.path.join(DATA, "us/counties", "county_boundaries_2025.geojson")):
        if not os.path.exists(z):
            http_get(url, z)
        fc = convert_zip(z, out)
        n = len(fc["features"])
        log(f"us/counties/county_boundaries_2025.geojson: {n} features")
    else:
        with open(out, encoding="utf-8") as f:
            n = len(json.load(f)["features"])
        log(f"us/counties/county_boundaries_2025.geojson: cached, {n} features")
    upsert_catalog("us/counties", "county_boundaries_2025.geojson", source=SRC_NAME,
                   source_url=url, published="2025 (TIGER 2025 release)",
                   lines_last_redrawn="n/a (county lines rarely change)",
                   features=n,
                   description="U.S. county boundaries (2025 vintage), national coverage.")

    # Congressional districts, 119th Congress: merge per-state zips
    folder, fname = "us/congress_districts", "congress_districts_119th_2025.geojson"
    out = os.path.join(DATA, folder, fname)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cache = os.path.join(ROOT, ".tools", "cache", "cd119")
    os.makedirs(cache, exist_ok=True)
    feats = []
    urls = []
    missing = []
    for fips in sorted(STATES):
        url = f"{TIGER}/CD/tl_2025_{fips}_cd119.zip"
        part = os.path.join(cache, f"cd119_{fips}.geojson")
        if not os.path.exists(part):
            z = f"/tmp/geo_cd_{fips}.zip"
            try:
                http_get(url, z)
            except Exception as e:
                log(f"SKIP CD {fips}: {e}")
                missing.append(fips)
                continue
            convert_zip(z, part)
            os.remove(z)
        with open(part, encoding="utf-8") as f:
            feats.extend(json.load(f)["features"])
        urls.append(url)
    if missing:
        log(f"CD MISSING (backfill later): {','.join(missing)}")
    coll = {"type": "FeatureCollection",
            "name": "congress_districts_119th_2025",
            "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
            "features": feats}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(coll, f, separators=(",", ":"), allow_nan=False)
    for fips in sorted(STATES):
        try:
            os.remove(f"/tmp/geo_cd_{fips}.zip")
        except FileNotFoundError:
            pass
    upsert_catalog(folder, fname, source=SRC_NAME,
                   source_url=f"{TIGER}/CD/  (per-state zips tl_2025_<FIPS>_cd119.zip, listing at this URL)",
                   published="2025 (TIGER 2025 release, 119th Congress)",
                   lines_last_redrawn="2022 regular cycle; TX redistricted 2025 (38 districts)",
                   features=len(feats),
                   description=("U.S. House of Representatives (Congressional) Districts, "
                                "119th Congress (2025-2026), all 50 states + DC + PR + "
                                "territorial delegations. Merged from per-state TIGER zips."))
    log(f"{folder}/{fname}: {len(feats)} features")


def job_state_leg():
    done = {"sldl": [], "sldu": []}
    for fips, (abbr, name) in sorted(STATES.items()):
        if fips == "11":  # DC has no state legislature
            continue
        for kind, dirn, ftype, label in [
            ("sldl", "state_house_districts", "SLDL (lower chamber)", "State house of representatives districts"),
            ("sldu", "state_senate_districts", "SLDU (upper chamber)", "State senate districts"),
        ]:
            if fips == "31" and kind == "sldl":
                continue  # Nebraska is unicameral
            if fips == "31" and kind == "sldu":
                dirn = "state_legislature_districts"
                label = "Nebraska unicameral legislature districts"
            url = f"{TIGER}/{kind.upper()}/tl_2025_{fips}_{kind}.zip"
            z = f"/tmp/geo_{kind}_{fips}.zip"
            try:
                http_get(url, z)
            except Exception as e:
                log(f"SKIP {kind} {fips}: {e}")
                continue
            folder = f"states/{abbr}/{dirn}"
            fname = f"{dirn.split('_')[0]}_{dirn.split('_')[1]}_districts_2025.geojson"
            out = os.path.join(DATA, folder, fname)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            fc = convert_zip(z, out)
            n = len(fc["features"])
            upsert_catalog(folder, fname, source=SRC_NAME, source_url=url,
                           published="2025 (TIGER 2025 release)",
                           lines_last_redrawn="2022 cycle (effective 2024); verify per-state vintage",
                           features=n,
                           description=f"{name}: {label}, TIGER {ftype}. {n} districts.")
            done[kind].append(f"{abbr}:{n}")
            log(f"{folder}/{fname}: {n} districts")
            os.remove(z)
    log(f"STATE_LEG done. SLDL {len(done['sldl'])}: " + ", ".join(done["sldl"]))
    log(f"STATE_LEG done. SLDU {len(done['sldu'])}: " + ", ".join(done["sldu"]))


def _schooldist_one(fips, layer, kind, fname, name):
    url = f"{TIGER}/{layer}/tl_2025_{fips}_{layer.lower()}.zip"
    z = f"/tmp/geo_{layer.lower()}_{fips}.zip"
    try:
        http_get(url, z)
    except Exception as e:
        log(f"SKIP {layer} {fips}: {e}")
        return
    folder = f"states/{STATES[fips][0]}/school_districts"
    out = os.path.join(DATA, folder, fname)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fc = convert_zip(z, out)
    n = len(fc["features"])
    upsert_catalog(folder, fname, source=SRC_NAME, source_url=url,
                   published="2025 (TIGER 2025 release)",
                   lines_last_redrawn="unknown (school district boundaries; Census vintage 2025)",
                   features=n,
                   description=f"{name}: {kind} boundaries (TIGER {layer}). {n} districts.")
    log(f"{folder}/{fname}: {n} districts")
    os.remove(z)


def job_schooldist():
    # Unified school districts (K-12): every jurisdiction has one
    for fips in sorted(STATES):
        abbr, name = STATES[fips]
        _schooldist_one(fips, "UNSD", "unified (K-12) school district",
                        "unified_school_districts_2025.geojson", name)
    # Elementary school districts: subset of states
    for fips in sorted(ELSD_STATES):
        abbr, name = STATES[fips]
        _schooldist_one(fips, "ELSD", "elementary school district",
                        "elementary_school_districts_2025.geojson", name)
    # Community school districts: subset of states
    for fips in SCHOOLDIST_STATES:
        abbr, name = STATES[fips]
        _schooldist_one(fips, "SCSD", "community school district",
                        "community_school_districts_2025.geojson", name)
    # State-administered school districts: national file
    url = f"{TIGER}/SDADM/tl_2025_50_sdadm.zip"
    z = "/tmp/geo_sdadm.zip"
    if not os.path.exists(z):
        http_get(url, z)
    folder, fname = "us/school_districts", "state_administered_school_districts_2025.geojson"
    out = os.path.join(DATA, folder, fname)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fc = convert_zip(z, out)
    n = len(fc["features"])
    upsert_catalog(folder, fname, source=SRC_NAME, source_url=url,
                   published="2025 (TIGER 2025 release)",
                   lines_last_redrawn="unknown (school district boundaries; Census vintage 2025)",
                   features=n,
                   description="State-administered school districts (TIGER SDADM), national coverage "
                               "(states/areas where the state, not a local district, administers schools).")
    log(f"{folder}/{fname}: {n} features")


def job_context():
    """Municipal + county-subdivision context layers (NOT council districts)."""
    for layer, fname, kind in [
        ("PLACE", "municipal_boundaries_2025.geojson",
         "incorporated places (cities/towns) boundaries"),
        ("COUSUB", "county_subdivisions_2025.geojson",
         "county subdivisions (civil townships, towns, municipalities) boundaries"),
    ]:
        for fips in sorted(STATES):
            abbr, name = STATES[fips]
            url = f"{TIGER}/{layer}/tl_2025_{fips}_{layer.lower()}.zip"
            z = f"/tmp/geo_{layer.lower()}_{fips}.zip"
            folder = f"states/{abbr}/municipalities" if layer == "PLACE" else \
                     f"states/{abbr}/county_subdivisions"
            out = os.path.join(DATA, folder, fname)
            if os.path.exists(out):
                continue
            try:
                http_get(url, z)
            except Exception as e:
                log(f"SKIP {layer} {fips}: {e}")
                continue
            os.makedirs(os.path.dirname(out), exist_ok=True)
            fc = convert_zip(z, out)
            n = len(fc["features"])
            upsert_catalog(folder, fname, source=SRC_NAME, source_url=url,
                           published="2025 (TIGER 2025 release)",
                           lines_last_redrawn="n/a (administrative boundaries)",
                           features=n,
                           description=f"{name}: {kind} (TIGER {layer}). "
                                       f"Context layer — does NOT include council "
                                       f"or commission district lines. {n} features.")
            log(f"{folder}/{fname}: {n} features")
            os.remove(z)


JOBS = {"NATIONAL": job_national, "STATE_LEG": job_state_leg, "SCHOOLDIST": job_schooldist,
        "CONTEXT": job_context}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", action="append", choices=sorted(JOBS))
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list:
        print("jobs:", ", ".join(sorted(JOBS)))
        return
    if not args.job:
        ap.error("no --job given")
    for j in args.job:
        log(f"=== job {j} ===")
        JOBS[j]()
    log("done")


if __name__ == "__main__":
    main()

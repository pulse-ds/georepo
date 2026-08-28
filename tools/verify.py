#!/usr/bin/env python3
"""verify.py — full-repo validation for the georepository.

Checks every data/**/*.geojson:
  1. parses as JSON and is a FeatureCollection
  2. CRS is WGS84/CRS84 (when a crs member is present)
  3. every feature has a geometry; all rings closed; coordinates
     numeric, finite, and within +-180 / +-90
Also cross-checks CATALOG.csv:
  4. every catalog row exists on disk (and no stale missing_on_disk=yes)
  5. every file on disk has a catalog row

Prints a per-geography-type feature summary + repo totals.
Exit code 0 = all good, 1 = problems found.

Usage:
    .tools/venv/bin/python tools/verify.py            # whole repo
    .tools/venv/bin/python tools/verify.py /states/md # path substring filter
"""
import csv
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CATALOG = os.path.join(ROOT, "CATALOG.csv")
EXPECTED_CRS = "urn:ogc:def:crs:OGC:1.3:CRS84"


def find_geojsons(subset=None):
    for dirpath, _dirs, names in os.walk(DATA):
        for n in sorted(names):
            if n.endswith(".geojson"):
                p = os.path.join(dirpath, n)
                if subset is None or subset in p:
                    yield p


def check_feature(ft, problems, i, allow_null_geom=False):
    if ft.get("type") != "Feature":
        problems.append(f"feature {i}: type {ft.get('type')!r}, not Feature")
    g = ft.get("geometry")
    if g is None:
        if not allow_null_geom:
            problems.append(f"feature {i}: null geometry")
        return

    def bad_coord(c, ctx):
        if not isinstance(c, (list, tuple)) or len(c) < 2:
            problems.append(f"{ctx}: bad coordinate {c!r}")
            return
        x, y = c[0], c[1]
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            problems.append(f"{ctx}: non-numeric coordinate {c!r}")
            return
        if math.isnan(x) or math.isnan(y):
            problems.append(f"{ctx}: NaN coordinate")
            return
        if not (-180.0 <= x <= 180.0 and -90.0 <= y <= 90.0):
            problems.append(f"{ctx}: coordinate out of bounds ({x}, {y})")

    def check_ring(ring, ctx):
        if not isinstance(ring, list) or not ring:
            problems.append(f"{ctx}: empty or non-list ring")
            return
        if ring[0] != ring[-1]:
            problems.append(f"{ctx}: ring not closed")
        for j, c in enumerate(ring):
            bad_coord(c, f"{ctx}[{j}]")

    def walk(gg, ctx):
        if not isinstance(gg, dict):
            problems.append(f"{ctx}: geometry node is {type(gg).__name__}, not object")
            return
        t = gg.get("type")
        c = gg.get("coordinates")
        if t == "Point":
            bad_coord(c, ctx)
        elif t == "LineString":
            check_ring(c, ctx)
        elif t == "Polygon":
            if not isinstance(c, list):
                problems.append(f"{ctx}: Polygon coordinates not a list")
            else:
                for j, ring in enumerate(c):
                    check_ring(ring, f"{ctx}.ring{j}")
        elif t == "MultiPolygon":
            if not isinstance(c, list):
                problems.append(f"{ctx}: MultiPolygon coordinates not a list")
            else:
                for j, poly in enumerate(c):
                    for k, ring in enumerate(poly or []):
                        check_ring(ring, f"{ctx}[{j}].ring{k}")
        elif t in ("MultiLineString", "MultiPoint"):
            if not isinstance(c, list):
                problems.append(f"{ctx}: {t} coordinates not a list")
            else:
                for j, sub in enumerate(c):
                    check_ring(sub, f"{ctx}[{j}]")
        elif t == "GeometryCollection":
            for j, sub in enumerate(c or []):
                walk(sub, f"{ctx}[{j}]")
        else:
            problems.append(f"{ctx}: unknown geometry type {t!r}")

    walk(g, f"feature {i}")


def main():
    subset = sys.argv[1] if len(sys.argv) > 1 else None
    files = list(find_geojsons(subset))

    bad_files = []
    total_features = 0
    by_type = {}

    for path in files:
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path, encoding="utf-8") as f:
                d = json.load(f)
        except Exception as e:
            bad_files.append((rel, [f"JSON parse error: {e}"]))
            continue
        problems = []
        if not isinstance(d, dict) or d.get("type") != "FeatureCollection":
            problems.append("top level is not a FeatureCollection")
        feats = d.get("features") if isinstance(d, dict) else None
        if not isinstance(feats, list):
            problems.append("features is not a list")
            feats = []
        crs = ((d.get("crs") or {}).get("properties") or {}).get("name")
        if crs is not None and crs != EXPECTED_CRS:
            problems.append(f"unexpected CRS {crs!r}")
        # Allow null geometry for county_commission_districts (at-large seats
        # have no polygon — e.g. Glynn GA 2 at-large + 5 districts = 7 features).
        allow_null = os.path.basename(os.path.dirname(path)) == "county_commission_districts"
        for i, ft in enumerate(feats):
            check_feature(ft, problems, i, allow_null_geom=allow_null)
        total_features += len(feats)
        etype = os.path.basename(os.path.dirname(path))
        by_type[etype] = by_type.get(etype, 0) + len(feats)
        if problems:
            bad_files.append((rel, problems[:10]))

    catalog_problems = []
    catalog_rows = 0
    catalog_keys = set()
    if os.path.exists(CATALOG):
        with open(CATALOG, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                catalog_rows += 1
                key = f"{row['folder']}/{row['filename']}"
                catalog_keys.add(key)
                p = os.path.join(ROOT, "data", row["folder"], row["filename"])
                if not os.path.exists(p):
                    catalog_problems.append(f"catalog row missing on disk: {key}")
                elif row.get("missing_on_disk") == "yes":
                    catalog_problems.append(f"stale missing_on_disk=yes: {key}")
    if subset is None:  # only meaningful for a full scan
        for path in files:
            key = os.path.relpath(path, DATA).replace(os.sep, "/")
            if key not in catalog_keys:
                catalog_problems.append(f"file on disk not in catalog: {key}")

    print(f"files checked:   {len(files)}")
    print(f"total features:  {total_features}")
    print("per geography type:")
    for k in sorted(by_type):
        print(f"   {k:36s} {by_type[k]:8d}")
    print(f"catalog rows:    {catalog_rows}")

    if bad_files:
        print(f"\nPROBLEMS IN {len(bad_files)} FILES:")
        for rel, probs in bad_files:
            print(f"  {rel}")
            for p in probs:
                print(f"    - {p}")
    if catalog_problems:
        print(f"\nCATALOG PROBLEMS ({len(catalog_problems)}):")
        for p in catalog_problems:
            print(f"  - {p}")

    if bad_files or catalog_problems:
        print("\nRESULT: FAIL")
        return 1
    print("\nRESULT: ALL GOOD")
    return 0


if __name__ == "__main__":
    sys.exit(main())

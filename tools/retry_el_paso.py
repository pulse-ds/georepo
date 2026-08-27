#!/usr/bin/env python3
"""Retry the flaky El Paso County (CO) ArcGIS service (layers 12-16)."""
import json
import os
import time
import urllib.request

BASE = "https://services3.arcgis.com/r1Gf4AJYRBIM0N25/arcgis/rest/services/Commissioner_Districts_Web_Map/MapServer"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "counties", "co", "el_paso", "county_commission_districts",
                   "county_commission_districts_2016.geojson")
CATALOG = os.path.join(ROOT, ".tools", "catalog.json")


def getj(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def main():
    ok = False
    for attempt in range(20):
        try:
            d = getj(BASE + "?f=json")
            ls = d.get("layers") or []
            if any(l["id"] == 12 for l in ls):
                ok = True
                print(f"root OK on attempt {attempt + 1}", flush=True)
                break
            print(f"attempt {attempt + 1}: root but no layers", flush=True)
        except Exception as e:
            print(f"attempt {attempt + 1}: {e}", flush=True)
        time.sleep(8)

    if not ok:
        print("GAVE UP - service still empty", flush=True)
        return

    feats = []
    for li in [12, 13, 14, 15, 16]:
        for a in range(6):
            try:
                d = getj(f"{BASE}/{li}/query?where=1%3D1&f=geojson&outSR=4326")
                feats.extend(d.get("features", []))
                print(f"layer {li}: {len(d.get('features', []))} features", flush=True)
                break
            except Exception as e:
                print(f"layer {li} attempt {a + 1}: {e}", flush=True)
                time.sleep(6)
        time.sleep(2)

    if len(feats) != 5:
        print(f"INCOMPLETE: {len(feats)}/5, NOT written", flush=True)
        return

    coll = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": feats,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(coll, f, separators=(",", ":"), allow_nan=False)
    cat = json.load(open(CATALOG))
    cat["counties/co/el_paso/county_commission_districts/county_commission_districts_2016.geojson"] = {
        "folder": "counties/co/el_paso/county_commission_districts",
        "filename": "county_commission_districts_2016.geojson",
        "source": "El Paso County, CO (official GIS)",
        "source_url": BASE,
        "published": "unknown",
        "lines_last_redrawn": "2016",
        "features": 5,
        "description": "El Paso County (CO) commissioner districts (5) - merged from layers 12-16 of the county web map service.",
    }
    json.dump(cat, open(CATALOG, "w"), indent=1, sort_keys=True)
    print("WROTE", OUT, flush=True)


if __name__ == "__main__":
    main()

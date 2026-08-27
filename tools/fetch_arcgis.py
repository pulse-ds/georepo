#!/usr/bin/env python3
"""Fetch boundary data from public ArcGIS REST services into the repository.

Companion to fetch_tiger.py for the local level (city council districts,
county commission districts, etc.). Reads tools/arcgis_manifest.json:

  [
    {
      "id": "tx/galveston/county_commission_districts",
      "locale": "counties/tx/galveston",
      "geography_type": "county_commission_districts",
      "vintage": "2025",
      "service": "https://services5.arcgis.com/.../FeatureServer",
      "layer": 0,
      "source": "Human-readable source name",
      "source_url": "https://... (portal page)",
      "published": "when the file was published (if known)",
      "lines_last_redrawn": "when the district lines were last redrawn",
      "expected": 4            (optional feature-count sanity check)
    }, ...
  ]

Usage:
    fetch_arcgis.py                # fetch all manifest entries
    fetch_arcgis.py --only ID...   # subset by id
    fetch_arcgis.py --probe        # probe entries, print counts, no writes

Outputs: data/<locale>/<geography_type>/<geography_type>_<vintage>.geojson
Catalog: upserted into .tools/catalog.json (render with make_catalog.py).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
CATALOG_JSON = os.path.join(ROOT, ".tools", "catalog.json")
MANIFEST = os.path.join(HERE, "arcgis_manifest.json")
PY = sys.executable
SH2G = os.path.join(HERE, "shp2geojson.py")

HDRS = {"User-Agent": "georepository/1.0"}


def log(msg):
    print(f"[fetch_arcgis] {msg}", flush=True)


def get(url, timeout=60, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=HDRS)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(2 * (i + 1))
    raise last


def norm_service(base):
    """URL-encode special chars (e.g. parens) in the service path."""
    p = urllib.parse.urlsplit(base)
    return urllib.parse.urlunsplit(
        (p.scheme, p.netloc, urllib.parse.quote(p.path, safe="/"), p.query, p.fragment)
    ).rstrip("/")


def layer_meta(base, layer=0):
    d = json.loads(get(f"{base.rstrip('/')}/{layer}?f=json", timeout=25))
    if "error" in d:
        raise RuntimeError(f"layer error: {d['error']}")
    return d


def fetch_layer_geojson(base, layer=0):
    """Fetch a full layer as a GeoJSON FeatureCollection (paginated)."""
    base = norm_service(base)
    meta = layer_meta(base, layer)
    max_records = meta.get("maxRecordCount") or 2000
    feats = []
    offset = 0
    while True:
        q = {
            "where": "1=1", "outFields": "*", "f": "geojson", "outSR": "4326",
            "resultOffset": str(offset), "resultRecordCount": str(max_records),
        }
        url = f"{base.rstrip('/')}/{layer}/query?" + urllib.parse.urlencode(q)
        d = json.loads(get(url, timeout=120))
        if "error" in d:
            raise RuntimeError(f"query error: {d['error']}")
        batch = d.get("features", [])
        feats.extend(batch)
        if len(batch) < max_records or offset + max_records > 200000:
            break
        offset += max_records
        time.sleep(0.5)
    coll = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": feats,
    }
    return coll, meta


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


def slug_locale(locale):
    return locale  # e.g. counties/tx/galveston or cities/il/chicago


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="fetch only these manifest ids")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()

    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)

    for e in manifest:
        if args.only and e["id"] not in args.only:
            continue
        if not e.get("enabled", True):
            log(f"SKIP (disabled) {e['id']}")
            continue
        etype, vintage = e["geography_type"], e["vintage"]
        folder = f"{slug_locale(e['locale'])}/{etype}"
        fname = f"{etype}_{vintage}.geojson"
        out = os.path.join(DATA, folder, fname)
        layer_ids = e.get("layers") or [e.get("layer", 0)]
        try:
            if len(layer_ids) == 1:
                coll, meta = fetch_layer_geojson(e["service"], layer_ids[0])
                layer_label = str(meta.get("name"))
            else:
                all_feats = []
                layer_label = " + ".join(str(l) for l in layer_ids)
                for li in layer_ids:
                    c, meta = fetch_layer_geojson(e["service"], li)
                    all_feats.extend(c["features"])
                    time.sleep(0.4)
                coll = {
                    "type": "FeatureCollection",
                    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
                    "features": all_feats,
                }
        except Exception as ex:
            log(f"FAIL {e['id']}: {ex}")
            continue
        n = len(coll["features"])
        exp = e.get("expected")
        status = "OK"
        if exp is not None and n != exp:
            status = f"WARN(count {n} != expected {exp})"
        log(f"{e['id']}: {n} features {status} (layer: {layer_label})")
        if args.probe:
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(coll, f, separators=(",", ":"), allow_nan=False)
        upsert_catalog(
            folder, fname,
            source=e.get("source", "Unknown"),
            source_url=e.get("source_url", e["service"]),
            published=e.get("published", "unknown"),
            lines_last_redrawn=e.get("lines_last_redrawn", "unknown"),
            features=n,
            description=e.get("description", f"{etype} ({vintage})."),
        )
    log("done")


if __name__ == "__main__":
    main()

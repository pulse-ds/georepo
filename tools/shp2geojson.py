#!/usr/bin/env python3
"""Convert an ESRI shapefile (or a zip containing one) to GeoJSON.

Pure Python (pyshp), no GDAL required. TIGER/Line files are WGS84 lon/lat.

Usage:
    shp2geojson.py ZIP_OR_DIR [-o OUT.geojson] [--keep-blobs]

If OUT is omitted, the .geojson sibling of the input (zip name minus .zip,
or shp name) is written next to the input.

Geometry types handled: Point, MultiPoint, PolyLine/MultiLineString,
PolyShape/MultiPolygon (rings reordered so the largest-area ring of each
polygon is first, per RFC 7946 orientation guidance).

Exit codes: 0 ok, 1 error.
"""
import argparse
import json
import math
import os
import sys
import zipfile
import tempfile

import shapefile  # pyshp


def _signed_area(ring):
    a = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i][0], ring[i][1]
        x2, y2 = ring[i + 1][0], ring[i + 1][1]
        a += x1 * y2 - x2 * y1
    return a / 2.0


def shape_to_geometry(shape):
    st = shape.shapeType
    pts = [[p[0], p[1]] for p in shape.points]
    if st == shapefile.POINT:
        return {"type": "Point", "coordinates": pts[0]}
    if st == shapefile.MULTIPOINT:
        return {"type": "MultiPoint", "coordinates": pts}
    if st in (shapefile.POLYLINE, shapefile.POLYGON):  # includes 3D/z/m variants
        parts = list(shape.parts) + [len(pts)]
        lines = [pts[a:b] for a, b in zip(parts[:-1], parts[1:])]
        if st == shapefile.POLYLINE:
            if len(lines) == 1:
                return {"type": "LineString", "coordinates": lines[0]}
            return {"type": "MultiLineString", "coordinates": lines}
        # Polygon: each part is a ring. Group rings into polygons: a ring
        # whose first point falls inside an existing shell becomes a hole.
        rings = [r for r in lines if len(r) >= 4]
        rings.sort(key=lambda r: abs(_signed_area(r)), reverse=True)
        polys = []  # list of lists of rings
        for ring in rings:
            placed = False
            for poly in polys:
                if _ring_in_ring(ring, poly[0]):
                    poly.append(ring)
                    placed = True
                    break
            if not placed:
                polys.append([ring])
        if len(polys) == 1:
            return {"type": "Polygon", "coordinates": polys[0]}
        return {"type": "MultiPolygon", "coordinates": polys}
    raise ValueError(f"unsupported shape type {st}")


def _ring_in_ring(ring, outer):
    """Ray-cast point-in-polygon for ring[0] against outer ring."""
    x, y = ring[0][0], ring[0][1]
    inside = False
    n = len(outer)
    j = n - 1
    for i in range(n):
        xi, yi = outer[i][0], outer[i][1]
        xj, yj = outer[j][0], outer[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def convert(shape_records, field_names):
    feats = []
    for sr in shape_records:
        shape_rec = sr.shape
        record = sr.record
        if shape_rec.shapeType == shapefile.NULL:
            continue
        props = {}
        for name, value in zip(field_names, record):
            # drop trailing padding on strings
            if isinstance(value, bytes):
                value = value.decode("utf-8", "replace").rstrip("\x00 ").rstrip()
            if isinstance(value, str):
                value = value.rstrip("\x00 ").rstrip()
            props[name] = value
        geom = shape_to_geometry(shape_rec)
        feats.append({"type": "Feature", "properties": props, "geometry": geom})
    return feats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="zip or directory containing .shp")
    ap.add_argument("-o", "--out", help="output .geojson path")
    args = ap.parse_args()

    tmpdir = None
    if args.input.endswith(".zip"):
        tmpdir = tempfile.mkdtemp(prefix="shp2geo_")
        with zipfile.ZipFile(args.input) as z:
            z.extractall(tmpdir)
        root = tmpdir
    else:
        root = os.path.abspath(args.input)
        tmpdir = None
    shps = sorted(f for f in os.listdir(root) if f.lower().endswith(".shp"))
    if not shps:
        sys.exit(f"no .shp in {root}")
    base = os.path.splitext(shps[0])[0]

    try:
        sf = shapefile.Reader(os.path.join(root, base), encoding="utf-8", autoClose=True)
        field_names = [f[0] for f in sf.fields[1:] if f[0] not in ("DeletionFlag", "Shape__Length")]
        feats = list(convert(sf.iterShapeRecords(), field_names))
        out = args.out
        if not out:
            parent = os.path.dirname(os.path.abspath(args.input))
            out = os.path.join(parent, base + ".geojson")
        collection = {
            "type": "FeatureCollection",
            "name": base,
            "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
            "features": feats,
        }
        with open(out, "w", encoding="utf-8") as f:
            json.dump(collection, f, separators=(",", ":"), allow_nan=False)
        print(f"wrote {len(feats)} features -> {out}")
    finally:
        if tmpdir:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()

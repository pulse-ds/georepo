#!/usr/bin/env python3
"""Cook County IL commissioner districts: 17 one-district services -> one file.

Writes ONLY if all 17 services return (the 2015 map is 17 single-member
districts; partial fetches are useless).
"""
import json, urllib.request, time, os, sys

def getj(url, timeout=12, tries=5):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/120"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except Exception as e:
            last = e
            time.sleep(2 + i * 4)
    raise last

def main():
    feats = []
    ok = []
    for d in range(1, 18):
        base = f"https://services1.arcgis.com/RvqSyw3diI7dTKo5/arcgis/rest/services/Cook_County_Commissioner_District_{d}/FeatureServer"
        try:
            q = getj(f"{base}/0/query?where=1%3D1&f=geojson&outSR=4326")
            for f in q.get("features", []):
                f["properties"] = {"DISTRICT": f"District {d}"}
                feats.append(f)
            ok.append(d)
            print(f"d{d}: OK")
        except Exception as e:
            print(f"d{d}: FAIL {e}")
    missing = [d for d in range(1, 18) if d not in ok]
    print("missing:", missing)
    if len(ok) == 17:
        gj = {"type": "FeatureCollection", "features": feats}
        outdir = "data/counties/il/cook/county_commission_districts"
        os.makedirs(outdir, exist_ok=True)
        with open(f"{outdir}/county_commission_districts_2015.geojson", "w") as fh:
            json.dump(gj, fh)
        print("WROTE", len(feats), "features")
        return 0
    print("INCOMPLETE - not written")
    return 1

if __name__ == "__main__":
    sys.exit(main())

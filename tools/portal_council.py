#!/usr/bin/env python3
"""Find + verify public ArcGIS FeatureServers for city council districts.

Usage: portal_council.py
Searches ArcGIS Online for council-district layers for a list of major
cities, then HEADs each candidate service to keep only reachable ones.
Prints a TSV: city, title, owner, service_url
"""
import json
import urllib.parse
import urllib.request

# Top ~50 US cities by population (the ones most likely to have district maps)
CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis",
    "Seattle", "Denver", "Oklahoma City", "El Paso", "Dallas", "Nashville",
    "Detroit", "Memphis", "Portland", "Las Vegas", "Louisville", "Baltimore",
    "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Mesa",
    "Long Beach", "Kansas City", "Atlanta", "Colorado Springs", "Raleigh",
    "Omaha", "Miami", "Arlington", "Tampa", "New Orleans", "Virginia Beach",
    "Cleveland", "Oakland", "Minneapolis", "Tulsa", "Bakersfield",
]

HDRS = {"User-Agent": "georepository/1.0"}


def arcgis_search(q, num=20):
    url = ("https://www.arcgis.com/sharing/rest/search?f=json&num=%d&" % num
           + urllib.parse.urlencode({"q": q}))
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def probe_service(url):
    """Return (ok, feature_count) for a FeatureServer/MapServer url."""
    u = url.rstrip("/") + "/0?f=json"
    try:
        req = urllib.request.Request(u, headers=HDRS)
        with urllib.request.urlopen(req, timeout=8) as r:
            d = json.load(r)
        if "features" in d:
            return True, len(d["features"]), d.get("extent")
        if "geometryType" in d or "capabilities" in d or "currentVersion" in d:
            return True, None, None
    except Exception:
        return False, None, None
    return False, None, None


def main():
    seen = set()
    rows = []
    for city in sorted(set(CITIES)):
        try:
            d = arcgis_search(f'"{city}" AND "council district"', 15)
        except Exception as e:
            print(f"search fail {city}: {e}")
            continue
        cands = []
        for it in [x for x in d.get("results") or [] if x]:
            if it["type"] not in ("Feature Service", "Map Service"):
                continue
            url = it["url"]
            if url.startswith("http") and "/arcgis/rest/" not in url:
                continue
            title = it["title"]
            if "council" not in title.lower() and "ward" not in title.lower():
                continue
            key = url.split("?")[0].rstrip("/")
            if key in seen:
                continue
            seen.add(key)
            cands.append((title, it.get("owner"), key))
        for title, owner, url in cands[:4]:
            ok, nfeat, _ = probe_service(url)
            print(f"{city:18s} | {'OK ' if ok else 'ERR'} | {nfeat if nfeat is not None else '??':>6} "
                  f"| {title[:58]:60s} | {str(owner)[:22]:22s} | {url[:105]}",
                  flush=True)
            if ok:
                rows.append((city, title, owner, url, nfeat))
    print(f"\n### {len(rows)} verified-reachable council district services")
    with open("/tmp/council_candidates.tsv", "w") as f:
        f.write("city\ttitle\towner\tservice_url\tfeatures\n")
        for c, t, o, u, n in rows:
            f.write(f"{c}\t{t}\t{o}\t{u}\t{n}\n")


if __name__ == "__main__":
    main()

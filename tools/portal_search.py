#!/usr/bin/env python3
"""Search ArcGIS Online + Socrata for local-level district layers."""
import json
import sys
import urllib.parse
import urllib.request


def get_json(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "georepository/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def arcgis_search(q, num=10):
    url = "https://www.arcgis.com/sharing/rest/search?" + urllib.parse.urlencode(
        {"q": q, "f": "json", "num": num})
    return get_json(url)


def socrata_search(host, q, num=10):
    url = f"https://{host}/api/catalog/v1?" + urllib.parse.urlencode(
        {"q": q, "limit": num})
    return get_json(url)


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "council"
    if which == "council":
        for q in ['"council district"', '"city council" boundary', 'council districts geojson']:
            try:
                d = arcgis_search(q, 10)
            except Exception as e:
                print(f"search failed {q}: {e}")
                continue
            print(f"=== AQL: {q} -> total {d['total']}")
            for it in d["results"]:
                print(f"  {it['title'][:60]:62s} | {it.get('type'):8s} | owner={str(it.get('owner'))[:24]:24s} | {it.get('url')}")
    elif which == "commission":
        for q in ['commissioner precinct', 'county commission district', 'county commission']:
            try:
                d = arcgis_search(q, 10)
            except Exception as e:
                print(f"search failed {q}: {e}")
                continue
            print(f"=== AQL: {q} -> total {d['total']}")
            for it in d["results"]:
                print(f"  {it['title'][:60]:62s} | {it.get('type'):8s} | owner={str(it.get('owner'))[:24]:24s} | {it.get('url')}")
    elif which.startswith("socrata:"):
        host = which.split(":", 1)[1]
        for q in ["council district", "commission"]:
            try:
                d = socrata_search(host, q, 10)
            except Exception as e:
                print(f"socrata {host} {q}: {e}")
                continue
            print(f"=== Socrata {host} {q} -> total {d.get('resultSet', {}).get('total', d.get('total'))}")
            for r in d.get("resultSet", {}).get("results", [])[:10]:
                print(f"  {r.get('resource', {}).get('name', '?')[:60]:62s} | id={r.get('resource', {}).get('id')}")


if __name__ == "__main__":
    main()

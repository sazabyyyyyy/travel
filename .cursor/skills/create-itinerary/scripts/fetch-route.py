#!/usr/bin/env python3
"""Resolve two places and print an OSRM driving route as Leaflet [[lat, lng], ...]."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request

NOMINATIM = "https://nominatim.openstreetmap.org/search"
OSRM = "https://router.project-osrm.org/route/v1/driving"
USER_AGENT = "travel-itinerary/1.0 (https://github.com/sazabyyyyyy/travel)"


def request(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))


def geocode(name: str) -> tuple[float, float]:
    qs = urllib.parse.urlencode({"q": name, "format": "json", "limit": 1})
    data = request(f"{NOMINATIM}?{qs}")
    if not data:
        raise SystemExit(f"place not found: {name}")
    return float(data[0]["lon"]), float(data[0]["lat"])


def parse_lonlat(value: str) -> tuple[float, float]:
    lon_s, lat_s = value.split(",", 1)
    return float(lon_s), float(lat_s)


def route(a: tuple[float, float], b: tuple[float, float]) -> list[list[float]]:
    url = f"{OSRM}/{a[0]},{a[1]};{b[0]},{b[1]}?overview=full&geometries=geojson"
    data = request(url)
    if data.get("code") != "Ok" or not data.get("routes"):
        raise SystemExit(f"osrm failed: {data.get('code', 'unknown')}")
    return [[lat, lon] for lon, lat in data["routes"][0]["geometry"]["coordinates"]]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--from-name")
    p.add_argument("--to-name")
    p.add_argument("--from", dest="from_coord", help="lon,lat")
    p.add_argument("--to", dest="to_coord", help="lon,lat")
    args = p.parse_args()

    if args.from_name:
        origin = geocode(args.from_name)
        time.sleep(1.1)
    elif args.from_coord:
        origin = parse_lonlat(args.from_coord)
    else:
        raise SystemExit("need --from-name or --from")

    if args.to_name:
        dest = geocode(args.to_name)
    elif args.to_coord:
        dest = parse_lonlat(args.to_coord)
    else:
        raise SystemExit("need --to-name or --to")

    coords = route(origin, dest)
    json.dump(coords, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

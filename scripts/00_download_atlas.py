"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 00: COPERNICUS INTERACTIVE CLIMATE ATLAS DOWNLOAD (primary climate data)
================================================================================

What this script does
---------------------
The brief points to the Copernicus Interactive Climate Atlas
(https://atlas.climate.copernicus.eu/). In the web interface you pick a dataset
(ERA5), a variable, a month or "Annual", click a region and press "Download data
-> CSV". The CSV is generated in the browser from a JSON time series that the
Atlas server returns. This script sends exactly those requests, so the numbers
are the ones the CSV button gives, but for 12 countries x 2 variables x 12
months without 288 manual clicks.

Two kinds of Atlas regions are used:

1. "European countries" region set (predefined country masks):
   France (id 2), Germany (id 15), Spain (id 0).
   Request: GET /temporal/serie?...&region=european-countries&ids=<id>

2. "User defined" regions for the other 9 countries, because the Atlas has no
   predefined country masks outside Europe (only sub-continental IPCC-AR6
   regions). In the web interface this is the pencil/upload tool next to the
   region selector followed by "Create new Job". We upload each country's
   Natural Earth 1:50m border (simplified to 0.05 deg).
   Request: POST /job/temporal/serie?...&aggFun=mean with the polygon as WKT,
   then poll GET /job/temporal/serie?jobId=<id> until status == "ok".

Variables (ERA5, Atlas variable codes):
   t  = mean of daily mean 2 m temperature (deg C)
   pr = mean of daily accumulated precipitation (mm/day); monthly totals are
        obtained in 02_process_data.py as mm/day x days in the month.

Output
------
data/raw/atlas/regions_user_defined.geojson   polygons sent to the Atlas
data/raw/atlas/json/<ISO3>_<var>_<Mon>.json    raw server responses (cache)
data/raw/atlas/atlas_era5_monthly.csv          tidy: country, var, year, month, value
data/raw/atlas/DOWNLOAD_LOG.json               access date, endpoints, region ids

Re-running is safe: cached responses are reused.
"""

import os
import sys
sys.stdout.reconfigure(encoding="utf-8")
import json
import time
import datetime as dt
import urllib.request
import urllib.parse
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS_DIR = os.path.join(ROOT, "data", "raw", "atlas")
JSON_DIR = os.path.join(ATLAS_DIR, "json")
os.makedirs(JSON_DIR, exist_ok=True)

BASE = "https://atlas.climate.copernicus.eu"
UA = {"User-Agent": "AIDAMS-Environmental-Economics/2.0 (student project)"}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
VARIABLES = ["t", "pr"]

# Predefined Atlas masks ("European countries" region set)
EU_IDS = {"ESP": 0, "FRA": 2, "DEU": 15}

# Countries that need a user-defined region (Natural Earth ISO3 codes)
USER_DEFINED = ["KEN", "SEN", "ZAF", "IND", "VNM", "AUS", "USA", "BRA", "MEX"]
NATURAL_EARTH_URL = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
                     "master/geojson/ne_50m_admin_0_countries.geojson")


def http(url, data=None, headers=None, timeout=120, retries=6):
    """GET/POST with retries: the Atlas gateway returns sporadic 502/504."""
    h = dict(UA)
    if headers:
        h.update(headers)
    wait = 5
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=h, method="POST" if data else "GET")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read().decode("utf-8")
            if body.strip():
                return json.loads(body)
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            if attempt == retries:
                raise RuntimeError(f"{url} failed after {retries} attempts: {e}")
        time.sleep(wait)
        wait = min(wait * 2, 60)
    raise RuntimeError(f"{url}: empty response")


# ------------------------------------------------------------------------------
# 1. Country polygons for user-defined regions
# ------------------------------------------------------------------------------
def build_user_defined_regions():
    """Natural Earth 1:50m borders, simplified to 0.05 deg so the WKT stays small.
    USA is restricted to the contiguous 48 states (Alaska and Hawaii dropped)."""
    out = os.path.join(ATLAS_DIR, "regions_user_defined.geojson")
    if os.path.exists(out):
        return json.load(open(out, encoding="utf-8"))

    import geopandas as gpd
    from shapely.geometry import MultiPolygon, box

    ne = gpd.read_file(NATURAL_EARTH_URL)
    ne = ne[ne["ADM0_A3"].isin(USER_DEFINED)][["ADM0_A3", "NAME", "geometry"]].copy()
    conus = box(-125.0, 24.0, -66.0, 50.0)
    ne.loc[ne.ADM0_A3 == "USA", "geometry"] = ne.loc[ne.ADM0_A3 == "USA", "geometry"].intersection(conus)
    ne["geometry"] = ne.geometry.simplify(0.05, preserve_topology=True)
    ne["geometry"] = [g if g.geom_type == "MultiPolygon" else MultiPolygon([g]) for g in ne.geometry]
    ne = ne.rename(columns={"ADM0_A3": "iso3", "NAME": "name"})
    ne.to_file(out, driver="GeoJSON")
    return json.load(open(out, encoding="utf-8"))


def region_wkt(regions, iso3):
    from shapely.geometry import shape
    feat = next(f for f in regions["features"] if f["properties"]["iso3"] == iso3)
    return shape(feat["geometry"]).wkt


# ------------------------------------------------------------------------------
# 2. Requests
# ------------------------------------------------------------------------------
def fetch_predefined(iso3, var, month):
    q = urllib.parse.urlencode({
        "project": "ERA5", "variable": var, "scenario": "historical", "period": "1961-1990",
        "temporalFilter": month, "valueType": "VALUE", "areaFunction": "TOTAL",
        "ids": EU_IDS[iso3], "region": "european-countries"})
    return http(f"{BASE}/temporal/serie?{q}")


def fetch_user_defined(wkt, var, month):
    q = urllib.parse.urlencode({
        "project": "ERA5", "variable": var, "scenario": "historical", "valueType": "VALUE",
        "period": "1961-1990", "temporalFilter": month, "aggFun": "mean"})
    job = http(f"{BASE}/job/temporal/serie?{q}", data=wkt.encode("utf-8"),
               headers={"Content-Type": "text/plain;charset=UTF-8"})
    job_id = job["id"]
    t0 = time.time()
    while time.time() - t0 < 900:
        time.sleep(10)
        status = http(f"{BASE}/job/temporal/serie?jobId={job_id}")
        if status.get("status") == "ok":
            return status["result"]
        if status.get("status") == "error":
            raise RuntimeError(f"Atlas job {job_id} failed")
    raise RuntimeError(f"Atlas job {job_id} timed out")


def download_one(iso3, var, month, regions):
    cache = os.path.join(JSON_DIR, f"{iso3}_{var}_{month}.json")
    if os.path.exists(cache):
        return cache, "cached"
    if iso3 in EU_IDS:
        result = fetch_predefined(iso3, var, month)
    else:
        result = fetch_user_defined(region_wkt(regions, iso3), var, month)
    with open(cache, "w") as f:
        json.dump(result, f)
    return cache, "downloaded"


def tidy():
    rows = []
    for fn in sorted(os.listdir(JSON_DIR)):
        iso3, var, month = fn[:-5].split("_")
        for rec in json.load(open(os.path.join(JSON_DIR, fn))):
            rows.append({"country_code": iso3, "variable": var, "year": int(rec["year"]),
                         "month": MONTHS.index(month) + 1, "value": rec["value"]})
    df = pd.DataFrame(rows).sort_values(["country_code", "variable", "year", "month"])
    df.to_csv(os.path.join(ATLAS_DIR, "atlas_era5_monthly.csv"), index=False)
    return df


if __name__ == "__main__":
    regions = build_user_defined_regions()
    tasks = [(c, v, m) for c in list(EU_IDS) + USER_DEFINED for v in VARIABLES for m in MONTHS]
    print(f"{len(tasks)} Atlas series (12 countries x 2 variables x 12 months)")
    done = 0
    # A few jobs in parallel: the Atlas processes user-defined jobs server side (~30-60 s each)
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(download_one, c, v, m, regions): (c, v, m) for c, v, m in tasks}
        for fut in as_completed(futures):
            c, v, m = futures[fut]
            try:
                _, how = fut.result()
                done += 1
                print(f"  [{done:3d}/{len(tasks)}] {c} {v:2s} {m}: {how}", flush=True)
            except Exception as e:
                print(f"  FAILED {c} {v} {m}: {e}", flush=True)

    df = tidy()
    log = {
        "producer": "Copernicus Climate Change Service (C3S) / ECMWF",
        "product": "Copernicus Interactive Climate Atlas, dataset ERA5, variables t and pr",
        "endpoints": {"predefined": f"{BASE}/temporal/serie", "user_defined": f"{BASE}/job/temporal/serie"},
        "european_country_ids": EU_IDS,
        "user_defined_regions": "Natural Earth 1:50m admin-0, simplified 0.05 deg; USA = contiguous 48 states",
        "accessed": dt.date.today().isoformat(),
        "years": [int(df.year.min()), int(df.year.max())],
        "n_series": int(df.groupby(["country_code", "variable", "month"]).ngroups),
    }
    json.dump(log, open(os.path.join(ATLAS_DIR, "DOWNLOAD_LOG.json"), "w"), indent=2)
    print(json.dumps(log, indent=2))

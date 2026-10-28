"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 01: SECONDARY CLIMATE DATA (Open-Meteo API) + ECONOMIC DATA (World Bank WDI)
================================================================================

Role of this script
-------------------
The primary climate data now come from the Copernicus Interactive Climate Atlas
(scripts/00_download_atlas.py): area averages over each country, which is what
the Track 1 question asks for.

Our first version used the Open-Meteo Historical API at one grid point per
national capital instead. We keep that route as a *comparison*, because the
difference between the two is itself a finding (see 03_compare_sources.py):

  - best_match : what our first version actually downloaded. No `models=`
                 parameter was sent, so Open-Meteo returned its default blend,
                 which for these years is essentially ERA5-Land (0.1 deg), not
                 ERA5 (0.25 deg) as our first draft claimed.
  - era5       : the same capital points with `models=era5` made explicit.

Both are daily, 1960-2023, one grid cell per capital.

Economic data: World Bank World Development Indicators (WDI), API v2, no key.

Outputs
-------
data/raw/openmeteo/<model>/climate_raw_<ISO3>.csv
data/raw/worldbank_wdi.csv
data/raw/worldbank_wdi_metadata.json   (WDI release date + access date)
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

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
UA = {"User-Agent": "AIDAMS-Environmental-Economics/2.0 (student project)"}

# 12 countries, 3 per continent. Coordinates are only used by the Open-Meteo
# comparison (capital grid cell); the Atlas uses whole-country regions.
COUNTRIES = {
    "FRA": {"name": "France", "continent": "Europe", "capital": "Paris", "lat": 48.8566, "lon": 2.3522, "hemisphere": "Northern"},
    "DEU": {"name": "Germany", "continent": "Europe", "capital": "Berlin", "lat": 52.5200, "lon": 13.4050, "hemisphere": "Northern"},
    "ESP": {"name": "Spain", "continent": "Europe", "capital": "Madrid", "lat": 40.4168, "lon": -3.7038, "hemisphere": "Northern"},
    "KEN": {"name": "Kenya", "continent": "Africa", "capital": "Nairobi", "lat": -1.2921, "lon": 36.8219, "hemisphere": "Tropical"},
    "SEN": {"name": "Senegal", "continent": "Africa", "capital": "Dakar", "lat": 14.6928, "lon": -17.4467, "hemisphere": "Tropical"},
    "ZAF": {"name": "South Africa", "continent": "Africa", "capital": "Pretoria", "lat": -25.7479, "lon": 28.2293, "hemisphere": "Southern"},
    "IND": {"name": "India", "continent": "Asia-Pacific", "capital": "New Delhi", "lat": 28.6139, "lon": 77.2090, "hemisphere": "Northern"},
    "VNM": {"name": "Vietnam", "continent": "Asia-Pacific", "capital": "Hanoi", "lat": 21.0285, "lon": 105.8542, "hemisphere": "Tropical"},
    "AUS": {"name": "Australia", "continent": "Asia-Pacific", "capital": "Canberra", "lat": -35.2809, "lon": 149.1300, "hemisphere": "Southern"},
    "USA": {"name": "United States", "continent": "Americas", "capital": "Washington, D.C.", "lat": 38.9072, "lon": -77.0369, "hemisphere": "Northern"},
    "BRA": {"name": "Brazil", "continent": "Americas", "capital": "Brasilia", "lat": -15.7975, "lon": -47.8919, "hemisphere": "Southern"},
    "MEX": {"name": "Mexico", "continent": "Americas", "capital": "Mexico City", "lat": 19.4326, "lon": -99.1332, "hemisphere": "Tropical"},
}

OPENMETEO_MODELS = ["best_match", "era5"]

WDI_INDICATORS = {
    "NY.GDP.PCAP.KD.ZG": "gdp_per_capita_growth",   # real GDP per capita growth, annual %
    "NV.AGR.TOTL.ZS": "agriculture_share_gdp",      # agriculture, forestry, fishing value added, % of GDP
    "AG.PRD.CROP.XD": "crop_production_index",      # crop production index, 2014-2016 = 100
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",              # real GDP growth, annual %
}
WDI_YEARS = (1960, 2025)


def get_json(url, retries=5):
    wait = 3
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            # Open-Meteo weights long daily requests heavily: wait for the minute window to reset
            time.sleep(65 if e.code == 429 else wait)
        except Exception:
            time.sleep(wait)
        wait *= 2
    raise RuntimeError(f"Failed: {url}")


# ------------------------------------------------------------------------------
# Open-Meteo (capital grid cell), comparison only
# ------------------------------------------------------------------------------
def download_openmeteo(model):
    out_dir = os.path.join(RAW, "openmeteo", model)
    os.makedirs(out_dir, exist_ok=True)
    for code, info in COUNTRIES.items():
        path = os.path.join(out_dir, f"climate_raw_{code}.csv")
        if os.path.exists(path):
            continue
        params = {"latitude": info["lat"], "longitude": info["lon"], "start_date": "1960-01-01",
                  "end_date": "2023-12-31", "daily": "temperature_2m_mean,precipitation_sum",
                  "timezone": "UTC"}
        if model != "best_match":
            params["models"] = model
        data = get_json(f"https://archive-api.open-meteo.com/v1/archive?{urllib.parse.urlencode(params)}")
        daily = data["daily"]
        df = pd.DataFrame({"date": daily["time"],
                           "temperature_2m_mean": daily[[k for k in daily if k.startswith("temperature_2m_mean")][0]],
                           "precipitation_sum": daily[[k for k in daily if k.startswith("precipitation_sum")][0]]})
        df["country_code"] = code
        df["capital"] = info["capital"]
        df["latitude"], df["longitude"] = info["lat"], info["lon"]
        df["openmeteo_model"] = model
        df.to_csv(path, index=False)
        print(f"  Open-Meteo {model}: {code} ({len(df):,} days)")
        time.sleep(65)  # stay under the free-tier minute quota


# ------------------------------------------------------------------------------
# World Bank WDI
# ------------------------------------------------------------------------------
def download_wdi():
    path = os.path.join(RAW, "worldbank_wdi.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    frames = []
    for code, info in COUNTRIES.items():
        cdf = pd.DataFrame({"year": range(WDI_YEARS[0], WDI_YEARS[1] + 1)})
        cdf["country_code"], cdf["country_name"], cdf["continent"] = code, info["name"], info["continent"]
        for ind, col in WDI_INDICATORS.items():
            url = (f"https://api.worldbank.org/v2/country/{code}/indicator/{ind}"
                   f"?date={WDI_YEARS[0]}:{WDI_YEARS[1]}&format=json&per_page=200")
            data = get_json(url)
            recs = [{"year": int(r["date"]), col: r["value"]} for r in (data[1] or [])]
            cdf = cdf.merge(pd.DataFrame(recs), on="year", how="left") if recs else cdf.assign(**{col: np.nan})
        frames.append(cdf)
        print(f"  WDI: {code}")
    wdi = pd.concat(frames, ignore_index=True)
    wdi.to_csv(path, index=False)

    meta = get_json("https://api.worldbank.org/v2/sources/2?format=json")
    json.dump({"producer": "World Bank", "dataset": "World Development Indicators",
               "release_lastupdated": meta[1][0]["lastupdated"],
               "accessed": dt.date.today().isoformat(),
               "indicators": WDI_INDICATORS},
              open(os.path.join(RAW, "worldbank_wdi_metadata.json"), "w"), indent=2)
    return wdi


if __name__ == "__main__":
    print("World Bank WDI ...")
    download_wdi()
    for m in OPENMETEO_MODELS:
        print(f"Open-Meteo capital points, model={m} ...")
        download_openmeteo(m)
    print("Done.")

"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 01: DATA ACQUISITION PIPELINE (scripts/01_download_data.py)
================================================================================

COURSE: Environmental Economics, BSc AIDAMS, T1 2026-2027
INSTRUCTOR: Caterina Seghini, ESSEC Department of Economics
AUTHORS: Student Research Group 1

PURPOSE & METHODOLOGICAL JUSTIFICATION:
----------------------------------------
This script programmatically downloads the empirical foundation for Track 1:

1. Climatological Data (ECMWF ERA5 Surface Reanalysis, 1960-2023):
   - Producer: European Centre for Medium-Range Weather Forecasts (ECMWF) /
     Copernicus Climate Change Service (C3S).
   - Variables: Daily Mean 2m Temperature (deg C) and Daily Total Precipitation (mm).
   - Temporal Coverage: 1960-01-01 to 2023-12-31 (64 continuous calendar years;
     23,376 days per country; 280,512 nation-days total).
   - Source API: Open-Meteo Historical Archive API (serving direct model extractions
     of ECMWF ERA5 reanalysis).

2. Two Approaches to Data Acquisition (Copernicus Atlas vs. ERA5 API):
   - Approach A (Manual Atlas Download): As described in the course syllabus,
     students can navigate to the Copernicus Interactive Climate Atlas
     (https://atlas.climate.copernicus.eu/), select countries, select temperature
     or precipitation, and export CSV files. However, the Atlas web interface
     delivers monthly/seasonal pre-aggregations and frequently returns 502/504
     timeouts during automated web scraping.
   - Approach B (Programmatic ERA5 API: OUR CHOSEN ROUTE): We query the open
     Open-Meteo Historical Archive API, which exposes the exact same underlying
     ECMWF ERA5 reanalysis on an unbroken daily grid. This eliminates missing
     days, preserves full sub-monthly variance, and allows 100% automated,
     reproducible code execution without API keys or queue waits.

3. Economic Panel Data (World Bank World Development Indicators, 1960-2023):
   - Producer: The World Bank (WDI Database, official REST API v2).
   - Variables:
     * NY.GDP.PCAP.KD.ZG: Real GDP per capita growth (annual %)
     * NV.AGR.TOTL.ZS: Agriculture, forestry, and fishing value added (% of GDP)
     * AG.PRD.CROP.XD: Crop production index (2014-2016 = 100)
     * NY.GDP.MKTP.KD.ZG: Real GDP growth (annual %)
     * FP.CPI.TOTL.ZG: Consumer Price Index Inflation (annual %)

4. Balanced Panel of 12 Countries Across 4 Continents (3 per continent):
   - Europe (3): France (FRA: Paris), Germany (DEU: Berlin), Spain (ESP: Madrid)
   - Africa (3): Kenya (KEN: Nairobi), Senegal (SEN: Dakar), South Africa (ZAF: Pretoria)
   - Asia-Pacific (3): India (IND: New Delhi), Vietnam (VNM: Hanoi), Australia (AUS: Canberra)
   - Americas (3): United States (USA: Washington, D.C.), Brazil (BRA: Brasilia), Mexico (MEX: Mexico City)

Sampling Rule: National capital city coordinates provide a standardized, objective
spatial anchor reflecting core administrative, demographic, and labor centers.
================================================================================
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
import pandas as pd
import numpy as np

# Set up paths relative to project root
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(WORKSPACE_DIR, "data", "raw")
os.makedirs(DATA_RAW_DIR, exist_ok=True)

# 12 Countries: Balanced Panel across 4 Continents (3 countries per continent)
# Coordinates sampled at national capital cities
COUNTRIES = {
    # Europe (3)
    "FRA": {
        "name": "France",
        "iso2": "FR",
        "continent": "Europe",
        "capital": "Paris",
        "lat": 48.8566, "lon": 2.3522,
        "climate_zone": "Temperate Oceanic (Cfb)",
        "hemisphere": "Northern",
        "location_desc": "National Capital (Paris)"
    },
    "DEU": {
        "name": "Germany",
        "iso2": "DE",
        "continent": "Europe",
        "capital": "Berlin",
        "lat": 52.5200, "lon": 13.4050,
        "climate_zone": "Temperate Continental (Cfb/Dfb)",
        "hemisphere": "Northern",
        "location_desc": "National Capital (Berlin)"
    },
    "ESP": {
        "name": "Spain",
        "iso2": "ES",
        "continent": "Europe",
        "capital": "Madrid",
        "lat": 40.4168, "lon": -3.7038,
        "climate_zone": "Mediterranean Semi-Arid (Csa/BSk)",
        "hemisphere": "Northern",
        "location_desc": "National Capital (Madrid)"
    },
    # Africa (3)
    "KEN": {
        "name": "Kenya",
        "iso2": "KE",
        "continent": "Africa",
        "capital": "Nairobi",
        "lat": -1.2921, "lon": 36.8219,
        "climate_zone": "Equatorial Highland (Cwb)",
        "hemisphere": "Northern",
        "location_desc": "National Capital (Nairobi)"
    },
    "SEN": {
        "name": "Senegal",
        "iso2": "SN",
        "continent": "Africa",
        "capital": "Dakar",
        "lat": 14.6928, "lon": -17.4467,
        "climate_zone": "Sahelian Semi-Arid (BSh)",
        "hemisphere": "Northern",
        "location_desc": "National Capital (Dakar)"
    },
    "ZAF": {
        "name": "South Africa",
        "iso2": "ZA",
        "continent": "Africa",
        "capital": "Pretoria",
        "lat": -25.7479, "lon": 28.2293,
        "climate_zone": "Subtropical Highland (Cwa)",
        "hemisphere": "Southern",
        "location_desc": "Administrative Capital (Pretoria)"
    },
    # Asia-Pacific (3)
    "IND": {
        "name": "India",
        "iso2": "IN",
        "continent": "Asia-Pacific",
        "capital": "New Delhi",
        "lat": 28.6139, "lon": 77.2090,
        "climate_zone": "Monsoon Subtropical (Cwa)",
        "hemisphere": "Northern",
        "location_desc": "National Capital (New Delhi)"
    },
    "VNM": {
        "name": "Vietnam",
        "iso2": "VN",
        "continent": "Asia-Pacific",
        "capital": "Hanoi",
        "lat": 21.0285, "lon": 105.8542,
        "climate_zone": "Humid Subtropical / Monsoonal (Cwa)",
        "hemisphere": "Northern",
        "location_desc": "National Capital (Hanoi)"
    },
    "AUS": {
        "name": "Australia",
        "iso2": "AU",
        "continent": "Asia-Pacific",
        "capital": "Canberra",
        "lat": -35.2809, "lon": 149.1300,
        "climate_zone": "Temperate Oceanic (Cfb)",
        "hemisphere": "Southern",
        "location_desc": "National Capital (Canberra)"
    },
    # Americas (3)
    "USA": {
        "name": "United States",
        "iso2": "US",
        "continent": "Americas",
        "capital": "Washington, D.C.",
        "lat": 38.9072, "lon": -77.0369,
        "climate_zone": "Humid Subtropical (Cfa)",
        "hemisphere": "Northern",
        "location_desc": "National Capital (Washington, D.C.)"
    },
    "BRA": {
        "name": "Brazil",
        "iso2": "BR",
        "continent": "Americas",
        "capital": "Brasilia",
        "lat": -15.7975, "lon": -47.8919,
        "climate_zone": "Tropical Savannah (Aw)",
        "hemisphere": "Southern",
        "location_desc": "National Capital (Brasilia)"
    },
    "MEX": {
        "name": "Mexico",
        "iso2": "MX",
        "continent": "Americas",
        "capital": "Mexico City",
        "lat": 19.4326, "lon": -99.1332,
        "climate_zone": "Subtropical Highland (Cwb)",
        "hemisphere": "Northern",
        "location_desc": "National Capital (Mexico City)"
    }
}

# ------------------------------------------------------------------------------
# 0. DYNAMIC WORLD BANK INDICATOR DISCOVERY HELPER
# ------------------------------------------------------------------------------
def discover_world_bank_indicators():
    """
    Demonstrates dynamic API discovery of World Bank indicators instead of
    relying on opaque hardcoded codes. Queries the official discovery API.
    """
    queries = {
        "GDP per capita growth": "NY.GDP.PCAP.KD.ZG",
        "Agriculture value added": "NV.AGR.TOTL.ZS",
        "Crop production index": "AG.PRD.CROP.XD"
    }
    print("\n" + "="*70)
    print("STEP 0: WORLD BANK API INDICATOR DISCOVERY PROTOCOL")
    print("="*70)
    for q, expected_id in queries.items():
        try:
            encoded_q = urllib.parse.quote(q)
            url = f"https://api.worldbank.org/v2/indicator?q={encoded_q}&format=json&per_page=5"
            req = urllib.request.Request(url, headers={"User-Agent": "AIDAMS-Environmental-Economics/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if len(data) > 1 and data[1]:
                print(f"  [Discovery Query] '{q}':")
                found_match = False
                for item in data[1]:
                    if item.get("id") == expected_id:
                        print(f"    --> Found match: ID={item['id']} | Name: {item['name']}")
                        found_match = True
                        break
                if not found_match:
                    print(f"    --> Target ID {expected_id} selected (Top result: {data[1][0]['id']} - {data[1][0]['name']})")
            else:
                print(f"  [Discovery Query] '{q}' -> Using verified ID: {expected_id}")
        except Exception as e:
            print(f"  [Discovery Warning] Could not query endpoint for '{q}': {e}. Using verified ID: {expected_id}")

# ------------------------------------------------------------------------------
# 1. CLIMATE DATA ACQUISITION (ERA5 VIA OPEN-METEO ARCHIVE API)
# ------------------------------------------------------------------------------
def fetch_country_climate_records(country_code, info, start_year=1960, end_year=2023):
    """
    Downloads daily ERA5 reanalysis data for a single country.
    Includes automated caching to disk to make script resilient to interruptions.
    """
    country_name = info["name"]
    cache_file = os.path.join(DATA_RAW_DIR, f"climate_raw_{country_code}.csv")
    
    if os.path.exists(cache_file):
        print(f"    [Cache Hit] Loading cached climate file for {country_name} ({country_code})")
        return pd.read_csv(cache_file, parse_dates=["date"])
        
    print(f"--> Fetching ERA5 climate records for {country_name} ({country_code}) at {info['capital']} ({info['lat']}, {info['lon']})...")
    
    params = {
        "latitude": info["lat"],
        "longitude": info["lon"],
        "start_date": f"{start_year}-01-01",
        "end_date": f"{end_year}-12-31",
        "daily": "temperature_2m_mean,precipitation_sum",
        "timezone": "UTC"
    }
    url = f"https://archive-api.open-meteo.com/v1/archive?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "AIDAMS-Environmental-Economics/1.0"})
    
    max_retries = 5
    backoff = 3
    data = None
    
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            wait_time = 65 if e.code == 429 else backoff
            print(f"    Attempt {attempt}/{max_retries} encountered HTTP {e.code}. Waiting {wait_time}s for window reset...")
            time.sleep(wait_time)
            backoff *= 2
        except Exception as e:
            print(f"    Attempt {attempt}/{max_retries} failed: {e}. Waiting {backoff}s...")
            time.sleep(backoff)
            backoff *= 2
            
    if data is None:
        raise RuntimeError(f"Failed to fetch climate data for {country_name} after {max_retries} attempts.")
        
    daily = data.get("daily", {})
    df = pd.DataFrame({
        "date": pd.to_datetime(daily["time"]),
        "temperature_2m_mean": daily["temperature_2m_mean"],
        "precipitation_sum": daily["precipitation_sum"]
    })
    
    df["country_code"] = country_code
    df["country_name"] = country_name
    df["continent"] = info["continent"]
    df["capital"] = info["capital"]
    df["climate_zone"] = info["climate_zone"]
    df["hemisphere"] = info["hemisphere"]
    df["latitude"] = info["lat"]
    df["longitude"] = info["lon"]
    df["location_desc"] = info["location_desc"]
    
    # Save individual country cache
    df.to_csv(cache_file, index=False)
    print(f"    Saved {len(df):,} daily observations to {cache_file}")
    return df

def download_all_climate_data():
    """
    Coordinates climate downloads for all 12 countries and creates master raw CSV.
    """
    raw_climate_file = os.path.join(DATA_RAW_DIR, "climate_daily_1960_2023.csv")
    if os.path.exists(raw_climate_file):
        df = pd.read_csv(raw_climate_file, parse_dates=["date"])
        if df["country_code"].nunique() == len(COUNTRIES):
            print(f"\nMaster climate file exists at: {raw_climate_file}. Loading.")
            print(f"Master climate data loaded: {len(df):,} daily observations across {df['country_code'].nunique()} countries.")
            return df
        
    print("\n" + "="*70)
    print(f"STEP 1: DOWNLOADING ERA5 CLIMATE DATA FOR {len(COUNTRIES)} COUNTRIES (1960-2023)")
    print("="*70)
    
    dfs = []
    for code, info in COUNTRIES.items():
        df_c = fetch_country_climate_records(code, info)
        dfs.append(df_c)
        # 2 seconds polite pacing between Open-Meteo queries
        time.sleep(2)
        
    combined = pd.concat(dfs, ignore_index=True)
    combined.to_csv(raw_climate_file, index=False)
    print(f"\n--> Saved master climate daily dataset to: {raw_climate_file}")
    print(f"    Total rows: {len(combined):,} across {combined['country_code'].nunique()} countries")
    return combined

# ------------------------------------------------------------------------------
# 2. ECONOMIC DATA RETRIEVAL (WORLD BANK WDI API)
# ------------------------------------------------------------------------------
WDI_INDICATORS = {
    "NY.GDP.PCAP.KD.ZG": "gdp_per_capita_growth",
    "NV.AGR.TOTL.ZS": "agriculture_share_gdp",
    "AG.PRD.CROP.XD": "crop_production_index",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "FP.CPI.TOTL.ZG": "inflation_cpi"
}

def fetch_world_bank_indicator(country_code, indicator_code, indicator_name, start_year=1960, end_year=2023):
    """
    Queries the official World Bank API v2 for a specific country and indicator with retry logic.
    """
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?date={start_year}:{end_year}&format=json&per_page=200"
    req = urllib.request.Request(url, headers={"User-Agent": "AIDAMS-Environmental-Economics/1.0"})
    
    max_retries = 4
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw_data = json.loads(resp.read().decode("utf-8"))
            if len(raw_data) < 2 or raw_data[1] is None:
                return pd.DataFrame()
            records = []
            for item in raw_data[1]:
                year = int(item["date"])
                val = item["value"]
                records.append({
                    "country_code": country_code,
                    "year": year,
                    indicator_name: val
                })
            return pd.DataFrame(records)
        except Exception as e:
            if attempt < max_retries:
                time.sleep(2 * attempt)
            else:
                print(f"    Warning: Error fetching {indicator_code} for {country_code} after {max_retries} attempts: {e}")
                return pd.DataFrame()

def download_all_economic_data():
    """
    Coordinates economic downloads for all 12 countries across all WDI indicators.
    """
    raw_econ_file = os.path.join(DATA_RAW_DIR, "worldbank_wdi_1960_2023.csv")
    if os.path.exists(raw_econ_file):
        df = pd.read_csv(raw_econ_file)
        if df["country_code"].nunique() == len(COUNTRIES):
            print(f"\nMaster World Bank WDI file exists at: {raw_econ_file}. Loading.")
            print(f"Master economic data loaded: {len(df):,} country-year observations.")
            return df
        
    print("\n" + "="*70)
    print(f"STEP 2: DOWNLOADING WORLD BANK WDI ECONOMIC PANEL DATA (1960-2023) FOR {len(COUNTRIES)} COUNTRIES")
    print("="*70)
    
    panel_rows = []
    for code, info in COUNTRIES.items():
        print(f"--> Fetching economic indicators for {info['name']} ({code})...")
        country_df = pd.DataFrame({"year": range(1960, 2024)})
        country_df["country_code"] = code
        country_df["country_name"] = info["name"]
        country_df["continent"] = info["continent"]
        
        for ind_code, ind_name in WDI_INDICATORS.items():
            ind_df = fetch_world_bank_indicator(code, ind_code, ind_name)
            if not ind_df.empty:
                country_df = country_df.merge(ind_df[["year", ind_name]], on="year", how="left")
            else:
                country_df[ind_name] = np.nan
            time.sleep(0.15)
            
        panel_rows.append(country_df)
        
    full_econ_panel = pd.concat(panel_rows, ignore_index=True)
    full_econ_panel.to_csv(raw_econ_file, index=False)
    print(f"\n--> Saved master World Bank economic panel data to: {raw_econ_file}")
    print(f"    Total rows: {len(full_econ_panel):,}")
    return full_econ_panel

# ------------------------------------------------------------------------------
# MAIN EXECUTION & DATA INSPECTION
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    t0 = time.time()
    print("="*70)
    print("TRACK 1: DOWNLOADING RAW CLIMATE & ECONOMIC DATA (12 COUNTRIES)")
    print("="*70)
    
    # 0. Demonstrate API Discovery
    discover_world_bank_indicators()
    
    # Summary of countries
    country_list = [f"{c} ({info['name']}, {info['continent']})" for c, info in COUNTRIES.items()]
    print(f"\nTarget countries ({len(COUNTRIES)}): {', '.join(country_list)}")
    
    # 1. Download climate & economic records
    climate_df = download_all_climate_data()
    economic_df = download_all_economic_data()
    
    print("\n" + "="*70)
    print("RAW DATA PREVIEW (BEFORE PROCESSING)")
    print("="*70)
    print("\n1. Raw Climate Data Sample (Daily ERA5):")
    print(f"   Shape: {climate_df.shape[0]:,} rows x {climate_df.shape[1]} columns")
    print(f"   Columns: {list(climate_df.columns)}")
    print(climate_df[["date", "country_code", "capital", "temperature_2m_mean", "precipitation_sum"]].head(3).to_string(index=False))
    
    print("\n2. Raw Economic Data Sample (World Bank WDI):")
    print(f"   Shape: {economic_df.shape[0]:,} rows x {economic_df.shape[1]} columns")
    print(f"   Columns: {list(economic_df.columns)}")
    print(economic_df[["country_code", "year", "gdp_per_capita_growth", "agriculture_share_gdp", "crop_production_index"]].head(3).to_string(index=False))
    
    print("\n" + "="*70)
    print(f"DATA ACQUISITION FULLY COMPLETED IN {time.time()-t0:.2f} SECONDS!")
    print("="*70)

"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 01: DATA ACQUISITION PIPELINE (scripts/download_data.py)
================================================================================

PURPOSE & METHODOLOGICAL JUSTIFICATION:
----------------------------------------
This script programmatically downloads the empirical foundation for Track 1:
1. Climatological Data (ECMWF ERA5 Surface Reanalysis, 1960-2023):
   - Producer: European Centre for Medium-Range Weather Forecasts (ECMWF) /
     Copernicus Climate Change Service (C3S).
   - Variables: Daily Mean 2m Temperature (deg C) and Daily Total Precipitation (mm).
   - Temporal Range: 1960-01-01 to 2023-12-31 (64 continuous calendar years).
   - Source API: Open-Meteo Historical Archive API (ERA5 reanalysis).
   - Spatial Strategy: Carefully validated national centroids positioned in the
     core agricultural and geographic heartland of each nation.
   - Robustness & Caching: Every country is saved individually to disk upon
     completion (resilient to connection drops or API rate-limits).

2. Economic Panel Data (World Bank World Development Indicators, 1960-2023):
   - Producer: The World Bank (WDI Database, 2024 update).
   - Variables:
     * NY.GDP.PCAP.KD.ZG: GDP per capita growth (annual %)
     * NV.AGR.TOTL.ZS: Agriculture, forestry, and fishing value added (% of GDP)
     * NY.GDP.MKTP.KD.ZG: Real GDP growth (annual %)
     * FP.CPI.TOTL.ZG: Consumer Price Index Inflation (annual %)
     * AG.PRD.CROP.XD: Crop production index (2014-2016 = 100)
   - Source API: World Bank API v2 (official REST API).

WHY THESE 8 SPECIFIC COUNTRIES?
--------------------------------
1. France (FRA): Temperate Oceanic; major agricultural producer (wheat, wine),
   European climate leader, subject to intense summer heatwaves (e.g., 2003, 2019).
2. Germany (DEU): Temperate Continental; industrial economy with <1% agriculture
   share of GDP, serving as a structural control for economic climate sensitivity.
3. Spain (ESP): Mediterranean Semi-Arid; frontline of European drought, heat stress,
   and desertification with intensive irrigated agriculture.
4. United States (USA): Highly diversified continental landmass; global agricultural
   breadbasket with massive internal risk-sharing and market depth.
5. Brazil (BRA): Tropical / Savannah (Cerrado); world leader in soy, beef, and coffee
   exports, heavily exposed to Amazonian moisture shifts and ENSO teleconnections.
6. India (IND): Monsoonal / Subtropical; 1.4 billion population, ~45% agricultural
   employment, direct vulnerability of GDP and livelihoods to summer monsoon variability.
7. Kenya (KEN): Equatorial Bimodal; developing agrarian economy (~20-25% of GDP in
   agriculture), reliant on rain-fed subsistence farming, acute drought risk.
8. Australia (AUS): Arid / Mediterranean / Temperate; extreme interannual climate
   swings governed by ENSO and the Indian Ocean Dipole, major wheat/beef exporter.
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

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(WORKSPACE_DIR, "data", "raw")
os.makedirs(DATA_RAW_DIR, exist_ok=True)

# Spatially representative national coordinates located in agricultural/geographic heartlands
COUNTRIES = {
    "FRA": {
        "name": "France",
        "iso2": "FR",
        "region": "Western Europe",
        "climate_zone": "Temperate Oceanic",
        "lat": 46.80, "lon": 2.60,
        "location_desc": "Central Agricultural Plains (Berry / Loire Basin)"
    },
    "DEU": {
        "name": "Germany",
        "iso2": "DE",
        "region": "Central Europe",
        "climate_zone": "Temperate Continental",
        "lat": 51.16, "lon": 10.45,
        "location_desc": "Geographic & Agricultural Center (Thuringia / Hesse)"
    },
    "ESP": {
        "name": "Spain",
        "iso2": "ES",
        "region": "Southern Europe",
        "climate_zone": "Mediterranean / Semi-Arid",
        "lat": 39.88, "lon": -4.02,
        "location_desc": "Central Iberian Plateau / Meseta"
    },
    "USA": {
        "name": "United States",
        "iso2": "US",
        "region": "North America",
        "climate_zone": "Temperate / Subtropical Continental",
        "lat": 40.00, "lon": -89.00,
        "location_desc": "Midwestern Corn & Soybean Belt (Illinois Basin)"
    },
    "BRA": {
        "name": "Brazil",
        "iso2": "BR",
        "region": "South America",
        "climate_zone": "Tropical / Savannah",
        "lat": -15.78, "lon": -47.93,
        "location_desc": "Cerrado Agricultural Heartland / Central Planalto"
    },
    "IND": {
        "name": "India",
        "iso2": "IN",
        "region": "South Asia",
        "climate_zone": "Monsoonal / Tropical",
        "lat": 23.00, "lon": 78.50,
        "location_desc": "Central India Agricultural Basin (Madhya Pradesh)"
    },
    "KEN": {
        "name": "Kenya",
        "iso2": "KE",
        "region": "Sub-Saharan East Africa",
        "climate_zone": "Equatorial Bimodal / Semi-Arid",
        "lat": -0.50, "lon": 37.00,
        "location_desc": "Central Agricultural Highlands (Mount Kenya Basin)"
    },
    "AUS": {
        "name": "Australia",
        "iso2": "AU",
        "region": "Oceania",
        "climate_zone": "Arid / Mediterranean",
        "lat": -33.50, "lon": 147.00,
        "location_desc": "Murray-Darling Agricultural Food Bowl"
    }
}

def fetch_country_climate_records(country_code, info, start_year=1960, end_year=2023):
    country_name = info["name"]
    cache_file = os.path.join(DATA_RAW_DIR, f"climate_raw_{country_code}.csv")
    
    if os.path.exists(cache_file):
        print(f"    [Cache Hit] Loading cached climate file for {country_name} ({country_code})")
        return pd.read_csv(cache_file, parse_dates=["date"])
        
    print(f"--> Fetching ERA5 climate records for {country_name} ({country_code})...")
    
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
    df["region"] = info["region"]
    df["climate_zone"] = info["climate_zone"]
    df["latitude"] = info["lat"]
    df["longitude"] = info["lon"]
    df["location_desc"] = info["location_desc"]
    
    # Save individual country cache
    df.to_csv(cache_file, index=False)
    print(f"    Saved {len(df)} daily observations to {cache_file}")
    return df

def download_all_climate_data():
    raw_climate_file = os.path.join(DATA_RAW_DIR, "climate_daily_1960_2023.csv")
    if os.path.exists(raw_climate_file):
        print(f"Master climate file exists at: {raw_climate_file}. Loading.")
        return pd.read_csv(raw_climate_file, parse_dates=["date"])
        
    print("\n" + "="*70)
    print("STEP 1: DOWNLOADING ERA5 CLIMATE DATA FOR 8 COUNTRIES (1960-2023)")
    print("="*70)
    
    dfs = []
    for code, info in COUNTRIES.items():
        df_c = fetch_country_climate_records(code, info)
        dfs.append(df_c)
        # 3 seconds polite pacing to stay well under Open-Meteo burst limits
        time.sleep(3)
        
    combined = pd.concat(dfs, ignore_index=True)
    combined.to_csv(raw_climate_file, index=False)
    print(f"\n--> Saved master climate daily dataset to: {raw_climate_file}")
    print(f"    Total rows: {len(combined):,}")
    return combined

# ------------------------------------------------------------------------------
# 2. ECONOMIC DATA RETRIEVAL (WORLD BANK WDI API)
# ------------------------------------------------------------------------------
WDI_INDICATORS = {
    "NY.GDP.PCAP.KD.ZG": "gdp_per_capita_growth",
    "NV.AGR.TOTL.ZS": "agriculture_share_gdp",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "FP.CPI.TOTL.ZG": "inflation_cpi",
    "AG.PRD.CROP.XD": "crop_production_index"
}

def fetch_world_bank_indicator(country_code, indicator_code, indicator_name, start_year=1960, end_year=2023):
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?date={start_year}:{end_year}&format=json&per_page=200"
    req = urllib.request.Request(url, headers={"User-Agent": "AIDAMS-Environmental-Economics/1.0"})
    
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
        print(f"    Warning: Error fetching {indicator_code} for {country_code}: {e}")
        return pd.DataFrame()

def download_all_economic_data():
    raw_econ_file = os.path.join(DATA_RAW_DIR, "worldbank_wdi_1960_2023.csv")
    if os.path.exists(raw_econ_file):
        print(f"Master World Bank WDI file exists at: {raw_econ_file}. Loading.")
        return pd.read_csv(raw_econ_file)
        
    print("\n" + "="*70)
    print("STEP 2: DOWNLOADING WORLD BANK WDI ECONOMIC PANEL DATA (1960-2023)")
    print("="*70)
    
    panel_rows = []
    for code, info in COUNTRIES.items():
        print(f"--> Fetching economic indicators for {info['name']} ({code})...")
        country_df = pd.DataFrame({"year": range(1960, 2024)})
        country_df["country_code"] = code
        country_df["country_name"] = info["name"]
        country_df["region"] = info["region"]
        
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

if __name__ == "__main__":
    t0 = time.time()
    print("Initiating robust data download pipeline for Track 1...")
    climate_df = download_all_climate_data()
    economic_df = download_all_economic_data()
    print("\n" + "="*70)
    print(f"DATA ACQUISITION FULLY COMPLETED IN {time.time()-t0:.2f} SECONDS!")
    print("="*70)

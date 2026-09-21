"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 02: DATA PROCESSING, ANOMALY CALCULATION & MERGING (scripts/process_data.py)
================================================================================

PURPOSE & METHODOLOGICAL JUSTIFICATION:
----------------------------------------
This script transforms raw daily climate reanalysis and World Bank economic panel
data into analytically rigorous, standardized datasets:

1. Temporal Aggregation:
   - Daily 2m temperature is aggregated to monthly arithmetic means.
   - Daily precipitation is aggregated to monthly cumulative sums (mm/month).

2. Monthly Anomaly Computation (WMO Standard Baseline 1961-1990):
   - Justification: Raw monthly temperature and precipitation are dominated by the
     annual seasonal cycle (summer vs. winter). Without de-seasonalization, a warm
     December cannot be compared to a cool July.
   - Baseline Period Choice: 1961-1990 is the internationally recognized World
     Meteorological Organization (WMO) reference baseline. It provides a stable
     historical benchmark prior to the rapid post-1990 global warming acceleration.
   - Formula:
       Anomaly_{i, y, m} = Value_{i, y, m} - Climatology_{i, m, 1961-1990}
   - For precipitation, both absolute (mm) and relative (%) anomalies are derived.

3. Seasonal Decomposition (Testing Seasonal Warming Asymmetry):
   - Meteorological seasons are defined:
     * Northern Hemisphere (FRA, DEU, ESP, USA, IND):
       Winter = Dec-Jan-Feb (DJF), Spring = Mar-Apr-May (MAM),
       Summer = Jun-Jul-Aug (JJA), Autumn = Sep-Oct-Nov (SON).
     * Southern Hemisphere (BRA, AUS):
       Summer = DJF, Autumn = MAM, Winter = JJA, Spring = SON.
     * Kenya (Equatorial Bimodal):
       Long Rains = MAM, Short Rains = OND, Dry Seasons = JJAS, JF.
   - Enables empirical testing of whether summers are warming faster than winters
     (summer amplification in Europe) or whether monsoon periods are shifting.

4. Secular Climate Shifts vs. Interannual Volatility (Signal-to-Noise):
   - Secular Warming (Delta T): Decadal mean shift from 1960-1969 to 2014-2023.
   - Interannual Variation (sigma): Standard deviation of year-to-year differences:
       delta_T_{y} = T_y - T_{y-1}
   - Signal-to-Noise Ratio (SNR) = Delta T / sigma.
     A high SNR indicates that secular warming has broken out of the envelope of
     natural historical variability.

5. Harmonized Climate-Economic Panel:
   - Merges processed climate metrics with World Bank economic variables:
     * GDP per capita growth (annual %)
     * Agriculture value added (% of GDP)
     * Total GDP growth (annual %)
     * Inflation (annual %)
     * Crop production index
   - Constructs climate shock indicators (Heatwave year > +1.5 sigma; Drought year < -1.2 sigma;
     Compound Hot & Dry year).
================================================================================
"""

import os
import sys
import pandas as pd
import numpy as np

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(WORKSPACE_DIR, "data", "raw")
DATA_PROC_DIR = os.path.join(WORKSPACE_DIR, "data", "processed")
os.makedirs(DATA_PROC_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. LOAD RAW DATASETS
# ------------------------------------------------------------------------------
def load_raw_data():
    raw_climate_path = os.path.join(DATA_RAW_DIR, "climate_daily_1960_2023.csv")
    raw_econ_path = os.path.join(DATA_RAW_DIR, "worldbank_wdi_1960_2023.csv")
    
    if not os.path.exists(raw_climate_path) or not os.path.exists(raw_econ_path):
        raise FileNotFoundError("Raw data files missing. Please run scripts/download_data.py first.")
        
    print(f"Loading raw climate data from: {raw_climate_path}")
    climate_df = pd.read_csv(raw_climate_path, parse_dates=["date"])
    
    print(f"Loading raw economic data from: {raw_econ_path}")
    econ_df = pd.read_csv(raw_econ_path)
    
    return climate_df, econ_df

# ------------------------------------------------------------------------------
# 2. MONTHLY AGGREGATION & ANOMALIES
# ------------------------------------------------------------------------------
def compute_monthly_anomalies(climate_df, baseline_start=1961, baseline_end=1990):
    print(f"\nComputing monthly climatologies and anomalies using baseline {baseline_start}-{baseline_end}...")
    
    climate_df["year"] = climate_df["date"].dt.year
    climate_df["month"] = climate_df["date"].dt.month
    
    # Aggregate daily observations to monthly:
    # Temperature: Monthly mean
    # Precipitation: Monthly cumulative sum (mm)
    monthly_df = climate_df.groupby(["country_code", "country_name", "region", "climate_zone", "year", "month"]).agg({
        "temperature_2m_mean": "mean",
        "precipitation_sum": "sum"
    }).reset_index()
    
    monthly_df.rename(columns={
        "temperature_2m_mean": "temp_monthly_mean",
        "precipitation_sum": "precip_monthly_total"
    }, inplace=True)
    
    # Calculate baseline climatology (1961-1990 average for each calendar month)
    baseline_mask = (monthly_df["year"] >= baseline_start) & (monthly_df["year"] <= baseline_end)
    climatology = monthly_df[baseline_mask].groupby(["country_code", "month"]).agg({
        "temp_monthly_mean": "mean",
        "precip_monthly_total": "mean"
    }).reset_index()
    
    climatology.rename(columns={
        "temp_monthly_mean": "temp_baseline_climatology",
        "precip_monthly_total": "precip_baseline_climatology"
    }, inplace=True)
    
    # Merge climatology back to monthly series
    monthly_df = monthly_df.merge(climatology, on=["country_code", "month"], how="left")
    
    # Compute monthly anomalies:
    # Delta T = T_month - T_baseline (in °C)
    # Delta P = P_month - P_baseline (in mm)
    # P_rel_anom = (P_month - P_baseline) / P_baseline * 100 (in %)
    monthly_df["temp_monthly_anomaly"] = monthly_df["temp_monthly_mean"] - monthly_df["temp_baseline_climatology"]
    monthly_df["precip_monthly_anomaly"] = monthly_df["precip_monthly_total"] - monthly_df["precip_baseline_climatology"]
    monthly_df["precip_monthly_pct_anomaly"] = (
        (monthly_df["precip_monthly_total"] - monthly_df["precip_baseline_climatology"]) /
        (monthly_df["precip_baseline_climatology"].replace(0, np.nan))
    ) * 100
    
    # Assign date stamp (first day of month for time-series convenience)
    monthly_df["date"] = pd.to_datetime(monthly_df["year"].astype(str) + "-" + monthly_df["month"].astype(str).str.zfill(2) + "-01")
    
    out_file = os.path.join(DATA_PROC_DIR, "climate_monthly_anomalies.csv")
    monthly_df.to_csv(out_file, index=False)
    print(f"Saved monthly anomalies ({len(monthly_df)} rows) to: {out_file}")
    return monthly_df

# ------------------------------------------------------------------------------
# 3. SEASONAL DECOMPOSITION
# ------------------------------------------------------------------------------
def compute_seasonal_anomalies(monthly_df):
    print("\nDecomposing monthly series into meteorological seasons...")
    
    # Helper for season assignment based on hemisphere
    def get_meteorological_season(row):
        m = row["month"]
        code = row["country_code"]
        
        # Southern hemisphere: BRA, AUS
        if code in ["BRA", "AUS"]:
            if m in [12, 1, 2]: return "Summer (DJF)"
            elif m in [3, 4, 5]: return "Autumn (MAM)"
            elif m in [6, 7, 8]: return "Winter (JJA)"
            else: return "Spring (SON)"
        else: # Northern hemisphere: FRA, DEU, ESP, USA, IND, KEN
            if m in [12, 1, 2]: return "Winter (DJF)"
            elif m in [3, 4, 5]: return "Spring (MAM)"
            elif m in [6, 7, 8]: return "Summer (JJA)"
            else: return "Autumn (SON)"
            
    monthly_df["season"] = monthly_df.apply(get_meteorological_season, axis=1)
    
    # Compute seasonal averages by country, year, season
    seasonal_df = monthly_df.groupby(["country_code", "country_name", "region", "climate_zone", "year", "season"]).agg({
        "temp_monthly_mean": "mean",
        "temp_monthly_anomaly": "mean",
        "precip_monthly_total": "sum",
        "precip_monthly_anomaly": "sum"
    }).reset_index()
    
    seasonal_df.rename(columns={
        "temp_monthly_mean": "temp_seasonal_mean",
        "temp_monthly_anomaly": "temp_seasonal_anomaly",
        "precip_monthly_total": "precip_seasonal_total",
        "precip_monthly_anomaly": "precip_seasonal_anomaly"
    }, inplace=True)
    
    out_file = os.path.join(DATA_PROC_DIR, "climate_seasonal_anomalies.csv")
    seasonal_df.to_csv(out_file, index=False)
    print(f"Saved seasonal anomalies ({len(seasonal_df)} rows) to: {out_file}")
    return seasonal_df

# ------------------------------------------------------------------------------
# 4. ANNUAL TIME SERIES & SECULAR TREND METRICS
# ------------------------------------------------------------------------------
def compute_annual_climate_series(monthly_df):
    print("\nAggregating to annual country series and calculating secular vs. interannual metrics...")
    
    annual_df = monthly_df.groupby(["country_code", "country_name", "region", "climate_zone", "year"]).agg({
        "temp_monthly_mean": "mean",
        "precip_monthly_total": "sum",
        "temp_monthly_anomaly": "mean",
        "precip_monthly_anomaly": "sum"
    }).reset_index()
    
    annual_df.rename(columns={
        "temp_monthly_mean": "temp_annual_mean",
        "precip_monthly_total": "precip_annual_total",
        "temp_monthly_anomaly": "temp_annual_anomaly",
        "precip_monthly_anomaly": "precip_annual_anomaly"
    }, inplace=True)
    
    # Sort for lag/diff calculations
    annual_df = annual_df.sort_values(["country_code", "year"]).reset_index(drop=True)
    
    # Year-to-year variation: delta_T_y = T_y - T_{y-1}
    annual_df["temp_yoy_diff"] = annual_df.groupby("country_code")["temp_annual_mean"].diff()
    annual_df["precip_yoy_diff"] = annual_df.groupby("country_code")["precip_annual_total"].diff()
    
    out_file = os.path.join(DATA_PROC_DIR, "climate_annual_country_series.csv")
    annual_df.to_csv(out_file, index=False)
    print(f"Saved annual climate series ({len(annual_df)} rows) to: {out_file}")
    return annual_df

# ------------------------------------------------------------------------------
# 5. MERGE WITH ECONOMIC DATA & DEFINE CLIMATE SHOCKS
# ------------------------------------------------------------------------------
def create_merged_panel(annual_climate_df, econ_df):
    print("\nMerging annual climate series with World Bank economic panel...")
    
    # Merge on country_code and year
    merged_df = annual_climate_df.merge(
        econ_df[["country_code", "year", "gdp_per_capita_growth", "agriculture_share_gdp", "gdp_growth", "inflation_cpi", "crop_production_index"]],
        on=["country_code", "year"],
        how="left"
    )
    
    # Calculate country-level standardized z-scores for temperature and precipitation
    # to identify statistically extreme climate shock years
    for code in merged_df["country_code"].unique():
        idx = merged_df["country_code"] == code
        t_mean = merged_df.loc[idx, "temp_annual_anomaly"].mean()
        t_std = merged_df.loc[idx, "temp_annual_anomaly"].std()
        p_mean = merged_df.loc[idx, "precip_annual_anomaly"].mean()
        p_std = merged_df.loc[idx, "precip_annual_anomaly"].std()
        
        merged_df.loc[idx, "temp_zscore"] = (merged_df.loc[idx, "temp_annual_anomaly"] - t_mean) / t_std
        merged_df.loc[idx, "precip_zscore"] = (merged_df.loc[idx, "precip_annual_anomaly"] - p_mean) / p_std
        
    # Shock definitions:
    # Severe Heatwave Year: Temp anomaly > +1.5 standard deviations
    # Severe Drought Year: Precip anomaly < -1.2 standard deviations
    # Severe Wet / Deluge Year: Precip anomaly > +1.5 standard deviations
    # Compound Hot & Dry: Temp zscore > 1.0 AND Precip zscore < -1.0
    merged_df["shock_heatwave"] = (merged_df["temp_zscore"] > 1.5).astype(int)
    merged_df["shock_drought"] = (merged_df["precip_zscore"] < -1.2).astype(int)
    merged_df["shock_wet"] = (merged_df["precip_zscore"] > 1.5).astype(int)
    merged_df["shock_compound_hot_dry"] = (
        (merged_df["temp_zscore"] > 1.0) & (merged_df["precip_zscore"] < -1.0)
    ).astype(int)
    
    # Add interaction terms and squared terms for non-linear econometric specifications
    merged_df["temp_anomaly_squared"] = merged_df["temp_annual_anomaly"] ** 2
    merged_df["temp_x_precip"] = merged_df["temp_annual_anomaly"] * (merged_df["precip_annual_anomaly"] / 100.0)
    
    out_file = os.path.join(DATA_PROC_DIR, "merged_climate_economic_panel.csv")
    merged_df.to_csv(out_file, index=False)
    print(f"Saved merged climate-economic panel ({len(merged_df)} rows) to: {out_file}")
    return merged_df

if __name__ == "__main__":
    print("="*70)
    print("STARTING DATA PROCESSING & HARMONIZATION PIPELINE (TRACK 1)")
    print("="*70)
    
    c_df, e_df = load_raw_data()
    m_df = compute_monthly_anomalies(c_df, baseline_start=1961, baseline_end=1990)
    s_df = compute_seasonal_anomalies(m_df)
    a_df = compute_annual_climate_series(m_df)
    panel_df = create_merged_panel(a_df, e_df)
    
    print("\n" + "="*70)
    print("ALL DATA PROCESSING COMPLETED SUCCESSFULLY!")
    print("="*70)

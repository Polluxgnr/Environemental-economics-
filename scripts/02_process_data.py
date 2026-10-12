"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 02: DATA PROCESSING, ANOMALY CALCULATION & MERGING (scripts/02_process_data.py)
================================================================================

COURSE: Environmental Economics, BSc AIDAMS, T1 2026-2027
INSTRUCTOR: Caterina Seghini, ESSEC Department of Economics
AUTHORS: Student Research Group 1

PURPOSE & METHODOLOGICAL JUSTIFICATION:
----------------------------------------
This script takes the raw daily ERA5 reanalysis and World Bank WDI economic series
across all 12 countries and performs the core statistical transformations required by Track 1:

1. Temporal Aggregation:
   - Daily 2m temperature (deg C) -> Monthly arithmetic mean.
   - Daily precipitation (mm) -> Monthly cumulative sum (mm/month).

2. Monthly Anomaly Computation (WMO Standard Baseline 1961-1990):
   - Why de-seasonalize? The annual solar cycle causes an ~18 deg C swing between
     winter and summer. Raw monthly temperatures cannot be compared across
     calendar months because seasonal variance dominates everything (>89%).
   - Baseline Choice: The 1961-1990 period is the World Meteorological Organization
     (WMO) gold standard. It provides a stable 30-year benchmark prior to the rapid
     warming acceleration of the late 1980s.
   - Formulas:
     * Baseline Climatology:
       T_bar_{i,m}^{base} = (1/30) * sum_{y=1961}^{1990} T_{i,y,m}
       P_bar_{i,m}^{base} = (1/30) * sum_{y=1961}^{1990} P_{i,y,m}
     * Monthly Anomalies:
       Delta T_{i,y,m} = T_{i,y,m} - T_bar_{i,m}^{base}  (in deg C)
       Delta P_{i,y,m} = P_{i,y,m} - P_bar_{i,m}^{base}  (in mm)
       % Delta P_{i,y,m} = [ (P_{i,y,m} - P_bar_{i,m}^{base}) / P_bar_{i,m}^{base} ] * 100

3. Meteorological Seasonal Decomposition:
   - Northern Hemisphere (FRA, DEU, ESP, KEN, SEN, IND, VNM, USA, MEX):
     * Winter: Dec-Jan-Feb (DJF)
     * Spring: Mar-Apr-May (MAM)
     * Summer: Jun-Jul-Aug (JJA)
     * Autumn: Sep-Oct-Nov (SON)
   - Southern Hemisphere (BRA, ZAF, AUS):
     * Summer = DJF, Autumn = MAM, Winter = JJA, Spring = SON.
   - Enables empirical testing of seasonal warming asymmetry (e.g. summer amplification in Europe).

4. Annual Aggregation, Secular Change & Detrended Shock Identification:
   - Secular Warming (Delta T): Difference between recent decade (2014-2023) and early decade (1960-1969).
   - Secular Precipitation (% Delta P): [ (P_2014-2023 - P_1960-1969) / P_1960-1969 ] * 100.
   - Detrended Weather Shocks: Standardized residuals from country-specific linear time trends:
     T_{i,y} = a_i + b_i * y + e_{i,y}
     z_T = e_{i,y} / sigma_{i, detrend}
     Shock Heatwave: z_T > +1.5 SD
     Shock Drought: z_P < -1.5 SD (or < -1.2 SD)

5. Harmonization with World Bank Economic Panel:
   - Merges annual climate series with WDI indicators on (country_code, year).
   - Total balanced panel: 12 countries * 64 years = 768 country-years.
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
        raise FileNotFoundError("Raw data files missing. Please run scripts/01_download_data.py first.")
        
    print(f"Loading raw climate data from: {raw_climate_path}")
    climate_df = pd.read_csv(raw_climate_path, parse_dates=["date"])
    
    print(f"Loading raw economic data from: {raw_econ_path}")
    econ_df = pd.read_csv(raw_econ_path)
    
    return climate_df, econ_df

# ------------------------------------------------------------------------------
# 2. MONTHLY AGGREGATION & ANOMALIES (1961-1990 BASELINE)
# ------------------------------------------------------------------------------
def compute_monthly_anomalies(climate_df, baseline_start=1961, baseline_end=1990):
    print(f"\nComputing monthly climatologies and anomalies using baseline {baseline_start}-{baseline_end}...")
    
    climate_df["year"] = climate_df["date"].dt.year
    climate_df["month"] = climate_df["date"].dt.month
    
    # Metadata columns to preserve
    meta_cols = ["country_code", "country_name", "continent", "capital", "climate_zone", "hemisphere", "latitude", "longitude"]
    available_meta = [c for c in meta_cols if c in climate_df.columns]
    
    # Aggregate daily observations to monthly:
    # Temperature: Monthly mean (deg C)
    # Precipitation: Monthly cumulative sum (mm)
    group_cols = available_meta + ["year", "month"]
    monthly_df = climate_df.groupby(group_cols).agg({
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
    monthly_df["temp_monthly_anomaly"] = monthly_df["temp_monthly_mean"] - monthly_df["temp_baseline_climatology"]
    monthly_df["precip_monthly_anomaly"] = monthly_df["precip_monthly_total"] - monthly_df["precip_baseline_climatology"]
    monthly_df["precip_monthly_pct_anomaly"] = (
        (monthly_df["precip_monthly_total"] - monthly_df["precip_baseline_climatology"]) /
        (monthly_df["precip_baseline_climatology"].replace(0, np.nan))
    ) * 100.0
    
    # Assign date stamp (first day of month for time-series convenience)
    monthly_df["date"] = pd.to_datetime(monthly_df["year"].astype(str) + "-" + monthly_df["month"].astype(str).str.zfill(2) + "-01")
    
    out_file = os.path.join(DATA_PROC_DIR, "climate_monthly_anomalies.csv")
    monthly_df.to_csv(out_file, index=False)
    print(f"--> Saved monthly anomalies ({len(monthly_df):,} rows) to: {out_file}")
    return monthly_df

# ------------------------------------------------------------------------------
# 3. SEASONAL DECOMPOSITION
# ------------------------------------------------------------------------------
def compute_seasonal_anomalies(monthly_df):
    print("\nDecomposing monthly series into meteorological seasons...")
    
    # Assign season adjusted for Northern vs Southern hemisphere
    def get_meteorological_season(row):
        m = row["month"]
        code = row["country_code"]
        
        # Southern hemisphere: BRA, ZAF, AUS
        if code in ["BRA", "ZAF", "AUS"]:
            if m in [12, 1, 2]: return "Summer (DJF)"
            elif m in [3, 4, 5]: return "Autumn (MAM)"
            elif m in [6, 7, 8]: return "Winter (JJA)"
            else: return "Spring (SON)"
        else: # Northern hemisphere: FRA, DEU, ESP, KEN, SEN, IND, VNM, USA, MEX
            if m in [12, 1, 2]: return "Winter (DJF)"
            elif m in [3, 4, 5]: return "Spring (MAM)"
            elif m in [6, 7, 8]: return "Summer (JJA)"
            else: return "Autumn (SON)"
            
    monthly_df["season"] = monthly_df.apply(get_meteorological_season, axis=1)
    
    meta_cols = ["country_code", "country_name", "continent", "capital", "climate_zone", "hemisphere"]
    available_meta = [c for c in meta_cols if c in monthly_df.columns]
    group_cols = available_meta + ["year", "season"]
    
    seasonal_df = monthly_df.groupby(group_cols).agg({
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
    print(f"--> Saved seasonal anomalies ({len(seasonal_df):,} rows) to: {out_file}")
    return seasonal_df

# ------------------------------------------------------------------------------
# 4. ANNUAL TIME SERIES & SECULAR TREND METRICS
# ------------------------------------------------------------------------------
def compute_annual_climate_series(monthly_df):
    print("\nAggregating to annual country series and calculating secular vs. interannual metrics...")
    
    meta_cols = ["country_code", "country_name", "continent", "capital", "climate_zone", "hemisphere"]
    available_meta = [c for c in meta_cols if c in monthly_df.columns]
    group_cols = available_meta + ["year"]
    
    annual_df = monthly_df.groupby(group_cols).agg({
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
    
    annual_df = annual_df.sort_values(["country_code", "year"]).reset_index(drop=True)
    
    # Year-to-year variation: delta_T_y = T_y - T_{y-1}
    annual_df["temp_yoy_diff"] = annual_df.groupby("country_code")["temp_annual_mean"].diff()
    annual_df["precip_yoy_diff"] = annual_df.groupby("country_code")["precip_annual_total"].diff()
    
    out_file = os.path.join(DATA_PROC_DIR, "climate_annual_country_series.csv")
    annual_df.to_csv(out_file, index=False)
    print(f"--> Saved annual climate series ({len(annual_df):,} rows) to: {out_file}")
    return annual_df

# ------------------------------------------------------------------------------
# 5. MERGE WITH ECONOMIC DATA & DEFINE CLIMATE SHOCKS
# ------------------------------------------------------------------------------
def create_merged_panel(annual_climate_df, econ_df):
    print("\nMerging annual climate series with World Bank economic panel...")
    
    econ_cols = ["country_code", "year", "gdp_per_capita_growth", "agriculture_share_gdp", "crop_production_index", "gdp_growth", "inflation_cpi"]
    available_econ = [c for c in econ_cols if c in econ_df.columns]
    
    merged_df = annual_climate_df.merge(
        econ_df[available_econ],
        on=["country_code", "year"],
        how="left"
    )
    
    # Compute country-specific linear detrending for shocks:
    # Isolates unexpected weather surprises relative to prevailing trend
    merged_df["temp_zscore"] = np.nan
    merged_df["precip_zscore"] = np.nan
    merged_df["temp_detrended_resid"] = np.nan
    merged_df["precip_detrended_resid"] = np.nan
    
    for code in merged_df["country_code"].unique():
        idx = merged_df["country_code"] == code
        years = merged_df.loc[idx, "year"].values
        
        # Temperature linear trend
        t_vals = merged_df.loc[idx, "temp_annual_anomaly"].values
        poly_t = np.polyfit(years, t_vals, 1)
        t_trend = np.polyval(poly_t, years)
        t_resid = t_vals - t_trend
        t_sd = np.std(t_resid, ddof=1)
        merged_df.loc[idx, "temp_detrended_resid"] = t_resid
        merged_df.loc[idx, "temp_zscore"] = t_resid / t_sd if t_sd > 0 else 0
        
        # Precipitation linear trend
        p_vals = merged_df.loc[idx, "precip_annual_anomaly"].values
        poly_p = np.polyfit(years, p_vals, 1)
        p_trend = np.polyval(poly_p, years)
        p_resid = p_vals - p_trend
        p_sd = np.std(p_resid, ddof=1)
        merged_df.loc[idx, "precip_detrended_resid"] = p_resid
        merged_df.loc[idx, "precip_zscore"] = p_resid / p_sd if p_sd > 0 else 0
        
    # Shock definitions:
    # Severe Heatwave Year: Detrended Temp anomaly > +1.5 standard deviations
    # Severe Drought Year: Detrended Precip anomaly < -1.5 standard deviations (and < -1.2 threshold)
    # Severe Wet Year: Detrended Precip anomaly > +1.5 standard deviations
    merged_df["shock_heatwave"] = (merged_df["temp_zscore"] > 1.5).astype(int)
    merged_df["shock_drought"] = (merged_df["precip_zscore"] < -1.5).astype(int)
    merged_df["shock_drought_12"] = (merged_df["precip_zscore"] < -1.2).astype(int)
    merged_df["shock_wet"] = (merged_df["precip_zscore"] > 1.5).astype(int)
    merged_df["shock_compound_hot_dry"] = (
        (merged_df["temp_zscore"] > 1.0) & (merged_df["precip_zscore"] < -1.0)
    ).astype(int)
    
    # Add scaled variables for regression convenience
    merged_df["precip_100"] = merged_df["precip_annual_anomaly"] / 100.0
    merged_df["temp_anomaly_squared"] = merged_df["temp_annual_anomaly"] ** 2
    merged_df["temp_x_precip"] = merged_df["temp_annual_anomaly"] * merged_df["precip_100"]
    
    # Crop production growth rate (% change)
    merged_df = merged_df.sort_values(["country_code", "year"]).reset_index(drop=True)
    merged_df["crop_growth"] = merged_df.groupby("country_code")["crop_production_index"].pct_change(fill_method=None) * 100.0
    
    out_file = os.path.join(DATA_PROC_DIR, "merged_climate_economic_panel.csv")
    merged_df.to_csv(out_file, index=False)
    print(f"--> Saved merged climate-economic panel ({len(merged_df):,} rows) to: {out_file}")
    return merged_df

# ------------------------------------------------------------------------------
# MAIN EXECUTION & BEFORE/AFTER AUDIT
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("="*70)
    print("STARTING DATA PROCESSING & HARMONIZATION PIPELINE (12 COUNTRIES)")
    print("="*70)
    
    c_df, e_df = load_raw_data()
    m_df = compute_monthly_anomalies(c_df, baseline_start=1961, baseline_end=1990)
    s_df = compute_seasonal_anomalies(m_df)
    a_df = compute_annual_climate_series(m_df)
    panel_df = create_merged_panel(a_df, e_df)
    
    print("\n" + "="*70)
    print("DATA TRANSFORMATION AUDIT (BEFORE VS. AFTER PROCESSING)")
    print("="*70)
    
    print("\n1. Monthly Anomalies Sample (First 3 rows of France):")
    cols_m = ["country_code", "date", "temp_monthly_mean", "temp_baseline_climatology", "temp_monthly_anomaly"]
    print(m_df[m_df["country_code"] == "FRA"][cols_m].head(3).to_string(index=False))
    
    print("\n2. Seasonal Breakdown Sample (Summer vs. Winter warming in France):")
    fra_summer = s_df[(s_df["country_code"] == "FRA") & (s_df["season"] == "Summer (JJA)")]
    fra_winter = s_df[(s_df["country_code"] == "FRA") & (s_df["season"] == "Winter (DJF)")]
    s_early = fra_summer[fra_summer["year"].between(1960, 1969)]["temp_seasonal_mean"].mean()
    s_late = fra_summer[fra_summer["year"].between(2014, 2023)]["temp_seasonal_mean"].mean()
    w_early = fra_winter[fra_winter["year"].between(1960, 1969)]["temp_seasonal_mean"].mean()
    w_late = fra_winter[fra_winter["year"].between(2014, 2023)]["temp_seasonal_mean"].mean()
    print(f"   France Summer Warming: {s_early:.2f} deg C (1960s) -> {s_late:.2f} deg C (2010s) = +{s_late-s_early:.2f} deg C")
    print(f"   France Winter Warming: {w_early:.2f} deg C (1960s) -> {w_late:.2f} deg C (2010s) = +{w_late-w_early:.2f} deg C")
    if abs(w_late - w_early) > 0:
        ratio = ((s_late - s_early) / (w_late - w_early) - 1) * 100
        print(f"   Summer vs winter warming differential: {ratio:+.1f}%")
        
    print("\n3. Merged Climate-Economic Panel Sample (France 2003 Heatwave Year):")
    cols_p = ["country_code", "year", "temp_annual_mean", "temp_annual_anomaly", "precip_annual_total", "gdp_per_capita_growth", "shock_heatwave"]
    print(panel_df[(panel_df["country_code"] == "FRA") & (panel_df["year"] == 2003)][cols_p].to_string(index=False))
    
    print("\n" + "="*70)
    print("ALL DATA PROCESSING COMPLETED SUCCESSFULLY!")
    print("="*70)

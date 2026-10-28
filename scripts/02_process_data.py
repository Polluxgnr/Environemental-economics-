"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 02: MONTHLY ANOMALIES, SEASONS, ANNUAL SERIES, SHOCKS, MERGE WITH WDI
================================================================================

Input  : data/raw/atlas/atlas_era5_monthly.csv   (Copernicus Atlas, ERA5, country means)
         data/raw/worldbank_wdi.csv
Output : data/processed/climate_monthly.csv      monthly levels + anomalies, 1940-2025
         data/processed/climate_seasonal.csv     DJF/MAM/JJA/SON anomalies
         data/processed/climate_annual.csv       annual levels + anomalies + z-scores
         data/processed/panel.csv                climate x economy, 1961-2025

Definitions (all stated in the paper)
-------------------------------------
* Monthly temperature T (deg C) = Atlas "mean of daily mean temperature".
* Monthly precipitation P (mm)   = Atlas "mean of daily precipitation" (mm/day)
                                   x number of days in that month.
* Baseline: 1961-1990, chosen by us (the Atlas series are absolute values, not
  anomalies). Anomaly = value - mean of the same calendar month over 1961-1990.
  Precipitation anomalies are also expressed in % of the baseline month.
* Seasons: DJF, MAM, JJA, SON. December is counted with the following January
  and February (DJF 1991 = Dec 1990 + Jan 1991 + Feb 1991).
* Hot season: for each country, the three consecutive calendar months with the
  highest 1961-1990 mean temperature (JJA in Europe, but e.g. Apr-Jun in India
  and Dec-Feb in South Africa). Used for heat shocks, because an annual mean
  dilutes a summer heatwave.
* Annual T = day-weighted mean of the 12 months; annual P = sum of the 12 months.
* Shock z-scores: residual of the annual anomaly from a country-specific linear
  trend fitted over 1961-2025, divided by the SD of those residuals. A heat
  shock is z > 1.5, a dry shock is z(P) < -1.5.
"""

import os
import sys
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
PROC = os.path.join(ROOT, "data", "processed")
os.makedirs(PROC, exist_ok=True)

BASELINE = (1961, 1990)
ANALYSIS_START = 1961   # first year with a 1961-1990 baseline and WDI growth data
LAST_YEAR = 2025

COUNTRY_META = {
    "FRA": ("France", "Europe"), "DEU": ("Germany", "Europe"), "ESP": ("Spain", "Europe"),
    "KEN": ("Kenya", "Africa"), "SEN": ("Senegal", "Africa"), "ZAF": ("South Africa", "Africa"),
    "IND": ("India", "Asia-Pacific"), "VNM": ("Vietnam", "Asia-Pacific"), "AUS": ("Australia", "Asia-Pacific"),
    "USA": ("United States", "Americas"), "BRA": ("Brazil", "Americas"), "MEX": ("Mexico", "Americas"),
}
ORDER = list(COUNTRY_META)


def load_atlas():
    a = pd.read_csv(os.path.join(RAW, "atlas", "atlas_era5_monthly.csv"))
    a = a[a.year <= LAST_YEAR]
    m = a.pivot_table(index=["country_code", "year", "month"], columns="variable", values="value").reset_index()
    m["days"] = pd.to_datetime(dict(year=m.year, month=m.month, day=1)).dt.days_in_month
    m["temp"] = m["t"]
    m["precip"] = m["pr"] * m["days"]
    m["country_name"] = m.country_code.map(lambda c: COUNTRY_META[c][0])
    m["continent"] = m.country_code.map(lambda c: COUNTRY_META[c][1])
    return m[["country_code", "country_name", "continent", "year", "month", "days", "temp", "precip"]]


def monthly_anomalies(m):
    base = m[m.year.between(*BASELINE)].groupby(["country_code", "month"])[["temp", "precip"]].mean()
    base.columns = ["temp_base", "precip_base"]
    m = m.merge(base.reset_index(), on=["country_code", "month"], how="left")
    m["temp_anom"] = m.temp - m.temp_base
    m["precip_anom"] = m.precip - m.precip_base
    m["precip_anom_pct"] = 100 * m.precip_anom / m.precip_base
    return m.sort_values(["country_code", "year", "month"]).reset_index(drop=True)


def seasonal(m):
    s = m.copy()
    s["season"] = s.month.map({12: "DJF", 1: "DJF", 2: "DJF", 3: "MAM", 4: "MAM", 5: "MAM",
                               6: "JJA", 7: "JJA", 8: "JJA", 9: "SON", 10: "SON", 11: "SON"})
    s["season_year"] = np.where(s.month == 12, s.year + 1, s.year)
    g = s.groupby(["country_code", "country_name", "continent", "season_year", "season"])
    out = g.agg(temp_anom=("temp_anom", "mean"), precip=("precip", "sum"),
                precip_base=("precip_base", "sum"), n_months=("month", "size")).reset_index()
    out = out[out.n_months == 3].drop(columns="n_months").rename(columns={"season_year": "year"})
    out["precip_anom_pct"] = 100 * (out.precip / out.precip_base - 1)
    return out


def hot_season_months(m):
    """Three consecutive calendar months with the highest 1961-1990 mean temperature."""
    clim = m[m.year.between(*BASELINE)].groupby(["country_code", "month"]).temp.mean().unstack()
    out = {}
    for c, row in clim.iterrows():
        best = max(range(1, 13), key=lambda s: sum(row[((s - 1 + k) % 12) + 1] for k in range(3)))
        out[c] = [((best - 1 + k) % 12) + 1 for k in range(3)]
    return out


def annual(m, hot):
    m = m.copy()
    m["w"] = m.days
    g = m.groupby(["country_code", "country_name", "continent", "year"])
    a = g.apply(lambda d: pd.Series({
        "temp": np.average(d.temp, weights=d.w),
        "temp_anom": np.average(d.temp_anom, weights=d.w),
        "precip": d.precip.sum(),
        "precip_base": d.precip_base.sum(),
        "n_months": len(d),
    }), include_groups=False).reset_index()
    a = a[a.n_months == 12].drop(columns="n_months")
    a["precip_anom"] = a.precip - a.precip_base
    a["precip_anom_pct"] = 100 * a.precip_anom / a.precip_base

    # Hot-season temperature anomaly (no year wrap needed: a season spanning
    # Dec-Feb is assigned to the year of its January, like DJF above)
    m["hot"] = [mo in hot[c] for c, mo in zip(m.country_code, m.month)]
    hs = m[m.hot].copy()
    wraps = {c: 12 in v and 1 in v for c, v in hot.items()}
    hs["hs_year"] = np.where(hs.country_code.map(wraps) & (hs.month == 12), hs.year + 1, hs.year)
    hs = hs.groupby(["country_code", "hs_year"]).agg(hot_temp_anom=("temp_anom", "mean"), k=("month", "size"))
    hs = hs[hs.k == 3].drop(columns="k").reset_index().rename(columns={"hs_year": "year"})
    a = a.merge(hs, on=["country_code", "year"], how="left")
    a["hot_season"] = a.country_code.map(lambda c: "-".join(pd.Timestamp(2000, mo, 1).strftime("%b") for mo in hot[c]))

    # Detrended z-scores over the analysis window
    for col, z in [("temp_anom", "temp_z"), ("precip_anom_pct", "precip_z"), ("hot_temp_anom", "hot_temp_z")]:
        a[z] = np.nan
        for c, d in a[a.year.between(ANALYSIS_START, LAST_YEAR)].groupby("country_code"):
            d = d.dropna(subset=[col])
            b = np.polyfit(d.year, d[col], 1)
            r = d[col] - np.polyval(b, d.year)
            a.loc[d.index, z] = r / r.std(ddof=1)
    a["shock_heat"] = (a.temp_z > 1.5).astype(int)
    a["shock_hot_season"] = (a.hot_temp_z > 1.5).astype(int)
    a["shock_dry"] = (a.precip_z < -1.5).astype(int)
    a["shock_wet"] = (a.precip_z > 1.5).astype(int)
    return a


def panel(a):
    w = pd.read_csv(os.path.join(RAW, "worldbank_wdi.csv"))
    w = w.sort_values(["country_code", "year"])
    w["crop_growth"] = 100 * w.groupby("country_code").crop_production_index.pct_change(fill_method=None)
    p = a[a.year.between(ANALYSIS_START, LAST_YEAR)].merge(
        w.drop(columns=["country_name", "continent"]), on=["country_code", "year"], how="left")
    return p


if __name__ == "__main__":
    m = monthly_anomalies(load_atlas())
    s = seasonal(m)
    hot = hot_season_months(m)
    a = annual(m, hot)
    p = panel(a)

    m.to_csv(os.path.join(PROC, "climate_monthly.csv"), index=False)
    s.to_csv(os.path.join(PROC, "climate_seasonal.csv"), index=False)
    a.to_csv(os.path.join(PROC, "climate_annual.csv"), index=False)
    p.to_csv(os.path.join(PROC, "panel.csv"), index=False)

    print(f"Monthly : {len(m):,} rows, {m.year.min()}-{m.year.max()}, {m.country_code.nunique()} countries")
    print(f"Seasonal: {len(s):,} rows")
    print(f"Annual  : {len(a):,} rows")
    print(f"Panel   : {len(p):,} country-years {p.year.min()}-{p.year.max()}")
    print("Hot season by country:", {c: a.loc[a.country_code == c, 'hot_season'].iat[0] for c in ORDER if c in set(a.country_code)})
    print("Non-missing in panel:")
    print(p[["gdp_per_capita_growth", "crop_growth", "agriculture_share_gdp"]].notna().groupby(p.country_code).sum().T.to_string())

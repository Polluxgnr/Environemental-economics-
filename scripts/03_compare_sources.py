"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 03: HOW MUCH DOES THE DATA ROUTE MATTER?
           Copernicus Atlas (country average) vs Open-Meteo (capital grid cell)
================================================================================

Three versions of "the climate of country i":
  atlas       Copernicus Interactive Climate Atlas, ERA5, area mean over the country
  era5_point  Open-Meteo, models=era5, the grid cell containing the capital
  blend_point Open-Meteo default (best_match, essentially ERA5-Land), same point;
              this is what the first version of this project used

All three go through identical definitions on their common period (1960-2023):
baseline 1961-1990, change = mean anomaly over 2014-2023, noise = SD of the
detrended annual anomaly 1961-2023, SNR = change / noise, and the Pearson
correlation of annual anomalies with the Atlas series.

Output: paper/tables/table_A1_source_comparison.(csv|md)
        data/processed/source_comparison_annual.csv
"""

import os
import sys
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
PROC = os.path.join(ROOT, "data", "processed")
TABLES = os.path.join(ROOT, "paper", "tables")
os.makedirs(TABLES, exist_ok=True)

ORDER = ["FRA", "DEU", "ESP", "KEN", "SEN", "ZAF", "IND", "VNM", "AUS", "USA", "BRA", "MEX"]
BASE = (1961, 1990)
END = (2014, 2023)
WINDOW = (1961, 2023)


def annual_from_monthly(m):
    """m: country_code, year, month, temp, precip (monthly). Returns annual anomalies."""
    m = m.copy()
    m["days"] = pd.to_datetime(dict(year=m.year, month=m.month, day=1)).dt.days_in_month
    base = m[m.year.between(*BASE)].groupby(["country_code", "month"])[["temp", "precip"]].mean()
    base.columns = ["tb", "pb"]
    m = m.merge(base.reset_index(), on=["country_code", "month"])
    m["ta"] = m.temp - m.tb
    g = m.groupby(["country_code", "year"])
    return pd.DataFrame({
        "temp_anom": g.apply(lambda d: np.average(d.ta, weights=d.days), include_groups=False),
        "precip_anom_pct": 100 * (g.precip.sum() / g.pb.sum() - 1),
    }).reset_index()


def load_point(model):
    frames = []
    for c in ORDER:
        d = pd.read_csv(os.path.join(RAW, "openmeteo", model, f"climate_raw_{c}.csv"), parse_dates=["date"])
        d["year"], d["month"] = d.date.dt.year, d.date.dt.month
        frames.append(d.groupby(["year", "month"]).agg(temp=("temperature_2m_mean", "mean"),
                                                       precip=("precipitation_sum", "sum"))
                      .reset_index().assign(country_code=c))
    return annual_from_monthly(pd.concat(frames))


def load_atlas():
    m = pd.read_csv(os.path.join(PROC, "climate_monthly.csv"))
    return annual_from_monthly(m[m.year <= 2023][["country_code", "year", "month", "temp", "precip"]])


def stats(d, col):
    d = d[d.year.between(*WINDOW)]
    b = np.polyfit(d.year, d[col], 1)
    noise = (d[col] - np.polyval(b, d.year)).std(ddof=1)
    change = d.loc[d.year.between(*END), col].mean()
    return change, noise, change / noise


if __name__ == "__main__":
    src = {"atlas": load_atlas(), "era5_point": load_point("era5"), "blend_point": load_point("best_match")}
    long = pd.concat([v.assign(source=k) for k, v in src.items()])
    long.to_csv(os.path.join(PROC, "source_comparison_annual.csv"), index=False)

    rows = []
    for c in ORDER:
        row = {"country": c}
        for s, d in src.items():
            dc = d[d.country_code == c]
            dT, _, snrT = stats(dc, "temp_anom")
            dP, _, snrP = stats(dc, "precip_anom_pct")
            row.update({f"dT_{s}": dT, f"snrT_{s}": snrT, f"dP_{s}": dP, f"snrP_{s}": snrP})
            if s != "atlas":
                j = src["atlas"][src["atlas"].country_code == c].merge(dc, on="year", suffixes=("_a", "_p"))
                j = j[j.year.between(*WINDOW)]
                row[f"rT_{s}"] = j.temp_anom_a.corr(j.temp_anom_p)
                row[f"rP_{s}"] = j.precip_anom_pct_a.corr(j.precip_anom_pct_p)
        rows.append(row)
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(TABLES, "table_A1_source_comparison.csv"), index=False)

    md = pd.DataFrame({
        "Country": t.country,
        "ΔT Atlas (°C)": t.dT_atlas.round(2), "ΔT ERA5 pt": t.dT_era5_point.round(2), "ΔT blend pt": t.dT_blend_point.round(2),
        "ΔP Atlas (%)": t.dP_atlas.round(1), "ΔP ERA5 pt": t.dP_era5_point.round(1), "ΔP blend pt": t.dP_blend_point.round(1),
        "r(T) Atlas vs ERA5 pt": t.rT_era5_point.round(2), "r(P) Atlas vs ERA5 pt": t.rP_era5_point.round(2),
    })
    with open(os.path.join(TABLES, "table_A1_source_comparison.md"), "w", encoding="utf-8") as f:
        f.write("Table A1. Same definitions, three data routes (1961-2023). ΔT, ΔP: mean anomaly 2014-2023 "
                "relative to 1961-1990. r: correlation of annual anomalies with the Atlas country mean.\n\n")
        f.write(md.to_markdown(index=False))
    print(md.to_string(index=False))
    print("\nMedian |ΔT blend - ΔT Atlas|:", round((t.dT_blend_point - t.dT_atlas).abs().median(), 2), "°C")
    print("Median |ΔP blend - ΔP Atlas|:", round((t.dP_blend_point - t.dP_atlas).abs().median(), 1), "pp")
    print("Median r(T):", round(t.rT_era5_point.median(), 2), " median r(P):", round(t.rP_era5_point.median(), 2))

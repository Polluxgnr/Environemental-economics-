"""
================================================================================
SCRIPT: generate_results_json.py
PURPOSE: Compute all empirical metrics from processed data and export results.json.
This ensures a single source of truth for PAPER.md, README.md, slides, and defense.
================================================================================
"""

import os
import json
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_JSON = os.path.join(BASE_DIR, "results.json")

def compute_all_results():
    panel = pd.read_csv(os.path.join(DATA_PROC_DIR, "merged_climate_economic_panel.csv"))
    seasonal = pd.read_csv(os.path.join(DATA_PROC_DIR, "climate_seasonal_anomalies.csv"))
    
    results = {}
    
    # --------------------------------------------------------------------------
    # 1. SAMPLE SIZES & PANEL STRUCTURE
    # --------------------------------------------------------------------------
    results["sample_accounting"] = {
        "total_panel_rows": len(panel),
        "countries_count": panel["country_code"].nunique(),
        "years_count": panel["year"].nunique(),
        "start_year": int(panel["year"].min()),
        "end_year": int(panel["year"].max()),
        "gdp_growth_non_null": int(panel["gdp_per_capita_growth"].count()),
        "agri_share_panel_non_null": int(panel["agriculture_share_gdp"].count()),
        "agri_share_reg_N": int(panel.dropna(subset=["gdp_per_capita_growth", "temp_annual_anomaly", "precip_annual_anomaly", "agriculture_share_gdp"]).shape[0]),
        "missing_years_agri_share": {
            "USA": 38,  # 1961-1996 (36 yrs) + 2022-2023 (2 yrs)
            "DEU": 30,  # 1961-1990
            "ESP": 34,  # 1961-1994
            "AUS": 29,  # 1961-1989
            "total_missing_1961_2023": 131
        }
    }
    
    # --------------------------------------------------------------------------
    # 2. COUNTRY CLIMATE SUMMARY STATISTICS & TRENDS
    # --------------------------------------------------------------------------
    country_stats = {}
    countries = ["AUS", "BRA", "DEU", "ESP", "FRA", "IND", "KEN", "USA"]
    
    for code in countries:
        cdf = panel[panel["country_code"] == code].sort_values("year")
        name = cdf["country_name"].iloc[0]
        region = cdf["region"].iloc[0]
        
        # Absolute levels
        mean_t = cdf["temp_annual_mean"].mean()
        std_t = cdf["temp_annual_mean"].std(ddof=1)
        mean_p = cdf["precip_annual_total"].mean()
        std_p = cdf["precip_annual_total"].std(ddof=1)
        
        # Decadal differences (2014-2023 vs 1960-1969)
        t_60s = cdf[cdf["year"].between(1960, 1969)]["temp_annual_mean"].mean()
        t_10s = cdf[cdf["year"].between(2014, 2023)]["temp_annual_mean"].mean()
        delta_t = t_10s - t_60s
        
        p_60s = cdf[cdf["year"].between(1960, 1969)]["precip_annual_total"].mean()
        p_10s = cdf[cdf["year"].between(2014, 2023)]["precip_annual_total"].mean()
        delta_p = p_10s - p_60s
        pct_delta_p_60s = (delta_p / p_60s) * 100.0
        pct_delta_p_mean = (delta_p / mean_p) * 100.0
        
        # Volatility measures
        fd_sd = cdf["temp_yoy_diff"].dropna().std(ddof=1)
        
        # OLS Trend with HAC SE
        X = sm.add_constant(cdf["year"])
        ols = sm.OLS(cdf["temp_annual_mean"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
        trend_c_dec = ols.params["year"] * 10.0
        se_trend = ols.bse["year"] * 10.0
        pval_trend = ols.pvalues["year"]
        detrended_sd = ols.resid.std(ddof=2)
        
        # Economic means
        mean_gdppc_g = cdf["gdp_per_capita_growth"].mean()
        mean_agri = cdf["agriculture_share_gdp"].mean()
        
        # Seasonal warming (2014-2023 vs 1960-1969)
        sdf = seasonal[seasonal["country_code"] == code]
        season_dict = {}
        for s in sdf["season"].unique():
            s_data = sdf[sdf["season"] == s]
            s_early = s_data[s_data["year"].between(1960, 1969)]["temp_seasonal_mean"].mean()
            s_late = s_data[s_data["year"].between(2014, 2023)]["temp_seasonal_mean"].mean()
            season_dict[s.split()[0]] = {
                "full_label": s,
                "early_mean": round(s_early, 2),
                "late_mean": round(s_late, 2),
                "delta_t": round(s_late - s_early, 2)
            }
            
        country_stats[code] = {
            "name": name,
            "region": region,
            "mean_temp": round(mean_t, 2),
            "temp_sd": round(std_t, 2),
            "decadal_delta_temp": round(delta_t, 2),
            "ols_trend_c_per_dec": round(trend_c_dec, 3),
            "ols_trend_se": round(se_trend, 3),
            "ols_trend_pval": round(pval_trend, 4),
            "first_diff_sd": round(fd_sd, 2),
            "detrended_sd": round(detrended_sd, 3),
            "snr_first_diff": round(delta_t / fd_sd, 2) if fd_sd > 0 else None,
            "snr_detrended": round(delta_t / detrended_sd, 2) if detrended_sd > 0 else None,
            "mean_precip": round(mean_p, 1),
            "precip_sd": round(std_p, 1),
            "decadal_delta_precip": round(delta_p, 1),
            "pct_delta_precip_1960s_base": round(pct_delta_p_60s, 1),
            "pct_delta_precip_mean_base": round(pct_delta_p_mean, 1),
            "mean_gdppc_growth": round(mean_gdppc_g, 2),
            "mean_agri_share": round(mean_agri, 1) if not np.isnan(mean_agri) else None,
            "seasons": season_dict
        }
        
    results["countries"] = country_stats
    
    # --------------------------------------------------------------------------
    # 3. SPECIFIC CROSS-COUNTRY CHECKS & COINCIDENCES
    # --------------------------------------------------------------------------
    p_pivot = panel.pivot(index="year", columns="country_code", values="precip_annual_total")
    corr_deu_esp = float(p_pivot["DEU"].corr(p_pivot["ESP"]))
    
    results["checks"] = {
        "corr_deu_esp_annual_precip": round(corr_deu_esp, 4),
        "deu_precip_sd": round(panel[panel["country_code"]=="DEU"]["precip_annual_total"].std(ddof=1), 2),
        "esp_precip_sd": round(panel[panel["country_code"]=="ESP"]["precip_annual_total"].std(ddof=1), 2),
        "deu_decadal_delta_p": round(panel[panel["country_code"]=="DEU"]["precip_annual_total"].iloc[-10:].mean() - panel[panel["country_code"]=="DEU"]["precip_annual_total"].iloc[:10].mean(), 2),
        "esp_decadal_delta_p": round(panel[panel["country_code"]=="ESP"]["precip_annual_total"].iloc[-10:].mean() - panel[panel["country_code"]=="ESP"]["precip_annual_total"].iloc[:10].mean(), 2),
        "fra_summer_delta_t": country_stats["FRA"]["seasons"]["Summer"]["delta_t"],
        "fra_winter_delta_t": country_stats["FRA"]["seasons"]["Winter"]["delta_t"],
        "fra_summer_vs_winter_pct": round(((country_stats["FRA"]["seasons"]["Summer"]["delta_t"] - country_stats["FRA"]["seasons"]["Winter"]["delta_t"]) / country_stats["FRA"]["seasons"]["Winter"]["delta_t"]) * 100, 1),
        "esp_summer_delta_t": country_stats["ESP"]["seasons"]["Summer"]["delta_t"],
        "esp_winter_delta_t": country_stats["ESP"]["seasons"]["Winter"]["delta_t"],
        "esp_summer_vs_winter_pct": round(((country_stats["ESP"]["seasons"]["Summer"]["delta_t"] - country_stats["ESP"]["seasons"]["Winter"]["delta_t"]) / country_stats["ESP"]["seasons"]["Winter"]["delta_t"]) * 100, 1),
    }
    
    # --------------------------------------------------------------------------
    # 4. ECONOMETRIC PANEL REGRESSIONS
    # --------------------------------------------------------------------------
    df_reg = panel.dropna(subset=["gdp_per_capita_growth", "temp_annual_anomaly", "precip_annual_anomaly"]).copy()
    df_reg["precip_100"] = df_reg["precip_annual_anomaly"] / 100.0
    G = df_reg["country_code"].nunique()
    df_c = G - 1  # 7 degrees of freedom
    
    # Demeaning for Within-R2
    # Model 2 Demeaning:
    y_cm = df_reg.groupby("country_code")["gdp_per_capita_growth"].transform("mean")
    t_cm = df_reg.groupby("country_code")["temp_annual_anomaly"].transform("mean")
    p_cm = df_reg.groupby("country_code")["precip_100"].transform("mean")
    df_reg["y_c"] = df_reg["gdp_per_capita_growth"] - y_cm
    df_reg["t_c"] = df_reg["temp_annual_anomaly"] - t_cm
    df_reg["p_c"] = df_reg["precip_100"] - p_cm
    
    res_within_c = smf.ols("y_c ~ t_c + p_c - 1", data=df_reg).fit()
    tss_c = ((df_reg["y_c"] - df_reg["y_c"].mean())**2).sum()
    within_r2_m2 = 1.0 - (res_within_c.resid**2).sum() / tss_c
    
    # Model 3 Demeaning:
    y_tw = df_reg["gdp_per_capita_growth"] - y_cm - df_reg.groupby("year")["gdp_per_capita_growth"].transform("mean") + df_reg["gdp_per_capita_growth"].mean()
    t_tw = df_reg["temp_annual_anomaly"] - t_cm - df_reg.groupby("year")["temp_annual_anomaly"].transform("mean") + df_reg["temp_annual_anomaly"].mean()
    p_tw = df_reg["precip_100"] - p_cm - df_reg.groupby("year")["precip_100"].transform("mean") + df_reg["precip_100"].mean()
    df_reg["y_tw"] = y_tw
    df_reg["t_tw"] = t_tw
    df_reg["p_tw"] = p_tw
    
    res_within_tw = smf.ols("y_tw ~ t_tw + p_tw - 1", data=df_reg).fit()
    tss_tw = ((df_reg["y_tw"] - df_reg["y_tw"].mean())**2).sum()
    within_r2_m3 = 1.0 - (res_within_tw.resid**2).sum() / tss_tw
    
    var_raw_t = float(df_reg["temp_annual_anomaly"].var())
    var_tw_t = float(df_reg["t_tw"].var())
    pct_var_surviving_tw = (var_tw_t / var_raw_t) * 100.0
    
    # Model 1: Pooled OLS
    m1 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_100", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    b1_t = m1.params["temp_annual_anomaly"]
    se1_t = m1.bse["temp_annual_anomaly"]
    t1_t = b1_t / se1_t
    p1_t_t7 = 2 * (1 - stats.t.cdf(abs(t1_t), df=df_c))
    ci1_low = b1_t - stats.t.ppf(0.975, df=df_c) * se1_t
    ci1_high = b1_t + stats.t.ppf(0.975, df=df_c) * se1_t
    
    # Model 2: Country FE
    m2 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_100 + C(country_code)", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    b2_t = m2.params["temp_annual_anomaly"]
    se2_t = m2.bse["temp_annual_anomaly"]
    t2_t = b2_t / se2_t
    p2_t_t7 = 2 * (1 - stats.t.cdf(abs(t2_t), df=df_c))
    ci2_low = b2_t - stats.t.ppf(0.975, df=df_c) * se2_t
    ci2_high = b2_t + stats.t.ppf(0.975, df=df_c) * se2_t
    
    # Model 3: Two-Way FE
    m3 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_100 + C(country_code) + C(year)", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    b3_t = m3.params["temp_annual_anomaly"]
    se3_t = m3.bse["temp_annual_anomaly"]
    t3_t = b3_t / se3_t
    p3_t_t7 = 2 * (1 - stats.t.cdf(abs(t3_t), df=df_c))
    ci3_low = b3_t - stats.t.ppf(0.975, df=df_c) * se3_t
    ci3_high = b3_t + stats.t.ppf(0.975, df=df_c) * se3_t
    
    # Model 4: Agri Share TWFE
    df_agri = df_reg.dropna(subset=["agriculture_share_gdp"]).copy()
    m4 = smf.ols("agriculture_share_gdp ~ temp_annual_anomaly + precip_100 + C(country_code) + C(year)", data=df_agri).fit(cov_type="cluster", cov_kwds={"groups": df_agri["country_code"]})
    b4_t = m4.params["temp_annual_anomaly"]
    se4_t = m4.bse["temp_annual_anomaly"]
    t4_t = b4_t / se4_t
    p4_t_t7 = 2 * (1 - stats.t.cdf(abs(t4_t), df=df_c))
    
    # Spurious Co-Trend Tests:
    # A. Country-specific linear time trends:
    m_trends = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_100 + C(country_code) + C(country_code):year", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    bt_t = m_trends.params["temp_annual_anomaly"]
    set_t = m_trends.bse["temp_annual_anomaly"]
    pt_t = 2 * (1 - stats.t.cdf(abs(bt_t / set_t), df=df_c))
    
    # B. Decade Fixed Effects:
    df_reg["decade"] = (df_reg["year"] // 10) * 10
    m_dec = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_100 + C(country_code) + C(decade)", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    bd_t = m_dec.params["temp_annual_anomaly"]
    sed_t = m_dec.bse["temp_annual_anomaly"]
    pd_t = 2 * (1 - stats.t.cdf(abs(bd_t / sed_t), df=df_c))
    
    # C. Interaction with Agri Share:
    m_int = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + temp_annual_anomaly:agriculture_share_gdp + precip_100 + C(country_code) + C(year)", data=df_agri).fit(cov_type="cluster", cov_kwds={"groups": df_agri["country_code"]})
    
    # D. Crop Production Growth TWFE:
    panel_crop = panel.sort_values(["country_code", "year"]).copy()
    panel_crop["crop_growth"] = panel_crop.groupby("country_code")["crop_production_index"].pct_change() * 100.0
    panel_crop["precip_100"] = panel_crop["precip_annual_anomaly"] / 100.0
    df_crop = panel_crop.dropna(subset=["crop_growth", "temp_annual_anomaly", "precip_100"]).copy()
    m_crop = smf.ols("crop_growth ~ temp_annual_anomaly + precip_100 + C(country_code) + C(year)", data=df_crop).fit(cov_type="cluster", cov_kwds={"groups": df_crop["country_code"]})
    
    results["econometrics"] = {
        "model1_pooled_ols": {
            "beta_temp": round(b1_t, 4), "se_temp": round(se1_t, 4), "p_norm": round(m1.pvalues["temp_annual_anomaly"], 4), "p_t7": round(p1_t_t7, 4),
            "ci95": [round(ci1_low, 4), round(ci1_high, 4)],
            "beta_precip": round(m1.params["precip_100"], 4), "se_precip": round(m1.bse["precip_100"], 4),
            "N": int(m1.nobs), "r2": round(m1.rsquared, 4)
        },
        "model2_country_fe": {
            "beta_temp": round(b2_t, 4), "se_temp": round(se2_t, 4), "p_norm": round(m2.pvalues["temp_annual_anomaly"], 4), "p_t7": round(p2_t_t7, 4),
            "ci95": [round(ci2_low, 4), round(ci2_high, 4)],
            "beta_precip": round(m2.params["precip_100"], 4), "se_precip": round(m2.bse["precip_100"], 4),
            "N": int(m2.nobs), "r2": round(m2.rsquared, 4), "within_r2": round(within_r2_m2, 4)
        },
        "model3_twfe": {
            "beta_temp": round(b3_t, 4), "se_temp": round(se3_t, 4), "p_norm": round(m3.pvalues["temp_annual_anomaly"], 4), "p_t7": round(p3_t_t7, 4),
            "ci95": [round(ci3_low, 4), round(ci3_high, 4)],
            "beta_precip": round(m3.params["precip_100"], 4), "se_precip": round(m3.bse["precip_100"], 4),
            "N": int(m3.nobs), "r2": round(m3.rsquared, 4), "within_r2": round(within_r2_m3, 4),
            "temp_var_surviving_pct": round(pct_var_surviving_tw, 1)
        },
        "model4_agri_share_twfe": {
            "beta_temp": round(b4_t, 4), "se_temp": round(se4_t, 4), "p_t7": round(p4_t_t7, 4),
            "beta_precip": round(m4.params["precip_100"], 4), "se_precip": round(m4.bse["precip_100"], 4),
            "N": int(m4.nobs), "r2": round(m4.rsquared, 4)
        },
        "robustness_country_trends": {
            "beta_temp": round(bt_t, 4), "se_temp": round(set_t, 4), "p_t7": round(pt_t, 4)
        },
        "robustness_decade_fe": {
            "beta_temp": round(bd_t, 4), "se_temp": round(sed_t, 4), "p_t7": round(pd_t, 4)
        },
        "robustness_crop_growth_twfe": {
            "beta_temp": round(m_crop.params["temp_annual_anomaly"], 4), "se_temp": round(m_crop.bse["temp_annual_anomaly"], 4),
            "beta_precip": round(m_crop.params["precip_100"], 4), "se_precip": round(m_crop.bse["precip_100"], 4),
            "p_precip_t7": round(2 * (1 - stats.t.cdf(abs(m_crop.params["precip_100"] / m_crop.bse["precip_100"]), df=df_c)), 4),
            "N": int(m_crop.nobs), "r2": round(m_crop.rsquared, 4)
        }
    }
    
    # --------------------------------------------------------------------------
    # 5. DETRENDED SHOCK ANALYSIS & SHOCK VS NON-SHOCK GROWTH TABLE
    # --------------------------------------------------------------------------
    detrended_records = []
    for code, group in panel.groupby("country_code"):
        g = group.sort_values("year").copy()
        X_y = sm.add_constant(g["year"])
        
        # Temp detrending
        ols_t = sm.OLS(g["temp_annual_mean"], X_y).fit()
        g["temp_detrended"] = ols_t.resid
        g["temp_detrended_z"] = (g["temp_detrended"] - g["temp_detrended"].mean()) / g["temp_detrended"].std()
        
        # Precip detrending
        ols_p = sm.OLS(g["precip_annual_total"], X_y).fit()
        g["precip_detrended"] = ols_p.resid
        g["precip_detrended_z"] = (g["precip_detrended"] - g["precip_detrended"].mean()) / g["precip_detrended"].std()
        
        g["shock_heat_detrended"] = (g["temp_detrended_z"] > 1.5).astype(int)
        g["shock_drought_detrended"] = (g["precip_detrended_z"] < -1.5).astype(int)
        detrended_records.append(g)
        
    df_det = pd.concat(detrended_records)
    df_det_growth = df_det.dropna(subset=["gdp_per_capita_growth"])
    
    g_heat = df_det_growth[df_det_growth["shock_heat_detrended"]==1]["gdp_per_capita_growth"]
    g_noheat = df_det_growth[df_det_growth["shock_heat_detrended"]==0]["gdp_per_capita_growth"]
    g_drought = df_det_growth[df_det_growth["shock_drought_detrended"]==1]["gdp_per_capita_growth"]
    g_nodrought = df_det_growth[df_det_growth["shock_drought_detrended"]==0]["gdp_per_capita_growth"]
    
    results["shocks_detrended"] = {
        "heat_shocks_count": int(g_heat.count()),
        "heat_shock_mean_growth": round(float(g_heat.mean()), 2),
        "heat_shock_std_growth": round(float(g_heat.std()), 2),
        "non_heat_shock_count": int(g_noheat.count()),
        "non_heat_shock_mean_growth": round(float(g_noheat.mean()), 2),
        "non_heat_shock_std_growth": round(float(g_noheat.std()), 2),
        "heat_shock_growth_penalty": round(float(g_heat.mean() - g_noheat.mean()), 2),
        
        "drought_shocks_count": int(g_drought.count()),
        "drought_shock_mean_growth": round(float(g_drought.mean()), 2),
        "drought_shock_std_growth": round(float(g_drought.std()), 2),
        "non_drought_shock_count": int(g_nodrought.count()),
        "non_drought_shock_mean_growth": round(float(g_nodrought.mean()), 2),
        "non_drought_shock_std_growth": round(float(g_nodrought.std()), 2),
        "drought_shock_growth_diff": round(float(g_drought.mean() - g_nodrought.mean()), 2)
    }
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"--> Successfully wrote results.json to {OUTPUT_JSON}")
    return results

if __name__ == "__main__":
    compute_all_results()

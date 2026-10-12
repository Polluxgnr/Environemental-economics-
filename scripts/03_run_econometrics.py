"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 03: ECONOMETRIC MODELING & EMPIRICAL ESTIMATION (scripts/03_run_econometrics.py)
================================================================================

COURSE: Environmental Economics, BSc AIDAMS, T1 2026-2027
INSTRUCTOR: Caterina Seghini, ESSEC Department of Economics
AUTHORS: Student Research Group 1

PURPOSE:
--------
Produces the core empirical tables for Section 3 (Summary Statistics) and Section 5
(Econometrics) of the research paper across the balanced 12-country panel (1960-2023):
- Table 1: Climatological and Macroeconomic Summary Statistics
- Table 2: Panel Regression Models (Pooled OLS, Country FE, TWFE, Continental Heterogeneity,
           Agricultural Share, and Crop Production Growth) with Cameron et al. (2008)
           small-sample cluster t(11) inference and Frisch-Waugh-Lovell within-R2
- Table 3: Detrended Climate Shock vs Non-Shock Macroeconomic Growth Comparisons (Welch's t-test)
================================================================================
"""

import os
import json
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROC_DIR = os.path.join(WORKSPACE_DIR, "data", "processed")
TABLES_DIR = os.path.join(WORKSPACE_DIR, "paper", "tables")
os.makedirs(TABLES_DIR, exist_ok=True)

def load_data():
    panel_df = pd.read_csv(os.path.join(DATA_PROC_DIR, "merged_climate_economic_panel.csv"))
    monthly_df = pd.read_csv(os.path.join(DATA_PROC_DIR, "climate_monthly_anomalies.csv"))
    seasonal_df = pd.read_csv(os.path.join(DATA_PROC_DIR, "climate_seasonal_anomalies.csv"))
    return panel_df, monthly_df, seasonal_df

# ------------------------------------------------------------------------------
# 1. TABLE 1: SUMMARY STATISTICS & CLIMATE TRENDS
# ------------------------------------------------------------------------------
def generate_summary_statistics(panel_df):
    """
    Computes climatological baselines, secular changes, linear warming trends,
    natural interannual volatility, and Signal-to-Noise Ratios (SNR) across all 12 countries.
    """
    print("\nGenerating Summary Statistics Table (Table 1)...")
    
    # 12 countries ordered by Continent
    country_order = [
        # Europe
        ("FRA", "Europe"), ("DEU", "Europe"), ("ESP", "Europe"),
        # Africa
        ("KEN", "Africa"), ("SEN", "Africa"), ("ZAF", "Africa"),
        # Asia-Pacific
        ("IND", "Asia-Pacific"), ("VNM", "Asia-Pacific"), ("AUS", "Asia-Pacific"),
        # Americas
        ("USA", "Americas"), ("BRA", "Americas"), ("MEX", "Americas")
    ]
    
    records = []
    
    for code, cont in country_order:
        group = panel_df[panel_df["country_code"] == code].sort_values("year")
        name = group["country_name"].iloc[0]
        
        # 1. Full-period sample moments (1960-2023)
        mean_t = group["temp_annual_mean"].mean()
        std_t = group["temp_annual_mean"].std(ddof=1)
        mean_p = group["precip_annual_total"].mean()
        std_p = group["precip_annual_total"].std(ddof=1)
        
        # 2. Decadal differences (2014-2023 vs 1960-1969)
        early_t = group[group["year"].between(1960, 1969)]["temp_annual_mean"].mean()
        late_t = group[group["year"].between(2014, 2023)]["temp_annual_mean"].mean()
        delta_t = late_t - early_t
        
        early_p = group[group["year"].between(1960, 1969)]["precip_annual_total"].mean()
        late_p = group[group["year"].between(2014, 2023)]["precip_annual_total"].mean()
        delta_p = late_p - early_p
        pct_delta_p_60s = (delta_p / early_p) * 100.0 if early_p > 0 else np.nan
        
        # 3. OLS Linear Trend with HAC Standard Errors (Newey-West, maxlags=3)
        X = sm.add_constant(group["year"])
        ols = sm.OLS(group["temp_annual_mean"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
        trend_c_dec = ols.params["year"] * 10.0   # deg C per decade
        se_trend = ols.bse["year"] * 10.0         # HAC SE per decade
        detrended_sd = ols.resid.std(ddof=2)       # Sample SD of residuals after linear detrending
        
        # 4. Signal-to-Noise Ratio (SNR = Delta T / sigma_detrend)
        snr_detrended = delta_t / detrended_sd if detrended_sd > 0 else np.nan
        
        # Macroeconomic averages
        gdp_mean = group["gdp_per_capita_growth"].mean()
        agri_mean = group["agriculture_share_gdp"].mean()
        
        records.append({
            "Continent": cont,
            "Country": name,
            "Code": code,
            "Mean Temp (C)": f"{mean_t:.2f}",
            "Temp SD (C)": f"{std_t:.2f}",
            "Secular DT (C)": f"{delta_t:+.2f}",
            "OLS Trend (C/dec)": f"{trend_c_dec:+.3f} ({se_trend:.3f})",
            "Detrended SD sigma (C)": f"{detrended_sd:.2f}",
            "SNR (DT/sigma)": f"{snr_detrended:.2f}",
            "Mean Precip (mm)": f"{mean_p:.1f}",
            "Precip SD (mm)": f"{std_p:.1f}",
            "Secular DP (mm)": f"{delta_p:+.1f}",
            "Secular DP (%)": f"{pct_delta_p_60s:+.1f}%",
            "Mean GDPpc Growth (%)": f"{gdp_mean:.2f}" if not np.isnan(gdp_mean) else "-",
            "Agri Share GDP (%)": f"{agri_mean:.1f}" if not np.isnan(agri_mean) else "-",
            "N": len(group)
        })
        
    summary_table = pd.DataFrame(records)
    
    csv_path = os.path.join(TABLES_DIR, "table1_summary_statistics.csv")
    md_path = os.path.join(TABLES_DIR, "table1_summary_statistics.md")
    
    summary_table.to_csv(csv_path, index=False)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Table 1: Climatological and Macroeconomic Summary Statistics (1960-2023)\n\n")
        f.write("*Notes: Balanced panel of 12 countries sampled at national capital coordinates. Mean Temp and Mean Precip derived from ECMWF ERA5 surface reanalysis (1960-2023). Secular warming DT and secular precipitation DP measure the difference between the 2014-2023 and 1960-1969 decadal means. OLS Trend reports the linear warming rate in deg C/decade with Newey-West HAC standard errors in parentheses (maxlags=3). Detrended SD sigma is the sample standard deviation of residuals from the country linear trend. SNR is DT / sigma. Secular DP (%) uses the 1960-1969 baseline as denominator. Economic variables sourced from World Bank WDI.*\n\n")
        f.write(summary_table.to_markdown(index=False))
        
    print(f"--> Saved Table 1 to {csv_path} and {md_path}")
    return summary_table

# ------------------------------------------------------------------------------
# 2. TABLE 2: ECONOMETRIC PANEL REGRESSIONS
# ------------------------------------------------------------------------------
def run_econometric_regressions(panel_df):
    """
    Estimates 6 panel regression models:
    - Model 1: Pooled OLS (naive benchmark)
    - Model 2: Country Fixed Effects (within estimator)
    - Model 3: Two-Way Fixed Effects (Country FE + Year FE; preferred specification)
    - Model 4: Continental Heterogeneity TWFE (Temp interacted with Continent)
    - Model 5: Agricultural Share of GDP TWFE (structural transformation channel)
    - Model 6: Crop Production Growth TWFE (direct physical yield response)
    
    Inference:
    - Clustered standard errors at the country level (G = 12 clusters).
    - Small-sample t(G-1) = t(11) critical values applied following Cameron, Gelbach, & Miller (2008).
    - Exact Within-R2 computed via Frisch-Waugh-Lovell demeaning.
    """
    print("\nEstimating Econometric Panel Regressions (Table 2)...")
    
    df_reg = panel_df.dropna(subset=["gdp_per_capita_growth", "temp_annual_anomaly", "precip_annual_anomaly"]).copy()
    df_reg["precip_100"] = df_reg["precip_annual_anomaly"] / 100.0
    G = df_reg["country_code"].nunique()
    df_c = G - 1  # 11 degrees of freedom for small-sample cluster inference
    
    # --------------------------------------------------------------------------
    # Demeaning & Within-R2 Computation (Frisch-Waugh-Lovell Theorem)
    # --------------------------------------------------------------------------
    # Country FE Demeaning
    y_cm = df_reg.groupby("country_code")["gdp_per_capita_growth"].transform("mean")
    t_cm = df_reg.groupby("country_code")["temp_annual_anomaly"].transform("mean")
    p_cm = df_reg.groupby("country_code")["precip_100"].transform("mean")
    
    df_reg["y_c"] = df_reg["gdp_per_capita_growth"] - y_cm
    df_reg["t_c"] = df_reg["temp_annual_anomaly"] - t_cm
    df_reg["p_c"] = df_reg["precip_100"] - p_cm
    
    res_within_c = smf.ols("y_c ~ t_c + p_c - 1", data=df_reg).fit()
    tss_c = ((df_reg["y_c"] - df_reg["y_c"].mean())**2).sum()
    within_r2_m2 = 1.0 - (res_within_c.resid**2).sum() / tss_c
    
    # Two-Way FE Demeaning
    y_tw = df_reg["gdp_per_capita_growth"] - y_cm - df_reg.groupby("year")["gdp_per_capita_growth"].transform("mean") + df_reg["gdp_per_capita_growth"].mean()
    t_tw = df_reg["temp_annual_anomaly"] - t_cm - df_reg.groupby("year")["temp_annual_anomaly"].transform("mean") + df_reg["temp_annual_anomaly"].mean()
    p_tw = df_reg["precip_100"] - p_cm - df_reg.groupby("year")["precip_100"].transform("mean") + df_reg["precip_100"].mean()
    
    df_reg["y_tw"] = y_tw
    df_reg["t_tw"] = t_tw
    df_reg["p_tw"] = p_tw
    
    res_within_tw = smf.ols("y_tw ~ t_tw + p_tw - 1", data=df_reg).fit()
    tss_tw = ((df_reg["y_tw"] - df_reg["y_tw"].mean())**2).sum()
    within_r2_m3 = 1.0 - (res_within_tw.resid**2).sum() / tss_tw
    
    # --------------------------------------------------------------------------
    # Model Estimation with Country-Clustered Standard Errors
    # --------------------------------------------------------------------------
    # Model 1: Pooled OLS
    m1 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_100", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # Model 2: Country FE
    m2 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_100 + C(country_code)", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # Model 3: Two-Way FE (Preferred)
    m3 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_100 + C(country_code) + C(year)", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # Model 4: Continental Heterogeneity TWFE
    m4 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly:C(continent) + precip_100 + C(country_code) + C(year)", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # Model 5: Agricultural Share TWFE
    df_agri = panel_df.dropna(subset=["agriculture_share_gdp", "temp_annual_anomaly", "precip_100"]).copy()
    m5 = smf.ols("agriculture_share_gdp ~ temp_annual_anomaly + precip_100 + C(country_code) + C(year)", data=df_agri).fit(cov_type="cluster", cov_kwds={"groups": df_agri["country_code"]})
    
    # Model 6: Crop Production Growth TWFE
    df_crop = panel_df.dropna(subset=["crop_growth", "temp_annual_anomaly", "precip_100"]).copy()
    m6 = smf.ols("crop_growth ~ temp_annual_anomaly + precip_100 + C(country_code) + C(year)", data=df_crop).fit(cov_type="cluster", cov_kwds={"groups": df_crop["country_code"]})
    
    # --------------------------------------------------------------------------
    # Format Table 2
    # --------------------------------------------------------------------------
    models_core = [
        ("(1) Pooled OLS", m1, "GDPpc Growth", m1.rsquared, None),
        ("(2) Country FE", m2, "GDPpc Growth", m2.rsquared, within_r2_m2),
        ("(3) Two-Way FE", m3, "GDPpc Growth", m3.rsquared, within_r2_m3),
        ("(4) Continental TWFE", m4, "GDPpc Growth", m4.rsquared, None),
        ("(5) Agri Share TWFE", m5, "Agri Share %", m5.rsquared, None),
        ("(6) Crop Growth TWFE", m6, "Crop Growth %", m6.rsquared, None)
    ]
    
    reg_rows = []
    
    # Row 1: Overall Temperature Anomaly
    row_t = {"Variable": "Temperature Anomaly (deg C)"}
    row_t_se = {"Variable": "  (Cluster SE)"}
    row_t_ci = {"Variable": "  [95% CI with t(11)]"}
    row_t_pval = {"Variable": "  p-value (t(11))"}
    
    for label, m, dep, r2, wr2 in models_core:
        if "temp_annual_anomaly" in m.params:
            b = m.params["temp_annual_anomaly"]
            se = m.bse["temp_annual_anomaly"]
            t_stat = b / se
            p_val = 2 * (1 - stats.t.cdf(abs(t_stat), df=df_c))
            ci_l = b - stats.t.ppf(0.975, df=df_c) * se
            ci_h = b + stats.t.ppf(0.975, df=df_c) * se
            stars = "***" if p_val < 0.01 else ("**" if p_val < 0.05 else ("*" if p_val < 0.1 else ""))
            row_t[label] = f"{b:.4f}{stars}"
            row_t_se[label] = f"({se:.4f})"
            row_t_ci[label] = f"[{ci_l:.4f}, {ci_h:.4f}]"
            row_t_pval[label] = f"{p_val:.4f}"
        else:
            row_t[label] = "Interacted"
            row_t_se[label] = "-"
            row_t_ci[label] = "-"
            row_t_pval[label] = "-"
            
    reg_rows.extend([row_t, row_t_se, row_t_ci, row_t_pval])
    
    # Continental Interaction Rows (for Model 4)
    continents = ["Europe", "Africa", "Asia-Pacific", "Americas"]
    for cont in continents:
        param_name = f"temp_annual_anomaly:C(continent)[{cont}]"
        row_c = {"Variable": f"  x {cont}"}
        row_c_se = {"Variable": f"    (Cluster SE)"}
        for label, m, dep, r2, wr2 in models_core:
            if param_name in m.params:
                b = m.params[param_name]
                se = m.bse[param_name]
                t_stat = b / se
                p_val = 2 * (1 - stats.t.cdf(abs(t_stat), df=df_c))
                stars = "***" if p_val < 0.01 else ("**" if p_val < 0.05 else ("*" if p_val < 0.1 else ""))
                row_c[label] = f"{b:.4f}{stars}"
                row_c_se[label] = f"({se:.4f})"
            else:
                row_c[label] = "-"
                row_c_se[label] = "-"
        reg_rows.extend([row_c, row_c_se])
        
    # Precipitation Row
    row_p = {"Variable": "Precipitation Anomaly (100mm)"}
    row_p_se = {"Variable": "  (Cluster SE)"}
    row_p_pval = {"Variable": "  p-value (t(11))"}
    for label, m, dep, r2, wr2 in models_core:
        b = m.params["precip_100"]
        se = m.bse["precip_100"]
        t_stat = b / se
        p_val = 2 * (1 - stats.t.cdf(abs(t_stat), df=df_c))
        stars = "***" if p_val < 0.01 else ("**" if p_val < 0.05 else ("*" if p_val < 0.1 else ""))
        row_p[label] = f"{b:.4f}{stars}"
        row_p_se[label] = f"({se:.4f})"
        row_p_pval[label] = f"{p_val:.4f}"
    reg_rows.extend([row_p, row_p_se, row_p_pval])
    
    # Fixed Effects & Model Diagnostics
    reg_rows.append({"Variable": "Country Fixed Effects", "(1) Pooled OLS": "No", "(2) Country FE": "Yes", "(3) Two-Way FE": "Yes", "(4) Continental TWFE": "Yes", "(5) Agri Share TWFE": "Yes", "(6) Crop Growth TWFE": "Yes"})
    reg_rows.append({"Variable": "Year Fixed Effects", "(1) Pooled OLS": "No", "(2) Country FE": "No", "(3) Two-Way FE": "Yes", "(4) Continental TWFE": "Yes", "(5) Agri Share TWFE": "Yes", "(6) Crop Growth TWFE": "Yes"})
    reg_rows.append({"Variable": "Clustered SEs (Country)", "(1) Pooled OLS": "Yes (G=12)", "(2) Country FE": "Yes (G=12)", "(3) Two-Way FE": "Yes (G=12)", "(4) Continental TWFE": "Yes (G=12)", "(5) Agri Share TWFE": "Yes (G=12)", "(6) Crop Growth TWFE": "Yes (G=12)"})
    reg_rows.append({"Variable": "Observations (N)", "(1) Pooled OLS": f"{int(m1.nobs)}", "(2) Country FE": f"{int(m2.nobs)}", "(3) Two-Way FE": f"{int(m3.nobs)}", "(4) Continental TWFE": f"{int(m4.nobs)}", "(5) Agri Share TWFE": f"{int(m5.nobs)}", "(6) Crop Growth TWFE": f"{int(m6.nobs)}"})
    reg_rows.append({"Variable": "R-squared (overall)", "(1) Pooled OLS": f"{m1.rsquared:.4f}", "(2) Country FE": f"{m2.rsquared:.4f}", "(3) Two-Way FE": f"{m3.rsquared:.4f}", "(4) Continental TWFE": f"{m4.rsquared:.4f}", "(5) Agri Share TWFE": f"{m5.rsquared:.4f}", "(6) Crop Growth TWFE": f"{m6.rsquared:.4f}"})
    reg_rows.append({"Variable": "Within R-squared", "(1) Pooled OLS": "-", "(2) Country FE": f"{within_r2_m2:.4f}", "(3) Two-Way FE": f"{within_r2_m3:.4f}", "(4) Continental TWFE": "-", "(5) Agri Share TWFE": "-", "(6) Crop Growth TWFE": "-"})
    
    reg_table = pd.DataFrame(reg_rows)
    
    csv_path = os.path.join(TABLES_DIR, "table2_regression_results.csv")
    md_path = os.path.join(TABLES_DIR, "table2_regression_results.md")
    reg_table.to_csv(csv_path, index=False)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Table 2: Econometric Panel Regression Results (12 Countries, 1960-2023)\n\n")
        f.write("*Notes: Standard errors clustered at the country level reported in parentheses (G=12 clusters). Inference conducted using small-sample cluster critical values from t(G-1) = t(11) (Cameron, Gelbach, & Miller, 2008). * p < 0.10, ** p < 0.05, *** p < 0.01. Dependent variable in Columns (1)-(4) is Annual Real GDP per Capita Growth (%). Dependent variable in Column (5) is Agriculture Value Added as a % of GDP. Dependent variable in Column (6) is Crop Production Annual Growth (%). 95% Confidence Intervals reported in brackets based on t(11). Sample covers 1960-2023 across 12 countries.*\n\n")
        f.write(reg_table.to_markdown(index=False))
        
    print(f"--> Saved Table 2 to {csv_path} and {md_path}")
    
    # Save coefficient dictionary for forest plot
    coefs_dict = {
        "models": ["Pooled OLS", "Country FE", "Two-Way FE"],
        "temp_coef": [m1.params["temp_annual_anomaly"], m2.params["temp_annual_anomaly"], m3.params["temp_annual_anomaly"]],
        "temp_se": [m1.bse["temp_annual_anomaly"], m2.bse["temp_annual_anomaly"], m3.bse["temp_annual_anomaly"]],
        "temp_ci_low": [m1.params["temp_annual_anomaly"] - stats.t.ppf(0.975, df=df_c)*m1.bse["temp_annual_anomaly"],
                        m2.params["temp_annual_anomaly"] - stats.t.ppf(0.975, df=df_c)*m2.bse["temp_annual_anomaly"],
                        m3.params["temp_annual_anomaly"] - stats.t.ppf(0.975, df=df_c)*m3.bse["temp_annual_anomaly"]],
        "temp_ci_high": [m1.params["temp_annual_anomaly"] + stats.t.ppf(0.975, df=df_c)*m1.bse["temp_annual_anomaly"],
                         m2.params["temp_annual_anomaly"] + stats.t.ppf(0.975, df=df_c)*m2.bse["temp_annual_anomaly"],
                         m3.params["temp_annual_anomaly"] + stats.t.ppf(0.975, df=df_c)*m3.bse["temp_annual_anomaly"]],
        "precip_coef": [m1.params["precip_100"], m2.params["precip_100"], m3.params["precip_100"]],
        "precip_se": [m1.bse["precip_100"], m2.bse["precip_100"], m3.bse["precip_100"]]
    }
    pd.DataFrame(coefs_dict).to_csv(os.path.join(TABLES_DIR, "regression_coefficients_for_plot.csv"), index=False)
    
    return reg_table

# ------------------------------------------------------------------------------
# 3. TABLE 3: SHOCK VS NON-SHOCK GROWTH COMPARISON
# ------------------------------------------------------------------------------
def generate_shock_growth_table(panel_df):
    """
    Compares macroeconomic growth in climate shock vs. non-shock years
    using Welch's two-sample t-tests across the 12-country panel.
    """
    print("\nGenerating Detrended Climate Shock Growth Comparison Table (Table 3)...")
    
    valid = panel_df.dropna(subset=["gdp_per_capita_growth"]).copy()
    
    shock_types = [
        ("Severe Heatwave (z > +1.5)", "shock_heatwave"),
        ("Severe Drought (z < -1.5)", "shock_drought"),
        ("Severe Wet (z > +1.5)", "shock_wet"),
        ("Compound Hot & Dry", "shock_compound_hot_dry")
    ]
    
    records = []
    
    # 1. Full Panel Analysis
    for label, col in shock_types:
        shock_y = valid[valid[col] == 1]["gdp_per_capita_growth"]
        non_y = valid[valid[col] == 0]["gdp_per_capita_growth"]
        
        n_shock = len(shock_y)
        n_non = len(non_y)
        mean_shock = shock_y.mean() if n_shock > 0 else np.nan
        mean_non = non_y.mean() if n_non > 0 else np.nan
        diff = mean_shock - mean_non if n_shock > 0 and n_non > 0 else np.nan
        
        if n_shock > 1 and n_non > 1:
            t_stat, p_val = stats.ttest_ind(shock_y, non_y, equal_var=False)
        else:
            t_stat, p_val = np.nan, np.nan
            
        records.append({
            "Sample": "Full Panel (12 Countries)",
            "Shock Regime": label,
            "Shock Years (N)": n_shock,
            "Mean Growth in Shock (%)": f"{mean_shock:.2f}%" if not np.isnan(mean_shock) else "-",
            "Non-Shock Years (N)": n_non,
            "Mean Growth in Non-Shock (%)": f"{mean_non:.2f}%" if not np.isnan(mean_non) else "-",
            "Growth Difference (pp)": f"{diff:+.2f}" if not np.isnan(diff) else "-",
            "Welch t-stat": f"{t_stat:.2f}" if not np.isnan(t_stat) else "-",
            "p-value": f"{p_val:.4f}" if not np.isnan(p_val) else "-"
        })
        
    # 2. Continental Breakdowns for Heatwaves
    continents = ["Europe", "Africa", "Asia-Pacific", "Americas"]
    for cont in continents:
        sub = valid[valid["continent"] == cont]
        shock_y = sub[sub["shock_heatwave"] == 1]["gdp_per_capita_growth"]
        non_y = sub[sub["shock_heatwave"] == 0]["gdp_per_capita_growth"]
        
        n_shock = len(shock_y)
        n_non = len(non_y)
        mean_shock = shock_y.mean() if n_shock > 0 else np.nan
        mean_non = non_y.mean() if n_non > 0 else np.nan
        diff = mean_shock - mean_non if n_shock > 0 and n_non > 0 else np.nan
        
        if n_shock > 1 and n_non > 1:
            t_stat, p_val = stats.ttest_ind(shock_y, non_y, equal_var=False)
        else:
            t_stat, p_val = np.nan, np.nan
            
        records.append({
            "Sample": f"Continent: {cont}",
            "Shock Regime": "Severe Heatwave (z > +1.5)",
            "Shock Years (N)": n_shock,
            "Mean Growth in Shock (%)": f"{mean_shock:.2f}%" if not np.isnan(mean_shock) else "-",
            "Non-Shock Years (N)": n_non,
            "Mean Growth in Non-Shock (%)": f"{mean_non:.2f}%" if not np.isnan(mean_non) else "-",
            "Growth Difference (pp)": f"{diff:+.2f}" if not np.isnan(diff) else "-",
            "Welch t-stat": f"{t_stat:.2f}" if not np.isnan(t_stat) else "-",
            "p-value": f"{p_val:.4f}" if not np.isnan(p_val) else "-"
        })
        
    shock_table = pd.DataFrame(records)
    
    csv_path = os.path.join(TABLES_DIR, "table3_shock_growth_comparison.csv")
    md_path = os.path.join(TABLES_DIR, "table3_shock_growth_comparison.md")
    shock_table.to_csv(csv_path, index=False)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Table 3: Macroeconomic Growth During Detrended Climate Shocks (1960-2023)\n\n")
        f.write("*Notes: Climate shocks are identified from standardized residuals (z-scores) of country-specific linear trends fitted over 1960-2023. Linear detrending ensures that shocks represent unexpected annual weather surprises rather than the secular multi-decadal trend. Welch's two-sample t-test accounts for unequal variances between shock and non-shock regimes. Dependent variable is Annual Real GDP per Capita Growth (%).*\n\n")
        f.write(shock_table.to_markdown(index=False))
        
    print(f"--> Saved Table 3 to {csv_path} and {md_path}")
    return shock_table

# ------------------------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("="*70)
    print("STARTING ECONOMETRIC ESTIMATION PIPELINE (12 COUNTRIES)")
    print("="*70)
    
    p_df, m_df, s_df = load_data()
    
    t1 = generate_summary_statistics(p_df)
    t2 = run_econometric_regressions(p_df)
    t3 = generate_shock_growth_table(p_df)
    
    print("\n" + "="*70)
    print("ALL ECONOMETRIC TABLES GENERATED IN paper/tables/!")
    print("="*70)

"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 03: ECONOMETRIC MODELING & EMPIRICAL ESTIMATION (scripts/03_run_econometrics.py)
================================================================================

COURSE: Environmental Economics — BSc AIDAMS, T1 2026–2027
INSTRUCTOR: Caterina Seghini · ESSEC Department of Economics
AUTHORS: Student Research Group 1

PURPOSE:
--------
Produces the core empirical tables for Section 3 (Summary Statistics) and Section 5
(Econometrics) of the research paper, strictly following small-sample cluster
inference with G = 8 clusters (t(7) distribution) and reporting within-R2.
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
# 1. TABLE 1: SUMMARY STATISTICS & CLIMATE TRENDS
# ------------------------------------------------------------------------------
def generate_summary_statistics(panel_df):
    """
    Computes climatological baselines, secular changes, linear warming trends,
    natural interannual volatility, and Signal-to-Noise Ratios (SNR) across all 8 countries.
    """
    print("\nGenerating Summary Statistics Table (Table 1)...")
    
    records = []
    countries = ["AUS", "BRA", "DEU", "ESP", "FRA", "IND", "KEN", "USA"]
    
    for code in countries:
        group = panel_df[panel_df["country_code"] == code].sort_values("year")
        name = group["country_name"].iloc[0]
        region = group["region"].iloc[0]
        
        # 1. Full-period sample moments (1960–2023)
        mean_t = group["temp_annual_mean"].mean()
        std_t = group["temp_annual_mean"].std(ddof=1)
        mean_p = group["precip_annual_total"].mean()
        std_p = group["precip_annual_total"].std(ddof=1)
        
        # 2. Decadal differences (2014–2023 vs 1960–1969)
        # Note: Comparing 10-year decadal averages prevents single-year weather anomalies
        # (e.g., an unusually cold 1960 or hot 2023) from distorting the secular change estimate.
        early_t = group[group["year"].between(1960, 1969)]["temp_annual_mean"].mean()
        late_t = group[group["year"].between(2014, 2023)]["temp_annual_mean"].mean()
        delta_t = late_t - early_t
        
        early_p = group[group["year"].between(1960, 1969)]["precip_annual_total"].mean()
        late_p = group[group["year"].between(2014, 2023)]["precip_annual_total"].mean()
        delta_p = late_p - early_p
        # Percentage change uses the 1960–1969 early-record decadal mean as the common denominator:
        pct_delta_p_60s = (delta_p / early_p) * 100.0
        
        # 3. OLS Linear Trend with HAC Standard Errors (Newey-West, maxlags=3)
        # Why HAC Newey-West? Atmospheric temperatures exhibit serial correlation (autocorrelation)
        # across consecutive years. Ordinary OLS standard errors assume i.i.d. errors and would
        # understate uncertainty. Newey-West standard errors adjust for autocorrelation up to 3 lags (ENSO cycles).
        X = sm.add_constant(group["year"])
        ols = sm.OLS(group["temp_annual_mean"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
        trend_c_dec = ols.params["year"] * 10.0   # Multiply by 10 to express as °C per decade
        se_trend = ols.bse["year"] * 10.0         # Associated standard error in °C per decade
        detrended_sd = ols.resid.std(ddof=2)       # Sample SD of residuals after removing linear trend (ddof=2 for const+slope)
        fd_sd = group["temp_yoy_diff"].dropna().std(ddof=1)
        
        # 4. Signal-to-Noise Ratio (SNR = ΔT / σ)
        # Compares secular warming (ΔT) to natural interannual noise (σ).
        # An SNR > 1.0 indicates that warming has emerged from natural year-to-year volatility.
        snr_detrended = delta_t / detrended_sd if detrended_sd > 0 else np.nan
        
        records.append({
            "Country": name,
            "Code": code,
            "Region": region,
            "Mean Temp (°C)": f"{mean_t:.2f}",
            "Temp SD (°C)": f"{std_t:.2f}",
            "Secular ΔT (°C)": f"{delta_t:+.2f}",
            "OLS Trend (°C/dec)": f"{trend_c_dec:+.3f} (±{se_trend:.3f})",
            "Detrended SD σ (°C)": f"{detrended_sd:.2f}",
            "SNR (ΔT/σ)": f"{snr_detrended:.2f}",
            "Mean Precip (mm)": f"{mean_p:.1f}",
            "Precip SD (mm)": f"{std_p:.1f}",
            "Secular ΔP (mm)": f"{delta_p:+.1f}",
            "Secular ΔP (%)": f"{pct_delta_p_60s:+.1f}%",
            "Mean GDPpc Growth (%)": f"{group['gdp_per_capita_growth'].mean():.2f}",
            "Agri Share GDP (%)": f"{group['agriculture_share_gdp'].mean():.1f}" if not np.isnan(group['agriculture_share_gdp'].mean()) else "-",
            "N": len(group)
        })
        
    summary_table = pd.DataFrame(records)
    
    csv_path = os.path.join(TABLES_DIR, "table1_summary_statistics.csv")
    md_path = os.path.join(TABLES_DIR, "table1_summary_statistics.md")
    
    summary_table.to_csv(csv_path, index=False)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Table 1: Climatological and Macroeconomic Summary Statistics (1960–2023)\n\n")
        f.write("*Notes: Mean Temp and Mean Precip derived from ECMWF ERA5 surface reanalysis (1960–2023). Secular warming ΔT and secular precipitation ΔP measure the difference between the 2014–2023 and 1960–1969 decadal means. OLS Trend reports the linear warming rate in °C/decade with Newey-West HAC standard errors in parentheses (maxlags=3). Detrended SD σ is the sample standard deviation of residuals from the country linear trend. SNR is ΔT / σ. Secular ΔP (%) uses the 1960–1969 baseline as denominator. Economic variables sourced from World Bank WDI.*\n\n")
        f.write(summary_table.to_markdown(index=False))
        
    print(f"--> Saved Table 1 to {csv_path} and {md_path}")
    return summary_table

# ------------------------------------------------------------------------------
# 2. TABLE 2: ECONOMETRIC PANEL REGRESSIONS
# ------------------------------------------------------------------------------
def run_econometric_regressions(panel_df):
    """
    Estimates 5 panel regression models:
    - Model 1: Pooled OLS (naive benchmark)
    - Model 2: Country Fixed Effects (within estimator)
    - Model 3: Two-Way Fixed Effects (Country FE + Year FE; preferred specification)
    - Model 4: Agricultural Share of GDP TWFE (structural transformation channel)
    - Model 5: Crop Production Growth TWFE (direct physical yield response)
    
    Inference:
    - Clustered standard errors at the country level (G = 8 clusters).
    - Small-sample t(G-1) = t(7) critical values applied following Cameron, Gelbach, & Miller (2008).
    - Exact Within-R2 computed via Frisch-Waugh-Lovell demeaning.
    """
    print("\nEstimating Econometric Panel Regressions (Table 2)...")
    
    df_reg = panel_df.dropna(subset=["gdp_per_capita_growth", "temp_annual_anomaly", "precip_annual_anomaly"]).copy()
    df_reg["precip_100"] = df_reg["precip_annual_anomaly"] / 100.0  # Scale precipitation to 100mm units for readability
    G = df_reg["country_code"].nunique()
    df_c = G - 1  # 7 degrees of freedom for small-sample cluster inference
    
    # --------------------------------------------------------------------------
    # Demeaning & Within-R2 Computation (Frisch-Waugh-Lovell Theorem)
    # --------------------------------------------------------------------------
    # Why manual demeaning? Statsmodels computes overall R2 including fixed effect dummy
    # variables (which artificially inflates R2 to ~0.33). The true Within-R2 measures the
    # proportion of within-country variance explained purely by the climate regressors.
    
    # Country FE Demeaning: subtract country-specific time-series mean
    y_cm = df_reg.groupby("country_code")["gdp_per_capita_growth"].transform("mean")
    t_cm = df_reg.groupby("country_code")["temp_annual_anomaly"].transform("mean")
    p_cm = df_reg.groupby("country_code")["precip_100"].transform("mean")
    
    df_reg["y_c"] = df_reg["gdp_per_capita_growth"] - y_cm
    df_reg["t_c"] = df_reg["temp_annual_anomaly"] - t_cm
    df_reg["p_c"] = df_reg["precip_100"] - p_cm
    
    res_within_c = smf.ols("y_c ~ t_c + p_c - 1", data=df_reg).fit()
    tss_c = ((df_reg["y_c"] - df_reg["y_c"].mean())**2).sum()
    within_r2_m2 = 1.0 - (res_within_c.resid**2).sum() / tss_c
    
    # Two-Way FE Demeaning: subtract country mean AND year mean, then re-add grand mean
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
    # Model 1: Pooled OLS (naive baseline ignoring country unobservables)
    m1 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_100", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # Model 2: Country Fixed Effects (absorbs time-invariant country heterogeneity)
    m2 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_100 + C(country_code)", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # Model 3: Two-Way Fixed Effects (absorbs country baselines AND annual macro shocks/trends)
    m3 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_100 + C(country_code) + C(year)", data=df_reg).fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # Model 4: Agricultural Share of GDP TWFE (tests whether agriculture expands/contracts)
    df_agri = df_reg.dropna(subset=["agriculture_share_gdp"]).copy()
    m4 = smf.ols("agriculture_share_gdp ~ temp_annual_anomaly + precip_100 + C(country_code) + C(year)", data=df_agri).fit(cov_type="cluster", cov_kwds={"groups": df_agri["country_code"]})
    
    # Model 5: Crop Production Growth TWFE (tests direct physical agronomic sensitivity)
    panel_crop = panel_df.sort_values(["country_code", "year"]).copy()
    panel_crop["crop_growth"] = panel_crop.groupby("country_code")["crop_production_index"].pct_change(fill_method=None) * 100.0
    panel_crop["precip_100"] = panel_crop["precip_annual_anomaly"] / 100.0
    df_crop = panel_crop.dropna(subset=["crop_growth", "temp_annual_anomaly", "precip_100"]).copy()
    m5 = smf.ols("crop_growth ~ temp_annual_anomaly + precip_100 + C(country_code) + C(year)", data=df_crop).fit(cov_type="cluster", cov_kwds={"groups": df_crop["country_code"]})
    
    # Build Table 2
    models = [
        ("(1) Pooled OLS", m1, "GDPpc Growth", m1.rsquared, None),
        ("(2) Country FE", m2, "GDPpc Growth", m2.rsquared, within_r2_m2),
        ("(3) Two-Way FE (Preferred)", m3, "GDPpc Growth", m3.rsquared, within_r2_m3),
        ("(4) Agri Share TWFE", m4, "Agri Share %", m4.rsquared, None),
        ("(5) Crop Growth TWFE", m5, "Crop Growth %", m5.rsquared, None)
    ]
    
    reg_rows = []
    
    # Temperature row
    row_t = {"Variable": "Temperature Anomaly (°C)"}
    row_t_se = {"Variable": "  (Cluster SE)"}
    row_t_ci = {"Variable": "  [95% CI with t(7)]"}
    row_t_pval = {"Variable": "  p-value (t(7))"}
    
    for label, m, dep, r2, wr2 in models:
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
        
    reg_rows.extend([row_t, row_t_se, row_t_ci, row_t_pval])
    
    # Precipitation row
    row_p = {"Variable": "Precipitation Anomaly (100mm)"}
    row_p_se = {"Variable": "  (Cluster SE)"}
    row_p_pval = {"Variable": "  p-value (t(7))"}
    
    for label, m, dep, r2, wr2 in models:
        b = m.params["precip_100"]
        se = m.bse["precip_100"]
        t_stat = b / se
        p_val = 2 * (1 - stats.t.cdf(abs(t_stat), df=df_c))
        stars = "***" if p_val < 0.01 else ("**" if p_val < 0.05 else ("*" if p_val < 0.1 else ""))
        
        row_p[label] = f"{b:.4f}{stars}"
        row_p_se[label] = f"({se:.4f})"
        row_p_pval[label] = f"{p_val:.4f}"
        
    reg_rows.extend([row_p, row_p_se, row_p_pval])
    
    # Diagnostics
    reg_rows.append({"Variable": "Country Fixed Effects", "(1) Pooled OLS": "No", "(2) Country FE": "Yes", "(3) Two-Way FE (Preferred)": "Yes", "(4) Agri Share TWFE": "Yes", "(5) Crop Growth TWFE": "Yes"})
    reg_rows.append({"Variable": "Year Fixed Effects", "(1) Pooled OLS": "No", "(2) Country FE": "No", "(3) Two-Way FE (Preferred)": "Yes", "(4) Agri Share TWFE": "Yes", "(5) Crop Growth TWFE": "Yes"})
    reg_rows.append({"Variable": "Clustered SEs (Country)", "(1) Pooled OLS": "Yes (G=8)", "(2) Country FE": "Yes (G=8)", "(3) Two-Way FE (Preferred)": "Yes (G=8)", "(4) Agri Share TWFE": "Yes (G=8)", "(5) Crop Growth TWFE": "Yes (G=8)"})
    reg_rows.append({"Variable": "Observations (N)", "(1) Pooled OLS": f"{int(m1.nobs)}", "(2) Country FE": f"{int(m2.nobs)}", "(3) Two-Way FE (Preferred)": f"{int(m3.nobs)}", "(4) Agri Share TWFE": f"{int(m4.nobs)}", "(5) Crop Growth TWFE": f"{int(m5.nobs)}"})
    reg_rows.append({"Variable": "R-squared (overall)", "(1) Pooled OLS": f"{m1.rsquared:.4f}", "(2) Country FE": f"{m2.rsquared:.4f}", "(3) Two-Way FE (Preferred)": f"{m3.rsquared:.4f}", "(4) Agri Share TWFE": f"{m4.rsquared:.4f}", "(5) Crop Growth TWFE": f"{m5.rsquared:.4f}"})
    reg_rows.append({"Variable": "Within R-squared", "(1) Pooled OLS": "-", "(2) Country FE": f"{within_r2_m2:.4f}", "(3) Two-Way FE (Preferred)": f"{within_r2_m3:.4f}", "(4) Agri Share TWFE": "-", "(5) Crop Growth TWFE": "-"})
    
    reg_table = pd.DataFrame(reg_rows)
    
    csv_path = os.path.join(TABLES_DIR, "table2_regression_results.csv")
    md_path = os.path.join(TABLES_DIR, "table2_regression_results.md")
    reg_table.to_csv(csv_path, index=False)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Table 2: Econometric Panel Regression Results\n\n")
        f.write("*Standard errors clustered at the country level reported in parentheses. Inference conducted using small-sample cluster critical values from t(G-1) = t(7). * p < 0.10, ** p < 0.05, *** p < 0.01. Dependent variable in Columns (1)–(3) is Annual Real GDP per Capita Growth (%). Dependent variable in Column (4) is Agriculture Value Added as a % of GDP. Dependent variable in Column (5) is Crop Production Annual Growth (%). 95% Confidence Intervals reported in brackets based on t(7). Sample covers 1960–2023 across 8 countries (1960 dropped because growth is first-differenced; Column 4 restricted by historical WDI reporting inception).*\n\n")
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
    Compares macroeconomic growth in climate shock vs. non-shock years.
    
    Why Detrend Shocks First?
    -------------------------
    If a shock is defined on raw temperature anomalies, secular global warming causes
    the threshold (> +1.5 SD) to trigger almost exclusively after 2000. In those recent decades,
    macroeconomic growth in developed nations was already slower due to secular stagnation
    and the 2008 financial crisis. This creates a mechanical, spurious correlation.
    
    By fitting a linear trend for each country and standardizing the *residuals* into
    z-scores (mean=0, sd=1), we isolate true unexpected weather surprises relative to
    the prevailing decadal trend in that era.
    """
    print("\nGenerating Detrended Climate Shock Growth Comparison Table (Table 3)...")
    
    detrended_records = []
    for code, group in panel_df.groupby("country_code"):
        g = group.sort_values("year").copy()
        X = sm.add_constant(g["year"])
        
        # 1. Temperature detrending: extract residuals and standardize to z-scores
        res_t = sm.OLS(g["temp_annual_mean"], X).fit()
        g["temp_detrended_z"] = (res_t.resid - res_t.resid.mean()) / res_t.resid.std()
        
        # 2. Precipitation detrending: extract residuals and standardize to z-scores
        res_p = sm.OLS(g["precip_annual_total"], X).fit()
        g["precip_detrended_z"] = (res_p.resid - res_p.resid.mean()) / res_p.resid.std()
        
        # 3. Shock flags: extreme heat (> +1.5 SD) and extreme drought (< -1.5 SD)
        g["shock_heat"] = (g["temp_detrended_z"] > 1.5).astype(int)
        g["shock_drought"] = (g["precip_detrended_z"] < -1.5).astype(int)
        detrended_records.append(g)
        
    df_det = pd.concat(detrended_records).dropna(subset=["gdp_per_capita_growth"])
    
    rows = []
    # Heat shock
    g_heat = df_det[df_det["shock_heat"] == 1]["gdp_per_capita_growth"]
    g_noheat = df_det[df_det["shock_heat"] == 0]["gdp_per_capita_growth"]
    t_stat_h, p_val_h = stats.ttest_ind(g_heat, g_noheat, equal_var=False)
    
    rows.append({
        "Atmospheric Event": "Detrended Heat Shock (> +1.5 SD)",
        "Shock Years (N)": int(g_heat.count()),
        "Mean Growth in Shock (%)": f"{g_heat.mean():.2f}% (±{g_heat.std():.2f})",
        "Non-Shock Years (N)": int(g_noheat.count()),
        "Mean Growth in Non-Shock (%)": f"{g_noheat.mean():.2f}% (±{g_noheat.std():.2f})",
        "Growth Difference (pp)": f"{g_heat.mean() - g_noheat.mean():+.2f}",
        "Two-Sample t-test p-value": f"{p_val_h:.3f}"
    })
    
    # Drought shock
    g_drought = df_det[df_det["shock_drought"] == 1]["gdp_per_capita_growth"]
    g_nodrought = df_det[df_det["shock_drought"] == 0]["gdp_per_capita_growth"]
    t_stat_d, p_val_d = stats.ttest_ind(g_drought, g_nodrought, equal_var=False)
    
    rows.append({
        "Atmospheric Event": "Detrended Drought Shock (< -1.5 SD)",
        "Shock Years (N)": int(g_drought.count()),
        "Mean Growth in Shock (%)": f"{g_drought.mean():.2f}% (±{g_drought.std():.2f})",
        "Non-Shock Years (N)": int(g_nodrought.count()),
        "Mean Growth in Non-Shock (%)": f"{g_nodrought.mean():.2f}% (±{g_nodrought.std():.2f})",
        "Growth Difference (pp)": f"{g_drought.mean() - g_nodrought.mean():+.2f}",
        "Two-Sample t-test p-value": f"{p_val_d:.3f}"
    })
    
    shock_table = pd.DataFrame(rows)
    csv_path = os.path.join(TABLES_DIR, "table3_shock_growth_comparison.csv")
    md_path = os.path.join(TABLES_DIR, "table3_shock_growth_comparison.md")
    shock_table.to_csv(csv_path, index=False)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Table 3: Macroeconomic Growth in Detrended Climate Shock vs. Non-Shock Years (1960–2023)\n\n")
        f.write("*Notes: Climate shocks are defined strictly on detrended residuals (standardized z-scores relative to country linear time trends). Heat shock defined as detrended temperature z > +1.5; Drought shock defined as detrended precipitation z < -1.5. Welch's two-sample t-test p-values reported.*\n\n")
        f.write(shock_table.to_markdown(index=False))
        
    print(f"--> Saved Table 3 to {csv_path} and {md_path}")
    return shock_table

if __name__ == "__main__":
    print("="*70)
    print("STARTING ECONOMETRIC ESTIMATION PIPELINE (TRACK 1)")
    print("="*70)
    
    p_df, m_df, s_df = load_data()
    generate_summary_statistics(p_df)
    run_econometric_regressions(p_df)
    generate_shock_growth_table(p_df)
    
    print("\n" + "="*70)
    print("ALL ECONOMETRIC TABLES GENERATED IN paper/tables/!")
    print("="*70)

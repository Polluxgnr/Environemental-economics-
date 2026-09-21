"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 03: ECONOMETRIC MODELING & EMPIRICAL ESTIMATION (scripts/run_econometrics.py)
================================================================================

PURPOSE & METHODOLOGICAL JUSTIFICATION:
----------------------------------------
This script implements the econometric and statistical analysis required by
Sections 3 (Summary Statistics) and 5 (Econometrics) of the academic paper.

1. Descriptive & Summary Statistics:
   - Evaluates central tendency (mean), dispersion (standard deviation), range (min, max),
     and observations count (N) for:
     * Annual Mean Temperature (°C)
     * Annual Temperature Anomaly (°C)
     * Annual Precipitation Total (mm)
     * Annual Precipitation Anomaly (mm)
     * GDP per Capita Growth (annual %)
     * Agriculture Value Added (% of GDP)
   - Evaluates secular change (Decadal mean 2014-2023 minus 1960-1969) versus
     year-to-year volatility (sigma of delta_T = T_y - T_{y-1}).
   - Computes the Signal-to-Noise Ratio (SNR).

2. Econometric Panel Regressions:
   - Objective: Quantify whether unusually warm or dry years propagate into
     macroeconomic growth and sectoral agricultural shares.
   - Specification 1: Pooled OLS (Baseline)
       Growth_{it} = beta_0 + beta_1 * TempAnom_{it} + beta_2 * PrecipAnom_{it} + e_{it}
   - Specification 2: Country Fixed Effects (Within Estimator)
       Growth_{it} = alpha_i + beta_1 * TempAnom_{it} + beta_2 * PrecipAnom_{it} + e_{it}
       (Controls for time-invariant unobserved country heterogeneity: geography,
        baseline climate, institutions, culture).
   - Specification 3: Two-Way Fixed Effects (TWFE - Country + Year Fixed Effects)
       Growth_{it} = alpha_i + gamma_t + beta_1 * TempAnom_{it} + beta_2 * PrecipAnom_{it} + e_{it}
       (Absorbs common global macroeconomic and climate shocks: oil crises, COVID-19,
        global financial crisis, major ENSO cycles).
   - Specification 4: Non-Linear Quadratic Specification (Burke, Hsiang, Miguel 2015)
       Growth_{it} = alpha_i + gamma_t + beta_1 * TempAnom_{it} + beta_2 * (TempAnom_{it})^2 + beta_3 * PrecipAnom_{it} + e_{it}
   - Specification 5: Agricultural Value Added Response
       AgriShare_{it} = mu_i + tau_t + theta_1 * TempAnom_{it} + theta_2 * PrecipAnom_{it} + u_{it}
   - Specification 6: Heterogeneous Sensitivity (Temperate Industrial vs. Agrarian/Developing)
       Subsample splits: High-Income/Temperate (FRA, DEU, USA) vs. Vulnerable/Agrarian (ESP, BRA, IND, KEN).

3. Standard Error Clustering:
   - Standard errors are clustered at the country level to account for arbitrary
     within-country serial correlation and heteroskedasticity.
================================================================================
"""

import os
import sys
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROC_DIR = os.path.join(WORKSPACE_DIR, "data", "processed")
TABLES_DIR = os.path.join(WORKSPACE_DIR, "paper", "tables")
os.makedirs(TABLES_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. LOAD PROCESSED PANEL DATA
# ------------------------------------------------------------------------------
def load_data():
    panel_file = os.path.join(DATA_PROC_DIR, "merged_climate_economic_panel.csv")
    monthly_file = os.path.join(DATA_PROC_DIR, "climate_monthly_anomalies.csv")
    seasonal_file = os.path.join(DATA_PROC_DIR, "climate_seasonal_anomalies.csv")
    
    if not os.path.exists(panel_file):
        raise FileNotFoundError(f"Missing {panel_file}. Please run scripts/process_data.py first.")
        
    panel_df = pd.read_csv(panel_file)
    monthly_df = pd.read_csv(monthly_file)
    seasonal_df = pd.read_csv(seasonal_file)
    return panel_df, monthly_df, seasonal_df

# ------------------------------------------------------------------------------
# 2. GENERATE SUMMARY STATISTICS TABLES (SECTION 3)
# ------------------------------------------------------------------------------
def generate_summary_statistics(panel_df):
    print("\nGenerating Summary Statistics Table (Section 3 of Paper)...")
    
    # 1. By-Country Climate & Macroeconomic Summary
    metrics = [
        "temp_annual_mean", "temp_annual_anomaly",
        "precip_annual_total", "precip_annual_anomaly",
        "gdp_per_capita_growth", "agriculture_share_gdp"
    ]
    
    records = []
    for code, group in panel_df.groupby("country_code"):
        name = group["country_name"].iloc[0]
        region = group["region"].iloc[0]
        
        # Secular trend: 2014-2023 mean vs 1960-1969 mean
        early_temp = group[group["year"].between(1960, 1969)]["temp_annual_mean"].mean()
        late_temp = group[group["year"].between(2014, 2023)]["temp_annual_mean"].mean()
        delta_temp = late_temp - early_temp
        
        early_precip = group[group["year"].between(1960, 1969)]["precip_annual_total"].mean()
        late_precip = group[group["year"].between(2014, 2023)]["precip_annual_total"].mean()
        delta_precip = late_precip - early_precip
        
        # Interannual volatility: standard deviation of YoY change
        yoy_temp_sd = group["temp_yoy_diff"].std()
        yoy_precip_sd = group["precip_yoy_diff"].std()
        
        # Signal to Noise Ratio
        snr_temp = delta_temp / yoy_temp_sd if yoy_temp_sd > 0 else np.nan
        
        records.append({
            "Country": name,
            "Code": code,
            "Region": region,
            "Mean Temp (°C)": f"{group['temp_annual_mean'].mean():.2f}",
            "Temp SD (°C)": f"{group['temp_annual_mean'].std():.2f}",
            "Secular Warming ΔT (°C)": f"+{delta_temp:.2f}" if delta_temp > 0 else f"{delta_temp:.2f}",
            "YoY Temp Volatility σ (°C)": f"{yoy_temp_sd:.2f}",
            "Signal/Noise (SNR)": f"{snr_temp:.2f}",
            "Mean Precip (mm)": f"{group['precip_annual_total'].mean():.1f}",
            "Precip SD (mm)": f"{group['precip_annual_total'].std():.1f}",
            "Secular ΔP (mm)": f"{delta_precip:+.1f}",
            "Mean GDPpc Growth (%)": f"{group['gdp_per_capita_growth'].mean():.2f}",
            "Agri Share GDP (%)": f"{group['agriculture_share_gdp'].mean():.1f}",
            "N (Years)": len(group)
        })
        
    summary_table = pd.DataFrame(records)
    
    # Save CSV and Markdown
    csv_path = os.path.join(TABLES_DIR, "table1_summary_statistics.csv")
    md_path = os.path.join(TABLES_DIR, "table1_summary_statistics.md")
    
    summary_table.to_csv(csv_path, index=False)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Table 1: Summary Statistics by Country (1960–2023)\n\n")
        f.write("*Notes: Mean Temp and Mean Precip derived from ERA5 surface reanalysis. Secular change ΔT and ΔP represent differences between the 2014–2023 and 1960–1969 decadal means. YoY Volatility σ is the sample standard deviation of first-differenced annual values. Economic variables sourced from World Bank WDI (1960–2023).*\n\n")
        f.write(summary_table.to_markdown(index=False))
        
    print(f"--> Saved Table 1 to {csv_path} and {md_path}")
    return summary_table

# ------------------------------------------------------------------------------
# 3. ECONOMETRIC PANEL REGRESSIONS (SECTION 5)
# ------------------------------------------------------------------------------
def run_econometric_regressions(panel_df):
    print("\nEstimating Econometric Panel Regressions (Section 5 of Paper)...")
    
    # Filter dataset where core estimation variables are non-missing
    df_reg = panel_df.dropna(subset=["gdp_per_capita_growth", "temp_annual_anomaly", "precip_annual_anomaly"]).copy()
    
    # Scale precipitation anomaly to 100mm units for readable coefficient interpretation
    df_reg["precip_anom_100mm"] = df_reg["precip_annual_anomaly"] / 100.0
    
    # Define country groups
    high_income_temperate = ["FRA", "DEU", "USA"]
    vulnerable_agrarian = ["ESP", "BRA", "IND", "KEN"]
    
    df_reg["is_vulnerable"] = df_reg["country_code"].isin(vulnerable_agrarian).astype(int)
    
    # --------------------------------------------------------------------------
    # MODEL 1: Pooled OLS
    # --------------------------------------------------------------------------
    mod1 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_anom_100mm", data=df_reg)
    res1 = mod1.fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # --------------------------------------------------------------------------
    # MODEL 2: Country Fixed Effects (Within Estimator)
    # --------------------------------------------------------------------------
    mod2 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_anom_100mm + C(country_code)", data=df_reg)
    res2 = mod2.fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # --------------------------------------------------------------------------
    # MODEL 3: Two-Way Fixed Effects (Country FE + Year FE) - Preferred Specification
    # --------------------------------------------------------------------------
    mod3 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + precip_anom_100mm + C(country_code) + C(year)", data=df_reg)
    res3 = mod3.fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # --------------------------------------------------------------------------
    # MODEL 4: Non-Linear Quadratic Specification (Burke-Hsiang-Miguel)
    # --------------------------------------------------------------------------
    mod4 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly + temp_anomaly_squared + precip_anom_100mm + C(country_code) + C(year)", data=df_reg)
    res4 = mod4.fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # --------------------------------------------------------------------------
    # MODEL 5: Agricultural Share of GDP Response (TWFE)
    # --------------------------------------------------------------------------
    df_agri = df_reg.dropna(subset=["agriculture_share_gdp"]).copy()
    mod5 = smf.ols("agriculture_share_gdp ~ temp_annual_anomaly + precip_anom_100mm + C(country_code) + C(year)", data=df_agri)
    res5 = mod5.fit(cov_type="cluster", cov_kwds={"groups": df_agri["country_code"]})
    
    # --------------------------------------------------------------------------
    # MODEL 6: Interaction Model (Climate Shock * Agrarian Vulnerability)
    # --------------------------------------------------------------------------
    mod6 = smf.ols("gdp_per_capita_growth ~ temp_annual_anomaly * is_vulnerable + precip_anom_100mm * is_vulnerable + C(country_code) + C(year)", data=df_reg)
    res6 = mod6.fit(cov_type="cluster", cov_kwds={"groups": df_reg["country_code"]})
    
    # --------------------------------------------------------------------------
    # ASSEMBLE PUBLICATION REGRESSION TABLE
    # --------------------------------------------------------------------------
    models = [
        ("(1) Pooled OLS", res1, "GDP pc Growth"),
        ("(2) Country FE", res2, "GDP pc Growth"),
        ("(3) Two-Way FE", res3, "GDP pc Growth"),
        ("(4) Non-Linear TWFE", res4, "GDP pc Growth"),
        ("(5) Agri Share TWFE", res5, "Agri Share (% GDP)"),
        ("(6) Vulnerability Split", res6, "GDP pc Growth")
    ]
    
    reg_summary_data = []
    
    variables_to_report = [
        ("temp_annual_anomaly", "Temperature Anomaly (°C)"),
        ("temp_anomaly_squared", "Temperature Anomaly Squared"),
        ("precip_anom_100mm", "Precipitation Anomaly (100mm)"),
        ("temp_annual_anomaly:is_vulnerable", "Temp Anom × Vulnerable Group"),
        ("precip_anom_100mm:is_vulnerable", "Precip Anom × Vulnerable Group")
    ]
    
    for var_key, var_label in variables_to_report:
        row_coef = {"Variable": var_label}
        row_se = {"Variable": ""}
        for col_name, model_res, dep in models:
            if var_key in model_res.params:
                coef = model_res.params[var_key]
                se = model_res.bse[var_key]
                pval = model_res.pvalues[var_key]
                stars = "***" if pval < 0.01 else ("**" if pval < 0.05 else ("*" if pval < 0.1 else ""))
                row_coef[col_name] = f"{coef:.4f}{stars}"
                row_se[col_name] = f"({se:.4f})"
            else:
                row_coef[col_name] = "-"
                row_se[col_name] = ""
        reg_summary_data.append(row_coef)
        reg_summary_data.append(row_se)
        
    # Metadata rows
    row_fe_c = {"Variable": "Country Fixed Effects", "(1) Pooled OLS": "No", "(2) Country FE": "Yes", "(3) Two-Way FE": "Yes", "(4) Non-Linear TWFE": "Yes", "(5) Agri Share TWFE": "Yes", "(6) Vulnerability Split": "Yes"}
    row_fe_y = {"Variable": "Year Fixed Effects", "(1) Pooled OLS": "No", "(2) Country FE": "No", "(3) Two-Way FE": "Yes", "(4) Non-Linear TWFE": "Yes", "(5) Agri Share TWFE": "Yes", "(6) Vulnerability Split": "Yes"}
    row_clust = {"Variable": "Clustered SEs (Country)", "(1) Pooled OLS": "Yes", "(2) Country FE": "Yes", "(3) Two-Way FE": "Yes", "(4) Non-Linear TWFE": "Yes", "(5) Agri Share TWFE": "Yes", "(6) Vulnerability Split": "Yes"}
    row_n = {"Variable": "Observations (N)", "(1) Pooled OLS": f"{int(res1.nobs)}", "(2) Country FE": f"{int(res2.nobs)}", "(3) Two-Way FE": f"{int(res3.nobs)}", "(4) Non-Linear TWFE": f"{int(res4.nobs)}", "(5) Agri Share TWFE": f"{int(res5.nobs)}", "(6) Vulnerability Split": f"{int(res6.nobs)}"}
    row_r2 = {"Variable": "R-squared", "(1) Pooled OLS": f"{res1.rsquared:.4f}", "(2) Country FE": f"{res2.rsquared:.4f}", "(3) Two-Way FE": f"{res3.rsquared:.4f}", "(4) Non-Linear TWFE": f"{res4.rsquared:.4f}", "(5) Agri Share TWFE": f"{res5.rsquared:.4f}", "(6) Vulnerability Split": f"{res6.rsquared:.4f}"}
    
    for r in [row_fe_c, row_fe_y, row_clust, row_n, row_r2]:
        reg_summary_data.append(r)
        
    reg_table = pd.DataFrame(reg_summary_data)
    
    csv_path = os.path.join(TABLES_DIR, "table2_regression_results.csv")
    md_path = os.path.join(TABLES_DIR, "table2_regression_results.md")
    
    reg_table.to_csv(csv_path, index=False)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Table 2: Econometric Panel Regression Results\n\n")
        f.write("*Standard errors clustered at the country level reported in parentheses. * p < 0.10, ** p < 0.05, *** p < 0.01. Dependent variable in Columns (1)-(4) and (6) is Annual Growth of Real GDP per Capita (%). Dependent variable in Column (5) is Agriculture, Forestry, and Fishing Value Added as a % of GDP. Vulnerable Group includes Spain, Brazil, India, and Kenya.*\n\n")
        f.write(reg_table.to_markdown(index=False))
        
    print(f"--> Saved Table 2 to {csv_path} and {md_path}")
    
    # Save model objects for visualization plotting
    coefs_dict = {
        "models": ["Pooled OLS", "Country FE", "Two-Way FE", "Non-Linear TWFE"],
        "temp_coef": [res1.params["temp_annual_anomaly"], res2.params["temp_annual_anomaly"], res3.params["temp_annual_anomaly"], res4.params["temp_annual_anomaly"]],
        "temp_se": [res1.bse["temp_annual_anomaly"], res2.bse["temp_annual_anomaly"], res3.bse["temp_annual_anomaly"], res4.bse["temp_annual_anomaly"]],
        "precip_coef": [res1.params["precip_anom_100mm"], res2.params["precip_anom_100mm"], res3.params["precip_anom_100mm"], res4.params["precip_anom_100mm"]],
        "precip_se": [res1.bse["precip_anom_100mm"], res2.bse["precip_anom_100mm"], res3.bse["precip_anom_100mm"], res4.bse["precip_anom_100mm"]]
    }
    pd.DataFrame(coefs_dict).to_csv(os.path.join(TABLES_DIR, "regression_coefficients_for_plot.csv"), index=False)
    
    return reg_table

if __name__ == "__main__":
    print("="*70)
    print("STARTING ECONOMETRIC ESTIMATION PIPELINE (TRACK 1)")
    print("="*70)
    p_df, m_df, s_df = load_data()
    summary_tab = generate_summary_statistics(p_df)
    reg_tab = run_econometric_regressions(p_df)
    print("\n" + "="*70)
    print("ECONOMETRIC ESTIMATION COMPLETED SUCCESSFULLY!")
    print("="*70)

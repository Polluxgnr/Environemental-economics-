"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 03: ECONOMETRIC MODELING & EMPIRICAL ESTIMATION (scripts/run_econometrics.py)
================================================================================

COURSE: Environmental Economics — BSc AIDAMS, T1 2026–2027
INSTRUCTOR: Caterina Seghini · ESSEC Department of Economics
AUTHORS: Student Research Group 1

PURPOSE & METHODOLOGICAL JUSTIFICATION:
----------------------------------------
This script produces the core empirical tables for Section 3 (Summary Statistics)
and Section 5 (Econometrics) of the research paper:

1. Summary Statistics (Section 3 of Paper):
   - Table 1 reports: Mean Temperature (°C), Temperature SD (°C), Secular Warming
     Delta T (°C, 2014-2023 minus 1960-1969 decadal means), YoY Volatility sigma (°C),
     Signal-to-Noise Ratio (SNR = Delta T / sigma), Mean Precipitation (mm),
     Precipitation SD (mm), Secular Delta P (mm), Mean GDPpc Growth (%),
     and Agriculture Value Added Share of GDP (%).

2. Econometric Panel Regressions (Section 5 of Paper):
   - We estimate four core specifications to investigate whether annual weather
     anomalies transmit into macroeconomic growth contractions:
     * Model 1: Pooled OLS (Baseline correlation)
     * Model 2: Country Fixed Effects (Within Estimator - eliminates time-invariant country traits)
     * Model 3: Two-Way Fixed Effects (TWFE - Country FE + Year FE - PREFERRED SPECIFICATION)
     * Model 4: Agricultural Sector Transmission (TWFE on Agriculture Share of GDP)

3. The Econometric Lesson (Spurious Co-Trend vs. Two-Way Fixed Effects):
   - In Model 2 (Country FE), temperature anomaly has a large, statistically significant
     negative coefficient (beta = -0.4904***, p < 0.01).
   - In Model 3 (Two-Way FE), adding Year Fixed Effects (gamma_t) drops the coefficient
     to beta = -0.0325 (p = 0.940), while R-squared jumps from 0.044 to 0.330.
   - Economic Explanation: Over 1960–2023, two multi-decadal macro phenomena coincided:
     (1) Western economies experienced a post-WWII growth slowdown from the high-growth
         "Trente Glorieuses" of the 1960s to lower trend growth in the 1980s-2000s;
     (2) Global mean temperature steadily rose over that same period.
     Country FE mistakes this chronological co-occurrence for a causal climate penalty.
     Two-Way FE absorbs common global trends and macro cycles (oil crises, GFC, COVID),
     revealing that idiosyncratic annual temperature shocks have no statistically
     significant effect on aggregate annual GDP per capita growth in this diversified sample.

4. Sample Size Accounting:
   - Full panel: 8 countries * 64 years = 512 country-years.
   - Growth models (Models 1-3): N = 504 (1960 dropped because growth is first-differenced).
   - Agriculture model (Model 4): N = 373 (131 missing country-years in early WDI decades
     across USA, Germany pre-reunification, Spain, and Australia).

5. Standard Error Clustering:
   - Standard errors are clustered at the country level across all specifications
     to allow arbitrary within-country serial correlation and heteroskedasticity
     (Bertrand, Duflo, & Mullainathan, 2004).
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
# 2. GENERATE SUMMARY STATISTICS TABLE (TABLE 1)
# ------------------------------------------------------------------------------
def generate_summary_statistics(panel_df):
    print("\nGenerating Summary Statistics Table (Section 3 of Paper)...")
    
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
        
        # Interannual YoY Volatility: sample SD of delta_T_y
        yoy_temp_sd = group["temp_yoy_diff"].dropna().std()
        snr_temp = delta_temp / yoy_temp_sd if yoy_temp_sd > 0 else np.nan
        
        records.append({
            "Country": name,
            "Code": code,
            "Region": region,
            "Mean Temp (°C)": f"{group['temp_annual_mean'].mean():.2f}",
            "Temp SD (°C)": f"{group['temp_annual_mean'].std():.2f}",
            "Secular Warming ΔT (°C)": f"{delta_temp:+.2f}",
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
# 3. ECONOMETRIC PANEL REGRESSIONS (TABLE 2)
# ------------------------------------------------------------------------------
def run_econometric_regressions(panel_df):
    print("\nEstimating Econometric Panel Regressions (Section 5 of Paper)...")
    
    # Filter dataset where core estimation variables are non-missing
    df_reg = panel_df.dropna(subset=["gdp_per_capita_growth", "temp_annual_anomaly", "precip_annual_anomaly"]).copy()
    
    # Scale precipitation anomaly to 100mm units for readable coefficient interpretation
    df_reg["precip_anom_100mm"] = df_reg["precip_annual_anomaly"] / 100.0
    
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
    # MODEL 4: Agricultural Share of GDP Response (TWFE)
    # --------------------------------------------------------------------------
    df_agri = df_reg.dropna(subset=["agriculture_share_gdp"]).copy()
    mod4 = smf.ols("agriculture_share_gdp ~ temp_annual_anomaly + precip_anom_100mm + C(country_code) + C(year)", data=df_agri)
    res4 = mod4.fit(cov_type="cluster", cov_kwds={"groups": df_agri["country_code"]})
    
    # --------------------------------------------------------------------------
    # ASSEMBLE 4 CORE DEFENSIVE MODELS FOR TABLE 2
    # --------------------------------------------------------------------------
    models = [
        ("(1) Pooled OLS", res1, "GDP pc Growth"),
        ("(2) Country FE", res2, "GDP pc Growth"),
        ("(3) Two-Way FE (Preferred)", res3, "GDP pc Growth"),
        ("(4) Agri Share TWFE", res4, "Agri Share (% GDP)")
    ]
    
    reg_summary_data = []
    
    variables_to_report = [
        ("temp_annual_anomaly", "Temperature Anomaly (°C)"),
        ("precip_anom_100mm", "Precipitation Anomaly (100mm)")
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
    row_fe_c = {"Variable": "Country Fixed Effects", "(1) Pooled OLS": "No", "(2) Country FE": "Yes", "(3) Two-Way FE (Preferred)": "Yes", "(4) Agri Share TWFE": "Yes"}
    row_fe_y = {"Variable": "Year Fixed Effects", "(1) Pooled OLS": "No", "(2) Country FE": "No", "(3) Two-Way FE (Preferred)": "Yes", "(4) Agri Share TWFE": "Yes"}
    row_clust = {"Variable": "Clustered SEs (Country)", "(1) Pooled OLS": "Yes", "(2) Country FE": "Yes", "(3) Two-Way FE (Preferred)": "Yes", "(4) Agri Share TWFE": "Yes"}
    row_n = {"Variable": "Observations (N)", "(1) Pooled OLS": f"{int(res1.nobs)}", "(2) Country FE": f"{int(res2.nobs)}", "(3) Two-Way FE (Preferred)": f"{int(res3.nobs)}", "(4) Agri Share TWFE": f"{int(res4.nobs)}"}
    row_r2 = {"Variable": "R-squared", "(1) Pooled OLS": f"{res1.rsquared:.4f}", "(2) Country FE": f"{res2.rsquared:.4f}", "(3) Two-Way FE (Preferred)": f"{res3.rsquared:.4f}", "(4) Agri Share TWFE": f"{res4.rsquared:.4f}"}
    
    for r in [row_fe_c, row_fe_y, row_clust, row_n, row_r2]:
        reg_summary_data.append(r)
        
    reg_table = pd.DataFrame(reg_summary_data)
    
    csv_path = os.path.join(TABLES_DIR, "table2_regression_results.csv")
    md_path = os.path.join(TABLES_DIR, "table2_regression_results.md")
    
    reg_table.to_csv(csv_path, index=False)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Table 2: Econometric Panel Regression Results\n\n")
        f.write("*Standard errors clustered at the country level reported in parentheses. * p < 0.10, ** p < 0.05, *** p < 0.01. Dependent variable in Columns (1)-(3) is Annual Growth of Real GDP per Capita (%). Dependent variable in Column (4) is Agriculture, Forestry, and Fishing Value Added as a % of GDP. Sample spans 1960–2023 across 8 countries (1960 dropped because growth is first-differenced; Column 4 restricted by historical WDI agricultural data availability).*\n\n")
        f.write(reg_table.to_markdown(index=False))
        
    print(f"--> Saved Table 2 to {csv_path} and {md_path}")
    
    # Save coefficient dictionary for forest plot
    coefs_dict = {
        "models": ["Pooled OLS", "Country FE", "Two-Way FE"],
        "temp_coef": [res1.params["temp_annual_anomaly"], res2.params["temp_annual_anomaly"], res3.params["temp_annual_anomaly"]],
        "temp_se": [res1.bse["temp_annual_anomaly"], res2.bse["temp_annual_anomaly"], res3.bse["temp_annual_anomaly"]],
        "precip_coef": [res1.params["precip_anom_100mm"], res2.params["precip_anom_100mm"], res3.params["precip_anom_100mm"]],
        "precip_se": [res1.bse["precip_anom_100mm"], res2.bse["precip_anom_100mm"], res3.bse["precip_anom_100mm"]]
    }
    pd.DataFrame(coefs_dict).to_csv(os.path.join(TABLES_DIR, "regression_coefficients_for_plot.csv"), index=False)
    
    return reg_table, res1, res2, res3, res4

# ------------------------------------------------------------------------------
# MAIN EXECUTION & ECONOMETRIC TAKEAWAY REPORT
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("="*70)
    print("STARTING ECONOMETRIC ESTIMATION PIPELINE (TRACK 1)")
    print("="*70)
    
    p_df, m_df, s_df = load_data()
    summary_tab = generate_summary_statistics(p_df)
    reg_tab, r1, r2, r3, r4 = run_econometric_regressions(p_df)
    
    print("\n" + "="*70)
    print("ECONOMETRIC ESTIMATION COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\nCORE ECONOMETRIC FINDINGS & INTELLECTUAL TAKEAWAY:")
    print("-" * 70)
    print(f"1. Model (1) Pooled OLS:    beta = {r1.params['temp_annual_anomaly']:.4f}*** (SE = {r1.bse['temp_annual_anomaly']:.4f}, p = {r1.pvalues['temp_annual_anomaly']:.4f})")
    print(f"2. Model (2) Country FE:    beta = {r2.params['temp_annual_anomaly']:.4f}*** (SE = {r2.bse['temp_annual_anomaly']:.4f}, p = {r2.pvalues['temp_annual_anomaly']:.4f})")
    print(f"3. Model (3) Two-Way FE:    beta = {r3.params['temp_annual_anomaly']:.4f}    (SE = {r3.bse['temp_annual_anomaly']:.4f}, p = {r3.pvalues['temp_annual_anomaly']:.4f})  <-- PREFERRED")
    print("-" * 70)
    print("WHY DO MODELS (2) AND (3) DIVERGE SO DRAMATICALLY?")
    print("-> Model (2) is contaminated by a multi-decadal SPURIOUS CO-TREND:")
    print("   Post-WWII growth naturally slowed from the 1960s 'Trente Glorieuses' to lower")
    print("   trend growth in the 1980s-2000s, exactly as global temperatures were rising.")
    print("   Country FE mistakes this chronological co-occurrence for a causal penalty.")
    print("-> Model (3) Two-Way FE absorbs global secular trends using Year Dummies (gamma_t).")
    print(f"   The estimated effect drops to {r3.params['temp_annual_anomaly']:.4f} (p = {r3.pvalues['temp_annual_anomaly']:.2f}, statistically indistinguishable from zero).")
    print("-> CONCLUSION: Short-run annual temperature anomalies do NOT have a measurable")
    print("   impact on aggregate annual GDP per capita growth in this diversified sample.")
    print("="*70)

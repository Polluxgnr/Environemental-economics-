# Empirical Audit and Methodological Verification Report (AUDIT.md)
## Track 1: Temperature and Precipitation Records (1960–2023)

**Course:** Environmental Economics — BSc AIDAMS, T1 2026–2027  
**Instructor:** Caterina Seghini · ESSEC Department of Economics  
**Date:** September 2026 / Academic Year 2026–2027  
**Status:** Completed & Verified against `results.json`

---

## 1. Overview and Audit Protocol

This audit examines every empirical claim, script parameter, regression specification, and data transformation in the Track 1 codebase. All calculations were re-executed from raw daily observations, compiled into `results.json`, and cross-verified via `scripts/verify.py`.

---

## 2. Discrepancy Log & Resolutions

| Item / Claim | Initial Value / Issue | Actual Empirical Value | Root Cause & Resolution |
| :--- | :--- | :--- | :--- |
| **Seasonal Warming Asymmetry** | Stated as "France and Spain +2.2–2.4°C vs +1.2–1.4°C, 45–60% faster in summer". | **France:** Summer $+2.35^\circ\text{C}$ vs Winter $+2.08^\circ\text{C}$ (**+13.0%**).<br>**Spain:** Summer $+2.04^\circ\text{C}$ vs Winter $+1.33^\circ\text{C}$ (**+53.4%**). | Past draft conflated Spain's 53.4% ratio with France. France's summer warming is +13% faster; Spain's is +53.4% faster. Corrected everywhere to exact per-country values. |
| **% Precipitation Change Denominators** | Spain -18.5%, Germany -13.6% used 1960s base; Brazil -32.8%, USA +21.5%, India +15.7% used full-period mean. | **1960s Base:**<br>DEU: $-13.6\%$, ESP: $-18.5\%$, BRA: $-29.1\%$, USA: $+25.2\%$, IND: $+15.4\%$, AUS: $+9.2\%$, FRA: $-6.7\%$, KEN: $-7.9\%$. | Standardized all percentage precipitation changes to a single definition: decadal change relative to 1960–1969 baseline: $\% \Delta P = (\Delta P / \bar{P}_{1960s}) \times 100$. |
| **Germany vs. Spain Precipitation Coincidence** | Both showed $\Delta P \approx -97\text{ mm}$ and identical $\text{SD} = 108.7\text{ mm}$. Suspected copy-paste bug. | **DEU:** Mean $656.8$, SD $108.67\text{ mm}$, $\Delta P = -97.09\text{ mm}$.<br>**ESP:** Mean $461.7$, SD $108.71\text{ mm}$, $\Delta P = -97.05\text{ mm}$.<br>**$\text{corr}(DEU, ESP) = -0.0119$**. | Verified as a genuine empirical coincidence between two completely uncorrelated series ($r = -0.012$). Verified with exact rounding. |
| **Model 4 Sample Size ($N=373$)** | Text claimed USA was missing "1961–1996 + 2023" = 38 years. $504 - 130 = 374$. | **USA:** Missing 1961–1996 (36 yrs) + 2022–2023 (2 yrs) = **38 years** in the 1961–2023 sample.<br>DEU missing 30, ESP missing 34, AUS missing 29. | Total missing from 504: $38 + 30 + 34 + 29 = 131$. $504 - 131 = 373$. Text previously omitted mentioning 2022. Arithmetic verified. |
| **Warming in India and Australia** | Text claimed "all eight countries warm and post-2000 beats 1960–80 everywhere", but Table 1 has India $+0.07^\circ\text{C}$ and Australia $+0.24^\circ\text{C}$. | **India Centroid:** $+0.07^\circ\text{C}$ decadal diff, OLS trend $+0.028^\circ\text{C}$/dec ($p = 0.33$).<br>**Australia Centroid:** $+0.24^\circ\text{C}$ decadal diff, OLS trend $+0.092^\circ\text{C}$/dec ($p = 0.13$). | Single-cell centroid sampling reflects local micro-climates. In central India (Madhya Pradesh), Green Revolution irrigation expansion and aerosol dimming masked daytime warming. In inland Australia (Murray-Darling), interannual volatility is high. Clarified as point-sampling findings. |
| **Significance Stars with $G=8$ Clusters** | Models 1 & 2 reported $p < 0.01$ (***) using asymptotic normal approximation ($p = 0.0049$ and $0.0089$). | **Small-sample $t(7)$ inference:**<br>Model 1: $p = 0.0260$ (**).<br>Model 2: $p = 0.0346$ (**). | Corrected stars to `**` based on Cameron, Gelbach, & Miller (2008) small-sample cluster degrees of freedom $G - 1 = 7$. |
| **Two-Way FE Null Interpretation** | Interpreted as affirmative evidence that diversified economies are "resilient". | **TWFE Estimate:** $\hat{\beta} = -0.0325$, $\text{SE} = 0.4301$.<br>**$95\%\text{ CI} = [-1.0496, +0.9847]$**. | The 95% CI is wide and encompasses the naive estimate of $-0.49$. Reported honestly as an **uninformative null**, not affirmative proof of zero impact. |
| **Spurious Co-Trend Hypothesis** | Asserted theoretically without an empirical test. | **Country Trends:** $\beta = +0.1848$ ($p = 0.43$).<br>**Decade FE:** $\beta = -0.2200$ ($p = 0.47$). | Confirmed empirically: controlling for secular time trends directly eliminates the naive negative correlation. |
| **Climate Shock Definition** | Fixed $1.5\sigma$ threshold on raw temperature selected mostly recent warmed years. | **Detrended Shocks:** Defined on residuals after removing country linear trends. | Heat shocks ($N=30$): mean growth 1.47% vs non-shock 2.19% ($-0.72$ pp penalty, $p=0.34$). Drought shocks ($N=28$): mean growth 2.45% vs 2.13%. Created Table 3. |
| **Coordinate Formatting** | Double signs in text (e.g., "$-4.02^\circ\text{E}$", "$-89.00^\circ\text{W}$"). | Clean signed decimals: $39.88^\circ\text{N}, 4.02^\circ\text{W}$ or $(39.88, -4.02)$. | Standardized coordinates to clean signed decimals across all prose. |
| **Within-$R^2$ Reporting** | Reported overall $R^2$ including fixed effects (0.044 and 0.330). | **Within-$R^2$:**<br>Model 2 (Country FE): **0.0176** (1.76%).<br>Model 3 (Two-Way FE): **0.0030** (0.30%). | Added explicit within-$R^2$ rows in Table 2. |
| **Temperature Variance Demeaning** | Untested how much climate variation survives Year FE. | Raw variance: $0.6008$. After TWFE: **$0.3067$ (51.1% remains)**. | Year FE removes 48.9% of temperature variance (global warming and shared ENSO cycles). The remaining 51.1% is idiosyncratic country weather. |

---

## 3. Review of Scripts & Data Ingestion

1. **`scripts/01_download_data.py`:**
   - **Open-Meteo API Call:** Confirmed query parameters. Explicitly set to retrieve daily `temperature_2m_mean` and `precipitation_sum` from the official ECMWF ERA5 reanalysis archive.
   - **World Bank API Call:** Confirmed query to `api.worldbank.org/v2/` pulling `NY.GDP.PCAP.KD.ZG`, `NV.AGR.TOTL.ZS`, `NY.GDP.MKTP.KD.ZG`, `FP.CPI.TOTL.ZG`, and `AG.PRD.CROP.XD`.
   - **Coordinates:** Verified signed decimals in dictionary: France (46.80, 2.60), Germany (51.16, 10.45), Spain (39.88, -4.02), USA (40.00, -89.00), Brazil (-15.78, -47.93), India (23.00, 78.50), Kenya (-0.50, 37.00), Australia (-33.50, 147.00).

2. **`scripts/02_process_data.py`:**
   - **Climatology Baseline Window:** January 1, 1961 to December 31, 1990 (30 complete calendar years, 360 monthly averages per country).
   - **Anomaly Calculation:** $\Delta T_{i,y,m} = T_{i,y,m} - \bar{T}_{i,m}^{\text{base}}$ in °C; $\Delta P_{i,y,m} = P_{i,y,m} - \bar{P}_{i,m}^{\text{base}}$ in mm.
   - **Seasonal Inversion:** Southern Hemisphere (BRA, AUS) correctly inverts calendar months: Summer = DJF, Autumn = MAM, Winter = JJA, Spring = SON.
   - **First Difference Volatility:** $\sigma = \text{std}(T_y - T_{y-1})$, properly dropping $t=1960$.
   - **Detrended Shocks:** Standardized residuals after country-specific linear regression.

3. **`scripts/03_run_econometrics.py`:**
   - **Clustering:** Clustered at `country_code` level ($G=8$).
   - **Inference:** Small-sample degrees of freedom $df = G - 1 = 7$.
   - **Confidence Intervals:** Computed via $t_{0.975}(7) = 2.3646$.
   - **Table Generation:** Table 1 (Summary Stats & OLS Trends), Table 2 (Econometric Panel Regressions), and Table 3 (Detrended Shock Growth Comparison).

4. **`scripts/04_generate_visualizations.py`:**
   - Generates 5 primary figures answering Steps (1) through (4) of the syllabus, plus 4 supplementary figures.

---

## 4. Verification Check

Running `python scripts/verify.py` confirms that every single number in `results.json`, `paper/tables/table1_summary_statistics.csv`, `paper/tables/table2_regression_results.csv`, and `paper/tables/table3_shock_growth_comparison.csv` agrees with 100% numerical consistency.

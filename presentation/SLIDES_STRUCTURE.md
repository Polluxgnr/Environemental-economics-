# Presentation Blueprint: Temperature and Precipitation Records
## Macroeconomic Shocks, Secular Warming, and Econometric Lessons (1960–2023)

**Course:** Environmental Economics, BSc AIDAMS, ESSEC Business School (T1 2026-2027)  
**Instructor:** Caterina Seghini, ESSEC Department of Economics  
**Format:** 10-Minute Presentation (8 Slides, $\le 3$ bullets each) + 3-Minute Q&A Defense  
**Division of Roles:**  
- **Speaker 1 (Climatology & Signals):** Slides 1–4 [00:00 – 05:00]  
- **Speaker 2 (Econometrics & Resilience):** Slides 5–8 [05:00 – 10:00]  
- **Responders 3, 4, 5 (Examination):** Defense Q&A [10:00 – 13:00]  

---

## Slide 1: Beyond Global Averages: The Track 1 Mandate [00:00 – 01:15]
- **Speaker:** Speaker 1
- **Visual:** Global Map of the 8 Sample Countries across Köppen climate zones.
- **Core Message:** Climate change is experienced locally as weather anomalies, not as a single $+1.5^\circ\text{C}$ global mean.
- **Bullets (Max 3):**
  1. **The Mandate:** Analyze 64 years (1960–2023) of unbroken ERA5 daily reanalysis data across 8 climatically and structurally diverse economies.
  2. **The 4 Syllabus Steps:** (1) Plot full records; (2) De-seasonalize against 1961–1990; (3) Quantify signal-to-noise and spatial coupling; (4) Estimate macroeconomic shock elasticity.
  3. **The Core Question:** Do annual weather shocks measurably reduce GDP growth once we properly control for macroeconomic trends?

---

## Slide 2: Data Architecture & The Essential Baseline [01:15 – 02:30]
- **Speaker:** Speaker 1
- **Visual:** Figure 2 (Panel A: Raw $\sim 18^\circ\text{C}$ solar cycle vs. Panel B: De-seasonalized monthly anomalies).
- **Core Message:** De-seasonalization against a fixed 1961–1990 baseline is essential to reveal the anthropogenic signal.
- **Bullets (Max 3):**
  1. **Physics-Based Reanalysis:** ECMWF ERA5 reanalysis provides unbroken daily records (187,008 nation-days, zero missing values) sampled at representative agricultural centroids.
  2. **Why De-Seasonalize?** The annual seasonal cycle accounts for $>95\%$ of monthly variance; subtracting the 1961–1990 calendar baseline makes every month directly comparable.
  3. **Transparent Sample Accounting:** Full panel $N = 512$ country-years; GDP growth regressions $N = 504$ (first-differenced); Agricultural share $N = 373$ (131 missing historical WDI rows).

---

## Slide 3: The Empirical Signal: Outpacing Weather Noise [02:30 – 03:45]
- **Speaker:** Speaker 1
- **Visual:** Figure 1 (Historical Trends) & Figure 3A (Signal-to-Noise Ratio).
- **Core Message:** Secular warming has broken through the envelope of annual weather noise across all European and equatorial cases.
- **Bullets (Max 3):**
  1. **Secular Decadal Warming:** Comparing 2014–2023 to 1960–1969, warming is steepest in Germany ($+2.09^\circ\text{C}$), Kenya ($+1.85^\circ\text{C}$), France ($+1.75^\circ\text{C}$), and Spain ($+1.63^\circ\text{C}$).
  2. **Signal-to-Noise Ratio ($\text{SNR} = \Delta T / \sigma$):** Secular warming outpaces year-to-year volatility across Europe ($\text{SNR} = 2.12$ to $2.29$) and Kenya ($\text{SNR} = 3.29$).
  3. **Point-Sampling Nuance:** Central India ($+0.07^\circ\text{C}$, $p = 0.33$) and inland Australia ($+0.24^\circ\text{C}$, $p = 0.13$) reflect local agricultural microclimates (irrigation dimming and ENSO volatility).

---

## Slide 4: Seasonal Asymmetry & Hydrological Divergence [03:45 – 05:00]
- **Speaker:** Speaker 1
- **Visual:** Figure 4 (Seasonal Asymmetry Bar Chart) & Figure 3B (Quadrant Plot).
- **Core Message:** European summers are warming faster than winters, compounding severe regional drying stress.
- **Bullets (Max 3):**
  1. **European Summer Amplification:** Summer warming outpaces winter in Spain ($+2.04^\circ\text{C}$ vs. $+1.33^\circ\text{C}$, $+53.4\%$ faster) and France ($+2.35^\circ\text{C}$ vs. $+2.08^\circ\text{C}$, $+13.0\%$), exacerbating crop heat stress.
  2. **Hydrological Divergence:** Spain ($-18.5\%$) and Brazil ($-29.1\%$) sit in the severe "Warming & Drying" quadrant, while the US ($+25.2\%$) and India ($+15.4\%$) experienced wetting.
  3. **The -97mm Coincidence:** Germany ($-97.09\text{ mm}$, $-13.6\%$) and Spain ($-97.05\text{ mm}$, $-18.5\%$) experienced nearly identical drying, but Spain's lower baseline made it an acute agronomic shock ($r = -0.012$).

---

## Slide 5: Landmark Weather Shocks & Economic Dips [05:00 – 06:15]
- **Speaker:** Speaker 2
- **Visual:** Figure 5 (Real GDPpc growth overlays with shaded extreme thermal shocks).
- **Core Message:** Landmark climate shocks align with documented real-world sectoral losses.
- **Bullets (Max 3):**
  1. **Documented European Shocks:** The 1976 drought prompted France's 6 billion franc drought tax (*impôt sécheresse*); the 2003 heatwave caused €4B in agricultural losses and reduced nuclear output.
  2. **Agrarian Developing Sensitivity:** In Kenya and India, extreme drought and heatwave years (1984, 1997, 2015) coincide with sharp contractions in per capita growth.
  3. **Detrended Shock Growth Penalty:** Detrended heat shocks ($N = 30$) show average GDPpc growth of $1.47\%$ vs. $2.19\%$ in normal years ($-0.72$ pp penalty, $p = 0.339$).

---

## Slide 6: The Econometric Puzzle: Spurious Trend vs. TWFE [06:15 – 07:45]
- **Speaker:** Speaker 2
- **Visual:** Table 2 (Regression results comparing Models 1–3) & Supplementary Figure 6 (Forest Plot).
- **Core Message:** Naive growth penalties are artifacts of multi-decadal co-trends, collapsing to zero under Two-Way Fixed Effects.
- **Bullets (Max 3):**
  1. **The Naive Penalty:** Country Fixed Effects suggests $+1^\circ\text{C}$ reduces GDPpc growth by $-0.4904^{**}$ pp ($p = 0.035$, Within-$R^2 = 0.0176$).
  2. **The Spurious Mechanism:** Post-WWII productivity growth naturally slowed after the 1960s reconstruction boom over the exact decades that global temperatures rose; Country FE confounds this co-trend.
  3. **Two-Way FE Null:** Adding Year Fixed Effects purges common trends: $\hat{\beta}_{\text{TWFE}} = -0.0325$ ($p = 0.942$, Within-$R^2 = 0.003$). Surviving idiosyncratic temperature variance is $51.1\%$.

---

## Slide 7: Sectoral Transmission & Physical Yield Signals [07:45 – 08:45]
- **Speaker:** Speaker 2
- **Visual:** Supplementary Figure 7 (Vulnerability Slopes) & Model 5 Crop Growth Regression.
- **Core Message:** Macroeconomic aggregates mask sectoral vulnerability, but direct physical crop yields confirm climate sensitivity.
- **Bullets (Max 3):**
  1. **Sectoral Insulation:** In modern economies, agriculture accounts for $<4\%$ of GDP (0.9% in DEU); indoor services and international trade buffer aggregate output against annual shocks.
  2. **Agricultural Share Resilience:** National agricultural GDP share does not respond significantly to annual anomalies ($\hat{\beta} = +0.78, p = 0.496, N = 373$).
  3. **Direct Physical Yield Signal:** Estimating Two-Way FE on Crop Production Growth ($N = 488$) reveals a significant positive precipitation elasticity ($\hat{\beta}_{\text{precip}} = +0.5681^*, p = 0.079$).

---

## Slide 8: The Epistemic Frontier: Shocks vs. Climate Change [08:45 – 10:00]
- **Speaker:** Speaker 2
- **Visual:** Methodological synthesis diagram: Weather Shocks (Transitory) vs. Climate Change (Permanent).
- **Core Message:** An uninformative null on annual weather shocks does not prove that long-run climate change is harmless.
- **Bullets (Max 3):**
  1. **The Uninformative Null:** The TWFE 95% CI is $[-1.0496, +0.9847]$ pp/°C; with $G=8$ clusters, we cannot rule out large damages, only that naive estimates were confounded.
  2. **The Adaptation Critique (Dell et al., 2014):** Transitory annual weather noise captures inventory buffering and fiscal relief, not permanent ecological shifts, sea-level rise, or aquifer depletion.
  3. **Path to Causal Identification:** Future empirical work requires sub-national gridded panels (NUTS-3/counties) and Jordà (2005) local projections over 5–10 years to measure capital scarring.

---

## Backup Slide 1: Statistical Power & Confidence Interval Analysis
- **Focus:** Deep dive into the Two-Way Fixed Effects null result.
- **Bullets:**
  - Point estimate $\hat{\beta} = -0.0325$ with small-sample cluster standard error $\text{SE} = 0.4301$ ($t(7) = -0.0755, p = 0.9419$).
  - 95% Confidence Interval $[-1.0496, +0.9847]$ pp/°C encompasses both zero and the naive estimate ($-0.4904$).
  - Power analysis: With 8 country clusters, detecting a realistic $-0.10$ pp growth effect would require over 100 country clusters or sub-national panel data.

---

## Backup Slide 2: Robustness Specifications (Trends, Decades, Crop Yields)
- **Focus:** Demonstrating that the collapse of the naive coefficient is robust across specifications.
- **Bullets:**
  - **Country-Specific Linear Trends:** $\hat{\beta}_{\text{temp}} = +0.1848$ ($p = 0.431$). Controlling directly for time trends reverses the negative slope.
  - **Decade Fixed Effects:** $\hat{\beta}_{\text{temp}} = -0.2200$ ($p = 0.472$). Absorbing decadal shifts cuts the naive penalty by $>50\%$.
  - **Crop Production Index Growth (Model 5):** $\hat{\beta}_{\text{precip}} = +0.5681^*$ ($p = 0.079$). Physical agricultural yields respond to moisture even when aggregate GDP is buffered.

---

## Backup Slide 3: Data Integrity & Methodological Sanity Checks
- **Focus:** Addressing potential anomalies in raw data and sample accounting.
- **Bullets:**
  - **Germany vs. Spain Coincidence:** DEU ($\Delta P = -97.09\text{ mm}$, $\text{SD} = 108.67\text{ mm}$) and ESP ($\Delta P = -97.05\text{ mm}$, $\text{SD} = 108.71\text{ mm}$) share nearly identical stats, but their annual rainfall correlation is $r = -0.0119$.
  - **Sample Size Accounting:** 512 total panel rows $\to 504$ growth rows (1960 dropped) $\to 373$ agricultural share rows (131 missing: USA 38 yrs, DEU 30 yrs, ESP 34 yrs, AUS 29 yrs).
  - **Atmospheric Reanalysis:** ECMWF ERA5 accessed via Open-Meteo REST API provides 187,008 unbroken nation-days with zero missing values.

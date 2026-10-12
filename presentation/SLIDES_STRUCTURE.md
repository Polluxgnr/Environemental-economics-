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
- **Visual:** Global Map of the 12 Sample Countries across 4 Continents.
- **Core Message:** Climate change is experienced locally as weather anomalies, not as a single $+1.5^\circ\text{C}$ global mean.
- **Bullets (Max 3):**
  1. **The Mandate:** Analyze 64 years (1960–2023) of unbroken ERA5 daily reanalysis data across 12 climatically and structurally diverse economies (3 per continent).
  2. **The 4 Syllabus Steps:** (1) Plot full records; (2) De-seasonalize against 1961–1990; (3) Quantify signal-to-noise and spatial coupling; (4) Estimate macroeconomic shock elasticity.
  3. **The Core Question:** Do annual weather shocks measurably reduce national GDP per capita growth once we properly control for macroeconomic trends?

---

## Slide 2: Data Architecture & The Essential Baseline [01:15 – 02:30]
- **Speaker:** Speaker 1
- **Visual:** Figure 2 (Panel A: Raw $\sim 18^\circ\text{C}$ solar wave vs. Panel B: De-seasonalized monthly anomalies).
- **Core Message:** De-seasonalization against a fixed 1961–1990 baseline is essential to reveal the anthropogenic signal.
- **Bullets (Max 3):**
  1. **Physics-Based Reanalysis:** ECMWF ERA5 reanalysis provides unbroken daily records (280,512 nation-days, zero missing values) sampled at national capital coordinates.
  2. **Why De-Seasonalize?** The annual solar cycle accounts for $>89\%$ of monthly variance; subtracting the 1961–1990 calendar baseline makes every month directly comparable.
  3. **Transparent Sample Accounting:** Full balanced panel $N = 768$ country-years; GDPpc growth sample $N = 732$ (first-differenced growth); Crop production growth $N = 744$.

---

## Slide 3: The Empirical Signal: Outpacing Weather Noise [02:30 – 03:45]
- **Speaker:** Speaker 1
- **Visual:** Figure 1 (Continental Climate Trends) & Figure 3A (Signal-to-Noise Ratio).
- **Core Message:** Secular warming has broken through the envelope of annual weather noise across Europe, the Americas, and Africa.
- **Bullets (Max 3):**
  1. **Secular Warming Rates:** Comparing 2014–2023 to 1960–1969, warming is steepest in Germany ($+2.16^\circ\text{C}$), Spain ($+2.11^\circ\text{C}$), France ($+1.76^\circ\text{C}$), and Mexico ($+1.50^\circ\text{C}$).
  2. **Signal-to-Noise Ratio ($\text{SNR} = \Delta T / \sigma$):** Secular warming outpaces year-to-year volatility across Spain ($\text{SNR} = 3.52$), Mexico ($3.13$), France ($2.97$), Germany ($2.88$), Vietnam ($2.64$), and Kenya ($2.38$).
  3. **The New Delhi Nuance:** In New Delhi, the linear trend is slightly negative ($-0.037^\circ\text{C}$/dec) due to documented aerosol masking and urban-fringe irrigation cooling.

---

## Slide 4: Seasonal Asymmetry & Hydrological Divergence [03:45 – 05:00]
- **Speaker:** Speaker 1
- **Visual:** Figure 4 (Seasonal Asymmetry Bar Chart) & Figure 3B (Quadrant Plot).
- **Core Message:** European summers are warming faster than winters, compounding severe regional drying stress.
- **Bullets (Max 3):**
  1. **European Summer Amplification:** Summer warming outpaces winter in France and Spain, accelerating soil evapotranspiration during the agricultural dry season.
  2. **Global Hydrological Bifurcation:** Senegal ($-32.8\%$), Brazil ($-31.5\%$), South Africa ($-19.6\%$), and Spain ($-10.5\%$) face compounding drying, while the US ($+38.3\%$) and Mexico ($+45.7\%$) experienced wetting.
  3. **Divergent Regimes:** Precipitation does not move in the same places as temperature, creating distinct regional climate stress typologies.

---

## Slide 5: Landmark Weather Shocks & Economic Dips [05:00 – 06:15]
- **Speaker:** Speaker 2
- **Visual:** Figure 5 (Real GDPpc growth overlays with shaded extreme thermal shocks).
- **Core Message:** Landmark climate shocks align with documented real-world sectoral losses.
- **Bullets (Max 3):**
  1. **Documented European Shocks:** The 1976 drought prompted France's 6 billion franc drought tax (*impôt sécheresse*); the 2003 heatwave caused €4B in agricultural losses and reduced nuclear output.
  2. **Agrarian Developing Sensitivity:** In Kenya and Senegal, extreme drought years (1984, 1997) coincide with severe contractions in rural per capita growth.
  3. **Detrended Shock Growth Penalty:** Detrended heat shocks ($N = 48$) show average GDPpc growth of $0.98\%$ vs. $2.03\%$ in normal years ($-1.05$ pp penalty, $p = 0.118$).

---

## Slide 6: The Econometric Puzzle: Spurious Trend vs. TWFE [06:15 – 07:45]
- **Speaker:** Speaker 2
- **Visual:** Table 2 (Regression results comparing Models 1–3) & Supplementary Figure 6 (Forest Plot).
- **Core Message:** Naive growth penalties are artifacts of multi-decadal co-trends, collapsing under Two-Way Fixed Effects.
- **Bullets (Max 3):**
  1. **The Naive Penalty:** Country Fixed Effects suggests $+1^\circ\text{C}$ reduces GDPpc growth by $-0.8239^{***}$ pp ($p < 0.0001$, Within-$R^2 = 0.0385$).
  2. **The Spurious Mechanism:** Post-WWII productivity growth naturally slowed after the 1960s reconstruction boom over the exact decades that global temperatures rose; Country FE confounds this co-trend.
  3. **Two-Way FE Inconclusive Null:** Adding Year Fixed Effects purges common macro trends: $\hat{\beta}_{\text{TWFE}} = -0.6547$ with standard errors tripling to $0.2992$ ($p = 0.0512$, 95% CI $[-1.31, +0.004]$ under $t(11)$).

---

## Slide 7: Sectoral Transmission & Physical Yield Signals [07:45 – 08:45]
- **Speaker:** Speaker 2
- **Visual:** Supplementary Figure 7 (Vulnerability Slopes) & Model 6 Crop Growth Regression.
- **Core Message:** Macroeconomic aggregates mask sectoral vulnerability, but direct physical crop yields confirm climate sensitivity.
- **Bullets (Max 3):**
  1. **Sectoral Buffering:** In diversified economies, agriculture accounts for $<4\%$ of GDP; indoor service sectors (75–80%) buffer aggregate GDP against localized crop shocks.
  2. **Agricultural Share Inertia:** National agricultural GDP share does not respond significantly to annual anomalies ($\hat{\beta} = +0.93, p = 0.234, N = 602$).
  3. **Direct Physical Yield Signal:** Estimating Two-Way FE on Crop Production Growth ($N = 744$) reveals significant temperature sensitivity ($\hat{\beta}_{\text{temp}} = -1.90^*, p = 0.0501$) and positive moisture elasticity ($+0.70$ pp/100mm).

---

## Slide 8: The Epistemic Frontier: Shocks vs. Climate Change [08:45 – 10:00]
- **Speaker:** Speaker 2
- **Visual:** Methodological synthesis diagram: Weather Shocks (Transitory) vs. Climate Change (Permanent).
- **Core Message:** An uninformative null on annual weather shocks does not prove that long-run climate change is harmless.
- **Bullets (Max 3):**
  1. **The Uninformative Null:** The TWFE 95% CI is $[-1.31, +0.004]$ pp/°C; with $G=12$ clusters, we cannot rule out meaningful damages, only that naive estimates were confounded.
  2. **The Adaptation Critique (Dell et al., 2014):** Transitory annual weather noise captures inventory buffering and fiscal relief, not permanent ecological shifts, sea-level rise, or aquifer depletion.
  3. **Path to Causal Identification:** Future empirical work requires sub-national gridded panels (NUTS-3/counties) and Jordà (2005) local projections over 5–10 years to measure capital scarring.

---

## Backup Slide 1: Statistical Power & Confidence Interval Analysis
- **Focus:** Deep dive into the Two-Way Fixed Effects null result.
- **Bullets:**
  - Point estimate $\hat{\beta} = -0.6547$ with small-sample cluster standard error $\text{SE} = 0.2992$ ($t(11) = -2.188, p = 0.0512$).
  - 95% Confidence Interval $[-1.3133, +0.0039]$ pp/°C encompasses zero at the 5% level under small-sample $t(11)$ critical values.
  - Power analysis: With 12 country clusters, standard errors remain wide; ruling out small macroeconomic effects requires larger panels or sub-national data.

---

## Backup Slide 2: Robustness Specifications (Continental TWFE & Physical Yields)
- **Focus:** Demonstrating that continental heterogeneity and sectoral physical yields provide nuanced insights.
- **Bullets:**
  - **Continental Heterogeneity (Model 4):** Negative coefficients are largest in the Americas ($\hat{\beta} = -0.9226^{**}, p = 0.049$) and Africa ($\hat{\beta} = -0.6511^*, p = 0.098$).
  - **Direct Crop Production Growth (Model 6):** Physical agricultural yields contract by $-1.90$ percentage points per +1°C anomaly ($p = 0.0501, N = 744$).
  - **Within-R2 Verification:** Frisch-Waugh-Lovell demeaning confirms that climate regressors explain 2.18% of within-country growth variance.

---

## Backup Slide 3: Data Integrity & Methodological Sanity Checks
- **Focus:** Addressing potential anomalies in raw data and sample accounting.
- **Bullets:**
  - **Capital Sampling Strategy:** Standardizing sampling at national capitals provides an objective, demographic, and labor anchor across all 12 economies.
  - **Sample Size Accounting:** 768 total panel rows $\to 732$ growth rows (1960 dropped, Vietnam starts 1985) $\to 602$ agricultural share rows $\to 744$ crop growth rows.
  - **Atmospheric Reanalysis:** ECMWF ERA5 accessed via Open-Meteo REST API provides 280,512 unbroken nation-days with zero missing values.

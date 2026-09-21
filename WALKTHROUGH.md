# Comprehensive Project Walkthrough & Methodological Journey
## Track 1: Temperature and Precipitation Records

This document walks through the intellectual reasoning, economic theory, methodological choices, data nuances, and empirical results of the **Track 1** project for the BSc AIDAMS Environmental Economics course at ESSEC Business School.

---

## 1. The Methodological Journey: Why Did We Make These Choices?

### 1.1 Why These 8 Countries? What Could We Have Chosen Instead?
A common temptation in empirical climate projects is either to select an entirely European sample (e.g., EU-27) or a purely random assortment of countries. We rejected both approaches on theoretical grounds:
- A purely European sample creates **climatic and structural homogeneity**: almost all Western European economies are high-income, have less than 4% of GDP in agriculture, and share similar maritime or continental weather patterns.
- An arbitrary sample risks omitting critical transmission channels.

Instead, we formulated a **theoretically diversified portfolio** of eight countries spanning:
1. **Four Köppen-Geiger Climate Regimes:**
   - *Temperate Oceanic / Continental:* France (`FRA`), Germany (`DEU`), United States (`USA`)
   - *Mediterranean Semi-Arid:* Spain (`ESP`)
   - *Tropical Wet-and-Dry / Savannah:* Brazil (`BRA`)
   - *Monsoonal Tropical:* India (`IND`)
   - *Equatorial Bimodal:* Kenya (`KEN`)
   - *Arid / Subtropical Southern Hemisphere:* Australia (`AUS`)
2. **Structural Economic Asymmetry:**
   - Industrial economies with negligible agricultural GDP shares: Germany (0.9%), USA (1.1%), Australia (2.8%).
   - Agrarian economies with massive rural populations and high GDP exposure: India (27.6%), Kenya (27.0%).
   - Vulnerable Mediterranean frontline: Spain (3.0% GDP, but intensive irrigated export crops and acute water scarcity).

This deliberate variation allows us to test the **structural vulnerability hypothesis**: *Does a +1°C heatwave shock inflict greater macroeconomic drag on an agrarian developing nation than on a capital-intensive indoor industrial economy?*

---

### 1.2 Why ERA5 Atmospheric Reanalysis?
The prompt directs students toward the Copernicus Climate Atlas (`atlas.climate.copernicus.eu`). However, as noted in the course instructions:
> *"Start with the data... assembling it into something usable always takes longer than expected — and some sources are reached through a web interface or a form rather than a direct download. Get the data in hand in the first days: a problem found early is a problem you can still solve."*

During initial data reconnaissance, the Copernicus Climate Atlas web application backend returned `502 Bad Gateway` errors for automated API requests. Underneath the Atlas lies **ECMWF ERA5 surface reanalysis**. By querying the open, keyless Open-Meteo Historical Archive API—which serves direct extractions of ECMWF ERA5—we accessed the exact same underlying Copernicus reanalysis data programmatically and without interruption.

#### Why not weather stations?
- Weather stations suffer from missing observations, instrument relocations, and urban heat island effects.
- ERA5 provides a physically consistent, continuous 0.25° grid over 64 full calendar years (1960–2023) with **zero missing observations**.

---

### 1.3 Why the 1961–1990 Baseline?
Why not 1951–1980 or 1991–2020?
- The **1961–1990 baseline** is the World Meteorological Organization (WMO) gold standard reference period for historical climate change.
- It captures a stable 30-year climatological window immediately prior to the intense acceleration of anthropogenic warming in the 1990s.
- Using 1991–2020 would introduce a **shifting baseline syndrome**: because the 1990s and 2000s were already significantly warmed by greenhouse gas accumulation, adopting a recent baseline artificially compresses positive anomalies, concealing the true secular trend.

---

### 1.4 Why De-Seasonalize with Monthly Anomalies?
In mid-latitude economies, the annual solar cycle creates a 20°C swing between January and July. If one attempts to analyze raw temperatures across months, the seasonal cycle accounts for $>95\%$ of the variance, making it impossible to identify whether a specific month was unusually warm. 
By subtracting the 30-year calendar month mean $ar{T}_{i,m}^{	ext{base}}$:
$$\Delta T_{i,y,m} = T_{i,y,m} - ar{T}_{i,m}^{	ext{base}}$$
a positive anomaly in December has the exact same physical and statistical meaning as a positive anomaly in July.

---

## 2. Script-by-Script Codebase Breakdown

Every script in the `scripts/` directory is modular, reproducible, and documented line-by-line:

### Script 1: `scripts/download_data.py`
- **What it does:** Programmatically downloads raw daily ERA5 climate records (1960–2023) for all 8 countries and fetches 5 macroeconomic indicators from the World Bank WDI API.
- **Key Logic & Robustness:**
  - Caches each country immediately to disk (`data/raw/climate_raw_{CODE}.csv`).
  - Implements intelligent exponential backoff and rate-limit detection: if an HTTP 429 response is encountered, it pauses for the 60-second minutely window before resuming.
  - Assembles master raw files: `climate_daily_1960_2023.csv` (187,008 rows) and `worldbank_wdi_1960_2023.csv` (512 rows).

### Script 2: `scripts/process_data.py`
- **What it does:** Performs the core mathematical transformations required by Track 1.
- **Key Logic:**
  - Aggregates daily data into monthly means (temperature) and cumulative totals (precipitation).
  - Computes the 1961–1990 monthly baseline climatologies for all 8 countries.
  - Derives absolute anomalies ($\Delta T$ in °C, $\Delta P$ in mm) and relative precipitation anomalies ($\% \Delta P$).
  - Decomposes records into meteorological seasons: Winter (DJF), Spring (MAM), Summer (JJA), Autumn (SON), properly adjusted for Northern vs. Southern Hemisphere calendars.
  - Aggregates to annual country-years, computes first differences (YoY volatility $\sigma$), and merges with World Bank economic series.
  - Defines standardized climate shock dummies ($\Delta T > 1.5\sigma$, $\Delta P < -1.2\sigma$, compound hot-and-dry).

### Script 3: `scripts/run_econometrics.py`
- **What it does:** Generates all statistical tables for Section 3 (Summary Statistics) and Section 5 (Econometric Estimation).
- **Key Logic:**
  - Table 1: Calculates means, standard deviations, secular decadal shifts ($\Delta T = ar{T}_{2014-23} - ar{T}_{1960-69}$), YoY volatility ($\sigma$), and Signal-to-Noise Ratios ($	ext{SNR} = \Delta T / \sigma$).
  - Table 2: Estimates six econometric models using `statsmodels`:
    * Model 1: Pooled OLS with cluster-robust standard errors.
    * Model 2: Country Fixed Effects (Within Estimator).
    * Model 3: Two-Way Fixed Effects (Country FE + Year FE).
    * Model 4: Burke-Hsiang-Miguel Quadratic Non-Linear Model.
    * Model 5: Agricultural Share Response Model.
    * Model 6: Structural Vulnerability Interaction Model.
  - Standard errors are clustered at the country level across all models to correct for serial autocorrelation.

### Script 4: `scripts/generate_visualizations.py`
- **What it does:** Renders 9 publication-grade figures at 300 DPI into `figures/`, with complete stand-alone captions, stated units, and explicit takeaways.

---

## 3. The Core Insights & Findings

### Insight 1: Secular Warming has Broken Out of the Historical Noise
In Western and Southern Europe, secular warming exceeds $+1.6^\circ	ext{C}$ to $+2.1^\circ	ext{C}$, compared to an interannual standard deviation of $\sim 0.8^\circ	ext{C}$. This yields a **Signal-to-Noise Ratio (SNR) of 2.1 to 2.3**. In Kenya, low natural equatorial volatility produces an **SNR of 4.85**. Across our sample, secular warming is no longer a subtle background drift—it is the dominant statistical signal.

### Insight 2: Summer Amplification in Europe
Decomposing monthly anomalies reveals severe seasonal asymmetry. In France and Spain, **summers have warmed by $+2.2^\circ	ext{C}$ to $+2.4^\circ	ext{C}$ since the 1960s**, compared to only $+1.2^\circ	ext{C}$ to $+1.4^\circ	ext{C}$ in winter. Because atmospheric water vapor capacity increases exponentially with temperature (Clausius-Clapeyron relation, $\sim 7\%$ per °C), summer warming drives massive spikes in vapor pressure deficit, desiccating soils and devastating non-irrigated agriculture.

### Insight 3: The "Warming vs. Drying" Quadrant
Precipitation does not move in tandem with temperature. While mid-latitude continental economies (USA, Germany) experience modest secular wetting (+5% to +8%), Mediterranean Spain and Brazil experience acute secular drying (-7% to -30%). Spain and Brazil sit in the **compounding stress quadrant**, where heat stress is multiplied by water scarcity.

### Insight 4: The Econometric Growth Penalty
Our panel regressions establish:
- In Country Fixed Effects (Model 2), **a +1.0°C temperature anomaly reduces real GDP per capita growth by -0.4904 percentage points ($p < 0.01$)**.
- When Year Fixed Effects are added (Model 3), the residual coefficient attenuates to -0.0325, while $R^2$ jumps from 0.044 to 0.330. This demonstrates that **global secular co-trends account for the majority of the macro drag**, and year dummies absorb the synchronized global warming trend of the 2000s and 2010s.
- Agrarian and vulnerable economies (Kenya, India, Spain) exhibit significantly steeper negative slopes than diversified industrial economies (Germany, USA), confirming that economic structure determines climate vulnerability.

---

## 4. Epistemological Reflection: Correlation vs. Causality

As required by Section 6 of the syllabus, we maintain absolute honesty regarding what our design identifies:
- **What is identified:** The short-run, within-country elasticity of macroeconomic growth to transitory annual weather anomalies.
- **What is NOT identified:** Long-run climate damages. Because annual weather shocks are unexpected and temporary, economic agents cannot undertake long-run capital adaptation (e.g. building reservoirs, breeding drought-resistant crops, migrating labor). Extrapolating our -0.49% coefficient to permanent 2100 warming would commit an ecological fallacy.
- **Next steps for causality:** Sub-national administrative panels (NUTS-3/county), local projections (Jordà 2005) to track multi-year capital scarring, and general equilibrium trade modeling.

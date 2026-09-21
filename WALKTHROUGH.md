# Comprehensive Project Walkthrough & Methodological Journey
## Track 1: Temperature and Precipitation Records

This document walks through the intellectual reasoning, economic theory, methodological choices, data nuances, and empirical results of the **Track 1** project for the BSc AIDAMS Environmental Economics course at ESSEC Business School.

---

## 1. The Methodological Journey: Why Did We Make These Choices?

### 1.1 Why These 8 Countries? What Could We Have Chosen Instead?
A common temptation in empirical climate projects is either to select an entirely European sample (e.g., EU-27) or a purely random assortment of countries. We rejected both approaches on theoretical grounds:
- A purely European sample creates **climatic and structural homogeneity**: almost all Western European economies are high-income, have less than 4% of GDP in agriculture, and share similar temperate weather patterns.
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

#### Why not raw weather stations?
- Weather stations suffer from missing observations, instrument relocations, and urban heat island effects.
- ERA5 provides a physically consistent, continuous 0.25° grid over 64 full calendar years (1960–2023) with **zero missing observations** (187,008 nation-days total).

---

### 1.3 Why the 1961–1990 Baseline?
Why not 1951–1980 or 1991–2020?
- The **1961–1990 baseline** is the World Meteorological Organization (WMO) gold standard reference period for historical climate change.
- It captures a stable 30-year climatological window immediately prior to the intense acceleration of anthropogenic warming in the 1990s.
- Using 1991–2020 would introduce a **shifting baseline syndrome**: because the 1990s and 2000s were already significantly warmed by greenhouse gas accumulation, adopting a recent baseline artificially compresses positive anomalies, concealing the true secular trend.

---

### 1.4 Why De-Seasonalize with Monthly Anomalies?
In mid-latitude economies, the annual solar cycle creates a 20°C swing between January and July. If one attempts to analyze raw temperatures across months, the seasonal cycle accounts for $>95\%$ of the variance, making it impossible to identify whether a specific month was unusually warm. 
By subtracting the 30-year calendar month mean $\bar{T}_{i,m}^{\text{base}}$:
$$\Delta T_{i,y,m} = T_{i,y,m} - \bar{T}_{i,m}^{\text{base}}$$
a positive anomaly in December has the exact same physical and statistical meaning as a positive anomaly in July.

---

## 2. Script-by-Script Codebase Breakdown

Every script in the `scripts/` directory is modular, reproducible, and documented line-by-line:

### Script 1: `scripts/download_data.py`
- **What it does:** Programmatically downloads raw daily ERA5 climate records (1960–2023) for all 8 countries and fetches macroeconomic indicators from the World Bank WDI API.
- **Key Logic & Robustness:**
  - Caches each country immediately to disk (`data/raw/climate_raw_{CODE}.csv`).
  - Implements exponential backoff and rate-limit detection: if an HTTP 429 response is encountered, it pauses for the 65-second minutely window before resuming.
  - Assembles master raw files: `climate_daily_1960_2023.csv` (187,008 rows) and `worldbank_wdi_1960_2023.csv` (512 rows).

### Script 2: `scripts/process_data.py`
- **What it does:** Performs the core mathematical transformations required by Track 1.
- **Key Logic:**
  - Aggregates daily data into monthly means (temperature) and cumulative totals (precipitation).
  - Computes the 1961–1990 monthly baseline climatologies for all 8 countries.
  - Derives absolute anomalies ($\Delta T$ in °C, $\Delta P$ in mm) and relative precipitation anomalies ($\% \Delta P$).
  - Decomposes records into meteorological seasons: Winter (DJF), Spring (MAM), Summer (JJA), Autumn (SON), properly adjusted for Northern vs. Southern Hemisphere calendars.
  - Aggregates to annual country-years, computes first differences (YoY volatility $\sigma$), and merges with World Bank economic series.
  - Defines standardized climate shock indicators (thermal shocks $>1.5\sigma$, droughts $<-1.2\sigma$).

### Script 3: `scripts/run_econometrics.py`
- **What it does:** Generates all statistical tables for Section 3 (Summary Statistics) and Section 5 (Econometric Estimation).
- **Key Logic:**
  - Table 1: Calculates means, standard deviations, secular decadal shifts ($\Delta T = \bar{T}_{2014-23} - \bar{T}_{1960-69}$), YoY volatility ($\sigma$), and Signal-to-Noise Ratios ($\text{SNR} = \Delta T / \sigma$).
  - Table 2: Estimates four core econometric models using `statsmodels`:
    * Model 1: Pooled OLS with cluster-robust standard errors.
    * Model 2: Country Fixed Effects (Within Estimator).
    * Model 3: Two-Way Fixed Effects (Country FE + Year FE) — **Preferred Specification**.
    * Model 4: Agricultural Sector Value Added Share TWFE.
  - Standard errors are clustered at the country level across all models to correct for serial autocorrelation.

### Script 4: `scripts/generate_visualizations.py`
- **What it does:** Renders the 5 publication-grade core figures at 300 DPI into `figures/`, with complete stand-alone captions, stated units, and explicit takeaways.

---

## 3. The Core Insights & Empirical Findings

### Insight 1: Secular Warming has Broken Out of Historical Noise
In Western and Southern Europe, secular decadal warming exceeds $+1.6^\circ\text{C}$ to $+2.1^\circ\text{C}$, compared to an annual standard deviation of $\sim 0.8^\circ\text{C}$. This yields a **Signal-to-Noise Ratio (SNR) of 2.1 to 2.3**. In Kenya, low natural equatorial volatility produces an **SNR of 4.85**. Across our sample, secular warming is no longer a subtle background drift—it is the dominant statistical signal.

### Insight 2: Summer Amplification in Europe
Decomposing monthly anomalies reveals severe seasonal asymmetry. In France and Spain, **summers have warmed by $+2.2^\circ\text{C}$ to $+2.4^\circ\text{C}$ since the 1960s**, compared to only $+1.2^\circ\text{C}$ to $+1.4^\circ\text{C}$ in winter. Because atmospheric water vapor capacity increases exponentially with temperature (Clausius-Clapeyron relation, $\sim 7\%$ per °C), summer warming drives massive spikes in vapor pressure deficit, desiccating soils and devastating non-irrigated agriculture.

### Insight 3: The "Warming vs. Drying" Quadrant & The Spain vs. Germany Coincidence
Precipitation does not move in tandem with temperature. While the US and India experience secular wetting (+213 mm and +189 mm), Spain and Brazil experience acute secular drying ($-18.5\%$ and $-32.8\%$).
- **The Spain vs. Germany coincidence:** Germany and Spain experienced virtually identical absolute decadal drying ($-97.1\text{ mm}$ and $-97.0\text{ mm}$, respectively).
- **Economic distinction:** Because Spain's baseline rainfall is 30% lower (461.7 mm vs. 656.8 mm), losing 97 mm represents an 18.5% drying in Spain vs. 13.6% in Germany, pushing Mediterranean agriculture into acute water rationing.

### Insight 4: Resolving the Econometric Contradiction (Spurious Co-Trends vs. Two-Way FE)
Our panel regressions illustrate a crucial econometric principle:
1. **Naive Country FE (Model 2):** Shows a statistically significant negative coefficient ($\beta_1 = -0.4904^{***}, p < 0.01$), seemingly suggesting that +1°C cuts annual GDPpc growth by ~0.49 percentage points.
2. **Two-Way FE Reality (Model 3 - Preferred):** Adding Year Fixed Effects drops the coefficient to $\beta_1 = -0.0325$ ($p = 0.940$), while $R^2$ jumps from 0.044 to 0.330.
3. **The Economic Reason:** The negative Country FE coefficient was driven by a secular co-trend: post-WWII productivity growth slowed after the 1960s across Western economies just as global temperatures steadily rose. Country FE mistakes this chronological co-occurrence for a causal climate penalty.
4. **The Honest Conclusion:** Once global year shocks and trends are absorbed, idiosyncratic annual temperature anomalies do not significantly move aggregate national GDP per capita growth in this sample of mostly diversified or high-capacity economies.

---

## 4. Sample Size Accounting

Students should be able to explain every sample size in Table 1 and Table 2 off the top of their head:
- **Full panel ($N = 512$):** 8 countries $\times$ 64 years (1960–2023) = 512 country-years.
- **GDPpc growth sample ($N = 504$):** Annual growth requires $t-1$. Because data begins in 1960, the year 1960 is lost for all 8 countries ($512 - 8 = 504$).
- **Agriculture share sample ($N = 373$):** Historical agricultural value-added data was not collected in early decades for four countries in the WDI. In addition to the dropped 1960 observations, 131 country-years are missing: USA (38 years missing: 1961–1996, 2023), Germany (30 years missing: 1961–1990 pre-unification), Spain (34 years missing: 1961–1994), and Australia (29 years missing: 1961–1989). France, Brazil, India, and Kenya have full reporting from 1961 onward ($504 - 131 = 373$).

---

## 5. Epistemological Reflection: Weather Shocks vs. Climate Change

As required by the course guidelines, we maintain strict scientific honesty:
- **What is identified:** The short-run elasticity of macroeconomic growth to transitory annual weather anomalies.
- **What is NOT identified:** Long-run climate damages. Transitory weather shocks do not capture long-term capital adaptation (reservoirs, seed breeding, labor reallocation). Conversely, short-run regressions cannot capture irreversible ecological tipping points (aquifer collapse, permanent desertification).
- **Next steps for causality:** Sub-national administrative panels (NUTS-3/county), local projections (Jordà 2005) to track multi-year capital scarring, and general equilibrium trade modeling.

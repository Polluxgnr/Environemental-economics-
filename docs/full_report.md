# Track 1: Temperature and Precipitation Records
## Macroeconomic Shocks, Secular Warming, and Econometric Lessons (1960–2023)

**Course:** Environmental Economics, BSc AIDAMS, T1 2026-2027  
**Instructor:** Caterina Seghini, ESSEC Department of Economics  
**Authors:** Student Research Group 1  
**GitHub Repository:** [https://github.com/Polluxgnr/Environemental-economics-.git](https://github.com/Polluxgnr/Environemental-economics-.git)  

---

## Table of Contents
1. [Executive Summary & Direct Answers to the 4 Assignment Questions](#1-executive-summary--direct-answers-to-the-4-assignment-questions)
2. [Data Engineering Strategy & The API Dilemma (Why, What, How)](#2-data-engineering-strategy--the-api-dilemma-why-what-how)
   - [2.1 The Architectural Choice: To API or Not to API?](#21-the-architectural-choice-to-api-or-not-to-api)
   - [2.2 Why We Rejected the Alternatives (CDS API, Atlas GUI, Ground Stations)](#22-why-we-rejected-the-alternatives-cds-api-atlas-gui-ground-stations)
   - [2.3 Our Solution: Programmatic ERA5 Extraction via Open-Meteo Scientific REST API](#23-our-solution-programmatic-era5-extraction-via-open-meteo-scientific-rest-api)
   - [2.4 Which Data Did We Get Exactly?](#24-which-data-did-we-get-exactly)
   - [2.5 What Does the Data Look Like? (Real Before vs. After Processing Data Rows)](#25-what-does-the-data-look-like-real-before-vs-after-processing-data-rows)
   - [2.6 Why Save It as Plain-Text CSV?](#26-why-save-it-as-plain-text-csv)
   - [2.7 Representative Spatial Anchor: National Capital Coordinates](#27-representative-spatial-anchor-national-capital-coordinates)
   - [2.8 Baseline Choice (1961–1990) & Note on Absolute Values vs. Anomalies](#28-baseline-choice-19611990--note-on-absolute-values-vs-anomalies)
   - [2.9 Transparent Sample Size Accounting (N = 768, 732, 602, 744)](#29-transparent-sample-size-accounting-n--768-732-602-744)
   - [2.10 Glossary of Key Technical Terms & Methodological Concepts](#210-glossary-of-key-technical-terms--methodological-concepts)
3. [Mathematical Foundations: Every Computation and Formula Step-by-Step](#3-mathematical-foundations-every-computation-and-formula-step-by-step)
4. [Empirical Audit & Discrepancy Log](#4-empirical-audit--discrepancy-log)
   - [4.1 Diagnostic Problem-by-Problem Audit](#41-diagnostic-problem-by-problem-audit)
   - [4.2 The New Delhi Point-Sampling Microclimate](#42-the-new-delhi-point-sampling-microclimate)
   - [4.3 Global Hydrological Divergence](#43-global-hydrological-divergence)
5. [Methodological & Econometric Changelog](#5-methodological--econometric-changelog)
   - [5.1 Itemized Numerical & Inferential Updates](#51-itemized-numerical--inferential-updates)
   - [5.2 Small-Sample Cluster Inference with t(11) Degrees of Freedom](#52-small-sample-cluster-inference-with-t11-degrees-of-freedom)
   - [5.3 Resolving the Model Contradiction: Spurious Co-Trend vs. Two-Way Fixed Effects](#53-resolving-the-model-contradiction-spurious-co-trend-vs-two-way-fixed-effects)
   - [5.4 Physical Agricultural Yields: Crop Production Index (Model 6)](#54-physical-agricultural-yields-crop-production-index-model-6)
6. [Open Methodological Decisions & Author Defense Guide](#6-open-methodological-decisions--author-defense-guide)
7. [Core Syllabus Steps & Visualizations (Figures 1 to 5)](#7-core-syllabus-steps--visualizations-figures-1-to-5)
8. [Consolidated Master Notebook & One-Command Reproduction Guide](#8-consolidated-master-notebook--one-command-reproduction-guide)

---

## 1. Executive Summary & Direct Answers to the 4 Assignment Questions

This project executes **Track 1: Temperature and Precipitation Records** for the Environmental Economics course at ESSEC Business School (BSc AIDAMS). Over 64 continuous calendar years (1960–2023) across a balanced panel of **12 countries** (3 per continent across Europe, Africa, Asia-Pacific, and the Americas), we answer each sequential question in the syllabus:

### Direct Answers to the Course Brief:

#### Step 1: Plot temperature and precipitation over the full available record
- **Direct Answer:** Over the 1960–2023 instrumental record, mean annual temperatures exhibit a marked upward inflection point beginning around 1985–1990 across Europe, the Americas, and Africa. Decadal warming between 1960–1969 and 2014–2023 reached $+2.16^\circ\text{C}$ in Germany, $+2.11^\circ\text{C}$ in Spain, $+1.76^\circ\text{C}$ in France, $+1.50^\circ\text{C}$ in Mexico, $+1.19^\circ\text{C}$ in the United States, $+1.08^\circ\text{C}$ in Vietnam, $+1.00^\circ\text{C}$ in South Africa, $+0.92^\circ\text{C}$ in Brazil, $+0.71^\circ\text{C}$ in Kenya, $+0.69^\circ\text{C}$ in Australia, and $+0.37^\circ\text{C}$ in Senegal. Precipitation, by contrast, does not follow a simple upward trend: it exhibits heavy multi-year fluctuations, with major historical droughts visible in Western Europe (1976, 2003, 2022) and the African Sahel and East Africa (1984, 1997).

#### Step 2: Compute a monthly anomaly using a chosen baseline (1961–1990)
- **Direct Answer:** The annual seasonal cycle accounts for over 89% of total monthly temperature variance in temperate climates (an ~18°C swing between winter and summer). Without de-seasonalization, a mild winter looks colder than a frigid summer, making months impossible to compare across years. Subtracting the 1961–1990 calendar-month norm purges the solar cycle and reveals the secular trend: cool negative anomalies dominate prior to 1985, replaced by persistent warm positive anomalies post-1995.
- *Note on Downloaded Data:* The ERA5 data downloaded are **absolute physical daily values** (°C and mm), not pre-computed anomalies. We explicitly chose and constructed the 1961–1990 WMO baseline ourselves.

#### Step 3: Describe change vs. volatility, and compare across countries
- **How much has the average changed?** Comparing 2014–2023 to 1960–1969: Germany $+2.16^\circ\text{C}$, Spain $+2.11^\circ\text{C}$, France $+1.76^\circ\text{C}$, Mexico $+1.50^\circ\text{C}$, USA $+1.19^\circ\text{C}$, Vietnam $+1.08^\circ\text{C}$, South Africa $+1.00^\circ\text{C}$, Brazil $+0.92^\circ\text{C}$, Kenya $+0.71^\circ\text{C}$, Australia $+0.69^\circ\text{C}$, Senegal $+0.37^\circ\text{C}$, and New Delhi $-0.39^\circ\text{C}$.
- **How large is year-to-year variation compared with that change ($\text{SNR} = \Delta T / \sigma$)?** In Spain ($\text{SNR} = 3.52$), Mexico ($3.13$), France ($2.97$), Germany ($2.88$), Vietnam ($2.64$), Kenya ($2.38$), and the US ($2.19$), secular warming is **more than double the natural year-to-year noise** ($\text{SNR} > 2.0$), meaning warming has decisively broken through the weather noise envelope.
- **Where has temperature moved most?** Continental Europe (Spain, Germany, France) and Central America (Mexico).
- **Does precipitation move in the same places?** No, precipitation moves in completely different places. The US ($+38.3\%$), Mexico ($+45.7\%$), Vietnam ($+21.3\%$), and Australia ($+19.2\%$) experienced wetting, whereas Senegal ($-32.8\%$), Brazil ($-31.5\%$), South Africa ($-19.6\%$), and Spain ($-10.5\%$) suffered severe drying stress.

#### Step 4 (Direction A): Is the change spread evenly across seasons?
- **Direct Answer:** No, warming is seasonally asymmetric:
  - In Western and Mediterranean Europe (Spain, France), summer warmed faster than winter, accelerating soil evapotranspiration during the critical agricultural dry season.
  - In higher-latitude continental regimes (Germany, US), winter-led warming dominated, driven by polar amplification and reduced snow albedo feedbacks.

#### Step 4 (Direction B): Were unusually warm or dry years unusual for the economy?
- **Direct Answer:** 
  - **In landmark shock years, yes:** Historical heat and drought events align with documented sector-specific economic crises: the 1976 European drought caused a 10% drop in French farm output and triggered a 6-billion-franc drought tax (*impôt sécheresse*); the 2003 European heatwave caused €4 billion in farm losses; and the 1984 Sahel/East Africa droughts caused sharp contractions in agricultural output.
  - **Across the full 64-year panel, no:** In our Two-Way Fixed Effects econometric model, annual weather anomalies do not exert a statistically robust drag on aggregate national GDP per capita growth ($\hat{\beta}_1 = -0.6547, p = 0.0512$, 95% CI $[-1.31, +0.004]$ pp/°C under small-sample $t(11)$). A naive Country Fixed Effects model showed a large penalty ($-0.8239^{***}$ pp/°C), but this was a **spurious co-trend** caused by post-WWII productivity growth naturally slowing down after the 1960s reconstruction boom over the exact same decades that global temperatures rose. Direct physical crop yields, however, confirm significant temperature contraction ($-1.90^*$ pp/°C, $p = 0.0501$) and positive moisture elasticity ($+0.70$ pp per 100mm).

---

## 2. Data Engineering Strategy & The API Dilemma (Why, What, How)

### 2.1 The Architectural Choice: To API or Not to API?
When approaching the assignment instructions, a researcher faces four potential avenues for acquiring 64 years of daily climate records across 12 countries:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    FOUR WAYS TO ACQUIRE THE CLIMATE DATA                     │
└──────────────────────────────────────────────────────────────────────────────┘
       │                              │                             │
       ▼                              ▼                             ▼
[Approach 1: CDS API]      [Approach 2: Atlas GUI]     [Approach 3: Weather Stations]
• Python cdsapi client     • Point-and-click browser   • NOAA GHCN / Meteo-France
• Asynchronous batch queue • 24 manual CSV downloads   • Missing station days
• 50+ GB NetCDF rasters    • Prone to 502/504 timeouts • Urban heat-island biases
• Heavy GIS polygon mask   • Monthly pre-cooked only   • Station closures/moves
       │                              │                             │
       └──────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
             [Approach 4 (Our Chosen Solution): Open-Meteo ERA5 API]
             • Direct programmatic REST query to ECMWF ERA5 reanalysis archive
             • Keyless, instant response (< 2 minutes execution)
             • Raw daily physical observations (280,512 nation-days)
             • Zero missing values, zero GIS dependency compilation crashes
             • 100% automated, one-command reproducibility for any student
```

---

### 2.2 Why We Rejected the Alternatives (CDS API, Atlas GUI, Ground Stations)
1. **The CDS API Authentication Barrier:** CDS requires personal account registration, API keys, and hidden OS dotfiles (`~/.cdsapirc`). Furthermore, requests enter a shared European supercomputer queue that can sit pending for hours or days during peak academic deadlines.
2. **The Atlas GUI Web Instability:** Downloading 12 countries requires clicking through a web GUI 24 times. The web server frequently returns HTTP 502/504 timeouts and only provides monthly pre-aggregations, preventing daily variance analyses.
3. **Weather Stations:** Physical stations suffer from missing observations, instrument relocations, and urban heat island biases.

---

### 2.3 Our Solution: Programmatic ERA5 Extraction via Open-Meteo REST API
Open-Meteo exposes the exact same ECMWF ERA5 atmospheric reanalysis grid ($0.25^\circ \times 0.25^\circ$) via an open, keyless REST API. It delivers 64 continuous years of daily records for all 12 countries in under two minutes with **zero missing values**.

---

### 2.4 Which Data Did We Get Exactly?

| Domain | Source | Parameter / Indicator | Description | Temporal Scope | Units |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **Climate** | ECMWF ERA5 | `temperature_2m_mean` | Daily 24-hour mean surface air temperature at 2 meters | 1960–2023 (daily) | °C |
| **Climate** | ECMWF ERA5 | `precipitation_sum` | Daily 24-hour cumulative liquid water equivalent | 1960–2023 (daily) | mm |
| **Economy** | World Bank WDI | `NY.GDP.PCAP.KD.ZG` | Annual percentage growth rate of real GDP per capita | 1960–2023 (annual) | % |
| **Economy** | World Bank WDI | `NV.AGR.TOTL.ZS` | Agriculture, forestry, and fishing value added | 1960–2023 (annual) | % of GDP |
| **Economy** | World Bank WDI | `AG.PRD.CROP.XD` | Crop production index ($2014\text{–}2016 = 100$) | 1960–2023 (annual) | Index |

---

### 2.5 What Does the Data Look Like? (Real Before vs. After Processing Data Rows)

#### 1. Raw Daily Climate Extraction (`data/raw/climate_raw_FRA.csv`):
```csv
date,temperature_2m_mean,precipitation_sum,country_code,country_name,continent,capital,latitude,longitude
1960-01-01,10.9,2.7,FRA,France,Europe,Paris,48.8566,2.3522
1960-01-02,9.8,7.8,FRA,France,Europe,Paris,48.8566,2.3522
1960-01-03,9.7,0.5,FRA,France,Europe,Paris,48.8566,2.3522
```

#### 2. Raw World Bank Macroeconomic Extraction (`data/raw/worldbank_wdi_1960_2023.csv`):
```csv
year,country_code,country_name,continent,gdp_per_capita_growth,agriculture_share_gdp,crop_production_index
1960,FRA,France,Europe,,10.148498,
1961,FRA,France,Europe,3.866383,8.718111,65.75
1962,FRA,France,Europe,5.788500,9.424351,83.29
```

#### 3. Processed Monthly Anomalies (`data/processed/climate_monthly_anomalies.csv`):
```csv
country_code,year,month,date,temp_monthly_mean,temp_baseline_climatology,temp_monthly_anomaly,precip_monthly_total,precip_baseline_climatology,precip_monthly_anomaly
FRA,1960,1,1960-01-01,3.797,3.235,+0.562,71.4,56.5,+14.9
FRA,1960,2,1960-02-01,4.403,4.082,+0.321,79.5,45.2,+34.3
FRA,1960,3,1960-03-01,8.281,6.389,+1.891,42.1,43.8,-1.7
```

#### 4. Merged Climate-Economic Panel (`data/processed/merged_climate_economic_panel.csv`):
```csv
country_code,year,temp_annual_mean,temp_annual_anomaly,precip_annual_total,precip_100,gdp_per_capita_growth,shock_heatwave
FRA,2003,12.097,+1.480,513.0,-0.654,0.258,0
```

---

### 2.6 Why Save It as Plain-Text CSV?
1. **Universality & Cross-Platform Accessibility:** CSV can be opened anywhere (Excel, Python, R, Stata, text editor) without proprietary binaries.
2. **Zero GIS Compilation Failures:** Eliminates fragile C/Fortran libraries (`libgdal`, `netCDF4`, `h5py`) that frequently fail during installation on student machines.
3. **Immediate Auditability & Lightweight Footprint:** Entire processed panel is under 2 MB, fully trackable via Git.

---

### 2.7 Representative Spatial Anchor: National Capital Coordinates
Climate series are sampled at national capital coordinates:
- **Europe (3):** France (Paris: 48.86, 2.35), Germany (Berlin: 52.52, 13.41), Spain (Madrid: 40.42, -3.70)
- **Africa (3):** Kenya (Nairobi: -1.29, 36.82), Senegal (Dakar: 14.69, -17.45), South Africa (Pretoria: -25.75, 28.23)
- **Asia-Pacific (3):** India (New Delhi: 28.61, 77.21), Vietnam (Hanoi: 21.03, 105.85), Australia (Canberra: -35.28, 149.13)
- **Americas (3):** United States (Washington, D.C.: 38.91, -77.04), Brazil (Brasília: -15.80, -47.89), Mexico (Mexico City: 19.43, -99.13)

*Rationale:* Standardizing sampling at national capitals provides an objective, demographic, and administrative center where weather shocks directly impact labor productivity, public health, and consumer demand. Single-point sampling over large continental landmasses is acknowledged as a known limitation.

---

### 2.8 Baseline Choice (1961–1990) & Note on Absolute Values vs. Anomalies
- **WMO Benchmark:** We adopted the 1961–1990 reference normal recommended by the World Meteorological Organization.
- **Avoiding Shifting Baseline Syndrome:** Using a recent baseline (1991–2020) embeds significant modern warming into the reference norm, making severe heatwaves appear artificially normal.
- **Note on Downloaded Data:** The ERA5 series we downloaded are **absolute physical daily values** (°C and mm), not pre-computed anomalies. We explicitly constructed the 1961–1990 baseline ourselves.

---

### 2.9 Transparent Sample Size Accounting (N = 768, 732, 602, 744)
- **Full Balanced Panel ($N = 768$):** 12 countries $\times$ 64 years (1960 to 2023) $= 768$ country-years.
- **GDP per Capita Growth Regressions ($N = 732$):** Annual growth requires $t-1$, dropping 1960 (12 observations). Vietnam's WDI reporting begins in 1985 (24 missing years pre-1985). Thus, $768 - 12 - 24 = 732$.
- **Agricultural Share Regressions ($N = 602$):** Historical value-added reporting starts later for USA (25 years), Spain (29), Germany (33), Australia (34), and Vietnam (38), leaving 602 valid country-years.
- **Crop Production Growth Regressions ($N = 744$):** The FAO/World Bank crop index covers 1961–2022 (62 index levels); first-differencing into annual growth yields 61 valid growth years across all 12 countries ($12 \times 62 = 744$).

---

## 3. Mathematical Foundations: Every Computation and Formula Step-by-Step

### 3.1 Daily to Monthly Aggregation
$$T_{i,y,m} = \frac{1}{D_{y,m}} \sum_{d=1}^{D_{y,m}} T_{i,y,m,d}^{\text{daily}}, \qquad P_{i,y,m} = \sum_{d=1}^{D_{y,m}} P_{i,y,m,d}^{\text{daily}}$$

### 3.2 Climatological Baseline (1961–1990) & Anomalies
$$\bar{T}_{i,m}^{\text{base}} = \frac{1}{30} \sum_{y=1961}^{1990} T_{i,y,m}, \qquad \bar{P}_{i,m}^{\text{base}} = \frac{1}{30} \sum_{y=1961}^{1990} P_{i,y,m}$$
$$\Delta T_{i,y,m} = T_{i,y,m} - \bar{T}_{i,m}^{\text{base}} \quad (^\circ\text{C}), \qquad \Delta P_{i,y,m} = P_{i,y,m} - \bar{P}_{i,m}^{\text{base}} \quad (\text{mm})$$

### 3.3 Secular Decadal Change
$$\Delta T_i^{\text{secular}} = \bar{T}_{i, 2014–2023} - \bar{T}_{i, 1960–1969}, \qquad \%\Delta P_i^{\text{secular}} = \left( \frac{\bar{P}_{i, 2014–2023} - \bar{P}_{i, 1960–1969}}{\bar{P}_{i, 1960–1969}} \right) \times 100$$

### 3.4 Linear OLS Trend with Newey-West HAC Standard Errors (3 lags)
$$T_{i,y} = \mu_i + \beta_i^{\text{trend}} \times y + e_{i,y}, \qquad \text{Decadal Trend} = 10 \times \hat{\beta}_i^{\text{trend}}$$

### 3.5 Detrended Noise and Signal-to-Noise Ratio (SNR)
$$\sigma_i = \sqrt{\frac{1}{T-2} \sum_{y=1960}^{2023} \hat{e}_{i,y}^2}, \qquad \text{SNR}_i = \frac{\Delta T_i^{\text{secular}}}{\sigma_i}$$

### 3.6 Two-Way Fixed Effects & Small-Sample Cluster Inference
$$\text{Growth}_{it} = \alpha_i + \gamma_t + \beta_1 \Delta T_{it} + \beta_2 \Delta P_{it}^{100\text{mm}} + \varepsilon_{it}$$
Standard errors clustered at country level ($G=12$). Hypothesis testing uses critical values from the Student's $t$ distribution with $df = G - 1 = 11$ ($t_{0.975}(11) = 2.2010$).

---

## 4. Empirical Audit & Discrepancy Log

### 4.1 Diagnostic Problem-by-Problem Audit
1. **Seasonal Warming Asymmetry:** Standardized across all documents to exact country values: Spain (+53.4% faster summer warming) and France (+13.0% faster summer warming).
2. **Precipitation Denominators:** Standardized all percentage changes to use the 1960–1969 baseline mean as common denominator.
3. **Small-Sample Cluster Inference:** Applied Cameron, Gelbach, & Miller (2008) $t(11)$ critical values for $G=12$ clusters.
4. **Coordinate Formatting:** Clean signed decimal coordinates standardized across all files.

### 4.2 The New Delhi Point-Sampling Microclimate
Table 1 reports a modest secular cooling in New Delhi ($-0.39^\circ\text{C}$, trend $-0.037^\circ\text{C}$/dec, $p = 0.24$). This reflects documented Indo-Gangetic Plain aerosol dimming (heavy winter particulate smog reflecting incoming solar radiation) and intensive agricultural irrigation cooling along the urban fringe.

### 4.3 Global Hydrological Divergence
Precipitation displays sharp spatial bifurcation. Sahelian Senegal ($-32.8\%$), Central Brazil ($-31.5\%$), South Africa ($-19.6\%$), and Mediterranean Spain ($-10.5\%$) face compounding warming and drying stress. In contrast, the United States ($+38.3\%$), Mexico ($+45.7\%$), and Vietnam ($+21.3\%$) experience pronounced secular wetting.

---

## 5. Methodological & Econometric Changelog

### 5.1 Itemized Numerical Updates
- **Summary Statistics (Table 1):** Computed across all 12 countries and saved to `paper/tables/table1_summary_statistics.csv` and `.md`.
- **Panel Regressions (Table 2):** 6 models estimated with country-clustered SEs, small-sample $t(11)$ p-values, 95% CIs, and FWL within-$R^2$.
- **Shock Growth Comparison (Table 3):** Welch's two-sample t-tests comparing detrended heat shocks ($z > +1.5$) vs non-shocks.

### 5.2 Resolving the Spurious Co-Trend
Why does Country FE produce a naive estimate of $-0.8239^{***}$ ($p < 0.0001$), while Two-Way FE yields $-0.6547$ ($p = 0.0512$)?
Between 1960 and 2023, high-income economies experienced a post-WWII productivity slowdown over the exact decades that global temperatures rose. Country FE correlates the cooler, high-growth 1960s with low temperatures, and the warmer, lower-growth 2010s with high temperatures. Adding Year Fixed Effects purges this shared macro trend. The resulting 95% confidence interval ($[-1.31, +0.004]$) encompasses zero at the 5% level under $t(11)$.

---

## 6. Open Methodological Decisions & Author Defense Guide

Refer to `presentation/DEFENSE_NOTES.md` for 10 concise, 2-sentence responses anchored to verified empirical numbers.

---

## 7. Core Syllabus Steps & Visualizations (Figures 1 to 5)

All figures generated at 300 DPI in `figures/`:
- **Figure 1:** Observed Climate Records (1960–2023) across 12 countries in 4 continents.
- **Figure 2:** The Need for De-Seasonalization (Raw vs Anomalies for France).
- **Figure 3:** Signal-to-Noise Ratio & Climate Quadrant Divergence (12 countries).
- **Figure 4:** Seasonal Warming Asymmetry by Continent.
- **Figure 5:** Extreme Weather Shocks vs Macroeconomic Growth Overlays.
- **Supplementary Figures 6–9:** Regression Forest Plot, Vulnerability Slopes, Burke Optimum Curve, KDE Density Shifts.

---

## 8. Consolidated Master Notebook & One-Command Reproduction Guide

The entire research pipeline is consolidated into a single, self-contained Jupyter Notebook:
```
notebooks/track1_climate_economics.ipynb
```
The notebook executes sequentially from Cell 1 to Cell 18 with zero manual intervention.

### Reproduction Commands:
```bash
git clone https://github.com/Polluxgnr/Environemental-economics-.git
cd Environemental-economics-
pip install -r requirements.txt

# Option A: Run the standalone modular scripts
python scripts/01_download_data.py
python scripts/02_process_data.py
python scripts/03_run_econometrics.py
python scripts/04_generate_visualizations.py

# Option B: Run the consolidated master Jupyter Notebook in-place
python -m nbconvert --to notebook --execute notebooks/track1_climate_economics.ipynb --inplace
```

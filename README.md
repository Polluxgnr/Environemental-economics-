# Track 1: Temperature and Precipitation Records
## Macroeconomic Shocks, Secular Warming, and Econometric Lessons (1960–2023)

**Course:** Environmental Economics — BSc AIDAMS, T1 2026–2027  
**Instructor:** Caterina Seghini · ESSEC Department of Economics  
**Authors:** Student Research Group 1  
**GitHub Repository:** [https://github.com/Polluxgnr/Environemental-economics-.git](https://github.com/Polluxgnr/Environemental-economics-.git)

---

## Table of Contents
1. [Project Overview & Narrative](#1-project-overview--narrative)
2. [Justification of Every Methodological Choice](#2-justification-of-every-methodological-choice)
   - [Why these 8 specific countries?](#21-why-these-8-specific-countries)
   - [Why these climatological indicators?](#22-why-these-climatological-indicators)
   - [Why these macroeconomic variables?](#23-why-these-macroeconomic-variables)
   - [Why the 1961–1990 baseline?](#24-why-the-19611990-baseline)
   - [Data Acquisition: Copernicus Climate Atlas vs. ERA5 Reanalysis API](#25-data-acquisition-copernicus-climate-atlas-vs-era5-reanalysis-api)
3. [Data Architecture: Before vs. After Processing](#3-data-architecture-before-vs-after-processing)
4. [Core Insights & Findings](#4-core-insights--findings)
   - [Insight 1: Secular Warming has Broken Out of the Noise](#41-insight-1-secular-warming-has-broken-out-of-the-noise)
   - [Insight 2: European Summer Amplification](#42-insight-2-european-summer-amplification)
   - [Insight 3: The Germany vs. Spain -97mm Coincidence](#43-insight-3-the-germany-vs-spain--97mm-coincidence)
   - [Insight 4: The Econometric Revelation (Spurious Co-Trend vs. Two-Way FE)](#44-insight-4-the-econometric-revelation-spurious-co-trend-vs-two-way-fe)
5. [The Core Visualizations](#5-the-core-visualizations)
6. [Econometric Panel Estimation](#6-econometric-panel-estimation)
7. [Limits, Challenges & Epistemic Boundaries](#7-limits-challenges--epistemic-boundaries)
8. [Beginner-Friendly Quickstart & Replication Guide](#8-beginner-friendly-quickstart--replication-guide)
9. [Statement on AI Usage](#9-statement-on-ai-usage)

---

## 1. Project Overview & Narrative

When public discourse discusses climate change, it almost always focuses on a single global number: +1.5°C or +2.0°C above pre-industrial levels. But human societies, businesses, farmers, and factories do not live in a global average. They experience local weather: hot summer heatwaves, dry spells, shifts in rainfall, and cold snaps.

This project tackles **Track 1: Temperature and Precipitation Records**. Over 64 continuous years (1960–2023) across eight diverse countries, we examine four core questions:
1. **The Instrumental Record:** How have temperature and precipitation changed across distinct climate regimes?
2. **Signal-to-Noise Ratio:** Has secular warming outpaced the natural year-to-year volatility of weather?
3. **Seasonal Asymmetry & Hydrology:** Is warming uniform throughout the year, or are summers warming faster than winters? Does rainfall increase where it warms, or do some regions face compounding heat and drying?
4. **Macroeconomic Shocks & Econometric Lessons:** Do landmark climate shock years systematically coincide with economic contractions? And when we estimate panel regressions, what is the true short-run elasticity of GDP per capita growth to temperature?

### The Central Discovery:
A naive within-country regression suggests that a +1.0°C warm temperature anomaly depresses annual real GDP per capita growth by **-0.49 percentage points ($p < 0.01$)**. However, this result is a **spurious correlation** driven by multi-decadal macro co-trends: post-WWII productivity growth naturally slowed down after the 1960s "Trente Glorieuses" across Western economies just as global temperatures were rising. 

Once Year Fixed Effects absorb common global macro cycles and trends (**Two-Way Fixed Effects**), the estimated short-run effect drops to **$-0.0325$ percentage points ($p = 0.94$)**. In our sample of mostly diversified or high-capacity economies, idiosyncratic annual temperature fluctuations do not have a detectable impact on aggregate national GDP per capita growth. Modern services, indoor manufacturing, international trade, and financial risk-sharing buffer aggregate national economies against one-year weather fluctuations.

---

## 2. Justification of Every Methodological Choice

### 2.1 Why these 8 specific countries?
Rather than picking 8 random countries or an entirely European sample (which would produce economic and climatic homogeneity), we selected eight countries that span five continents, distinct Köppen-Geiger climate zones, and contrasting economic structures:

| Country | Code | Climate Zone | Agricultural Heartline / Centroid | Economic Structure & Justification |
| :--- | :---: | :--- | :--- | :--- |
| **France** | `FRA` | Temperate Oceanic | Central Plains (Berry / Loire Basin: 46.80°N, 2.60°E) | European agricultural breadbasket (wheat, viticulture); frontline of European summer heatwaves (1976, 2003, 2019). |
| **Germany** | `DEU` | Temperate Continental | Central Basin (Thuringia / Hesse: 51.16°N, 10.45°E) | **Industrial control group**: Agriculture is <1% of GDP; allows us to test whether climate sensitivity is driven by economic structure. |
| **Spain** | `ESP` | Mediterranean Semi-Arid | Central Iberian Meseta (39.88°N, -4.02°E) | Mediterranean frontline: Intense heatwaves, desertification risk, highly intensive irrigated export agriculture. |
| **United States** | `USA` | Temperate Continental | Midwest Corn Belt (Illinois Basin: 40.00°N, -89.00°W) | Continental agricultural giant; global agricultural price setter with massive domestic financial risk-sharing. |
| **Brazil** | `BRA` | Tropical / Savannah | Cerrado Agricultural Heartland (-15.78°S, -47.93°W) | Leading global exporter of soy, beef, coffee; sensitive to Amazon moisture recycling and ENSO cycles. |
| **India** | `IND` | Monsoonal / Subtropical | Central Agricultural Plains (23.00°N, 78.50°E) | 1.4 billion population; ~45% of workforce in agriculture; acute macro-dependency on the southwest monsoon. |
| **Kenya** | `KEN` | Equatorial Bimodal | Central Highlands (Mt. Kenya Basin: -0.50°S, 37.00°E) | Agrarian developing economy (~27% GDP in agriculture); highly vulnerable to rain-fed crop failure and drought. |
| **Australia** | `AUS` | Arid / Mediterranean | Murray-Darling Food Bowl (-33.50°S, 147.00°E) | Southern hemisphere arid agriculture; extreme interannual precipitation volatility driven by ENSO and IOD. |

### 2.2 Why these climatological indicators?
1. **Daily Mean 2m Temperature ($T_{2m}$, °C):** Standard metric of surface thermal energy.
2. **Daily Precipitation Sum ($P$, mm):** Standard metric of atmospheric moisture supply.
3. **Monthly Climatological Baseline (1961–1990):** De-seasonalizes data so a warm December can be compared to a cool July.
4. **Monthly Anomalies ($\Delta T$ in °C, $\Delta P$ in mm and %):** Isolates deviations from the historical norm.
5. **Seasonal Anomalies (DJF, MAM, JJA, SON):** Tests for seasonal asymmetry (e.g. summer warming outrunning winter warming).
6. **First-Difference Volatility ($\sigma$):** Standard deviation of $T_y - T_{y-1}$, measuring natural year-to-year weather noise.
7. **Signal-to-Noise Ratio ($\text{SNR} = \Delta T / \sigma$):** Directly answers Question 2: has the secular warming trend broken out of ambient noise?

### 2.3 Why these macroeconomic variables?
From the World Bank World Development Indicators (WDI):
1. **Real GDP per Capita Growth (`NY.GDP.PCAP.KD.ZG`):** Measures changes in national economic productivity and living standards.
2. **Agriculture Value Added as % of GDP (`NV.AGR.TOTL.ZS`):** Directly captures the economic sector with physical biological exposure to temperature and precipitation.
3. **Headline Real GDP Growth (`NY.GDP.MKTP.KD.ZG`) & CPI Inflation (`FP.CPI.TOTL.ZG`):** Contextual macro controls.

### 2.4 Why the 1961–1990 baseline?
- It is the **World Meteorological Organization (WMO)** official reference baseline for long-term historical climate change.
- It covers a stable 30-year period immediately preceding the post-1990 global warming acceleration.
- Using a more recent period (e.g., 1991–2020) would introduce **shifting baseline syndrome**: because 1991–2020 was already substantially warmed, comparing recent years to that baseline artificially hides secular warming.

### 2.5 Data Acquisition: Copernicus Climate Atlas vs. ERA5 Reanalysis API
The assignment syllabus recommends the **Copernicus Interactive Climate Atlas** (`atlas.climate.copernicus.eu`). Students should understand the relationship between the Atlas and our programmatic pipeline:
- **What the Atlas provides:** A web graphical interface where you click on predefined country polygons and download CSV files of monthly/seasonal aggregated climate indices.
- **Why we chose the ERA5 Reanalysis API:** The underlying dataset of the Copernicus Climate Atlas is **ECMWF ERA5 surface reanalysis**. When accessing the Atlas during high-traffic periods, automated web scraping often encounters HTTP 502/504 gateway timeouts. By querying the open, keyless Open-Meteo Historical Archive API, we pull the exact same underlying ECMWF ERA5 reanalysis directly, daily, and with zero missing days (187,008 observations). This ensures 100% automated reproducibility from code alone.

---

## 3. Data Architecture: Before vs. After Processing

Our pipeline transforms raw, noisy daily observations into clean, harmonized country-year datasets:

```
[Raw ERA5 Reanalysis]       [Raw World Bank WDI]
 187,008 daily rows          512 country-years
        │                           │
        ▼                           ▼
[Monthly Aggregation]               │
 6,144 monthly rows                 │
        │                           │
        ▼                           ▼
[1961-1990 Baseline]                │
 Climatology subtracted             │
        │                           │
        ▼                           ▼
[Seasonal & Annual Aggregation]     │
 512 annual climate rows            │
        │                           │
        └─────────────┬─────────────┘
                      ▼
        [Merged Climate-Economic Panel]
         512 rows (504 growth, 373 agri)
```

### Table: Data Transformation Stages

| Stage | Dataset File | Rows | Columns | Key Variables | Description |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **Raw Climate** | `data/raw/climate_daily_1960_2023.csv` | 187,008 | 10 | `date`, `temp_2m_mean`, `precip_sum` | Daily continuous records (23,376 days per country). |
| **Raw Economic** | `data/raw/worldbank_wdi_1960_2023.csv` | 512 | 9 | `country_code`, `year`, `gdp_per_capita_growth`, `agriculture_share_gdp` | Unprocessed annual country panel from World Bank API v2. |
| **Monthly Processed** | `data/processed/climate_monthly_anomalies.csv` | 6,144 | 12 | `temp_monthly_anomaly`, `precip_monthly_anomaly`, `precip_monthly_pct_anomaly` | Monthly means/totals minus 1961–1990 baseline climatology. |
| **Seasonal Processed** | `data/processed/climate_seasonal_anomalies.csv` | 2,048 | 8 | `season`, `temp_seasonal_anomaly`, `precip_seasonal_total` | Meteorological seasons (DJF, MAM, JJA, SON) with hemispheric inversion. |
| **Annual Climate** | `data/processed/climate_annual_country_series.csv` | 512 | 11 | `temp_annual_mean`, `temp_yoy_diff`, `precip_annual_total` | Annual series with first-differenced annual volatility ($\sigma$). |
| **Merged Panel** | `data/processed/merged_climate_economic_panel.csv` | 512 | 24 | All climate + economic indicators + shock dummies | Final panel ready for econometric estimation. |

### Sample Data Preview:

#### 1. Raw Daily Data Sample (France):
```csv
date,country_code,temperature_2m_mean,precipitation_sum
1960-01-01,FRA,10.2,0.2
1960-01-02,FRA,9.7,17.4
1960-01-03,FRA,8.8,2.3
```

#### 2. Processed Monthly Anomalies Sample (France, January):
```csv
country_code,date,temp_monthly_mean,temp_baseline_climatology,temp_monthly_anomaly
FRA,1960-01-01,3.55,3.24,+0.30
FRA,1961-01-01,2.81,3.24,-0.43
FRA,1962-01-01,4.12,3.24,+0.88
```

#### 3. Merged Annual Panel Sample (France 2003 European Heatwave):
```csv
country_code,year,temp_annual_mean,temp_annual_anomaly,precip_annual_total,gdp_per_capita_growth,shock_heatwave
FRA,2003,12.51,+1.64,726.9,0.26,1
```

---

## 4. Core Insights & Findings

### 4.1 Insight 1: Secular Warming has Broken Out of the Noise
Comparing the recent decade (2014–2023) to the early decade (1960–1969), absolute secular warming is largest in continental Europe:
- Germany: **+2.09°C** ($\text{SNR} = 2.29$)
- Kenya: **+1.85°C** ($\text{SNR} = 4.85$)
- France: **+1.75°C** ($\text{SNR} = 2.17$)
- Spain: **+1.63°C** ($\text{SNR} = 2.12$)
- United States: **+1.26°C** ($\text{SNR} = 1.31$)

In all European countries, the secular signal is more than double the annual volatility ($\text{SNR} > 2.0$). In Kenya, low equatorial temperature volatility ($\sigma = 0.38^\circ\text{C}$) produces an extraordinary $\text{SNR} = 4.85$, meaning that recent temperatures represent a completely unprecedented regime.

### 4.2 Insight 2: European Summer Amplification
In France and Spain, warming exhibits acute seasonal asymmetry:
- **France:** Summer warming (+2.35°C) outpaces winter warming (+2.08°C).
- **Spain:** Summer warming (+2.24°C) outpaces winter warming (+1.21°C) by over 60%.
Because summer is the period of peak agricultural water demand and lowest precipitation, rapid summer warming exponentially increases atmospheric vapor pressure deficit, pulling moisture from crops and soil.

### 4.3 Insight 3: The Germany vs. Spain -97mm Coincidence
Both Germany and Spain experienced nearly identical absolute declines in mean annual precipitation between 1960–1969 and 2014–2023:
- Germany: $714.7\text{ mm} \to 617.6\text{ mm} \implies \Delta P = -97.1\text{ mm}$ ($-13.6\%$)
- Spain: $525.8\text{ mm} \to 428.8\text{ mm} \implies \Delta P = -97.0\text{ mm}$ ($-18.5\%$)
While the $-97\text{ mm}$ absolute drop is an arithmetic coincidence, Spain's 30% lower baseline rainfall makes this an 18.5% drying compared to 13.6% in Germany, pushing Mediterranean agriculture into severe water rationing.

### 4.4 Insight 4: The Econometric Revelation (Spurious Co-Trend vs. Two-Way FE)
- **Model (2) Country FE:** $\beta = -0.4904^{***}$ ($p < 0.01$). Suggests that +1°C reduces annual growth by nearly 0.5 percentage points.
- **Model (3) Two-Way FE (Preferred):** $\beta = -0.0325$ ($p = 0.94$). Insignificant null result!
- **Why?** Over 1960–2023, high-income economies experienced a post-WWII productivity slowdown (from the 1960s "Trente Glorieuses" to lower trend growth) at the exact same time that global temperatures rose. Country FE mistakes this chronological co-trend for a causal climate penalty. Adding Year Fixed Effects ($\gamma_t$) purges the common global trend, showing that short-run annual weather anomalies do not have a detectable impact on aggregate national GDP in this diversified sample.

---

## 5. The Core Visualizations

All figures are rendered at 300 DPI in `figures/` and stand entirely on their own:

| Figure | Filename | Topic | Core Conclusion |
| :---: | :--- | :--- | :--- |
| **Fig 1** | `figures/fig1_historical_climate_trends.png` | Observed Climate Records (1960–2023) | Unmistakable upward temperature inflection beginning in late 1980s; multi-year drought troughs visible in Europe (1976, 2003, 2022). |
| **Fig 2** | `figures/fig2_warming_stripes_anomalies.png` | Warming Stripes & Monthly Anomalies | De-seasonalization reveals that positive thermal anomalies (reds) become near-universal post-1995 across all calendar months. |
| **Fig 3** | `figures/fig3_warming_vs_precipitation_quadrant.png` | Signal-to-Noise & Climate Quadrants | Secular warming exceeds noise ($\text{SNR} > 1$) across Europe and Africa; Spain and Brazil occupy the compounding "Warming & Drying" quadrant. |
| **Fig 4** | `figures/fig4_seasonal_asymmetry.png` | Seasonal Warming Asymmetry | Summer warming outpaces winter warming by 45%–60% in Western/Mediterranean Europe, compounding agricultural drought risk. |
| **Fig 5** | `figures/fig5_climate_shocks_vs_economic_dips.png` | Weather Shocks vs. Economic Dips | Landmark shock years align with real losses: 1976 French drought (6B franc tax), 2003 heatwave (€4B loss), and severe agrarian dips in Kenya/India. |

---

## 6. Econometric Panel Estimation

### Table 2: Panel Regression Results (1960–2023)

| Regressor / Specification | (1) Pooled OLS | (2) Country FE | (3) Two-Way FE (Preferred) | (4) Agri Share TWFE |
| :--- | :---: | :---: | :---: | :---: |
| **Dependent Variable** | *GDPpc Growth (%)* | *GDPpc Growth (%)* | *GDPpc Growth (%)* | *Agri Share (% GDP)* |
| **Temperature Anomaly (°C)** | **-0.5009\*\*\*** | **-0.4904\*\*\*** | **-0.0325** | 0.7827 |
| *(Cluster-Robust SE)* | *(0.1780)* | *(0.1875)* | *(0.4301)* | *(1.0898)* |
| **Precipitation Anomaly (100mm)** | 0.0596 | 0.0347 | 0.0635 | -0.0766 |
| *(Cluster-Robust SE)* | *(0.0703)* | *(0.0634)* | *(0.0550)* | *(0.1121)* |
| Country Fixed Effects | No | Yes | Yes | Yes |
| Year Fixed Effects | No | No | Yes | Yes |
| Clustered SEs (Country) | Yes | Yes | Yes | Yes |
| Observations ($N$) | 504 | 504 | 504 | 373 |
| $R^2$ | 0.0210 | 0.0444 | 0.3300 | 0.9170 |

*\* p < 0.10, \*\* p < 0.05, \*\*\* p < 0.01. Standard errors clustered by country in parentheses.*

### Exact Sample Size Accounting:
- **512 total panel rows:** 8 countries $\times$ 64 years (1960–2023).
- **504 observations in Columns 1–3:** Annual GDP per capita growth is first-differenced, dropping 1960 for all 8 countries ($512 - 8 = 504$).
- **373 observations in Column 4:** Historical agricultural value-added data starts later in early WDI decades:
  - USA: missing 38 years (1961–1996, 2023)
  - Germany: missing 30 years (1961–1990 pre-unification)
  - Spain: missing 34 years (1961–1994)
  - Australia: missing 29 years (1961–1989)
  - France, Brazil, India, Kenya: full reporting from 1961 onward ($504 - 131 = 373$).

---

## 7. Limits, Challenges & Epistemic Boundaries

In accordance with course guidelines on correlation and causality:
1. **Weather Shocks $\neq$ Long-Run Climate Change:**
   Our regressions capture the response to *transitory, unanticipated annual weather anomalies* (Dell, Jones, & Olken, 2014). They do not measure long-run equilibrium adaptation. Over a 50-year horizon, farmers invest in irrigation, shift planting dates, and switch cultivars. Conversely, annual regressions cannot capture irreversible long-run ecological tipping points (e.g. aquifer depletion).
2. **Spatial Aggregation Low-Pass Filter:**
   National-level averages dampen acute localized disasters. A total crop failure in Andalusia or the Murray-Darling basin is devastating to regional farmers, but represents a small percentage of total national GDP in service-dominated economies.
3. **What Would Be Needed for Full Causality?**
   - Sub-national panels (NUTS-3 in Europe, county-level in the US).
   - Local projections (Jordà, 2005) over 5–10 year horizons to measure permanent capital scarring.

---

## 8. Beginner-Friendly Quickstart & Replication Guide

To replicate every table, number, and figure from scratch:

### 1. Clone the repository
```bash
git clone https://github.com/Polluxgnr/Environemental-economics-.git
cd "Environemental economics track 1"
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the pipeline step-by-step
```bash
# Step 1: Download raw ERA5 climate and WDI economic data
python scripts/download_data.py

# Step 2: Compute monthly baselines, anomalies, and merge panel
python scripts/process_data.py

# Step 3: Run econometric panel regressions and produce Tables 1 & 2
python scripts/run_econometrics.py

# Step 4: Render all publication-grade figures in figures/
python scripts/generate_visualizations.py
```

---

## 9. Statement on AI Usage

In accordance with Section 4 of the project guidelines:
- **Tools Used:** Antigravity AI coding assistant (Google DeepMind agentic framework).
- **Role of AI:** Assisted in drafting repetitive Python data pipeline code, formatting Markdown tables, and structuring LaTeX formulas.
- **Human Intellectual Responsibility:** The student research team designed the research questions, chose the country sample and centroid coordinates, directed the econometric modeling, discovered and resolved the spurious correlation in the Country FE specification, verified all empirical numbers against the raw data, and authored the paper and defense notes.

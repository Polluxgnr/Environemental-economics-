# Track 1: Temperature and Precipitation Records
## Macroeconomic Shocks, Secular Warming, and Econometric Lessons (1960–2023)

**Course:** Environmental Economics — BSc AIDAMS, T1 2026–2027  
**Instructor:** Caterina Seghini · ESSEC Department of Economics  
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
   - [2.7 Representative Centroid Strategy & Köppen-Geiger Classifications](#27-representative-centroid-strategy--k%C3%B6ppen-geiger-classifications)
   - [2.8 Baseline Choice (1961–1990) & Note on Absolute Values vs. Anomalies](#28-baseline-choice-19611990--note-on-absolute-values-vs-anomalies)
   - [2.9 Transparent Sample Size Accounting (N = 512, 504, 496, 373)](#29-transparent-sample-size-accounting-n--512-504-496-373)
3. [Empirical Audit & Discrepancy Log](#3-empirical-audit--discrepancy-log)
   - [3.1 Diagnostic Problem-by-Problem Audit](#31-diagnostic-problem-by-problem-audit)
   - [3.2 The Germany vs. Spain Precipitation Coincidence (-97mm)](#32-the-germany-vs-spain-precipitation-coincidence--97mm)
   - [3.3 Point-Sampling Microclimates in India and Australia](#33-point-sampling-microclimates-in-india-and-australia)
4. [Methodological & Econometric Changelog](#4-methodological--econometric-changelog)
   - [4.1 Itemized Numerical & Inferential Updates](#41-itemized-numerical--inferential-updates)
   - [4.2 Small-Sample Cluster Inference with t(7) Degrees of Freedom](#42-small-sample-cluster-inference-with-t7-degrees-of-freedom)
   - [4.3 Resolving the Model Contradiction: Spurious Co-Trend vs. Two-Way Fixed Effects](#43-resolving-the-model-contradiction-spurious-co-trend-vs-two-way-fixed-effects)
   - [4.4 Physical Agricultural Yields: Crop Production Index (Model 5)](#44-physical-agricultural-yields-crop-production-index-model-5)
5. [Open Methodological Decisions & Author Defense Guide](#5-open-methodological-decisions--author-defense-guide)
6. [Core Syllabus Steps & Visualizations (Figures 1 to 5)](#6-core-syllabus-steps--visualizations-figures-1-to-5)
7. [Step-by-Step Reproduction Guide & Code Walkthrough](#7-step-by-step-reproduction-guide--code-walkthrough)

---

## 1. Executive Summary & Direct Answers to the 4 Assignment Questions

This project executes **Track 1: Temperature and Precipitation Records** for the Environmental Economics course at ESSEC Business School (BSc AIDAMS). Over 64 continuous calendar years (1960–2023) across eight climatically diverse countries—**France, Germany, Spain, the United States, Brazil, India, Kenya, and Australia**—we answer each sequential question in the syllabus:

### Direct Answers to the Course Brief:

#### Step (1) — Plot temperature and precipitation over the full available record:
- **Direct Answer:** Over the 1960–2023 instrumental record, mean annual temperatures show a noticeable upward inflection beginning around 1985–1990 across all eight regions. Decadal warming between 1960–1969 and 2014–2023 reached $+2.09^\circ\text{C}$ in Germany, $+1.85^\circ\text{C}$ in Kenya, $+1.75^\circ\text{C}$ in France, $+1.63^\circ\text{C}$ in Spain, and $+1.26^\circ\text{C}$ in the United States. Precipitation, by contrast, does not follow a simple upward trend: it exhibits heavy multi-year fluctuations, with major historical droughts visible in Europe (1976, 2003, 2022) and East Africa (1984, 1997).

#### Step (2) — Compute a monthly anomaly using a chosen baseline (1961–1990):
- **Direct Answer:** The annual seasonal cycle accounts for over 89% of total monthly temperature variance in temperate climates (an ~18°C swing between winter and summer). Without de-seasonalization, a mild winter looks colder than a frigid summer, making months impossible to compare across years. Subtracting the 1961–1990 calendar-month norm purges the solar cycle and reveals the secular trend: cool negative anomalies dominate prior to 1985, replaced by persistent warm positive anomalies post-1995.
- *Note on Downloaded Data:* The ERA5 data we downloaded are **absolute physical daily values** (°C and mm), not pre-computed anomalies. We explicitly chose and constructed the 1961–1990 WMO baseline ourselves.

#### Step (3) — Describe change vs. volatility, and compare across countries:
- **How much has the average changed?** Comparing 2014–2023 to 1960–1969: Germany $+2.09^\circ\text{C}$, Kenya $+1.85^\circ\text{C}$, France $+1.75^\circ\text{C}$, Spain $+1.63^\circ\text{C}$, USA $+1.26^\circ\text{C}$, Brazil $+0.70^\circ\text{C}$, Australia $+0.24^\circ\text{C}$, and India $+0.07^\circ\text{C}$.
- **How large is year-to-year variation compared with that change ($\text{SNR} = \Delta T / \sigma$)?** In Western Europe and Kenya, secular warming is **2.7 to 3.3 times larger than natural year-to-year noise** ($\text{SNR} > 2.0$), meaning warming has decisively broken through the weather noise envelope. In inland Australia and central India, annual noise exceeds the local trend ($\text{SNR} < 0.4$).
- **Where has temperature moved most?** Continental Europe (Germany, France, Spain) and East Africa (Kenya).
- **Does precipitation move in the same places?** No, precipitation moves in completely different places. The US ($+25.2\%$) and India ($+15.4\%$) experienced wetting, whereas Spain ($-18.5\%$), Brazil ($-29.1\%$), and Germany ($-13.6\%$) suffered severe drying. Spain and Brazil face compounding warming and drying stress.

#### Step (4, Direction A) — Is the change spread evenly across seasons?
- **Direct Answer:** No, warming is seasonally asymmetric:
  - In Mediterranean Spain, summer warmed **+53.4% faster** than winter ($+2.04^\circ\text{C}$ in summer vs. $+1.33^\circ\text{C}$ in winter).
  - In France, summer warmed **+13.0% faster** than winter ($+2.35^\circ\text{C}$ in summer vs. $+2.08^\circ\text{C}$ in winter).
  - This summer amplification accelerates soil moisture depletion during the critical agricultural dry season. Conversely, higher-latitude continental regimes (Germany at $+3.38^\circ\text{C}$ and the US at $+2.54^\circ\text{C}$) experienced winter-led warming.

#### Step (4, Direction B) — Were unusually warm or dry years unusual for the economy?
- **Direct Answer:** 
  - **In landmark shock years, yes:** Landmark heat and drought events align with documented sector-specific economic crises: the 1976 European drought caused a 10% drop in French farm output and triggered a 6-billion-franc drought tax (*impôt sécheresse*); the 2003 European heatwave caused €4 billion in farm losses; and the 1984/1997 Kenyan droughts caused sharp contractions in agricultural output.
  - **Across the full 64-year panel, no:** In our Two-Way Fixed Effects econometric model, annual weather anomalies do not exert a statistically detectable drag on aggregate national GDP per capita growth ($\hat{\beta} = -0.0325, p = 0.9419$, 95% CI $[-1.0496, +0.9847]$ pp/°C). A naive Country Fixed Effects model showed a large penalty ($-0.4904^{**}$ pp/°C), but this was a **spurious co-trend** caused by post-WWII growth naturally slowing down after the 1960s reconstruction boom over the exact same decades that global temperatures rose. Two-Way Fixed Effects purges this macro trend. The resulting null is an **uninformative null** due to sample size ($G=8$), not proof of total economic resilience. Direct physical crop yields, however, confirm significant positive moisture elasticity ($\hat{\beta}_{\text{precip}} = +0.5664^*, p = 0.077$).

---

## 2. Data Engineering Strategy & The API Dilemma (Why, What, How)

### 2.1 The Architectural Choice: To API or Not to API?

When approaching the assignment instructions, a researcher faces four potential avenues for acquiring 64 years of daily climate records across eight countries:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    FOUR WAYS TO ACQUIRE THE CLIMATE DATA                     │
└──────────────────────────────────────────────────────────────────────────────┘
       │                              │                             │
       ▼                              ▼                             ▼
[Approach 1: CDS API]      [Approach 2: Atlas GUI]     [Approach 3: Weather Stations]
• Python `cdsapi` client   • Point-and-click browser   • NOAA GHCN / Meteo-France
• Asynchronous batch queue • 16 manual CSV downloads   • Missing station days
• 50+ GB NetCDF rasters    • Prone to 502/504 timeouts • Urban heat-island biases
• Heavy GIS polygon mask   • Monthly pre-cooked only   • Station closures/moves
       │                              │                             │
       └──────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
             [Approach 4 (Our Chosen Solution): Open-Meteo ERA5 API]
             • Direct programmatic REST query to ECMWF ERA5 reanalysis archive
             • Keyless, instant response (< 2 minutes execution)
             • Raw daily physical observations (187,008 nation-days)
             • Zero missing values, zero GIS dependency compilation crashes
             • 100% automated, one-command reproducibility for any student
```

---

### 2.2 Why We Rejected the Alternatives (CDS API, Atlas GUI, Ground Stations)

#### Why Not Approach 1: The Official Copernicus Climate Data Store (CDS) API (`cdsapi`)?
1. **The Authentication Barrier:** CDS requires every user to create a personal account on `cds.climate.copernicus.eu`, agree to terms, generate a personal API key, and configure a hidden `~/.cdsapirc` file on their operating system. If a student or professor clones the repository, the script fails immediately unless they have their own credentials configured.
2. **Supercomputing Queue Bottlenecks:** CDS is designed for massive archival extractions. When a script calls `cdsapi.Client().retrieve()`, the request enters a shared European supercomputer queue. During peak university semesters, jobs can sit queued for **several hours to several days** before downloading. This makes automated, dynamic execution impossible.
3. **Massive Multidimensional NetCDF Arrays:** CDS delivers global grids in NetCDF (`.nc`) or GRIB format. Extracting eight countries requires downloading 50+ GB of gridded rasters, installing complex C/Fortran geospatial libraries (`netCDF4`, `h5py`, `geopandas`, `rioxarray`, `libgdal`), and rasterizing national polygon boundaries. These libraries frequently fail to compile on student Windows/Mac laptops.

#### Why Not Approach 2: The Copernicus Interactive Climate Atlas Web GUI (`atlas.climate.copernicus.eu`)?
1. **Manual Web Scraping vs. Reproducible Code:** The Atlas is an interactive web frontend. Downloading eight countries requires clicking through the UI 16 times (temperature and precipitation for 8 countries). This violates the foundational computer science requirement of an automated, end-to-end Python pipeline.
2. **Web Server Instability:** During academic submission deadlines, the Atlas web server frequently returns HTTP 502 Bad Gateway and 504 Gateway Timeout errors.
3. **Pre-Cooked Monthly Summaries Only:** The Atlas GUI only provides monthly aggregate indices. It does not provide raw daily time series, preventing researchers from examining daily temperature distributions, heatwave durations, or daily-derived variance.

#### Why Not Approach 3: Raw Weather Station Networks (NOAA GHCN / Ground Stations)?
1. **Missing Data & Attrition Bias:** Physical weather stations suffer power failures, instrument breakdowns, and missing observation records.
2. **Station Relocations:** Moving a station from a city center to an airport introduces an artificial non-climatic jump in the temperature series.
3. **Urban Heat Island (UHI) Contamination:** Stations located near growing urban airports measure artificial warming caused by expanding asphalt runways and concrete terminals rather than greenhouse forcing.
4. **Spatial Sparsity:** Stations are dense in wealthy coastal cities but sparse in agricultural basins.

---

### 2.3 Our Solution: Programmatic ERA5 Extraction via Open-Meteo Scientific REST API

**Is Open-Meteo different data? No. It is the exact same ECMWF ERA5 reanalysis archive.**  
Open-Meteo is an open-source scientific initiative that mirrors the official ECMWF ERA5 atmospheric reanalysis grid ($0.25^\circ \times 0.25^\circ$, $\approx 31\text{ km} \times 31\text{ km}$) and exposes it via an open REST API:
- **100% Programmatic Reproducibility:** No account registration, no private API tokens, no hidden configuration files. Anyone can clone this repository and run `python scripts/01_download_data.py`.
- **Instant Speed:** Pulls 64 years of daily data for all eight countries in under two minutes, bypassing multi-hour supercomputing batch queues.
- **Physical Accuracy & Completeness:** Provides unbroken, physics-based daily observations across all 187,008 nation-days with **zero missing values**.

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

To see the exact transformations, here are actual sample rows from the raw and processed datasets:

#### 1. Raw Daily Climate Extraction (`data/raw/climate_raw_FRA.csv`):
```csv
date,temperature_2m_mean,precipitation_sum,country_code,country_name,region,climate_zone,latitude,longitude,location_desc
1960-01-01,10.2,0.2,FRA,France,Western Europe,Temperate Oceanic,46.8,2.6,Central Agricultural Plains (Berry / Loire Basin)
1960-01-02,9.7,17.4,FRA,France,Western Europe,Temperate Oceanic,46.8,2.6,Central Agricultural Plains (Berry / Loire Basin)
1960-01-03,8.8,2.3,FRA,France,Western Europe,Temperate Oceanic,46.8,2.6,Central Agricultural Plains (Berry / Loire Basin)
```
*Notice: Raw daily values are absolute numbers (°C and mm) with exact geographic metadata.*

#### 2. Raw World Bank Macroeconomic Extraction (`data/raw/worldbank_wdi_1960_2023.csv`):
```csv
year,country_code,country_name,region,gdp_per_capita_growth,agriculture_share_gdp,gdp_growth,inflation_cpi,crop_production_index
1960,FRA,France,Western Europe,,10.1484983970751,,4.13993575518437,
1961,FRA,France,Western Europe,3.86638337263079,8.71811104626433,4.94642545980355,2.40046104546311,65.75
1962,FRA,France,Western Europe,5.78849953083436,9.42435111401664,6.85626464484753,5.33128007065639,83.29
```
*Notice: 1960 GDP growth is missing because annual growth requires the t-1 lag (1959).*

#### 3. Processed Monthly Anomalies (`data/processed/climate_monthly_anomalies.csv`):
```csv
country_code,year,month,date,temp_monthly_mean,temp_baseline_climatology,temp_monthly_anomaly,precip_monthly_total,precip_baseline_climatology,precip_monthly_anomaly
FRA,1960,1,1960-01-01,3.545,3.243,+0.302,72.4,62.1,+10.3
FRA,1960,2,1960-02-01,5.348,4.471,+0.877,88.1,51.8,+36.3
FRA,1960,3,1960-03-01,8.542,6.495,+2.047,45.2,49.1,-3.9
```
*Notice: The calendar-month baseline (1961–1990) is subtracted from each month's observed mean to isolate the anomaly.*

#### 4. Processed Seasonal Aggregates (`data/processed/climate_seasonal_anomalies.csv`):
```csv
country_code,year,season,temp_seasonal_mean,temp_seasonal_anomaly,precip_seasonal_total
FRA,1960,Winter (DJF),3.46,-0.12,210.5
FRA,1960,Spring (MAM),9.98,-0.15,185.3
FRA,1960,Summer (JJA),18.00,-0.45,165.2
FRA,1960,Autumn (SON),11.98,-0.08,239.7
```
*Notice: Calendar months are grouped into standard meteorological seasons (inverted for Southern Hemisphere countries).*

#### 5. Merged Climate-Economic Panel (`data/processed/merged_climate_economic_panel.csv`):
```csv
country_code,year,temp_annual_mean,temp_annual_anomaly,precip_annual_total,precip_annual_anomaly_100mm,gdp_per_capita_growth,agriculture_share_gdp,shock_heatwave
FRA,2003,12.51,+1.64,726.9,-0.35,0.26,2.41,1
```
*Notice: All physical and macroeconomic variables are harmonized on (country_code, year) for panel econometric estimation.*

---

### 2.6 Why Save It as Plain-Text CSV?

1. **Universality & Cross-Platform Accessibility:** Plain-text CSV can be opened and verified by anyone—in Excel, Python (`pandas`), R, Stata, Julia, or a standard text editor—with zero proprietary software.
2. **Zero GIS Compilation Failures:** NetCDF (`.nc`) and GRIB (`.grib`) files require specialized C/Fortran binary packages (`libgdal`, `netCDF4`, `h5py`) that frequently fail during installation on student machines. CSV runs everywhere out-of-the-box.
3. **Immediate Auditability:** A student or examiner can open any CSV in `data/processed/` and verify an individual data point (e.g. France in 2003) in five seconds.
4. **Git Version Control & Lightweight Footprint:** The entire processed dataset is under 1 MB, allowing clean git tracking without Git LFS (Large File Storage).

---

### 2.7 Representative Centroid Strategy & Köppen-Geiger Classifications

Rather than sampling unpopulated deserts or tundra, centroids were placed in each country's primary agricultural and demographic heartland using clean signed decimal coordinates:

| Country | Code | Coordinates | Region / Heartland | Köppen-Geiger Classification | Rationale |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **France** | `FRA` | `(46.80, 2.60)` | Berry / Centre-Val de Loire | `Cfb` (Temperate oceanic) | Major European cereal breadbasket; temperate maritime climate. |
| **Germany** | `DEU` | `(51.16, 10.45)` | Thuringian Basin / Central Germany | `Cfb / Dfb` (Temperate continental) | Industrial economic structure (<1% agriculture GDP); central European climate. |
| **Spain** | `ESP` | `(39.88, -4.02)` | Central Iberian Meseta (Toledo) | `Csa` (Mediterranean semi-arid) | European frontline of drought, heatwaves, and seasonal water stress. |
| **United States** | `USA` | `(40.00, -89.00)` | Midwestern Corn Belt (Illinois) | `Dfa` (Humid continental) | Global agricultural grain export powerhouse; continental climate extremes. |
| **Brazil** | `BRA` | `(-15.78, -47.93)` | Central Cerrado Heartland (Brasília) | `Aw` (Tropical savannah) | Southern hemisphere tropical agribusiness belt (soybeans, beef). |
| **India** | `IND` | `(23.00, 78.50)` | Central Agricultural Plains (Madhya Pradesh) | `Cwa / Aw` (Monsoon subtropical) | Agrarian developing economy (27% GDP); rain-fed Kharif monsoon farming. |
| **Kenya** | `KEN` | `(-0.50, 37.00)` | Central Agricultural Highlands (Mount Kenya) | `Cfb / Cwb` (Equatorial highland) | Equatorial agrarian economy (27% GDP); bimodal rainfall; low annual $\sigma$. |
| **Australia** | `AUS` | `(-33.50, 147.00)` | Murray-Darling Agricultural Basin (NSW) | `BSh / Cfa` (Semi-arid steppe) | Southern hemisphere arid agriculture governed by intense ENSO cycles. |

---

### 2.8 Baseline Choice (1961–1990) & Note on Absolute Values vs. Anomalies

- **WMO Benchmark:** We adopted the 1961–1990 reference normal recommended by the World Meteorological Organization.
- **Avoiding Shifting Baseline Syndrome:** Using a recent baseline (1991–2020) embeds significant modern warming into the reference norm, making severe heatwaves appear artificially normal.
- **Note on Downloaded Data:** The ERA5 series we downloaded are **absolute physical daily values** (°C and mm), not pre-computed anomalies. We explicitly chose and constructed the 1961–1990 baseline ourselves.

---

### 2.9 Transparent Sample Size Accounting (N = 512, 504, 496, 373)

- **Full Panel ($N = 512$):** 8 countries $\times$ 64 years (1960 to 2023) $= 512$ country-years.
- **GDP per Capita Growth Regressions ($N = 504$):** Annual growth requires $t-1$. Because our data starts in 1960, the year 1960 is lost for all 8 countries ($512 - 8 = 504$).
- **Crop Production Growth Regressions ($N = 496$):** The World Bank crop index begins in 1960; percentage growth is defined from 1962 onward ($8 \times 62 = 496$).
- **Agricultural Share Regressions ($N = 373$):** Historical World Bank reporting has gaps in value-added shares for four countries, dropping exactly **131 country-years**:
  - United States: Missing 38 years (1961–1996 and 2022–2023).
  - Germany: Missing 30 years (1961–1990 pre-unification).
  - Spain: Missing 34 years (1961–1994 pre-Eurostat harmonization).
  - Australia: Missing 29 years (1961–1989).
  - France, Brazil, India, Kenya: Complete reporting 1961–2023 (0 missing).
  - Total available: $504 - 131 = \mathbf{373}$ observations.

---

## 3. Empirical Audit & Discrepancy Log

### 3.1 Diagnostic Problem-by-Problem Audit

Following peer review, an exhaustive audit was performed across all scripts, tables, and prose to eliminate internal discrepancies. Every metric was recomputed from scratch and verified against `results.json`:

| Item / Claim | Initial Value / Issue | Actual Empirical Value | Root Cause & Resolution |
| :--- | :--- | :--- | :--- |
| **Seasonal Warming Asymmetry** | Stated as "France and Spain +2.2–2.4°C vs +1.2–1.4°C, 45–60% faster in summer". | **France:** Summer $+2.35^\circ\text{C}$ vs Winter $+2.08^\circ\text{C}$ (**+13.0%**).<br>**Spain:** Summer $+2.04^\circ\text{C}$ vs Winter $+1.33^\circ\text{C}$ (**+53.4%**). | Past draft conflated Spain's high ratio (+53.4%) with France (+13.0%). Standardized across all documents to exact country values. |
| **% Precipitation Change Denominators** | Spain -18.5%, Germany -13.6% used 1960s base; Brazil -32.8%, USA +21.5%, India +15.7% used full-period mean. | **1960s Base:**<br>DEU: $-13.6\%$, ESP: $-18.5\%$, BRA: $-29.1\%$, USA: $+25.2\%$, IND: $+15.4\%$, AUS: $+9.2\%$, FRA: $-6.7\%$, KEN: $-7.9\%$. | Standardized all percentage changes to a single definition: decadal change relative to 1960–1969 baseline: $\% \Delta P = (\Delta P / \bar{P}_{1960s}) \times 100$. |
| **Germany vs. Spain Precipitation Coincidence** | Both showed $\Delta P \approx -97\text{ mm}$ and identical $\text{SD} = 108.7\text{ mm}$. Suspected copy-paste bug. | **DEU:** Mean $656.8$, SD $108.67\text{ mm}$, $\Delta P = -97.09\text{ mm}$.<br>**ESP:** Mean $461.7$, SD $108.71\text{ mm}$, $\Delta P = -97.05\text{ mm}$.<br>**$\text{corr}(DEU, ESP) = -0.0119$**. | Verified as a genuine empirical coincidence between two completely uncorrelated physical series ($r = -0.012$). |
| **Model 4 Sample Size ($N=373$)** | Text claimed USA was missing "1961–1996 + 2023" = 38 years ($504 - 130 = 374$). | **USA:** Missing 1961–1996 (36 yrs) + 2022–2023 (2 yrs) = **38 years**.<br>DEU missing 30, ESP missing 34, AUS missing 29. | Total missing from 504: $38 + 30 + 34 + 29 = 131$. $504 - 131 = 373$. Text previously omitted mentioning 2022. Arithmetic verified. |
| **Warming in India and Australia** | Text claimed "all eight countries warm and post-2000 beats 1960–80 everywhere", but Table 1 has India $+0.07^\circ\text{C}$ and Australia $+0.24^\circ\text{C}$. | **India Centroid:** $+0.07^\circ\text{C}$ decadal diff, OLS trend $+0.028^\circ\text{C}$/dec ($p = 0.33$).<br>**Australia Centroid:** $+0.24^\circ\text{C}$ decadal diff, OLS trend $+0.092^\circ\text{C}$/dec ($p = 0.13$). | Single-cell centroid sampling reflects local microclimates (irrigation dimming in MP, India; ENSO volatility in Australia). Clarified as point-sampling findings. |
| **Significance Stars with $G=8$ Clusters** | Models 1 & 2 reported $p < 0.01$ (***) using asymptotic normal approximation ($p = 0.0049$ and $0.0089$). | **Small-sample $t(7)$ inference:**<br>Model 1: $p = 0.0260$ (**).<br>Model 2: $p = 0.0346$ (**). | Corrected stars to `**` based on Cameron, Gelbach, & Miller (2008) small-sample cluster degrees of freedom $G - 1 = 7$. |
| **Two-Way FE Null Interpretation** | Interpreted as affirmative evidence that diversified economies are "resilient". | **TWFE Estimate:** $\hat{\beta} = -0.0325$, $\text{SE} = 0.4301$.<br>**$95\%\text{ CI} = [-1.0496, +0.9847]$**. | The 95% CI is wide and encompasses the naive estimate of $-0.49$. Reported honestly as an **uninformative null**, not proof of zero impact. |
| **Spurious Co-Trend Hypothesis** | Asserted theoretically without an empirical test. | **Country Trends:** $\beta = +0.1848$ ($p = 0.43$).<br>**Decade FE:** $\beta = -0.2200$ ($p = 0.47$). | Confirmed empirically: controlling for secular time trends directly eliminates the naive negative correlation. |
| **Climate Shock Definition** | Fixed $1.5\sigma$ threshold on raw temperature selected mostly recent warmed years. | **Detrended Shocks:** Defined on residuals after removing country linear trends. | Heat shocks ($N=30$): mean growth 1.47% vs non-shock 2.19% ($-0.72$ pp penalty, $p=0.34$). Drought shocks ($N=28$): mean growth 2.45% vs 2.13%. Created Table 3. |
| **Coordinate Formatting** | Double signs in text (e.g., "$-4.02^\circ\text{E}$", "$-89.00^\circ\text{W}$"). | Clean signed decimals: `(39.88, -4.02)`. | Standardized coordinates to clean signed decimals across all prose. |
| **Within-$R^2$ Reporting** | Reported overall $R^2$ including fixed effects (0.044 and 0.330). | **Within-$R^2$:**<br>Model 2 (Country FE): **0.0176** (1.76%).<br>Model 3 (Two-Way FE): **0.0030** (0.30%). | Added explicit within-$R^2$ rows in Table 2. |
| **Temperature Variance Demeaning** | Untested how much climate variation survives Year FE. | Raw variance: $0.6008$. After TWFE: **$0.3067$ (51.1% remains)**. | Year FE removes 48.9% of temperature variance. The remaining 51.1% is idiosyncratic country weather variation. |

---

### 3.2 The Germany vs. Spain Precipitation Coincidence (-97mm)

In Table 1, Germany and Spain show nearly identical values for decadal precipitation change ($-97.09\text{ mm}$ vs. $-97.05\text{ mm}$) and identical standard deviations ($108.67\text{ mm}$ vs. $108.71\text{ mm}$). 

We performed an explicit empirical test to confirm this was not an indexing bug:
- **Correlation:** Computing the Pearson correlation between Germany and Spain's annual rainfall series yields $r(\text{DEU}_{\text{precip}}, \text{ESP}_{\text{precip}}) = \mathbf{-0.0119}$.
- **Different Baselines:** Germany's 1960–1969 baseline rainfall was $714.7\text{ mm}$ (dropping to $617.6\text{ mm}$ in 2014–2023), representing a **$-13.6\%$** reduction. Spain's baseline rainfall was $525.8\text{ mm}$ (dropping to $428.8\text{ mm}$), representing an **$-18.5\%$** reduction.
- **Economic & Agronomic Implication:** Losing $97\text{ mm}$ of rainfall in temperate, water-abundant Germany leaves agriculture well above water-stress thresholds. In semi-arid Spain, losing $97\text{ mm}$ pushed cereal and olive groves toward severe drought stress. The identical drop is a genuine numerical coincidence between two physically uncorrelated series.

---

### 3.3 Point-Sampling Microclimates in India and Australia

Table 1 reports modest secular warming for the India centroid ($+0.07^\circ\text{C}$, trend $+0.028^\circ\text{C}$/dec, $p = 0.33$) and Australia centroid ($+0.24^\circ\text{C}$, trend $+0.092^\circ\text{C}$/dec, $p = 0.13$). This highlights the distinction between a single $0.25^\circ$ grid cell and a continental national landmass:
- **Central India (Madhya Pradesh: `23.00, 78.50`):** During 1970–2010, the Green Revolution drove massive tubewell irrigation expansion across the Indo-Gangetic and central plains. Enhanced surface evapotranspiration creates a local evaporative cooling effect during the dry season. Concurrently, high atmospheric aerosol optical depth (sulfate and black carbon from agricultural burning and coal) caused solar dimming, suppressing daytime warming trends.
- **Inland Australia (Murray-Darling Basin: `-33.50, 147.00`):** This semi-arid pastoral zone is governed by the El Niño–Southern Oscillation (ENSO). Annual temperature and rainfall fluctuations are so severe ($\sigma_{\text{precip}} = 148.4\text{ mm}$) that they mask decadal trends over a single grid cell.
- **Pedagogical Takeaway:** Rather than claiming uniform warming across all grid points, environmental economists must recognize how local land-use, irrigation, and aerosols intersect with macro climate forcing.

---

## 4. Methodological & Econometric Changelog

### 4.1 Itemized Numerical & Inferential Updates

All metrics across the project adhere strictly to the following verified values:

1. **Seasonal Warming Decomposition:**
   - **Spain:** Summer $+2.04^\circ\text{C}$ vs. Winter $+1.33^\circ\text{C}$ (**+53.4% faster in summer**).
   - **France:** Summer $+2.35^\circ\text{C}$ vs. Winter $+2.08^\circ\text{C}$ (**+13.0% faster in summer**).
   - **Germany:** Winter $+3.38^\circ\text{C}$ vs. Summer $+2.48^\circ\text{C}$ (winter-led warming).
   - **United States:** Winter $+2.54^\circ\text{C}$ vs. Summer $+0.74^\circ\text{C}$ (winter-led warming).
2. **Precipitation Changes (1960–1969 Baseline Denominator):**
   - Spain: $-18.5\%$ ($-97.05\text{ mm}$) | Germany: $-13.6\%$ ($-97.09\text{ mm}$)
   - Brazil: $-29.1\%$ ($-472.7\text{ mm}$) | USA: $+25.2\%$ ($+212.8\text{ mm}$)
   - India: $+15.4\%$ ($+189.1\text{ mm}$) | Australia: $+9.2\%$ ($+39.6\text{ mm}$)
   - France: $-6.7\%$ ($-53.3\text{ mm}$) | Kenya: $-7.9\%$ ($-133.4\text{ mm}$)
3. **Signal-to-Noise Ratios ($\text{SNR} = \Delta T / \sigma$):**
   - Kenya: $3.29$ | Germany: $2.94$ | France: $2.86$ | Spain: $2.68$ | USA: $1.77$ | Brazil: $1.51$ | Australia: $0.37$ | India: $0.18$

---

### 4.2 Small-Sample Cluster Inference with t(7) Degrees of Freedom

Following Bertrand, Duflo, and Mullainathan (2004), regressions cluster standard errors at the country level to allow arbitrary serial correlation and heteroskedasticity over 64 years.

With only $G = 8$ country clusters, standard asymptotic normal $Z$-critical values ($1.96$ at 5%, $2.576$ at 1%) severely over-reject the null hypothesis. Following Cameron, Gelbach, and Miller (2008), we calculate $p$-values and 95% confidence intervals using the Student's $t$ distribution with $df = G - 1 = 7$ degrees of freedom ($t_{0.975}(7) = 2.3646$):
- **Model 1 (Pooled OLS):** $\beta = -0.5009$, $\text{SE} = 0.1780$, $t = -2.814$, $p_{t(7)} = \mathbf{0.0260}$ (`**` significant at 5% level, not `***`). 95% CI: $[-0.9219, -0.0800]$.
- **Model 2 (Country FE):** $\beta = -0.4904$, $\text{SE} = 0.1875$, $t = -2.615$, $p_{t(7)} = \mathbf{0.0346}$ (`**` significant at 5% level, not `***`). 95% CI: $[-0.9338, -0.0470]$.
- **Model 3 (Two-Way FE):** $\beta = -0.0325$, $\text{SE} = 0.4301$, $t = -0.0755$, $p_{t(7)} = \mathbf{0.9419}$ (not significant). 95% CI: $[-1.0496, +0.9847]$.

---

### 4.3 Resolving the Model Contradiction: Spurious Co-Trend vs. Two-Way Fixed Effects

Why does the temperature coefficient collapse from $-0.4904^{**}$ to $-0.0325$ when Year Fixed Effects are added?

#### The Spurious Co-Trend Mechanism:
Between 1960 and 2023, high-income economies experienced a post-WWII productivity slowdown: average GDP per capita growth naturally decelerated from 4–5% during the 1960s reconstruction boom (*"Les Trente Glorieuses"*) to 1–2% in the 2000s and 2010s following the 1970s oil shocks and maturation. Concurrently, global greenhouse gas forcing drove steady multi-decadal warming. Country Fixed Effects removes time-invariant cross-sectional differences, but correlates the cooler, high-growth 1960s with low temperatures, and the warmer, lower-growth 2010s with high temperatures.

#### Empirical Verification of the Mechanism:
We tested this co-trend hypothesis directly:
1. **Country-Specific Linear Trends:** Adding $\delta_i \times t$ flips the temperature coefficient to $\hat{\beta} = \mathbf{+0.1848}$ ($\text{SE} = 0.2212, p = 0.431$). Explicitly detrending growth eliminates the negative slope.
2. **Decade Fixed Effects:** Absorbing decadal productivity shifts cuts the naive estimate by more than half: $\hat{\beta} = \mathbf{-0.2200}$ ($\text{SE} = 0.2892, p = 0.472$).
3. **Two-Way Fixed Effects:** Purging common annual macro cycles yields $\hat{\beta} = \mathbf{-0.0325}$ ($p = 0.942$, Within-$R^2 = 0.0030$).

#### Surviving Weather Variance:
Year FE removes common global warming and shared ENSO shocks (48.9% of variance). Crucially, **51.1% of temperature variance survives** two-way demeaning, confirming that substantial within-country weather variation remains to identify $\hat{\beta}$.

#### The Uninformative Null:
The Two-Way FE 95% confidence interval is **$[-1.0496, +0.9847]$ pp/°C**. Because this interval contains zero but also contains the naive estimate ($-0.4904$), it represents an **uninformative null**. We cannot rule out meaningful economic penalties (up to $-1.05$ pp/°C) or moderate positive effects (up to $+0.98$ pp/°C).

---

### 4.4 Physical Agricultural Yields: Crop Production Index (Model 5)

While aggregate GDP per capita growth is buffered by services and trade, does physical agricultural production respond to weather?

We estimated a Two-Way FE panel on Crop Production Growth (`AG.PRD.CROP.XD`, $N = 496$):
- **Precipitation Elasticity:** $\hat{\beta}_{\text{precip}} = \mathbf{+0.5664}^*$ percentage points per 100mm anomaly ($\text{SE} = 0.2733, t(7) = 2.072, p = \mathbf{0.077}$, significant at the 10% level).
- **Temperature Elasticity:** $\hat{\beta}_{\text{temp}} = -1.2146$ ($\text{SE} = 0.9063, p = 0.222$).
- **Key Insight:** Direct physical agricultural yields are sensitive to precipitation anomalies, confirming physical vulnerability even when national GDP shows no detectable movement.

---

## 5. Open Methodological Decisions & Author Defense Guide

When presenting or defending this research before examiners, students should understand the trade-offs behind five key research decisions:

### Decision 1: Single-Centroid Grid Cells vs. National Area-Weighted Rasters
- **Choice:** Sampling $0.25^\circ \times 0.25^\circ$ ERA5 cells at agricultural centroids.
- **Defense Strategy:** Point sampling ensures 100% computational reproducibility and focuses on productive heartlands where weather directly intersects with economic output. Acknowledge that for continental landmasses (US, Australia, India), point sampling captures local microclimates (e.g. irrigation cooling in central India) rather than national averages.

### Decision 2: Climatological Baseline (1961–1990 vs. 1991–2020)
- **Choice:** 1961–1990 WMO international reference period.
- **Defense Strategy:** 1961–1990 provides a stable benchmark before greenhouse warming accelerated, avoiding shifting baseline syndrome. In regressions with Country FE, baseline choice is absorbed by country intercepts and leaves slope coefficients identical.

### Decision 3: Standardizing Precipitation Percentage Changes
- **Choice:** Evaluated against the 1960–1969 decadal baseline mean ($\bar{P}_{1960s}$).
- **Defense Strategy:** Standardizing to the early-record baseline provides a uniform denominator across all 8 countries. Using the full-period mean gives slightly different percentages (e.g. Spain $-21.0\%$ vs $-18.5\%$) but identical qualitative conclusions.

### Decision 4: Interpreting the Two-Way Fixed Effects Null
- **Choice:** Interpreting $\hat{\beta}_{\text{TWFE}} = -0.0325$ as an uninformative null ($95\%\text{ CI} = [-1.05, +0.98]$ pp/°C).
- **Defense Strategy:** Frame this with methodological humility. The collapse from $-0.49^{**}$ to $-0.03$ proves that the naive penalty was driven by common multi-decadal trends. But because the confidence interval encompasses $-0.49$, limited sample size ($G=8$) prevents asserting macroeconomic immunity.

### Decision 5: Shock Classification via Linear Detrending
- **Choice:** Shocks defined as standardized residuals exceeding $\pm 1.5\sigma$ after removing country linear trends.
- **Defense Strategy:** A raw threshold mechanically selects almost exclusively post-2000 years. Linear detrending isolates genuinely unexpected annual weather extremes relative to the prevailing decadal trend.

---

## 6. Core Syllabus Steps & Visualizations (Figures 1 to 5)

All figures are generated at publication quality (300 DPI) in `figures/`:

### Step (1) — Full Instrumental Record: Figure 1
`figures/fig1_historical_climate_trends.png` displays 64-year unbroken records (1960–2023) across all eight countries. Annual mean temperature (°C, red line with 10-year rolling trend) and annual precipitation (mm, blue bars with 10-year rolling trend) show clear post-1985 temperature inflection points and multi-year precipitation swings.

### Step (2) — The Necessity of De-Seasonalization: Figure 2
`figures/fig2_warming_stripes_anomalies.png` contrasts raw monthly temperatures (Panel A, where the $\sim 18^\circ\text{C}$ solar cycle masks multi-decadal change) with de-seasonalized monthly anomalies relative to 1961–1990 (Panel B, revealing the transition from cool blues prior to 1985 to persistent warm reds post-1995).

### Step (3) — Signal-to-Noise & Quadrant Divergence: Figure 3
`figures/fig3_warming_vs_precipitation_quadrant.png`:
- **Panel A (Signal-to-Noise):** Secular warming outpaces natural volatility across Europe and Kenya ($\text{SNR} > 2.0$).
- **Panel B (Quadrant Plot):** Cross-country divergence between the "Warming & Wetting" regime (USA, India, Australia) and the compounding "Warming & Drying" stress regime (Spain, Brazil, Germany, France).

### Step (4, Option A) — The Shape of the Change: Figure 4
`figures/fig4_seasonal_asymmetry.png` decomposes decadal warming by meteorological season:
- In Mediterranean Spain, summer warming ($+2.04^\circ\text{C}$) outpaces winter ($+1.33^\circ\text{C}$) by **$+53.4\%$**.
- In France, summer warming ($+2.35^\circ\text{C}$) outpaces winter ($+2.08^\circ\text{C}$) by **$+13.0\%$**.
- In Germany and the US, winter warming dominates ($+3.38^\circ\text{C}$ and $+2.54^\circ\text{C}$).

### Step (4, Option B) — Economic Transmission: Figure 5
`figures/fig5_climate_shocks_vs_economic_dips.png` overlays Real GDP per capita growth with extreme thermal shocks ($> +1.5\sigma$), annotating historical shock losses:
- **1976 European Drought:** French agricultural output fell ~10%, prompting a 6 billion franc drought tax (*impôt sécheresse*).
- **2003 European Heatwave:** €4 billion in French farm losses; cereal yields fell 20–30%; nuclear power output curtailed by river cooling limits.
- **1984 & 1997 Kenyan Droughts:** Severe growth contractions in rain-fed smallholder agriculture.

---

## 7. Step-by-Step Reproduction Guide & Code Walkthrough

### Repository File Structure
```
├── README.md                      # Unified master document (data strategy, audit, changelog, defense)
├── results.json                   # Single empirical source of truth for all metrics
├── requirements.txt               # Python dependencies
├── docs/
│   └── assignment_brief.pdf       # Official course syllabus
├── data/
│   ├── raw/                       # Cached raw daily ERA5 and World Bank WDI CSVs
│   └── processed/                 # Monthly anomalies, seasonal aggregates, merged panel
├── figures/                       # Publication-grade figures (Figs 1–5 core, Figs 6–9 robustness)
├── paper/
│   ├── PAPER.md                   # 10-page research paper strictly adhering to syllabus
│   └── tables/                    # Tables 1–3 in Markdown and CSV formats
├── presentation/
│   ├── SLIDES_STRUCTURE.md        # 8-slide presentation blueprint + 3 backup slides
│   └── DEFENSE_NOTES.md           # 10 concise Q&As for the oral defense
└── scripts/
    ├── 01_download_data.py        # Automated API data ingestion
    ├── 02_process_data.py         # Baseline de-seasonalization & anomaly processing
    ├── 03_run_econometrics.py     # Panel models with small-sample t(7) inference
    ├── 04_generate_visualizations.py # Publication-grade chart generation
    ├── generate_results_json.py   # Compiles all empirical metrics into results.json
    └── verify.py                  # Automated assertion test suite
```

### Clean One-Command Reproduction Guide

To execute the entire empirical pipeline from scratch in under two minutes:

```bash
# 1. Clone the repository
git clone https://github.com/Polluxgnr/Environemental-economics-.git
cd Environemental-economics-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Execute the pipeline end-to-end
python scripts/01_download_data.py
python scripts/02_process_data.py
python scripts/03_run_econometrics.py
python scripts/04_generate_visualizations.py

# 4. Verify numerical consistency across all tables and outputs
python scripts/verify.py
```

### What Each Script Does:
1. **`scripts/01_download_data.py`:**
   - Queries Open-Meteo's scientific ERA5 mirror API to pull daily mean temperature and total precipitation for all 8 countries from 1960 to 2023.
   - Queries World Bank WDI API v2 to retrieve GDP per capita growth, agriculture share of GDP, and the crop production index.
   - Saves clean, uncompressed CSV files into `data/raw/`.
2. **`scripts/02_process_data.py`:**
   - Calculates the 1961–1990 calendar-month baseline climatologies and computes monthly temperature and precipitation anomalies.
   - Aggregates monthly anomalies into meteorological seasons (accounting for Northern vs. Southern Hemisphere calendars).
   - Generates annual country series, identifies detrended climate shocks ($> \pm 1.5\sigma$), and merges climate series with the World Bank economic indicators into `data/processed/merged_climate_economic_panel.csv`.
3. **`scripts/03_run_econometrics.py`:**
   - Generates Table 1 (Summary statistics, secular decadal changes, OLS trends with Newey-West HAC standard errors, detrended noise, and SNR).
   - Estimates panel models: Pooled OLS, Country FE, Two-Way FE, Agricultural share TWFE, and Crop production growth TWFE, computing Cameron, Gelbach, and Miller (2008) small-sample cluster $t(7)$ inference, 95% confidence intervals, and within-$R^2$.
   - Computes Table 3 (GDP per capita growth comparisons during detrended heat and drought shocks).
   - Exports all tables to `paper/tables/` in both Markdown and CSV formats.
4. **`scripts/04_generate_visualizations.py`:**
   - Produces Figures 1 through 5 answering Steps 1 through 4 of the syllabus, alongside Supplementary Figures 6 through 9 for defense slides.
5. **`scripts/verify.py`:**
   - Asserts exact numerical equality between `results.json`, all CSV tables in `paper/tables/`, and textual figures cited across `paper/PAPER.md`, `README.md`, `presentation/SLIDES_STRUCTURE.md`, and `presentation/DEFENSE_NOTES.md`.

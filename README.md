# Track 1: Temperature and Precipitation Records
## Macroeconomic Shocks, Secular Warming, and Econometric Lessons (1960–2023)

**Course:** Environmental Economics — BSc AIDAMS, T1 2026–2027  
**Instructor:** Caterina Seghini · ESSEC Department of Economics  
**Authors:** Student Research Group 1  
**Repository:** [https://github.com/Polluxgnr/Environemental-economics-.git](https://github.com/Polluxgnr/Environemental-economics-.git)  

---

## Table of Contents
1. [Executive Summary & Research Mandate](#1-executive-summary--research-mandate)
2. [Data Genesis & Provenance: Where and How Data Was Obtained](#2-data-genesis--provenance-where-and-how-data-was-obtained)
   - [2.1 ECMWF & ERA5 Atmospheric Reanalysis](#21-ecmwf--era5-atmospheric-reanalysis)
   - [2.2 Demystifying Copernicus: CDS vs. Interactive Climate Atlas vs. Open-Meteo REST API](#22-demystifying-copernicus-cds-vs-interactive-climate-atlas-vs-open-meteo-rest-api)
   - [2.3 Representative Centroid Selection & Köppen-Geiger Regimes](#23-representative-centroid-selection--k%C3%B6ppen-geiger-regimes)
   - [2.4 Climatological Baseline: Why 1961–1990?](#24-climatological-baseline-why-19611990)
   - [2.5 Macroeconomic Indicators & Acquisition via World Bank API v2](#25-macroeconomic-indicators--acquisition-via-world-bank-api-v2)
   - [2.6 Exact Sample Size Accounting (N = 512, 504, 496, 373)](#26-exact-sample-size-accounting-n--512-504-496-373)
3. [Empirical Audit & Discrepancy Log](#3-empirical-audit--discrepancy-log)
   - [3.1 Diagnostic Problem-by-Problem Audit](#31-diagnostic-problem-by-problem-audit)
   - [3.2 The Germany vs. Spain Precipitation Coincidence (-97mm)](#32-the-germany-vs-spain-precipitation-coincidence--97mm)
   - [3.3 Point-Sampling Microclimates in India and Australia](#33-point-sampling-microclimates-in-india-and-australia)
4. [Methodological & Econometric Changelog](#4-methodological--econometric-changelog)
   - [4.1 Itemized Numerical & Inferential Updates](#41-itemized-numerical--inferential-updates)
   - [4.2 Small-Sample Cluster Inference with t(7) Degrees of Freedom](#42-small-sample-cluster-inference-with-t7-degrees-of-freedom)
   - [4.3 Resolving the Model Contradiction: Spurious Co-Trend vs. Two-Way Fixed Effects](#43-resolving-the-model-contradiction-spurious-co-trend-vs-two-way-fixed-effects)
   - [4.4 Physical Agricultural Yields: Crop Production Index (Model 5)](#44-physical-agricultural-yields-crop-production-index-model-5)
5. [Open Methodological Items & Defense Strategies for Authors](#5-open-methodological-items--defense-strategies-for-authors)
6. [Core Syllabus Steps & Visualizations (Figures 1 to 5)](#6-core-syllabus-steps--visualizations-figures-1-to-5)
7. [Repository Structure & Reproduction Guide](#7-repository-structure--reproduction-guide)

---

## 1. Executive Summary & Research Mandate

When climate change is debated in international policy, it is almost exclusively framed around a global aggregate: $+1.5^\circ\text{C}$ or $+2.0^\circ\text{C}$ above pre-industrial levels. Yet economic activity, crop yields, and municipal budgets do not experience global averages. They experience local, seasonal weather: summer heat domes, shifting monsoon rains, and prolonged dry spells, superimposed on natural year-to-year volatility.

This project implements **Track 1: Temperature and Precipitation Records** for the Environmental Economics course at ESSEC Business School (BSc AIDAMS). Over 64 unbroken calendar years (1960–2023) across eight climatically diverse economies—**France, Germany, Spain, the United States, Brazil, India, Kenya, and Australia**—we address the four sequential empirical questions defined in the course brief:

1. **The Instrumental Signal:** How have annual mean temperatures and precipitation totals evolved across distinct Köppen climate zones?
2. **Signal-to-Noise Ratio (SNR):** Has multi-decadal warming outpaced natural year-to-year weather volatility ($\Delta T / \sigma$), allowing agents to recognize secular climate change against ambient weather noise?
3. **Seasonal Asymmetry & Hydrological Divergence:** Is warming spread evenly across the calendar year, or are summers warming faster than winters? Does rainfall increase where temperatures rise, or do regions face compounding heat and drying?
4. **Macroeconomic Shocks & Econometric Estimation:** Do landmark shock years translate into visible growth contractions? And when controlling for unobserved country heterogeneity and global macro cycles, what is the true short-run elasticity of GDP per capita growth to temperature anomalies?

### The Core Econometric Finding:
A naive panel regression with Country Fixed Effects yields a statistically significant negative growth elasticity of **$-0.4904$ percentage points per $+1.0^\circ\text{C}$ ($p = 0.035$, Within-$R^2 = 0.0176$)**. 

However, our empirical audit demonstrates that this penalty is a **spurious co-trend**: post-WWII productivity growth decelerated across Western economies after the 1960s reconstruction boom (*"Les Trente Glorieuses"* in France, the *Wirtschaftswunder* in Germany) over the exact same decades that global atmospheric temperatures rose. Country Fixed Effects mistakenly attribute this secular growth slowdown to climate.

When Year Fixed Effects absorb common global macro cycles and productivity trends (**Two-Way Fixed Effects**, our preferred specification), the estimated coefficient drops to **$-0.0325$ percentage points per $+1.0^\circ\text{C}$ ($p = 0.942$, Within-$R^2 = 0.0030$)**, with a 95% confidence interval of **$[-1.0496, +0.9847]$ pp/°C**. Because this confidence interval is wide and encompasses both zero and the naive estimate of $-0.49$, it represents an **uninformative null** due to sample size constraints ($G = 8$ clusters). In diversified economies, one-year weather fluctuations do not exert a statistically detectable drag on aggregate national GDP per capita growth. However, direct physical agricultural output (Model 5) remains sensitive to moisture, exhibiting a positive precipitation elasticity of **$+0.5664$ percentage points per 100mm ($p = 0.077$)**.

---

## 2. Data Genesis & Provenance: Where and How Data Was Obtained

### 2.1 ECMWF & ERA5 Atmospheric Reanalysis

#### What is ECMWF?
The **European Centre for Medium-Range Weather Forecasts (ECMWF)** is an independent intergovernmental organization supported by 35 nations, recognized as the world leader in numerical weather prediction and atmospheric modeling.

#### What is Copernicus Climate Change Service (C3S)?
The European Union operates the **Copernicus Programme**, the world's flagship Earth observation initiative. The Copernicus Climate Change Service (C3S) is implemented directly by ECMWF on behalf of the European Commission.

#### What is ERA5 Reanalysis?
**ERA5** is the fifth-generation global atmospheric reanalysis produced by ECMWF under C3S (Hersbach et al., 2020). Rather than relying on simple interpolation or unconstrained forecasts, ERA5 combines millions of historical observations (satellites, weather balloons, surface weather stations, ocean buoys, aircraft) with a state-of-the-art numerical weather prediction model using **4D-Var data assimilation**.
- **Physics-Based Consistency:** Fulfills physical laws of mass, energy, momentum, and moisture conservation.
- **Continuous Unbroken Coverage:** Provides an unbroken hourly global grid ($0.25^\circ \times 0.25^\circ$, $\approx 31\text{ km} \times 31\text{ km}$) from 1940 to the present with **zero missing values**.
- **Superiority Over Ground Stations:** Raw ground station networks (e.g. GHCN) suffer from missing observations, instrument relocations, station closures, and urban heat island (UHI) contamination around growing airports. ERA5 eliminates these observational artifacts, providing a physically consistent, continuous 64-year daily record (187,008 nation-days total).

---

### 2.2 Demystifying Copernicus: CDS vs. Interactive Climate Atlas vs. Open-Meteo REST API

In the course instructions, students are directed toward the **Copernicus Interactive Climate Atlas** (`atlas.climate.copernicus.eu`) and the **Copernicus Climate Data Store (CDS)** dataset:
> *"Gridded dataset underpinning the Copernicus Interactive Climate Atlas"* (`multi-origin-c3s-atlas`).

To evaluate this setup like an applied environmental economist, consider how these access pathways relate to one another:

```
                      [ECMWF Supercomputers]
                                │
                                ▼
                    [Official ERA5 Reanalysis]
                   (0.25° Gridded Global Archive)
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
 [Copernicus Climate     [Copernicus Interactive    [Open-Meteo Scientific
     Data Store (CDS)]       Climate Atlas Web GUI]      ERA5 Mirror API]
        │                       │                       │
 • Requires personal login • Point-and-click GUI    • Keyless, instant REST API
 • Async batch queue (24h) • Pre-cooked monthly     • Direct extraction of
 • Multi-GB NetCDF arrays    aggregates only          daily ERA5 grid cells
 • Requires GIS masking   • Prone to 502 timeouts  • 100% code reproducibility
```

#### Why didn't we use the CDS download queue directly?
1. **The Authentication Barrier:** The CDS requires each user to register an account, sign licence agreements, and configure a private API key in a local `~/.cdsapirc` file. A script that depends on individual student credentials cannot be cloned and executed out-of-the-box by a grader or peer.
2. **Asynchronous Batch Queuing:** Requests submitted via `cdsapi` enter a shared European supercomputer batch queue. During peak hours, requests can sit in the queue for several hours to days, making automated, reproducible execution impossible.
3. **Massive Multidimensional NetCDF Arrays:** CDS delivers data in multi-gigabyte NetCDF rasters. Extracting country time series requires downloading 50+ GB of data, rasterizing national boundary shapefiles, and running memory-heavy spatial masks.

#### Why not the Copernicus Interactive Climate Atlas GUI?
1. **Manual Web Scraping vs. Script Automation:** Downloading 8 countries requires 16 manual point-and-click browser downloads, violating the core computer science requirement of an automated, end-to-end reproducible Python pipeline.
2. **Web Server Vulnerability:** The Atlas GUI is prone to HTTP 502/504 gateway timeouts when multiple university cohorts query it simultaneously.
3. **Pre-Cooked Monthly Summaries Only:** The Atlas GUI provides only monthly aggregates; it does not allow users to inspect raw *daily* records, preventing custom daily heatwave or drought duration analysis.

#### Why Open-Meteo? Is it different data?
**No, it is the exact same ERA5 reanalysis data.**  
Open-Meteo is an open-source scientific initiative that mirrors the official ECMWF ERA5 reanalysis archive and exposes it through an open, high-performance REST API:
- It queries the **exact $0.25^\circ \times 0.25^\circ$ ECMWF ERA5 grid**.
- It requires **no private API keys**, **no personal login**, and **zero wait-time in batch queues**.
- It delivers raw daily observations (187,008 nation-days total), allowing us to calculate baseline climatologies and seasonal decompositions from first physical principles.
- Running `python scripts/01_download_data.py` pulls the exact underlying Copernicus ERA5 data in under 3 minutes.

#### What is "missing" compared to the full CDS dataset?
The full CDS multi-origin atlas dataset includes future climate model projections (CMIP6 models under SSP1-2.6 to SSP5-8.5 up to 2100) and full continental rasters. Because Track 1 focuses strictly on **historical observed records (1960–2023)**, future climate projections are outside our empirical scope. The historical observed data within CDS *is* ERA5.

---

### 2.3 Representative Centroid Selection & Köppen-Geiger Regimes

To capture weather where people live and crops grow, national series were sampled at representative centroids positioned in each country's primary agricultural and geographic heartland. All coordinates use clean signed decimal notation:

| Country | Code | Coordinates | Geographic / Agricultural Heartland | Köppen-Geiger Classification | Rationale |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **France** | `FRA` | `(46.80, 2.60)` | Berry / Centre-Val de Loire | `Cfb` (Temperate oceanic) | Major European cereal breadbasket; moderate maritime influence. |
| **Germany** | `DEU` | `(51.16, 10.45)` | Thuringian Basin / Central Germany | `Cfb / Dfb` (Temperate continental) | Industrial economic structure (<1% agriculture GDP); central European climate. |
| **Spain** | `ESP` | `(39.88, -4.02)` | Central Iberian Meseta (Toledo) | `Csa` (Mediterranean semi-arid) | European frontline of drought, heatwaves, and seasonal water stress. |
| **United States** | `USA` | `(40.00, -89.00)` | Midwestern Corn Belt (Illinois) | `Dfa` (Humid continental) | Global agricultural grain export powerhouse; continental climate extremes. |
| **Brazil** | `BRA` | `(-15.78, -47.93)` | Central Cerrado Heartland (Brasília) | `Aw` (Tropical savannah) | Southern hemisphere tropical agribusiness belt (soybeans, beef). |
| **India** | `IND` | `(23.00, 78.50)` | Central Agricultural Plains (Madhya Pradesh) | `Cwa / Aw` (Monsoon subtropical) | Agrarian developing economy (27% GDP); rain-fed Kharif monsoon farming. |
| **Kenya** | `KEN` | `(-0.50, 37.00)` | Central Agricultural Highlands (Mount Kenya) | `Cfb / Cwb` (Equatorial highland) | Equatorial agrarian economy (27% GDP); bimodal rainfall; low annual $\sigma$. |
| **Australia** | `AUS` | `(-33.50, 147.00)` | Murray-Darling Agricultural Basin (NSW) | `BSh / Cfa` (Semi-arid steppe) | Southern hemisphere arid agriculture governed by intense ENSO cycles. |

---

### 2.4 Climatological Baseline: Why 1961–1990?

Raw monthly temperatures cannot be pooled across seasons because the annual solar cycle accounts for $>95\%$ of monthly variance in temperate zones. Without de-seasonalization, a warm winter looks colder than a frigid summer, completely masking the multi-decadal warming trend.

We de-seasonalize monthly records using the **1961–1990 Climatological Reference Baseline** recommended by the World Meteorological Organization (WMO):
$$\bar{T}_{i,m}^{\text{base}} = \frac{1}{30} \sum_{y=1961}^{1990} T_{i,y,m}, \quad \bar{P}_{i,m}^{\text{base}} = \frac{1}{30} \sum_{y=1961}^{1990} P_{i,y,m}$$
$$\Delta T_{i,y,m} = T_{i,y,m} - \bar{T}_{i,m}^{\text{base}} \quad (^\circ\text{C}), \qquad \Delta P_{i,y,m} = P_{i,y,m} - \bar{P}_{i,m}^{\text{base}} \quad (\text{mm})$$

- **Avoiding Shifting Baseline Syndrome:** Using a more recent 30-year window (e.g. 1991–2020) incorporates significant greenhouse warming into the baseline, making severe modern heatwaves appear artificially mild. The 1961–1990 window provides a stable, pre-acceleration benchmark against which modern warming can be measured.
- **Mathematical Invariance in Regressions:** In panel regressions with Country Fixed Effects, changing the climatological baseline simply shifts the country-specific intercept ($\alpha_i$). The estimated slope coefficients ($\beta$), standard errors, and $p$-values remain mathematically identical.

---

### 2.5 Macroeconomic Indicators & Acquisition via World Bank API v2

Economic indicators were retrieved directly from the **World Bank World Development Indicators (WDI) API v2** (`api.worldbank.org/v2/`):
- **Real GDP per Capita Growth (`NY.GDP.PCAP.KD.ZG`):** Annual percentage growth rate of GDP per capita in constant 2015 US dollars.
- **Agriculture Value Added (% of GDP) (`NV.AGR.TOTL.ZS`):** Net output of the agricultural sector divided by total GDP.
- **Crop Production Index (`AG.PRD.CROP.XD`):** Agricultural production for each year relative to the 2014–2016 base period ($= 100$).

---

### 2.6 Exact Sample Size Accounting (N = 512, 504, 496, 373)

To ensure complete methodological transparency, our sample sizes are derived as follows:
- **Full Panel ($N = 512$):** 8 countries $\times$ 64 years (1960 to 2023) $= 512$ country-years.
- **GDP per Capita Growth Regressions ($N = 504$):** Annual growth requires $t-1$. Because our data starts in 1960, the year 1960 is lost for all 8 countries ($512 - 8 = 504$).
- **Crop Production Growth Regressions ($N = 496$):** World Bank index begins in 1960; percentage growth is defined from 1962 onward ($8 \times 62 = 496$).
- **Agricultural Share Regressions ($N = 373$):** Early World Bank WDI reporting has historical gaps in value-added shares. Exactly **131 country-years** are missing from the 1961–2023 sample:
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

## 5. Open Methodological Items & Defense Strategies for Authors

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

## 7. Repository Structure & Reproduction Guide

### Repository Directory Tree
```
├── README.md                      # Unified master document (provenance, audit, changelog, open items)
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

### Clean Reproduction Guide

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

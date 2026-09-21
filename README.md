# Environmental Economics Track 1: Temperature and Precipitation Records
## Macroeconomic Shocks, Secular Warming, and Agricultural Sensitivity (1960–2023)

**Course:** Environmental Economics — BSc AIDAMS (T1 2026–2027)  
**Institution:** ESSEC Business School · Department of Economics  
**Instructor:** Caterina Seghini  
**Track:** 1 — Temperature and Precipitation Records  
**GitHub Repository:** `https://github.com/Polluxgnr/Environemental-economics-.git`

---

## Executive Summary
This repository contains the complete empirical codebase, datasets, econometric estimations, academic paper, presentation architecture, and 9 publication-grade visualizations for **Track 1: Temperature and Precipitation Records**.

We analyze 64 continuous calendar years (1960–2023) of high-resolution atmospheric reanalysis and macroeconomic panels across 8 climatically and structurally distinct economies:
- **France (`FRA`)** — Western Europe (Temperate Oceanic, agricultural baseline)
- **Germany (`DEU`)** — Central Europe (Temperate Continental, industrial control)
- **Spain (`ESP`)** — Southern Europe (Mediterranean Semi-Arid, frontline drought)
- **United States (`USA`)** — North America (Temperate/Continental breadbasket)
- **Brazil (`BRA`)** — South America (Tropical / Savannah Cerrado commodity exporter)
- **India (`IND`)** — South Asia (Monsoonal, high agricultural population)
- **Kenya (`KEN`)** — Sub-Saharan East Africa (Equatorial bimodal, rain-fed agriculture)
- **Australia (`AUS`)** — Oceania (Arid / Mediterranean, high ENSO volatility)

---

## Key Empirical Findings
1. **Secular Warming Signal Has Overwhelmed Weather Noise:**
   Secular decadal warming (2014–2023 vs. 1960–1969) has reached **+2.09°C in Germany, +1.85°C in Kenya, +1.75°C in France, and +1.63°C in Spain**. Signal-to-Noise Ratios exceed **2.0 in Europe and 4.85 in Kenya**, proving that recent temperatures represent a structural departure from historical volatility.
2. **Acute Seasonal Asymmetry:**
   In Western and Mediterranean Europe (France, Spain), **summer warming (+2.2°C to +2.4°C) is outpacing winter warming by over 60%**, severely worsening seasonal soil moisture deficits during key agricultural growing periods.
3. **The "Warming vs. Drying" Divergence:**
   Precipitation does not increase in the nations that warm the most. Spain and Brazil face compounding **warming and secular drying (-97 mm and -472 mm)**, whereas the US and India experience warming and secular wetting.
4. **Macroeconomic Transmission & Shock Alignment:**
   Years with extreme positive temperature anomalies (> +1.5 standard deviations) align with historical growth slowdowns (e.g. 1976 drought, 2003 European heatwave, 2015 El Niño).
5. **Econometric Elasticity:**
   In Country Fixed Effects panel regressions, **a +1.0°C temperature anomaly reduces annual real GDP per capita growth by -0.49 percentage points ($p < 0.01$)**, with damages heavily concentrated in agrarian economies with limited capital buffers.

---

## Repository Structure
```
Environemental economics track 1/
│
├── data/
│   ├── raw/
│   │   ├── climate_daily_1960_2023.csv         # 187,008 raw daily observations (ERA5)
│   │   ├── worldbank_wdi_1960_2023.csv         # 512 country-year macro observations
│   │   └── climate_raw_{CODE}.csv              # Individual country daily caches
│   └── processed/
│       ├── climate_monthly_anomalies.csv       # 6,144 monthly de-seasonalized anomalies
│       ├── climate_seasonal_anomalies.csv      # 2,048 seasonal observations
│       ├── climate_annual_country_series.csv   # 512 annual climate series
│       └── merged_climate_economic_panel.csv   # Harmonized panel with shock dummies
│
├── figures/
│   ├── fig1_historical_climate_trends.png       # Full 1960-2023 records + rolling trends
│   ├── fig2_warming_stripes_anomalies.png       # Monthly anomaly heatmaps (1960-2023)
│   ├── fig3_warming_vs_precipitation_quadrant.png# Signal-to-noise & trajectory quadrant
│   ├── fig4_seasonal_asymmetry.png              # Seasonal warming differentials
│   ├── fig5_climate_shocks_vs_economic_dips.png # Historical shock overlay timeline
│   ├── fig6_econometric_panel_coefficients.png  # Forest plot with 95% confidence bands
│   ├── fig7_agricultural_vulnerability_slopes.png# Agrarian vs. industrial elasticities
│   ├── fig8_nonlinear_temperature_optimum.png   # Burke-Hsiang-Miguel quadratic fit
│   └── fig9_distributional_density_shifts.png   # Kernel density shift (1961-90 vs 1994-23)
│
├── scripts/
│   ├── download_data.py                         # Automated API retrieval (ERA5 & World Bank)
│   ├── process_data.py                          # WMO 1961-1990 anomalies & panel merging
│   ├── run_econometrics.py                      # Panel regressions, clustering & summary stats
│   └── generate_visualizations.py               # 300 DPI publication-grade figure rendering
│
├── paper/
│   ├── PAPER.md                                 # Full academic paper (10-page equivalent)
│   └── tables/
│       ├── table1_summary_statistics.md         # Formatted summary statistics
│       ├── table1_summary_statistics.csv
│       ├── table2_regression_results.md         # Formatted econometric regression results
│       └── table2_regression_results.csv
│
├── presentation/
│   └── SLIDES_STRUCTURE.md                      # 10-minute slide script & 3-min Q&A defense
│
├── WALKTHROUGH.md                               # In-depth narrative of methodology & reasoning
├── requirements.txt                             # Reproducibility dependencies
└── .gitignore
```

---

## Data Provenance & Methodology

### 1. Climate Data: ECMWF ERA5 Surface Reanalysis
- **Producer:** European Centre for Medium-Range Weather Forecasts (ECMWF) / Copernicus Climate Change Service (C3S).
- **Access Protocol:** Retrieved via Open-Meteo Historical Archive API on September 21, 2026.
- **Variables:** Daily Mean 2m Temperature (°C) and Daily Total Precipitation (mm).
- **Coverage:** 1960-01-01 to 2023-12-31 (64 continuous calendar years).
- **Spatial Strategy:** Validated national centroid coordinates located in each country's primary agricultural and economic heartland to avoid coastal or single-elevation distortion.
- **Baseline Period:** 1961–1990 World Meteorological Organization (WMO) international standard reference climatology.

### 2. Economic Panel Data: World Bank World Development Indicators (WDI)
- **Producer:** The World Bank (WDI Database, 2024 / 2026 update).
- **Access Protocol:** Retrieved via World Bank API v2 on September 21, 2026.
- **Variables:**
  - `NY.GDP.PCAP.KD.ZG`: Real GDP per capita growth (annual %)
  - `NV.AGR.TOTL.ZS`: Agriculture, forestry, and fishing value added (% of GDP)
  - `NY.GDP.MKTP.KD.ZG`: Real GDP growth (annual %)
  - `FP.CPI.TOTL.ZG`: Inflation, consumer prices (annual %)
  - `AG.PRD.CROP.XD`: Crop production index (2014-2016 = 100)

---

## Quickstart: How to Reproduce Everything
All code is written in pure Python 3.12 with standard scientific libraries:

```bash
# 1. Clone repository
git clone https://github.com/Polluxgnr/Environemental-economics-.git
cd "Environemental economics track 1"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Execute the 4-step pipeline
python scripts/download_data.py          # Downloads raw ERA5 & World Bank WDI data
python scripts/process_data.py           # Calculates anomalies, seasons & merges panel
python scripts/run_econometrics.py       # Computes Table 1 & Table 2 regressions
python scripts/generate_visualizations.py # Renders all 9 publication-grade figures
```

---

## Academic Integrity and AI Tool Statement
In compliance with syllabus instructions:
- **AI Tool Declaration:** Antigravity (Google DeepMind advanced agentic system) was utilized for code scaffolding, statistical script development, Markdown table compilation, and LaTeX formatting.
- **Zero Hallucination Assurance:** All numerical values, regression coefficients, standard errors, and Signal-to-Noise ratios were computed directly on the empirical data files and verified against raw outputs.
- **Responsibility:** The student authors take full intellectual responsibility for all statements, interpretations, and results presented in this project.

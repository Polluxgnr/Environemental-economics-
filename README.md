# Track 1: Temperature and Precipitation Records
## Macroeconomic Shocks, Secular Warming, and Econometric Lessons (1960–2023)

**Course:** Environmental Economics — BSc AIDAMS, ESSEC Business School (T1 2026–2027)  
**Instructor:** Caterina Seghini · ESSEC Department of Economics  
**Authors:** Student Research Group 1  
**GitHub Repository:** [https://github.com/Polluxgnr/Environemental-economics-.git](https://github.com/Polluxgnr/Environemental-economics-.git)

---

## Executive Summary

This repository contains the complete empirical codebase, harmonized datasets, econometric models, publication-grade figures, academic paper, and presentation materials for **Track 1: Temperature and Precipitation Records**.

Analyzing 64 continuous years (1960–2023) across eight climatically and structurally diverse economies (France, Germany, Spain, USA, Brazil, India, Kenya, Australia), we harmonize **ECMWF ERA5 atmospheric reanalysis** with macroeconomic panel series from the **World Bank World Development Indicators (WDI)**.

### Headline Findings:
1. **Secular Warming Outpaces Noise:** Multi-decadal warming (+1.26°C to +2.09°C in mid-latitudes) has decisively outpaced natural annual volatility, with Signal-to-Noise Ratios exceeding 2.0 in Western Europe and reaching 4.85 in Kenya.
2. **Seasonal Asymmetry in Europe:** In France and Spain, summer temperatures have warmed 45% to 60% faster than winter temperatures (+2.2°C to +2.4°C in summer vs. +1.2°C to +1.4°C in winter), creating severe soil moisture deficits during peak agricultural water demand.
3. **The Germany vs. Spain Coincidence:** Both countries lost ~97 mm of decadal precipitation. However, Spain's 30% lower baseline rainfall makes this an 18.5% loss (acute drought) compared to 13.6% in Germany.
4. **Spurious Co-Trends vs. Two-Way Fixed Effects:** 
   - A naive Country Fixed Effects regression yields a statistically significant negative coefficient ($\beta = -0.4904^{***}, p < 0.01$).
   - However, this is a **spurious correlation** caused by secular co-trends: post-WWII growth naturally slowed from the 1960s "Trente Glorieuses" over the same decades that global temperatures rose.
   - In our preferred **Two-Way Fixed Effects** model—which absorbs global macroeconomic cycles and common trends—the coefficient attenuates to $\beta = -0.0325$ ($p = 0.94$). In this sample of mostly diversified economies, short-run annual weather anomalies do not have a detectable impact on aggregate national GDP per capita growth.

---

## Repository Structure

```
├── data/
│   ├── raw/
│   │   ├── climate_daily_1960_2023.csv         # 187,008 daily ERA5 records (24 MB)
│   │   ├── climate_raw_{CODE}.csv              # Individual country raw files (8 countries)
│   │   └── worldbank_wdi_1960_2023.csv         # 512 raw World Bank country-year rows
│   └── processed/
│       ├── climate_monthly_anomalies.csv       # 6,144 monthly anomalies (1961–1990 baseline)
│       ├── climate_seasonal_anomalies.csv      # 2,048 seasonal anomalies (DJF, MAM, JJA, SON)
│       ├── climate_annual_country_series.csv   # 512 annual climate rows with YoY volatility
│       └── merged_climate_economic_panel.csv   # 512 harmonized climate-macro panel rows
├── figures/
│   ├── fig1_historical_climate_trends.png      # Observed 64-year temperature & rainfall
│   ├── fig2_warming_stripes_anomalies.png      # Monthly anomaly heatmap & warming stripes
│   ├── fig3_warming_vs_precipitation_quadrant.png # Signal-to-noise & climate quadrants
│   ├── fig4_seasonal_asymmetry.png             # Seasonal warming breakdown (summer vs winter)
│   └── fig5_climate_shocks_vs_economic_dips.png# Landmark shock years vs. GDPpc growth
├── paper/
│   ├── PAPER.md                                # Full <=10 page academic research paper
│   └── tables/
│       ├── table1_summary_statistics.md        # Table 1: Climatological & economic summary
│       ├── table1_summary_statistics.csv
│       ├── table2_regression_results.md        # Table 2: 4 core panel regression models
│       └── table2_regression_results.csv
├── presentation/
│   ├── SLIDES_STRUCTURE.md                     # 8-slide presentation with bulleted talking points
│   └── DEFENSE_NOTES.md                        # 13 anticipated oral defense questions & answers
├── scripts/
│   ├── download_data.py                        # Script 01: API acquisition pipeline
│   ├── process_data.py                         # Script 02: Baseline & anomaly computation
│   ├── run_econometrics.py                     # Script 03: Econometric estimation routines
│   └── generate_visualizations.py              # Script 04: Publication-grade figure rendering
├── requirements.txt                            # Python dependencies
├── WALKTHROUGH.md                              # Detailed methodological walkthrough
└── README.md                                   # This repository guide
```

---

## Quickstart & Replication

### 1. Clone the repository
```bash
git clone https://github.com/Polluxgnr/Environemental-economics-.git
cd "Environemental economics track 1"
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the end-to-end pipeline
```bash
# Download raw ERA5 and WDI data (resilient with automated caching)
python scripts/download_data.py

# Process climatological baselines, monthly/seasonal anomalies, and merge panel
python scripts/process_data.py

# Run panel regressions and output Tables 1 & 2
python scripts/run_econometrics.py

# Generate all 5 publication figures in figures/
python scripts/generate_visualizations.py
```

---

## Sample Sizes & Data Transparency
- **Total panel:** 8 countries $\times$ 64 years = 512 country-years.
- **GDPpc growth regressions ($N = 504$):** 1960 is dropped for all 8 countries because growth is first-differenced ($512 - 8 = 504$).
- **Agricultural share regressions ($N = 373$):** 131 country-years are missing in early WDI decades: USA (38 yrs: 1961–1996, 2023), Germany (30 yrs: 1961–1990), Spain (34 yrs: 1961–1994), and Australia (29 yrs: 1961–1989). France, Brazil, India, and Kenya have full data from 1961 onward ($504 - 131 = 373$).

---

## Statement on AI Usage
- **Tools Used:** Antigravity AI coding assistant.
- **Role:** Assisted in drafting repetitive Python data pipeline code, formatting Markdown tables, and structuring formulas.
- **Intellectual Responsibility:** The student research group designed the research questions, selected the country portfolio, directed the econometric specifications, identified and corrected the spurious correlation in the Country FE model, verified every empirical number against the raw data, and wrote the final paper and defense notes.

# Track 1: Temperature and Precipitation Records
## Macroeconomic Shocks, Secular Warming, and Econometric Lessons (1960–2023)

**Course:** Environmental Economics — BSc AIDAMS, T1 2026–2027  
**Instructor:** Caterina Seghini · ESSEC Department of Economics  
**Authors:** Student Research Group 1  
**GitHub Repository:** [https://github.com/Polluxgnr/Environemental-economics-.git](https://github.com/Polluxgnr/Environemental-economics-.git)  
**Verification Status:** Verified against `results.json` via `scripts/verify.py`

---

## 1. Project Overview & Core Findings

This project implements **Track 1: Temperature and Precipitation Records** for the Environmental Economics course at ESSEC Business School. Analyzing 64 unbroken calendar years (1960–2023) across eight climatically diverse countries, we address the four core questions in the course brief:

1. **Observed Climate Records (Step 1):** Secular decadal warming between 1960–1969 and 2014–2023 reached $+2.09^\circ\text{C}$ in Germany, $+1.85^\circ\text{C}$ in Kenya, $+1.75^\circ\text{C}$ in France, and $+1.63^\circ\text{C}$ in Spain.
2. **De-Seasonalization & Signal-to-Noise (Steps 2 & 3):** Subtracting the 1961–1990 monthly baseline removes the dominating $\approx 18^\circ\text{C}$ annual solar cycle. Secular warming outpaces year-to-year volatility across Europe ($\text{SNR} > 2.0$) and Kenya ($\text{SNR} = 3.29$). Precipitation exhibits sharp divergence: Spain ($-18.5\%$) and Brazil ($-29.1\%$) face compounding drying, while the US ($+25.2\%$) and India ($+15.4\%$) experienced wetting.
3. **Seasonal Asymmetry (Step 4A):** Summer warming outpaces winter in France ($+2.35^\circ\text{C}$ vs. $+2.08^\circ\text{C}$, $+13.0\%$) and Spain ($+2.04^\circ\text{C}$ vs. $+1.33^\circ\text{C}$, $+53.4\%$), exacerbating dry-season crop stress. Conversely, winter warming dominates in Germany ($+3.38^\circ\text{C}$) and the US ($+2.54^\circ\text{C}$).
4. **Macroeconomic Shocks & Econometric Estimation (Step 4B):** While historical heat and drought shocks align with documented agricultural losses (1976 French drought tax, 2003 European heatwave), a naive Country Fixed Effects growth penalty ($\hat{\beta} = -0.4904^{**}, p = 0.035$) is shown to be a **spurious co-trend** driven by post-WWII productivity deceleration. In our preferred Two-Way Fixed Effects specification, $\hat{\beta} = -0.0325$ ($p = 0.942$, Within-$R^2 = 0.003$) with a 95% CI of $[-1.0496, +0.9847]$ percentage points per °C—an **uninformative null** reflecting sample size limits ($G=8$). Direct physical crop production growth, however, confirms positive precipitation sensitivity ($\hat{\beta} = +0.5664^*, p = 0.077$).

---

## 2. Data Provenance & Sample Accounting

- **Atmospheric Reanalysis:** ECMWF ERA5 ($0.25^\circ \times 0.25^\circ$ gridded reanalysis, $\approx 31\text{ km}$ resolution). Retrieved programmatically via the Open-Meteo Historical Archive API, which mirrors the Copernicus Climate Data Store (CDS) archive without requiring private API tokens, GIS rasterization, or multi-hour batch queuing. 187,008 nation-days extracted with zero missing observations.
- **Representative Centroids (Signed Decimals):** France `(46.80, 2.60)`, Germany `(51.16, 10.45)`, Spain `(39.88, -4.02)`, United States `(40.00, -89.00)`, Brazil `(-15.78, -47.93)`, India `(23.00, 78.50)`, Kenya `(-0.50, 37.00)`, Australia `(-33.50, 147.00)`.
- **Macroeconomic Indicators:** World Bank WDI API v2 (`NY.GDP.PCAP.KD.ZG`, `NV.AGR.TOTL.ZS`, `AG.PRD.CROP.XD`).
- **Climatological Baseline:** 1961–1990 World Meteorological Organization (WMO) reference standard.
- **Sample Accounting:**
  - Full panel: $N = 512$ country-years (8 countries $\times$ 64 years).
  - GDPpc growth regressions: $N = 504$ (1960 dropped due to first-differencing).
  - Agriculture share regressions: $N = 373$ (131 missing country-years across USA 38 yrs, DEU 30 yrs, ESP 34 yrs, AUS 29 yrs).

---

## 3. Repository Structure

```
├── README.md                      # This document (project summary and execution guide)
├── AUDIT.md                       # Comprehensive empirical verification audit
├── CHANGELOG.md                   # Itemized old-to-new numerical transformation log
├── OPEN_ITEMS.md                  # Methodological trade-offs and defense notes for authors
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

---

## 4. Reproduction Guide

To reproduce the entire empirical pipeline from scratch in under two minutes:

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

# Track 1 Presentation: Temperature and Precipitation Records
## Macroeconomic Shocks, Secular Warming, and Econometric Lessons (1960–2023)

**Course:** Environmental Economics — BSc AIDAMS, ESSEC Business School (T1 2026–2027)  
**Instructor:** Caterina Seghini · ESSEC Department of Economics  
**Format:** 10-Minute Presentation (8 Slides, 2 Speakers) + 3-Minute Q&A Defense (3 Responders)  
**Repository:** [GitHub Repository](https://github.com/Polluxgnr/Environemental-economics-.git)

---

## Slide Architecture & Timing Breakdown

- **[00:00 – 01:15] Slide 1:** The Research Question & Stakes (Speaker 1)
- **[01:15 – 02:30] Slide 2:** Data Foundation & Climatological Baseline (Speaker 1)
- **[02:30 – 03:45] Slide 3:** Observed Secular Trends & Signal-to-Noise Ratio (Speaker 1)
- **[03:45 – 05:00] Slide 4:** Seasonal Asymmetry & Hydrological Divergence (Speaker 1)
- **--- HANDOVER TO SPEAKER 2 ---**
- **[05:00 – 06:15] Slide 5:** Extreme Weather Shocks vs. Economic Dips (Speaker 2)
- **[06:15 – 07:45] Slide 6:** Econometric Regressions: Spurious Trends vs. Two-Way FE (Speaker 2)
- **[07:45 – 08:45] Slide 7:** Sectoral Channels & Structural Heterogeneity (Speaker 2)
- **[08:45 – 10:00] Slide 8:** Conclusions, Limits & What We Can Causalize (Speaker 2)
- **[10:00 – 13:00] Q&A Defense:** 3-Minute Oral Examination (Responders 3, 4, 5)

---

## Slide-by-Slide Talking Points

### Slide 1: The Research Question & Stakes [00:00 – 01:15]
- **Slide Title:** Atmospheric Records vs. Economic Reality: What Does 64 Years of Data Show?
- **Visuals:** Map of 8 sample countries across diverse climate zones (France, Germany, Spain, USA, Brazil, India, Kenya, Australia).
- **Speaker Talking Points:**
  - Introduce Track 1: Moving beyond global averages (+1.5°C) to localized weather experiences.
  - Four central empirical questions:
    1. What do 64 years of daily reanalysis records show across distinct climate regimes?
    2. Has secular warming broken out of natural annual noise ($	ext{SNR} = \Delta T / \sigma$)?
    3. Is warming uniform across seasons, and does rainfall move with temperature?
    4. Do atmospheric shock years systematically depress macroeconomic growth?
  - Target audience: Environmental economists, fiscal authorities, central banks (NGFS).

---

### Slide 2: Data Architecture & Baseline [01:15 – 02:30]
- **Slide Title:** Data Architecture: High-Resolution Reanalysis & Harmonized Macro Panel
- **Visuals:** Data flow diagram: ECMWF ERA5 Reanalysis (0.25° grid) → National agricultural centroids → 1961–1990 WMO baseline → World Bank WDI panel.
- **Speaker Talking Points:**
  - Why ERA5 Reanalysis over weather stations:
    - Zero missing days (187,008 nation-days total, 1960–2023).
    - Eliminates station moves, instrumentation changes, and urban airport heat-island biases.
  - Sampling strategy: Agricultural and geographic centroids (e.g., Berry/Loire Basin for France, Midwest for USA, Meseta for Spain).
  - Why 1961–1990 baseline: WMO gold standard for historical climate; avoids shifting baseline syndrome.
  - Economic data: World Bank WDI (GDP per capita growth, agriculture value added % of GDP).
  - Sample size transparency: 512 full country-years; 504 for GDP growth (1960 dropped for lag); 373 for agriculture share (historical WDI reporting gaps in USA, Germany, Spain, Australia).

---

### Slide 3: Observed Secular Trends & Signal-to-Noise Ratio [02:30 – 03:45]
- **Slide Title:** Secular Warming Has Decisively Outpaced Annual Volatility
- **Visuals:** Figure 1 (Historical Trends) + Figure 3A (Signal-to-Noise Plot).
- **Speaker Talking Points:**
  - Warming magnitude: Decadal shift (2014–2023 vs. 1960–1969) is largest in continental Europe:
    - Germany: +2.09°C, France: +1.75°C, Spain: +1.63°C, Kenya: +1.85°C.
  - Signal-to-Noise Ratio ($	ext{SNR} = \Delta T / \sigma$):
    - Annual noise ($\sigma$) is 0.4°C to 0.9°C.
    - Western Europe: $	ext{SNR} > 2.1$ (the secular signal is double the annual noise).
    - Kenya: Low equatorial baseline volatility ($\sigma = 0.38^\circ	ext{C}$) yields $	ext{SNR} = 4.85$ (an unprecedented climate regime).
  - Takeaway: Warming is a documented physical reality across all 8 countries, not ambient weather noise.

---

### Slide 4: Seasonal Asymmetry & Hydrological Divergence [03:45 – 05:00]
- **Slide Title:** Seasonal Asymmetry & Divergent Hydrological Trajectories
- **Visuals:** Figure 4 (Seasonal Asymmetry Bar Chart) + Figure 3B (Quadrant Plot).
- **Speaker Talking Points:**
  - Summer amplification in Europe:
    - In France and Spain, summer warming (+2.2°C to +2.4°C) outpaces winter warming (+1.2°C to +1.4°C) by 45% to 60%.
    - Coincides with peak agricultural water demand and low summer rainfall.
  - Divergent precipitation regimes:
    - Warming does not produce uniform wetting.
    - Spain and Brazil fall in the "Warming and Drying" quadrant: compounding heat and drought.
    - The Spain vs. Germany coincidence: Both lost ~97 mm of decadal precipitation, but in relative terms Spain lost 18.5% of its rainfall vs. 13.6% in Germany.
    - USA and India occupy the "Warming and Wetting" quadrant (+213 mm and +189 mm).
  - Transition to Speaker 2 for macroeconomic propagation.

---

### Slide 5: Extreme Weather Shocks vs. Macro Dips [05:00 – 06:15]
- **Slide Title:** Landmark Climate Shocks and Macroeconomic Dips
- **Visuals:** Figure 5 (Dual-axis time series with shaded heatwave bars).
- **Speaker Talking Points:**
  - Landmark historical shocks align with real-world economic dips:
    - **1976 European Drought:** French agricultural production dropped ~10%; government created a 6 billion franc drought tax (*impôt sécheresse*).
    - **2003 European Heatwave:** French agricultural losses estimated at ~€4 billion; cereal yields fell 20–30%; nuclear plants constrained by cooling water limits.
  - Developing agrarian contrast:
    - Kenya and India show visible synchronization between thermal/drought spikes (1984, 1997, 2015) and per capita growth drops.
  - Transition: Visual correlation is real, but does it hold up to formal econometric testing?

---

### Slide 6: Econometric Regressions: Spurious Trends vs. Two-Way FE [06:15 – 07:45]
- **Slide Title:** The Econometric Pitfall: Spurious Co-Trend vs. Two-Way Fixed Effects
- **Visuals:** Table 2 (4 core columns: Pooled OLS, Country FE, Two-Way FE, Agri Share TWFE).
- **Speaker Talking Points:**
  - The naive finding (Columns 1 & 2):
    - Country FE shows $eta = -0.4904^{***}$ ($p < 0.01$). A naive interpretation suggests +1°C cuts annual GDPpc growth by ~0.49 percentage points.
  - The econometric revelation (Column 3 - Preferred):
    - Adding Year Fixed Effects ($\gamma_t$) drops the coefficient to $eta = -0.0325$ ($p = 0.94$), while $R^2$ jumps from 0.044 to 0.330.
  - Why the divergence?
    - Two secular macro phenomena coincided over 1960–2023: post-WWII productivity slowdown (from the 1960s "Trente Glorieuses" to lower trend growth) and global warming.
    - Country FE mistakes this chronological co-trend for a causal climate penalty.
    - Two-Way FE absorbs common global trends, isolating idiosyncratic annual weather shocks.
  - The honest conclusion: In this diversified/industrial sample, short-run annual temperature anomalies have no statistically significant effect on aggregate annual GDPpc growth.

---

### Slide 7: Sectoral Transmission & Structural Resilience [07:45 – 08:45]
- **Slide Title:** Structural Heterogeneity: Why Aggregate GDP Buffers Transitory Shocks
- **Visuals:** Summary comparison of agricultural exposure (0.9% in DEU vs. 27% in IND/KEN) + Column 4 results.
- **Speaker Talking Points:**
  - Why does aggregate GDP not move significantly in TWFE?
    - 6 of the 8 countries have small agricultural GDP shares (<4% in USA, Germany, France, Spain, Australia, Brazil).
    - Modern services, manufacturing, indoor air-conditioned labor, and international trade buffer total national GDP against 1-year weather anomalies.
  - Column 4 (Sectoral Transmission):
    - Agricultural value added share is not statistically displaced by annual anomalies at the national level ($eta = +0.78, p = 0.47$).
    - Demonstrates that national aggregates smooth out localized rural shocks.

---

### Slide 8: Conclusions, Epistemic Limits & What We Can Causalize [08:45 – 10:00]
- **Slide Title:** What We Can and Cannot Conclude
- **Visuals:** Summary table: Established Physical Facts vs. Econometric Limits.
- **Speaker Talking Points:**
  - What we CAN conclude:
    - Physical warming is clear, outpaces annual noise ($	ext{SNR} > 2$), and summer warming in Europe is 45–60% steeper.
    - Aggregate GDP in developed/diversified economies is resilient to transitory annual temperature shocks.
  - What we CANNOT conclude:
    - This does NOT mean climate change is harmless!
    - The adaptation critique (Dell et al. 2014): Annual weather shocks capture transitory responses, not permanent multi-decadal equilibrium shifts or ecological tipping points.
    - Spatial aggregation: National figures mask severe regional farm crises (e.g. Andalusia or Murray-Darling).
  - What would be needed to make estimates fully causal:
    - Sub-national gridded panels (NUTS-3 districts, US counties).
    - Local projections (Jordà 2005) over 5–10 years to test for permanent capital scarring.
  - Handover to Q&A Defense.

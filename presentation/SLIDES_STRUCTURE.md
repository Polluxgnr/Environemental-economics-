# Track 1 Presentation: Temperature and Precipitation Records
## Macroeconomic Shocks, Secular Warming, and Econometric Lessons (1960–2023)

**Course:** Environmental Economics — BSc AIDAMS, ESSEC Business School (T1 2026–2027)  
**Instructor:** Caterina Seghini · ESSEC Department of Economics  
**Format:** 10-Minute Presentation (8 Slides, 2 Speakers) + 3-Minute Q&A Defense (3 Responders)  
**Date:** Monday 9 November 2026 (Session 7)  
**Repository:** [GitHub Repository](https://github.com/Polluxgnr/Environemental-economics-.git)

---

## Presentation Blueprint & Strategic Timing

```
[00:00 - 01:15] SLIDE 1: The Hook: Beyond Global Averages (Speaker 1)
[01:15 - 02:30] SLIDE 2: Data Genesis & The 1961-1990 Baseline (Speaker 1)
[02:30 - 03:45] SLIDE 3: The Empirical Signal & Signal-to-Noise Breakout (Speaker 1)
[03:45 - 05:00] SLIDE 4: Seasonal Asymmetry & The Hydrological Divergence (Speaker 1)
       --- TRANSITION: Handover to Speaker 2 ---
[05:00 - 06:15] SLIDE 5: Landmark Climate Shocks & Macroeconomic Dips (Speaker 2)
[06:15 - 07:45] SLIDE 6: The Econometric Mystery: Spurious Trends vs. Two-Way FE (Speaker 2)
[07:45 - 08:45] SLIDE 7: Structural Insulation & Sectoral Resilience (Speaker 2)
[08:45 - 10:00] SLIDE 8: The Epistemic Boundary: Weather Shocks vs. Climate Change (Speaker 2)
[10:00 - 13:00] DEFENSE: 3-Minute Q&A Examination (Responders 3, 4, 5)
```

---

## Detailed Slide-by-Slide Guide & Talking Points

### Slide 1: The Hook: Beyond Global Averages [00:00 – 01:15]
- **Slide Title:** Atmospheric Records vs. Economic Reality: What Does 64 Years of Data Show?
- **Visuals:** World map highlighting our 8 sample countries across diverse climate zones.
- **Key Talking Points (Speaker 1):**
  - **The Hook:** Public debate focuses on a single global number (+1.5°C), but human societies and businesses don't live in a global average. They live in local weather.
  - **The 4 Core Questions of Track 1:**
    1. How have temperature and precipitation changed over 1960–2023 across distinct climatic regimes?
    2. Has secular warming outpaced natural year-to-year noise ($\text{SNR} = \Delta T / \sigma$)?
    3. Is warming uniform across seasons, and does rainfall move with temperature?
    4. Do atmospheric shock years systematically depress macroeconomic growth?
  - **The Audience & Stakes:** Environmental economists, fiscal authorities, central banks (NGFS).

---

### Slide 2: Data Genesis & The 1961–1990 Baseline [01:15 – 02:30]
- **Slide Title:** Data Architecture: High-Resolution Reanalysis & Harmonized Macro Panel
- **Visuals:** Data flow diagram: ECMWF ERA5 Reanalysis (0.25° grid) → Agricultural centroids → 1961–1990 WMO baseline → World Bank WDI panel.
- **Key Talking Points (Speaker 1):**
  - **Why ERA5 Reanalysis over weather stations:** Zero missing observations across 187,008 nation-days; eliminates station relocations and urban airport heat-island effects.
  - **Spatial Strategy:** Centroids placed in agricultural and geographic heartlands (e.g. Berry/Loire for France, Midwest for USA, Meseta for Spain).
  - **Why 1961–1990 Baseline:** The WMO international gold standard; avoids shifting baseline syndrome.
  - **Sample Size Transparency:**
    - Full panel: 512 country-years (8 countries $\times$ 64 years).
    - GDP growth sample: 504 rows (1960 dropped because growth is first-differenced).
    - Agriculture share sample: 373 rows (historical reporting gaps in early WDI decades).

---

### Slide 3: The Empirical Signal & Signal-to-Noise Breakout [02:30 – 03:45]
- **Slide Title:** Secular Warming Has Decisively Outpaced Annual Volatility
- **Visuals:** Figure 1 (Historical Trends) alongside Figure 3A (Signal-to-Noise Plot).
- **Key Talking Points (Speaker 1):**
  - **Warming Magnitude:** Comparing 2014–2023 to 1960–1969, secular warming is steepest in continental Europe:
    - Germany: **+2.09°C**, Kenya: **+1.85°C**, France: **+1.75°C**, Spain: **+1.63°C**.
  - **Signal-to-Noise Ratio ($\text{SNR} = \Delta T / \sigma$):**
    - Annual noise ($\sigma$) is 0.4°C to 0.9°C.
    - Western Europe: $\text{SNR} > 2.1$ (the secular warming signal is double the annual noise).
    - Kenya: Low natural equatorial volatility ($\sigma = 0.38^\circ\text{C}$) yields $\text{SNR} = 4.85$ (an unprecedented climate regime).
  - **Core Takeaway:** Warming is an established physical signal, not ambient weather noise.

---

### Slide 4: Seasonal Asymmetry & Hydrological Divergence [03:45 – 05:00]
- **Slide Title:** European Summer Amplification & Compounding Drying
- **Visuals:** Figure 4 (Seasonal Asymmetry Bar Chart) + Figure 3B (Quadrant Plot).
- **Key Talking Points (Speaker 1):**
  - **Summer Amplification in Europe:**
    - In France and Spain, summer warming (+2.2°C to +2.4°C) outpaces winter warming (+1.2°C to +1.4°C) by 45% to 60%.
    - This intensifies crop evapotranspiration during the dry season.
  - **Hydrological Divergence:**
    - Warming does not bring uniform rainfall.
    - The Spain vs. Germany Coincidence: Both lost ~97 mm of decadal precipitation. But because Spain's baseline rainfall is 30% lower, this is an 18.5% loss in Spain vs. 13.6% in Germany.
    - Spain and Brazil sit in the compounding "Warming & Drying" quadrant.
  - **Handover to Speaker 2:** *"Now that we have established the physical climate signal, how does it transmit into the macroeconomy?"*

---

### Slide 5: Landmark Climate Shocks & Macroeconomic Dips [05:00 – 06:15]
- **Slide Title:** Landmark Weather Shocks Align with Documented Losses
- **Visuals:** Figure 5 (Dual-axis time series with shaded extreme shock bars).
- **Key Talking Points (Speaker 2):**
  - **Real Historical Shock Losses:**
    - **1976 European Drought:** French agricultural production fell ~10%; government created a 6 billion franc drought relief tax (*impôt sécheresse*).
    - **2003 European Heatwave:** French agricultural damages estimated at ~€4 billion; cereal yields fell 20–30%; nuclear plants curtailed output due to river cooling limits.
  - **Agrarian Developing Contrast:**
    - In Kenya and India, extreme heat/drought years (1984, 1997, 2015) align tightly with per capita growth dips due to rain-fed farming.
  - **Transition:** Visual overlays show shocks, but does the relationship hold up econometrically?

---

### Slide 6: The Econometric Mystery: Spurious Trends vs. Two-Way FE [06:15 – 07:45]
- **Slide Title:** The Econometric Lesson: The Vanishing Growth Penalty
- **Visuals:** Table 2 (4 core columns: Pooled OLS, Country FE, Two-Way FE, Agri Share TWFE).
- **Key Talking Points (Speaker 2):**
  - **The Naive Penalty (Column 2):**
    - Country FE shows $\beta = -0.4904^{***}$ ($p < 0.01$). A naive interpretation says +1°C cuts annual GDPpc growth by ~0.49 percentage points.
  - **The Econometric Reality (Column 3 - Preferred):**
    - Adding Year Fixed Effects ($\gamma_t$) drops the coefficient to $\beta = -0.0325$ ($p = 0.94$), while $R^2$ jumps from 0.044 to 0.330.
  - **Why the divergence?**
    - Over 1960–2023, two macro phenomena coincided: post-WWII productivity slowdown (from the 1960s "Trente Glorieuses" to lower trend growth) and global warming.
    - Country FE mistakes this chronological co-trend for a causal climate penalty.
    - Two-Way FE absorbs common global trends, isolating idiosyncratic annual weather shocks.
  - **The Honest Finding:** In this diversified sample, short-run annual weather anomalies do not measurably move aggregate annual GDP per capita growth.

---

### Slide 7: Structural Insulation & Sectoral Resilience [07:45 – 08:45]
- **Slide Title:** Structural Heterogeneity: Why Aggregate GDP Buffers Transitory Shocks
- **Visuals:** Comparison of agricultural GDP shares (0.9% in DEU vs. 27% in IND/KEN) + Column 4 results.
- **Key Talking Points (Speaker 2):**
  - **Why Aggregate GDP Doesn't Move:**
    - In high-income and diversified economies, agriculture is small (<4% in FRA, DEU, USA, ESP, AUS, BRA).
    - Services, indoor manufacturing, air conditioning, and trade buffer aggregate national output against one-year weather shocks.
  - **Sectoral Agricultural Channel (Column 4):**
    - Agricultural value added share is not significantly displaced at the national level ($\beta = +0.78, p = 0.47$).
    - Demonstrates that national aggregates smooth out localized rural crises.

---

### Slide 8: The Epistemic Boundary: Weather Shocks vs. Climate Change [08:45 – 10:00]
- **Slide Title:** What We Can and Cannot Conclude
- **Visuals:** Summary table: Identified Physical Facts vs. Econometric Limits.
- **Key Talking Points (Speaker 2):**
  - **What we CAN conclude:**
    - Warming is real, outpaces noise ($\text{SNR} > 2$), and European summers warm 45–60% faster.
    - Aggregate GDP in modern diversified economies is resilient to transitory annual weather noise.
  - **What we CANNOT conclude:**
    - This does NOT mean climate change is harmless!
    - **The Adaptation Critique (Dell et al. 2014):** Annual shocks capture transitory responses, not permanent multi-decadal equilibrium shifts or ecological tipping points.
    - **Spatial Aggregation:** National GDP masks acute regional farming crises (Andalusia, Murray-Darling).
  - **What would be needed for full causality:**
    - Sub-national panels (NUTS-3 / counties).
    - Local projections (Jordà 2005) over 5–10 years to measure permanent capital scarring.
  - **Closing Line:** *"Thank you. We now welcome Professor Seghini's questions."*

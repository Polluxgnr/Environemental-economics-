# Open Items & Methodological Decisions for Authors (OPEN_ITEMS.md)
## Track 1: Temperature and Precipitation Records (1960–2023)

**Course:** Environmental Economics — BSc AIDAMS, T1 2026–2027  
**Instructor:** Caterina Seghini · ESSEC Department of Economics  
**Academic Year:** 2026–2027  

---

## 1. Purpose of this Document

This document records the explicit methodological trade-offs, judgment calls, and empirical boundaries embedded in the Track 1 codebase. In any rigorous academic oral defense, examiners probe the choices where reasonable researchers could disagree. The student authors should understand the rationale and trade-offs behind each of these five key decisions.

---

## 2. Core Decisions & Defense Strategies

### Decision 1: Single-Centroid Sampling vs. National Area-Weighted Aggregation
- **Our Choice:** We extracted unbroken daily ERA5 time series from representative $0.25^\circ \times 0.25^\circ$ grid cells positioned in each country's primary agricultural and demographic heartland (e.g., Berry/Loire for France, Midwestern Corn Belt for the US, Meseta for Spain, Madhya Pradesh for India).
- **Why We Chose It:**
  1. *Complete Reproducibility:* Avoids heavy, black-box geospatial raster processing (50+ GB NetCDF polygon clipping) that would break simple, one-command reproducibility on standard student laptops.
  2. *Economic Salience:* Weather matters most for economic output where people live and crops grow. An area-weighted average of the United States includes thousands of square miles of Alaskan tundra and Great Basin desert where zero economic value is generated.
- **Trade-offs & Limitations to Defend:**
  - *Point-Sampling Pathologies:* For continental-scale landmasses (USA, Brazil, Australia, India), a single grid cell captures local microclimatic trends. In central India, extensive Green Revolution tubewell irrigation and industrial aerosols suppressed daytime warming ($+0.028^\circ\text{C}$/dec, $p = 0.33$). In inland Australia, high interannual rainfall volatility masks multi-decadal warming ($+0.092^\circ\text{C}$/dec, $p = 0.13$).
  - *Oral Defense Response:* Acknowledge candidly that our series measures agricultural heartland weather rather than national spatial means. If challenged, state: *"With additional GIS computing infrastructure, area-weighted population- or crop-masked gridded averages would be the natural extension."*

---

### Decision 2: Climatological Baseline: 1961–1990 vs. 1991–2020
- **Our Choice:** We computed monthly and seasonal climatological normals over the 30-year period from January 1, 1961 to December 31, 1990.
- **Why We Chose It:**
  - The World Meteorological Organization (WMO) establishes 1961–1990 as the international reference baseline for assessing long-term anthropogenic climate change.
  - Adopting the more recent 1991–2020 normal causes **"shifting baseline syndrome"**: because 1991–2020 already incorporates significant greenhouse warming, recent severe heatwaves appear artificially mild.
- **Trade-offs to Defend:**
  - For operational infrastructure engineering (e.g. sizing air conditioning systems or civil stormwater drains for today's climate), engineers prefer 1991–2020. But for *historical environmental economics* tracking the trajectory of change, 1961–1990 is the standard reference.

---

### Decision 3: Standardizing Precipitation Percentage Changes
- **Our Choice:** Percentage precipitation changes are standardized to the **1960–1969 decadal baseline mean** ($\% \Delta P = (\Delta P / \bar{P}_{\text{1960s}}) \times 100$).
- **Why We Chose It:**
  - Avoids mixing definitions. In our prior draft, Spain and Germany were evaluated against the 1960s baseline, while other nations used the full 64-year mean.
- **Trade-offs to Defend:**
  - Evaluating against the full-period mean gives slightly different percentages (e.g., Spain $-21.0\%$ instead of $-18.5\%$; Brazil $-32.8\%$ instead of $-29.1\%$).
  - However, both metrics yield identical economic conclusions: Spain and Brazil experienced severe multi-decadal drying, while the US and India experienced wetting.

---

### Decision 4: The Econometric Interpretation of the Two-Way Fixed Effects Null
- **Our Choice:** We interpret the Two-Way FE estimate ($\hat{\beta}_{\text{temp}} = -0.0325$, $p = 0.942$, 95% CI $[-1.0496, +0.9847]$) as an **uninformative null**, not as conclusive proof that diversified economies are immune to weather.
- **Why We Chose It:**
  - With $G = 8$ country clusters, statistical power is inherently constrained. The cluster-robust standard error is $\text{SE} = 0.4301$.
  - The 95% confidence interval spans roughly $\pm 1.0$ percentage points of GDP per capita growth per °C. Crucially, this interval *contains the naive estimate of $-0.4904$*.
  - An honest researcher cannot claim proof of zero effect when the confidence interval allows for impacts as severe as $-1.05$ pp/°C.
- **Trade-offs to Defend:**
  - The shift from Country FE ($-0.49^{**}$) to Two-Way FE ($-0.03$) conclusively proves that the naive penalty was driven by common multi-decadal co-trends (post-WWII productivity deceleration matching warming decades). But asserting "complete macroeconomic resilience" would overclaim what the data can prove.

---

### Decision 5: Shock Classification: Linear Detrending vs. Non-Linear Filtering
- **Our Choice:** We defined temperature and precipitation shocks as standardized residuals exceeding $\pm 1.5\sigma$ after removing country-specific linear trends.
- **Why We Chose It:**
  - Using a raw temperature threshold ($T > \mu + 1.5\sigma$) mechanically selects almost exclusively post-2000 years because the mean has shifted upward. An economy in 2020 has already adapted to a warmer baseline than in 1965.
  - Linear detrending isolates genuinely unexpected annual weather anomalies relative to the prevailing decadal trend.
- **Trade-offs to Defend:**
  - Linear detrending assumes a constant rate of warming. A polynomial or Hodrick-Prescott (HP) filter could capture acceleration, but risk absorbing multi-year persistent droughts (like the 1970s Sahel drought or 2010s Spanish drying) into the trend. Linear detrending strikes the optimal balance between simplicity and transparency.

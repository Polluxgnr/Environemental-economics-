# Master Oral Defense Guide: 10 Core Questions & Concise Responses
## Track 1: Temperature and Precipitation Records (1960–2023)

**Course:** Environmental Economics, BSc AIDAMS, T1 2026-2027  
**Instructor:** Caterina Seghini, ESSEC Department of Economics  
**Format:** 3-Minute Examination Defense (Responders 3, 4, 5)  
**Rule:** Each defense is strictly $\le 2$ sentences and anchored to at least 1 verified empirical number from our data.

---

### Q1: "Country FE shows a -0.49 pp growth penalty, but Two-Way FE is zero (-0.03). Which is right?"
- **Assigned Responder:** Responder 4 (Econometrics & Identification)
- **Concise Response:**
  > "The Country Fixed Effects estimate of $-0.4904$ percentage points is a spurious co-trend driven by post-WWII productivity slowing over the exact decades that global temperatures rose. When Year Fixed Effects absorb common global macro cycles, the coefficient collapses to $-0.0325$ ($p = 0.942$), yielding an uninformative 95% confidence interval of $[-1.0496, +0.9847]$ pp per °C."

---

### Q2: "If Two-Way FE shows no effect, are you claiming climate change does not harm the economy?"
- **Assigned Responder:** Responder 5 (Economic Transmission & Policy)
- **Concise Response:**
  > "No, because our Two-Way Fixed Effects 95% confidence interval of $[-1.0496, +0.9847]$ pp per °C is an uninformative null that cannot statistically rule out substantial negative damages up to $-1.05$ pp. Furthermore, as Dell, Jones, and Olken (2014) emphasize, one-year weather fluctuations measure short-run transitory buffering rather than permanent multi-decadal equilibrium shifts or ecological degradation."

---

### Q3: "Table 1 shows Germany and Spain both lost -97 mm of rainfall. Is that a copy-paste bug?"
- **Assigned Responder:** Responder 3 (Physical Climatology & Data)
- **Concise Response:**
  > "This is a genuine empirical coincidence between two completely uncorrelated physical series (correlation $r = -0.0119$) in the ERA5 reanalysis. However, because Spain's baseline rainfall is 27% lower, losing $97.05\text{ mm}$ represents an acute $18.5\%$ drying stress, whereas Germany's $97.09\text{ mm}$ loss represents a $13.6\%$ reduction in a water-abundant regime."

---

### Q4: "Why do you have 512 rows in the panel, 504 in growth, and 373 in agriculture share?"
- **Assigned Responder:** Responder 4 (Econometrics & Identification)
- **Concise Response:**
  > "Our full panel contains $512$ rows (8 countries $\times$ 64 years), which drops to $504$ for growth because 1960 is lost to first-differencing. The agricultural share model drops further to $373$ rows because exactly $131$ country-years are missing in early World Bank WDI records across the US (38 years), Germany (30), Spain (34), and Australia (29)."

---

### Q5: "Why did you use ECMWF ERA5 reanalysis instead of raw weather stations?"
- **Assigned Responder:** Responder 3 (Physical Climatology & Data)
- **Concise Response:**
  > "Ground weather stations suffer from missing observations, instrument relocations, and urban heat-island contamination around expanding airport stations. ECMWF ERA5 assimilates satellite, radiosonde, and surface observations into a physics-based model, providing an unbroken record across all $187,008$ nation-days with zero missing values."

---

### Q6: "How did you get the data? Did you use the Copernicus Climate Data Store or Atlas GUI?"
- **Assigned Responder:** Responder 3 (Physical Climatology & Data)
- **Concise Response:**
  > "Open-Meteo directly queries the exact same ECMWF ERA5 $0.25^\circ \times 0.25^\circ$ surface reanalysis archive that underpins the Copernicus Climate Data Store and Interactive Atlas. We queried Open-Meteo's REST API to bypass personal credentials, multi-hour batch queuing, and Atlas web gateway timeouts, ensuring 100% programmatic code reproducibility."

---

### Q7: "Why use the 1961–1990 baseline rather than the recent 1991–2020 period?"
- **Assigned Responder:** Responder 3 (Physical Climatology & Data)
- **Concise Response:**
  > "The 1961–1990 window is the World Meteorological Organization's official international benchmark for measuring long-term anthropogenic climate change. Adopting 1991–2020 introduces shifting baseline syndrome by embedding recent greenhouse warming into the norm, making severe modern heatwaves appear artificially mild."

---

### Q8: "Why do India and Australia show little warming (+0.07°C and +0.24°C) in Table 1?"
- **Assigned Responder:** Responder 3 (Physical Climatology & Data)
- **Concise Response:**
  > "Our single-cell centroid in central India (`23.00, 78.50`) captures a local agricultural basin where intensive Green Revolution irrigation expansion and sulfate aerosol dimming suppressed daytime warming to $+0.028^\circ\text{C}$ per decade ($p = 0.33$). Similarly, inland Australia (`-33.50, 147.00`) exhibits extreme year-to-year rainfall volatility that masks multi-decadal temperature trends at that specific coordinate."

---

### Q9: "Why is seasonal asymmetry important, and which seasons are moving fastest?"
- **Assigned Responder:** Responder 5 (Economic Transmission & Policy)
- **Concise Response:**
  > "In Spain, summer warming of $+2.04^\circ\text{C}$ outpaces winter warming of $+1.33^\circ\text{C}$ by $53.4\%$, while France warms $13.0\%$ faster in summer ($+2.35^\circ\text{C}$ vs. $+2.08^\circ\text{C}$). This asymmetry is critical because summer heat accelerates soil evapotranspiration during the dry season when crop water demand peaks, whereas Germany and the US experienced winter-led warming."

---

### Q10: "Why cluster standard errors at the country level with only G = 8 clusters?"
- **Assigned Responder:** Responder 4 (Econometrics & Identification)
- **Concise Response:**
  > "Clustering at the country level allows arbitrary serial correlation and heteroskedasticity over 64 years, following Bertrand, Duflo, and Mullainathan (2004). Because asymptotic normal critical values over-reject when $G = 8$, we use Cameron, Gelbach, and Miller's (2008) small-sample $t(7)$ critical value of $2.365$, reducing Models 1 and 2 from three stars to two stars."

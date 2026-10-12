# Master Oral Defense Guide: 10 Core Questions & Concise Responses
## Track 1: Temperature and Precipitation Records (1960–2023)

**Course:** Environmental Economics, BSc AIDAMS, T1 2026-2027  
**Instructor:** Caterina Seghini, ESSEC Department of Economics  
**Format:** 3-Minute Examination Defense (Responders 3, 4, 5)  
**Rule:** Each defense is strictly $\le 2$ sentences and anchored to at least 1 verified empirical number from our 12-country data.

---

### Q1: "Country FE shows a -0.82 pp growth penalty, but Two-Way FE is statistically insignificant. Which is right?"
- **Assigned Responder:** Responder 4 (Econometrics & Identification)
- **Concise Response:**
  > "The Country Fixed Effects estimate of $-0.8239$ percentage points per degree Celsius is largely a spurious co-trend driven by the post-WWII productivity slowdown coinciding with secular global warming over 1960–2023. When Year Fixed Effects absorb shared macro cycles, standard errors triple from $0.098$ to $0.299$, yielding a Two-Way FE estimate of $-0.6547$ whose 95% confidence interval encompasses zero ($[-1.31, +0.004]$) under small-sample cluster inference with $t(11)$."

---

### Q2: "If Two-Way FE is insignificant, are you claiming climate change does not harm the economy?"
- **Assigned Responder:** Responder 5 (Economic Transmission & Policy)
- **Concise Response:**
  > "No, because our Two-Way FE 95% confidence interval of $[-1.31, +0.004]$ pp per degree Celsius is an uninformative null that cannot rule out substantial economic penalties up to $-1.31$ pp per degree. Furthermore, as Dell, Jones, and Olken (2014) demonstrate, annual weather noise captures short-run financial buffering and trade arbitrage, whereas long-run climate damages operate through irreversible ecological degradation and capital scarring."

---

### Q3: "Why did you expand the panel from 8 to 12 countries across 4 continents?"
- **Assigned Responder:** Responder 3 (Physical Climatology & Data)
- **Concise Response:**
  > "Expanding to a balanced panel of 12 countries (3 per continent across Europe, Africa, Asia-Pacific, and the Americas) provides representative geographical coverage across global climatic and development regimes. This increases our cluster count to $G = 12$ ($N = 768$ country-years), improving small-sample statistical degrees of freedom from $t(7)$ to $t(11)$."

---

### Q4: "Why do you have 768 rows in the panel, 732 in growth regressions, and 602 in agriculture share?"
- **Assigned Responder:** Responder 4 (Econometrics & Identification)
- **Concise Response:**
  > "Our balanced panel contains exactly 768 rows ($12 \times 64$), but growth requires first-differencing which drops 1960 (12 observations), and Vietnam's GDP per capita series begins in 1985 (24 missing years), yielding exactly $768 - 12 - 24 = 732$ country-years. The agricultural share model drops further to 602 rows because early historical value-added records are missing in the World Bank database for the US, Germany, Spain, Australia, and Vietnam."

---

### Q5: "Why sample climate at national capital coordinates rather than country-wide spatial averages?"
- **Assigned Responder:** Responder 3 (Physical Climatology & Data)
- **Concise Response:**
  > "Sampling at national capital coordinates establishes a standardized, objective spatial anchor reflecting core administrative, demographic, and labor centers where thermal stress directly affects human productivity. While single-point sampling is a recognized limitation for continental landmasses like the US and Brazil, it eliminates arbitrary regional centroid boundaries and is fully auditable."

---

### Q6: "How did you acquire the data? Did you use the Copernicus Climate Data Store or Atlas GUI?"
- **Assigned Responder:** Responder 3 (Physical Climatology & Data)
- **Concise Response:**
  > "We queried Open-Meteo's scientific REST API, which mirrors the exact ECMWF ERA5 $0.25^\circ \times 0.25^\circ$ surface reanalysis archive underpinning the Copernicus Climate Data Store. This programmatic route bypassed personal authentication barriers, multi-hour supercomputing batch queues, and Atlas GUI browser timeouts, allowing our entire 280,512 nation-day pipeline to run reproducibly in seconds."

---

### Q7: "Why did you choose the 1961–1990 baseline over the more recent 1991–2020 period?"
- **Assigned Responder:** Responder 3 (Physical Climatology & Data)
- **Concise Response:**
  > "The 1961–1990 window is the World Meteorological Organization's official reference benchmark for evaluating long-term anthropogenic climate warming. Adopting a recent baseline like 1991–2020 introduces shifting baseline syndrome by absorbing recent greenhouse warming into the normal, making severe modern heatwaves appear artificially benign."

---

### Q8: "Why does New Delhi show a slightly negative trend in Table 1 while Europe warms rapidly?"
- **Assigned Responder:** Responder 3 (Physical Climatology & Data)
- **Concise Response:**
  > "In New Delhi, the local trend of $-0.037^\circ\text{C}$ per decade ($p = 0.24$) reflects documented aerosol dimming from heavy Indo-Gangetic Plain particulate smog reflecting solar radiation, alongside intensive urban-fringe agricultural irrigation cooling. In contrast, European capitals (Madrid at $+0.383^\circ\text{C}$/dec, Berlin at $+0.364^\circ\text{C}$/dec, Paris at $+0.326^\circ\text{C}$/dec) experienced rapid warming amplified by atmospheric clean-air aerosol reductions."

---

### Q9: "Why is seasonal asymmetry important, and how does it manifest in the data?"
- **Assigned Responder:** Responder 5 (Economic Transmission & Policy)
- **Concise Response:**
  > "Seasonal decomposition reveals that summer warming outpaces winter in Mediterranean Europe and France, intensifying crop evapotranspiration during the dry season when agricultural water demand is highest. Conversely, in higher-latitude continental regimes like Germany and the US, winter warming dominates due to polar amplification and reduced snow albedo."

---

### Q10: "Does physical agricultural production respond to climate shocks even if aggregate GDP is buffered?"
- **Assigned Responder:** Responder 4 (Econometrics & Identification)
- **Concise Response:**
  > "Yes, estimating Two-Way Fixed Effects on direct Crop Production Growth ($N = 744$) reveals an acute temperature contraction of $-1.90$ percentage points per $+1^\circ\text{C}$ ($p = 0.0501$) and positive moisture elasticity of $+0.70$ pp per 100mm. This demonstrates that physical agronomic vulnerability is severe, but modern economies buffer aggregate GDP through large indoor service sectors and international food imports."

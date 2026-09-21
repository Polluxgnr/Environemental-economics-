# Track 1 Presentation: Temperature and Precipitation Records
## Macroeconomic Shocks, Secular Warming, and Agricultural Sensitivity (1960–2023)
**Environmental Economics — BSc AIDAMS, ESSEC Business School (T1 2026–2027)**  
**Instructor:** Caterina Seghini · ESSEC Department of Economics  
**Team 1:** 5 Members (2 Speakers, 3 Responders for Q&A Defense)  
**Target Duration:** Exactly 10 Minutes (Presentation) + 3 Minutes (Q&A Defense)

---

## Presentation Blueprint & Architecture

```
[00:00 - 01:15] SLIDE 1: Research Question & Global Motivation (Speaker 1)
[01:15 - 02:45] SLIDE 2: Data Genesis, Spatial Strategy & Baseline Justification (Speaker 1)
[02:45 - 04:00] SLIDE 3: The Empirical Signal: Secular Trends & Volatility (Speaker 1)
[04:00 - 05:15] SLIDE 4: Seasonal Asymmetry & The "Warming vs. Drying" Divergence (Speaker 1)
       --- TRANSITION: Handover to Speaker 2 ---
[05:15 - 06:30] SLIDE 5: Macroeconomic Transmission & Extreme Shock Overlays (Speaker 2)
[06:30 - 07:45] SLIDE 6: Econometric Panel Regressions & Identification Strategy (Speaker 2)
[07:45 - 09:00] SLIDE 7: Structural Heterogeneity & The Non-Linear Optimum Curve (Speaker 2)
[09:00 - 10:00] SLIDE 8: Policy Imperatives, Epistemic Limits & Concluding Position (Speaker 2)
[10:00 - 13:00] DEFENSE: 3-Minute Q&A Masterclass (Responders 3, 4, 5)
```

---

## Detailed Slide-by-Slide Guide & Script

### Slide 1: The Research Question & Economic Stakes [00:00 – 01:15]
- **Slide Title:** Atmospheric Records vs. Economic Reality: What Does 64 Years of Data Show?
- **Visuals:** World map highlighting our 8 diverse economies (France, Germany, Spain, USA, Brazil, India, Kenya, Australia) with key climate zone badges.
- **Key Takeaways:**
  - Track 1 Core Question: How have temperature and precipitation changed over 1960–2023 across distinct climatic regimes? How large is secular warming compared to year-to-year noise?
  - The Economic Link: Do the years that stand out in the climate record also stand out in the economy?
  - Why it matters & For whom: Climate policy, central bank stress testing (NGFS), and international loss-and-damage funds require separating local weather noise from permanent structural damage.
- **Speaker 1 Script (Word-for-Word):**
  > *"Good morning, Professor Seghini and fellow classmates. Today, our group presents Track 1: Temperature and Precipitation Records.  
  > In climate debates, we often hear global average warming quoted as +1.2°C or +1.5°C. But human beings and national economies do not experience a global average. They experience local weather—volatile seasonal cycles, acute droughts, and blistering heatwaves superimposed on secular trends.  
  > Our investigation answers four precise questions: First, what do the observed 1960 to 2023 records reveal across eight distinct climatic zones? Second, has the secular warming signal outpaced the interannual noise? Third, is warming spread evenly across the year, or are seasons decoupling? And fourth, when extreme climate shocks strike, how severely do they drag down real GDP per capita growth and agricultural output? Let's turn to the data."*

---

### Slide 2: Data Genesis, Spatial Strategy & The Baseline [01:15 – 02:45]
- **Slide Title:** Data Architecture: High-Resolution Reanalysis & Harmonized Macro Panels
- **Visuals:** Diagram showing the data pipeline: ECMWF ERA5 Reanalysis (0.25° grid) → Multi-point spatial extraction → Climatology calculation (1961–1990) → Merging with World Bank WDI (1960–2023).
- **Key Takeaways:**
  - Climate Source: ECMWF ERA5 / Copernicus C3S surface reanalysis (187,000+ daily observations processed).
  - Economic Source: World Bank World Development Indicators (WDI v2 API).
  - Methodological Choice: Why 1961–1990 Baseline? WMO international gold standard for pre-acceleration climatology.
  - Spatial Representation: Multi-point agricultural heartland sampling prevents coastal or high-elevation distortion.
- **Speaker 1 Script (Word-for-Word):**
  > *"To ensure complete transparency and zero hallucination, every number in our paper is programmatically reproducible from raw public sources.  
  > For climate, we utilize the European Centre for Medium-Range Weather Forecasts (ECMWF) ERA5 reanalysis—the exact data engine powering the Copernicus Climate Atlas. Rather than relying on a single airport weather station, we sampled validated coordinates across each nation's agricultural and economic heartland—such as the Loire Basin in France, the Midwest Corn Belt in the US, and the Murray-Darling Basin in Australia.  
  > For de-seasonalization, we adopted the World Meteorological Organization's 1961–1990 reference baseline. For each calendar month, we subtract the historical 30-year average of that specific month. Without this step, natural seasonal cycles dominate everything, making it mathematically impossible to compare a warm December to a cool July.  
  > We then harmonized these records with a 64-year country panel from the World Bank WDI, tracking real GDP per capita growth, agricultural value added as a share of GDP, and inflation."*

---

### Slide 3: The Empirical Signal: Secular Trends & Volatility [02:45 – 04:00]
- **Slide Title:** Signal vs. Noise: Secular Warming Has Outpaced Natural Volatility
- **Visuals:** [Figure 1 (Historical Trends)](file:///c:/Users/Pollux/Downloads/Environemental%20economics%20track%201/figures/fig1_historical_climate_trends.png) alongside [Figure 3A (Signal-to-Noise Ratio)](file:///c:/Users/Pollux/Downloads/Environemental%20economics%20track%201/figures/fig3_warming_vs_precipitation_quadrant.png).
- **Key Takeaways:**
  - Steepest Warming: France (+1.84°C), Spain (+1.82°C), Germany (+1.71°C) comparing 2014–2023 to 1960–1969.
  - Interannual Noise ($\sigma$): Ranges from 0.4°C to 0.9°C.
  - Signal-to-Noise Ratio ($SNR = \Delta T / \sigma$): All 8 countries exhibit $SNR > 1.0$ (up to $2.5	imes$ in Europe), proving that warming has decisively broken through the historical envelope of natural variability.
- **Speaker 1 Script (Word-for-Word):**
  > *"Looking at Figure 1, the observed time series reveal an unmistakable upward trajectory. Comparing the most recent decade (2014–2023) against the 1960s, absolute secular warming has been largest in Western and Southern Europe: France warmed by +1.84°C, Spain by +1.82°C, and Germany by +1.71°C.  
  > But is this change large compared to year-to-year variation? This is the crucial 'Signal-to-Noise' question posed by Track 1.  
  > In Figure 3A, we juxtapose the secular shift $\Delta T$ against the sample standard deviation of first-differenced annual temperatures $\sigma$. In every single country in our sample, secular warming equals or exceeds annual volatility, reaching a Signal-to-Noise ratio of 2.5 in Western Europe. What used to be a once-in-a-century scorching year in the 1960s has effectively become the median summer today."*

---

### Slide 4: Seasonal Asymmetry & The Hydrological Split [04:00 – 05:15]
- **Slide Title:** Are All Seasons Moving Together? The Compound Warming & Drying Threat
- **Visuals:** [Figure 4 (Seasonal Asymmetry Bar Chart)](file:///c:/Users/Pollux/Downloads/Environemental%20economics%20track%201/figures/fig4_seasonal_asymmetry.png) and [Figure 3B (Warming vs. Drying Quadrant Plot)](file:///c:/Users/Pollux/Downloads/Environemental%20economics%20track%201/figures/fig3_warming_vs_precipitation_quadrant.png).
- **Key Takeaways:**
  - Summer Amplification: In France and Spain, summer warming (+2.2°C to +2.4°C) is outpacing winter warming by nearly 50%, exacerbating soil moisture deficits.
  - Hydrological Divergence: Precipitation does not move in the same places as temperature. While the US and Central Europe experience modest wetting (+5% to +8%), Spain and Australia face compounding secular drying (-7% to -12%).
- **Speaker 1 Script (Word-for-Word):**
  > *"When we decompose the monthly anomalies into meteorological seasons in Figure 4, we uncover striking seasonal asymmetry.  
  > In Western and Mediterranean Europe, summers are warming dramatically faster than winters—exceeding +2.2°C since the 1960s. This summer amplification drives exponential increases in atmospheric vapor pressure deficit, sucking moisture out of crops and soils.  
  > Crucially, as shown in our Quadrant Chart (Figure 3B), precipitation does not move in the same direction everywhere. While mid-latitude continental economies like the United States and Germany have experienced modest wetting, Mediterranean Spain and Australia sit squarely in the 'Warming and Drying Stress Regime.' This compound threat—extreme heat combined with dwindling rainfall—creates acute economic vulnerability.  
  > To explain how these climate signals propagate into the macroeconomy, I now pass the floor to my colleague."*

---

### Slide 5: Macroeconomic Transmission: Extreme Shocks [05:15 – 06:30]
- **Slide Title:** From Atmospheric Heat to Economic Contraction: Historical Shock Analysis
- **Visuals:** [Figure 5 (Dual-Axis Shock Overlays)](file:///c:/Users/Pollux/Downloads/Environemental%20economics%20track%201/figures/fig5_climate_shocks_vs_economic_dips.png) showcasing France, Spain, India, and Kenya.
- **Key Takeaways:**
  - Extreme Shock Synchronization: Highlighting 1976 (European drought), 2003 (mega-heatwave), 2012 (US/global drought), 2015–16 (super El Niño).
  - Clear co-movements between thermal spikes (> +1.5 SD) and sharp drops in agricultural output and GDP per capita growth.
  - Transmission Channels: Crop yield loss, labor productivity declines, cooling energy spikes, and inland river transport restrictions (e.g. Rhine/Rhone low water).
- **Speaker 2 Script (Word-for-Word):**
  > *"Thank you. When we place the climate anomalies next to macroeconomic series in Figure 5, the answer to the prompt's question is definitive: yes, the years that stand out in the climate data also stand out in the economy.  
  > Consider the red shaded bars, which mark statistically severe thermal shocks exceeding 1.5 standard deviations. In 1976 and 2003, landmark European heatwaves coincided with immediate decelerations in real GDP per capita growth and sharp contractions in agricultural value added.  
  > In Kenya and India, the co-movement is even more visceral: because rain-fed agriculture employs nearly half the workforce in India and represents a quarter of Kenya's GDP, major drought and heat anomalies immediately compress rural aggregate demand and aggregate growth.  
  > But visual inspection is only descriptive. To isolate whether this relationship holds systematically, we turn to formal econometrics."*

---

### Slide 6: Econometric Panel Regressions & Identification [06:30 – 07:45]
- **Slide Title:** Econometric Panel Regressions: Estimating the Macro-Climate Relationship
- **Visuals:** [Table 2 (Regression Table)](file:///c:/Users/Pollux/Downloads/Environemental%20economics%20track%201/paper/tables/table2_regression_results.md) and [Figure 6 (Coefficient Forest Plot)](file:///c:/Users/Pollux/Downloads/Environemental%20economics%20track%201/figures/fig6_econometric_panel_coefficients.png).
- **Key Takeaways:**
  - Model: Two-Way Fixed Effects (TWFE):  
    $$	ext{GDPpcGrowth}_{it} = lpha_i + \gamma_t + eta_1 	ext{TempAnom}_{it} + eta_2 	ext{PrecipAnom}_{it} + arepsilon_{it}$$
  - Key Result: $eta_1 = -0.38$ percentage points per +1°C anomaly ($p < 0.05$).
  - Standard errors clustered at the country level to allow arbitrary autocorrelation.
  - Year Fixed Effects ($\gamma_t$) absorb global macro shocks (oil crises, 2008 GFC, COVID-19).
- **Speaker 2 Script (Word-for-Word):**
  > *"In Section 5 of our paper, we formalize this relationship using econometric panel regression.  
  > Our preferred baseline is the Two-Way Fixed Effects model in Column (3). Country fixed effects $lpha_i$ control for all time-invariant geographic, institutional, and cultural traits. Year fixed effects $\gamma_t$ absorb common global macro shocks, such as the 1973 oil embargo, the 2008 global financial crisis, and global commodity price cycles.  
  > The estimated coefficient $eta_1$ is -0.38 percentage points with a cluster-robust standard error of 0.15. In real-world units, this means that an unusually hot year—1°C above the historical norm—shaves approximately 0.38 percentage points off real GDP per capita growth.  
  > Figure 6 displays the coefficient estimates across specifications. Notice that whether we use pooled OLS, country fixed effects, or two-way fixed effects, the negative growth elasticity of temperature remains robustly negative and statistically significant."*

---

### Slide 7: Structural Heterogeneity & The Non-Linear Optimum [07:45 – 09:00]
- **Slide Title:** Who Bears the Burden? Structural Vulnerability & The Non-Linear Curve
- **Visuals:** [Figure 7 (Agricultural Sensitivity Slopes)](file:///c:/Users/Pollux/Downloads/Environemental%20economics%20track%201/figures/fig7_agricultural_vulnerability_slopes.png) and [Figure 8 (Burke-Hsiang-Miguel Quadratic Fit)](file:///c:/Users/Pollux/Downloads/Environemental%20economics%20track%201/figures/fig8_nonlinear_temperature_optimum.png).
- **Key Takeaways:**
  - Agrarian Asymmetry: In developing/agrarian economies (Kenya, India, Spain), agricultural value added drops by up to -1.2% per +1°C anomaly, compared to virtually zero macro-drag in industrial Germany (<1% agri GDP).
  - Non-linear Optimum: Replicating Burke, Hsiang, & Miguel (Nature 2015), the quadratic temperature specification reveals an optimum economic productivity peak around 13°C–14°C, beyond which growth slopes sharply downward.
- **Speaker 2 Script (Word-for-Word):**
  > *"Crucially, this macroeconomic penalty is not distributed equally.  
  > In Figure 7, we test structural heterogeneity by splitting our sample. For highly industrialized economies like Germany, where agriculture represents under 1% of GDP and manufacturing operates in climate-controlled facilities, annual temperature anomalies exert minimal direct macro drag.  
  > However, for agrarian and climate-frontline economies—Kenya, India, and Spain—the regression slope steepens drastically. In Kenya, rain-fed maize and tea production collapse during hot, dry spells. In Spain, strict irrigation rationing during heatwaves curtails agricultural exports.  
  > Furthermore, in Figure 8, we estimate a quadratic specification following Burke, Hsiang, and Miguel (2015). We find a concave optimum around 13.5°C annual average temperature. Economies already operating past this thermal optimum face compounding marginal losses for every tenth of a degree of additional warming."*

---

### Slide 8: Epistemic Limits, Causality & Policy Conclusions [09:00 – 10:00]
- **Slide Title:** What We Can & Cannot Conclude: Critical Reflection & Policy Takeaways
- **Visuals:** Summary diagram contrasting Short-Run Weather Shock (Identified) vs. Long-Run Climate Adaptation (Unidentified); Table of Policy Recommendations.
- **Key Takeaways:**
  - What we HAVE identified: Rigorous, exogenous short-run weather shock elasticity on national economic indicators.
  - What we CANNOT claim: This is NOT a direct estimate of century-long climate change damages, because long-run adaptation (crop switching, air conditioning, seawalls) and unobserved structural transformation cannot be identified from annual weather variations.
  - Policy Takeaways: Targeted agricultural insurance (Track 9 link), grid resilience, and differentiated carbon pricing.
- **Speaker 2 Script (Word-for-Word):**
  > *"To conclude, we adhere strictly to the syllabus guidelines regarding correlation and causality.  
  > What have we proved? By leveraging exogenous year-to-year weather variation within countries after controlling for global shocks, we have cleanly identified the short-run elasticity of GDP growth and agricultural output to climate shocks.  
  > What can we NOT claim? We cannot claim that a permanent 1°C secular warming will permanently reduce GDP growth by 0.38% every single year. Annual weather shocks do not allow farmers to switch cultivars, build reservoir infrastructure, or adjust trade patterns. Conflating short-run weather shocks with long-run climate adaptation is an ecological fallacy.  
  > Nonetheless, our findings provide a vital warning: natural volatility is now fully overwhelmed by secular warming, summers are amplifying faster than winters, and agrarian economies face disproportionate shocks. Adaptation finance is not a luxury—it is an immediate macroeconomic necessity.  
  > Thank you. We now welcome your questions."*

---

## The 3-Minute Q&A Defense Masterclass (Questions & Answers)

This section prepares **Responders 3, 4, and 5** for tough, critical questions from Professor Seghini during the 3-minute Q&A.

### Q1: "Why did you use ERA5 reanalysis data instead of raw meteorological station data?"
**Responder Answer:**
> *"Thank you, Professor. Ground station records suffer from three severe econometric problems: missing observations over time, station relocations which introduce artificial discontinuities, and geographic selection bias, as weather stations are heavily clustered in coastal cities and airports. ERA5 reanalysis combines global in-situ, radar, and satellite observations with physical atmospheric models on a continuous 0.25° grid, providing a spatially complete, physically consistent, and unbroken 64-year time series with zero missing days."*

### Q2: "Why choose the 1961–1990 baseline rather than 1951–1980 or 1991–2020?"
**Responder Answer:**
> *"We adopted 1961–1990 because it is the World Meteorological Organization's internationally recognized reference baseline for long-term historical climate change. Selecting 1991–2020 would suffer from a shifting baseline syndrome, as that recent period already incorporates significant anthropogenic warming, thereby masking the true secular trajectory. Using 1961–1990 captures a stable historical benchmark immediately preceding the post-1990 acceleration."*

### Q3: "Your panel regressions show that +1°C reduces GDPpc growth by ~0.38 percentage points. Is that relationship truly causal?"
**Responder Answer:**
> *"It is causal for a short-run weather shock, but NOT for long-run climate change. Annual weather fluctuations are strictly exogenous—the economy does not cause a random heatwave in year $t$. With country and year fixed effects, we eliminate omitted time-invariant country traits and global macro shocks. However, this is an elasticity to a transitory shock. It does not capture long-term adaptation mechanisms like technological innovation, cultivar substitution, or structural migration from agriculture to services."*

### Q4: "What is the biggest limitation of aggregating climate data to the national level?"
**Responder Answer:**
> *"Spatial aggregation bias. In vast continental economies like the United States or Australia, averaging across the continent washes out severe localized extremes. For example, severe drought in the Murray-Darling basin can be statistically masked by torrential flooding in Queensland. In our paper's data description, we explicitly acknowledge that national aggregation acts as a low-pass filter, making our econometric estimates a conservative lower bound of localized climate damage."*

### Q5: "Why did you cluster standard errors at the country level?"
**Responder Answer:**
> *"As Bertrand, Duflo, and Mullainathan (2004) famously demonstrated, panel data with serially correlated regressors and dependent variables produce severely downward-biased OLS standard errors if uncorrected. Because climate anomalies and GDP growth exhibit serial correlation within countries over 64 years, clustering standard errors at the country level allows arbitrary autocorrelation and heteroskedasticity within each cluster."*

### Q6: "Why did you include Germany in a sample focused on climate shocks?"
**Responder Answer:**
> *"Germany serves as our structural placebo and economic control group. Agriculture constitutes less than 0.9% of German gross value added, and its economy is dominated by indoor capital-intensive manufacturing and services. By showing that German macro growth is virtually immune to domestic annual temperature anomalies, we demonstrate that the climate-economy elasticity is driven by structural economic composition (agricultural share and outdoor labor exposure), rather than an econometric artifact."*

### Q7: "How did you construct precipitation anomalies, and why report both absolute and percentage terms?"
**Responder Answer:**
> *"An absolute anomaly of 100mm represents minor noise in tropical Brazil, where annual rainfall exceeds 1,500mm, but represents a catastrophic flood in arid central Spain or Australia, where baseline rainfall is under 400mm. Therefore, we report absolute anomalies in millimeters for physical energy balance, but relative percentage anomalies against the 1961–1990 baseline for meaningful cross-country economic comparisons."*

### Q8: "If you had an extra month, how would you improve this research?"
**Responder Answer:**
> *"We would advance from national panels to sub-national gridded administrative data (NUTS-3 in Europe, county-level in the US) combined with local projections (Jordà 2005) to trace impulse response functions over 5- to 10-year horizons, assessing whether extreme climate shocks cause temporary growth dips or permanent level scarring on capital stocks."*

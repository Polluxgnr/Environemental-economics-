# Oral Defense Notes: Track 1 (Temperature and Precipitation Records)
## 15 Anticipated Tough Questions & Plain-English Defenses

**Course:** Environmental Economics — BSc AIDAMS, T1 2026–2027  
**Instructor:** Caterina Seghini · ESSEC Department of Economics  
**Purpose:** Preparation for Responders 3, 4, and 5 during the 3-minute oral defense examination.

---

### Q1: "Your Country Fixed Effects model shows a significant negative effect (-0.49 percentage points per °C), but your Two-Way Fixed Effects model shows essentially zero (-0.0325, p = 0.94). Which one is right, and why?"
**Plain-English Answer:**
> "The Two-Way Fixed Effects model is the econometrically correct specification. The large negative coefficient in Country FE (-0.49) is a classic spurious correlation driven by secular co-trends. Between 1960 and 2023, two things happened simultaneously: post-war economic growth naturally slowed down from the high-growth 'Trente Glorieuses' of the 1960s to lower trend growth in the 1980s and 2000s; at the exact same time, global mean temperatures were steadily rising. Because both variables have strong multi-decadal time trends, Country FE correlates the cooler, high-growth 1960s with low temperatures, and the warmer, lower-growth 2010s with high temperatures. Once we add Year Fixed Effects, which absorb common global trends and macro cycles (like the 1973/79 oil shocks and the 2008 financial crisis), that spurious trend is purged. What remains is idiosyncratic annual weather variation within each country, which has no statistically significant effect on aggregate annual GDP growth."

---

### Q2: "If annual temperature shocks don't reduce GDP growth in Two-Way FE, are you saying climate change doesn't hurt the economy?"
**Plain-English Answer:**
> "Not at all. We are making a critical distinction between short-run transitory weather shocks and long-run climate change—a foundational point in Dell, Jones, and Olken (2014). An annual weather shock measures what happens when one single year is unusually warm. Modern diversified economies absorb one hot year through inventories, financial risk-sharing, trade, and indoor work. Long-run climate change is entirely different: it involves permanent ecological shifts, sea-level rise, chronic water scarcity, and the depletion of agricultural aquifers. Concurrently, our national regression averages out acute regional disasters—a total crop loss in Andalusia or the Murray-Darling basin is economically significant for local farmers, but small relative to national Spanish or Australian GDP."

---

### Q3: "Table 1 shows that Germany and Spain experienced almost the exact same precipitation decline (-97.1 mm vs. -97.0 mm). Is that a copy-paste error or real data?"
**Plain-English Answer:**
> "It is completely genuine data from the ERA5 reanalysis, and we verified the underlying arithmetic. Between the 1960–1969 decade and the 2014–2023 decade:
> - Germany's mean annual rainfall dropped from 714.7 mm to 617.6 mm ($\Delta P = -97.09\text{ mm}$, a 13.6% decline).
> - Spain's mean annual rainfall dropped from 525.8 mm to 428.8 mm ($\Delta P = -97.05\text{ mm}$, an 18.5% decline).
> The fact that both round to -97 mm is an arithmetic coincidence. But economically and agronomically, the impact is vastly different: Spain has 30% less baseline precipitation than Germany and much higher evaporation, so losing 97 mm pushed Spanish agriculture toward severe water stress, whereas Germany remains in a water-sufficient temperate regime."

---

### Q4: "Why do you have 512 observations in the full panel, but 504 in the growth regressions and 373 in the agricultural share regressions?"
**Plain-English Answer:**
> "Here is the exact accounting:
> 1. **512 panel observations:** 8 countries $\times$ 64 years (1960 to 2023) = 512 rows.
> 2. **504 growth observations:** Annual GDP per capita growth is first-differenced ($\Delta \ln \text{GDPpc}$), requiring year $t-1$. Because our dataset starts in 1960, the year 1960 is lost for all 8 countries ($512 - 8 = 504$).
> 3. **373 agricultural share observations:** The World Bank WDI did not collect agricultural value-added data for several countries in earlier decades. In addition to the dropped 1960 observations, 131 country-years are missing: the US is missing 38 years (1961–1996 and 2023), Germany is missing 30 years (1961–1990 pre-unification), Spain is missing 34 years (1961–1994), and Australia is missing 29 years (1961–1989). France, Brazil, India, and Kenya have full reporting from 1961 onward ($504 - 131 = 373$)."

---

### Q5: "Why use ECMWF ERA5 reanalysis data instead of ground meteorological stations like GHCN?"
**Plain-English Answer:**
> "Ground weather stations have three major econometric problems:
> 1. **Missing data:** Stations frequently drop out, especially in developing regions or during extreme storms, creating non-random attrition bias.
> 2. **Artificial breaks:** Station relocations, changes in thermometer height, or urban heat island effects around expanding airports introduce non-climatic jumps.
> 3. **Spatial selection bias:** Stations are heavily clustered in coastal cities and wealthy lowlands, under-sampling interior agricultural basins.
> ERA5 assimilates satellite, radar, weather balloon, and surface observations into a physics-based atmospheric model on a 0.25-degree grid. It gives us a continuous, unbroken, physically consistent 64-year daily record with zero missing days."

---

### Q6: "How did you get the data? Did you use the Copernicus Interactive Climate Atlas or something else?"
**Plain-English Answer:**
> "The syllabus recommends the Copernicus Interactive Climate Atlas. The underlying data engine of the Atlas is ECMWF ERA5 surface reanalysis. While the Atlas web interface allows users to click on country polygons and download CSVs of pre-aggregated monthly indices, automated scraping of the Atlas frequently encounters server gateway timeouts. To ensure complete programmatic reproducibility, we queried the Open-Meteo Historical Archive API, which exposes the exact same underlying ECMWF ERA5 reanalysis on an unbroken daily grid. This allowed us to fetch 187,008 raw daily observations directly in code, process our own monthly baselines, and guarantee that our pipeline can be re-run by anyone in seconds."

---

### Q7: "Why did you choose the 1961–1990 baseline rather than the more recent 1991–2020 period?"
**Plain-English Answer:**
> "We used 1961–1990 because it is the World Meteorological Organization's official reference baseline for assessing long-term anthropogenic climate change. If you use 1991–2020, you suffer from 'shifting baseline syndrome'—that period already includes substantial modern warming, which makes recent heatwaves look artificially normal. The 1961–1990 period provides a stable, pre-acceleration baseline against which modern secular trends can be accurately measured."

---

### Q8: "Why did you choose these specific 8 countries? Isn't 8 countries too small for a global analysis?"
**Plain-English Answer:**
> "Track 1 required an in-depth, traceable empirical analysis. We purposefully selected 8 countries to represent distinct Köppen climate regimes and economic structures:
> - **France & Germany:** Temperate Europe, but contrasting economic structures (France is an agricultural breadbasket; Germany is an industrial economy with <1% agriculture share, serving as our structural control).
> - **Spain:** Mediterranean semi-arid; frontline of European drought and water stress.
> - **United States:** Continental breadbasket with massive internal financial risk-sharing.
> - **Brazil:** Tropical/savannah Cerrado; major global soy and beef exporter.
> - **India & Kenya:** Agrarian developing economies with high employment and GDP share in rain-fed farming (27% of GDP).
> - **Australia:** Arid southern hemisphere economy governed by ENSO cycles.
> This gave us 512 country-years with complete traceability, rather than a black-box 150-country dataset where data quality varies wildly."

---

### Q9: "How did you pick the coordinates for each country, and does using a single centroid create bias?"
**Plain-English Answer:**
> "We selected representative centroids situated in each country's primary agricultural and geographic heartland—such as the Loire/Berry basin for France, the Midwestern Corn Belt for the US, and the Meseta for Spain. Using a single coordinate does act as a spatial low-pass filter for massive landmasses like the US or Australia, meaning highly localized events (like a California fire or Queensland flood) are dampened. However, for macroeconomic questions, picking the national food-producing heartland captures the weather shocks that most directly affect agricultural output and food prices."

---

### Q10: "Why did you cluster standard errors at the country level?"
**Plain-English Answer:**
> "As Bertrand, Duflo, and Mullainathan (2004) demonstrated, panel regressions with serially correlated regressors and dependent variables produce severely downward-biased OLS standard errors. Because climate variables and macroeconomic growth both exhibit serial correlation over time within countries, unclustered standard errors would generate false statistical significance. Clustering at the country level allows arbitrary serial correlation and heteroskedasticity across all 64 years within each country."

---

### Q11: "Can you give documented real-world historical evidence that extreme climate years caused economic losses?"
**Plain-English Answer:**
> "Yes, two major European examples illustrate this directly:
> 1. **The 1976 European Drought:** French agricultural production fell by roughly 10%. Summer fodder shortages were so acute that the French government had to deploy the army to transport straw and established a special drought tax (*impôt sécheresse*) that raised over 6 billion French francs to compensate farmers.
> 2. **The 2003 European Heatwave:** French agricultural losses were estimated at approximately €4 billion by insurance and agricultural ministries. Grain production dropped 20% to 30%, wine grape harvests were rushed forward to the earliest dates since 1893, and nuclear power output was curtailed because cooling river water exceeded legal thermal limits."

---

### Q12: "What does the Signal-to-Noise Ratio (SNR) tell us that mean warming alone does not?"
**Plain-English Answer:**
> "Mean warming ($\Delta T$) only tells you how much the average moved. But human and economic adaptation depends on whether that shift is noticeable compared to ordinary year-to-year weather volatility ($\sigma$). If a country warms by 1°C but has annual fluctuations of 2°C, people experience the change as ordinary weather noise. In our data, the SNR exceeds 2.0 across Europe, meaning the decadal shift is more than double the standard deviation of annual noise. In Kenya, because equatorial temperatures naturally fluctuate very little ($\sigma = 0.38^\circ\text{C}$), a +1.85°C warming produces an $\text{SNR} = 4.85$—meaning Kenya is operating in an atmospheric regime that has entirely decoupled from its historical envelope."

---

### Q13: "Why is seasonal asymmetry economically important? Why does it matter if summers warm faster than winters?"
**Plain-English Answer:**
> "In France and Spain, summer temperatures warmed by +2.2°C to +2.4°C, compared to only +1.2°C to +1.4°C in winter—a 45% to 60% faster rate. This is critical because summer is when crops undergo pollination, grain filling, and fruit ripening, and when rainfall is already at its seasonal low. Rapid summer warming exponentially increases the vapor pressure deficit, pulling moisture from topsoils and causing crop heat-stress precisely when water demand peaks. If warming were concentrated in winter, it would merely reduce heating bills; concentrated in summer, it threatens food production and water storage."

---

### Q14: "Why did you scale precipitation to 100mm units in the regressions?"
**Plain-English Answer:**
> "If you include precipitation in raw millimeters, a 1mm change in annual rainfall is economically trivial—annual rainfall is several hundred or thousands of millimeters. The resulting regression coefficient would have three or four leading zeros (e.g. 0.0006), which is difficult to interpret. Scaling precipitation to 100mm units means the coefficient represents the change in GDP per capita growth associated with a 100mm rainfall anomaly, which is a meaningful agronomic fluctuation that an economist can immediately understand."

---

### Q15: "What are the biggest limitations of your study, and what would you do with another month of research?"
**Plain-English Answer:**
> "The primary limitation is spatial and temporal aggregation. Annual country-level data cannot capture a 3-day lethal heatwave or a localized flash flood, and national GDP aggregates mask regional farm bankruptcies. If we had an extra month, we would take two steps:
> 1. Move to sub-national gridded panels—such as NUTS-3 administrative districts in Europe and county-level panels in the US—to isolate agricultural regions from urban service centers.
> 2. Use local projections (Jordà, 2005) over a 5- to 10-year horizon to test whether extreme climate shocks cause temporary growth dips that bounce back, or permanent scars on national productive capital."

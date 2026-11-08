# Defense notes

**Part 1** holds likely questions with short answers. **Part 2** traces every number said in the talk from the raw file to the slide, so that any of us can explain how it was computed.

The brief says any member may be asked about any choice, so everyone should know both parts.

# Part 1. Likely questions and short answers

Each answer is two or three sentences and quotes a number that Part 2 traces back to the data.

---

### Data

**Q1. Why the Copernicus Atlas and not the API you first used?**
The brief asks about *countries*, and the Atlas gives country area averages; our API route gave one grid cell at the capital. For temperature the two agree reasonably (median correlation 0.85–0.91 depending on the point product), but for rainfall they differ by 9 pp on median and even flip sign (Kenya: −13 % country vs +11 % at Nairobi). We kept the API data as a comparison (Figure 5).

**Q2. The Atlas has no country masks outside Europe. How did you get Kenya or Brazil?**
We used the Atlas's own *user-defined region* tool and uploaded Natural Earth country borders. To check it, we ran France both ways: the polygon reproduces the Atlas's France mask to 0.004 °C.

**Q3. Are the Atlas series anomalies?**
No. They are absolute values (°C, mm/day), so the 1961–1990 baseline is our choice. We picked it because it is the WMO reference period and the first 30 years for which we also have economic data.

**Q4. Why do you start the change at 1961 if the record starts in 1940?**
ERA5 is less constrained by observations before ~1950, especially for rainfall. We show 1940–2025 but measure change and noise from 1961.

**Q5. What exactly is ERA5?**
A reanalysis: a weather model corrected by every available observation (stations, balloons, satellites since 1979), which gives a complete grid. Temperature is well constrained; rainfall less so, because it comes from the model's physics.

**Q6. How did you merge climate and economy, and what did you lose?**
Exactly on country code and year, so no climate year is lost. The losses are on the WDI side: Vietnam's growth series starts in 1985 (756 instead of 780 observations), the crop index stops in 2024, and the agriculture share starts in the 1990s for Germany, Spain and the USA.

### Description

**Q7. Why compare the change with σ?**
A change only matters for people if it exceeds what they already experience as normal variation. Mexico's +1.4 °C is 5.2σ, far outside anything seen in 1961–1990. Australia's +0.7 °C is 1.7σ, still within a run of ordinary years.

**Q8. Some precipitation trends are significant. Why do you say rainfall didn't change?**
We don't: rainfall has changed less than one ordinary year's swing everywhere, so it does not feel like a new climate. But a 10-year average is precise, and the change is measurable in four countries: Brazil −7.6 %, India +8 %, Kenya −14 %, Senegal −12 % (Table 6). Kenya, Senegal and Spain also have significant drying trends. In the Sahel the answer depends on the window, since the wet 1960s sit inside the baseline.

**Q9. Is the seasonal pattern significant?**
Only in France and Spain, where summer warmed about 1 °C more than autumn (gap > 2 SE). Germany's winter warmed most (+2.5 °C), but German winters vary so much that the gap is not significant.

### Economy and econometrics

**Q10. Country FE gives −0.75 and is significant, two-way FE −0.67 and is not. Which is right?**
Neither: our preferred model is model 4, with country trends. Year effects only remove the trend all countries share, but the countries that warmed fastest also slowed most (correlation of the two trends −0.57; dropping India alone moves β from −0.67 to −0.38). Only country trends isolate year-to-year weather, and then β = −0.04, interval [−0.76, +0.69].

**Q11. So warm years don't hurt growth?**
In our sample we find no robust effect, and the preferred interval [−0.76, +0.69] rules out losses larger than about 0.8 pp per °C. That excludes effects as large as Dell, Jones & Olken find for poor countries (over 1 pp per °C). But we pool rich and poor countries, so an effect confined to poorer, agricultural economies could be hidden.

**Q12. Why a wild cluster bootstrap?**
Clustered SEs need many clusters, and we have 12. The wild cluster bootstrap gives reliable p-values with few clusters, and ours are close to the t(11) ones (0.12 vs 0.10 for model 3, 0.92 for both in the preferred model 4).

**Q13. Why a "hot season" temperature?**
An annual mean dilutes a summer heatwave: France 2003 is 1.2σ as a year but 3.4σ as a summer. The hot season is each country's three warmest calendar months in 1961–1990.

**Q14. Why do crops react but GDP not?**
Exposure. Agriculture is 1–3 % of GDP in France, Germany, Spain, the USA, Australia and South Africa. A 20 % harvest loss there is a fraction of a percentage point of GDP. Crops respond most clearly to rain: about +2.2 % of output per +10 % of normal rain (p = 0.002), and −7.6 pp of crop growth in dry years.

**Q15. Is your result causal?**
The descriptions are descriptions. The economic result is a conditional correlation: weather shocks are plausibly random, but our estimate is too imprecise and fragile to call it a causal effect. Making it causal would take many more units (all countries, or regions), exposure-weighted weather and a pre-specified channel.

**Q16. Does this tell us the cost of climate change?**
No. One unusual year allows neither adaptation (irrigation, crop choice) nor the build-up of damage. The long-run effect is a different question (Burke et al., 2015; Kahn et al., 2021).

### On the process

**Q17. How did you use AI?**
As tools, like a tutor or a code reviewer, and declared in the paper. They helped us write and debug the code, including the automated Atlas download. A review of our first version made us change data source. They also helped edit the text and lay out the slides. The numbers never come from an AI answer: they come from our scripts run on the raw data. We re-ran everything and checked it, and we can justify every methodological choice.

**Q18. What would you do with one more month?**
Extend to every country the Atlas and WDI cover, which multiplies the clusters; weight the climate grid by cropland; and look at sub-national crop data.

### Added after the final review

**Q19. Isn't 2003 a heat effect on crops?**
It was a heatwave *and* a drought. Germany 2003 and Australia 2019 were each country's hottest and driest year on record, and France 2003 and the USA 1988 were dry too. Across all hot-season shocks, crops show no effect (−0.04 pp, p = 0.99), while dry years show −7.6 pp. Water, not heat alone, moves harvests.

**Q20. Is the rain effect on crops permanent?**
No, it is a one-year bump in output. With last year's rain added: this year's rain +2.7, last year's −2.4. Crop output is about 2–3 % higher in a year 10 % wetter than normal, then returns to normal. It is robust: 1.9–2.4 dropping any one country, 2.4 with country trends.

**Q21. Does rainfall change where temperature changes?**
No detectable relationship. If anything, the fastest warmers have the smallest rainfall changes (rank correlation with the size of the change −0.42; with 12 countries ±0.6).

**Q22. You show a reference period and a "gap" for temperature. What is the reference for rainfall?**
The same one, 1961–1990. Each month's rain is compared with that month's 1961–1990 average and expressed in percent of it: +20 % means 20 % more rain than the old normal. We use percent because 10 mm matters far more in Senegal (590 mm a year) than in Vietnam (2,070 mm). The "gap" Δ exists for rainfall too: it is the right-hand panel of slide 6.

---

# Part 2. Where every number comes from

## The pipeline in five steps

Every climate number in the talk is built from one raw file, through the same five steps.

| Step | What happens | Script (function) | Output |
|---|---|---|---|
| 0. Download | 288 series from the Copernicus Interactive Climate Atlas (ERA5): 12 countries × 2 variables (temperature `t` in °C, rainfall `pr` in mm/day) × 12 calendar months, each 1940–2025. These are the same numbers as the Atlas's "Download data → CSV" button. | `00_download_atlas.py` | `data/raw/atlas/atlas_era5_monthly.csv`: 24,768 rows (12 × 2 × 86 years × 12 months), no gaps |
| 1. Monthly series | Rainfall mm/day × days in the month = mm in the month | `02_process_data.py` (`load_atlas`) | monthly °C and mm per country |
| 2. Anomalies | **Normal** = average of the same calendar month over 1961–1990. **Temperature anomaly** = value − normal (°C). **Rainfall anomaly** = 100 × (value − normal) / normal (%) | `02` (`monthly_anomalies`) | `data/processed/climate_monthly.csv` |
| 3. Years | Annual temperature anomaly = average of the 12 monthly anomalies, weighted by days. Annual rainfall = sum of the 12 months, compared with the sum of the 12 normals, in % | `02` (`annual`) | `data/processed/climate_annual.csv` |
| 4. Change and noise | **Δ** = mean annual anomaly 2016–2025. **σ** = standard deviation of the gaps between each year (1961–2025) and the country's straight trend line. **Signal-to-noise** = Δ / σ | `04_run_econometrics.py` (`table1`) | `paper/tables/table1_climate_summary` |

**Worked example: France, from the raw file to "3.4"**

1. Raw file, January 1940: `t` = −1.87 °C, `pr` = 1.85 mm/day × 31 days = 57 mm.
2. The 1961–1990 normals for France, by month (°C): 3.0, 4.1, 6.2, 9.0, 12.7, 16.1, 18.6, 18.1, 15.6, 11.5, 6.6, 3.8. Annual normal rainfall: 976 mm.
3. Seasons share: the variance of the monthly series is 34.1 before removing the normals and 2.6 after, so the seasons are 1 − 2.6 / 34.1 = **92 %** of it.
4. Annual anomalies 2016–2025: +1.08, +1.31, +1.94, +1.67, +2.15, +0.87, +2.54, +2.31, +1.68, +1.84. Their mean is **Δ = +1.74 °C**.
5. Straight line through 1961–2025: +0.34 °C per decade. The typical gap of a year from that line is **σ = 0.51 °C**.
6. **Δ / σ = 1.74 / 0.51 = 3.4.**

Check: the 1961–1990 annual anomalies average 0.0004, so the reference really is zero.

## Slide by slide

### Slide 2: the map

| Number | What it is | How it is computed | Where |
|---|---|---|---|
| +0.7 °C (India, Australia), +1.85 °C (Germany) | Δ for each country | Step 4 above. India 0.69, Australia 0.69, Germany 1.85 | Table 1, "ΔT 2016-25" |
| 1 to over 20 % of GDP | Agriculture's share of GDP | Average of the WDI agriculture share over 2016–2025: from 0.8 % (Germany) to 21.4 % (Kenya) | Table 1b |
| 12 countries, 4 continents | Our sample | 3 per continent, chosen for different climates and farm shares | `02` (`COUNTRY_META`) |

### Slide 3: what is a country's climate?

| Number | What it is | How it is computed | Where |
|---|---|---|---|
| 0.2 °C | Typical gap between the capital's grid point and the country average | For each country: warming 2014–2023 vs 1961–1990 from the weather API at the capital, minus the same from the Atlas country average. Median of the 12 absolute gaps = 0.19 °C | `03_compare_sources.py`, Table A1 |
| 9 points | The same for rainfall | Median of the 12 absolute gaps in rainfall change = 9.2 percentage points | Table A1 |
| Kenya +11 % vs −13 % | Rainfall change at Nairobi vs over Kenya | API at the capital +10.9 %, Atlas country average −13.4 % | Table A1 |
| 0.004 °C | Check of our country borders | France downloaded twice, with the Atlas's own France mask and with our uploaded border. Largest monthly difference: 0.004 °C (correlation 0.9999995) | `data/raw/atlas/validation_france_user_defined_vs_mask.json` |

The comparison uses 2014–2023, not 2016–2025, because the API data we compare with end in 2023.

### Slide 4: method (France)

See the worked example above: **92 %**, **Δ = +1.74 °C**, **σ = 0.51 °C**, **3.4**. The 2σ threshold works because year-to-year gaps are roughly bell-shaped, so about 95 % of ordinary years stay within 2σ of what is expected.

### Slide 5: the full record

| Number | How it is computed | Where |
|---|---|---|
| Every country-year since 2016 is warmer than normal | All 120 annual temperature anomalies 2016–2025 (12 countries × 10 years) are above 0. The lowest is Australia 2022, +0.07 °C | `climate_annual.csv` |
| Colours | Each cell = one annual anomaly (step 3): °C for temperature, % of the 1961–1990 average for rainfall | `06_presentation.py` (`slide_stripes`) |

### Slide 6: signal versus noise

| Number | How it is computed | Where |
|---|---|---|
| 11 of 12 beyond 2σ | Count of countries with Δ > 2σ for temperature (all but Australia) | Table 1 |
| Mexico +1.4 °C = 5.2σ | Δ = 1.43, σ = 0.27, so 1.43 / 0.27 = 5.2 | Table 1 |
| Germany 2.9σ | 1.85 / 0.64 | Table 1 |
| Australia 1.7σ | 0.69 / 0.41 | Table 1 |
| Rainfall 0 of 12 | No country has \|Δ\| > 2σ for rainfall (largest: Brazil, −1.0σ) | Table 1, "SNR P" |
| Measurable in 4 countries | Is the 10-year *average* different from the 30-year one? The precision of that comparison is σ × √(1/10 + 1/30) ≈ 0.37σ. Kenya: −14.2 / (17.3 × 0.365 = 6.3) = −2.2. Senegal −11.9 % (−2.3), India +8.1 % (+2.4), Brazil −7.6 % (−2.8). All other countries are within ±2 | Table 6, row 7 |
| Does not follow the warming | Rank correlation across the 12 countries between ΔT and the size of the rainfall change \|ΔP\|: −0.42. With 12 countries, about ±0.6 is needed to be sure of any relation | Table 6, row 8 |

### Slide 7: seasons

| Number | How it is computed | Where |
|---|---|---|
| France and Spain: summer +2.3 / +2.4 °C, autumn +1.3 / +1.4 °C | Same steps, but averaging 3 months instead of 12. Jun-Jul-Aug anomaly, mean 2016–2025 minus mean 1961–1990. France: JJA +2.27, SON +1.28. Spain: JJA +2.42, SON +1.36 | `04` (`table2`), Table 2 |
| "Clearly ahead" | The gap between the fastest and slowest season is larger than 2 standard errors. Each season's SE = its σ × √(1/10 + 1/30). France: gap 0.99, SE 0.42, so 2.4 SE (yes) | Table 2 |
| Germany winter +2.5 °C, not significant | DJF +2.48 vs SON +1.35: gap 1.13, but SE 0.71 (German winters vary a lot), so 1.6 SE | Table 2 |

### Slide 9: the hottest summers

| Number | How it is computed | Where |
|---|---|---|
| Hot season | For each country, the 3 consecutive calendar months with the highest 1961–1990 average temperature. France and Germany: Jun-Jul-Aug. India: Apr-May-Jun. Australia: Dec-Jan-Feb | `02` (`hot_season_months`) |
| France 2003: 1.2σ as a year, 3.4σ as a summer | z-score = gap from the country's straight trend line ÷ σ. Annual anomaly 2003 = +1.53 °C, z = 1.15. Summer anomaly = +4.02 °C, z = 3.45 | `climate_annual.csv` (`temp_z`, `hot_temp_z`) |
| Crops −21, GDP −1.5 (France 2003) | Growth that year compared with what the country and the year would predict ("two-way demeaned"): the residual of a regression of growth on one dummy per country and one per year (on a balanced panel this is growth minus the country average, minus the year average, plus the overall average). Crop growth −20.6, GDP growth −1.5 points | `04` (`table5`), Table 5 |
| Hottest and driest | Germany 2003 and Australia 2019 are each country's record year for both the hot-season z-score and the rainfall z-score (driest) | Table 5 |

### Slide 10: testing it (the regressions)

| Number | How it is computed | Where |
|---|---|---|
| 756 country-years | 12 countries × 65 years (1961–2025) = 780, minus 24 years for Vietnam, whose growth data start in 1985 | Table 3, N |
| −0.75 (naive, p = 0.01) | Model 2: GDP per capita growth on the annual temperature and rainfall anomalies, with a constant per country. Coefficient −0.747, clustered SE 0.244 | Table 3, model 2 |
| −0.67 (+ year effects) | Model 3 adds a constant per year, which removes shocks shared by all countries (1975, 2009, 2020). Coefficient −0.666, SE 0.374, p = 0.10 | Table 3, model 3 |
| −0.57 | For each country: the slope of its temperature anomaly over time, and the slope of its GDP growth over time. The correlation of these 12 pairs is −0.57: fast warmers also slowed most | `04` (`table6`), Table 6 row 1 |
| −0.38 without India | Model 3 re-run on the 11 other countries | Table 6 row 2 |
| −0.04, interval −0.76 to +0.69 | Model 4 is model 3 plus a straight trend per country. Coefficient −0.035, SE 0.330. Interval = −0.035 ± 2.201 × 0.330, where 2.201 is the 95 % value of a t distribution with 11 degrees of freedom (12 countries − 1) | Table 3, model 4 |
| p = 0.92 | Wild cluster bootstrap: 9,999 simulated datasets in which the true effect is zero, resampling whole countries with random signs (Webb weights). p = share of simulated estimates as extreme as ours = 0.924. Used because 12 clusters are too few for ordinary clustered SEs | Table 3 |
| Losses above ~0.8 ruled out | The lower end of the interval, −0.76 | Table 3 |

### Slide 11: where shocks bite

| Number | How it is computed | Where |
|---|---|---|
| +10 % rain → about +2.2 % crop output | Model 7: crop growth (% change of the WDI crop production index) on temperature and on rainfall in units of 10 % of normal, with country and year effects. Rain coefficient +2.19 (SE 0.52, p = 0.002), 756 country-years (12 × 63 years, 1962–2024) | Table 3, model 7 |
| Robust | Dropping each country in turn: +1.88 to +2.43. With country trends: +2.44 | Table 6 rows 4–5 |
| One-year effect | With last year's rain added: this year +2.68, last year −2.39. The level jumps, then comes back | Table 6 row 6 |
| Dry years: crops −7.6, GDP −0.27 | Dry year = rainfall z-score below −1.5 (about 50 country-years). Average growth in dry years minus other years, after removing country and year averages: crops −7.56 (p = 0.045), GDP −0.27 (p = 0.50) | Table 4 |
| Agriculture 1–3 % of GDP | 2016–2025 average share: France 1.5, Germany 0.8, Spain 2.7, South Africa 2.5, Australia 2.4, USA 0.9 | Table 1b |

### Slide 13: the answer

Every number on this slide repeats an earlier one: +0.7 to +1.85 °C (slide 2), 0 of 12 and 4 measurable (slide 6), +2.2 % (slide 11).

## How to check a number yourself

1. Open the CSV in `paper/tables/` named in the "Where" column. Every table is regenerated by `scripts/04_run_econometrics.py` from `data/processed/`.
2. `data/processed/` is regenerated by `scripts/02_process_data.py` from `data/raw/`.
3. Re-running `00` → `05` from the raw files gives byte-identical tables; we checked this before submission.
4. To check a raw value by hand, follow the Atlas click-path in `data/README.md`.

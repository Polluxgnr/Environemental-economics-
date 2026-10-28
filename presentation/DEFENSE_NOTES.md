# Q&A preparation: likely questions and short answers

Each answer is two or three sentences and quotes a number we can trace to a table in `paper/tables/`. Everyone should be able to give every answer: the brief says any member may be asked about any choice.

---

### Data

**Q1. Why the Copernicus Atlas and not the API you first used?**
The brief asks about *countries*, and the Atlas gives country area averages; our API route gave one grid cell at the capital. For temperature the two agree reasonably (median correlation 0.91), but for rainfall they differ by 9 pp on median and even flip sign (Kenya: −13 % country vs +11 % at Nairobi). We kept the API data as a comparison (Figure 6).

**Q2. The Atlas has no country masks outside Europe. How did you get Kenya or Brazil?**
We used the Atlas's own *user-defined region* tool and uploaded Natural Earth country borders. To check it, we ran France both ways: the polygon reproduces the Atlas's France mask to 0.004 °C.

**Q3. Are the Atlas series anomalies?**
No. They are absolute values (°C, mm/day), so the 1961–1990 baseline is our choice. We picked it because it is the WMO reference period and the first 30 years for which we also have economic data.

**Q4. Why do you start the change at 1961 if the record starts in 1940?**
ERA5 is less constrained by observations before ~1950, especially for rainfall. We show 1940–2025 but measure change and noise from 1961.

**Q5. What exactly is ERA5?**
A reanalysis: a weather model corrected by every available observation (stations, balloons, satellites since 1979), which gives a complete grid. Temperature is well constrained; rainfall less so, because it comes from the model's physics.

**Q6. How did you merge climate and economy, and what did you lose?**
Exactly on country code and year, so no climate year is lost. The losses are on the WDI side: Vietnam's growth series starts in 1985 (756 instead of 780 observations), the crop index stops in 2023, and the agriculture share starts in the 1990s for Germany, Spain and the USA.

### Description

**Q7. Why compare the change with σ?**
A change only matters for people if it exceeds what they already experience as normal variation. Mexico's +1.4 °C is 5.2σ, far outside anything seen in 1961–1990. Australia's +0.7 °C is 1.7σ, still within a run of ordinary years.

**Q8. Some precipitation trends are significant. Why do you say rainfall didn't change?**
Kenya (−3.4 %/decade), Senegal (−4.1 %) and Spain (−1.8 %) have significant linear trends. But in every country the last decade is within one σ of normal. In the Sahel the trend depends on the window: the wet 1960s are at the start of the sample. We say the evidence for a rainfall change is weak and window-dependent, not that nothing changed.

**Q9. Is the seasonal pattern significant?**
Only in France and Spain, where summer warmed about 1 °C more than autumn (gap > 2 SE). Germany's winter warmed most (+2.5 °C), but German winters vary so much that the gap is not significant.

### Economy and econometrics

**Q10. Country FE gives −0.75 and is significant, two-way FE −0.67 and is not. Which is right?**
Two-way FE. Without year effects, the joint drift of warming and the post-1970s growth slowdown leaks into the estimate. With year effects we only compare countries in the same year. The point estimate barely changes, but the SE rises, the CI becomes [−1.49, +0.16], and adding country trends brings it to −0.04.

**Q11. So warm years don't hurt growth?**
We can't say that. The interval includes zero *and* a loss of 1.5 pp per °C; 12 countries are too few to tell them apart. A typical warm year (0.38 °C above normal) would cost about 0.25 pp if the point estimate were right.

**Q12. Why a wild cluster bootstrap?**
Clustered SEs need many clusters, and we have 12. The wild cluster bootstrap gives reliable p-values with few clusters, and ours are close to the t(11) ones (0.12 vs 0.10 for the preferred model).

**Q13. Why a "hot season" temperature?**
An annual mean dilutes a summer heatwave: France 2003 is 1.2σ as a year but 3.5σ as a summer. The hot season is each country's three warmest calendar months in 1961–1990.

**Q14. Why do crops react but GDP not?**
Exposure. Agriculture is 1–3 % of GDP in France, Germany, Spain, the USA, Australia and South Africa. A 20 % harvest loss there is a fraction of a percentage point of GDP. Crops respond most clearly to rain: +2.2 pp per +10 % of normal (p = 0.002), and −7.6 pp in dry years.

**Q15. Is your result causal?**
The descriptions are descriptions. The economic result is a conditional correlation: weather shocks are plausibly random, but our estimate is too imprecise and fragile to call it a causal effect. Making it causal would take many more units (all countries, or regions), exposure-weighted weather and a pre-specified channel.

**Q16. Does this tell us the cost of climate change?**
No. One unusual year allows neither adaptation (irrigation, crop choice) nor the build-up of damage. The long-run effect is a different question (Burke et al., 2015; Kahn et al., 2021).

### On the process

**Q17. How did you use AI?**
[Group to answer consistently with the AI statement in the paper: which tools, for what, and that every number was produced by our code from the raw data.]

**Q18. What would you do with one more month?**
Extend to every country the Atlas and WDI cover, which multiplies the clusters; weight the climate grid by cropland; and look at sub-national crop data.

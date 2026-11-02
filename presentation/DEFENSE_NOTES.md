# Q&A preparation: likely questions and short answers

Each answer is two or three sentences and quotes a number we can trace to a table in `paper/tables/`. Everyone should be able to give every answer: the brief says any member may be asked about any choice.

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
Exactly on country code and year, so no climate year is lost. The losses are on the WDI side: Vietnam's growth series starts in 1985 (756 instead of 780 observations), the crop index stops in 2023, and the agriculture share starts in the 1990s for Germany, Spain and the USA.

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
Exposure. Agriculture is 1–3 % of GDP in France, Germany, Spain, the USA, Australia and South Africa. A 20 % harvest loss there is a fraction of a percentage point of GDP. Crops respond most clearly to rain: +2.2 pp per +10 % of normal (p = 0.002), and −7.6 pp in dry years.

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

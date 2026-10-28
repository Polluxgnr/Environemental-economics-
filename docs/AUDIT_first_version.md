# Audit: Track 1 project (Environmental Economics, ESSEC/AIDAMS)

Repo audited: `Polluxgnr/Environemental-economics-` (main), against the brief in `docs/assignment_brief.pdf` (Track 1 + sections 3, 4, 6, 7) and the course slides (Cours_CSeghini_2026).
Deadline: paper **Mon 2 Nov 2026**, presentation **Mon 9 Nov 2026**.

## Verdict

The project's structure and reproducibility are strong. I re-ran scripts 02–04 from the committed raw data, and every processed CSV and every table came out identical. Brief steps 1–4 are all covered, and Section 5 already treats the country-FE result with appropriate caution.

The main risks for the grade come from the criteria the brief stresses most: **data honesty, claims that match the evidence, and traceable numbers**. Several statements in the paper either contradict the project's own data or have no source. The underlying dataset also isn't the one the paper describes. All of this can be fixed before 2 November.

---

## A. Critical: fix before submission

### A1. The climate data is not "ERA5 0.25°" as stated
`01_download_data.py` calls the Open-Meteo archive **without a `models=` parameter**, so Open-Meteo returns its default `best_match` blend rather than pure ERA5. I re-downloaded the same 12 capital points with `models=era5` and got different results:

Each column shows your committed data ("blend") next to pure ERA5, for the same coordinates and dates (Δ = 2014–23 mean minus 1960–69 mean):

| | ΔT blend | ΔT ERA5 | SNR blend | SNR ERA5 | ΔP % blend | ΔP % ERA5 |
|---|---|---|---|---|---|---|
| FRA | 1.77 | 1.83 | 3.02 | 3.11 | +3.7 | +2.3 |
| DEU | 2.17 | 2.06 | 2.92 | 2.84 | −7.1 | −8.0 |
| ESP | 2.11 | 2.02 | 3.54 | 3.98 | −10.5 | **−20.0** |
| KEN | 0.71 | **1.48** | 2.40 | **4.87** | +6.5 | **−26.0** |
| SEN | 0.37 | 0.71 | 0.91 | 1.73 | −32.8 | −32.2 |
| ZAF | 1.00 | 1.25 | 1.73 | 2.45 | −19.6 | −16.9 |
| IND | **−0.38** | **+0.17** | −0.71 | 0.36 | −7.0 | −4.9 |
| VNM | 1.08 | 1.05 | 2.66 | 2.66 | +21.3 | **+4.9** |
| AUS | 0.69 | 0.68 | 1.44 | 1.51 | +19.2 | +7.4 |
| USA | 1.18 | **1.92** | 2.20 | 3.76 | +38.3 | **+19.4** |
| BRA | 0.92 | 1.18 | 1.98 | 2.74 | −31.5 | −24.1 |
| MEX | 1.49 | **1.95** | 3.15 | **5.49** | +45.7 | **+25.0** |

(I recomputed both columns with the same formula from daily data, so the "blend" column differs from your Table 1 by about ±0.05.)

A side check on Delhi shows the blend is essentially **ERA5-Land** (0.1°), a different product from ERA5 (0.25°): Delhi ΔT is −0.38 in the blend, −0.32 in ERA5-Land and +0.17 in ERA5. Your paper states the product is ERA5 0.25°, so the paper is inaccurate either way.

The consequences go beyond rounding. Kenya's rainfall flips from +6.5 % to −26 %, India's cooling disappears, the US and Mexico warm about 0.5–0.75 °C more, and the "wetting" in the US, Mexico and Vietnam roughly halves. **Several headline sentences in the paper and README change.**

Both products are legitimate. The issue is that results for a single grid cell depend on which product you use, and the paper names the wrong one. That sensitivity is itself the strongest argument for country averages (see A2).

**Minimum fix (one line):** add `"models": "era5"` (or `"era5_land"`, as long as you say which) to `params` in `fetch_country_climate_records`, delete the cached `data/raw/climate_raw_*.csv` and `climate_daily_1960_2023.csv`, and re-run 01→04. Then update every number in the paper and README.

**New Delhi.** The "aerosol masking + irrigation cooling" explanation has no source and no test behind it. With pure ERA5 the Delhi cooling disappears, so the anomaly most likely came from the data product. Remove the explanation, or keep it only as a cited hypothesis.

### A2. A capital grid cell is not a country
The question asks about *countries*. One grid cell per capital (Mexico City sits at 2,240 m; Washington stands in for the whole USA) is then regressed against *national* GDP. That has two consequences:
- **Description:** a "+46 % precipitation in Mexico" is a statement about one ~30 km cell, not about Mexico.
- **Econometrics:** capital weather is a noisy proxy for national weather. Measurement error biases β toward zero (attenuation), which works *against* finding an effect. Say this explicitly in Section 6.

**Best fix:** download country-averaged series from the **Copernicus Interactive Climate Atlas**, the source the brief names (ERA5, country regions, CSV export). It's 12 countries × 2 variables of clicking, about an hour. If you can't, at least validate 2–3 countries against the Atlas and report the gap. Otherwise, relabel everything as "capital-city climate" (title, figures, conclusions).

### A3. Precipitation changes are presented as signal, but most are noise
You compute a signal-to-noise ratio (SNR) for temperature but not for precipitation. From your current committed data (recompute after A1, because the values will change) (annual totals, Δ = 2014–23 minus 1960–69, divided by the detrended SD):

| | BRA | MEX | USA | VNM | ZAF | SEN | AUS | ESP | DEU | IND | FRA | KEN |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ΔP % | −31.5 | +45.7 | +38.3 | +21.3 | −19.6 | −32.8 | +19.2 | −10.5 | −7.1 | −7.0 | +3.7 | +6.5 |
| ΔP / σ | **−2.03** | **+2.20** | 1.74 | 1.11 | −1.09 | −1.24 | 0.67 | −0.46 | −0.45 | −0.29 | 0.25 | 0.20 |
| Linear trend %/decade | −5.4 | +5.1 | +4.4 | +0.8 | −3.7 | −4.7 | +0.8 | −3.1 | −0.6 | −1.0 | −0.5 | **−2.3** |

- "Spain faces compounding warming and drying stress" doesn't hold up: the change is under half a standard deviation of normal year-to-year variation.
- Kenya's endpoint change (+6.5 %) and its trend (−2.3 %/dec) have **opposite signs**, so the result depends on which decades you compare.
- This is actually a better answer to the brief's question ("does precipitation move in the same places?"). **Temperature change stands out clearly above the noise. Precipitation change mostly doesn't, except at Brasília and Mexico City.** State it that way, and add a precipitation SNR column to Table 1 and to Fig. 3.

### A4. The seasonal claims contradict your own numbers
Warming by season, 2014–23 minus 1960–69 (°C), from `climate_seasonal_anomalies.csv`:

| | Winter | Spring | Summer | Autumn |
|---|---|---|---|---|
| DEU | **3.46** | 1.58 | 2.47 | 1.14 |
| FRA | 2.26 | 1.18 | 2.32 | 1.29 |
| ESP | 1.75 | 2.10 | **2.70** | 1.88 |
| USA | **2.69** | 0.94 | 0.30 | 0.82 |

- Paper §6.1(3) says "In Europe, summer warming outpaced winter warming". That's false for Germany, and France is a tie (2.32 vs 2.26). Only Spain fits. Fig. 4 averages the three countries, which hides this.
- No uncertainty is attached. The difference between two 10-year means has a standard error of about 0.45 × σ_season. German winters have σ ≈ 1.9 °C, so the SE is about ±0.85 °C, and the winter–summer gap of 1 °C is **not distinguishable** from zero.
- "Polar amplification" doesn't explain Berlin or Washington. Either drop the mechanism or cite it with a source (IPCC AR6 WG1).
- DJF/JJA "winter/summer" means little in Nairobi, Dakar, Hanoi or Delhi, where wet and dry seasons are what matter. Say so, or restrict the seasonal analysis to mid-latitude countries.
- Minor: the code groups December with January–February of the *same* year. The usual DJF convention takes December from the previous year.

**Fix:** replace Fig. 4 with a **12 × 4 country-by-season heatmap**, marking cells where |Δ| > 2 SE, and rewrite the conclusion to match.

### A5. The "landmark shock years" story is not in your data, and its numbers have no source
§4.5 and the README claim that 1976, 2003 and 1984 "match visible drops". In your own panel:

| Case | Detrended temp z | Precip z | Crop growth | GDPpc growth (country mean) |
|---|---|---|---|---|
| FRA 1976 | 1.10 | −2.03 | −1.1 % (z −0.25) | **+3.9 %** (2.1) |
| FRA 2003 | **0.91** (not a "shock") | −1.70 | −13.6 % | 0.3 % |
| ESP 2003 | **0.27** | +1.29 | **+13.9 %** | 1.1 % |
| SEN 1984 | 0.49 | −1.78 | +5.6 % | 1.1 % (the drop was **1983**: −36.5 % crop, −8.1 % GDP) |
| KEN 1984 | 0.06 | −0.64 | −14.9 % | −1.9 % |

- In 1976 French GDP per capita grew *above* its average, and the crop index barely moved.
- 2003 isn't even flagged as a heat shock, because **an annual mean dilutes a 2-week summer heatwave**. That's a useful finding to state, and it argues for using summer (JJA) or growing-season anomalies.
- "6-billion-franc *impôt sécheresse*" and "€4 billion farm losses" have no citation. The brief says untraceable figures count as unsupported, and it warns specifically about LLM-produced numbers. Cite a source for them or delete them.
- "Caused documented economic crises" is causal language your design can't support. Use "coincided with".

### A6. Table 3 (shock vs non-shock growth) is driven by COVID and by country composition
The 48 heat-shock years include **2020 for France (−7.7 %) and Mexico (−9.1 %)**. Re-computed from your panel:

| Heatwave gap (pp) | Raw | Country-demeaned | Country+year demeaned |
|---|---|---|---|
| All years | −1.05 (p 0.12) | −1.08 (p 0.08) | **−0.57 (p 0.30)** |
| Without 2020 | −0.73 (p 0.25) | −0.77 (p 0.18) | −0.43 (p 0.44) |

The raw comparison also pools countries with very different average growth (Senegal 0.4 % vs Vietnam 4.9 %), so the result depends on which countries happen to have more shock years. Report the demeaned version, and either flag 2020 or exclude it. Also note that Welch tests treat country-years as independent.

### A7. Inconsistencies a grader will notice
- SNR > 2 lists **6** countries in §3 and **7** in §4.3; the README says "seven". (The US, at 2.19, is missing from §3.)
- The short answer says SNR > 2 "across … East Africa". That's only Kenya.
- §2.4 says the crop index covers 1961–2022 (62 levels, 61 growth years), but the data runs 1961–2023 (63 levels, 62 growth years). The N = 744 is right; the text is wrong.
- §4.5 says "Across the full panel, **no**", but §5.2 correctly calls the result an **uninformative null** (CI −1.31 to +0.004). Use the §5.2 wording everywhere: "we cannot detect an effect, and we cannot rule out a sizeable one".
- §6.1(4) says crop sensitivity is "**confirmed**" at p = 0.0501. That's marginal at best. Write "suggestive".
- `01_download_data.py` labels Kenya (lat −1.29) as "Northern" hemisphere (harmless for seasons, but wrong).
- The compound hot-and-dry shock uses ±1.0 SD thresholds, not ±1.5. This isn't stated anywhere.

---

## B. Econometrics: tighten, don't expand

1. **Interpret the size of the effect in the problem's units, as the brief asks.** β = −0.65 pp per °C, and the typical annual anomaly SD is about 0.5 °C, so a one-SD warm year goes with ≈ −0.3 pp of growth. Compare that with average growth of ~2 %.
2. **Cameron–Gelbach–Miller (2008) is cited, but its method isn't used.** That paper is about the *wild cluster bootstrap*. With 12 clusters, either run it (e.g. the `wildboottest` package) or cite only what you did (t(11) critical values).
3. **Model 4 (continent interactions):** each slope rests on 3 clusters, so its stars aren't credible. Drop the stars or drop the model.
4. **Model 5 (agriculture share in levels):** the R² of 0.90 comes entirely from fixed effects, and weather affecting a *level* share isn't a sensible relationship. Drop it, or use the change in the share.
5. **Remove references you don't use** (Jordà 2005 local projections; Bertrand et al. 2004), or use them.
6. **Report the robustness check you mention.** The AI statement says you tested country-specific trends and decade effects. Put that result in a footnote, since it's your evidence for the "spurious co-trend" story.
7. **One addition worth making:** regress **crop growth on summer/growing-season temperature** rather than the annual mean (see A5). That's the economically meaningful exposure channel.

## C. Figures (graded as "can be read on its own and supports a clear conclusion")

| Fig | Problem | Fix |
|---|---|---|
| 1 | The thin raw-data lines use different colours from the legend, so you can't tell which country is which. The 10-yr mean is *trailing* (starts ~1969 and lags). Some panels mix 12 °C and 24 °C series. | Same colour for raw and smoothed lines; centred rolling mean; or plot anomalies so the series share a scale. Caption should state the conclusion. |
| 2 | Pure methodology: nothing about the question can be concluded from it (the brief says such figures "do not belong"). | Replace with **warming stripes / heatmap of annual anomalies, 12 countries × 64 years** (the filename already says "stripes"). Keep the deseasonalisation point in one sentence of text. |
| 3 | India's label overlaps its value. DEU/ESP labels collide. No uncertainty. "Global hydrological divergence" overclaims from 12 points. | Add precipitation SNR / error bars; fix the labels; retitle. |
| 4 | Continent averages hide opposite country patterns (A4). | 12 × 4 heatmap with significance markers. |
| 5 | Only 4 of 12 countries. The landmark years discussed in the text aren't shown. Dual y-axes. 2020 COVID coincides with a "shock". | Scatter of detrended temp z vs demeaned growth (all country-years, shocks highlighted), or crop growth with drought years marked. |

Applies to all figures: drop the "Figure N:" title baked into the PNG, since the caption already carries it. Make the source line complete, e.g. "ERA5 via Open-Meteo (model era5), capital grid cell, accessed 12 Oct 2026; World Bank WDI".

## D. Writing, structure, compliance

- **Length.** The 10-page limit includes figures and tables. With a 13-column Table 1, Tables 2–3 and five full-width figures, the paper is very likely over the limit once rendered. Export to PDF early and cut: merge Table 3 into text and drop Models 4–5.
- **Tone.** "Short Answer: / Direct Answer: / Question from Brief:" reads like a checklist (and like AI output). Write normal paragraphs. Title: something plain like *"Warming, rainfall and growth in 12 countries, 1960–2023"*. Use "secular" far less.
- **Authors.** "Student Research Group 1" → list the five names.
- **Economic argument** (an assessment criterion). Use the course's **hazard / exposure / vulnerability** framework (IPCC, in the slides): the climate series is the *hazard*, agriculture's share of GDP is *exposure*, and that explains why crop output reacts while national GDP barely does. Cite **Kahn et al. (2021)** from the course, who measure temperature as *deviation from historical norms*, which is exactly your anomaly. Benchmark your European warming against **IPCC AR6 WG1** (Europe warming faster than the global mean). Briefly contrast with **Nordhaus's DICE damage function** (damages from levels vs. your year-to-year shocks).
- **Section 6.** Add one explicit sentence per result: *§3–4 = description; §5 = conditional correlation (with year FE, close to quasi-experimental weather variation, but measured at one point and with 12 clusters); causal claims would need national-area weather, more clusters and a pre-specified exposure channel.*
- **Data citation (brief §4).** Add the Open-Meteo **model name** and ERA5 version, the WDI **release/last-updated date**, and the access date, for each dataset.
- **AI statement.** It must list *every* tool used, including Claude if you use this audit. The sentence "the authors … authored the final prose" must be literally true, or reworded. Undeclared use is penalised; declared use isn't.
- **Repo hygiene.** The README, `docs/full_report.md`, the notebook and `presentation/*` repeat the same numbers. Update them all after the ERA5 re-download, or delete `full_report.md` so there's one source of truth.

## E. Suggested plan (6 days)

1. **Today–Wed:** set `models=era5`, or better, Copernicus Atlas country series → re-run the pipeline → refresh all numbers (A1, A2).
2. **Wed:** fix A3–A7 in the text; add precipitation SNR; demean Table 3.
3. **Thu:** redo Figs 2, 4, 5; fix the colours and labels in Figs 1 and 3.
4. **Fri:** economic framing and citations (D); trim to 10 pages; render the PDF.
5. **Sat–Sun:** read-through by all five members; every member should be able to explain every number (brief §4). Submit Monday.
6. **Defence (9 Nov):** prepare answers to "why capitals?", "why Open-Meteo rather than the Atlas?", "why is the p = 0.051 result a null?", and "what would make it causal?"

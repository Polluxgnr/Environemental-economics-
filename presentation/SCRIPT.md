# Talk script: 10 minutes + 3 minutes Q&A (9 November 2026)

**There is one deck:** the designed deck, <https://claude.ai/artifact/1zyA9MS72NWnftvQrRFxCT> (source: `presentation/deck_source/`). Its speaker notes contain the same text as this file. For an offline copy, use the deck's own export (PDF or PowerPoint) on the morning of the talk.

**Length.** 1,264 spoken words. At 140 words per minute that is 9 minutes; at a calmer 135 plus a few seconds per slide change it is exactly 10:00, which is the timing below. So aim for a steady 140 and never slower. If one part runs long, cut examples, never the handover sentences.

## Who says what

| Speaker | Slides | Part | Time |
|---|---|---|---|
| Speaker 1 | 1–3 | The question, the 12 countries, what "a country's climate" means | 0:00–2:15 |
| Speaker 2 (Pollux) | 4–6 | How we measure change; the full record; signal versus noise | 2:15–5:10 |
| Speaker 3 | 7–10 | Seasons; the economy: hottest summers, the regressions | 5:10–7:45 |
| Speaker 4 | 11–13 | Where shocks bite, what we can claim, the answer | 7:45–10:00 |

Write each person's name in the table above once the split is final. All four answer questions (see `DEFENSE_NOTES.md`).

## The thread: every question gets its answer

Each slide answers the question the previous one raised. If you lose your place, find your slide in this table.

| Slide | Question it answers | Answer | Question it hands on |
|---|---|---|---|
| 1 | — | Is today's climate still the one we planned for? Does the economy notice? | (the two questions of the talk) |
| 2 | Which countries? | 12 countries, 4 continents; every one is warmer | What *is* a country's climate? |
| 3 | What is a country's climate? | 30-year average weather, over the whole territory. A capital's point is not that, above all for rain | How do we measure change? |
| 4 | How do we measure change? | Remove the seasons with a 1961–1990 reference, then compare the change Δ with the noise σ | What does it show for all 12? |
| 5 | What does it show? | Every recent year is red; rainfall has no colour trend | Is that contrast clear in numbers? |
| 6 | In numbers? | Temperature beyond 2σ in 11/12; rainfall in 0/12, measurable in 4 → **answer to question 1** | When in the year? |
| 7 | When in the year? | Evenly, except summer in France and Spain | Does the economy notice? |
| 8 | (part two) | Were the unusual climate years unusual for the economy? | |
| 9 | What happened in the hottest seasons? | Big crop losses, but when heat met drought | Heat or water? Does it reach GDP? |
| 10 | Does heat reach GDP? | No robust effect once we isolate weather | So where do shocks bite? |
| 11 | Where do shocks bite? | Harvests, through water, for one year; not GDP | What kind of claim is this? |
| 12 | What kind of claim? | Description: solid. Correlation: mixed. Causation: not claimed | |
| 13 | **Answer to both opening questions** | Temperature: no longer the old climate. Rainfall: mostly yes. Economy: harvests notice, GDP not detectably | Questions |

**Delivery.**
- One number per sentence: say it, then point at it on the chart.
- Say the type of each result out loud: *description*, *correlation*.
- Each handover is a sentence, not a silence: the last speaker names the next question, the next speaker answers it.

---

### 1. Is today's climate still the one we planned for?  ·  Speaker 1  ·  0:00–0:35

*On screen:* the title over warming stripes (one row per country, one stripe per year since 1940).

> Every plan we make, a harvest, a dam, a heating system, assumes that a normal year looks like the normal years we remember. Our question is whether that is still true. We read eighty-five years of temperature and rainfall records for twelve countries, measured how far they have moved, compared that with ordinary year-to-year swings, and then asked whether the unusual years were also unusual for the economy.

### 2. Twelve countries, and every one is warmer  ·  Speaker 1  ·  0:35–1:15

*Point at:* Germany (darkest), then India and Australia (lightest).

> We chose three countries per continent: temperate Europe, the Mediterranean, the Sahel, East Africa, the monsoon and the Americas, with economies where farming is anywhere from one to over twenty percent of GDP. The headline is already on this map: every one of them is warmer than in 1961 to 1990, from +0.7 degrees in India and Australia to +1.85 in Germany. But before we can say whether that is a lot, we had to answer a more basic question: what exactly is the climate of a country?

### 3. What is a country's climate?  ·  Speaker 1  ·  1:15–2:15

*Point at:* Kenya's two dots (rainfall panel).

> Climate is the weather averaged over thirty years: that is the World Meteorological Organization's definition. And a country's climate is that average over its whole territory, not at one spot. Our first version took one grid point at each capital, from a weather API. When we rebuilt the data from the Copernicus Climate Atlas, which averages the ERA5 reanalysis over each country's borders, temperature barely moved: the typical gap is 0.2 degrees. Rainfall did not survive: the typical gap is nine percentage points, and Kenya even flips sign, from +11 percent at Nairobi to −13 for the country. A warm year is warm over hundreds of kilometres; rain is local. So everything from now on is a country average. *(handover)* Now, how do we measure whether that climate has changed?

### 4. Method: remove the seasons, then compare the change with the noise  ·  Speaker 2 (Pollux)  ·  2:15–3:20

*Point at:* the left panel, then the shaded reference period, the arrow Δ, the grey band σ.

> Here is the whole method on one country, France. On the left, raw monthly temperature. Almost everything you see is the seasons: they are 92 percent of the variation, so a mild January still looks colder than a cool July. To remove them, we compare each month with the same month over 1961 to 1990: a thirty-year climate normal, and the WMO's reference period. What is left is the anomaly. On the right, the yearly anomaly, summed up by two numbers. The change, delta: the last ten years against the reference, +1.74 degrees. The noise, sigma: how far an ordinary year strays from the trend, 0.51. Their ratio, 3.4, asks one question: could the last decade pass for an ordinary year? Above two, it could not. Rainfall goes through exactly the same steps, against the same reference, in percent of normal.

### 5. The full record  ·  Speaker 2 (Pollux)  ·  3:20–4:05

*Point at:* the bar marking 1961–1990 on top, then the right-hand edge of the temperature panel.

> Now all twelve countries, every year since 1940: one row per country, one cell per year, and both panels measured against the same reference, marked on top. On the left, temperature: mostly blue before the 1980s, red after, and every country-year since 2016 is warmer than its 1961–1990 normal. On the right, rainfall: brown is a drier year, blue a wetter one. It flickers, with no colour trend. The years before 1961 are faded: fewer observations stand behind them, so we show them but measure change from 1961. Is the contrast as clear in numbers?

### 6. Signal versus noise  ·  Speaker 2 (Pollux)  ·  4:05–5:10

*Point at:* Mexico, Germany, Australia on the left; Kenya and Senegal on the right.

> It is. Each dot is a country's change; the grey bands are one and two sigma of its ordinary variation. Temperature is beyond two sigma in 11 of 12 countries. Mexico is the clearest case: +1.4 degrees is 5.2 sigma, because its temperature barely varies. Germany warmed more, but its winters swing so much that it is 2.9 sigma. Australia is the one exception, at 1.7. Rainfall is different: everywhere, the change is smaller than one ordinary year's swing, so nobody would feel a new rainfall climate. But a ten-year average is precise, and in four countries, Brazil, India, Kenya and Senegal, the change is measurable: Kenya −14 percent. And it does not follow the warming. So: temperature has clearly moved; rainfall much less. *(handover)* But when in the year does the warming happen?

### 7. When in the year  ·  Speaker 3  ·  5:10–5:40

*Point at:* the boxed summer cells of France and Spain, then Germany's winter.

> Mostly, evenly across the year. Only in France and Spain is one season clearly ahead: summer warmed by about +2.3 degrees, against +1.3 in autumn. Germany's winter warmed even more, +2.5, but German winters vary so much that we cannot call it faster. Summer-heavy warming matters because it lands exactly when crops need water and cities need cooling. Which brings us to the second half of our question.

### 8. Part two: the economy  ·  Speaker 3  ·  5:40–5:45

> Were the unusual climate years also unusual for the economy?

*(Read the title, one beat of silence, next slide.)*

### 9. The hottest summers  ·  Speaker 3  ·  5:45–6:40

*Point at:* France 2003 (purple bar −21, black bar −1.5).

> One measurement point first: an annual mean dilutes a heatwave. France's 2003 is 1.2 sigma as a year, but 3.4 sigma as a summer. So we use each country's hot season, its three warmest months. Here is every country's hottest one, and how growth compared with what the country and the year would predict: purple for crops, black for GDP. France 2003: crops −21 points, GDP −1.5. But the big crop losses were heat and drought together: Germany 2003 and Australia 2019 were each country's hottest and driest year, and France 2003 and the US in 1988 were dry too. So, heat or water? And does it reach GDP? We tested both on every country-year.

### 10. Testing it  ·  Speaker 3  ·  6:40–7:45

*Point at:* the grey lines, then the red line (model 4) crossing zero.

> We regress growth on the temperature and rainfall anomalies: 756 country-years. The grey lines are the naive versions: comparing each country only with itself, a warmer year costs 0.75 points of growth, and it looks significant. Year effects remove shocks every country shares, like 2009. But one problem remains: the countries that warmed fastest also slowed most. The two trends correlate at −0.57, and dropping India alone moves the estimate from −0.67 to −0.38. So our preferred model, in red, also gives each country its own trend, which leaves only year-to-year weather. The effect: −0.04 points per degree, with an interval from −0.76 to +0.69, and a wild bootstrap, built for twelve clusters, gives p = 0.92. No detectable effect, and losses above about 0.8 points per degree are ruled out in our sample. *(handover)* So where do climate shocks bite?

### 11. Where shocks bite  ·  Speaker 4  ·  7:45–8:35

*Point at:* the right panel's slope.

> In harvests rather than GDP, and through water rather than heat. On the right, a year ten percent wetter than normal goes with crop output about 2.2 percent higher, and that is robust: dropping any country, or adding country trends, barely changes it. It lasts one year: the next year output returns to normal. In dry years crop growth is 7.6 points below normal, while GDP growth is only 0.27 below. The likely reason is exposure: in most of our countries agriculture is one to three percent of GDP. That is the IPCC chain from the course: a hazard becomes a loss only through exposure and vulnerability.

### 12. What we can and cannot conclude  ·  Speaker 4  ·  8:35–9:25

> What kind of claims are these? The climate results are descriptions, and they are solid. The economic results are correlations. Year-to-year weather is close to random, so our design is close to an experiment; but with twelve countries, rich and poor pooled together, we do not claim causal effects, and an effect limited to poorer, farming economies could be hidden. And a hot year is not climate change: it allows no adaptation and no build-up of damage. Going further would take many more regions, weather weighted by where crops and people are, and a channel fixed in advance.

### 13. So, is today's climate still the one we planned for?  ·  Speaker 4  ·  9:25–10:00

> Back to our question. For temperature, no: every country is warmer, and in 11 of 12 the last decade could not pass for an ordinary year. For rainfall, mostly yes: it changed far less, locally, and how much depends on how carefully you measure it. And does the economy notice? Harvests do, for a year, through water; GDP, not detectably in our twelve countries. Thank you; we are happy to take questions.

---

### Backup: data and definitions (Q&A only)

- Climate: Copernicus Interactive Climate Atlas (C3S/ECMWF), ERA5, monthly 1940–2025, 288 series (12 countries × 2 variables × 12 calendar months). FRA/DEU/ESP: Atlas country masks; 9 others: Atlas user-defined regions with Natural Earth borders (USA = 48 contiguous states). Validated on France to 0.004 °C.
- Anomaly = month minus its 1961–1990 calendar-month mean; rainfall = mm/day × days in the month, anomaly in % of the 1961–1990 average; Δ = mean 2016–2025; σ = SD of the detrended annual anomaly, 1961–2025.
- Economy: World Bank WDI, release 8 Oct 2026: GDP per capita growth, crop production index, agriculture share.
- Regressions: two-way fixed effects (+ country trends in the preferred model 4), SE clustered by country, t(11) + wild cluster bootstrap (Webb weights, 9,999 draws).
- How each number above is computed, from the raw file to the slide: `DEFENSE_NOTES.md`, part 2.

# Talk script: 10 minutes + 3 minutes Q&A (9 November 2026)

**The deck:** [`Track1_presentation.pptx`](Track1_presentation.pptx), 12 slides. There is no "Questions?" slide: Eliott's last line opens the Q&A, and everything for the Q&A (data definitions, likely questions, how each number is computed) is in `DEFENSE_NOTES.md`. Each slide's speaker notes contain its text below, with the speaker and the timing. Rebuilt by `scripts/08_build_deck.py`.

**Length.** 1,304 spoken words: 9 min 20 s at 140 words per minute, plus about 3 seconds per slide change, which gives the timings below (end at 9:55). Aim for a steady 140; if a part runs long, cut examples, never the handover sentences.

## Who says what

| Who | Slides | Part | Time |
|---|---|---|---|
| Saty | 1–3 | The question, our countries, our data | 0:00–2:35 |
| Pollux | 4–6 | How we measure change; how far the climate moved; is it large next to normal swings | 2:35–5:20 |
| Augustin | 7–9 | Seasons; the economy: hottest summers, the regressions | 5:20–7:45 |
| Eliott | 10–12 | Where shocks bite, what we can claim, the answers | 7:45–9:55 |

All four answer questions (see `DEFENSE_NOTES.md`).

## The thread: three questions, answered in order

Slide 1 asks three questions. Every slide after it answers one of them, or the question the slide before it raised, and slide 12 answers all three.

| Slide | Question it answers | Answer | Question it hands on |
|---|---|---|---|
| 1 | — | **Q1** How far has the climate moved? **Q2** Is that large next to normal ups and downs? **Q3** Were the unusual years unusual for the economy? | |
| 2 | Which countries, and why? | 3 per continent, different climates and economies; every one is warmer | How do we get one number for a whole country? |
| 3 | How do we get a country's number? | Not one point at the capital, but the Copernicus Atlas country average | How do we measure change? |
| 4 | How do we measure change? | Three steps: remove the seasons, measure the change Δ, compare it with the noise σ | |
| 5 | **Q1** How far has the climate moved? | Every country-year since 2016 is warmer; rainfall has no trend | **Q2** Is that large next to normal swings? |
| 6 | **Q2** | Temperature: yes in 11/12. Rainfall: no, though its average shifted in 4 | When in the year? |
| 7 | When in the year? | Evenly, except summer in France and Spain | **Q3** |
| 8 | **Q3** Were the unusual years unusual for the economy? First: what happened in the hottest seasons? | Big crop losses, but when heat met drought | Heat or water? Does it reach GDP? |
| 9 | Does heat reach GDP? | No robust effect once we isolate weather | So where do shocks bite? |
| 10 | Where do shocks bite? | Harvests, through water, for one year; not GDP | What kind of claim is this? |
| 11 | What kind of claim? | Description: solid. Correlation: mixed. Causation: not claimed | |
| 12 | **Q1, Q2, Q3** | +0.7 to +1.85 °C · temperature beyond normal swings in 11/12, rainfall in none · harvests notice, GDP not detectably | Questions |

**Delivery.**
- One number per sentence: say it, then point at it on the chart.
- Say the type of each result out loud: *description*, *correlation*.
- Each handover is a sentence, not a silence: the last speaker names the next question, the next speaker answers it.

---

### 1. Is today's climate still the one we planned for?  ·  Saty  ·  0:00–0:40

*On screen:* the title and the three questions of the talk.

> Every plan we make, from when to sow a field to how high to build a dam, assumes that next year will look like the years we remember. We want to know if that is still true. To find out, we looked at temperature and rainfall records for twelve countries, from 1940 to 2025, and asked three things. How far has the climate moved? Is that large next to normal ups and downs? And were the unusual years also unusual for the economy?

### 2. Our choice of countries  ·  Saty  ·  0:40–1:30

*Point at:* France, Germany and Spain for Europe, then Kenya and South Africa, then Germany (darkest), India and Australia (lightest).

> We looked at four continents and chose three countries in each, trying to get different economies or different climates within each continent. In Europe, that gives us a temperate, a continental and a Mediterranean climate. In Africa, farming is about 21% of GDP in Kenya and 2.5% in South Africa, and that difference will matter later. The map gives the headline. We compare the last ten years with 1961 to 1990, our reference period, and every country is warmer, from +0.7 degrees in India and Australia to +1.8 in Germany. Each of those numbers is a single value for a whole country. Getting that value is harder than it looks, as our first attempt showed.

### 3. Our data: a capital is not a country  ·  Saty  ·  1:30–2:35

*Point at:* the orange crosses in the legend, the black dots, then the Kenya row on the right panel.

> In that first attempt, we took one point at each capital from a free weather API. Those are the orange crosses. But a capital is not a country, so we rebuilt everything from the Copernicus Climate Atlas. It uses ERA5, a weather model corrected with millions of real observations, and averages it over each country's borders. Those are the black dots. For temperature, on the left, the two mostly agree, typically about 0.2 degrees apart. For rainfall, on the right, they often don't, and in three countries the sign flips. In Kenya, the capital point says rainfall went up 11%; the country average says it fell 13%. A warm year is warm over hundreds of kilometres, while rain is local. That was our first lesson: check what your data measure. So every number from here on is a country average. The next question is how to measure change.

### 4. How we measure change: three steps  ·  Pollux  ·  2:35–3:40

*Point at:* the step cards one by one; for step 1 the left panel, for step 2 the black arrow, for step 3 the grey band.

> How do we measure change? In three steps, shown here on France. Step one: remove the seasons. On the left is raw monthly temperature, and the seasons are 92 percent of what you see: a mild January still looks colder than a cool July. So we compare each month with the same month in 1961 to 1990, the WMO's reference period. What is left is the anomaly; on the right, it is averaged by year. Step two: the change, delta, the last ten years against the reference: +1.74 degrees. Step three: compare it with the noise, sigma, how far an ordinary year strays from the trend: 0.51 degrees. The ratio is 3.4. Above two, the last decade could not pass for an ordinary year. Rainfall gets the same three steps, in percent of its 1961–1990 average.

### 5. How far has the climate moved?  ·  Pollux  ·  3:40–4:25

*Point at:* the "reference 1961–1990" bar on top, the dark-red right edge of the temperature panel, then the rainfall panel.

> Now the same method on all twelve countries, every year since 1940: one row per country, one cell per year, both measured against the same reference, marked on top. Temperature, on the left: mostly blue before the 1980s, red after, and all hundred and twenty country-years since 2016 are warmer than their old normal. Rainfall, on the right: brown is a drier year, blue a wetter one, and they simply alternate, with no trend. The years before 1961 are faded because fewer observations stand behind them. So for temperature, the climate has clearly moved. But is that large next to normal ups and downs?

### 6. Is it large next to normal swings?  ·  Pollux  ·  4:25–5:20

*Point at:* Mexico, Germany, Australia on the left; Kenya and Senegal on the right.

> This chart answers it. Each dot is a country's change; the grey bands are one and two sigma, that country's normal swing. Temperature is beyond two sigma in 11 of 12 countries. Mexico is the clearest case: +1.4 degrees is 5.2 sigma, because its temperature barely varies. Germany warmed more, but its winters swing so much that it is 2.9 sigma. Australia is the only exception, at 1.7. Rainfall: everywhere, the change is smaller than one ordinary year's swing, so nobody would feel a new rainfall climate. Still, its ten-year average shifted measurably in four countries: Brazil, India, Kenya and Senegal. So temperature has clearly moved, rainfall much less. *(handover)* But when in the year does the warming happen?

### 7. When in the year  ·  Augustin  ·  5:20–5:50

*Point at:* the boxed summer cells of France and Spain, then Germany's winter.

> Mostly, evenly across the year. Only in France and Spain is one season clearly ahead: summer warmed by about +2.3 degrees, against +1.3 in autumn. Germany's winter warmed even more, +2.5, but German winters vary so much that we cannot call it faster. Summer-heavy warming matters because it lands exactly when crops need water and cities need cooling. Which brings us to our third question.

### 8. The hottest summers  ·  Augustin  ·  5:50–6:45

*Point at:* France 2003 (purple bar −21, black bar −1.5).

> Were the unusual climate years also unusual for the economy? One measurement point first: an annual mean dilutes a heatwave. France's 2003 is 1.2 sigma as a year, but 3.4 sigma as a summer. So we use each country's hot season, its three warmest months. Here is every country's hottest one, and how growth compared with what the country and the year would predict: purple for crops, black for GDP. France 2003: crops −21 points, GDP −1.5. But the big crop losses were heat and drought together: Germany 2003 and Australia 2019 were each country's hottest and driest year, and France 2003 and the US in 1988 were dry too. So, heat or water? And does it reach GDP? We tested both on every country-year.

### 9. Testing it  ·  Augustin  ·  6:45–7:45

*Point at:* the grey lines, then the red line (model 4) crossing zero.

> We regress growth on the temperature and rainfall anomalies: 756 country-years. The grey lines are the naive versions: comparing each country only with itself, a warmer year costs 0.75 points of growth, and it looks significant. Year effects remove shocks every country shares, like 2009. But the countries that warmed fastest also slowed most: the two trends correlate at −0.57, and dropping India alone moves the estimate from −0.67 to −0.38. So our preferred model, in red, also gives each country its own trend, which leaves only year-to-year weather. The effect: −0.04 points per degree, interval −0.76 to +0.69, and the wild bootstrap gives p = 0.92. No detectable effect, and losses above about 0.8 points per degree are ruled out in our sample. *(handover)* So where do climate shocks bite?

### 10. Where shocks bite  ·  Eliott  ·  7:45–8:30

*Point at:* the right panel's slope, then the flat red line on the left.

> In harvests rather than GDP, and through water rather than heat. On the right, a year ten percent wetter than normal goes with crop output about 2.2 percent higher, and that holds whichever country we drop. It lasts one year: the next year output returns to normal. In dry years crop growth is 7.6 points below normal, while GDP growth is only 0.27 below. The likely reason is exposure: in most of our countries agriculture is one to three percent of GDP. That is the IPCC chain from the course: a hazard becomes a loss only through exposure and vulnerability.

### 11. What we can and cannot conclude  ·  Eliott  ·  8:30–9:15

> What kind of claims are these? The climate results are descriptions, and they are solid. The economic results are correlations. Year-to-year weather is close to random, so our design is close to an experiment; but with twelve countries, rich and poor pooled together, we do not claim causal effects, and an effect limited to poorer, farming economies could be hidden. And a hot year is not climate change: it allows no adaptation. Going further would take many more regions, weather weighted by where crops and people are, and a channel fixed in advance.

### 12. Back to our three questions  ·  Eliott  ·  9:15–9:55

*Point at:* the three columns, left to right.

> Back to our three questions. How far has the climate moved? Every country is warmer, by 0.7 to 1.85 degrees. Is that large next to normal ups and downs? For temperature, yes, in 11 of 12 countries; for rainfall, no, though its average shifted in four. And were the unusual years unusual for the economy? Harvests, yes, for a year and through water; GDP, not detectably. So for temperature, today's climate is no longer the one we planned for. Thank you; we are happy to take questions.

---

For the Q&A: data definitions, 22 likely questions and how every number above is computed are in `DEFENSE_NOTES.md`.

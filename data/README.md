# Data

Everything the paper uses is in this folder, together with the scripts that downloaded it. Each script caches its downloads, so re-running the pipeline uses these files and doesn't hit the APIs again.

## 1. Climate: Copernicus Interactive Climate Atlas (primary source)

| | |
|---|---|
| Producer | Copernicus Climate Change Service (C3S), implemented by ECMWF |
| Product | Copernicus Interactive Climate Atlas, dataset **ERA5** (reanalysis) |
| Variables | `t`: mean of daily mean 2 m temperature (°C); `pr`: mean of daily accumulated precipitation (mm/day) |
| Spatial unit | area average over each country |
| Frequency | monthly (one series per calendar month), 1940–2025 |
| Accessed | 28 October 2026 (see `raw/atlas/DOWNLOAD_LOG.json`) |
| Files | `raw/atlas/json/<ISO3>_<var>_<Mon>.json` (raw server responses), `raw/atlas/atlas_era5_monthly.csv` (tidy) |

**The series are absolute values, not anomalies.** We chose and computed the 1961–1990 baseline ourselves.

### How to get the same numbers by hand
1. Open https://atlas.climate.copernicus.eu/atlas and close the welcome window.
2. *Select a dataset* → **ERA5**. *Select a variable* → **Mean temperature** (or **Precipitation → Mean of daily accumulated precipitation**).
3. *Season or month* → pick a month (or *Annual*). *Quantity* → **Value**.
4. Region selector above the map:
   - France, Germany, Spain: choose **European countries**, click the country, then **Regional Information → Download data → CSV**.
   - The other nine countries: the Atlas has no predefined country masks outside Europe, only the large IPCC-AR6 regions. Choose **User defined**, upload or draw the country border (the upload icon accepts a GeoJSON; ours is `raw/atlas/regions_user_defined.geojson`), then **Create new Job**. When the job shows *OK*, open it and download the CSV.

`scripts/00_download_atlas.py` sends exactly the requests these clicks trigger:
- `GET /temporal/serie?project=ERA5&variable=t&...&region=european-countries&ids=<id>` for the European masks (France = 2, Germany = 15, Spain = 0).
- `POST /job/temporal/serie?...&aggFun=mean`, with the polygon as WKT, for user-defined regions. The script then polls `GET /job/temporal/serie?jobId=...`.

We checked this in the browser's network log: the CSV button formats that same JSON response.

### Region choices and what they imply
- **Borders.** The nine user-defined regions are Natural Earth 1:50m admin-0 borders, simplified to 0.05°.
- **United States.** Restricted to the 48 contiguous states; Alaska and Hawaii are excluded.
- **Coastal cells.** These are partly sea, so a country mean includes some ocean grid area at the coast (the Atlas reports land and sea area for its European masks).
- **ERA5 itself.** It is a reanalysis: a weather model constrained by observations. Before about 1950, and before satellites in 1979, fewer observations constrain it, especially for precipitation over Africa. We show the full 1940–2025 record but measure change from 1961 onwards.

## 2. Climate: Open-Meteo capital grid points (comparison only)

| | |
|---|---|
| Producer | Open-Meteo Historical Weather API, serving ECMWF reanalyses |
| Files | `raw/openmeteo/best_match/` (our first version), `raw/openmeteo/era5/` |
| Unit | one grid cell containing the national capital, daily, 1960–2023 |
| Accessed | best_match: 12 Oct 2026; era5: 27 Oct 2026 |

Our first version downloaded these files **without** a `models=` parameter, so Open-Meteo returned its default *best_match* blend. For these dates that blend is essentially ERA5-Land (0.1°), not ERA5 (0.25°) as we first wrote. `scripts/03_compare_sources.py` puts all three routes through identical definitions (Table A1, Figure 6).

## 3. Economy: World Bank World Development Indicators

| | |
|---|---|
| Producer | World Bank |
| Dataset | World Development Indicators, API v2, release of **8 October 2026** |
| Accessed | 28 October 2026 (`raw/worldbank_wdi_metadata.json`) |
| Indicators | `NY.GDP.PCAP.KD.ZG` real GDP per capita growth (%); `AG.PRD.CROP.XD` crop production index (2014–2016 = 100); `NV.AGR.TOTL.ZS` agriculture, forestry and fishing value added (% of GDP); `NY.GDP.MKTP.KD.ZG` real GDP growth (%) |
| File | `raw/worldbank_wdi.csv`, 1960–2025 |

**Merge.** The two sources are merged on (ISO3 country code, calendar year), and the match is exact: no climate year is lost.

**What the merge loses.** Gaps on the WDI side:
- Vietnam's GDP per capita growth starts in 1985.
- The crop index ends in 2023.
- The agriculture share starts late for several countries: Germany 1991, Spain 1995, the USA 1997.
- Germany's pre-1991 GDP figures are the World Bank's reconstruction for unified Germany.

## 4. Maps

`raw/maps/ne_110m_admin0.geojson`: Natural Earth 1:110m borders, used only for the map on the title slide.

## Processed files (`processed/`)

| File | Content |
|---|---|
| `climate_monthly.csv` | monthly levels, 1961–1990 climatology, anomalies (°C, mm, %), 1940–2025 |
| `climate_seasonal.csv` | DJF/MAM/JJA/SON anomalies (December counted with the following year) |
| `climate_annual.csv` | annual levels and anomalies, hot-season anomaly, detrended z-scores, shock flags |
| `panel.csv` | climate × WDI, 12 countries × 1961–2025 |
| `source_comparison_annual.csv` | annual anomalies under the three data routes |
| `regression_results_raw.csv` | every coefficient, SE, CI and p-value behind Table 3 |

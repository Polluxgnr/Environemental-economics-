"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 06: PRESENTATION VISUALS (16:9)
================================================================================

Output: presentation/figures/*.png   (the charts of the designed deck, without baked-in titles, plus the
                                      warming stripes of the cover and the section slides)

The talk itself is the designed deck (presentation/deck_source/); its spoken text
is presentation/SCRIPT.md, and DEFENSE_NOTES.md traces every number it quotes.
All numbers drawn here are computed from data/processed and paper/tables.
"""

import os
import sys
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap
from matplotlib.patches import Rectangle

# Rainfall anomalies: dry = brown (earth), normal = white, wet = blue (water)
RAIN_CMAP = LinearSegmentedColormap.from_list(
    "dry_wet", ["#7f3b08", "#c47a2c", "#f1d9a7", "#f7f7f5", "#a6cee3", "#3b82c4", "#08306b"])

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "data", "processed")
TABLES = os.path.join(ROOT, "paper", "tables")
OUT = os.path.join(ROOT, "presentation", "figures")
MAPS = os.path.join(ROOT, "data", "raw", "maps")
os.makedirs(OUT, exist_ok=True)
os.makedirs(MAPS, exist_ok=True)

ORDER = ["FRA", "DEU", "ESP", "KEN", "SEN", "ZAF", "IND", "VNM", "AUS", "USA", "BRA", "MEX"]
NAMES = {"FRA": "France", "DEU": "Germany", "ESP": "Spain", "KEN": "Kenya", "SEN": "Senegal",
         "ZAF": "South Africa", "IND": "India", "VNM": "Vietnam", "AUS": "Australia",
         "USA": "United States", "BRA": "Brazil", "MEX": "Mexico"}
INK, MUTED, WARM, COOL, WET, DRY, CROP = "#1f2328", "#6e7781", "#c0392b", "#2c7fb8", "#1b7f6b", "#a6611a", "#7a5195"
W, H = 13.33, 7.5
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 15, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.dpi": 150})
SRC = "Copernicus Interactive Climate Atlas, ERA5 country means (accessed 28 Oct 2026)"


def detrended_sd(d, col):
    return (d[col] - np.polyval(np.polyfit(d.year, d[col], 1), d.year)).std(ddof=1)


# "Clean" mode draws the charts for the designed deck: no baked-in title or footer (the slide
# carries them), painted on the deck's paper colour. Set it to False for standalone charts
# with their title and source line.
CLEAN = True
DECK_BG = "#F7F5F0"


def footer(fig, text):
    import textwrap
    if CLEAN:
        return
    fig.text(0.015, -0.05, textwrap.fill(text, 175), fontsize=10, color=MUTED, va="top")


def save(fig, name):
    out_dir = OUT
    kw = {}
    if CLEAN:
        if fig._suptitle is not None:
            fig._suptitle.set_visible(False)
        fig.patch.set_facecolor(DECK_BG)
        for ax in fig.axes:
            ax.set_facecolor(DECK_BG)
        kw["facecolor"] = DECK_BG
    fig.savefig(os.path.join(out_dir, name), bbox_inches="tight", pad_inches=0.3, **kw)
    plt.close(fig)
    return os.path.join(out_dir, name)


def deck_stripes(a):
    """Full-bleed warming stripes of the 12 countries (cover) and of their mean (section band). No text."""
    years = np.arange(1940, a.year.max() + 1)
    M = a.pivot(index="country_code", columns="year", values="temp_anom").reindex(index=ORDER, columns=years)
    norm = TwoSlopeNorm(0, -2.2, 2.2)
    os.makedirs(OUT, exist_ok=True)
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(M.values, aspect="auto", cmap="RdBu_r", norm=norm, interpolation="nearest")
    for y in np.arange(0.5, 11.5):
        ax.axhline(y, color="#14213D", lw=1.2, alpha=0.35)
    ax.set_axis_off()
    fig.savefig(os.path.join(OUT, "cover_stripes.png"), dpi=100)
    plt.close(fig)
    fig = plt.figure(figsize=(19.2, 2.4), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(M.mean().values[None, :], aspect="auto", cmap="RdBu_r", norm=TwoSlopeNorm(0, -1.6, 1.6),
              interpolation="nearest")
    ax.set_axis_off()
    fig.savefig(os.path.join(OUT, "band_stripes.png"), dpi=100)
    plt.close(fig)


def country_changes(a):
    rows = []
    for c in ORDER:
        d = a[(a.country_code == c) & a.year.between(1961, 2025)]
        last = d.year.between(2016, 2025)
        rows.append({"c": c, "dT": d.loc[last, "temp_anom"].mean(), "sT": detrended_sd(d, "temp_anom"),
                     "dP": d.loc[last, "precip_anom_pct"].mean(), "sP": detrended_sd(d, "precip_anom_pct")})
    return pd.DataFrame(rows).set_index("c")


# ------------------------------------------------------------------------------
def slide_map(ch):
    import geopandas as gpd
    path = os.path.join(MAPS, "ne_110m_admin0.geojson")
    if not os.path.exists(path):
        gpd.read_file("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
                      "ne_110m_admin_0_countries.geojson")[["ADM0_A3", "NAME", "geometry"]].to_file(path, driver="GeoJSON")
    from shapely.geometry import box
    world = gpd.read_file(path)
    world = world[world.ADM0_A3 != "ATA"]
    # metropolitan France only (Natural Earth includes French Guiana in the same feature)
    world.loc[world.ADM0_A3 == "FRA", "geometry"] = world.loc[world.ADM0_A3 == "FRA", "geometry"].intersection(box(-6, 41, 10, 52))
    # contiguous USA, as in the Atlas region we used
    world.loc[world.ADM0_A3 == "USA", "geometry"] = world.loc[world.ADM0_A3 == "USA", "geometry"].intersection(box(-125, 24, -66, 50))
    world["dT"] = world.ADM0_A3.map(ch.dT)
    fig, ax = plt.subplots(figsize=(W, H))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.08)
    world.plot(ax=ax, color="#eaeef2", edgecolor="white", lw=0.4)
    sel = world.dropna(subset=["dT"])
    sel.plot(ax=ax, column="dT", cmap="Reds", vmin=0, vmax=2.2, edgecolor=INK, lw=0.6, legend=True,
             legend_kwds={"orientation": "horizontal", "shrink": 0.3, "pad": 0.0, "aspect": 30,
                          "label": "Warming, 2016-2025 vs 1961-1990 (°C)"})
    # label anchor (lon, lat), placed in the ocean so labels never overlap
    label_pos = {"FRA": (-40, 50), "DEU": (30, 62), "ESP": (-40, 33), "KEN": (58, -8), "SEN": (-42, 14),
                 "ZAF": (45, -38), "IND": (80, 2), "VNM": (128, 14), "AUS": (118, -45),
                 "USA": (-140, 40), "BRA": (-20, -15), "MEX": (-135, 14)}
    for _, r in sel.iterrows():
        p = r.geometry.representative_point()
        ax.annotate(f"{NAMES[r.ADM0_A3]} +{r.dT:.1f} °C", (p.x, p.y), xytext=label_pos[r.ADM0_A3],
                    ha="center", va="center", fontsize=12, fontweight="bold", color=INK,
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8),
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#d0d7de"))
    ax.set_xlim(-160, 170); ax.set_ylim(-52, 72)
    ax.set_axis_off()
    fig.suptitle("12 countries, 4 continents: every one is warmer than in 1961-1990",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Country-average temperature. " + SRC)
    return save(fig, "slide_02_map.png")


def slide_route():
    t = pd.read_csv(os.path.join(TABLES, "table_A1_source_comparison.csv")).set_index("country").reindex(ORDER)
    fig, axes = plt.subplots(1, 2, figsize=(W, H), sharey=True, gridspec_kw={"wspace": 0.06})
    styles = [("atlas", "Country average (Copernicus Atlas)", "o", INK, 11),
              ("blend_point", "One grid point at the capital (our first version)", "X", "#e66101", 11)]
    for ax, v, unit, title in [(axes[0], "dT", "°C", "Temperature change"), (axes[1], "dP", "%", "Rainfall change")]:
        for i, c in enumerate(ORDER):
            vals = [t.loc[c, f"{v}_{s}"] for s, *_ in styles]
            ax.plot(vals, [i, i], color="#d0d7de", lw=6, solid_capstyle="round", zorder=1)
            for s, lab, mk, col, ms in styles:
                ax.plot(t.loc[c, f"{v}_{s}"], i, mk, color=col, ms=ms, label=lab if i == 0 else None, zorder=2)
        ax.axvline(0, color=MUTED, lw=1)
        ax.set_xlabel(f"2014-2023 vs 1961-1990 ({unit})")
        ax.set_title(title, loc="left", fontsize=17, fontweight="bold")
    axes[0].set_yticks(range(12)); axes[0].set_yticklabels([NAMES[c] for c in ORDER]); axes[0].invert_yaxis()
    fig.legend(*axes[0].get_legend_handles_labels(), frameon=False, fontsize=13, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.04))
    n_flip = int(((np.sign(t.dP_atlas) != np.sign(t.dP_blend_point)) & (t.dP_atlas.abs() > 3)).sum())
    fig.suptitle(f"A capital is not a country: rainfall change flips sign in {n_flip} of 12 countries",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Same definitions for both routes, 1961-2023. Open-Meteo API (default model) vs " + SRC)
    return save(fig, "slide_03_data_route.png")


def slide_stripes(a):
    years = np.arange(1940, a.year.max() + 1)
    fig, axes = plt.subplots(1, 2, figsize=(W, H), sharey=True, gridspec_kw={"wspace": 0.09})
    for ax, col, cmap, lim, title, words in [
            (axes[0], "temp_anom", "RdBu_r", 2.5, "Temperature (°C vs 1961-1990)", "← colder than 1961-1990     warmer →"),
            (axes[1], "precip_anom_pct", RAIN_CMAP, 40, "Rainfall (% vs 1961-1990)", "← drier than 1961-1990     wetter →")]:
        M = a.pivot(index="country_code", columns="year", values=col).reindex(index=ORDER, columns=years)
        im = ax.imshow(M.values, aspect="auto", cmap=cmap, norm=TwoSlopeNorm(0, -lim, lim),
                       extent=[years[0] - .5, years[-1] + .5, 11.5, -.5], interpolation="nearest")
        for y in [2.5, 5.5, 8.5]:
            ax.axhline(y, color="white", lw=3)
        # 1940-1960: fewer observations behind ERA5, shown but not used to measure change
        ax.axvspan(years[0] - .5, 1960.5, color=DECK_BG if CLEAN else "white", alpha=0.55, lw=0, zorder=3)
        # the reference period both anomalies are measured against
        ax.plot([1960.6, 1990.4], [-0.75, -0.75], color=INK, lw=2.5, clip_on=False, solid_capstyle="butt")
        ax.text(1975.5, -0.95, "reference 1961-1990", ha="center", va="bottom", fontsize=12, color=INK)
        ax.set_ylim(11.5, -1.6)
        ax.spines["left"].set_bounds(11.5, -0.5)
        ax.set_title(title, loc="left", fontsize=17, fontweight="bold")
        ax.set_xticks([1940, 1960, 1980, 2000, 2020])
        cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.045, pad=0.07, aspect=35)
        cb.set_label(words, fontsize=13, color=INK)
    axes[0].set_yticks(range(12)); axes[0].set_yticklabels([NAMES[c] for c in ORDER])
    fig.suptitle("Every recent year is red. Rainfall has no colour trend: it is noise around the normal",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "One cell = one year, 1940-2025. Both variables are measured against the same reference period, "
                "1961-1990: temperature in °C above or below it, rainfall in % of its 1961-1990 average. "
                "1940-1960 faded: fewer observations behind the reanalysis. " + SRC)
    return save(fig, "slide_05_stripes.png")


def slide_signal(ch):
    t = ch.sort_values("dT")
    fig, axes = plt.subplots(1, 2, figsize=(W, H), sharey=True, gridspec_kw={"wspace": 0.06})
    for ax, d, s, col, unit, title in [(axes[0], "dT", "sT", WARM, "°C", "Temperature"),
                                       (axes[1], "dP", "sP", WET, "%", "Rainfall")]:
        for i, (c, r) in enumerate(t.iterrows()):
            ax.add_patch(Rectangle((-2 * r[s], i - .35), 4 * r[s], .7, color="#d0d7de", lw=0))
            ax.add_patch(Rectangle((-r[s], i - .35), 2 * r[s], .7, color="#afb8c1", lw=0))
            out = abs(r[d]) > 2 * r[s]
            ax.plot(r[d], i, "o", ms=12, mfc=col if out else "white", mec=col, mew=2.5, zorder=3)
            ax.text(r[d] + (0.1 if d == "dT" else 3) * np.sign(r[d] if r[d] else 1), i, f"{r[d] / r[s]:+.1f}σ",
                    va="center", ha="left" if r[d] >= 0 else "right", fontsize=12)
        ax.axvline(0, color=INK, lw=1)
        ax.set_title(title, loc="left", fontsize=17, fontweight="bold")
        ax.set_xlabel(f"Change 2016-2025 vs 1961-1990 ({unit})")
    axes[0].set_xlim(-2 * t.sT.max() - .2, t.dT.max() + .9)
    lim = max(t.dP.abs().max(), 2 * t.sP.max()) * 1.35
    axes[1].set_xlim(-lim, lim)
    axes[0].set_yticks(range(12)); axes[0].set_yticklabels([NAMES[c] for c in t.index])
    nT = int((t.dT > 2 * t.sT).sum()); nP = int((t.dP.abs() > 2 * t.sP).sum())
    fig.suptitle(f"Warming is outside normal variability in {nT} of 12 countries; rainfall change in {nP}",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Grey bands: ±1σ and ±2σ of ordinary year-to-year variation (detrended SD, 1961-2025). Filled = beyond 2σ. " + SRC)
    return save(fig, "slide_06_signal_noise.png")


def slide_seasons(s):
    seas = ["DJF", "MAM", "JJA", "SON"]
    M = np.zeros((12, 4)); SE = np.zeros_like(M)
    for i, c in enumerate(ORDER):
        for j, se in enumerate(seas):
            d = s[(s.country_code == c) & (s.season == se) & s.year.between(1961, 2025)]
            M[i, j] = d.loc[d.year.between(2016, 2025), "temp_anom"].mean() - d.loc[d.year.between(1961, 1990), "temp_anom"].mean()
            SE[i, j] = detrended_sd(d, "temp_anom") * np.sqrt(1 / 10 + 1 / 30)
    fig, ax = plt.subplots(figsize=(W, H))
    im = ax.imshow(M.T, cmap="Reds", vmin=0, vmax=np.ceil(M.max() * 2) / 2, aspect="auto")
    nsig = 0
    for i in range(12):
        jmax, jmin = M[i].argmax(), M[i].argmin()
        sig = M[i, jmax] - M[i, jmin] > 2 * np.hypot(SE[i, jmax], SE[i, jmin])
        nsig += sig
        for j in range(4):
            ax.text(i, j, f"{M[i, j]:+.1f}", ha="center", va="center", fontsize=14,
                    color="white" if M[i, j] > M.max() * .6 else INK, fontweight="bold" if sig and j == jmax else "normal")
        if sig:
            ax.add_patch(Rectangle((i - .47, jmax - .47), .94, .94, fill=False, ec=INK, lw=2.5))
    ax.set_xticks(range(12)); ax.set_xticklabels([NAMES[c] for c in ORDER], rotation=30, ha="right")
    ax.set_yticks(range(4)); ax.set_yticklabels(["Dec-Feb", "Mar-May", "Jun-Aug", "Sep-Nov"])
    for x in [2.5, 5.5, 8.5]:
        ax.axvline(x, color="white", lw=4)
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02, label="°C")
    fig.suptitle(f"Seasons: the fastest season is significantly ahead of the slowest in {nsig} of 12 countries",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Warming 2016-2025 vs 1961-1990 by calendar season. Box = gap fastest-slowest > 2 SE. Brazil, South Africa, Australia: Jun-Aug is winter. " + SRC)
    return save(fig, "slide_07_seasons.png")


def slide_method(m, a):
    """Teach the method on one country: raw monthly series -> anomalies -> change vs noise."""
    fr_m = m[(m.country_code == "FRA") & m.year.between(1961, 2025)].copy()
    fr_m["t"] = fr_m.year + (fr_m.month - 0.5) / 12
    fr = a[(a.country_code == "FRA") & a.year.between(1961, 2025)].sort_values("year")
    fr_all = m[m.country_code == "FRA"]
    share = 1 - fr_all.temp_anom.var() / fr_all.temp.var()   # full record, as in the paper
    b = np.polyfit(fr.year, fr.temp_anom, 1)
    trend = np.polyval(b, fr.year)
    sd = (fr.temp_anom - trend).std(ddof=1)
    delta = fr.loc[fr.year.between(2016, 2025), "temp_anom"].mean()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(W, H), gridspec_kw={"wspace": 0.18, "width_ratios": [1, 1.25]})
    ax1.plot(fr_m.t, fr_m.temp, color=MUTED, lw=0.6)
    ax1.set_title("1. Raw monthly temperature", loc="left", fontsize=16, fontweight="bold")
    ax1.set_ylabel("°C")
    ax1.set_ylim(fr_m.temp.min() - 1, fr_m.temp.max() + 8)
    ax1.text(0.02, 0.98, f"The seasonal cycle is {share:.0%} of the\nvariance: a mild January still looks\ncolder than a cool July",
             transform=ax1.transAxes, va="top", fontsize=12.5, color=INK)

    cols = [WARM if v > 0 else COOL for v in fr.temp_anom]
    ax2.axvspan(1960.5, 1990.5, color="#eaeef2", zorder=0)
    ax2.fill_between(fr.year, trend - sd, trend + sd, color="#d0d7de", alpha=0.8, lw=0, zorder=1, label="±1σ around the trend")
    ax2.bar(fr.year, fr.temp_anom, color=cols, width=0.8, alpha=0.9, zorder=2)
    ax2.plot(fr.year, trend, color=INK, lw=1.5)
    ax2.axhline(0, color=INK, lw=0.8)
    ax2.text(1975.5, -1.45, "baseline 1961-1990 (mean = 0)", ha="center", fontsize=12, color=MUTED)
    ax2.annotate("", xy=(2026.8, delta), xytext=(2026.8, 0), arrowprops=dict(arrowstyle="<->", color=INK, lw=2))
    ax2.plot([2015.6, 2025.4], [delta, delta], color=INK, lw=2.5)
    ax2.text(2006, 2.5, f"Δ = +{delta:.2f} °C (mean 2016-2025)", ha="center", fontsize=13, fontweight="bold", zorder=3)
    ax2.text(1993, -0.3, f"σ = {sd:.2f} °C: how far an ordinary\nyear strays from the trend\n"
                         f"signal-to-noise = Δ / σ = {delta / sd:.1f}", fontsize=13, va="top", color=INK)
    ax2.set_ylim(-1.7, 2.75)
    ax2.set_xlim(1959, 2029)
    ax2.set_title("2. Annual anomaly vs 1961-1990: change vs noise", loc="left", fontsize=16, fontweight="bold")
    ax2.set_ylabel("°C relative to 1961-1990")
    ax2.legend(frameon=False, fontsize=11.5, loc="lower right")
    fig.suptitle("Method in one picture (France): remove the seasons, then compare the change with the noise",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Anomaly = month minus the same calendar month's 1961-1990 mean; annual = day-weighted mean. "
                "σ = SD of the detrended annual anomaly 1961-2025. " + SRC)
    return save(fig, "slide_04_method.png")


def slide_events():
    t = pd.read_csv(os.path.join(TABLES, "table5_landmark_years.csv"))
    t = t[t.Shock.str.startswith("Hottest")].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(W, H))
    y = np.arange(len(t))
    ax.barh(y + .2, t["Crop growth vs normal (pp)"], height=.38, color=CROP, label="Crop production growth")
    ax.barh(y - .2, t["Growth vs normal (pp)"], height=.38, color=INK, label="GDP per capita growth")
    ax.set_yticks(y); ax.set_yticklabels([f"{r.Country} {r.Year}" for r in t.itertuples()])
    ax.axvline(0, color=MUTED, lw=1)
    ax.set_xlabel("Deviation from what the country and the year would predict (percentage points)")
    ax.legend(frameon=False, fontsize=13, loc="lower left")
    ax.invert_yaxis()
    fig.suptitle("Each country's hottest season: the big crop losses came when heat met drought",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Hottest = largest detrended hot-season temperature z-score 1961-2025. Growth two-way demeaned. "
                "World Bank WDI; " + SRC)
    return save(fig, "slide_08_hottest_years.png")


def slide_coefs():
    raw = pd.read_csv(os.path.join(PROC, "regression_results_raw.csv"))
    raw = raw[raw.Dependent == "gdp_per_capita_growth"].iloc[::-1].reset_index(drop=True)
    # The designed deck shows the p-values in cards beside the chart, so its version is narrower and larger
    fig, ax = plt.subplots(figsize=(9.2, 6.6) if CLEAN else (W, H))
    n = len(raw)
    ax.axhspan(n - 2.5, n - 0.5, color="#ECE8DF" if CLEAN else "#f6f8fa", zorder=0)
    for i, r in raw.iterrows():
        x = r.temp_var
        col = WARM if r.Model.startswith("(4)") else (MUTED if r.Model.startswith(("(1)", "(2)")) else INK)
        ax.plot([r[f"ci_lo_{x}"], r[f"ci_hi_{x}"]], [i, i], color=col, lw=6 if CLEAN else 5, solid_capstyle="round")
        ax.plot(r[f"b_{x}"], i, "o", color=col, ms=16 if CLEAN else 14)
        if not CLEAN:
            ax.text(1.01, i, f"p = {r[f'p_{x}']:.2f}  (bootstrap {r[f'pwild_{x}']:.2f})", transform=ax.get_yaxis_transform(),
                    va="center", fontsize=12.5, color=col)
    ax.axvline(0, color=INK, lw=1.2)
    ax.set_yticks(range(n)); ax.set_yticklabels(raw.Model, fontsize=17 if CLEAN else 15)
    ax.tick_params(axis="x", labelsize=16 if CLEAN else 15)
    ax.text(0.01, n - 0.55, "naive: no year effects", transform=ax.get_yaxis_transform(), fontsize=15 if CLEAN else 12,
            color=MUTED, va="top")
    ax.set_xlabel("Growth change for a +1 °C warmer year (pp), 95% CI" if CLEAN else
                  "Change in GDP per capita growth for a +1 °C warmer year (percentage points), 95% CI",
                  fontsize=17 if CLEAN else 15)
    fig.suptitle("The 'climate penalty' disappears once we remove everything that is not weather",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Panel regressions, 12 countries, 1961-2025 (756 country-years). SE clustered by country, t(11) and wild cluster "
                "bootstrap p-values. Red = preferred model: country and year effects + country trends. World Bank WDI; " + SRC)
    return save(fig, "slide_09_coefficients.png")


def twoway_resid(d, col, control):
    X = pd.concat([pd.get_dummies(d.country_code, dtype=float), pd.get_dummies(d.year, dtype=float),
                   d[[control]].astype(float)], axis=1).values
    return d[col].values - X @ np.linalg.lstsq(X, d[col].values, rcond=None)[0]


def slide_crops_rain(p):
    raw = pd.read_csv(os.path.join(PROC, "regression_results_raw.csv")).set_index("Model")
    p = p.copy()
    p["precip_10"] = p.precip_anom_pct / 10.0
    fig, axes = plt.subplots(1, 2, figsize=(W, H), gridspec_kw={"wspace": 0.22})
    panels = [(axes[0], "gdp_per_capita_growth", "temp_anom", "precip_10", "(3) Two-way FE", WARM,
               "Warmer than usual (°C)", "GDP per capita growth (pp)", "Heat → GDP", "pp per °C"),
              (axes[1], "crop_growth", "precip_10", "temp_anom", "(7) Crop growth, two-way FE", WET,
               "Wetter than usual (+10% of normal rain)", "Crop production growth (pp)", "Rain → crops", "pp per +10%")]
    for ax, y, x, ctrl, mod, col, xl, yl, title, unit in panels:
        d = p.dropna(subset=[y, x, ctrl]).copy()
        d["ry"], d["rx"] = twoway_resid(d, y, ctrl), twoway_resid(d, x, ctrl)
        ax.scatter(d.rx, d.ry, s=14, color="#8c959f", alpha=0.4, lw=0)
        bm = d.groupby(pd.qcut(d.rx, 10), observed=True)[["rx", "ry"]].mean()
        ax.plot(bm.rx, bm.ry, "s", color=INK, ms=9, label="decile means")
        r = raw.loc[mod]
        xs = np.linspace(d.rx.quantile(0.01), d.rx.quantile(0.99), 50)
        ax.fill_between(xs, r[f"ci_lo_{x}"] * xs, r[f"ci_hi_{x}"] * xs, color=col, alpha=0.18, lw=0)
        ax.plot(xs, r[f"b_{x}"] * xs, color=col, lw=3.5)
        ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
        ax.set_ylim(np.percentile(d.ry, [1, 99]) * 1.3)
        ax.set_xlabel(xl); ax.set_ylabel(yl)
        ax.set_title(f"{title}: {r[f'b_{x}']:+.2f} {unit}  [{r[f'ci_lo_{x}']:+.2f}, {r[f'ci_hi_{x}']:+.2f}]",
                     loc="left", fontsize=16, fontweight="bold", color=col)
        ax.legend(frameon=False, fontsize=12, loc="lower right")
    fig.suptitle("Where climate shocks bite: rain moves harvests for a year; heat leaves no robust trace in GDP",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Each dot = a country-year 1961-2025 after removing country averages, year averages and the other climate variable. "
                "Line = regression slope with 95% CI (clustered by country). World Bank WDI; " + SRC)
    return save(fig, "slide_10_crops_rain.png")


# ------------------------------------------------------------------------------
# Numbers used in the talk, all read from the generated tables
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    a = pd.read_csv(os.path.join(PROC, "climate_annual.csv"))
    m = pd.read_csv(os.path.join(PROC, "climate_monthly.csv"))
    s = pd.read_csv(os.path.join(PROC, "climate_seasonal.csv"))
    p = pd.read_csv(os.path.join(PROC, "panel.csv"))
    ch = country_changes(a)
    for fn, args in [(slide_map, (ch,)), (slide_route, ()), (slide_method, (m, a)), (slide_stripes, (a,)),
                     (slide_signal, (ch,)), (slide_seasons, (s,)), (slide_events, ()), (slide_coefs, ()),
                     (slide_crops_rain, (p,))]:
        fn(*args)
    deck_stripes(a)
    print("Slide charts:", OUT)



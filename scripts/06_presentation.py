"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 06: PRESENTATION VISUALS (16:9) + POWERPOINT DECK WITH SPEAKER NOTES
================================================================================

Output: presentation/figures/slide_*.png
        presentation/Track1_presentation.pptx   (10 min talk + backup slides)

All numbers on the slides are read from paper/tables and data/processed, so the
deck stays consistent with the paper after any re-run.
"""

import os
import sys
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Rectangle

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


def footer(fig, text):
    import textwrap
    fig.text(0.015, -0.05, textwrap.fill(text, 175), fontsize=10, color=MUTED, va="top")


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    return os.path.join(OUT, name)


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
    fig, axes = plt.subplots(1, 2, figsize=(W, H), sharey=True, gridspec_kw={"wspace": 0.04})
    for ax, col, cmap, lim, title in [(axes[0], "temp_anom", "RdBu_r", 2.5, "Temperature anomaly (°C)"),
                                      (axes[1], "precip_anom_pct", "BrBG", 50, "Rainfall anomaly (% of normal)")]:
        M = a.pivot(index="country_code", columns="year", values=col).reindex(index=ORDER, columns=years)
        im = ax.imshow(M.values, aspect="auto", cmap=cmap, norm=TwoSlopeNorm(0, -lim, lim),
                       extent=[years[0] - .5, years[-1] + .5, 11.5, -.5], interpolation="nearest")
        for y in [2.5, 5.5, 8.5]:
            ax.axhline(y, color="white", lw=3)
        ax.set_title(title, loc="left", fontsize=17, fontweight="bold")
        ax.set_xticks([1940, 1960, 1980, 2000, 2020])
        fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.045, pad=0.07, aspect=35)
    axes[0].set_yticks(range(12)); axes[0].set_yticklabels([NAMES[c] for c in ORDER])
    fig.suptitle("Every recent year is red. Rainfall has no colour trend: it is noise around the normal",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "One cell = one year, 1940-2025, anomaly vs 1961-1990 (our baseline). " + SRC)
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
    fig.suptitle("In each country's hottest season on record, crops often drop; GDP barely moves",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Hottest = largest detrended hot-season temperature z-score 1961-2025. Growth two-way demeaned. "
                "World Bank WDI; " + SRC)
    return save(fig, "slide_08_hottest_years.png")


def slide_coefs():
    raw = pd.read_csv(os.path.join(PROC, "regression_results_raw.csv"))
    raw = raw[raw.Dependent == "gdp_per_capita_growth"].iloc[::-1].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(W, H))
    n = len(raw)
    ax.axhspan(n - 2.5, n - 0.5, color="#f6f8fa", zorder=0)
    for i, r in raw.iterrows():
        x = r.temp_var
        col = WARM if r.Model.startswith("(3)") else (MUTED if r.Model.startswith(("(1)", "(2)")) else INK)
        ax.plot([r[f"ci_lo_{x}"], r[f"ci_hi_{x}"]], [i, i], color=col, lw=5, solid_capstyle="round")
        ax.plot(r[f"b_{x}"], i, "o", color=col, ms=14)
        ax.text(1.01, i, f"p = {r[f'p_{x}']:.2f}  (bootstrap {r[f'pwild_{x}']:.2f})", transform=ax.get_yaxis_transform(),
                va="center", fontsize=12.5, color=col)
    ax.axvline(0, color=INK, lw=1.2)
    ax.set_yticks(range(n)); ax.set_yticklabels(raw.Model)
    ax.text(0.01, n - 0.55, "naive: no year effects", transform=ax.get_yaxis_transform(), fontsize=12, color=MUTED, va="top")
    ax.set_xlabel("Change in GDP per capita growth for a +1 °C warmer year (percentage points), 95% CI")
    fig.suptitle("The 'climate penalty' shrinks as we remove everything that is not weather",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Panel regressions, 12 countries, 1961-2025 (756 country-years). SE clustered by country, t(11) and wild cluster "
                "bootstrap p-values. Red = preferred two-way fixed effects model. World Bank WDI; " + SRC)
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
    fig.suptitle("Where climate shocks really bite: rain moves harvests, heat barely moves GDP",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Each dot = a country-year 1961-2025 after removing country averages, year averages and the other climate variable. "
                "Line = regression slope with 95% CI (clustered by country). World Bank WDI; " + SRC)
    return save(fig, "slide_10_crops_rain.png")


# ------------------------------------------------------------------------------
# Numbers used in the talk, all read from the generated tables
# ------------------------------------------------------------------------------
def talk_numbers(a, m, ch):
    from scipy import stats
    t2 = pd.read_csv(os.path.join(TABLES, "table2_seasonal_change.csv")).set_index("Country")
    t3 = pd.read_csv(os.path.join(TABLES, "table3_regressions.csv")).set_index("Model")
    t4 = pd.read_csv(os.path.join(TABLES, "table4_shock_years.csv"))
    t5 = pd.read_csv(os.path.join(TABLES, "table5_landmark_years.csv"))
    tA = pd.read_csv(os.path.join(TABLES, "table_A1_source_comparison.csv")).set_index("country")
    raw = pd.read_csv(os.path.join(PROC, "regression_results_raw.csv")).set_index("Model")
    fr_m = m[(m.country_code == "FRA") & m.year.between(1961, 2025)]
    fra03 = a[(a.country_code == "FRA") & (a.year == 2003)].iloc[0]
    hot = t5[t5.Shock.str.startswith("Hottest")]
    pick = lambda out, shock: t4[t4.Outcome.str.startswith(out) & t4.Shock.str.startswith(shock) & (t4.Sample == "all years")].iloc[0]
    first = lambda cell: float(str(cell).split(" ")[0])
    lo2 = ch.dT.nsmallest(2).index
    return {
        "lo": ch.dT.min(), "hi": ch.dT.max(), "lo_c": " and ".join(NAMES[c] for c in lo2), "hi_c": NAMES[ch.dT.idxmax()],
        "nT": int((ch.dT > 2 * ch.sT).sum()), "nP": int((ch.dP.abs() > 2 * ch.sP).sum()),
        "snr_mex": ch.loc["MEX", "dT"] / ch.loc["MEX", "sT"], "snr_aus": ch.loc["AUS", "dT"] / ch.loc["AUS", "sT"],
        "snr_deu": ch.loc["DEU", "dT"] / ch.loc["DEU", "sT"], "mex": ch.loc["MEX", "dT"],
        "rho": stats.spearmanr(ch.dT, ch.dP).statistic,
        "share": 1 - m[m.country_code == "FRA"].temp_anom.var() / m[m.country_code == "FRA"].temp.var(),
        "fr_sd": ch.loc["FRA", "sT"], "fr_d": ch.loc["FRA", "dT"],
        "fr_jja": first(t2.loc["France", "JJA"]), "fr_son": first(t2.loc["France", "SON"]),
        "de_djf": first(t2.loc["Germany", "DJF"]),
        "nseas": int((t2["Gap > 2 SE"] == "yes").sum()),
        "seas_c": " and ".join(t2.index[t2["Gap > 2 SE"] == "yes"]),
        "fr03_z": fra03.temp_z, "fr03_hz": fra03.hot_temp_z,
        "fr03_crop": float(hot.loc[hot.Country == "France", "Crop growth vs normal (pp)"].iat[0]),
        "fr03_gdp": float(hot.loc[hot.Country == "France", "Growth vs normal (pp)"].iat[0]),
        "n_crop5": int((hot["Crop growth vs normal (pp)"] < -5).sum()),
        "n_gdp_neg": int((hot["Growth vs normal (pp)"] < 0).sum()),
        "cfe": raw.loc["(2) Country FE"], "tw": raw.loc["(3) Two-way FE"],
        "tr": raw.loc["(4) Two-way FE + country trends"], "crop": raw.loc["(7) Crop growth, two-way FE"],
        "n_obs": int(raw.loc["(3) Two-way FE", "N"]),
        "sd_eff": t3.loc["(3) Two-way FE", "Effect of a 1-SD warm year (pp)"],
        "dry_crop": pick("Crop", "Dry")["Within-country & year gap"],
        "dry_gdp": pick("GDP", "Dry")["Within-country & year gap"],
        "ken_atlas": tA.loc["KEN", "dP_atlas"], "ken_pt": tA.loc["KEN", "dP_blend_point"],
        "usa_atlas": tA.loc["USA", "dP_atlas"], "usa_pt": tA.loc["USA", "dP_blend_point"],
        "med_dP": (tA.dP_blend_point - tA.dP_atlas).abs().median(),
        "med_dT": (tA.dT_blend_point - tA.dT_atlas).abs().median(),
    }


def slides_content(imgs, N):
    """The talk: one list drives both the PowerPoint (visuals + speaker notes) and presentation/SCRIPT.md."""
    tw, cfe, tr, crop = N["tw"], N["cfe"], N["tr"], N["crop"]
    return [
        dict(time="0:00-0:35", who="Speaker 1", kind="title", title="Is today's climate still the one we planned for?",
             sub="Temperature and precipitation records for 12 countries, 1940-2025, and what they did to the economy",
             say="Every plan we make, a harvest, a dam, a heating system, assumes that a normal year looks like "
                 "the normal years we remember. Our question is whether that is still true. We read 85 years of "
                 "temperature and rainfall records for twelve countries, measured how far they have moved, compared "
                 "that with ordinary year-to-year swings, and then asked whether the unusual years were also unusual "
                 "for the economy."),
        dict(time="0:35-1:15", who="Speaker 1", kind="image", img=imgs["map"], title="Twelve countries, one answer",
             say=f"Three countries per continent, chosen to cover temperate Europe, the Mediterranean, the Sahel, "
                 f"East Africa, the monsoon and the Americas, and economies where agriculture is anywhere from one to "
                 f"twenty-three percent of GDP. The headline is already on this map: every one of them is warmer than "
                 f"in 1961 to 1990, from +{N['lo']:.1f} degrees in {N['lo_c']} to +{N['hi']:.2f} in {N['hi_c']}. "
                 f"The rest of the talk asks whether that is large, when in the year it happens, and whether it matters. "
                 f"But first, a question we had to answer before anything else: what is the climate of a country?"),
        dict(time="1:15-2:15", who="Speaker 1", kind="image", img=imgs["route"], title="What does our data measure?",
             say=f"Our first version used a weather API and one grid point at each capital. When we rebuilt the "
                 f"data from the Copernicus Climate Atlas, which averages the ERA5 reanalysis over the whole country, "
                 f"temperature barely moved: the typical gap is {N['med_dT']:.1f} degrees. Rainfall did not survive: the "
                 f"typical gap is {N['med_dP']:.0f} percentage points, the United States goes from +{N['usa_pt']:.0f} percent "
                 f"at Washington to +{N['usa_atlas']:.0f} for the country, and Kenya flips from +{N['ken_pt']:.0f} to "
                 f"{N['ken_atlas']:.0f}. A warm year is warm over hundreds of kilometres; rain is local. So everything "
                 f"from now on is a country average. For France, Germany and Spain the Atlas has country masks; for the "
                 f"others we uploaded the borders into the Atlas's own user-defined region tool, and checked on France "
                 f"that both routes agree to four thousandths of a degree."),
        dict(time="2:15-3:10", who="Speaker 1", kind="image", img=imgs["method"], title="Method",
             say=f"Here is the whole method on one country. On the left, raw monthly temperature: the seasons are "
                 f"{N['share']:.0%} of the variation, so a January cannot be compared with a July. For each calendar "
                 f"month we subtract its average over our baseline, 1961 to 1990. The Atlas gives absolute values, so "
                 f"the baseline is our choice: the WMO reference period, before most of the warming. On the right, the "
                 f"annual result, with two numbers. The change, the last ten years against the baseline: "
                 f"+{N['fr_d']:.2f} degrees. And the noise, sigma, how far an ordinary year strays from the trend: "
                 f"{N['fr_sd']:.2f}. Their ratio, {N['fr_d'] / N['fr_sd']:.1f}, tells us whether the change could pass "
                 f"for a normal year. Above two, it could not."),
        dict(time="3:10-3:50", who="Speaker 1", kind="image", img=imgs["stripes"], title="The full record",
             say="Now all twelve countries, every year since 1940. On the left, temperature: blue before the 1980s, "
                 "red after, and every country-year since 2016 is above its normal. On the right, rainfall, built the "
                 "same way: it flickers between wet and dry, with no colour trend. The 1940s are faded because the "
                 "reanalysis rests on fewer observations then, which is why we measure change from 1961. The next "
                 "slide puts numbers on this contrast."),
        dict(time="3:50-4:50", who="Speaker 1", kind="image", img=imgs["signal"], title="Signal versus noise",
             say=f"Each dot is the change; the grey bands are one and two sigmas of ordinary variation. Temperature is "
                 f"outside two sigma in {N['nT']} of 12 countries. Mexico is the clearest case: +{N['mex']:.1f} degrees "
                 f"is {N['snr_mex']:.1f} sigma, because its temperature barely varies from year to year. Germany warmed "
                 f"more, but its winters are so variable that it is {N['snr_deu']:.1f} sigma. Australia is the exception, at "
                 f"{N['snr_aus']:.1f}. Rainfall: zero of twelve. Kenya and Senegal do show significant drying trends, but "
                 f"the last decade is still within a normal range. And rainfall does not change where warming is "
                 f"largest: the rank correlation across countries is {N['rho']:.2f}."),
        dict(time="4:50-5:35", who="Speaker 1", kind="image", img=imgs["seasons"], title="When in the year",
             say=f"Is the warming spread evenly across the year? Mostly, yes. Only in {N['seas_c']} is one season "
                 f"clearly ahead: there, summer warmed by about +{N['fr_jja']:.1f} degrees against +{N['fr_son']:.1f} "
                 f"in autumn. Germany's winter warmed even more, +{N['de_djf']:.1f}, but German winters vary so much that "
                 f"we cannot call it faster. Summer-heavy warming matters because it lands exactly when crops need water "
                 f"and cities need cooling, which brings us to the economy."),
        dict(time="5:35-6:35", who="Speaker 2", kind="image", img=imgs["events"], title="The hottest summers",
             say=f"So, the last part of the question: were the unusual climate years unusual for the economy? One "
                 f"measurement point first. An annual mean dilutes a heatwave: France's 2003 is only {N['fr03_z']:.1f} "
                 f"sigma as a year, but {N['fr03_hz']:.1f} sigma as a summer. So we use each country's hot season, its "
                 f"three warmest months. Here is every country's hottest one on record, and how growth compared with "
                 f"what the country and the year would predict. Purple is crops, black is GDP. France 2003: crops "
                 f"{N['fr03_crop']:.0f} points, GDP {N['fr03_gdp']:.1f}. In {N['n_crop5']} of 12 cases crops fell by more "
                 f"than five points; GDP fell in only {N['n_gdp_neg']}. These are anecdotes, but they form a pattern, "
                 f"so let us test it."),
        dict(time="6:35-7:50", who="Speaker 2", kind="image", img=imgs["coefs"], title="Testing it",
             say=f"We regress growth on the temperature and rainfall anomalies over all {N['n_obs']} country-years. The "
                 f"grey lines are the naive versions. Comparing each country only with itself, a warmer year costs "
                 f"{abs(cfe['b_temp_anom']):.2f} points, and it looks significant. But that is partly timing: the world "
                 f"warmed while growth slowed after the 1960s. Year effects remove that, because they compare countries "
                 f"within the same year and absorb oil shocks, 2009 and COVID. That is our preferred model, in red: "
                 f"{tw['b_temp_anom']:.2f} points per degree, with an interval from {tw['ci_lo_temp_anom']:.1f} to "
                 f"+{tw['ci_hi_temp_anom']:.2f}. With only twelve countries we check it with a wild bootstrap: p = "
                 f"{tw['pwild_temp_anom']:.2f}. Add country trends and it falls to {tr['b_temp_anom']:.2f}. In words: a "
                 f"typical warm year might cost about {abs(N['sd_eff']):.2f} points of growth, and we cannot tell that "
                 f"apart from zero."),
        dict(time="7:50-8:35", who="Speaker 2", kind="image", img=imgs["rain"], title="Where shocks bite",
             say=f"So where do climate shocks bite? In harvests rather than GDP, and through water rather than heat. On "
                 f"the right, a year ten percent wetter than normal goes with crop growth {crop['b_precip_10']:.1f} points "
                 f"higher, and that estimate is precise. In dry years crop growth is {abs(N['dry_crop']):.1f} points "
                 f"below normal, while GDP growth is only {abs(N['dry_gdp']):.2f} below. The likely reason is exposure: "
                 f"in most of our countries agriculture is one to three percent of GDP. This is the IPCC chain from the "
                 f"course: a hazard becomes a loss only through exposure and vulnerability."),
        dict(time="8:35-9:30", who="Speaker 2", kind="text", title="What we can and cannot conclude",
             bullets=[f"Description (solid): every country has warmed; {N['nT']}/12 beyond normal variability; rainfall change within the noise.",
                      "Correlation: dry years go with lower harvests (clear); warm years with slightly lower GDP growth (not distinguishable from zero).",
                      "Not causal, and not climate change: one unusual year allows no adaptation; 12 countries are too few; national averages hide local losses.",
                      "To make it causal: many more units (all countries, regions), exposure-weighted weather, a channel fixed in advance."],
             say="Let us be precise about what kind of claims these are. The climate results are descriptions, and they "
                 "are solid. The economic results are correlations. Year-to-year weather is close to random, so our "
                 "design is close to an experiment, but twelve countries give intervals too wide to claim a causal "
                 "effect on GDP. And a hot year is not climate change: one unusual year allows no adaptation and no "
                 "build-up of damage. To go further we would need many more units, weather weighted by where crops and "
                 "people are, and a channel chosen before looking at the data."),
        dict(time="9:30-10:00", who="Speaker 2", kind="text", title="Three takeaways",
             bullets=[f"Warming is unmistakable: +{N['lo']:.1f} to +{N['hi']:.2f} °C since 1961-1990, far outside normal variability.",
                      "Rainfall is local and noisy, and it depends on how you measure it.",
                      "Climate shocks reach harvests long before they reach GDP."],
             say="To close: the warming in these records is unmistakable. Rainfall is a different, local story, and one "
                 "that depends on how carefully you measure it. And when the climate misbehaves, the first place it "
                 "shows is the harvest, not GDP. Thank you; we are happy to take questions."),
        dict(time="Q&A", who="Backup", kind="text", title="Backup: data and definitions",
             bullets=["Climate: Copernicus Interactive Climate Atlas (C3S/ECMWF), ERA5, monthly 1940-2025, 288 series. FRA/DEU/ESP: Atlas country masks; 9 others: Atlas user-defined regions with Natural Earth borders (USA = 48 states). Validated on France to 0.004 °C.",
                      "Anomaly = month minus its 1961-1990 calendar-month mean; precipitation = mm/day × days; Δ = mean 2016-2025; σ = SD of the detrended annual anomaly.",
                      "Economy: World Bank WDI, release 8 Oct 2026: GDP per capita growth, crop production index, agriculture share.",
                      "Regressions: two-way fixed effects, SE clustered by country, t(11) + wild cluster bootstrap (Webb weights, 9,999 draws)."],
             say="Use in Q&A only."),
        dict(time="Q&A", who="Backup", kind="text", title="Backup: likely questions",
             bullets=["Why not the API? One grid point is not a country, above all for rainfall.",
                      "Why does the naive model give a big effect? Warming and the growth slowdown both trend over time.",
                      "Is p ≈ 0.1 'no effect'? No: the interval also includes a loss of 1.5 pp per °C.",
                      "Why the hot season? France 2003: 1.2σ as a year, 3.4σ as a summer.",
                      "Why 1961-1990? WMO reference, before most of the warming, and the start of the WDI data."],
             say="Use in Q&A only."),
    ]


def build_deck(slides):
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    blank = prs.slide_layouts[6]
    ink, red, muted = RGBColor(0x1f, 0x23, 0x28), RGBColor(0xc0, 0x39, 0x2b), RGBColor(0x6e, 0x77, 0x81)

    def textbox(s, x, y, w, h, text, size, bold=False, color=ink):
        tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
        tf.word_wrap = True
        tf.text = text
        for p in tf.paragraphs:
            for r in p.runs:
                r.font.size, r.font.bold, r.font.color.rgb = Pt(size), bold, color
        return tf

    def accent(s):
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.18), prs.slide_height)
        bar.fill.solid()
        bar.fill.fore_color.rgb = red
        bar.line.fill.background()

    for k, sl in enumerate(slides, 1):
        s = prs.slides.add_slide(blank)
        if sl["kind"] == "image":
            w, h = Image.open(sl["img"]).size
            scale = min(prs.slide_width / w, prs.slide_height / h)
            pw, ph = int(w * scale), int(h * scale)
            s.shapes.add_picture(sl["img"], (prs.slide_width - pw) // 2, (prs.slide_height - ph) // 2, width=pw, height=ph)
        elif sl["kind"] == "title":
            accent(s)
            textbox(s, 0.9, 2.0, 11.5, 1.6, sl["title"], 40, bold=True)
            textbox(s, 0.9, 3.7, 11.5, 1.0, sl["sub"], 20, color=muted)
            textbox(s, 0.9, 5.4, 11.5, 1.2, "Track 1 · Environmental Economics · ESSEC BSc AIDAMS · 9 November 2026\n"
                    "[Group members]", 16, color=muted)
        else:
            accent(s)
            textbox(s, 0.7, 0.45, 12, 1.0, sl["title"], 34, bold=True)
            body = s.shapes.add_textbox(Inches(0.9), Inches(1.7), Inches(11.6), Inches(5.3)).text_frame
            body.word_wrap = True
            size = 16 if sl["who"] == "Backup" else (22 if len(sl["bullets"]) <= 3 else 19)
            for j, b in enumerate(sl["bullets"]):
                p = body.paragraphs[0] if j == 0 else body.add_paragraph()
                p.text = "▸  " + b
                p.font.size, p.font.color.rgb = Pt(size), ink
                p.space_after = Pt(16)
        if sl["who"] != "Backup":
            textbox(s, 12.5, 7.05, 0.7, 0.4, f"{k}", 11, color=muted)
        s.notes_slide.notes_text_frame.text = f"[{sl['who']} · {sl['time']}]\n\n{sl['say']}"

    out = os.path.join(ROOT, "presentation", "Track1_presentation.pptx")
    prs.save(out)
    return out


def write_script(slides):
    talk = [sl for sl in slides if sl["who"] != "Backup"]
    words = sum(len(sl["say"].split()) for sl in talk)
    lines = [
        "# Talk script: 10 minutes + 3 minutes Q&A (9 November 2026)", "",
        "*Generated by `scripts/06_presentation.py` from the same text as the speaker notes in `Track1_presentation.pptx`; "
        "every number is read from `paper/tables/`. Edit the script there, not here, so slides, notes and paper never diverge.*", "",
        "## The thread", "",
        "Each slide answers the question the previous one raises:", "",
        "1. **Question.** Is today's climate still the one people plan around? And does the economy notice when it is not?",
        "2. **What is a country's climate?** A capital's grid point is not the country, so we rebuilt everything from "
        "Copernicus Atlas country averages. *Raises: how do we measure change?*",
        "3. **Method.** Monthly anomalies against 1961-1990, then change compared with noise (σ). *Raises: what does it show?*",
        "4. **Results.** Warming beyond normal variability almost everywhere; rainfall within the noise; summer leads only in "
        "France and Spain. *Raises: does it matter for the economy?*",
        "5. **Economy.** The hottest summers hit crops, not GDP. Regressions confirm it: heat → GDP is small and imprecise; "
        "rain → crops is clear. *Raises: what kind of claim is that?*",
        "6. **Claims.** Description, correlation or causation, and what would make the result causal.", "",
        f"**Length.** About {words} spoken words, about {words / 140:.0f} minutes at 140 words per minute. Rehearse with a timer.", "",
        "**Roles.**",
        "- Speaker 1 (climate): slides 1-7.",
        "- Speaker 2 (economy): slides 8-12.",
        "- The other three members: the Q&A (see `DEFENSE_NOTES.md`).", "",
        "**Delivery.**",
        "- One number per slide: say it, then point at it.",
        "- Name the type of each result out loud (*description*, *correlation*).",
        "- The handover at slide 8 is the sentence ending slide 7, not a pause.", "",
        "---", "",
    ]
    for k, sl in enumerate(slides, 1):
        lines += [f"### {k}. {sl['title']}  ·  {sl['who']}  ·  {sl['time']}", ""]
        if sl["kind"] == "image":
            lines += [f"![slide {k}](figures/{os.path.basename(sl['img'])})", ""]
        if sl.get("bullets"):
            lines += [f"- {b}" for b in sl["bullets"]] + [""]
        lines += [f"> {sl['say']}", ""]
    with open(os.path.join(ROOT, "presentation", "SCRIPT.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return words


if __name__ == "__main__":
    a = pd.read_csv(os.path.join(PROC, "climate_annual.csv"))
    m = pd.read_csv(os.path.join(PROC, "climate_monthly.csv"))
    s = pd.read_csv(os.path.join(PROC, "climate_seasonal.csv"))
    p = pd.read_csv(os.path.join(PROC, "panel.csv"))
    ch = country_changes(a)
    imgs = {"map": slide_map(ch), "route": slide_route(), "method": slide_method(m, a), "stripes": slide_stripes(a),
            "signal": slide_signal(ch), "seasons": slide_seasons(s), "events": slide_events(),
            "coefs": slide_coefs(), "rain": slide_crops_rain(p)}
    slides = slides_content(imgs, talk_numbers(a, m, ch))
    print("Deck:", build_deck(slides))
    print("Script: presentation/SCRIPT.md,", write_script(slides), "spoken words")



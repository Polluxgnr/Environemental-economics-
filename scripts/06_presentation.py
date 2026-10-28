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
    return save(fig, "slide_01_map.png")


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
    return save(fig, "slide_02_data_route.png")


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
    return save(fig, "slide_03_stripes.png")


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
    return save(fig, "slide_04_signal_noise.png")


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
    return save(fig, "slide_05_seasons.png")


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
    return save(fig, "slide_06_hottest_years.png")


def slide_coefs():
    raw = pd.read_csv(os.path.join(PROC, "regression_results_raw.csv")).iloc[::-1].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(W, H))
    for i, r in raw.iterrows():
        x = r.temp_var
        col = CROP if r.Dependent == "crop_growth" else (WARM if r.Model.startswith("(3)") else INK)
        ax.plot([r[f"ci_lo_{x}"], r[f"ci_hi_{x}"]], [i, i], color=col, lw=4)
        ax.plot(r[f"b_{x}"], i, "o", color=col, ms=12)
    ax.axvline(0, color=INK, lw=1)
    ax.set_yticks(range(len(raw))); ax.set_yticklabels(raw.Model)
    ax.set_xlabel("Effect of a +1 °C warmer year on growth (percentage points), 95% CI")
    fig.suptitle("Once common shocks are removed, the effect of a warm year is small and imprecise",
                 x=0.015, ha="left", fontsize=20, fontweight="bold")
    footer(fig, "Panel regressions, 12 countries 1961-2025, SE clustered by country, t(11). Black: GDP per capita; red: preferred; purple: crops.")
    return save(fig, "slide_07_coefficients.png")


# ------------------------------------------------------------------------------
def build_deck(imgs, ch):
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor

    t1 = pd.read_csv(os.path.join(TABLES, "table1_climate_summary.csv"))
    t3 = pd.read_csv(os.path.join(TABLES, "table3_regressions.csv"))
    raw = pd.read_csv(os.path.join(PROC, "regression_results_raw.csv")).set_index("Model")
    pref = raw.loc["(3) Two-way FE"]
    cfe = raw.loc["(2) Country FE"]
    sd_effect = t3.set_index("Model").loc["(3) Two-way FE", "Effect of a 1-SD warm year (pp)"]
    top = ch.dT.sort_values(ascending=False)
    nT = int((ch.dT > 2 * ch.sT).sum()); nP = int((ch.dP.abs() > 2 * ch.sP).sum())

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    blank = prs.slide_layouts[6]

    def text_slide(title, bullets, notes, size=26):
        s = prs.slides.add_slide(blank)
        tb = s.shapes.add_textbox(Inches(0.6), Inches(0.5), Inches(12), Inches(1.2)).text_frame
        tb.word_wrap = True
        tb.text = title
        tb.paragraphs[0].runs[0].font.size = Pt(34); tb.paragraphs[0].runs[0].font.bold = True
        body = s.shapes.add_textbox(Inches(0.8), Inches(1.9), Inches(11.8), Inches(5)).text_frame
        body.word_wrap = True
        for k, b in enumerate(bullets):
            p = body.paragraphs[0] if k == 0 else body.add_paragraph()
            p.text = b
            p.font.size = Pt(size)
            p.space_after = Pt(14)
        s.notes_slide.notes_text_frame.text = notes
        return s

    def image_slide(img, notes):
        from PIL import Image
        s = prs.slides.add_slide(blank)
        w, h = Image.open(img).size
        scale = min(prs.slide_width / w, prs.slide_height / h)
        pw, ph = int(w * scale), int(h * scale)
        s.shapes.add_picture(img, (prs.slide_width - pw) // 2, (prs.slide_height - ph) // 2, width=pw, height=ph)
        s.notes_slide.notes_text_frame.text = notes
        return s

    s = text_slide("Temperature and precipitation records, 1940-2025",
                   ["What the observed records show for 12 countries, and whether the years that stand out in the "
                    "climate also stand out in the economy",
                    "Track 1 · Environmental Economics · ESSEC BSc AIDAMS · 9 November 2026",
                    "[Group members]"],
                   "Speaker 1 (0:00-0:30). Introduce the group and the question in one sentence.", size=22)

    image_slide(imgs["map"],
                f"Speaker 1 (0:30-1:30). Three countries per continent so that we cover temperate, Mediterranean, "
                f"tropical, monsoon and semi-arid climates. Point at the colours: warming since 1961-1990 ranges from "
                f"+{top.iloc[-1]:.1f} °C ({NAMES[top.index[-1]]}) to +{top.iloc[0]:.1f} °C ({NAMES[top.index[0]]}). "
                f"Data: Copernicus Interactive Climate Atlas, ERA5 reanalysis, averaged over each country; World Bank "
                f"WDI for the economy.")

    image_slide(imgs["route"],
                "Speaker 1 (1:30-2:45). Our first version used an API and one grid point at each capital. When we "
                "re-did it with the Atlas country averages the brief recommends, temperature barely changed, but "
                "rainfall did: Kenya, Mexico, the US change sign or size. Rainfall is local; a single 30 km cell is "
                "not a country. Lesson: check what the data measure before analysing them. Everything that follows "
                "uses country averages.")

    image_slide(imgs["stripes"],
                "Speaker 1 (2:45-3:45). Each row is a country, each cell a year since 1940. We compute monthly "
                "anomalies against our own 1961-1990 baseline (the Atlas gives absolute values), which removes the "
                "seasonal cycle. Left: the last two decades are red everywhere. Right: rainfall alternates wet and dry "
                "without a clear drift. Pre-1950 data rest on fewer observations.")

    image_slide(imgs["signal"],
                f"Speaker 1 (3:45-5:00). Our core description. Change of the last decade against the baseline, "
                f"compared with how much an ordinary year deviates (σ). Temperature: beyond 2σ in {nT} of 12 "
                f"countries, i.e. the recent climate is outside what normal variability would produce. Rainfall: only "
                f"{nP} of 12. Temperature moves most in Europe and Mexico; rainfall moves in different places, and "
                f"mostly not detectably.")

    image_slide(imgs["seasons"],
                "Speaker 2 (5:00-6:00). Is the warming spread evenly across the year? Mostly yes within the noise. "
                "The boxed countries are those where the fastest season is significantly ahead, e.g. summer in "
                "France and Spain. Germany's winter warmed a lot but winters are so variable that the gap is not "
                "significant. Warning: Jun-Aug is winter in the southern hemisphere.")

    image_slide(imgs["events"],
                "Speaker 2 (6:00-7:15). Now the economy. Hot-season temperature catches heatwaves that annual means "
                "dilute: France 2003 is a 3.5σ summer, but only 1.2σ as an annual mean. In the hottest summers, crop "
                "output often falls well below normal; GDP per capita barely moves, because agriculture is a few "
                "percent of GDP in most of our countries.")

    image_slide(imgs["coefs"],
                f"Speaker 2 (7:15-8:30). Panel regression of growth on temperature and rainfall anomalies. Without "
                f"year effects we would report {cfe['b_temp_anom']:+.2f} pp per °C, but warming and the post-1970 "
                f"growth slowdown trend together. With country and year effects (preferred): "
                f"{pref['b_temp_anom']:+.2f} pp per °C, 95% CI [{pref['ci_lo_temp_anom']:+.2f}, "
                f"{pref['ci_hi_temp_anom']:+.2f}], wild bootstrap p = {pref['pwild_temp_anom']:.2f}. A typical warm "
                f"year (1 SD) = {sd_effect:+.2f} pp. 12 countries cannot tell this from zero.")

    text_slide("What we can and cannot conclude",
               [f"Description (solid): every country has warmed; the change exceeds year-to-year noise in {nT}/12. "
                f"Rainfall change is mostly within the noise ({nP}/12 beyond 2σ).",
                "Correlation (weak): unusually warm years go with slightly lower growth and lower crop output, "
                "but 12 countries cannot distinguish this from zero.",
                "Not causal, not climate change: year-to-year weather is not a permanent shift; adaptation and "
                "national aggregation hide local losses. Causality would need sub-national data, many more "
                "countries and a pre-specified exposure channel."],
               "Speaker 2 (8:30-9:30). Be explicit about the type of each result: description, correlation, not "
               "causal. This is what the brief grades.", size=21)

    text_slide("Three takeaways",
               [f"1. Warming is unmistakable: +{top.iloc[-1]:.1f} to +{top.iloc[0]:.1f} °C since 1961-1990, "
                "far outside normal variability.",
                "2. Rainfall is different: local, noisy, and sensitive to how you measure it.",
                "3. Climate shocks show up in crops before they show up in GDP."],
               "Speaker 2 (9:30-10:00). Close, then hand over to the Q&A team.", size=26)

    text_slide("Backup: data and definitions",
               ["Climate: Copernicus Interactive Climate Atlas (C3S/ECMWF), ERA5, monthly 1940-2025. France, Germany, "
                "Spain: Atlas 'European countries' masks; 9 others: Atlas 'user-defined region' with Natural Earth borders "
                "(USA = 48 contiguous states).",
                "Anomalies vs 1961-1990 per calendar month; precipitation = mm/day x days.",
                "Economy: World Bank WDI, release 8 Oct 2026: GDP per capita growth, crop production index, agriculture share.",
                "Regressions: two-way fixed effects, SE clustered by country (t(11)) + wild cluster bootstrap."],
               "Use in Q&A only.", size=18)

    text_slide("Backup: likely questions",
               ["Why not the capital-city API? Rainfall at one point is not the country's rainfall (slide 3).",
                "Why does Country FE give a big effect? Warming and the growth slowdown both trend over time.",
                "Is p ≈ 0.5 'no effect'? No: the CI is wide; we cannot rule out a sizeable effect.",
                "Why hot season? An annual mean dilutes a 2-month heatwave (France 2003: 3.5σ summer, 1.2σ year)."],
               "Use in Q&A only.", size=18)

    out = os.path.join(ROOT, "presentation", "Track1_presentation.pptx")
    prs.save(out)
    return out


if __name__ == "__main__":
    a = pd.read_csv(os.path.join(PROC, "climate_annual.csv"))
    s = pd.read_csv(os.path.join(PROC, "climate_seasonal.csv"))
    ch = country_changes(a)
    imgs = {"map": slide_map(ch), "route": slide_route(), "stripes": slide_stripes(a), "signal": slide_signal(ch),
            "seasons": slide_seasons(s), "events": slide_events(), "coefs": slide_coefs()}
    print("Slides:", build_deck(imgs, ch))

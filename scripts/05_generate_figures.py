"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 05: PAPER FIGURES
================================================================================

Every figure answers one part of the question and carries its own units,
period and source, so it can be read without the text (brief, section 3.4).

  fig1_climate_stripes.png        full record 1940-2025, T and P anomalies, 12 countries
  fig2_signal_vs_noise.png        change 2016-25 vs year-to-year noise, T and P
  fig3_seasonal_heatmap.png       warming by season and country
  fig4_climate_vs_growth.png      warm years vs growth and crop output (within-country, within-year)
  fig5_coefficients.png           temperature coefficient across specifications
  fig6_data_route.png             Atlas country mean vs capital grid point (our first route)
  figA1_levels.png                annual levels, full record (appendix)
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
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)

ORDER = ["FRA", "DEU", "ESP", "KEN", "SEN", "ZAF", "IND", "VNM", "AUS", "USA", "BRA", "MEX"]
NAMES = {"FRA": "France", "DEU": "Germany", "ESP": "Spain", "KEN": "Kenya", "SEN": "Senegal",
         "ZAF": "South Africa", "IND": "India", "VNM": "Vietnam", "AUS": "Australia",
         "USA": "United States", "BRA": "Brazil", "MEX": "Mexico"}
REGION = {"FRA": "Europe", "DEU": "Europe", "ESP": "Europe", "KEN": "Africa", "SEN": "Africa", "ZAF": "Africa",
          "IND": "Asia-Pacific", "VNM": "Asia-Pacific", "AUS": "Asia-Pacific",
          "USA": "Americas", "BRA": "Americas", "MEX": "Americas"}
LAST_DECADE = (2016, 2025)

SRC_ATLAS = "Source: Copernicus Interactive Climate Atlas (C3S/ECMWF), ERA5 country means, accessed 28 Oct 2026."
SRC_WDI = "World Bank WDI (release 8 Oct 2026)."

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
    "figure.dpi": 110, "savefig.dpi": 220, "savefig.bbox": "tight",
})
INK, MUTED, WARM, COOL, WET, DRY = "#1f2328", "#6e7781", "#c0392b", "#2c7fb8", "#1b7f6b", "#a6611a"


def source(fig, text, y=-0.01):
    import textwrap
    width = int(fig.get_figwidth() * 19)
    wrapped = "\n".join(textwrap.fill(part, width) for part in text.split("\n"))
    fig.text(0.01, y, wrapped, fontsize=7, color=MUTED, ha="left", va="top")


def detrended_sd(d, col):
    return (d[col] - np.polyval(np.polyfit(d.year, d[col], 1), d.year)).std(ddof=1)


# ------------------------------------------------------------------------------
def fig1_stripes(a):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True, gridspec_kw={"wspace": 0.05})
    years = np.arange(a.year.min(), a.year.max() + 1)
    base = a[a.year.between(1961, 1990)].groupby("country_code")[["temp", "precip"]].mean()
    for ax, col, cmap, lim, title, unit in [
        (axes[0], "temp_anom", "RdBu_r", 2.5, "Temperature anomaly", "°C"),
        (axes[1], "precip_anom_pct", "BrBG", 50, "Precipitation anomaly", "% of 1961-1990 normal")]:
        M = a.pivot(index="country_code", columns="year", values=col).reindex(index=ORDER, columns=years)
        im = ax.imshow(M.values, aspect="auto", cmap=cmap, norm=TwoSlopeNorm(0, -lim, lim),
                       extent=[years[0] - .5, years[-1] + .5, len(ORDER) - .5, -.5], interpolation="nearest")
        ax.axvspan(1939.5, 1949.5, color="white", alpha=0.35, lw=0)
        ax.add_patch(Rectangle((1960.5, -0.48), 30, len(ORDER) - 0.04, fill=False, ec=INK, lw=0.8, ls="--"))
        for y in [2.5, 5.5, 8.5]:
            ax.axhline(y, color="white", lw=2)
        ax.set_title(f"{title} ({unit})", loc="left")
        ax.set_xticks([1940, 1960, 1980, 2000, 2020])
        cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.05, pad=0.09, aspect=40)
        cb.ax.tick_params(labelsize=7)
    axes[0].set_yticks(range(len(ORDER)))
    axes[0].set_yticklabels([f"{NAMES[c]}  ({base.loc[c, 'temp']:.1f} °C, {base.loc[c, 'precip']:.0f} mm)" for c in ORDER])
    axes[0].text(1976, -0.9, "baseline 1961-1990", fontsize=7, ha="center", color=INK)
    axes[0].text(1945, -0.9, "pre-1950: fewer observations", fontsize=7, ha="center", color=MUTED)
    fig.suptitle("Figure 1. Every country is warmer than its 1961-1990 normal in almost every recent year; rainfall shows no such pattern",
                 x=0.01, ha="left", fontsize=10.5, fontweight="bold", y=1.02)
    source(fig, "Each cell is one year, 1940-2025. Labels give the 1961-1990 mean annual temperature and rainfall. "
                "Anomalies relative to 1961-1990 (our baseline; the Atlas returns absolute values). " + SRC_ATLAS, y=0.0)
    fig.savefig(os.path.join(FIG, "fig1_climate_stripes.png"))
    plt.close(fig)


# ------------------------------------------------------------------------------
def fig2_signal_noise(a):
    d = a[a.year.between(1961, 2025)]
    rows = []
    for c in ORDER:
        dc = d[d.country_code == c]
        rows.append({"c": c, "dT": dc.loc[dc.year.between(*LAST_DECADE), "temp_anom"].mean(), "sT": detrended_sd(dc, "temp_anom"),
                     "dP": dc.loc[dc.year.between(*LAST_DECADE), "precip_anom_pct"].mean(), "sP": detrended_sd(dc, "precip_anom_pct")})
    t = pd.DataFrame(rows).sort_values("dT").reset_index(drop=True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, dcol, scol, color, unit, title in [
        (axes[0], "dT", "sT", WARM, "°C", "Temperature"), (axes[1], "dP", "sP", WET, "% of normal", "Precipitation")]:
        for i, r in t.iterrows():
            ax.add_patch(Rectangle((-2 * r[scol], i - 0.32), 4 * r[scol], 0.64, color="#d0d7de", lw=0))
            ax.add_patch(Rectangle((-r[scol], i - 0.32), 2 * r[scol], 0.64, color="#afb8c1", lw=0))
            out = abs(r[dcol]) > 2 * r[scol]
            c = (color if r[dcol] > 0 else (COOL if dcol == "dT" else DRY)) if out else "white"
            ax.plot(r[dcol], i, "o", ms=7, mfc=c, mec=color if r[dcol] > 0 or dcol == "dT" else DRY, mew=1.5, zorder=3)
            ax.text(r[dcol] + (0.06 if dcol == "dT" else 2.5) * (1 if r[dcol] >= 0 else -1), i,
                    f"{r[dcol]:+.1f}" + (f"  ({r[dcol] / r[scol]:.1f}σ)"), va="center",
                    ha="left" if r[dcol] >= 0 else "right", fontsize=7.5, color=INK)
        ax.axvline(0, color=INK, lw=0.8)
        ax.set_xlabel(f"Change, mean 2016-2025 minus 1961-1990 ({unit})")
        ax.set_title(title, loc="left")
    lim = max(t.dP.abs().max(), 2 * t.sP.max()) * 1.35
    axes[1].set_xlim(-lim, lim)
    axes[0].set_xlim(-2 * t.sT.max() - 0.2, t.dT.max() + 1.0)
    axes[0].set_yticks(range(len(t)))
    axes[0].set_yticklabels([NAMES[c] for c in t.c])
    axes[0].set_ylim(-0.7, len(t) - 0.3)
    fig.suptitle("Figure 2. Warming stands far outside normal year-to-year variation everywhere; rainfall change mostly does not",
                 x=0.01, ha="left", fontsize=10.5, fontweight="bold", y=1.0)
    source(fig, "Dots: change in the 10-year mean. Dark band: ±1σ, light band: ±2σ, where σ is the SD of the detrended annual "
                "anomaly 1961-2025 (one ordinary year's deviation). Filled dot = change larger than 2σ; open dot = within 2σ. "
                + SRC_ATLAS, y=-0.02)
    fig.savefig(os.path.join(FIG, "fig2_signal_vs_noise.png"))
    plt.close(fig)


# ------------------------------------------------------------------------------
def fig3_seasons(s, a):
    seas = ["DJF", "MAM", "JJA", "SON"]
    M = np.zeros((len(ORDER), 4)); SE = np.zeros_like(M)
    for i, c in enumerate(ORDER):
        for j, se in enumerate(seas):
            d = s[(s.country_code == c) & (s.season == se) & s.year.between(1961, 2025)]
            sd = detrended_sd(d, "temp_anom")
            M[i, j] = d.loc[d.year.between(*LAST_DECADE), "temp_anom"].mean() - d.loc[d.year.between(1961, 1990), "temp_anom"].mean()
            SE[i, j] = sd * np.sqrt(1 / 10 + 1 / 30)
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    im = ax.imshow(M, cmap="Reds", vmin=0, vmax=np.ceil(M.max() * 2) / 2, aspect="auto")
    for i in range(len(ORDER)):
        jmax, jmin = M[i].argmax(), M[i].argmin()
        sig = M[i, jmax] - M[i, jmin] > 2 * np.hypot(SE[i, jmax], SE[i, jmin])
        for j in range(4):
            ax.text(j, i, f"{M[i, j]:+.1f}\n±{2 * SE[i, j]:.1f}", ha="center", va="center", fontsize=7.2,
                    color="white" if M[i, j] > M.max() * 0.6 else INK,
                    fontweight="bold" if (sig and j == jmax) else "normal")
            if sig and j == jmax:
                ax.add_patch(Rectangle((j - .48, i - .48), .96, .96, fill=False, ec=INK, lw=1.6))
    hemi = {"ZAF": " (S)", "AUS": " (S)", "BRA": " (S)", "KEN": " (eq.)"}
    ax.set_yticks(range(len(ORDER))); ax.set_yticklabels([NAMES[c] + hemi.get(c, "") for c in ORDER])
    ax.set_xticks(range(4)); ax.set_xticklabels(["Dec-Feb", "Mar-May", "Jun-Aug", "Sep-Nov"])
    ax.xaxis.tick_top()
    for y in [2.5, 5.5, 8.5]:
        ax.axhline(y, color="white", lw=2.5)
    fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02, label="Warming (°C)")
    ax.set_title("Figure 3. Some seasons warm faster than others,\nbut in only a few countries is the gap larger than the noise",
                 loc="left", fontsize=10, pad=28)
    source(fig, "Cells: mean anomaly 2016-2025 minus 1961-1990 (°C) ± 2 SE. Box and bold: the fastest season is warming\n"
                "significantly faster than the slowest (gap > 2 SE). (S) southern hemisphere: Jun-Aug is winter.\n" + SRC_ATLAS, y=0.02)
    fig.savefig(os.path.join(FIG, "fig3_seasonal_heatmap.png"))
    plt.close(fig)


# ------------------------------------------------------------------------------
def twoway_resid(d, col):
    """Residual after country FE, year FE and the precipitation anomaly (Frisch-Waugh-Lovell),
    so the slope of the residual scatter equals the regression coefficient in Table 3."""
    X = pd.concat([pd.get_dummies(d.country_code, dtype=float), pd.get_dummies(d.year, dtype=float),
                   d[["precip_anom_pct"]].astype(float)], axis=1).values
    return d[col].values - X @ np.linalg.lstsq(X, d[col].values, rcond=None)[0]


def fig4_economy(p, raw):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"wspace": 0.25})
    for ax, y, x, lab, mod, ylab in [
        (axes[0], "gdp_per_capita_growth", "temp_anom", "annual temperature", "(3) Two-way FE", "GDP per capita growth (pp)"),
        (axes[1], "crop_growth", "hot_temp_anom", "hot-season temperature", "(8) Crop growth, hot-season T", "Crop production growth (pp)")]:
        d = p.dropna(subset=[y, x, "precip_anom_pct"]).copy()
        d["ry"], d["rx"] = twoway_resid(d, y), twoway_resid(d, x)
        ax.scatter(d.rx, d.ry, s=8, color="#8c959f", alpha=0.45, lw=0)
        zcol = "temp_z" if x == "temp_anom" else "hot_temp_z"
        hot = d[d[zcol] > 1.5]
        ax.scatter(hot.rx, hot.ry, s=18, color=WARM, alpha=0.9, lw=0, label="shock year (z > 1.5)")
        bins = pd.qcut(d.rx, 10)
        bm = d.groupby(bins, observed=True)[["rx", "ry"]].mean()
        ax.plot(bm.rx, bm.ry, "s", color=INK, ms=5, label="decile means")
        r = raw[raw.Model == mod].iloc[0]
        xs = np.linspace(d.rx.quantile(0.01), d.rx.quantile(0.99), 50)
        ax.plot(xs, r[f"b_{x}"] * xs, color=WARM, lw=2)
        ax.fill_between(xs, r[f"ci_lo_{x}"] * xs, r[f"ci_hi_{x}"] * xs, color=WARM, alpha=0.12, lw=0)
        ax.axhline(0, color=MUTED, lw=0.6); ax.axvline(0, color=MUTED, lw=0.6)
        ax.set_ylim(np.percentile(d.ry, [0.5, 99.5]) * 1.25)
        ax.set_xlabel(f"Unusually warm {lab} (°C)\nvs the country's and the year's average")
        ax.set_ylabel(ylab)
        ax.set_title(f"slope {r[f'b_{x}']:+.2f} pp/°C, 95% CI [{r[f'ci_lo_{x}']:+.2f}, {r[f'ci_hi_{x}']:+.2f}]",
                     loc="left", fontsize=9, fontweight="normal")
        ax.legend(frameon=False, fontsize=7, loc="lower left")
    fig.suptitle("Figure 4. Unusually warm years go with slightly lower growth, but the relationship is weak and imprecise",
                 x=0.01, ha="left", fontsize=10.5, fontweight="bold", y=1.03)
    source(fig, "Each dot is a country-year, 1961-2025, after removing country and year averages (two-way fixed effects). "
                "Line: regression slope with 95% CI (clustered by country, t(11)).\n" + SRC_ATLAS + " " + SRC_WDI, y=-0.04)
    fig.savefig(os.path.join(FIG, "fig4_climate_vs_growth.png"))
    plt.close(fig)


# ------------------------------------------------------------------------------
def fig5_coefficients(raw):
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    raw = raw.iloc[::-1].reset_index(drop=True)
    for i, r in raw.iterrows():
        x = r.temp_var
        crop = r.Dependent == "crop_growth"
        col = "#7a5195" if crop else (WARM if r.Model.startswith("(3)") else INK)
        ax.plot([r[f"ci_lo_{x}"], r[f"ci_hi_{x}"]], [i, i], color=col, lw=2)
        ax.plot(r[f"b_{x}"], i, "o", color=col, ms=6)
        pw = r.get(f"pwild_{x}", np.nan)
        ax.text(1.02, i, f"p = {r[f'p_{x}']:.2f} / {pw:.2f}", transform=ax.get_yaxis_transform(), va="center", fontsize=7.5, color=MUTED)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_yticks(range(len(raw))); ax.set_yticklabels(raw.Model)
    ax.set_xlabel("Effect of a +1 °C anomaly on annual growth (percentage points), 95% CI")
    ax.text(1.02, len(raw) - 0.3, "p: t(11) / wild\nbootstrap", transform=ax.get_yaxis_transform(), fontsize=7, color=MUTED, va="bottom")
    ax.set_title("Figure 5. Only the naive models give a precise penalty;\nwith year effects every interval includes zero or almost does",
                 loc="left", fontsize=10)
    source(fig, "GDP per capita growth (black, preferred specification in red) and crop production growth (purple), 12 countries, "
                "1961-2025.\nCluster-robust 95% CI with t(11). " + SRC_ATLAS + " " + SRC_WDI, y=-0.02)
    fig.savefig(os.path.join(FIG, "fig5_coefficients.png"))
    plt.close(fig)


# ------------------------------------------------------------------------------
def fig6_route():
    t = pd.read_csv(os.path.join(TABLES, "table_A1_source_comparison.csv")).set_index("country").reindex(ORDER)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.3), sharey=True, gridspec_kw={"wspace": 0.08})
    styles = [("atlas", "Atlas: country average (now used)", "o", INK, 7),
              ("era5_point", "Capital grid cell, ERA5", "D", "#2c7fb8", 5),
              ("blend_point", "Capital grid cell, Open-Meteo default (our first version)", "x", "#e66101", 7)]
    for ax, v, unit, title in [(axes[0], "dT", "°C", "Temperature change"), (axes[1], "dP", "%", "Precipitation change")]:
        for i, c in enumerate(ORDER):
            vals = [t.loc[c, f"{v}_{s}"] for s, *_ in styles]
            ax.plot([min(vals), max(vals)], [i, i], color="#d0d7de", lw=4, solid_capstyle="round", zorder=1)
            for s, lab, mk, col, ms in styles:
                ax.plot(t.loc[c, f"{v}_{s}"], i, mk, color=col, ms=ms, mew=2, label=lab if i == 0 else None, zorder=2)
        ax.axvline(0, color=MUTED, lw=0.7)
        ax.set_xlabel(f"Mean 2014-2023 minus 1961-1990 ({unit})")
        ax.set_title(title, loc="left")
    axes[0].set_yticks(range(len(ORDER))); axes[0].set_yticklabels([NAMES[c] for c in ORDER]); axes[0].invert_yaxis()
    axes[0].legend(frameon=False, fontsize=7.5, loc="lower right")
    fig.suptitle("Figure 6. A single grid point is not a country: rainfall changes, and even the sign, depend on the data route",
                 x=0.01, ha="left", fontsize=10.5, fontweight="bold", y=1.0)
    source(fig, "Same definitions for all three routes, common period 1961-2023. Open-Meteo Historical Weather API (best_match "
                "and models=era5), accessed Oct 2026; " + SRC_ATLAS.replace("Source: ", ""), y=-0.01)
    fig.savefig(os.path.join(FIG, "fig6_data_route.png"))
    plt.close(fig)


# ------------------------------------------------------------------------------
def figA1_levels(a):
    fig, axes = plt.subplots(4, 6, figsize=(12, 7.5), sharex=True)
    for k, c in enumerate(ORDER):
        d = a[a.country_code == c].sort_values("year")
        axT, axP = axes[k // 3, (k % 3) * 2], axes[k // 3, (k % 3) * 2 + 1]
        for ax, col, color, unit in [(axT, "temp", WARM, "°C"), (axP, "precip", WET, "mm")]:
            ax.plot(d.year, d[col], color=color, lw=0.7, alpha=0.6)
            ax.plot(d.year, d[col].rolling(11, center=True, min_periods=6).mean(), color=color, lw=1.8)
            ax.tick_params(labelsize=6.5)
            ax.set_title(f"{NAMES[c]}, {'temperature' if col == 'temp' else 'precipitation'} ({unit})", fontsize=7.5, loc="left")
    fig.suptitle("Figure A1. Annual mean temperature and annual total precipitation, 1940-2025 (thin: annual; thick: 11-year centred mean)",
                 x=0.01, ha="left", fontsize=10, fontweight="bold")
    fig.tight_layout()
    source(fig, SRC_ATLAS, y=0.0)
    fig.savefig(os.path.join(FIG, "figA1_levels.png"))
    plt.close(fig)


if __name__ == "__main__":
    a = pd.read_csv(os.path.join(PROC, "climate_annual.csv"))
    s = pd.read_csv(os.path.join(PROC, "climate_seasonal.csv"))
    p = pd.read_csv(os.path.join(PROC, "panel.csv"))
    raw = pd.read_csv(os.path.join(PROC, "regression_results_raw.csv"))
    fig1_stripes(a); fig2_signal_noise(a); fig3_seasons(s, a)
    fig4_economy(p, raw); fig5_coefficients(raw); fig6_route(); figA1_levels(a)
    print("Figures written to", FIG)

"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 04: SUMMARY STATISTICS, TRENDS, SEASONS, SHOCK YEARS, PANEL REGRESSIONS
================================================================================

Tables written to paper/tables/ (csv + md):
  table1_climate_summary      per country: baseline level, trend (Newey-West SE),
                              change 2016-2025 vs 1961-1990, noise, signal-to-noise
  table1b_economy_summary     per country: growth, crop growth, agriculture share
  table2_seasonal_change      change by season with standard errors
  table3_regressions          panel regressions, cluster SE + wild cluster bootstrap
  table4_shock_years          growth in shock vs normal years, raw and demeaned
  table5_landmark_years       the largest climate shock in each country and what
                              the economy did that year

Inference with 12 countries: clustered SEs use t(G-1) = t(11) critical values,
and we add wild cluster bootstrap-t p-values (restricted, Webb 6-point weights,
9,999 draws), the small-cluster method of Cameron, Gelbach & Miller (2008) and
Webb (2023).
"""

import os
import sys
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "data", "processed")
TABLES = os.path.join(ROOT, "paper", "tables")
os.makedirs(TABLES, exist_ok=True)

ORDER = ["FRA", "DEU", "ESP", "KEN", "SEN", "ZAF", "IND", "VNM", "AUS", "USA", "BRA", "MEX"]
NAMES = {"FRA": "France", "DEU": "Germany", "ESP": "Spain", "KEN": "Kenya", "SEN": "Senegal",
         "ZAF": "South Africa", "IND": "India", "VNM": "Vietnam", "AUS": "Australia",
         "USA": "United States", "BRA": "Brazil", "MEX": "Mexico"}
LAST_DECADE = (2016, 2025)
WINDOW = (1961, 2025)
rng = np.random.default_rng(20261102)


def save(df, name, title):
    df.to_csv(os.path.join(TABLES, f"{name}.csv"), index=False)
    with open(os.path.join(TABLES, f"{name}.md"), "w", encoding="utf-8") as f:
        f.write(f"{title}\n\n{df.to_markdown(index=False)}\n")


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def hac_trend(y, x, lags=3):
    """OLS trend with Newey-West SE; returns slope per decade and its SE."""
    X = sm.add_constant((np.asarray(x) - np.mean(x)) / 10.0)
    r = sm.OLS(np.asarray(y), X).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return r.params[1], r.bse[1], r.pvalues[1]


# ------------------------------------------------------------------------------
# Table 1: description of each series
# ------------------------------------------------------------------------------
def table1(a, p):
    rows = []
    for c in ORDER:
        d = a[(a.country_code == c) & a.year.between(*WINDOW)]
        base = a[(a.country_code == c) & a.year.between(1961, 1990)]
        out = {"Country": NAMES[c], "Region": d.continent.iat[0]}
        out["T 1961-90 (°C)"] = round(base.temp.mean(), 1)
        bt, st, _ = hac_trend(d.temp_anom, d.year)
        out["T trend (°C/dec)"] = f"{bt:+.2f} ({st:.2f})"
        dT = d.loc[d.year.between(*LAST_DECADE), "temp_anom"].mean()
        resT = d.temp_anom - np.polyval(np.polyfit(d.year, d.temp_anom, 1), d.year)
        out["ΔT 2016-25 (°C)"] = round(dT, 2)
        out["σT (°C)"] = round(resT.std(ddof=1), 2)
        out["SNR T"] = round(dT / resT.std(ddof=1), 1)
        out["P 1961-90 (mm/yr)"] = int(round(base.precip.mean()))
        bp, sp, pp = hac_trend(d.precip_anom_pct, d.year)
        out["P trend (%/dec)"] = f"{bp:+.1f} ({sp:.1f}){stars(pp)}"
        dP = d.loc[d.year.between(*LAST_DECADE), "precip_anom_pct"].mean()
        resP = d.precip_anom_pct - np.polyval(np.polyfit(d.year, d.precip_anom_pct, 1), d.year)
        out["ΔP 2016-25 (%)"] = round(dP, 1)
        out["σP (%)"] = round(resP.std(ddof=1), 1)
        out["SNR P"] = round(dP / resP.std(ddof=1), 1)
        out["Years"] = len(d)
        rows.append(out)
    t = pd.DataFrame(rows)
    save(t, "table1_climate_summary",
         "Table 1. Temperature and precipitation by country, Copernicus Atlas ERA5 country means, 1961-2025. "
         "Trend: OLS slope of the annual anomaly per decade, Newey-West SE (3 lags) in parentheses. "
         "ΔT, ΔP: mean anomaly 2016-2025 relative to the 1961-1990 baseline. σ: SD of the detrended annual anomaly "
         "(year-to-year noise). SNR = Δ/σ. * p<0.10, ** p<0.05, *** p<0.01 for the precipitation trend "
         "(every temperature trend is significant at 1%).")

    rows = []
    for c in ORDER:
        d = p[p.country_code == c]
        g, cg, ag = d.gdp_per_capita_growth.dropna(), d.crop_growth.dropna(), d.agriculture_share_gdp.dropna()
        rows.append({"Country": NAMES[c],
                     "GDPpc growth mean (%)": round(g.mean(), 2), "SD": round(g.std(), 2),
                     "Min": round(g.min(), 1), "Max": round(g.max(), 1), "N": len(g),
                     "Crop growth mean (%)": round(cg.mean(), 1), "Crop SD": round(cg.std(), 1), "N crop": len(cg),
                     "Agri share 2016-25 (% GDP)": round(d.loc[d.year >= 2016, "agriculture_share_gdp"].mean(), 1),
                     "Agri first year": int(d.loc[d.agriculture_share_gdp.notna(), "year"].min())})
    t2 = pd.DataFrame(rows)
    save(t2, "table1b_economy_summary",
         "Table 1b. Economic variables, World Bank WDI (release 2026-10-08), 1961-2025. "
         "Crop growth = annual % change of the crop production index (2014-2016 = 100).")
    return t


# ------------------------------------------------------------------------------
# Table 2: seasonal change with standard errors
# ------------------------------------------------------------------------------
def table2(s):
    rows = []
    for c in ORDER:
        row = {"Country": NAMES[c]}
        vals = {}
        for se_name in ["DJF", "MAM", "JJA", "SON"]:
            d = s[(s.country_code == c) & (s.season == se_name) & s.year.between(*WINDOW)]
            res = d.temp_anom - np.polyval(np.polyfit(d.year, d.temp_anom, 1), d.year)
            sd = res.std(ddof=1)
            last = d.loc[d.year.between(*LAST_DECADE), "temp_anom"]
            basev = d.loc[d.year.between(1961, 1990), "temp_anom"]
            delta = last.mean() - basev.mean()
            se = sd * np.sqrt(1 / len(last) + 1 / len(basev))
            vals[se_name] = (delta, se)
            row[se_name] = f"{delta:+.2f} ({se:.2f})"
        hi = max(vals, key=lambda k: vals[k][0])
        lo = min(vals, key=lambda k: vals[k][0])
        gap = vals[hi][0] - vals[lo][0]
        gap_se = np.hypot(vals[hi][1], vals[lo][1])
        row["Fastest"] = hi
        row["Slowest"] = lo
        row["Gap (°C)"] = f"{gap:.2f} ({gap_se:.2f})"
        row["Gap > 2 SE"] = "yes" if gap > 2 * gap_se else "no"
        rows.append(row)
    t = pd.DataFrame(rows)
    save(t, "table2_seasonal_change",
         "Table 2. Warming by season: mean anomaly 2016-2025 minus 1961-1990 (°C), Copernicus Atlas ERA5. "
         "SE in parentheses = SD of the detrended seasonal anomaly x sqrt(1/10 + 1/30). DJF includes the "
         "previous December. Seasons are calendar seasons: JJA is summer in the north and winter in the south. "
         "The gap compares the fastest and slowest season; the SE of the gap ignores their covariance.")
    return t


# ------------------------------------------------------------------------------
# Regressions
# ------------------------------------------------------------------------------
def design(df, y, xs, year_fe=True, trends=False):
    d = df.dropna(subset=[y] + xs).copy()
    X = d[xs].astype(float)
    X = pd.concat([X, pd.get_dummies(d.country_code, prefix="c", drop_first=True, dtype=float)], axis=1)
    if year_fe:
        X = pd.concat([X, pd.get_dummies(d.year, prefix="y", drop_first=True, dtype=float)], axis=1)
    if trends:
        for c in d.country_code.unique():
            X[f"tr_{c}"] = np.where(d.country_code == c, (d.year - 1990) / 10.0, 0.0)
    X = sm.add_constant(X)
    return d, d[y].astype(float).values, X


def cluster_t(Xv, y, groups, k):
    """OLS beta, CR1 cluster SE for coefficient k."""
    XtX_inv = np.linalg.pinv(Xv.T @ Xv)
    b = XtX_inv @ Xv.T @ y
    u = y - Xv @ b
    meat = np.zeros((Xv.shape[1], Xv.shape[1]))
    for g in np.unique(groups):
        s = Xv[groups == g].T @ u[groups == g]
        meat += np.outer(s, s)
    G, n, kk = len(np.unique(groups)), len(y), Xv.shape[1]
    V = XtX_inv @ meat @ XtX_inv * G / (G - 1) * (n - 1) / (n - kk)
    return b[k], np.sqrt(V[k, k])


def wild_cluster_p(Xv, y, groups, k, B=9999):
    """Restricted wild cluster bootstrap-t (WCR), Webb 6-point weights."""
    b_hat, se_hat = cluster_t(Xv, y, groups, k)
    t_hat = b_hat / se_hat
    Xr = np.delete(Xv, k, axis=1)
    br = np.linalg.lstsq(Xr, y, rcond=None)[0]
    fit_r, u_r = Xr @ br, y - Xr @ br
    gids = np.unique(groups)
    idx = np.searchsorted(gids, groups)
    webb = np.array([-np.sqrt(1.5), -1, -np.sqrt(0.5), np.sqrt(0.5), 1, np.sqrt(1.5)])
    XtX_inv = np.linalg.pinv(Xv.T @ Xv)
    P = XtX_inv @ Xv.T
    G, n, kk = len(gids), len(y), Xv.shape[1]
    scale = G / (G - 1) * (n - 1) / (n - kk)
    ts = np.empty(B)
    for i in range(B):
        w = webb[rng.integers(0, 6, G)][idx]
        ys = fit_r + u_r * w
        b = P @ ys
        u = ys - Xv @ b
        Xu = Xv * u[:, None]
        S = np.zeros((G, kk))
        np.add.at(S, idx, Xu)
        v = (XtX_inv @ (S.T @ S) @ XtX_inv)[k, k] * scale
        ts[i] = b[k] / np.sqrt(v)
    return np.mean(np.abs(ts) >= abs(t_hat))


def regress(df, y, xs, label, year_fe=True, country_fe=True, trends=False, boot=True):
    if country_fe:
        d, yv, X = design(df, y, xs, year_fe, trends)
    else:
        d = df.dropna(subset=[y] + xs).copy()
        yv, X = d[y].astype(float).values, sm.add_constant(d[xs].astype(float))
    Xv, groups = X.values, d.country_code.values
    G = len(np.unique(groups))
    out = {"Model": label, "Dependent": y, "N": len(d), "G": G}
    for j, x in enumerate(xs):
        k = list(X.columns).index(x)
        b, se = cluster_t(Xv, yv, groups, k)
        pt = 2 * stats.t.sf(abs(b / se), G - 1)
        out[f"b_{x}"], out[f"se_{x}"], out[f"p_{x}"] = b, se, pt
        out[f"ci_lo_{x}"] = b - stats.t.ppf(0.975, G - 1) * se
        out[f"ci_hi_{x}"] = b + stats.t.ppf(0.975, G - 1) * se
        if j == 0 and boot:
            out[f"pwild_{x}"] = wild_cluster_p(Xv, yv, groups, k)
    # within R2 of the climate regressors (FWL): share of FE-residual variance explained
    if country_fe:
        _, _, Xfe = design(df, y, [], year_fe, trends)
        Xfe_v = Xfe.values
        ry = yv - Xfe_v @ np.linalg.lstsq(Xfe_v, yv, rcond=None)[0]
        full = yv - Xv @ np.linalg.lstsq(Xv, yv, rcond=None)[0]
        out["within_R2"] = 1 - (full ** 2).sum() / (ry ** 2).sum()
    return out


def table3(p):
    p = p.copy()
    p["precip_10"] = p.precip_anom_pct / 10.0   # per 10 % of normal annual rainfall
    g = "gdp_per_capita_growth"
    specs = [
        ("(1) Pooled OLS", g, ["temp_anom", "precip_10"], dict(country_fe=False)),
        ("(2) Country FE", g, ["temp_anom", "precip_10"], dict(year_fe=False)),
        ("(3) Two-way FE", g, ["temp_anom", "precip_10"], {}),
        ("(4) Two-way FE + country trends", g, ["temp_anom", "precip_10"], dict(trends=True)),
        ("(5) Two-way FE, hot-season T", g, ["hot_temp_anom", "precip_10"], {}),
        ("(6) Two-way FE, excl. 2020-21", g, ["temp_anom", "precip_10"], {}),
        ("(7) Crop growth, two-way FE", "crop_growth", ["temp_anom", "precip_10"], {}),
        ("(8) Crop growth, hot-season T", "crop_growth", ["hot_temp_anom", "precip_10"], {}),
    ]
    res = []
    for label, y, xs, kw in specs:
        data = p[~p.year.isin([2020, 2021])] if "excl. 2020" in label else p
        r = regress(data, y, xs, label, **kw)
        r["temp_var"] = xs[0]
        res.append(r)
        print(f"  {label:34s} b={r['b_' + xs[0]]:+.3f} se={r['se_' + xs[0]]:.3f} "
              f"p_t11={r['p_' + xs[0]]:.3f} p_wild={r.get('pwild_' + xs[0], np.nan):.3f} N={r['N']}")
    raw = pd.DataFrame(res)
    raw.to_csv(os.path.join(PROC, "regression_results_raw.csv"), index=False)

    # Typical size of a temperature shock: within-country SD of the detrended anomaly
    def detrended_sd(col):
        d = p.dropna(subset=[col])
        return d.groupby("country_code").apply(
            lambda g: (g[col] - np.polyval(np.polyfit(g.year, g[col], 1), g.year)).std(), include_groups=False).mean()
    sd_T, sd_hot = detrended_sd("temp_anom"), detrended_sd("hot_temp_anom")

    rows = []
    for r in res:
        x = r["temp_var"]
        sd = sd_T if x == "temp_anom" else sd_hot
        rows.append({
            "Model": r["Model"],
            "Temperature (°C)": f"{r['b_' + x]:+.2f}{stars(r['p_' + x])} ({r['se_' + x]:.2f})",
            "95% CI": f"[{r['ci_lo_' + x]:+.2f}, {r['ci_hi_' + x]:+.2f}]",
            "p t(11)": round(r["p_" + x], 3),
            "p wild bootstrap": round(r.get("pwild_" + x, np.nan), 3),
            "Effect of a 1-SD warm year (pp)": round(r["b_" + x] * sd, 2),
            "Precip (+10% of normal)": f"{r['b_precip_10']:+.2f}{stars(r['p_precip_10'])} ({r['se_precip_10']:.2f})",
            "Within R²": round(r["within_R2"], 3) if "within_R2" in r else "-",
            "N": r["N"],
        })
    t = pd.DataFrame(rows)
    save(t, "table3_regressions",
         "Table 3. Annual growth on annual climate anomalies, 12 countries, 1961-2025. Dependent variable: real GDP "
         "per capita growth (%) in (1)-(6), crop production growth (%) in (7)-(8). Temperature: annual anomaly "
         "relative to 1961-1990 (°C), or the hot-season anomaly (warmest three calendar months) in (5) and (8). "
         "Precipitation: annual anomaly in units of 10% of normal rainfall. Standard errors clustered by country "
         f"(G = 12) in parentheses; stars and CIs use t(11). Wild bootstrap: restricted wild cluster bootstrap-t, "
         f"Webb weights, 9,999 draws. 1-SD warm year: coefficient x average within-country SD of the detrended "
         f"anomaly ({sd_T:.2f} °C annual, {sd_hot:.2f} °C hot season). Within R²: share of the variance left after "
         "the fixed effects that the climate variables explain.")
    return t, raw


# ------------------------------------------------------------------------------
# Table 4: shock years vs normal years
# ------------------------------------------------------------------------------
def demean(d, col):
    """Two-way demeaning on an unbalanced panel via regression on country and year dummies."""
    dd = d.dropna(subset=[col])
    X = pd.concat([pd.get_dummies(dd.country_code, dtype=float), pd.get_dummies(dd.year, dtype=float)], axis=1).values
    resid = dd[col].values - X @ np.linalg.lstsq(X, dd[col].values, rcond=None)[0]
    return pd.Series(resid, index=dd.index)


def table4(p):
    p = p.copy()
    rows = []
    for outcome, oname in [("gdp_per_capita_growth", "GDP per capita growth"), ("crop_growth", "Crop production growth")]:
        p[outcome + "_c"] = p[outcome] - p.groupby("country_code")[outcome].transform("mean")
        p[outcome + "_tw"] = demean(p, outcome)
        for shock, sname in [("shock_heat", "Hot year (annual T, z > 1.5)"),
                             ("shock_hot_season", "Hot season (z > 1.5)"),
                             ("shock_dry", "Dry year (P, z < -1.5)")]:
            for excl in [False, True]:
                d = p[~p.year.isin([2020, 2021])] if excl else p
                d = d.dropna(subset=[outcome])
                n_shock = int(d[shock].sum())
                row = {"Outcome": oname, "Shock": sname, "Sample": "excl. 2020-21" if excl else "all years",
                       "Shock years": n_shock}
                for col, lab in [(outcome, "Raw gap (pp)"), (outcome + "_c", "Within-country gap"),
                                 (outcome + "_tw", "Within-country & year gap")]:
                    gap = d.loc[d[shock] == 1, col].mean() - d.loc[d[shock] == 0, col].mean()
                    row[lab] = round(gap, 2)
                # p-value: regression of two-way demeaned outcome on the shock dummy, clustered by country
                X = sm.add_constant(d[shock].astype(float))
                r = sm.OLS(d[outcome + "_tw"], X).fit(cov_type="cluster", cov_kwds={"groups": d.country_code})
                row["p (cluster, t(11))"] = round(2 * stats.t.sf(abs(r.tvalues[shock]), 11), 3)
                rows.append(row)
    t = pd.DataFrame(rows)
    save(t, "table4_shock_years",
         "Table 4. Growth in climate-shock years minus growth in other years (percentage points), 12 countries, "
         "1961-2025. Shocks are standardised residuals from a country-specific linear trend. Raw gap: simple "
         "difference in means, which mixes fast- and slow-growing countries. Within-country gap: each country "
         "compared with its own average. Within-country & year gap: also removes years that were bad everywhere "
         "(1975, 2009, 2020). p-value from the last column.")
    return t


# ------------------------------------------------------------------------------
# Table 5: biggest shock per country and what the economy did
# ------------------------------------------------------------------------------
def table5(p):
    p = p.copy()
    p["growth_dev"] = demean(p, "gdp_per_capita_growth")
    p["crop_dev"] = demean(p, "crop_growth")
    rows = []
    for c in ORDER:
        d = p[p.country_code == c]
        for kind, col, pick in [("Hottest (hot season)", "hot_temp_z", "max"), ("Driest", "precip_z", "min")]:
            dd = d.dropna(subset=[col])
            i = dd[col].idxmax() if pick == "max" else dd[col].idxmin()
            r = dd.loc[i]
            rows.append({"Country": NAMES[c], "Shock": kind, "Year": int(r.year), "z": round(r[col], 2),
                         "Growth vs normal (pp)": round(r.growth_dev, 1) if pd.notna(r.growth_dev) else None,
                         "Crop growth vs normal (pp)": round(r.crop_dev, 1) if pd.notna(r.crop_dev) else None})
    t = pd.DataFrame(rows)
    save(t, "table5_landmark_years",
         "Table 5. The most extreme hot-season and dry year in each country (detrended z-score, 1961-2025) and the "
         "deviation of growth that year from what the country and the year would predict (two-way demeaned, pp). "
         "WDI data; Copernicus Atlas ERA5.")
    return t


if __name__ == "__main__":
    a = pd.read_csv(os.path.join(PROC, "climate_annual.csv"))
    s = pd.read_csv(os.path.join(PROC, "climate_seasonal.csv"))
    p = pd.read_csv(os.path.join(PROC, "panel.csv"))
    print("Table 1 ..."); print(table1(a, p).to_string(index=False))
    print("Table 2 ..."); print(table2(s).to_string(index=False))
    print("Table 3 (bootstrap takes a minute) ...")
    t3, _ = table3(p); print(t3.to_string(index=False))
    print("Table 4 ..."); print(table4(p).to_string(index=False))
    print("Table 5 ..."); print(table5(p).to_string(index=False))

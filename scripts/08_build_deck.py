"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 08: THE TALK AS A POWERPOINT DECK
================================================================================

Input:  presentation/figures/*.png   (charts drawn by 06_presentation.py)
        presentation/SCRIPT.md       (spoken text, one section per slide)
Output: presentation/Track1_presentation.pptx

12 slides for the 10-minute talk, 16:9. The data definitions and Q&A material are in DEFENSE_NOTES.md.
Each slide's speaker notes hold its part of SCRIPT.md, with speaker and timing.
Fonts are Cambria (titles) and Calibri (text), which ship with every Office.
"""

import os
import re
import sys
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "presentation", "figures")
OUT = os.path.join(ROOT, "presentation", "Track1_presentation.pptx")

NAVY, PAPER, SAND, WHITE = "14213D", "F7F5F0", "ECE8DF", "FFFFFF"
RED, GREEN, PURPLE, BROWN, ORANGE = "B5332A", "1B7F6B", "7A5195", "A6611A", "D9772B"
INK, BODY, MUTED, LINE = "14213D", "4A5568", "6B7280", "D9D4C7"
PINK, PALE, PALER = "E8A598", "C9D3E0", "A9B6C8"
HEAD, TEXT = "Cambria", "Calibri"

SW, SH = 13.333, 7.5        # slide size (in)
X0, CW = 0.75, 11.833       # left margin, content width
TOP = 2.1                   # top of the content area


# ------------------------------------------------------------------------------
# Drawing helpers
# ------------------------------------------------------------------------------
def rgb(h):
    return RGBColor.from_string(h)


def background(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(color)


def box(slide, x, y, w, h, fill=None, line=None, rounded=False, alpha=None, name=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                                 Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded:
        shp.adjustments[0] = 0.06
    if fill:
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(fill)
        if alpha is not None:
            clr = shp.fill._xPr.find(qn("a:solidFill")).find(qn("a:srgbClr"))
            clr.append(clr.makeelement(qn("a:alpha"), {"val": str(int(alpha * 100000))}))
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = rgb(line[0])
        shp.line.width = Pt(line[1])
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    if name:
        shp.name = name
    return shp


def dot(slide, x, y, d, color):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb(color)
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def text(slide, x, y, w, h, paras, size=15, color=BODY, font=TEXT, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, spacing=None, line=1.1, after=0):
    """paras: a string, or a list of paragraphs; a paragraph is a string or a list of (text, {overrides}) runs."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    if isinstance(paras, str):
        paras = [paras]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line
        p.space_after = Pt(after)
        runs = [(para, {})] if isinstance(para, str) else para
        for t, o in runs:
            r = p.add_run()
            r.text = t
            f = r.font
            f.name = o.get("font", font)
            f.size = Pt(o.get("size", size))
            f.bold = o.get("bold", bold)
            f.color.rgb = rgb(o.get("color", color))
            if spacing:
                r._r.get_or_add_rPr().set("spc", str(int(spacing * 100)))
    return tb


def picture(slide, name, x, y, w, h, align="center"):
    """Fit a chart inside the box (x, y, w, h), keeping its aspect ratio."""
    path = os.path.join(FIG, name)
    iw, ih = Image.open(path).size
    s = min(w / iw, h / ih)
    pw, ph = iw * s, ih * s
    px = x + (w - pw) / 2 if align == "center" else x
    return slide.shapes.add_picture(path, Inches(px), Inches(y), Inches(pw), Inches(ph))


def frame(prs, eyebrow, title, footer=None, number=None, bg=PAPER, eyebrow_color=RED):
    """Content slide: eyebrow, title, source line and slide number at fixed positions."""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    background(s, bg)
    text(s, X0, 0.62, CW, 0.3, eyebrow.upper(), size=12, color=eyebrow_color, bold=True, spacing=1.5)
    text(s, X0, 0.95, CW, 1.05, title, size=28, color=INK, font=HEAD, bold=True, line=1.0)
    if footer:
        text(s, X0, 6.92, CW - 0.8, 0.3, footer, size=11, color=MUTED)
    if number:
        text(s, SW - X0 - 0.6, 6.92, 0.6, 0.3, str(number), size=11, color=MUTED, align=PP_ALIGN.RIGHT)
    return s


def card(slide, x, y, w, h, title, body, marker=None, fill=WHITE, line=(LINE, 0.75), tcolor=INK, bcolor=BODY,
         tsize=16, bsize=14):
    box(slide, x, y, w, h, fill=fill, line=line, rounded=True)
    tx = x + 0.25
    if marker:
        dot(slide, tx, y + 0.27, 0.16, marker)
        tx += 0.3
    text(slide, tx, y + 0.18, x + w - tx - 0.2, 0.35, title, size=tsize, color=tcolor, bold=True)
    text(slide, x + 0.25, y + 0.58, w - 0.45, h - 0.7, body, size=bsize, color=bcolor, line=1.1)


def step(slide, x, y, w, h, n, title, body, color=RED):
    box(slide, x, y, w, h, fill=WHITE, line=(LINE, 0.75), rounded=True)
    dot(slide, x + 0.22, y + 0.2, 0.42, color)
    text(slide, x + 0.22, y + 0.2, 0.42, 0.42, str(n), size=15, color=WHITE, bold=True, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE)
    text(slide, x + 0.8, y + 0.22, w - 1.0, 0.4, title, size=16, color=INK, bold=True)
    text(slide, x + 0.8, y + 0.62, w - 1.0, h - 0.7, body, size=13.5, color=BODY, line=1.1)


def stat(slide, x, y, w, number, label, color, nsize=54):
    text(slide, x, y, w, 0.85, number, size=nsize, color=color, font=HEAD, bold=True, line=0.9)
    text(slide, x, y + 0.9, w, 0.75, label, size=14, color=BODY, line=1.1)


# ------------------------------------------------------------------------------
# Speaker notes from SCRIPT.md
# ------------------------------------------------------------------------------
def notes_from_script():
    s = open(os.path.join(ROOT, "presentation", "SCRIPT.md"), encoding="utf-8").read()
    out = {}
    for part in s.split("\n### ")[1:]:
        m = re.match(r"(\d+)\. [^\n]*?  ·  ([^·]+?)  ·  (\S+)", part)
        if not m:
            continue
        lines = part.split("\n")
        say = " ".join(l[2:] for l in lines if l.startswith("> ")).replace("*(handover)* ", "[handover] ")
        point = [l for l in lines if l.startswith("*Point at:*") or l.startswith("*On screen:*")]
        point = point[0].replace("*", "") if point else ""
        out[int(m.group(1))] = f"{m.group(2).strip()} · {m.group(3)}\n\n{say}" + (f"\n\n{point}" if point else "")
    return out


# ------------------------------------------------------------------------------
# The slides
# ------------------------------------------------------------------------------
def build():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(SW), Inches(SH)
    cp = prs.core_properties
    cp.title = "Is today's climate still the one we planned for?"
    cp.author = "Eliott Beghin, Pollux Gronier, Saty Viard Laroque, Augustin Vlandas"
    cp.subject = "Environmental Economics, Track 1, ESSEC BSc AIDAMS, 9 November 2026"
    slides = []

    # 1. Cover: the question, and the three questions the talk answers in order
    s = prs.slides.add_slide(prs.slide_layouts[6])
    background(s, NAVY)
    text(s, X0 + 0.15, 1.35, 6.4, 0.3, "ENVIRONMENTAL ECONOMICS · TRACK 1", size=12, color=PINK, bold=True, spacing=1.5)
    text(s, X0 + 0.15, 1.8, 6.6, 2.2, "Is today’s climate still the one we planned for?", size=42, color=PAPER,
         font=HEAD, bold=True, line=0.95)
    text(s, X0 + 0.15, 3.7, 6.2, 0.8, "Temperature and rainfall records for 12 countries, 1940–2025, and what they "
         "did to the economy", size=16, color=PALE, line=1.15)
    text(s, X0 + 0.15, 4.85, 6.4, 0.6, "Eliott Beghin · Pollux Gronier · Saty Viard Laroque · Augustin Vlandas",
         size=14, color=PAPER, bold=True, line=1.15)
    text(s, X0 + 0.15, 5.5, 6.4, 0.3, "ESSEC BSc AIDAMS · Caterina Seghini · 9 November 2026", size=12, color=PALER)
    qx = 7.85
    qw = SW - X0 - qx
    text(s, qx, 1.35, qw, 0.3, "THREE QUESTIONS", size=12, color=PINK, bold=True, spacing=1.5)
    for i, q in enumerate(["How far has the climate moved?", "Is that large next to normal ups and downs?",
                           "Were the unusual years also unusual for the economy?"]):
        y = 1.8 + i * 1.45
        box(s, qx, y, qw, 1.25, fill="22325A", rounded=True)
        text(s, qx + 0.3, y + 0.15, 0.6, 0.95, str(i + 1), size=36, color=PINK, font=HEAD, bold=True,
             anchor=MSO_ANCHOR.MIDDLE)
        text(s, qx + 1.0, y + 0.15, qw - 1.25, 0.95, q, size=17, color=PAPER, line=1.1, anchor=MSO_ANCHOR.MIDDLE)
    slides.append(s)

    # 2. Our countries
    s = frame(prs, "01 · Our countries", "Our choice: three contrasting countries per continent, and every one is "
              "warmer than in 1961–1990", "Warming = country-average temperature, mean 2016–2025 minus 1961–1990 "
              "(Copernicus Atlas, ERA5) · farming share of GDP: World Bank WDI, 2016–2025 average", 2)
    picture(s, "slide_02_map.png", X0, TOP + 0.35, 8.2, 4.4, align="left")
    rx = 9.25
    rw = SW - X0 - rx
    for i, (region, countries, detail, strong) in enumerate([
            ("EUROPE", "France · Germany · Spain", "temperate, continental, Mediterranean", False),
            ("AFRICA", "Kenya · Senegal · South Africa", "farming: 21 % of GDP in Kenya, 2.5 % in South Africa", True),
            ("ASIA-PACIFIC", "India · Vietnam · Australia", "monsoon, tropical, dry", False),
            ("AMERICAS", "United States · Brazil · Mexico", "temperate, tropical, highland", False)]):
        y = TOP + 0.1 + [0, 1.05, 2.3, 3.35][i]
        text(s, rx, y, rw, 0.25, region, size=11, color=RED, bold=True, spacing=1.2)
        text(s, rx, y + 0.27, rw, 0.3, countries, size=15, color=INK, bold=True)
        text(s, rx, y + 0.6, rw, 0.45, detail, size=13, color=INK if strong else BODY, bold=strong, line=1.05)
    slides.append(s)

    # 3. Our data
    s = frame(prs, "02 · Our data", "A capital is not a country: we use country averages",
              "Change 2014–2023 vs 1961–1990, same definitions · Copernicus Atlas (ERA5) vs Open-Meteo API (default model)", 3)
    picture(s, "slide_03_data_route.png", X0, TOP, 7.3, 4.55, align="left")
    rx = 8.35
    rw = SW - X0 - rx
    card(s, rx, TOP + 0.05, rw, 1.2, "Orange: our first attempt",
         "One point at each capital, from a free weather API", marker=ORANGE)
    card(s, rx, TOP + 1.4, rw, 1.2, "Black: what we use",
         "Copernicus Climate Atlas: ERA5 averaged over each country’s borders", marker=NAVY)
    card(s, rx, TOP + 2.75, rw, 1.65, "Kenya: +11 % vs −13 %",
         "Rainfall at the capital vs the country. Temperature agrees (about 0.2 °C apart); rain is local. Check what "
         "your data measure.", fill=NAVY, line=None, tcolor=PAPER, bcolor=PALE)
    slides.append(s)

    # 4. How we measure change
    s = frame(prs, "03 · How we measure change", "Three steps: remove the seasons, measure the change, compare it "
              "with the noise", "France, 1961–2025 · rainfall gets the same three steps, in % of its 1961–1990 "
              "average · Copernicus Atlas, ERA5", 4)
    picture(s, "slide_04_method.png", X0, TOP + 0.05, 7.75, 4.5, align="left")
    rx = 8.75
    rw = SW - X0 - rx
    step(s, rx, TOP + 0.05, rw, 1.42, 1, "Remove the seasons",
         "Each month minus the same month’s 1961–1990 average = the anomaly")
    step(s, rx, TOP + 1.57, rw, 1.42, 2, "Measure the change Δ", "Last 10 years vs 1961–1990: +1.74 °C")
    step(s, rx, TOP + 3.09, rw, 1.42, 3, "Compare it with the noise σ",
         "Normal swing 0.51 °C, so Δ/σ = 3.4. Above 2: unlike any ordinary year")
    slides.append(s)

    # 5. How far has the climate moved?
    s = frame(prs, "04 · How far has the climate moved?", "Same method, all twelve countries: every recent year is "
              "red, rainfall has no trend", "One cell = one year · both vs 1961–1990: °C, and % of the 1961–1990 "
              "average rain · 1940–60 faded: fewer observations", 5)
    picture(s, "slide_05_stripes.png", X0, TOP - 0.05, 8.6, 4.75, align="left")
    rx = 9.6
    rw = SW - X0 - rx
    stat(s, rx, TOP + 0.35, rw, "120 / 120", "country-years since 2016 warmer than their 1961–1990 normal", RED,
         nsize=40)
    stat(s, rx, TOP + 2.25, rw, "No trend", "in rainfall: drier and wetter years simply alternate", GREEN, nsize=40)
    slides.append(s)

    # 6. Is it large next to normal swings?
    s = frame(prs, "05 · Is it large next to normal swings?", "Warming is far outside normal year-to-year swings; "
              "rainfall changed far less", "σ = SD of the detrended annual anomaly, 1961–2025 · Copernicus Atlas, ERA5", 6)
    picture(s, "slide_06_signal_noise.png", X0, TOP, 7.3, 4.55, align="left")
    rx = 8.45
    rw = SW - X0 - rx
    stat(s, rx, TOP + 0.1, rw, "11 / 12", "countries where warming exceeds one ordinary year’s swing (2σ)", RED)
    stat(s, rx, TOP + 1.85, rw, "0 / 12", "for rainfall, though its 10-year average shifted measurably in Brazil, "
         "India, Kenya, Senegal", GREEN)
    text(s, rx, TOP + 3.65, rw, 0.7, "Rainfall change does not follow the warming (rank correlation −0.42, not "
         "significant with 12 countries)", size=13, color=BODY, line=1.1)
    slides.append(s)

    # 7. Seasons
    s = frame(prs, "06 · When in the year", "Warming is spread evenly across the year, except in France and Spain",
              "Calendar seasons; Jun–Aug is winter in the south · box = gap > 2 SE · Copernicus Atlas, ERA5", 7)
    picture(s, "slide_07_seasons.png", X0, TOP, 7.3, 4.55, align="left")
    rx, rw = 8.35, SW - X0 - 8.35
    card(s, rx, TOP + 0.05, rw, 1.3, "Summer leads", "France and Spain: summer +2.3 to +2.4 °C, autumn +1.3 to "
         "+1.4 °C", marker=RED)
    card(s, rx, TOP + 1.55, rw, 1.3, "Large, but noisy", "German winters +2.5 °C, yet so variable that the gap is "
         "not significant", marker=MUTED)
    text(s, rx, TOP + 3.1, rw, 0.9, "Why it matters: summer heat lands when crops need water and cities need "
         "cooling.", size=14, color=BODY, line=1.1)
    slides.append(s)

    # 8. Hottest summers
    s = frame(prs, "07 · The hottest summers", "In each country’s hottest season, the big crop losses came when heat "
              "met drought", "Growth vs what the country and the year would predict (pp) · World Bank WDI; "
              "Copernicus Atlas, ERA5", 8)
    picture(s, "slide_08_hottest_years.png", X0, TOP + 0.1, 7.4, 4.4, align="left")
    rx, rw = 8.45, SW - X0 - 8.45
    stat(s, rx, TOP + 0.05, rw, "−21", "crop points in France, summer 2003 (GDP: −1.5)", INK)
    card(s, rx, TOP + 1.65, rw, 1.55, "Heat and drought together", "Germany 2003, Australia 2019: hottest and "
         "driest year. France 2003, USA 1988: dry too.", marker=BROWN)
    text(s, rx, TOP + 3.4, rw, 0.6, "Across all hot seasons, crops show no effect on average.", size=14, color=BODY)
    slides.append(s)

    # 9. Testing it
    s = frame(prs, "08 · Testing it", "The “climate penalty” disappears once we remove everything that is not "
              "weather", "756 country-years, 1961–2025 · SE clustered by country, t(11) and wild cluster bootstrap · "
              "WDI; Atlas", 9)
    picture(s, "slide_09_coefficients.png", X0, TOP + 0.1, 7.4, 4.4, align="left")
    rx, rw = 8.45, SW - X0 - 8.45
    box(s, rx, TOP + 0.05, rw, 0.85, fill=SAND, rounded=True)
    text(s, rx + 0.25, TOP + 0.15, rw - 0.4, 0.3, "Naive: country effects only", size=13, color=MUTED, bold=True)
    text(s, rx + 0.25, TOP + 0.45, rw - 0.4, 0.35, "−0.75 pp/°C · p = 0.01", size=16, color=INK, bold=True)
    box(s, rx, TOP + 1.05, rw, 1.15, fill=SAND, rounded=True)
    text(s, rx + 0.25, TOP + 1.15, rw - 0.4, 0.3, "+ year effects", size=13, color=MUTED, bold=True)
    text(s, rx + 0.25, TOP + 1.45, rw - 0.4, 0.35, "−0.67 pp/°C · p = 0.10", size=16, color=INK, bold=True)
    text(s, rx + 0.25, TOP + 1.8, rw - 0.4, 0.3, "fast warmers also slowed most (trends: −0.57)", size=13, color=BODY)
    box(s, rx, TOP + 2.35, rw, 1.15, fill=WHITE, line=(RED, 2), rounded=True)
    text(s, rx + 0.25, TOP + 2.45, rw - 0.4, 0.3, "Preferred: + country trends", size=13, color=RED, bold=True)
    text(s, rx + 0.25, TOP + 2.75, rw - 0.4, 0.35, "−0.04 pp/°C", size=16, color=INK, bold=True)
    text(s, rx + 0.25, TOP + 3.1, rw - 0.4, 0.3, "95% CI [−0.76, +0.69] · bootstrap p = 0.92", size=13, color=BODY)
    text(s, rx, TOP + 3.7, rw, 0.6, "No detectable effect; losses above ~0.8 pp per °C ruled out here.", size=14,
         color=BODY)
    slides.append(s)

    # 10. Where shocks bite
    s = frame(prs, "09 · Where shocks bite", "Rain moves harvests for a year; heat leaves no robust trace in GDP",
              "Each dot: a country-year, after country and year effects (left: + country trends, model 4) · WDI; "
              "Copernicus Atlas, ERA5", 10)
    picture(s, "slide_10_crops_rain.png", X0, TOP - 0.1, CW, 3.95)
    text(s, X0, 6.05, CW, 0.65, [[
        ("+10 % rain: crop output about ", {}), ("2.2 %", {"bold": True, "color": INK}),
        (" higher, robust to dropping any country or adding trends, and it lasts one year. Dry years: crops ", {}),
        ("7.6 points", {"bold": True, "color": INK}), (" below normal, GDP only ", {}),
        ("0.27", {"bold": True, "color": INK}), (".", {})]], size=15, color=BODY, line=1.1)
    slides.append(s)

    # 11. Claims
    s = frame(prs, "10 · What we can and cannot conclude", "Three kinds of claim, three levels of confidence",
              "Paper §6", 11, bg=SAND)
    cw3, gap = (CW - 2 * 0.35) / 3, 0.35
    for i, (label, col, title, body) in enumerate([
            ("DESCRIPTION · SOLID", NAVY, "Every country has warmed",
             "11 of 12 beyond normal variability. Rainfall changed far less (measurable in 4 countries). Summer "
             "leads in France and Spain."),
            ("CORRELATION · MIXED", GREEN, "Harvests clearly; GDP barely",
             "Dry years go with lower crop output for a year. Warm years show no robust link with GDP growth."),
            ("NOT CLAIMED", RED, "Causal effects of climate change",
             "One hot year allows no adaptation. Needed: many more units, exposure-weighted weather, a channel "
             "fixed in advance.")]):
        x = X0 + i * (cw3 + gap)
        box(s, x, TOP + 0.2, cw3, 3.6, fill=WHITE, rounded=True)
        dot(s, x + 0.35, TOP + 0.55, 0.18, col)
        text(s, x + 0.65, TOP + 0.5, cw3 - 0.9, 0.3, label, size=12, color=col, bold=True, spacing=1.2)
        text(s, x + 0.35, TOP + 1.05, cw3 - 0.7, 1.0, title, size=22, color=INK, font=HEAD, bold=True, line=1.0)
        text(s, x + 0.35, TOP + 2.15, cw3 - 0.7, 2.0, body, size=15, color=BODY, line=1.15)
    slides.append(s)

    # 12. The answers
    s = frame(prs, "11 · The answers", "Back to our three questions",
              "Warming 2016–2025 vs 1961–1990 · normal swing = 2σ of the detrended annual anomaly · crop output per "
              "+10 % rain", 12)
    for i, (question, num, col, body) in enumerate([
            ("1 · How far has the climate moved?", "+0.7–1.85 °C", RED, "All 12 countries warmed, from India and Australia (+0.7) to Germany (+1.85)"),
            ("2 · Is that large next to normal swings?", "11 / 12", INK, "Temperature: yes, in 11 of 12 countries. "
             "Rainfall: no, though its average shifted in 4"),
            ("3 · Did the economy notice?", "+2.2 %", PURPLE, "Harvests, for a year, through water (crop output per "
             "+10 % rain). GDP: not detectably")]):
        x = X0 + i * (cw3 + gap)
        text(s, x, TOP + 0.15, cw3 - 0.1, 0.7, question, size=15, color=MUTED, bold=True, line=1.05)
        text(s, x, TOP + 0.9, cw3, 0.85, num, size=40, color=col, font=HEAD, bold=True, line=0.9)
        text(s, x, TOP + 1.85, cw3 - 0.1, 1.4, body, size=16, color=INK, line=1.15)
    text(s, X0, 5.75, CW, 0.5, "For temperature, today’s climate is no longer the one we planned for.", size=22,
         color=INK, font=HEAD, bold=True)
    slides.append(s)

    # Speaker notes
    say = notes_from_script()
    for k, s in enumerate(slides, 1):
        s.notes_slide.notes_text_frame.text = say[k]
    prs.save(OUT)
    return OUT, len(slides), sorted(say)


if __name__ == "__main__":
    out, n, noted = build()
    print(f"Deck: {out} ({n} slides; script notes on slides {noted})")

"""
================================================================================
TRACK 1: TEMPERATURE AND PRECIPITATION RECORDS
SCRIPT 07: RENDER paper/PAPER.md TO paper/PAPER.pdf (A4) WITH HEADLESS CHROME
================================================================================

Markdown -> HTML (python-markdown, tables extension), the display equation is
rendered with matplotlib mathtext, then Chrome/Edge prints the page to PDF.
Pass the browser path as an argument if it is not found automatically.
"""

import os
import re
import sys
import shutil
import subprocess
sys.stdout.reconfigure(encoding="utf-8")
import markdown
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(ROOT, "paper")

CSS = """
@page { size: A4; margin: 17mm 16mm 17mm 16mm; }
body { font-family: 'Georgia', 'Times New Roman', serif; font-size: 10.2pt; line-height: 1.38; color: #1f2328; }
h1 { font-size: 17pt; margin: 0 0 4pt 0; }
h2 { font-size: 12.5pt; margin: 13pt 0 4pt 0; border-bottom: 1px solid #d0d7de; padding-bottom: 2pt; }
p { margin: 4pt 0; text-align: justify; }
img { width: 100%; display: block; margin: 8pt auto 2pt auto; page-break-inside: avoid; }
img[alt="Figure 3"] { width: 62%; }
img[alt="Figure 5"] { width: 72%; }
img[alt="equation"] { width: 46%; margin: 6pt auto; }
table { border-collapse: collapse; width: 100%; font-size: 7.6pt; margin: 4pt 0; page-break-inside: avoid; }
th, td { border-bottom: 1px solid #d0d7de; padding: 2pt 3pt; text-align: right; }
th:first-child, td:first-child { text-align: left; }
th { border-bottom: 1.5px solid #1f2328; }
em { color: #444; }
ul { margin: 3pt 0 3pt 14pt; padding: 0; }
li { margin: 1pt 0; font-size: 9.2pt; }
hr { border: none; border-top: 1px solid #d0d7de; margin: 6pt 0; }
code { font-size: 8.5pt; }
"""

GREEK = {r"\alpha": "α", r"\gamma": "γ", r"\beta": "β", r"\delta": "δ", r"\varepsilon": "ε", r"\,": " "}


def inline_math(tex):
    for k, v in GREEK.items():
        tex = tex.replace(k, v)
    tex = re.sub(r"_\{([^}]*)\}", r"<sub>\1</sub>", tex)
    tex = re.sub(r"_(\w)", r"<sub>\1</sub>", tex)
    return f"<i>{tex}</i>"


def render_equation(tex, path):
    fig = plt.figure(figsize=(6, 0.5))
    fig.text(0.5, 0.5, f"${tex}$", ha="center", va="center", fontsize=15)
    fig.savefig(path, dpi=250, bbox_inches="tight", pad_inches=0.05, transparent=True)
    plt.close(fig)


def find_browser():
    candidates = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                  r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                  r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                  "google-chrome", "chromium", "chromium-browser"]
    for c in candidates:
        if os.path.exists(c) or shutil.which(c):
            return c
    return None


if __name__ == "__main__":
    md = open(os.path.join(PAPER, "PAPER.md"), encoding="utf-8").read()
    # python-markdown needs a blank line before a list that follows a paragraph line
    lines, out = md.split("\n"), []
    is_item = lambda s: bool(re.match(r"\s*(- |\d+\. )", s))
    for line in lines:
        if is_item(line) and out and out[-1].strip() and not is_item(out[-1]):
            out.append("")
        out.append(line)
    md = "\n".join(out)
    eq_dir = os.path.join(PAPER, "assets")
    os.makedirs(eq_dir, exist_ok=True)
    for k, block in enumerate(re.findall(r"\$\$(.+?)\$\$", md, flags=re.S)):
        img = os.path.join(eq_dir, f"eq{k}.png")
        render_equation(block.strip(), img)
        md = md.replace(f"$${block}$$", f"![equation](assets/eq{k}.png)")
    md = re.sub(r"\$([^$\n]+?)\$", lambda m: inline_math(m.group(1)), md)
    body = markdown.markdown(md, extensions=["tables"])
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    html_path = os.path.join(PAPER, "PAPER.html")
    open(html_path, "w", encoding="utf-8").write(html)

    browser = sys.argv[1] if len(sys.argv) > 1 else find_browser()
    if not browser:
        sys.exit("No Chrome/Edge found: open paper/PAPER.html and print to PDF.")
    pdf = os.path.join(PAPER, "PAPER.pdf")
    subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "file:///" + html_path.replace("\\", "/")],
                   check=True, capture_output=True, timeout=180)
    print("Wrote", pdf)

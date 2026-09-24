"""
make_fig_a1_rpys.py — Supplementary Figure A.1 for the Methodological Appendix
==============================================================================
The unwindowed Reference Publication Year Spectroscopy series, 1935-2025,
for both corpora. Companion to Figure 6.15 (windowed to pre-1990).
Shows WHY the window exists: recent decades are inflated by ordinary
citation recency, and would bury the foundational years if plotted together.
Palette, type and sizing identical to the chapter figures
(make_figures_palette.py).
"""
import json, os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "analysis_outputs")
FIG = os.path.join(HERE, "..", "figs_out", "palette")
os.makedirs(FIG, exist_ok=True)

for f in ["Tinos-Regular.ttf", "Tinos-Bold.ttf", "Tinos-Italic.ttf", "Tinos-BoldItalic.ttf"]:
    p = os.path.join("/usr/share/fonts/truetype/croscore", f)
    if os.path.exists(p):
        font_manager.fontManager.addfont(p)

SLATE, TAN = "#3F6E96", "#C08030"
INK, INK2, MUTED, GRID = "#1a1a1a", "#4a4a4a", "#8a8880", "#e6e5e1"
WINDOW_SHADE = "#f0efeb"

plt.rcParams.update({
    "font.family": "Tinos", "font.size": 12,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK2,
    "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": INK2, "ytick.color": INK2,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "axes.labelsize": 12,
    "grid.color": GRID, "grid.linewidth": 0.7,
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
    "legend.fontsize": 12,
})

RF = json.load(open(os.path.join(OUT, "REFINED_RESULTS.json")))

# Labels: the windowed figure's foundational years, plus the recency-era
# peaks the chapter's prose already names (Stam & Naremore 2000; Leitch 2007),
# plus Hutcheon 2006 marked as the year that does NOT spike.
# Each entry: year -> (label, (dx, dy) offset in points, ha)
MARKS = {
    "TS-J": {1959: ("Jakobson\n1959", (-4, 7), "center"),
             1972: ("Holmes\n1972", (-16, 5), "center"),
             1978: ("Halliday\n1978", (8, 9), "left")},
    "AS-J": {1957: ("Bluestone\n1957", (0, 7), "center"),
             1984: ("Andrew\n1984", (0, 7), "center"),
             2000: ("Stam & Naremore\n2000", (-8, 8), "center"),
             2007: ("Leitch\n2007", (12, 8), "left")},
}

fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.8), sharex=True)
for ax, corpus, col in [(axes[0], "TS-J", SLATE), (axes[1], "AS-J", TAN)]:
    dev = RF["R3_rpys"][corpus]["full_deviation"]
    years = [int(y) for y in dev if 1935 <= int(y) <= 2025]
    years.sort()
    vals = [dev[str(y)] for y in years]
    # shade the pre-1990 window that Figure 6.15 reports
    ax.axvspan(1934.5, 1990.5, color=WINDOW_SHADE, zorder=0)
    ax.bar(years, vals, color=col, width=0.82, zorder=2)
    ax.axhline(0, color=MUTED, lw=0.9, zorder=3)
    lo, hi = min(vals), max(vals)
    for y, (lab, off, ha) in MARKS[corpus].items():
        if y in years:
            ax.annotate(lab, (y, max(dev[str(y)], 0)),
                        textcoords="offset points", xytext=off,
                        ha=ha, fontsize=10.5, color=INK, zorder=4)
    if corpus == "AS-J":
        # Hutcheon 2006: most-read book, no spectral peak — open marker at zero-ish dev
        d06 = dev.get("2006", 0)
        ax.plot([2006], [d06], marker="o", ms=6, mfc="white", mec=INK2, mew=1.1, zorder=5)
        ax.annotate("Hutcheon 2006\n(no peak)", (2006, d06),
                    textcoords="offset points", xytext=(16, -44),
                    ha="left", fontsize=10, color=INK2, zorder=5,
                    arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    ax.set_ylabel(f"{corpus}\ndeviation")
    ax.grid(True, axis="y", alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_ylim(lo * 1.2, hi * 1.55)
    # window boundary line
    ax.axvline(1990.5, color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=3)

axes[0].annotate("window of Figure 6.15", xy=(1946, axes[0].get_ylim()[1] * 0.90),
                 ha="center", fontsize=10.5, color=INK2, style="italic")
axes[1].set_xlabel("Publication year of the cited reference")
fig.savefig(os.path.join(FIG, "fig_a1_rpys_unwindowed.png"))
print("saved fig_a1_rpys_unwindowed.png")

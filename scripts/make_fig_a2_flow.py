"""make_fig_a2_flow.py — Figure A.2: corpus-construction flow diagram.

A PRISMA-style funnel for each of the three corpora, drawn from the query
log (Appendix A, Table A.1) and the frozen-corpora table (Table A.2). The
study is a bibliometric analysis, not a systematic review, so PRISMA does
not govern it; the diagram is provided as a courtesy visualization of the
retrieval protocol the tables document. All values are frozen constants
from Tables A.1–A.2.

Palette and type match the thesis figures: slate #3F6E96 (TS), tan
#C08030 (AS-J), light tan #E4C08C (AS-T), Tinos/Times, 6.5 in, 300 dpi.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

SLATE = "#3F6E96"
TAN = "#C08030"
LIGHT_TAN = "#E4C08C"
GREY = "#6B6B6B"
PAPER = "#F7F4EE"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Tinos", "Times New Roman", "Liberation Serif"],
    "font.size": 12,
    "figure.dpi": 300,
    "savefig.dpi": 300,
})

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figs_out")
os.makedirs(OUT, exist_ok=True)

fig, ax = plt.subplots(figsize=(6.5, 7.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

COLS = {  # column centre x, half-width
    "TS-J": (17.5, 15.5),
    "AS-J": (50.0, 15.5),
    "AS-T": (82.5, 15.5),
}
COLORS = {"TS-J": SLATE, "AS-J": TAN, "AS-T": TAN}


def box(cx, cy, w, h, text, edge, face="white", fs=7.8, bold_first=False,
        text_color="#222222"):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.6,rounding_size=1.2",
                                linewidth=1.2, edgecolor=edge,
                                facecolor=face, mutation_scale=1))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            color=text_color, linespacing=1.35)


def arrow(cx, y1, y2, color):
    ax.annotate("", xy=(cx, y2), xytext=(cx, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4))


# column headers
for name, (cx, hw) in COLS.items():
    label = {"TS-J": "TS-J\nTranslation Studies journals",
             "AS-J": "AS-J\nAdaptation Studies journals",
             "AS-T": "AS-T\nDispersed adaptation literature"}[name]
    face = {"TS-J": SLATE, "AS-J": TAN, "AS-T": LIGHT_TAN}[name]
    tc = "white" if name != "AS-T" else "#4A3208"
    box(cx, 96.0, 2 * hw, 6.0, label, edge=face, face=face, fs=8.4,
        text_color=tc)

ROW_ID, ROW_EX, ROW_FR, ROW_RF = 82.8, 64.3, 45.8, 29.2
BH = 12.6  # box height

# --- identification row -------------------------------------------------
box(*[COLS["TS-J"][0], ROW_ID], 31, BH,
    "Identification\n21 seed journal titles,\nsearched by source (SO),\n"
    "no date limit\nQ-06 · 29 Jul 2026\n14,252 records", SLATE)
box(*[COLS["AS-J"][0], ROW_ID], 31, BH,
    "Identification\nThe field's dedicated journals,\nsearched by source (SO),\n"
    "no date limit\nQ-03 · 29 Jul 2026\n2,281 records", TAN)
box(*[COLS["AS-T"][0], ROW_ID], 31, BH,
    "Identification\nTopic search TS=(adaptation),\nall research areas\n"
    "29 Jul 2026\n794,314 records", TAN)

# --- screening / refinement row ----------------------------------------
box(*[COLS["TS-J"][0], ROW_EX], 31, BH,
    "Screening\n1 title returned no records\n(not indexed in the\n"
    "Core Collection)\n→ 20 journals retained", SLATE)
box(*[COLS["AS-J"][0], ROW_EX], 31, BH,
    "Correction\nJ. of Adaptation in Film &\nPerformance missed by a\n"
    "query-string error; corrected\nQ-07 · 29 Jul 2026\n2,761 records", TAN)
box(*[COLS["AS-T"][0], ROW_EX], 31, BH,
    "Refinement\nRestricted to 13 Humanities\nresearch areas; 775,748\n"
    "records outside them excluded\nQ-08 · 4 Aug 2026\n18,566 records", TAN)

# --- frozen corpus row --------------------------------------------------
box(*[COLS["TS-J"][0], ROW_FR], 31, BH,
    "Frozen corpus\nRe-export Q-09 · 4 Aug 2026\n14,258 records\n"
    "20 journals\n(+6 records of database\ndrift in one week)", SLATE,
    face=PAPER)
box(*[COLS["AS-J"][0], ROW_FR], 31, BH,
    "Frozen corpus\nRe-export Q-10 · 4 Aug 2026\n2,763 records\n"
    "3 journals\n(+2 records of database\ndrift in one week)", TAN,
    face=PAPER)
box(*[COLS["AS-T"][0], ROW_FR], 31, BH,
    "Frozen corpus\nQ-08 · 4 Aug 2026\n18,566 records\n3,599 journals\n"
    "842 (4.5%) in adaptation's\nown three journals", TAN, face=PAPER)

# --- references row -----------------------------------------------------
box(*[COLS["TS-J"][0], ROW_RF], 31, 8.6,
    "Cited references\n333,707 carried\n318,442 parsed (95.4%)", SLATE)
box(*[COLS["AS-J"][0], ROW_RF], 31, 8.6,
    "Cited references\n48,954 carried\n44,126 parsed (90.1%)", TAN)
box(*[COLS["AS-T"][0], ROW_RF], 31, 8.6,
    "Cited references\n660,554 carried\n627,992 parsed (95.1%)", TAN)

# arrows
for name, (cx, hw) in COLS.items():
    c = COLORS[name]
    arrow(cx, 92.6, 89.6, c)
    arrow(cx, ROW_ID - BH / 2 - 0.7, ROW_EX + BH / 2 + 1.0, c)
    arrow(cx, ROW_EX - BH / 2 - 0.7, ROW_FR + BH / 2 + 1.0, c)
    arrow(cx, ROW_FR - BH / 2 - 0.7, ROW_RF + 8.6 / 2 + 1.0, c)

# --- total band ---------------------------------------------------------
box(50, 14.0, 96, 7.0,
    "Analyzed together:  35,587 records   ·   1,043,215 cited references"
    "   ·   990,560 parsed (95.0%)",
    edge=GREY, face=PAPER, fs=9.2)
for name, (cx, hw) in COLS.items():
    arrow(cx, ROW_RF - 8.6 / 2 - 0.7, 18.2, GREY)

ax.text(50, 6.6,
        "Queries, dates and counts from Table A.1; frozen corpora from "
        "Table A.2. Identical queries re-run later return\nslightly "
        "different counts (database drift); every count in the thesis "
        "therefore carries its export date.",
        ha="center", va="center", fontsize=8.2, color=GREY, style="italic",
        linespacing=1.4)

fig.savefig(os.path.join(OUT, "fig_a2_corpus_flow.png"),
            bbox_inches="tight", pad_inches=0.08)
print("wrote", os.path.join(OUT, "fig_a2_corpus_flow.png"))

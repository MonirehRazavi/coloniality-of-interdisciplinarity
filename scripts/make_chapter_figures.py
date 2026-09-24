"""make_chapter_figures.py — regenerates the thesis figures NOT drawn by
make_figures_palette.py / make_fig_a1_rpys.py, so that every figure in the
thesis has a script in this deposit.

Coverage (final thesis numbering):
    Figure 1.1  WoS categories, topic search "adaptation"      (treemap)
    Figure 1.2  WoS categories, topic search "translation"     (treemap)
    Figure 4.1  The mirror test: each canon in the other's journals
    Figure 5.1  Landmark moments in the formation of TS and AS (timeline)
    Figure 5.2  Two narrative grammars: river and delta         (schematic)
    Figure 5.3  Thematic evolution of AS-J, 1992–2023
    Figure 5.4  Geography of publication across the three corpora
    Figure 5.5  TS authors cited in the AS journal corpus
    Figure 5.6  Research areas of the dispersed corpus (AS-T)

The remaining figures are drawn by make_figures_palette.py (Figures 1.3,
1.4, 3.1, 3.2, 4.2–4.6, 5.7 — under their original fig_6_* output names;
see the mapping in the README) and make_fig_a1_rpys.py (Figure A.1).

Data sources, by figure:
  * 1.1/1.2, 5.6, and the milestone content of 5.1/5.2 are drawn from
    values embedded below as frozen constants. The category counts in
    1.1/1.2 were read from the Web of Science search interface on
    29 July 2026 (they describe the raw word before any corpus exists,
    so no export carries them); the research-area counts in 5.6 are the
    WoS "refine" panel counts for the frozen AS-T corpus (4 August 2026);
    5.1/5.2 are illustrative diagrams whose content is bibliographic.
  * 4.1 and 5.5 are computed from ../analysis_outputs/ALL_RESULTS.json.
  * 5.3 and 5.4 recompute from the raw WoS exports in ../data/ (not
    included in the public deposit — see the README's data-availability
    note). The published values are recorded in comments beside each.

Palette and type match the rest of the thesis: slate #3F6E96 (TS),
tan #C08030 (AS), light tan #E4C08C (AS-T), Tinos/Times 12 pt, 6.5 in
wide, 300 dpi.
"""

import json
import os
import re
from collections import Counter, defaultdict

import wos_parser as W   # the package parser (D17: one parser for every figure)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager  # noqa: F401

SLATE = "#3F6E96"
TAN = "#C08030"
LIGHT_TAN = "#E4C08C"
LIGHT_SLATE = "#9FB8CC"
GREY = "#6B6B6B"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Tinos", "Times New Roman", "Liberation Serif"],
    "font.size": 12,
    "axes.edgecolor": "#B0B0B0",
    "axes.linewidth": 0.8,
    "figure.dpi": 300,
    "savefig.dpi": 300,
})

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figs_out")
os.makedirs(OUT, exist_ok=True)
AO = os.path.join(HERE, "..", "analysis_outputs")
DATA = os.path.join(HERE, "..", "data")


def finish(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("wrote", path)


# ----------------------------------------------------------------------
# Figures 1.1 and 1.2 — WoS category treemaps
# Counts read from the WoS Core Collection search interface, 29 Jul 2026.
# Topic search TS=(adaptation): 794,314 records; TS=(translation): the
# ten largest categories below. Humanities palette highlight: categories
# in which the word's Humanities sense lives are tan; all others slate.
# ----------------------------------------------------------------------
ADAPTATION_TOP10 = [
    ("Engineering, Electrical & Electronic", 58273, SLATE),
    ("Environmental Sciences", 43430, SLATE),
    ("Computer Science, Artificial Intelligence", 41722, SLATE),
    ("Biochemistry & Molecular Biology", 35207, SLATE),
    ("Ecology", 34111, SLATE),
    ("Plant Sciences", 33293, SLATE),
    ("Neurosciences", 31779, SLATE),
    ("Multidisciplinary Sciences", 31770, SLATE),
    ("Computer Science, Information Systems", 28407, SLATE),
    ("Computer Science, Theory & Methods", 27505, SLATE),
]
TRANSLATION_TOP10 = [
    ("Biochemistry & Molecular Biology", 52351, SLATE),
    ("Language & Linguistics", 29198, TAN),
    ("Cell Biology", 24932, SLATE),
    ("Computer Science, Artificial Intelligence", 24049, SLATE),
    ("Linguistics", 20943, TAN),
    ("Engineering, Electrical & Electronic", 18491, SLATE),
    ("Computer Science, Theory & Methods", 16737, SLATE),
    ("Multidisciplinary Sciences", 16674, SLATE),
    ("Genetics & Heredity", 13399, SLATE),
    ("Pharmacology & Pharmacy", 13124, SLATE),
]


def shade(base_hex, k, n):
    """Lighten base colour towards white with rank (largest = darkest)."""
    import matplotlib.colors as mc
    r, g, b = mc.to_rgb(base_hex)
    f = 0.15 + 0.55 * (k / max(n - 1, 1))
    return (r + (1 - r) * f, g + (1 - g) * f, b + (1 - b) * f)


def treemap(data, name):
    import squarify
    fig, ax = plt.subplots(figsize=(6.5, 3.1))
    sizes = [v for _, v, _ in data]
    colors = []
    slate_rank = tan_rank = 0
    n_slate = sum(1 for *_, c in data if c == SLATE)
    n_tan = sum(1 for *_, c in data if c == TAN)
    for _, _, c in data:
        if c == SLATE:
            colors.append(shade(SLATE, slate_rank, max(n_slate, 2)))
            slate_rank += 1
        else:
            colors.append(shade(TAN, tan_rank, max(n_tan, 2)))
            tan_rank += 1
    labels = [f"{lab}\n{v:,}" for lab, v, _ in data]
    squarify.plot(sizes=sizes, label=labels, color=colors, ax=ax,
                  pad=True, text_kwargs={"fontsize": 8.5, "color": "#222222"})
    ax.axis("off")
    finish(fig, name)


# ----------------------------------------------------------------------
# Figure 4.1 — the mirror test (top canon authors in the other's journals)
# Computed from ALL_RESULTS.json (6.4b blocks). Denominators: parsed
# references, AS-J 44,126 and TS-J 318,442 (Table A.2).
# ----------------------------------------------------------------------
def fig_mirror():
    d = json.load(open(os.path.join(AO, "ALL_RESULTS.json")))
    ts_in_asj = d["6.4b_ts_canon_in_ASJ"]
    as_in_tsj = d["6.4b_as_canon_in_TSJ"]

    def top6(block):
        rows = [(name.split(",")[0], v["references"]) for name, v in block.items()]
        return sorted(rows, key=lambda r: -r[1])[:6]

    left = top6(ts_in_asj)     # AS journals citing the TS canon
    right = top6(as_in_tsj)    # TS journals citing the AS canon
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.6))
    for ax, rows, color, title, rate in (
        (axes[0], left, TAN, "AS journals citing the TS canon", 32.9),
        (axes[1], right, SLATE, "TS journals citing the AS canon", 6.6),
    ):
        names = [r[0] for r in rows][::-1]
        vals = [r[1] for r in rows][::-1]
        ax.barh(names, vals, color=color, height=0.62)
        for y, v in enumerate(vals):
            ax.text(v + max(vals) * 0.02, y, str(v), va="center", fontsize=10)
        ax.set_title(title, fontsize=11, fontweight="bold", loc="left")
        ax.set_xlabel(f"Cited references — {rate} per 10,000 references",
                      fontsize=10, color=GREY)
        ax.set_xlim(0, max(vals) * 1.15)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=10)
    fig.tight_layout()
    finish(fig, "fig_4_01_mirror_canons.png")


# ----------------------------------------------------------------------
# Figure 5.1 — landmark moments (timeline). Bibliographic milestones.
# ----------------------------------------------------------------------
TS_MILESTONES = [
    # (year, label, label_x, label_y)  — label positions hand-set to avoid
    # collisions, matching the published layout
    (1959, "Jakobson,\n'translation proper'", 1959, 0.55),
    (1972, "Holmes, 'The Name\nand Nature of\nTranslation Studies'", 1972, 1.75),
    (1976, "Leuven\ncolloquium", 1980, 0.55),
    (1995, "Toury, Descriptive\nTranslation Studies", 1995, 0.55),
    (2006, "Snell-Hornby,\nThe Turns of\nTranslation Studies", 2006, 1.75),
]
AS_MILESTONES = [
    (1957, "Bluestone,\nNovels into Film", 1957, -0.55),
    (1984, "Andrew,\n'Adaptation'", 1984, -0.55),
    (2003, "Leitch,\n'Twelve\nFallacies'", 2001, -0.75),
    (2006, "Hutcheon,\nA Theory of\nAdaptation;\nAAS founded", 2006, -1.75),
    (2014, "Cattrysse,\nDescriptive\nAdaptation\nStudies", 2013, -2.95),
    (2017, "Oxford\nHandbook of\nAdaptation\nStudies", 2018, -1.75),
    (2020, "Elliott,\nTheorizing\nAdaptation", 2023, -0.75),
]


def fig_timeline():
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.hlines(1, 1953, 2025, color=SLATE, lw=3)
    ax.hlines(0, 1953, 2025, color=TAN, lw=3)
    for yr, lab, lx, ly in TS_MILESTONES:
        ax.plot(yr, 1, "o", color=SLATE, ms=7)
        ax.annotate(lab, (yr, 1), xytext=(lx, 1 + ly),
                    ha="center", va="bottom", fontsize=9,
                    arrowprops=dict(arrowstyle="-", color=LIGHT_SLATE, lw=1))
    for yr, lab, lx, ly in AS_MILESTONES:
        ax.plot(yr, 0, "o", color=TAN, ms=7)
        ax.annotate(lab, (yr, 0), xytext=(lx, ly),
                    ha="center", va="top", fontsize=9,
                    arrowprops=dict(arrowstyle="-", color=LIGHT_TAN, lw=1))
    ax.annotate("", xy=(1972, 0.55), xytext=(1957, 0.55),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=1))
    ax.text(1964.5, 0.62, "fifteen years", ha="center",
            fontsize=10, style="italic", color=GREY)
    ax.text(2025.7, 1, "Translation Studies", color=SLATE, va="center", fontsize=12)
    ax.text(2025.7, 0, "Adaptation Studies", color=TAN, va="center", fontsize=12)
    ax.set_ylim(-4.3, 3.1)
    ax.set_xlim(1951, 2040)
    ax.set_yticks([])
    ax.set_xlabel("Publication year")
    ax.spines[["top", "right", "left"]].set_visible(False)
    finish(fig, "fig_5_01_landmarks.png")


# ----------------------------------------------------------------------
# Figure 5.2 — two narrative grammars (river / delta schematic)
# ----------------------------------------------------------------------
def fig_grammars():
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.4))
    ax = axes[0]
    turns = ["linguistic turn", "cultural turn", "sociological turn",
             "activist turn", "technological turn"]
    ax.vlines(0.15, 0.02, 0.98, color=SLATE, lw=4)
    for i, t in enumerate(turns):
        y = 0.10 + i * 0.20
        ax.plot(0.15, y, "o", color=SLATE, ms=8)
        ax.text(0.24, y, t, va="center", fontsize=12)
    ax.set_title("Translation Studies: a river", color=SLATE, fontsize=13)
    ax.text(0.5, -0.12, "one channel; a centre\nthat can reorient itself",
            ha="center", fontsize=11, style="italic", color=GREY,
            transform=ax.transAxes)
    ax = axes[1]
    trunk_x, fork_y = 0.5, 0.42
    ax.plot([trunk_x, trunk_x], [0.02, fork_y], color=TAN, lw=4,
            solid_capstyle="round")
    branches = [(-0.30, 0.52, "fidelity", "right"),
                (-0.10, 0.90, "intertextuality", "right"),
                (0.10, 0.90, "cultural politics", "left"),
                (0.30, 0.52, "digital\nconvergence", "left")]
    for dx, top, lab, side in branches:
        ax.plot([trunk_x, trunk_x + dx], [fork_y, top], color=TAN, lw=3.5,
                solid_capstyle="round")
        ax.plot(trunk_x + dx, top, "o", color=TAN, ms=8)
        off = -0.03 if side == "right" else 0.03
        ax.text(trunk_x + dx + off, top, lab, fontsize=12,
                ha=side, va="center")
    ax.set_title("Adaptation Studies: a delta", color=TAN, fontsize=13)
    ax.text(0.5, -0.12, "streams that coexist; no channel\nthat can speak for the rest",
            ha="center", fontsize=11, style="italic", color=GREY,
            transform=ax.transAxes)
    for ax in axes:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    finish(fig, "fig_5_02_grammars.png")


# ----------------------------------------------------------------------
# Figure 5.3 — thematic evolution of AS-J, 1992–2023.
# Recomputed from the raw AS-J export in ../data/AS-J/ (not included in
# the public deposit). Term sets fixed before analysis, from the four
# streams named in §5.1; a record matches a theme if any term matches
# its title, abstract, author keywords or Keywords Plus.
# Values as reported in the thesis after the 22 Sep 2026 rerun (D17), five-
# year rolling share: fidelity 0.9% (1995) → peak 7.0% (2021), 6.4% (2023);
# intertextuality 0 → 14.6% (2023); cultural politics 3.6% → peak 26.0%
# (2022); digital/transmedia 0 → 21.3% (2023).  The August 2026 figure
# carried slightly different values from a script that was not preserved
# and matched terms without word boundaries; see the decision log, D17.
# ----------------------------------------------------------------------
TERM_SETS = {
    "Fidelity": [r"fidelit\w*", r"faithful", r"unfaithful", r"betray\w*"],
    "Intertextuality": [r"intertextual\w*", r"appropriat\w*", r"dialogic\w*",
                        r"palimpsest\w*", r"hypertext\w*"],
    "Cultural politics": [r"postcolonial\w*", r"ideolog\w*", r"gender",
                          r"feminis\w*", r"race", r"racial", r"queer",
                          r"nationalism", r"politics", r"political"],
    "Digital and transmedia": [r"transmedia\w*", r"digital", r"videogame",
                               r"video game", r"convergen\w*", r"franchis\w*",
                               r"streaming", r"paratext\w*", r"fandom",
                               r"fan fiction"],
}
THEME_COLORS = {"Fidelity": TAN, "Intertextuality": SLATE,
                "Cultural politics": "#7A4E12", "Digital and transmedia": LIGHT_SLATE}


def load_records(corpus_dir):
    """SUPERSEDED (D17, 22 Sep 2026): kept for the record only. It joined the
    C1 address lines into one string, so a record's authors from several
    countries were counted under the last one; wos_parser.load_corpus keeps
    C1 as a list and is used instead.  Minimal WoS plain-text reader: returns list of dicts with PY and text
    fields (TI/AB/DE/ID), honouring the field-wrapping convention."""
    recs = []
    for fn in sorted(os.listdir(corpus_dir)):
        if not fn.lower().endswith(".txt"):
            continue
        cur, field = {}, None
        for line in open(os.path.join(corpus_dir, fn), encoding="utf-8-sig",
                         errors="replace"):
            line = line.rstrip("\n")
            if line[:2] == "ER":
                if cur:
                    recs.append(cur)
                cur, field = {}, None
            elif line[:2] == "  " and field:
                cur[field] = cur.get(field, "") + " " + line.strip()
            elif len(line) >= 3 and line[2] == " ":
                field = line[:2]
                cur[field] = line[3:].strip()
    return recs


def fig_thematic_evolution():
    src = os.path.join(DATA, "AS-J")
    if not os.path.isdir(src):
        print("skip fig_5_03: raw AS-J export not present (see README, "
              "data availability)")
        return
    recs = W.load_corpus(src, verbose=False)
    # CORRECTION, 22 Sep 2026 (decision log D17): match whole words only.
    # Without the boundaries "race" matched "trace"/"embrace", "digital"
    # matched nothing wrongly but "gender" matched "engendered", etc.
    pats = {t: re.compile("|".join(r"\b(?:" + p + r")\b" for p in ps), re.I)
            for t, ps in TERM_SETS.items()}
    yr_tot = Counter()
    yr_hit = defaultdict(Counter)
    for r in recs:
        try:
            py = int(r.get("PY", "")[:4])
        except ValueError:
            continue
        if not 1990 <= py <= 2024:
            continue
        yr_tot[py] += 1
        text = " ".join(
            (" ".join(r[f]) if isinstance(r.get(f), list) else r.get(f, ""))
            for f in ("TI", "AB", "DE", "ID"))
        for t, pat in pats.items():
            if pat.search(text):
                yr_hit[t][py] += 1
    years = list(range(1992, 2024))
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    for t in TERM_SETS:
        series = []
        for y in years:
            win = range(y - 4, y + 1)
            tot = sum(yr_tot[w] for w in win)
            hit = sum(yr_hit[t][w] for w in win)
            series.append(100 * hit / tot if tot else 0)
        ax.plot(years, series, color=THEME_COLORS[t], lw=2.2, label=t)
        ax.annotate(t, (years[-1], series[-1]), xytext=(5, 0),
                    textcoords="offset points", va="center", fontsize=10.5,
                    color=THEME_COLORS[t])
        pk = max(range(len(years)), key=lambda i: series[i])
        print(f"  {t:24s} 1995={series[years.index(1995)]:.1f}% "
              f"2005={series[years.index(2005)]:.1f}% "
              f"2015={series[years.index(2015)]:.1f}% "
              f"2023={series[years.index(2023)]:.1f}%  "
              f"peak={series[pk]:.1f}% ({years[pk]})")
    from matplotlib.ticker import PercentFormatter
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.set_ylabel("Share of AS-J records")
    ax.set_xlabel("Publication year")
    ax.set_xlim(years[0], years[-1] + 9)
    ax.set_xticks(list(range(1995, 2024, 5)))
    ax.grid(axis="y", color="#e6e5e1", lw=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    finish(fig, "fig_5_03_thematic_evolution.png")


# ----------------------------------------------------------------------
# Figure 5.4 — geography of publication (three corpora).
# Recomputed from the C1 (author address) field of the raw exports.
# Values as reported in the thesis after the 22 Sep 2026 rerun (D17), share
# of records carrying an affiliation, TS-J / AS-J / AS-T: USA 8/47/22,
# UK 15/22/12, Spain 16/1/9, China 12/2/5, Brazil 8/<1/3, Canada 6/4/4,
# Russia <1/0/5, Turkey 1/5/2, Belgium 4/2/2, Germany 2/1/4, Australia
# 3/4/4.  Denominators: TS-J 11,887 of 14,258; AS-J 1,754 of 2,763; AS-T
# 15,787 of 18,566.  Global South (UNCTAD grouping): 30.0 / 8.7 / 23.3.
# ----------------------------------------------------------------------
COUNTRY_ALIASES = {
    "USA": "USA", "PEOPLES R CHINA": "China", "ENGLAND": "UK",
    "SCOTLAND": "UK", "WALES": "UK", "NORTH IRELAND": "UK",
    "RUSSIA": "Russia", "TURKIYE": "Turkey", "TURKEY": "Turkey",
}
SHOW = ["USA", "UK", "Spain", "China", "Brazil", "Canada", "Russia",
        "Turkey", "Belgium", "Germany", "Australia"]


US_STATES = set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA "
                "MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN "
                "TX UT VT VA WA WV WI WY DC PR".split())


def country_of_address(addr):
    """Country of one WoS C1 address: the last comma-separated element,
    with the two US forms the database uses ('MD 21218 USA' and the bare
    'MD 21218') both resolved to USA.  CORRECTION, 22 Sep 2026 (D17): the
    earlier version only recognised an address whose last element was
    exactly 'USA', so most US addresses were counted under their state."""
    addr = re.sub(r"^\[.*?\]\s*", "", addr)          # drop "[Author, A] "
    tail = addr.split(",")[-1].strip().rstrip(".").upper()
    if tail.endswith("USA"):
        return "USA"
    m = re.match(r"^([A-Z]{2})(?: \d{5}(?:-\d{4})?)?$", tail)
    if m and m.group(1) in US_STATES:
        return "USA"
    return COUNTRY_ALIASES.get(tail, tail.title())


def countries_of(rec):
    c1 = rec.get("C1", "")
    if isinstance(c1, list):
        addrs = c1
    else:
        addrs = [a for a in c1.split(";") if a.strip()]
    return {country_of_address(a) for a in addrs if country_of_address(a)}


# The Global South share quoted in §6.9 uses the UNCTAD grouping of
# "developing economies": every country outside Europe (Russia included),
# Northern America, Australia, New Zealand, Japan and Israel counts as
# South.  The North set is declared here so a reader can move a country
# and see what changes.  Records with authors on both sides count as
# carrying a Global-South affiliation.
GLOBAL_NORTH = {"USA", "Canada", "Australia", "New Zealand", "Japan", "Israel",
    # Europe
    "UK", "Ireland", "France", "Germany", "Austria", "Switzerland", "Belgium",
    "Netherlands", "Luxembourg", "Denmark", "Sweden", "Norway", "Finland",
    "Iceland", "Italy", "Spain", "Portugal", "Greece", "Malta", "Cyprus",
    "Poland", "Czech Republic", "Slovakia", "Hungary", "Romania", "Bulgaria",
    "Slovenia", "Croatia", "Serbia", "Bosnia & Herceg", "Montenegro",
    "North Macedonia", "Macedonia", "Albania", "Kosovo", "Estonia", "Latvia",
    "Lithuania", "Ukraine", "Belarus", "Moldova", "Russia", "Georgia",
    "Armenia", "Liechtenstein", "Monaco", "Andorra", "San Marino"}


def fig_geography():
    dirs = {"TS-J": ("TS-J", SLATE), "AS-J": ("AS-J", TAN),
            "AS-T": ("AS-T", LIGHT_TAN)}
    shares = {}
    for key, (sub, _) in dirs.items():
        src = os.path.join(DATA, sub)
        if not os.path.isdir(src):
            print("skip fig_5_04: raw exports not present (see README)")
            return
        recs = W.load_corpus(src, verbose=False)
        withaff = [r for r in recs if r.get("C1")]
        cnt = Counter()
        for r in withaff:
            for c in countries_of(r):
                cnt[c] += 1
        shares[key] = {c: 100 * cnt[c] / len(withaff) for c in SHOW}
        south = sum(1 for r in withaff
                    if any(c not in GLOBAL_NORTH for c in countries_of(r)))
        print(f"  {key}: {len(withaff):,} records with an affiliation; "
              + "; ".join(f"{c} {shares[key][c]:.1f}%" for c in SHOW)
              + f"; Brazil n={cnt['Brazil']}; Global South share "
              f"{100 * south / len(withaff):.1f}%")
    fig, ax = plt.subplots(figsize=(6.5, 5.4))
    idx = range(len(SHOW))
    h = 0.27
    for off, (key, (sub, color)) in zip((-h, 0, h), dirs.items()):
        vals = [shares[key][c] for c in SHOW]
        for i, v in zip(idx, vals):
            ax.text(v + 0.4, i + off, "<1" if 0 < v < 0.5 else f"{v:.0f}",
                    va="center", fontsize=9, color="#4a4a4a")
        ax.barh([i + off for i in idx], vals, height=h, color=color,
                label={"TS-J": "Translation Studies journals (TS-J)",
                       "AS-J": "Adaptation Studies journals (AS-J)",
                       "AS-T": "Dispersed adaptation literature (AS-T)"}[key])
    ax.set_yticks(list(idx), SHOW)
    ax.invert_yaxis()
    ax.set_xlabel("Share of records carrying an affiliation (%)")
    from matplotlib.ticker import PercentFormatter
    ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.grid(axis="x", color="#e6e5e1", lw=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=10, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    finish(fig, "fig_5_04_geography.png")


# ----------------------------------------------------------------------
# Figure 5.5 — TS authors cited in the AS journal corpus.
# From ALL_RESULTS.json, 6.4b_ts_canon_in_ASJ (all 23 canon authors).
# ----------------------------------------------------------------------
def fig_ts_authors_in_asj():
    """Figure 6.14 in the thesis.  Redrawn 22 Sep 2026 (D17) in the thesis's
    lollipop layout, with authors cited at least 3 times, and the rate
    stated per 10,000 PARSED references (32.9), the same denominator used in
    Figure 6.2, Table 6.4 and Table 6.6; an earlier hand-drawn version of
    this figure quoted 29.6, the rate per raw reference, which the text
    nowhere else uses."""
    d = json.load(open(os.path.join(AO, "ALL_RESULTS.json")))
    block = d["6.4b_ts_canon_in_ASJ"]
    tot = d["6.4b_totals"]["TS_canon_in_ASJ"]
    rows = sorted(((n.split(",")[0], v["references"]) for n, v in block.items()),
                  key=lambda r: -r[1])
    rows = [r for r in rows if r[1] >= 3]
    names = [r[0] for r in rows][::-1]
    vals = [r[1] for r in rows][::-1]
    top3 = {"Venuti", "Jakobson", "Lefevere"}
    fig, ax = plt.subplots(figsize=(6.5, 0.3 * len(rows) + 1.3))
    for y, (n, v) in enumerate(zip(names, vals)):
        c = TAN if n in top3 else SLATE
        ax.plot([0, v], [y, y], color=c, lw=1.6, alpha=0.75, zorder=1)
        ax.plot([v], [y], "o", color=c, ms=7, zorder=2)
        ax.text(v + 0.6, y, str(v), va="center", fontsize=10, color="#4a4a4a")
    ax.set_yticks(range(len(names)), names)
    ax.set_xlim(0, max(vals) * 1.18)
    ax.set_xlabel("Cited references within AS-J")
    ax.grid(axis="x", color="#e6e5e1", lw=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=10.5)
    ax.text(0.97, 0.12,
            f"{tot['references']} references in 44,126 parsed\n"
            f"({tot['per_10k_references']} per 10,000)\n\n"
            "Jakobson, Lefevere and Venuti\naccount for 62 of the 145",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=10.5,
            color="#4a4a4a",
            bbox=dict(boxstyle="square,pad=0.7", fc="#f4f1ea", ec="none"))
    finish(fig, "fig_5_05_ts_authors_in_asj.png")


# ----------------------------------------------------------------------
# Figure 5.6 — research areas of the dispersed corpus (AS-T).
# WoS refine-panel counts for the frozen corpus, 4 Aug 2026. A record can
# carry more than one area, so counts exceed 18,566 in total.
# ----------------------------------------------------------------------
AST_AREAS = [
    ("Literature", 5551), ("Arts & Humanities, other", 4581),
    ("Communication", 2360), ("Film, radio and television", 2063),
    ("Area Studies", 1771), ("Theater", 1100), ("Linguistics", 825),
    ("Cultural Studies", 796), ("Music", 739), ("Art", 698),
    ("Asian Studies", 640), ("Women's Studies", 594),
]


def fig_ast_areas():
    names = [a for a, _ in AST_AREAS][::-1]
    vals = [v for _, v in AST_AREAS][::-1]
    fig, ax = plt.subplots(figsize=(6.5, 4.6))
    ax.barh(names, vals, color=TAN, height=0.62)
    for y, v in enumerate(vals):
        ax.text(v + 60, y, f"{v:,}", va="center", fontsize=10)
    ax.set_xlabel("Records in the dispersed adaptation corpus (AS-T)")
    ax.text(0.97, 0.28,
            "18,566 records\n3,599 journals\n660,554 cited references\n\n"
            "842 records (4.5%) appear in\nadaptation's own three journals",
            transform=ax.transAxes, ha="right", fontsize=10,
            bbox=dict(facecolor="#F2EEE6", edgecolor="none", pad=8))
    ax.spines[["top", "right"]].set_visible(False)
    finish(fig, "fig_5_06_ast_research_areas.png")


if __name__ == "__main__":
    treemap(ADAPTATION_TOP10, "fig_1_01_adaptation_treemap.png")
    treemap(TRANSLATION_TOP10, "fig_1_02_translation_treemap.png")
    fig_mirror()
    fig_timeline()
    fig_grammars()
    fig_thematic_evolution()
    fig_geography()
    fig_ts_authors_in_asj()
    fig_ast_areas()

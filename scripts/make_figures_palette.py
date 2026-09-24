"""
make_figures_palette.py — Chapter 6 figures 6.03–6.13, blue-grey/tan palette
============================================================================
APA style: no titles inside images (figure number + title live in the document).
Type: Tinos (Times New Roman metric equivalent), 12 pt base.
Palette: slate blue-grey for Translation Studies, warm tan for Adaptation
Studies (the emphasized class), light tan for the dispersed AS-T corpus,
light slate for neutral fills. Matches Figures 6.1–6.2 (treemaps).
"""
import json, os, pickle, re
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import PercentFormatter, FuncFormatter

import wos_parser as W

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "analysis_outputs")
FIG = os.path.join(HERE, "..", "figs_out", "palette")
os.makedirs(FIG, exist_ok=True)

for f in ["Tinos-Regular.ttf", "Tinos-Bold.ttf", "Tinos-Italic.ttf", "Tinos-BoldItalic.ttf"]:
    p = os.path.join("/usr/share/fonts/truetype/croscore", f)
    if os.path.exists(p):
        font_manager.fontManager.addfont(p)

SLATE, TAN = "#3F6E96", "#C08030"          # TS / AS (emphasis)
TAN_LIGHT, SLATE_LIGHT = "#E4C08C", "#9FB8CC"
INK, INK2, MUTED, GRID = "#1a1a1a", "#4a4a4a", "#8a8880", "#e6e5e1"

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

A = json.load(open(os.path.join(OUT, "ALL_RESULTS.json")))
RF = json.load(open(os.path.join(OUT, "REFINED_RESULTS.json")))
NW = json.load(open(os.path.join(OUT, "NETWORK_RESULTS.json")))
C = pickle.load(open(os.path.join(OUT, "corpora.pkl"), "rb"))["C"]

saved = []
def finish(fig, name):
    fig.savefig(os.path.join(FIG, name))
    plt.close(fig)
    saved.append(name)
    print("  saved", name)

def thousands(x, _):
    return f"{int(x):,}"


# ===========================================================================
# 6.03 — indexed output per year, three corpora
# ===========================================================================
def year_counts(recs, lo=1975, hi=2025):
    c = Counter()
    for r in recs:
        py = r.get("PY", "")
        if py.isdigit() and lo <= int(py) <= hi:
            c[int(py)] += 1
    return c

fig, ax = plt.subplots(figsize=(7.2, 4.0))
for name, col in [("TS-J", SLATE), ("AS-T", TAN_LIGHT), ("AS-J", TAN)]:
    c = year_counts(C[name])
    ys = sorted(c)
    ax.plot(ys, [c[y] for y in ys], color=col, lw=2.4, label=name,
            solid_capstyle="round")
    ax.annotate(name, (ys[-1], c[ys[-1]]), textcoords="offset points",
                xytext=(7, 0), color=col if col != TAN_LIGHT else "#B98A45",
                fontsize=12, va="center")
ax.axvspan(2015, 2017, color=GRID, alpha=0.65, zorder=0)
ax.annotate("ESCI expansion\n2015–17", xy=(2016, ax.get_ylim()[1] * 0.9),
            ha="center", fontsize=11, color=MUTED, style="italic")
ax.set_xlabel("Publication year")
ax.set_ylabel("Records indexed that year")
ax.grid(True, alpha=0.6); ax.set_axisbelow(True)
ax.set_xlim(1975, 2028)
ax.yaxis.set_major_formatter(FuncFormatter(thousands))
finish(fig, "fig_6_03_indexed_output.png")


# ===========================================================================
# 6.04 — who each field reads (most-cited authors within own corpus)
# ===========================================================================
def local_cited_authors(corpus, n=15):
    c = Counter()
    for i, cr in W.iter_refs(C[corpus]):
        a, y, s = W.split_cr(cr)
        if a:
            sn, ini = W.norm_author(a)
            if sn and sn != "[ANONYMOUS]":
                c[(sn, ini)] += 1
    return c.most_common(n)

fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.8))
for ax, corpus, col in [(axes[0], "TS-J", SLATE), (axes[1], "AS-J", TAN)]:
    top = local_cited_authors(corpus)[::-1]
    labels = [f"{sn.title()}, {ini}" for (sn, ini), _ in top]
    vals = [v for _, v in top]
    bars = ax.barh(labels, vals, color=col, height=0.68)
    for bar, v in zip(bars, vals):
        ax.text(v + max(vals) * 0.015, bar.get_y() + bar.get_height() / 2,
                f"{v:,}", va="center", fontsize=11, color=INK)
    ax.set_xlim(0, max(vals) * 1.17)
    ax.set_title(corpus, fontsize=12, fontweight="bold", color=INK, loc="left")
    ax.set_xlabel("Cited references within the corpus")
    ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
fig.tight_layout()
finish(fig, "fig_6_04_who_each_field_reads.png")


# ===========================================================================
# 6.05 — what TS reads, by neighbouring field (AS bar emphasized)
# ===========================================================================
b = A["6.4c_benchmarks_in_TSJ"]
order = sorted(b.items(), key=lambda x: x[1]["references"])
labels = [k for k, _ in order]
vals = [v["references"] for _, v in order]
cols = [TAN if "Adaptation" in k else SLATE for k in labels]
fig, ax = plt.subplots(figsize=(7.2, 3.6))
bars = ax.barh(labels, vals, color=cols, height=0.64)
for bar, v in zip(bars, vals):
    ax.text(v + max(vals) * 0.013, bar.get_y() + bar.get_height() / 2,
            f"{v:,}", va="center", ha="left", fontsize=12, color=INK)
ax.set_xlim(0, max(vals) * 1.16)
ax.set_xlabel("Cited references in TS-J (n = 318,442 parsed)")
ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
finish(fig, "fig_6_05_neighbouring_fields.png")


# ===========================================================================
# 6.06 — direction of flow, journal level
# ===========================================================================
led = A["6.5_ledger"]
rows = [("AS-J → TS journals", led["AS-J -> TS journals"]["per_10k_parsed_references"], TAN),
        ("AS-T → TS journals", led["AS-T -> TS journals"]["per_10k_parsed_references"], TAN_LIGHT),
        ("TS-J → AS journals", led["TS-J -> AS journals"]["per_10k_parsed_references"], SLATE)]
fig, ax = plt.subplots(figsize=(7.2, 2.9))
bars = ax.barh([r[0] for r in rows], [r[1] for r in rows],
               color=[r[2] for r in rows], height=0.58)
for bar, r in zip(bars, rows):
    ax.text(r[1] + 0.3, bar.get_y() + bar.get_height() / 2, f"{r[1]:.2f}",
            va="center", fontsize=12, color=INK)
ax.set_xlabel("Cross-citations per 10,000 parsed references")
ax.set_xlim(0, max(r[1] for r in rows) * 1.18)
ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
finish(fig, "fig_6_06_direction_of_flow.png")


# ===========================================================================
# 6.07 — self-citation baselines against cross-citation
# ===========================================================================
al = A["6.5_ledger"]["author_level"]
groups = ["Cites its OWN canon", "Cites the OTHER field's canon"]
ts_vals = [al["TS canon per 10k TS-J refs (self-reference baseline)"],
           al["AS canon per 10k TS-J refs"]]
as_vals = [al["AS canon per 10k AS-J refs (self-reference baseline)"],
           al["TS canon per 10k AS-J refs"]]
x = range(2); w = 0.36
fig, ax = plt.subplots(figsize=(7.2, 5.0))
b1 = ax.bar([i - w / 2 - 0.012 for i in x], ts_vals, w, color=SLATE,
            label="Translation Studies journals (TS-J)")
b2 = ax.bar([i + w / 2 + 0.012 for i in x], as_vals, w, color=TAN,
            label="Adaptation Studies journals (AS-J)")
for bars in (b1, b2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 9,
                f"{bar.get_height():.1f}", ha="center", fontsize=12, color=INK)
ax.set_xticks(list(x)); ax.set_xticklabels(groups)
ax.set_ylabel("References per 10,000 (normalised)")
ax.set_ylim(0, 585)
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.legend(frameon=False, loc="upper right")
ax.annotate("a 5.0 : 1 gap", xy=(1, 135), fontsize=12, color=INK2,
            ha="center", style="italic")
ax.annotate("", xy=(1 - w / 2, 100), xytext=(1 + w / 2, 100),
            arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.1))
finish(fig, "fig_6_07_selfcitation_baselines.png")


# ===========================================================================
# 6.08 — frontier vs core (lollipop)
# ===========================================================================
fv = A["6.6_frontier_vs_core"]
core = sorted(fv["core"].items(), key=lambda x: x[1]["references"])
front = sorted(fv["frontier"].items(), key=lambda x: x[1]["references"])
names = [k.split(",")[0] for k, _ in front] + [""] + [k.split(",")[0] for k, _ in core]
vals = [v["references"] for _, v in front] + [0] + [v["references"] for _, v in core]
cols = [TAN] * len(front) + ["none"] + [SLATE] * len(core)
fig, ax = plt.subplots(figsize=(7.2, 5.8))
ypos = range(len(names))
for y, v, c in zip(ypos, vals, cols):
    if c == "none":
        continue
    ax.plot([0, v], [y, y], color=c, lw=1.8, alpha=0.55, solid_capstyle="round")
    ax.plot(v, y, "o", color=c, ms=8, markeredgecolor="white", markeredgewidth=1.4)
    ax.text(v + 32, y, f"{v:,}", va="center", fontsize=11, color=INK)
ax.set_yticks(list(ypos)); ax.set_yticklabels(names)
ax.set_xlabel("Cited references within TS-J")
ax.set_xlim(0, max(vals) * 1.18)
ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
ax.text(max(vals) * 0.6, 1.0,
        "Frontier mean: 295 refs/author\nCore mean: 1,179 refs/author\nRatio 4.0 : 1",
        fontsize=12, color=INK2, va="center",
        bbox=dict(facecolor="#f5f2ec", edgecolor="none", pad=6))
finish(fig, "fig_6_08_frontier_vs_core.png")


# ===========================================================================
# 6.09 — thematic map of TS-J
# ===========================================================================
# Plotted from the frozen published values (Table 6.9) so that figure and
# table can never disagree; the rerun's Louvain partition differs slightly
# under newer library versions (see §6.6.2's robustness discussion).
T69 = [
    # (centrality, density, label, peripheral?, dx, dy, ha)
    (12.15, 3.59, "simultaneous\ninterpreting",              False,   0,  16, "center"),
    (11.29, 1.99, "translation",                             False,   0, -32, "center"),
    ( 9.03, 3.95, "audiovisual\ntranslation",                False,   0,  16, "center"),
    ( 8.21, 2.48, "translator\ntraining",                    False,   0, -44, "center"),
    ( 3.69, 3.76, "machine\ntranslation",                    False,   0,  16, "center"),
    ( 3.43, 0.80, "literary translation,\nadaptation, equivalence", True, 14, -10, "left"),
    ( 3.38, 2.04, "ideology",                                True, -12,   6, "right"),
    ( 1.26, 6.83, "translation studies,\nsociology of translation", True, 13, -6, "left"),
    ( 0.81, 4.49, "legal\ntranslation",                      True,  13,  -6, "left"),
    ( 0.57,11.01, "domestication",                           True,  13,  -6, "left"),
]
fig, ax = plt.subplots(figsize=(7.2, 5.6))
cmed, dmed = 3.56, 3.675   # medians of the published values
ax.axvline(cmed, color=MUTED, lw=0.9, ls=(0, (4, 3)))
ax.axhline(dmed, color=MUTED, lw=0.9, ls=(0, (4, 3)))
for c, d, lab, peripheral, dx, dy, ha in T69:
    col = TAN if peripheral else SLATE
    ax.scatter(c, d, s=340, color=col, alpha=0.6,
               edgecolor="white", linewidth=1.4, zorder=3)
    ax.annotate(lab, (c, d), textcoords="offset points", xytext=(dx, dy),
                ha=ha, va="center" if ha == "left" else "baseline",
                fontsize=10.5, color=INK, zorder=4, linespacing=1.05)
ax.set_xlim(-1.2, 14.2)
ax.set_ylim(-1.6, 13.2)
ax.set_xlabel("Callon centrality  →  relevance to the field")
ax.set_ylabel("Callon density  →  internal development")
for lbl, xy, ha, va in [("MOTOR", (0.985, 0.975), "right", "top"),
                        ("NICHE", (0.015, 0.975), "left", "top"),
                        ("EMERGING / DECLINING", (0.015, 0.02), "left", "bottom"),
                        ("BASIC / TRANSVERSAL", (0.985, 0.02), "right", "bottom")]:
    ax.annotate(lbl, xy=xy, xycoords="axes fraction", ha=ha, va=va,
                fontsize=10.5, color=MUTED, style="italic",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=1.6))
ax.grid(True, alpha=0.5); ax.set_axisbelow(True)
finish(fig, "fig_6_09_thematic_map.png")


# ===========================================================================
# 6.10 — two sovereignties (mirror hub)
# ===========================================================================
tsp = NW["TS-J"]["watched_term_placement"]
asp = NW["AS-J"]["watched_term_placement"]
cats = ["Its own term", "The other field's term"]
tsv = [tsp["translation"]["degree_centrality"], tsp["adaptation"]["degree_centrality"]]
asv = [asp["adaptation"]["degree_centrality"], asp["translation"]["degree_centrality"]]
x = range(2); w = 0.36
fig, ax = plt.subplots(figsize=(7.0, 4.4))
b1 = ax.bar([i - w / 2 - 0.012 for i in x], tsv, w, color=SLATE,
            label="TS-J keyword network")
b2 = ax.bar([i + w / 2 + 0.012 for i in x], asv, w, color=TAN,
            label="AS-J keyword network")
for bars, terms in ((b1, ["translation", "adaptation"]), (b2, ["adaptation", "translation"])):
    for bar, t in zip(bars, terms):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.018,
                f"{bar.get_height():.2f}\n{t}", ha="center", fontsize=11, color=INK)
ax.set_xticks(list(x)); ax.set_xticklabels(cats)
ax.set_ylabel("Degree centrality in the keyword network")
ax.set_ylim(0, 1.16)
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.legend(frameon=False, loc="upper right")
finish(fig, "fig_6_10_two_sovereignties.png")


# ===========================================================================
# 6.11 — two clocks
# ===========================================================================
def smooth(series, k=3):
    ys = sorted(int(y) for y in series)
    out = []
    for i, y in enumerate(ys):
        w_ = [series[str(ys[j])]["rate_pct"]
              for j in range(max(0, i - k // 2), min(len(ys), i + k // 2 + 1))]
        out.append((y, sum(w_) / len(w_)))
    return out

ts_f = smooth(RF["R2_clocks"]["TS-J fidelity/faithfulness"]["series"])
as_f = smooth(RF["R2_clocks"]["AS-J fidelity/faithfulness"]["series"])
fig, ax = plt.subplots(figsize=(7.2, 4.4))
ax.plot([y for y, _ in ts_f], [v for _, v in ts_f], color=SLATE, lw=2.4, label="TS-J")
ax.plot([y for y, _ in as_f], [v for _, v in as_f], color=TAN, lw=2.4, label="AS-J")
pk_ts = RF["R2_clocks"]["TS-J fidelity/faithfulness"]["peak_year_of_rate"]
pk_as = RF["R2_clocks"]["AS-J fidelity/faithfulness"]["peak_year_of_rate"]
for pk, col in [(pk_ts, SLATE), (pk_as, TAN)]:
    ax.axvline(pk, color=col, lw=1.0, ls=(0, (3, 3)), alpha=0.85)
ax.annotate("TS-J", (ts_f[-1][0], ts_f[-1][1]), textcoords="offset points",
            xytext=(7, 0), color=SLATE, fontsize=12, va="center")
ax.annotate("AS-J", (as_f[-1][0], as_f[-1][1]), textcoords="offset points",
            xytext=(7, 0), color=TAN, fontsize=12, va="center")
ax.annotate("13-year gap", xy=((pk_ts + pk_as) / 2, 7.55), ha="center",
            fontsize=12, color=INK2)
ax.annotate("", xy=(pk_ts, 7.1), xytext=(pk_as, 7.1),
            arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.1))
ax.set_xlabel("Publication year")
ax.set_ylabel("% of the year's documents engaging fidelity")
ax.yaxis.set_major_formatter(PercentFormatter())
ax.grid(True, alpha=0.5); ax.set_axisbelow(True)
ax.set_xlim(1990, 2026)
finish(fig, "fig_6_11_two_clocks.png")


# ===========================================================================
# 6.12 — RPYS: two archives
# ===========================================================================
fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.8), sharex=True)
for ax, corpus, col, marks in [
        (axes[0], "TS-J", SLATE, {1959: "Jakobson", 1972: "Holmes", 1978: "Halliday"}),
        (axes[1], "AS-J", TAN, {1957: "Bluestone", 1984: "Andrew"})]:
    dev = RF["R3_rpys"][corpus]["full_deviation"]
    years = [int(y) for y in dev if 1935 <= int(y) <= 1990]
    vals = [dev[str(y)] for y in years]
    ax.bar(years, vals, color=col, width=0.82)
    ax.axhline(0, color=MUTED, lw=0.9)
    for y, lab in marks.items():
        if y in years:
            ax.annotate(f"{lab}\n{y}", (y, dev[str(y)]), textcoords="offset points",
                        xytext=(0, 7), ha="center", fontsize=11, color=INK)
    ax.set_ylabel(f"{corpus}\ndeviation")
    ax.grid(True, axis="y", alpha=0.5); ax.set_axisbelow(True)
    lo, hi = min(vals), max(vals)
    ax.set_ylim(lo * 1.15, hi * 1.45)
axes[1].set_xlabel("Publication year of the cited reference")
finish(fig, "fig_6_12_two_archives.png")


# ===========================================================================
# 6.13 — author countries
# ===========================================================================
COUNTRY_FIX = {"USA": "USA", "ENGLAND": "UK", "SCOTLAND": "UK", "WALES": "UK",
               "NORTH IRELAND": "UK", "PEOPLES R CHINA": "China",
               "U ARAB EMIRATES": "UAE"}

def countries(recs, n=12):
    c = Counter()
    for r in recs:
        seen = set()
        for addr in r.get("C1", []):
            parts = [p.strip() for p in addr.split(",")]
            if parts:
                ctry = parts[-1].upper().rstrip(".")
                ctry = re.sub(r"\b\d{4,}\b", "", ctry).strip()
                # D17 (22 Sep 2026): 'MD 21218 USA' and the bare 'MD 21218'
                # of older records are both the USA, not a state.
                if ctry.endswith("USA") or re.fullmatch(r"[A-Z]{2}", ctry):
                    ctry = "USA"
                ctry = COUNTRY_FIX.get(ctry, ctry.title())
                if ctry and len(ctry) > 1:
                    seen.add(ctry)
        for ctry in seen:
            c[ctry] += 1
    return c.most_common(n)

fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6))
for ax, corpus, col in [(axes[0], "TS-J", SLATE), (axes[1], "AS-J", TAN)]:
    top = countries(C[corpus])[::-1]
    vals = [v for _, v in top]
    bars = ax.barh([k for k, _ in top], vals, color=col, height=0.68)
    for bar, v in zip(bars, vals):
        ax.text(v + max(vals) * 0.02, bar.get_y() + bar.get_height() / 2,
                f"{v:,}", va="center", fontsize=11, color=INK)
    ax.set_xlim(0, max(vals) * 1.18)
    ax.set_title(corpus, fontsize=12, fontweight="bold", color=INK, loc="left")
    ax.set_xlabel("Documents with an author based there")
    ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
fig.tight_layout()
finish(fig, "fig_6_13_author_countries.png")

print("\nAll done:", len(saved), "figures")

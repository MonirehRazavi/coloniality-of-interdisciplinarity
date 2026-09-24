"""
make_figures.py — Chapter 6 figures
===================================
Produces the print figures for §§6.4–6.9 at 300 dpi.

DESIGN NOTES (so the choices are defensible, not decorative)
------------------------------------------------------------
* Two-colour categorical scheme throughout: Translation Studies = blue
  #2a78d6, Adaptation Studies = orange #eb6834, plus aqua #1baf7a where a
  third class is unavoidable. This set was validated for colour-vision
  deficiency (worst adjacent pair deltaE 9.2 deutan, 27.6 normal vision) so
  the figures survive both colour-blind readers and greyscale printing of the
  bound thesis.
* Every series is ALSO directly labelled, so identity never depends on colour
  alone — necessary because a printed dissertation may be photocopied.
* Recessive grid, no chartjunk, no dual axes.
* Serif type to sit with thesis body text.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis_outputs")
FIG = os.path.join(os.path.dirname(__file__), "..", "figs_out", "original_set")
os.makedirs(FIG, exist_ok=True)

TS_BLUE, AS_ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8880"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "font.size": 9,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": INK2, "ytick.color": INK2,
    "grid.color": "#e6e5e1", "grid.linewidth": 0.6,
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
    "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlelocation": "left",
})

A = json.load(open(os.path.join(OUT, "ALL_RESULTS.json")))
RF = json.load(open(os.path.join(OUT, "REFINED_RESULTS.json")))
NW = json.load(open(os.path.join(OUT, "NETWORK_RESULTS.json")))
saved = []


def finish(fig, name, caption):
    p = os.path.join(FIG, name)
    fig.savefig(p)
    plt.close(fig)
    saved.append((name, caption))
    print(f"  saved {name}")


# ---------------------------------------------------------------------------
# FIGURE 6.3 — §6.4(c) Benchmark: how much of TS-J's reference record goes to
# each neighbouring field. The comparison class is the whole point.
# ---------------------------------------------------------------------------
b = A["6.4c_benchmarks_in_TSJ"]
order = sorted(b.items(), key=lambda x: x[1]["references"])
labels = [k for k, _ in order]
vals = [v["references"] for _, v in order]
cols = [AS_ORANGE if "Adaptation" in k else TS_BLUE for k in labels]

fig, ax = plt.subplots(figsize=(6.6, 3.1))
bars = ax.barh(labels, vals, color=cols, height=0.62)
for bar, v in zip(bars, vals):
    ax.text(v + max(vals) * 0.012, bar.get_y() + bar.get_height() / 2,
            f"{v:,}", va="center", ha="left", fontsize=8.5, color=INK)
ax.set_xlim(0, max(vals) * 1.15)
ax.set_xlabel("Cited references in TS-J (n = 318,442 parsed)")
ax.set_title("Figure 6.3  What Translation Studies cites, by neighbouring field")
ax.xaxis.grid(True); ax.set_axisbelow(True)
ax.tick_params(axis="y", length=0)
finish(fig, "fig_6_3_benchmarks.png",
       "Cited references in TS-J to the canonical authors of five neighbouring "
       "fields. Adaptation Studies (orange) is cited less than sociology, "
       "cognitive science and linguistics, and more than the film-studies canon.")


# ---------------------------------------------------------------------------
# FIGURE 6.4 — theasymmetry: each field's self-citation baseline against its
# citation of the other. The baselines are what make the gap interpretable.
# ---------------------------------------------------------------------------
al = A["6.5_ledger"]["author_level"]
groups = ["Cites its OWN canon", "Cites the OTHER field's canon"]
ts_vals = [al["TS canon per 10k TS-J refs (self-reference baseline)"],
           al["AS canon per 10k TS-J refs"]]
as_vals = [al["AS canon per 10k AS-J refs (self-reference baseline)"],
           al["TS canon per 10k AS-J refs"]]

x = range(len(groups)); w = 0.36
fig, ax = plt.subplots(figsize=(6.0, 3.4))
b1 = ax.bar([i - w / 2 - 0.01 for i in x], ts_vals, w, color=TS_BLUE,
            label="Translation Studies journals (TS-J)")
b2 = ax.bar([i + w / 2 + 0.01 for i in x], as_vals, w, color=AS_ORANGE,
            label="Adaptation Studies journals (AS-J)")
for bars in (b1, b2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8,
                f"{bar.get_height():.1f}", ha="center", fontsize=8.5, color=INK)
ax.set_xticks(list(x)); ax.set_xticklabels(groups)
ax.set_ylabel("References per 10,000 (normalised)")
ax.set_ylim(0, 560)
ax.set_title("Figure 6.4  Near-identical self-citation, radically unequal cross-citation")
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.legend(frameon=False, loc="upper right", fontsize=8.5)
ax.annotate("a 5.0 : 1 gap", xy=(1, 130), fontsize=9, color=INK2, ha="center",
            style="italic")
ax.annotate("", xy=(1 - w/2, 100), xytext=(1 + w/2, 100),
            arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.9))
finish(fig, "fig_6_4_asymmetry.png",
       "Each field cites its own canon at almost the same intensity (491 vs 430 "
       "per 10,000 references), which rules out a difference in citation culture. "
       "Cross-citation is asymmetric by a factor of five.")


# ---------------------------------------------------------------------------
# FIGURE 6.5 — journal-level directional ledger
# ---------------------------------------------------------------------------
led = A["6.5_ledger"]
rows = [("AS-J → TS journals", led["AS-J -> TS journals"]["per_10k_parsed_references"], AS_ORANGE),
        ("AS-T → TS journals", led["AS-T -> TS journals"]["per_10k_parsed_references"], AQUA),
        ("TS-J → AS journals", led["TS-J -> AS journals"]["per_10k_parsed_references"], TS_BLUE)]
fig, ax = plt.subplots(figsize=(6.2, 2.5))
bars = ax.barh([r[0] for r in rows], [r[1] for r in rows],
               color=[r[2] for r in rows], height=0.55)
for bar, r in zip(bars, rows):
    ax.text(r[1] + 0.35, bar.get_y() + bar.get_height() / 2, f"{r[1]:.2f}",
            va="center", fontsize=8.5, color=INK)
ax.set_xlabel("Cross-citations per 10,000 parsed references")
ax.set_xlim(0, max(r[1] for r in rows) * 1.2)
ax.set_title("Figure 6.5  The direction of flow between the two literatures")
ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
finish(fig, "fig_6_5_direction.png",
       "Journal-to-journal citation, normalised by reference volume. Adaptation "
       "Studies journals cite Translation Studies journals 13.3 times more "
       "intensively than the reverse.")


# ---------------------------------------------------------------------------
# FIGURE 6.6 — frontier vs core inside TS-J
# ---------------------------------------------------------------------------
fv = A["6.6_frontier_vs_core"]
core = sorted(fv["core"].items(), key=lambda x: x[1]["references"])
front = sorted(fv["frontier"].items(), key=lambda x: x[1]["references"])
names = [k.split(",")[0] for k, _ in front] + [""] + [k.split(",")[0] for k, _ in core]
vals = [v["references"] for _, v in front] + [0] + [v["references"] for _, v in core]
cols = [AS_ORANGE] * len(front) + ["none"] + [TS_BLUE] * len(core)

fig, ax = plt.subplots(figsize=(6.2, 4.2))
ypos = range(len(names))
for y, v, c in zip(ypos, vals, cols):
    if c == "none":
        continue
    ax.plot([0, v], [y, y], color=c, lw=1.4, alpha=0.55, solid_capstyle="round")
    ax.plot(v, y, "o", color=c, ms=6.5, markeredgecolor="white", markeredgewidth=1.2)
    ax.text(v + 30, y, f"{v:,}", va="center", fontsize=8, color=INK)
ax.set_yticks(list(ypos)); ax.set_yticklabels(names)
ax.set_xlabel("Cited references within TS-J")
ax.set_xlim(0, max(vals) * 1.18)
ax.set_title("Figure 6.6  The expansionist frontier (orange) against the\ninstitutional core (blue), inside TS's own citation record")
ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
ax.text(max(vals) * 0.62, 1.0, "Frontier mean: 295 refs/author\nCore mean: 1,179 refs/author\nRatio 4.0 : 1",
        fontsize=8.5, color=INK2, va="center",
        bbox=dict(facecolor="#f5f4f0", edgecolor="none", pad=5))
finish(fig, "fig_6_6_frontier_core.png",
       "Local citation of the seven expansionist critics named in Chapter 5 "
       "against seven institutional-core theorists, within TS-J itself. "
       "Bassnett is excluded as unclassifiable and reported separately (818).")


# ---------------------------------------------------------------------------
# FIGURE 6.7 — thematic map of TS-J (Callon centrality x density)
# ---------------------------------------------------------------------------
th = NW["TS-J"]["themes"]
fig, ax = plt.subplots(figsize=(6.4, 4.6))
cmed = th[0]["median_centrality"]; dmed = th[0]["median_density"]
ax.axvline(cmed, color=MUTED, lw=0.8, ls=(0, (4, 3)))
ax.axhline(dmed, color=MUTED, lw=0.8, ls=(0, (4, 3)))
maxw = max(x["documents_weight"] for x in th)
# Alternate label placement above/below in reading order so neighbouring
# points in the crowded lower-left do not overprint one another.
for i, t in enumerate(sorted(th, key=lambda z: (z["centrality"], z["density"]))):
    peripheral = t["quadrant"] in ("Emerging/Declining", "Niche")
    col = AS_ORANGE if peripheral else TS_BLUE
    sz = 40 + 900 * (t["documents_weight"] / maxw)
    ax.scatter(t["centrality"], t["density"], s=sz, color=col, alpha=0.5,
               edgecolor="white", linewidth=1.2, zorder=3)
    dy = 15 if i % 2 == 0 else -20
    ha = "center"
    if t["centrality"] > 10:      # keep right-edge labels inside the axes
        ha, dx = "right", 8
    elif t["centrality"] < 0.6:
        ha, dx = "left", -8
    else:
        dx = 0
    ax.annotate(t["label"].split(",")[0], (t["centrality"], t["density"]),
                textcoords="offset points", xytext=(dx, dy), ha=ha,
                fontsize=7.2, color=INK, zorder=4)
xs = [t["centrality"] for t in th]; ys = [t["density"] for t in th]
ax.set_xlim(min(xs) - 1.4, max(xs) + 1.8)
ax.set_ylim(min(ys) - 3.0, max(ys) + 2.4)
ax.set_xlabel("Callon centrality  →  relevance to the field")
ax.set_ylabel("Callon density  →  internal development")
ax.set_title("Figure 6.7  Thematic map of Translation Studies journals")
for lbl, xy, ha, va in [("MOTOR", (0.985, 0.975), "right", "top"),
                        ("NICHE", (0.015, 0.975), "left", "top"),
                        ("EMERGING / DECLINING", (0.015, 0.02), "left", "bottom"),
                        ("BASIC / TRANSVERSAL", (0.985, 0.02), "right", "bottom")]:
    ax.annotate(lbl, xy=xy, xycoords="axes fraction", ha=ha, va=va, fontsize=7.5,
                color=MUTED, style="italic",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.75, pad=1.5))
ax.grid(True, alpha=0.5); ax.set_axisbelow(True)
finish(fig, "fig_6_7_thematic_map.png",
       "Louvain themes plotted on Callon centrality x density. The applied "
       "clusters (audiovisual translation, interpreting, training, machine "
       "translation) hold the motor quadrant; equivalence, multimodality and "
       "intersemiotic translation sit in the emerging/declining quadrant.")


# ---------------------------------------------------------------------------
# FIGURE 6.8 — the mirror hub: own term vs other term in each network
# ---------------------------------------------------------------------------
tsp = NW["TS-J"]["watched_term_placement"]
asp = NW["AS-J"]["watched_term_placement"]
cats = ["Its own term", "The other field's term"]
tsv = [tsp["translation"]["degree_centrality"], tsp["adaptation"]["degree_centrality"]]
asv = [asp["adaptation"]["degree_centrality"], asp["translation"]["degree_centrality"]]
x = range(2); w = 0.36
fig, ax = plt.subplots(figsize=(5.8, 3.2))
b1 = ax.bar([i - w / 2 - 0.01 for i in x], tsv, w, color=TS_BLUE, label="TS-J keyword network")
b2 = ax.bar([i + w / 2 + 0.01 for i in x], asv, w, color=AS_ORANGE, label="AS-J keyword network")
for bars, terms in ((b1, ["translation", "adaptation"]), (b2, ["adaptation", "translation"])):
    for bar, t in zip(bars, terms):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
                f"{bar.get_height():.2f}\n{t}", ha="center", fontsize=7.6, color=INK)
ax.set_xticks(list(x)); ax.set_xticklabels(cats)
ax.set_ylabel("Degree centrality in the keyword network")
ax.set_ylim(0, 1.12)
ax.set_title("Figure 6.8  Two sovereignties: each field's own term is its hub")
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=8.5, loc="upper right")
finish(fig, "fig_6_8_mirror_hub.png",
       "Degree centrality of 'translation' and 'adaptation' in each field's own "
       "keyword co-occurrence network. Each term is near-total in its home "
       "network and peripheral in the other's.")


# ---------------------------------------------------------------------------
# FIGURE 6.9 — two clocks: fidelity engagement rate over time
# ---------------------------------------------------------------------------
def smooth(series, k=3):
    ys = sorted(int(y) for y in series)
    out = []
    for i, y in enumerate(ys):
        w = [series[str(ys[j])]["rate_pct"]
             for j in range(max(0, i - k // 2), min(len(ys), i + k // 2 + 1))]
        out.append((y, sum(w) / len(w)))
    return out


ts_f = smooth(RF["R2_clocks"]["TS-J fidelity/faithfulness"]["series"])
as_f = smooth(RF["R2_clocks"]["AS-J fidelity/faithfulness"]["series"])
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot([y for y, _ in ts_f], [v for _, v in ts_f], color=TS_BLUE, lw=2, label="TS-J")
ax.plot([y for y, _ in as_f], [v for _, v in as_f], color=AS_ORANGE, lw=2, label="AS-J")
pk_ts = RF["R2_clocks"]["TS-J fidelity/faithfulness"]["peak_year_of_rate"]
pk_as = RF["R2_clocks"]["AS-J fidelity/faithfulness"]["peak_year_of_rate"]
for pk, col, lab in [(pk_ts, TS_BLUE, "TS peak 2008"), (pk_as, AS_ORANGE, "AS peak 2021")]:
    ax.axvline(pk, color=col, lw=0.9, ls=(0, (3, 3)), alpha=0.8)
ax.annotate("TS-J", (ts_f[-1][0], ts_f[-1][1]), textcoords="offset points",
            xytext=(6, 0), color=TS_BLUE, fontsize=9, va="center")
ax.annotate("AS-J", (as_f[-1][0], as_f[-1][1]), textcoords="offset points",
            xytext=(6, 0), color=AS_ORANGE, fontsize=9, va="center")
ax.annotate("13-year gap", xy=((pk_ts + pk_as) / 2, 7.4), ha="center",
            fontsize=8.5, color=INK2)
ax.annotate("", xy=(pk_ts, 7.0), xytext=(pk_as, 7.0),
            arrowprops=dict(arrowstyle="<->", color=MUTED, lw=0.9))
ax.set_xlabel("Publication year"); ax.set_ylabel("% of the year's documents engaging fidelity")
ax.yaxis.set_major_formatter(PercentFormatter())
ax.set_title("Figure 6.9  Two clocks: engagement with fidelity, as a share of each\nfield's annual output (3-year moving average)")
ax.grid(True, alpha=0.5); ax.set_axisbelow(True)
ax.set_xlim(1990, 2025)
finish(fig, "fig_6_9_two_clocks.png",
       "Rate-normalised, so corpus growth cannot generate the pattern. AS-J's "
       "fidelity discourse peaks 13 years after TS-J's — and at four times the "
       "intensity.")


# ---------------------------------------------------------------------------
# FIGURE 6.10 — RPYS: two foundational archives
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 1, figsize=(6.6, 5.0), sharex=True)
for ax, corpus, col, marks in [
        (axes[0], "TS-J", TS_BLUE, {1959: "Jakobson", 1972: "Holmes", 1978: "Halliday"}),
        # 1977's largest cited work is an unattributed record, so it is left
        # unlabelled rather than credited to a text it does not represent.
        (axes[1], "AS-J", AS_ORANGE, {1957: "Bluestone", 1984: "Andrew"})]:
    dev = RF["R3_rpys"][corpus]["full_deviation"]
    years = [int(y) for y in dev if 1935 <= int(y) <= 1990]
    vals = [dev[str(y)] for y in years]
    ax.bar(years, vals, color=col, width=0.8)
    ax.axhline(0, color=MUTED, lw=0.8)
    for y, lab in marks.items():
        if y in years:
            ax.annotate(f"{lab}\n{y}", (y, dev[str(y)]), textcoords="offset points",
                        xytext=(0, 6), ha="center", fontsize=7.4, color=INK)
    ax.set_ylabel(f"{corpus}\ndeviation")
    ax.grid(True, axis="y", alpha=0.5); ax.set_axisbelow(True)
    lo, hi = min(vals), max(vals)
    ax.set_ylim(lo * 1.15, hi * 1.42)      # headroom so labels clear the bars
axes[0].set_title("Figure 6.10  Reference Publication Year Spectroscopy:\ntwo separate foundational archives")
axes[1].set_xlabel("Publication year of the cited reference")
finish(fig, "fig_6_10_rpys.png",
       "Deviation of each year's cited-reference count from the surrounding "
       "5-year median. TS-J spikes at 1959 (Jakobson) and 1972 (Holmes); AS-J "
       "at 1957 (Bluestone) and 1984 (Andrew). Neither peak appears in the "
       "other's spectrum.")


# ---------------------------------------------------------------------------
print("\nFigure manifest:")
man = [{"file": n, "caption": c} for n, c in saved]
json.dump(man, open(os.path.join(FIG, "manifest.json"), "w"), indent=2)
for n, c in saved:
    print(f"  {n}")

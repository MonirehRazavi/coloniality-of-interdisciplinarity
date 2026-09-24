"""
make_labelled_maps.py — thematic maps with keywords written beside the circles
===============================================================================
Emits four figures from one run of one procedure (analysis_three_corpora.py):

  fig_themes_TSJ.png    Translation Studies journals     slate  #3F6E96
  fig_themes_ASJ.png    Adaptation Studies journals      tan    #C08030
  fig_themes_AST.png    dispersed adaptation literature  light  #E4C08C
  fig_themes_combined_standardised.png   all three on one pair of axes

The first three are standalone, each a full text-block wide, so every cluster
can carry its keywords in place rather than a number keyed to a list.

The fourth puts all thirty clusters on one plot, which raw Callon values do
not permit: centrality is a SUM over boundary-crossing edges and therefore
scales with network size, so AS-J's 124-edge network would occupy the left
quarter of a shared axis whatever the field is like. Each axis is therefore
expressed in units of its own corpus's interquartile range, centred on its
own corpus's median — the same median that already defines the quadrants.
A theme's position then means "central, or peripheral, for its own field",
which is a comparable statement; a raw magnitude is not.

Open circles mark clusters belonging to another sense of the word. Only the
keyword-defined corpus has any.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.transforms import Bbox

for f in ["Tinos-Regular.ttf", "Tinos-Bold.ttf", "Tinos-Italic.ttf", "Tinos-BoldItalic.ttf"]:
    p = os.path.join("/usr/share/fonts/truetype/croscore", f)
    if os.path.exists(p):
        font_manager.fontManager.addfont(p)

SLATE, TAN, TAN_LIGHT = "#3F6E96", "#C08030", "#E4C08C"
TAN_LIGHT_INK = "#A87C34"          # readable text version of the light tan
GREY_EDGE = "#8E8C85"
INK, INK2, MUTED, GRID = "#1a1a1a", "#4a4a4a", "#8a8880", "#e6e5e1"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figs_out", "thematic_maps")
os.makedirs(OUT, exist_ok=True)

# Identical to make_figures_palette.py, so this set sits with the others.
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
ANNOT = 10.5        # in-figure annotation size used by every Chapter 6 figure

TARGET_W_IN = 6.5          # matches the width band of the chapter's other figures
DPI = 300


def pad_to_width(path, target_in=TARGET_W_IN, dpi=DPI):
    """Pad the tight-cropped PNG back out to the authored canvas width.

    savefig(bbox="tight") crops to whatever ink a figure happens to contain,
    so a set of figures drawn at one canvas size comes out at several
    different widths. Anything inserted at a common width in the document
    then shows its type at a different size from its neighbours. Padding to
    a single width means every figure in this set renders 12 pt type as
    12 pt when placed at 7.2 in, and proportionally otherwise.
    """
    from PIL import Image
    target = int(round(target_in * dpi))
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if w < target:
        canvas = Image.new("RGB", (target, h), "white")
        canvas.paste(im, ((target - w) // 2, 0))
        im = canvas
    elif w > target:
        im = im.resize((target, int(round(h * target / w))), Image.LANCZOS)
    im.save(path, dpi=(dpi, dpi))


R = json.load(open(os.path.join(OUT, "..", "..", "analysis_outputs", "THREE_CORPORA_THEMES.json")))

OTHER_SENSE = {
    "climate change, politics, resilience",
    "health, model, perceptions",
    "identity, migration, culture",
    "scale, reliability, validity",
}

LABEL = {
 # TS-J
 "translation, language, english": "translation, language,\nEnglish",
 "audiovisual translation, subtitling, dubbing": "audiovisual translation,\nsubtitling, dubbing",
 "translator training, quality, translation competence": "translator training,\nquality, competence",
 "simultaneous interpreting, performance, cognitive load": "simultaneous interpreting,\nperformance",
 "literary translation, retranslation, adaptation": "literary translation, retranslation,\nadaptation, equivalence,\nintersemiotic translation",
 "interpreting, ethics, interpreter training": "interpreting, ethics,\ninterpreter training",
 "ideology, discourse, news translation": "ideology, discourse,\nnews translation",
 "machine translation, post-editing, translation technology": "machine translation,\npost-editing",
 "translation studies, translation history, sociology of translation": "translation studies,\nsociology of translation",
 "legal translation, institutional translation, translation policy": "legal translation,\npolicy",
 "domestication, foreignization, cultural references": "domestication,\nforeignization",
 # AS-J
 "adaptation, translation, intertextuality": "adaptation, translation,\nintertextuality, fidelity",
 "film, gender, television": "film, gender,\ntelevision",
 "shakespeare, appropriation, hamlet": "Shakespeare,\nappropriation",
 "adaptation studies, film adaptation, cinema": "adaptation studies,\nfilm adaptation",
 "nostalgia, intermediality, remediation": "intermediality,\nremediation",
 "horror, radio drama, film noir": "horror,\nfilm noir",
 "othello, william shakespeare, desdemona": "Othello,\nDesdemona",
 "adaptation theory, jane austen": "adaptation theory,\nAusten",
 "authorship, screenwriting": "authorship,\nscreenwriting",
 "kubrick, masculinity": "Kubrick,\nmasculinity",
 "dracula, vampire": "Dracula,\nvampire",
 # AS-T
 "adaptation, translation, film adaptation": "adaptation, film adaptation,\nShakespeare, intertextuality",
 "climate change, politics, resilience": "climate change,\nresilience",
 "communication, media, social media": "communication,\nmedia",
 "identity, migration, culture": "migration,\nacculturation",
 "health, model, perceptions": "health, stress,\nadjustment",
 "gender, women, race": "gender, women,\nrace",
 "education, history, covid-19": "education, history,\nmemory",
 "scale, reliability, validity": "scale, reliability,\nvalidity",
}

SHORT = {k: v.replace("\n", " ") for k, v in LABEL.items()}
SHORT.update({
 "literary translation, retranslation, adaptation": "literary translation,\nadaptation, equivalence",
 "adaptation, translation, intertextuality": "adaptation, translation,\nintertextuality",
 "adaptation, translation, film adaptation": "adaptation,\nfilm adaptation",
 "simultaneous interpreting, performance, cognitive load": "simultaneous\ninterpreting",
 "audiovisual translation, subtitling, dubbing": "audiovisual\ntranslation",
 "translator training, quality, translation competence": "translator\ntraining",
 "machine translation, post-editing, translation technology": "machine\ntranslation",
 "translation studies, translation history, sociology of translation": "translation studies,\nsociology",
 "interpreting, ethics, interpreter training": "interpreting,\nethics",
 "ideology, discourse, news translation": "ideology,\ndiscourse",
 "legal translation, institutional translation, translation policy": "legal\ntranslation",
 "domestication, foreignization, cultural references": "domestication",
 "translation, language, english": "translation,\nlanguage",
 "adaptation studies, film adaptation, cinema": "adaptation studies,\nfilm adaptation",
 "communication, media, social media": "communication",
 "education, history, covid-19": "education,\nhistory",
 "gender, women, race": "gender, women",
 "film, gender, television": "film, gender,\ntelevision",
})

CAND = [(14, 0, "left", "center"), (-14, 0, "right", "center"),
        (0, 15, "center", "bottom"), (0, -15, "center", "top"),
        (12, 12, "left", "bottom"), (-12, 12, "right", "bottom"),
        (12, -12, "left", "top"), (-12, -12, "right", "top"),
        (26, 0, "left", "center"), (-26, 0, "right", "center"),
        (0, 30, "center", "bottom"), (0, -30, "center", "top"),
        (26, 22, "left", "bottom"), (-26, 22, "right", "bottom"),
        (26, -22, "left", "top"), (-26, -22, "right", "top"),
        (44, 0, "left", "center"), (-44, 0, "right", "center"),
        (0, 46, "center", "bottom"), (0, -46, "center", "top"),
        (44, 34, "left", "bottom"), (-44, 34, "right", "bottom"),
        (44, -34, "left", "top"), (-44, -34, "right", "top"),
        (66, 0, "left", "center"), (-66, 0, "right", "center"),
        (0, 66, "center", "bottom"), (0, -66, "center", "top")]


def place(ax, fig, items, fs=9.5, extra=()):
    r = fig.canvas.get_renderer()
    taken = list(extra)
    for (x, y, _t, _c, rad, _it) in items:
        px, py = ax.transData.transform((x, y))
        taken.append(Bbox.from_bounds(px - rad, py - rad, 2 * rad, 2 * rad))
    ab = ax.get_window_extent()
    for (x, y, txt, col, rad, ital) in items:
        ok = False
        for dx, dy, ha, va in CAND:
            ox = dx + (rad * .7 if dx > 0 else -rad * .7 if dx < 0 else 0)
            oy = dy + (rad * .7 if dy > 0 else -rad * .7 if dy < 0 else 0)
            t = ax.annotate(txt, (x, y), textcoords="offset points", xytext=(ox, oy),
                            ha=ha, va=va, fontsize=fs, color=col, zorder=6,
                            linespacing=1.08, style="italic" if ital else "normal",
                            bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=1.1))
            bb = t.get_window_extent(r).expanded(1.03, 1.10)
            if (bb.x0 >= ab.x0 - 1 and bb.x1 <= ab.x1 + 1 and bb.y0 >= ab.y0 - 1
                    and bb.y1 <= ab.y1 + 1 and not any(bb.overlaps(b) for b in taken)):
                taken.append(bb); ok = True; break
            t.remove()
        if not ok:
            t = ax.annotate(txt, (x, y), textcoords="offset points",
                            xytext=(rad * .7 + 14, 0), ha="left", va="center",
                            fontsize=fs, color=col, zorder=6, linespacing=1.08,
                            style="italic" if ital else "normal",
                            bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=1.1))
            taken.append(t.get_window_extent(r))


def corners(ax, fig, small=False):
    out = []
    for lbl, xy, ha, va in [("MOTOR", (0.988, 0.978), "right", "top"),
                            ("NICHE", (0.012, 0.978), "left", "top"),
                            ("EMERGING / DECLINING", (0.012, 0.018), "left", "bottom"),
                            ("BASIC / TRANSVERSAL", (0.988, 0.018), "right", "bottom")]:
        out.append(ax.annotate(lbl, xy=xy, xycoords="axes fraction", ha=ha, va=va,
                               fontsize=9 if small else ANNOT, color=MUTED,
                               style="italic", zorder=2,
                               bbox=dict(facecolor="white", edgecolor="none",
                                         alpha=0.85, pad=1.4)))
    return out


# =========================================================================
# 1–3. three standalone maps, keywords written beside the circles
# =========================================================================
SPEC = [("TS-J", SLATE, SLATE, "Translation Studies journals", "fig_themes_TSJ.png"),
        ("AS-J", TAN, TAN, "Adaptation Studies journals", "fig_themes_ASJ.png"),
        ("AS-T", TAN_LIGHT, TAN_LIGHT_INK, "the dispersed adaptation literature",
         "fig_themes_AST.png")]

for corpus, fill, inkc, descr, fname in SPEC:
    th = R[corpus]["themes"]
    fig, ax = plt.subplots(figsize=(6.6, 7.7))
    fig.subplots_adjust(left=0.112, right=0.985, top=0.99, bottom=0.078)
    cmed, dmed = th[0]["median_centrality"], th[0]["median_density"]
    ax.axvline(cmed, color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.axhline(dmed, color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)

    cs = [t["centrality"] for t in th]; ds = [t["density"] for t in th]
    rx, ry = max(cs) - min(cs), max(ds) - min(ds)
    ax.set_xlim(min(cs) - rx * .32 - .25, max(cs) + rx * .32 + .25)
    ax.set_ylim(min(ds) - ry * .19 - .25, max(ds) + ry * .22 + .25)

    maxw = max(t["documents_weight"] for t in th)
    items = []
    for t in sorted(th, key=lambda t: -t["documents_weight"]):
        other = t["label"] in OTHER_SENSE
        s = 70 + 880 * (t["documents_weight"] / maxw)
        if other:
            ax.scatter(t["centrality"], t["density"], s=s, facecolor="white",
                       edgecolor=GREY_EDGE, linewidth=1.35, zorder=3)
        else:
            ax.scatter(t["centrality"], t["density"], s=s, color=fill, alpha=0.70,
                       edgecolor="white", linewidth=1.3, zorder=3)
        items.append((t["centrality"], t["density"], LABEL.get(t["label"], t["label"].replace(", ", ",\n")),
                      GREY_EDGE if other else INK, (s ** .5) / 2 * 1.06, other))

    ax.set_xlabel("Callon centrality  →  relevance to the corpus")
    ax.set_ylabel("Callon density  →  internal development")
    ax.grid(True, alpha=0.55); ax.set_axisbelow(True)
    # No title inside the image: the chapter's figures are APA, with the
    # figure number and title set as document text above the image.
    fig.canvas.draw()
    cbx = corners(ax, fig)
    fig.canvas.draw()
    _r = fig.canvas.get_renderer()
    place(ax, fig, items, fs=ANNOT,
          extra=[c.get_window_extent(_r).expanded(1.2, 1.2) for c in cbx])
    if corpus == "AS-T":
        ax.legend(handles=[Line2D([], [], marker="o", ls="", markersize=9,
                                  markerfacecolor="white", markeredgecolor=GREY_EDGE,
                                  markeredgewidth=1.35,
                                  label="another sense of the word")],
                  loc="upper center", bbox_to_anchor=(0.5, -0.105),
                  frameon=False, fontsize=ANNOT, handletextpad=0.5)
        fig.subplots_adjust(bottom=0.145)
    fig.savefig(os.path.join(OUT, fname))
    plt.close(fig)
    pad_to_width(os.path.join(OUT, fname))
    print("saved", fname)


# =========================================================================
# 4. all thirty clusters on one pair of axes, standardised within corpus
# =========================================================================
fig, ax = plt.subplots(figsize=(6.6, 8.0))
fig.subplots_adjust(left=0.108, right=0.985, top=0.99, bottom=0.112)
ax.axvline(0, color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)
ax.axhline(0, color=MUTED, lw=0.9, ls=(0, (4, 3)), zorder=1)

allpts, maxw_all = [], max(t["documents_weight"]
                          for c in R for t in R[c]["themes"])
for corpus, fill, inkc, descr, _ in SPEC:
    th = R[corpus]["themes"]
    cs = np.array([t["centrality"] for t in th])
    ds = np.array([t["density"] for t in th])
    cmed, dmed = th[0]["median_centrality"], th[0]["median_density"]
    ciqr = np.subtract(*np.percentile(cs, [75, 25])) or 1.0
    diqr = np.subtract(*np.percentile(ds, [75, 25])) or 1.0
    for t in th:
        x = (t["centrality"] - cmed) / ciqr
        y = (t["density"] - dmed) / diqr
        allpts.append((x, y, t, corpus, fill, inkc))

for x, y, t, corpus, fill, inkc in sorted(allpts, key=lambda p: -p[2]["documents_weight"]):
    other = t["label"] in OTHER_SENSE
    s = 55 + 700 * (t["documents_weight"] / maxw_all) ** 0.62
    if other:
        ax.scatter(x, y, s=s, facecolor="white", edgecolor=GREY_EDGE,
                   linewidth=1.3, zorder=3)
    else:
        ax.scatter(x, y, s=s, color=fill, alpha=0.70, edgecolor="white",
                   linewidth=1.2, zorder=3)

items = [(x, y, SHORT.get(t["label"], t["label"].split(",")[0]), GREY_EDGE if t["label"] in OTHER_SENSE else
          (inkc if corpus == "AS-T" else INK),
          ((55 + 700 * (t["documents_weight"] / maxw_all) ** 0.62) ** .5) / 2 * 1.06,
          t["label"] in OTHER_SENSE)
         for x, y, t, corpus, fill, inkc in
         sorted(allpts, key=lambda p: -p[2]["documents_weight"])]

xs = [p[0] for p in allpts]; ys = [p[1] for p in allpts]
ax.set_xlim(min(xs) - 0.85, max(xs) + 0.85)
ax.set_ylim(min(ys) - 0.55, max(ys) + 0.55)
ax.set_xlabel("centrality, in interquartile ranges from each corpus's own median  →")
ax.set_ylabel("density, in interquartile ranges from each corpus's own median  →")
ax.grid(True, alpha=0.55); ax.set_axisbelow(True)
fig.canvas.draw()
cbx = corners(ax, fig, small=True)
fig.canvas.draw()
_r = fig.canvas.get_renderer()
place(ax, fig, items, fs=9,
      extra=[c.get_window_extent(_r).expanded(1.2, 1.2) for c in cbx])

leg = [Line2D([], [], marker="o", ls="", markersize=9, alpha=0.70,
              markerfacecolor=SLATE, markeredgecolor="white", label="TS-J"),
       Line2D([], [], marker="o", ls="", markersize=9, alpha=0.70,
              markerfacecolor=TAN, markeredgecolor="white", label="AS-J"),
       Line2D([], [], marker="o", ls="", markersize=9, alpha=0.70,
              markerfacecolor=TAN_LIGHT, markeredgecolor="white", label="AS-T"),
       Line2D([], [], marker="o", ls="", markersize=9, markerfacecolor="white",
              markeredgecolor=GREY_EDGE, markeredgewidth=1.3,
              label="another sense of the word")]
ax.legend(handles=leg, loc="upper center", bbox_to_anchor=(0.5, -0.088),
          frameon=False, ncol=4, fontsize=ANNOT, handletextpad=0.45, columnspacing=1.8)
fig.savefig(os.path.join(OUT, "fig_themes_combined_standardised.png"))
pad_to_width(os.path.join(OUT, "fig_themes_combined_standardised.png"))
print("saved fig_themes_combined_standardised.png")

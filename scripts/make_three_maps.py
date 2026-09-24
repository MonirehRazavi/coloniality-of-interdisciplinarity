"""
make_three_maps.py — Figure: The Themes of the Three Corpora, side by side
===========================================================================
One exhibit, three thematic maps, drawn from a single run of a single
procedure (analysis_three_corpora.py) so that the comparison rests on one
execution rather than three stitched together.

COLOUR = CORPUS, following the palette used throughout Chapter 6:
    Translation Studies journals (TS-J)     slate blue   #3F6E96
    Adaptation Studies journals (AS-J)      tan          #C08030
    dispersed adaptation literature (AS-T)  light tan    #E4C08C

OPEN CIRCLES = a cluster belonging to another sense of the word. Only AS-T
has any, because only AS-T was defined by a keyword rather than by a list of
journals. Open-versus-filled survives greyscale printing, which a second fill
colour would not.

Bubbles are numbered rather than labelled in place: at three panels to a
page-width there is no room for keyword strings, and a numbered key below
keeps every theme legible at 8.5 pt instead of shrinking labels to 5 pt.
"""
import json, os, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D

for f in ["Tinos-Regular.ttf", "Tinos-Bold.ttf", "Tinos-Italic.ttf", "Tinos-BoldItalic.ttf"]:
    p = os.path.join("/usr/share/fonts/truetype/croscore", f)
    if os.path.exists(p):
        font_manager.fontManager.addfont(p)

SLATE, TAN, TAN_LIGHT = "#3F6E96", "#C08030", "#E4C08C"
GREY_EDGE = "#8E8C85"
INK, INK2, MUTED, GRID = "#1a1a1a", "#4a4a4a", "#8a8880", "#e6e5e1"

plt.rcParams.update({
    "font.family": "Tinos", "font.size": 11,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK2,
    "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": INK2, "ytick.color": INK2,
    "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "axes.labelsize": 9,
    "grid.color": GRID, "grid.linewidth": 0.6,
    "figure.dpi": 300, "savefig.dpi": 300,
})

NUM_CANDIDATES = [(0, 9), (9, 0), (0, -9), (-9, 0),
                  (7, 7), (7, -7), (-7, 7), (-7, -7),
                  (0, 15), (15, 0), (0, -15), (-15, 0),
                  (12, 12), (12, -12), (-12, 12), (-12, -12)]


def place_numbers(ax, fig, marks, extra=()):
    """Numbers just outside each bubble; first non-colliding slot wins."""
    from matplotlib.transforms import Bbox
    r = fig.canvas.get_renderer()
    taken = list(extra)
    for (x, y, _txt, _c, rad) in marks:
        px, py = ax.transData.transform((x, y))
        taken.append(Bbox.from_bounds(px - rad, py - rad, 2 * rad, 2 * rad))
    for (x, y, txt, col, rad) in marks:
        done = False
        for dx, dy in NUM_CANDIDATES:
            ox = dx + (rad * 0.8 if dx > 0 else -rad * 0.8 if dx < 0 else 0)
            oy = dy + (rad * 0.8 if dy > 0 else -rad * 0.8 if dy < 0 else 0)
            t = ax.annotate(txt, (x, y), textcoords="offset points",
                            xytext=(ox, oy), ha="center", va="center",
                            fontsize=7.8, color=col, zorder=6)
            bb = t.get_window_extent(r).expanded(1.5, 1.35)
            ab = ax.get_window_extent()
            if (bb.x0 >= ab.x0 and bb.x1 <= ab.x1 and bb.y0 >= ab.y0
                    and bb.y1 <= ab.y1 and not any(bb.overlaps(b) for b in taken)):
                taken.append(bb); done = True; break
            t.remove()
        if not done:
            t = ax.annotate(txt, (x, y), textcoords="offset points",
                            xytext=(rad * 0.8 + 9, 0), ha="center", va="center",
                            fontsize=7.8, color=col, zorder=6)
            taken.append(t.get_window_extent(r))


R = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis_outputs", "THREE_CORPORA_THEMES.json")))

OTHER_SENSE = {
    "climate change, politics, resilience",
    "health, model, perceptions",
    "identity, migration, culture",
    "scale, reliability, validity",
}

# short key entries: what to print beside each number
KEY = {
 "translation, language, english": "translation, language, English",
 "audiovisual translation, subtitling, dubbing": "audiovisual translation, subtitling",
 "translator training, quality, translation competence": "translator training, competence",
 "simultaneous interpreting, performance, cognitive load": "simultaneous interpreting",
 "literary translation, retranslation, adaptation": "literary translation, retranslation,\n      adaptation, equivalence, intersemiotic",
 "interpreting, ethics, interpreter training": "interpreting, ethics",
 "ideology, discourse, news translation": "ideology, discourse, news",
 "machine translation, post-editing, translation technology": "machine translation, post-editing",
 "translation studies, translation history, sociology of translation": "translation studies, sociology",
 "legal translation, institutional translation, translation policy": "legal translation, policy",
 "domestication, foreignization, cultural references": "domestication, foreignization",

 "adaptation, translation, intertextuality": "adaptation, translation,\n      intertextuality, fidelity",
 "film, gender, television": "film, gender, television",
 "shakespeare, appropriation, hamlet": "Shakespeare, appropriation",
 "adaptation studies, film adaptation, cinema": "adaptation studies, film adaptation",
 "nostalgia, intermediality, remediation": "intermediality, remediation",
 "horror, radio drama, film noir": "horror, film noir",
 "othello, william shakespeare, desdemona": "Othello, Desdemona",
 "adaptation theory, jane austen": "adaptation theory, Austen",
 "authorship, screenwriting": "authorship, screenwriting",
 "kubrick, masculinity": "Kubrick, masculinity",
 "dracula, vampire": "Dracula, vampire",

 "adaptation, translation, film adaptation": "adaptation, film adaptation,\n      Shakespeare, intertextuality",
 "climate change, politics, resilience": "climate change, resilience",
 "communication, media, social media": "communication, media",
 "identity, migration, culture": "migration, acculturation",
 "health, model, perceptions": "health, stress, adjustment",
 "gender, women, race": "gender, women, race",
 "education, history, covid-19": "education, history, memory",
 "scale, reliability, validity": "scale, reliability, validity",
}

PANELS = [("TS-J", SLATE,     "Translation Studies journals",
           "14,258 records · 250 keywords"),
          ("AS-J", TAN,       "Adaptation Studies journals",
           "2,763 records · 78 keywords"),
          ("AS-T", TAN_LIGHT, "dispersed adaptation literature",
           "18,566 records · 250 keywords")]

fig = plt.figure(figsize=(7.2, 5.85))
gs = fig.add_gridspec(2, 3, height_ratios=[1.32, 1.0],
                      left=0.068, right=0.988, top=0.875, bottom=0.055,
                      wspace=0.30, hspace=0.30)

for col, (corpus, colour, title, sub) in enumerate(PANELS):
    ax = fig.add_subplot(gs[0, col])
    th = R[corpus]["themes"]
    cmed, dmed = th[0]["median_centrality"], th[0]["median_density"]
    ax.axvline(cmed, color=MUTED, lw=0.8, ls=(0, (3.5, 2.5)), zorder=1)
    ax.axhline(dmed, color=MUTED, lw=0.8, ls=(0, (3.5, 2.5)), zorder=1)

    cs = [t["centrality"] for t in th]; ds = [t["density"] for t in th]
    rx, ry = max(cs) - min(cs), max(ds) - min(ds)
    ax.set_xlim(min(cs) - rx * 0.17 - 0.2, max(cs) + rx * 0.17 + 0.2)
    ax.set_ylim(min(ds) - ry * 0.13 - 0.2, max(ds) + ry * 0.22 + 0.2)

    maxw = max(t["documents_weight"] for t in th)
    marks = []
    for i, t in enumerate(th, start=1):
        other = t["label"] in OTHER_SENSE
        s = 46 + 520 * (t["documents_weight"] / maxw)
        if other:
            ax.scatter(t["centrality"], t["density"], s=s, facecolor="white",
                       edgecolor=GREY_EDGE, linewidth=1.2, zorder=3)
        else:
            ax.scatter(t["centrality"], t["density"], s=s, color=colour,
                       alpha=0.72, edgecolor="white", linewidth=1.0, zorder=3)
        marks.append((t["centrality"], t["density"], str(i),
                      GREY_EDGE if other else colour, (s ** 0.5) / 2 + 1.5))
    corner_txt = []
    for lbl, xy, ha, va in [("motor", (0.985, 0.975), "right", "top"),
                            ("niche", (0.015, 0.975), "left", "top"),
                            ("emerging", (0.015, 0.02), "left", "bottom"),
                            ("basic", (0.985, 0.02), "right", "bottom")]:
        corner_txt.append(ax.annotate(
            lbl, xy=xy, xycoords="axes fraction", ha=ha, va=va,
            fontsize=7, color=MUTED, style="italic", zorder=2,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.75, pad=0.8)))
    fig.canvas.draw()
    _r = fig.canvas.get_renderer()
    place_numbers(ax, fig, marks,
                  extra=[t.get_window_extent(_r).expanded(1.25, 1.25)
                         for t in corner_txt])

    ax.grid(True, alpha=0.55); ax.set_axisbelow(True)
    ax.set_xlabel("centrality  →", labelpad=2)
    if col == 0:
        ax.set_ylabel("density  →", labelpad=2)
    ax.annotate(corpus, xy=(0, 1.135), xycoords="axes fraction", fontsize=10.5,
                color=colour if corpus != "AS-T" else "#B9893F", ha="left")
    ax.annotate(title, xy=(0, 1.072), xycoords="axes fraction", fontsize=8.3,
                color=INK2, ha="left")
    ax.annotate(sub, xy=(0, 1.014), xycoords="axes fraction", fontsize=7.4,
                color=MUTED, ha="left")

    # ---- numbered key beneath its own panel ------------------------------
    kax = fig.add_subplot(gs[1, col]); kax.axis("off")
    y = 1.0
    for i, t in enumerate(th, start=1):
        other = t["label"] in OTHER_SENSE
        txt = KEY.get(t["label"], t["label"])
        kax.text(0.0, y, f"{i}", fontsize=7.8, color=GREY_EDGE if other else colour,
                 va="top", ha="left", transform=kax.transAxes)
        kax.text(0.075, y, txt, fontsize=7.8,
                 color=GREY_EDGE if other else INK2, va="top", ha="left",
                 transform=kax.transAxes, linespacing=1.18,
                 style="italic" if other else "normal")
        y -= 0.088 * (1 + txt.count("\n") * 0.92)

handles = [
    Line2D([], [], marker="o", ls="", markersize=8, markerfacecolor="white",
           markeredgecolor=GREY_EDGE, markeredgewidth=1.2,
           label="open circle: a cluster belonging to another sense of the word"),
    Line2D([], [], marker="o", ls="", markersize=8, alpha=0.72,
           markerfacecolor="#9a9a9a", markeredgecolor="white",
           label="bubble area: keyword occurrences in the cluster"),
]
fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.055, 0.001),
           frameon=False, ncol=2, fontsize=7.8, handletextpad=0.4,
           columnspacing=2.0)

_fig_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figs_out", "thematic_maps")
os.makedirs(_fig_dir, exist_ok=True)
fig.savefig(os.path.join(_fig_dir, "fig_three_thematic_maps.png"))
print("saved")

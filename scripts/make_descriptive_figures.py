"""
make_descriptive_figures.py — Chapter 6, descriptive figures (Python)
=====================================================================
Replaces the biblioshiny (R) descriptive outputs of 6 August 2026 with Python
equivalents, so that the whole toolchain is a single language and every figure
in the thesis derives from a script supplied in the appendix.

Each figure below has a biblioshiny counterpart, named in its comment, so the
two sets can be compared if needed. The calculations are standard and are
explained in place rather than assumed.

Output: ../figs/descriptive/*.png at 300 dpi
"""
import json, os, re
from collections import Counter, defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter

import wos_parser as W

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
FIG = os.path.join(os.path.dirname(__file__), "..", "figs_out", "descriptive")
os.makedirs(FIG, exist_ok=True)

# Same validated palette as the analytical figures: Translation Studies blue,
# Adaptation Studies orange, aqua where a third class is unavoidable.
TS_BLUE, AS_ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8880"

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"], "font.size": 9,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": INK2, "ytick.color": INK2,
    "grid.color": "#e6e5e1", "grid.linewidth": 0.6,
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
    "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlelocation": "left",
})

print("Loading corpora ...")
C = {n: W.load_corpus(f"{BASE}/{n}", verbose=False) for n in ["TS-J", "AS-J", "AS-T"]}
saved = []


def finish(fig, name, caption):
    fig.savefig(os.path.join(FIG, name))
    plt.close(fig)
    saved.append((name, caption))
    print(f"  saved {name}")


def thousands(x, _):
    return f"{int(x):,}"


# ===========================================================================
# D1 — Annual indexed output.  (biblioshiny: "Annual Scientific Production")
# ---------------------------------------------------------------------------
# CAPTION DISCIPLINE (decision log D3): this is *indexed* output, not the
# growth of either field. Journals enter Web of Science at different dates,
# and the Emerging Sources Citation Index admitted large numbers of humanities
# journals at once from 2015. Any surge around 2015-17 is substantially an
# artefact of database expansion, and the axis label says so.
# ===========================================================================
def year_counts(recs, lo=1975, hi=2025):
    c = Counter()
    for r in recs:
        py = r.get("PY", "")
        if py.isdigit() and lo <= int(py) <= hi:
            c[int(py)] += 1
    return c


fig, ax = plt.subplots(figsize=(6.6, 3.4))
for name, col in [("TS-J", TS_BLUE), ("AS-T", AQUA), ("AS-J", AS_ORANGE)]:
    c = year_counts(C[name])
    ys = sorted(c)
    ax.plot(ys, [c[y] for y in ys], color=col, lw=2, label=name)
    ax.annotate(name, (ys[-1], c[ys[-1]]), textcoords="offset points",
                xytext=(6, 0), color=col, fontsize=9, va="center")
ax.axvspan(2015, 2017, color="#e6e5e1", alpha=0.6, zorder=0)
ax.annotate("ESCI expansion\n2015–17", xy=(2016, ax.get_ylim()[1] * 0.92),
            ha="center", fontsize=7.5, color=MUTED, style="italic")
ax.set_xlabel("Publication year")
ax.set_ylabel("Records indexed that year")
ax.set_title("Figure D1  Indexed output per year, all three corpora")
ax.grid(True, alpha=0.6); ax.set_axisbelow(True)
ax.set_xlim(1975, 2027)
ax.yaxis.set_major_formatter(FuncFormatter(thousands))
finish(fig, "D1_annual_indexed_output.png",
       "Records indexed per year. This is indexed output, NOT the growth of "
       "either field: journals enter the database at different dates, and the "
       "shaded band marks the Emerging Sources Citation Index expansion, which "
       "admitted large numbers of humanities journals at once.")


# ===========================================================================
# D2 — Journal composition of TS-J.  (biblioshiny: "Most Relevant Sources")
# ===========================================================================
so = Counter(r.get("SO", "").upper() for r in C["TS-J"])
SHORT = {
    "PERSPECTIVES-STUDIES IN TRANSLATION THEORY AND PRACTICE": "Perspectives",
    "BABEL-REVUE INTERNATIONALE DE LA TRADUCTION-INTERNATIONAL JOURNAL OF TRANSLATION": "Babel",
    "TARGET-INTERNATIONAL JOURNAL OF TRANSLATION STUDIES": "Target",
    "SENDEBAR-REVISTA DE TRADUCCION E INTERPRETACION": "Sendebar",
    "FORUM-REVUE INTERNATIONALE D INTERPRETATION ET DE TRADUCTION-INTERNATIONAL JOURNAL OF INTERPRETATION AND TRANSLATION": "FORUM",
    "LINGUISTICA ANTVERPIENSIA NEW SERIES-THEMES IN TRANSLATION STUDIES": "Linguistica Antverpiensia",
    "TRANSLATION IN THE ARAB WORLD: THE ABBASID GOLDEN AGE": "Translation in the Arab World",
    "JOURNAL OF SPECIALISED TRANSLATION": "JoSTrans",
    "INTERPRETER AND TRANSLATOR TRAINER": "The Interpreter & Translator Trainer",
}
def pretty(s):
    return SHORT.get(s, s.title())

items = sorted(so.items(), key=lambda x: x[1])
fig, ax = plt.subplots(figsize=(6.6, 4.6))
bars = ax.barh([pretty(k) for k, _ in items], [v for _, v in items],
               color=TS_BLUE, height=0.66)
for bar, (_, v) in zip(bars, items):
    ax.text(v + 30, bar.get_y() + bar.get_height() / 2, f"{v:,}",
            va="center", fontsize=7.8, color=INK)
ax.set_xlim(0, max(so.values()) * 1.13)
ax.set_xlabel("Records in the frozen corpus")
ax.set_title("Figure D2  The twenty Translation Studies journals (TS-J, n = 14,258)")
ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
finish(fig, "D2_ts_journal_composition.png",
       "Every journal in TS-J by record count. Counts are case-insensitive: six "
       "journals also appear under a mixed-case duplicate source string, and "
       "counting raw strings gives a spurious twenty-six 'journals'.")


# ===========================================================================
# D3 — Bradford's law.  (biblioshiny: "Bradford's Law")
# ---------------------------------------------------------------------------
# Bradford's law describes how a literature concentrates: rank the journals by
# output, and the journals dividing the literature into equal thirds fall into
# groups of roughly 1 : n : n^2. The point of plotting it here is NOT to test
# Bradford but to show how concentrated each field is: how few venues carry
# the bulk of the indexed record.
# ===========================================================================
fig, ax = plt.subplots(figsize=(6.4, 3.4))
for name, col in [("TS-J", TS_BLUE), ("AS-T", AQUA)]:
    src = Counter(r.get("SO", "").upper() for r in C[name] if r.get("SO"))
    ranked = [v for _, v in src.most_common()]
    total = sum(ranked)
    cum = []
    run = 0
    for v in ranked:
        run += v
        cum.append(100 * run / total)
    ax.plot(range(1, len(cum) + 1), cum, color=col, lw=2, label=name)
    third = next(i for i, v in enumerate(cum, 1) if v >= 33.3)
    ax.plot([third], [cum[third - 1]], "o", color=col, ms=7,
            markeredgecolor="white", markeredgewidth=1.2, zorder=4)
    ax.annotate(f"{name}: {third} journal{'s' if third > 1 else ''}\ncarry the first third",
                (third, cum[third - 1]), textcoords="offset points",
                xytext=(12, -4), fontsize=8, color=col)
ax.axhline(33.3, color=MUTED, lw=0.9, ls=(0, (4, 3)))
ax.set_xscale("log")
ax.set_xlabel("Journals, ranked by output (log scale)")
ax.set_ylabel("Cumulative share of records")
ax.yaxis.set_major_formatter(PercentFormatter())
ax.set_title("Figure D3  How concentrated each literature is")
ax.grid(True, alpha=0.6); ax.set_axisbelow(True)
finish(fig, "D3_bradford_concentration.png",
       "Cumulative share of records against journal rank. TS-J is a closed set "
       "of twenty venues by construction; AS-T is dispersed across hundreds of "
       "other disciplines' journals, which is the shape of ceded practice.")


# ===========================================================================
# D4 — Lotka's law.  (biblioshiny: "Lotka's Law")
# ---------------------------------------------------------------------------
# Lotka's law: in most literatures the number of authors publishing n papers
# falls off roughly as 1/n^2 — a very large number of one-paper authors and a
# very small number of prolific ones. Plotted here to characterise each field's
# author base rather than to test the law.
# ===========================================================================
def author_productivity(recs):
    c = Counter()
    for r in recs:
        for a in (r.get("AF") or r.get("AU") or []):
            sn, ini = W.norm_author(a)
            if sn:
                c[(sn, ini)] += 1
    return Counter(c.values())


fig, ax = plt.subplots(figsize=(6.0, 3.4))
for name, col in [("TS-J", TS_BLUE), ("AS-J", AS_ORANGE)]:
    dist = author_productivity(C[name])
    tot = sum(dist.values())
    xs = sorted(dist)[:15]
    ax.plot(xs, [100 * dist[x] / tot for x in xs], "o-", color=col, lw=1.8,
            ms=5, markeredgecolor="white", markeredgewidth=1, label=name)
    ax.annotate(f"{name}: {100*dist[1]/tot:.0f}% of authors\nappear once",
                (1, 100 * dist[1] / tot), textcoords="offset points",
                xytext=(14, -6), fontsize=8, color=col)
ax.set_xlabel("Documents published in the corpus")
ax.set_ylabel("Share of that corpus's authors")
ax.yaxis.set_major_formatter(PercentFormatter())
ax.set_title("Figure D4  Author productivity in each field")
ax.grid(True, alpha=0.6); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=8.5)
finish(fig, "D4_lotka_author_productivity.png",
       "The share of each field's authors publishing one, two, three… documents "
       "in the corpus. Both fields show the steep distribution typical of "
       "academic literatures: most authors appear once.")


# ===========================================================================
# D5 — Most-cited authors inside each corpus.
#      (biblioshiny: "Most Local Cited Authors")
# ---------------------------------------------------------------------------
# "Local" citation means: cited by documents WITHIN this corpus, as opposed to
# a global citation count from the whole database. It answers "who does this
# field read?" rather than "who is famous?"
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


fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.2))
for ax, corpus, col in [(axes[0], "TS-J", TS_BLUE), (axes[1], "AS-J", AS_ORANGE)]:
    top = local_cited_authors(corpus)[::-1]
    labels = [f"{sn.title()}, {ini}" for (sn, ini), _ in top]
    vals = [v for _, v in top]
    bars = ax.barh(labels, vals, color=col, height=0.66)
    for bar, v in zip(bars, vals):
        ax.text(v + max(vals) * 0.015, bar.get_y() + bar.get_height() / 2,
                f"{v:,}", va="center", fontsize=7.6, color=INK)
    ax.set_xlim(0, max(vals) * 1.16)
    ax.set_title(f"{corpus}")
    ax.set_xlabel("Cited references within the corpus")
    ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
fig.suptitle("Figure D5  Who each field reads: most-cited authors within its own corpus",
             x=0.02, ha="left", fontsize=10, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.94])
finish(fig, "D5_most_cited_authors.png",
       "The fifteen most-cited first authors inside each corpus. Names are "
       "normalised to surname plus first initial, so the database's four "
       "renderings of the same person are merged.")


# ===========================================================================
# D6 — Most-cited SOURCES inside each corpus.
#      (biblioshiny: "Most Local Cited Sources")
# ===========================================================================
def local_cited_sources(corpus, n=15):
    c = Counter()
    for i, cr in W.iter_refs(C[corpus]):
        a, y, s = W.split_cr(cr)
        if s and len(s) > 3:
            c[s] += 1
    return c.most_common(n)


fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.2))
for ax, corpus, col in [(axes[0], "TS-J", TS_BLUE), (axes[1], "AS-J", AS_ORANGE)]:
    top = local_cited_sources(corpus)[::-1]
    labels = [s.title()[:34] for s, _ in top]
    vals = [v for _, v in top]
    bars = ax.barh(labels, vals, color=col, height=0.66)
    for bar, v in zip(bars, vals):
        ax.text(v + max(vals) * 0.015, bar.get_y() + bar.get_height() / 2,
                f"{v:,}", va="center", fontsize=7.4, color=INK)
    ax.set_xlim(0, max(vals) * 1.18)
    ax.set_title(f"{corpus}")
    ax.set_xlabel("Times cited within the corpus")
    ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
fig.suptitle("Figure D6  What each field cites: most-cited sources and works",
             x=0.02, ha="left", fontsize=10, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.94])
finish(fig, "D6_most_cited_sources.png",
       "The fifteen most-cited sources within each corpus. Web of Science "
       "truncates these strings at twenty characters, so book titles appear "
       "abbreviated; journal abbreviations and book titles share the field.")


# ===========================================================================
# D7 — Document types in TS-J.
# ---------------------------------------------------------------------------
# Included because the 3,824 book reviews are argumentatively relevant: which
# books a discipline chooses to review is jurisdictional behaviour.
# ===========================================================================
dt = Counter()
for r in C["TS-J"]:
    d = r.get("DT", "").split(";")[0].strip().title()
    if d:
        dt[d] += 1
items = [(k, v) for k, v in dt.most_common(6)][::-1]
fig, ax = plt.subplots(figsize=(6.0, 2.6))
cols = [AS_ORANGE if k.startswith("Book Review") else TS_BLUE for k, _ in items]
bars = ax.barh([k for k, _ in items], [v for _, v in items], color=cols, height=0.62)
for bar, (_, v) in zip(bars, items):
    ax.text(v + 120, bar.get_y() + bar.get_height() / 2, f"{v:,}",
            va="center", fontsize=8, color=INK)
ax.set_xlim(0, max(v for _, v in items) * 1.15)
ax.set_xlabel("Records")
ax.set_title("Figure D7  What Translation Studies journals publish")
ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
finish(fig, "D7_document_types.png",
       "Document types in TS-J. Book reviews (orange) are 27% of the corpus and "
       "are retained deliberately: which books a discipline reviews is "
       "jurisdictional behaviour.")


# ===========================================================================
# D8 — Where the two fields are written from.
#      (biblioshiny: "Most Relevant Affiliations" / "Corresponding Author's Country")
# ---------------------------------------------------------------------------
# The country is taken from the last comma-separated element of each address
# in the C1 (author address) field. Reported with the caveat that Web of
# Science's own coverage bias shapes this heavily — it is a finding about the
# indexed record, not about where adaptation and translation are studied.
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
                ctry = COUNTRY_FIX.get(ctry, ctry.title())
                if ctry and len(ctry) > 1:
                    seen.add(ctry)
        for ctry in seen:
            c[ctry] += 1
    return c.most_common(n)


fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.8))
for ax, corpus, col in [(axes[0], "TS-J", TS_BLUE), (axes[1], "AS-J", AS_ORANGE)]:
    top = countries(C[corpus])[::-1]
    if not top:
        continue
    vals = [v for _, v in top]
    bars = ax.barh([k for k, _ in top], vals, color=col, height=0.66)
    for bar, v in zip(bars, vals):
        ax.text(v + max(vals) * 0.02, bar.get_y() + bar.get_height() / 2,
                f"{v:,}", va="center", fontsize=7.6, color=INK)
    ax.set_xlim(0, max(vals) * 1.18)
    ax.set_title(corpus)
    ax.set_xlabel("Documents with an author based there")
    ax.xaxis.grid(True); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
fig.suptitle("Figure D8  Where the indexed record is written from",
             x=0.02, ha="left", fontsize=10, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.93])
finish(fig, "D8_author_countries.png",
       "Author locations in each corpus. This describes the INDEXED record, not "
       "the fields: Web of Science's own coverage bias toward Anglophone and "
       "European venues shapes it directly, which is itself the point.")


# ===========================================================================
print("\nManifest:")
json.dump([{"file": n, "caption": c} for n, c in saved],
          open(os.path.join(FIG, "manifest.json"), "w"), indent=2)
for n, c in saved:
    print(f"  {n}")

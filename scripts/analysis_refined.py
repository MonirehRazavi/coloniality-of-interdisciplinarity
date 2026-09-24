"""
analysis_refined.py — Chapter 6: three refinements to the first pass
====================================================================
The first pass (analysis_cross_corpus.py) produced usable counts but three of
its operationalisations were too crude to report in a thesis. This script
replaces them. Each replacement is documented with WHY the first version was
inadequate, because the chapter's reflexive commitment applies to its own
statistics as much as to its corpus.

  R1. MARKEDNESS at the token level, not the document level.
      First pass asked "does this document ever use 'translation' without a
      modifier?" — which almost every document does, so both fields scored
      ~90% "bare" and the contrast vanished. Markedness is a property of
      OCCURRENCES, not of documents. Counting tokens recovers the measure.

  R2. TEMPORAL analysis by RATE, not by count.
      First pass took the median year of documents using 'fidelity'. But both
      corpora grow steeply over time, so that median measures when each corpus
      got big, not when its fidelity discourse peaked. Using the annual
      PROPORTION of documents engaging the term removes the growth confound.

  R3. RPYS restricted to the foundational period.
      First pass reported the largest absolute deviations, which land in
      1995–2017 simply because recent years carry far more references. RPYS
      exists to surface FOUNDATIONAL spikes; the standard remedy is to run the
      transform on the pre-1990 window separately, which is done here.
"""
import json, os, re, csv
from collections import Counter

import wos_parser as W
import canon as K

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis_outputs")
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

print("Loading corpora ...")
C = {n: W.load_corpus(f"{BASE}/{n}", verbose=False) for n in ["TS-J", "AS-J", "AS-T"]}
PARSED = {n: [(i,) + W.split_cr(cr) for i, cr in W.iter_refs(C[n])] for n in C}
R = {}


def field_text(r, fields):
    # (D14) DE/ID arrive as joined text; the within-field wrap is repaired in
    # the parser, so concatenating fields here is safe.
    parts = []
    for f in fields:
        v = r.get(f)
        if isinstance(v, list):
            parts.extend(v)
        elif v:
            parts.append(v)
    return " ; ".join(parts).lower()


# ===========================================================================
# R1 — TOKEN-LEVEL MARKEDNESS
# ---------------------------------------------------------------------------
# For every OCCURRENCE of the term, ask: is it preceded by a modifier?
#   "audiovisual translation"  -> marked
#   "translation"              -> unmarked (bare)
# The unmarked share is the operationalisation of §5.4's synecdoche argument:
# a term is unmarked in a field when the field can use it with no qualifier and
# be understood to mean the default thing.
# ===========================================================================
print("\nR1 — token-level markedness")


def markedness_tokens(recs, term, modifiers, fields=("TI", "AB", "DE", "ID")):
    mods = sorted(modifiers, key=len, reverse=True)
    marked_rx = re.compile(
        r"\b(" + "|".join(re.escape(m) for m in mods) + r")[\s\-]+(" + term + r"s?)\b", re.I)
    any_rx = re.compile(r"\b" + term + r"s?\b", re.I)
    total = marked = 0
    mod_counter = Counter()
    for r in recs:
        t = field_text(r, list(fields))
        if term not in t:
            continue
        total += len(any_rx.findall(t))
        for m in marked_rx.finditer(t):
            marked += 1
            mod_counter[m.group(1).lower()] += 1
    bare = total - marked
    return {"total_occurrences": total,
            "marked_occurrences": marked,
            "bare_occurrences": bare,
            "pct_bare": round(100 * bare / total, 1) if total else None,
            "pct_marked": round(100 * marked / total, 1) if total else None,
            "top_modifiers": dict(mod_counter.most_common(12))}


mk = {
    "translation in TS-J": markedness_tokens(C["TS-J"], "translation", K.TRANSLATION_MODIFIERS),
    "adaptation in TS-J": markedness_tokens(C["TS-J"], "adaptation", K.ADAPTATION_MODIFIERS),
    "adaptation in AS-J": markedness_tokens(C["AS-J"], "adaptation", K.ADAPTATION_MODIFIERS),
    "translation in AS-J": markedness_tokens(C["AS-J"], "translation", K.TRANSLATION_MODIFIERS),
    "adaptation in AS-T": markedness_tokens(C["AS-T"], "adaptation", K.ADAPTATION_MODIFIERS),
}
for k, v in mk.items():
    print(f"  {k:24s} n={v['total_occurrences']:7,}  bare={v['pct_bare']:5.1f}%  "
          f"marked={v['pct_marked']:5.1f}%   top: {', '.join(list(v['top_modifiers'])[:4])}")
R["R1_markedness_tokens"] = mk

# The four-cell comparison that §6.7 turns on: each field's OWN term vs the
# OTHER field's term, inside the same corpus.
grid = {
    "TS-J": {"own term (translation)": mk["translation in TS-J"]["pct_bare"],
             "other term (adaptation)": mk["adaptation in TS-J"]["pct_bare"]},
    "AS-J": {"own term (adaptation)": mk["adaptation in AS-J"]["pct_bare"],
             "other term (translation)": mk["translation in AS-J"]["pct_bare"]},
}
print("  Mirror grid (% of occurrences used BARE):")
for corp, d in grid.items():
    print(f"      {corp}: " + "  ".join(f"{k} = {v}%" for k, v in d.items()))
R["R1_mirror_grid"] = grid


# ===========================================================================
# R2 — TEMPORAL ANALYSIS BY RATE
# ===========================================================================
print("\nR2 — rate-normalised term trajectories (§6.8)")


def rate_series(recs, terms, min_docs=15, fields=("TI", "AB", "DE", "ID")):
    rx = re.compile(r"\b(" + "|".join(terms) + r")\w*", re.I)
    tot, hit = Counter(), Counter()
    for r in recs:
        py = r.get("PY", "")
        if not py.isdigit():
            continue
        y = int(py)
        if y < 1975 or y > 2025:
            continue
        tot[y] += 1
        if rx.search(field_text(r, list(fields))):
            hit[y] += 1
    return {y: {"documents": tot[y], "with_term": hit[y],
                "rate_pct": round(100 * hit[y] / tot[y], 2)}
            for y in sorted(tot) if tot[y] >= min_docs}


def peak_of_rate(series, smooth=3):
    """Peak year of a 3-year moving average of the RATE, which is robust to
    single-year spikes in small corpora."""
    ys = sorted(series)
    best, besty = -1, None
    for i, y in enumerate(ys):
        w = [series[ys[j]]["rate_pct"] for j in range(max(0, i - smooth // 2),
                                                      min(len(ys), i + smooth // 2 + 1))]
        m = sum(w) / len(w)
        if m > best:
            best, besty = m, y
    return besty, round(best, 2)


clocks = {}
for label, corpus, terms in [
    ("TS-J fidelity/faithfulness", "TS-J", ["fidelit", "faithful"]),
    ("AS-J fidelity/faithfulness", "AS-J", ["fidelit", "faithful"]),
    ("TS-J equivalence", "TS-J", ["equivalen"]),
    ("AS-J equivalence", "AS-J", ["equivalen"]),
    ("TS-J adaptation", "TS-J", ["adaptation"]),
    ("AS-J translation", "AS-J", ["translation"]),
]:
    s = rate_series(C[corpus], terms)
    py, pv = peak_of_rate(s)
    clocks[label] = {"series": s, "peak_year_of_rate": py, "peak_rate_pct": pv,
                     "mean_rate_pct": round(sum(d["rate_pct"] for d in s.values()) / len(s), 2) if s else None}
    print(f"  {label:30s} rate peaks {py} at {pv}%  (mean {clocks[label]['mean_rate_pct']}%)")

lag = clocks["AS-J fidelity/faithfulness"]["peak_year_of_rate"] - \
      clocks["TS-J fidelity/faithfulness"]["peak_year_of_rate"]
print(f"\n  FIDELITY LAG (AS peak - TS peak) = {lag:+d} years")
print("  (Positive = AS later than TS, the direction Chapter 5's 'temporal othering'")
print("   claim would predict. Negative or zero = no empirical substrate for it.)")
R["R2_clocks"] = clocks
R["R2_fidelity_lag_years"] = lag


# ===========================================================================
# R3 — RPYS ON THE FOUNDATIONAL WINDOW
# ===========================================================================
print("\nR3 — RPYS, foundational window 1900–1990 (§6.9)")


def rpys(corpus, lo, hi):
    """Reference Publication Year Spectroscopy.

    NOTE (correction, 6 Aug 2026): counts are accumulated over the FULL year
    range, not the reporting window. An earlier version accumulated only within
    [lo, hi], which made the 5-year median at the window edge include years
    that were empty *by construction* — inflating 1989 and 1990 into spurious
    'foundational peaks'. Deviations are computed on the complete series and
    only REPORTED for the window."""
    c = Counter()
    for i, a, y, s in PARSED[corpus]:
        if y and 1800 <= y <= 2026:
            c[y] += 1
    years = list(range(lo, hi + 1))
    dev = {}
    for y in years:
        window = [c.get(yy, 0) for yy in range(y - 2, y + 3)]
        med = sorted(window)[len(window) // 2]
        dev[y] = c.get(y, 0) - med
    return c, dev


rp = {}
for n in ["TS-J", "AS-J"]:
    cf, devf = rpys(n, 1900, 1990)
    cfull, devfull = rpys(n, 1900, 2025)
    peaks = sorted(devf.items(), key=lambda x: -x[1])[:12]
    rp[n] = {
        "foundational_peaks_1900_1990": [
            {"year": y, "references": cf.get(y, 0), "deviation": d} for y, d in peaks],
        "full_series": {str(y): cfull.get(y, 0) for y in range(1900, 2026)},
        "full_deviation": {str(y): devfull[y] for y in range(1900, 2026)},
    }
    print(f"  {n} — top foundational peaks:")
    for y, d in peaks[:8]:
        print(f"      {y}: {cf.get(y,0):5d} refs  (deviation +{d})")
R["R3_rpys"] = rp

# What actually sits at the biggest spikes? Report the most-cited works of the
# peak years, so the chapter can name the founding texts rather than assert them.
print("\n  Most-cited works at the principal foundational peaks:")
peak_works = {}
for n, years in [("TS-J", [1959, 1958, 1972, 1978]), ("AS-J", [1957, 1975, 1977, 1984])]:
    peak_works[n] = {}
    for y in years:
        c = Counter()
        for i, a, yy, s in PARSED[n]:
            if yy == y and a and s:
                c[f"{a} | {s}"] += 1
        peak_works[n][str(y)] = dict(c.most_common(5))
        print(f"    {n} {y}: " + "; ".join(f"{k.split(' | ')[0]} ({v})"
                                           for k, v in c.most_common(3)))
R["R3_peak_works"] = peak_works

with open(os.path.join(OUT, "REFINED_RESULTS.json"), "w") as f:
    json.dump(R, f, indent=2, ensure_ascii=False)
print("\nWritten: out/REFINED_RESULTS.json")

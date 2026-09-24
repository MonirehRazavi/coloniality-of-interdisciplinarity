"""
analysis_cross_corpus.py — Chapter 6, §6.4, §6.5, §6.7
======================================================
The cross-corpus analyses. These are the ones bibliometrix cannot perform,
because bibliometrix's unit of work is a single corpus: it can tell you what
TS-J cites, but not what proportion of what TS-J cites is AS-J, nor how that
compares with the reverse direction.

Run:  python3 analysis_cross_corpus.py
Out:  ../out/*.json, ../out/*.csv  (every number reported in §§6.4–6.7)

Each step prints what it is doing and why, so the console transcript is itself
a record of the procedure.
"""
import json, re, csv, os, pickle, random
from collections import Counter, defaultdict

import wos_parser as W
import canon as K

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis_outputs")
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
random.seed(20260806)          # fixed seed: sampling below must be reproducible

RESULTS = {}


def save(name, obj):
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def write_csv(name, rows, header):
    with open(os.path.join(OUT, name + ".csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


# ===========================================================================
# STEP 0 — Load, and re-verify the chain of custody
# ===========================================================================
print("=" * 78)
print("STEP 0 — Loading corpora and re-verifying counts against the frozen searches")
print("=" * 78)
EXPECTED = {"TS-J": 14258, "AS-J": 2763, "AS-T": 18566}
C = {n: W.load_corpus(f"{BASE}/{n}") for n in ["TS-J", "AS-J", "AS-T"]}
audit = {}
for n, recs in C.items():
    audit[n] = {"loaded": len(recs), "expected": EXPECTED[n],
                "match": len(recs) == EXPECTED[n], **W.corpus_stats(recs)}
    print(f"  {n}: loaded {len(recs)} / expected {EXPECTED[n]} "
          f"-> {'OK' if len(recs)==EXPECTED[n] else 'MISMATCH'}")
RESULTS["audit"] = audit
save("00_audit", audit)


# ===========================================================================
# STEP 1 — Build journal-abbreviation sets EMPIRICALLY
# ---------------------------------------------------------------------------
# A cited reference names its source in WoS's abbreviated form (the "J9"
# field), not in the journal's published title. Rather than guess those
# abbreviations, we read them off the corpora themselves: every J9 value
# occurring in AS-J *is*, by construction, an AS journal abbreviation as WoS
# writes it. Same for TS-J. This removes a whole class of silent match failure
# — it is the systematic fix for the dropped-ampersand problem recorded in
# decision D5.
# ===========================================================================
print()
print("=" * 78)
print("STEP 1 — Deriving journal abbreviations from the corpora themselves")
print("=" * 78)


def j9_set(recs):
    """Collect the source forms a corpus's own records carry.

    J9 is the 29-character abbreviation Web of Science uses inside cited-
    reference strings; SO is the full journal title, which does NOT appear in
    cited references. Both are collected (SO is harmless and documents the
    mapping) but only J9 forms and their 20-char truncations can actually
    match, which is what makes the empirical derivation reliable: these are
    the journals' names as the database itself writes them, not as I remember
    them. This is the systematic fix for the dropped-ampersand failure of D5."""
    c = Counter()
    for r in recs:
        j9 = W.NORM(r.get("J9", ""))
        so = W.NORM(r.get("SO", ""))
        if j9:
            c[j9] += 1
        if so:
            c[so] += 1
    return c


TSJ_SOURCES = j9_set(C["TS-J"])
ASJ_SOURCES = j9_set(C["AS-J"])

# Keep only forms attested at least 3 times, to avoid one-off typos entering
# the matcher. Both sets are printed in full so they can be inspected.
TS_ABBR = {s for s, n in TSJ_SOURCES.items() if n >= 3}
AS_ABBR = {s for s, n in ASJ_SOURCES.items() if n >= 3}

print(f"  AS journal source forms ({len(AS_ABBR)}):")
for s in sorted(AS_ABBR):
    print(f"      {s}  (n={ASJ_SOURCES[s]})")
print(f"  TS journal source forms ({len(TS_ABBR)}) — first 12 shown:")
for s in sorted(TS_ABBR)[:12]:
    print(f"      {s}  (n={TSJ_SOURCES[s]})")

RESULTS["journal_forms"] = {"AS": sorted(AS_ABBR), "TS": sorted(TS_ABBR)}
save("01_journal_forms", RESULTS["journal_forms"])


# ===========================================================================
# STEP 2 — Parse every cited reference once, and report the parse rate
# ---------------------------------------------------------------------------
# Reported because §6.4 must state its match rate. A reference that cannot be
# parsed cannot be matched, and pretending otherwise would inflate confidence.
# ===========================================================================
print()
print("=" * 78)
print("STEP 2 — Parsing cited references; reporting parse rate (§6.4 match rate)")
print("=" * 78)

PARSED = {}
for n, recs in C.items():
    rows, ok, bad = [], 0, 0
    for i, cr in W.iter_refs(recs):
        a, y, s = W.split_cr(cr)
        if a is None:
            bad += 1
            rows.append((i, None, None, None))
        else:
            ok += 1
            rows.append((i, a, y, s))
    PARSED[n] = rows
    rate = 100 * ok / (ok + bad) if ok + bad else 0
    print(f"  {n}: {ok:,} of {ok+bad:,} references parsed ({rate:.1f}%); "
          f"{bad:,} unparseable")
    audit[n]["references_parsed"] = ok
    audit[n]["references_unparseable"] = bad
    audit[n]["parse_rate_pct"] = round(rate, 2)
save("00_audit", audit)


# ===========================================================================
# STEP 3 — §6.4(a): the word 'adaptation' inside TS-J
# ---------------------------------------------------------------------------
# Chapter 5 ¶673: "the term adaptation circulates everywhere in TS, but the
# field it names is cited almost nowhere." (a) measures the first half.
# ===========================================================================
print()
print("=" * 78)
print("STEP 3 — §6.4(a) The term 'adaptation' in TS-J: title, abstract, keywords")
print("=" * 78)


def field_text(r, fields):
    """Concatenate the requested fields into one lower-cased blob.

    NOTE (D14): DE/ID/SC/WC are now stored as joined text rather than as one
    item per line, because Web of Science wraps them mid-item. Joining the
    fields with " ; " here is safe precisely because the within-field wrap has
    already been repaired by the parser."""
    parts = []
    for f in fields:
        v = r.get(f)
        if isinstance(v, list):
            parts.extend(v)
        elif v:
            parts.append(v)
    return " ; ".join(parts).lower()


def count_term(recs, term, fields):
    rx = re.compile(r"\b" + term + r"\w*", re.I)
    return sum(1 for r in recs if rx.search(field_text(r, fields)))


tsj = C["TS-J"]
term_stats = {
    "TS-J records": len(tsj),
    "mentioning 'adaptation' anywhere (TI/AB/DE/ID)":
        count_term(tsj, "adaptation", ["TI", "AB", "DE", "ID"]),
    "with 'adaptation' in title": count_term(tsj, "adaptation", ["TI"]),
    "with 'adaptation' as author keyword": count_term(tsj, "adaptation", ["DE"]),
    "mentioning the phrase 'adaptation studies'":
        sum(1 for r in tsj if "adaptation studies" in field_text(r, ["TI", "AB", "DE", "ID"])),
    "with 'adaptation studies' in title/abstract/keywords (vD&R replication)":
        sum(1 for r in tsj if "adaptation studies" in field_text(r, ["TI", "AB", "DE"])),
}
for k, v in term_stats.items():
    pct = f"  ({100*v/len(tsj):.2f}%)" if isinstance(v, int) and k != "TS-J records" else ""
    print(f"  {k}: {v:,}{pct}")
RESULTS["6.4a_term_presence"] = term_stats
save("02_term_presence", term_stats)


# ===========================================================================
# STEP 4 — §6.4(b)+(c): the AS canon and AS journals in TS-J's references,
#          benchmarked; and the mirror test (TS canon in AS-J).
# ===========================================================================
print()
print("=" * 78)
print("STEP 4 — §6.4(b,c) Canon matching, with benchmark comparison classes")
print("=" * 78)


def author_index(parsed_rows):
    """(SURNAME, INITIAL) -> [n_references, set of citing record indices]

    Uses wos_parser.norm_author() so that the four Web of Science renderings of
    the same person collapse to one key. See the note in wos_parser.py (D9)."""
    idx = defaultdict(lambda: [0, set()])
    for i, a, y, s in parsed_rows:
        if a:
            key = W.norm_author(a)
            if key[0]:
                idx[key][0] += 1
                idx[key][1].add(i)
    return idx


AIDX = {n: author_index(PARSED[n]) for n in C}


def match_group(corpus, group):
    """Count references and citing documents for each name in a canon group."""
    idx, out = AIDX[corpus], {}
    for label, variants in group.items():
        refs, docs = 0, set()
        hit_variants = {}
        for v in variants:
            if v in idx:
                refs += idx[v][0]
                docs |= idx[v][1]
                hit_variants[v] = idx[v][0]
        out[label] = {"references": refs, "citing_documents": len(docs),
                      "pct_of_corpus": round(100 * len(docs) / len(C[corpus]), 3),
                      # tuple keys stringified so the record is JSON-serialisable
                      "variants_matched": {f"{k[0]}, {k[1]}": v
                                           for k, v in hit_variants.items()}}
    return out


def group_total(corpus, group):
    idx, refs, docs = AIDX[corpus], 0, set()
    for variants in group.values():
        for v in variants:
            if v in idx:
                refs += idx[v][0]
                docs |= idx[v][1]
    return {"references": refs, "citing_documents": len(docs),
            "pct_of_corpus_documents": round(100 * len(docs) / len(C[corpus]), 2),
            "per_10k_references": round(10000 * refs / audit[corpus]["references_parsed"], 1)}


as_in_ts = match_group("TS-J", K.AS_CANON)
ts_in_as = match_group("AS-J", K.TS_CANON)

print("\n  (b) AS canon inside TS-J:")
for k, v in sorted(as_in_ts.items(), key=lambda x: -x[1]["references"]):
    print(f"      {k:26s} refs={v['references']:5d}  docs={v['citing_documents']:5d}"
          f"  ({v['pct_of_corpus']:.2f}% of TS-J)")
print(f"    TOTAL: {group_total('TS-J', K.AS_CANON)}")

print("\n  MIRROR — TS canon inside AS-J:")
for k, v in sorted(ts_in_as.items(), key=lambda x: -x[1]["references"])[:12]:
    print(f"      {k:26s} refs={v['references']:5d}  docs={v['citing_documents']:5d}"
          f"  ({v['pct_of_corpus']:.2f}% of AS-J)")
print(f"    TOTAL: {group_total('AS-J', K.TS_CANON)}")

print("\n  (c) BENCHMARK — comparison classes inside TS-J:")
bench = {}
for field, group in K.BENCHMARKS.items():
    bench[field] = group_total("TS-J", group)
    print(f"      {field:34s} refs={bench[field]['references']:6d}  "
          f"docs={bench[field]['citing_documents']:5d}  "
          f"({bench[field]['pct_of_corpus_documents']:.2f}% of TS-J)")
bench["Adaptation Studies canon"] = group_total("TS-J", K.AS_CANON)
print(f"      {'Adaptation Studies canon':34s} "
      f"refs={bench['Adaptation Studies canon']['references']:6d}  "
      f"docs={bench['Adaptation Studies canon']['citing_documents']:5d}  "
      f"({bench['Adaptation Studies canon']['pct_of_corpus_documents']:.2f}% of TS-J)")

RESULTS["6.4b_as_canon_in_TSJ"] = as_in_ts
RESULTS["6.4b_ts_canon_in_ASJ"] = ts_in_as
RESULTS["6.4c_benchmarks_in_TSJ"] = bench
RESULTS["6.4b_totals"] = {"AS_canon_in_TSJ": group_total("TS-J", K.AS_CANON),
                          "TS_canon_in_ASJ": group_total("AS-J", K.TS_CANON)}
save("03_canon_matching", {"as_in_ts": as_in_ts, "ts_in_as": ts_in_as,
                           "benchmarks": bench, "totals": RESULTS["6.4b_totals"]})

write_csv("t64_as_canon_in_TSJ",
          [[k, v["references"], v["citing_documents"], v["pct_of_corpus"]]
           for k, v in sorted(as_in_ts.items(), key=lambda x: -x[1]["references"])],
          ["Author", "Cited references in TS-J", "Citing documents", "% of TS-J documents"])
write_csv("t64_ts_canon_in_ASJ",
          [[k, v["references"], v["citing_documents"], v["pct_of_corpus"]]
           for k, v in sorted(ts_in_as.items(), key=lambda x: -x[1]["references"])],
          ["Author", "Cited references in AS-J", "Citing documents", "% of AS-J documents"])
write_csv("t64_benchmarks",
          [[k, v["references"], v["citing_documents"], v["pct_of_corpus_documents"],
            v["per_10k_references"]] for k, v in
           sorted(bench.items(), key=lambda x: -x[1]["references"])],
          ["Comparison class", "Cited references in TS-J", "Citing documents",
           "% of TS-J documents", "References per 10,000"])


# ===========================================================================
# STEP 5 — §6.5: the directional ledger, normalised by REFERENCES not documents
# ---------------------------------------------------------------------------
# Design document Part IV, Q2: "Normalise by total references (not document
# count) — corpora differ in size *and* in average reference-list length."
# TS-J averages 25.5 refs/record, AS-J 18.5, so document-normalisation alone
# would bias the comparison by ~38%.
# ===========================================================================
print()
print("=" * 78)
print("STEP 5 — §6.5 Directional cross-citation ledger (journal-level)")
print("=" * 78)


def journal_hits(corpus, abbr_set):
    """Match a cited reference's source field against a set of journal forms.

    Web of Science TRUNCATES the cited-source string to 20 characters
    ("DESCRIPTIVE TRANSLAT", "OXFORD HDB ADAPTATIO"), so a plain equality test
    silently misses every journal whose abbreviation is longer than 20 chars.
    Each known form is therefore also registered under its 20-character prefix,
    and matching is exact against that expanded set. Exact-on-prefix rather
    than substring: substring matching on "ADAPTATION" would capture every book
    title containing the word, which is the very confusion §6.3.2 is about."""
    expanded = set()
    for f in abbr_set:
        expanded.add(f)
        if len(f) > 20:
            expanded.add(f[:20])
    refs, docs = 0, set()
    per_form = Counter()
    for i, a, y, s in PARSED[corpus]:
        if s and s in expanded:
            refs += 1
            docs.add(i)
            per_form[s] += 1
    return refs, docs, per_form


ts2as_refs, ts2as_docs, ts2as_forms = journal_hits("TS-J", AS_ABBR)
as2ts_refs, as2ts_docs, as2ts_forms = journal_hits("AS-J", TS_ABBR)
ast2ts_refs, ast2ts_docs, _ = journal_hits("AS-T", TS_ABBR)

ledger = {
    "TS-J -> AS journals": {
        "references": ts2as_refs,
        "per_10k_parsed_references": round(10000 * ts2as_refs / audit["TS-J"]["references_parsed"], 2),
        "citing_documents": len(ts2as_docs),
        "pct_of_corpus_documents": round(100 * len(ts2as_docs) / len(C["TS-J"]), 2),
        "by_journal": dict(ts2as_forms.most_common()),
    },
    "AS-J -> TS journals": {
        "references": as2ts_refs,
        "per_10k_parsed_references": round(10000 * as2ts_refs / audit["AS-J"]["references_parsed"], 2),
        "citing_documents": len(as2ts_docs),
        "pct_of_corpus_documents": round(100 * len(as2ts_docs) / len(C["AS-J"]), 2),
        "by_journal": dict(as2ts_forms.most_common(15)),
    },
    "AS-T -> TS journals": {
        "references": ast2ts_refs,
        "per_10k_parsed_references": round(10000 * ast2ts_refs / audit["AS-T"]["references_parsed"], 2),
        "citing_documents": len(ast2ts_docs),
        "pct_of_corpus_documents": round(100 * len(ast2ts_docs) / len(C["AS-T"]), 2),
    },
}
a = ledger["TS-J -> AS journals"]["per_10k_parsed_references"]
b = ledger["AS-J -> TS journals"]["per_10k_parsed_references"]
ledger["asymmetry_ratio_AS_to_TS_over_TS_to_AS"] = round(b / a, 2) if a else None

for k in ["TS-J -> AS journals", "AS-J -> TS journals", "AS-T -> TS journals"]:
    v = ledger[k]
    print(f"  {k:24s} refs={v['references']:6d}  "
          f"per10k={v['per_10k_parsed_references']:8.2f}  "
          f"docs={v['citing_documents']:5d} ({v['pct_of_corpus_documents']:.2f}%)")
print(f"\n  Asymmetry ratio (AS->TS : TS->AS) = "
      f"{ledger['asymmetry_ratio_AS_to_TS_over_TS_to_AS']} : 1")

# Author-level ledger — the canon comparison, normalised the same way.
ledger["author_level"] = {
    "AS canon per 10k TS-J refs":
        round(10000 * group_total("TS-J", K.AS_CANON)["references"] / audit["TS-J"]["references_parsed"], 2),
    "TS canon per 10k AS-J refs":
        round(10000 * group_total("AS-J", K.TS_CANON)["references"] / audit["AS-J"]["references_parsed"], 2),
    "TS canon per 10k AS-T refs":
        round(10000 * group_total("AS-T", K.TS_CANON)["references"] / audit["AS-T"]["references_parsed"], 2),
    "AS canon per 10k AS-J refs (self-reference baseline)":
        round(10000 * group_total("AS-J", K.AS_CANON)["references"] / audit["AS-J"]["references_parsed"], 2),
    "TS canon per 10k TS-J refs (self-reference baseline)":
        round(10000 * group_total("TS-J", K.TS_CANON)["references"] / audit["TS-J"]["references_parsed"], 2),
}
print("\n  Author-level, per 10,000 parsed references:")
for k, v in ledger["author_level"].items():
    print(f"      {k:56s} {v:8.2f}")

RESULTS["6.5_ledger"] = ledger
save("04_directional_ledger", ledger)


# ===========================================================================
# STEP 6 — §6.5b: WHAT KIND of citation travels in each direction
# ---------------------------------------------------------------------------
# The claim (§3.1.5, §5.6): the centre supplies concepts, the margin supplies
# cases. Operationalised as: of the cross-citations that occur, what share go
# to the other field's *theoretical canon* (its definitional apparatus) versus
# to its journal literature (its case material)?
# ===========================================================================
print()
print("=" * 78)
print("STEP 6 — §6.5(b) Kind of citation: definitional apparatus vs case material")
print("=" * 78)

kind = {
    "AS-J citing TS": {
        "to TS canonical theorists": group_total("AS-J", K.TS_CANON)["references"],
        "to TS journal articles": as2ts_refs,
    },
    "TS-J citing AS": {
        "to AS canonical theorists": group_total("TS-J", K.AS_CANON)["references"],
        "to AS journal articles": ts2as_refs,
    },
}
for k, v in kind.items():
    tot = sum(v.values())
    v["total"] = tot
    v["pct_to_canon"] = round(100 * list(v.values())[0] / tot, 1) if tot else None
    print(f"  {k}: canon={list(v.values())[0]}, journals={list(v.values())[1]}, "
          f"canon share={v['pct_to_canon']}%")
RESULTS["6.5b_citation_kind"] = kind
save("05_citation_kind", kind)


# ===========================================================================
# STEP 7 — §6.7: markedness. Bare term vs modified term, in each corpus.
# ===========================================================================
print()
print("=" * 78)
print("STEP 7 — §6.7 Markedness: bare vs modified forms of each field's own term")
print("=" * 78)


def markedness(recs, term, modifiers, fields=("TI", "AB", "DE", "ID")):
    mods = sorted(modifiers, key=len, reverse=True)
    mod_rx = re.compile(r"\b(" + "|".join(re.escape(m) for m in mods) + r")[\s\-]+" + term + r"s?\b", re.I)
    any_rx = re.compile(r"\b" + term + r"s?\b", re.I)
    marked = Counter()
    n_marked = n_bare = n_any = 0
    for r in recs:
        t = field_text(r, list(fields))
        hits = mod_rx.findall(t)
        allhits = any_rx.findall(t)
        if not allhits:
            continue
        n_any += 1
        if hits:
            n_marked += 1
            for h in hits:
                marked[h.lower()] += 1
        # a document counts as "bare" if the term appears at least once NOT
        # preceded by a modifier
        stripped = mod_rx.sub(" ", t)
        if any_rx.search(stripped):
            n_bare += 1
    return {"documents_using_term": n_any,
            "documents_with_modified_use": n_marked,
            "documents_with_bare_use": n_bare,
            "pct_bare": round(100 * n_bare / n_any, 1) if n_any else None,
            "pct_modified": round(100 * n_marked / n_any, 1) if n_any else None,
            "top_modifiers": dict(marked.most_common(15))}


mk = {
    "'translation' in TS-J": markedness(C["TS-J"], "translation", K.TRANSLATION_MODIFIERS),
    "'adaptation' in TS-J": markedness(C["TS-J"], "adaptation", K.ADAPTATION_MODIFIERS),
    "'adaptation' in AS-J": markedness(C["AS-J"], "adaptation", K.ADAPTATION_MODIFIERS),
    "'translation' in AS-J": markedness(C["AS-J"], "translation", K.TRANSLATION_MODIFIERS),
    "'adaptation' in AS-T": markedness(C["AS-T"], "adaptation", K.ADAPTATION_MODIFIERS),
}
for k, v in mk.items():
    print(f"  {k:26s} n={v['documents_using_term']:6d}  "
          f"bare={v['pct_bare']:5.1f}%  modified={v['pct_modified']:5.1f}%")
    print(f"      top modifiers: {', '.join(list(v['top_modifiers'])[:6])}")
RESULTS["6.7_markedness"] = mk
save("06_markedness", mk)


# ===========================================================================
# STEP 8 — §6.3.4/§6.3.5: the AS-T noise rate, estimated on a random sample
# ---------------------------------------------------------------------------
# The draft has a pending placeholder for this. Estimated by classifying a
# random sample of AS-T records: does the record use 'adaptation' in a
# humanities/media sense, or in a climate/biology/organisational sense? A
# keyword heuristic is applied and the sample is reported so the estimate can
# be checked by hand.
# ===========================================================================
print()
print("=" * 78)
print("STEP 8 — §6.3.4 Estimating residual non-humanities noise in AS-T")
print("=" * 78)

NON_HUM = re.compile(
    r"\b(climate|climatic|global warming|drought|crop|agricultur|farmer|"
    r"ecosystem|species|evolutionar|phenotyp|genotyp|thermal|physiolog|"
    r"neural adaptation|phonolog|loanword|adaptive reuse|resilience to|"
    r"livelihood|smallholder|fishery|biodiversity|carbon|greenhouse)\b", re.I)
HUM = re.compile(
    r"\b(film|cinema|novel|literary|literature|screen|stage|theatre|theater|"
    r"television|adaptation studies|fidelity|narrative|intermedial|comic|"
    r"manga|anime|opera|musical|shakespear|director|audience|spectator)\b", re.I)

SAMPLE_N = 400
sample = random.sample(C["AS-T"], SAMPLE_N)
noise = hum = ambiguous = 0
noise_examples = []
for r in sample:
    t = field_text(r, ["TI", "AB", "DE", "ID"])
    nh, h = bool(NON_HUM.search(t)), bool(HUM.search(t))
    if nh and not h:
        noise += 1
        if len(noise_examples) < 12:
            noise_examples.append(r.get("TI", "")[:110])
    elif h:
        hum += 1
    else:
        ambiguous += 1
noise_est = {
    "sample_size": SAMPLE_N,
    "seed": 20260806,
    "clearly_non_humanities": noise,
    "clearly_humanities_media": hum,
    "ambiguous": ambiguous,
    "estimated_noise_rate_pct": round(100 * noise / SAMPLE_N, 1),
    "estimated_noise_rate_pct_upper_bound_incl_ambiguous":
        round(100 * (noise + ambiguous) / SAMPLE_N, 1),
    "example_non_humanities_titles": noise_examples,
}
print(f"  Sample n={SAMPLE_N} (seed 20260806)")
print(f"  Clearly non-humanities: {noise} ({noise_est['estimated_noise_rate_pct']}%)")
print(f"  Clearly humanities/media: {hum}")
print(f"  Ambiguous: {ambiguous}")
print(f"  Estimated noise rate: {noise_est['estimated_noise_rate_pct']}% "
      f"(upper bound incl. ambiguous: "
      f"{noise_est['estimated_noise_rate_pct_upper_bound_incl_ambiguous']}%)")
print("  Examples classified as non-humanities:")
for e in noise_examples[:6]:
    print(f"      - {e}")
RESULTS["6.3.4_noise_estimate"] = noise_est
save("07_noise_estimate", noise_est)


# ===========================================================================
# STEP 9 — §6.6 support: local citation of frontier vs core authors in TS-J
# ===========================================================================
print()
print("=" * 78)
print("STEP 9 — §6.6 Frontier vs core: citation within TS-J's own reference record")
print("=" * 78)

front = match_group("TS-J", K.FRONTIER)
core = match_group("TS-J", K.CORE)
amb = match_group("TS-J", K.AMBIGUOUS_FRONTIER)

print("  CORE (institutional defaults):")
for k, v in sorted(core.items(), key=lambda x: -x[1]["references"]):
    print(f"      {k:26s} refs={v['references']:5d}  docs={v['citing_documents']:5d}")
print("  FRONTIER (expansionist critics):")
for k, v in sorted(front.items(), key=lambda x: -x[1]["references"]):
    print(f"      {k:26s} refs={v['references']:5d}  docs={v['citing_documents']:5d}")
print("  REPORTED SEPARATELY (classification ambiguous — see canon.py note):")
for k, v in amb.items():
    print(f"      {k:26s} refs={v['references']:5d}  docs={v['citing_documents']:5d}")

fc = {
    "core_total": group_total("TS-J", K.CORE),
    "frontier_total": group_total("TS-J", K.FRONTIER),
    "ambiguous_bassnett": group_total("TS-J", K.AMBIGUOUS_FRONTIER),
    "core_members": len(K.CORE), "frontier_members": len(K.FRONTIER),
}
fc["core_mean_refs_per_author"] = round(fc["core_total"]["references"] / fc["core_members"], 1)
fc["frontier_mean_refs_per_author"] = round(fc["frontier_total"]["references"] / fc["frontier_members"], 1)
fc["core_to_frontier_ratio"] = round(
    fc["core_mean_refs_per_author"] / fc["frontier_mean_refs_per_author"], 2)
print(f"\n  Core mean {fc['core_mean_refs_per_author']} refs/author vs "
      f"frontier mean {fc['frontier_mean_refs_per_author']} "
      f"-> ratio {fc['core_to_frontier_ratio']}:1")
RESULTS["6.6_frontier_vs_core"] = {"core": core, "frontier": front,
                                   "ambiguous": amb, "summary": fc}
save("08_frontier_vs_core", RESULTS["6.6_frontier_vs_core"])

write_csv("t66_frontier_vs_core",
          [[k, "core", v["references"], v["citing_documents"]] for k, v in core.items()] +
          [[k, "frontier", v["references"], v["citing_documents"]] for k, v in front.items()] +
          [[k, "ambiguous", v["references"], v["citing_documents"]] for k, v in amb.items()],
          ["Author", "Group", "Cited references in TS-J", "Citing documents"])


# ===========================================================================
# STEP 10 — §6.8/§6.9 inputs: fidelity/equivalence over time, and RPYS
# ===========================================================================
print()
print("=" * 78)
print("STEP 10 — §6.8 term trajectories and §6.9 reference-year spectroscopy")
print("=" * 78)


def term_by_year(recs, terms, fields=("TI", "AB", "DE", "ID")):
    per_year_total, per_year_hit = Counter(), Counter()
    rx = re.compile(r"\b(" + "|".join(terms) + r")\w*", re.I)
    for r in recs:
        py = r.get("PY", "")
        if not py.isdigit():
            continue
        y = int(py)
        per_year_total[y] += 1
        if rx.search(field_text(r, list(fields))):
            per_year_hit[y] += 1
    return {y: {"documents": per_year_total[y], "with_term": per_year_hit[y],
                "pct": round(100 * per_year_hit[y] / per_year_total[y], 2)}
            for y in sorted(per_year_total) if per_year_total[y] >= 10}


clocks = {
    "TS-J fidelity/faithfulness": term_by_year(C["TS-J"], ["fidelit", "faithful"]),
    "TS-J equivalence": term_by_year(C["TS-J"], ["equivalen"]),
    "AS-J fidelity/faithfulness": term_by_year(C["AS-J"], ["fidelit", "faithful"]),
    "AS-J equivalence": term_by_year(C["AS-J"], ["equivalen"]),
}


def weighted_median_year(series):
    pairs = [(y, d["with_term"]) for y, d in series.items()]
    tot = sum(n for _, n in pairs)
    if tot == 0:
        return None
    run = 0
    for y, n in sorted(pairs):
        run += n
        if run >= tot / 2:
            return y
    return None


clock_summary = {k: {"median_year_of_use": weighted_median_year(v),
                     "total_documents_using_term": sum(d["with_term"] for d in v.values())}
                 for k, v in clocks.items()}
for k, v in clock_summary.items():
    print(f"  {k:32s} median year = {v['median_year_of_use']}  "
          f"(n={v['total_documents_using_term']})")
lag = None
if clock_summary["AS-J fidelity/faithfulness"]["median_year_of_use"] and \
   clock_summary["TS-J fidelity/faithfulness"]["median_year_of_use"]:
    lag = (clock_summary["AS-J fidelity/faithfulness"]["median_year_of_use"] -
           clock_summary["TS-J fidelity/faithfulness"]["median_year_of_use"])
print(f"\n  Fidelity lag (AS median - TS median) = {lag} years")
RESULTS["6.8_two_clocks"] = {"series": clocks, "summary": clock_summary,
                             "fidelity_lag_years": lag}
save("09_two_clocks", RESULTS["6.8_two_clocks"])


def rpys(corpus, lo=1900, hi=2025):
    c = Counter()
    for i, a, y, s in PARSED[corpus]:
        if y and lo <= y <= hi:
            c[y] += 1
    years = sorted(c)
    # Deviation from the 5-year median — the standard RPYS transform, which
    # turns a growth curve into visible spikes.
    dev = {}
    for y in years:
        window = [c.get(yy, 0) for yy in range(y - 2, y + 3)]
        med = sorted(window)[len(window) // 2]
        dev[y] = c[y] - med
    return c, dev


rp = {}
for n in ["TS-J", "AS-J"]:
    c, dev = rpys(n)
    peaks = sorted(dev.items(), key=lambda x: -x[1])[:15]
    rp[n] = {"counts": {str(k): v for k, v in sorted(c.items())},
             "top_peaks_by_deviation": [{"year": y, "deviation": d, "references": c[y]}
                                        for y, d in peaks]}
    print(f"\n  RPYS {n} — top reference-year peaks (deviation from 5-yr median):")
    for y, d in peaks[:10]:
        print(f"      {y}: {c[y]:5d} refs  (deviation +{d})")
RESULTS["6.9_rpys"] = rp
save("10_rpys", rp)


# ===========================================================================
# STEP 11 — §6.9b: structural separation (author and source overlap)
# ===========================================================================
print()
print("=" * 78)
print("STEP 11 — §6.9(b) Structural separation: author and cited-source overlap")
print("=" * 78)


def authors_of(recs):
    """Distinct authors, normalised to (SURNAME, INITIAL).

    CORRECTION (D15): this originally compared exact full-name strings from
    the AF field. That reproduced, in the overlap measure, exactly the bug D9
    documents for cited references — Web of Science writes the same person as
    'CATTRYSSE, P' and 'CATTRYSSE, PATRICK', and both appeared in the overlap
    set as two different people. Applying the same surname+initial rule used
    everywhere else raised the measured TS-J/AS-J author overlap from 45 to
    140. The under-count was threefold and ran in the direction that flattered
    the chapter's own argument, which is the reason to state it plainly."""
    out = set()
    for r in recs:
        for a in (r.get("AF") or r.get("AU") or []):
            sn, ini = W.norm_author(a)
            if sn:
                out.add((sn, ini))
    return out


A_ts, A_as = authors_of(C["TS-J"]), authors_of(C["AS-J"])
overlap = A_ts & A_as
sep = {
    "TS-J unique authors": len(A_ts),
    "AS-J unique authors": len(A_as),
    "authors appearing in both": len(overlap),
    "pct_of_AS-J_authors_also_in_TS-J": round(100 * len(overlap) / len(A_as), 2),
    "pct_of_TS-J_authors_also_in_AS-J": round(100 * len(overlap) / len(A_ts), 2),
    "example_overlapping_authors": [f"{a}, {b}" for a, b in sorted(overlap)[:25]],
}
for k, v in sep.items():
    if k != "example_overlapping_authors":
        print(f"  {k}: {v}")

# cited-source overlap (co-citation of venues)
def cited_sources(corpus, top=300):
    c = Counter()
    for i, a, y, s in PARSED[corpus]:
        if s:
            c[s] += 1
    return c


S_ts, S_as = cited_sources("TS-J"), cited_sources("AS-J")
top_ts = {s for s, _ in S_ts.most_common(300)}
top_as = {s for s, _ in S_as.most_common(300)}
sep["top300_cited_source_overlap"] = len(top_ts & top_as)
sep["top300_overlapping_sources"] = sorted(top_ts & top_as)[:30]
print(f"  Top-300 cited-source overlap: {sep['top300_cited_source_overlap']} of 300")
RESULTS["6.9b_separation"] = sep
save("11_structural_separation", sep)


# ===========================================================================
print()
print("=" * 78)
print("Writing consolidated results")
print("=" * 78)
# Deposit the raw cited-reference author-form counts for the authors the
# chapter discusses by name, so that every figure quoted in §6.4.5 and in
# decision-log D9 is recoverable from the outputs rather than asserted.
raw_forms = {}
for corpus in C:
    cnt = Counter()
    for i, a, y, s_ in PARSED[corpus]:
        if a:
            cnt[a] += 1
    raw_forms[corpus] = {
        name: {f: n for f, n in cnt.items() if f.startswith(name)}
        for name in ["TOURY", "JAKOBSON", "BLUESTONE", "HUTCHEON", "VENUTI",
                     "STAM ", "LEITCH", "MCFARLANE", "HOLMES", "CATTRYSSE"]
    }
save("12_raw_author_forms", raw_forms)
RESULTS["raw_author_forms_TSJ_TOURY"] = raw_forms["TS-J"]["TOURY"]

# ---------------------------------------------------------------------------
# STEP 11 (added 22 Sep 2026, D18) — the two founders across all three
# corpora: Table 6.1 of the thesis.  This had been computed by hand in
# August from the parsed references; it is now written to its own file so
# that Table 6.1 is derivable from the outputs like every other table.
# "per 10,000" is per 10,000 PARSED references, the denominator used
# throughout the thesis.
# ---------------------------------------------------------------------------
founders = {}
for corpus in C:
    n_docs = len(C[corpus])
    n_parsed = sum(1 for _i, a, _y, _s in PARSED[corpus] if a)
    founders[corpus] = {"documents": n_docs, "parsed_references": n_parsed}
    for label, key in [("Jakobson, Roman", ("JAKOBSON", "R")),
                       ("Bluestone, George", ("BLUESTONE", "G")),
                       ("Hutcheon, Linda", ("HUTCHEON", "L"))]:
        refs, docs = 0, set()
        for i, a, _y, _s in PARSED[corpus]:
            if a and W.norm_author(a) == key:
                refs += 1
                docs.add(i)
        founders[corpus][label] = {
            "references": refs, "citing_documents": len(docs),
            "pct_of_corpus": round(100 * len(docs) / n_docs, 2),
            "per_10k_parsed_references": round(1e4 * refs / n_parsed, 2)}
save("13_founders_across_corpora", founders)
print("  Table 6.1 (founders across corpora) written to 13_founders_across_corpora.json")

save("ALL_RESULTS", RESULTS)
with open(os.path.join(OUT, "corpora.pkl"), "wb") as f:
    pickle.dump({"C": C, "PARSED": PARSED, "AS_ABBR": sorted(AS_ABBR),
                 "TS_ABBR": sorted(TS_ABBR)}, f)
print("Done. Results in ../analysis_outputs/")

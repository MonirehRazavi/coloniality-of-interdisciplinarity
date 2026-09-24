"""
wos_parser.py — Chapter 6, PhD dissertation (M. Razavi)
======================================================
A minimal, dependency-light parser for Web of Science "field-tagged" plain-text
exports (the format produced by WoS's Export > Plain text > Record Content =
"Full Record and Cited References").

WHY THIS EXISTS
---------------
The standard tool for this chapter is R's bibliometrix, and bibliometrix's
convert2df() is used for every analysis it supports. But three of Chapter 6's
analyses are CROSS-CORPUS reference-matching problems (§6.4, §6.5) plus a
markedness regex pass (§6.7), and bibliometrix has no function for any of them:
its unit of work is one corpus at a time. Those analyses are therefore written
here from scratch, which is what §6.3.1 of the chapter describes as "purpose-
written scripts for the cross-corpus reference matching that no off-the-shelf
tool performs."

THE FILE FORMAT, IN PLAIN LANGUAGE
----------------------------------
A WoS export is a text file of stacked records. Each record:

    PT J                          <- "Publication Type": J = journal. Starts a record.
    AU Fresno, N                  <- a two-letter TAG, a space, then the value
       Igareda, P                 <- continuation: 3 leading spaces = "still the AU field"
    TI Subtitle speed in the ...
    SO PERSPECTIVES-STUDIES IN ...
    PY 2024
    CR Toury G, 1995, DESCRIPTIVE TRANSL, P1     <- one cited reference per line
       Venuti L, 1995, TRANSLATOR INVISIB
    UT WOS:000123456700001        <- the record's unique accession number
    ER                            <- "End of Record"

So parsing is: walk the lines; a line whose first two characters are a tag and
whose third is a space starts a new field; a line starting with three spaces
continues the previous field; "ER" closes the record.

Multi-value fields (authors, keywords, cited references) are kept as LISTS,
because for AU/DE/ID/CR each continuation line is a separate item, not a
continuation of a sentence. Single-value fields (TI, AB, SO) are joined with a
space, because there a continuation line really is the rest of a sentence.
"""

import os
import re
import glob
import unicodedata

# Fields where each line is a SEPARATE ITEM rather than a wrapped sentence.
#
# CORRECTION, 6 Aug 2026 (decision log D14): DE, ID, SC and WC were originally
# in this set. They do not belong here. Web of Science WRAPS these fields at
# the line width and separates their items with semicolons, so a keyword may
# straddle a line break:
#
#       DE literary translation; adaptation; literary adaptation; adaptation
#          studies; Herman Melville; Moby Dick; men's literature; Danish
#
# Treating each line as an item split "adaptation studies" into "adaptation"
# and "studies", which made one record invisible to the phrase search that
# replicates van Doorslaer and Raw (§6.4.2) — the single most rhetorically
# loaded count in the chapter. These fields are now joined with a space and
# split on the semicolon, which is what the format actually specifies.
#
# AU, AF, CR and C1 genuinely do carry one item per line and stay here.
LIST_FIELDS = {"AU", "AF", "CR", "C1", "FU", "OI", "RI"}

# Fields that wrap and are semicolon-delimited.
SEMICOLON_FIELDS = {"DE", "ID", "SC", "WC"}

# Fields we keep. Dropping the rest keeps memory sane on the 18,566-record corpus.
KEEP = {
    "PT", "AU", "AF", "TI", "SO", "LA", "DT", "DE", "ID", "AB",
    "C1", "CR", "NR", "TC", "PY", "J9", "JI", "VL", "DI",
    "WC", "SC", "UT", "SN", "PU", "BP", "EP",
}


def _norm(s):
    """Strip accents and upper-case, so 'Cadernos de Tradução' and
    'CADERNOS DE TRADUCAO' compare equal. WoS is inconsistent about accents in
    cited-reference strings, which would otherwise cause silent match failures."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.upper().strip()


def parse_file(path):
    """Parse one WoS plain-text export file into a list of record dicts."""
    records, rec, tag = [], None, None
    with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n").rstrip("\r")
            if not line:
                continue
            if line.startswith("PT ") and rec is None:
                rec = {}
                tag = "PT"
                rec["PT"] = line[3:].strip()
                continue
            if rec is None:
                continue  # header lines (FN / VR) before the first record
            if line.strip() == "ER":
                records.append(rec)
                rec, tag = None, None
                continue
            if line.startswith("   "):           # continuation of current field
                if tag and tag in KEEP:
                    val = line[3:].strip()
                    if tag in LIST_FIELDS:
                        rec.setdefault(tag, []).append(val)
                    else:
                        rec[tag] = (rec.get(tag, "") + " " + val).strip()
                continue
            m = re.match(r"^([A-Z0-9]{2}) ?(.*)$", line)   # a new field tag
            if m:
                tag, val = m.group(1), m.group(2).strip()
                if tag in KEEP:
                    if tag in LIST_FIELDS:
                        rec.setdefault(tag, [])
                        if val:
                            rec[tag].append(val)
                    else:
                        rec[tag] = val
    return records


def load_corpus(folder, dedupe=True, verbose=True):
    """Load every .txt directly inside `folder` (NOT subfolders, so the
    quarantined _duplicates/ directory is excluded exactly as load_corpora.R
    excludes it), then de-duplicate on UT — the WoS accession number, the
    database's own unique identifier. Deduplicating on UT rather than on title
    is deliberate: title matching produces false merges between, e.g., an
    article and its own erratum."""
    files = sorted(glob.glob(os.path.join(folder, "*.txt")))
    allrecs = []
    for f in files:
        allrecs.extend(parse_file(f))
    raw = len(allrecs)
    if dedupe:
        seen, out = set(), []
        for r in allrecs:
            ut = r.get("UT", "")
            if ut and ut in seen:
                continue
            if ut:
                seen.add(ut)
            out.append(r)
        allrecs = out
    if verbose:
        print(f"  {os.path.basename(folder):6s}  files={len(files):3d}  "
              f"raw={raw:6d}  unique={len(allrecs):6d}")
    return allrecs


# --------------------------------------------------------------------------
# Cited-reference helpers
# --------------------------------------------------------------------------
# A WoS cited-reference string looks like one of:
#     Toury G, 1995, DESCRIPTIVE TRANSLATION STUDIES, P12, DOI 10.1075/btl.4
#     Hutcheon L, 2006, THEORY ADAPTATION
#     Venuti L, 1995, TRANSLATORS INVISIBILITY
# i.e. FIRST-AUTHOR, YEAR, SOURCE-OR-BOOK-TITLE, [volume/page/DOI...]
# Books and journal articles are NOT distinguished by the format; the third
# field is the journal's abbreviated name for an article and the book's
# (abbreviated, uppercased) title for a book. This is why the AS canon — which
# is books — has to be matched on author+year+title-fragment rather than on a
# journal name, and why the match rate must be reported (§6.4).

CR_RE = re.compile(r"^\s*([^,]+),\s*(\d{4}),\s*([^,]*)")


def split_cr(cr_string):
    """Split one cited-reference string into (author, year, source). Returns
    (None, None, None) when the string does not follow the pattern — roughly
    2-4% of references, typically malformed or non-standard entries. Those are
    counted and reported rather than silently dropped."""
    m = CR_RE.match(cr_string)
    if not m:
        return None, None, None
    return _norm(m.group(1)), int(m.group(2)), _norm(m.group(3))


# ---------------------------------------------------------------------------
# AUTHOR-NAME NORMALISATION — the correction of 6 August 2026 (decision D9)
# ---------------------------------------------------------------------------
# An initial version of this analysis matched cited-reference authors by exact
# string ("TOURY G"). Inspection of the actual data showed that Web of Science
# renders the SAME author in at least four ways within a single corpus:
#
#       TOURY GIDEON.   922 references
#       TOURY G.        201
#       TOURY GIDEON    161
#       TOURY G          67
#
# Exact matching therefore captured 67 of 1,351 Toury references — a 20-fold
# undercount. Arts & Humanities Citation Index records give full forenames far
# more often than the science indexes bibliometric convention is built around,
# which is precisely why the naive approach fails here and would not have
# failed on a science corpus.
#
# The correction: reduce every name to (SURNAME, FIRST-INITIAL). This merges
# the four Toury forms while still separating MCFARLANE/B (the adaptation
# theorist) from MCFARLANE/J (a different author entirely). Initial-level
# rather than surname-level matching is the conservative choice: it keeps
# distinct scholars distinct at the cost of splitting the rare author who is
# indexed under two different forenames.
#
# This error is recorded rather than silently repaired, per the decision log's
# standing principle that the chapter should show error correction rather than
# a clean path.

_SUFFIXES = {"JR", "SR", "II", "III", "IV"}


def _is_initialish(tok):
    """True for tokens that are initials rather than forenames: 'G', 'G.',
    'JP', 'KA', 'APL'. Length <= 3 after stripping punctuation."""
    t = tok.replace(".", "").replace(",", "")
    return 1 <= len(t) <= 3 and t.isalpha()


def norm_author(name):
    """Reduce a WoS cited-reference author string to (SURNAME, INITIAL).

    'TOURY GIDEON.'      -> ('TOURY', 'G')
    'TOURY G.'           -> ('TOURY', 'G')
    'VAN DOORSLAER L'    -> ('VAN DOORSLAER', 'L')
    'SNELL-HORNBY M'     -> ('SNELL-HORNBY', 'M')
    'ERICSSON KA'        -> ('ERICSSON', 'K')
    'LEITCH THOMASM.'    -> ('LEITCH', 'T')
    '[ANONYMOUS]'        -> (None, None)
    """
    if not name:
        return None, None
    n = _norm(name)
    if n.startswith("[") or "ANONYMOUS" in n:
        return None, None
    toks = [t for t in n.replace(",", " ").split() if t]
    toks = [t for t in toks if t.replace(".", "") not in _SUFFIXES]
    if not toks:
        return None, None
    if len(toks) == 1:
        return toks[0].replace(".", ""), ""
    # Collect the trailing run of initial-like tokens.
    j = len(toks)
    while j > 1 and _is_initialish(toks[j - 1]):
        j -= 1
    if j < len(toks):                      # found trailing initials
        surname = " ".join(toks[:j])
        initial = toks[j].replace(".", "")[0]
    else:                                  # last token is a spelled-out forename
        surname = " ".join(toks[:-1])
        initial = toks[-1].replace(".", "")[0] if toks[-1].replace(".", "") else ""
    surname = surname.replace(".", "").strip()
    if not surname:
        return None, None
    return surname, initial


def iter_refs(records):
    """Yield (record_index, raw_cr_string) for every cited reference in the corpus."""
    for i, r in enumerate(records):
        for cr in r.get("CR", []):
            yield i, cr


def corpus_stats(records):
    n = len(records)
    with_cr = sum(1 for r in records if r.get("CR"))
    total_refs = sum(len(r.get("CR", [])) for r in records)
    years = [int(r["PY"]) for r in records if r.get("PY", "").isdigit()]
    return {
        "records": n,
        "records_with_references": with_cr,
        "total_cited_references": total_refs,
        "mean_refs_per_record": round(total_refs / n, 2) if n else 0,
        "mean_refs_per_referencing_record": round(total_refs / with_cr, 2) if with_cr else 0,
        "year_min": min(years) if years else None,
        "year_max": max(years) if years else None,
    }


def kw_list(rec, field):
    """Return a field's items as a list, splitting the joined text on the
    semicolon delimiter Web of Science actually uses."""
    v = rec.get(field, "")
    if isinstance(v, list):
        v = " ".join(v)
    return [k.strip() for k in v.split(";") if k.strip()]


NORM = _norm

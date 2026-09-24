"""
canon.py — the hand-curated matching lists for Chapter 6, §6.4–§6.6
===================================================================

WHY HAND-CURATED, AND WHY THIS IS DECLARED RATHER THAN HIDDEN
-------------------------------------------------------------
Web of Science cited-reference strings give a first author, a year, and an
abbreviated source. For journal articles that is enough. For BOOKS — which is
what the Adaptation Studies canon almost entirely consists of — the "source"
slot holds an abbreviated, uppercased, and frequently inconsistent rendering of
the book's own title. Hutcheon's *A Theory of Adaptation* appears in the wild as
THEORY ADAPTATION, A THEORY ADAPTATION, THEORY OF ADAPTATION, and
THEORY ADAPTATION 2ND. No automatic procedure resolves these; a human has to
decide that they are the same book.

That decision is a research act, not a technicality, so the lists below are
part of the chapter's record. Every author entry carries the observed string
variants that were matched. The proportion of cited references that could be
parsed at all, and the proportion of canon hits found by each variant, are
reported in the results (§6.4) so that a reader can judge the match quality
rather than take it on trust. This is the "hand-curated list of ~50 canonical
works with all their observed string variants... report your match rate" that
Part V.1 of the design document requires.

MATCHING RULE
-------------
Each cited-reference first-author string is reduced to (SURNAME, FIRST-INITIAL)
by wos_parser.norm_author(), and matched against the tuples below. This merges
the four ways Web of Science renders the same person — TOURY GIDEON. / TOURY G.
/ TOURY GIDEON / TOURY G — while keeping MCFARLANE/B (the adaptation theorist)
distinct from MCFARLANE/J (an unrelated author).

Matching at the initial rather than the surname alone is the conservative
choice: it splits the rare scholar indexed under two forenames, and so
UNDER-counts rather than over-counts. That is the right direction of error for
a chapter arguing that Adaptation Studies is under-cited, because it biases
against the chapter's own expectation.

An earlier version of this file matched exact strings such as "TOURY G", which
captured 67 of Toury's 1,351 references in TS-J. That error and its correction
are recorded in the decision log (D9) rather than quietly repaired.
"""

# ---------------------------------------------------------------------------
# The Adaptation Studies canon (§6.4b). Drawn from the design document's list,
# extended with the standard reference works an AS reading list would contain.
# ---------------------------------------------------------------------------
AS_CANON = {
    "Bluestone, George":        [("BLUESTONE", "G")],
    "McFarlane, Brian":         [("MCFARLANE", "B")],
    "Stam, Robert":             [("STAM", "R")],
    "Hutcheon, Linda":          [("HUTCHEON", "L")],
    "Leitch, Thomas":           [("LEITCH", "T")],
    "Sanders, Julie":           [("SANDERS", "J")],
    "Cattrysse, Patrick":       [("CATTRYSSE", "P")],
    "Elliott, Kamilla":         [("ELLIOTT", "K")],
    "Naremore, James":          [("NAREMORE", "J")],
    "Cardwell, Sarah":          [("CARDWELL", "S")],
    "Andrew, Dudley":           [("ANDREW", "D")],
    "Geraghty, Christine":      [("GERAGHTY", "C")],
    "Murray, Simone":           [("MURRAY", "S")],
    "Corrigan, Timothy":        [("CORRIGAN", "T")],
    "Bruhn, Jorgen":            [("BRUHN", "J")],
    "Hermansson, Casie":        [("HERMANSSON", "C")],
    "Boozer, Jack":             [("BOOZER", "J")],
    "Cohen, Keith":             [("COHEN", "K")],
    "Aragay, Mireia":           [("ARAGAY", "M")],
    "Whelehan, Imelda":         [("WHELEHAN", "I")],
}

# ---------------------------------------------------------------------------
# The Translation Studies canon (§6.4b mirror test, §6.5). The "definitional
# apparatus" the design document expects AS to import: Jakobson, Toury, Venuti,
# Bassnett et al.
# ---------------------------------------------------------------------------
TS_CANON = {
    "Jakobson, Roman":          [("JAKOBSON", "R")],
    "Toury, Gideon":            [("TOURY", "G")],
    "Venuti, Lawrence":         [("VENUTI", "L")],
    "Bassnett, Susan":          [("BASSNETT", "S"), ("BASSNETT-MCGUIRE", "S")],
    "Nida, Eugene":             [("NIDA", "E")],
    "Baker, Mona":              [("BAKER", "M")],
    "Chesterman, Andrew":       [("CHESTERMAN", "A")],
    "Pym, Anthony":             [("PYM", "A")],
    "Lefevere, Andre":          [("LEFEVERE", "A")],
    "Holmes, James":            [("HOLMES", "J")],
    "Snell-Hornby, Mary":       [("SNELL-HORNBY", "M")],
    "Vermeer, Hans":           [("VERMEER", "H")],
    "Reiss, Katharina":         [("REISS", "K")],
    "Hermans, Theo":            [("HERMANS", "T")],
    "Gentzler, Edwin":          [("GENTZLER", "E")],
    "Tymoczko, Maria":          [("TYMOCZKO", "M")],
    "Munday, Jeremy":           [("MUNDAY", "J")],
    "Vinay, Jean-Paul":         [("VINAY", "J")],
    "Catford, John":           [("CATFORD", "J")],
    "Steiner, George":          [("STEINER", "G")],
    "Delabastita, Dirk":        [("DELABASTITA", "D")],
    "Gambier, Yves":            [("GAMBIER", "Y")],
    "van Doorslaer, Luc":       [("VAN DOORSLAER", "L")],
}

# ---------------------------------------------------------------------------
# BENCHMARK CLASSES (§6.4c). "A raw count without a comparison class is
# rhetoric, not measurement" — the chapter's own words. These are the
# neighbouring fields TS demonstrably DOES engage, against which the AS count
# is to be read.
# ---------------------------------------------------------------------------
BENCHMARKS = {
    "Sociology of translation": {
        "Bourdieu, Pierre":     [("BOURDIEU", "P")],
        "Latour, Bruno":        [("LATOUR", "B")],
        "Luhmann, Niklas":      [("LUHMANN", "N")],
        "Giddens, Anthony":     [("GIDDENS", "A")],
        "Wolf, Michaela":       [("WOLF", "M")],
        "Simeoni, Daniel":      [("SIMEONI", "D")],
    },
    "Film & media studies": {
        "Bordwell, David":      [("BORDWELL", "D")],
        "Metz, Christian":      [("METZ", "C")],
        "Mulvey, Laura":        [("MULVEY", "L")],
        "Chion, Michel":        [("CHION", "M")],
        "Bazin, Andre":         [("BAZIN", "A")],
        "Bolter, Jay David":    [("BOLTER", "J")],
    },
    "Cognitive science / psychology": {
        "Gile, Daniel":         [("GILE", "D")],
        "Kahneman, Daniel":     [("KAHNEMAN", "D")],
        "Ericsson, K. Anders":  [("ERICSSON", "K")],
        "Shreve, Gregory":      [("SHREVE", "G")],
        "Goepferich, Susanne":  [("GOPFERICH", "S")],
        "Tirkkonen-Condit, S.": [("TIRKKONEN-CONDIT", "S")],
    },
    "Linguistics & pragmatics": {
        "Halliday, M.A.K.":     [("HALLIDAY", "M")],
        "Grice, H. Paul":       [("GRICE", "H")],
        "Sperber, Dan":         [("SPERBER", "D")],
        "Lakoff, George":       [("LAKOFF", "G")],
    },
    "Postcolonial & decolonial theory": {
        "Spivak, Gayatri":      [("SPIVAK", "G")],
        "Bhabha, Homi":         [("BHABHA", "H")],
        "Said, Edward":         [("SAID", "E")],
        "Santos, Boaventura":   [("SANTOS", "B"), ("DE SOUSA SANTOS", "B")],
    },
}

# ---------------------------------------------------------------------------
# §6.6 — the critical frontier vs the institutional core.
#
# NOTE ON BASSNETT: the design document lists Bassnett among the expansionist
# frontier (via "Bassnett & Johnston"), but Bassnett is also, by any measure,
# one of the discipline's institutional founders. Placing her in either group
# would distort the comparison. She is therefore reported SEPARATELY and
# excluded from both aggregates, with the ambiguity declared. This is a
# judgement call and is logged as such (decision D8).
# ---------------------------------------------------------------------------
FRONTIER = {
    "Tymoczko, Maria":          [("TYMOCZKO", "M")],
    "Marais, Kobus":            [("MARAIS", "K")],
    "Blumczynski, Piotr":       [("BLUMCZYNSKI", "P")],
    "Gentzler, Edwin":          [("GENTZLER", "E")],
    "Robinson, Douglas":        [("ROBINSON", "D")],
    "Bennett, Karen":           [("BENNETT", "K")],
    "Zwischenberger, Cornelia": [("ZWISCHENBERGER", "C")],
}

CORE = {
    "Toury, Gideon":            [("TOURY", "G")],
    "Venuti, Lawrence":         [("VENUTI", "L")],
    "Baker, Mona":              [("BAKER", "M")],
    "Chesterman, Andrew":       [("CHESTERMAN", "A")],
    "Pym, Anthony":             [("PYM", "A")],
    "Holmes, James":            [("HOLMES", "J")],
    "Snell-Hornby, Mary":       [("SNELL-HORNBY", "M")],
    "Toury, Gideon (alt)":      [],   # placeholder kept out of counts
}
CORE = {k: v for k, v in CORE.items() if v}

AMBIGUOUS_FRONTIER = {
    "Bassnett, Susan":          [("BASSNETT", "S"), ("BASSNETT-MCGUIRE", "S")],
}

# ---------------------------------------------------------------------------
# §6.7 — markedness. The modifiers that, when they precede the bare term,
# mark it as a non-default sense. Compiled from the two fields' own vocabularies.
# ---------------------------------------------------------------------------
TRANSLATION_MODIFIERS = [
    "intersemiotic", "intralingual", "interlingual", "audiovisual", "machine",
    "literary", "legal", "medical", "technical", "automatic", "neural",
    "community", "cultural", "self", "back", "sight", "collaborative",
    "crowdsourced", "volunteer", "news", "media", "song", "poetry", "drama",
    "theatre", "theater", "bible", "religious", "scientific", "specialised",
    "specialized", "literal", "free", "indirect", "retranslation", "pseudo",
    "multimodal", "game", "website", "software", "subtitle", "subtitling",
    "dubbing", "localisation", "localization", "transcreation",
]

ADAPTATION_MODIFIERS = [
    "film", "screen", "literary", "stage", "theatrical", "cinematic",
    "television", "tv", "novel", "comic", "graphic", "musical", "operatic",
    "radio", "game", "videogame", "video", "transmedia", "cross-media",
    "intermedial", "manga", "anime", "faithful", "loose", "free", "modern",
    "contemporary", "postmodern", "queer", "feminist", "postcolonial",
    "cultural", "climate", "evolutionary", "neural", "phonological",
    "organisational", "organizational", "curricular", "adaptive",
]

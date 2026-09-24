"""
analysis_networks.py — Chapter 6, §6.6 and §6.7 (network analyses)
==================================================================
Keyword co-occurrence networks, Louvain community detection, and the Callon
centrality x density thematic map — the analyses §6.6 and §6.7 require.

WHY THIS IS IMPLEMENTED HERE RATHER THAN CALLED FROM bibliometrix
-----------------------------------------------------------------
These are bibliometrix's own analyses, and bibliometrix would be the natural
tool. It could not be used in the analysis environment: the sandbox in which
these scripts were executed has no route to CRAN, and neither R installation
available to it carried the package. The formulas below are therefore
implemented directly from Callon, Courtial & Laville (1991), which is the
source bibliometrix itself implements, and a matching R script
(verify_in_bibliometrix.R) reproduces the same measures for cross-checking on
a machine that does have bibliometrix installed.

THE CALLON MEASURES, IN PLAIN LANGUAGE
--------------------------------------
Build a network in which each node is a keyword and each edge joins two
keywords that appear together on the same document. Partition it into
communities ("themes"). Then for each theme:

  * The EQUIVALENCE INDEX between two keywords i and j is

            e_ij = c_ij^2 / (c_i * c_j)

    where c_ij is how often they co-occur and c_i, c_j how often each occurs
    alone. Squaring the numerator and dividing by the product normalises away
    sheer frequency, so a rare pair that always appears together scores high.

  * DENSITY = 100 x (mean e_ij among keywords INSIDE the theme).
    How tightly the theme coheres internally — its degree of development.

  * CENTRALITY = 10 x (sum of e_ij between the theme and everything OUTSIDE).
    How strongly the theme connects to the rest of the field — its importance
    to the discipline's overall structure.

The thematic map plots centrality (x) against density (y) and reads the four
quadrants:

    high centrality, high density  = MOTOR themes    (central and developed)
    low  centrality, high density  = NICHE themes    (developed but isolated)
    low  centrality, low  density  = EMERGING/DECLINING
    high centrality, low  density  = BASIC/TRANSVERSAL

§6.6 operationalises Chapter 5's "structurally marginal" as low centrality.
That is a CHOICE, and the chapter defends it as one.
"""
import json, os, re, itertools
from collections import Counter, defaultdict

import networkx as nx
import wos_parser as W

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis_outputs")
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

print("Loading corpora ...")
C = {n: W.load_corpus(f"{BASE}/{n}", verbose=False) for n in ["TS-J", "AS-J", "AS-T"]}
R = {}


# ---------------------------------------------------------------------------
# Keyword extraction. DE = author keywords, ID = Keywords Plus (WoS-generated).
# Both are used, as bibliometrix's field="ID" convention does, but they are
# also reported separately so the reader can see how much of the structure is
# the authors' vocabulary and how much is the database's.
# ---------------------------------------------------------------------------
STOP = {"", "article", "articles", "research", "study", "studies", "analysis",
        "paper", "approach", "case study", "review"}


def keywords_of(rec, use=("DE", "ID")):
    """Keywords, split on the semicolon delimiter WoS actually uses.

    (D14) DE and ID are stored as joined text, because Web of Science wraps
    them mid-keyword; splitting on line breaks fragmented multi-word keywords
    such as 'adaptation studies'."""
    ks = []
    for f in use:
        for entry in W.kw_list(rec, f):
            for k in re.split(r"[;]", entry):
                k = re.sub(r"\s+", " ", k.strip().lower())
                k = k.strip(" .,")
                if k and k not in STOP and len(k) > 2:
                    ks.append(k)
    return sorted(set(ks))


def build_network(recs, use=("DE", "ID"), top_n=250, min_freq=5):
    docs = [keywords_of(r, use) for r in recs]
    docs = [d for d in docs if len(d) >= 2]
    freq = Counter(k for d in docs for k in d)
    vocab = {k for k, n in freq.most_common(top_n) if n >= min_freq}
    co = Counter()
    for d in docs:
        ks = [k for k in d if k in vocab]
        for a, b in itertools.combinations(sorted(ks), 2):
            co[(a, b)] += 1
    G = nx.Graph()
    for k in vocab:
        G.add_node(k, freq=freq[k])
    for (a, b), c in co.items():
        if c >= 2:                       # drop single co-occurrences (noise)
            e = (c * c) / (freq[a] * freq[b])      # Callon equivalence index
            G.add_edge(a, b, cooc=c, equiv=e)
    return G, freq, len(docs)


def thematic_map(G, freq, resolution=1.0, seed=20260806):
    """Louvain communities + Callon centrality/density per community."""
    if G.number_of_edges() == 0:
        return []
    comms = nx.community.louvain_communities(
        G, weight="equiv", resolution=resolution, seed=seed)
    themes = []
    for cid, nodes in enumerate(comms):
        nodes = set(nodes)
        if len(nodes) < 2:
            continue
        internal, external = [], []
        for u, v, d in G.edges(data=True):
            iu, iv = u in nodes, v in nodes
            if iu and iv:
                internal.append(d["equiv"])
            elif iu or iv:
                external.append(d["equiv"])
        density = 100 * (sum(internal) / len(nodes)) if nodes else 0
        centrality = 10 * sum(external)
        label_nodes = sorted(nodes, key=lambda k: -freq[k])[:4]
        themes.append({
            "cluster": cid,
            "label": ", ".join(label_nodes[:3]),
            "keywords": sorted(nodes, key=lambda k: -freq[k]),
            "size": len(nodes),
            "documents_weight": int(sum(freq[k] for k in nodes)),
            "centrality": round(centrality, 3),
            "density": round(density, 3),
        })
    # Quadrants relative to the MEDIAN of each axis (bibliometrix's convention)
    if themes:
        cs = sorted(t["centrality"] for t in themes)
        ds = sorted(t["density"] for t in themes)
        cmed = cs[len(cs) // 2]
        dmed = ds[len(ds) // 2]
        for t in themes:
            hi_c, hi_d = t["centrality"] >= cmed, t["density"] >= dmed
            t["quadrant"] = ("Motor" if hi_c and hi_d else
                             "Niche" if not hi_c and hi_d else
                             "Basic/Transversal" if hi_c and not hi_d else
                             "Emerging/Declining")
        for t in themes:
            t["median_centrality"] = round(cmed, 3)
            t["median_density"] = round(dmed, 3)
    return sorted(themes, key=lambda t: -t["documents_weight"])


# ===========================================================================
print()
print("=" * 78)
print("§6.6 / §6.7 — Keyword networks and thematic maps")
print("=" * 78)

for corpus in ["TS-J", "AS-J"]:
    G, freq, ndocs = build_network(C[corpus])
    print(f"\n{corpus}: {ndocs:,} documents with >=2 keywords; "
          f"network {G.number_of_nodes()} nodes / {G.number_of_edges()} edges")
    themes = thematic_map(G, freq)
    print(f"  {len(themes)} themes detected (Louvain, seed 20260806)")
    print(f"  {'quadrant':20s} {'centr':>8s} {'dens':>8s}  label")
    for t in themes:
        print(f"  {t['quadrant']:20s} {t['centrality']:8.2f} {t['density']:8.2f}  {t['label']}")

    # Where do the terms of interest sit?
    watch = ["translation", "adaptation", "equivalence", "interpreting",
             "intersemiotic translation", "multimodality", "audiovisual translation",
             "corpus", "fidelity", "film adaptation", "intermediality"]
    placement = {}
    for w in watch:
        for t in themes:
            if w in t["keywords"]:
                placement[w] = {"quadrant": t["quadrant"], "theme": t["label"],
                                "frequency": freq[w],
                                "degree_centrality": round(nx.degree_centrality(G).get(w, 0), 4),
                                "betweenness": round(nx.betweenness_centrality(
                                    G, weight=None).get(w, 0), 4)}
    print("  Placement of watched terms:")
    for k, v in placement.items():
        print(f"      {k:28s} -> {v['quadrant']:20s} (freq {v['frequency']}, "
              f"deg {v['degree_centrality']}, betw {v['betweenness']})")

    # Top keywords by frequency and by betweenness — the hub test of §6.7
    dc = nx.degree_centrality(G)
    bc = nx.betweenness_centrality(G)
    top_freq = sorted(freq.items(), key=lambda x: -x[1])[:20]
    top_bet = sorted(((k, bc.get(k, 0)) for k in G.nodes()), key=lambda x: -x[1])[:15]
    print(f"  Top keywords by frequency: "
          f"{', '.join(k for k, _ in top_freq[:8])}")
    print(f"  Top keywords by betweenness: {', '.join(k for k, _ in top_bet[:8])}")

    R[corpus] = {
        "network": {"nodes": G.number_of_nodes(), "edges": G.number_of_edges(),
                    "documents_with_keywords": ndocs},
        "themes": themes,
        "watched_term_placement": placement,
        "top_keywords_by_frequency": [{"keyword": k, "n": n} for k, n in top_freq],
        "top_keywords_by_betweenness": [{"keyword": k, "betweenness": round(v, 4)}
                                        for k, v in top_bet],
        "degree_centrality_top": sorted(
            ({"keyword": k, "degree_centrality": round(v, 4)} for k, v in dc.items()),
            key=lambda d: -d["degree_centrality"])[:20],
    }

with open(os.path.join(OUT, "NETWORK_RESULTS.json"), "w") as f:
    json.dump(R, f, indent=2, ensure_ascii=False)
print("\nWritten: out/NETWORK_RESULTS.json")

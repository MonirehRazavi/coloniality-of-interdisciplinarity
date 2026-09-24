"""
analysis_three_corpora.py — one run, three corpora, identical parameters
=========================================================================
Produces the thematic map data for TS-J, AS-J and AS-T in a single pass so
that a three-panel comparison rests on one execution of one procedure rather
than on three runs stitched together.

Parameters are those of the original analysis_networks.py, unchanged:
    DE + Keywords Plus; top 250 keywords with frequency >= 5; edges at
    co-occurrence >= 2 weighted by the Callon equivalence index; Louvain,
    weight="equiv", resolution 1.0, seed 20260806; density = 100 * mean
    internal equivalence per keyword; centrality = 10 * summed boundary
    equivalence; quadrants by median split.
"""
import json, os, re, itertools, sys
from collections import Counter

import networkx as nx
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wos_parser as W

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis_outputs")
os.makedirs(OUT, exist_ok=True)

STOP = {"", "article", "articles", "research", "study", "studies", "analysis",
        "paper", "approach", "case study", "review"}


def keywords_of(rec, use=("DE", "ID")):
    ks = []
    for f in use:
        for entry in W.kw_list(rec, f):
            for k in re.split(r"[;]", entry):
                k = re.sub(r"\s+", " ", k.strip().lower()).strip(" .,")
                if k and k not in STOP and len(k) > 2:
                    ks.append(k)
    return sorted(set(ks))


def build_network(recs, top_n=250, min_freq=5):
    docs = [keywords_of(r) for r in recs]
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
        if c >= 2:
            G.add_edge(a, b, cooc=c, equiv=(c * c) / (freq[a] * freq[b]))
    return G, freq, len(docs)


def thematic_map(G, freq, resolution=1.0, seed=20260806):
    comms = nx.community.louvain_communities(G, weight="equiv",
                                             resolution=resolution, seed=seed)
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
        themes.append({
            "label": ", ".join(sorted(nodes, key=lambda k: -freq[k])[:3]),
            "keywords": sorted(nodes, key=lambda k: -freq[k]),
            "size": len(nodes),
            "documents_weight": int(sum(freq[k] for k in nodes)),
            "centrality": round(10 * sum(external), 3),
            "density": round(100 * (sum(internal) / len(nodes)), 3),
        })
    cs = sorted(t["centrality"] for t in themes)
    ds = sorted(t["density"] for t in themes)
    cmed, dmed = cs[len(cs) // 2], ds[len(ds) // 2]
    for t in themes:
        hi_c, hi_d = t["centrality"] >= cmed, t["density"] >= dmed
        t["quadrant"] = ("Motor" if hi_c and hi_d else
                         "Niche" if not hi_c and hi_d else
                         "Basic/Transversal" if hi_c and not hi_d else
                         "Emerging/Declining")
        t["median_centrality"], t["median_density"] = round(cmed, 3), round(dmed, 3)
    return sorted(themes, key=lambda t: -t["documents_weight"])


R = {}
for corpus in ["TS-J", "AS-J", "AS-T"]:
    recs = W.load_corpus(f"{BASE}/{corpus}", verbose=False)
    G, freq, ndocs = build_network(recs)
    themes = thematic_map(G, freq)
    de = sum(1 for r in recs if keywords_of(r, ("DE",)))
    idp = sum(1 for r in recs if keywords_of(r, ("ID",)))
    print(f"\n{'='*76}\n{corpus}: {len(recs):,} records, {ndocs:,} usable "
          f"({ndocs/len(recs):.1%}); {G.number_of_nodes()} nodes / "
          f"{G.number_of_edges()} edges; {len(themes)} themes")
    print(f"  DE {de:,} ({de/len(recs):.1%})   ID {idp:,} ({idp/len(recs):.1%})")
    for t in themes:
        print(f"  {t['quadrant']:19s} c={t['centrality']:7.2f} d={t['density']:6.2f} "
              f"w={t['documents_weight']:6d} n={t['size']:3d}  {t['label']}")
    R[corpus] = {"records": len(recs),
                 "network": {"nodes": G.number_of_nodes(),
                             "edges": G.number_of_edges(),
                             "documents_with_keywords": ndocs,
                             "records_with_author_keywords": de,
                             "records_with_keywords_plus": idp},
                 "themes": themes}

json.dump(R, open(os.path.join(OUT, "THREE_CORPORA_THEMES.json"), "w"),
          indent=2, ensure_ascii=False)
print(f"\nWritten {OUT}/THREE_CORPORA_THEMES.json")

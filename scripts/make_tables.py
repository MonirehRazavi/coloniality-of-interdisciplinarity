"""make_tables.py — exports every data-derived table in the thesis as a
CSV, from the frozen JSON outputs in ../analysis_outputs/, so that each
table's numbers can be checked against the deposited pipeline without
re-running anything.

Coverage (thesis numbering of 22 September 2026, D18):
    Table 6.1  Jakobson and Bluestone across all three corpora
    Table 6.2  Peak engagement with "fidelity" per field (+ full series)
    Table 6.4  Citation between the two literatures, journal to journal
    Table 6.5  Frontier vs core within TS's citation record
    Table A.2  The three corpora as frozen (restated from the audit)
    Table S.1  The themes of TS-J with Callon quadrants (Figure 6.5 data)
    Table S.2  Term presence of "adaptation" in TS-J (the counts behind
               Table 6.3 and §6.7; the eleven records themselves are
               listed in Table 6.3 from the parsed corpus)

Not exported here, because they are not products of this pipeline:
    Table 1.1  Four defensible definitions of "adaptation research" —
               Web of Science interface counts, recorded in Appendix A
               (Table A.1, queries Q-01–Q-10) with dates.
    Table 6.6  Comparative historiographical profiles — a conceptual
               table; its measured row restates the baselines in
               ALL_RESULTS.json (6.5_ledger) and Table 6.4.
    Tables A.1/A.3 — authored directly in Appendix A.
"""

import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
AO = os.path.join(HERE, "..", "analysis_outputs")
OUT = os.path.join(HERE, "..", "tables_out")
os.makedirs(OUT, exist_ok=True)


def load(name):
    return json.load(open(os.path.join(AO, name)))


def write(name, header, rows):
    path = os.path.join(OUT, name)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", path)


ALL = load("ALL_RESULTS.json")
REF = load("REFINED_RESULTS.json")
NET = load("NETWORK_RESULTS.json")

# Table S.1 — themes of TS-J (thematic-map quadrants; data behind Figure 6.5)
themes = NET["TS-J"]["themes"]
rows = []
for t in themes:
    if isinstance(t, dict):
        rows.append([t.get("label") or t.get("name"),
                     t.get("centrality"), t.get("density"),
                     t.get("quadrant", ""),
                     "; ".join(t.get("keywords", [])[:8])])
write("table_S1_ts_themes.csv",
      ["theme", "callon_centrality", "density", "quadrant", "top_keywords"],
      rows)

# Table 6.5 — frontier vs core
fc = load("08_frontier_vs_core.json")
rows = [[k, json.dumps(v) if isinstance(v, (dict, list)) else v]
        for k, v in fc.items()]
write("table_6_5_frontier_vs_core.csv", ["measure", "value"], rows)

# Table 6.1 — the two founders across the corpora, from
# 13_founders_across_corpora.json (written by analysis_cross_corpus.py,
# step 11).  Per 10,000 is per 10,000 parsed references.
fd = load("13_founders_across_corpora.json")
rows = []
for corpus, block in fd.items():
    for author in ("Jakobson, Roman", "Bluestone, George", "Hutcheon, Linda"):
        v = block[author]
        rows.append([corpus, author, v["references"], v["citing_documents"],
                     v["pct_of_corpus"], v["per_10k_parsed_references"]])
write("table_6_1_founders_across_corpora.csv",
      ["corpus", "author", "references", "citing_documents", "pct_of_corpus",
       "per_10k_parsed_references"], rows)

# Table 6.2 — fidelity engagement per field: full yearly series + peaks
clocks = REF["R2_clocks"]
rows = []
for series, data in clocks.items():
    if "fidelity" not in series or not isinstance(data, dict):
        continue
    for year, v in sorted(data.get("series", {}).items()):
        rows.append([series, year, v["documents"], v["with_term"],
                     v["rate_pct"]])
    rows.append([series + " — PEAK", data.get("peak_year_of_rate"),
                 "", "", data.get("peak_rate_pct")])
rows.append(["fidelity lag (years, AS peak minus TS peak)",
             REF["R2_fidelity_lag_years"], "", "", ""])
write("table_6_2_fidelity_clocks.csv",
      ["series", "year", "documents", "with_term", "rate_pct"], rows)

# Table S.2 — term presence of "adaptation" in TS-J (counts behind Table 6.3)
tp = ALL["6.4a_term_presence"]
write("table_S2_term_presence_tsj.csv", ["measure", "value"],
      [[k, v] for k, v in tp.items()])

# Table 6.4 — journal-to-journal directional ledger
ledger = ALL["6.5_ledger"]
rows = []
for direction, block in ledger.items():
    if not isinstance(block, dict):
        continue
    rows.append([direction, "TOTAL", block.get("references"),
                 block.get("per_10k_parsed_references"),
                 block.get("citing_documents")])
    for j, n in (block.get("by_journal") or {}).items():
        rows.append([direction, j, n, "", ""])
write("table_6_4_directional_ledger.csv",
      ["direction", "journal", "references", "per_10k", "citing_documents"],
      rows)

# Table A.2 — corpora as frozen (from the audit output)
audit = load("00_audit.json")
rows = [[k, json.dumps(v) if isinstance(v, (dict, list)) else v]
        for k, v in audit.items()]
write("table_A2_corpora_audit.csv", ["measure", "value"], rows)

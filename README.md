# Supplementary Electronic Files: The Bibliometric Analyses

**Thesis:** *Weighed and Found Wanting: A Close and Distant Reading of the Coloniality of Interdisciplinarity: The Case of Translation Studies and Adaptation Studies* — Monireh Sadat Razavi Ganji (Moni Zavi), PhD dissertation, School of Translation and Interpretation, University of Ottawa, 2026. Supervisor: Salah Basalamah.

**Repository:** https://github.com/MonirehRazavi/coloniality-of-interdisciplinarity — release `v1.0-as-submitted` is the version deposited with the thesis (Appendix A.4 and Appendix B). Later commits, if any, are listed in the release notes and do not alter the deposited outputs.

**Version:** 22 September 2026 (the pre-submission rerun; supersedes the 24 August package).

**What this is.** The complete methodological record behind the thesis's bibliometric analyses (Chapter Six, with the counts used in §1.3.2 and Appendix A): the fifteen analysis and figure scripts, the analysis outputs every table and figure was drawn from, the figures and tables as drawn, the logs of the run that produced them, and the two working logs (the decision log D1–D20 and the process log) that Appendix A condenses.

**How it was checked.** On 22 September 2026 the whole pipeline was re-executed from the 73 raw Web of Science export files in a clean environment and compared with the outputs the thesis was written from: 19 of 21 analysis files byte-identical (the two exceptions are the community-detection partitions, see below), all 7 table exports identical, 14 of the 22 thesis figures pixel-identical, 5 identical in their values, and 3 redrawn from a corrected script. The record of that check is in `logs/` and in decision-log entries D17–D20.

---

## Contents

```
Supplementary_files/
├── README.md                     (this file)
├── requirements.txt              Python packages, with the versions used on 22 Sep 2026
├── run_all.py                    Runs everything below in order, logs each script,
│                                 compares every output with the deposited copy
├── run_all.ipynb                 The same, one script per notebook cell
├── scripts/
│   ├── wos_parser.py             Reads WoS plain-text exports; parses cited references;
│   │                             author normalisation (Appendix A.4 listing)
│   ├── canon.py                  Canon, benchmark, frontier and core author lists
│   │                             (Appendix A.2) with their database matching forms
│   ├── analysis_cross_corpus.py  Audit, term presence, canon matching, directional
│   │                             ledger, baselines, citation kind, noise sample,
│   │                             frontier/core, clocks, RPYS, founders (§§6.3, 6.5–6.9)
│   ├── analysis_refined.py       Token-level markedness, rate-normalised clocks,
│   │                             windowed RPYS (§§6.5, 6.6, 6.11)
│   ├── analysis_networks.py      Keyword co-occurrence network of TS-J and AS-J,
│   │                             Louvain themes, Callon centrality/density (§6.4)
│   ├── analysis_three_corpora.py The same procedure run once over TS-J, AS-J and AS-T
│   │                             (the data behind Figures 6.4–6.6)
│   ├── make_figures_palette.py   Figures 6.1, 6.7–6.13, 6.15 (Tinos 12 pt, 6.5 in)
│   ├── make_fig_a1_rpys.py       Figure A.1
│   ├── make_labelled_maps.py     Figures 6.4, 6.5, 6.6 (labelled thematic maps)
│   ├── make_three_maps.py        Three-panel variant of the maps (not used in the thesis)
│   ├── make_chapter_figures.py   Figures 1.1, 1.2, 5.1, 6.2, 6.3, 6.14, 6.16, 6.17
│   ├── make_fig_a2_flow.py       Figure A.2 (corpus-construction flow)
│   ├── make_tables.py            Tables 6.1, 6.2, 6.4, 6.5, A.2 and two supplementary
│   │                             tables, as CSV, from analysis_outputs/ alone
│   ├── make_figures.py           The first figure set (August 2026), superseded; kept
│   │                             because Appendix B reproduces it
│   └── make_descriptive_figures.py  Descriptive figures, superseded; kept for the same reason
├── analysis_outputs/
│   ├── 00_audit.json … 13_founders_across_corpora.json
│   │                             Step-by-step outputs of analysis_cross_corpus.py
│   ├── ALL_RESULTS.json          Consolidated cross-corpus results
│   ├── REFINED_RESULTS.json      Markedness, clocks, RPYS
│   ├── NETWORK_RESULTS.json      TS-J and AS-J networks and thematic maps (deposited partition)
│   ├── THREE_CORPORA_THEMES.json TS-J, AS-J, AS-T maps in one pass (deposited partition)
│   ├── *_rerun_networkx3.6.1.json  The partitions the 22 Sep rerun produced (see below)
│   ├── networkx_version_test.json  What is and is not invariant across eight networkx versions
│   └── t64_*.csv, t66_*.csv      Table-ready exports (the file names keep the August numbering)
├── figures_as_in_thesis/         One PNG per thesis figure, named Figure_6_1.png etc.,
│                                 with MANIFEST.md stating for each whether it is the
│                                 thesis image, the same values re-typeset, or a replacement
├── figs_out/                     The figures exactly as the scripts write them
│   ├── palette/  thematic_maps/  original_set/  descriptive/
├── tables_out/                   The table CSVs as exported by make_tables.py
└── logs/
    ├── 01_… 13_….log             Printed output of every script, 22 Sep 2026 run
    ├── run_all_22Sep2026.log     The whole run, including the comparison
    ├── Ch6_decision_log.md       D1–D20: every methodological choice and every error found
    ├── Ch6_process_log.md        What each script does, in plain language
    └── VERIFICATION_REPORT_22Sep2026.md   What was checked, what held, what changed
```

## How to reproduce

Requirements: Python 3.11 or later and the packages in `requirements.txt` (`pip install -r requirements.txt`): matplotlib, networkx, squarify, numpy and Pillow. The figures use the Tinos face (the metric equivalent of Times New Roman; `fonts-croscore` on Debian/Ubuntu, or any Times) and fall back to the system serif if it is absent.

1. Place the raw Web of Science export files (see *Data availability*) in `data/TS-J/`, `data/AS-J/` and `data/AS-T/`, one subfolder per corpus, exactly as exported (`savedrecs*.txt`).
2. Run `python3 run_all.py` from this folder. It runs the thirteen scripts in order (the four analysis scripts, then the figure and table scripts), prints and logs each one, and finishes with an IDENTICAL / DIFFERS line for every file in `analysis_outputs/` against the deposited copy (which it first preserves as `analysis_outputs_frozen/`). The full run takes about ninety seconds.
3. `python3 run_all.py --figures` redraws, without the raw data, every figure and table that derives from the deposited outputs alone (Figures 1.1, 1.2, 5.1, 6.2, 6.4–6.6, 6.14, 6.17, A.1, A.2 and all tables); Figures 6.1, 6.3, 6.16 and the superseded descriptive set read the exports and are skipped.

Each script can also be run on its own, from inside `scripts/`, in the order listed in `run_all.py`. Every number in the thesis's bibliometric tables and figures derives from the files in `analysis_outputs/`, which are included so the chapter can be checked without re-running anything.

## Reproducibility of the thematic maps (please read before comparing partitions)

The keyword networks reproduce exactly. The Louvain community detection on top of them does **not** reproduce across versions of `networkx`: versions 3.1 through 3.6.1 each return a slightly different partition at the same seed (20260806), and none reproduces the deposited partition exactly (decision log, D19; `analysis_outputs/networkx_version_test.json`). `run_all.py` therefore keeps the fresh partition beside the deposited one (`*_rerun_networkx<version>.json`) and draws the maps from the deposited partition, which is the one the thesis describes. What the thesis claims about the maps is what holds in every version tested: in TS-J *adaptation* falls in the lowest-density cluster with *literary translation*, *retranslation*, *equivalence*, *intersemiotic translation* and *rewriting*; the AS-J partition is identical in every version; in AS-T the adaptation theme is the largest and among the least dense. The quadrant labels are indicative only (Appendix A.8).

## Data availability

The raw Web of Science exports (73 plain-text files; 35,587 records; 126 MB) are **not** included, because redistribution of Web of Science records is restricted by Clarivate's subscriber licence. The corpora are reconstructible from the query log in Appendix A (Table A.1, queries Q-08, Q-09 and Q-10), and the frozen export files are available from the author on request for verification. The database itself moves: identical queries re-run later return slightly different counts (the drift is measured in the Table A.1 note), which is why every count in the thesis carries its export date.

## Section numbers in the scripts

The analyses were first written up as a stand-alone chapter numbered §§6.3–6.9 (August 2026), then distributed across Chapters 1–5 (24 August), then gathered again into Chapter Six in its present form (13 September). Comments inside the older scripts refer to the August numbering; the mapping to the present thesis is: old §6.4 (term presence, canon matching, benchmarks) → §6.7 and §6.8; old §6.5 (ledger, baselines, citation kind) → §6.7 and §6.11; old §6.6 (networks) → §6.4; old §6.7 (markedness) → §6.11; old §6.8 (clocks) → §6.5; old §6.9 (RPYS) → §6.6; old §6.3.4 (noise) → §6.2 and Appendix A.1. The file names `t64_*` and `t66_*` keep their August prefixes; they are the same data.

## Licence

Code (`scripts/`, `run_all.py`, `run_all.ipynb`): MIT (`LICENSE`). Outputs, figures, tables and logs: CC BY 4.0 (`LICENSE-OUTPUTS.md`). Please cite the thesis and this repository (`CITATION.cff`).

## Contact

Moni Zavi — monirazav@gmail.com

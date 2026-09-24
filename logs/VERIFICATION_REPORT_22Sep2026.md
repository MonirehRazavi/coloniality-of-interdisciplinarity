# Pre-submission Rerun of the Bibliometric Pipeline

## Verification Report and Paste-Ready Edits, 22 September 2026

Moni Zavi, PhD dissertation. Prepared against *September 22.docx* (Working Drafts/Final drafts different versions) and the supplementary package *Restructure/Supplementary_files*.

## 1. What was done

Every script of the bibliometric pipeline was re-executed from the 73 raw Web of Science export files (TS-J 29 files, AS-J 6, AS-T 38; 126 MB; 35,587 records) in a clean environment: Python 3.11.15, matplotlib 3.10.9, networkx 3.6.1, seed 20260806. The scripts were run one at a time, in the order the README prescribes, and every output was compared mechanically with the outputs the thesis was written from: JSON and CSV files byte for byte; figures pixel for pixel against the images embedded in *September 22.docx* (after allowing for Word's 220-dpi recompression of embedded images); every number in Chapter Six and Appendix A read out of the document and checked against the outputs. The printed output of every script is in the deposited `logs/` folder; the whole run is repeatable with `run_all.py` (about ninety seconds) or, cell by cell, with `run_all.ipynb`.

## 2. What held

**Corpora.** All three corpora load to the frozen counts (14,258 / 2,763 / 18,566); parse rates 95.4% / 90.1% / 95.1%.

**Analysis outputs.** Nineteen of the twenty-one analysis files are byte-for-byte identical to the deposited versions: all fourteen step files of `analysis_cross_corpus.py`, `ALL_RESULTS.json`, `REFINED_RESULTS.json`, and the four table exports. The two exceptions are the Louvain partitions (section 4).

**Tables.** Every table export reproduces. Tables 6.1, 6.2, 6.4, 6.5, 6.6 (measured row), A.1, A.2 and A.3 in the thesis were read back and match the outputs. Table 6.1 was re-derived independently from the parsed references: Jakobson 438/414/2.90%/13.75 (TS-J), 18/17/0.62%/4.08 (AS-J), 170/148/0.80%/2.71 (AS-T); Bluestone 1/1/0.01%/0.03 and 175/175/0.94%/2.79.

**Figures.** Of the 22 figures in the thesis, 14 are pixel-identical to what the scripts draw today: 6.1, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10, 6.11, 6.12, 6.13, 6.15, A.1 and A.2. Five more (1.1, 1.2, 5.1, 6.2, 6.17) carry exactly the same values in a slightly different typesetting; nothing needs to change in them. Three were redrawn (section 3).

**Numbers in the text.** The following claims in Chapter Six were each recomputed and confirmed: 25.5 vs 18.5 references per article and the 38% distortion; the 11 records naming "adaptation studies" (0.08%); 210 references / 134 documents / 0.94% / 6.6 per 10,000 for the AS canon in TS-J, a third of it Hutcheon, 107 once Hutcheon and Cattrysse are removed; 145 / 68 / 2.46% / 32.9 for the TS canon in AS-J, with Venuti 29, Jakobson 18, Lefevere 15 (43%); the 13.3 : 1 journal-level asymmetry and the 10 : 1 for AS-T; the author-level 5 : 1; the baselines 491 and 430; "seventy-four visits" and "one in thirteen"; the core-to-frontier ratio 4.0 : 1 and every author count in Table 6.5; Bassnett's 818; the fidelity peaks 2008 (1.92%) and 2021 (8.28%), the thirteen-year lag and the fourfold intensity; the foundational years 1959, 1972, 1957, 1984; 107 shared authors of 10,975 and 5.4%; 18 of 300 shared venues (6%); the ratios of a tenth, a seventh and twice against the benchmark canons; 86% / 10% / 73% / 5% for the network hubs and "nearly half" of the shortest paths (0.45); 842 AS-T records (4.5%) in the three AS journals; 3,599 periodicals; every research-area count in Figure 6.17 and the 2,411 of area and Asian studies; "four times the rate" for linguistics; Jakobson at a fifth of his TS intensity and at parity with Bluestone; the ninetyfold Bluestone asymmetry and "an eighth of Hutcheon's rate".

## 3. What did not hold, and what changed

### 3.1 Figures 6.3 and 6.16 (decision log, D17)

These two figures were first drawn on 11 August by a script (`figs_45.py`) that was never saved. The deposited re-implementation (`make_chapter_figures.py`, 24 August) had never been run against them. Run today, it produced different numbers, and inspection found two errors in it: the term sets of Figure 6.3 were matched without word boundaries (*race* matched *trace*, *gender* matched *engendered*), and the private parser inside the script counted only the last country of a multi-address record and treated pre-1990 American addresses (state and ZIP code without "USA") as states. The Global South share in §6.9 had been computed from a country list that was never written down.

You chose to repair the deposited script and let the thesis report what it produces. The script now matches whole words, reads the corpus through the package parser like every other script, resolves both American address forms, and declares the Global South grouping (UNCTAD's developing economies). The corrected figures are `Figure_6_3.png` and `Figure_6_16.png` in the deposited `figures_as_in_thesis/` folder; paste them over the current images. The values change as follows.

| Series (Figure 6.3, five-year rolling share of AS-J records) | In the thesis now | Corrected |
|---|---|---|
| Fidelity, 1995 → peak → 2023 | 0.4% → 7.8% (2019) → 6.2% | 0.9% → 7.0% (2021) → 6.4% |
| Intertextuality, 1995 → 2023 | 0.4% → 18.8% | 0.0% → 14.6% (still its maximum) |
| Cultural politics, 1995 → peak → 2023 | 3.2% → 26.1% (2022) → 25.9% | 3.6% → 26.0% (2022) → 25.1% |
| Digital and transmedia, 2023 | 22.3% (peak 24.0%) | 21.3% (its maximum) |

| Figure 6.16, share of records carrying an affiliation | In the thesis now | Corrected |
|---|---|---|
| TS-J: Spain / UK / China / Brazil / USA | 16 / 15 / 12 / 8 / 7 | 16 / 15 / 12 / 8 / 8 |
| AS-J: USA / UK | 42 / 22 | 47 / 22 |
| AS-T: USA / UK | 21 / 12 | 22 / 12 |
| Global South share, TS-J / AS-J / AS-T | 24.5 / 7.3 / 18.3 | 30.0 / 8.7 / 23.3 |
| Brazil, TS-J / AS-J / AS-T records | 949 / none (text) or 5 (text) / 459 | 949 / 5 / 457 |

No conclusion changes; the direction of every finding is the same, and the American concentration of AS-J is stronger than the thesis currently says. Two phrases are withdrawn: "fifteen times its share three decades earlier" (the corrected rise is about sevenfold, and the 1995 base was one record in 220) and "contributes none to the adaptation journal corpus" (Brazil contributes five, as §6.9 itself says two paragraphs later).

### 3.2 Figure 6.14 (D18)

The box in the current image quotes 29.6 per 10,000, the rate per raw reference; Figure 6.2, Table 6.4 and Table 6.6 use 32.9, the rate per parsed reference. The figure was redrawn from the outputs with 32.9. Paste `Figure_6_14.png` over the current image; no text changes.

### 3.3 Table 6.1 (D18)

Correct as printed, but it had been typed by hand; it is now derived from a new output file (`13_founders_across_corpora.json`) and exported by `make_tables.py`. No change to the thesis.

## 4. The thematic maps (D19)

The keyword networks reproduce exactly. The Louvain community detection does not reproduce across releases of networkx (3.1–3.6.1 all tested): the partitions differ at the margins and none reproduces the deposited partition keyword for keyword. Everything §6.4 says about the TS-J and AS-J maps holds in every release. Two statements about the AS-T map do not: "peripheral on both axes" holds only in the deposited partition and one release, and "more than twice its nearest rival" in three of nine. You chose to soften that paragraph to what survives every release; the replacement is in section 6. Appendix A.8 now reports the cross-version test. The deposited partition remains the one the figures show; `run_all.py` keeps any fresh partition beside it and draws the maps from the deposited one.

## 5. Other corrections found while reading the chapter against the outputs

**One arithmetic slip.** §6.6: "5.4% of the adaptation community and under 1% of the translation one". The value is 107 of 8,984, which is 1.2%. Replacement in section 6.

**Internal contradiction.** §6.9 says Brazil "contributes none to the adaptation journal corpus" and, in the next paragraph, "Brazil, with 5 of the 2,763 records in the journal core". Five is right. Replacement in section 6.

**Stale cross-references in Chapter Six** (left by the September restructuring; each is one number to change):

| Paragraph begins | Reads | Should read |
|---|---|---|
| "One objection should be met…" (§6.3) | "Figure 6.6 places the two canons side by side" | Figure 6.2 |
| "Two things follow that the citation record reaches…" (§6.4) | "the 2021 peak in §6.8" | §6.5 |
| "The keyword measure in Figure 6.7…" (§6.4) | "reported in §6.12" | §6.11 |
| "There is a way of asking a field…" (§6.6) | "Figure 6.8 plots both spectra" | Figure 6.9 |
| "Neither field's founding moment…" (§6.6) | "at parity with its own founder (§6.5)" | (§6.3) |
| "The composition is as informative…" (§6.7) | "the temporal othering of §6.6" | §6.5 |
| "Measured by the geography of its journals…" (§6.9) | "the third series in Figure 6.15" | Figure 6.16 |
| "The parent disciplines were different…" (§6.10) | "the citation record of §6.7 shows why" | §6.6 |

**Stale cross-references in Appendix A.** All corrected in the paste-ready Appendix A (references to §§3.2.4, 3.3.2, 4.3, 4.4, 4.5.1, 4.6.1, 4.7, 4.8, 5.5 and Figures 4.3, 4.5, 4.6 now point to Chapter Six; the "[n] records" placeholder in A.1 is filled with 400; "eleven scripts" is now fifteen; Table A.3 is now the journal table and the errors table is Table A.4, because the current document numbers both "A.3").

**Lists of Tables and Figures.** The front matter still lists the pre-restructuring numbering (Tables 3.1–5.1, Figures 1.3–5.7). Word will rebuild both lists from the captions if they are caption-styled; otherwise they need to be retyped to Tables 1.1, 6.1–6.6, A.1–A.4 and Figures 1.1, 1.2, 5.1, 6.1–6.17, A.1, A.2.

**§7.9.** The heading is empty; §6.11 refers to it ("§7.9 records it as the first of the openings").

## 6. Paste-ready replacements

**§6.4, the paragraph beginning "Chapter Three read the Turns as TS's narrative grammar". Replace from "Concerns accumulate and none declines" to the end of the paragraph with:**

Concerns accumulate and none declines. Cultural politics rises from 3.6% of records in 1995 to a peak of 26.0% in 2022 and stands at 25.1% in 2023; intertextuality from nothing in the mid-1990s to 14.6%, still climbing at the end of the series; digital and transmedia concerns from nothing before the mid-2000s to 21.3%, also at their maximum. And fidelity, the debate the field's own historiography most insistently describes as superseded, rises from under 1% of records in 1995 to a peak of 7.0% in 2021 and stands at 6.4% in 2023, some seven times its share three decades earlier and within a point of its highest recorded level. All four streams are at or near their maxima at the same moment.

**§6.4, the paragraph beginning "The third panel in Figure 6.6 is a different kind of object". Replace the second and third sentences (from "When adaptation research is retrieved by topic" to "hold the central positions.") with:**

When adaptation research is retrieved by topic rather than by journal, the field's own theme is by far the largest cluster in the corpus, at 83 keywords, between one and a half and nearly twice its nearest rival depending on the release of the clustering library (Appendix A.8), and it is the thinnest cluster on the map: the least internally developed in every version tested, and, in the partition drawn here, below the median on centrality as well, while climate adaptation and health adjustment hold the central positions.

**§6.6, the paragraph beginning "Neither field's founding moment registers". Replace "5.4% of the adaptation community and under 1% of the translation one" with:**

5.4% of the adaptation community and 1.2% of the translation one

**§6.9, the first paragraph. Replace from "Its largest producer is Spain" to the end of the paragraph with:**

Its largest producer is Spain, with 16% of records carrying an affiliation, followed by the United Kingdom (15%), China (12%), and Brazil and the United States (8% each). AS is the concentrated one: the United States alone accounts for 47% of its journal records and the United Kingdom for a further 22%, so that two countries supply more than two-thirds of the field's output. By the share of records carrying at least one Global South affiliation, on the grouping stated in Appendix A.9, TS stands at 30% and AS at under 9%. Brazil, which contributes 949 records to the translation corpus, contributes five to the adaptation journal corpus (Figure 6.16).

**§6.9, the second paragraph. Replace "the United States share falls from 42% to 21%, the United Kingdom's from 22% to 12%, and the Global South share rises from 7.3% to 18.3%. Brazil, with 5 of the 2,763 records in the journal core, supplies 459 records of the dispersed literature." with:**

the United States share falls from 47% to 22%, the United Kingdom's from 22% to 12%, and the Global South share rises from under 9% to 23%. Brazil, with 5 of the 2,763 records in the journal core, supplies 457 records of the dispersed literature.

**§6.9, the same paragraph, one sentence later:** "the third series in Figure 6.15" → "the third series in Figure 6.16".

**§7.5 or §7.6, if the chapter mentions the number of errors found:** the count is now seven (five in the analysis, two in the pre-submission rerun), and one of the two new ones ran against the argument rather than for it (Appendix A.3).

## 7. What to submit with the thesis

The folder `Supplementary_files_22Sep2026` (13 MB) is the deposit: README, requirements, `run_all.py`, `run_all.ipynb`, the fifteen scripts, the analysis outputs (deposited partitions plus the rerun partitions and the cross-version test), the figures as drawn and as numbered in the thesis with a manifest, the table CSVs, the logs of today's run, the decision log (D1–D20), the process log, and this report. The raw exports stay out of it (licence); keep `Chapter 6/bibliometric_data` as your private frozen copy for verification requests.

Paste-ready documents delivered with this report: *Appendices_A_B_UPDATED_22Sep2026.docx* (replace the current Appendix A and Appendix B entirely), *Ch6_decision_log_22Sep2026.docx* and *Ch6_process_log_22Sep2026.docx* (the logs as Word files, for the reader who will not open Markdown).

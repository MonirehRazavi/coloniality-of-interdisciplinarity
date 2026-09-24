# Chapter 6 — Decision Log

### A running record of methodological choices, for the reflexive sections of the chapter

**Purpose.** Chapter 5 (¶611) criticises the *hubris of the zero point* — knowledge presented as though produced from nowhere, by no one, from no position. Bibliometric findings dropped into the thesis as finished charts would enact exactly that. This log records what was chosen, what was excluded, what the database would not show, and what was decided on grounds of convenience rather than principle. It is the raw material for §6.3 and §6.10.

**Sessions covered:** Session 1 — 29 July 2026 (corpus construction). Session 2 — 6 August 2026 (loading, analysis, and the errors found in it). Session 3 — 22 September 2026 (full re-execution of the pipeline from the raw exports before submission, and the errors found in *that*).

# SESSION 1 — 29 July 2026

Web of Science Core Collection, accessed via University of Ottawa proxy.

## D1. Database: Web of Science Core Collection as primary

**Decision.** WoS Core Collection as the main corpus; OpenAlex to be run separately as a coverage comparison.

**Why.** Three considerations, only two of them intellectual:

1. §1.5.1 already commits the thesis to WoS.
2. WoS cited-reference strings are human-readable and self-contained, which is what makes the citation-matching analysis (§6.4) possible at all. OpenAlex returns references as internal identifiers, requiring an extra resolution step.
3. It is conventional in translation-studies bibliometrics, and therefore citable as precedent.

**What this costs.** WoS is the most selective of the available databases and the weakest on books — and Adaptation Studies is a substantially book-based field. The corpus therefore under-represents AS by construction. This is not a neutral technical limitation: it is the thesis's own argument about the uneven distribution of epistemic visibility, reappearing at the level of the instrument. To be stated in §6.3, not buried in a limitations paragraph.

**Session 2 addendum.** The cost is now measurable. AS-J's cited references parse at 90.1% against TS-J's 95.4% — a 5-point gap that is itself a consequence of book-heavy citation practice, since book references are the ones WoS renders least consistently. The instrument is measurably worse at reading Adaptation Studies than at reading Translation Studies.

## D2. Field delineation: journals for TS, journals + topic for AS

**Decision.** TS is defined by its journals. AS is defined by its journals *plus* a topic search.

**Why the asymmetry.** An initial topic search on "translation studies" OR "translation theory" OR "translatology" returned 6,482 records — but topic-searching finds documents that *name* the discipline, which skews heavily toward self-reflexive and meta-disciplinary writing. An article in *Meta* on subtitling may never use the phrase. Journal-based delineation avoids this.

The same method cannot be applied to AS, because AS has only three dedicated journals against TS's twenty. Defining AS by venue alone would produce a corpus that is small, and dominated by a film-studies journal (*Literature/Film Quarterly*, founded 1973) that predates AS as a self-conscious field.

**What this costs.** The two corpora are not constructed by identical procedures, which weakens strict comparability. This must be declared rather than discovered by the examiner. It is also, in itself, evidence: the reason the procedures cannot match is that the two fields have radically unequal venue infrastructure — which is what Abbott's *ceded practice* settlement (¶671) looks like from the outside.

**Retained for possible secondary use.** The 6,482-record topic corpus is precisely TS's self-reflexive literature — where disciplinary self-narration happens. Potentially interesting against Chapter 4.

## D3. No date limit; no document-type limit at export

**Decision.** Export everything. Filter afterwards, in software.

**Why.** Subsetting after the fact is one line and reversible; re-exporting is an afternoon. It also preserves the option of charting output over time, and of the secondary analysis of book reviews (*which books does TS choose to review?* — directly relevant to ¶673).

**Known confounder, to be stated wherever a growth curve appears.** Journals enter WoS at different dates, and the Emerging Sources Citation Index (launched 2015) admitted large numbers of humanities journals at once. Any apparent surge in either field around 2015–2017 is substantially an artefact of database expansion. Growth figures must therefore be captioned **"indexed output"**, never "growth of the field," and accompanied by a table of first-year-of-coverage per journal.

**Session 2 addendum — this confounder nearly produced a wrong finding.** The §6.8 analysis initially took the *median publication year* of documents engaging *fidelity*, which is a count-based measure and therefore inherits the growth curve directly. It returned a 3-year lag in the wrong direction. Re-normalising to the annual *proportion* of each corpus engaging the term reversed the result to a 13-year lag in the predicted direction (see D10). The confounder is not hypothetical; it changed the sign of a headline finding.

## D4. Subject-area filtering of the Adaptation topic search

**Decision.** Two filterings were built and the second was adopted.

**The 29 July version (superseded).** A phrase-based query (Q-04, 3,376 records) refined by 11 WoS *Categories* → 1,756 records.

**The 4 August version (adopted).** The bare keyword TS=(adaptation) refined by 13 WoS **Research Areas** → **18,566 records**.

**Retained research areas (13):** Area Studies; Art; Arts & Humanities – Other Topics; Asian Studies; Classics; Communication; Cultural Studies; Dance; Film, Radio & Television; Literature; Music; Theater; Women's Studies.

**Excluded after consideration:** Linguistics (6,595 at the time of exclusion) — dominated by loanword and phonological adaptation; Architecture (1,470) — adaptive reuse of buildings, a fascinating conceptual neighbour but a different literature; History (2,796) — societal adaptation predominates.

**Added during review:** Area Studies and Women's Studies, on the parity argument that including Asian Studies while omitting the areas hosting Latin American, African, Middle Eastern and feminist adaptation scholarship would manufacture precisely the kind of absence this chapter studies.

**A precision that matters, added Session 2.** WoS assigns records to *multiple* research areas. The filter retains any record carrying at least one of the thirteen — not only records carrying nothing else. Linguistics (825 records) and History (334) therefore appear *inside* AS-T despite being excluded as retrieval criteria; they arrive attached to records already retrieved under Literature or Communication. Verification: of 18,566 records, 4 carry no research area among the thirteen, and all 4 are line-wrapping artefacts in the export rather than genuine escapees. 12,246 records carry one area, 4,840 carry two, 1,480 carry three or more. An examiner will ask this; the answer is now on record.

**Why this belongs in the chapter, not just the appendix.** The exclusion is not housekeeping. That "adaptation" must be *disambiguated* before it can be studied — while "translation" needs no such operation, its disciplinary sense being unmarked and assumed — is the markedness argument of §5.4 turning up as a practical obstacle in the data.

## D5. Two corrections to earlier claims

Recorded because the reflexive chapter should show error correction, not a clean path.

1. **The *Journal of Adaptation in Film & Performance* IS indexed.** An initial search suggested zero records. This was wrong: WoS drops the ampersand in the abbreviated source field, indexing it as J ADAPT FILM PERFORM. It carries 480 records. The earlier inference — that half of AS's journal apparatus is invisible to WoS — was an artefact of my query string, not a fact about the database.
2. **TTR (*Traduction, terminologie, rédaction*) is confirmed absent from WoS Core Collection.** Verified through the Publication Title Index: a substring search on TRADUCTION returns nine indexed titles, none of them TTR. This is a real absence, not a query error.

## D6. A journal found by accident: FORUM

The TRADUCTION index search also surfaced **FORUM — Revue internationale d'interprétation et de traduction** (408 records), which I had not thought to include. It was added.

**Why this is worth recording rather than quietly fixing.** The seed list was built from journals I could recall, which is to say from journals that are visible from an Anglophone centre. FORUM is Korean-based, bilingual French/English, and was missing for no better reason than that it did not come to mind. The correction was accidental — it fell out of a search run for another purpose entirely.

Whatever else the corpus is, it is the product of one researcher's disciplinary memory, partially corrected by chance. A field's boundaries, when drawn this way, will tend to reproduce the centre of the person drawing them.

**Still unresolved:** there is no principled reason to think FORUM was the only omission. A systematic check against BITRA or the Translation Studies Bibliography journal lists would help, and is **not yet done**.

# SESSION 2 — 6 August 2026

Loading, verification, and analysis. Every decision below was made after the corpora were frozen, so none of them could have been used to select data.

## D7. Analysis software: bibliometrix for loading, Python for the cross-corpus work

**Decision.** The corpora are loaded and audited in R with bibliometrix (Aria & Cuccurullo, 2017), and the descriptive figures come from biblioshiny. Every *inferential* analysis in §§6.4–6.9 is written from scratch in Python 3.11.

**Why, and it is a constraint rather than a preference.** bibliometrix's unit of work is one corpus at a time. The questions this chapter exists to answer — what proportion of TS-J's reference record is AS literature, and how does that compare with the reverse — are cross-corpus by construction, and the package has no function for them. The design document said as much in Part IV ("biblioshiny analyses one corpus at a time. Q1, Q2 and Q6 are inherently two-corpus questions and cannot be done in the GUI").

**What I considered and rejected.** Reporting the Python-computed figures under the bibliometrix name, because bibliometrix is the citable convention and appears in the draft's methods sentence. This was rejected as a false methods statement. An examiner asking to see the bibliometrix output behind Table 6.4 would find there is none. §6.3.1 now states the division of labour explicitly.

**Mitigation.** A verification script (verify_in_bibliometrix.R) reproduces the shared measures in bibliometrix, so the Python figures can be cross-checked on any machine with the package installed. This should be run before submission and the agreement reported.

**Honest note on where the analysis ran.** The Python analysis was executed in a sandboxed environment with no route to CRAN, so bibliometrix could not be installed there and the cross-check has not yet been performed. That is a gap, and it is recorded as one rather than glossed.

## D8. Bassnett is excluded from both the frontier and the core

**Decision.** In the §6.6 frontier-vs-core comparison, Susan Bassnett is reported separately (818 references) and excluded from both aggregates.

**Why.** The design document placed her among the expansionist frontier via *Bassnett & Johnston*. She is also, by any measure, one of the discipline's institutional founders. Her 818 references would place her first in the frontier group, ahead of Tymoczko's 700 (lifting its mean from 295 to 360), or sixth in the core (lowering its mean from 1,179 to 1,134). Assigning her either way would move the ratio in the direction of the assignment, which is precisely the kind of analyst degree-of-freedom that makes a finding untrustworthy.

**What this costs.** The comparison is 7 against 7 rather than 8 against 7, and a reader who thinks the classification is obvious will think I have dodged it. I would rather be accused of over-caution than of having chosen the grouping that produced the ratio I wanted.

## D9. The author-matching bug — the most consequential error in the analysis

**What went wrong.** Author matching against cited references was first implemented as exact string comparison ("TOURY G"). Inspection of the actual data showed WoS renders the same author in at least four ways within one corpus:

| Form | References in TS-J |
|------|--------------------|
| TOURY GIDEON. | 922 |
| TOURY G. | 201 |
| TOURY GIDEON | 161 |
| TOURY G | 67 |

Exact matching therefore captured **67 of 1,351** Toury references — an undercount by a factor of twenty. The first complete run reported the AS canon at 26 references in TS-J; the correct figure is **210**.

**Why it happened, and why that is interesting.** The Arts & Humanities Citation Index records full forenames far more often than the science indexes around which bibliometric convention — and my expectation — was built. The bug was an imported convention that does not hold in a humanities corpus, and its effect was to make a humanities literature look eight times more absent than it is. Given what this chapter argues, that is not a neutral coincidence and §6.10 says so.

**The fix.** Normalise every name to (surname, first initial). This merges the four Toury forms while keeping MCFARLANE B (the adaptation theorist) distinct from MCFARLANE J (unrelated). Matching at the initial rather than the surname alone is the conservative choice: it splits the rare scholar indexed under two forenames and therefore *under*-counts — the right direction of error for a chapter arguing AS is under-cited, because it biases against my own expectation.

**How it was caught.** By checking the top-20 most-cited authors in each corpus against the match results and noticing that Jakobson and Toury returned zero hits in AS-J, which was not credible. The lesson for the write-up: every automated match should be sanity-checked against a manually inspected frequency list before any number derived from it is reported.

## D10. Temporal analysis by rate, not by count

**Decision.** §6.8's fidelity/equivalence trajectories are measured as the annual *proportion* of each corpus engaging the term, not as counts or as the median year of engaging documents.

**Why.** Both corpora grow steeply. A count-based median measures when a corpus became large. Running it first gave AS's fidelity engagement as peaking 3 years *earlier* than TS's; rate-normalisation reversed this to 13 years *later*. Same data, opposite finding. The count-based version is reported nowhere; this entry is the only record that it existed, and it exists so that the choice of measure is visible as a choice.

## D11. RPYS window-edge artefact

**What went wrong.** Reference Publication Year Spectroscopy computes each year's deviation from the surrounding 5-year median. The first implementation accumulated reference counts only within the reporting window (1900–1990), so the median at the window edge included years that were empty *by construction*. This manufactured spurious "foundational peaks" at 1989 (+428) and 1990 (+976) — the two largest in the series, and both entirely artefactual.

**The fix.** Accumulate counts over the full year range; report deviations only for the window. The corrected TS-J deviation ranking is 1978 (+391), 1981 (+222), 1959 (+211, Jakobson), 1986 (+202), 1972 (+178, Holmes). Table 6.13 names 1959 and 1972 because they resolve to identifiable founding texts, not because they are the largest deviations — 1981 and 1986 are larger and resolve to nothing in particular. That selection is interpretive and the table now says so. AS-J's three (1977, 1984, 1957) *are* its three largest.

**Why it is logged.** Because a version of Figure 6.10 existed in which the largest spike in Translation Studies' foundational archive was an artefact of my own window boundary, and it looked entirely plausible.

## D12. Journal abbreviations derived from the corpora, not from memory

**Decision.** Rather than hand-listing how Clarivate abbreviates each journal, the abbreviation set is read off the corpora themselves: every source form appearing in AS-J's own records is, by construction, an AS journal name as WoS writes it.

**Why.** This is the systematic fix for D5's dropped-ampersand failure. Hand-listing reproduces exactly the memory-shaped gaps that D6 records; deriving from the data cannot.

**What it caught.** WoS truncates cited-source strings at **twenty characters** (DESCRIPTIVE TRANSLAT, OXFORD HDB ADAPTATIO). A plain equality test therefore silently misses every journal whose abbreviation is longer than twenty characters. Each known form is now registered under its truncation as well as its full length.

## D13. The markedness operationalisation is reported as a failure, not repaired

**Decision.** §6.7's lexical markedness test (bare vs modified uses of each field's own term) returns a null result and is reported as such, with no adjustment to the modifier lists.

**Why.** The temptation was to tune the modifier list until the predicted asymmetry appeared. That would be fitting the instrument to the hypothesis. On reflection the measure is wrong in principle — it captures topicality, not markedness in Jakobson's structural sense — and no modifier list would fix it. The argument survives in two other forms (network hub position, and the database's own taxonomy), and §5.4 should be narrowed to those.

## D14. The keyword-field parsing error — found in verification, and it cost the headline number

**What went wrong.** My parser treated the author-keyword (DE), Keywords Plus (ID) and subject-category (SC/WC) fields as one item per line. They are not. Web of Science *wraps* these fields at the line width and separates items with semicolons, so a multi-word keyword can straddle a line break:

    DE literary translation; adaptation; literary adaptation; adaptation
       studies; Herman Melville; Moby Dick; men's literature; Danish
       translation

The parser split this into ...adaptation and studies..., so the phrase "adaptation studies" was not present in the record as far as any search was concerned.

**What it cost.** Exactly one record — and it was one of the eleven that constitute the van Doorslaer and Raw replication, the most rhetorically loaded count in the chapter. The buggy figure was **ten**, which matched van Doorslaer and Raw's "not more than ten" so neatly that it read as a striking result. The correct figure is **eleven**: still a close replication, no longer an uncanny one.

**Why this one unsettles me most.** The bug produced a *better* result than the truth, and it would have survived any check that did not go back to the raw export. I had no reason to doubt ten. It is the clearest instance in this project of the thing §1.5 warns about: an error that confirms the expectation is much harder to see than one that contradicts it.

**Downstream effects, all recomputed:** keyword co-occurrence networks (TS-J edges 2,385 → 2,132), degree centralities (*translation* in TS-J 0.948 → 0.864, *adaptation* in AS-J 0.711 → 0.727), the thematic map (13 themes → 11, with *adaptation*, *equivalence*, *multimodality* and *intersemiotic translation* now resolving into a single lowest-density cluster — a sharper confirmation of §6.6's prediction than the buggy version gave), and token-level markedness (by ~0.5 points; the null result is unchanged).

## D15. The same author-matching error, in a second measure

**What went wrong.** The §6.9.2 measure of how many authors publish in both fields compared **exact full-name strings**. This is D9's bug again, in a place I had not thought to look — and the evidence was sitting in my own output file, which listed both CATTRYSSE, P and CATTRYSSE, PATRICK among the "overlapping authors": one person counted as two.

**What it cost.** The measured overlap was **45 authors**; the surname-plus-initial normalisation used everywhere else gives **107**. The distinct-author totals also fall (TS-J 9,975 → 8,984; AS-J 2,089 → 1,991), since the same merging applies within each corpus.

**Why it matters beyond the number.** 45 out of 12,000 supported the sentence "almost entirely separate author communities." 107 out of 11,000 — 5.4% of the AS community — supports "very largely separate," which is weaker. The finding survives; the adjective did not.

**The pattern worth naming.** Three coding errors (D9, D14, D15) and one methodological artefact (D11) were found in this project. **Every one biased the result toward the thesis.** I do not think that reflects intent; the code was written before most results were known. I think it reflects that an error confirming what you expect does not announce itself — which is why the verification pass, in which every numeric claim in the chapter was mechanically checked against the analysis outputs, is not housekeeping but part of the method, and should be described as such in §1.5.

## D16. The figures are set in the thesis body face, at the thesis body size

**The decision.** Every figure is redrawn in a Times New Roman substitute at 12 pt, on a canvas exactly 6.5 in wide — the width of the thesis text block on US Letter paper with 1 in margins.

**Why it is not merely cosmetic.** A figure whose labels are set in a different typeface at a different size announces itself as an imported object. In a chapter that argues about what belongs inside a field and what is admitted from outside it, having the evidence look like a visitor is an avoidable irony. Matching the type is also what makes the numbers inside the figures readable at the same effort as the numbers in the prose.

**The substitution, stated plainly.** Times New Roman is proprietary (Monotype) and could not be installed in the analysis environment. The figures use a metrically compatible free Times clone (Nimbus Roman / Tinos, with Liberation Serif as fallback). At 300 dpi inside a raster image, neither is distinguishable from Times New Roman in print or in PDF. If an examiner asks, this is the honest answer and it costs nothing.

**What had to be true for "12 pt" to mean 12 pt.** Type inside a raster image is only 12 pt on the page if the image is placed at native scale. Three adjustments follow from that, and all three are in scripts/tnr_mode.py:

1. Each figure is authored at exactly 6.5 in wide and saved with 300 dpi metadata, so Word's default insertion size *is* the correct size. **Do not resize the images after inserting them** — dragging a corner changes the type size.
2. Each figure's height is scaled by (6.5 / original width) × (12 / 9), preserving the original ratio of type to drawing area. The scripts were authored at 9 pt, hence the 12/9. Every explicit font size in the drawing code — annotations at 7.4–8.5 pt, panel headings at 10 pt — is scaled by the same factor rather than overridden, so the internal hierarchy survives. The resulting range, about 10–13 pt, sits inside the 8–14 pt APA 7 permits within a figure.
3. Hand-placed label offsets, which are specified in points and therefore do not grow with the type, are scaled by the same factor. Four labels on the thematic map (Figure 6.9) still collided and were re-placed onto separate rows; those placements are recorded in make_figures.py, not nudged by eye.

**One bug worth recording, because it would have shipped silently.** Saving with bbox_inches="tight" cropped the last word off the x-axis label of the two-panel figures. The cause is that Figure.get_tightbbox() does not report an axis label wider than the axes it is centred on, so the crop was computed from a bounding box that excluded the label's tail. The fix is to save the full canvas instead. It was caught by reading the delivered images at full size rather than trusting that the figure code had not changed behaviour — the same habit that caught D14.

# SESSION 3 — 22 September 2026

Every script re-executed from the 73 raw exports, in order, in a clean environment (Python 3.11.15, matplotlib 3.10.9, networkx 3.6.1), and every output compared with the deposited outputs the thesis was written from. Nineteen of the twenty-one analysis files reproduced byte-for-byte; all tables reproduced; fourteen of the twenty-two figures in the thesis reproduced pixel-for-pixel. What did not reproduce is recorded below, in the same spirit as D9–D15: the errors are logged, not repaired quietly.

## D17. Two figures could not be reproduced by the deposited script, and the deposited script had two bugs

**What was found.** Figure 6.3 (thematic evolution of AS-J) and Figure 6.16 (geography of publication) were first drawn on 11 August by a script (`figs_45.py`) that was never saved. When the analyses were restructured on 24 August, `make_chapter_figures.py` re-implemented both from their description. That re-implementation was deposited, but nobody re-ran it against the published figures. Run today, it gives different numbers: the cultural-politics stream peaks at 30.9% of AS-J records instead of the 26.1% in the text, and the United States' share of AS-J falls to 34% instead of 42%.

**Why the numbers differed.** Two bugs and one lost choice. (i) The term sets were matched without word boundaries, so *race* matched *trace* and *embrace*, *gender* matched *engendered*, and the cultural-politics series was inflated. (ii) The minimal parser inside the script joined the address lines of a record into one string, so a record with authors in three countries was counted under the last country only; and an address ending in a US state and ZIP code without the word USA — the form the database uses for records before about 1990 — was counted under the state rather than the country. (iii) The Global South share (24.5% / 7.3% / 18.3%) was computed from a country list that was never written down.

**Decision.** Repair the deposited script rather than search for the lost one, and let the thesis report what the deposited script produces. Whole-word matching; the package parser (`wos_parser.load_corpus`) instead of the private one, so that every figure reads the corpus the same way; a US-state rule for the pre-1990 addresses; and a *declared* Global South list — the UNCTAD grouping of developing economies (everything outside Europe, Northern America, Australia, New Zealand, Japan and Israel), written into the script so a reader can move a country and see what changes.

**What changed in the thesis.** Figure 6.3: fidelity 0.9% (1995) → peak 7.0% (2021), 6.4% (2023); intertextuality 0 → 14.6%; cultural politics 3.6% → peak 26.0% (2022); digital and transmedia 0 → 21.3%. The pattern the section argues from — no stream declines, all four at or near their maxima together — is unchanged; the phrase "fifteen times its share three decades earlier" is withdrawn (the corrected series rises about sevenfold). Figure 6.16: the United States is 47% of AS-J records rather than 42%, the United Kingdom 22%, so the two countries supply two-thirds rather than "nearly two-thirds"; Spain 16%, the United Kingdom 15%, China 12%, and Brazil and the United States tied at 8% in TS-J; Global South shares 30.0% (TS-J), 8.7% (AS-J) and 23.3% (AS-T). The finding is the same in direction and stronger in degree. The paste-ready sentences are in the verification report.

**Why it is logged.** Because the two figures whose scripts were lost are the two whose numbers drifted, and because the direction of drift was, once again, mixed rather than random: the geography error understated the American concentration of AS-J (against the argument), while the term-matching error overstated cultural politics (for it). D9, D14 and D15 all ran toward the thesis; D17 is the first that ran both ways.

## D18. Table 6.1 and the rate in Figure 6.14 are now derived from the outputs

**What was found.** Table 6.1 (Jakobson and Bluestone across all three corpora) had been computed by hand in August and typed into the chapter; no output file contained its AS-T row. And the box in Figure 6.14 quoted the translation canon's presence in AS-J as 29.6 per 10,000, the rate per *raw* reference, while Figure 6.2, Table 6.4 and Table 6.6 use 32.9, the rate per *parsed* reference. Both were re-derived today and both were arithmetically correct; the problem was provenance and consistency, not error.

**Decision.** A step 11 added to `analysis_cross_corpus.py` writes `13_founders_across_corpora.json`, and `make_tables.py` exports Table 6.1 from it (values unchanged: 13.75 / 4.08 / 2.71 per 10,000 for Jakobson; 0.03 / 17.90 / 2.79 for Bluestone). Figure 6.14 was redrawn from the outputs with the parsed-reference rate (32.9), the one denominator the thesis uses. `make_tables.py` was renumbered to the September structure (Tables 6.1, 6.2, 6.4, 6.5, A.2; the TS-J theme table and the term-presence counts are exported as supplementary tables S.1 and S.2).

## D19. The Louvain partition is not reproducible across library versions; what is invariant is stated instead

**What was found.** The keyword networks reproduce exactly (TS-J 250 nodes / 2,132 edges; every frequency, degree centrality and betweenness value identical). The community detection on top of them does not: `networkx` 3.1, 3.2.1, 3.3, 3.4.1, 3.4.2, 3.5, 3.6.0 and 3.6.1 each return a slightly different Louvain partition at the same seed, and none of the eight reproduces the deposited (August/September) partition exactly. The run is deterministic within a version (the Python hash seed makes no difference). The README's warning that "cluster memberships replicate while numbering may not" was therefore too optimistic: memberships at the cluster margins move too.

**What is invariant, in all nine partitions (eight versions plus the deposited one).** In TS-J, *adaptation* sits in the lowest-density cluster on the map together with *literary translation*, *retranslation*, *equivalence*, *intersemiotic translation*, *rewriting* and *Shakespeare*, in every version (eighteen keywords in six of nine, up to thirty in the others). The AS-J partition is identical in every version: *translation* in the largest, most central cluster, beside *adaptation*, *intertextuality* and *fidelity*; Shakespeare naming two clusters. In AS-T, the adaptation theme is always the largest (76–83 keywords) and always among the least dense, and the four other-sense clusters are always present.

**What is not invariant.** In AS-T, "peripheral on both axes" (the emerging/declining quadrant) holds in the deposited partition and one version; in the other seven the adaptation theme is central but thin (the basic/transversal quadrant). "More than twice its nearest rival" holds in three of nine (the ratio ranges from 1.5 to 1.8 in the others). The number of AS-T themes is 8 or 9; TS-J 10 or 11.

**Decision.** The deposited partition is retained as the one every figure and sentence describes, and is kept in the deposit; `run_all.py` keeps a fresh partition beside it under its library version and redraws the maps from the deposited one, printing why. §6.4's sentence on the AS-T theme is softened to what survives every version, and Appendix A.8 now reports this cross-version test in place of the earlier twelve-configuration check (which varied seed and resolution but not the library). The quadrant labels were already declared indicative in A.8; this is the case that shows why.

## D20. Four scripts were missing from the deposit; the deposit is restructured so that it runs

**What was found.** The scripts behind Figures 6.4–6.6 (`analysis_three_corpora.py`, `make_labelled_maps.py`, `make_three_maps.py`, written 18 September) were on disk but not in the supplementary package or Appendix B; `make_fig_a2_flow.py` (Figure A.2) was listed in Appendix B but its listing in the thesis was cut off after the first forty lines, and no copy existed outside the paste-ready appendix file. Several scripts carried absolute paths to the machine they were written on.

**Decision.** All fifteen scripts are in the deposit with paths relative to the package; `run_all.py` executes them in order, logs each, and compares every output with the deposited copy; `requirements.txt` pins the environment; the README states the reproduction procedure that was actually followed today, including the Louvain caveat. Appendix B lists all fifteen. The two superseded scripts (`analysis_as_networks.py`, `make_as_thematic_map.py`, the two-panel adaptation map that Figures 6.4–6.6 replaced) are not deposited.

**Verification of the rest.** Every number in Chapter 6 and Appendix A was checked against the rerun outputs; the two-paragraph list of remaining text corrections (one arithmetic slip — "under 1%" for a value of 1.19% — and the stale section cross-references left by the September restructuring) is in the verification report, not here, because they are copy-editing rather than method.


## Query log

| # | Corpus | Query | Date | Result |
|---|--------|-------|------|--------|
| Q-01 | TS (topic, exploratory) | TS=("translation studies" OR "translation theory" OR "translatology") | 29 Jul 2026 | 6,482 |
| Q-02 | TS (journals) | SO=(20 journal titles) AND PY=(1990-2025) | 29 Jul 2026 | 13,271 |
| Q-03 | AS (journals) | SO=("ADAPTATION" OR "LITERATURE FILM QUARTERLY" …) — no date limit; JAFP missed | 29 Jul 2026 | 2,281 |
| Q-04 | AS (topic, phrase-based) | TS=("adaptation studies" OR "film adaptation" OR "literary adaptation" OR "screen adaptation" OR "stage adaptation" OR "cinematic adaptation" OR "theatrical adaptation" OR "adaptation theory") | 29 Jul 2026 | 3,376 |
| Q-05 | AS (topic, 11 categories) | Q-04 refined by WoS Categories | 29 Jul 2026 | 1,756 |
| Q-06 | TS (journals, FINAL) | SO=(21 seed titles; 20 return records) — no date limit, FORUM added | 29 Jul 2026 | 14,252 |
| Q-07 | AS (journals, FINAL) | SO=("ADAPTATION" OR "ADAPTATION-THE JOURNAL OF LITERATURE ON SCREEN STUDIES" OR "JOURNAL OF ADAPTATION IN FILM PERFORMANCE" OR "LITERATURE FILM QUARTERLY") — no date limit | 29 Jul 2026 | 2,761 |
| Q-08 | AS-T (topic, 13 research areas, FINAL) | TS=(adaptation) refined by 13 Research Areas | 4 Aug 2026 | **18,566** |
| Q-09 | TS-J re-export | Q-06 re-run for export | 4 Aug 2026 | **14,258** |
| Q-10 | AS-J re-export | Q-07 re-run for export | 4 Aug 2026 | **2,763** |

**Database drift, measured.** Q-06 → Q-09 gained 6 records and Q-07 → Q-10 gained 2, in one week, with identical queries. Every count in the chapter therefore carries its date. A replicator will get different numbers, and that is a property of the object, not a failure of the method.

## The three corpora, as frozen

| Corpus | Definition | Records | Cited references | Parsed | Parse rate |
|--------|-----------|---------|------------------|--------|------------|
| **TS-J** | 20 Translation Studies journals | 14,258 | 333,707 | 318,442 | 95.4% |
| **AS-J** | 3 Adaptation Studies journals | 2,763 | 48,954 | 44,126 | 90.1% |
| **AS-T** | Adaptation topic, 13 humanities research areas | 18,566 | 660,554 | 627,992 | 95.1% |
| **Total** | | **35,587** | **1,043,215** | **990,560** | **95.0%** |

AS-J and AS-T are kept **separate**, not merged. AS-J is adaptation research as a venue-based field; AS-T is adaptation research dispersed through other people's journals. The distinction speaks directly to ¶671's *ceded practice*. Merging would destroy exactly the contrast worth measuring.

**The headline ratio: 14,258 against 2,763 — roughly 5:1.** How much of that is the fields and how much is Clarivate is not separable from within WoS, which is what the OpenAlex comparison is for.

### TS journal composition (Q-09, the frozen corpus)

**Correction to Session 1.** The Session 1 table listed 20 journals with counts drawn from the date-limited Q-02. The frozen corpus (Q-09, no date limit) is as follows. Note also that *Translation Studies in Translation*, listed in Session 1 at 13 records, does not appear in the export; the 13-record entry is *Translation in the Arab World*. The seed list contained 21 titles; 20 return records.

| Journal | Records |
|---------|---------|
| Meta | 2,356 |
| Translation Review | 1,538 |
| Cadernos de Tradução | 1,385 |
| Perspectives | 1,069 |
| Translation and Literature | 1,046 |
| Journal of Specialised Translation | 837 |
| Babel | 768 |
| The Translator | 694 |
| Translation Studies | 671 |
| Target | 620 |
| The Interpreter and Translator Trainer | 533 |
| Sendebar | 442 |
| FORUM | 408 |
| Translation and Interpreting Studies | 372 |
| Across Languages and Cultures | 353 |
| MonTI | 343 |
| Interpreting | 307 |
| Linguistica Antverpiensia NS | 280 |
| Translation Spaces | 223 |
| Translation in the Arab World | 13 |
| **20 journals** | **14,258** |

*Counts are case-insensitive. Six of these journals also appear under a mixed-case duplicate source string in the export; counting raw strings gives 26 "journals" and loses 22 records.*

### AS journal composition (Q-10)

| Journal | Records |
|---------|---------|
| Literature/Film Quarterly | 1,772 |
| Adaptation (Oxford) | 511 |
| Journal of Adaptation in Film & Performance | 480 |
| **3 journals** | **2,763** |

### TS-J document types (Q-09)

**Correction to Session 1**, which reported the date-limited Q-02 figures.

| Type | Count |
|------|-------|
| Article | 8,644 |
| Book Review | 3,824 |
| Editorial Material | 870 |
| Poetry | 318 |
| Article; Early Access | 244 |
| Review | 69 |
| Book Review; Early Access | 49 |
| Biographical-Item | 43 |

## Outstanding

**Closed since Session 1.**

- Re-run TS without the date limit — Q-09, 14,258
- Verify TTR — confirmed genuinely absent (D5)
- Re-run AS journals with corrected JAFP title — Q-10, 2,763
- Decide on merging AS-J and AS-T — kept separate
- Export all three corpora — 73 files, audited, three-way match confirmed
- Estimate residual noise in AS-T — 4.8% on a 400-record random sample (seed 20260806)

**Closed in Session 3 (22 September 2026).**

- Full rerun from the raw exports in a clean environment: 19 of 21 analysis outputs byte-identical, all tables identical, 14 of 22 figures pixel-identical; the rest repaired and logged (D17–D20).
- Scripts for Figures 6.4–6.6 and A.2 added to the deposit; Table 6.1 derived from an output file (D18).

**Still open.**

- Run the OpenAlex comparison and quantify what WoS misses, especially books. **This is the single most useful remaining piece of work**, because D1's cost is currently declared but not measured.
- Run verify_in_bibliometrix.R on a machine with CRAN access and report the agreement (D7).
- Record first-year-of-WoS-coverage for all 20 journals (for the growth-curve caveat, D3).
- Systematic check of the TS journal seed list against BITRA / TSB (D6).
- Identify which of the 21 seed titles returned no records (D12 / §6.3.3).
- The attribution analysis of ¶654 — deferred to future work, and named as such in §6.10.

## Notes toward §6.10

Six things that emerged from this work are arguments, not housekeeping.

1. **Adaptation requires disambiguation; translation does not.** Filtering the adaptation searches cut them by orders of magnitude. No equivalent operation was needed for "translation," whose disciplinary sense is unmarked and assumed. §5.4's markedness argument, arrived at through a data-cleaning problem rather than through Jakobson.

2. **The instrument enacts the thesis.** TTR absent; AS book literature under-indexed; AS references parsing 5 points worse than TS's; a Korean journal missing from the seed list until chance corrected it; cited sources truncated at 20 characters. This cannot be corrected away — only declared.

3. **The analyst enacts it too.** D9's matching bug was not random. It imported a science-index convention into a humanities corpus and made a humanities literature look eight times more absent than it is. The researcher's own tools carry the same centre as the researcher's memory (D6). Nor was it a one-off: three separate coding errors (D9, D14, D15) each biased the result toward the thesis, and one of them produced a number so satisfying that only a return to the raw export exposed it.

4. **The corpus is a made object.** Twenty journals rather than nineteen or twenty-five; thirteen research areas rather than nine or fourteen; each boundary defensible, none inevitable. The counts are findings about *this* corpus, built *this* way, on *this* date.

5. **Three of the chapter's own predictions failed** — the comparison-class test (§6.4), the kind-of-citation test (§6.5.3), and the lexical markedness test (§6.7) — and are reported as failures. A chapter that only confirmed itself would be evidence of a badly-designed test, not of a correct thesis.

6. **Verification is part of the method, not a courtesy.** Every numeric claim in the chapter was mechanically re-derived from the analysis outputs before the §6.10 verdicts were written. That pass found four errors, changed the headline replication figure from ten to eleven, and weakened one adjective in the conclusion. A thesis arguing that knowledge is shaped by the position of the knower cannot exempt its own arithmetic from the claim.

7. **The central finding was predicted in advance, in the right direction, by a method that examined no citation data.** Chapter 5 derived the direction of the TS–AS relation from handbooks, taxonomies and definitional gestures. The citation record's asymmetry runs the same way, at 5:1 and 13:1, against near-identical self-citation baselines. That is the strongest corroboration this dissertation's integrative method can produce, and §6.10 should claim it — carefully, and no more widely than the data allow.

# Chapter 6 — Technical Process Log & Defence Companion

*A beginner-friendly record of every technical step, what it did, why it was chosen, and how to answer questions about it. Companion to* Ch6_decision_log.md *(which records the research decisions; this file records the mechanics). Updated 6 August 2026, after the analyses were run. Two figures corrected 13 August 2026 (both marked in place).*

## Part 1 — The environment

**What I use.** Two tools, for two different jobs.

**R (4.5.2) with RStudio and the bibliometrix package (5.4.1), including its point-and-click interface biblioshiny.** R is a statistical programming language — the engine. RStudio is the application I work in. bibliometrix is an add-on written by Massimo Aria and Corrado Cuccurullo (2017) that specialises in bibliometric analysis: it knows how to read Web of Science files and compute citation networks, keyword maps and thematic analyses. On my own machine, this is what loaded the three corpora into the frozen .RData datasets on 6 August 2026 and produced the biblioshiny descriptive figures in Visuals/TSJ-biblioshiny-aug6/.

**Python (3.11), with purpose-written scripts.** Python is a general-purpose programming language. I use it for the analyses bibliometrix cannot perform — see Part 2.

**If asked: "Why bibliometrix?"** Three reasons. (1) It is the standard citable tool in bibliometric research — analyses are reported as "conducted in bibliometrix (Aria & Cuccurullo, 2017)," which makes my method comparable and replicable. (2) It is open source: anyone can verify what the functions do, unlike proprietary tools. (3) Alternatives were considered: VOSviewer is excellent for network visuals but is a visualisation tool, not a full analysis environment; CiteSpace is Java-based and oriented to the sciences.

**If asked: "Then why is half of Chapter 6 done in Python?"** — *and this question will be asked, so the answer must be exact.* Because bibliometrix's unit of analysis is **one corpus at a time**. Chapter 6's central questions are cross-corpus: what proportion of Translation Studies' reference record consists of Adaptation Studies literature, and how does that compare with the reverse? No function in bibliometrix answers that, and my own research design document said so in advance ("biblioshiny analyses one corpus at a time… Q1, Q2 and Q6 are inherently two-corpus questions and cannot be done in the GUI"). So the division is:

| Job | Tool |
|-----|------|
| Loading and parsing the 73 export files | R / bibliometrix convert2df() — **and** independently in Python |
| Deduplication, audit, frozen datasets | R / bibliometrix (.RData) |
| Descriptive figures (production, sources, authors, Bradford, Lotka) | biblioshiny |
| **Cross-corpus reference matching (§6.4, §6.5)** | **Python** |
| **Markedness regex pass (§6.7)** | **Python** |
| **Rate-normalised trend analysis (§6.8)** | **Python** |
| **RPYS and structural separation (§6.9)** | **Python** |
| **Keyword networks and Callon thematic map (§6.6, §6.7)** | **Python** (see note) |

*Note on the last row.* Thematic mapping and keyword co-occurrence ARE bibliometrix functions, and bibliometrix would have been the natural tool. The environment in which the analysis scripts ran had no network route to CRAN, so the package could not be installed there. The Callon centrality and density formulas were therefore implemented directly from Callon, Courtial & Laville (1991) — the source bibliometrix itself implements — and verify_in_bibliometrix.R reproduces them for cross-checking on my own machine, where the package is installed.

**Be exact about this if asked.** Every number reported in §§6.4–6.9 was computed by the Python scripts. The R/bibliometrix side of the work is the load, the audit and the descriptive figures. The cross-check script has been written but **not yet run**; running it, and reporting the agreement, is an outstanding item.

**If asked: "Did you write the analysis code yourself?"** The scripts were written with the help of an AI coding assistant, used for drafting and debugging code, and I executed, checked, and can explain every step — this log is that explanation. The substantive decisions (corpus definitions, inclusion and exclusion of research areas, interpretive framings, and the choice to report failed predictions as failures) are documented as mine in the decision log, with rationale. Four errors in the code and its measures were found and corrected during the work; all four are documented in Part 6 and in decision log D9, D11, D14 and D15, and I can explain each of them.

**If asked: "Why not just report everything as bibliometrix?"** Because it would be untrue, and an examiner who asked to see the bibliometrix output behind Table 6.4 would find there is none. This is recorded as decision D7.

## Part 2 — Data collection (summary; full detail in Ch6_decision_log.md)

**What I did.** Ran three frozen searches in Web of Science Core Collection (via uOttawa's subscription, July–August 2026), then exported every record as plain-text files, 500 records at a time, with the setting **Record Content = "Full Record and Cited References."**

**The three corpora, as loaded:**

| Corpus | Definition | Records | Cited references |
|--------|-----------|---------|------------------|
| TS-J | All records in 20 Translation Studies journals | 14,258 | 333,707 |
| AS-J | All records in the 3 dedicated Adaptation Studies journals | 2,763 | 48,954 |
| AS-T | Topic search adaptation filtered to 13 humanities Research Areas | 18,566 | 660,554 |
| **Total** | | **35,587** | **1,043,215** |

**If asked: "Why plain text and not BibTeX/Excel?"** Plain text ("Web of Science field-tagged format") is the format bibliometrix parses most completely, and it is the only export I verified to carry the full cited-reference lists in a stable structure. Mixing formats risks inconsistent field coverage.

**If asked: "Why 'Full Record and Cited References'?"** Because the chapter's central analyses are *relational* — who cites whom. Without the cited-references field (CR), a record tells you only what was published, not what it drew on. This setting is also why exports were capped at 500 records per file (WoS lowers its cap from 1,000 to 500 when references are included), which is why the corpora travelled as 73 separate files.

**If asked: "How do you know the export is complete and uncorrupted?"** Every file was audited: record counts per file (grep for the PT field that begins every record), byte-level duplicate detection by md5 checksum (which caught two accidental duplicate files, quarantined rather than deleted), and unique-record counts against the frozen search totals. Final audit: TS-J 14,258 unique of 14,258 expected; AS-J 2,763 of 2,763; AS-T 18,566 of 18,566. **Zero gaps.** The counts were then independently re-derived in Python from the raw files, without reference to the R output, and agree exactly — which is a stronger check than either tool alone.

## Part 3 — The load script (load_corpora.R), line by line

This is the script I ran on 6 August 2026.

    library(bibliometrix)

**What it does:** loads the bibliometrix package into this R session, making its functions available. Installing a package (done once) puts it on the computer; library() (done every session) switches it on.

    base <- "/Users/.../Chapter 6/bibliometric_data"

**What it does:** stores the path to my data folder in a variable called base, so the folder location is written once and reused. <- is R's assignment arrow: "put the thing on the right into the name on the left."

    load_corpus <- function(folder) { ... }

**What it does:** defines a small reusable function of my own. A function is a recipe: I give it a folder name ("TS-J") and it performs the same sequence of steps for any corpus. Writing it once and using it three times guarantees all three corpora are processed *identically* — a methodological point, not just a convenience: no corpus received different treatment.

    files <- list.files(file.path(base, folder), pattern = "\\.txt$", full.names = TRUE)

**What it does:** collects the names of all files ending in .txt inside the corpus folder. pattern = "\\.txt$" is a regular expression meaning "ends with .txt". list.files without recursive = TRUE looks only at the folder itself, not inside its subfolders — this is what ensures the quarantined duplicates (which sit in a _duplicates subfolder) are NOT loaded. full.names = TRUE returns complete paths.

    M <- convert2df(file = files, dbsource = "wos", format = "plaintext")

**What it does — the most important line:** reads all the raw text files and converts them into a single structured table (a "data frame" — one giant spreadsheet where each row is one publication and each column one field). The raw files are in WoS's "field-tagged" format: every line starts with a two-letter tag (TI = title, AU = authors, SO = source, PY = publication year, AB = abstract, DE = author keywords, CR = the full cited-reference list, UT = the record's unique accession number). convert2df knows this grammar. It also standardises as it reads, which is what makes later matching possible.

**If asked:** "The unit of analysis is the indexed document; each row of the resulting matrix is one document, each column one Web of Science metadata field, including the complete cited-reference string."

    M <- M[!duplicated(M$UT), ]

**What it does:** removes duplicate records. M$UT is the column of unique WoS accession numbers (every indexed document has exactly one, like an ISBN). duplicated() flags any row whose UT has already appeared; ! means "not". In words: "keep each document the first time you see it, drop any second appearance."

**Why duplicates existed at all:** the 500-record export windows were entered by hand; one window in TS-J overlapped its neighbour by one record, and this line removed that overlap (14,259 raw → 14,258 unique).

**If asked:** "Deduplication was by Web of Science accession number (UT), the database's own unique identifier — not by title matching, which can produce false merges between an article and its own erratum."

    save(TSJ, file = ...)

**What it does:** writes the finished table to disk in R's native .RData format, so the corpora load in seconds instead of the 5–15 minutes of re-parsing. It also **freezes** the dataset: every analysis runs from these three saved files, so the data cannot silently drift between analyses.

**If asked:** "The frozen analysis datasets are TSJ.RData, ASJ.RData, AST.RData, created 6 August 2026."

## Part 4 — The Python scripts, and what each one does

Four scripts, in the order they run. All are in the supplementary files and all print a running commentary as they execute, so the console transcript is itself a record of the procedure.

### wos_parser.py — reading the raw files independently

**What it does.** Parses the same 73 plain-text files that bibliometrix reads, into the same structure, without using bibliometrix.

**Why a second parser exists at all.** Two reasons, one practical and one methodological. Practically, the Python analyses need the data in Python. Methodologically, parsing the corpus twice with independent code and getting identical counts (14,258 / 2,763 / 18,566) is a real verification: a bug in one parser would show up as a disagreement. It did not.

**The format, in one paragraph.** A WoS export is a stack of records. Each record starts with PT J and ends with ER. A line whose first two characters are a tag and whose third is a space starts a new field; a line beginning with three spaces continues the previous field. Multi-value fields (authors, keywords, cited references) keep each line as a separate item; single-value fields (title, abstract) join continuation lines with a space.

### canon.py — the hand-curated matching lists

**What it does.** Holds the lists of canonical authors for each field, plus five benchmark comparison classes, as (surname, first-initial) pairs.

**If asked: "Why hand-curated?"** Because the Adaptation Studies canon is books, and WoS renders book titles in the cited-source slot inconsistently and truncated at 20 characters (*A Theory of Adaptation* appears as A THEORY OF ADAPTATION, THEORY ADAPTATION, OXFORD HDB ADAPTATIO…). No automatic procedure resolves these; a human has to decide that they are the same book. The decision is a research act, so the lists are part of the chapter's record rather than buried in code.

**If asked: "Couldn't your list be biased toward finding absence?"** The matching rule under-counts by design (see Part 6, "the Toury problem"), which biases *against* the chapter's own expectation. And the benchmark classes were built by the same procedure and matched against the same corpus, so any bias applies equally to the comparison — which is exactly why a comparison class is there.

### analysis_cross_corpus.py — §6.4, §6.5, and the audit

**What it does, in eleven printed steps:** re-verifies the record counts; derives each field's journal-abbreviation set from the corpora themselves; parses every cited reference and reports the parse rate; counts the term *adaptation* in TS-J; matches both canons and all five benchmark classes; builds the directional cross-citation ledger; classifies cross-citations as canon or journal; runs the markedness pass; estimates the AS-T noise rate on a seeded random sample; compares frontier and core authors; and computes RPYS and author overlap.

### analysis_refined.py — three measures replaced

**What it does.** Replaces three operationalisations from the first pass that were too crude to report, each documented in place with why: markedness moved from document level to occurrence level; temporal analysis moved from counts to rates (which reversed the §6.8 finding); RPYS corrected for a window-edge artefact.

### analysis_networks.py — §6.6 and §6.7 networks

**What it does.** Builds keyword co-occurrence networks, partitions them into themes by Louvain community detection, and computes Callon centrality and density for each theme.

**If asked to explain Callon centrality and density in plain language:** Build a network where each node is a keyword and each edge joins two keywords that appear on the same document. Group the network into clusters ("themes"). Then **density** is how tightly a theme holds together internally — its degree of development. **Centrality** is how strongly it connects to everything outside itself — its importance to the field overall. Plotting the two against each other gives four quadrants: *motor* themes are central and developed; *niche* themes are developed but isolated; *emerging or declining* themes are neither; *basic/transversal* themes are central but not yet developed.

**If asked: "Isn't 'structurally marginal' just whatever your measure says it is?"** Yes, and the chapter says so explicitly at §6.6. Operationalising marginality as low network centrality is a *choice*, defended as one, not a discovery. The finding is reported alongside a second, independent operationalisation (author-level citation counts), and the two agree.

## Part 5 — Log of analysis steps

**2026-08-06 09:35 — Corpora loaded and frozen (R/bibliometrix).** TS-J 14,258; AS-J 2,763; AS-T 18,566. Three-way match against the frozen search counts and the raw-file audit.

**2026-08-06 09:35–09:45 — biblioshiny descriptive figures for TS-J.** Annual scientific production, average citations per year, most relevant sources, source impact, source dynamics, Bradford's law, most local cited sources, most relevant authors, authors' production over time, author impact, Lotka's law, most local cited authors, most relevant affiliations, affiliations over time, three-field plot, missing-data table. Saved to Visuals/TSJ-biblioshiny-aug6/.

**2026-08-06 — Independent re-parse in Python.** Counts agree exactly with the R load. Cited references: 1,043,215 total, 990,560 parsed (95.0%).

**2026-08-06 — First analysis pass.** Produced the full §§6.4–6.9 results. **Rejected** after verification: the author matcher was matching exact strings and undercounting by up to 20× (see Part 6).

**2026-08-06 — Author matcher corrected**, journal abbreviations moved to empirical derivation, 20-character truncation handled. Second pass produced the figures now reported.

**2026-08-06 — Three measures refined** (markedness → occurrence level; trends → rate-normalised; RPYS → window-edge fix). The trend refinement reversed the sign of the §6.8 finding.

**2026-08-06 — Networks, thematic maps, and the ten publication figures.**

**2026-08-06 — Verification pass.** Every numeric claim in the chapter and both logs was mechanically re-derived from the analysis outputs. Four errors found (D11, D14, D15, plus the journal-count case-sensitivity issue), all corrected, all logged. The van Doorslaer and Raw replication changed from ten to eleven; the author overlap from 45 to 107; the thematic map from 13 themes to 11.

**2026-08-06 — Re-ran all analyses and regenerated all ten figures** from the corrected parser.

**Still to do:** run verify_in_bibliometrix.R on my own machine and report the agreement; run the OpenAlex coverage comparison.

## Part 6 — Anticipated defence questions, quick answers

**"Why Web of Science only?"** §6.3 addresses this directly: a reasoned choice (cited-reference quality, disciplinary convention, consistency with §1.5.1) whose costs — book-weak coverage that structurally under-represents AS — are analysed *as part of the finding*, not hidden. The cost is now measured, not just asserted: AS-J's references parse at 90.1% against TS-J's 95.4%, a gap that is itself a consequence of book-heavy citation practice.

**"Why are the two fields' corpora built differently?"** Because the fields are differently institutionalised: TS can be found at its own 20 journal addresses; AS has 3 journals and a diaspora. Identical procedures would have produced a sham symmetry. The asymmetry of method mirrors the asymmetry under study and is declared in §6.3.

**"Couldn't your keyword filtering have biased the AS corpus?"** Yes, and the chapter says so: four defensible definitions of "adaptation research" differ by orders of magnitude (Table 6.1). That instability is reported as a property of the field's indexed existence. Residual non-humanities noise in AS-T is estimated at 4.8% on a 400-record random sample with a fixed seed, so the estimate is reproducible.

**"How replicable is this?"** Fully, with dates: verbatim queries, search dates, per-corpus counts, export settings, audit procedure, package and language versions, frozen .RData files, and the Python scripts with a fixed random seed. A replicator a year later will get different counts — the databases grow, and I measured the drift myself (+6 records in TS-J and +2 in AS-J within one week) — which is why every count carries its date.

### "The Toury problem" — the error I found in my own analysis

*This is the question I most want to be asked, and the one I should raise myself if it is not.*

**What happened.** My first author-matching code compared exact strings, looking for TOURY G. (The per-form counts quoted below are deposited in analysis_outputs/12_raw_author_forms.json, so they can be checked rather than taken on trust.) Web of Science actually writes the same author four different ways in the same corpus: TOURY GIDEON. (922 references), TOURY G. (201), TOURY GIDEON (161), TOURY G (67). My code found 67 of 1,351 — a twentyfold undercount. The first full run reported the Adaptation Studies canon at 26 references in Translation Studies; the correct figure is 210.

**How I caught it.** By checking the matcher's output against a manually inspected list of the twenty most-cited authors in each corpus. Jakobson and Toury came back as zero in the Adaptation Studies corpus, which is not credible, and that is what exposed the bug.

**How I fixed it.** Every name is now reduced to surname plus first initial, which merges the four Toury forms while keeping MCFARLANE B (the adaptation theorist) separate from MCFARLANE J (an unrelated author). This deliberately under-counts rather than over-counts — it splits the rare scholar indexed under two forenames — which is the right direction of error for a chapter arguing that Adaptation Studies is under-cited, because it biases against my own hypothesis.

**Why it is in the chapter rather than hidden.** Two reasons. First, integrity: a chapter that criticises knowledge presented as though produced from nowhere cannot present its own numbers as though they arrived without a first attempt. Second, because the error was not random. It imported a convention from the science citation indexes — where forenames are rarely recorded — into a humanities corpus where they routinely are, and its effect was to make a humanities literature look eight times more absent than it is. That is the chapter's own argument happening inside its own code.

### "Did anything else go wrong?"

Yes — three more things, and I would rather present them than have them found.

**The RPYS window artefact (D11).** Reference Publication Year Spectroscopy measures each year's deviation from the surrounding five-year median. My first implementation counted references only inside the reporting window, so at the window edge the median included years that were empty by construction. It produced two large, entirely artefactual "foundational peaks" at 1989 and 1990 — which looked completely plausible, and would have been the biggest spikes in the figure. Fixed by computing over the full range and reporting only the window.

**The keyword line-wrap (D14) — the one that changed the headline number.** Web of Science *wraps* the author-keyword field and separates keywords with semicolons, so a two-word keyword can straddle a line break. My parser was treating each line as a separate keyword, which split "adaptation studies" into "adaptation" and "studies" in one record. That record is one of the eleven that constitute the van Doorslaer and Raw replication. The buggy count was **ten** — which matched their "not more than ten" so beautifully that it read as an uncanny result and I had no reason to question it. The true count is eleven.

**The author-overlap measure (D15) — the same bug as the Toury problem, in a second place.** §6.9.2 asks how many authors publish in both fields. It was comparing exact full-name strings, so CATTRYSSE, P and CATTRYSSE, PATRICK counted as two different people. Both were sitting in my own output file. The corrected overlap is 107 authors, not 45.

**If asked what these have in common:** every single one biased the result *in favour of* the chapter's thesis. Ten is a better story than eleven; 45 shared authors is a better story than 107; a science-index name convention made a humanities literature look eight times more absent than it is. I do not think this reflects intent, since most of the code predates the results. I think it reflects something the dissertation itself argues: an error that confirms what you expect does not announce itself. That is why every numeric claim in Chapter 6 was mechanically re-checked against the analysis outputs before the conclusions were written, and why I would describe that verification pass as part of the method rather than as proofreading.

### "Three of your predictions failed. Doesn't that weaken the chapter?"

It is the reason to believe the ones that held. The lexical markedness test (§6.7), the comparison-class test (§6.4) and the kind-of-citation test (§6.5.3) all failed or partially failed, and all three are reported as failures with the disconfirmation criteria they were tested against stated in advance in the chapter (§6.3.9). A chapter in which every prediction was confirmed would be evidence that the tests were too easy, not that the thesis was right. What survives — a 5:1 to 13:1 citation asymmetry against near-identical self-citation baselines, two disjoint foundational archives, 107 shared authors out of nearly eleven thousand — survives having been genuinely exposed. *(Corrected 13 Aug 2026: an earlier version of this paragraph still carried the pre-correction figure of 45 shared authors and pointed to a superseded section number.)*

### "Your central claim rests on the self-citation baselines. Why should I trust them?"

Because they are the part of the analysis with the least room for manoeuvre. They are computed by the same code, on the same corpora, in the same units, as the cross-citation figures they contextualise. If the matching under-counts — and it does — it under-counts both. And the result they produce (491 against 430 per 10,000) is one I had no reason to want: had the two fields' citation cultures differed appreciably, the whole directional argument of §6.5 would have collapsed into an artefact, and I would have had to report that instead.


---

## Session 3 — 22 September 2026: the pre-submission rerun

**What was done, in plain language.** Every script in the package was run again, from the raw Web of Science files, on a clean machine, one after another, and everything it produced was compared with what the thesis had been written from. The comparison was mechanical: files compared byte by byte, figures compared pixel by pixel against the images embedded in the thesis document, every number in Chapter 6 and Appendix A read back out of the document and checked against the outputs.

**What held.** The three corpora load to the frozen counts. The four analysis scripts reproduce their outputs exactly (nineteen of twenty-one files identical; the two that differ are the community-detection partitions, D19). Every table reproduces. Fourteen of the twenty-two figures are the same image the scripts draw today; six more show the same values in a different typesetting.

**What did not, and what was done about it.** Two figures (6.3 and 6.16) had been drawn by a script that was lost, and the deposited replacement had two bugs; the replacement was repaired and the thesis now reports what it produces (D17). Table 6.1 and the rate in Figure 6.14 were correct but hand-typed; they are now derived from an output file (D18). The community detection behind the thematic maps depends on the library version; the deposited partition is kept, and the text now claims only what every version gives (D19). Four scripts were missing from the deposit (D20).

**How to check it yourself.** `python3 run_all.py` in the package folder, with the raw exports in `data/`, does the whole run and prints IDENTICAL or DIFFERS for every output. The `logs/` folder holds the printed output of every script from today's run. The Jupyter notebook `run_all.ipynb` does the same thing one cell at a time.

#!/usr/bin/env python3
"""
run_all.py — re-executes the whole bibliometric pipeline of the thesis, in
order, and reports whether every output matches the deposited ("frozen")
analysis outputs the thesis was written from.

Usage, from the folder that contains this file:

    python3 run_all.py            # full run (needs data/TS-J, data/AS-J, data/AS-T)
    python3 run_all.py --figures  # figure and table scripts that need no raw data

What it does
------------
1. Copies the deposited analysis_outputs/ to analysis_outputs_frozen/ once,
   so the rerun can be compared against them afterwards.
2. Runs the scripts below, each in its own process, printing their output
   to the screen AND to logs/<nn>_<script>.log.
3. Compares every JSON/CSV the analysis scripts wrote with the frozen copy
   and prints IDENTICAL / DIFFERS per file.  The only files expected to
   differ are the two Louvain partitions (NETWORK_RESULTS.json and
   THREE_CORPORA_THEMES.json): community detection is sensitive to the
   networkx version (see README, "Reproducibility of the thematic maps").
   With networkx pinned to the version in requirements.txt they replicate.

Run order (the same as README, "How to reproduce"):
    analysis_cross_corpus.py     -> analysis_outputs/00..08, ALL_RESULTS.json, t64/t66 CSVs
    analysis_refined.py          -> REFINED_RESULTS.json
    analysis_networks.py         -> NETWORK_RESULTS.json
    analysis_three_corpora.py    -> THREE_CORPORA_THEMES.json
    make_figures_palette.py      -> figs_out/palette/       (Figures 6.1, 6.7-6.13, 6.15)
    make_fig_a1_rpys.py          -> figs_out/palette/       (Figure A.1)
    make_labelled_maps.py        -> figs_out/thematic_maps/ (Figures 6.4, 6.5, 6.6)
    make_three_maps.py           -> figs_out/thematic_maps/ (three-panel variant, unused)
    make_chapter_figures.py      -> figs_out/               (Figures 1.1, 1.2, 5.1, 6.2, 6.3, 6.14, 6.16, 6.17)
    make_fig_a2_flow.py          -> figs_out/               (Figure A.2)
    make_tables.py               -> tables_out/             (Tables 6.1-6.5, A.2 as CSV)
    make_figures.py              -> figs_out/original_set/  (first figure set, superseded)
    make_descriptive_figures.py  -> figs_out/descriptive/   (descriptive set, superseded)
"""
import filecmp, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "scripts")
AO = os.path.join(HERE, "analysis_outputs")
FROZEN = os.path.join(HERE, "analysis_outputs_frozen")
LOGS = os.path.join(HERE, "logs")
DATA = os.path.join(HERE, "data")

ANALYSIS = ["analysis_cross_corpus.py", "analysis_refined.py",
            "analysis_networks.py", "analysis_three_corpora.py"]
FIGURES = ["make_figures_palette.py", "make_fig_a1_rpys.py",
           "make_labelled_maps.py", "make_three_maps.py",
           "make_chapter_figures.py", "make_fig_a2_flow.py", "make_tables.py",
           "make_figures.py", "make_descriptive_figures.py"]
# Scripts that read the raw exports as well as the outputs (the growth
# curves of Figure 6.1, the country counts, the descriptive set); skipped
# in --figures mode.  make_chapter_figures.py skips its own two
# data-dependent figures (6.3, 6.16) by itself when data/ is absent.
NEED_DATA = {"make_figures_palette.py", "make_descriptive_figures.py"}

figures_only = "--figures" in sys.argv
os.makedirs(LOGS, exist_ok=True)

if not figures_only:
    for sub in ("TS-J", "AS-J", "AS-T"):
        if not os.path.isdir(os.path.join(DATA, sub)):
            sys.exit(f"Raw exports not found: {os.path.join(DATA, sub)}\n"
                     "Place the Web of Science plain-text exports in data/TS-J, "
                     "data/AS-J and data/AS-T (see README, Data availability), "
                     "or run with --figures to redraw from the frozen outputs.")
    if not os.path.isdir(FROZEN):
        shutil.copytree(AO, FROZEN)
        print(f"Frozen copy of analysis_outputs/ kept in {FROZEN}\n")

PARTITIONS = ("NETWORK_RESULTS.json", "THREE_CORPORA_THEMES.json")


def keep_frozen_partitions():
    """After the analysis scripts have run: if a Louvain partition differs
    from the deposited one, keep the fresh result beside it (suffix
    _rerun_networkx<version>) and restore the deposited partition, which is
    the one every thematic-map figure and every sentence in the thesis
    describes.  Nothing else in analysis_outputs/ is touched."""
    import networkx
    for f in PARTITIONS:
        a, b = os.path.join(AO, f), os.path.join(FROZEN, f)
        if os.path.exists(a) and os.path.exists(b) and not filecmp.cmp(a, b, shallow=False):
            keep = a[:-5] + f"_rerun_networkx{networkx.__version__}.json"
            shutil.move(a, keep)
            shutil.copy(b, a)
            print(f"  {f}: partition differs from the deposited one under "
                  f"networkx {networkx.__version__}; fresh result kept as "
                  f"{os.path.basename(keep)}, deposited partition restored "
                  "for the figures (see README).")


todo = ([f for f in FIGURES if f not in NEED_DATA] if figures_only
        else ANALYSIS + FIGURES)
if figures_only:
    print("--figures: redrawing from the deposited outputs; "
          + ", ".join(sorted(NEED_DATA)) + " need the raw exports and are skipped.\n")
t0 = time.time()
for n, script in enumerate(todo, 1):
    if script == FIGURES[0] and not figures_only:
        keep_frozen_partitions()
    print("=" * 78)
    print(f"[{n:02d}/{len(todo)}]  python3 scripts/{script}")
    print("=" * 78, flush=True)
    log = os.path.join(LOGS, f"{n:02d}_{script[:-3]}.log")
    with open(log, "w") as fh:
        p = subprocess.Popen([sys.executable, script], cwd=SCRIPTS,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True)
        for line in p.stdout:
            print(line, end="")
            fh.write(line)
        p.wait()
    if p.returncode != 0:
        sys.exit(f"\n{script} failed (exit {p.returncode}); see {log}")
    print(flush=True)

if not figures_only:
    print("=" * 78)
    print("COMPARISON WITH THE FROZEN OUTPUTS")
    print("=" * 78)
    names = sorted(f for f in os.listdir(FROZEN)
                   if f.endswith((".json", ".csv")) and "rerun" not in f)
    for f in PARTITIONS:   # compare the fresh partition, not the restored copy
        fresh = [g for g in os.listdir(AO) if g.startswith(f[:-5] + "_rerun_")]
        if fresh:
            names[names.index(f)] = fresh[0]
    n_same = 0
    for f in names:
        base = f.split("_rerun_")[0] + ".json" if "_rerun_" in f else f
        a, b = os.path.join(AO, f), os.path.join(FROZEN, base)
        if os.path.exists(a) and filecmp.cmp(a, b, shallow=False):
            print(f"  IDENTICAL  {f}"); n_same += 1
        else:
            tag = ("(expected: Louvain partition is networkx-version-sensitive)"
                   if base in PARTITIONS else "")
            print(f"  DIFFERS    {f}  {tag}")
    print(f"\n{n_same} of {len(names)} output files identical to the frozen copy.")

print(f"\nDone in {time.time() - t0:.0f} s.  Logs in {LOGS}/")

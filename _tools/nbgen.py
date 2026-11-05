"""Generate Colab notebooks (student version with blanks, solution version) from one source."""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/tmp/shim")
import build  # noqa: F401  (importing registers all code blocks)
import qbuild
import content_ex
import content_p0
from modsrc import MODULE_ADD_PARSE, MODULE_ADD_REGION

SITE_CODE = {}
for tag, c in qbuild.COLLECTED_CODE:
    SITE_CODE[tag] = c

OUT = Path("nb")
BASE_URL = "https://atharva-bhagwat.github.io/assets/data/"


def site(tag, *fills):
    c = SITE_CODE[tag]
    for old, new in fills:
        assert old in c, (tag, old)
        c = c.replace(old, new, 1)
    return c


def blank(answer):
    return "\u27e6" + answer + "\u27e7"


def md_from_html(t):
    t = re.sub(r"</?(code)>", "`", t)
    t = re.sub(r"</?(strong)>", "**", t)
    t = re.sub(r"</?(em)>", "*", t)
    t = re.sub(r"<kbd>(.*?)</kbd>", r"`\1`", t)
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t)


def exercises(*ids, skip_run=()):
    """Exercise cells: markdown task, starter code, check code."""
    cells = []
    for e in content_ex.EXERCISES:
        if e["id"] not in ids:
            continue
        task = ""
        for h in content_ex.BY_STAGE[e["stage"]]:
            if f'data-ex="{e["id"]}"' in h:
                task = re.search(r'<div class="q-ex-task">(.*?)</div><div class="qcode', h, re.S).group(1)
        cells.append(("md", f"### Your turn: {e['title']}\n\n{md_from_html(task)}\n\nWhen the check cell prints `all checks passed`, tick *Done* on the guide page."))
        cells.append(("excode", e["starter"], e["solution"], e["id"]))
        if e["tests"]:
            cells.append(("code", e["tests"] + '\nprint("all checks passed")'))
    return cells


def render(cells, solution):
    out = []
    for c in cells:
        kind = c[0]
        if kind == "md":
            out.append(("markdown", c[1]))
        elif kind == "code":
            txt = c[1]
            txt = re.sub("\u27e6(.*?)\u27e7", (lambda m: m.group(1)) if solution else "____", txt)
            out.append(("code", txt))
        elif kind == "excode":
            out.append(("code", c[2] if solution else c[1]))
        elif kind == "raises":          # a cell that is *meant* to fail when run
            txt = re.sub("\u27e6(.*?)\u27e7", (lambda m: m.group(1)) if solution else "____", c[1])
            out.append(("code", txt + ("\n# RAISES" if False else "")))
    return out


def to_ipynb(rendered):
    cells = []
    for kind, text in rendered:
        src = text.split("\n")
        src = [l + "\n" for l in src[:-1]] + [src[-1]]
        if kind == "markdown":
            cells.append({"cell_type": "markdown", "metadata": {}, "source": src})
        else:
            cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": src})
    return {"cells": cells,
            "metadata": {"colab": {"provenance": []}, "kernelspec": {"display_name": "Python 3", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 0}


HOW = """## How this notebook works

* Run a cell with **Shift + Enter**. Run cells **in order, top to bottom**.
* A `____` is a **blank** for you to fill in. Replace it, then run the cell.
* Cells titled **Your turn** are small tasks. Write your code, then run the **check cell** under it. It prints `all checks passed` when you are right, and shows an error when you are not. Read the error: it is telling you something.
* Cells marked with a star are the ones that give the answer to a **puzzle on the guide page**. Type your answer there to earn the star.
* Stuck, or the notebook behaves strangely? **Runtime, Restart session and run all** is your friend.
* First, save your own copy: **File, Save a copy in Drive**."""

SETUP_DATA = 'BASE = "' + BASE_URL + '"\n'
HELPERS = ("import pandas as pd\n\n\n" + MODULE_ADD_PARSE.strip("\n") + "\n\n\n" + MODULE_ADD_REGION.strip("\n"))


def fresh_setup(extra=""):
    return [
        ("md", "## Setup\n\nRun this cell. It loads the PTEN table and the two helper functions you wrote earlier (`parse_hgvs`, `label_regions`), so this notebook works in a fresh session."),
        ("code", HELPERS),
        ("code", "import matplotlib.pyplot as plt\nimport seaborn as sns\nfrom pathlib import Path\n\n" + SETUP_DATA +
         'df = pd.read_csv(BASE + "pten-variant-abundance.csv")\nregions = pd.read_csv(BASE + "pten-region-annotations.csv")\n'
         'df = label_regions(parse_hgvs(df), regions)\nmiss = df[df["record_type"] == "missense"]\n\n'
         'sns.set_theme(style="whitegrid", context="notebook", palette="colorblind")\n'
         'TYPES = ["synonymous", "missense", "nonsense"]\ndata = df[df["record_type"].isin(TYPES)]\n\n'
         'FIGS = Path("figures")   # shows up in the Files panel (folder icon, left)\nFIGS.mkdir(exist_ok=True)\n' + extra),
    ]


NOTEBOOKS = {}

# =============================================================== NB0
NOTEBOOKS["00_project0_python_to_data"] = [
    ("md", "# Project 0: from Python basics to your first analysis\n\nAbout 60 minutes. You will climb a ladder: **value, list, dictionary, numpy array, pandas Series, pandas DataFrame**, using DNA sequences as the thing to analyse. Each rung is built from the one below, and by the end you will see how they connect.\n\n" + HOW),
    ("md", "## Rung 1: values\n\nOne thing at a time: a number, some text, a yes/no."),
    ("code", 'gene = "geneC"                 # text (a string)\nlength = ' + blank("30") + '                    # a whole number (an int)\nis_long = length > ' + blank("32") + '          # True or False (a bool)\nprint(gene, length, is_long)\ntype(length), type(gene), type(is_long)'),
    ("md", "**Predict before you run:** what will `is_long` be? Then run the cell and check yourself."),
    ("md", "## Rung 2: lists and dictionaries\n\nA **list** holds many values in order. A **dictionary** stores values under names."),
    ("code", 'names = ["geneA", "geneB", "geneC", "geneD"]\nlengths = [36, 36, 30, 33]\n\nprint(lengths[0], lengths[' + blank("-1") + '], len(lengths))     # first, last, how many\n\nlength_of = dict(zip(names, lengths))\nprint(length_of["' + blank("geneB") + '"])\n\nfor name in names:\n    print(name, length_of[name] // 3, "codons")'),
    ("md", "## Rung 3: libraries and numpy\n\nA **library** is a package of extra tools loaded with `import`. Why bother? Compare the loop with the numpy version."),
    ("code", site("p0_numpy", ("np.array(lengths)", "np." + blank("array") + "(lengths)"), ("arr > 31", "arr > " + blank("31")))),
    ("md", "Doing maths on a whole collection at once is called **vectorising**. It is the idea behind pandas.\n\n**Check yourself:** the line `arr[arr > 31]` keeps only the lengths above 31. Change the 31 and predict the result before running."),
    ("md", "## Rungs 4 and 5: from arrays to tables"),
    ("code", site("p0_pandas", ("pd.Series(lengths", "pd." + blank("Series") + "(lengths"))),
    ("md", "A DataFrame is a bundle of Series that share the same row labels. Selecting a column gives you a Series, and everything you did with arrays works on it."),
    ("md", "## A taste of Biopython\n\nDNA is text, but Biopython gives it biology-aware tools. Install it (Colab may already have it):"),
    ("code", "%pip install -q biopython"),
    ("code", site("p0_seq", ("dna.reverse_complement()", "dna." + blank("reverse_complement") + "()"), ("dna.translate(to_stop=True)", "dna.translate(to_stop=" + blank("True") + ")"))),
    ("md", "**Think:** the first `translate()` shows a `*` in the middle. What does a `*` mean here, and why is the second version shorter?"),
    ("md", "## FASTA files\n\nA **FASTA** file is a line starting with `>` naming a sequence, followed by its letters. Here the file is a text string so there is nothing to upload."),
    ("code", site("p0_fasta")),
    ("code", site("p0_records", ('"fasta"', '"' + blank("fasta") + '"'))),
    ("md", "## Closing the loop\n\n`records` is a **list** of **dictionaries**, exactly the shape a DataFrame wants."),
    ("code", site("p0_table", ("pd.DataFrame(records)", "pd." + blank("DataFrame") + "(records)"), ('seqs["gc"] > 0.5', 'seqs["gc"] > ' + blank("0.5")))),
    ("md", "## \u2b50 Puzzle cells\n\nUse your `seqs` table to answer the two questions on the guide page:\n\n1. The **GC fraction of `geneC`** (3 decimals).\n2. The **total** of the `protein_len` column."),
    ("code", 'print(round(seqs.loc[seqs["id"] == "' + blank("geneC") + '", "gc"].iloc[0], 3))\nprint(seqs["protein_len"].' + blank("sum") + "())"),
] + exercises("e12a", "e12b")

# =============================================================== NB1
NOTEBOOKS["01_python_kernel_and_errors"] = [
    ("md", "# Python basics, the kernel, and reading errors\n\nAbout 70 minutes. Covers **Stage 1** (cells, kernels, strings, loops) and **Stage 2** (errors are directions, not insults) of the guide.\n\n" + HOW),
    ("md", "## The kernel has a memory\n\nBehind this notebook is a **kernel**: a Python process that remembers every variable you have created. The notebook shows the code; the kernel holds the state. They can disagree.\n\n**Experiment.** Run the two cells below. Then change the first to `x = 100` but **do not run it**. Run the second again. Write your prediction first."),
    ("code", "x = 10"),
    ("code", "print(x * 2)"),
    ("md", "My prediction was: *(double-click to type)*\n\nWhat actually happened, and why?\n\n**The notebook rule:** a notebook is only trustworthy if it works from the top, in order, in a fresh kernel. Use **Runtime, Restart session and run all** before you believe any result."),
    ("md", "## Printing, types and strings"),
    ("code", 'n_reads = 1250\nprint(f"reads counted: {n_reads}")\nprint(f"as thousands: {n_reads / 1000:.2f}k")\n\ncount = 24\nscore = 3.49\nname = "p.Trp18Ter"\nis_low = score < 2\nvariants = ["a", "b"]\nprint(type(count), type(score), type(name), type(is_low), type(variants))'),
    ("md", "A **slice** `text[start:stop]` takes characters from `start` up to, but **not including**, `stop`. Counting starts at 0; negatives count from the end."),
    ("code", 'v = "p.Trp18Ter"\nprint(v[' + blank("2:5") + '])     # should print Trp\nprint(v[' + blank("5:-3") + '])    # should print 18\nprint(v[' + blank("-3:") + '])     # should print Ter\nprint(int(v[5:-3]) + 1)    # 19\nprint(v.startswith("p."), v.endswith("Ter"), v.upper(), v.replace("p.", ""))'),
    ("md", "## Conditions and loops"),
    ("code", 'score = 1.4\nif score < 0.5:\n    label = "low"\nelif score < ' + blank("1.0") + ':\n    label = "in between"\nelse:\n    label = "wild-type-like"\nprint(label)\n\nnames = ["WT", "p.Trp18Ter", "p.Leu25Pro"]\nfor i, name in enumerate(names):\n    print(i, name, len(name))\n\nlengths = [len(name) for name in names]\nlengths'),
    ("code", 'variants = ["p.Gly12Gly", "p.Trp18Ter", "p.Leu25Pro", "p.Val30Asp",\n            "p.Gln36Ter", "p.Ile40Asn", "p.Ser45Thr", "p.Gly46Arg"]'),
    ("md", "## \u2b50 Puzzle cells (guide, Stage 1)\n\n1. Add up the **positions** of all variants.\n2. Count how many are **synonymous, nonsense and missense** (in that order)."),
    ("code", 'total = 0\nfor v in variants:\n    total += int(v[' + blank("5:-3") + '])\nprint(total)\n\nsyn = non = mis = 0\nfor v in variants:\n    ref, alt = v[2:5], v[' + blank("-3:") + ']\n    if ref == alt:\n        syn += 1\n    elif alt == "Ter":\n        non += 1\n    else:\n        mis += 1\nprint(f"{syn},{non},{mis}")'),
] + exercises("e1a", "e1b", "e1c") + [
    ("md", "# Errors are directions, not insults\n\nRead a traceback **from the bottom**: the last line says what went wrong; the arrow points at your line; the middle is library internals you can ignore.\n\nRun each of the next cells. They fail on purpose. For each, write what the last line tells you."),
    ("raises", 'scores = {"score": 3.49}\nscores["Score"]              # KeyError: what is the key really called?'),
    ("raises", 'names = ["WT", "p.Trp18Ter"]\nnames[5]                     # IndexError'),
    ("raises", '"mean score: " + 2.718          # TypeError: what are the two types?'),
    ("md", "### Fix three bugs in one script\n\nThe errors will arrive one at a time, in this order: `SyntaxError`, `NameError`, `TypeError`. Fix each. What does it print at the end? (That is the answer to Stage 2's second puzzle.)"),
    ("raisesfix", 'scores = [3.45, 1.55, 2.18, 2.59, 3.82]\n\ntotal = 0\nfor s in scores\n    total = total + s\n\nmean = total / len(score)\nprint("mean score: " + mean)',
     'scores = [3.45, 1.55, 2.18, 2.59, 3.82]\n\ntotal = 0\nfor s in scores:\n    total = total + s\n\nmean = total / len(scores)\nprint(f"mean score: {mean:.3f}")'),
    ("md", "Some silent bugs do not raise an error at all. `assert` makes the computer complain on your behalf:"),
    ("code", 'assert len(variants) == 8, f"expected 8 variants, got {len(variants)}"\nprint("fine")'),
] + exercises("e2a", "e2b")

# =============================================================== NB2
NOTEBOOKS["02_pandas_and_functions"] = [
    ("md", "# pandas, scores and functions\n\nAbout 2 hours. Covers **Stage 3** (your first DataFrame), **Stage 4** (new columns, groups, pivots) and **Stage 5** (functions).\n\nThe toy table is an invented experiment: each *row* is one named item measured once, and `bin1_count` to `bin4_count` say how many reads fell into four brightness buckets, from the lowest signal (bin 1) to the highest (bin 4).\n\n" + HOW),
    ("md", "## Stage 3: load and look"),
    ("code", 'import pandas as pd\n\nBASE = "' + BASE_URL + '"\ndf = pd.read_csv(BASE + "toy_vampseq_bin_counts.csv")\ndf'),
    ("code", site("s3_look", ("df.head() ", "df." + blank("head") + "() "))),
    ("md", "### Pick rows by condition\n\nA comparison on a column gives a column of `True`/`False`. Using that to index keeps the `True` rows: a **boolean mask**. Combine conditions with `&`, `|`, `~` and wrap each in parentheses."),
    ("code", 'is_nonsense = df["variant_type"] == "nonsense"\ndf[is_nonsense]\n\ndf[(df["variant_type"] == "missense") & (df["replicate"] == ' + blank("1") + ')]'),
    ("code", site("s3_filter", ('"nonsense", "synonymous"', '"nonsense", "' + blank("synonymous") + '"'))),
    ("md", "**Try the trap.** Replace `&` with `and` in the first filter above and read the error. That is `ValueError: truth value of a Series is ambiguous`: Python's `and` wants one yes/no, but you gave it a whole column."),
    ("md", "## \u2b50 Stage 3 puzzle cells\n\n1. How many rows are `missense` **and** `replicate` 2?\n2. The **sum of all counts** in the four bin columns."),
    ("code", 'sub = df[(df["variant_type"] == "missense") & (df["replicate"] == ' + blank("2") + ')]\nprint(len(sub))\n\nbins = ["bin1_count", "bin2_count", "bin3_count", "bin4_count"]\nprint(df[bins].sum().' + blank("sum") + '())'),
] + exercises("e3a", "e3b", "e3c") + [
    ("md", "## Stage 4: make a score\n\nA **weighted average** of the bins: bin 1 has weight 1 ... bin 4 has weight 4. All reads in bin 1 gives 1, all in bin 4 gives 4.\n\n`score = (1*bin1 + 2*bin2 + 3*bin3 + 4*bin4) / total_reads`\n\n(This is *our* score for the toy table. The real PTEN table later has a different, normalised score. Do not confuse them.)"),
    ("code", site("s4_score", ("sum(axis=1)                   # axis=1", blank("sum") + "(axis=1)                   # axis=1") if False else ("sum(axis=1) / df", "sum(axis=1) / df"))),
    ("code", site("s4_group", ('"variant_type")["score"]', '"variant_type")["' + blank("score") + '"]'))),
    ("code", site("s4_pivot")),
    ("code", 'wide["diff"] = (wide[1] - wide[2]).abs()\nwide.sort_values("diff", ascending=False)'),
    ("md", "## \u2b50 Stage 4 puzzle cells\n\n1. Mean score of the `WT` rows (2 decimals).\n2. Which variant has the **largest disagreement** between replicates?"),
    ("code", 'print(df[df["variant"] == "WT"]["score"].mean().round(2))\nprint(wide["diff"].' + blank("idxmax") + '())'),
    ("md", "Look at that variant's `total_reads`. Should we trust its score? Write one sentence below.\n\n*(double-click to type)*"),
] + exercises("e4a", "e4b", "e4c") + [
    ("md", "## Stage 5: functions\n\nThe second time you copy a block of code, write a function. Anatomy: `def`, parameters (with defaults), a **docstring**, and `return`."),
    ("code", site("s5_func", ('out["total_reads"] = out[BINS].sum(axis=1)', 'out["total_reads"] = out[BINS].' + blank("sum") + "(axis=1)"))),
    ("code", site("s5_use")),
    ("code", site("s5_tests")),
    ("md", "## \u2b50 Stage 5 puzzle cells\n\n1. The score of `p.Ser45Thr` in replicate 1 (3 decimals).\n2. With `min_reads=50`, the mean score of all `missense` rows (3 decimals)."),
    ("code", 'scored = add_scores(df)\nrow = scored[(scored["variant"] == "p.Ser45Thr") & (scored["replicate"] == 1)]\nprint(round(row["score"].iloc[0], 3))\n\nstrict = add_scores(df, ' + blank("min_reads") + '=50)\nmis = strict[strict["variant_type"] == "missense"]\nprint(round(mis["score"].mean(), 3), mis["score"].count())'),
] + exercises("e5a", "e5b", "e5c")

# =============================================================== NB3
NOTEBOOKS["03_pten_data_audit_and_regions"] = [
    ("md", "# The PTEN data: audit, parse, summarise\n\nAbout 90 minutes. Covers **Stage 7** (audit) and **Stage 8** (regions) of the guide.\n\n" + HOW),
    ("md", "## What this dataset is about\n\n**PTEN** is a human protein that acts as a brake on cell growth signalling: an enzyme (a phosphatase) that dampens a growth pathway. When it is damaged, the brake weakens, and PTEN changes are linked to several cancers and inherited conditions. Many single-letter DNA changes swap one amino acid for another (**missense** variants), and for most nobody knows whether they matter.\n\nA *multiplexed assay of variant effect* makes thousands of variants and measures each. This table measures **abundance**: how much of each variant ends up in the cell. Each variant is tagged with a fluorescent marker, cells are sorted into four bins from dim to bright, and sequencing counts each variant per bin. An unstable variant is cleared away, so its cells look dim.\n\n**Abundance is not activity, and activity is not disease.** It tells you which changes destabilise the protein: one ingredient in judging whether a variant is harmful.\n\n### Two scores, one idea\n\nThe toy table's `score` was a weighted average of bins, 1 to 4. The PTEN table's `score` is published, **normalised** (reference about 1, broken proteins about 0). Same idea (one number for where a variant's cells land on the dim-to-bright spectrum), different procedure and scale. **Never compare raw numbers across the two tables.**"),
    ("code", 'import pandas as pd\n\nBASE = "' + BASE_URL + '"\ndf = pd.read_csv(BASE + "pten-variant-abundance.csv")\ndf.head()'),
    ("md", "Look at the columns. `hgvs_pro` is the variant name (reference amino acid, position, new amino acid), `score` is the abundance, `record_type` says what kind of variant it is, `expts` how many experiments contributed.\n\n**Reference points.** Nonsense variants cut the protein short, so they should look broken (near 0). Synonymous variants keep the amino acid, so they are *expected* to look like the reference (near 1). Check:"),
    ("code", site("s7_anchor", ('["score"].median()', '["' + blank("score") + '"].median()'))),
    ("md", "## The audit checklist"),
    ("code", site("s7_audit", ("df.shape ", "df." + blank("shape") + " "), ("df.isna().sum() ", "df." + blank("isna") + "().sum() "))),
    ("md", "## \u2b50 Stage 7 puzzle cells\n\nHow many rows does the table have? (Do the second one after parsing, below.)"),
    ("code", "print(len(df))"),
    ("md", "## Turn names into columns, one small step at a time"),
    ("code", site("s7_slice1")),
    ("code", site("s7_slice2", ("str[2:5]", "str[" + blank("2:5") + "]"))),
    ("md", "**Trap:** slicing works on most rows and quietly fails on some. Look at the synonymous names (`p.Asn12=`):"),
    ("code", site("s7_oddballs")),
    ("md", "The last three characters are `12=`, not an amino acid. Fix those rows, then pull the position out with a tiny regular expression: `\\d+` means *one or more digits*."),
    ("code", site("s7_pos", ('endswith("=")', 'endswith("' + blank("=") + '")'))),
    ("code", site("s7_asserts")),
    ("md", "## A function that does it all\n\nOne longer pattern with named parts does the three extractions at once. Optional reading: paste the pattern into regex101.com."),
    ("code", site("s7_module")),
    ("code", 'print(df["position"].nunique())            # second Stage 7 puzzle: distinct positions'),
    ("md", "### \u2b50 Interpretation (Stage 7, third star)\n\nThe guide asks three multiple-choice questions about comparing scores across tables, why nonsense/synonymous variants are reference points, and what a low abundance score does and does not mean. Think about them here first.\n\n*(double-click to write a few sentences)*"),
] + exercises("e7a", "e7b") + [
    ("md", "## Stage 8: group, merge and summarise\n\nPTEN has two folded parts, a **phosphatase domain** (the enzyme part) and a **C2 domain** (helps the protein attach to membranes), followed by a floppy **tail** with no fixed shape. A second table lists those stretches of the sequence."),
    ("code", site("s8_regions")),
    ("code", site("s8_label")),
    ("code", site("s8_module")),
    ("code", site("s8_miss")),
    ("code", site("s8_byregion", ('.agg(n="size"', '.agg(n="' + blank("size") + '"'))),
    ("md", "**Always put the n next to the mean.** A median from 12 variants and one from 1,500 are not equally trustworthy."),
    ("code", site("s8_bypos")),
    ("code", site("s8_merge")),
    ("md", "## \u2b50 Stage 8 puzzle cells\n\n1. Mean missense score in the `phosphatase_domain` (3 decimals).\n2. Which of the three regions has the **lowest median** missense score?"),
    ("code", 'sub = df[(df["record_type"] == "missense") & (df["region"] == "' + blank("phosphatase_domain") + '")]\nprint(round(sub["score"].mean(), 3), len(sub))\n\nby_region = miss.groupby("region")["score"].median()\nprint(by_region.drop(["other", "no_position"], errors="ignore").idxmin())'),
    ("md", "### \u2b50 Write your interpretation (Stage 8, third star)\n\nLook at your `by_region` table and write about four sentences: which region looks most and which least tolerant of changes; does that make biological sense for a folded domain versus a floppy tail; and how does the **number of variants in each region** affect how much you trust the comparison? Then submit it on the guide page.\n\n*(double-click to write)*"),
] + exercises("e8a", "e8b", "e8c")

# =============================================================== NB4
NOTEBOOKS["04_plots"] = [
    ("md", "# Plots: distributions, relationships and patterns\n\nAbout 100 minutes. Covers **Stage 9** (core) and **Stage 10** (optional).\n\n" + HOW),
] + fresh_setup() + [
    ("md", "## Two libraries, one mental model\n\nmatplotlib is the foundation: a **figure** is the canvas and an **axes** is one chart on it. seaborn sits on top and draws statistical plots from a DataFrame in one line. The pattern:\n\n```python\nfig, ax = plt.subplots(figsize=(6, 4))\nsns.<something>(data=..., x=..., y=..., ax=ax)\nax.set(xlabel=\"...\", ylabel=\"...\", title=\"...\")\n```\n\n**A plot without axis labels and units is a rumour.**"),
    ("md", "## Which plot answers which question?\n\n| Question | Plot |\n|---|---|\n| Shape of one variable | histogram |\n| Compare distributions without choosing bins | ECDF |\n| Compare group centres and spread | box plot |\n| Compare group shapes | violin |\n| Show every observation | strip plot |\n| How many of each category | count / bar plot |"),
    ("code", site("s9_hist", ("sns.histplot(", "sns." + blank("histplot") + "("))),
    ("code", site("s9_kde")),
    ("code", site("s9_ecdf")),
    ("code", site("s9_box", ("sns.boxplot(", "sns." + blank("boxplot") + "("))),
    ("code", site("s9_violin")),
    ("code", site("s9_strip")),
    ("code", site("s9_count")),
    ("md", "**Two groups hiding inside a box?** Look at the histogram and the box plot of the same missense scores and describe what each shows and hides."),
    ("code", site("s9_panel")),
    ("md", "## \u2b50 Stage 9 puzzle cells\n\n1. The **median** score of `nonsense` variants (2 decimals).\n2. How many missense variants have a score **strictly below 0.5**?"),
    ("code", 'print(round(df.loc[df["record_type"] == "' + blank("nonsense") + '", "score"].median(), 2))\nprint((miss["score"] < ' + blank("0.5") + ').sum())'),
] + exercises("e9a", "e9b") + [
    ("md", "# Stage 10 (optional): relationships and patterns"),
    ("code", site("s10_scatter")),
    ("code", site("s10_reg")),
    ("code", site("s10_hex")),
    ("code", site("s10_err")),
    ("md", "**Read the error.** If the error-bar cell ever says `'yerr' must not contain negative values`, matplotlib wants error *sizes*, not end points. That is why the code subtracts the score."),
    ("code", site("s10_track")),
    ("code", site("s10_heat", ('cmap="viridis"', 'cmap="' + blank("viridis") + '"'))),
    ("md", "## \u2b50 Stage 10 puzzle cells\n\n1. Which **new amino acid** (three letters) has the lowest mean missense score?\n2. In windows of 10 positions (`position // 10 * 10`), among windows with at least 30 missense variants, which window has the **lowest mean**?"),
    ("code", 'print(miss.groupby("alt")["score"].mean().' + blank("idxmin") + '())\n\nw = miss.assign(window=miss["position"] // 10 * 10).groupby("window")["score"].agg(n="size", mean="mean")\nprint(w[w["n"] >= 30]["mean"].idxmin())'),
] + exercises("e10a", "e10b", "e10c")

# =============================================================== NB5
NOTEBOOKS["05_sensitivity_and_conclusions"] = [
    ("md", "# Does your conclusion survive a different rule?\n\nAbout 60 minutes. Covers **Stage 11** of the guide.\n\nEvery analysis hides judgement calls: which rows to keep, how to score, where to cut. A trustworthy analysis shows how much the answer **depends** on them. Today's question: *should we trust variants that were measured in only a couple of experiments?*\n\n" + HOW),
] + fresh_setup() + [
    ("md", "## Turn the rule into a dial"),
    ("code", site("s11_func", ('keep &= df["expts"] >= min_expts', 'keep &= df["expts"] >= ' + blank("min_expts")))),
    ("md", "Now sweep the dial and look at the **whole curve**, not one cherry-picked value."),
    ("code", site("s11_sweep")),
    ("code", site("s11_plot")),
    ("md", "## \u2b50 Puzzle cells\n\n1. Keep rows with `expts` **at least 3**, across the whole table. How many remain?\n2. Mean missense score in the phosphatase domain **with** `min_expts=3` **minus** without it (3 decimals, keep the sign)."),
    ("code", 'print((df["expts"] >= ' + blank("3") + ').sum())\n\nafter = summarise(df, min_expts=3)["mean"]\nbefore = summarise(df)["mean"]\nprint(round(after - before, 3))'),
    ("md", "## \u2b50 Write the conclusion (third star)\n\nWrite four to six sentences as you would in a lab meeting:\n\n* the mean with and without the rule, and how many variants each rule keeps;\n* whether you think the conclusion is **robust** to this choice, and why;\n* the cost of keeping fewer variants;\n* one *other* analysis choice that could change the result.\n\nThen submit it on the guide page.\n\n*(double-click to write)*"),
] + exercises("e11a")


def main():
    for sub in ("student", "solutions"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
    for name, cells in NOTEBOOKS.items():
        for sub, sol in (("student", False), ("solutions", True)):
            norm = []
            for c in cells:
                if c[0] == "raises":
                    norm.append(("code", c[1]))
                elif c[0] == "raisesfix":
                    norm.append(("code", c[2] if sol else c[1]))
                else:
                    norm.append(c)
            nb = to_ipynb(render(norm, sol))
            (OUT / sub / f"{name}.ipynb").write_text(json.dumps(nb, indent=1), encoding="utf-8")
    print("wrote", len(NOTEBOOKS) * 2, "notebooks")


if __name__ == "__main__":
    main()

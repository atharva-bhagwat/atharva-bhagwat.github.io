from qbuild import *
from qbuild import answer_hash
from modsrc import MODULE_V1, MODULE_ADD_PARSE, MODULE_ADD_REGION, MODULE_FULL

STAGES_B = []


# =====================================================================
# Stage 6
# =====================================================================

DOWNLOAD = r'''
"""Download the data files into data/raw/. Safe to re-run."""
from pathlib import Path
from urllib.request import urlretrieve

BASE = "https://atharva-bhagwat.github.io/assets/data/"
FILES = {
    "toy_vampseq_bin_counts.csv": BASE + "toy_vampseq_bin_counts.csv",
    "pten-variant-abundance.csv": BASE + "pten-variant-abundance.csv",
    "pten-region-annotations.csv": BASE + "pten-region-annotations.csv",
}

out_dir = Path("data/raw")
out_dir.mkdir(parents=True, exist_ok=True)

for name, url in FILES.items():
    target = out_dir / name
    if target.exists():
        print(f"skip   {name} (already there)")
        continue
    urlretrieve(url, target)
    print(f"saved  {name}  ({target.stat().st_size:,} bytes)")
'''

CHECK_PROJECT = r'''
from pathlib import Path

expected = [
    "data/raw", "data/derived", "notebooks", "src",
    "results/figures", "README.md", "environment.yml",
]

found = 0
for item in expected:
    ok = Path(item).exists()
    found += ok
    print(("[x] " if ok else "[ ] ") + item)

print(f"project check: {found}/{len(expected)}")
'''

STAGES_B.append(stage(
    6, "Project Lodge", "a tidy home and a trustworthy download", 50,
    "You will lay out a project folder, download real data with a script, prove the file is intact, and move your function into a module any notebook can import.",
    [
        p("In Part 1 you worked in Colab notebooks, where files live in a temporary session. Real projects live in folders on a disk, so now you will give yours a proper home."),
        p("Analyses that survive are organised. Not fancy, just predictable. When someone (including you in six months) opens the folder, they should know where the raw data is, what is code, and what is output."),
        tree('''pandas-quest/
├── README.md              what this is and how to run it
├── environment.yml        the exact recipe for the conda environment
├── data/
│   ├── raw/               downloads exactly as received. Never edited.
│   └── derived/           tables your code produces
├── notebooks/             exploration, in numbered order
├── src/                   functions you reuse (plain .py files)
└── results/
    └── figures/           plots saved by code, not screenshots'''),
        callout("why", "Two rules that prevent most disasters",
                ul(["<strong>Raw data is read-only.</strong> Never open a raw file in Excel and save it; Excel silently rewrites numbers, dates and gene names. Your code reads from <code>data/raw</code> and writes to <code>data/derived</code>.",
                    "<strong>Everything in <code>results/</code> can be deleted and regenerated</strong> by running your code. If it cannot, you have a hidden manual step."])),
        h3("1. Build the skeleton"),
        p("From your project folder, in the terminal where <code>(pandas-quest)</code> is active (this one-liner works on every operating system):"),
        code('python -c "from pathlib import Path; [Path(p).mkdir(parents=True, exist_ok=True) for p in [\'data/raw\', \'data/derived\', \'notebooks\', \'src\', \'results/figures\']]"',
             "bash", "terminal"),
        h3("2. Get the data"),
        p("Three files power the rest of the guide. You can click to download them by hand, but the script below is better because it is a record of where each file came from."),
        table(["File", "What it is"], [
            ['<a href="/assets/data/toy_vampseq_bin_counts.csv" download>toy_vampseq_bin_counts.csv</a>', "Invented table of read counts, used in the pandas stages (3 to 5)."],
            ['<a href="/assets/data/pten-variant-abundance.csv" download>pten-variant-abundance.csv</a>', "The real table: one row per protein variant, used from Stage 7."],
            ['<a href="/assets/data/pten-region-annotations.csv" download>pten-region-annotations.csv</a>', "Three named stretches of the sequence, used in the region and plotting stages."],
        ]),
        p("Save this as <code>download_data.py</code> in the project root and run <code>python download_data.py</code>."),
        code(DOWNLOAD, "python", "download_data.py", test="s6_download_syntax"),
        callout("note", "Working directory",
                p("<code>Path(\"data/raw\")</code> is a <em>relative</em> path: it means \"from wherever Python was started\". That is why you run the script from the project root. "
                  "When something cannot find a file, print <code>Path.cwd()</code> before anything else. In a VS Code notebook, the working directory is the notebook's own folder, <code>notebooks/</code>.")),
        h3("3. Check the file is the file"),
        p("A truncated or edited download looks fine until it quietly ruins your results. A <strong>SHA-256 hash</strong> is a fingerprint of a file's exact bytes; change one character and it changes completely. "
          'The guide knows the fingerprint of the original file. Compute yours:'),
        code('import hashlib\nfrom pathlib import Path\n\npath = Path("data/raw/pten-variant-abundance.csv")\nprint(hashlib.sha256(path.read_bytes()).hexdigest())',
             "python", "any cell or script", test="s6_hash_syntax"),
        h3("4. Move your function into <code>src/</code>"),
        p("Create <code>src/vampseq_tools.py</code> and paste in the three functions you wrote in Part 1: <code>add_scores</code> (Stage 5), <code>parse_hgvs</code> (Stage 7) and <code>label_regions</code> (Stage 8). The file looks like this:"),
        code(MODULE_FULL, "python", "src/vampseq_tools.py", test="s6_module"),
        p("Now any notebook can import it. Put this in the first cell of each notebook:"),
        code('''import sys
from pathlib import Path

# Make the project's src/ folder importable, wherever the notebook runs from
ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(ROOT / "src"))
RAW = ROOT / "data" / "raw"

%load_ext autoreload
%autoreload 2

import pandas as pd
from vampseq_tools import add_scores, parse_hgvs, label_regions''', "python", "first cell of every notebook"),
        ul([
            "<strong>Why the <code>sys.path</code> line?</strong> Python only imports from certain folders. This adds yours.",
            "<strong>Why <code>%autoreload 2</code>?</strong> The kernel remembers imported code (Stage 1!). Without autoreload, editing <code>vampseq_tools.py</code> changes nothing until you restart the kernel. With it, edits are picked up on the next run.",
        ]),
        callout("trap", "<code>ModuleNotFoundError: No module named 'vampseq_tools'</code>",
                p("Python could not find your file. Is it inside <code>src/</code>? Is the name spelled the same? Did you run the cell with the <code>sys.path</code> line first? "
                  "Print <code>sys.path[0]</code> and look inside that folder.")),
        h3("5. Write it down: README and environment"),
        code('''# PTEN variant abundance, a pandas practice project

Explores a published dataset of protein variant abundance scores.

## Run it
    conda env create -f environment.yml
    conda activate pandas-quest
    python download_data.py
    python src/make_figures.py

## Layout
data/raw (never edited), data/derived, notebooks/, src/, results/figures/

## Decisions
- Score = weighted average of the four bins (weights 1-4).
- Variants with fewer than 50 reads are excluded from scores.''', "markdown", "README.md"),
        p("Freeze the environment so someone else (or a new laptop) can rebuild it:"),
        code("conda env export --from-history > environment.yml", "bash", "terminal"),
        p("<code>--from-history</code> records only the packages you asked for, not every dependency, so the file stays portable between operating systems. "
          "To rebuild: <code>conda env create -f environment.yml</code>."),
        h3("6. Optional but wise: version control"),
        code('git init\nprintf "data/raw/\\n__pycache__/\\n.ipynb_checkpoints/\\n.DS_Store\\n" > .gitignore\ngit add .\ngit commit -m "Project skeleton"',
             "bash", "terminal"),
        p("Commit whenever something works. A commit is a save point you can always return to, and the message is a one-line diary entry. "
          "(On Windows, create <code>.gitignore</code> in VS Code and paste those four lines instead.)"),
        h3("7. Check your skeleton"),
        p("Save this as <code>check_project.py</code> in the project root, and run it with <code>python check_project.py</code>:"),
        code(CHECK_PROJECT, "python", "check_project.py", test="s6_check_project"),
    ],
    [
        puzzle("s6p1", 1,
               p("Compute the SHA-256 of <code>data/raw/pten-variant-abundance.csv</code> and paste the 64 characters. "
                 "The checker compares it with the fingerprint of the original file. If it does not match, the file is not the one published, so download again before going further."),
               kind="paste", placeholder="64 hexadecimal characters",
               hint="A mismatch usually means a partial download (check the file size: it should be roughly a megabyte), or the file was opened and re-saved in a spreadsheet program. Delete it and run <code>download_data.py</code> again.",
               solution='import hashlib\nfrom pathlib import Path\n\nprint(hashlib.sha256(Path("data/raw/pten-variant-abundance.csv").read_bytes()).hexdigest())'),
        puzzle("s6p2", 2,
               p("Paste the output of <code>check_project.py</code>. It should end with <code>project check: 7/7</code>."),
               kind="paste", placeholder="[x] data/raw\n[x] data/derived\n...\nproject check: 7/7",
               hint="Any line starting with <code>[ ]</code> is missing. Create it in the VS Code Explorer (right-click, New Folder or New File), or re-run the skeleton command."),
    ],
))

# =====================================================================
# Stage 7
# =====================================================================

S7_ANS = {i: answer_hash(f"s7p3-{i}", l) for i, l in enumerate("cab")}

STAGES_B.append(stage(
    7, "Audit Pass", "trust, but verify", 60,
    "You have been handed a table with thousands of rows. Before you plot anything you will learn what it measures, find out what is in it and what is missing, and check that the labels mean what they say.",
    [
        p("Open notebook 3 with the Colab button above. Real data arrives with quirks, so the habit that separates careful analysts from unlucky ones is a <strong>data audit</strong>: "
          "a short, boring, systematic look at the table before any conclusions."),
        h3("What this dataset is about"),
        p("<strong>PTEN</strong> is a human protein that acts as a brake on cell growth signalling. It is an enzyme (a phosphatase) that removes a phosphate group from a signalling lipid, which dampens a pathway that tells cells to grow. "
          "When PTEN is damaged, the brake weakens, and changes in the PTEN gene are linked to several cancers and to inherited conditions. "
          "Geneticists keep finding single-letter changes in the gene. Many swap one amino acid in the protein for another (a <strong>missense</strong> variant), and for most of them nobody knows whether the change matters."),
        p("A <strong>multiplexed assay of variant effect</strong> attacks that gap by making thousands of variants at once and measuring each one. "
          "This table comes from an experiment that measured <strong>abundance</strong>: how much of each PTEN variant ends up in the cell. "
          "Each variant is tagged with a fluorescent marker and put into cells. Cells are then sorted into four bins from dim to bright and sequenced, "
          "so each variant gets a count of reads per bin. That is exactly the shape of the toy table from Stage 3, only with about four thousand variants. "
          "A change that makes the protein unstable gets cleared away by the cell, so its cells look dim and its reads pile up in the low bins."),
        callout("why", "Abundance is not activity, and activity is not disease",
                p("A variant can be abundant but inactive, or scarce and still partly working. Abundance data tells you which changes destabilise the protein, "
                  "which is one useful ingredient when judging whether a variant is harmful. It does not tell you the final answer.")),
        h3("Two scores, one idea"),
        p("Be careful: the toy table and this table both have a column called <code>score</code>, but they are <strong>not the same measurement</strong>."),
        table(["", "Toy table (Stage 4)", "PTEN table (this stage)"], [
            ["How it was made", "You computed it: a weighted average of the four bins, weights 1 to 4.", "Published by the researchers, from their own analysis of the sorted-cell data."],
            ["Typical range", "1 to 4. Higher means brighter cells.", "Roughly 0 to 1 (a few outside). It has been rescaled."],
            ["Anchors", "None. 4 means all reads in the brightest bin.", "The reference protein is set to 1. Broken, cut-short proteins sit near 0."],
        ]),
        p("They share an idea: summarise <em>where along the dim-to-bright spectrum a variant's cells land</em> as one number. But the procedures and scales differ, "
          "so never compare raw numbers across the two tables. Compare patterns <em>within</em> a table, measured against that table's own reference points. You will check this yourself in a moment."),
        h3("Load it"),
        code('import pandas as pd\n\nBASE = "https://atharva-bhagwat.github.io/assets/data/"\ndf = pd.read_csv(BASE + "pten-variant-abundance.csv")\ndf.head()', "python", "cell", test="s7_load"),
        p("What the columns hold, in plain terms (<code>score</code> is the one that matters most):"),
        table(["Column", "Meaning"], [
            ["<code>hgvs_pro</code>", "Variant name such as <code>p.Asn12Ile</code>: reference amino acid, position, new amino acid. This is the identity of a row."],
            ["<code>score</code>", "The measured abundance, already normalised: about 1 means \"like the unchanged reference\", about 0 means \"like a broken protein\"."],
            ["<code>sd</code>, <code>se</code>, <code>lower_ci</code>, <code>upper_ci</code>", "Spread and uncertainty of that measurement."],
            ["<code>expts</code>", "How many experiments contributed to the score."],
            ["<code>record_type</code>", "<code>missense</code> (one amino acid swapped), <code>synonymous</code> (the DNA changed but the amino acid did not), <code>nonsense</code> (a stop signal, so the protein is cut short), <code>wild_type</code> (the reference itself)."],
            ["<code>abundance_class</code>, <code>abundance_class_label</code>", "A binned version of the score, as a number and as a text label."],
            ["<code>accession</code>, <code>snv</code>", "Database identifier, and a flag for whether one DNA change can produce the variant."],
        ]),
        callout("note", "Why look at synonymous and nonsense variants first?",
                p("They are your reference points. Nonsense variants cut the protein short, so they should look broken (scores near 0). "
                  "Synonymous variants keep the amino acid sequence, so they are expected to look like the reference (near 1). "
                  "\"Expected\" is the important word: a silent DNA change can occasionally matter for other reasons, which is why you check rather than assume.")),
        code('df.groupby("record_type")["score"].median()', "python", "cell: do the anchors look right?", test="s7_anchor"),
        h3("The audit checklist"),
        code('df.shape                                    # rows, columns\ndf.dtypes                                   # anything numeric stored as text?\ndf.isna().sum()                             # missing values per column\ndf["hgvs_pro"].is_unique                    # one row per variant?\ndf.duplicated(subset="hgvs_pro").sum()      # how many repeats\ndf["record_type"].value_counts()            # counts per type\ndf["abundance_class_label"].value_counts(dropna=False)\npd.crosstab(df["abundance_class"], df["abundance_class_label"])   # do number and label agree?\ndf[["score", "sd", "se", "expts"]].describe()',
             "python", "cell", test="s7_audit"),
        callout("tip", "Compare with what you were told",
                p("If a collaborator tells you how many rows and how many of each record type to expect, check that your table agrees. "
                  "If a number differs, that is not a nuisance, it is a finding. Write down why.")),
        h3("Turn names into columns, one small step at a time"),
        p("A variant name packs three facts into one string. To summarise by position later, you need them as separate columns. You already know the first tool: slicing."),
        code('name = "p.Asn12Ile"\nname[2:5], name[-3:]      # reference and new amino acid', "python", "cell", test="s7_slice1"),
        p("The same slicing works on a whole column through <code>.str</code>:"),
        code('df["ref"] = df["hgvs_pro"].str[2:5]\ndf["alt"] = df["hgvs_pro"].str[-3:]\ndf[["hgvs_pro", "ref", "alt"]].sample(5, random_state=1)',
             "python", "cell", test="s7_slice2"),
        callout("trap", "A method that works on most rows is the dangerous kind",
                p("Look at a synonymous name such as <code>p.Asn12=</code>. The last three characters are <code>12=</code>, not an amino acid. Check the odd ones on purpose:")
                + code('df[df["hgvs_pro"].str.endswith("=")][["hgvs_pro", "alt"]].head(3)', "python", "cell", test="s7_oddballs")),
        p("Fix them with a filter you already know, and then pull out the position, which is the digits in the middle. "
          "The <code>\\d+</code> below is a tiny <strong>regular expression</strong>, a pattern language for text: <code>\\d</code> means a digit and <code>+</code> means one or more."),
        code('df.loc[df["hgvs_pro"].str.endswith("="), "alt"] = "="\n\ndf["position"] = pd.to_numeric(df["hgvs_pro"].str.extract(r"(\\d+)")[0]).astype("Int64")\ndf[df["position"].isna()]       # which rows have no position, and is that expected?',
             "python", "cell", test="s7_pos"),
        p("The <code>Int64</code> type (capital I) is a whole number that can also be missing. The rows without a position, such as the wild-type reference row, are your cue to look at them, not ignore them."),
        p("Last, test that the labels agree with the contents. If they do not, you have found a problem worth knowing about now:"),
        code('assert (df.loc[df["record_type"] == "nonsense", "alt"] == "Ter").all()\nassert (df.loc[df["record_type"] == "synonymous", "alt"] == "=").all()\nassert df.loc[df["record_type"] == "missense", "alt"].notna().all()\nprint("labels and names agree")',
             "python", "cell", test="s7_asserts"),
        h3("Package the steps as a function"),
        p("You will use this parsing in every later notebook, so wrap the steps in a function (in Part 2 it moves into a file you can import). "
          "This version uses one longer pattern with named parts that does the three extractions at once. It is optional reading: "
          'paste it into <a href="https://regex101.com/" target="_blank" rel="noopener">regex101.com</a> with a few variant names to see each piece light up.'),
        code(MODULE_ADD_PARSE, "python", "function: parse_hgvs", test="s7_module"),
        p("Then in a notebook: <code>df = parse_hgvs(df)</code>. The notebooks for the next stages include this function in their first cell."),
    ],
    [
        puzzle("s7p1", 1,
               p("How many <strong>rows</strong> does the table have (not counting the header)?"),
               kind="number", placeholder="a whole number",
               hint="<code>df.shape</code> gives <code>(rows, columns)</code>. <code>len(df)</code> gives the rows directly.",
               solution='print(len(df))'),
        puzzle("s7p2", 2,
               p("After parsing <code>hgvs_pro</code>, how many <strong>distinct positions</strong> appear in the table? Ignore rows where no position could be read."),
               kind="number", placeholder="a whole number",
               hint="<code>df[\"position\"].nunique()</code> already skips missing values.",
               solution='print(df["position"].nunique())', test="s7p2"),
        puzzle("s7p3", 3,
               p("Interpretation time. Pick the best answer for each."),
               kind="choices",
               choices=[
                   ("A learner says: \"a PTEN variant with score 0.9 is <em>lower</em> than a toy variant scoring 3.4, so the PTEN variant is worse.\" What is wrong?",
                    ["Nothing; 0.9 is lower than 3.4.", "PTEN scores are wrong because they are below 1.", "The two scores come from different procedures and scales, so raw numbers cannot be compared across tables. Compare against each table's own reference points."]),
                   ("Why do analysts look at nonsense and synonymous variants before anything else?",
                    ["They give reference points: nonsense should look broken and synonymous should look like the reference, so a surprise means something may be wrong.", "They are the most common variants.", "They are the only variants with scores."]),
                   ("A missense variant has a very low abundance score. What can you conclude?",
                    ["It causes disease.", "The protein with this change is probably present at lower levels in the cell. Whether it affects function or health needs other evidence.", "It has no effect on PTEN."]),
               ],
               spec={"kind": "choices", "hs": [S7_ANS[i] for i in range(3)]},
               hint="Question 1: ask what \"score\" means in each table. Question 3: abundance and activity are different things."),
    ],
))

# =====================================================================
# Stage 8
# =====================================================================

STAGES_B.append(stage(
    8, "Region Rapids", "group, merge and summarise", 50,
    "You will attach a second table to the first, summarise by position and by region, and learn why every summary needs a count next to it.",
    [
        p("Stage 7 gave you one row per variant. Questions usually live at a coarser level: <em>per position</em>, <em>per region</em>, <em>per category</em>. "
          "PTEN has two folded parts, a <strong>phosphatase domain</strong> (the enzyme part) and a <strong>C2 domain</strong> (which helps the protein attach to membranes), followed by a floppy <strong>tail</strong> with no fixed shape. "
          "A second table lists those stretches of the sequence with start and end positions:"),
        code('regions = pd.read_csv(BASE + "pten-region-annotations.csv")\nregions',
             "python", "cell", test="s8_regions"),
        h3("Label each row with its region"),
        p("Write a small function that answers \"which region contains this position?\" for one position, then apply it to the whole column with <code>.map</code>:"),
        code('def find_region(position, regions):\n    if pd.isna(position):\n        return "no_position"\n    for r in regions.itertuples():\n        if r.start <= position <= r.end:\n            return r.region\n    return "other"\n\ndf["region"] = df["position"].map(lambda pos: find_region(pos, regions))\ndf["region"].value_counts()',
             "python", "cell", test="s8_label"),
        callout("trap", "The missing-value guard is not optional",
                p("Remove the <code>pd.isna</code> check and the function dies with <code>TypeError: boolean value of NA is ambiguous</code> on the first row without a position. "
                  "Missing values do not behave like numbers; they need an explicit decision.")),
        p("That logic is reusable, so package it as a function too, next to <code>parse_hgvs</code>:"),
        code(MODULE_ADD_REGION, "python", "function: label_regions", test="s8_module"),
        h3("Focus the question"),
        p("Different record types answer different questions. For \"how do single-letter changes affect abundance?\" keep only <code>missense</code> rows and give that table a name:"),
        code('miss = df[df["record_type"] == "missense"]\nlen(miss)', "python", "cell", test="s8_miss"),
        h3("Summarise by region, with counts"),
        code('by_region = (\n    miss.groupby("region")["score"]\n        .agg(n="size", mean="mean", median="median")\n        .round(3)\n)\nby_region',
             "python", "cell", test="s8_byregion"),
        callout("why", "Always put the n next to the mean",
                p("A mean of 3 variants and a mean of 3,000 look identical in a table. The count tells the reader how much weight to give each number. "
                  "Median versus mean is worth looking at too: when they differ a lot, the distribution is lopsided, and a single number is hiding something.")),
        h3("Summarise by position, then merge back"),
        code('by_position = (\n    miss.groupby("position")["score"]\n        .agg(n_subs="size", mean_score="mean")\n        .reset_index()\n)\nby_position.sort_values("mean_score").head(10)       # the most affected positions',
             "python", "cell", test="s8_bypos"),
        code('merged = df.merge(by_position, on="position", how="left")   # adds n_subs and mean_score to every row\nassert len(merged) == len(df), "a merge changed the number of rows!"\nmerged[["hgvs_pro", "score", "n_subs", "mean_score"]].head()',
             "python", "cell", test="s8_merge"),
        p("<code>how=\"left\"</code> keeps every row of the left table and fills blanks where there is no match. "
          "The <code>assert</code> after a merge is cheap insurance: if the key is not unique on the right side, a merge silently multiplies rows."),
        callout("note", "Choosing a merge type",
                ul(["<code>left</code>: keep everything from the table on the left (most common).",
                    "<code>inner</code>: keep only rows that match on both sides.",
                    "<code>outer</code>: keep everything from both.",
                    "<code>validate=\"many_to_one\"</code> makes pandas raise an error if your assumption about keys is wrong."])),
        h3("Read the table like a scientist"),
        p("Numbers become findings only when you ask what they mean. Before you answer the last puzzle of this stage, look at your <code>by_region</code> table and ask three questions:"),
        ol([
            "<strong>How big is each group?</strong> A median from 12 variants and one from 1,500 are not equally trustworthy.",
            "<strong>Does the pattern make biological sense?</strong> Folded domains need an exact shape, so changing their amino acids often destabilises them. A floppy tail has no shape to lose.",
            "<strong>What can abundance not tell you?</strong> A region can tolerate changes in abundance and still be essential for function.",
        ]),
    ],
    [
        puzzle("s8p1", 1,
               p("Using only <code>missense</code> rows, what is the mean <code>score</code> of variants in the <code>phosphatase_domain</code> region, to 3 decimal places? "
                 "(Regions include both their start and end positions.)"),
               kind="number", placeholder="3 decimal places",
               hint="Parse positions, label regions, filter on <code>record_type == \"missense\"</code> and <code>region == \"phosphatase_domain\"</code>, then <code>.mean()</code> of <code>score</code>. "
                    "If your number includes nonsense or synonymous rows, it will be off.",
               solution='sub = df[(df["record_type"] == "missense") & (df["region"] == "phosphatase_domain")]\nprint(round(sub["score"].mean(), 3), len(sub))', test="s8p1"),
        puzzle("s8p2", 2,
               p("Among the three annotated regions (<code>phosphatase_domain</code>, <code>c2_domain</code>, <code>disordered_tail</code>), which has the <strong>lowest median</strong> missense <code>score</code>? "
                 "Write the region name."),
               kind="text", placeholder="region_name",
               hint="The <code>by_region</code> table above has the medians. Ignore the rows named <code>other</code> and <code>no_position</code>, then look at the smallest median.",
               solution='by_region = miss.groupby("region")["score"].median()\nprint(by_region.drop(["other", "no_position"], errors="ignore").idxmin())', test="s8p2"),
        puzzle("s8p3", 3,
               p("<strong>Write your interpretation</strong> (about four sentences). Using your own <code>by_region</code> table, say: which region looks most and which least tolerant of changes, "
                 "whether that makes biological sense for a folded domain versus a floppy tail, and how the <strong>number of variants in each region</strong> affects how much you trust the comparison."),
               kind="reflect", minwords=45, placeholder="The ... has the lowest median (value, n = ...), while the ...",
               hint="Start from the numbers: name the regions, quote a median and an n for each. Then give one biological reason and one reason to be cautious.",
               model='<h4>A model answer (use your own numbers)</h4>'
                     '<p>\"The ___ has the lowest median missense score (___, n = ___) and the ___ the highest (___, n = ___). '
                     'That fits the idea that folded domains must keep a precise shape, so many amino acid swaps there destabilise the protein, '
                     'while a disordered tail has no fixed structure to lose and is more forgiving. '
                     'The regions have very different numbers of variants, so a median from a small group is less reliable and I would not over-read a small gap. '
                     'Also, abundance is only one property: a region that keeps the protein stable might still matter for activity.\"</p>'
                     '<h4>Did you cover</h4><ul><li>Named the extreme regions with a number and an n?</li><li>Gave a biological reason and judged whether it fits?</li>'
                     '<li>Said how group size changes your confidence?</li><li>Noted what abundance cannot tell you?</li></ul>'),
    ],
))

# =====================================================================
# Stage 9
# =====================================================================
STAGES_B.append(stage(
    9, "Histogram Meadow", "plots for distributions", 60,
    "Seven plots for the question every experimentalist asks first: what does my data look like, and do my groups differ? You will learn when each one is the right choice.",
    [
        p("Open notebook 4 in Colab (button above). Its first cells reload the data and define the helper functions from earlier stages, so it works in a fresh session. The setup looks like this:"),
        code('import pandas as pd\nfrom pathlib import Path\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nBASE = "https://atharva-bhagwat.github.io/assets/data/"\ndf = pd.read_csv(BASE + "pten-variant-abundance.csv")\nregions = pd.read_csv(BASE + "pten-region-annotations.csv")\ndf = label_regions(parse_hgvs(df), regions)    # the two helpers from Stages 6 and 7\n\nsns.set_theme(style="whitegrid", context="notebook", palette="colorblind")\nTYPES = ["synonymous", "missense", "nonsense"]\ndata = df[df["record_type"].isin(TYPES)]\n\nFIGS = Path("figures")          # in Colab: the Files panel (folder icon) shows it\nFIGS.mkdir(exist_ok=True)',
             "python", "first cells", test="s9_setup"),
        h3("Two libraries, one mental model"),
        p('<a href="https://matplotlib.org/stable/index.html" target="_blank" rel="noopener">matplotlib</a> is the foundation: a <strong>figure</strong> is the canvas and an <strong>axes</strong> is one chart on it. '
          '<a href="https://seaborn.pydata.org/" target="_blank" rel="noopener">seaborn</a> sits on top and draws statistical plots from a DataFrame in one line. '
          "The pattern you will repeat all stage:"),
        code('fig, ax = plt.subplots(figsize=(6, 4))        # make a canvas with one chart\nsns.<something>(data=..., x=..., y=..., ax=ax)    # draw onto that chart\nax.set(xlabel="...", ylabel="...", title="...")   # label it\n',
             "python", "the pattern"),
        callout("tip", "Name your axes",
                p("A plot without axis labels and units is a rumour. Add <code>xlabel</code> and <code>ylabel</code> every time, even in exploration. It also forces you to know what the plot says.")),
        h3("Which plot answers which question?"),
        table(["Question", "Plot", "Watch out for"], [
            ["What is the shape of one variable?", "<strong>Histogram</strong>", "The number of bins changes the picture. Try 20, 40 and 80."],
            ["Same, smoothed, for several groups", "<strong>KDE</strong> (density)", "Smoothing can invent bumps and spill past the real range."],
            ["Compare distributions without choosing bins", "<strong>ECDF</strong>", "Less familiar, but the most honest. Read it as \"what fraction is below this value\"."],
            ["Compare group centres and spread", "<strong>Box plot</strong>", "Hides the shape. Two humps look like one box."],
            ["Compare group shapes", "<strong>Violin</strong>", "Needs plenty of points per group."],
            ["Show every observation", "<strong>Strip plot</strong>", "Overlapping points. Use <code>alpha</code> and a small <code>size</code>."],
            ["How many of each category?", "<strong>Count / bar plot</strong>", "Start bars at zero. Always."],
        ]),
        h3("The gallery"),
        p("Each cell below is a complete plot. Run them, change one thing, run again."),
        code('fig, ax = plt.subplots(figsize=(6, 4))\nsns.histplot(data=data[data["record_type"] == "missense"], x="score", bins=40, ax=ax)\nax.set(xlabel="abundance score", ylabel="number of variants", title="Histogram: missense variants")',
             "python", "1. histogram", test="s9_hist"),
        code('fig, ax = plt.subplots(figsize=(6, 4))\nsns.kdeplot(data=data, x="score", hue="record_type", hue_order=TYPES,\n            common_norm=False, fill=True, alpha=0.3, ax=ax)\nax.set(xlabel="abundance score", title="KDE: one curve per record type")',
             "python", "2. density (KDE)", test="s9_kde"),
        code('fig, ax = plt.subplots(figsize=(6, 4))\nsns.ecdfplot(data=data, x="score", hue="record_type", hue_order=TYPES, ax=ax)\nax.set(xlabel="abundance score", ylabel="fraction of variants at or below", title="ECDF")',
             "python", "3. ECDF", test="s9_ecdf"),
        code('fig, ax = plt.subplots(figsize=(6, 4))\nsns.boxplot(data=data, x="record_type", y="score", order=TYPES, ax=ax)\nax.set(xlabel="", ylabel="abundance score", title="Box plot")',
             "python", "4. box plot", test="s9_box"),
        code('fig, ax = plt.subplots(figsize=(6, 4))\nsns.violinplot(data=data, x="record_type", y="score", order=TYPES, inner="quart", cut=0, ax=ax)\nax.set(xlabel="", ylabel="abundance score", title="Violin plot")',
             "python", "5. violin", test="s9_violin"),
        code('fig, ax = plt.subplots(figsize=(6, 4))\nsns.stripplot(data=data, x="record_type", y="score", order=TYPES, size=2, alpha=0.4, jitter=0.25, ax=ax)\nax.set(xlabel="", ylabel="abundance score", title="Strip plot: every variant is a dot")',
             "python", "6. strip plot", test="s9_strip"),
        code('fig, ax = plt.subplots(figsize=(6, 4))\nsns.countplot(data=data, x="record_type", order=TYPES, ax=ax)\nax.set(xlabel="", ylabel="number of variants", title="Count plot")',
             "python", "7. count plot", test="s9_count"),
        h3("Assemble a multi-panel figure and save it"),
        code('fig, axes = plt.subplots(1, 3, figsize=(14, 4))\n\nsns.histplot(data=data[data["record_type"] == "missense"], x="score", bins=40, ax=axes[0])\nsns.ecdfplot(data=data, x="score", hue="record_type", hue_order=TYPES, ax=axes[1])\nsns.boxplot(data=data, x="record_type", y="score", order=TYPES, ax=axes[2])\n\nfor ax, letter in zip(axes, "abc"):\n    ax.set_title(letter, loc="left", fontweight="bold")\naxes[0].set(xlabel="abundance score", ylabel="number of variants")\naxes[1].set(xlabel="abundance score", ylabel="cumulative fraction")\naxes[2].set(xlabel="", ylabel="abundance score")\n\nfig.tight_layout()\n\nfig.savefig(FIGS / "score_distributions.png", dpi=300, bbox_inches="tight")\nfig.savefig(FIGS / "score_distributions.pdf", bbox_inches="tight")',
             "python", "a three-panel figure", test="s9_panel"),
        ul([
            "<strong>PNG</strong> at 300 dpi for slides and documents; <strong>PDF</strong> or <strong>SVG</strong> (vector, infinitely sharp) for papers and posters.",
            "<code>bbox_inches=\"tight\"</code> trims the white border so labels are not clipped.",
            "Use one palette and keep each category the same colour in every figure. Readers learn your colours.",
            "The <code>colorblind</code> palette is a safe default; avoid red/green as the only distinction.",
        ]),
        callout("why", "Pick the plot after you pick the question",
                p("Do not browse for a pretty chart. Write the sentence you want the reader to take away (\"nonsense variants sit near zero; most missense variants do not\") and choose the plot that makes that sentence obvious.")),
    ],
    [
        puzzle("s9p1", 1,
               p("What is the <strong>median</strong> <code>score</code> of the <code>nonsense</code> variants, to 2 decimal places? "
                 "This is the line in the middle of the nonsense box in your box plot."),
               kind="number", placeholder="2 decimal places",
               hint="Filter to <code>record_type == \"nonsense\"</code>, take <code>[\"score\"].median()</code>.",
               solution='print(round(df.loc[df["record_type"] == "nonsense", "score"].median(), 2))', test="s9p1"),
        puzzle("s9p2", 2,
               p("The histogram of missense scores is rarely one tidy hump. Count the missense variants with a <code>score</code> <strong>strictly below 0.5</strong>."),
               kind="number", placeholder="a whole number",
               hint="A boolean mask again: <code>(miss[\"score\"] &lt; 0.5).sum()</code> adds up the <code>True</code> values.",
               solution='miss = df[df["record_type"] == "missense"]\nprint((miss["score"] < 0.5).sum())', test="s9p2"),
    ],
))

# =====================================================================
# Stage 10
# =====================================================================
STAGES_B.append(stage(
    10, "Heatmap Heights", "plots for relationships and patterns", 65,
    "Scatter plots, density views, error bars, a track along the sequence, and the heatmap that shows thousands of values at once.",
    [
        p("Open notebook 4 again (this stage is its second half) and add <code>miss = df[df[\"record_type\"] == \"missense\"]</code> if your session was reset. "
          "Distributions answered \"what does it look like?\". These plots answer \"what goes with what?\" and \"where along the protein?\"."),
        h3("Two variables"),
        code('fig, ax = plt.subplots(figsize=(6, 4.5))\nsns.scatterplot(data=miss, x="se", y="score", s=8, alpha=0.4, ax=ax)\nax.set(xlabel="standard error", ylabel="abundance score", title="Do noisier measurements score differently?")',
             "python", "1. scatter", test="s10_scatter"),
        code('fig, ax = plt.subplots(figsize=(6, 4.5))\nsns.regplot(data=miss, x="expts", y="se", x_jitter=0.2,\n            scatter_kws={"s": 6, "alpha": 0.3}, line_kws={"color": "C3"}, ax=ax)\nax.set(xlabel="number of experiments", ylabel="standard error")\n\nmiss[["score", "se", "expts"]].corr(method="spearman").round(2)',
             "python", "2. trend line + correlation", test="s10_reg"),
        callout("note", "Correlation is a number; the plot is the check",
                p("A correlation coefficient can look strong because of one cluster, or weak because the relationship is curved. Always look at the scatter that goes with it. "
                  "Spearman (used above) compares ranks, so it is robust to outliers and to curved but steadily rising relationships.")),
        code('fig, ax = plt.subplots(figsize=(6, 4.5))\nhb = ax.hexbin(miss["score"], miss["se"], gridsize=30, mincnt=1, cmap="viridis")\nfig.colorbar(hb, ax=ax, label="number of variants")\nax.set(xlabel="abundance score", ylabel="standard error", title="Hexbin: when dots overlap")',
             "python", "3. hexbin (many points)", test="s10_hex"),
        h3("Show the uncertainty"),
        code('sub = miss[miss["position"].between(75, 76)].sort_values("hgvs_pro")\nlower = (sub["score"] - sub["lower_ci"]).clip(lower=0)   # error bars must not be negative\nupper = (sub["upper_ci"] - sub["score"]).clip(lower=0)\n\nfig, ax = plt.subplots(figsize=(11, 4))\nax.errorbar(range(len(sub)), sub["score"], yerr=[lower, upper], fmt="o", capsize=2, ms=4)\nax.set_xticks(range(len(sub)), sub["hgvs_pro"], rotation=90, fontsize=8)\nax.axhline(1, ls="--", color="grey", lw=1)\nax.set(ylabel="abundance score", title="Scores with 95% intervals")',
             "python", "4. points with error bars", test="s10_err"),
        callout("trap", "<code>ValueError: 'yerr' must not contain negative values</code>",
                p("Matplotlib wants error sizes, not endpoints, and sizes cannot be negative. That is why the code subtracts the score from the interval ends. "
                  "Read the message, think about what you passed, fix the arithmetic.")),
        h3("A track along the sequence"),
        p("Position on the x-axis, a summary on the y-axis, and shaded bands for the annotated regions. This is the plot that connects a table to the structure of the thing it came from."),
        code('by_position = (\n    miss.groupby("position")["score"]\n        .agg(n_subs="size", mean_score="mean")\n        .reset_index()\n)\nx = by_position["position"].astype(int)\nsmooth = by_position["mean_score"].rolling(5, center=True, min_periods=1).mean()\n\nfig, ax = plt.subplots(figsize=(12, 3.8))\nfor r, colour in zip(regions.itertuples(), ["C0", "C1", "C2"]):\n    ax.axvspan(r.start, r.end, color=colour, alpha=0.12)\n    ax.text((r.start + r.end) / 2, 1.28, r.region, ha="center", fontsize=9)\nax.plot(x, by_position["mean_score"], lw=0.8, color="grey", label="mean per position")\nax.plot(x, smooth, lw=2, color="black", label="5-position rolling mean")\nax.set(xlim=(1, 403), ylim=(0, 1.35), xlabel="position", ylabel="mean missense score")\nax.legend(loc="lower right", frameon=False)',
             "python", "5. line track with region bands", test="s10_track"),
        h3("The heatmap"),
        p("One cell per substitution: position along the x-axis, the new letters on the y-axis, colour for the score. "
          "Thousands of numbers become one picture where stripes mean \"this position hates any change\" and horizontal bands mean \"this substitution is bad everywhere\"."),
        code('AA = ["Ala", "Val", "Ile", "Leu", "Met", "Phe", "Trp", "Tyr", "Cys", "Gly",\n      "Pro", "Ser", "Thr", "Asn", "Gln", "Asp", "Glu", "His", "Lys", "Arg"]\n\ngrid = miss.pivot_table(index="alt", columns="position", values="score").reindex(AA)\n\nfig, ax = plt.subplots(figsize=(14, 5))\nax.set_facecolor("#dddddd")      # untested substitutions show as grey\nsns.heatmap(grid, cmap="viridis", vmin=0, vmax=1.2, xticklabels=25,\n            cbar_kws={"label": "abundance score"}, ax=ax)\nax.set(xlabel="position", ylabel="new letters")',
             "python", "6. heatmap", test="s10_heat"),
        callout("tip", "Make the heatmap readable",
                ul(["Fix <code>vmin</code>/<code>vmax</code> so colours mean the same thing across plots.",
                    "Order the rows meaningfully (here by chemical similarity) instead of alphabetically.",
                    "Use a perceptually even colormap like <code>viridis</code>; avoid rainbow maps that invent edges.",
                    "Show missing cells honestly, in grey, rather than as zero."])),
        h3("Plot hygiene checklist"),
        ul(["Axis labels with units; a title that states the finding, not just the variables.",
            "Same colour = same category in every figure.",
            "Text readable at the size it will be printed (14 to 16 pt at final size is a good aim).",
            "Save from code, with a descriptive filename, into <code>results/figures/</code>.",
            "Show the raw data points where you can; summaries alone hide too much."]),
    ],
    [
        puzzle("s10p1", 1,
               p("Using only <code>missense</code> rows, group by the new letters (<code>alt</code>) and take the mean <code>score</code>. "
                 "Which new amino acid, written as its three letters like <code>Ala</code>, has the <strong>lowest</strong> mean? "
                 "It is the dimmest horizontal band in your heatmap."),
               kind="text", placeholder="Xxx",
               hint="<code>miss.groupby(\"alt\")[\"score\"].mean().idxmin()</code>. Remember <code>miss</code> must only contain missense rows, otherwise <code>Ter</code> and <code>=</code> sneak in.",
               solution='print(miss.groupby("alt")["score"].mean().idxmin())', test="s10p1"),
        puzzle("s10p2", 2,
               p("Cut the sequence into windows of 10 positions: <code>window = position // 10 * 10</code>, so positions 120 to 129 form window <code>120</code>. "
                 "Among windows that contain <strong>at least 30 missense variants</strong>, which window has the lowest mean missense <code>score</code>? "
                 "Answer with the window's starting number."),
               kind="number", placeholder="a multiple of 10",
               hint="Make a <code>window</code> column, <code>groupby(\"window\")</code> with <code>n=(\"score\", \"size\")</code> and <code>mean=(\"score\", \"mean\")</code>, filter on <code>n &gt;= 30</code>, then <code>idxmin()</code> of the mean.",
               solution='miss = miss.assign(window=miss["position"] // 10 * 10)\nw = miss.groupby("window")["score"].agg(n="size", mean="mean")\nprint(w[w["n"] >= 30]["mean"].idxmin())', test="s10p2"),
    ],
))

# =====================================================================
# Stage 11
# =====================================================================
MAKE_FIGURES = r'''
"""Rebuild every figure from the raw data.

Run from anywhere:  python src/make_figures.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      # draw straight to files, no window
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from vampseq_tools import label_regions, parse_hgvs   # same folder as this script

ROOT = Path(__file__).resolve().parent.parent
RAW, FIGS = ROOT / "data" / "raw", ROOT / "results" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook", palette="colorblind")
TYPES = ["synonymous", "missense", "nonsense"]

df = pd.read_csv(RAW / "pten-variant-abundance.csv")
regions = pd.read_csv(RAW / "pten-region-annotations.csv")
df = label_regions(parse_hgvs(df), regions)
data = df[df["record_type"].isin(TYPES)]

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sns.ecdfplot(data=data, x="score", hue="record_type", hue_order=TYPES, ax=axes[0])
sns.boxplot(data=data, x="record_type", y="score", order=TYPES, ax=axes[1])
axes[0].set(xlabel="abundance score", ylabel="cumulative fraction")
axes[1].set(xlabel="", ylabel="abundance score")
fig.tight_layout()
fig.savefig(FIGS / "score_distributions.png", dpi=300, bbox_inches="tight")

print("wrote", FIGS / "score_distributions.png")
'''

STAGES_B.append(stage(
    11, "The Summit", "does your conclusion survive a different rule?", 60,
    "A result is only as solid as the choices behind it. You will change one rule, measure how much the answer moves, and write down what you conclude.",
    [
        p("Every analysis contains judgement calls: which rows to keep, how to score, where to cut. "
          "A trustworthy analysis shows how much the answer <em>depends</em> on them. Take one call you have already made implicitly: "
          "<strong>should we trust variants that were measured in only a couple of experiments?</strong>"),
        h3("Turn the rule into a dial"),
        code('def summarise(df, region="phosphatase_domain", min_expts=None):\n    """Count and mean of missense scores in one region.\n\n    min_expts: keep only variants measured in at least this many experiments\n    (None keeps everything).\n    """\n    keep = (df["record_type"] == "missense") & (df["region"] == region)\n    if min_expts is not None:\n        keep &= df["expts"] >= min_expts\n    return df.loc[keep, "score"].agg(["count", "mean"])\n\nsummarise(df), summarise(df, min_expts=3)',
             "python", "cell", test="s11_func"),
        p("Now sweep the dial and look at the whole curve, not one cherry-picked value:"),
        code('rows = []\nfor k in [1, 2, 3, 4, 5, 6, 7, 8]:\n    s = summarise(df, min_expts=k)\n    rows.append({"min_expts": k, "n_variants": int(s["count"]), "mean_score": s["mean"]})\nsweep = pd.DataFrame(rows)\nsweep.round(3)',
             "python", "cell", test="s11_sweep"),
        code('fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))\nsns.lineplot(data=sweep, x="min_expts", y="n_variants", marker="o", ax=axes[0])\nsns.lineplot(data=sweep, x="min_expts", y="mean_score", marker="o", ax=axes[1])\naxes[0].set(xlabel="minimum experiments", ylabel="variants kept")\naxes[1].set(xlabel="minimum experiments", ylabel="mean missense score")\nfig.tight_layout()',
             "python", "cell", test="s11_plot"),
        p("If the mean barely moves while the count falls, the conclusion is robust to this rule. If it swings, say so in your write-up. Either answer is a result."),
        callout("why", "This is the heart of reproducible research",
                p("Readers should be able to change the dial themselves. A function with a documented parameter lets them. A hand-edited spreadsheet does not.")),
        h3("Write the conclusion"),
        p("A number is not a conclusion. A conclusion says what you found, how sure you are, and what could change it. "
          "Look at your sweep: how many variants does each rule keep, and how far does the mean move?"),
    ],
    [
        puzzle("s11p1", 1,
               p("Keep only rows whose <code>expts</code> is <strong>at least 3</strong>, across the whole table (every record type). How many rows remain?"),
               kind="number", placeholder="a whole number",
               hint="<code>(df[\"expts\"] &gt;= 3).sum()</code> or <code>len(df[df[\"expts\"] &gt;= 3])</code>. Rows with a missing <code>expts</code> fail the comparison and are not counted.",
               solution='print((df["expts"] >= 3).sum())', test="s11p1"),
        puzzle("s11p2", 2,
               p("Use <code>summarise</code> for the <code>phosphatase_domain</code>. Compute the mean missense score <strong>with</strong> the rule <code>min_expts=3</code> minus the mean <strong>without</strong> it. "
                 "Give the difference (after minus before) to 3 decimal places; keep the sign."),
               kind="number", placeholder="e.g. -0.012",
               hint="<code>summarise(df, min_expts=3)[\"mean\"] - summarise(df)[\"mean\"]</code>. A tiny difference is good news for the robustness of the earlier answer.",
               solution='after = summarise(df, min_expts=3)["mean"]\nbefore = summarise(df)["mean"]\nprint(round(after - before, 3))', test="s11p2"),
        puzzle("s11p3", 3,
               p("<strong>Write a short conclusion</strong> (four to six sentences) about the phosphatase domain, as you would in a lab meeting. "
                 "Include the mean with and without the rule, how many variants each rule keeps, whether you think the conclusion is robust to this choice, and one other analysis choice that could change it."),
               kind="reflect", minwords=55, placeholder="Using all variants, the mean missense score in the phosphatase domain is ... After requiring at least 3 experiments ...",
               hint="Use the sentence frame: finding with numbers, then how it changed, then your confidence, then a caveat or next check.",
               model='<h4>A model answer (use your own numbers)</h4>'
                     '<p>\"Across all ___ missense variants in the phosphatase domain the mean score is ___. Requiring at least 3 experiments keeps ___ variants and moves the mean to ___ (a change of ___). '
                     'Because the shift is [small / large] compared with the spread between variants, I consider the domain-level conclusion [robust / sensitive] to this rule. '
                     'The sweep shows the estimate [stabilises / keeps changing] as the threshold rises, but fewer variants means a noisier mean. '
                     'Other choices could matter too, such as excluding variants with large standard errors, or using the median instead of the mean, so I would check those next before making any strong claim.\"</p>'
                     '<h4>Did you cover</h4><ul><li>Both means and both counts?</li><li>A judgement about robustness, with a reason?</li>'
                     '<li>The cost of keeping fewer variants?</li><li>A different choice that could change the result?</li></ul>'),
    ],
))

# =====================================================================
# Stage 13 (Part 2): ship it
# =====================================================================
STAGES_B.append(stage(
    13, "Ship It", "from notebook to script", 40,
    "Make your analysis re-runnable end to end, so that someone else (or you in a year) can rebuild every figure with one command.",
    [
        p("In Part 1 you explored in notebooks. Final results should not depend on cells you clicked in some order. Here is the checklist that turns exploration into something reproducible."),
                ol([
            "<strong>Restart and Run All</strong> every notebook. Fix anything that fails or depends on a cell you ran once and forgot.",
            "Move final plotting code into a script so figures regenerate with one command. Save this as <code>src/make_figures.py</code>:",
        ]),
        code(MAKE_FIGURES, "python", "src/make_figures.py", test="s11_script"),
        ol([
            "Run it from the project root: <code>python src/make_figures.py</code>. Delete <code>results/figures</code> first to prove it rebuilds everything.",
            "Re-export the environment: <code>conda env export --from-history &gt; environment.yml</code>.",
            "Update the README with the dial you chose and why, then commit.",
        ]),
        code("python src/make_figures.py", "bash", "terminal"),
        p("Your final <code>src/vampseq_tools.py</code> now holds <code>add_scores</code>, <code>parse_hgvs</code> and <code>label_regions</code>: "
          "three small functions, each documented, each reused by notebooks and scripts alike. That is the whole habit in miniature."),
        h3("Where to go next"),
        ul([
            '<a href="https://pandas.pydata.org/docs/user_guide/10min.html" target="_blank" rel="noopener">10 minutes to pandas</a>: the official short tour. You can now read all of it.',
            '<a href="https://seaborn.pydata.org/examples/index.html" target="_blank" rel="noopener">seaborn gallery</a> and <a href="https://matplotlib.org/stable/gallery/index.html" target="_blank" rel="noopener">matplotlib gallery</a>: browse for a plot shape, copy the code, adapt it.',
            "Put your project on GitHub so your future lab can see it.",
            "Pick a question of your own about this dataset and answer it with a figure, a paragraph, and a function.",
        ]),

    ],
    [],
))

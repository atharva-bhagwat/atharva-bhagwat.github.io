"""Generate the Colab notebooks (student version with blanks, solution version)."""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, "/tmp/shim")
import ex2
ex2.LOCAL_BASE = "/tmp/srv2/flat/"
import qbuild
import buildsite

SITE_CODE = dict(qbuild.COLLECTED_CODE)
OUT = Path("nb")
URL = "https://atharvabhagwat.dev/assets/data/"


def site(tag, *fills):
    c = SITE_CODE[tag]
    for old, new in fills:
        assert old in c, (tag, old)
        c = c.replace(old, new, 1)
    return c


def B(answer):
    return "\u27e6" + answer + "\u27e7"


def md_from_html(t):
    t = re.sub(r"</?code>", "`", t)
    t = re.sub(r"</?strong>", "**", t)
    t = re.sub(r"</?em>", "*", t)
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t)


HOW = """## How this notebook works

* Run a cell by clicking it and pressing **Shift + Enter** (or the \u25b6 button on its left). Go from top to bottom.
* A `____` is a **blank**. Replace it with the right word or number, then run the cell.
* Cells called **Exercise** are small tasks. Try them yourself first. The expected output is shown so you can compare.
* Cells marked with a star give the answer to a **question on the guide page**. Type your answer there to light up a star.
* If something looks strange, choose **Runtime, Restart session and run all**.
* First, save your own copy: **File, Save a copy in Drive**."""

SETUP_REAL = ('import pandas as pd\n\n'
              'df = pd.read_csv("' + URL + 'pten-variant-abundance.csv")\n\n'
              '# the same steps as Stages 6 and 7\n'
              'df["alt"] = df["hgvs_pro"].str[-3:]\n'
              'df.loc[df["hgvs_pro"].str.endswith("="), "alt"] = "="\n'
              'df["position"] = pd.to_numeric(df["hgvs_pro"].str.extract(r"(\\d+)", expand=False))\n\n'
              'df["region"] = "other"\n'
              'df.loc[df["position"].between(14, 185), "region"] = "phosphatase_domain"\n'
              'df.loc[df["position"].between(190, 350), "region"] = "c2_domain"\n'
              'df.loc[df["position"].between(352, 403), "region"] = "disordered_tail"\n\n'
              'miss = df[df["record_type"] == "missense"].copy()\n'
              'miss.shape')


def exercise_cells(*keys):
    cells = []
    for key in keys:
        for e in ex2.BY_STAGE.get(key, []):
            md = f"### Exercise: {e['title']}\n\n{md_from_html(e['task'])}"
            if e["kind"] == "auto":
                md += "\n\n**Expected output:**\n\n```\n" + ex2.expected(e) + "\n```"
            elif e["kind"] == "real":
                md += "\n\n*Your numbers depend on the real table, so there is no fixed output to compare with.*"
            cells.append(("md", md))
            if e["kind"] == "manual" and e["lang"] != "python":
                cells.append(("md", "Do this in your **terminal**, not in this notebook."))
            elif e["kind"] == "manual" and not e["ask"].strip().startswith("# no"):
                cells.append(("exc", e["ask"], e["solution"]))
            elif e["kind"] != "manual":
                cells.append(("exc", e["starter"], e["full"] if e["kind"] == "auto" else e["solution"]))
            else:
                cells.append(("md", "*Write your answer in a text cell below.*"))
    return cells


def render(cells, solution):
    out = []
    for c in cells:
        k = c[0]
        if k == "md":
            out.append(("markdown", c[1]))
        elif k == "code":
            out.append(("code", re.sub("\u27e6(.*?)\u27e7", (lambda m: m.group(1)) if solution else "____", c[1])))
        elif k == "exc":
            out.append(("code", c[2] if solution else c[1]))
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
    return {"cells": cells, "metadata": {"colab": {"provenance": []}, "kernelspec": {"display_name": "Python 3", "name": "python3"},
                                         "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 0}


def section(title, intro):
    return ("md", f"## {title}\n\n{intro}")


NB = {}

# ----------------------------------------------------------------------------- warm-up
NB["warmup_first_10_minutes"] = [
    ("md", "# Your first 10 minutes with code\n\nNo experience needed, and nothing to install. Code is **a list of instructions the computer follows from top to bottom**. Today you will not write much: you will learn to **read** it, run it, and change it to see what happens.\n\n"
           "**How this works**\n\n* Click into a grey cell and press **Shift + Enter** (or the \u25b6 button on its left) to run it. The result appears underneath.\n* Go from top to bottom.\n* You cannot break anything. If something looks strange, choose **Runtime, Restart session and run all**.\n* Where you see `____`, fill in the blank, then run the cell."),
    ("md", "## 0. Reading code is like reading English\n\nRead each note (the line starting with `#`), then the code under it. They say the same thing."),
    ("code", '# Say hello.\nprint("Hello")\n\n# Remember that the age is 25.\nage = 25\n\n# If the age is more than 18, say "adult".\nif age > 18:\n    print("adult")'),
    ("md", "## 1. Your first line of code\n\nThe line below tells the computer to *print* some words. Lines that start with `#` are notes for humans, and the computer ignores them. Run it, then change the words inside the quotes and run it again."),
    ("code", '# print() shows something on the screen\nprint("Hello, biology!")'),
    ("md", "## 2. Variables are labelled boxes\n\nA **variable** stores a value under a name, so you can use it later. The `=` sign means *store this under that name* (it does not mean \"equals\" like in maths).\n\nHere the name is `dna` and the value is a piece of text (text always goes inside quotes)."),
    ("code", 'dna = "ATGGAAGCTCTGTTTAAAGGCTAA"\nprint(dna)'),
    ("md", "`len()` counts how many letters are in a piece of text. Fill in the blank so the sentence prints the length."),
    ("code", 'length = len(dna)\nprint("My DNA has", ' + B("length") + ', "letters")'),
    ("md", "## 3. Arithmetic\n\nPython is a calculator. Run this cell and look at each answer.\n\n| symbol | meaning |\n|---|---|\n| `+` `-` `*` | add, subtract, multiply |\n| `/` | divide |\n| `//` | divide and drop the remainder |\n| `%` | the remainder |\n| `**` | power |"),
    ("code", 'print(2 + 3)\nprint(10 - 4)\nprint(6 * 7)\nprint(10 / 4)\nprint(10 // 4)\nprint(10 % 4)\nprint(2 ** 5)'),
    ("md", "**Predict first, then run:** what will `print(17 // 5)` and `print(17 % 5)` show? Write your guess here, then add those two lines to the cell above and check.\n\n*(double-click this cell to type your guess)*"),
    ("md", "DNA is read three letters at a time. How many groups of three are in our DNA? Fill in the blank with the symbol for \"divide and drop the remainder\"."),
    ("code", 'groups = length ' + B("//") + ' 3\nprint("That is", groups, "groups of three letters")'),
    ("md", "A variable can be **updated**: take the old value, do something to it, store the result under the same name. Read each line, guess the final number, then run it."),
    ("code", 'count = 0\ncount = count + 1\ncount = count + 1\ncount = count + 1\nprint(count)'),
    ("md", "## 4. Comparing things\n\nA **comparison** asks a yes/no question, and the answer is `True` or `False`.\n\n| symbol | question |\n|---|---|\n| `==` | is it equal to? |\n| `!=` | is it NOT equal to? |\n| `<` `>` | is it less than? more than? |\n| `<=` `>=` | is it at most? at least? |\n\nNotice that asking \"is it equal?\" uses **two** equals signs. One `=` stores a value; two `==` ask a question."),
    ("code", 'print(length > 20)\nprint(length == 24)\nprint(length != 24)\nprint(length <= 10)\nprint(dna == "ATG")'),
    ("md", "**Predict first:** which of those five lines will say `True`? Then run it and check."),
    ("md", "## 5. Working with text\n\nText has its own tools. Each line below does one thing. Run the cell and match each output to its line."),
    ("code", 'print(dna.lower())                # all lowercase\nprint(dna.count("G"))             # how many G letters\nprint(dna + "AAA")                # glue text together\nprint(dna[0:3])                   # the first three letters (counting starts at 0)'),
    ("md", "## 6. Putting it together: GC content\n\nScientists often ask what fraction of a DNA sequence is the letters G and C (the **GC fraction**). You can now read this whole recipe: count the Gs, count the Cs, add them, divide by the length."),
    ("code", 'g = dna.count("G")\nc = dna.count("C")\ngc = (g + c) / len(dna)\nprint("GC fraction:", gc)\nprint("As a percentage:", round(gc * 100, 1), "%")'),
    ("md", "\u2b50 **Write down the GC fraction of this DNA, rounded to 3 decimal places.** You will type it into the guide in a moment. (Run the next cell to see it rounded.)"),
    ("code", 'print(round(gc, 3))'),
    ("md", "## 7. Making a decision\n\n`if` runs some code only when a comparison is `True`, and `else` runs when it is not. The lines inside are **indented** (pushed in): that is how Python knows they belong to the `if`. Fill in a threshold and run it, then try a different number."),
    ("code", 'if gc > ' + B("0.5") + ':\n    print("This DNA is GC-rich")\nelse:\n    print("This DNA is AT-rich")'),
    ("md", "## 8. Doing something many times\n\nA **loop** repeats code once for each item in a list. Read this one aloud: *for each sequence in the list, work out its GC fraction and print it.*"),
    ("code", 'sequences = ["ATATAT", "GGGCCC", "ATGGAAGCT"]\n\nfor seq in sequences:\n    fraction = (seq.count("G") + seq.count("C")) / len(seq)\n    print(seq, "->", round(fraction, 2))'),
    ("md", "### Your turn\n\nAdd your own DNA (any letters from A, C, G, T, in quotes) to the `sequences` list above and run the cell again. Its GC fraction should appear."),
    ("md", "## What you just learned\n\n* **print** shows things; **#** starts a note for humans\n* **variables** store values under names\n* **arithmetic**: `+ - * / // % **`\n* **comparisons**: `== != < > <= >=` give True or False\n* **text** has tools such as `len`, `count`, slicing and `lower`\n* **if / else** makes decisions, **for** repeats things\n\nThat is the real foundation. Everything in the guide is built from these pieces, and you just read all of them.\n\n**Next:** go back to the guide, type the GC fraction you wrote down, and see the plan. Everything after this is optional, and you choose the pace."),
]

# ----------------------------------------------------------------------------- Stage 0
NB["00_python_building_blocks"] = [
    ("md", "# Stage 0: Python building blocks\n\nFrom a single value to a table of data, using short DNA sequences. Each step is built from the one before it.\n\n" + HOW),
    ("md", "## Step 1: values\n\nA **variable** is a name that holds a value. Text goes in quotes."),
    ("code", site("z0_values", ("length = 30 ", "length = " + B("30") + " "))),
    ("md", "## Step 2: lists\n\nA **list** holds several values in order. Counting starts at 0, so the third item is number 2."),
    ("code", site("z0_lists", ("lengths[2]", "lengths[" + B("2") + "]"))),
    ("md", "## Step 3: dictionaries\n\nA **dictionary** links names to values, with curly brackets."),
    ("code", site("z0_dict", ('length_of["geneB"]', 'length_of["' + B("geneB") + '"]'))),
    ("md", "## Step 4: libraries\n\nA **library** is a set of extra tools. Run the cell to see numpy at work. You do not need to memorise it. To find out more about any function, use `help(...)` or search its documentation:"),
    ("code", site("z0_numpy")),
    ("code", "help(np.mean)"),
    ("md", "Documentation websites: [numpy](https://numpy.org/doc/stable/), [pandas](https://pandas.pydata.org/docs/), [matplotlib](https://matplotlib.org/stable/), [seaborn](https://seaborn.pydata.org/). On any page, read the one-line summary first, then look for **Examples**."),
    ("md", "## Step 5: tables with pandas\n\nA table is a **DataFrame**. Here is one made from a dictionary of lists."),
    ("code", site("z0_table")),
    ("code", site("z0_cols")),
    ("md", "Keep only some rows by putting a condition in square brackets. Try changing the number."),
    ("code", site("z0_filter", ('> 0.5', '> ' + B("0.5")))),
    ("md", "## \u2b50 Questions for the guide\n\n1. What is the GC fraction of `geneC`? (3 decimals)\n2. How many genes have a GC fraction above 0.5?"),
    ("code", 'print(genes[genes["gene"] == "geneC"]["gc"])\nprint(len(genes[genes["gc"] > 0.5]))'),
] + exercise_cells(12)

# ----------------------------------------------------------------------------- Stage 1
NB["01_notebooks_text_loops"] = [
    ("md", "# Stage 1: Notebooks, text and loops\n\nHow notebooks work, how the kernel remembers things, and how to work with text and repeat actions.\n\n" + HOW),
    ("md", "## The kernel has a memory\n\nBehind this notebook runs a **kernel** that remembers every variable. Run the two cells below. Then change the first to `x = 100` but **do not run it**, and run the second again. What do you get, and why?"),
    ("code", site("z1_mem1")),
    ("code", site("z1_mem2")),
    ("md", "My prediction was: *(double-click to type)*\n\nWhat happened, and why?\n\n**When to restart:** if results look wrong, if you edited cells near the top, if you get a `NameError` for something you did create, or before sharing. Use **Runtime, Restart session and run all**. It clears the kernel's memory (variables), keeps your code, and then runs everything in order."),
    ("md", "### Running out of order\n\nRun this cell three times, one after another. What does it print each time? Then restart and run it once."),
    ("code", 'total = 5\ntotal = total + 1\nprint(total)'),
    ("md", "Now try this: put `total = 5` in one cell and `total = total + 1` with the print in another. Run the second cell several times without running the first. What changes?"),
    ("md", "## Text\n\nA **slice** `text[start:stop]` takes letters from `start` up to, but not including, `stop`."),
    ("code", site("z1_text", ("name[2:5]", "name[" + B("2:5") + "]"))),
    ("code", site("z1_int")),
    ("md", "## Comparisons and decisions"),
    ("code", site("z1_if", ("score < 1.0", "score < " + B("1.0")))),
    ("md", "## Loops\n\nA loop repeats code for each item in a list."),
    ("code", site("z1_loop", ("for variant in variants:", "for variant in " + B("variants") + ":"))),
    ("md", "## \u2b50 Questions for the guide\n\n1. Add up the positions in all the variant names.\n2. Count how many variants are synonymous, nonsense and missense."),
    ("code", 'total = 0\nfor variant in variants:\n    total = total + int(variant[5:-3])\nprint(total)\n\nsyn = 0\nnon = 0\nmis = 0\nfor variant in variants:\n    if variant[2:5] == variant[-3:]:\n        syn = syn + 1\n    elif variant[-3:] == "Ter":\n        non = non + 1\n    else:\n        mis = mis + 1\nprint(syn, non, mis)'),
] + exercise_cells(1)

# ----------------------------------------------------------------------------- Stage 2
NB["02_error_messages"] = [
    ("md", "# Stage 2: Reading error messages\n\nErrors are directions, not insults. Read from the **bottom**: the last line says what went wrong, the arrow points at your line, and the middle is library code you can ignore.\n\n" + HOW),
    ("md", "## See three errors\n\nEach cell below fails on purpose. Run it, read the last line, and write in the cell after it what the error says."),
    ("code", 'scores = {"score": 3.49}\nprint(scores["Score"])        # KeyError: what is the key really called?'),
    ("md", "My reading: *(double-click to type)*"),
    ("code", 'names = ["WT", "p.Trp18Ter"]\nprint(names[5])               # IndexError: how many items are there?'),
    ("md", "My reading: *(double-click to type)*"),
    ("code", 'print("average: " + 2.718)       # TypeError: what are the two types?'),
    ("md", "My reading: *(double-click to type)*"),
    ("md", "## Fix three bugs in one cell\n\nThe errors arrive one at a time, in this order: `SyntaxError`, `NameError`, `TypeError`. Fix each. What average does it print at the end? That is the answer to the second guide question."),
    ("exc", 'scores = [3.45, 1.55, 2.18, 2.59, 3.82]\n\ntotal = 0\nfor s in scores\n    total = total + s\n\nmean = total / len(score)\nprint("average: " + mean)',
            'scores = [3.45, 1.55, 2.18, 2.59, 3.82]\n\ntotal = 0\nfor s in scores:\n    total = total + s\n\nmean = total / len(scores)\nprint("average:", mean)'),
    ("md", "Check your results too. A wrong number with no error is the worst kind of bug, so print things and ask whether they are plausible:"),
    ("code", 'print(len(scores))\nprint(scores)'),
] + exercise_cells(2)

# ----------------------------------------------------------------------------- Stages 3 to 5
NB["03_pandas_tables_and_functions"] = [
    ("md", "# Stages 3 to 5: Tables with pandas, calculations, functions\n\nThe toy table is an invented experiment: each row is one named item measured once, and `bin1_count` to `bin4_count` say how many reads fell into four brightness buckets.\n\n" + HOW),
    ("md", "# Stage 3: Tables with pandas\n\n## Load and look"),
    ("code", site("z3_load")),
    ("code", site("z3_look")),
    ("md", "## Pick columns"),
    ("code", site("z3_cols")),
    ("md", "## Keep only some rows\n\nA comparison gives True or False for every row. Putting it in square brackets keeps the True rows."),
    ("code", site("z3_filter1", ('"nonsense"', '"' + B("nonsense") + '"'))),
    ("code", site("z3_filter2")),
    ("md", "**Try the trap.** Replace `&` with the word `and` in the cell above and read the error. It is `ValueError: The truth value of a Series is ambiguous`."),
    ("code", site("z3_sort", ('"bin1_count"', '"' + B("bin1_count") + '"'))),
    ("md", "## \u2b50 Questions for the guide (Stage 3)\n\n1. How many rows are missense AND replicate 2?\n2. What is the total of all four bin columns?"),
    ("code", 'rows = df[(df["variant_type"] == "missense") & (df["replicate"] == 2)]\nprint(len(rows))\n\nprint(df["bin1_count"].sum() + df["bin2_count"].sum() + df["bin3_count"].sum() + df["bin4_count"].sum())'),
] + exercise_cells(3) + [
    ("md", "# Stage 4: Calculations and groups\n\nThe score is a weighted average of the four bins: bin 1 counts as 1, bin 4 as 4.\n\n`score = (1 x bin1 + 2 x bin2 + 3 x bin3 + 4 x bin4) / total reads`"),
    ("code", site("z4_score")),
    ("md", "## Group"),
    ("code", site("z4_group", ('groupby("variant_type")', 'groupby("' + B("variant_type") + '")'))),
    ("md", "## Replicates side by side"),
    ("code", site("z4_pivot")),
    ("code", site("z4_diff")),
    ("md", "## \u2b50 Questions for the guide (Stage 4)\n\n1. The average score of the WT rows (2 decimals).\n2. Which variant has the largest disagreement between replicates?"),
    ("code", 'print(df[df["variant"] == "WT"]["score"].mean())\nprint(wide["difference"].idxmax())'),
] + exercise_cells(4) + [
    ("md", "# Stage 5: Writing functions\n\nThe second time you copy code, write a function. A function has a name, things you give it (parameters), and a `return`."),
    ("code", site("z5_double", ("return number * 2", "return number " + B("*") + " 2"))),
    ("code", site("z5_func")),
    ("code", site("z5_use")),
    ("md", "## \u2b50 Questions for the guide (Stage 5)\n\n1. The score of `p.Ser45Thr` in replicate 1 (3 decimals).\n2. With `min_reads=50`, the average score of the missense rows (3 decimals)."),
    ("code", 'row = scored[(scored["variant"] == "p.Ser45Thr") & (scored["replicate"] == 1)]\nprint(row["score"])\n\nmissense = strict[strict["variant_type"] == "missense"]\nprint(missense["score"].mean())'),
] + exercise_cells(5)

# ----------------------------------------------------------------------------- Stages 6 and 7
NB["04_checking_real_data"] = [
    ("md", "# Stages 6 and 7: Checking real data and summarising by region\n\n" + HOW),
    ("md", "## What this dataset is about\n\n**PTEN** is a human protein that acts as a brake on cell growth signalling. Many single-letter DNA changes swap one amino acid for another (**missense** variants), and for most nobody knows whether they matter. A *multiplexed assay of variant effect* makes thousands of variants and measures each one. This table measures **abundance**: how much of each variant ends up in the cell. Each variant is tagged with a fluorescent marker, cells are sorted into four bins from dim to bright, and sequencing counts each variant per bin, just like the toy table.\n\n**Abundance is not activity, and activity is not disease.**\n\n### Two scores, one idea\n\nThe toy `score` was a weighted average of bins, 1 to 4. The PTEN `score` was published by the researchers and **rescaled** (the unchanged protein is about 1, broken proteins about 0). Same idea, different method and scale. **Never compare raw numbers across the two tables.**"),
    ("md", "# Stage 6: Checking real data"),
    ("code", site("z7_load")),
    ("md", "Nonsense variants cut the protein short, so they should look broken. Synonymous variants keep the amino acids, so they should look like the unchanged protein. Check:"),
    ("code", site("z7_anchor", ('["score"]', '["' + B("score") + '"]'))),
    ("md", "## The audit checklist"),
    ("code", site("z7_audit")),
    ("md", "## Turn names into columns"),
    ("code", site("z7_slice1", ("name[2:5]", "name[" + B("2:5") + "]"))),
    ("code", site("z7_slice2")),
    ("md", "**Trap:** slicing works on most rows and quietly fails on some. Look at the synonymous names:"),
    ("code", site("z7_odd")),
    ("code", site("z7_pos")),
    ("code", site("z7_check")),
    ("md", "## \u2b50 Questions for the guide (Stage 6)\n\nHow many rows are there? How many different positions?"),
    ("code", 'print(len(df))\nprint(df["position"].nunique())'),
    ("md", "The guide also asks three multiple-choice questions about comparing scores across tables, reference points, and what a low abundance score does and does not mean. Think about them here first.\n\n*(double-click to write a few sentences)*"),
] + exercise_cells(7) + [
    ("md", "# Stage 7: Summarising by region\n\nPTEN has two folded parts, a **phosphatase domain** (the enzyme part) and a **C2 domain** (helps the protein attach to membranes), followed by a floppy **tail**."),
    ("code", site("z8_regions")),
    ("code", site("z8_label")),
    ("code", site("z8_miss")),
    ("code", site("z8_byregion", ('groupby("region")', 'groupby("' + B("region") + '")'))),
    ("md", "**Always show the count next to the average.** An average of 3 variants and one of 3,000 are not equally trustworthy."),
    ("code", site("z8_bypos")),
    ("md", "## \u2b50 Questions for the guide (Stage 7)\n\n1. The average missense score in the `phosphatase_domain` (3 decimals).\n2. Which of the three regions has the lowest median score?"),
    ("code", 'print(by_region.loc["phosphatase_domain", "mean"])\nprint(by_region.drop("other")["median"].idxmin())'),
    ("md", "### \u2b50 Write your interpretation\n\nLook at `by_region` and write about four sentences: which region looks most and which least tolerant of changes; does that make biological sense for a folded domain versus a floppy tail; and how does the **number of variants in each region** change how much you trust the comparison? Then submit it on the guide page.\n\n*(double-click to write)*"),
] + exercise_cells(8)

# ----------------------------------------------------------------------------- Stages 8 and 9
NB["05_plots"] = [
    ("md", "# Stages 8 and 9: Plots\n\n" + HOW),
    ("md", "## Setup\n\nJust run this cell. It repeats the steps from Stages 6 and 7 so this notebook works in a fresh session."),
    ("code", SETUP_REAL),
    ("md", "# Stage 8: Plotting distributions\n\n**matplotlib** draws and saves pictures. **seaborn** draws statistical plots from a table in one line. Every plot: draw it with seaborn, add labels with matplotlib, then show it. **A plot without labels is a rumour.**"),
    ("code", site("z9_setup")),
    ("code", site("z9_hist", ("sns.histplot(", "sns." + B("histplot") + "("))),
    ("code", site("z9_box", ("sns.boxplot(", "sns." + B("boxplot") + "("))),
    ("code", site("z9_violin")),
    ("code", site("z9_strip")),
    ("code", site("z9_count")),
    ("md", "Two groups hiding in one box? Compare the histogram and the box plot of the same scores and describe what each shows and hides."),
    ("code", site("z9_save")),
    ("md", "The saved file appears in the Files panel (folder icon on the left). Right-click it to download."),
    ("md", "## \u2b50 Questions for the guide (Stage 8)\n\n1. The median score of the nonsense variants (2 decimals).\n2. How many missense variants have a score strictly below 0.5?"),
    ("code", 'print(df[df["record_type"] == "nonsense"]["score"].median())\nprint(len(miss[miss["score"] < ' + B("0.5") + ']))'),
] + exercise_cells(9) + [
    ("md", "# Stage 9: More plots (optional)"),
    ("code", site("z10_scatter")),
    ("code", site("z10_line")),
    ("code", site("z10_heat", ('cmap="viridis"', 'cmap="' + B("viridis") + '"'))),
    ("code", site("z10_window")),
    ("md", "## \u2b50 Questions for the guide (Stage 9)\n\n1. Which new amino acid has the lowest average missense score?\n2. Among windows of 10 positions with at least 30 variants, which window has the lowest average?"),
    ("code", 'print(miss.groupby("alt")["score"].mean().idxmin())\nprint(means[counts >= 30].idxmin())'),
] + exercise_cells(10)

# ----------------------------------------------------------------------------- Stage 10
NB["06_checking_conclusion"] = [
    ("md", "# Stage 10: Checking your conclusion\n\nEvery analysis hides judgement calls. A trustworthy one shows how much the answer depends on them. Question for today: *should we trust variants measured in only a couple of experiments?*\n\n" + HOW),
    ("md", "## Setup\n\nJust run this cell."),
    ("code", SETUP_REAL),
    ("code", site("z11_phos")),
    ("code", site("z11_strict", ('>= 3', '>= ' + B("3")))),
    ("code", site("z11_loop")),
    ("md", "If the average barely moves while the number of variants falls, the conclusion is **robust** to this choice."),
    ("md", "## \u2b50 Questions for the guide\n\n1. How many rows (whole table) have `expts` at least 3?\n2. The change in the average: with the rule minus without."),
    ("code", 'print(len(df[df["expts"] >= 3]))\nprint(strict["score"].mean() - phos["score"].mean())'),
    ("md", "## \u2b50 Write the conclusion\n\nWrite four to six sentences as you would in a lab meeting: the average with and without the rule and how many variants each keeps; whether the conclusion is robust to this choice, and why; the cost of keeping fewer variants; and one other analysis choice that could change the result. Then submit it on the guide page.\n\n*(double-click to write)*"),
] + exercise_cells(11)

# ----------------------------------------------------------------------------- Extra
NB["07_extra_biopython"] = [
    ("md", "# Extra: DNA sequences with Biopython\n\nOptional. Biopython is a library with tools for biology.\n\n" + HOW),
    ("code", "%pip install -q biopython"),
    ("code", site("x15_seq", ("dna.reverse_complement()", "dna." + B("reverse_complement") + "()"))),
    ("md", "The `*` is a stop signal. Why is the second protein shorter?"),
    ("code", site("x15_fasta")),
    ("code", site("x15_read")),
    ("code", site("x15_table")),
]


def main():
    for sub in ("student", "solutions"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
    for name, cells in NB.items():
        for sub, sol in (("student", False), ("solutions", True)):
            (OUT / sub / f"{name}.ipynb").write_text(json.dumps(to_ipynb(render(cells, sol)), indent=1), encoding="utf-8")
    print("wrote", len(NB) * 2, "notebooks")


if __name__ == "__main__":
    ex2.LOCAL_BASE = ex2.LOCAL_BASE or "/tmp/srv2/flat/"
    main()

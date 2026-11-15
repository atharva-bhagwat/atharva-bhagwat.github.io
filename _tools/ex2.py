"""Practice exercises.

Every exercise is a small task with a starter, a hidden solution and, when the data is fixed,
the exact output the learner should see. There are no automatic checks: learners compare their
output with the expected output. Exercises that use the real PTEN table show no expected numbers
(they depend on the real file), only what to look for.
"""
import contextlib
import io

from qbuild import code, details, esc

EXERCISES = []     # all exercises, in order
BY_STAGE = {}      # stage key -> list of exercise dicts

BASE_URL = "https://atharvabhagwat.dev/assets/data/"
LOCAL_BASE = None  # set by the build/test scripts to run solutions against local copies


def _run(src):
    """Run code and capture what it prints (used for expected output)."""
    buf = io.StringIO()
    ns = {}
    code_src = src.replace(BASE_URL, LOCAL_BASE) if LOCAL_BASE else src
    with contextlib.redirect_stdout(buf):
        exec(code_src, ns)
    return buf.getvalue().rstrip("\n")


def ex(stage, eid, title, task, setup, ask, solution, kind="auto", lang="python"):
    """kind: 'auto' = run solution to get expected output (fixed data);
             'real' = uses the real table, no expected output;
             'manual' = nothing to run (terminal or writing tasks)."""
    starter = (setup.strip("\n") + "\n\n" if setup.strip() else "") + ask.strip("\n")
    full_solution = (setup.strip("\n") + "\n\n" if setup.strip() else "") + solution.strip("\n")
    EXERCISES.append(dict(stage=stage, id=eid, title=title, task=task, setup=setup.strip("\n"), ask=ask.strip("\n"),
                          starter=starter, solution=solution.strip("\n"), full=full_solution, kind=kind, lang=lang))
    BY_STAGE.setdefault(stage, []).append(EXERCISES[-1])


def expected(e):
    if e["kind"] != "auto":
        return None
    return _run(e["full"])


def page_html(e):
    """Exercise as shown on the stage page: task, then a hidden solution with the expected output."""
    inner = ""
    exp = expected(e)
    if e["kind"] == "auto":
        inner += "<p>The output should look like this:</p>" + code(exp, "text", "expected output")
    elif e["kind"] == "real":
        inner += "<p>Your numbers will depend on the real table, so there is no fixed output to compare with.</p>"
    inner += code(e["full"] if e["kind"] != "real" else e["solution"], e["lang"], "one solution")
    return (
        f'<div class="q-ex"><h4>{e["title"]}</h4><div class="q-ex-task">{e["task"]}</div>'
        + details("Show a solution (try it first)", inner, "q-ex-sol") + "</div>"
    )


# ============================================================ Stage 0: Python building blocks
ex(12, "e0a", "Link names to lengths",
   "A <strong>dictionary</strong> links a name to a value. Make one for three genes, then look one up.",
   'names = ["geneA", "geneB", "geneC"]\nlengths = [36, 36, 30]',
   '# 1. Make a dictionary called length_of with curly brackets { } that links each name to its length.\n# 2. Print the length of geneC.',
   'length_of = {"geneA": 36, "geneB": 36, "geneC": 30}\nprint(length_of["geneC"])')

ex(12, "e0b", "Add a column and filter a table",
   "Add a new column to a table, then keep only the rows you care about.",
   'import pandas as pd\n\ngenes = pd.DataFrame({\n    "gene": ["geneA", "geneB", "geneC", "geneD"],\n    "length": [36, 36, 30, 33],\n})',
   '# 1. Add a column called codons that is the length divided by 3.\n# 2. Print only the rows where codons is at least 11.',
   'genes["codons"] = genes["length"] / 3\nprint(genes[genes["codons"] >= 11])')

# ============================================================ Stage 1: notebooks, strings, loops
ex(1, "e1a", "Count a letter with a loop",
   "Use a loop to count how many times the letter <code>I</code> appears in a protein sequence.",
   'seq = "MTAIIKEIVSRNKRR"\ncount = 0',
   '# Loop over every letter in seq. Each time the letter is "I", add 1 to count.\n# Then print count.',
   'for letter in seq:\n    if letter == "I":\n        count = count + 1\nprint(count)')

ex(1, "e1b", "Pick a variant name apart",
   "A variant name such as <code>p.Val30Asp</code> holds three facts: the old amino acid, the position, and the new amino acid. Use slicing to print each one.",
   'name = "p.Val30Asp"',
   '# Print the old amino acid (letters 2 to 5), the position (letters 5 to 7), and the new amino acid (the last 3 letters).',
   'print(name[2:5])\nprint(name[5:7])\nprint(name[-3:])')

ex(1, "e1c", "Break the kernel's memory on purpose",
   "In a new cell write <code>score = 5</code> and run it. In a second cell write <code>print(score * 2)</code> and run it. "
   "Now change the first cell to <code>score = 50</code> but <strong>do not run it</strong>, and run the second cell again. "
   "Then choose <strong>Runtime, Restart session and run all</strong>. Write in a text cell what changed each time, and why.",
   "", "# no starter: do this in your own cells", "# (no code to submit: describe what you saw)", kind="manual")

# ============================================================ Stage 2: error messages
ex(2, "e2a", "Fix three small bugs",
   "Each pair of lines has one bug. Run the cell, read the error, fix the line, and run again. The comment says what you want.",
   "", 'names = ["WT", "p.Trp18Ter", "p.Leu25Pro"]\nlast_name = names[3]          # I want the LAST name\nprint(last_name)\n\nscores = {"WT": 3.49, "p.Trp18Ter": 1.5}\nprint(scores["wt"])           # I want the WT score\n\nreads = [120, 80, 45]\nprint(sum(reads) / len(read)) # I want the average',
   'names = ["WT", "p.Trp18Ter", "p.Leu25Pro"]\nlast_name = names[2]\nprint(last_name)\n\nscores = {"WT": 3.49, "p.Trp18Ter": 1.5}\nprint(scores["WT"])\n\nreads = [120, 80, 45]\nprint(sum(reads) / len(reads))')

ex(2, "e2b", "Read an error message",
   "Run the cell below. It fails on purpose. In a text cell, write down: (1) the type of error, (2) the line it points to, and (3) how you would fix it.",
   "", 'scores = {"score": 3.49}\nprint(scores["Score"])', "# fix: the key is spelled score, with a small s", kind="manual")

# ============================================================ Stage 3: tables with pandas
TOY = 'import pandas as pd\n\ndf = pd.read_csv("' + BASE_URL + 'toy_vampseq_bin_counts.csv")'

ex(3, "e3a", "List the nonsense variants",
   "Show the names of the variants whose <code>variant_type</code> is <code>nonsense</code>, each name once.",
   TOY,
   '# Keep the rows where variant_type is "nonsense", pick the variant column, and print its unique values.',
   'nonsense = df[df["variant_type"] == "nonsense"]\nprint(nonsense["variant"].unique())')

ex(3, "e3b", "Find the top three",
   "Among the <code>missense</code> rows of <strong>replicate 2</strong>, which three variants have the most reads in <code>bin1_count</code>?",
   TOY,
   '# 1. Keep rows that are missense AND replicate 2 (use & and put each condition in brackets).\n# 2. Sort by bin1_count from biggest to smallest.\n# 3. Print the variant column of the first 3 rows.',
   'rows = df[(df["variant_type"] == "missense") & (df["replicate"] == 2)]\nrows = rows.sort_values("bin1_count", ascending=False)\nprint(rows["variant"].head(3))')

# ============================================================ Stage 4: calculations and groups
SCORED = TOY + '\n\ndf["total_reads"] = df["bin1_count"] + df["bin2_count"] + df["bin3_count"] + df["bin4_count"]'

ex(4, "e4a", "Make a fraction column",
   "Add a column with the share of each row's reads that fall in bin 4.",
   SCORED,
   '# 1. Make a column called frac_bin4: bin4_count divided by total_reads.\n# 2. Print the variant, replicate and frac_bin4 columns of the first 5 rows (use .head()).',
   'df["frac_bin4"] = df["bin4_count"] / df["total_reads"]\nprint(df[["variant", "replicate", "frac_bin4"]].head())')

ex(4, "e4b", "Average by group",
   "Work out the average total reads for each <code>variant_type</code>.",
   SCORED,
   '# Group by variant_type, take total_reads, and print the mean.',
   'print(df.groupby("variant_type")["total_reads"].mean())')

# ============================================================ Stage 5: functions
ex(5, "e5a", "Write a percentage function",
   "Write a function called <code>percent</code> that takes two numbers, <code>part</code> and <code>whole</code>, and gives back the percentage.",
   "",
   '# Fill in the function, then run the three print lines at the bottom.\ndef percent(part, whole):\n    # your code here\n    pass\n\nprint(percent(3, 8))\nprint(percent(1, 4))\nprint(percent(50, 50))',
   'def percent(part, whole):\n    return part / whole * 100\n\nprint(percent(3, 8))\nprint(percent(1, 4))\nprint(percent(50, 50))')

ex(5, "e5b", "Count a letter in a function",
   "Write a function that counts how many times a letter appears in some DNA, then use it twice.",
   "",
   '# Fill in the function, then run the two print lines at the bottom.\ndef count_letter(dna, letter):\n    # your code here\n    pass\n\nprint(count_letter("ATGCATGC", "A"))\nprint(count_letter("GGGCCC", "G"))',
   'def count_letter(dna, letter):\n    return dna.count(letter)\n\nprint(count_letter("ATGCATGC", "A"))\nprint(count_letter("GGGCCC", "G"))')

# ============================================================ Stage 6 (audit)
ex(7, "e6a", "Count and check",
   "Use the table <code>df</code> from the notebook. Print how many rows there are of each <code>record_type</code>, and how many values are missing in the <code>score</code> column.",
   "",
   '# Use value_counts() on record_type, and isna().sum() on the score column.',
   'print(df["record_type"].value_counts())\nprint(df["score"].isna().sum())', kind="real")

ex(7, "e6b", "Do the reference points look right?",
   "Print the average score of <code>synonymous</code> variants and of <code>nonsense</code> variants. In a text cell, write one sentence: do the two numbers look the way you expect, and why?",
   "",
   '# Group by record_type and take the mean of the score column.',
   'print(df.groupby("record_type")["score"].mean())', kind="real")

# ============================================================ Stage 7 (regions)
ex(8, "e7a", "Summarise by amino acid",
   "Using the missense table <code>miss</code>, find the average score for each new amino acid (<code>alt</code>), sorted from lowest to highest.",
   "",
   '# Group miss by alt, take the mean of score, then sort_values().',
   'print(miss.groupby("alt")["score"].mean().sort_values())', kind="real")

ex(8, "e7b", "Write your reading of the table",
   "Look at your <code>by_region</code> table and write three sentences in a text cell: which region looks most affected, whether that makes biological sense, and how the number of variants in each region changes how much you trust it.",
   "", "# no code: write in a text cell", "# (describe what you see)", kind="manual")

# ============================================================ Stage 8 (distribution plots)
ex(9, "e8a", "Plot nonsense scores",
   "Draw a histogram of the scores of the <code>nonsense</code> variants. Give it a title and label both axes.",
   "",
   '# Keep the nonsense rows of df, then use sns.histplot, then plt.title, plt.xlabel, plt.ylabel, plt.show.',
   'nonsense = df[df["record_type"] == "nonsense"]\nsns.histplot(data=nonsense, x="score", bins=20)\nplt.title("Nonsense variants")\nplt.xlabel("abundance score")\nplt.ylabel("number of variants")\nplt.show()', kind="real")

ex(9, "e8b", "Compare regions with a box plot",
   "Draw a box plot of missense scores for each <code>region</code>. Label the axes.",
   "",
   '# Use sns.boxplot with data=miss, x="region", y="score".',
   'sns.boxplot(data=miss, x="region", y="score")\nplt.xlabel("region")\nplt.ylabel("abundance score")\nplt.show()', kind="real")

# ============================================================ Stage 9 (more plots, optional)
ex(10, "e9a", "Does a noisier measurement score differently?",
   "Draw a scatter plot of <code>se</code> (x) against <code>score</code> (y) for the missense variants. Describe what you see in one sentence.",
   "",
   '# Use sns.scatterplot(data=miss, x=..., y=...).',
   'sns.scatterplot(data=miss, x="se", y="score", alpha=0.4)\nplt.xlabel("standard error")\nplt.ylabel("abundance score")\nplt.show()', kind="real")

# ============================================================ Stage 10 (conclusion)
ex(11, "e10a", "Try a stricter rule",
   "Repeat the comparison with <code>expts &gt;= 5</code> instead of 3. How many variants are left, and what is the new mean?",
   "",
   '# Copy the code for expts >= 3 and change the 3 to a 5.',
   'strict5 = phos[phos["expts"] >= 5]\nprint(len(strict5))\nprint(strict5["score"].mean())', kind="real")

# ============================================================ Part 2
ex(0, "e11a", "Terminal drill",
   "Open your terminal and, using only the commands from the table, do this in order: (1) print where you are; (2) make a folder called <code>practice</code>; "
   "(3) step into it; (4) make two folders inside it called <code>data</code> and <code>results</code>; (5) list what is there (you should see both); "
   "(6) step back out and print where you are.",
   "", "pwd\n# your commands here", "pwd\nmkdir practice\ncd practice\nmkdir data results\nls\ncd ..\npwd", kind="manual", lang="bash")

ex(0, "e11b", "Make and use a second environment",
   "Create an environment called <code>test-env</code> with Python in it, activate it, run <code>pip list</code> and notice how short the list is, then go back to <code>pybio</code> and delete <code>test-env</code>.",
   "", "# your commands here",
   "conda create -n test-env python=3.12 -y\nconda activate test-env\npip list\nconda deactivate\nconda activate pybio\nconda remove -n test-env --all -y", kind="manual", lang="bash")

ex(6, "e12a", "Build the project folders",
   "Create the folders from the layout above, then run <code>ls</code> to check them. Paste the output into the puzzle below when you are done.",
   "", "# your commands here",
   "mkdir -p data/raw data/derived notebooks results/figures\nls", kind="manual", lang="bash")

ex(13, "e13a", "Run your own script",
   "Make a file called <code>hello.py</code> containing <code>print(\"Hello from a script\")</code>, and run it from the terminal with <code>python hello.py</code>.",
   "", "# your commands here", 'echo \'print("Hello from a script")\' > hello.py\npython hello.py', kind="manual", lang="bash")

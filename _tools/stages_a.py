from qbuild import *
from qbuild import answer_hash

BASE = "https://atharvabhagwat.dev/assets/data/"
STAGES = {}   # key -> stage html


def add(key, title, promise, blocks, puzzles):
    """title is shown as the page title; the stage() helper needs a heading, we reuse it."""
    STAGES[key] = stage(key, title, "", 0, promise, blocks, puzzles)


# ======================================================================= Stage 0: Python building blocks
SEQS = {
    "geneA": "ATGAAATTTAAAGAAATTATTAAAGAAGTTAAAAAA",
    "geneB": "ATGGGCGCCGGCCGCGCCGGGCCCGGCGCCGCCGGC",
    "geneC": "ATGACCGAATGGCTGTAATGCCGTAACGAT",
    "geneD": "ATGGTGCTGAGCCCGGAAGATAAAACCAACGTG",
}
SEQ_LINES = ",\n    ".join(f'"{s}"' for s in SEQS.values())

add(12, "Python building blocks", "Learn the small pieces everything else is built from: values, lists, dictionaries, libraries and tables.", [
    p("Every analysis in this guide is made of a few small pieces. In this stage you will meet them one at a time, from the simplest to the most useful, and see how each one leads to the next:"),
    table(["Step", "What it is", "Example"], [
        ["<strong>1. value</strong>", "One thing: a number, some text, or yes/no.", "<code>length = 30</code>"],
        ["<strong>2. list</strong>", "Several values in order.", "<code>[36, 36, 30, 33]</code>"],
        ["<strong>3. dictionary</strong>", "Values with names attached.", "<code>{\"geneA\": 36}</code>"],
        ["<strong>4. library</strong>", "Extra tools other people wrote, such as numpy.", "<code>np.mean(lengths)</code>"],
        ["<strong>5. table</strong>", "Rows and columns, like a spreadsheet (pandas).", "<code>genes[\"length\"]</code>"],
    ]),
    h3("Step 1: values"),
    p("A <strong>variable</strong> is a name that holds a value. The <code>=</code> sign means \"store this under that name\". Text always goes inside quotes."),
    code('gene = "geneC"            # text\nlength = 30               # a whole number\nis_long = length > 32     # True or False\nprint(gene, length, is_long)', "python", "run this", test="z0_values"),
    h3("Step 2: lists"),
    p("A <strong>list</strong> holds several values in order, inside square brackets. Counting starts at 0, not 1."),
    code('names = ["geneA", "geneB", "geneC", "geneD"]\nlengths = [36, 36, 30, 33]\n\nprint(names[0])       # the first item\nprint(lengths[2])     # the third item\nprint(len(lengths))   # how many items', "python", "run this", test="z0_lists"),
    h3("Step 3: dictionaries"),
    p("A <strong>dictionary</strong> keeps values under names, so you can look things up by name instead of by position. It uses curly brackets <code>{ }</code>, with <code>name: value</code> pairs."),
    code('length_of = {"geneA": 36, "geneB": 36, "geneC": 30, "geneD": 33}\n\nprint(length_of["geneB"])', "python", "run this", test="z0_dict"),
    h3("Step 4: libraries"),
    p("Python on its own is small. A <strong>library</strong> is a collection of extra tools that other people wrote and shared. You load one with <code>import</code>. "
      "Here is <strong>numpy</strong>, a library for numbers. You do not need to memorise it: just see how it is used."),
    code('import numpy as np\n\nlengths = [36, 36, 30, 33]\n\nprint(np.mean(lengths))     # the average\nprint(np.max(lengths))      # the biggest\nprint(np.sum(lengths))      # the total', "python", "run this", test="z0_numpy"),
    callout("tip", "Where to look things up",
            p("Nobody remembers every function. Learn where to look:")
            + ul(['Every library has an official <strong>documentation</strong> website, for example <a href="https://numpy.org/doc/stable/" target="_blank" rel="noopener">numpy.org/doc</a>, '
                  '<a href="https://pandas.pydata.org/docs/" target="_blank" rel="noopener">pandas.pydata.org/docs</a>, '
                  '<a href="https://matplotlib.org/stable/" target="_blank" rel="noopener">matplotlib.org</a> and <a href="https://seaborn.pydata.org/" target="_blank" rel="noopener">seaborn.pydata.org</a>.',
                  "In a notebook, <code>help(np.mean)</code> shows the built-in instructions for that function.",
                  "Searching the web for <em>pandas filter rows</em> usually finds what you need. On a documentation page, read the one-line summary first, then look for the <em>Examples</em>."])),
    h3("Step 5: tables with pandas"),
    p("<strong>pandas</strong> is the library for tables. A table is called a <strong>DataFrame</strong>: rows are things you measured, columns are what you measured about them. "
      "Here is a table of four short DNA sequences. Notice that you build it from the lists and dictionaries you just learned."),
    code('import pandas as pd\n\ngenes = pd.DataFrame({\n    "gene": ["geneA", "geneB", "geneC", "geneD"],\n    "sequence": [\n    ' + SEQ_LINES + ',\n    ],\n})\ngenes', "python", "run this", test="z0_table"),
    p("A new column is just maths on an existing column. Here we count letters, then work out the <strong>GC fraction</strong>: the share of letters that are G or C."),
    code('genes["length"] = genes["sequence"].str.len()\ngenes["g"] = genes["sequence"].str.count("G")\ngenes["c"] = genes["sequence"].str.count("C")\ngenes["gc"] = (genes["g"] + genes["c"]) / genes["length"]\ngenes', "python", "run this", test="z0_cols"),
    p("To keep only some rows, put a condition inside square brackets. The condition gives True or False for every row, and only the True rows stay."),
    code('genes[genes["gc"] > 0.5]', "python", "run this", test="z0_filter"),
    callout("why", "How the steps connect",
            p("A table column is a list with a name. A table is several columns that share the same rows. A library is where the tools for working with them live. "
              "Everything later in this guide is these five steps used on bigger data.")),
], [
    puzzle("s12p1", 1,
           p("Using your <code>genes</code> table, what is the <strong>GC fraction</strong> of <code>geneC</code>, to 3 decimal places?"),
           kind="number", placeholder="3 decimal places", spec={"kind": "num", "value": 0.466667, "dp": 3},
           hint="Keep the row where <code>gene</code> equals <code>\"geneC\"</code> and look at its <code>gc</code> column.",
           solution='print(genes[genes["gene"] == "geneC"]["gc"])', test="z0p1"),
    puzzle("s12p2", 2,
           p("How many of the four genes have a GC fraction <strong>above 0.5</strong>?"),
           kind="number", placeholder="a whole number", spec={"kind": "int", "h": answer_hash("s12p2", "2")},
           hint="The filter in the last cell shows exactly those rows. Count them with <code>len(...)</code>.",
           solution='print(len(genes[genes["gc"] > 0.5]))', test="z0p2"),
])

# ======================================================================= Stage 1: notebooks, strings, loops
VARIANTS = '["p.Gly12Gly", "p.Trp18Ter", "p.Leu25Pro", "p.Val30Asp",\n            "p.Gln36Ter", "p.Ile40Asn", "p.Ser45Thr", "p.Gly46Arg"]'

add(1, "Notebooks, text and loops", "How notebooks work, why the kernel's memory matters, and how to work with text and repeat things.", [
    p("A <strong>notebook</strong> mixes code, results and notes in one document. It is made of <strong>cells</strong>. A code cell holds Python and shows its result underneath. A text cell holds notes, headings and reminders for yourself."),
    callout("tip", "Keyboard shortcuts worth learning today",
            ul(["<kbd>Shift</kbd>+<kbd>Enter</kbd>: run the cell and move to the next one (Colab and VS Code).",
                "Colab: <kbd>Ctrl</kbd>/<kbd>Cmd</kbd>+<kbd>M</kbd> then <kbd>B</kbd> adds a cell below, then <kbd>D</kbd> deletes a cell.",
                "In both, the <strong>+ Code</strong> and <strong>+ Text</strong> buttons add cells."])),
    h3("The kernel has a memory"),
    p("Behind every notebook runs a <strong>kernel</strong>: a Python program that does the work. When you run a cell, the kernel runs it and <strong>remembers</strong> the variables you created. "
      "The notebook shows the code; the kernel holds the values. They can disagree. Try it with two cells:"),
    code("x = 10", "python", "cell 1", test="z1_mem1"),
    code("print(x * 2)", "python", "cell 2", test="z1_mem2"),
    p("Run both and you get <code>20</code>. Now change cell 1 to <code>x = 100</code> but <strong>do not run it</strong>, and run cell 2 again. Still <code>20</code>: the page says 100, but the kernel still remembers 10."),
    h3("When things go wrong with memory"),
    table(["What you see", "Why it happens", "What to do"], [
        ["An old value shows up after you edited a cell", "You changed the code but did not run it again.", "Run the cell, and the cells below it."],
        ["<code>NameError: name 'df' is not defined</code>", "The cell that creates it has not run in this session (new session, restart, or you skipped it).", "Run the cells above it, or <strong>Run all</strong>."],
        ["A number grows every time you run a cell", "Cells like <code>count = count + 1</code> add again each run.", "Run the cell that sets <code>count = 0</code> first, or restart."],
        ["Results that do not match your code", "You ran cells in a different order than they appear.", "<strong>Restart and run all</strong>."],
        ["Colab says it ran out of memory, or the session crashed", "The data was too big for the free machine, or the session was idle too long.", "Restart the session. Work on a smaller piece of the data first."],
    ]),
    callout("why", "Restart, then run everything",
            p("A notebook is only trustworthy if it works from the top, in order, in a fresh kernel. Before you believe a result or share a notebook, restart and run all. "
              "In Colab: <strong>Runtime, Restart session and run all</strong>. In VS Code: the <strong>Restart</strong> button, then <strong>Run All</strong>.")
            + ul(["<strong>Restart</strong> clears the kernel's memory (all variables). Your code and notes stay.",
                  "Colab also forgets everything when a session ends: variables, and any files you uploaded. Save your notebook to Drive.",
                  "You do not need to clear memory often. Restart when results look wrong, after big edits near the top, or when the notebook feels stuck."])),
    h3("Text"),
    p("Text in Python is called a <strong>string</strong>. A <strong>slice</strong> <code>text[start:stop]</code> takes letters from <code>start</code> up to, but not including, <code>stop</code>. Counting starts at 0, and negative numbers count from the end."),
    code('name = "p.Trp18Ter"\n\nprint(name[2:5])      # Trp\nprint(name[5:7])      # 18\nprint(name[-3:])      # Ter\nprint(len(name))      # how many letters\nprint(name.upper())   # capital letters', "python", "run this", test="z1_text"),
    p("Text can be turned into a number with <code>int()</code>, which lets you do maths with it:"),
    code('position = int(name[5:7])\nprint(position + 1)', "python", "run this", test="z1_int"),
    h3("Comparisons and decisions"),
    p("A <strong>comparison</strong> asks a yes/no question. <code>==</code> means \"is equal to\" (one <code>=</code> stores a value, two ask a question). Others: <code>!=</code> not equal, <code>&lt;</code> <code>&gt;</code> less or more, <code>&lt;=</code> <code>&gt;=</code> at most or at least. "
      "<code>if</code> runs some code only when the answer is yes:"),
    code('score = 1.4\n\nif score < 0.5:\n    print("low")\nelif score < 1.0:\n    print("in between")\nelse:\n    print("like the reference")', "python", "run this", test="z1_if"),
    h3("Loops"),
    p("A <strong>loop</strong> repeats code once for each item in a list. Read it aloud: <em>for each variant in the list, do this.</em> The indented lines are inside the loop."),
    code('variants = ' + VARIANTS + '\n\nfor variant in variants:\n    print(variant, len(variant))', "python", "run this", test="z1_loop"),
], [
    puzzle("s1p1", 1,
           p("In the <code>variants</code> list above, every name has the position in letters 5 up to (not including) the last 3. Use a loop and <code>int()</code> to add all the positions together. What is the total?"),
           kind="number", placeholder="a whole number", spec=None,
           hint="Start with <code>total = 0</code>. In the loop, add <code>int(variant[5:-3])</code> to <code>total</code>. Print <code>total</code> after the loop.",
           solution='variants = ' + VARIANTS + '\n\ntotal = 0\nfor variant in variants:\n    total = total + int(variant[5:-3])\nprint(total)', test="z1p1"),
    puzzle("s1p2", 2,
           p("Sort each variant into a kind: <strong>synonymous</strong> if the old and new amino acid letters (<code>variant[2:5]</code> and <code>variant[-3:]</code>) are the same, "
             "<strong>nonsense</strong> if the new one is <code>Ter</code>, otherwise <strong>missense</strong>. Count each kind and type the three counts in that order, separated by commas."),
           kind="text", placeholder="e.g. 3,4,1",
           hint="Keep three counters at 0. In the loop use <code>if</code>, <code>elif</code> and <code>else</code> to add 1 to the right one. Print them at the end.",
           solution='variants = ' + VARIANTS + '\n\nsyn = 0\nnon = 0\nmis = 0\nfor variant in variants:\n    if variant[2:5] == variant[-3:]:\n        syn = syn + 1\n    elif variant[-3:] == "Ter":\n        non = non + 1\n    else:\n        mis = mis + 1\nprint(syn, non, mis)', test="z1p2"),
])

# ======================================================================= Stage 2: reading error messages
add(2, "Reading error messages", "Everyone sees red error text all day. The skill is reading it quickly, and it is easier than it looks.", [
    p("An error message is the computer telling you, as clearly as it can, where it got stuck and why. Here is a real one:"),
    '<div class="q-trace"><pre><code>'
    '<span class="t-dim">---------------------------------------------------------------------------</span>\n'
    '<span class="t-err">KeyError</span><span class="t-dim">                                  Traceback (most recent call last)</span>\n'
    '<span class="t-dim">Cell In[4], </span><span class="t-line">line 2</span>\n'
    '<span class="t-dim">      1 df = pd.read_csv("toy.csv")</span>\n'
    '<span class="t-arrow">----&gt; 2</span> <span class="t-hot">print(df["Score"].mean())</span>\n'
    '\n'
    '<span class="t-dim">... (many lines from inside pandas) ...</span>\n'
    '\n'
    '<span class="t-err">KeyError: \'Score\'</span>'
    '</code></pre></div>',
    ol([
        "<strong>Start at the bottom.</strong> <code>KeyError: 'Score'</code> says you asked for something by name and it is not there. The first word is the kind of error; the rest is the detail.",
        "<strong>Find your line.</strong> The arrow <code>----&gt; 2</code> points at <em>your</em> code. Ignore the middle section: it is the library's own code, and the mistake is almost never there.",
        "<strong>Check what you assumed.</strong> Which column names really exist? <code>print(df.columns)</code> shows them, and you will see <code>score</code> with a small s. Names must match exactly.",
    ]),
    h3("The usual errors"),
    table(["Error", "In plain English", "First thing to try"], [
        ["<code>SyntaxError</code>", "Python could not read the line. Often a missing colon, bracket or quote.", "Look at the marked line and the one above it."],
        ["<code>NameError</code>", "You used a name Python does not know.", "A typo? Or the cell that creates it has not run (kernel memory)."],
        ["<code>TypeError</code>", "The wrong kind of thing, such as adding text to a number.", "<code>print(type(x))</code> for each thing involved."],
        ["<code>ValueError</code>", "The right kind of thing, but a value it cannot use, such as <code>int(\"abc\")</code>.", "Print the value you passed in."],
        ["<code>KeyError</code>", "A column or dictionary key is not there.", "<code>print(df.columns)</code>. Check spelling and capital letters."],
        ["<code>IndexError</code>", "You asked for item 10 of a list with 5 items.", "<code>print(len(my_list))</code>."],
        ["<code>FileNotFoundError</code>", "The path points to nothing.", "Check the file name and which folder you are in."],
        ["<code>ModuleNotFoundError</code>", "The library is not installed here.", "In Colab, run <code>%pip install name</code>."],
    ]),
    h3("A routine that works"),
    ol([
        "Read the last line slowly.",
        "Go to the line the arrow points at. Is it what you meant to write?",
        "Check what you assumed: <code>print(type(x))</code>, <code>print(df.shape)</code>, <code>print(df.columns)</code>.",
        "Make the problem smaller: try it on two lines in a fresh cell.",
        "Suspect the kernel. Restart and run all.",
        "Search the web with the error type and the library, for example <em>pandas KeyError column</em>, and read why it happens before copying a fix.",
    ]),
    callout("why", "Loud errors are the good ones",
            p("The worst bugs give no error at all, just a wrong number. Get in the habit of checking your results: print the number of rows, look at the first few rows, and ask whether the answer is plausible.")),
    callout("tip", "Errors arrive one at a time",
            p("Fixing one error often reveals the next. That is progress. A <code>SyntaxError</code> always comes first, because Python reads the whole cell before running any of it.")),
], [
    puzzle("s2p1", 1, p("Pick the best answer for each."), kind="choices",
           choices=[
               ("Which line of an error message tells you <em>what</em> went wrong?", ["The first line", "The last line", "The longest line"]),
               ("<code>KeyError: 'Score'</code> after <code>df[\"Score\"]</code>. The file's column is called <code>score</code>. What is the fix?",
                ["Reinstall pandas", "Use <code>df[\"score\"]</code>. Names must match exactly.", "Restart the computer"]),
               ("You uploaded <code>toy.csv</code> in Colab, and <code>pd.read_csv(\"data/raw/toy.csv\")</code> gives <code>FileNotFoundError</code>. Most likely cause?",
                ["The CSV is corrupted", "pandas cannot read CSV files", "There is no <code>data/raw/</code> folder, only <code>toy.csv</code> itself, so the path is wrong"]),
               ("<code>total = 0</code>, then <code>for s in [\"1.5\", \"2.5\"]: total = total + s</code> gives a <code>TypeError</code>. What is <code>s</code>?",
                ["Text, so number + text fails", "A number", "Nothing"]),
           ],
           spec={"kind": "choices", "hs": [answer_hash(f"s2p1-{i}", c) for i, c in enumerate("bbca")]},
           hint="Question 2: compare the name in the error with the real column name, letter by letter."),
    puzzle("s2p2", 2,
           p("This code has three bugs. Paste it into a cell, run it, and fix what each error tells you, one at a time. When it works it prints an average. What is that average, to 3 decimal places?")
           + code('scores = [3.45, 1.55, 2.18, 2.59, 3.82]\n\ntotal = 0\nfor s in scores\n    total = total + s\n\nmean = total / len(score)\nprint("average: " + mean)', "python", "paste into a cell"),
           kind="number", placeholder="3 decimal places", spec={"kind": "num", "value": 2.718, "dp": 3},
           hint="Expect three different errors, in this order: <code>SyntaxError</code> (something missing at the end of a line), <code>NameError</code> (one name is misspelled), then <code>TypeError</code> (you cannot join text and a number with +). For the last one, print the number on its own: <code>print(\"average:\", mean)</code>.",
           solution='scores = [3.45, 1.55, 2.18, 2.59, 3.82]\n\ntotal = 0\nfor s in scores:\n    total = total + s\n\nmean = total / len(scores)\nprint("average:", mean)', test="z2p2"),
])

# ======================================================================= Stage 3: tables with pandas
TOYURL = BASE + "toy_vampseq_bin_counts.csv"

add(3, "Tables with pandas", "Load a table, look around, pick columns and keep only the rows you want.", [
    p("This stage uses a small made-up experiment. Each <em>row</em> is one named item measured once. The four columns <code>bin1_count</code> to <code>bin4_count</code> say how many reads fell into four brightness buckets, from the lowest signal (bin 1) to the highest (bin 4). You do not need to know where the numbers came from: the point is learning to work with a table."),
    h3("Load the table"),
    p("<code>pd.read_csv</code> reads a CSV file (a plain-text table) into a DataFrame. It can read straight from a web address:"),
    code('import pandas as pd\n\ndf = pd.read_csv("' + TOYURL + '")\ndf', "python", "run this", test="z3_load"),
    h3("Look before you touch"),
    p("Before doing anything, find out what you have. Run each line in its own cell:"),
    code('df.head()                          # the first 5 rows\ndf.shape                           # (number of rows, number of columns)\ndf.columns                         # the column names\ndf.info()                          # types of each column, and missing values\ndf.describe()                      # averages, minimums and maximums\ndf["variant_type"].value_counts()  # how many rows of each kind', "python", "run these", test="z3_look"),
    h3("Pick columns"),
    code('print(df["variant"])                     # one column\nprint(df[["variant", "replicate"]])       # several columns: note the double brackets', "python", "run this", test="z3_cols"),
    h3("Keep only some rows"),
    p("A comparison on a column gives True or False for every row. Putting that inside square brackets keeps the True rows. This is called a <strong>filter</strong>, and you will use it constantly."),
    code('is_nonsense = df["variant_type"] == "nonsense"\ndf[is_nonsense]', "python", "run this", test="z3_filter1"),
    p("To combine two conditions use <code>&amp;</code> (and) or <code>|</code> (or), and put each condition in round brackets:"),
    code('df[(df["variant_type"] == "missense") & (df["replicate"] == 1)]', "python", "run this", test="z3_filter2"),
    callout("trap", "Use &amp;, not the word and",
            p("Writing <code>and</code> between two conditions gives <code>ValueError: The truth value of a Series is ambiguous</code>. "
              "Python's <code>and</code> wants one yes/no, but a column holds many. Use <code>&amp;</code>, and keep the round brackets.")),
    h3("Sort"),
    code('df.sort_values("bin1_count", ascending=False)   # biggest first', "python", "run this", test="z3_sort"),
    callout("tip", "Reading documentation",
            p('Open the page for <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html" target="_blank" rel="noopener"><code>DataFrame.sort_values</code></a>. '
              "Read the one-line summary, then <em>Parameters</em>, then jump to <em>Examples</em>. You do not need to understand all of it. In a notebook, <code>help(df.sort_values)</code> shows the same text.")),
], [
    puzzle("s3p1", 1, p("How many rows are <code>missense</code> <strong>and</strong> from <code>replicate</code> 2?"),
           kind="number", placeholder="a whole number", spec=None,
           hint="Two conditions joined with <code>&amp;</code>, each in round brackets. Then count the rows with <code>len(...)</code>.",
           solution='rows = df[(df["variant_type"] == "missense") & (df["replicate"] == 2)]\nprint(len(rows))', test="z3p1"),
    puzzle("s3p2", 2, p("Add up every number in the four <code>bin*_count</code> columns across the whole table. What is the total?"),
           kind="number", placeholder="a whole number", spec=None,
           hint="<code>df[\"bin1_count\"].sum()</code> adds up one column. Do that for all four columns and add the four answers.",
           solution='total = df["bin1_count"].sum() + df["bin2_count"].sum() + df["bin3_count"].sum() + df["bin4_count"].sum()\nprint(total)', test="z3p2"),
])

# ======================================================================= Stage 4: calculations and groups
add(4, "Calculations and groups", "Make new columns with maths, summarise by group, and line two replicates up side by side.", [
    p("Raw counts are hard to compare: one row has 20 reads, another has 700. A common fix is a <strong>weighted average</strong> of the bins. Bin 1 counts as 1, bin 2 as 2, and so on. "
      "A row with all its reads in bin 1 scores 1, all in bin 4 scores 4, and anything in between lands in between."),
    code("score = (1 x bin1 + 2 x bin2 + 3 x bin3 + 4 x bin4) / total reads", "text", "the idea"),
    h3("New columns are just maths on columns"),
    p("pandas does maths on a whole column at once, with no loop needed. First reload the table, then add two new columns."),
    code('import pandas as pd\n\ndf = pd.read_csv("' + TOYURL + '")\n\ndf["total_reads"] = df["bin1_count"] + df["bin2_count"] + df["bin3_count"] + df["bin4_count"]\n\ndf["score"] = (df["bin1_count"] * 1 + df["bin2_count"] * 2 + df["bin3_count"] * 3 + df["bin4_count"] * 4) / df["total_reads"]\n\ndf[["variant", "replicate", "total_reads", "score"]]', "python", "run this", test="z4_score"),
    callout("note", "This is our own score",
            p("We made this score ourselves for the toy table. The real PTEN table later has a different score, made by the original researchers. They are not the same thing, and you will see why in Stage 6.")),
    h3("Summarise by group"),
    p("<code>groupby</code> splits the table by a column, summarises each piece, and puts the answers together: <em>split, summarise, combine</em>."),
    code('print(df.groupby("variant_type")["score"].mean())    # average score per kind\nprint(df.groupby("variant")["score"].mean())         # average score per variant', "python", "run this", test="z4_group"),
    h3("Put the two replicates side by side"),
    p("Every variant was measured twice. A <strong>pivot</strong> turns that into one row per variant, with one column per replicate. Then you can compare them."),
    code('wide = df.pivot(index="variant", columns="replicate", values="score")\nwide', "python", "run this", test="z4_pivot"),
    code('wide["difference"] = (wide[1] - wide[2]).abs()      # how much the two replicates disagree\nwide.sort_values("difference", ascending=False)', "python", "run this", test="z4_diff"),
    callout("why", "Look before you average",
            p("If one variant's two replicates disagree a lot, ask why <em>before</em> averaging them. The answer is sometimes in a column you already have, such as how many reads it had.")),
], [
    puzzle("s4p1", 1, p("What is the average <code>score</code> of the <code>WT</code> rows (both replicates), to 2 decimal places?"),
           kind="number", placeholder="2 decimal places", spec=None,
           hint="Keep the rows where <code>variant</code> equals <code>\"WT\"</code>, take the <code>score</code> column, and use <code>.mean()</code>.",
           solution='print(df[df["variant"] == "WT"]["score"].mean())', test="z4p1"),
    puzzle("s4p2", 2, p("Which variant has the <strong>largest</strong> disagreement between replicate 1 and replicate 2? Type its name exactly as it appears."),
           kind="text", placeholder="p.Xxx00Yyy", spec=None,
           hint="Use the <code>wide</code> table and its <code>difference</code> column. Sort it, or use <code>wide[\"difference\"].idxmax()</code>. Then look at that variant's <code>total_reads</code>: should you trust it?",
           solution='print(wide["difference"].idxmax())', test="z4p2"),
])

# ======================================================================= Stage 5: functions
add(5, "Writing functions", "Turn code you use more than once into a function with a name, so you write it once and use it everywhere.", [
    p("In Stage 4 you scored the whole table. Next week you may want to score a different table, or ignore rows with too few reads. If you copy and paste the code, the copies drift apart and you forget which one you trust."),
    callout("why", "The rule of two",
            p("The second time you copy a block of code, turn it into a <strong>function</strong>. A function is a named recipe. Fix a mistake in one place and everything that uses it gets the fix.")),
    h3("A tiny function"),
    code('def double(number):\n    return number * 2\n\nprint(double(4))\nprint(double(10))', "python", "run this", test="z5_double"),
    ul(["<code>def</code> starts the recipe, then its name, then the <strong>parameters</strong> (the things you give it) in round brackets and a colon.",
        "The indented lines are the recipe.",
        "<code>return</code> hands the answer back.",
        "Calling it, <code>double(4)</code>, runs the recipe with 4."]),
    h3("Our scoring recipe as a function"),
    code('def add_scores(df, min_reads=0):\n    """Add total_reads and score columns. Rows with fewer than min_reads reads get no score."""\n    df = df.copy()    # work on a copy, so the original table is not changed\n    df["total_reads"] = df["bin1_count"] + df["bin2_count"] + df["bin3_count"] + df["bin4_count"]\n    df["score"] = (df["bin1_count"] * 1 + df["bin2_count"] * 2 + df["bin3_count"] * 3 + df["bin4_count"] * 4) / df["total_reads"]\n    df.loc[df["total_reads"] < min_reads, "score"] = None\n    return df', "python", "run this", test="z5_func"),
    ul(["<code>min_reads=0</code> is a parameter with a <strong>default</strong>: if you do not say otherwise, it is 0.",
        "The text in triple quotes is the <strong>docstring</strong>. It explains the function, and <code>help(add_scores)</code> shows it.",
        "<code>df.copy()</code> makes a copy, so the function never changes your original table."]),
    h3("Use it"),
    code('import pandas as pd\n\ntoy = pd.read_csv("' + TOYURL + '")\n\nscored = add_scores(toy)                    # no filtering\nstrict = add_scores(toy, min_reads=50)      # same recipe, one setting changed\n\nprint(scored[["variant", "replicate", "score"]].head())\nprint(strict["score"].isna().sum(), "rows have no score now")', "python", "run this", test="z5_use"),
    callout("tip", "Documentation is for your future self",
            ul(["Give things names that say what they are: <code>add_scores</code> is better than <code>func2</code>.",
                "A one-line docstring saying what the function does is enough.",
                "Write notes in text cells before each section: one sentence about the question and what you decided."])),
], [
    puzzle("s5p1", 1, p("Define <code>add_scores</code> and run it on the toy table. What is the <code>score</code> of <code>p.Ser45Thr</code> in <strong>replicate 1</strong>, to 3 decimal places?"),
           kind="number", placeholder="3 decimal places", spec=None,
           hint="Call <code>add_scores(toy)</code>, then filter the result on both <code>variant</code> and <code>replicate</code>, and look at the <code>score</code> column.",
           solution='scored = add_scores(toy)\nrow = scored[(scored["variant"] == "p.Ser45Thr") & (scored["replicate"] == 1)]\nprint(row["score"])', test="z5p1"),
    puzzle("s5p2", 2, p("Run the same function with <code>min_reads=50</code>. Among the <code>missense</code> rows, what is the average <code>score</code> now, to 3 decimal places? (Rows with no score are skipped when pandas averages.)"),
           kind="number", placeholder="3 decimal places", spec=None,
           hint="<code>strict = add_scores(toy, min_reads=50)</code>, then keep the missense rows and take the mean of <code>score</code>.",
           solution='strict = add_scores(toy, min_reads=50)\nmissense = strict[strict["variant_type"] == "missense"]\nprint(missense["score"].mean())', test="z5p2"),
])

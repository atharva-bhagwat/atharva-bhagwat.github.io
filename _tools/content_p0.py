from qbuild import *
from qbuild import answer_hash

FASTA_TEXT = """>geneA low-GC test gene
ATGAAATTTAAAGAAATTATTAAAGAAGTTAAAAAA
>geneB high-GC test gene
ATGGGCGCCGGCCGCGCCGGGCCCGGCGCCGCCGGC
>geneC contains an early stop codon
ATGACCGAATGGCTGTAATGCCGTAACGAT
>geneD mixed test gene
ATGGTGCTGAGCCCGGAAGATAAAACC
AACGTG
"""

STAGES_P0 = []

LADDER = table(["Rung", "What it is", "Example", "What it gives you"], [
    ["<strong>value</strong>", "One thing: a number, some text, a yes/no.", "<code>length = 36</code>", "The atoms. Everything else is built from these."],
    ["<strong>list</strong>", "An ordered pile of values.", "<code>lengths = [36, 36, 30, 33]</code>", "Loop over it, count it, slice it."],
    ["<strong>dictionary</strong>", "Labelled values: look things up by name.", "<code>{\"geneA\": 36}</code>", "Names attached to data."],
    ["<strong>numpy array</strong>", "A list built for fast maths on every element at once.", "<code>np.array(lengths) / 3</code>", "No loops: whole-column arithmetic."],
    ["<strong>pandas Series</strong>", "An array that also has labels.", "<code>pd.Series(lengths, index=names)</code>", "Maths <em>and</em> lookup by name."],
    ["<strong>pandas DataFrame</strong>", "Several Series sharing one set of labels: a table.", "<code>pd.DataFrame({\"length\": ..., \"gc\": ...})</code>", "Filter, group, summarise, plot. Everything in this guide."],
])

STAGES_P0.append(stage(
    12, "Project 0", "from Python basics to your first analysis", 75,
    "You will climb from a single value to a full table of data, using DNA sequences as the thing to analyse. By the end you will see how every idea connects to the next.",
    [
        p("Most introductions teach Python's pieces one at a time and never show how they fit together. Here, the pieces are rungs on one ladder, and each rung is built from the one below:"),
        LADDER,
        p("The Colab notebook for this stage has each rung as a short section with blanks to fill in. The page below explains the thinking, and you can try the same code in the notebook. "
          "Everything runs on Colab's computers, so there is nothing to install and nothing to break."),
        h3("Rung 1 and 2: values, lists and dictionaries"),
        code('gene = "geneC"            # text (a string)\nlength = 30                # a whole number (an int)\nis_long = length > 32      # True or False (a bool)\nprint(gene, length, is_long)',
             "python", "values", test="p0_values"),
        p("A <strong>list</strong> holds many values in order. A <strong>dictionary</strong> stores values under names, which is how you answer questions like \"what is the length of geneB?\" without remembering a position."),
        code('names = ["geneA", "geneB", "geneC", "geneD"]\nlengths = [36, 36, 30, 33]\n\nlengths[0], lengths[-1], len(lengths)       # first, last, how many\n\nlength_of = dict(zip(names, lengths))        # {"geneA": 36, ...}\nlength_of["geneB"]\n\nfor name in names:\n    print(name, length_of[name] // 3, "codons")',
             "python", "lists and dictionaries", test="p0_lists"),
        h3("Rung 3: libraries and numpy"),
        p("Python itself is small on purpose. A <strong>library</strong> is a package of extra tools you load with <code>import</code>. "
          "Why bother? Compare computing every length divided by three with a loop versus with <strong>numpy</strong>:"),
        code('import numpy as np\n\n# the loop way\ncodons = []\nfor n in lengths:\n    codons.append(n / 3)\n\n# the numpy way: the whole list at once\narr = np.array(lengths)\narr / 3\n\narr.mean(), arr.max(), arr[arr > 31]      # summaries, and a filter',
             "python", "numpy", test="p0_numpy"),
        callout("why", "This is the idea behind pandas",
                p("Doing maths on a whole collection at once is called <strong>vectorising</strong>. It is shorter, easier to read and much faster than a loop. "
                  "pandas takes the same idea and adds <em>labels</em>.")),
        h3("Rung 4 and 5: from arrays to tables"),
        code('import pandas as pd\n\ns = pd.Series(lengths, index=names)       # an array with labels\ns["geneB"], s.mean()\n\ntable = pd.DataFrame({"length": lengths}, index=names)\ntable["codons"] = table["length"] // 3    # a new column is just maths on a column\ntable',
             "python", "pandas", test="p0_pandas"),
        p("A DataFrame is a bundle of Series that share the same row labels. Selecting a column gives you a Series back, and everything you did with arrays works on it. "
          "That is why <code>df[\"score\"] * 2</code> or <code>df[df[\"score\"] &gt; 1]</code> look so natural in later stages."),
        h3("A taste of Biopython: sequences as objects"),
        p("DNA is text, but treating it as plain text means rewriting reverse-complement and translation yourself. "
          '<a href="https://biopython.org/" target="_blank" rel="noopener">Biopython</a> is a library with biology-aware tools. Install it (in Colab, once per session) and meet its <code>Seq</code> object, which behaves like a string you already know how to slice:'),
        code('%pip install -q biopython', "python", "Colab cell (Colab may already have it)"),
        code('from Bio.Seq import Seq\n\ndna = Seq("ATGACCGAATGGCTGTAATGCCGTAACGAT")\nlen(dna), dna[:6]              # sliced just like a string\ndna.reverse_complement()        # the other strand, read backwards\ndna.translate()                 # DNA to protein; * marks a stop\ndna.translate(to_stop=True)     # stop reading at the first stop',
             "python", "Seq objects", test="p0_seq"),
        p("Real sequences live in <strong>FASTA</strong> files: a line starting with <code>&gt;</code> naming the sequence, then its letters. "
          "<code>SeqIO.parse</code> reads them. Here the file is a text string so you do not need to upload anything:"),
        code('FASTA = """' + FASTA_TEXT + '"""', "python", "a tiny FASTA file", test="p0_fasta"),
        code('from io import StringIO\nfrom Bio import SeqIO\nfrom Bio.SeqUtils import gc_fraction\n\nrecords = []\nfor rec in SeqIO.parse(StringIO(FASTA), "fasta"):\n    records.append({\n        "id": rec.id,\n        "length": len(rec.seq),\n        "gc": gc_fraction(rec.seq),\n        "protein": str(rec.seq.translate()),\n        "protein_len": len(rec.seq.translate(to_stop=True)),\n    })\nrecords[0]',
             "python", "reading FASTA", test="p0_records"),
        h3("Closing the loop: sequences to DataFrame to answer"),
        p("Look at what <code>records</code> is: a <strong>list</strong> of <strong>dictionaries</strong>. That is exactly the shape a DataFrame wants. "
          "The ladder just closed: Biopython objects, to dictionaries, to a list, to a table you can filter and plot."),
        code('seqs = pd.DataFrame(records)\nseqs\n\nseqs[seqs["gc"] > 0.5]                       # filter, like Stage 3\nseqs.sort_values("gc", ascending=False)\nseqs.plot.bar(x="id", y="gc", legend=False)    # a first chart',
             "python", "a table of sequences", test="p0_table"),
        callout("tip", "Reading a whole new library",
                p("You will not remember every function in numpy, pandas or Biopython, and nobody does. The skill is knowing the ladder: what type of thing do I have, "
                  "what can that type do, and where do I look it up (the library's documentation, and <code>help(thing)</code>)?")),
    ],
    [
        puzzle("s12p1", 1,
               p("Run the code above on the FASTA text. What is the <strong>GC fraction</strong> (share of G and C letters) of <code>geneC</code>, to 3 decimal places?"),
               kind="number", placeholder="3 decimal places",
               spec={"kind": "num", "value": 0.466667, "dp": 3},
               hint="Look at the <code>gc</code> column of your <code>seqs</code> table, or use <code>gc_fraction</code> on <code>geneC</code>'s sequence.",
               solution='print(round(seqs.loc[seqs["id"] == "geneC", "gc"].iloc[0], 3))', test="p0p1"),
        puzzle("s12p2", 2,
               p("Translate each gene and stop reading at the first stop codon (<code>to_stop=True</code>). Adding up the protein lengths of all four genes, how many amino acids is that in total?"),
               kind="number", placeholder="a whole number",
               spec={"kind": "int", "h": answer_hash("s12p2", "40")},
               hint="The <code>protein_len</code> column already holds each length. Add the column up with <code>.sum()</code>. Notice that <code>geneC</code> is shorter than its DNA suggests, and ask yourself why.",
               solution='print(seqs["protein_len"].sum())', test="p0p2"),
    ],
))

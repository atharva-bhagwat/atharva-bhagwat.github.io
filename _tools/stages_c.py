from qbuild import *
from qbuild import answer_hash

BASE = "https://atharvabhagwat.dev/assets/data/"
STAGES = {}
ENV = "pybio"
PROJECT = "pybio-project"


def add(key, title, promise, blocks, puzzles):
    STAGES[key] = stage(key, title, "", 0, promise, blocks, puzzles)


MINICONDA_MAC = ("uname -m\n\n# Apple silicon Mac (the answer was arm64):\nURL=https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh\n"
                 "# Intel Mac (x86_64): use this line instead\n# URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh\n"
                 "# Linux: use this line instead\n# URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh\n\n"
                 "mkdir -p ~/miniconda3\ncurl -L $URL -o ~/miniconda3/miniconda.sh\nbash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3\nrm ~/miniconda3/miniconda.sh\n\n~/miniconda3/bin/conda init bash zsh")
MINICONDA_WIN = ('Invoke-WebRequest -Uri "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile ".\\miniconda.exe"\n'
                 'Start-Process -FilePath ".\\miniconda.exe" -ArgumentList "/InstallationType=JustMe","/RegisterPython=0","/S","/D=$env:USERPROFILE\\miniconda3" -Wait\n'
                 'Remove-Item ".\\miniconda.exe"\n\n& "$env:USERPROFILE\\miniconda3\\Scripts\\conda.exe" init powershell')

# ======================================================================= Stage 0 (Part 2): setting up your computer
add(0, "Setting up your computer", "Install Python tools on your own machine, once, so your work lasts and you can run bigger jobs.", [
    p("In Part 1 you worked in Colab, where everything was ready. That is the best way to learn, but it has limits: sessions reset and your files disappear, big datasets do not fit, and you cannot rebuild exactly the same setup next year. "
      "Your own computer fixes all of these, and it needs a little setup, once."),
    h3("Terminal first aid"),
    p("The <strong>terminal</strong> is a window where you type commands instead of clicking. It only does what you tell it. Open it now: <strong>Terminal</strong> on macOS (press <kbd>Cmd</kbd>+<kbd>Space</kbd>, type Terminal), "
      "<strong>PowerShell</strong> on Windows (Start menu, type PowerShell). End every line with <kbd>Enter</kbd>."),
    p("A terminal is always standing in one folder, called the <strong>working directory</strong>. These commands cover most of what you will need:"),
    table(["Command", "What it does"], [
        ["<code>pwd</code>", "Print the folder you are standing in."],
        ["<code>ls</code>", "List what is in this folder."],
        ["<code>cd folder_name</code>", "Step into a folder. <code>cd ..</code> steps back out."],
        ["<code>mkdir new_folder</code>", "Make a new folder."],
        ["<code>python script.py</code>", "Run a Python file."],
    ]),
    ul(["Press <kbd>Tab</kbd> after typing the first letters of a name and the terminal finishes it.",
        "Press <kbd>&uarr;</kbd> to bring back the last command. Press <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop something that is running.",
        "A command that prints nothing usually worked. An error message is read exactly like in Stage 2: start at the last line."]),
    h3("1. Install VS Code"),
    p('Download it from <a href="https://code.visualstudio.com/" target="_blank" rel="noopener">code.visualstudio.com</a> and run the installer. VS Code is an editor where you write scripts, run notebooks, browse files and use a terminal in one window.'),
    h3("2. Install Miniconda from the terminal"),
    p("<strong>conda</strong> makes <strong>environments</strong>: separate boxes, each with its own Python and its own libraries. A project can use one version of pandas while another project uses a different one, and neither breaks the other. "
      "<strong>Miniconda</strong> is the small installer. On a Mac, first type <code>uname -m</code>: <code>arm64</code> means Apple silicon, <code>x86_64</code> means Intel."),
    os_code(MINICONDA_MAC, MINICONDA_WIN, "bash", "powershell", "macOS / Linux terminal", "Windows (PowerShell)"),
    p("The last line connects conda to your terminal. <strong>Close the terminal completely and open a new one.</strong> The prompt should now start with <code>(base)</code>. Check:"),
    code("conda --version", "bash", "terminal"),
    callout("trap", "Windows: \"running scripts is disabled on this system\"",
            p("PowerShell blocks conda's startup file. Run <code>Set-ExecutionPolicy -Scope CurrentUser RemoteSigned</code>, answer Y, then open a new PowerShell window.")),
    callout("trap", "conda mentions \"Terms of Service\"",
            p("Newer conda versions may ask you to accept terms before installing packages. The message prints the exact command to run. Copy it, run it, then repeat your first command.")),
    h3("3. Make an environment"),
    p("Name it something short. We use <code>" + ENV + "</code>. This one command makes it and installs the libraries you used in Part 1:"),
    code("conda create -n " + ENV + " -c conda-forge python=3.12 pandas numpy matplotlib seaborn scipy ipykernel -y", "bash", "terminal"),
    p("Switch into it with <code>activate</code>. Do this every time you open a new terminal. The prompt now starts with <code>(" + ENV + ")</code>. If that prefix is missing, you are not inside the environment."),
    code("conda activate " + ENV + "\nconda env list", "bash", "terminal"),
    p("<code>conda env list</code> shows every environment you have, with a star next to the active one."),
    h3("4. See what is installed, and add more"),
    p("<code>pip</code> is the tool that installs Python libraries. <code>pip list</code> shows everything in the active environment, with version numbers:"),
    code("pip list", "bash", "terminal"),
    p("To add a library, use <code>pip install</code> and its name. For example, Biopython, which you will use in the optional DNA stage at the end:"),
    code("pip install biopython\npip list", "bash", "terminal"),
    p("Run <code>pip list</code> again and <code>biopython</code> is now in the list. To remove a library: <code>pip uninstall biopython</code>."),
    h3("5. Save and share an environment"),
    p("Six months from now, or on a colleague's laptop, you will want exactly the same setup. There are two files for that."),
    p("<strong>environment.yml</strong> describes a whole conda environment. A <strong>YAML</strong> file is just a plain text file of settings written as <code>name: value</code> and lists with dashes. conda writes it for you:"),
    code("conda env export --from-history > environment.yml", "bash", "terminal"),
    p("Open <code>environment.yml</code> in VS Code to read it. It names the environment, the places packages come from, and the packages you asked for. Anyone can rebuild your environment from it:"),
    code("conda env create -f environment.yml", "bash", "terminal"),
    p("<strong>requirements.txt</strong> is the plainer cousin: just a list of Python libraries, one per line. <code>pip</code> writes and reads it:"),
    code("pip freeze > requirements.txt\npip install -r requirements.txt", "bash", "terminal"),
    ul(["<code>&gt;</code> means \"put the output into this file\".",
        "<code>-f</code> means \"from this file\", and <code>-r</code> means \"read this list\".",
        "Use <code>environment.yml</code> when others use conda, and <code>requirements.txt</code> when they only use pip. Many projects keep both."]),
    h3("6. Add VS Code extensions"),
    p("An <strong>extension</strong> teaches VS Code new skills. You install them with a few clicks:"),
    ol(["Click the <strong>Extensions</strong> icon in the bar on the far left (four squares, one drifting away). Or use the menu <strong>View, then Extensions</strong>. Shortcut: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd> (<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd> on Mac).",
        "Click the search box at the top. It says <em>Search Extensions in Marketplace</em>.",
        "Type the name from the table below, for example <code>Python</code>.",
        "Check the <strong>publisher</strong> under the title and the download count (good ones have millions or hundreds of thousands).",
        "Click the blue <strong>Install</strong> button. When it changes to a gear icon, it worked. If you see a <strong>Reload</strong> button, click it.",
        "Repeat for each extension."]),
    table(["Search for", "Publisher", "What it does for you"], [
        ["<strong>Python</strong>", "Microsoft", "Runs <code>.py</code> files and finds your conda environments."],
        ["<strong>Jupyter</strong>", "Microsoft", "Opens notebooks (<code>.ipynb</code>) inside VS Code."],
        ["<strong>Rainbow CSV</strong>", "mechatroner", "Colours the columns of a CSV so raw data is readable."],
        ["<strong>Error Lens</strong>", "usernamehw", "Shows errors at the end of the line that caused them."],
    ]),
    p("To check, type <code>@installed</code> in the search box. All four should be listed."),
    h3("7. Open a notebook in your environment"),
    ol(["<strong>File, then Open Folder</strong>, and choose a folder for your work.",
        "<strong>File, then New File</strong>, choose <em>Jupyter Notebook</em> (or open a notebook you downloaded from Colab with <strong>File, Download, .ipynb</strong>).",
        "Click <strong>Select Kernel</strong> at the top right, choose <strong>Python Environments</strong>, then pick <code>" + ENV + "</code>.",
        "Run a cell containing the two lines below."]),
    code("import sys\nprint(sys.executable)", "python", "run this in a notebook cell"),
    p("It prints the path of the Python being used. It should contain <code>envs/" + ENV + "</code> (or <code>envs\\" + ENV + "</code> on Windows). If not, pick the kernel again."),
], [
    puzzle("s0p1", 1, p("Type <code>conda env list</code> in your terminal and paste everything it printed. The checker looks for your <code>" + ENV + "</code> environment."),
           kind="paste", placeholder="# conda environments:\nbase    /Users/you/miniconda3\n" + ENV + "    /Users/you/miniconda3/envs/" + ENV,
           spec={"kind": "paste", "patterns": [[r"\b" + ENV + r"\b", "I do not see an environment called " + ENV + ". Run the conda create command in step 3 again and read its last lines."]]},
           hint="If the list is missing it, the create command in step 3 did not finish. Run it again and read the last lines it prints."),
    puzzle("s0p2", 2, p("Run <code>import sys; print(sys.executable)</code> in a notebook cell in VS Code, using the <code>" + ENV + "</code> kernel, and paste the path it printed."),
           kind="paste", placeholder="/Users/you/miniconda3/envs/" + ENV + "/bin/python",
           spec={"kind": "paste", "patterns": [[ENV + r"[\\/].*python", "That path does not point into the " + ENV + " environment. Click the kernel picker at the top right of the notebook, choose " + ENV + ", and run the cell again."]]},
           hint="Not seeing " + ENV + " in the kernel list? Click the refresh icon in the picker, or restart VS Code once. The environment needs <code>ipykernel</code>, which step 3 installed."),
])

# ======================================================================= Stage 6 (Part 2): organising a project
TREE = """pybio-project/
├── README.md              what this is and how to run it
├── environment.yml        the recipe for the conda environment
├── data/
│   ├── raw/               downloaded files, never edited
│   └── derived/           tables your code creates
├── notebooks/             your notebooks, numbered in order
│   └── helpers.py         functions you reuse
└── results/
    └── figures/           plots saved by code"""

CURL_MAC = ('curl -L -o data/raw/toy_vampseq_bin_counts.csv ' + BASE + 'toy_vampseq_bin_counts.csv\n'
            'curl -L -o data/raw/pten-variant-abundance.csv ' + BASE + 'pten-variant-abundance.csv\n'
            'curl -L -o data/raw/pten-region-annotations.csv ' + BASE + 'pten-region-annotations.csv')
CURL_WIN = ('Invoke-WebRequest -Uri ' + BASE + 'toy_vampseq_bin_counts.csv -OutFile data/raw/toy_vampseq_bin_counts.csv\n'
            'Invoke-WebRequest -Uri ' + BASE + 'pten-variant-abundance.csv -OutFile data/raw/pten-variant-abundance.csv\n'
            'Invoke-WebRequest -Uri ' + BASE + 'pten-region-annotations.csv -OutFile data/raw/pten-region-annotations.csv')

add(6, "Organising a project", "Give your work a tidy home: folders, a download you can repeat, a check that the file is intact, and a place for code you reuse.", [
    p("In Part 1 your files lived in a temporary Colab session. Real projects live in folders on your disk. Analyses that last are organised in a way anyone can understand. Not fancy, just predictable."),
    tree(TREE),
    callout("why", "Two rules that prevent most disasters",
            ul(["<strong>Raw data is never edited.</strong> Do not open a raw file in Excel and save it: Excel quietly changes numbers, dates and gene names. Your code reads from <code>data/raw</code> and saves new tables in <code>data/derived</code>.",
                "<strong>Everything in <code>results/</code> can be deleted and rebuilt</strong> by running your code. If it cannot, there is a hidden manual step."])),
    h3("1. Make the folders"),
    p("In your terminal, choose where the project should live (with <code>cd</code>), then:"),
    os_code("mkdir " + PROJECT + "\ncd " + PROJECT + "\nmkdir -p data/raw data/derived notebooks results/figures\nls",
            "mkdir " + PROJECT + "\ncd " + PROJECT + "\nmkdir data/raw, data/derived, notebooks, results/figures\nls", "bash", "powershell", "macOS / Linux terminal", "Windows (PowerShell)"),
    h3("2. Download the data"),
    p("Downloading with commands is a record of where each file came from, which clicking links is not. Three files power the rest of this guide: the toy table, the real PTEN table, and the table of regions. Run these from inside the project folder:"),
    os_code(CURL_MAC, CURL_WIN, "bash", "powershell", "macOS / Linux terminal", "Windows (PowerShell)"),
    p("Check they arrived:"),
    code("ls data/raw", "bash", "terminal"),
    h3("3. Check the file is the real file"),
    p("A partial or edited download can look fine and quietly ruin your results. A <strong>checksum</strong> is a fingerprint of a file: change one character and the fingerprint changes completely. Compute yours:"),
    os_code("shasum -a 256 data/raw/pten-variant-abundance.csv", "Get-FileHash data/raw/pten-variant-abundance.csv", "bash", "powershell", "macOS / Linux terminal", "Windows (PowerShell)"),
    h3("4. Write a README"),
    p("A <strong>README</strong> is a short note that explains the project. Make a file called <code>README.md</code> in the project folder with something like:"),
    code("# PTEN abundance analysis\n\nExplores a published table of protein variant abundance scores.\n\n## How to run\n1. conda env create -f environment.yml\n2. conda activate " + ENV + "\n3. open the notebooks in order\n\n## Decisions\n- Score = weighted average of four bins.\n- Variants with fewer than 50 reads are left out.", "markdown", "README.md"),
    p("Save the environment next to it, as in Stage 11:"),
    code("conda env export --from-history > environment.yml", "bash", "terminal"),
    h3("5. A file for code you reuse"),
    p("In Stage 5 you wrote <code>add_scores</code>. Instead of pasting it into every notebook, put it in a file next to your notebooks. Create <code>notebooks/helpers.py</code> containing:"),
    code('def add_scores(df, min_reads=0):\n    """Add total_reads and score columns. Rows with fewer than min_reads reads get no score."""\n    df = df.copy()\n    df["total_reads"] = df["bin1_count"] + df["bin2_count"] + df["bin3_count"] + df["bin4_count"]\n    df["score"] = (df["bin1_count"] * 1 + df["bin2_count"] * 2 + df["bin3_count"] * 3 + df["bin4_count"] * 4) / df["total_reads"]\n    df.loc[df["total_reads"] < min_reads, "score"] = None\n    return df', "python", "notebooks/helpers.py"),
    p("Any notebook in that folder can now use it with one line:"),
    code("from helpers import add_scores", "python", "in a notebook cell"),
    callout("note", "If a change to helpers.py does not show up",
            p("The kernel remembers what it has already loaded (Stage 1). After editing <code>helpers.py</code>, restart the kernel and run again.")),
], [
    puzzle("s6p1", 1, p("Compute the checksum of <code>data/raw/pten-variant-abundance.csv</code> and paste the line it printed. The checker compares it with the fingerprint of the original file. If it does not match, download the file again."),
           kind="paste", placeholder="64 letters and digits",
           hint="A mismatch usually means a partial download (the file should be about a megabyte), or the file was opened and re-saved in a spreadsheet program. Delete it and download it again."),
    puzzle("s6p2", 2, p("Run <code>ls</code> inside your project folder (not inside <code>data</code>) and paste the output. It should list <code>data</code>, <code>notebooks</code>, <code>results</code>, <code>README.md</code> and <code>environment.yml</code>."),
           kind="paste", placeholder="README.md\ndata\nenvironment.yml\nnotebooks\nresults",
           spec={"kind": "paste", "patterns": [[r"\bdata\b", "I do not see the data folder."], [r"notebooks", "I do not see the notebooks folder."], [r"results", "I do not see the results folder."],
                                                [r"README\.md", "I do not see README.md."], [r"environment\.yml", "I do not see environment.yml. Run the export command in step 4."]]},
           hint="Create whatever is missing, then run <code>ls</code> again from the project folder."),
])

# ======================================================================= Stage 13 (Part 2): running a script
add(13, "Running a script", "Move from clicking cells to one command that rebuilds a result, so anyone can repeat it.", [
    p("Notebooks are wonderful for exploring. Final results should not depend on cells you clicked in a certain order. A <strong>script</strong> is a plain <code>.py</code> file that runs from top to bottom with one command."),
    h3("A first script"),
    p("In VS Code, make a new file called <code>make_figure.py</code> in your project folder containing:"),
    code('import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\ndf = pd.read_csv("data/raw/pten-variant-abundance.csv")\nmiss = df[df["record_type"] == "missense"]\n\nsns.histplot(data=miss, x="score", bins=40)\nplt.xlabel("abundance score")\nplt.ylabel("number of variants")\nplt.savefig("results/figures/score_histogram.png", dpi=300, bbox_inches="tight")\n\nprint("saved results/figures/score_histogram.png")', "python", "make_figure.py"),
    p("Open a terminal in the project folder, activate your environment, and run it:"),
    code("conda activate " + ENV + "\npython make_figure.py", "bash", "terminal"),
    p("The file <code>results/figures/score_histogram.png</code> now exists, made entirely by code. Delete it and run the script again: it comes back."),
    callout("tip", "The folder you run from matters",
            p("Paths like <code>data/raw/...</code> are relative to the folder the terminal is in (Stage 2: <code>FileNotFoundError</code>). Always run the script from the project folder.")),
    h3("A checklist for repeatable work"),
    ol(["<strong>Restart and run all</strong> every notebook. Fix anything that fails or depends on a cell you ran once and forgot.",
        "Move the final plotting code into a script like the one above.",
        "Save the environment: <code>conda env export --from-history &gt; environment.yml</code>.",
        "Write the README: how to run it, and the choices you made.",
        "Delete <code>results/</code> and run everything again to prove it rebuilds."]),
    h3("Where to go next"),
    ul(['<a href="https://pandas.pydata.org/docs/user_guide/10min.html" target="_blank" rel="noopener">10 minutes to pandas</a>: the official short tour. You can read all of it now.',
        'The <a href="https://seaborn.pydata.org/examples/index.html" target="_blank" rel="noopener">seaborn gallery</a> and <a href="https://matplotlib.org/stable/gallery/index.html" target="_blank" rel="noopener">matplotlib gallery</a>: find a plot, copy the code, adapt it.',
        "Pick a question of your own about the PTEN table and answer it with a figure, a paragraph and a function."]),
], [])

# ======================================================================= Extra (15): DNA sequences with Biopython
FASTA = """>geneA low-GC test gene
ATGAAATTTAAAGAAATTATTAAAGAAGTTAAAAAA
>geneB high-GC test gene
ATGGGCGCCGGCCGCGCCGGGCCCGGCGCCGCCGGC
>geneC contains an early stop codon
ATGACCGAATGGCTGTAATGCCGTAACGAT
>geneD mixed test gene
ATGGTGCTGAGCCCGGAAGATAAAACC
AACGTG
"""

add(15, "DNA sequences with Biopython", "Optional: a library built for biology that knows how to translate DNA and read sequence files.", [
    p("<strong>Biopython</strong> is a library of biology tools. You need to install it once. In Colab, run the first cell. On your own computer, use <code>pip install biopython</code> in your environment."),
    code("%pip install -q biopython", "python", "Colab cell"),
    h3("A DNA sequence as an object"),
    p("A <code>Seq</code> behaves like text you already know how to slice, and it also knows biology:"),
    code('from Bio.Seq import Seq\n\ndna = Seq("ATGACCGAATGGCTGTAATGCCGTAACGAT")\n\nprint(len(dna))\nprint(dna[:6])                    # slicing, like text\nprint(dna.reverse_complement())    # the other strand, read backwards\nprint(dna.translate())             # DNA to protein; * is a stop signal\nprint(dna.translate(to_stop=True)) # stop reading at the first stop', "python", "run this", test="x15_seq"),
    h3("Reading a FASTA file"),
    p("A <strong>FASTA</strong> file lists sequences: a line starting with <code>&gt;</code> gives the name, then the letters follow. Here the file is a piece of text so there is nothing to upload:"),
    code('FASTA = """' + FASTA + '"""', "python", "a tiny FASTA file", test="x15_fasta"),
    code('from io import StringIO\nfrom Bio import SeqIO\n\nfor record in SeqIO.parse(StringIO(FASTA), "fasta"):\n    print(record.id, len(record.seq))', "python", "run this", test="x15_read"),
    h3("Sequences in a table"),
    p("Collect what you want into a list of dictionaries, then turn it into a table, exactly as in Stage 0:"),
    code('import pandas as pd\n\nrows = []\nfor record in SeqIO.parse(StringIO(FASTA), "fasta"):\n    rows.append({"gene": record.id, "length": len(record.seq), "protein": str(record.seq.translate())})\n\nseqs = pd.DataFrame(rows)\nseqs', "python", "run this", test="x15_table"),
    callout("tip", "Where to look next",
            p('The <a href="https://biopython.org/wiki/Documentation" target="_blank" rel="noopener">Biopython documentation</a> has a tutorial for each of these tools, and the Python for Biologists tutorials (linked on the plan page) cover sequences and files in more depth.')),
], [])

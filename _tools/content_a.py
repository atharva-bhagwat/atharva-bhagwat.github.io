from qbuild import *

TOY_URL = "https://atharva-bhagwat.github.io/assets/data/toy_vampseq_bin_counts.csv"

STAGES_A = []

# =====================================================================
# Stage 0
# =====================================================================
STAGES_A.append(stage(
    0, "Basecamp", "set up your tools", 60,
    "By the end you will have an isolated Python environment, an editor that understands it, and proof that both talk to each other.",
    [
        p("You have been writing code in Colab, where everything is ready-made. That is the best way to learn, but it has limits: "
          "sessions reset and your files disappear, you cannot easily run a script on a schedule, big datasets do not fit, and you cannot rebuild exactly the same setup next year. "
          "Your own computer fixes all of those, and it needs a little setup, once."),
        p("Most beginner pain is not about Python at all. It is about <em>which</em> Python is running, and where. "
          "So we fix that first, once, properly."),
        h3("Terminal first aid"),
        p("The <strong>terminal</strong> is a window where you type commands instead of clicking. It looks unfriendly but it only does what you tell it, and it never breaks anything you did not ask it to. "
          "Open it now: <strong>Terminal</strong> on macOS (press <kbd>Cmd</kbd>+<kbd>Space</kbd>, type Terminal), <strong>PowerShell</strong> on Windows (Start menu, type PowerShell). "
          "Each line you type ends with <kbd>Enter</kbd>."),
        p("A terminal is always \"standing\" in one folder, called the <strong>working directory</strong>. These five commands cover 90 percent of what you will ever need:"),
        table(["Command", "What it does"], [
            ["<code>pwd</code>", "Print where you are standing now (on Windows PowerShell: also <code>pwd</code>)."],
            ["<code>ls</code>", "List what is in this folder (Windows PowerShell understands <code>ls</code> too)."],
            ["<code>cd folder_name</code>", "Step into a folder. <code>cd ..</code> steps back out to the parent folder."],
            ["<code>mkdir new_folder</code>", "Make a new folder."],
            ["<code>python script.py</code>", "Run a Python file (once Python is installed, below)."],
        ]),
        ul([
            "Press <kbd>Tab</kbd> after typing the first letters of a name and the terminal completes it. It saves typing and typos.",
            "Press <kbd>&uarr;</kbd> to bring back the previous command. Press <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop something that is running.",
            "Copy a command, right-click or <kbd>Cmd</kbd>/<kbd>Ctrl</kbd>+<kbd>V</kbd> to paste, then Enter. A command that prints nothing usually worked.",
            "An error message is not a disaster: read the last line, exactly as in Stage 2.",
        ]),
        p("Do the <strong>terminal drill</strong> in the practice section at the end of this stage before you start the install steps."),
        h3("1. Install VS Code"),
        p('Download it from <a href="https://code.visualstudio.com/" target="_blank" rel="noopener">code.visualstudio.com</a> and run the installer. '
          "VS Code is a text editor that grows into an IDE when you add extensions. It will be where you write scripts, run notebooks, "
          "browse files, and use a terminal, all in one window."),
        callout("tip", "macOS only: enable the <code>code</code> command",
                p("Open VS Code, press <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>, type <code>Shell Command: Install 'code' command in PATH</code> and press Enter. "
                  "Windows and Linux installers usually do this for you.")),
        h3("2. Install Miniconda from the command line"),
        p("conda is a program that creates <strong>environments</strong>: separate folders, each with its own Python and its own set of libraries. "
          "Project A can use pandas 2 while project B uses pandas 3, and neither can break the other. "
          "<strong>Miniconda</strong> is the small installer: just conda and Python. We install it entirely from the terminal. "
          "Open a terminal first: Terminal on macOS or Linux, <strong>PowerShell</strong> on Windows (Start menu, type PowerShell)."),
        p("Pick your system. On a Mac, check which chip you have with <code>uname -m</code>: <code>arm64</code> means Apple silicon, <code>x86_64</code> means Intel."),
        '<div class="q-os" data-os-group><div class="q-os-tabs" role="tablist" aria-label="Operating system">'
        '<button type="button" role="tab" data-os="mac">macOS / Linux</button><button type="button" role="tab" data-os="win">Windows</button></div>'
        '<div class="q-os-pane" data-os-pane="mac">'
        + code("uname -m\n\n# macOS, Apple silicon (arm64):\nURL=https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh\n# macOS, Intel (x86_64): use this line instead\n# URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh\n# Linux (x86_64): use this line instead\n# URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh\n\nmkdir -p ~/miniconda3\ncurl -L $URL -o ~/miniconda3/miniconda.sh\nbash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3\nrm ~/miniconda3/miniconda.sh\n\n~/miniconda3/bin/conda init bash zsh", "bash", "macOS / Linux terminal")
        + '</div><div class="q-os-pane" data-os-pane="win">'
        + code('Invoke-WebRequest -Uri "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile ".\\miniconda.exe"\nStart-Process -FilePath ".\\miniconda.exe" -ArgumentList "/InstallationType=JustMe","/RegisterPython=0","/S","/D=$env:USERPROFILE\\miniconda3" -Wait\nRemove-Item ".\\miniconda.exe"\n\n& "$env:USERPROFILE\\miniconda3\\Scripts\\conda.exe" init powershell', "powershell", "Windows (PowerShell)")
        + '</div></div>',
        p("The last line connects conda to your shell. <strong>Close the terminal completely and open a new one</strong>. The prompt should now start with <code>(base)</code>. Then check:"),
        code("conda --version\nwhich python    # Windows: Get-Command python", "bash", "terminal"),
        callout("trap", "Windows: \"running scripts is disabled on this system\"",
                p("PowerShell blocks the startup file conda adds. Run <code>Set-ExecutionPolicy -Scope CurrentUser RemoteSigned</code>, answer Y, then open a new PowerShell window.")),
        callout("trap", "conda says something about \"Terms of Service\"",
                p("Newer conda versions can stop and ask you to accept channel terms before installing packages. "
                  "The message prints the exact command to run. Copy it, run it, then repeat your original command. "
                  "This is your first lesson in reading error messages: the answer was in the message.")),
        p("Optional but pleasant: stop conda from activating <code>base</code> in every new terminal."),
        code("conda config --set auto_activate_base false", "bash", "terminal"),
        h3("3. Create the environment"),
        p("One command makes a fresh environment called <code>pandas-quest</code> with everything this guide needs:"),
        code("conda create -n pandas-quest -c conda-forge python=3.12 pandas numpy matplotlib seaborn scipy ipykernel -y",
             "bash", "terminal"),
        p("Then step inside it. You will do this every time you open a new terminal:"),
        code("conda activate pandas-quest", "bash", "terminal"),
        p("Your prompt now starts with <code>(pandas-quest)</code>. That prefix is your seatbelt light: if it is missing, you are not in the environment."),
        h3("4. Make a project folder and open it"),
        os_code(
            "mkdir pandas-quest\ncd pandas-quest\ncode .",
            "mkdir pandas-quest\ncd pandas-quest\ncode .",
            win_lang="bash",
        ),
        p("VS Code opens with that folder. Always open the <em>folder</em>, not single files. It is what lets VS Code find your data, scripts and environment."),
        h3("5. Add extensions"),
        p("An <strong>extension</strong> is an add-on that teaches VS Code new skills. You install them from inside VS Code, and you will use the same few clicks every time you want a new one."),
        ol([
            "Click the <strong>Extensions</strong> icon in the vertical bar on the far left of the window. It looks like four squares with one flying off. "
            "No icon bar? Use the menu: <strong>View</strong>, then <strong>Extensions</strong>. Keyboard shortcut: <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd> (Windows, Linux) or <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd> (Mac).",
            "Click the search box at the top of the panel. It says <em>Search Extensions in Marketplace</em>. The Marketplace is VS Code's app store, and everything in it is free to install.",
            "Type the name from the table below, for example <code>Python</code>. Results appear underneath, most popular first.",
            "Pick the right result: check the <strong>publisher name</strong> under the title, and the download count (the good ones have millions or hundreds of thousands). Click the result to read its description on the right.",
            "Click the blue <strong>Install</strong> button. Wait a few seconds until it changes to a gear icon. That means it worked. If a <strong>Reload</strong> or <strong>Restart Extensions</strong> button appears, click it.",
            "Repeat for each extension in the table.",
        ]),
        table(["Search for", "Publisher", "What it does for you"], [
            ["<strong>Python</strong>", "Microsoft", "Runs and debugs <code>.py</code> files, finds your conda environments, adds autocomplete."],
            ["<strong>Jupyter</strong>", "Microsoft", "Opens <code>.ipynb</code> notebooks inside VS Code and runs cells."],
            ["<strong>Rainbow CSV</strong>", "mechatroner", "Colours each column of a CSV differently so you can read raw data files."],
            ["<strong>Data Wrangler</strong>", "Microsoft", "Opens a DataFrame as a scrollable grid with summary stats."],
            ["<strong>Error Lens</strong>", "Alexander (usernamehw)", "Prints errors and warnings at the end of the offending line. Great for making errors feel normal."],
        ]),
        callout("tip", "Find an exact extension with its ID",
                p("Every extension has a unique ID. Typing it with <code>@id:</code> in front shows exactly one result, so you cannot pick a look-alike. Try <code>@id:ms-python.python</code>. "
                  "The IDs for this guide are <code>ms-python.python</code>, <code>ms-toolsai.jupyter</code>, <code>mechatroner.rainbow-csv</code>, <code>ms-toolsai.datawrangler</code> and <code>usernamehw.errorlens</code>.")),
        callout("trap", "Look-alikes",
                p("Searching <code>Python</code> returns many extensions. Choose the one published by <strong>Microsoft</strong> with the blue verified checkmark next to the publisher name and the largest download count. "
                  "Installing the Python extension also adds a few helpers (such as Pylance) automatically. That is normal.")),
        p("To confirm everything is installed, type <code>@installed</code> in the search box. You should see all five in the list. "
          "The same box shows other useful filters: <code>@recommended</code> for suggestions, and the clock icon for recently updated extensions."),
        h3("6. Tell VS Code which Python to use"),
        p("Press <kbd>Ctrl</kbd>/<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>, type <code>Python: Select Interpreter</code>, and choose the one named <code>pandas-quest</code>. "
          "Its path contains <code>envs/pandas-quest</code>. A notebook has its own picker, which you will use in the next stage."),
        h3("7. Run the check script"),
        p("In VS Code create a new file named <code>check_setup.py</code> (File, New File), paste this in, save, and run it from the terminal with "
          "<code>python check_setup.py</code>."),
        code('import sys\nimport platform\n\nprint("python    ", platform.python_version())\n'
             'for name in ["pandas", "numpy", "matplotlib", "seaborn", "scipy"]:\n'
             '    module = __import__(name)\n'
             '    print(f"{name:<10}", module.__version__)\n'
             'print("env       ", sys.prefix.replace("\\\\", "/").split("/")[-1])',
             "python", "check_setup.py", test="s0_check"),
        p("You should see something shaped like this (your version numbers will differ):"),
        code("python     3.12.8\npandas     3.0.1\nnumpy      2.3.5\nmatplotlib 3.10.7\nseaborn    0.13.2\nscipy      1.16.3\nenv        pandas-quest",
             "text", "example output"),
        callout("trap", "<code>ModuleNotFoundError: No module named 'pandas'</code>",
                p("Python is running, but it is not the one inside <code>pandas-quest</code>. Check for the <code>(pandas-quest)</code> prefix in your terminal, "
                  "and re-run <code>Python: Select Interpreter</code>. Nine times out of ten, this is the whole story.")),
    ],
    [
        puzzle("s0p1", 1,
               p("Paste everything <code>check_setup.py</code> printed. The checker looks for Python, pandas, matplotlib and seaborn versions, and an <code>env</code> line that says <code>pandas-quest</code>."),
               kind="paste", placeholder="python     3.12.x\npandas     x.y.z\n...",
               hint="If a library line is missing, the install command in step 3 did not finish. Run it again and read the last lines it prints."),
        puzzle("s0p2", 2,
               p("Now prove VS Code itself uses that environment. In the next stage you will create a notebook; for now, any notebook will do "
                 "(<kbd>Ctrl</kbd>/<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>, then <code>Create: New Jupyter Notebook</code>). "
                 "Click <strong>Select Kernel</strong> at the top right, pick <code>pandas-quest</code>, run this in a cell, and paste the path it prints."),
               kind="paste", placeholder="/.../envs/pandas-quest/bin/python",
               hint="Not seeing pandas-quest in the kernel list? Click the refresh icon in the kernel picker, or restart VS Code once. The environment needs <code>ipykernel</code> installed, which step 3 did.",
               solution="import sys\nprint(sys.executable)", ),
    ],
))

# =====================================================================
# Stage 1
# =====================================================================
VARIANTS = '["p.Gly12Gly", "p.Trp18Ter", "p.Leu25Pro", "p.Val30Asp",\n            "p.Gln36Ter", "p.Ile40Asn", "p.Ser45Thr", "p.Gly46Arg"]'

STAGES_A.append(stage(
    1, "Notebook Ridge", "cells, kernels and Python basics", 50,
    "You will learn the one rule that explains most notebook weirdness, then use strings, loops and conditions to take a variant name apart.",
    [
        p("A <strong>Jupyter notebook</strong> (<code>.ipynb</code>) mixes code, results and notes in one document. It is made of <strong>cells</strong>. "
          "Code cells run Python and show what they produce underneath. Markdown cells hold text, headings and reminders to future you."),
        callout("tip", "Keyboard shortcuts worth learning today",
                ul(["<kbd>Shift</kbd>+<kbd>Enter</kbd>: run the cell and move to the next one (both Colab and VS Code).",
                    "Colab: <kbd>Ctrl</kbd>/<kbd>Cmd</kbd>+<kbd>M</kbd> then <kbd>A</kbd> or <kbd>B</kbd> inserts a cell above or below; then <kbd>M</kbd> or <kbd>Y</kbd> makes it Markdown or code; then <kbd>D</kbd> deletes it.",
                    "VS Code (and classic Jupyter): <kbd>Esc</kbd> first, then the same letters without <kbd>Ctrl</kbd>+<kbd>M</kbd>."])),
        p("Open the notebook with the button above, choose <strong>File, Save a copy in Drive</strong> so your edits are yours, and run it cell by cell. "
          "Colab runs Python on a Google computer, so there is nothing to install. The code on this page is also in the notebook, with blanks (<code>____</code>) for you to fill in."),
        h3("The kernel is a running program with a memory"),
        p("Behind the notebook is a <strong>kernel</strong>: a Python process that executes your cells and remembers every variable you have created. "
          "The notebook shows the code; the kernel holds the state. They can disagree. Try it:"),
        code("x = 10", "python", "cell 1"),
        code("print(x * 2)", "python", "cell 2"),
        p("Run both: you get <code>20</code>. Now edit cell 1 to <code>x = 100</code> but <em>do not run it</em>, then re-run cell 2. Still <code>20</code>. "
          "The page says 100; the kernel still thinks 10."),
        callout("why", "The notebook rule",
                p("A notebook is only trustworthy if it works from the top, in order, in a fresh kernel. "
                  "Get in the habit of <strong>restarting and running everything</strong> before you believe any result, and before you share a notebook. "
                  "In Colab: <strong>Runtime, Restart session and run all</strong>. In VS Code: the <strong>Restart</strong> and <strong>Run All</strong> toolbar buttons.")),
        h3("Printing, and what shows up on its own"),
        p("The last expression in a cell is displayed automatically. <code>print()</code> is for everything else: checking an assumption, "
          "logging progress inside a loop, leaving yourself a trail of what happened. F-strings make labels painless:"),
        code('n_reads = 1250\nprint(f"reads counted: {n_reads}")\nprint(f"as thousands: {n_reads / 1000:.2f}k")', "python", "cell"),
        callout("note", "When to print",
                p("Print while you are figuring things out; delete or reduce the prints once you trust a step. Loud notebooks hide the one line that matters.")),
        h3("Data types, in five lines"),
        code('count = 24             # int\nscore = 3.49           # float\nname = "p.Trp18Ter"    # str\nis_low = score < 2     # bool\nvariants = ["a", "b"]  # list\nprint(type(count), type(score), type(name), type(is_low), type(variants))',
             "python", "cell"),
        p("<code>type(x)</code> is the first thing to check when something behaves strangely. It is the notebook equivalent of looking at the label on the jar."),
        h3("Strings, and slicing them"),
        p("A <strong>slice</strong> <code>text[start:stop]</code> takes characters from <code>start</code> up to, but not including, <code>stop</code>. "
          "Counting starts at 0, and negative numbers count from the end."),
        code('v = "p.Trp18Ter"\n#    index: 0123456789...\nprint(v[2:5])    # Trp\nprint(v[5:-3])   # 18\nprint(v[-3:])    # Ter\nprint(int(v[5:-3]) + 1)   # 19\nprint(v.startswith("p."), v.endswith("Ter"), v.upper(), v.replace("p.", ""))',
             "python", "cell", test="s1_slices"),
        callout("trap", "Off-by-one",
                p("<code>v[2:5]</code> has three characters, not four, because the stop position is excluded. "
                  "When a slice is wrong by one, write out the indices on paper. It takes ten seconds.")),
        h3("Math, conditions, loops"),
        code('print(7 + 2, 7 - 2, 7 * 2, 7 / 2, 7 // 2, 7 % 2, 7 ** 2)   # 9 5 14 3.5 3 1 49\nprint(round(3.4902, 2))',
             "python", "cell"),
        code('score = 1.4\nif score < 0.5:\n    label = "low"\nelif score < 1.0:\n    label = "in between"\nelse:\n    label = "wild-type-like"\nprint(label)',
             "python", "cell"),
        code('names = ["WT", "p.Trp18Ter", "p.Leu25Pro"]\nfor i, name in enumerate(names):\n    print(i, name, len(name))\n\n# the same idea in one line, called a list comprehension\nlengths = [len(name) for name in names]',
             "python", "cell"),
        p("Python reads close to English: <em>for each name in names, print it</em>. Indentation (four spaces) is how Python knows what is inside the loop or the <code>if</code>, "
          "so it is part of the grammar, not decoration."),
        p("Here is the list you will use for the puzzles. Every entry follows the pattern <code>p.</code> + three-letter <em>reference</em> + <em>position</em> + three-letter <em>alternate</em>. "
          "(<code>Ter</code> means the protein stops there; the same three letters twice means the amino acid is unchanged, although the DNA underneath was edited.)"),
        code(f"variants = {VARIANTS}", "python", "cell", test="s1_list"),
    ],
    [
        puzzle("s1p1", 1,
               p("Using slicing, pull the position number out of every variant, convert it to an integer, and add them all up. What is the sum?"),
               kind="number", placeholder="a whole number",
               hint="Every variant has the same shape, so <code>v[5:-3]</code> works for all of them. Loop over the list and add <code>int(...)</code> to a running total starting at 0.",
               solution='total = 0\nfor v in variants:\n    total += int(v[5:-3])\nprint(total)', test="s1p1"),
        puzzle("s1p2", 2,
               p("Classify each variant with a loop and <code>if</code>/<code>elif</code>/<code>else</code>: "
                 "<strong>synonymous</strong> if the reference and alternate letters are identical, <strong>nonsense</strong> if the alternate is <code>Ter</code>, otherwise <strong>missense</strong>. "
                 "Report the counts in the order synonymous, nonsense, missense, separated by commas."),
               kind="text", placeholder="e.g. 3,4,1",
               hint="Reference is <code>v[2:5]</code> and alternate is <code>v[-3:]</code>. Check synonymous first, then nonsense. Keep three counters and print them with an f-string.",
               solution='syn = non = mis = 0\nfor v in variants:\n    ref, alt = v[2:5], v[-3:]\n    if ref == alt:\n        syn += 1\n    elif alt == "Ter":\n        non += 1\n    else:\n        mis += 1\nprint(f"{syn},{non},{mis}")', test="s1p2"),
    ],
))

# =====================================================================
# Stage 2
# =====================================================================
STAGES_A.append(stage(
    2, "Traceback Gorge", "errors are directions, not insults", 35,
    "Every programmer sees red text all day. The skill is not avoiding it, it is reading it fast. You will learn the anatomy of an error and a repeatable way to chase one down.",
    [
        p("An error message is the computer telling you, as precisely as it can, where it got stuck and why. "
          "It is more helpful than most feedback you will ever get. Here is a real one from a notebook:"),
        '<div class="q-trace">'
        '<pre><code>'
        '<span class="t-dim">---------------------------------------------------------------------------</span>\n'
        '<span class="t-err">KeyError</span><span class="t-dim">                                  Traceback (most recent call last)</span>\n'
        '<span class="t-dim">Cell In[4], </span><span class="t-line">line 2</span>\n'
        '<span class="t-dim">      1 df = pd.read_csv("data/raw/toy.csv")</span>\n'
        '<span class="t-arrow">----&gt; 2</span> <span class="t-hot">print(df["Score"].mean())</span>\n'
        '\n'
        '<span class="t-dim">File ~/miniconda3/envs/pandas-quest/lib/python3.12/site-packages/pandas/core/frame.py:4102, in DataFrame.__getitem__(self, key)</span>\n'
        '<span class="t-dim">   ... (about thirty lines of pandas internals) ...</span>\n'
        '\n'
        '<span class="t-err">KeyError: \'Score\'</span>'
        '</code></pre></div>',
        ol([
            "<strong>Start at the bottom.</strong> <code>KeyError: 'Score'</code> says: you asked for something by name and it is not there. The type tells you the category; the message tells you the specifics.",
            "<strong>Find your line.</strong> The arrow <code>----&gt; 2</code> points at <em>your</em> code. Ignore the middle section about library internals; those are the pandas authors' lines, and the bug is almost never theirs.",
            "<strong>Ask what you would expect.</strong> Which column names really exist? <code>print(df.columns)</code>. You will see <code>score</code>, lowercase. Keys are case-sensitive.",
        ]),
        h3("The usual suspects"),
        table(["Error", "Plain-English meaning", "First thing to try"], [
            ["<code>SyntaxError</code>", "Python could not even read the code. A missing colon, quote or bracket. Nothing ran.", "Look at the line it marks and the line <em>above</em>."],
            ["<code>NameError</code>", "You used a name Python has never seen.", "Typo? Or you did not run the cell that creates it (kernel memory!)."],
            ["<code>TypeError</code>", "Right operation, wrong kind of thing, such as adding a string to a number.", "<code>print(type(x))</code> for each thing involved."],
            ["<code>ValueError</code>", "Right kind of thing, unacceptable value, such as <code>int(\"abc\")</code>.", "Print the value that was passed in."],
            ["<code>KeyError</code>", "A dictionary key or DataFrame column is not there.", "<code>df.columns</code>. Check case and stray spaces."],
            ["<code>IndexError</code>", "You asked for item 10 of a list with 5 items.", "<code>len(...)</code> before indexing."],
            ["<code>AttributeError</code>", "That object has no such method or attribute.", "Typo, or it is a different type than you think."],
            ["<code>FileNotFoundError</code>", "The path points to nothing.", "Print the current folder with <code>from pathlib import Path; Path.cwd()</code>."],
            ["<code>ModuleNotFoundError</code>", "The library is not installed in <em>this</em> environment.", "Colab: install it with <code>%pip install name</code>. On your own computer: wrong kernel or interpreter (Stage 0, step 6)."],
        ]),
        h3("A routine that works"),
        ol([
            "Read the last line of the traceback out loud, slowly.",
            "Go to the line the arrow points at. Is it what you expected to run?",
            "Check what you <em>assumed</em>: <code>print(type(x))</code>, <code>df.shape</code>, <code>df.columns</code>, <code>df.head()</code>.",
            "Shrink the problem. Reproduce it on three rows, or in a fresh cell with two lines.",
            "Suspect the kernel. <strong>Restart</strong> and <strong>Run All</strong>. A surprising number of bugs vanish.",
            "Search the message with your own names removed: <code>KeyError pandas column</code> beats <code>KeyError 'Score'</code>. "
            "Read the answer for why it happens, not just a line to copy.",
            "Still stuck? Write a question someone can answer: what you wanted, what you ran, the full error, what you already tried. "
            "That is also the best prompt for an AI assistant, which is a fine tool as long as you understand the fix before pasting it in.",
        ]),
        callout("why", "Loud failures are a gift",
                p("The dangerous bugs do not raise errors at all. They give you a plausible, wrong number. "
                  "This is why analysts check shapes and counts constantly, and use <code>assert</code> to make the computer complain on your behalf:")
                + code('assert len(df) == 24, f"expected 24 rows, got {len(df)}"', "python", "cell")),
        callout("tip", "Errors come one at a time",
                p("Fixing one error often reveals the next. That is progress, not failure. A script with three bugs will show you three different errors, in the order Python meets them. "
                  "A <code>SyntaxError</code> always comes first because Python reads the whole file before running a single line.")),
        p("Warm-up: four quick questions about reading errors. Then a broken script to fix on your own machine."),
    ],
    [
        puzzle("s2p1", 1,
               p("Pick the best answer for each."),
               kind="choices",
               choices=[
                   ("Which line of a traceback tells you <em>what</em> went wrong?",
                    ["The first line", "The last line", "The longest line"]),
                   ("<code>KeyError: 'Score'</code> after <code>df[\"Score\"]</code>. The file's header is <code>variant,score,se</code>. What is the fix?",
                    ["Reinstall pandas", "Use <code>df[\"score\"]</code>. Column names are case-sensitive.", "Restart the computer"]),
                   ("You uploaded <code>toy.csv</code> in Colab's Files panel (it lands in <code>/content/toy.csv</code>), and <code>pd.read_csv(\"data/raw/toy.csv\")</code> gives <code>FileNotFoundError</code>. Most likely cause?",
                    ["The CSV is corrupted", "pandas cannot read CSV files", "The path is relative to the current folder, and there is no <code>data/raw/</code> folder there, only <code>toy.csv</code> itself"]),
                   ("<code>total = 0</code>, then <code>for s in [\"1.5\", \"2.5\"]: total = total + s</code> gives <code>TypeError: unsupported operand type(s) for +: 'int' and 'str'</code>. What is <code>s</code>?",
                    ["A string, so int + str fails", "A number", "None"]),
               ],
               hint="Question 2: the error names the key it could not find. Compare it, character by character, with the real column name."),
        puzzle("s2p2", 2,
               p("This code has three separate bugs. Paste it into a new cell and run it, then fix what the errors tell you, one at a time. "
                 "When it finally runs, it prints a mean score. What is that mean, to 3 decimal places?")
               + code('scores = [3.45, 1.55, 2.18, 2.59, 3.82]\n\ntotal = 0\nfor s in scores\n    total = total + s\n\nmean = total / len(score)\nprint("mean score: " + mean)',
                      "python", "paste into a cell"),
               kind="number", placeholder="3 decimal places",
               hint="Expect three different errors, in this order: <code>SyntaxError</code> (a missing character at the end of a line), then <code>NameError</code> (one name is misspelled), then <code>TypeError</code> (you cannot add a string and a float; try an f-string).",
               solution='scores = [3.45, 1.55, 2.18, 2.59, 3.82]\n\ntotal = 0\nfor s in scores:\n    total = total + s\n\nmean = total / len(scores)\nprint(f"mean score: {mean:.3f}")', test="s2p2"),
    ],
))

# =====================================================================
# Stage 3
# =====================================================================
STAGES_A.append(stage(
    3, "Table Flats", "your first DataFrame", 45,
    "Libraries, read a CSV, look around, pick columns and filter rows. The four moves behind most data analysis.",
    [
        p("A <strong>library</strong> is code someone else wrote that you borrow with <code>import</code>. "
          'The one that matters most here is <a href="https://pandas.pydata.org/docs/" target="_blank" rel="noopener">pandas</a>, which gives Python a table type called a <strong>DataFrame</strong>: '
          "rows are observations, columns are named measurements, and every column has a type."),
        p("Our first table is a tiny made-up experiment. No biology needed: each <em>row</em> is one named item measured once, and four columns "
          "(<code>bin1_count</code> to <code>bin4_count</code>) say how many reads fell into each of four buckets, from the lowest signal (bin 1) to the highest (bin 4). "
          ),
        p("In the Colab notebook (button above), read the CSV straight from its web address. The file is hosted on this site, so there is nothing to upload:"),
        code(f'import pandas as pd\n\nURL = "{TOY_URL}"\ndf = pd.read_csv(URL)\ndf',
             "python", "cell", test="s3_load"),
        h3("Look before you touch"),
        p("Before any analysis, find out what you actually have. Run each of these in its own cell:"),
        code('df.head()                      # first 5 rows (df.tail() for the last 5)\ndf.shape                       # (rows, columns)\ndf.columns                     # the column names\ndf.dtypes                      # type of each column\ndf.info()                      # types + missing values in one view\ndf.describe()                  # count, mean, min, max... of numeric columns\ndf["variant_type"].value_counts()   # how many rows per category\ndf["variant"].nunique()        # how many different variants',
             "python", "cell", test="s3_look"),
        callout("note", "Types you will meet",
                p("Numbers show as <code>int64</code> or <code>float64</code>. Text is <code>object</code> in pandas 2 and <code>str</code> in pandas 3. Both are fine. "
                  "If a column that should be numeric shows up as text, something odd is hiding in it, which is worth knowing early.")),
        h3("Pick columns"),
        code('df["variant"]                       # one column -> a Series\ndf[["variant", "replicate"]]         # several columns -> a DataFrame (note the double brackets)',
             "python", "cell"),
        h3("Pick rows by condition"),
        p("A comparison on a column produces a column of <code>True</code>/<code>False</code>. Using that to index the DataFrame keeps only the <code>True</code> rows. "
          "This is called a <strong>boolean mask</strong>, and it is the pandas move you will use most."),
        code('is_nonsense = df["variant_type"] == "nonsense"\ndf[is_nonsense]\n\n# combine conditions with & (and), | (or), ~ (not) and wrap each one in parentheses\ndf[(df["variant_type"] == "missense") & (df["replicate"] == 1)]\n\n# membership and text tests\ndf[df["variant_type"].isin(["nonsense", "synonymous"])]\ndf[df["variant"].str.endswith("Arg")]\n\n# the same filter, written as a readable string\ndf.query("variant_type == \'missense\' and replicate == 1")',
             "python", "cell", test="s3_filter"),
        callout("trap", "<code>and</code> versus <code>&amp;</code>",
                p("Writing <code>df[(a) and (b)]</code> raises <code>ValueError: The truth value of a Series is ambiguous</code>. "
                  "Python's <code>and</code> wants one yes/no, but you gave it a whole column of them. Use <code>&amp;</code>, and keep the parentheses; "
                  "without them, the operators bind in an order you did not intend.")),
        h3("Select by position or label"),
        code('df.loc[0:2, ["variant", "bin1_count"]]   # by label: rows 0 to 2 (inclusive!), named columns\ndf.iloc[0:2, 0:2]                         # by position: rows 0 and 1 (stop excluded), first two columns',
             "python", "cell"),
        callout("tip", "Read the docs like a map",
                p('Open <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html" target="_blank" rel="noopener">the page for <code>DataFrame.query</code></a>. '
                  "Read the one-line summary, then Parameters, then jump to Examples. You do not have to understand all of it. "
                  "In a notebook, put the cursor inside a function's brackets and press <kbd>Shift</kbd>+<kbd>Tab</kbd> to see the same text in place.")),
    ],
    [
        puzzle("s3p1", 1,
               p("How many rows are <code>missense</code> <strong>and</strong> from <code>replicate</code> 2?"),
               kind="number", placeholder="a whole number",
               hint="Two conditions joined with <code>&amp;</code>, each in parentheses. Then count rows with <code>len(...)</code> or <code>.shape[0]</code>.",
               solution='sub = df[(df["variant_type"] == "missense") & (df["replicate"] == 2)]\nprint(len(sub))', test="s3p1"),
        puzzle("s3p2", 2,
               p("Add up every count in the four <code>bin*_count</code> columns across the whole table. What is the grand total of reads?"),
               kind="number", placeholder="a whole number",
               hint="Select the four columns as a list, then <code>.sum()</code> sums each column. A second <code>.sum()</code> adds those four numbers together.",
               solution='bins = ["bin1_count", "bin2_count", "bin3_count", "bin4_count"]\nprint(df[bins].sum().sum())', test="s3p2"),
    ],
))

# =====================================================================
# Stage 4
# =====================================================================
STAGES_A.append(stage(
    4, "Score Falls", "new columns, groups and pivots", 55,
    "You will turn raw counts into one number per row, summarise it per variant, and line up replicates side by side.",
    [
        p("Raw counts are hard to compare: one row has 20 reads, another has 700. A common fix is a <strong>weighted average</strong> of the bins. "
          "Give bin 1 weight 1, bin 2 weight 2, and so on. A row with all its reads in bin 1 scores 1, all in bin 4 scores 4, and anything between lands in between."),
        code("score = (1*bin1 + 2*bin2 + 3*bin3 + 4*bin4) / total_reads", "text", "the formula"),
        h3("Make new columns without loops"),
        p("pandas works on whole columns at once. That is called <strong>vectorised</strong> code. It is shorter, easier to read, and much faster than looping over rows."),
        code('bins = ["bin1_count", "bin2_count", "bin3_count", "bin4_count"]\n\ndf["total_reads"] = df[bins].sum(axis=1)                   # axis=1: add across the columns of each row\ndf["score"] = (df[bins] * [1, 2, 3, 4]).sum(axis=1) / df["total_reads"]\ndf[["variant", "replicate", "total_reads", "score"]].round(3)',
             "python", "cell", test="s4_score"),
        callout("note", "What is <code>axis</code>?",
                p("<code>axis=0</code> means \"down the rows\" (one answer per column). <code>axis=1</code> means \"across the columns\" (one answer per row). "
                  "If you get a result with the wrong shape, check the axis first.")),
        h3("Sort and rename"),
        code('df.sort_values("score")                       # smallest first\ndf.sort_values("score", ascending=False)\ndf.rename(columns={"score": "bin_score"})',
             "python", "cell"),
        h3("Summarise by group"),
        p("<code>groupby</code> splits the table by a column, applies a summary to each piece, and glues the answers back together: <em>split, apply, combine</em>."),
        code('df.groupby("variant_type")["score"].mean()\n\n# several summaries at once, with names you choose\nper_variant = df.groupby("variant").agg(\n    mean_score=("score", "mean"),\n    reads=("total_reads", "sum"),\n    n_rows=("score", "size"),\n).reset_index()\nper_variant.sort_values("mean_score")',
             "python", "cell", test="s4_group"),
        h3("Pivot: one row per variant, one column per replicate"),
        code('wide = df.pivot(index="variant", columns="replicate", values="score")\nwide                       # columns are named 1 and 2\nwide[1].corr(wide[2])      # how well do the replicates agree?',
             "python", "cell", test="s4_pivot"),
        code('wide["diff"] = (wide[1] - wide[2]).abs()\nwide.sort_values("diff", ascending=False)',
             "python", "cell"),
        callout("why", "A mean can hide the story",
                p("Two variants can have the same average score for completely different reasons. A quick look at the raw bins shows it:")
                + code('pick = df[(df["replicate"] == 1) & df["variant"].isin(["p.Ile40Asn", "p.Gly46Arg"])]\nfrac = pick[bins].div(pick["total_reads"], axis=0)   # each row now sums to 1\nfrac.index = pick["variant"]\nfrac.T.plot.bar()                                      # bins on x, one colour per variant',
                       "python", "cell (no star for this one)", test="s4_bonus")
                + p("<code>p.Ile40Asn</code> piles up in the middle bins. <code>p.Gly46Arg</code> splits between the lowest and highest. Same average, different shapes. "
                    "Stage 9 is all about plots that expose this.")),
        callout("tip", "Look at your pivot table before trusting it",
                p("If one variant's replicates disagree wildly, ask why <em>before</em> averaging them. The answer is sometimes in a column you already have.")),
    ],
    [
        puzzle("s4p1", 1,
               p("What is the mean <code>score</code> of the <code>WT</code> rows (both replicates), to 2 decimal places?"),
               kind="number", placeholder="2 decimal places",
               hint="Filter to rows where <code>variant == \"WT\"</code> and take <code>.mean()</code> of the <code>score</code> column.",
               solution='print(df[df["variant"] == "WT"]["score"].mean().round(2))', test="s4p1"),
        puzzle("s4p2", 2,
               p("Pivot the scores so replicates sit side by side, and take the absolute difference between replicate 1 and 2 for each variant. "
                 "Which variant has the <strong>largest</strong> disagreement? Write its name exactly as it appears."),
               kind="text", placeholder="p.Xxx00Yyy",
               hint="Use the <code>pivot</code> and <code>diff</code> code above, then <code>idxmax()</code> on the diff column, or sort descending and read the top row. Then look at that variant's <code>total_reads</code> and ask whether you trust it.",
               solution='wide = df.pivot(index="variant", columns="replicate", values="score")\nwide["diff"] = (wide[1] - wide[2]).abs()\nprint(wide["diff"].idxmax())', test="s4p2"),
    ],
))

# =====================================================================
# Stage 5
# =====================================================================
STAGES_A.append(stage(
    5, "Function Forge", "write it once, reuse it forever", 50,
    "You will turn working notebook code into a documented function, learn the habits that make it safe to reuse, and test it.",
    [
        p("In Stage 4 you computed scores for the whole table. Now imagine a collaborator wants a different weighting, or you want to ignore rows with too few reads, or you need the same calculation for next month's dataset. "
          "Copy and paste works exactly once. The second time you paste, the two copies start to differ, and you forget which one you trust."),
        callout("why", "The rule of two",
                p("The second time you copy a block of code, turn it into a function instead. "
                  "A function is a named, reusable recipe: you fix a bug in one place, and every use of it gets the fix.")),
        h3("Anatomy of a function"),
        code('BINS = ["bin1_count", "bin2_count", "bin3_count", "bin4_count"]\n\n\ndef add_scores(df, weights=(1, 2, 3, 4), min_reads=0):\n    """Add total_reads and a weighted-average bin score.\n\n    score = sum(weight_i * count_i) / total_reads, so 1 means every read\n    is in bin 1 (lowest signal) and 4 means every read is in bin 4.\n\n    Rows with fewer than `min_reads` total reads get score = NaN, because\n    a number built from 20 reads is not one we should trust.\n\n    Returns a new DataFrame; the input is left unchanged.\n    """\n    out = df.copy()\n    out["total_reads"] = out[BINS].sum(axis=1)\n    out["score"] = (out[BINS] * list(weights)).sum(axis=1) / out["total_reads"]\n    out.loc[out["total_reads"] < min_reads, "score"] = float("nan")\n    return out',
             "python", "cell", test="s5_func"),
        ul([
            "<code>def name(parameters):</code> starts the recipe. Parameters with <code>=</code> have <strong>defaults</strong>, so callers only mention what they want to change.",
            "The triple-quoted text right under <code>def</code> is the <strong>docstring</strong>. It is what <code>help(add_scores)</code> and <kbd>Shift</kbd>+<kbd>Tab</kbd> show.",
            "<code>return</code> hands the result back. A function with no <code>return</code> gives back <code>None</code>, a classic cause of \"why is my variable empty?\".",
            "<code>df.copy()</code> means the function works on its own copy and never changes the caller's table behind their back.",
        ]),
        h3("Use it"),
        code('scored = add_scores(df)                    # defaults\nstrict = add_scores(df, min_reads=50)      # same recipe, one dial changed\nflat = add_scores(df, weights=(1, 1, 1, 1))\n\nscored[["variant", "replicate", "total_reads", "score"]].head()',
             "python", "cell", test="s5_use"),
        h3("Check it, so you can stop worrying about it"),
        p("An <code>assert</code> silently passes when true and shouts when false. A few of them under a function are tiny, permanent tests:"),
        code('assert len(scored) == len(df)                          # no rows lost\nassert scored["score"].between(1, 4).all()              # scores live in 1-4\nassert strict["score"].isna().sum() == 2                # exactly the 2 low-read rows were blanked\n\nbefore = df.columns.tolist()\nadd_scores(df)\nassert df.columns.tolist() == before                     # the input was not modified',
             "python", "cell", test="s5_tests"),
        callout("note", "If an assert fails",
                p("You will get an <code>AssertionError</code> pointing at that line. That is the point. It is a loud failure that says \"your assumption was wrong\", which is far better than a silent wrong answer. "
                  "Print the pieces and look.")),
        h3("Documentation is a kindness to future you"),
        ul([
            "<strong>Name things for what they are.</strong> <code>add_scores</code> beats <code>func2</code>. Verbs for actions, nouns for data.",
            "<strong>Docstrings say what and why;</strong> comments explain the <em>why</em> of a non-obvious line, not what the code already says.",
            "<strong>Markdown cells are your lab notebook.</strong> Before each section write one sentence: what question this answers and what you decided.",
            "<strong>Keep functions small and single-purpose.</strong> If the docstring needs the word \"and\" three times, split it.",
            "<strong>Show an example</strong> in the docstring or the next cell. Examples are the documentation people actually read.",
        ]),
        p("Later, in Part 2, you will move this function out of the notebook into its own file so that every notebook and script can import it."),
    ],
    [
        puzzle("s5p1", 1,
               p("Define <code>add_scores</code> in your notebook and call it on the toy table. What is the <code>score</code> of <code>p.Ser45Thr</code> in <strong>replicate 1</strong>, to 3 decimal places?"),
               kind="number", placeholder="3 decimal places",
               hint="Call <code>add_scores(df)</code>, then filter on both <code>variant</code> and <code>replicate</code>, and pick the <code>score</code> column.",
               solution='scored = add_scores(df)\nrow = scored[(scored["variant"] == "p.Ser45Thr") & (scored["replicate"] == 1)]\nprint(round(row["score"].iloc[0], 3))', test="s5p1"),
        puzzle("s5p2", 2,
               p("Reuse the same function with <code>min_reads=50</code>. Among rows with <code>variant_type</code> equal to <code>missense</code>, what is the mean <code>score</code> now (3 decimal places)? "
                 "Rows with too few reads should not count. pandas skips <code>NaN</code> when it averages."),
               kind="number", placeholder="3 decimal places",
               hint="One call to <code>add_scores(df, min_reads=50)</code>, filter to missense, <code>.mean()</code>. If your answer feels too high or too low, check how many rows went into it with <code>.count()</code>.",
               solution='strict = add_scores(df, min_reads=50)\nmis = strict[strict["variant_type"] == "missense"]\nprint(round(mis["score"].mean(), 3), mis["score"].count())', test="s5p2"),
    ],
))

from qbuild import *

M = "https://crc-pages.pitt.edu/user-manual/"


def link(path, text):
    return f'<a href="{M}{path}" target="_blank" rel="noopener">{text}</a>'


BATCH = r'''
#!/bin/bash
#SBATCH --job-name=make-figures
#SBATCH --cluster=CLUSTER_NAME        # placeholder: copy real values from the manual
#SBATCH --partition=PARTITION_NAME    # placeholder
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=logs/%x-%j.out       # %x = job name, %j = job id

# 1. make the same Python the same way you did on your laptop
#    (how to load conda or Python on the cluster is on the manual's Python page)
conda activate pandas-quest

# 2. run from the project root so relative paths behave
cd "$SLURM_SUBMIT_DIR"

# 3. run the script, not a notebook
python src/make_figures.py
'''

HPC = stage_html = (
    '<section class="q-stage" id="hpc">'
    '<header class="q-stage-head"><div class="q-stage-title"><span class="q-stage-num">After the summit</span>'
    '<h2>Taking your work to the HPC cluster</h2></div></header>'
    '<p class="q-promise">What this guide was for, when a laptop stops being enough, and how to move the same project onto the cluster. '
    '<span class="q-time">No stars here, just a map.</span></p>'
    '<div class="q-prose">'
    + h3("What this guide was really for")
    + p("Your laptop is where you learn and where you develop. Data is small, feedback is instant, and a mistake costs seconds. "
        "Everything in the twelve stages was practice for the habits that make a cluster usable later:")
    + table(["Habit you built", "Why the cluster needs it"], [
        ["Isolated environment plus <code>environment.yml</code>", "You rebuild the exact same Python on the cluster in one command."],
        ["Scripts like <code>src/make_figures.py</code>", "A cluster job runs a script, not a notebook you click through."],
        ["Relative paths from a project root", "The same code runs in a different folder on a different machine."],
        ["Functions with parameters", "One script can process any sample or setting you hand it."],
        ["Raw data never edited, results regenerated", "Jobs can be re-run safely, and you always know where an output came from."],
        ["Reading the last line of an error", "Failed jobs leave you a log file full of tracebacks. You already know how to read one."],
    ])
    + h3("When do you actually need HPC?")
    + p("Not for this dataset: four thousand rows fit on any laptop. Develop small, then scale up when one of these happens:")
    + ul([
        "<strong>Memory:</strong> you hit <code>MemoryError</code>, or your laptop starts crawling because the data does not fit in RAM.",
        "<strong>Time:</strong> one run takes hours, or you need to repeat it for many samples or many parameter settings.",
        "<strong>Hardware:</strong> you need many cores at once, or a GPU.",
    ])
    + callout("trap", "Never run heavy work on a login node",
              p("When you log in, you land on a shared machine used by everyone to edit files and submit jobs. "
                "Anything big belongs in a job that the scheduler (Slurm) places on a compute node. "
                "Start with an interactive job to try things, and a batch job once it works."))
    + h3("The same project, on the cluster")
    + ol([
        "<strong>Get access.</strong> Request an account and read how resources are allocated: " + link("getting-started/getting-started-step1-account/", "getting an account") + " and " + link("keystone/requesting/", "requesting resources") + ".",
        "<strong>Log in.</strong> Use a terminal (" + link("getting-started/terminal/", "SSH") + ") or the browser portal (" + link("getting-started/open-ondemand/", "Open OnDemand") + "). OnDemand also offers " + link("getting-started/quickstart-python-ondemand/", "Python and Jupyter sessions") + " if you want a notebook on a compute node.",
        "<strong>Bring your code.</strong> Put the project in a Git repository on your laptop, then <code>git clone</code> it on the cluster. Code travels through Git; it keeps a history and avoids \"which copy is newest?\".",
        "<strong>Bring your data.</strong> Large files go through a transfer tool, not Git. See " + link("data-management/file-transfer-methods/", "file transfer") + " (" + link("data-management/file-transfer-methods/globus/", "Globus") + " is the usual choice) and the " + link("data-management/file-systems/", "file systems") + " page to decide where files should live. Big temporary files belong in " + link("slurm/scratch-storage/", "scratch") + ".",
        "<strong>Rebuild the environment.</strong> Load conda or Python the way the " + link("applications/python/", "Python page") + " describes, then recreate yours: <code>conda env create -f environment.yml</code>. This is why you froze it in Stage 6.",
        "<strong>Test on a small slice.</strong> Ask for a short " + link("slurm/interactive-jobs/", "interactive job") + ", run your script on a few rows, and fix errors where you can see them.",
        "<strong>Submit a batch job.</strong> Write a short job script and hand it to Slurm (" + link("slurm/batch-jobs/", "batch jobs") + ").",
        "<strong>Check, then copy results home.</strong> Read the log, confirm the outputs look right, and copy <code>results/</code> back to your laptop for figures and writing.",
    ])
    + h3("A job script")
    + p("A batch script is a shell script with <code>#SBATCH</code> lines that tell Slurm what to reserve. "
        "The names of clusters and partitions, and sensible memory and time requests, are specific to your group; copy real values from the manual rather than from this sketch.")
    + code(BATCH, "bash", "run_make_figures.sh")
    + p("Submit it and keep an eye on it:")
    + code("mkdir -p logs\nsbatch run_make_figures.sh     # prints: Submitted batch job 12345678\nsqueue --me                    # what is queued or running\nsacct -j 12345678              # what happened, after it finishes\nscancel 12345678               # stop it", "bash", "terminal on the cluster")
    + callout("note", "Reading a failed job",
              p("The log file in <code>logs/</code> is your traceback. Open it and go to the bottom, exactly like Stage 2. "
                "A job killed for time or memory says so: ask for a little more of what ran out, not ten times more. "
                "Smaller requests usually start sooner."))
    + h3("Habits that make cluster work painless")
    + ul([
        "<strong>Develop small, run big.</strong> Add a small slice or a <code>--sample</code> option to your script so you can test in seconds.",
        "<strong>Many similar tasks?</strong> Do not write a loop in one long job; use a " + link("slurm/job-arrays/", "job array") + " so each sample runs on its own.",
        "<strong>Keep sessions alive.</strong> " + link("tips/persist-sessions/", "tmux and nohup") + " let long-running work survive a dropped connection.",
        "<strong>Edit comfortably.</strong> VS Code can work on cluster files directly: see the " + link("slurm/vscode/", "VS Code page") + ".",
        "<strong>Record what you ran.</strong> Commit the job script, the <code>environment.yml</code> and the README. Next month, they are your memory.",
        "<strong>Stuck?</strong> Check " + link("faq/", "Common Problems") + " and the " + link("", "main user manual") + ", then ask the support team with the job ID and the last lines of the log.",
    ])
    + p("The full documentation for everything above lives in the " + link("", "CRCD User Manual") + ".")
    + '</div></section>'
)

from qbuild import *
from qbuild import answer_hash

BASE = "https://atharvabhagwat.dev/assets/data/"
PTEN = BASE + "pten-variant-abundance.csv"
REGIONS = BASE + "pten-region-annotations.csv"
STAGES = {}


def add(key, title, promise, blocks, puzzles):
    STAGES[key] = stage(key, title, "", 0, promise, blocks, puzzles)


# ======================================================================= Stage 7: checking real data
S7_ANS = [answer_hash(f"s7p3-{i}", l) for i, l in enumerate("cab")]

add(7, "Checking real data", "Before you plot anything, find out what is in a table, what is missing, and whether the labels mean what they say.", [
    p("Real data arrives with quirks. The habit that separates careful analysts from unlucky ones is a <strong>data audit</strong>: a short, systematic look at the table before you draw any conclusions."),
    h3("What this dataset is about"),
    p("<strong>PTEN</strong> is a human protein that acts as a brake on cell growth signalling. When it is damaged the brake weakens, and changes in the PTEN gene are linked to several cancers and inherited conditions. "
      "Geneticists keep finding single-letter changes in the gene. Many swap one amino acid in the protein for another (a <strong>missense</strong> variant), and for most of them nobody knows whether the change matters."),
    p("A <strong>multiplexed assay of variant effect</strong> attacks this by making thousands of variants at once and measuring each one. "
      "This table comes from an experiment that measured <strong>abundance</strong>: how much of each PTEN variant ends up in the cell. "
      "Each variant is tagged with a fluorescent marker and put into cells. The cells are sorted into four bins from dim to bright and sequenced, so every variant gets a count of reads per bin. "
      "That is the same shape as the toy table in Stage 3, only with about four thousand variants. A change that makes the protein unstable is cleared away by the cell, so its cells look dim."),
    callout("why", "Abundance is not activity, and activity is not disease",
            p("A variant can be plentiful but not working, or scarce and still partly working. Abundance tells you which changes destabilise the protein, which is one useful clue when judging whether a variant is harmful. It is not the final answer.")),
    h3("Two scores, one idea"),
    p("Both the toy table and this table have a column called <code>score</code>, but they are <strong>not the same measurement</strong>."),
    table(["", "Toy table (Stage 4)", "PTEN table (this stage)"], [
        ["How it was made", "You calculated it: a weighted average of the four bins.", "Published by the researchers, from their own analysis."],
        ["Typical range", "1 to 4. Higher means brighter cells.", "About 0 to 1. It has been rescaled."],
        ["Reference points", "None. 4 means every read was in the brightest bin.", "The unchanged protein is set to 1. Broken, cut-short proteins sit near 0."],
    ]),
    p("Both turn \"where along the dim-to-bright scale do this variant's cells land?\" into one number. But the methods and scales differ, so never compare raw numbers across the two tables. Compare patterns <em>inside</em> one table, against that table's own reference points."),
    h3("Load the table"),
    code('import pandas as pd\n\ndf = pd.read_csv("' + PTEN + '")\ndf.head()', "python", "run this", test="z7_load"),
    p("The columns, in plain terms (<code>score</code> matters most):"),
    table(["Column", "Meaning"], [
        ["<code>hgvs_pro</code>", "The variant's name, such as <code>p.Asn12Ile</code>: old amino acid, position, new amino acid."],
        ["<code>score</code>", "The measured abundance. About 1 means \"like the unchanged protein\", about 0 means \"like a broken one\"."],
        ["<code>sd</code>, <code>se</code>, <code>lower_ci</code>, <code>upper_ci</code>", "How uncertain that measurement is."],
        ["<code>expts</code>", "How many experiments contributed to the score."],
        ["<code>record_type</code>", "<code>missense</code> (one amino acid swapped), <code>synonymous</code> (the DNA changed but the amino acid did not), <code>nonsense</code> (a stop signal, so the protein is cut short), <code>wild_type</code> (the unchanged protein itself)."],
        ["<code>abundance_class</code>, <code>abundance_class_label</code>", "A grouped version of the score, as a number and as a word."],
    ]),
    callout("note", "Why look at synonymous and nonsense variants first?",
            p("They are your reference points. Nonsense variants cut the protein short, so they should look broken (scores near 0). Synonymous variants keep the same amino acids, so they are <em>expected</em> to look like the unchanged protein (near 1). "
              "\"Expected\" is the key word: a silent DNA change can occasionally matter for other reasons, which is why you check rather than assume.")),
    code('df.groupby("record_type")["score"].median()', "python", "do the reference points look right?", test="z7_anchor"),
    h3("The audit checklist"),
    code('print(df.shape)                                  # rows, columns\nprint(df.dtypes)                                 # is anything that should be a number stored as text?\nprint(df.isna().sum())                           # missing values in each column\nprint(df["hgvs_pro"].duplicated().sum())         # how many variant names repeat?\nprint(df["record_type"].value_counts())          # how many of each kind', "python", "run this", test="z7_audit"),
    p("If a collaborator tells you how many rows and kinds to expect, check that your table agrees. If a number differs, that is not a nuisance, it is a finding. Write down why."),
    h3("Turn names into columns, one small step at a time"),
    p("A variant name packs three facts into one piece of text. To summarise by position later, you need them in separate columns. You already know the first tool: slicing."),
    code('name = "p.Asn12Ile"\nprint(name[2:5])     # old amino acid\nprint(name[-3:])     # new amino acid', "python", "run this", test="z7_slice1"),
    p("The same slicing works on a whole column when you add <code>.str</code>:"),
    code('df["ref"] = df["hgvs_pro"].str[2:5]\ndf["alt"] = df["hgvs_pro"].str[-3:]\ndf[["hgvs_pro", "ref", "alt"]].head()', "python", "run this", test="z7_slice2"),
    callout("trap", "A method that works on most rows is the dangerous kind",
            p("Look at a synonymous name such as <code>p.Asn12=</code>. Its last three characters are <code>12=</code>, not an amino acid. Check the odd ones on purpose:")
            + code('df[df["hgvs_pro"].str.endswith("=")][["hgvs_pro", "alt"]].head(3)', "python", "run this", test="z7_odd")),
    p("Fix those rows with a filter you already know. Then get the position, which is the digits in the middle. In <code>(\\d+)</code> below, <code>\\d</code> means \"a digit\" and <code>+</code> means \"one or more\": it is a tiny <strong>pattern</strong> for finding numbers in text."),
    code('df.loc[df["hgvs_pro"].str.endswith("="), "alt"] = "="\n\ndf["position"] = pd.to_numeric(df["hgvs_pro"].str.extract(r"(\\d+)", expand=False))\n\ndf[df["position"].isna()]      # which rows have no position, and is that expected?', "python", "run this", test="z7_pos"),
    p("The rows with no position (such as the unchanged-protein row) are your cue to look at them, not to ignore them. Finally, check the labels agree with the names. Each line should print <code>True</code>:"),
    code('print((df.loc[df["record_type"] == "nonsense", "alt"] == "Ter").all())\nprint((df.loc[df["record_type"] == "synonymous", "alt"] == "=").all())', "python", "run this", test="z7_check"),
], [
    puzzle("s7p1", 1, p("How many <strong>rows</strong> does the table have (not counting the header)?"),
           kind="number", placeholder="a whole number", spec=None,
           hint="<code>df.shape</code> gives (rows, columns). <code>len(df)</code> gives the rows directly.", solution='print(len(df))'),
    puzzle("s7p2", 2, p("After adding the <code>position</code> column, how many <strong>different positions</strong> appear in the table? Ignore rows with no position."),
           kind="number", placeholder="a whole number", spec=None,
           hint="<code>df[\"position\"].nunique()</code> counts different values and skips blanks.", solution='print(df["position"].nunique())', test="z7p2"),
    puzzle("s7p3", 3, p("Interpretation time. Pick the best answer for each."), kind="choices",
           choices=[
               ("A learner says: \"a PTEN variant with score 0.9 is <em>lower</em> than a toy variant scoring 3.4, so the PTEN variant is worse.\" What is wrong?",
                ["Nothing; 0.9 is lower than 3.4.", "PTEN scores are wrong because they are below 1.", "The two scores come from different methods and scales, so raw numbers cannot be compared across tables. Compare against each table's own reference points."]),
               ("Why do analysts look at nonsense and synonymous variants before anything else?",
                ["They give reference points: nonsense should look broken and synonymous should look like the unchanged protein, so a surprise means something may be wrong.", "They are the most common variants.", "They are the only variants with scores."]),
               ("A missense variant has a very low abundance score. What can you conclude?",
                ["It causes disease.", "The protein with this change is probably present at lower levels in the cell. Whether it affects function or health needs other evidence.", "It has no effect on PTEN."]),
           ],
           spec={"kind": "choices", "hs": S7_ANS},
           hint="Question 1: ask what \"score\" means in each table. Question 3: abundance and activity are different things."),
])

# ======================================================================= Stage 8: regions
add(8, "Summarising by region", "Label each variant with the part of the protein it falls in, summarise by group, and read the result like a scientist.", [
    p("Stage 7 gave you one row per variant. Questions usually live at a coarser level: <em>per position</em>, <em>per region</em>, <em>per kind</em>. "
      "PTEN has two folded parts, a <strong>phosphatase domain</strong> (the enzyme part) and a <strong>C2 domain</strong> (which helps the protein attach to membranes), followed by a floppy <strong>tail</strong> with no fixed shape. "
      "A second small table lists those stretches with their start and end positions:"),
    code('regions = pd.read_csv("' + REGIONS + '")\nregions', "python", "run this", test="z8_regions"),
    h3("Label each row with its region"),
    p("<code>.between(14, 185)</code> gives True for positions from 14 to 185, including both ends. Use it to fill a new column, one region at a time:"),
    code('df["region"] = "other"\ndf.loc[df["position"].between(14, 185), "region"] = "phosphatase_domain"\ndf.loc[df["position"].between(190, 350), "region"] = "c2_domain"\ndf.loc[df["position"].between(352, 403), "region"] = "disordered_tail"\n\ndf["region"].value_counts()', "python", "run this", test="z8_label"),
    p("The numbers come from the <code>regions</code> table above. (Rows with no position, and positions between regions, stay as <code>other</code>.)"),
    h3("Keep only one kind of variant"),
    p("Different kinds answer different questions. To ask \"how do single amino acid swaps affect abundance?\", keep only the <code>missense</code> rows and give that table a name. <code>.copy()</code> makes it a separate table you can add columns to."),
    code('miss = df[df["record_type"] == "missense"].copy()\nlen(miss)', "python", "run this", test="z8_miss"),
    h3("Summarise by region, with counts"),
    code('by_region = miss.groupby("region")["score"].agg(["count", "mean", "median"])\nby_region', "python", "run this", test="z8_byregion"),
    callout("why", "Always show the count next to the average",
            p("An average of 3 variants and an average of 3,000 look identical in a table. The count tells the reader how much to trust each number. "
              "Comparing the mean with the median helps too: if they differ a lot, the scores are lopsided and one number is hiding something.")),
    h3("Summarise by position"),
    code('by_position = miss.groupby("position")["score"].mean()\nby_position.sort_values().head(10)      # the ten positions with the lowest average', "python", "run this", test="z8_bypos"),
    h3("Read the table like a scientist"),
    p("Numbers become findings only when you ask what they mean. Before the last puzzle of this stage, look at <code>by_region</code> and ask three questions:"),
    ol(["<strong>How big is each group?</strong> A median from 12 variants and one from 1,500 are not equally trustworthy.",
        "<strong>Does the pattern make biological sense?</strong> Folded domains need an exact shape, so changing their amino acids often destabilises them. A floppy tail has no shape to lose.",
        "<strong>What can abundance not tell you?</strong> A region can tolerate changes in abundance and still be essential for function."]),
], [
    puzzle("s8p1", 1, p("Using only <code>missense</code> rows, what is the average <code>score</code> in the <code>phosphatase_domain</code>, to 3 decimal places?"),
           kind="number", placeholder="3 decimal places", spec=None,
           hint="Look at the <code>mean</code> column of <code>by_region</code>, or filter <code>miss</code> on <code>region</code> yourself.",
           solution='print(by_region.loc["phosphatase_domain", "mean"])', test="z8p1"),
    puzzle("s8p2", 2, p("Among the three named regions (<code>phosphatase_domain</code>, <code>c2_domain</code>, <code>disordered_tail</code>), which has the <strong>lowest median</strong> score? Type the region name."),
           kind="text", placeholder="region_name", spec=None,
           hint="Look at the <code>median</code> column of <code>by_region</code>, and ignore the row called <code>other</code>.",
           solution='print(by_region.drop("other")["median"].idxmin())', test="z8p2"),
    puzzle("s8p3", 3,
           p("<strong>Write your interpretation</strong> (about four sentences). Using your own <code>by_region</code> table: which region looks most and which least tolerant of changes, does that make biological sense for a folded domain versus a floppy tail, "
             "and how does the <strong>number of variants in each region</strong> affect how much you trust the comparison?"),
           kind="reflect", minwords=45, placeholder="The ... has the lowest median (value, n = ...), while the ...",
           hint="Start from the numbers: name the regions and quote a median and a count for each. Then give one biological reason and one reason to be careful.",
           model='<h4>A model answer (use your own numbers)</h4>'
                 '<p>"The ___ has the lowest median score (___, n = ___) and the ___ the highest (___, n = ___). '
                 'That fits the idea that folded domains must keep a precise shape, so many amino acid swaps there destabilise the protein, while a floppy tail has no fixed structure to lose. '
                 'The regions have very different numbers of variants, so a median from a small group is less reliable and I would not over-read a small gap. '
                 'Also, abundance is only one property: a region that keeps the protein stable might still matter for activity."</p>'
                 '<h4>Did you cover</h4><ul><li>Named the extreme regions with a number and a count?</li><li>Gave a biological reason and judged whether it fits?</li>'
                 '<li>Said how group size changes your confidence?</li><li>Noted what abundance cannot tell you?</li></ul>'),
])

# ======================================================================= Stage 9: plotting distributions
SETUP_PLOT = ('import matplotlib.pyplot as plt\nimport seaborn as sns\n\nsns.set_theme(style="whitegrid")\n\n'
              'data = df[df["record_type"].isin(["synonymous", "missense", "nonsense"])]')

add(9, "Plotting distributions", "Five plots for the question every experimentalist asks first: what does my data look like, and do my groups differ?", [
    p("You will use two plotting libraries. <strong>matplotlib</strong> is the foundation: it draws and saves pictures. <strong>seaborn</strong> sits on top and draws statistical plots from a table in one line. "
      "Every plot in this stage follows the same three steps: draw it with seaborn, add labels with matplotlib, then show it."),
    p("This stage continues with the table <code>df</code> and the <code>miss</code> table from the previous stages. In the notebook, the first cell sets everything up for you. First, load the plotting tools:"),
    code(SETUP_PLOT, "python", "run this first", test="z9_setup"),
    callout("tip", "Name your axes",
            p("A plot without labels is a rumour. Add a title and label both axes every time, even while exploring. It also forces you to know what the plot says.")),
    h3("Which plot answers which question?"),
    table(["Question", "Plot", "Watch out for"], [
        ["What is the shape of one measurement?", "<strong>Histogram</strong>", "The number of bins changes the picture. Try 20, 40 and 80."],
        ["Compare the centre and spread of groups", "<strong>Box plot</strong>", "It hides the shape. Two humps can look like one box."],
        ["Compare the shapes of groups", "<strong>Violin plot</strong>", "Needs plenty of points per group."],
        ["Show every single observation", "<strong>Strip plot</strong>", "Dots overlap, so make them small and see-through."],
        ["How many of each category?", "<strong>Count plot</strong>", "Bars should start at zero."],
    ]),
    h3("The plots"),
    code('sns.histplot(data=miss, x="score", bins=40)\nplt.title("Missense variants")\nplt.xlabel("abundance score")\nplt.ylabel("number of variants")\nplt.show()', "python", "1. histogram", test="z9_hist"),
    code('sns.boxplot(data=data, x="record_type", y="score")\nplt.title("Score by kind of variant")\nplt.xlabel("kind of variant")\nplt.ylabel("abundance score")\nplt.show()', "python", "2. box plot", test="z9_box"),
    code('sns.violinplot(data=data, x="record_type", y="score")\nplt.title("Score by kind of variant")\nplt.xlabel("kind of variant")\nplt.ylabel("abundance score")\nplt.show()', "python", "3. violin plot", test="z9_violin"),
    code('sns.stripplot(data=data, x="record_type", y="score", size=2, alpha=0.4)\nplt.title("Every variant is a dot")\nplt.xlabel("kind of variant")\nplt.ylabel("abundance score")\nplt.show()', "python", "4. strip plot", test="z9_strip"),
    code('sns.countplot(data=data, x="record_type")\nplt.title("How many variants of each kind")\nplt.xlabel("kind of variant")\nplt.ylabel("number of variants")\nplt.show()', "python", "5. count plot", test="z9_count"),
    h3("Saving a figure"),
    p("Add one line before <code>plt.show()</code> to save the picture as a file. <code>dpi=300</code> makes it sharp enough for print. In Colab, the file appears in the Files panel (the folder icon on the left), where you can download it."),
    code('sns.histplot(data=miss, x="score", bins=40)\nplt.xlabel("abundance score")\nplt.ylabel("number of variants")\nplt.savefig("score_histogram.png", dpi=300, bbox_inches="tight")\nplt.show()', "python", "run this", test="z9_save"),
    callout("why", "Pick the plot after you pick the question",
            p("Do not browse for a pretty chart. Write the sentence you want the reader to take away (\"nonsense variants sit near zero; most missense variants do not\") and choose the plot that makes it obvious.")),
], [
    puzzle("s9p1", 1, p("What is the <strong>median</strong> <code>score</code> of the <code>nonsense</code> variants, to 2 decimal places? It is the line in the middle of the nonsense box in the box plot."),
           kind="number", placeholder="2 decimal places", spec=None,
           hint="Keep the rows where <code>record_type</code> is <code>\"nonsense\"</code>, take the <code>score</code> column, and use <code>.median()</code>.",
           solution='print(df[df["record_type"] == "nonsense"]["score"].median())', test="z9p1"),
    puzzle("s9p2", 2, p("The histogram of missense scores is rarely one tidy hump. How many missense variants have a <code>score</code> <strong>strictly below 0.5</strong>?"),
           kind="number", placeholder="a whole number", spec=None,
           hint="<code>miss[miss[\"score\"] &lt; 0.5]</code> keeps those rows. Count them with <code>len(...)</code>.",
           solution='print(len(miss[miss["score"] < 0.5]))', test="z9p2"),
])

# ======================================================================= Stage 10: more plots
add(10, "More plots", "Optional: scatter plots, a line along the protein, and a heatmap that shows thousands of values at once.", [
    p("These plots answer \"what goes with what?\" and \"where along the protein?\". They use the same pattern as before: draw, label, show. Skip this stage if you are short of time; the plots in Stage 8 are enough for most work."),
    h3("Two measurements against each other"),
    code('sns.scatterplot(data=miss, x="se", y="score", alpha=0.4)\nplt.title("Do noisier measurements score differently?")\nplt.xlabel("standard error")\nplt.ylabel("abundance score")\nplt.show()', "python", "scatter plot", test="z10_scatter"),
    h3("Along the protein"),
    p("Position goes on the x-axis and the average score on the y-axis. Dips show where changes hurt the most."),
    code('by_position = miss.groupby("position")["score"].mean()\n\nplt.plot(by_position.index, by_position.values)\nplt.title("Average score along the protein")\nplt.xlabel("position")\nplt.ylabel("average abundance score")\nplt.show()', "python", "line plot", test="z10_line"),
    h3("A heatmap"),
    p("One small square for every swap: the position along the bottom, the new amino acid up the side, and the colour for the score. Vertical stripes mean \"this position dislikes every change\". Grey squares were not measured."),
    code('grid = miss.pivot_table(index="alt", columns="position", values="score")\ngrid.columns = grid.columns.astype(int)\n\nplt.figure(figsize=(12, 5))\nsns.heatmap(grid, cmap="viridis", vmin=0, vmax=1.2, xticklabels=25)\nplt.title("Score for every amino acid swap")\nplt.xlabel("position")\nplt.ylabel("new amino acid")\nplt.show()', "python", "heatmap", test="z10_heat"),
    callout("tip", "Make a heatmap readable",
            ul(["Fix <code>vmin</code> and <code>vmax</code> so the same colour always means the same value.",
                "Use a colormap like <code>viridis</code> that is easy on the eye. Avoid rainbow colours.",
                "Show missing squares honestly (blank), not as zero."])),
    h3("Windows along the protein"),
    p("Group neighbouring positions into windows of 10: <code>position // 10 * 10</code> turns 123 into 120. Then summarise each window."),
    code('miss["window"] = miss["position"] // 10 * 10\n\ncounts = miss.groupby("window").size()\nmeans = miss.groupby("window")["score"].mean()\n\nmeans[counts >= 30].sort_values().head()', "python", "run this", test="z10_window"),
], [
    puzzle("s10p1", 1, p("Using only <code>missense</code> rows, group by the new amino acid (<code>alt</code>) and take the average <code>score</code>. Which new amino acid, written as its three letters like <code>Ala</code>, has the <strong>lowest</strong> average?"),
           kind="text", placeholder="Xxx", spec=None,
           hint="<code>miss.groupby(\"alt\")[\"score\"].mean().idxmin()</code>.",
           solution='print(miss.groupby("alt")["score"].mean().idxmin())', test="z10p1"),
    puzzle("s10p2", 2, p("In windows of 10 positions, among windows with <strong>at least 30 missense variants</strong>, which window has the lowest average score? Answer with the window's starting number."),
           kind="number", placeholder="a multiple of 10", spec=None,
           hint="The last code cell already does it: <code>means[counts &gt;= 30]</code> keeps windows with enough variants, and <code>.idxmin()</code> finds the lowest.",
           solution='print(means[counts >= 30].idxmin())', test="z10p2"),
])

# ======================================================================= Stage 11: checking your conclusion
add(11, "Checking your conclusion", "A result is only as solid as the choices behind it. Change one rule, see how far the answer moves, and write down what you conclude.", [
    p("Every analysis hides judgement calls: which rows to keep, where to draw a line. A trustworthy analysis shows how much the answer <em>depends</em> on them. "
      "Today's question: <strong>should we trust variants that were measured in only a couple of experiments?</strong>"),
    p("Use the <code>miss</code> table from before. First, the missense variants in the phosphatase domain:"),
    code('phos = miss[miss["region"] == "phosphatase_domain"]\n\nprint(len(phos), "variants, average score", phos["score"].mean())', "python", "run this", test="z11_phos"),
    p("Now keep only variants measured in at least 3 experiments and compare:"),
    code('strict = phos[phos["expts"] >= 3]\n\nprint(len(strict), "variants, average score", strict["score"].mean())\nprint("change in the average:", strict["score"].mean() - phos["score"].mean())', "python", "run this", test="z11_strict"),
    p("One comparison could be luck. Try several settings and look at the whole picture, not one cherry-picked value. A loop does it in a few lines:"),
    code('for minimum in [1, 2, 3, 4, 5, 6]:\n    kept = phos[phos["expts"] >= minimum]\n    print("at least", minimum, "experiments:", len(kept), "variants, average", kept["score"].mean())', "python", "run this", test="z11_loop"),
    p("If the average barely moves while the number of variants falls, the conclusion is <strong>robust</strong> to this choice. If it swings, say so. Either answer is a result."),
    callout("why", "This is the heart of reproducible research",
            p("Readers should be able to see how much your answer depends on your choices. Writing the choice into the code, with a number you can change, lets them.")),
    h3("Write the conclusion"),
    p("A number is not a conclusion. A conclusion says what you found, how sure you are, and what could change it. Look at your loop output: how many variants does each setting keep, and how far does the average move?"),
], [
    puzzle("s11p1", 1, p("Keep only rows whose <code>expts</code> is <strong>at least 3</strong>, across the whole table (every kind of variant). How many rows remain?"),
           kind="number", placeholder="a whole number", spec=None,
           hint="<code>len(df[df[\"expts\"] &gt;= 3])</code>. Rows with a blank <code>expts</code> do not pass the test, so they are not counted.",
           solution='print(len(df[df["expts"] >= 3]))', test="z11p1"),
    puzzle("s11p2", 2, p("For the missense variants in the <code>phosphatase_domain</code>: the average score <strong>with</strong> the rule <code>expts &gt;= 3</code> minus the average <strong>without</strong> it. Give the difference to 3 decimal places, keeping the sign."),
           kind="number", placeholder="e.g. -0.012", spec=None,
           hint="The code above already prints it as <code>change in the average</code>. A tiny difference is good news for how robust the earlier answer was.",
           solution='print(strict["score"].mean() - phos["score"].mean())', test="z11p2"),
    puzzle("s11p3", 3,
           p("<strong>Write a short conclusion</strong> (four to six sentences) about the phosphatase domain, as you would in a lab meeting. Include the average with and without the rule, how many variants each keeps, "
             "whether you think the conclusion is robust to this choice, and one other analysis choice that could change it."),
           kind="reflect", minwords=55, placeholder="Using all variants, the average score in the phosphatase domain is ... After requiring at least 3 experiments ...",
           hint="Use this order: the finding with numbers, how it changed, how confident you are, and one caveat.",
           model='<h4>A model answer (use your own numbers)</h4>'
                 '<p>"Across all ___ missense variants in the phosphatase domain the average score is ___. Requiring at least 3 experiments keeps ___ variants and moves the average to ___ (a change of ___). '
                 'Because the shift is [small / large] compared with the spread between variants, I consider the domain-level conclusion [robust / sensitive] to this rule. '
                 'The loop shows the estimate [settles / keeps changing] as the threshold rises, but keeping fewer variants makes the average noisier. '
                 'Other choices could matter too, such as dropping variants with large standard errors or using the median instead of the average, so I would check those next before claiming anything strongly."</p>'
                 '<h4>Did you cover</h4><ul><li>Both averages and both counts?</li><li>A judgement about robustness, with a reason?</li>'
                 '<li>The cost of keeping fewer variants?</li><li>A different choice that could change the result?</li></ul>'),
])

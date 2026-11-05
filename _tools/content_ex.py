"""Practice exercises. Each has starter code, a self-check cell and a hidden solution."""
from qbuild import code, details, esc

EXERCISES = []   # dicts, used by the test harness
BY_STAGE = {}    # stage number -> list of html


STRETCH = {"e2b", "e4c", "e5c", "e7b", "e8b", "e8c", "e10a", "e10b", "e10c", "e11b", "e6a", "e6b"}


def ex(stage, eid, title, task, starter, tests, solution, stretch=False, lang="python"):
    stretch = stretch or eid in STRETCH
    EXERCISES.append(dict(stage=stage, id=eid, title=title, starter=starter.strip("\n"),
                          tests=(tests or "").strip("\n"), solution=solution.strip("\n"), manual=tests is None))
    html = (
        f'<div class="q-ex" data-ex="{eid}">'
        f'<div class="q-ex-head"><h4>Your turn: {title}{" <span class=\"q-badge is-stretch\">Stretch</span>" if stretch else ""}</h4>'
        f'<label class="q-ex-done"><input type="checkbox" class="q-ex-check"> Done</label></div>'
        f'<div class="q-ex-task">{task}</div>'
        + code(starter, lang, "starter: copy into a cell and complete it" if lang == "python" else "your commands")
        + (code(tests + '\nprint("all checks passed")', "python", "check: run this after your code") if tests is not None else "")
        + details("Show a solution (try for ten minutes first)", code(solution, lang, "one solution"), "q-ex-sol")
        + '</div>'
    )
    BY_STAGE.setdefault(stage, []).append(html)


INTRO = (
    '<h3>Practice: your turn</h3>'
    '<p>Reading code teaches you what code looks like; writing it teaches you to code. '
    'Do these in your notebook. Each has a starter, a <strong>check cell</strong> that stays silent when you are right and raises an error when you are not '
    '(read it: that is your Stage 2 skill at work), and a hidden solution. Tick <em>Done</em> when the check prints <code>all checks passed</code>.</p>'
)

# ===================================================================== stage 1
ex(1, "e1a", "count a letter",
   "<code>seq</code> is a short protein sequence. <strong>Without</strong> using <code>seq.count</code>, use a loop to count how many times the letter <code>\"I\"</code> appears and store it in <code>n_I</code>.",
   'seq = "MTAIIKEIVSRNKRR"\n\nn_I = 0\n# TODO: loop over seq and add 1 to n_I for every "I"',
   'assert n_I == 3',
   'seq = "MTAIIKEIVSRNKRR"\n\nn_I = 0\nfor letter in seq:\n    if letter == "I":\n        n_I += 1')

ex(1, "e1b", "letter frequencies",
   "Build a <strong>dictionary</strong> <code>counts</code> that maps every letter of <code>seq</code> to how many times it occurs, for example <code>{\"M\": 1, \"I\": 3, ...}</code>. "
   "Hint: <code>counts.get(letter, 0)</code> returns 0 for a letter you have not seen yet.",
   'seq = "MTAIIKEIVSRNKRR"\n\ncounts = {}\n# TODO: loop over seq and update counts',
   'assert counts["R"] == 3 and counts["I"] == 3 and counts["K"] == 2\nassert sum(counts.values()) == len(seq)',
   'seq = "MTAIIKEIVSRNKRR"\n\ncounts = {}\nfor letter in seq:\n    counts[letter] = counts.get(letter, 0) + 1')

ex(1, "e1c", "filter with a comprehension",
   "From <code>variants</code>, make a list <code>late</code> holding the <strong>positions (as integers)</strong> that are greater than 30, using a single list comprehension.",
   'variants = ["p.Gly12Gly", "p.Trp18Ter", "p.Leu25Pro", "p.Val30Asp",\n            "p.Gln36Ter", "p.Ile40Asn", "p.Ser45Thr", "p.Gly46Arg"]\n\nlate = []   # TODO: replace with a list comprehension',
   'assert late == [36, 40, 45, 46]',
   'variants = ["p.Gly12Gly", "p.Trp18Ter", "p.Leu25Pro", "p.Val30Asp",\n            "p.Gln36Ter", "p.Ile40Asn", "p.Ser45Thr", "p.Gly46Arg"]\n\nlate = [int(v[5:-3]) for v in variants if int(v[5:-3]) > 30]')

# ===================================================================== stage 2
ex(2, "e2a", "fix three small bugs",
   "Each pair of lines has a bug that raises an error. Run the cell, read the error, fix one line at a time. The comment says what you want.",
   'names = ["WT", "p.Trp18Ter", "p.Leu25Pro"]\nlast = names[3]            # want the last name\n\nscores = {"WT": 3.49, "p.Trp18Ter": 1.5}\nwt_score = scores["wt"]    # want the WT score\n\nreads = ["120", "80", "45"]\ntotal = sum(reads)         # want 245',
   'assert last == "p.Leu25Pro"\nassert wt_score == 3.49\nassert total == 245',
   'names = ["WT", "p.Trp18Ter", "p.Leu25Pro"]\nlast = names[-1]\n\nscores = {"WT": 3.49, "p.Trp18Ter": 1.5}\nwt_score = scores["WT"]\n\nreads = ["120", "80", "45"]\ntotal = sum(int(r) for r in reads)')

ex(2, "e2b", "catch errors on purpose",
   "Each snippet below fails in a different way. Loop over them, run each inside <code>try</code>/<code>except Exception as e</code>, and append the <strong>name of the error type</strong> "
   "(<code>type(e).__name__</code>) to <code>error_names</code>. You will see all five names from the cheat sheet, and learn how programs survive errors.",
   'snippets = [\n    lambda: undefined_name,\n    lambda: "a" + 1,\n    lambda: {"a": 1}["b"],\n    lambda: [1, 2][5],\n    lambda: int("x"),\n]\n\nerror_names = []\nfor run in snippets:\n    pass   # TODO: try run(), except Exception as e, record type(e).__name__',
   'assert error_names == ["NameError", "TypeError", "KeyError", "IndexError", "ValueError"]',
   'snippets = [\n    lambda: undefined_name,\n    lambda: "a" + 1,\n    lambda: {"a": 1}["b"],\n    lambda: [1, 2][5],\n    lambda: int("x"),\n]\n\nerror_names = []\nfor run in snippets:\n    try:\n        run()\n    except Exception as e:\n        error_names.append(type(e).__name__)')

# ===================================================================== stage 3
ex(3, "e3a", "name the nonsense",
   "Using the toy table <code>df</code>, make a <strong>sorted list of unique variant names</strong> whose <code>variant_type</code> is <code>nonsense</code>, called <code>nonsense_names</code>.",
   'nonsense_names = []   # TODO: filter df, take the variant column, make it unique and sorted',
   'assert nonsense_names == ["p.Gln36Ter", "p.Trp18Ter", "p.Tyr52Ter"]',
   'nonsense_names = sorted(df.loc[df["variant_type"] == "nonsense", "variant"].unique())')

ex(3, "e3b", "which rows are bright?",
   "In <strong>replicate 1</strong>, find the variants whose <code>bin4_count</code> is greater than their <code>bin1_count</code> (more reads in the brightest bin than the dimmest). "
   "Store the names as a sorted list called <code>bright</code>. Compare two columns, then combine with the replicate filter.",
   'bright = []   # TODO',
   'assert "p.Leu25Pro" not in bright and "p.Trp18Ter" not in bright\nassert "p.Lys50Arg" in bright and len(bright) == 7',
   'rep1 = df[df["replicate"] == 1]\nbright = sorted(rep1.loc[rep1["bin4_count"] > rep1["bin1_count"], "variant"])')

ex(3, "e3c", "top three",
   "Among <code>missense</code> rows of <strong>replicate 2</strong>, sort by <code>bin1_count</code> from largest to smallest and keep the <strong>top 3 variant names</strong> in a list called <code>top3</code>.",
   'top3 = []   # TODO: filter, sort_values(..., ascending=False), head(3), then tolist()',
   'assert top3 == ["p.Leu25Pro", "p.Gly46Arg", "p.Val30Asp"]',
   'sub = df[(df["variant_type"] == "missense") & (df["replicate"] == 2)]\ntop3 = sub.sort_values("bin1_count", ascending=False).head(3)["variant"].tolist()')

# ===================================================================== stage 4
ex(4, "e4a", "a fraction column",
   "Continue in your Stage 4 notebook, where <code>df</code> already has <code>total_reads</code>. Add a column <code>frac_bin4</code>: the share of each row's reads that fall in bin 4. "
   "Then find the <strong>replicate 1</strong> variant with the highest <code>frac_bin4</code> and store its name in <code>top_variant</code>.",
   'top_variant = ""   # TODO',
   'assert "frac_bin4" in df.columns\nassert df["frac_bin4"].between(0, 1).all()\nassert top_variant == "p.Lys50Arg"',
   'df["frac_bin4"] = df["bin4_count"] / df["total_reads"]\nrep1 = df[df["replicate"] == 1]\ntop_variant = rep1.loc[rep1["frac_bin4"].idxmax(), "variant"]')

ex(4, "e4b", "scores by type",
   "Make a Series <code>type_means</code> with the mean <code>score</code> for each <code>variant_type</code>. Two of its facts will be checked: which type scores lowest, and which highest.",
   'type_means = None   # TODO: groupby + mean',
   'assert type_means.idxmin() == "nonsense"\nassert type_means.idxmax() == "wild_type"\nassert len(type_means) == 4',
   'type_means = df.groupby("variant_type")["score"].mean()')

ex(4, "e4c", "a summary table",
   "Build a DataFrame <code>summary</code> with <strong>one row per variant</strong> (variant name as the index) and two columns: <code>mean_score</code> (mean over replicates) and <code>rep_diff</code> (absolute difference between replicate 1 and 2). "
   "Combine <code>groupby</code>, <code>pivot</code> and a join, or use <code>agg</code> cleverly. Several routes work.",
   'summary = None   # TODO',
   'assert summary.shape == (12, 2)\nassert list(summary.columns) == ["mean_score", "rep_diff"]\nassert abs(summary.loc["p.Ala58Val", "rep_diff"] - 1.15) < 1e-9',
   'wide = df.pivot(index="variant", columns="replicate", values="score")\nsummary = pd.DataFrame({\n    "mean_score": wide.mean(axis=1),\n    "rep_diff": (wide[1] - wide[2]).abs(),\n})')

# ===================================================================== stage 5
ex(5, "e5a", "fraction_in_bin",
   "Write a function <code>fraction_in_bin(df, k)</code> that returns a Series: the fraction of each row's reads that fall in bin <code>k</code> (1 to 4). "
   "Include a docstring, and <code>raise ValueError(\"k must be 1, 2, 3 or 4\")</code> if <code>k</code> is anything else.",
   'def fraction_in_bin(df, k):\n    # TODO: docstring, validation, calculation\n    pass',
   'f = fraction_in_bin(df, 4)\nassert abs(f.iloc[0] - 376 / 694) < 1e-9\nassert f.between(0, 1).all() and len(f) == len(df)\ntry:\n    fraction_in_bin(df, 5)\n    raise AssertionError("k=5 should raise ValueError")\nexcept ValueError:\n    pass\nassert fraction_in_bin.__doc__',
   'def fraction_in_bin(df, k):\n    """Fraction of each row\'s reads in bin k (1 to 4)."""\n    if k not in (1, 2, 3, 4):\n        raise ValueError("k must be 1, 2, 3 or 4")\n    bins = ["bin1_count", "bin2_count", "bin3_count", "bin4_count"]\n    return df[f"bin{k}_count"] / df[bins].sum(axis=1)')

ex(5, "e5b", "flag_low_coverage",
   "Write <code>flag_low_coverage(df, min_reads=50)</code> returning a <strong>boolean Series</strong> that is <code>True</code> for rows whose total reads (sum of the four bins) are below <code>min_reads</code>.",
   'def flag_low_coverage(df, min_reads=50):\n    pass   # TODO',
   'assert flag_low_coverage(df).sum() == 2\nassert flag_low_coverage(df, min_reads=10_000).all()\nassert not flag_low_coverage(df, min_reads=1).any()',
   'def flag_low_coverage(df, min_reads=50):\n    """True for rows with fewer than min_reads total reads."""\n    bins = ["bin1_count", "bin2_count", "bin3_count", "bin4_count"]\n    return df[bins].sum(axis=1) < min_reads')

ex(5, "e5c", "summarise_variants",
   "Reuse <code>add_scores</code> from this stage. Write <code>summarise_variants(df, min_reads=50)</code> returning a DataFrame indexed by variant with two columns: "
   "<code>mean_score</code> (mean over replicates, ignoring masked rows) and <code>n_used</code> (how many rows contributed). Calling a function from inside another is how real code grows.",
   'def summarise_variants(df, min_reads=50):\n    pass   # TODO: scored = add_scores(...), then groupby("variant")',
   's = summarise_variants(df)\nassert s.shape == (12, 2)\nassert s.loc["p.Ala58Val", "n_used"] == 0\nassert s.loc["WT", "n_used"] == 2\nassert abs(s.loc["WT", "mean_score"] - 3.49) < 0.01',
   'def summarise_variants(df, min_reads=50):\n    """Mean score and number of usable rows per variant."""\n    scored = add_scores(df, min_reads=min_reads)\n    return scored.groupby("variant")["score"].agg(mean_score="mean", n_used="count")')

# ===================================================================== stage 6
ex(6, "e6a", "file_fingerprint",
   "Write <code>file_fingerprint(path)</code> that returns the SHA-256 of a file as a hex string. Then add it to <code>src/vampseq_tools.py</code> so any notebook can import it. "
   "(Test it here first; the check writes a tiny temporary file.)",
   'import hashlib\nfrom pathlib import Path\n\n\ndef file_fingerprint(path):\n    pass   # TODO',
   'import tempfile\nwith tempfile.TemporaryDirectory() as folder:\n    p = Path(folder) / "abc.txt"\n    p.write_bytes(b"abc")\n    assert file_fingerprint(p) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"\n    assert file_fingerprint(str(p)) == file_fingerprint(p)   # accepts a str as well',
   'import hashlib\nfrom pathlib import Path\n\n\ndef file_fingerprint(path):\n    """SHA-256 of a file, as a hex string."""\n    return hashlib.sha256(Path(path).read_bytes()).hexdigest()')

ex(6, "e6b", "ensure_dirs",
   "Write <code>ensure_dirs(root, names)</code> that creates each folder in <code>names</code> under <code>root</code> (including nested ones such as <code>\"results/figures\"</code>) "
   "and returns the list of names it <strong>newly created</strong>. Calling it twice must not fail, and the second call returns an empty list. This is the skeleton command from earlier, turned into a reusable tool.",
   'from pathlib import Path\n\n\ndef ensure_dirs(root, names):\n    pass   # TODO',
   'import tempfile\nwith tempfile.TemporaryDirectory() as folder:\n    wanted = ["data/raw", "notebooks", "results/figures"]\n    assert ensure_dirs(folder, wanted) == wanted\n    assert all((Path(folder) / n).is_dir() for n in wanted)\n    assert ensure_dirs(folder, wanted) == []',
   'from pathlib import Path\n\n\ndef ensure_dirs(root, names):\n    """Create folders under root. Return the names that did not exist yet."""\n    created = []\n    for name in names:\n        path = Path(root) / name\n        if not path.exists():\n            path.mkdir(parents=True)\n            created.append(name)\n    return created')

# ===================================================================== stage 7
ex(7, "e7a", "an audit function",
   "Turn the audit checklist into a function. Write <code>audit(df)</code> returning a dictionary with keys "
   "<code>rows</code>, <code>columns</code>, <code>missing_cells</code> (total missing values in the whole table), <code>duplicate_names</code> (rows whose <code>hgvs_pro</code> repeats an earlier one) "
   "and <code>by_type</code> (a dictionary of <code>record_type</code> counts). Run it on every new dataset from now on.",
   'def audit(df):\n    pass   # TODO',
   'tiny = pd.DataFrame({"hgvs_pro": ["a", "b", "b"], "score": [1.0, None, 2.0], "record_type": ["x", "x", "y"]})\nr = audit(tiny)\nassert r["rows"] == 3 and r["columns"] == 3\nassert r["missing_cells"] == 1 and r["duplicate_names"] == 1\nassert r["by_type"] == {"x": 2, "y": 1}\nprint(audit(df))',
   'def audit(df):\n    """Quick facts about a variant table."""\n    return {\n        "rows": len(df),\n        "columns": df.shape[1],\n        "missing_cells": int(df.isna().sum().sum()),\n        "duplicate_names": int(df.duplicated(subset="hgvs_pro").sum()),\n        "by_type": df["record_type"].value_counts().to_dict(),\n    }')

ex(7, "e7b", "split one variant name",
   "Without pandas this time. Write <code>split_variant(name)</code> using <code>re.match</code> and the pattern from this stage. "
   "It returns a tuple <code>(ref, position, alt)</code> with the position as an <code>int</code>, or <code>None</code> if the name does not match.",
   'import re\n\n\ndef split_variant(name):\n    pass   # TODO',
   'assert split_variant("p.Trp18Ter") == ("Trp", 18, "Ter")\nassert split_variant("p.Asn12=") == ("Asn", 12, "=")\nassert split_variant("_wt") is None\nassert split_variant("p.Gly12_Asp13del") is None',
   'import re\n\n\ndef split_variant(name):\n    """Return (ref, position, alt) or None."""\n    m = re.match(r"^p\\.([A-Za-z]{3})(\\d+)([A-Za-z]{3}|=)$", name)\n    if m is None:\n        return None\n    return m.group(1), int(m.group(2)), m.group(3)')

# ===================================================================== stage 8
ex(8, "e8a", "a reusable group summary",
   "Write <code>summarise_by(df, column)</code> that keeps only <code>missense</code> rows, groups by <code>column</code>, and returns a DataFrame with columns <code>n</code>, <code>mean</code> and <code>median</code> of the score. "
   "One function now answers \"by region?\", \"by new letters?\", \"by anything?\".",
   'def summarise_by(df, column):\n    pass   # TODO',
   't = summarise_by(df, "region")\nassert list(t.columns) == ["n", "mean", "median"]\nassert t["n"].sum() == (df["record_type"] == "missense").sum()\nassert 19 <= len(summarise_by(df, "alt")) <= 20',
   'def summarise_by(df, column):\n    """n, mean and median missense score per group."""\n    miss = df[df["record_type"] == "missense"]\n    return miss.groupby(column)["score"].agg(n="size", mean="mean", median="median")')

ex(8, "e8b", "the most sensitive positions",
   "Among positions with <strong>at least 15 missense variants</strong>, find the <strong>10 positions with the lowest mean missense score</strong>. Store them, lowest first, in a list <code>most_sensitive</code>. "
   "Your <code>miss</code> table from this stage is the starting point.",
   'most_sensitive = []   # TODO: groupby position, filter on n, sort, head(10)',
   'g = miss.groupby("position")["score"].agg(n="size", mean="mean")\ng = g[g["n"] >= 15].sort_values("mean")\nassert len(most_sensitive) == 10\nassert [int(p) for p in most_sensitive] == [int(p) for p in g.index[:10]]',
   'g = miss.groupby("position")["score"].agg(n="size", mean="mean")\ng = g[g["n"] >= 15].sort_values("mean")\nmost_sensitive = list(g.index[:10])')

ex(8, "e8c", "attach the notes",
   "The regions table has an <code>annotation</code> column with a plain-English description. Merge it onto <code>df</code> through the <code>region</code> column so every row gets its description (rows with no region stay, with a blank). "
   "Call the result <code>with_notes</code>, and make sure the row count did not change.",
   'with_notes = None   # TODO: df.merge(...)',
   'assert len(with_notes) == len(df)\nassert "annotation" in with_notes.columns\nassert with_notes.loc[with_notes["region"] == "phosphatase_domain", "annotation"].notna().all()',
   'with_notes = df.merge(regions[["region", "annotation"]], on="region", how="left")')

# ===================================================================== stage 9
ex(9, "e9a", "a plotting function",
   "Write <code>plot_ecdf_by(data, column, ax)</code> that draws one ECDF line per group of <code>column</code> onto the given <code>ax</code>, labels the x-axis, and <strong>returns the axes</strong>. "
   "Functions that take an <code>ax</code> can be dropped into any multi-panel figure.",
   'def plot_ecdf_by(data, column, ax):\n    pass   # TODO',
   'fig, ax = plt.subplots()\nout = plot_ecdf_by(data, "record_type", ax)\nassert out is ax\nassert len(ax.lines) >= 3\nassert ax.get_xlabel() != ""',
   'def plot_ecdf_by(data, column, ax):\n    """One ECDF line per group, drawn onto ax."""\n    sns.ecdfplot(data=data, x="score", hue=column, ax=ax)\n    ax.set(xlabel="abundance score", ylabel="cumulative fraction")\n    return ax')

ex(9, "e9b", "design your own figure",
   "Make a figure with two panels side by side: on the left a <strong>histogram</strong> of missense scores (30 bins); on the right a <strong>box plot</strong> of missense score by <code>region</code>. "
   "Label all axes, tidy the layout, and save it as <code>my_figure.png</code> in <code>results/figures</code> at 300 dpi. Choose colours you would be happy to show a supervisor.",
   'fig, axes = plt.subplots(1, 2, figsize=(11, 4))\n# TODO: left panel, right panel, labels, tight_layout, savefig',
   'assert (FIGS / "my_figure.png").exists() and (FIGS / "my_figure.png").stat().st_size > 10_000\nassert len(axes[0].patches) > 10\nassert axes[0].get_xlabel() != "" and axes[1].get_ylabel() != ""',
   'miss = df[df["record_type"] == "missense"]\nfig, axes = plt.subplots(1, 2, figsize=(11, 4))\nsns.histplot(data=miss, x="score", bins=30, ax=axes[0])\nsns.boxplot(data=miss, x="region", y="score", ax=axes[1])\naxes[0].set(xlabel="abundance score", ylabel="number of variants")\naxes[1].set(xlabel="region", ylabel="abundance score")\naxes[1].tick_params(axis="x", rotation=30)\nfig.tight_layout()\nfig.savefig(FIGS / "my_figure.png", dpi=300, bbox_inches="tight")')

# ==================================================================== stage 10
ex(10, "e10a", "window_means",
   "Generalise the 10-position windows from the puzzle. Write <code>window_means(miss, size=10)</code> returning a DataFrame with columns <code>window</code>, <code>n</code> and <code>mean</code> (mean missense score), one row per window of <code>size</code> positions.",
   'def window_means(miss, size=10):\n    pass   # TODO',
   'w10 = window_means(miss)\nw25 = window_means(miss, size=25)\nassert list(w10.columns) == ["window", "n", "mean"]\nassert len(w25) < len(w10)\nassert w10["n"].sum() == len(miss)\nassert (w25["window"] % 25 == 0).all()',
   'def window_means(miss, size=10):\n    """Mean missense score in windows of `size` positions."""\n    windows = miss["position"] // size * size\n    out = miss.groupby(windows)["score"].agg(n="size", mean="mean")\n    out.index.name = "window"\n    return out.reset_index()')

ex(10, "e10b", "zoom in on a stretch",
   "Draw the heatmap again, but only for <strong>positions 100 to 140</strong>, with the new letters in the order of <code>AA</code>. Store the pivoted table in <code>grid_zoom</code> and plot it with <code>annot=False</code> and tick labels on every position. "
   "Zooming in is how you turn a pattern into a story.",
   'grid_zoom = None   # TODO: filter positions, pivot_table, reindex(AA)\n# TODO: sns.heatmap(...)',
   'assert grid_zoom.shape[0] == 20\nassert 1 <= grid_zoom.shape[1] <= 41\nassert min(int(c) for c in grid_zoom.columns) >= 100 and max(int(c) for c in grid_zoom.columns) <= 140',
   'zoom = miss[miss["position"].between(100, 140)]\ngrid_zoom = zoom.pivot_table(index="alt", columns="position", values="score").reindex(AA)\nfig, ax = plt.subplots(figsize=(12, 4.5))\nax.set_facecolor("#dddddd")\nsns.heatmap(grid_zoom, cmap="viridis", vmin=0, vmax=1.2, xticklabels=1, ax=ax)')

ex(10, "e10c", "does noisier mean lower?",
   "For each position compute the mean missense <code>score</code> and the mean <code>se</code> (put them in a DataFrame <code>by_pos</code> with columns <code>mean_score</code> and <code>mean_se</code>). "
   "Draw a scatter of one against the other, and store the <strong>Spearman correlation</strong> between the two columns in <code>rho</code>. Then write one sentence in a Markdown cell: what does the plot say?",
   'by_pos = None   # TODO\nrho = None      # TODO',
   'assert list(by_pos.columns) == ["mean_score", "mean_se"]\nassert -1 <= rho <= 1\nassert abs(rho - by_pos["mean_score"].corr(by_pos["mean_se"], method="spearman")) < 1e-12',
   'by_pos = miss.groupby("position").agg(mean_score=("score", "mean"), mean_se=("se", "mean"))\nrho = by_pos["mean_score"].corr(by_pos["mean_se"], method="spearman")\nfig, ax = plt.subplots(figsize=(5.5, 4.5))\nsns.scatterplot(data=by_pos, x="mean_se", y="mean_score", s=14, ax=ax)\nax.set(xlabel="mean standard error", ylabel="mean score", title=f"Spearman rho = {rho:.2f}")')

# ==================================================================== stage 11
ex(11, "e11a", "sweep as a function",
   "Write <code>sweep(df, ks)</code> that calls <code>summarise</code> for every value in <code>ks</code> and returns a DataFrame with columns <code>min_expts</code>, <code>n_variants</code>, <code>mean_score</code>. "
   "Then call it with <code>[1, 3, 5, 7]</code> and plot <code>mean_score</code> against <code>min_expts</code>.",
   'def sweep(df, ks):\n    pass   # TODO',
   's = sweep(df, [1, 3, 5])\nassert list(s.columns) == ["min_expts", "n_variants", "mean_score"]\nassert len(s) == 3\nassert s["n_variants"].is_monotonic_decreasing',
   'def sweep(df, ks):\n    """Mean missense score in the phosphatase domain for each min_expts."""\n    rows = []\n    for k in ks:\n        r = summarise(df, min_expts=k)\n        rows.append({"min_expts": k, "n_variants": int(r["count"]), "mean_score": r["mean"]})\n    return pd.DataFrame(rows)')

ex(13, "e11b", "your own report script",
   "Create <code>src/report.py</code>: a script, not a notebook, that loads the two CSVs from <code>data/raw</code> (build the paths from <code>Path(__file__)</code> so it works from anywhere), "
   "parses and labels regions with your module, then prints exactly: a line <code>rows: N</code>, a line <code>missense: N</code>, and the mean missense score per region (rounded to 3 places). "
   "Run it from the terminal with <code>python src/report.py</code>. The check cell below runs it for you.",
   '"""Print a short report about the variant table."""\n# TODO: imports, paths from __file__, load, parse, label, print three things',
   'import subprocess, sys\nout = subprocess.run([sys.executable, str(ROOT / "src" / "report.py")], capture_output=True, text=True)\nassert out.returncode == 0, out.stderr\nassert "rows:" in out.stdout and "missense:" in out.stdout\nassert "phosphatase_domain" in out.stdout',
   'from pathlib import Path\n\nimport pandas as pd\n\nfrom vampseq_tools import label_regions, parse_hgvs\n\nROOT = Path(__file__).resolve().parent.parent\ndf = pd.read_csv(ROOT / "data" / "raw" / "pten-variant-abundance.csv")\nregions = pd.read_csv(ROOT / "data" / "raw" / "pten-region-annotations.csv")\ndf = label_regions(parse_hgvs(df), regions)\nmiss = df[df["record_type"] == "missense"]\n\nprint("rows:", len(df))\nprint("missense:", len(miss))\nprint(miss.groupby("region")["score"].mean().round(3).to_string())')


# ===================================================================== stage 0 (terminal)
ex(0, "e0a", "terminal drill",
   "Open your terminal and, using only the commands from the table, do this in order: (1) print where you are; (2) make a folder called <code>quest-drill</code>; (3) step into it; "
   "(4) make two folders inside it called <code>data</code> and <code>results</code>; (5) list what is there (you should see both); (6) step back out to where you started and print where you are. "
   "There is no check cell: the check is that <code>ls</code> showed <code>data</code> and <code>results</code> and that the last <code>pwd</code> matches the first.",
   'pwd\n# your commands here',
   None,
   'pwd\nmkdir quest-drill\ncd quest-drill\nmkdir data results\nls\ncd ..\npwd',
   lang="bash")

# ===================================================================== stage 12 (Project 0)
ex(12, "e12a", "gc_content from scratch",
   "Before using <code>gc_fraction</code>, write the idea yourself. Write <code>gc_content(seq)</code> that takes a string of DNA and returns the <strong>fraction</strong> of its letters that are <code>G</code> or <code>C</code>. "
   "Use a loop (or <code>str.count</code>), and add a docstring. Return <code>0</code> for an empty string instead of dividing by zero.",
   'def gc_content(seq):\n    pass   # TODO',
   'assert gc_content("GGCC") == 1.0\nassert gc_content("ATAT") == 0.0\nassert gc_content("ATGC") == 0.5\nassert gc_content("") == 0\nassert abs(gc_content("ATGACCGAATGGCTGTAATGCCGTAACGAT") - 14 / 30) < 1e-9',
   'def gc_content(seq):\n    """Fraction of letters in seq that are G or C."""\n    if len(seq) == 0:\n        return 0\n    gc = 0\n    for letter in seq.upper():\n        if letter in "GC":\n            gc += 1\n    return gc / len(seq)')

ex(12, "e12b", "records to a table, then a question",
   "Using the <code>records</code> list from this stage, make a DataFrame <code>seqs</code>, then a second DataFrame <code>rich</code> holding only the genes with GC fraction <strong>above 0.5</strong>, sorted from highest to lowest GC. "
   "Finally, in one sentence in a text cell, say which gene is the most GC-rich and why a very GC-rich sequence might be harder to work with in the lab.",
   'seqs = None\nrich = None   # TODO',
   'assert list(rich["id"]) == ["geneB", "geneD"]\nassert rich["gc"].is_monotonic_decreasing',
   'seqs = pd.DataFrame(records)\nrich = seqs[seqs["gc"] > 0.5].sort_values("gc", ascending=False)')

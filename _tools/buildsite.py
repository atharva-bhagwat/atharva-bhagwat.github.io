"""Build the multi-page guide. Run:  python site.py /path/to/repo"""
import json
import re
import sys
from pathlib import Path

import ex2
import stages_a
import stages_b
import stages_c
from qbuild import answer_hash, esc, puzzle, code, p, h3, ul, ol, table, callout, details

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content_hpc

ROOT_URL = "/articles/intro-to-python-biosci"
ENV = stages_c.ENV

STAGES = {}
STAGES.update(stages_a.STAGES)
STAGES.update(stages_b.STAGES)
STAGES.update(stages_c.STAGES)

PART1 = [12, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
PART2 = [0, 6, 13]
EXTRA = [15]
ORDER = PART1 + PART2 + EXTRA
DISPLAY = {key: i for i, key in enumerate(ORDER)}

SLUG = {12: "python-building-blocks", 1: "notebooks-text-loops", 2: "error-messages", 3: "pandas-tables", 4: "calculations-groups",
        5: "functions", 7: "checking-real-data", 8: "summarising-regions", 9: "plotting-distributions", 10: "more-plots",
        11: "checking-conclusion", 0: "computer-setup", 6: "organising-project", 13: "running-scripts", 15: "biopython-extra",
        "hpc": "hpc", "cert": "certificate", "plan": "plan", "faq": "faq"}
NAMES = {12: "Python building blocks", 1: "Notebooks, text and loops", 2: "Reading error messages", 3: "Tables with pandas",
         4: "Calculations and groups", 5: "Writing functions", 7: "Checking real data", 8: "Summarising by region",
         9: "Plotting distributions", 10: "More plots", 11: "Checking your conclusion", 0: "Setting up your computer",
         6: "Organising a project", 13: "Running a script", 15: "DNA sequences with Biopython", 14: "Warm-up"}
SUBS = {14: "reading code like English, in about 10 minutes", 12: "values, lists, dictionaries, libraries, tables", 1: "cells, kernel memory, text, loops",
        2: "what error messages mean and what to do", 3: "load a table, pick columns, filter rows", 4: "new columns, groups, pivots",
        5: "reuse code with a function", 7: "look at real data before trusting it", 8: "group, summarise, interpret",
        9: "histogram, box plot, violin, strip, count", 10: "scatter, line, heatmap", 11: "does the answer survive a different rule?",
        0: "terminal, Miniconda, environments, VS Code", 6: "folders, downloads, checksums, helper files", 13: "one command that rebuilds a result",
        15: "translate and read sequence files"}
# key -> (notebook key in _data/colab.yaml, track, minutes, number of stars)
META = {12: ("nb0", "core", 60, 2), 1: ("nb1", "core", 45, 2), 2: ("nberrors", "core", 30, 2), 3: ("nb2", "core", 40, 2),
        4: ("nb2", "core", 40, 2), 5: ("nb2", "core", 40, 2), 7: ("nb3", "core", 45, 3), 8: ("nb3", "core", 40, 3),
        9: ("nb4", "core", 40, 2), 10: ("nb4", "optional", 45, 2), 11: ("nb5", "core", 40, 3),
        0: (None, "levelup", 60, 2), 6: (None, "levelup", 45, 2), 13: (None, "levelup", 30, 0), 15: ("nbbio", "optional", 40, 0)}
NB_STAGES = {"nb0": "Stage 0", "nb1": "Stage 1", "nberrors": "Stage 2", "nb2": "Stages 3 to 5", "nb3": "Stages 6 and 7",
             "nb4": "Stages 8 and 9", "nb5": "Stage 10", "nbbio": "the Extra stage"}
BADGE = {"core": ("is-core", "Core"), "optional": ("is-optional", "Optional"), "levelup": ("is-optional", "Level up")}
TOTAL_STARS = sum(META[k][3] for k in ORDER) + 1
FLOW = ORDER[:14] + ["hpc"] + ORDER[14:] + ["cert"]
PART_LABEL = {**{k: "Part 1" for k in PART1}, **{k: "Part 2" for k in PART2}, 15: "Extra", "hpc": "Part 2", "cert": "Part 2"}


def url(key):
    return ROOT_URL if key == "start" else f"{ROOT_URL}/{SLUG[key]}"


def label_of(key):
    if key == "hpc":
        return "Taking your work to the HPC cluster"
    if key == "cert":
        return "Your certificate"
    return NAMES[key]


def page_title(key):
    if key in ("hpc", "cert"):
        return label_of(key)
    if key == 15:
        return "Extra: " + NAMES[15]
    return f"Stage {DISPLAY[key]}: {NAMES[key]}"


# -------------------------------------------------------------- shared pieces
def assets():
    return ('<link rel="stylesheet" href="/assets/css/quest.css">\n'
            '<script src="/assets/js/quest-answers.js" defer></script>\n'
            '<script src="/assets/js/quest.js" defer></script>\n')


def bar(quiet=False):
    return ('<div class="q-bar' + (' is-quiet' if quiet else '') + '">'
            '<span class="q-bar-stars"><span class="q-glyph" aria-hidden="true">&#9733;</span><span id="q-bar-count">0</span></span>'
            '<span class="q-bar-rank" id="q-bar-rank"></span>'
            f'<span class="q-bar-links"><a href="{url("plan")}">Plan</a><button type="button" class="q-reset">Reset stars</button></span></div>')


def credits():
    return ('<div class="q-credits"><p class="q-credit-line">Special thanks to '
            '<a href="https://github.com/itsjustnilay" target="_blank" rel="noopener">Nilay</a>!</p>'
            '<button type="button" class="q-reset">Reset all stars on this browser</button></div>')


def wrap(inner, extra_attrs="", quiet=False):
    return (f'<div class="quest" id="quest" data-total-stars="{TOTAL_STARS}" data-total-ex="0"{extra_attrs}>\n'
            + assets() + bar(quiet) + "\n" + inner + "\n" + credits() + "\n</div>\n")


def front(title, permalink, extra=""):
    return f'---\nlayout: guide\ntitle: "{title.replace(chr(34), chr(92) + chr(34))}"\npermalink: {permalink.lstrip("/")}\n{extra}---\n'


def finalize(fm, body):
    return fm + "{% raw %}\n" + body + "{% endraw %}\n"


def nav(key):
    i = FLOW.index(key)
    prev = FLOW[i - 1] if i > 0 else None
    nxt = FLOW[i + 1] if i + 1 < len(FLOW) else None

    def card(k, cls, word):
        return (f'<a class="q-nav-link {cls}" href="{url(k)}"><span class="q-nav-dir">{word}</span>'
                f'<span class="q-nav-name">{esc(label_of(k))}</span></a>')
    left = card(prev, "is-prev", "Back") if prev is not None else (
        f'<a class="q-nav-link is-prev" href="{url("plan")}"><span class="q-nav-dir">Back</span><span class="q-nav-name">The plan</span></a>')
    right = card(nxt, "is-next", "Next") if nxt is not None else (
        f'<a class="q-nav-link is-next" href="{url("plan")}"><span class="q-nav-dir">Finished</span><span class="q-nav-name">Back to the plan</span></a>')
    return f'<nav class="q-nav" aria-label="Previous and next">{left}{right}</nav>'


def crumbs(key):
    return (f'<nav class="q-crumbs" aria-label="Breadcrumb"><a href="{url("plan")}">Plan</a>'
            f'<span aria-hidden="true"> / </span><span>{PART_LABEL[key]}</span></nav>')


# ------------------------------------------------------------ stage pages
def stage_html(key):
    h = STAGES[key]
    nb, track, minutes, stars = META[key]
    cls, label = BADGE[track]
    num = "Extra" if key == 15 else f"Stage {DISPLAY[key]}"
    h = re.sub(r'<span class="q-stage-num">Stage \d+</span>', f'<span class="q-stage-num">{num}<span class="q-badge {cls}">{label}</span></span>', h, count=1)
    h = re.sub(r"<h2>.*?</h2>", "", h, count=1, flags=re.S)       # the page title already shows it
    if stars == 3:
        h = h.replace('<span class="q-s" data-part="2">&#9733;</span>', '<span class="q-s" data-part="2">&#9733;</span><span class="q-s" data-part="3">&#9733;</span>', 1)
    elif stars == 0:
        h = re.sub(r'<div class="q-stage-stars".*?</div>', "", h, count=1, flags=re.S)
    extra = ""
    if nb is not None:
        link = "https://colab.research.google.com/drive/{% endraw %}{{ site.data.colab." + nb + " }}{% raw %}"
        where = NB_STAGES[nb]
        section = ("It covers " + where + ", so scroll to the section with this stage's number." if nb in ("nb2", "nb3", "nb4")
                   else "It is all about this stage.")
        extra += ('<div class="q-practice"><h3>Now practise in Colab</h3>'
                  '<p>You have read the ideas. Next, try them. The notebook repeats the code above with a few blanks for you to fill in, then ends with small exercises. '
                  + section + ' Run the cells in order.</p>'
                  f'<p class="q-colab-row"><a class="q-colab" href="{link}" target="_blank" rel="noopener">Open the practice notebook</a>'
                  '<span class="q-colab-note">You need a free Google account. When it opens, choose File, then Save a copy in Drive, so your work is yours.</span></p></div>')
    exes = ex2.BY_STAGE.get(key, [])
    if exes:
        extra += ('<div class="q-practice"><h3>Exercises</h3><p>These are also in the notebook. Try each one yourself before you open the solution.</p>'
                  + "".join(ex2.page_html(e) for e in exes) + '</div>')
    marker = '<div class="q-puzzles">'
    if stars and marker in h:
        h = h.replace(marker, extra + '<h3 class="q-puzzle-title">Check your understanding</h3>' + marker, 1)
    else:
        h = h.replace('<div class="q-puzzles"></div>', extra)
    return h


# -------------------------------------------------------------- trail table
def trail_table():
    rows = []
    sections = [("Part 1: learn by running code (all in Colab, nothing to install)", [14] + PART1),
                ("Part 2: your own computer, then the cluster", PART2),
                ("Extra", EXTRA)]
    for label, keys in sections:
        rows.append(f'<tr class="q-df-part"><th colspan="5" scope="colgroup">{esc(label)}</th></tr>')
        for key in keys:
            if key == 14:
                stars, idx, link, badge, mins = 1, "start", url("start"), "", ""
            else:
                stars = META[key][3]
                idx = "extra" if key == 15 else DISPLAY[key]
                link = url(key)
                badge = f' <span class="q-badge {BADGE[META[key][1]][0]}">{BADGE[META[key][1]][1]}</span>'
                mins = f" &middot; about {META[key][2]} min"
            cells = []
            for part in (1, 2, 3):
                cells.append(f'<td data-cell="s{key}p{part}"><span class="q-nan">NaN</span></td>' if part <= stars else '<td class="q-df-none">&ndash;</td>')
            rows.append(f'<tr><th scope="row">{idx}</th><td class="q-df-name"><a href="{link}">{esc(NAMES[key])}</a>{badge}'
                        f'<span class="q-df-sub">{esc(SUBS[key])}{mins}</span></td>' + "".join(cells) + '</tr>')
    return ('<table class="q-df q-df-plan"><thead><tr><th></th><th class="q-df-name">stage</th><th>star1</th><th>star2</th><th>star3</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


# ------------------------------------------------------------------ pages
ENGLISH_PYTHON = '''# Say hello.
print("Hello")

# Remember that the age is 25.
age = 25

# If the age is more than 18, say "adult".
if age > 18:
    print("adult")'''


def start_page():
    q = puzzle("s14p1", 1, "<p>Back from the warm-up? Type the GC fraction you wrote down, rounded to 3 decimal places.</p>",
               kind="number", placeholder="e.g. 0.123", spec={"kind": "num", "value": 0.375, "dp": 3},
               hint="It is the number printed by the last cell, the one with <code>round(gc, 3)</code>. Run that cell again in the notebook if you need to.")
    q = q.replace('data-qid="s14p1" data-part="1"', 'data-qid="s14p1" data-part="1" data-done-msg="You did it. That was real code. Your plan is ready just below."')
    stage_urls = {str(k): url(k) for k in ORDER}
    body = (
        '<section class="q-start">'
        '<p class="q-start-lede">Learn to analyse biological data with Python.</p>'
        '<p class="q-start-text">You do not need any experience. We start with a short, friendly first exercise that runs in your browser. There is nothing to install.</p>'
        '<h3>Reading Python is like reading English</h3>'
        '<p>Code is a list of instructions the computer follows from top to bottom, like a recipe. Read each note (the line starting with <code>#</code>), then the code under it. They say the same thing.</p>'
        + code(ENGLISH_PYTHON, "python", "English in the notes, Python in the code")
        + '<p class="q-colab-row"><a class="q-colab q-colab-big" href="https://colab.research.google.com/drive/{% endraw %}{{ site.data.colab.warmup }}{% raw %}" target="_blank" rel="noopener">Start the 10-minute warm-up</a>'
        '<span class="q-colab-note">Opens in Google Colab. You need a free Google account. Once it opens, choose File, then Save a copy in Drive.</span></p>'
        '<div class="q-puzzles">' + q + '</div>'
        f'<div class="q-start-after" data-reveal-on="s14p1" hidden><a class="q-colab q-colab-big" href="{url("plan")}">See the plan</a>'
        '<span class="q-colab-note">Everything after this is optional. You choose what to do and when.</span></div>'
        '<div class="q-start-trail" data-show-when-stars="1" hidden><h3>Your progress</h3>'
        '<p class="q-start-text">Pick any stage to jump to it. Stars are saved in this browser.</p>'
        '<div class="q-nb"><div class="q-nb-row q-nb-out"><div class="q-nb-label">Out[1]:</div><div class="q-nb-body">' + trail_table() + '</div></div></div></div>'
        f'<p class="q-start-faq">Already know some Python? <a href="{url("faq")}">Where should I start?</a></p>'
        '</section>')
    attrs = f" data-hide-total=\"1\" data-hash-map='{json.dumps(stage_urls)}'"
    fm = ('---\nlayout: guide\ntitle: "Introduction to Bioinformatics Programming in Python"\n'
          'categories: articles\npermalink: articles/intro-to-python-biosci\nauthor: Atharva Bhagwat\n---\n')
    return finalize(fm, wrap(body, attrs, quiet=True))


PFB = ('<h3>A free book to read alongside</h3>'
       '<p><a href="https://www.pythonforbiologists.org" target="_blank" rel="noopener">Python for Biologists</a> is a free set of short episodes with videos, code and exercises that teach the basics of Python '
       'through genomics examples. It assumes no programming or genetics background. It is a good second source for anything in Part 1: when an idea here does not click, '
       'look for the same idea there, and code along.</p>')


def plan_page():
    body = ('<section class="q-plan">'
            '<p class="q-lede">Everything here is optional. Take what is useful, skip what is not, and go at your own pace. There are no deadlines, and the stars are just a way to see where you have been.</p>'
            f'<p class="q-lede">New to code? Start at the top and go down. Already know some Python? The <a href="{url("faq")}">FAQ</a> shows where to jump in.</p>'
            '<div class="q-nb" aria-label="Your progress, shown as a DataFrame">'
            '<div class="q-nb-row q-nb-in"><div class="q-nb-label">In [1]:</div><div class="q-nb-code">plan</div></div>'
            '<div class="q-nb-row q-nb-out"><div class="q-nb-label">Out[1]:</div><div class="q-nb-body">' + trail_table() + '</div></div>'
            '<div class="q-nb-row q-nb-in"><div class="q-nb-label">In [2]:</div><div class="q-nb-code">plan[["star1", "star2", "star3"]].notna().sum().sum()</div></div>'
            '<div class="q-nb-row q-nb-out"><div class="q-nb-label">Out[2]:</div><div class="q-nb-result" id="q-total">0</div></div></div>'
            '<h3>How the parts fit together</h3>'
            '<p><strong>Part 1</strong> runs entirely in Colab. Each stage has a short page to read, then a notebook to practise in, then a few questions. Stages marked <em>Core</em> are the main path; <em>Optional</em> ones go deeper.</p>'
            '<p><strong>Part 2</strong> is for when you want to work on your own computer: the terminal, Miniconda, VS Code, project folders, scripts, and finally the HPC cluster. You can skip it until you need it.</p>'
            + PFB +
            f'<p class="q-colab-row"><a class="q-colab" href="{url(PART1[0])}">Start with Stage 0</a></p></section>')
    return finalize(front("Your plan", url("plan")), wrap(body))


def route(key_or_start, text):
    return f'<a href="{url(key_or_start)}">{esc(text)}</a>'


FAQ = [
    ("Do I have to do everything?", "No. Nothing is required. The stars are only there so you can see where you have been, not to grade you. Take what helps and skip the rest."),
    ("I have never written code. Where do I start?", f'Start with the <a href="{url("start")}">warm-up</a> (about 10 minutes), then follow the plan from the top. Do one stage at a time. Each is small, and you can stop whenever you like.'),
    ("How long does it take?", "The warm-up takes about 10 minutes. Each stage after that is roughly 30 to 60 minutes, and there is no deadline. The Core stages add up to about 6 hours, spread over as many days as you like. Part 2 and the optional stages are extra."),
    ("I know a little Python. Where should I jump in?", "Every notebook sets itself up, so you can start at any stage. Pick the row that describes you:"),
    ("Do I need to install anything?", "Not for Part 1. Everything runs in Google Colab in your browser, and you only need a free Google account. Part 2 is where you set up Python on your own computer, and it is optional."),
    ("What are the stars? Are they saved?", "At the end of each stage you answer a few questions: run your code, type the answer, and a star lights up. A few ask you to explain in your own words what a result means. "
     "Your stars are saved in this web browser, on this computer only. Clearing your browser data or switching devices starts you from zero, but your notebooks stay safe in your own Google Drive."),
    ("Does Colab save my work?", "Only if you choose <strong>File, Save a copy in Drive</strong> when you open a notebook. Without that, your edits are lost when the session ends. Files you create inside a session also disappear when it ends."),
    ("I am stuck. What do I do?", f'Read the last line of the error message first: it usually says what is wrong. <a href="{url(2)}">Reading error messages</a> shows how. Every exercise has a solution you can open after trying, and every question has a nudge.'),
    ("Do I need to know biology?", f'No. Each word is explained when it first appears, and <a href="{url(7)}">Checking real data</a> gives a short background on the dataset.'),
    ("Where can I learn more Python?", 'The free <a href="https://www.pythonforbiologists.org" target="_blank" rel="noopener">Python for Biologists</a> episodes (videos, code and exercises, no programming background needed) are a good companion. The official documentation of each library is the best place to look things up.'),
    ("Can I use my own computer instead of Colab?", f'Yes. Download a notebook from Colab (File, Download, .ipynb) and open it in VS Code or Jupyter. <a href="{url(0)}">Setting up your computer</a> shows how.'),
    ("How do I reset my stars?", "Use the Reset stars link at the top of any page. It clears everything stored in this browser."),
]
ROUTES = [("You have never coded", "start", "Warm-up, then Stage 0"),
          ("You know variables, loops and a bit of Python, but not pandas", 3, "Tables with pandas"),
          ("You know basic pandas and want real data", 7, "Checking real data"),
          ("You only want plotting", 9, "Plotting distributions"),
          ("You want to practise writing conclusions from data", 11, "Checking your conclusion"),
          ("You want to set up your own computer", 0, "Setting up your computer"),
          ("You want to run things on the cluster", "hpc", "the HPC page")]


def faq_page():
    items = []
    for q, a in FAQ:
        extra = ""
        if q.startswith("I know a little Python"):
            rows = "".join(f'<tr><td>{esc(w)}</td><td><a href="{url(k)}">{esc(n)}</a></td></tr>' for w, k, n in ROUTES)
            extra = ('<div class="q-table-wrap"><table class="q-table"><thead><tr><th>If...</th><th>Start at</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
                     '<p>If a stage feels too hard, go back one. If it feels too easy, skip ahead.</p>')
        items.append(f'<details class="q-faq" open><summary>{esc(q)}</summary><p>{a}</p>{extra}</details>')
    body = ('<section class="q-plan"><p class="q-lede">Short answers to the questions people ask first.</p>' + "".join(items)
            + f'<p class="q-colab-row"><a class="q-colab" href="{url("plan")}">Back to the plan</a></p></section>')
    return finalize(front("Questions and answers", url("faq")), wrap(body))


def stage_page(key):
    body = crumbs(key) + stage_html(key) + nav(key)
    return finalize(front(page_title(key), url(key)), wrap(body))


def hpc_html():
    h = content_hpc.HPC
    h = re.sub(r"<h2>.*?</h2>", "", h, count=1, flags=re.S)
    h = h.replace('<span class="q-stage-num">After the summit</span>', '<span class="q-stage-num">Part 2<span class="q-badge is-optional">Level up</span></span>')
    return h


def hpc_page():
    return finalize(front(label_of("hpc"), url("hpc")), wrap(crumbs("hpc") + hpc_html() + nav("hpc")))


def certificate():
    return ('<section class="q-cert-wrap" id="q-cert-wrap" hidden>'
            '<p class="q-promise">You reached the top. Enter your name, then print it or save it as a PDF.</p>'
            '<div class="q-cert-controls"><input id="q-cert-input" type="text" placeholder="Your name" autocomplete="name" aria-label="Your name">'
            '<button type="button" class="q-check" id="q-cert-print">Print certificate</button></div>'
            '<div class="q-cert"><p>This certifies that</p><p class="q-cert-name" id="q-cert-name">Your name here</p>'
            '<p>completed <strong>Introduction to Bioinformatics Programming in Python</strong>: learned the basics of Python, worked with tables, '
            'checked a real dataset and plotted it.</p>'
            '<p class="q-cert-stars" id="q-cert-stars" aria-hidden="true"></p><p class="q-cert-rank" id="q-cert-rank"></p>'
            '<p><small>atharvabhagwat.dev</small></p></div></section>')


def cert_page():
    locked = ('<p class="q-promise" id="q-cert-locked">The certificate opens when you earn the first star of Checking your conclusion. '
              f'<a href="{url(11)}">Go there</a>.</p>')
    return finalize(front(label_of("cert"), url("cert")), wrap(crumbs("cert") + locked + certificate() + nav("cert")))


def write_all(site):
    site = Path(site)
    data_dir = site / "assets" / "data"
    if not (data_dir / "toy_vampseq_bin_counts.csv").exists():
        raise SystemExit("Need assets/data/toy_vampseq_bin_counts.csv in the repo to compute expected exercise output.")
    ex2.LOCAL_BASE = str(data_dir) + "/"
    (site / "guide").mkdir(exist_ok=True)
    (site / "_posts" / "articles").mkdir(parents=True, exist_ok=True)
    files = {site / "_posts" / "articles" / "2026-11-04-introduction-to-bioinformatics-programming-in-python.md": start_page(),
             site / "guide" / "plan.md": plan_page(), site / "guide" / "faq.md": faq_page(),
             site / "guide" / "hpc.md": hpc_page(), site / "guide" / "certificate.md": cert_page()}
    for key in ORDER:
        files[site / "guide" / f"{SLUG[key]}.md"] = stage_page(key)
    for path, text in files.items():
        path.write_text(text, encoding="utf-8")
    return files


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    fs = write_all(out)
    print("wrote", len(fs), "files")

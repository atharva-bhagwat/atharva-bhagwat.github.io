"""Multi-page version of the guide: start page, plan, FAQ, one page per stage."""
import json
import re
from pathlib import Path

import build as B
from qbuild import answer_hash, esc, puzzle

ROOT_URL = "/articles/intro-to-python-biosci"

SLUG = {
    12: "project-0", 1: "notebook-ridge", 2: "traceback-gorge", 3: "table-flats", 4: "score-falls",
    5: "function-forge", 7: "audit-pass", 8: "region-rapids", 9: "histogram-meadow", 10: "heatmap-heights",
    11: "the-summit", 0: "basecamp", 6: "project-lodge", 13: "ship-it",
    "hpc": "hpc", "cert": "certificate", "plan": "plan", "faq": "faq",
}
SUBS = {
    14: "10 minutes, no experience needed", 12: "values, lists, tables, a taste of Biopython", 1: "cells, kernels, strings, loops",
    2: "reading error messages", 3: "your first DataFrame", 4: "new columns, groups, pivots", 5: "write it once, reuse it",
    7: "look at real data, carefully", 8: "group, merge, summarise", 9: "plots for distributions", 10: "heatmaps and patterns",
    11: "does your conclusion survive?", 0: "terminal, Miniconda, VS Code", 6: "project folders and downloads", 13: "from notebook to script",
}
NAMES = dict(B.STAGE_NAMES)
NAMES[14] = "Warm-up"
TOTAL_STARS = sum(B.META[k][3] for k in B.ORDER) + 1   # +1 for the warm-up star
TOTAL_EX = len(B.content_ex.EXERCISES)

START_KEY = 14
FLOW = list(B.ORDER) + ["hpc", "cert"]
PART_OF = {k: ("Part 1" if k in B.PART1 else "Part 2") for k in B.ORDER}
PART_OF["hpc"] = "Part 2"
PART_OF["cert"] = "Part 2"


def url(key):
    if key == "start":
        return ROOT_URL
    return f"{ROOT_URL}/{SLUG[key]}"


def title_of(key):
    if key == "hpc":
        return "Taking your work to the HPC cluster"
    if key == "cert":
        return "Summit register"
    h = BY_KEY_HTML[key]
    return re.search(r"<h2>(.*?)</h2>", h, re.S).group(1)


BY_KEY_HTML = {k: B.finish_stage(k) for k in B.ORDER}


# ----------------------------------------------------------------- pieces
def assets():
    return ('<link rel="stylesheet" href="/assets/css/quest.css">\n'
            '<script src="/assets/js/quest-answers.js" defer></script>\n'
            '<script src="/assets/js/quest.js" defer></script>\n')


def bar(quiet=False):
    return (
        '<div class="q-bar' + (' is-quiet' if quiet else '') + '">'
        '<span class="q-bar-stars"><span class="q-glyph" aria-hidden="true">&#9733;</span><span id="q-bar-count">0</span></span>'
        '<span class="q-bar-rank" id="q-bar-rank"></span>'
        '<span class="q-bar-ex" id="q-bar-ex" title="Practice exercises ticked as done"></span>'
        f'<span class="q-bar-links"><a href="{url("plan")}">Plan</a><button type="button" class="q-reset">Reset stars</button></span>'
        '</div>'
    )


def credits_block():
    return B.credits()


def wrap(inner, extra_attrs="", quiet=False):
    return (
        f'<div class="quest" id="quest" data-total-stars="{TOTAL_STARS}" data-total-ex="{TOTAL_EX}"{extra_attrs}>\n'
        + assets() + bar(quiet) + "\n" + inner + "\n" + credits_block() + "\n</div>\n"
    )


def front(title, permalink, extra=""):
    t = title.replace('"', '\\"')
    return f'---\nlayout: guide\ntitle: "{t}"\npermalink: {permalink.lstrip("/")}\n{extra}---\n'


def finalize(front_matter, body):
    return front_matter + "{% raw %}\n" + B.renumber(body) + "{% endraw %}\n"


def nav(key):
    i = FLOW.index(key)
    prev = FLOW[i - 1] if i > 0 else None
    nxt = FLOW[i + 1] if i + 1 < len(FLOW) else None
    left = (f'<a class="q-nav-link is-prev" href="{url(prev)}"><span class="q-nav-dir">Back</span><span class="q-nav-name">{esc(NAMES.get(prev, title_of(prev)) if prev not in ("hpc", "cert") else title_of(prev))}</span></a>'
            if prev is not None else
            f'<a class="q-nav-link is-prev" href="{url("plan")}"><span class="q-nav-dir">Back</span><span class="q-nav-name">The plan</span></a>')
    if nxt is not None:
        nm = NAMES.get(nxt) if nxt not in ("hpc", "cert") else title_of(nxt)
        right = f'<a class="q-nav-link is-next" href="{url(nxt)}"><span class="q-nav-dir">Next</span><span class="q-nav-name">{esc(nm)}</span></a>'
    else:
        right = f'<a class="q-nav-link is-next" href="{url("plan")}"><span class="q-nav-dir">Finished</span><span class="q-nav-name">Back to the plan</span></a>'
    return f'<nav class="q-nav" aria-label="Previous and next">{left}{right}</nav>'


def crumbs(key):
    return (f'<nav class="q-crumbs" aria-label="Breadcrumb"><a href="{url("plan")}">Plan</a>'
            f'<span aria-hidden="true"> / </span><span>{PART_OF[key]}</span></nav>')


# ------------------------------------------------------------- trail table
def trail_table():
    rows = []
    sections = [("Part 1: learn by running code (all in Colab, nothing to install)", [14] + B.PART1),
                ("Part 2: your own computer, then the cluster", B.PART2)]
    for label, keys in sections:
        rows.append(f'<tr class="q-df-part"><th colspan="5" scope="colgroup">{esc(label)}</th></tr>')
        for key in keys:
            if key == 14:
                stars, idx, link = 1, "start", url("start")
                track = ""
            else:
                stars = B.META[key][3]
                idx = B.DISPLAY[key]
                link = url(key)
                track = B.BADGE[B.META[key][1]][1]
            mins = "" if key == 14 else f" &middot; about {B.META[key][2]} min"
            sub = f'<span class="q-df-sub">{esc(SUBS[key])}{mins}</span>'
            badge = (f' <span class="q-badge {B.BADGE[B.META[key][1]][0]}">{track}</span>' if key != 14 else "")
            cells = []
            for part in (1, 2, 3):
                if part <= stars:
                    cells.append(f'<td data-cell="s{key}p{part}"><span class="q-nan">NaN</span></td>')
                else:
                    cells.append('<td class="q-df-none">&ndash;</td>')
            rows.append(f'<tr><th scope="row">{idx}</th><td class="q-df-name"><a href="{link}">{esc(NAMES[key])}</a>{badge}{sub}</td>' + "".join(cells) + '</tr>')
    return ('<table class="q-df q-df-plan"><thead><tr><th></th><th class="q-df-name">stage</th><th>star1</th><th>star2</th><th>star3</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


# ------------------------------------------------------------------ pages
def start_page():
    q = puzzle("s14p1", 1,
               '<p>Back from the warm-up? Type the GC fraction you wrote down, rounded to 3 decimal places.</p>',
               kind="number", placeholder="e.g. 0.123", spec={"kind": "num", "value": 0.375, "dp": 3},
               hint="It is the number printed by the cell that says <code>round(gc, 3)</code>. Run that cell again in the notebook if you need to.")
    q = q.replace('data-qid="s14p1" data-part="1"', 'data-qid="s14p1" data-part="1" data-done-msg="You did it. That was real code. Your plan is ready just below."')
    stage_urls = {str(k): url(k) for k in B.ORDER}
    body = (
        '<section class="q-start">'
        '<p class="q-start-lede">Learn to analyse biological data with Python.</p>'
        '<p class="q-start-text">You do not need any experience. We start with a short, friendly first exercise that runs in your browser. There is nothing to install.</p>'
        '<p class="q-colab-row"><a class="q-colab q-colab-big" href="https://colab.research.google.com/drive/{% endraw %}{{ site.data.colab.warmup }}{% raw %}" target="_blank" rel="noopener">Start the 10-minute warm-up</a>'
        '<span class="q-colab-note">Opens in Google Colab. You need a free Google account. Once it opens, choose File, then Save a copy in Drive.</span></p>'
        '<div class="q-puzzles">' + q + '</div>'
        f'<div class="q-start-after" data-reveal-on="s14p1" hidden><a class="q-colab q-colab-big" href="{url("plan")}">See the plan</a>'
        '<span class="q-colab-note">Everything after this is optional. You choose what to do and when.</span></div>'
        '<div class="q-start-trail" data-show-when-stars="1" hidden>'
        '<h3>Your progress</h3>'
        '<p class="q-start-text">Pick any stage to jump to it. Stars are saved in this browser.</p>'
        '<div class="q-nb"><div class="q-nb-row q-nb-out"><div class="q-nb-label">Out[1]:</div><div class="q-nb-body">' + trail_table() + '</div></div></div>'
        '</div>'
        f'<p class="q-start-faq">Already know some Python? <a href="{url("faq")}">Where should I start?</a></p>'
        '</section>'
    )
    attrs = f" data-hide-total=\"1\" data-hash-map='{json.dumps(stage_urls)}'"
    fm = ('---\nlayout: guide\ntitle: "Introduction to Bioinformatics Programming in Python"\n'
          'categories: articles\npermalink: articles/intro-to-python-biosci\nauthor: Atharva Bhagwat\n---\n')
    return fm + "{% raw %}\n" + B.renumber(wrap(body, attrs, quiet=True)) + "{% endraw %}\n"


def plan_page():
    body = (
        '<section class="q-plan">'
        '<p class="q-lede">Everything here is optional. Take what is useful, skip what is not, and go at your own pace. '
        'There are no deadlines, and the stars are just a way to see where you have been.</p>'
        f'<p class="q-lede">New to code? Start at the top and go down. Already know some Python? The <a href="{url("faq")}">FAQ</a> shows where to jump in.</p>'
        '<div class="q-nb" aria-label="Your progress, shown as a DataFrame">'
        '<div class="q-nb-row q-nb-in"><div class="q-nb-label">In [1]:</div><div class="q-nb-code">plan</div></div>'
        '<div class="q-nb-row q-nb-out"><div class="q-nb-label">Out[1]:</div><div class="q-nb-body">' + trail_table() + '</div></div>'
        '<div class="q-nb-row q-nb-in"><div class="q-nb-label">In [2]:</div><div class="q-nb-code">plan[["star1", "star2", "star3"]].notna().sum().sum()</div></div>'
        '<div class="q-nb-row q-nb-out"><div class="q-nb-label">Out[2]:</div><div class="q-nb-result" id="q-total">0</div></div>'
        '</div>'
        '<h3>How the parts fit together</h3>'
        '<p><strong>Part 1</strong> runs entirely in Colab. You press a button, run cells, fill in blanks, and write small pieces of code. '
        'Stages marked <em>Core</em> are the main path; <em>Optional</em> ones go deeper.</p>'
        '<p><strong>Part 2</strong> is for when you want to run things on your own computer: the terminal, Miniconda, VS Code, project folders, scripts, and finally the HPC cluster. '
        'You can skip it until you need it.</p>'
        f'<p class="q-colab-row"><a class="q-colab" href="{url(B.PART1[0])}">Start with Project 0</a></p>'
        '</section>'
    )
    return finalize(front("Your plan", url("plan")), wrap(body))


FAQ_ITEMS = [
    ("Do I have to do everything?",
     "No. Nothing is required. The stars exist so you can see where you have been, not to grade you. Take the stages that help you and skip the rest."),
    ("I have never written code. Where do I start?",
     f'Start with the <a href="{url("start")}">warm-up</a> (about 10 minutes), then follow the plan from the top: Project 0, Notebook Ridge, Traceback Gorge, and so on. '
     "Do one stage at a time. Each is small, and you can stop whenever you like."),
    ("How long does it take?",
     "The warm-up takes about 10 minutes. Each stage after that is roughly 30 to 60 minutes, and there is no deadline. The stages marked Core add up to about 7 hours, spread over as many days as you like. "
     "Part 2 and the optional stages are extra."),
    ("I know a little Python. Where should I jump in?",
     "Every notebook sets itself up, so you can start at any stage. Pick the row that describes you:"),
    ("Do I need to install anything?",
     "Not for Part 1. Everything runs in Google Colab in your browser, and you need only a free Google account. Part 2 is where you set up Python on your own computer, and it is optional."),
    ("What are the stars? Are they saved?",
     "Each stage ends with a puzzle: run your code, type the answer you get, and a star lights up. A few ask you to explain what a result means in your own words. "
     "Your stars are saved in this web browser only, on this computer. Clearing your browser data or switching devices starts you from zero, but your notebooks are safe in your own Google Drive."),
    ("Does Colab save my work?",
     "Only if you choose <strong>File, Save a copy in Drive</strong> when you open a notebook. Without that, your edits are lost when the session ends. Files you create inside a session also disappear when it ends."),
    ("I am stuck. What do I do?",
     f'Read the last line of the error message first: it usually says what is wrong. <a href="{url(2)}">Traceback Gorge</a> shows how. '
     "Every exercise has a hidden solution you can open when you have tried for a while, and every puzzle has a nudge."),
    ("Do I need to know biology?",
     f'No. Each column and word is explained when it first appears, and <a href="{url(7)}">Audit Pass</a> gives a short background on the dataset.'),
    ("Can I use my own computer instead of Colab?",
     f'Yes. Download a notebook from Colab (File, Download, .ipynb) and open it in VS Code or Jupyter. <a href="{url(0)}">Basecamp</a> shows how to set that up.'),
    ("How do I reset my stars?",
     "Use the Reset stars link at the top of any page. It clears everything on this browser."),
]

ROUTES = [
    ("You have never coded", "start", "Warm-up, then Project 0"),
    ("You know variables, loops and a bit of Python, but not pandas", 3, "Table Flats"),
    ("You know basic pandas and want real data", 7, "Audit Pass"),
    ("You only want plotting", 9, "Histogram Meadow"),
    ("You want to practise writing conclusions from data", 11, "The Summit"),
    ("You want to set up your own computer", 0, "Basecamp"),
    ("You want to run things on the cluster", "hpc", "the HPC page"),
]


def faq_page():
    items = []
    for q, a in FAQ_ITEMS:
        extra = ""
        if q.startswith("I know a little Python"):
            rows = []
            for who, key, nm in ROUTES:
                rows.append(f'<tr><td>{esc(who)}</td><td><a href="{url(key)}">{esc(nm)}</a></td></tr>')
            extra = ('<div class="q-table-wrap"><table class="q-table"><thead><tr><th>If...</th><th>Start at</th></tr></thead><tbody>'
                     + "".join(rows) + '</tbody></table></div>'
                     '<p>If a stage feels too hard, go back one. If it feels too easy, skip ahead.</p>')
        items.append(f'<details class="q-faq" open><summary>{esc(q)}</summary><p>{a}</p>{extra}</details>')
    body = ('<section class="q-plan"><p class="q-lede">Short answers to the questions people ask first.</p>'
            + "".join(items) +
            f'<p class="q-colab-row"><a class="q-colab" href="{url("plan")}">Back to the plan</a></p></section>')
    return finalize(front("Questions and answers", url("faq")), wrap(body))


def strip_h2(html_):
    return re.sub(r"<h2>.*?</h2>", "", html_, count=1, flags=re.S)


def stage_page(key):
    h = strip_h2(BY_KEY_HTML[key])
    body = crumbs(key) + h + nav(key)
    return finalize(front(title_of(key), url(key)), wrap(body))


def hpc_page():
    h = strip_h2(B.content_hpc.HPC).replace('<span class="q-stage-num">After the summit</span>', '<span class="q-stage-num">Part 2<span class="q-badge is-optional">Level up</span></span>')
    return finalize(front(title_of("hpc"), url("hpc")), wrap(crumbs("hpc") + h + nav("hpc")))


def cert_page():
    c = B.certificate().replace("<h2>Summit register</h2>", "")
    locked = ('<p class="q-promise" id="q-cert-locked">The register opens when you earn the first star of The Summit. '
              f'<a href="{url(11)}">Go to The Summit</a>.</p>')
    body = crumbs("cert") + locked + c + nav("cert")
    return finalize(front(title_of("cert"), url("cert")), wrap(body))


def write_all(site):
    site = Path(site)
    (site / "guide").mkdir(exist_ok=True)
    (site / "_posts" / "articles").mkdir(parents=True, exist_ok=True)
    files = {
        site / "_posts" / "articles" / "2026-11-04-introduction-to-bioinformatics-programming-in-python.md": start_page(),
        site / "guide" / "plan.md": plan_page(),
        site / "guide" / "faq.md": faq_page(),
        site / "guide" / "hpc.md": hpc_page(),
        site / "guide" / "certificate.md": cert_page(),
    }
    for key in B.ORDER:
        files[site / "guide" / f"{SLUG[key]}.md"] = stage_page(key)
    for p, text in files.items():
        p.write_text(text, encoding="utf-8")
    return files
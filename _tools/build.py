"""Assemble the Introduction to Bioinformatics Programming in Python article, its answers file and print a summary."""
import json
import re
from pathlib import Path

import qbuild
from qbuild import answer_hash, esc
import content_a
import content_b
import content_hpc
import content_ex
import content_p0

import sys
SITE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
ALL = content_a.STAGES_A + content_b.STAGES_B + content_p0.STAGES_P0


def with_exercises(stage_html):
    n = int(re.search(r'data-stage="(\d+)"', stage_html).group(1))
    items = content_ex.BY_STAGE.get(n)
    if not items:
        return stage_html
    block = '<div class="q-practice">' + content_ex.INTRO + "".join(items) + "</div>"
    marker = '<div class="q-puzzles">'
    assert stage_html.count(marker) == 1
    return stage_html.replace(marker, block + marker)


BY_KEY = {int(re.search(r'data-stage="(\d+)"', h).group(1)): with_exercises(h) for h in ALL}

# Order of the guide. Keys are the internal stage ids (they never change, so saved progress and answers stay valid).
PART1 = [12, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
PART2 = [0, 6, 13]
ORDER = PART1 + PART2
DISPLAY = {key: i for i, key in enumerate(ORDER)}

COLAB_TOKENS = {0: "COLAB_NB0_ID", 1: "COLAB_NB1_ID", 2: "COLAB_NB2_ID", 3: "COLAB_NB3_ID", 4: "COLAB_NB4_ID", 5: "COLAB_NB5_ID"}
# stage key -> (colab token key, track, minutes, number of stars)
META = {
    12: (0, "core", 60, 2), 1: (1, "core", 40, 2), 2: (1, "core", 30, 2), 3: (2, "core", 40, 2),
    4: (2, "core", 45, 2), 5: (2, "core", 40, 2), 7: (3, "core", 45, 3), 8: (3, "core", 40, 3),
    9: (4, "core", 45, 2), 10: (4, "optional", 60, 2), 11: (5, "core", 40, 3),
    0: (None, "levelup", 60, 2), 6: (None, "levelup", 50, 2), 13: (None, "levelup", 40, 0),
}
COLAB_TEXT = {
    0: "Notebook 0: Project 0", 1: "Notebook 1: Python, kernels and errors", 2: "Notebook 2: pandas and functions",
    3: "Notebook 3: the PTEN data", 4: "Notebook 4: plots", 5: "Notebook 5: sensitivity and conclusions",
}
BADGE = {"core": ("is-core", "Core"), "optional": ("is-optional", "Optional"), "levelup": ("is-optional", "Level up")}


def finish_stage(key):
    h = BY_KEY[key]
    nb, track, minutes, stars = META[key]
    cls, label = BADGE[track]
    h = re.sub(r'<span class="q-time">About \d+ minutes\.</span>', f'<span class="q-time">About {minutes} minutes.</span>', h)
    h = h.replace('<span class="q-stage-num">Stage ' + str(key) + '</span>',
                  '<span class="q-stage-num">Stage ' + str(key) + f'<span class="q-badge {cls}">{label}</span></span>', 1)
    if stars == 3:
        h = h.replace('<span class="q-s" data-part="2">&#9733;</span>', '<span class="q-s" data-part="2">&#9733;</span><span class="q-s" data-part="3">&#9733;</span>', 1)
    elif stars == 0:
        h = re.sub(r'<div class="q-stage-stars".*?</div>', '', h, count=1, flags=re.S)
    if nb is not None:
        url = "https://colab.research.google.com/drive/" + COLAB_TOKENS[nb]
        row = (f'<p class="q-colab-row"><a class="q-colab" href="{url}" target="_blank" rel="noopener">Open in Colab: {COLAB_TEXT[nb]}</a>'
               f'<span class="q-colab-note">Free Google account needed. Use File, Save a copy in Drive.</span></p>')
        h = h.replace('<div class="q-prose">', row + '<div class="q-prose">', 1)
    return h


def renumber(html):
    """Prose says 'Stage 7' using internal ids. Show the display numbers instead."""
    return re.sub(r"Stage (\d+)", lambda m: "Stage " + str(DISPLAY.get(int(m.group(1)), int(m.group(1)))), html)


def part_header(kicker, title, text):
    return f'<div class="q-part"><span class="q-part-kicker">{kicker}</span><h2>{title}</h2><p>{text}</p></div>'


N_EXERCISES = len(content_ex.EXERCISES)



# ------------------------------------------------------------------ hero
STAGE_NAMES = {
    12: "Project 0", 1: "Notebook Ridge", 2: "Traceback Gorge", 3: "Table Flats", 4: "Score Falls", 5: "Function Forge",
    7: "Audit Pass", 8: "Region Rapids", 9: "Histogram Meadow", 10: "Heatmap Heights", 11: "The Summit",
    0: "Basecamp", 6: "Project Lodge", 13: "Ship It",
}


def hero():
    rows = []
    for key in ORDER:
        stars = META[key][3]
        cells = []
        for part in (1, 2, 3):
            if part <= stars:
                cells.append(f'<td data-cell="s{key}p{part}"><span class="q-nan">NaN</span></td>')
            else:
                cells.append('<td class="q-df-none">&ndash;</td>')
        rows.append(
            f'<tr><th scope="row">{DISPLAY[key]}</th>'
            f'<td class="q-df-name"><a href="#stage-{key}">{esc(STAGE_NAMES[key])}</a></td>' + "".join(cells) + '</tr>'
        )
    table = (
        '<table class="q-df"><thead><tr><th></th><th class="q-df-name">stage</th><th>star1</th><th>star2</th><th>star3</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
    )
    return (
        '<div class="q-bar">'
        '<span class="q-bar-stars"><span class="q-glyph" aria-hidden="true">&#9733;</span><span id="q-bar-count">0 / 0</span></span>'
        '<span class="q-bar-rank" id="q-bar-rank">Trailhead</span>'
        '<span class="q-bar-ex" id="q-bar-ex" title="Practice exercises ticked as done"></span>'
        '<span class="q-bar-links"><a href="#trail">Trail</a><button type="button" class="q-reset">Reset stars</button></span>'
        '</div>'
        '<section class="q-hero" id="trail">'
        '<p class="q-lede">You will learn to analyse real data with Python. Start in your browser: press a button, run code, and see results straight away. '
        'Along the way you will build intuition for how data, code and biology fit together, and only then set up your own computer and learn the habits that make analyses reliable. '
        'No coding, no terminal and no biology background assumed.</p>'
        '<ul class="q-tracks">'
        '<li><strong>Part 1: Core track, about 7 hours, in Colab</strong>Nothing to install. Project 0, notebooks and kernels, debugging, pandas, functions, a real dataset, plots, and a written conclusion.</li>'
        '<li><strong>Part 2 and extras, about 5 more hours</strong>Your own computer: terminal, Miniconda, VS Code, project folders, scripts, then HPC. Plus stages and exercises marked Optional or Stretch.</li>'
        '</ul>'
        '<ul class="q-rules">'
        '<li><strong>Run it yourself.</strong>Every stage has hands-on practice where you write code, and ends with a puzzle. Type the answer you get to earn a star.</li>'
        '<li><strong>Think, not just calculate.</strong>Some stars ask you to interpret results or write a short conclusion, because that is the real skill.</li>'
        '<li><strong>Nothing leaves your browser.</strong>Progress is saved in this browser only. Nothing is uploaded and there is no account.</li>'
        '</ul>'
        '<div class="q-nb" aria-label="Your progress, shown as a DataFrame">'
        '<div class="q-nb-row q-nb-in"><div class="q-nb-label">In [1]:</div><div class="q-nb-code">trail</div></div>'
        '<div class="q-nb-row q-nb-out"><div class="q-nb-label">Out[1]:</div><div class="q-nb-body">' + table + '</div></div>'
        '<div class="q-nb-row q-nb-in"><div class="q-nb-label">In [2]:</div><div class="q-nb-code">trail[["star1", "star2", "star3"]].notna().sum().sum()</div></div>'
        '<div class="q-nb-row q-nb-out"><div class="q-nb-label">Out[2]:</div><div class="q-nb-result" id="q-total">0</div></div>'
        '</div>'
        '</section>'
    )


def certificate():
    return (
        '<section class="q-cert-wrap" id="q-cert-wrap" hidden>'
        '<h2>Summit register</h2>'
        '<p class="q-promise">You reached the top. Sign the register: enter your name, then print it or save it as a PDF.</p>'
        '<div class="q-cert-controls">'
        '<input id="q-cert-input" type="text" placeholder="Your name" autocomplete="name" aria-label="Your name">'
        '<button type="button" class="q-check" id="q-cert-print">Print certificate</button>'
        '</div>'
        '<div class="q-cert">'
        '<p>This certifies that</p>'
        '<p class="q-cert-name" id="q-cert-name">Your name here</p>'
        '<p>completed <strong>Introduction to Bioinformatics Programming in Python</strong>: set up a Python environment, learned pandas, wrote reusable functions, audited a real dataset and plotted it more than a dozen ways.</p>'
        '<p class="q-cert-stars" id="q-cert-stars" aria-hidden="true"></p>'
        '<p class="q-cert-rank" id="q-cert-rank"></p>'
        '<p><small>atharvabhagwat.dev</small></p>'
        '</div>'
        '</section>'
    )


def credits():
    return (
        '<div class="q-credits">'
        '<p class="q-credit-line">With <span class="q-heart" role="img" aria-label="love">&#x2764;&#xFE0F;</span> from '
        '<a href="https://atharvabhagwat.dev" target="_blank" rel="noopener">Atharva</a> &middot; Made with '
        '<a href="https://claude.ai" target="_blank" rel="noopener">Claude</a> &middot; Humanized by '
        '<a href="https://github.com/itsjustnilay" target="_blank" rel="noopener">Nilay</a>.</p>'
        '<button type="button" class="q-reset">Reset all stars on this browser</button>'
        '</div>'
    )


# --------------------------------------------------------------- answers
def static_answers():
    """Answers that never change. Integers and text are stored as hashes."""
    H = answer_hash
    a = {
        "s1p1": {"kind": "int", "h": H("s1p1", "252")},
        "s1p2": {"kind": "text", "h": H("s1p2", "1,2,5")},
        "s2p1": {"kind": "choices", "hs": [H(f"s2p1-{i}", c) for i, c in enumerate("bbca")]},
        "s2p2": {"kind": "num", "value": 2.718, "dp": 3},
        "s3p1": {"kind": "int", "h": H("s3p1", "7")},
        "s3p2": {"kind": "int", "h": H("s3p2", "10400")},
        "s4p1": {"kind": "num", "value": 3.490026, "dp": 2},
        "s4p2": {"kind": "text", "h": H("s4p2", "p.Ala58Val")},
        "s5p1": {"kind": "num", "value": 3.347902, "dp": 3},
        "s5p2": {"kind": "num", "value": 2.694628, "dp": 3},
    }
    return a


ANSWERS_TEMPLATE = r"""/* Answers for Introduction to Bioinformatics Programming in Python.
   - Toy-table answers are fixed (integers and text stored as short hashes).
   - Real-table answers live in REAL below. Generate them once with make_answer_key.py
     (pandas-quest-source/), which rewrites the block between the two markers.
   - To change a puzzle, edit its entry; quest.js does not need to change. */
(function () {
  "use strict";

  /*REAL_KEY_START*/
  var REAL = {};
  /*REAL_KEY_END*/

  function real(kind, key, dp) { var v = REAL[key]; return { kind: kind, value: v, dp: dp, missing: v === undefined }; }

  /* ------------ paste checks ------------ */
  function pasteSetup(text) {
    var need = [
      [/python\s+3\.\d+/i, "a line like  python     3.12.x"],
      [/pandas\s+\d+\.\d+/i, "a line like  pandas     x.y.z"],
      [/matplotlib\s+\d+\.\d+/i, "a line like  matplotlib x.y.z"],
      [/seaborn\s+\d+\.\d+/i, "a line like  seaborn    x.y.z"]
    ];
    for (var i = 0; i < need.length; i++) if (!need[i][0].test(text)) return { ok: false, msg: "Missing " + need[i][1] + ". Paste the whole output of check_setup.py." };
    if (!/env\s+pandas-quest\b/i.test(text)) return { ok: false, msg: "The env line does not say pandas-quest. Activate that environment (conda activate pandas-quest) and run the script again." };
    return { ok: true };
  }
  function pasteKernel(text) {
    if (/pandas-quest[\\/].*python/i.test(text)) return { ok: true };
    if (!text.trim()) return { ok: false, msg: "Paste the path the cell printed." };
    return { ok: false, msg: "That path does not point into the pandas-quest environment. In the notebook, click the kernel picker at the top right and choose pandas-quest, then run the cell again." };
  }
  function pasteHash(text) {
    if (!REAL.sha256) return { ok: false, msg: "The answer key for this puzzle has not been generated yet." };
    var m = text.toLowerCase().match(/[0-9a-f]{64}/);
    if (!m) return { ok: false, msg: "No 64-character hash found. Paste the full line the script printed." };
    if (m[0] === REAL.sha256) return { ok: true };
    return { ok: false, msg: "That hash does not match the original file. The download may be incomplete or the file may have been edited. Delete it and run download_data.py again." };
  }
  function pasteProject(text) {
    if (/project check:\s*7\s*\/\s*7/i.test(text)) return { ok: true };
    var m = /project check:\s*(\d+)\s*\/\s*(\d+)/i.exec(text);
    if (m) return { ok: false, msg: "You have " + m[1] + " of " + m[2] + ". Create whatever is marked [ ] and run the script again." };
    return { ok: false, msg: "Paste the full output; the last line should read  project check: 7/7." };
  }

  window.QUEST_ANSWERS = {
    checks: {
__STATIC__
      s0p1: { kind: "paste", test: pasteSetup },
      s0p2: { kind: "paste", test: pasteKernel },
      s6p1: { kind: "paste", test: pasteHash },
      s6p2: { kind: "paste", test: pasteProject },

      /* ---- real table: values come from REAL ---- */
      s7p1: real("int", "s7p1"),
      s7p2: real("int", "s7p2"),
      s8p1: real("num", "s8p1", 3),
      s8p2: real("text", "s8p2"),
      s9p1: real("num", "s9p1", 2),
      s9p2: real("int", "s9p2"),
      s10p1: real("text", "s10p1"),
      s10p2: real("int", "s10p2"),
      s11p1: real("int", "s11p1"),
      s11p2: real("num", "s11p2", 3)
    }
  };
})();
"""


def answers_js():
    st = static_answers()
    lines = "".join(f"      {qid}: {json.dumps(spec)},\n" for qid, spec in st.items())
    return ANSWERS_TEMPLATE.replace("__STATIC__", "      /* ---- toy table ---- */\n" + lines)


# ------------------------------------------------------------------ post
FRONT = """---
layout: post
title: "Introduction to Bioinformatics Programming in Python"
categories: articles
permalink: articles/intro-to-python-biosci
author: Atharva Bhagwat
---
"""


def post():
    body = (
        '<div class="quest" id="quest">\n'
        '<link rel="stylesheet" href="/assets/css/quest.css">\n'
        '<script src="/assets/js/quest-answers.js" defer></script>\n'
        '<script src="/assets/js/quest.js" defer></script>\n'
        + hero() + "\n"
        + part_header("Part 1", "Learn by running code", "Everything here runs in Colab, in your browser. Press the button, run the cells, fill in the blanks, see what happens.") + "\n"
        + "\n".join(finish_stage(k) for k in PART1) + "\n"
        + part_header("Part 2", "Take it to your own computer", "Once you have seen what notebooks can do, the limits become obvious. Now set up a proper workspace, learn the terminal, organise a project, and scale up on the cluster.") + "\n"
        + "\n".join(finish_stage(k) for k in PART2) + "\n"
        + content_hpc.HPC + "\n"
        + certificate() + "\n"
        + credits() + "\n"
        + '<button type="button" class="q-top" aria-label="Back to top"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>\n'
        '</div>\n'
    )
    return FRONT + "{% raw %}\n" + renumber(body) + "{% endraw %}\n"


if __name__ == "__main__":
    out = post()
    path = SITE / "_posts" / "articles" / "2026-11-04-introduction-to-bioinformatics-programming-in-python.md"
    path.write_text(out, encoding="utf-8")
    (SITE / "assets" / "js" / "quest-answers.js").write_text(answers_js(), encoding="utf-8")
    print("post bytes:", len(out.encode()), "lines:", out.count("\n"))
    qids = re.findall(r'data-qid="(\w+)"', out)
    print("puzzles:", len(qids), qids)
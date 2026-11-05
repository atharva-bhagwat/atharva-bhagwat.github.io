"""Assemble the MSCBIO2025 The Right Way article, its answers file and print a summary."""
import json
import re
from pathlib import Path

import qbuild
from qbuild import answer_hash, esc
import content_a
import content_b
import content_hpc
import content_ex

import sys
SITE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
STAGES = content_a.STAGES_A + content_b.STAGES_B


def with_exercises(stage_html):
    n = int(re.search(r'data-stage="(\d+)"', stage_html).group(1))
    items = content_ex.BY_STAGE.get(n)
    if not items:
        return stage_html
    block = '<div class="q-practice">' + content_ex.INTRO + "".join(items) + "</div>"
    marker = '<div class="q-puzzles">'
    assert stage_html.count(marker) == 1
    return stage_html.replace(marker, block + marker)


STAGES = [with_exercises(s) for s in STAGES]
N_EXERCISES = len(content_ex.EXERCISES)



# ------------------------------------------------------------------ hero
STAGE_INFO = [
    (0, "Basecamp", "set up your tools"),
    (1, "Notebook Ridge", "cells, kernels and Python basics"),
    (2, "Traceback Gorge", "errors are directions"),
    (3, "Table Flats", "your first DataFrame"),
    (4, "Score Falls", "new columns, groups, pivots"),
    (5, "Function Forge", "write it once, reuse it"),
    (6, "Project Lodge", "project layout and downloads"),
    (7, "Audit Pass", "trust, but verify"),
    (8, "Region Rapids", "group, merge, summarise"),
    (9, "Histogram Meadow", "plots for distributions"),
    (10, "Heatmap Heights", "plots for patterns"),
    (11, "The Summit", "robustness and reproducibility"),
]


def hero():
    rows = []
    for n, place, sub in STAGE_INFO:
        rows.append(
            f'<tr><th scope="row">{n}</th>'
            f'<td class="q-df-name"><a href="#stage-{n}">{esc(place)}</a></td>'
            f'<td data-cell="s{n}p1"><span class="q-nan">NaN</span></td>'
            f'<td data-cell="s{n}p2"><span class="q-nan">NaN</span></td></tr>'
        )
    table = (
        '<table class="q-df"><thead><tr><th></th><th class="q-df-name">stage</th><th>star1</th><th>star2</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
    )
    return (
        '<div class="q-bar">'
        '<span class="q-bar-stars"><span class="q-glyph" aria-hidden="true">&#9733;</span><span id="q-bar-count">0 / 24</span></span>'
        '<span class="q-bar-rank" id="q-bar-rank">Trailhead</span>'
        '<span class="q-bar-ex" id="q-bar-ex" title="Practice exercises ticked as done"></span>'
        '<span class="q-bar-links"><a href="#trail">Trail</a><button type="button" class="q-reset">Reset stars</button></span>'
        '</div>'
        '<section class="q-hero" id="trail">'
        '<p class="q-lede">Twelve stages take you from an empty laptop to publication-style figures. '
        'You will install the tools, learn pandas on a tiny table, build a project folder, then audit and plot a real dataset of more than four thousand protein variants. '
        'No biology is needed: every column is explained when you meet it.</p>'
        '<ul class="q-rules">'
        '<li><strong>Run it yourself.</strong>Each stage has hands-on practice, where you write functions and small analyses, and ends with a puzzle. Run everything on your own machine and type the answer you get.</li>'
        '<li><strong>Earn two stars a stage.</strong>The first star unlocks a harder second one. Twenty-four in all. Allow about fifteen hours with the practice exercises.</li>'
        '<li><strong>Nothing leaves your browser.</strong>Progress is saved in this browser only. Nothing is uploaded and there is no account.</li>'
        '</ul>'
        '<div class="q-nb" aria-label="Your progress, shown as a DataFrame">'
        '<div class="q-nb-row q-nb-in"><div class="q-nb-label">In [1]:</div><div class="q-nb-code">trail</div></div>'
        '<div class="q-nb-row q-nb-out"><div class="q-nb-label">Out[1]:</div><div class="q-nb-body">' + table + '</div></div>'
        '<div class="q-nb-row q-nb-in"><div class="q-nb-label">In [2]:</div><div class="q-nb-code">trail[["star1", "star2"]].notna().sum().sum()</div></div>'
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
        '<p>completed <strong>MSCBIO2025: The Right Way</strong>: set up a Python environment, learned pandas, wrote reusable functions, audited a real dataset and plotted it more than a dozen ways.</p>'
        '<p class="q-cert-stars" id="q-cert-stars" aria-hidden="true"></p>'
        '<p class="q-cert-rank" id="q-cert-rank"></p>'
        '<p><small>atharva-bhagwat.github.io/articles/mscbio2025-the-right-way</small></p>'
        '</div>'
        '</section>'
    )


def credits():
    return (
        '<div class="q-credits">'
        '<p><button type="button" class="q-reset">Reset all stars on this browser</button></p>'
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


ANSWERS_TEMPLATE = r"""/* Answers for MSCBIO2025 The Right Way.
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
title: "MSCBIO2025: The Right Way"
categories: articles
permalink: articles/mscbio2025-the-right-way
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
        + "\n".join(STAGES) + "\n"
        + content_hpc.HPC + "\n"
        + certificate() + "\n"
        + credits() + "\n"
        '</div>\n'
    )
    return FRONT + "{% raw %}\n" + body + "{% endraw %}\n"


if __name__ == "__main__":
    out = post()
    path = SITE / "_posts" / "articles" / "2026-11-04-mscbio2025-the-right-way.md"
    path.write_text(out, encoding="utf-8")
    (SITE / "assets" / "js" / "quest-answers.js").write_text(answers_js(), encoding="utf-8")
    print("post bytes:", len(out.encode()), "lines:", out.count("\n"))
    qids = re.findall(r'data-qid="(\w+)"', out)
    print("puzzles:", len(qids), qids)

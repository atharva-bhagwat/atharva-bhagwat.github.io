"""Tiny DSL that renders the Pandas Quest article as plain HTML.

Everything is emitted as static HTML (no markdown inside) so kramdown leaves
it alone, and the whole body is wrapped in {% raw %} for Liquid.
"""
import html
import re

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer

FORMATTER = HtmlFormatter(nowrap=True, classprefix="")


def esc(s):
    return html.escape(s, quote=False)


def fnv(s: str) -> str:
    """FNV-1a 32-bit, mirrored in quest.js so static answers are not plain text."""
    h = 0x811C9DC5
    for b in s.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def norm_text(s: str) -> str:
    return re.sub(r"\s+", "", s.strip().lower())


def answer_hash(qid: str, answer: str) -> str:
    return fnv(f"pq:{qid}:{norm_text(answer)}")


# ---------------------------------------------------------------- code blocks
COLLECTED_CODE = []  # (qid_or_label, code) pairs for testing


def code(text, lang="python", name=None, test=None):
    """A copyable code block. lang='text' renders as program output."""
    text = text.strip("\n")
    if test:
        COLLECTED_CODE.append((test, text))
    if lang == "text":
        body = esc(text)
        cls = "qcode is-output"
        label = name or "output"
        bar_btn = ""
    else:
        try:
            lexer = get_lexer_by_name(lang)
        except Exception:
            lexer = TextLexer()
        body = highlight(text, lexer, FORMATTER).rstrip("\n")
        cls = "qcode"
        label = name or lang
        bar_btn = '<button class="qcopy" type="button">Copy</button>'
    return (
        f'<div class="{cls}"><div class="qcode-bar"><span class="qcode-name">{esc(label)}</span>{bar_btn}</div>'
        f'<pre><code>{body}</code></pre></div>'
    )


def os_code(mac, win, lang="bash", win_lang="powershell", mac_name="macOS / Linux terminal", win_name="Windows (Anaconda Prompt)"):
    """Same step, two operating systems."""
    return (
        '<div class="q-os" data-os-group>'
        '<div class="q-os-tabs" role="tablist" aria-label="Operating system">'
        '<button type="button" role="tab" data-os="mac">macOS / Linux</button>'
        '<button type="button" role="tab" data-os="win">Windows</button>'
        '</div>'
        f'<div class="q-os-pane" data-os-pane="mac">{code(mac, lang, mac_name)}</div>'
        f'<div class="q-os-pane" data-os-pane="win">{code(win, win_lang, win_name)}</div>'
        '</div>'
    )


# ------------------------------------------------------------------- prose
def p(text):
    return f"<p>{text}</p>"


def h3(text):
    return f"<h3>{text}</h3>"


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ol(items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def table(headers, rows, cls="q-table"):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="q-table-wrap"><table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def callout(kind, title, body):
    """kind: note | trap | why | tip"""
    return f'<aside class="q-callout is-{kind}"><strong class="q-callout-title">{title}</strong>{body}</aside>'


def details(summary, body, cls=""):
    return f'<details class="q-details {cls}"><summary>{summary}</summary>{body}</details>'


def tree(text):
    return f'<pre class="q-tree"><code>{esc(text.strip(chr(10)))}</code></pre>'


# ------------------------------------------------------------------ puzzles
def puzzle(qid, part, question, kind="text", placeholder="", hint="", solution=None, solution_lang="python",
           choices=None, unit=None, test=None, spec=None, minwords=40, model=None):
    """kind: text | number | choices | paste | reflect.

    spec (optional) makes the puzzle self-contained: {"kind": "int"|"num"|"text"|"choices", "h":..., "value":..., "dp":..., "hs":[...]}.
    Puzzles without spec are looked up in quest-answers.js.
    """
    star_label = {1: "First star", 2: "Second star", 3: "Third star"}.get(part, "Star")
    attrs = ""
    if spec:
        attrs += f' data-kind="{spec["kind"]}"'
        if "h" in spec: attrs += f' data-h="{spec["h"]}"'
        if "value" in spec: attrs += f' data-value="{spec["value"]}"'
        if "dp" in spec: attrs += f' data-dp="{spec["dp"]}"'
        if "hs" in spec: attrs += f' data-hs="{",".join(spec["hs"])}"'
    if kind == "reflect":
        attrs += f' data-kind="reflect" data-minwords="{minwords}"'
    if kind == "choices":
        qs = []
        for qi, (qtext, opts) in enumerate(choices):
            radios = "".join(
                f'<label class="q-choice"><input type="radio" name="{qid}-{qi}" value="{chr(97 + oi)}"><span>{o}</span></label>'
                for oi, o in enumerate(opts)
            )
            qs.append(f'<fieldset class="q-choice-set"><legend>{qtext}</legend>{radios}</fieldset>')
        control = '<div class="q-choices">' + "".join(qs) + "</div>" + \
            '<div class="q-answer is-choices"><button type="button" class="q-check">Check answers</button></div>'
    elif kind == "reflect":
        control = (
            f'<div class="q-answer is-paste"><label class="q-prompt" for="in-{qid}">your conclusion</label>'
            f'<textarea id="in-{qid}" rows="7" spellcheck="true" autocomplete="off" placeholder="{esc(placeholder)}"></textarea>'
            f'<button type="button" class="q-check">Submit my conclusion</button></div>'
            f'<div class="q-model" hidden>{model or ""}</div>'
        )
    elif kind == "paste":
        control = (
            f'<div class="q-answer is-paste"><label class="q-prompt" for="in-{qid}">paste output</label>'
            f'<textarea id="in-{qid}" rows="6" spellcheck="false" autocomplete="off" placeholder="{esc(placeholder)}"></textarea>'
            '<button type="button" class="q-check">Check output</button></div>'
        )
    else:
        mode = "decimal" if kind == "number" else "text"
        control = (
            f'<div class="q-answer"><label class="q-prompt" for="in-{qid}">answer =</label>'
            f'<input id="in-{qid}" type="text" inputmode="{mode}" spellcheck="false" autocomplete="off" '
            f'autocapitalize="off" placeholder="{esc(placeholder)}">'
            '<button type="button" class="q-check">Check answer</button></div>'
        )
    helper = ""
    parts = []
    if hint:
        parts.append(f"<p>{hint}</p>")
    if solution:
        if test:
            COLLECTED_CODE.append((test, solution.strip("\n")))
        parts.append(code(solution, solution_lang, "one way to get it"))
    if parts:
        helper = details("Stuck? Nudge and solution" if kind != "reflect" else "Stuck? How to start", "".join(parts), "q-help")
    hidden = " hidden" if part >= 2 else ""
    cls = "q-puzzle is-part2" if part >= 2 else "q-puzzle"
    return (
        f'<div class="{cls}" data-qid="{qid}" data-part="{part}"{attrs}{hidden}>'
        f'<div class="q-puzzle-head"><span class="q-star" aria-hidden="true">&#9733;</span>'
        f'<h4>{star_label}</h4></div>'
        f'<div class="q-puzzle-body">{question}</div>'
        f'{control}'
        f'<p class="q-feedback" role="status" aria-live="polite"></p>'
        f'{helper}'
        f'</div>'
    )


# ------------------------------------------------------------------- stages
def stage(n, place, title, minutes, promise, blocks, puzzles):
    body = "".join(blocks)
    pz = "".join(puzzles)
    return (
        f'<section class="q-stage" id="stage-{n}" data-stage="{n}">'
        f'<header class="q-stage-head">'
        f'<div class="q-stage-title"><span class="q-stage-num">Stage {n}</span>'
        f'<h2>{place}: {title}</h2></div>'
        f'<div class="q-stage-stars" data-stars-for="{n}" aria-label="Stars earned in this stage">'
        f'<span class="q-s" data-part="1">&#9733;</span><span class="q-s" data-part="2">&#9733;</span></div>'
        f'</header>'
        f'<p class="q-promise">{promise} <span class="q-time">About {minutes} minutes.</span></p>'
        f'<div class="q-prose">{body}</div>'
        f'<div class="q-puzzles">{pz}</div>'
        f'</section>'
    )

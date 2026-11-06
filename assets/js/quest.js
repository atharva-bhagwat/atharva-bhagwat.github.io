/* MSCBIO2025 The Right Way: engine.
   Handles progress (saved in this browser only), answer checking,
   copy buttons, OS tabs and the printable certificate.
   Answers live in quest-answers.js, so you can edit content without touching this file. */
(function () {
  "use strict";

  var STORE_KEY = "mscbio2025.v1";
  var OS_KEY = "mscbio2025.os";
  var TOTAL_STARS = 24;   // recalculated from the page in start()
  var RANKS = [
    [0, "Trailhead"], [0.1, "Camper"], [0.22, "Hiker"], [0.38, "Ridge walker"],
    [0.58, "Peak bagger"], [0.8, "Summit seeker"], [1, "Summit"]
  ];

  var memory = { solved: {}, answers: {}, ex: {}, name: "" };   // fallback if localStorage is unavailable
  var root, A;

  /* ------------------------------------------------------------- storage */
  function load() {
    try {
      var raw = window.localStorage.getItem(STORE_KEY);
      if (raw) { var d = JSON.parse(raw); if (d && d.solved) { d.answers = d.answers || {}; d.ex = d.ex || {}; return d; } }
    } catch (e) { /* private mode etc. */ }
    return memory;
  }
  function save(state) {
    memory = state;
    try { window.localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) { /* ignore */ }
  }
  var state = { solved: {}, answers: {}, ex: {}, name: "" };

  /* ------------------------------------------------------------- hashing */
  function fnv(s) {
    var h = 0x811c9dc5, bytes = new TextEncoder().encode(s);
    for (var i = 0; i < bytes.length; i++) { h ^= bytes[i]; h = Math.imul(h, 0x01000193) >>> 0; }
    return ("00000000" + (h >>> 0).toString(16)).slice(-8);
  }
  function normText(s) { return String(s).trim().toLowerCase().replace(/\s+/g, ""); }
  function hashAnswer(qid, s) { return fnv("pq:" + qid + ":" + normText(s)); }

  /* ------------------------------------------------------------ checkers */
  function parseNumber(s) {
    var t = String(s).trim().replace(/,/g, "");
    if (t === "" || !/^[-+]?(\d+\.?\d*|\.\d+)(e[-+]?\d+)?$/i.test(t)) return NaN;
    return parseFloat(t);
  }
  function tooHighLow(user, expected) { return user > expected ? "Too high." : "Too low."; }

  function compare(spec, qid, raw, expected) {
    // returns {ok, msg}
    var kind = spec.kind;
    if (kind === "int" || kind === "num") {
      var u = parseNumber(raw);
      if (isNaN(u)) return { ok: false, msg: "That does not look like a number. Type just the digits, for example 12 or 0.345." };
      if (kind === "int") {
        if (Math.abs(u - Math.round(u)) > 1e-9) return { ok: false, msg: "This one is a whole number." };
        if (expected === undefined && spec.value !== undefined) expected = spec.value;
        if (expected === undefined) {
          return hashAnswer(qid, String(Math.round(u))) === spec.h ? { ok: true } : { ok: false, msg: "Not quite." };
        }
        return Math.round(u) === Math.round(expected) ? { ok: true } : { ok: false, msg: tooHighLow(u, expected) };
      }
      var tol = 0.5 * Math.pow(10, -(spec.dp === undefined ? 3 : spec.dp)) + 1e-9;
      var exp = expected === undefined ? spec.value : expected;
      return Math.abs(u - exp) <= tol ? { ok: true } : { ok: false, msg: tooHighLow(u, exp) + " Check the number of decimal places, too." };
    }
    // text
    if (expected === undefined && spec.value !== undefined) expected = spec.value;
    if (expected === undefined) {
      return hashAnswer(qid, raw) === spec.h ? { ok: true } : { ok: false, msg: "Not the one we are looking for." };
    }
    return normText(raw) === normText(expected) ? { ok: true } : { ok: false, msg: "Not the one we are looking for." };
  }

  function readAnswer(box, spec) {
    if (spec.kind === "choices") {
      var sets = box.querySelectorAll(".q-choice-set"), picks = [];
      for (var i = 0; i < sets.length; i++) {
        var r = sets[i].querySelector("input:checked");
        picks.push(r ? r.value : "");
      }
      return picks;
    }
    var el = box.querySelector("input[type=text], textarea");
    return el ? el.value : "";
  }

  function setFeedback(box, kind, text) {
    var f = box.querySelector(".q-feedback");
    f.className = "q-feedback" + (kind ? " is-" + kind : "");
    f.textContent = text || "";
  }

  function datasetSpec(box) {
    var d = box.dataset;
    if (!d.kind) return null;
    var spec = { kind: d.kind };
    if (d.h) spec.h = d.h;
    if (d.value !== undefined) spec.value = parseFloat(d.value);
    if (d.dp !== undefined) spec.dp = parseInt(d.dp, 10);
    if (d.hs) spec.hs = d.hs.split(",");
    return spec;
  }

  function wordCount(t) { var m = String(t).trim().match(/\S+/g); return m ? m.length : 0; }

  function check(box) {
    var qid = box.getAttribute("data-qid"), spec = A.checks[qid] || datasetSpec(box);
    if (!spec) { setFeedback(box, "bad", "This puzzle has no answer registered. Check quest-answers.js."); return; }
    if (spec.missing) { setFeedback(box, "bad", "The answer key for this puzzle has not been generated yet. See the setup notes for the site owner."); return; }
    var val = readAnswer(box, spec);

    if (spec.kind === "reflect") {
      var need = parseInt(box.getAttribute("data-minwords") || "40", 10), have = wordCount(val);
      if (have < need) { setFeedback(box, "bad", "Write a little more: " + have + " of at least " + need + " words. Use your own numbers and say what you think they mean."); return; }
      return solved(box, qid, false, String(val));
    }

    if (spec.kind === "choices") {
      if (val.some(function (v) { return !v; })) { setFeedback(box, "bad", "Answer all the questions first."); return; }
      var sets = box.querySelectorAll(".q-choice-set"), right = 0;
      for (var i = 0; i < sets.length; i++) {
        var good = hashAnswer(qid + "-" + i, val[i]) === spec.hs[i];
        sets[i].classList.toggle("is-right", good);
        sets[i].classList.toggle("is-wrong", !good);
        if (good) right++;
      }
      if (right === sets.length) return solved(box, qid, false, val.join(","));
      return setFeedback(box, "bad", right + " of " + sets.length + " correct. The questions marked in red need another look.");
    }

    if (spec.kind === "paste") {
      var res = spec.test(String(val));
      return res.ok ? solved(box, qid, false, String(val)) : setFeedback(box, "bad", res.msg);
    }

    if (!String(val).trim()) { setFeedback(box, "bad", "Type an answer first."); return; }

    var r2 = compare(spec, qid, val);
    if (r2.ok) solved(box, qid, false, val); else setFeedback(box, "bad", r2.msg);
  }

  /* ------------------------------------------------------------ progress */
  function starsCount() {
    var n = 0;
    for (var k in state.solved) if (state.solved[k]) n++;
    return n;
  }
  function rankFor(n) {
    var name = RANKS[0][1];
    RANKS.forEach(function (r) { if (n / TOTAL_STARS >= r[0] - 1e-9) name = r[1]; });
    return name;
  }

  function solved(box, qid, quiet, typed) {
    var first = !state.solved[qid];
    state.solved[qid] = true;
    if (typed !== undefined) state.answers[qid] = String(typed).slice(0, 3000);
    save(state);
    box.classList.add("is-solved");
    if (!quiet && first) box.classList.add("is-just-solved");
    var part = box.getAttribute("data-part");
    var stage = box.closest(".q-stage").getAttribute("data-stage");
    var next = box.parentNode.querySelector('.q-puzzle[data-part="' + (parseInt(part, 10) + 1) + '"]');
    if (!quiet) {
      var msg = next
        ? "Star earned. The next part is unlocked just below."
        : "Star earned. This stage is complete.";
      if (stage === "11" && part === "1") msg = "Star earned. Your certificate is at the bottom of the page.";
      setFeedback(box, "ok", msg);
    } else {
      setFeedback(box, "ok", "Solved.");
    }
    if (next) next.hidden = false;
    box.querySelectorAll(".q-model").forEach(function (m) { m.hidden = false; });
    var sf = box.querySelector("input[type=text], textarea");
    if (sf) {
      if (!sf.value && state.answers[qid]) sf.value = state.answers[qid];
      sf.readOnly = true;
    }
    if (quiet && state.answers[qid] && box.querySelector(".q-choice")) {
      var saved = state.answers[qid].split(",");
      box.querySelectorAll(".q-choice-set").forEach(function (set, i) {
        var r = set.querySelector('input[value="' + saved[i] + '"]');
        if (r) r.checked = true;
      });
    }
    box.querySelectorAll(".q-choice input").forEach(function (i) { i.disabled = true; });
    refresh(!quiet && first ? { qid: qid, stage: stage, part: part } : null);
  }

  function refresh(justSolved) {
    var n = starsCount();
    var total = document.getElementById("q-total");
    if (total) total.textContent = n;
    var out = document.getElementById("q-bar-count");
    if (out) out.textContent = n + " / " + TOTAL_STARS;
    var rank = document.getElementById("q-bar-rank");
    if (rank) rank.textContent = rankFor(n);
    var bar = root.querySelector(".q-bar");
    if (bar && justSolved) { bar.classList.remove("is-bump"); void bar.offsetWidth; bar.classList.add("is-bump"); }

    root.querySelectorAll("[data-stars-for]").forEach(function (el) {
      var s = el.getAttribute("data-stars-for");
      el.querySelectorAll(".q-s").forEach(function (star) {
        var part = star.getAttribute("data-part");
        star.classList.toggle("is-on", !!state.solved["s" + s + "p" + part]);
      });
    });
    root.querySelectorAll("td[data-cell]").forEach(function (td) {
      var key = td.getAttribute("data-cell");               // e.g. s3p1
      var got = !!state.solved[key];
      td.innerHTML = got ? '<span class="q-got" aria-label="solved">&#9733;</span>' : '<span class="q-nan">NaN</span>';
      if (got && justSolved && justSolved.qid === key) td.classList.add("is-just-solved");
    });

    var exBox = document.getElementById("q-bar-ex");
    if (exBox) {
      var total = root.querySelectorAll(".q-ex").length, done = 0;
      for (var k in state.ex) if (state.ex[k]) done++;
      exBox.textContent = total ? "Practice " + done + " / " + total : "";
    }

    var cert = document.getElementById("q-cert-wrap");
    if (cert) cert.hidden = !state.solved.s11p1;
    var stars = document.getElementById("q-cert-stars");
    if (stars) {
      var s = "";
      for (var i = 0; i < TOTAL_STARS; i++) s += i < n ? "\u2605" : '<span class="q-off">\u2605</span>';
      stars.innerHTML = s;
    }
    var cr = document.getElementById("q-cert-rank");
    if (cr) cr.textContent = rankFor(n) + ": " + n + " of " + TOTAL_STARS + " stars";
  }

  /* ---------------------------------------------------------------- init */
  function initPuzzles() {
    root.querySelectorAll(".q-puzzle").forEach(function (box) {
      var qid = box.getAttribute("data-qid");
      var btn = box.querySelector(".q-check");
      btn.addEventListener("click", function () { check(box); });
      var input = box.querySelector("input[type=text]");
      if (input) input.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); check(box); } });
      if (state.solved[qid]) solved(box, qid, true);
    });
  }

  function initExercises() {
    root.querySelectorAll(".q-ex").forEach(function (box) {
      var id = box.getAttribute("data-ex");
      var cb = box.querySelector(".q-ex-check");
      cb.checked = !!state.ex[id];
      box.classList.toggle("is-done", cb.checked);
      cb.addEventListener("change", function () {
        state.ex[id] = cb.checked;
        box.classList.toggle("is-done", cb.checked);
        save(state);
        refresh(null);
      });
    });
  }

  function initCopy() {
    root.addEventListener("click", function (e) {
      var btn = e.target.closest(".qcopy");
      if (!btn) return;
      var code = btn.closest(".qcode").querySelector("code").textContent;
      function done() {
        btn.textContent = "Copied"; btn.classList.add("is-done");
        setTimeout(function () { btn.textContent = "Copy"; btn.classList.remove("is-done"); }, 1400);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code).then(done, function () { fallbackCopy(code, done); });
      } else fallbackCopy(code, done);
    });
  }
  function fallbackCopy(text, done) {
    var ta = document.createElement("textarea");
    ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); done(); } catch (e) { /* ignore */ }
    document.body.removeChild(ta);
  }

  function guessOS() {
    var p = (navigator.userAgentData && navigator.userAgentData.platform) || navigator.platform || "";
    return /win/i.test(p) ? "win" : "mac";
  }
  function initOS() {
    var saved = null;
    try { saved = window.localStorage.getItem(OS_KEY); } catch (e) { /* ignore */ }
    var os = saved || guessOS();
    function apply(which) {
      root.querySelectorAll("[data-os-group]").forEach(function (g) {
        g.querySelectorAll("[data-os]").forEach(function (b) { b.setAttribute("aria-selected", b.getAttribute("data-os") === which ? "true" : "false"); });
        g.querySelectorAll("[data-os-pane]").forEach(function (p) { p.hidden = p.getAttribute("data-os-pane") !== which; });
      });
    }
    apply(os);
    root.addEventListener("click", function (e) {
      var b = e.target.closest("[data-os]");
      if (!b || !b.closest("[data-os-group]")) return;
      os = b.getAttribute("data-os");
      try { window.localStorage.setItem(OS_KEY, os); } catch (err) { /* ignore */ }
      apply(os);
    });
  }

  function initCertificate() {
    var input = document.getElementById("q-cert-input");
    var nameEl = document.getElementById("q-cert-name");
    var print = document.getElementById("q-cert-print");
    if (!input) return;
    input.value = state.name || "";
    nameEl.textContent = input.value || "Your name here";
    input.addEventListener("input", function () {
      state.name = input.value; save(state);
      nameEl.textContent = input.value || "Your name here";
    });
    print.addEventListener("click", function () {
      document.body.classList.add("q-printing");
      window.print();
    });
    window.addEventListener("afterprint", function () { document.body.classList.remove("q-printing"); });
  }

  function initReset() {
    root.querySelectorAll(".q-reset").forEach(function (b) {
      b.addEventListener("click", function () {
        if (window.confirm("Clear all your stars on this browser? This cannot be undone.")) {
          save({ solved: {}, answers: {}, ex: {}, name: "" });
          window.location.reload();
        }
      });
    });
  }

  function initTop() {
    var btn = root.querySelector(".q-top");
    if (!btn) return;
    var ticking = false;
    function update() {
      btn.classList.toggle("is-visible", window.pageYOffset > 400);
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    btn.addEventListener("click", function () {
      var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      window.scrollTo({ top: 0, behavior: calm ? "auto" : "smooth" });
      var bar = root.querySelector(".q-bar a, .q-bar button");
      if (bar) bar.focus({ preventScroll: true });
    });
    update();
  }

  function start() {
    root = document.getElementById("quest");
    A = window.QUEST_ANSWERS;
    if (!root || !A) return;
    state = load();
    TOTAL_STARS = root.querySelectorAll(".q-puzzle").length || TOTAL_STARS;
    initCopy();
    initOS();
    initPuzzles();
    initExercises();
    initCertificate();
    initReset();
    initTop();
    refresh(null);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
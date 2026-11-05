/* Answers for MSCBIO2025 The Right Way.
   - Toy-table answers are fixed (integers and text stored as short hashes).
   - Real-table answers live in REAL below. Generate them once with make_answer_key.py
     (pandas-quest-source/), which rewrites the block between the two markers.
   - To change a puzzle, edit its entry; quest.js does not need to change. */
(function () {
  "use strict";

  /*REAL_KEY_START*/
  var REAL = {
    "sha256": "e5a0a552896dd3f1d028f93a56861879c366e2b53f4242a98e722c447f163f8a",
    "s7p1": 4409,
    "s7p2": 361,
    "s8p1": 0.677069,
    "s8p2": "phosphatase_domain",
    "s9p1": 0.064255,
    "s9p2": 1044,
    "s10p1": "Pro",
    "s10p2": 270,
    "s11p1": 4048,
    "s11p2": 0.004595
  };
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
      /* ---- toy table ---- */
      s1p1: {"kind": "int", "h": "764a7680"},
      s1p2: {"kind": "text", "h": "7fa3d19e"},
      s2p1: {"kind": "choices", "hs": ["2d57137b", "c6c8cd74", "e6a4929e", "6eee199f"]},
      s2p2: {"kind": "num", "value": 2.718, "dp": 3},
      s3p1: {"kind": "int", "h": "c9065612"},
      s3p2: {"kind": "int", "h": "dbda3119"},
      s4p1: {"kind": "num", "value": 3.490026, "dp": 2},
      s4p2: {"kind": "text", "h": "3238a8d7"},
      s5p1: {"kind": "num", "value": 3.347902, "dp": 3},
      s5p2: {"kind": "num", "value": 2.694628, "dp": 3},

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

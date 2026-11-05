"""Generate the answer key for the real-data puzzles (run once).

  python make_answer_key.py pten-variant-abundance.csv pten-region-annotations.csv \
         /path/to/atharva-bhagwat.github.io/assets/js/quest-answers.js

It reads the two real CSVs, computes every answer with pandas using the same steps the
guide teaches, and rewrites the block between /*REAL_KEY_START*/ and /*REAL_KEY_END*/.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import pandas as pd

abundance_path, regions_path, js_path = map(Path, sys.argv[1:4])
df = pd.read_csv(abundance_path)
regions = pd.read_csv(regions_path)

pattern = r"^p\.(?P<ref>[A-Za-z]{3})(?P<position>\d+)(?P<alt>[A-Za-z]{3}|=)$"
parts = df["hgvs_pro"].str.extract(pattern)
df["position"] = pd.to_numeric(parts["position"]).astype("Int64")
df["alt"] = parts["alt"]


def find_region(pos):
    if pd.isna(pos):
        return "no_position"
    for r in regions.itertuples():
        if r.start <= pos <= r.end:
            return r.region
    return "other"


df["region"] = df["position"].map(find_region)
miss = df[df["record_type"] == "missense"]
dom = miss[miss["region"] == "phosphatase_domain"]

windows = miss.assign(window=miss["position"] // 10 * 10).groupby("window")["score"].agg(n="size", mean="mean")
medians = miss.groupby("region")["score"].median().drop(["other", "no_position"], errors="ignore")

key = {
    "sha256": hashlib.sha256(abundance_path.read_bytes()).hexdigest(),
    "s7p1": int(len(df)),
    "s7p2": int(df["position"].nunique()),
    "s8p1": round(float(dom["score"].mean()), 6),
    "s8p2": str(medians.idxmin()),
    "s9p1": round(float(df.loc[df["record_type"] == "nonsense", "score"].median()), 6),
    "s9p2": int((miss["score"] < 0.5).sum()),
    "s10p1": str(miss.groupby("alt")["score"].mean().idxmin()),
    "s10p2": int(windows[windows["n"] >= 30]["mean"].idxmin()),
    "s11p1": int((df["expts"] >= 3).sum()),
    "s11p2": round(float(dom[dom["expts"] >= 3]["score"].mean() - dom["score"].mean()), 6),
}

js = js_path.read_text(encoding="utf-8")
block = "/*REAL_KEY_START*/\n  var REAL = " + json.dumps(key, indent=2).replace("\n", "\n  ") + ";\n  /*REAL_KEY_END*/"
js, n = re.subn(r"/\*REAL_KEY_START\*/.*?/\*REAL_KEY_END\*/", lambda m: block, js, flags=re.S)
if n != 1:
    sys.exit("Could not find the REAL_KEY markers in " + str(js_path))
js_path.write_text(js, encoding="utf-8")
print(json.dumps(key, indent=2))
print("Wrote", js_path)

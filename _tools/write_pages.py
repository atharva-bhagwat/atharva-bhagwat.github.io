"""Write ONLY the guide pages (start page + guide/ folder). Does not touch assets/js/quest-answers.js.

Run from the repo root:   python _tools/write_pages.py .
"""
import sys
from pathlib import Path

import pages

site = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
files = pages.write_all(site)
print("wrote", len(files), "files")
for p in sorted(files):
    print("  ", p.relative_to(site))

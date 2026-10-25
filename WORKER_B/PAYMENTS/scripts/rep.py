"""Apply exact, unique string replacements to repository files.

Usage: python -I rep.py <edits.json>
The JSON is a list of {"file": <repo-relative path>, "old": <text>, "new": <text>}.
Each old text must occur exactly once; all edits of a run are checked before any file is written.
Files are read and written as bytes (UTF-8), so line endings are kept as they are.
"""
import json
import sys
from pathlib import Path

ROOT = Path(r"C:\dev\masaha\app-b")

edits = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
contents = {}
for e in edits:
    p = ROOT / e["file"]
    if e["file"] not in contents:
        contents[e["file"]] = p.read_bytes().decode("utf-8")
    text = contents[e["file"]]
    crlf = "\r\n" in text
    old = e["old"].replace("\r\n", "\n")
    new = e["new"].replace("\r\n", "\n")
    if crlf:
        old = old.replace("\n", "\r\n")
        new = new.replace("\n", "\r\n")
    n = text.count(old)
    if n != 1:
        print(f"FAIL {e['file']}: old text found {n} times: {old[:80]!r}")
        sys.exit(1)
    contents[e["file"]] = text.replace(old, new)
for f, text in contents.items():
    (ROOT / f).write_bytes(text.encode("utf-8"))
    print(f"OK {f}")

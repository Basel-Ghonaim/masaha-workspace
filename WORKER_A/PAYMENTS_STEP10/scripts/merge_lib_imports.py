"""Merges every `import { … } from '@shared/lib';` line of each given file into the first one, names sorted."""
import re
import sys

PATTERN = re.compile(r"^import \{ ([^}]*) \} from '@shared/lib';\n", re.M)

for path in sys.argv[1:]:
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    matches = list(PATTERN.finditer(text))
    if len(matches) < 2:
        continue
    names = sorted({n.strip() for m in matches for n in m.group(1).split(",") if n.strip()}, key=str.lower)
    merged = "import { " + ", ".join(names) + " } from '@shared/lib';\n"
    first = matches[0]
    out = text[: first.start()] + merged
    rest = text[first.end():]
    rest = PATTERN.sub("", rest)
    out += rest
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print("merged", path, names)

"""Commit 3 (C4) edits: the spark marks what matters now. newline='' keeps line endings."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
WEB = ROOT / 'apps' / 'web' / 'src'
DS = WEB / 'shared' / 'design-system'


def edit(path, pairs):
    with open(path, encoding='utf-8', newline='') as f:
        s = f.read()
    for old, new, count in pairs:
        n = s.count(old)
        if n != count:
            raise SystemExit(f'{path}: expected {count} occurrence(s), found {n}: {old[:80]!r}')
        s = s.replace(old, new)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(s)
    print('edited', path.relative_to(ROOT))


edit(DS / 'components/navigation/Tabs/Tabs.tsx', [
    (
        "// default: pills in a row that scrolls on a phone, as in the Owner › Members stress test, and a\n"
        "// segmented control from the tablet up. line: an underlined row, for the sections of a page.\n",
        "// default: pills in a row that scrolls on a phone, as in the Owner › Members stress test, and a\n"
        "// segmented control from the tablet up. line: an underlined row, for the sections of a page, the\n"
        "// active tab marked by a line in the spark.\n",
        1,
    ),
    ("after:h-0.5 after:bg-primary after:opacity-0", "after:h-0.5 after:bg-spark after:opacity-0", 1),
])

edit(DS / 'leaflet.css', [
    (
        "/* The selected mark: a ring on the primary colour and a floating shadow, never a fill. */\n"
        ".map-mark-selected span {\n"
        "  outline: 3px solid var(--primary);\n",
        "/*\n"
        " * The selected mark: a ring in the spark and a floating shadow, never a fill. The span keeps the\n"
        " * light theme, so the spark resolves as on the light tiles.\n"
        " */\n"
        ".map-mark-selected span {\n"
        "  outline: 3px solid var(--spark);\n",
        1,
    ),
])

edit(WEB / 'features/spaces/components/contacts/ContactsSheet.tsx', [
    ("(lifted || dragging) && 'border-primary shadow-floating'",
     "(lifted || dragging) && 'border-spark shadow-floating'", 1),
])

edit(WEB / 'features/spaces/components/photos/PhotosEdit.tsx', [
    ("(lifted || dragging) && 'outline-2 outline-primary'",
     "(lifted || dragging) && 'outline-2 outline-spark'", 1),
])

edit(WEB / 'pages/showcase/sections/fields/SortableSection.tsx', [
    ("(lifted || dragging) && 'border-primary shadow-floating'",
     "(lifted || dragging) && 'border-spark shadow-floating'", 2),
])

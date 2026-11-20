"""Commit 1 (C2) edits: hover is the neutral role, selected keeps the tint. Each old string must
occur exactly once; files are read and written with newline='' so line endings stay as they are."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
WEB = ROOT / 'apps' / 'web' / 'src'
DS = WEB / 'shared' / 'design-system'
C = DS / 'components'


def edit(path, pairs):
    with open(path, encoding='utf-8', newline='') as f:
        s = f.read()
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            raise SystemExit(f'{path}: expected 1 occurrence, found {n}: {old[:80]!r}')
        s = s.replace(old, new)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(s)
    print('edited', path.relative_to(ROOT))


# --- the layer ---------------------------------------------------------------------------------
edit(C / 'actions/Button/Button.tsx', [
    (
        "// A filled variant's hover mixes its fill toward the foreground rather than fading it: fading\n"
        "// primary to 90% leaves its label below AA in the light theme, while mixing toward the foreground\n"
        "// raises the contrast with the label in both themes. The outline variant is edged like a card,\n"
        "// so the edge stays visible in the dark theme, where the plain border is faint. A button marked\n"
        "// `aria-disabled`, which waits but keeps its place in the focus order, looks disabled too.\n",
        "// A hover never fades a fill: fading primary to 90% would leave its label below AA. The ink's\n"
        "// hover is a role of its own (`primary-hover`); secondary and destructive mix their fill toward\n"
        "// the foreground, which raises the contrast with the label in both themes. Outline and ghost\n"
        "// hover, and mark their open menu, with the neutral `hover` fill, never the selected tint. The\n"
        "// outline variant is edged like a card, so the edge stays visible in the dark theme, where the\n"
        "// plain border is faint. A button marked `aria-disabled`, which waits but keeps its place in the\n"
        "// focus order, looks disabled too.\n",
    ),
    (
        "'bg-primary text-primary-foreground hover:bg-[color-mix(in_oklch,var(--primary),var(--foreground)_12%)]',",
        "'bg-primary text-primary-foreground hover:bg-primary-hover',",
    ),
    (
        "'border-(--card-border) bg-card text-foreground hover:bg-accent hover:text-accent-foreground aria-expanded:bg-accent aria-expanded:text-accent-foreground',",
        "'border-(--card-border) bg-card text-foreground hover:bg-hover hover:text-hover-foreground aria-expanded:bg-hover aria-expanded:text-hover-foreground',",
    ),
    (
        "'text-foreground hover:bg-accent hover:text-accent-foreground aria-expanded:bg-accent aria-expanded:text-accent-foreground',",
        "'text-foreground hover:bg-hover hover:text-hover-foreground aria-expanded:bg-hover aria-expanded:text-hover-foreground',",
    ),
])

edit(C / 'fields/Calendar/Calendar.tsx', [
    (
        "// A filled day (chosen, or an end of a range) takes the primary pair, and its hover mixes toward\n"
        "// the foreground as the primary Button's does; a day inside a range takes the accent pair.\n"
        "const FILLED =\n"
        "  'bg-primary text-primary-foreground hover:bg-[color-mix(in_oklch,var(--primary),var(--foreground)_12%)] hover:text-primary-foreground';\n",
        "// A filled day (chosen, or an end of a range) takes the primary pair and the ink's own hover, as\n"
        "// the primary Button does. A day inside a range takes the selected tint (the accent pair) and keeps\n"
        "// it under the pointer, so it has no ghost hover. Today's cell is muted, where the neutral hover\n"
        "// would vanish in dark: today's day, unless filled, hovers with the ink's wash.\n"
        "const FILLED =\n"
        "  'bg-primary text-primary-foreground hover:bg-primary-hover hover:text-primary-foreground';\n",
    ),
    (
        "  const single =\n"
        "    modifiers.selected && !modifiers.range_start && !modifiers.range_end && !modifiers.range_middle;\n",
        "  const single =\n"
        "    modifiers.selected && !modifiers.range_start && !modifiers.range_end && !modifiers.range_middle;\n"
        "  const filled = single || modifiers.range_start || modifiers.range_end;\n",
    ),
    (
        "      ref={ref}\n"
        "      variant=\"ghost\"\n"
        "      size=\"icon\"\n"
        "      data-day={day.isoDate}\n",
        "      ref={ref}\n"
        "      variant={modifiers.range_middle ? null : 'ghost'}\n"
        "      size=\"icon\"\n"
        "      data-day={day.isoDate}\n",
    ),
    (
        "        (single || modifiers.range_start || modifiers.range_end) && FILLED,\n",
        "        filled && FILLED,\n"
        "        modifiers.today && !filled && !modifiers.range_middle && 'hover:bg-hover-on-muted',\n",
    ),
])

edit(C / 'actions/DropdownMenu/DropdownMenu.tsx', [
    (
        "pointer-coarse:min-h-(--control-height) focus:bg-accent focus:text-accent-foreground data-disabled:",
        "pointer-coarse:min-h-(--control-height) focus:bg-hover focus:text-hover-foreground data-disabled:",
    ),
    (
        "focus:[&_svg]:text-accent-foreground",
        "focus:[&_svg]:text-hover-foreground",
    ),
    (
        "'data-open:bg-accent data-open:text-accent-foreground'",
        "'data-open:bg-hover data-open:text-hover-foreground'",
    ),
])

edit(C / 'fields/Select/Select.tsx', [
    (
        "select-none focus:bg-accent focus:text-accent-foreground data-disabled:",
        "select-none focus:bg-hover focus:text-hover-foreground data-disabled:",
    ),
])

edit(C / 'fields/Combobox/Combobox.tsx', [
    (
        "data-[selected=true]:bg-accent data-[selected=true]:text-accent-foreground",
        "data-[selected=true]:bg-hover data-[selected=true]:text-hover-foreground",
    ),
])

edit(C / 'data/Table/Table.tsx', [
    (
        " * A table of records, as in the Owner › Members stress test: a muted header row, dense rows with a\n"
        " * divider, and a row that takes the accent while hovered or while its row menu is open. It scrolls\n",
        " * A table of records, as in the Owner › Members stress test: a muted header row, dense rows with a\n"
        " * divider, and a row that takes the hover fill while hovered or while its row menu is open. It scrolls\n",
    ),
    (
        " * One row. It takes the accent under the pointer, and while a menu opened from it is open, so the\n"
        " * row an action applies to stays marked (the Data reports stress test). Text on the accent keeps\n"
        " * its colour: `foreground` and `muted-foreground` are verified on it (foundation §5).\n",
        " * One row. It takes the neutral `hover` fill under the pointer, and while a menu opened from it is\n"
        " * open, so the row an action applies to stays marked (the Data reports stress test); never the\n"
        " * selected tint. Text on it keeps its colour: `muted-foreground` is verified on it, and\n"
        " * `foreground` is its `-foreground`'s value (foundation §5).\n",
    ),
    (
        "'border-b border-border transition-colors hover:bg-accent has-data-open:bg-accent',",
        "'border-b border-border transition-colors hover:bg-hover has-data-open:bg-hover',",
    ),
])

edit(C / 'data/DataTable/DataTable.tsx', [
    (
        "  const direction = column.getIsSorted();\n"
        "  return (\n",
        "  const direction = column.getIsSorted();\n"
        "  // The header row is muted, where the neutral hover would vanish in dark: the sort button hovers\n"
        "  // with the ink's wash, its text the foreground.\n"
        "  return (\n",
    ),
    (
        "rounded-sm px-2 transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:",
        "rounded-sm px-2 transition-colors hover:bg-hover-on-muted hover:text-foreground focus-visible:",
    ),
])

edit(C / 'fields/Input/Input.tsx', [
    (
        "after:-inset-1.5 hover:bg-accent hover:text-accent-foreground focus-visible:",
        "after:-inset-1.5 hover:bg-hover hover:text-hover-foreground focus-visible:",
    ),
])

edit(C / 'fields/ToggleGroup/ToggleGroup.tsx', [
    (
        " * One chip. When on, it takes the accent pair, a primary edge and a check at its start, so the\n"
        " * state never rests on colour alone. The edges are sampled from the stress test: `input` off,\n"
        " * `primary` on.\n",
        " * One chip. When on, it takes the selected tint (the accent pair), a spark edge and a check at its\n"
        " * start, so the state never rests on colour alone, and keeps the tint under the pointer: only a\n"
        " * chip that is off hovers, with the neutral fill. Its edge is `input` off, the spark on.\n",
    ),
    (
        "text-foreground transition-colors select-none hover:bg-accent hover:text-accent-foreground focus-visible:",
        "text-foreground transition-colors select-none not-data-on:hover:bg-hover not-data-on:hover:text-hover-foreground focus-visible:",
    ),
    (
        "data-on:border-primary data-on:bg-accent data-on:text-accent-foreground",
        "data-on:border-spark data-on:bg-accent data-on:text-accent-foreground",
    ),
])

edit(C / 'navigation/Tabs/Tabs.tsx', [
    (
        "not-data-active:hover:bg-accent not-data-active:hover:text-accent-foreground data-active:border-primary",
        "not-data-active:hover:bg-hover not-data-active:hover:text-hover-foreground data-active:border-primary",
    ),
    (
        "md:not-data-active:hover:bg-transparent md:not-data-active:hover:text-foreground",
        "md:not-data-active:hover:bg-hover-on-muted md:not-data-active:hover:text-foreground",
    ),
])

edit(C / 'fields/SegmentedControl/SegmentedControl.tsx', [
    (
        "text-muted-foreground transition-colors select-none hover:text-foreground focus-visible:",
        "text-muted-foreground transition-colors select-none hover:text-foreground data-unchecked:hover:bg-hover-on-muted focus-visible:",
    ),
])

edit(C / 'navigation/Sidebar/Sidebar.tsx', [
    (
        "  /** The page shown now: highlighted, and marked as the current page. */\n",
        "  /**\n"
        "   * The page shown now: the selected tint and a spark bar at its start, kept under the pointer,\n"
        "   * and marked as the current page.\n"
        "   */\n",
    ),
    (
        "  const item = (\n"
        "    <Comp\n",
        "  // Only an item that is not the current page hovers, with the neutral fill: the current one keeps\n"
        "  // its tint under the pointer and has a 3 px spark bar at its inline start, clipped by its radius.\n"
        "  const item = (\n"
        "    <Comp\n",
    ),
    (
        "'flex h-10 w-full items-center gap-3 rounded-md px-3 text-body text-sidebar-foreground transition-colors pointer-coarse:h-(--control-height) hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sidebar-ring data-[active=true]:bg-sidebar-accent data-[active=true]:text-sidebar-accent-foreground [&_svg]:",
        "'relative flex h-10 w-full items-center gap-3 overflow-hidden rounded-md px-3 text-body text-sidebar-foreground transition-colors pointer-coarse:h-(--control-height) not-data-[active=true]:hover:bg-hover not-data-[active=true]:hover:text-hover-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sidebar-ring data-[active=true]:bg-sidebar-accent data-[active=true]:text-sidebar-accent-foreground data-[active=true]:before:absolute data-[active=true]:before:inset-y-0 data-[active=true]:before:start-0 data-[active=true]:before:w-0.75 data-[active=true]:before:bg-spark [&_svg]:",
    ),
])

edit(C / 'display/FilterTag/FilterTag.tsx', [
    (
        " * the Admin › Data reports stress test (finding 8). The pill is the chips' shape on the\n"
        " * `secondary` pair; the button is 32px, and the control height on touch, so it stays a 44px target.\n",
        " * the Admin › Data reports stress test (finding 8). The pill is the chips' shape on the\n"
        " * `secondary` pair; the button is 32px, and the control height on touch, so it stays a 44px target.\n"
        " * It hovers with the ink's wash: on the pill, the neutral hover would vanish in dark.\n",
    ),
    (
        'className="size-8 rounded-(--radius-pill) pointer-coarse:size-(--control-height)"',
        'className="size-8 rounded-(--radius-pill) hover:bg-hover-on-muted pointer-coarse:size-(--control-height)"',
    ),
])

edit(DS / 'leaflet.css', [
    (
        ".leaflet-bar a:hover {\n"
        "  background-color: var(--accent);\n"
        "  color: var(--accent-foreground);\n"
        "}\n",
        ".leaflet-bar a:hover {\n"
        "  background-color: var(--hover);\n"
        "  color: var(--hover-foreground);\n"
        "}\n",
    ),
])

# --- features and pages: a card or tile hovers with the neutral fill ----------------------------
for rel, old, new in [
    ('features/directory/components/card/SpaceCard.tsx',
     '<Card className="h-full overflow-hidden pt-0 hover:bg-accent">',
     '<Card className="h-full overflow-hidden pt-0 hover:bg-hover">'),
    ('features/directory/components/page/ContactList.tsx',
     'transition-colors hover:bg-accent focus-visible:',
     'transition-colors hover:bg-hover focus-visible:'),
    ('features/finance/components/DebtsTab.tsx',
     "'h-full hover:bg-accent'",
     "'h-full hover:bg-hover'"),
    ('features/overview/components/admin/PlatformTiles.tsx',
     'className="flex-1 hover:bg-accent"',
     'className="flex-1 hover:bg-hover"'),
    ('features/overview/components/owner/OwnerOverview.tsx',
     'className="h-full hover:bg-accent"',
     'className="h-full hover:bg-hover"'),
    ('pages/site/public/home/AreaCards.tsx',
     '<Card className="h-full hover:bg-accent">',
     '<Card className="h-full hover:bg-hover">'),
    ('features/spaces/components/contacts/ContactsSheet.tsx',
     'select-none hover:bg-accent focus-visible:',
     'select-none hover:bg-hover focus-visible:'),
    ('pages/showcase/sections/fields/SortableSection.tsx',
     'select-none hover:bg-accent focus-visible:',
     'select-none hover:bg-hover focus-visible:'),
]:
    edit(WEB / rel, [(old, new)])

# The contact tile is muted, where the neutral hover would vanish in dark: the muted fill moves to
# the list item, and the link lays the ink's wash over it (D1).
edit(WEB / 'features/spaces/components/contacts/ContactsView.tsx', [
    (
        '          <li key={tile.key} className="min-w-0">\n',
        '          <li key={tile.key} className="min-w-0 rounded-lg bg-muted">\n',
    ),
    (
        'className="flex min-w-0 items-center gap-3 rounded-lg bg-muted px-3 py-2 hover:bg-accent focus-visible:',
        'className="flex min-w-0 items-center gap-3 rounded-lg px-3 py-2 hover:bg-hover-on-muted focus-visible:',
    ),
    (
        " * a working link, its value isolated left to right, a contact's own name in no known direction.\n",
        " * a working link, its value isolated left to right, a contact's own name in no known direction. The\n"
        " * tile's muted fill is the list item's, so the link's hover lays the ink's wash over it.\n",
    ),
])

# The showcase's current entry keeps the selected tint; only the others hover.
edit(WEB / 'pages/showcase/ShowcaseNav.tsx', [
    (
        "          'block rounded-md px-3 py-1.5 text-body-sm text-foreground hover:bg-accent hover:text-accent-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring',\n"
        "          className,\n"
        "          isActive && 'bg-accent text-accent-foreground',\n",
        "          'block rounded-md px-3 py-1.5 text-body-sm text-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring',\n"
        "          className,\n"
        "          isActive ? 'bg-accent text-accent-foreground' : 'hover:bg-hover hover:text-hover-foreground',\n",
    ),
])

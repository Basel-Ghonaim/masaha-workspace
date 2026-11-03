root = 'C:/dev/masaha/app-lane-b/docs'

def edit(rel, pairs):
    p = root + '/' + rel
    with open(p, encoding='utf8', newline='') as f:
        s = f.read()
    for old, new in pairs:
        assert s.count(old) == 1, (rel, old[:60], s.count(old))
        s = s.replace(old, new)
    with open(p, 'w', encoding='utf8', newline='') as f:
        f.write(s)

edit('frontend/design-system/foundation.md', [
    ('| `display` | shows content | Avatar · Badge · Card · StatCard · Separator |',
     '| `display` | shows content | Avatar · Badge · Card · StatCard · Separator · FilterTag |'),
    ('| StatCard | hand-built | Dashboard overview numbers |\n',
     '| StatCard | hand-built | Dashboard overview numbers |\n'
     '| FilterTag | hand-built | A filter in force: its label and a remove button named by a prop (finding 8) · the chips\' `radius-pill` on the `secondary` pair · the button 32px, the control height on touch ([finding 8](../../architecture/findings/8-the-stress-tests-applied-filter-tag-has-no-component.md)) |\n'),
])

edit('architecture/findings/8-the-stress-tests-applied-filter-tag-has-no-component.md', [
    ('**Status:** Open · **Date:** 2026-09-28', '**Status:** Resolved · **Date:** 2026-09-28'),
    ('- **Until then:** the finding stays open, and nothing is built now.\n',
     '- **Until then:** the finding stays open, and nothing is built now.\n\n'
     '**Resolution (2026-10-28, #PRNUM):** `FilterTag`, used by the admin\'s data reports. A `display` component with a foundation §12 row: the caller\'s label and a ghost remove button with an `XIcon`, named by `removeLabel` (the layer has no words), a pill on the `secondary` pair; the button is 32px and the control height on touch. The admin\'s reports show the space and the field in force as tags at every width, beside «مسح الفلاتر» (DI-40).\n'),
])

edit('architecture/findings/README.md', [
    ('## Open\n\n- [8. The stress test\'s applied-filter tag has no component](8-the-stress-tests-applied-filter-tag-has-no-component.md)\n',
     '## Open\n\n'),
    ('- [7. The stress test\'s filter chips have no component](7-the-stress-tests-filter-chips-have-no-component.md)\n',
     '- [7. The stress test\'s filter chips have no component](7-the-stress-tests-filter-chips-have-no-component.md)\n'
     '- [8. The stress test\'s applied-filter tag has no component](8-the-stress-tests-applied-filter-tag-has-no-component.md)\n'),
])
print('ok')

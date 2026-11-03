import glob, os
os.chdir('C:/dev/masaha/app-lane-w2')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


F99 = '../architecture/findings/99-the-owners-checklist-cannot-name-a-retired-amenity.md'
edit('docs/features/lookups.md', [
("""Set for an owner (`source`), it reads the public catalogue only, which names no retired amenity: one the space still has stays in the value, unseen and never toggled, and one line under the list counts them ([finding 99](%s)). On either list, an amenity ticked but not linked that is retired before the save is no longer offered: the next tick or untick leaves it out of the value (the space editor's section takes it out at once when the save is refused for it), and the line counts only the linked ones.""" % F99,
 """Set for an owner (`source`), it reads the public catalogue only, which names no retired amenity: the retired ones the space holds come named with the space's read (`retired`, the read's `retiredAmenities`), listed after the others, ticked, with "No longer on the platform’s list" beside them; unticked, one is left out of the next save, and stays listed until then ([finding 99](%s), resolved). On either list, an amenity ticked but not linked that is retired before the save is no longer offered: the next tick or untick leaves it out of the value (the space editor's section takes it out at once when the save is refused for it).""" % F99),
("""the public checklist keeps a retired amenity in the value and counts it ([finding 99](%s)). 2026-10-20, #96.""" % F99,
 """the public checklist keeps a retired amenity in the value and counts it ([finding 99](%s)). 2026-10-20, #96. Since #PRNUM it names each from the space's read instead, marked, so the owner can leave it out. 2026-10-29, #PRNUM.""" % F99),
("""- [99](%s): the owner's checklist cannot name a retired amenity.
""" % F99, ""),
("""- #PRNUM — the switches only in the rows;""",
 """- #PRNUM — the owner's checklist names the retired amenities the space holds, from the space's read, marked, and drops one unticked; the count line removed (finding 99).
- #PRNUM — the switches only in the rows;"""),
])
s = open('docs/features/lookups.md', encoding='utf8').read()
assert '## Open findings\n\n## History' not in s, 'empty open findings'

edit('docs/features/spaces.md', [
("""and a retired amenity stays linked, counted in one line ([finding 99](%s));""" % F99,
 """and a retired amenity the space holds is listed from the space's read (`retiredAmenities`), ticked and marked «لم يعد في قائمة المنصة», until a save leaves it out ([finding 99](%s), resolved);""" % F99),
])
p = 'docs/features/spaces.md'
s = open(p, encoding='utf8', newline='').read()
i = s.index('### Web history')
j = s.find('\n### ', i + 5)
j = len(s) if j == -1 else j
section = s[i:j].rstrip('\n')
section += "\n- #PRNUM — the amenities' section hands `lookups`' checklist the space's retired amenities (`retired`), named, so an owner's lists them (finding 99).\n"
s = s[:i] + section + ('\n' + s[j:].lstrip('\n') if j < len(s) else '')
open(p, 'w', encoding='utf8', newline='').write(s)

p = glob.glob('docs/architecture/findings/99-*.md')[0]
s = open(p, encoding='utf8', newline='').read()
s = s.replace('**Status:** Open · **Date:** 2026-10-20', '**Status:** Resolved · **Date:** 2026-10-20 · **Resolved:** 2026-10-29', 1)
s = s.rstrip('\n') + "\n\n**Resolution (#PRNUM):** The space's reads name its retired amenities (`retiredAmenities`, D2.15), and the owner's checklist lists each after the others, ticked and marked «لم يعد في قائمة المنصة» / \"No longer on the platform’s list\", until a save leaves it out (D6.13); the count line is gone.\n"
open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')

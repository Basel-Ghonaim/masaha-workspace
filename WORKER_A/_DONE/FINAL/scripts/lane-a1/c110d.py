def edit(p, pairs):
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)
D = r'C:\dev\masaha\app-lane-a1\docs'
edit(D + r'\api\api-contract.md', [
("""`false` deactivates the person's reception link and ends every session they hold ([security.md](../backend/security.md#tokens-and-cookies));""",
 """`false` deactivates the person's reception link, and ends every session they hold when no other active link of theirs remains ([security.md](../backend/security.md#tokens-and-cookies)); a person with another link keeps their sessions, and this space closes to them at once, since the boundary reads the links on every request (2026-10-29, #PRNUM);"""),
])
edit(D + r'\backend\security.md', [
("""a Google link and the deactivation of a reception link end every session of the user:""",
 """a Google link and the deactivation of a person's last active link, a reception link (a person who keeps another active link keeps their sessions, [finding 92](../architecture/findings/92-an-owner-can-end-the-sessions-of-another-spaces-owner-at-will.md), 2026-10-29, #PRNUM), end every session of the user:"""),
])
edit(D + r'\features\space-links.md', [
("""- **A deactivation or a re-activation takes the space's lock, then the person's, and acts on a reception link only,**""",
 """- **A deactivation ends the person's sessions only when no other active link of theirs remains** (`countOtherActiveLinks`, under the person's lock). *Why:* an owner of one space must not end another space's owner's sessions at will ([finding 92](../architecture/findings/92-an-owner-can-end-the-sessions-of-another-spaces-owner-at-will.md)); the space boundary reads the links on every request, so this space closes to them at once anyway. Supersedes "the deactivation ends every session" below. 2026-10-29, #PRNUM.
- **A deactivation or a re-activation takes the space's lock, then the person's, and acts on a reception link only,**"""),
("""- [92](../architecture/findings/92-an-owner-can-end-the-sessions-of-another-spaces-owner-at-will.md): an owner can end the sessions of another space's owner at will.
""", ""),
("the spaces list's statuses one schema, `editable` among them.", "the spaces list's statuses one schema, `editable` among them; a deactivation keeps the sessions of a person with another active link."),
])
p = D + r'\architecture\findings\92-an-owner-can-end-the-sessions-of-another-spaces-owner-at-will.md'
s = open(p, encoding='utf8').read()
old = '**Status:** Open · **Date:** 2026-10-18'
assert s.count(old) == 1
s = s.replace(old, '**Status:** Resolved · **Date:** 2026-10-18 · **Resolved:** 2026-10-29')
s = s.rstrip('\n') + '\n\n**Resolution (#PRNUM):** A deactivation ends the person\'s sessions only when no other active link remains (D1.9).\n'
open(p, 'w', encoding='utf8', newline='').write(s)

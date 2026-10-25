R = 'C:/dev/masaha/app-b/docs/'


def ed(p, pairs):
    s = open(R + p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:80])
        s = s.replace(a, b)
    open(R + p, 'w', encoding='utf-8', newline='').write(s)


ed('features/directory.md', [
("**Last Updated:** 2026-10-22", "**Last Updated:** 2026-10-24"),
("""- Answers a space's public page: its profile, hours and shifts, prices, amenities, contacts and each group's freshness.""",
"""- Answers a space's public page: its profile, hours and shifts, prices, amenities, contacts and each group's freshness, and its running and upcoming announcements."""),
("""The announcements, the reports and the favourites' cards are not built.""",
"""The reports and the favourites' cards are not built; the page's announcements are answered by the API, not shown on the site yet."""),
("""- **Leaves** the live status to [`occupancy`](occupancy.md): its rule, and which spaces are available now.""",
"""- **Leaves** the live status to [`occupancy`](occupancy.md): its rule, and which spaces are available now.
- **Leaves** which announcements the public sees, and their order, to [`announcements`](announcements.md)."""),
("""- **The card and the pin carry the live status, never a count;""",
"""- **The page carries the space's running and upcoming announcements, at most 20, read after the space's share lock** (D5). *Why:* an announcement is no fact group, so it need not be read with the facts; one posted between the two reads shows on the next, and one that starts or ends within the page's 30 seconds. 2026-10-24, #PRNUM.
- **The card and the pin carry the live status, never a count;"""),
("""- #94 — the live status on the card and the pin, the `availableNow` filter, and a space's live status alone.
""", """- #94 — the live status on the card and the pin, the `availableNow` filter, and a space's live status alone.
- #PRNUM — a space's running and upcoming announcements on its page.
"""),
])

ed('plans/v1-mvp.md', [
("""and `GET /spaces/:slug`, a space's public page, without announcements;""",
"""and `GET /spaces/:slug`, a space's public page, with its running and upcoming announcements (2026-10-24, #PRNUM);"""),
("""| GET | `/spaces/:slug` | 🌐 | its announcements, with step 10 |""",
"""| GET | `/spaces/:slug` | 🌐 | its running and upcoming announcements, built (#PRNUM) |"""),
])
print('ok')

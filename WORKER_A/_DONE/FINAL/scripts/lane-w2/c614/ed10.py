p = 'C:/dev/masaha/app-lane-w2/docs/features/lookups.md'
s = open(p, encoding='utf8', newline='').read()


def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)


rep("**Last Updated:** 2026-10-24", "**Last Updated:** 2026-10-29")
rep("""with the page's hint under them; the tab shown is kept in the address""",
    """with the tab's own hint under them (the governorates' says what hiding does, the amenities' what retiring does; both that the order here is the order shown); the tab shown is kept in the address""")
rep("""- a sheet adds or renames a governorate or an area;
- each row can be hidden or restored, and moved up or down its list;""",
    """- a sheet adds or renames a governorate or an area: its two names only, since its switch lives in its row;
- each row can be hidden or restored, and moved up or down its list; each arrow is named with where the row stands ("Move up: Al-Rimal — 2 of 11"), the moved row keeps the focus, and a polite live region in the row says where it now stands ("Al-Rimal: 1 of 11") once the move has landed, the rows that made room saying nothing;
- the sheet that edits a row of a list of more than ten rows (the governorates, or one governorate's areas) also offers its "Position", 1 to the list's count, Arabic-Indic digits read, refused outside the range in its helper's words ("From 1 to 11"); after the names, a new position is saved through the list's order route, the whole order with the row moved, so the last row reaches the top in one write;""")
rep("""- a sheet adds or edits an amenity: its names, its icon, chosen from a grid of the eight, and, when editing, its "Active" switch; its key, which the server derives from its English name, is never shown;""",
    """- a sheet adds or edits an amenity: its names and its icon, chosen from a grid of the eight, and, editing one of more than ten amenities, its "Position", as a governorate's; its "Active" switch is its row's alone; its key, which the server derives from its English name, is never shown;""")
rep("""- **The page's two sections sit under tabs, the tab kept in the address;**""",
    """- **A row's switch lives only in its row; its sheet keeps its names, and an amenity's icon** (AD-025). *Why:* one control and one feedback per fact; a switch in both places could be set two ways at once. 2026-10-29, #PRNUM.
- **A list of more than ten rows offers a row's position in its sheet, saved through the list's order route after the names** (AD-026). *Why:* with eleven areas, the arrows alone take ten writes to bring the last to the top; the order route takes the whole order, so the row moved is sent with every other id, and its 409 reads as any order's. The field is bounded by the list as the sheet opens, and its order waits out every arrow of the list, as an arrow's does. 2026-10-29, #PRNUM.
- **An arrow is named with where its row stands, and a move is said once it lands** (AD-026). *Why:* a screen reader hears where the row is before it moves it, and where it went after, without leaving the row; the live region is the row's own, so only the row moved speaks. 2026-10-29, #PRNUM.
- **The page's two sections sit under tabs, the tab kept in the address;**""")
rep("""- #111 — the public areas for Home (`usePublicAreas`).""",
    """- #111 — the public areas for Home (`usePublicAreas`).
- #PRNUM — the switches only in the rows; a row's position in its sheet past ten rows; the arrows named with the row's position, and a move said; each tab its own hint.""")
open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')

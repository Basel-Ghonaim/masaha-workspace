import io, sys
R = 'C:/dev/masaha/app-b/'
def edit(path, pairs):
    p = R + path
    s = io.open(p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        n = s.count(a)
        if n != 1:
            sys.exit(f'{path}: {n}x {a[:60]!r}')
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)

# Item 1, its documents
fav_c1 = [
    ("**Save.** In one transaction: the user's row locked",
     "**Save.** Whether the space is publicly listed is read first, before the transaction (those reads are not the transaction's, [conventions §8](../backend/conventions.md#transactions)); then, in one transaction: the user's row locked"),
    ("a space the public listing does not list is `not_found`;",
     "a space the public listing did not list is `not_found`;"),
    ("- #121 — a signed-in user's favourites saved and removed, idempotent, at most 200; read whole as the directory's cards, newest saved first or nearest first.\n",
     "- #121 — a signed-in user's favourites saved and removed, idempotent, at most 200; read whole as the directory's cards, newest saved first or nearest first.\n- #PRNUM — the save reads the listing before it takes the user's lock (#121's review); a saved space that left, saved again, is tested.\n"),
    ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
]
mode = sys.argv[1]
if mode == 'c1':
    edit('docs/features/favorites.md', fav_c1)
else:
    # Items 2 (dates), 3 (directory's authority), 5 (the tie)
    edit('docs/features/favorites.md', [
        ("held under the user's lock** (`FAVORITES_LIMIT_REACHED`, S9). *Why:* the list is answered whole; two saves at 199 would otherwise both pass the count. #121.",
         "held under the user's lock** (`FAVORITES_LIMIT_REACHED`, S9). *Why:* the list is answered whole; two saves at 199 would otherwise both pass the count. 2026-10-25, #121."),
        ("so a saved space at 200 still answers 204. #121.", "so a saved space at 200 still answers 204. 2026-10-25, #121."),
        ("a copy would drift. #121.", "a copy would drift. 2026-10-25, #121."),
        ("no one else's record. #121.", "no one else's record. 2026-10-25, #121."),
        ("so the user can remove it (C7). #121.", "so the user can remove it (C7). 2026-10-25, #121."),
        ("newest saved first, then by space id", "newest saved first, then the higher space id first"),
    ])
    edit('docs/api/api-contract.md', [
        ("(§5, *Favourites*; #121)", "(§5, *Favourites*; 2026-10-25, #121)"),
        ("it is not audited. Built #121.", "it is not audited. Built 2026-10-25, #121."),
        ("past the user's 200, #121)", "past the user's 200, 2026-10-25, #121)"),
        ("the newest saved first, then by space id.", "the newest saved first, then the higher space id first."),
        ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
    ])
    edit('docs/backend/conventions.md', [
        ("answers as its cards, #121)", "answers as its cards, 2026-10-25, #121)"),
        ("`favorites` never reads live status. #121.", "`favorites` never reads live status. 2026-10-25, #121."),
        ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
    ])
    edit('docs/features/directory.md', [
        ("a space's public page and its live status. Its endpoints are owned by the [API contract](../api/api-contract.md#directory-public);",
         "a space's public page and its live status; and a signed-in user's favourites as its cards. Its endpoints are owned by the [API contract](../api/api-contract.md#directory-public) and [its favourites](../api/api-contract.md#favourites);"),
        ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
    ])
print('ok', mode)

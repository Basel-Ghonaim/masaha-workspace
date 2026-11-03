"""Commit 5's documents: directory.md, favorites.md, users.md, architecture §2, overview."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\docs'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times: {old[:70]}')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


D = 'features\\directory.md'
edit(D, "On the web, the directory's list, its filters and near me, its map, and a space's page are built.",
     "On the web, the directory's list, its filters and near me, its map, a space's page, and the account's favourites are built.")
edit(D, """- On the site, shows a space's page at `/spaces/:slug`: its prices per audience, its hours with today, its amenities, its description, its place on a map with directions, its contacts, and each group's freshness; an unverified space's notice offers the platform's contact.

The favourites' screen is not built; the page's announcements""", """- On the site, shows a space's page at `/spaces/:slug`: its prices per audience, its hours with today, its amenities, its description, its place on a map with directions, its contacts, and each group's freshness; an unverified space's notice offers the platform's contact.
- On the site's «المفضّلة», shows a signed-in user's favourites as its cards, newest saved first or nearest first, and the spaces that left by their names.

The page's announcements""")
edit(D, "- **A signed-in user,** through the API: `GET /me/favorites`; on the site, the hearts read from it which spaces are saved (2026-10-28, #PRNUM).",
     "- **A signed-in user,** through the API: `GET /me/favorites`; on the site, the hearts read from it which spaces are saved, and «المفضّلة» (`/me/favorites`) lists them (2026-10-28, #PRNUM).")
edit(D, """**Home's spaces on the web.**""", """**The favourites on the web** (`FavoritesView`, composed by `pages/site/account/FavoritesPage.tsx` in the account's layout, signed-in only). «المفضّلة» says what it lists, then the count («مساحتان محفوظتان», «3 saved spaces») with «الأقرب إليّ» in a row and near me's state line — the Directory's store, button and line; «اختر منطقتك» leads to the Directory, and «حدّد موقعي على الخريطة» starts the pick and opens its map. It reads `GET /me/favorites` whole under `['me', 'favorites', {}]`, newest saved first, or, while near me sorts by distance, with `sort=distance` and the point in the `Masaha-Near` header under `['me', 'favorites', { near }]`, nearest first with each card's distance; clearing near me drops that answer too. The listed spaces are the directory's cards in a grid (one column, two from 768 px, three from 1280 px), each with the page's heart, pressed; then the spaces that left, each a muted card with its name as text, «لم تعد هذه المساحة معروضة في الدليل» and the page's «إزالة». Loading shows three skeleton cards; a failure says so with its reference and «إعادة المحاولة»; none saved says «لم تحفظ أي مساحة بعد» with «تصفّح المساحات»; while the order changes the cards shown stay, the section marked busy. A row removed while its action holds the focus hands it to the next row's «إزالة», else the first card's heart, else the count.

**Home's spaces on the web.**""")
edit(D, """- **The hearts read the saved spaces from the user's favourites, the directory's own read** (S13):""", """- **«المفضّلة» is the directory's screen, its cards the directory's** (S1, A3 not taken): the favourites are read from this capability's route and drawn as its cards; `favorites` sets the heart and «إزالة» in its slots. Near me is the Directory's, in memory, never in the address (S8). 2026-10-28, #PRNUM.
- **A space that left is a muted card with its name, its line and «إزالة» with «تراجع»** (C7, DI-58); **the focus after «إزالة» goes to the next row, else the first heart, else the count** (DI-52). 2026-10-28, #PRNUM.
- **The hearts read the saved spaces from the user's favourites, the directory's own read** (S13):""")
edit(D, "the saved spaces' ids in `hooks/favorites/useFavoriteIds.ts`",
     "the saved spaces' ids in `hooks/favorites/useFavoriteIds.ts` and «المفضّلة»'s view and its focus after a removal in `hooks/favorites/` (`FavoritesView` and the card of a space that left in `components/favorites/`, exported `FavoritesView`, mounted by `pages/site/account/`)")
edit(D, """- 2026-10-28, #PRNUM — the cards' and the page's actions, told whether the user saved the space; the page's report slot.""",
     """- 2026-10-28, #PRNUM — the cards' and the page's actions, told whether the user saved the space; the page's report slot.
- 2026-10-28, #PRNUM — «المفضّلة»: the user's favourites as cards, newest saved first or nearest first, and the spaces that left with «إزالة».""")

F = 'features\\favorites.md'
edit(F, "The API is built; on the web, the heart on the site's cards and on a space's page.",
     "The API is built; on the web, the heart on the site's cards and on a space's page, and «إزالة» in the account's favourites.")
edit(F, "the heart's save and removal, and a guest's held favourite.",
     "the heart's save and removal, «إزالة» of a space that left, and a guest's held favourite.")
edit(F, "a guest's press asks them to sign in first (2026-10-28, #PRNUM). The account's favourites are not built.",
     "a guest's press asks them to sign in first; in the account's «المفضّلة», the [directory](directory.md)'s screen, the hearts and «إزالة» of a space that left (2026-10-28, #PRNUM).")
edit(F, """**The list** (`directory`).""", """**«إزالة» on the web** (`RemoveFavorite`, set by the account's «المفضّلة» on each space that left the directory). Named «إزالة {name} من المفضّلة», it removes the space once and says «أُزيلت من المفضّلة» with the name and «تراجع», which saves it again; it holds, not disabled, while it is sent, so the focus stays on it until its row leaves.

**The list** (`directory`).""")
edit(F, "(`FavoriteButton`, `ResumeFavorite`), set by `pages/site/public/` (the Directory's, Home's and a space's page, through `useHeart`)",
     "(`FavoriteButton`, `RemoveFavorite`, `ResumeFavorite`), set by `pages/site/public/` (the Directory's, Home's and a space's page, through `useHeart`) and `pages/site/account/FavoritesPage.tsx`")
edit(F, """- 2026-10-28, #PRNUM — the heart on the site's cards and beside a space's name: optimistic, «تراجع» and «إعادة المحاولة» in its toasts; a guest asked to sign in, the favourite held in memory and saved on return.""",
     """- 2026-10-28, #PRNUM — the heart on the site's cards and beside a space's name: optimistic, «تراجع» and «إعادة المحاولة» in its toasts; a guest asked to sign in, the favourite held in memory and saved on return.
- 2026-10-28, #PRNUM — «إزالة» of a space that left, in the account's «المفضّلة», with «تراجع».""")

U = 'features\\users.md'
edit(U, "On the site it links the account's pages the shell passes — «بلاغاتي» — after the name (P4);",
     "On the site it links the account's pages the shell passes — «المفضّلة» and «بلاغاتي» — after the name (P4);")
edit(U, "- 2026-10-28, #PRNUM — the site's account menu and its phone section link «بلاغاتي».",
     "- 2026-10-28, #PRNUM — the site's account menu and its phone section link «المفضّلة» and «بلاغاتي».")

A = 'frontend\\architecture.md'
edit(A, "`AccountLayout`, inside `SiteLayout`, with «بلاغاتي» (2026-10-28, #PRNUM).",
     "`AccountLayout`, inside `SiteLayout`, with «المفضّلة» and «بلاغاتي» (2026-10-28, #PRNUM).")
edit(A, "with «بلاغاتي», the user's reports of [data-reports](../features/data-reports.md), signed-in only (2026-10-28, #PRNUM);",
     "with «المفضّلة», the user's favourites of [directory](../features/directory.md) with [favorites](../features/favorites.md)' heart and «إزالة», and «بلاغاتي», the user's reports of [data-reports](../features/data-reports.md), each signed-in only (2026-10-28, #PRNUM);")

O = 'project\\overview.md'
edit(O, "read whole as the directory's cards, nearest first when the device's location is sent.",
     "read whole as the directory's cards, nearest first when the device's location is sent; on the site, the heart on the cards and on a space's page, and the account's «المفضّلة».")
print('ok')

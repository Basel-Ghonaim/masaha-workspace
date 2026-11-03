"""Commit 4's documents: favorites.md, directory.md, architecture §7, finding 168."""
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


F = 'features\\favorites.md'
edit(F, "**Last Updated:** 2026-10-26 · **Owner:** Basel Ghoneim\n> **Authority:** The `favorites` capability",
     "**Last Updated:** 2026-10-28 · **Owner:** Basel Ghoneim\n> **Authority:** The `favorites` capability")
edit(F, "The API is built; no screen yet.",
     "The API is built; on the web, the heart on the site's cards and on a space's page.")
edit(F, "> **Scope:** the API module `favorites` (L2); `@masaha/shared/favorites`.",
     "> **Scope:** the API module `favorites` (L2); `@masaha/shared/favorites`; the web feature `features/favorites`, any page group: the heart's save and removal, and a guest's held favourite.")
edit(F, "the list, `GET /me/favorites`, is the [directory](directory.md)'s. The space page's heart and the account's favourites are not built.",
     "the list, `GET /me/favorites`, is the [directory](directory.md)'s. On the site, the heart on the Directory's and Home's cards and beside a space's name; a guest's press asks them to sign in first (2026-10-28, #PRNUM). The account's favourites are not built.")
edit(F, """**The list** (`directory`).""", """**The heart on the web** (`FavoriteButton`, set by the site's Directory, Home and space pages in the directory's slots: over a card's cover, beside the card's link and never inside it, and beside the page's name). A toggle, the layer's icon button (44 × 44 on a coarse pointer), named by what it does — «حفظ {name} في المفضّلة» or «إزالة {name} من المفضّلة» — and pressed (`aria-pressed`, the heart filled) while the space is saved; whether it is saved is the directory's favourites, read once per signed-in visit. Pressed by a signed-in user, it flips at once and holds while its write is pending; the save or the removal is sent once, with no key. Done, the toast says «أُضيفت إلى المفضّلة» or «أُزيلت من المفضّلة» with the space's name under it and «تراجع», which sends the inverse once; the user's scope is read again, and the favourites then say the truth. Failed, the heart goes back and the toast says «تعذّر حفظ {name} في المفضّلة» or «تعذّرت إزالة {name} من المفضّلة» with «إعادة المحاولة»; a full list says `FAVORITES_LIMIT_REACHED`'s line with «إدارة المفضّلة», and a space gone «لم تعد هذه المساحة في الدليل.». A guest's press holds the favourite in memory and the page asks them to sign in, «سجّل الدخول لحفظ المساحات في المفضّلة», with «إنشاء حساب» and «تسجيل الدخول», each carrying the page as the one to return to; once they are back signed in, the site's shell saves it once and says «حُفظت {name} في المفضّلة» (a failure with «إعادة المحاولة»). Closing the sign-in lets the held favourite go.

**The list** (`directory`).""")
edit(F, """## Code map
""", """### Web decisions

- **The hearts read the saved spaces from the directory's favourites; the writes are `favorites`', which read the whole `['me']` scope again** (S13). *Why:* the only read that knows a favourite is `GET /me/favorites`, the directory's; a heart's write invalidates the scope that list sits in, as architecture §7 allows a write whose screen shows another capability's view. *Cost:* one request per signed-in visit to a page with cards, none for a guest. 2026-10-28, #PRNUM.
- **The heart is optimistic, and the only one** (architecture §7): pressed at once, held while its write is pending, put back on a failure; the favourites read again are the truth. 2026-10-28, #PRNUM.
- **One way for every heart: «تراجع» in the toast, a failure said with «إعادة المحاولة»** (DI-49). *Why:* the page's heart assumed success and skipped the undo; a heart pressed by mistake is undone where it is said. The undo runs outside the heart, so it still works once the heart has left the page. 2026-10-28, #PRNUM.
- **«المفضّلة», with the shadda, everywhere** (DI-50). 2026-10-28, #PRNUM.
- **The heart is the layer's icon button: 44 × 44 on a coarse pointer** (DI-51). 2026-10-28, #PRNUM.
- **A guest's favourite waits in memory, never in the address, and is saved on return by the site's shell** (S14, DI-61): a link carrying it would let a crafted link save a space for a signed-in user; closing the sign-in lets it go. *Cost:* a reload, or a recovery by email, loses it ([finding 168](../architecture/findings/168-a-guests-intent-does-not-survive-a-password-recovery.md)). 2026-10-28, #PRNUM.
- **Sent once, with no key** (S4): a save or a removal is idempotent by design, and a lost answer is retried from its toast. 2026-10-28, #PRNUM.

## Code map
""")
edit(F, """- `packages/shared/src/favorites/` — the ceiling.""", """- `packages/shared/src/favorites/` — the ceiling.
- **Web:** `apps/web/src/features/favorites/`, entry `index.ts` (`FavoriteButton`, `ResumeFavorite`), set by `pages/site/public/` (the Directory's, Home's and a space's page, through `useHeart`) and mounted by `pages/site/shell/SiteLayout.tsx`: the save and the removal in `repository/`; the write, its toasts and its read of the scope in `hooks/favoriteWrite.ts` and `components/toast/`; the heart's view in `hooks/toggle/`; a guest's held favourite in `hooks/intent/`, saved on return by `hooks/resume/`. Words: the catalogue's `favorites` section.""")
edit(F, """## Open findings

None.""", """## Open findings

- [168. A guest's intent does not survive a password recovery](../architecture/findings/168-a-guests-intent-does-not-survive-a-password-recovery.md) — the favourite held for a guest is lost by a reload or a recovery by email.""")
edit(F, """- #123 — the save reads the listing before it takes the user's lock (#121's review); a saved space that left, saved again, is tested.""", """- #123 — the save reads the listing before it takes the user's lock (#121's review); a saved space that left, saved again, is tested.

### Web history

- 2026-10-28, #PRNUM — the heart on the site's cards and beside a space's name: optimistic, «تراجع» and «إعادة المحاولة» in its toasts; a guest asked to sign in, the favourite held in memory and saved on return.""")

D = 'features\\directory.md'
edit(D, "**Last Updated:** 2026-10-26 · **Owner:** Basel Ghoneim\n> **Authority:** The `directory` capability",
     "**Last Updated:** 2026-10-28 · **Owner:** Basel Ghoneim\n> **Authority:** The `directory` capability")
edit(D, "The favourites' screen and the space page's heart are not built; the page's announcements",
     "The favourites' screen is not built; the page's announcements")
edit(D, "- **A signed-in user,** through the API: `GET /me/favorites`.",
     "- **A signed-in user,** through the API: `GET /me/favorites`; on the site, the hearts read from it which spaces are saved (2026-10-28, #PRNUM).")
edit(D, """**Home's spaces on the web.**""", """**The cards' and the page's actions on the web.** A page sets an action on each card (`DirectorySlots.cardAction`, also `HomeSpaces`') and beside a space's name (`SpaceDetails`' `heart`); the site sets [favorites](favorites.md)' heart there. Each is handed the space's id, its name as shown, and whether the user saved it: with a session, the user's favourites are read once, newest saved first, under `['me', 'favorites', {}]`, and their ids, listed or not, say which; for a guest nothing is read and none is saved. A card's action stands over its cover's corner, beside the card's link, never inside it, so the card stays one link and the action one button. The page's report is `SpaceDetails`' `report`, last in the main column, handed the space's slug, name and verification.

**Home's spaces on the web.**""")
edit(D, """- **A space's page has one order at every width; from 1024 px the status and the contacts move to an aside** (U8).""", """- **The hearts read the saved spaces from the user's favourites, the directory's own read** (S13): the ids of the whole list, newest saved first, under the session's scope, read only with a session; a favourite saved or removed reads the scope again. *Why:* `GET /me/favorites` is the only read that knows a favourite, and it is this capability's. 2026-10-28, #PRNUM.
- **A space's page has one order at every width; from 1024 px the status and the contacts move to an aside** (U8).""")
edit(D, "the card in `components/card/`, the results",
     "the card in `components/card/` (its action beside the link), the saved spaces' ids in `hooks/favorites/useFavoriteIds.ts` (the request's type in `types/FavoritesRequest.ts`, the slots' `ActionSpace` in `types/DirectorySlots.ts`), the results")
edit(D, """- #111 — the live status's badge and words, for About's legend.""", """- #111 — the live status's badge and words, for About's legend.
- 2026-10-28, #PRNUM — the cards' and the page's actions, told whether the user saved the space; the page's report slot.""")

A = 'frontend\\architecture.md'
edit(A, "A package saved with a shift gone meanwhile invalidates the whole `['space', spaceId]` scope, since the shifts are `spaces`'.",
     "A package saved with a shift gone meanwhile invalidates the whole `['space', spaceId]` scope, since the shifts are `spaces`'. `favorites`' save and removal invalidate the whole `['me']` scope, whose favourites list is `directory`'s (2026-10-28, #PRNUM).")

N = 'architecture\\findings\\168-a-guests-intent-does-not-survive-a-password-recovery.md'
edit(N, "— the report of wrong information on a space's page (#PRNUM) —",
     "— the report of wrong information on a space's page, or the favourite's heart on a card or a page (#PRNUM) —")
edit(N, "so the held action runs once the session is established.",
     "so the held action runs once the session is established: the report's dialog opens, and the favourite is saved and said.")
print('ok')

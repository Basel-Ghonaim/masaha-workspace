"""R3-F1's documents and finding 187."""
import io

APP = 'C:/dev/masaha/app/'


def edit(path, pairs):
    p = APP + path
    s = io.open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70])
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf8', newline='').write(s)
    print('ok', path)


edit('docs/features/favorites.md', [
    ("it removes the space once and says «أُزيلت من المفضّلة» with the name and «تراجع», which saves it again; it holds,",
     "it removes the space once and says «أُزيلت {name} من المفضّلة. لا يمكن حفظها من جديد ما دامت خارج الدليل.», with no «تراجع»: the API saves no space out of the directory (404), so an undo could never work (DI-58, the owner's word, #129's review; [finding 187](../architecture/findings/187-a-favourite-just-removed-cannot-be-saved-again-for-an-undo.md)); it holds,"),
    ("- 2026-10-28, #129 — «إزالة» of a space that left, in the account's «المفضّلة», with «تراجع».",
     "- 2026-10-28, #129 — «إزالة» of a space that left, in the account's «المفضّلة», said with no «تراجع» (it cannot be saved meanwhile)."),
])
edit('docs/features/directory.md', [
    ("- **A space that left is a muted card with its name, its line and «إزالة» with «تراجع»** (C7, DI-58);",
     "- **A space that left is a muted card with its name, its line and «إزالة», with no «تراجع»** (C7, DI-58: the API saves no space out of the directory, so the undo is not offered — the owner's decision on #129's review);"),
])
p = APP + 'docs/architecture/findings/187-a-favourite-just-removed-cannot-be-saved-again-for-an-undo.md'
io.open(p, 'w', encoding='utf8', newline='').write(
    "# 187. A favourite just removed cannot be saved again for an undo\n\n"
    "**Status:** Open · **Date:** 2026-10-28\n\n"
    "**Evidence:** «المفضّلة» offers «إزالة» on a saved space that left the directory (C7, DI-58). `POST "
    "/me/favorites/:spaceId` answers `not_found` (404) for a space that is not publicly listed — unknown, hidden, "
    "deleted, or in an area not listed — which is what such a space is, so a «تراجع» after its removal could never "
    "save it again. #129's review found the undo offered (R3-F1); by the owner's decision (DI-58, option (a)) the "
    "removal now says the space cannot be saved again while it is out of the directory, and offers no undo. The "
    "user who removes it by mistake loses it until the space is listed again.\n\n"
    "**Resolves when:** the API lets a user save again, for a short while, a favourite they have just removed, "
    "whatever the space's listing, and «إزالة» offers «تراجع» again; or the owner accepts the removal without an "
    "undo.\n")
print('ok 187')

"""C11: findings 220 and 221, and their index lines (append-only, in order)."""
import os

F = r"C:\dev\masaha\app-design-lane-c\docs\architecture\findings"

F220 = "220-the-admins-top-bar-still-offers-to-hide-and-delete-a-space-found-deleted.md"
F221 = "221-the-readmes-screenshots-show-sea.md"

TEXT_220 = """# 220. The admin's top bar still offers to hide and delete a space found deleted

**Status:** Open · **Date:** 2026-11-12

**Evidence:** seen in #143's fix round, in its run in Chrome: the admin's editor of an unverified space open in one tab, the space deleted from a second tab, then «حفظ» in the first. The page turns to the 404, «الصفحة غير موجودة», and the top bar above it still offers «إخفاء عن الزوار» and «حذف المساحة» (below 768 px, its «إجراءات الصفحة» menu) for the space just found deleted. `SpaceEditorActions` (`apps/web/src/features/spaces/components/editor/SpaceEditorActions.tsx`, in `SpaceEditPage`'s top bar) draws what `useSpaceEditorActions` (`hooks/editor/useSpaceEditorActions.ts`) returns, and that hook returns the actions whenever the space's query (`useSpaceQuery('admin', spaceId)`) holds data: it returns none only while `query.data` is `undefined`. TanStack Query keeps a query's last data when a later read fails, so once the space answers 404 the query holds the error and the space read before it. The editor (`useSpaceEditor`) and the page's title (`useSpaceName`) read that 404 as the space being gone, whatever was read before; the actions' hook does not.

**Resolves when:** the top bar's actions read a space found deleted as the editor and the title do, offering nothing once the space's read answers 404, with a test that draws them, answers 404 to a later read, and finds no action.
"""

TEXT_221 = """# 221. The README's screenshots show Sea

**Status:** Open · **Date:** 2026-11-12

**Evidence:** the root `README.md` pictures the site with the screenshots in `docs/assets/readme/` (its `*.webp` images and `masaha.gif`), taken under *Sea*, the petrol teal, and the text wordmark. The site now draws ink + berry and its logo ([ADR 0019](../decisions/0019-ink-and-spark-brand.md)), so the README shows a look the site no longer has.

**Resolves when:** the screenshots and the GIF are re-shot under ink + berry, in a README task.
"""

for name, text in ((F220, TEXT_220), (F221, TEXT_221)):
    path = os.path.join(F, name)
    assert not os.path.exists(path), path
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("wrote", name)

index = os.path.join(F, "README.md")
with open(index, encoding="utf-8", newline="") as f:
    s = f.read()
last = "- [219. A toast's removal timer can outlive its test file's jsdom](219-a-toasts-removal-timer-can-outlive-its-test-files-jsdom.md)\n"
assert s.count(last) == 1 and s.count("220.") == 0 and s.count("221.") == 0
s = s.replace(
    last,
    last
    + "- [220. The admin's top bar still offers to hide and delete a space found deleted](" + F220 + ")\n"
    + "- [221. The README's screenshots show Sea](" + F221 + ")\n",
)
with open(index, "w", encoding="utf-8", newline="") as f:
    f.write(s)
print("indexed 220 and 221 under Open")

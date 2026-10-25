def edit(path, old, new):
    t=open(path,encoding='utf-8',newline='').read(); assert t.count(old)==1,(path,old[:50],t.count(old)); open(path,'w',encoding='utf-8',newline='').write(t.replace(old,new))
P='docs/api/api-contract.md'
edit(P, "\n### Internal\n", """
### Favourites

A signed-in user keeps the listed spaces they want to find again, at most 200 (`FAVORITES_MAX`, `@masaha/shared/favorites`). A favourite is the user's own choice: it is not audited. Built #PRNUM.

#### `POST /me/favorites/:spaceId` · 👤
- **204**, no body: the space is saved, dated now. A space already saved answers 204 and writes nothing, even at the ceiling; two saves at once make one (the user's lock, the primary key behind it).
- **Errors**, each writing nothing: `unauthorized` (401) without a signed-in user; `not_found` (404) for a space that is not publicly listed — unknown, hidden, deleted, or in an area not listed; `conflict` (409) `FAVORITES_LIMIT_REACHED` for a new one past 200, held under the user's lock, so two saves at 199 make one.

#### `DELETE /me/favorites/:spaceId` · 👤
- **204**, no body, whether the space was saved or not, listed or not; only the caller's own favourite is removed.
- **Errors:** `unauthorized` (401) without a signed-in user; `not_found` (404) for a malformed id.

### Internal
""")
edit(P, "`REPORT_ALREADY_DECIDED` (409: a decided report decided again, otherwise than it was, 2026-10-25, #120).",
 "`REPORT_ALREADY_DECIDED` (409: a decided report decided again, otherwise than it was, 2026-10-25, #120) · `FAVORITES_LIMIT_REACHED` (409: a new favourite past the user's 200, #PRNUM).")

The plan is approved. Build it, with the answers below.

## Your decisions D1–D9 — approved, with two refinements
- **D1–D6, D8, D9 — approved as written.**
- **D6 refinement — separators:** before the phone rule runs, strip the separators people type: spaces,
  dashes, dots and parentheses (`059-123 4567`, `(08) 282 1234`). Nothing else is relaxed. One unit
  case per separator kind.
- **D7 refinement — Facebook profile links keep their id:** a `facebook.com/profile.php?id=<digits>`
  URL keeps its `id` (stored as `https://www.facebook.com/profile.php?id=<digits>`); every other query
  and every fragment is still dropped. Without it, a page that has no username loses its address. One
  unit case for it, and one for an ordinary URL's query being dropped.

## The owner's answers in your session
Recorded as you list them (A1: duplicates are 422 on the right row field; `stale=true` includes
missing groups; a shift in use is 409 with no code; fold findings 31, 41 and 36).

## Parallel work — one shared line to watch
Worker B is editing `docs/features/lookups.md` right now (the amenities tab). Your one clause on its
line 12 ("which amenities are active") may conflict: keep it to that clause, and if GitHub shows a
conflict when you open the PR, rebase then and keep both sides.

Everything else stands: the shapes, the server design and its write order, the migration (created
once, read, then applied; its effect on existing rows proven by hand and recorded in the PR), the six
commits, the tests with the breaks you named, the Review Focus and the lanes.

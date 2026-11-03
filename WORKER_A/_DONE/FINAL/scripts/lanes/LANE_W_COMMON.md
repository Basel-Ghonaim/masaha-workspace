# The web lanes (W1–W4) — what they add to LANE_COMMON.md

- **Your base** is `feat/final` at the sha your lane file names: the foundation U0 (the grouped navigation, the skip
  link and focus rule in every shell, the account in the drawer, **every route of the screens still to come already
  made**, each new page a stub file that renders `PageHeader` — you replace its body; the copy's new sections
  `overview`, `finance`, `audit` registered empty — you fill yours), and whatever lanes the lead has joined by then
  (your lane file says which).
- **Never edit the route tables or the navigation** (`pages/dashboard/{routes.tsx,navigation.ts}`,
  `pages/site/{routes.tsx,navigation.ts}`), the copy's `index.ts`/`shape.ts`, or another lane's files (§9.3). A route
  or a navigation change you find you need → record it and tell the lead in your reply.
- **Dependencies on other lanes.** Your lane file lists, for each of your commits, the other lanes' commits it needs.
  Build **first the commits whose needs are already in your base**, in §9.1's order among themselves. When every
  commit left waits on something not in your base, end your turn with a **HAND-OVER** reply naming the commits made
  and those waiting (and what each waits for). The lead joins the lanes you wait on into `feat/final` and continues
  you with a message giving the new `feat/final` sha: then `git rebase <sha>` your branch onto it (in your worktree;
  a conflict in a file of yours → resolve keeping both sides' intent; record it), `npm run build -w @masaha/shared`,
  and continue. The order of your commits may then differ from §9.1's; that is expected (the lead records it).
- **A shared type you need** comes from the API lanes' commits (`packages/shared`): code against it only once it is in
  your base; never write it yourself.
- **The layer** (`shared/design-system`), `shared/lists`, `shared/lib` are lane L's: call them, never change them. A
  layer gap you meet → record it; tell the lead.
- **Lane-wide checks before DONE:** lint, typecheck, `test:unit -w @masaha/web`, `test:component -w @masaha/web`
  (whole), `npm run check:classes`, `npm run check:links` (if you touched docs) — through the grant.

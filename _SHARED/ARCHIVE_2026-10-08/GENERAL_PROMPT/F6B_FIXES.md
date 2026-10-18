F-6b — review fixes for PR #30 (the ONE list)

One independent review ran against effe45a; the owner's analyst verified the findings in the code. CI was green on effe45a. Apply everything below on this same branch and PR. Don't merge.

## Owner decisions

O1 — The four lines not drawn in a design are approved as they are in the PR: Main navigation («التنقّل الرئيسي»), Menu, Close menu, Dark theme / Light theme.
O2 — On a route error, the header keeps marking that route's link as current. Keep it: `aria-current` says where the URL is, the 404 already marks none, and unmarking would couple the shell to the boundary's state. The PR already records it.

## Should-fix

S1 — The root error test proves less than its title. `RootLayout.component.test.tsx`: the throwing route is a plain page and the tree has no shell, so "no banner" proves nothing; and nothing covers `router.tsx`'s `ErrorBoundary: RootError` (removing it would pass every test).
- Fix: make the failing route a layout (a `<header>` and an `<Outlet/>`) that throws, or mount `siteRoutes` with `SiteLayout` mocked to throw. Assert the general error's h1 and that no banner is present. Add a test that the app's real route tree (from `router.tsx`, or its exported routes) renders `RootError` when the site shell fails.

S2 — The phone menu closes only through the links' `onClick`. Browser or Android back/forward while the sheet is open changes the page under it, and the sheet stays open.
- Fix: close the sheet whenever the location changes (`useLocation()`), and drop the per-link `onClick` handlers. Keep the existing "closes when a link is chosen" test, and add one: the sheet closes when the history moves (a memory router navigating back).

## Nits (fix all; each is small)

N1 — `toggles.tsx`: `otherLanguage` assumes exactly two languages. Make that explicit and checked: a type-level assertion (or a comment plus a unit test) that the registered languages are exactly two, so adding a third forces a real switcher.
N2 — `navigation.ts`: `'contact'` is written twice. Write the path from the anchor constant.
N3 — `SiteMenu.tsx`: the dialog's accessible name is the wordmark, so a screen reader hears "Masaha, dialog". Keep the drawn wordmark, and name the dialog with the menu's own label (`copy.site.menu`), for example through a visually hidden `SheetTitle` or `aria-label`.
N4 — `architecture.md`: "Built so far: `app/`" sits next to the line listing `dashboardRoutes` in `router.tsx`. Say `app/` (without `dashboardRoutes`).
N5 — `foundation.md`: "split in its plan steps (F-6a; 2026-10-03 for the rest)" is hard to parse. Follow F-5's form: "split in its plan step (date)", with F-6a's own date if it has one.

## History and reporting (the owner's rules)

- **Fold every fix into the commit it corrects** (no separate fix commits): `git commit --fixup=<sha>` for each, then `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash origin/main`. S1 and S2 fold into their feature commits, N4 into the architecture commit, N5 into the plans commit. Check each rewritten commit on its own (`git rebase --exec "npm run lint && npm run typecheck && npm run test:unit" origin/main`), then `git push --force-with-lease` on this branch only.
- **Worker A's PR #29 will probably merge second,** so you likely don't need to rebase onto it. If `main` moves before you finish, rebase and keep both sides.
- **Report only once CI is green on the pushed head** (`gh pr checks 30`).
- **Update the PR description** to the final state, and add ONE "Review fixes" comment: the reviewed head `effe45a`, the new head, and a table of each id (O1, O2, S1, S2, N1–N5), its severity and the commit it was folded into.
- Stop and report.

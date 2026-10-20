# USERS — PR 1 (`feat/admin-users`) — the executor's report

Executor: Claude Code (Opus 5.5), 2026-10-19. Plan: `2_PLAN.md` (approved; its note binds). Prompt: `3_EXEC_PROMPT.md`.

## 1. First checks (§13)

- `gh pr view 91 --json state` → `{"headRefName":"feat/admin-owner-links","mergedAt":"2026-10-19T11:46:09Z","state":"MERGED"}`.
- `git status` → `nothing to commit, working tree clean`, on `main`; `git fetch origin`; `git pull --ff-only` → `Already up to date.`; `origin/main` = `a8c39bda` (Merge pull request #91).
- `gh pr list --state merged --head feat/admin-owner-links --json number,mergeCommit` → `[{"mergeCommit":{"oid":"a8c39bda…"},"number":91}]`.
- `git diff --name-status 02cc70ae origin/main` → 24 files, all PR 3's fix round (`4_REPORT_PR3.md` FR1). The code files this plan names, and how they changed:
  - `hooks/link/useLinkOwnerDialog.ts` — the chosen space is now read from the latest options (`spaces.options.find(id) ?? chosen`). Compatible: commit 4's `atDesk` rides on the same options.
  - `hooks/link/useLinkOwnerDialog.component.test.tsx` — one new test; the `validation` expectation is now «That account no longer exists.» Compatible.
  - `hooks/owner-actions/useOwnerActions.ts` — its dialog type moved to `types/OwnerDialog.ts` (new). Compatible: commit 4 only adds `role` and `deskIds` to the link target.
  - `components/link/LinkOwnerDialog.tsx`, `components/unlink/UnlinkOwnerDialog.tsx` — an optional `fallbackFocus` prop. Compatible (optional; this plan does not need it).
  - `shared/copy/{english,arabic}/spaceLinks.ts` — `link.refusals.validation` lost «— choose another» / «— اختر غيره». Compatible. (§11's review focus quotes the old wording; the line is now «لم يعد هذا الحساب موجودًا.»)
  - `docs/architecture/findings/94-…`, `95-…` added; `README.md`, `space-links.md`, `users.md`, `spaces.md` edited. Documents only.
  - No `packages/shared` change, so no shared build.
  → No difference the plan does not cover; no stop.
- Finding `<n>`: **not used** — the approval note takes alternative B (no finding). For reference, the latest index ends at 95.
- §13.5 checks:
  - `DropdownMenuItem` spreads its props onto Radix's `Item`, so `asChild` is forwarded → the lead item uses `asChild` around a `Link` (no fallback).
  - `shared/session/model.ts`: `{ status: 'authenticated'; user: SessionUser; accessToken: string }` → as §13 reads it.
  - `packages/shared/src/space-links/requests.ts`: `adminUsersQuerySchema = paginationQuerySchema.extend({ … role: z.enum(USER_ROLE_FILTERS).optional(), … })` → as §13 reads it.
  - `DataTable.component.test.tsx`'s `matchMedia` stub reads any `(min-width: Npx)` → kept.

Branch: `git switch --no-track -c feat/admin-users origin/main` → `Switched to a new branch 'feat/admin-users'` at `a8c39bda`.

## 2. Commits

### Commit 1 — `c7d089bc` `feat(design-system): keep a table's cards to lg` (47 chars)
- Red before the code: `npx vitest run --project component src/shared/design-system/components/data/DataTable` → `Tests  1 failed | 10 passed (11)` («keeps each row a card until 1024px when asked…»: `expect(element).not.toBeInTheDocument()` — the table drawn at 768).
- The spaces list (the approval note's alternative B): its tests used 1280 and 390 only, none assumed the table at 768. Added «keeps a card per space until 1024 px, as it has more than five columns» (768): red before `cardsBelow="lg"` → `Tests  1 failed | 23 skipped (24)` (`expect(element).not.toBeInTheDocument()`); the describe «from 768 px» renamed «from 1024 px» (its tests run at 1280).
- Green after: `npx vitest run --project component src/features/space-links/components/admin-list src/shared/design-system/components/data src/features/space-links/hooks/admin-list` → `Test Files  5 passed (5)` / `Tests  63 passed (63)`.
- `npm run lint` → `> eslint .`, exit 0; `npm run typecheck` → `tsc -b`, exit 0; prettier on the changed code → `All matched files use Prettier code style!`.
- Docs: foundation §12's Table + DataTable row (the plan's clause); `space-links.md` — the spaces list's layout line (a table from 1024 px, cards below it), a web decision, and the PR's web-history line (begun here, extended by later commits). No finding `<n>` (approval note).

### Commit 2 — `cb05dd12` `refactor(space-links): share the users list's core` (50 chars)
- A pure refactor: no new test; the proof is the existing tests unchanged. Green after: `npx vitest run --project component src/features/space-links/hooks/owners-list src/features/space-links/components/owners-list src/features/space-links/hooks/users-list` → `Test Files  3 passed (3)` / `Tests  9 passed (9)`; `npx vitest run --project unit src/features/space-links` → `Test Files  7 passed (7)` / `Tests  59 passed (59)`.
- Break (a refactor mistake): `useOwnersList` passes `fixedRole: undefined` → `Tests  2 failed | 5 passed (7)`, `AssertionError: expected { state: 'suspended', page: 1 } to deeply equal { state: 'suspended', page: 1, …(1) }`; restored.
- `npm run lint` → exit 0; `npm run typecheck` → `tsc -b`, no error; prettier → unchanged.
- **Departure:** a fifth file, `services/userRowView.ts` — its `lines` type narrowed to `Pick<…ownersList, 'states'>`: the core hook's `words` is the plan's `Pick`, which a parameter typed as the whole `ownersList` would refuse (commit 4 replaces the parameter anyway). `AdminUsersListWords` is exported beside `AdminUsersListView` in the hook's file for the `Pick`.

### Commit 3 — `fda7f967` (was `aba2c778`) `fix(space-links): show front desks before upgrade` (49 chars)
- Red before the code: `npx vitest run --project unit src/features/space-links/services/userRowView` → `Tests  1 failed | 3 passed (4)` (`AssertionError: expected undefined to deeply equal [ { text: 'Olive Desk' }, …(1) ]`); `npx vitest run --project component src/features/space-links/components/add-owner` → 2 failed (`TestingLibraryElementError: Unable to find an element with the text: Front desk, which matches selector 'dt'`).
- Green after: unit `Tests  4 passed (4)`; `npx vitest run --project component src/features/space-links/components/add-owner src/features/space-links/hooks/add-owner` → `Tests  16 passed (16)`.
- Breaks: ★ the desks' row not drawn in `AddOwnerNotice` → `Tests  1 failed` (`Unable to find an element with the text: Front desk…`); desks read from `row.spaces` → `Tests  1 failed | 3 passed (4)` (`AssertionError: expected [ { text: 'Focus Hub' }, …(1) ] to deeply equal [ { text: 'Olive Desk' }, …(1) ]`). Both restored.
- `npm run lint` → exit 0; `npm run typecheck` → exit 0; prettier → `All matched files use Prettier code style!`; `npm run check:links` → `2220 links in 176 documents and 1280 source files all resolve.`
- The existing upgrade test's `getByText('None')` became two term-by-term reads (`Spaces` → None, `Front desk` → None): «None» is now the words of both rows in English.
- Folded in (`--fixup` + autosquash): `routes.component.test.tsx`'s owners-page row lacked `receptionSpaces`, so the row view's new map crashed it (`TypeError: Cannot read properties of undefined (reading 'map')`, found before commit 4); `receptionSpaces: []` added → `Tests  2 passed | 36 skipped (38)`. A file beyond §7's commit 3 list.
- Docs: finding 88 Resolved with its line, its index line moved to *Resolved*; `space-links.md` behaviour, web decision, open findings (88 removed), web history.

### The owner's note mid-work (#92, SETTINGS, merged as `eff0a3d1`)
- Run once, no test running: `docker ps` → `masaha-postgres-1 Up 3 hours (healthy)`; `cd apps/api && npx prisma migrate deploy` → `18 migrations found in prisma/migrations` / `No pending migrations to apply.`; `npx prisma generate` → `✔ Generated Prisma Client (7.10.0)`; `npm run build -w @masaha/shared` → `tsc -p tsconfig.build.json`, exit 0.
- **As it stands:** the branch is cut from `a8c39bda` (before #92), so its migrations folder lacks `20261019092820_reception_typed_prices`: `masaha_dev` did **not** gain `reception_may_type_prices`, and the client and shared `dist` are the branch's own. This matches the code the real run's API runs from. No rebase (the owner's rule: only if the PR shows DIRTY). Findings 94–97 are taken; this PR records none (the approval note dropped `<n>`).

### Commit 4 — `9e247178` `feat(space-links): add the admin's users page` (45 chars)
- Red before the code (each new test, stubbed modules where a file did not exist yet, so the red is an assertion, not an import): `usersFiltersOf` unit → 2 failed (`expected { page: 1 } to deeply equal { role: 'admin', page: 1 }`); `useUsersFilters` → `Tests  2 failed | 2 passed (4)` (`chooseRole is not a function`); `userRowView` it.each → `Tests  7 failed (7)` (the new signature); `useLinkOwnerDialog` + `LinkOwnerDialog` → `Tests  2 failed | 15 passed (17)`; `useUsersList` → 2 failed (`Error: Not built yet`); `UsersList` → `Tests  5 failed (5)`; `useUserLinkActions` → `Tests  5 failed (5)`. `UserActionsMenu` and the routes test were written after their code: their breaks below are their red.
- Green after: `npx vitest run --project component src/features/space-links src/pages` → `Test Files  30 passed (30)` / `Tests  221 passed (221)`; `npx vitest run --project unit src/features/space-links` → `Test Files  7 passed (7)` / `Tests  65 passed (65)`.
- Breaks (scratchpad `breaks.py`: make, run the focused test, restore), all red:
  | Break | Result | Error |
  |---|---|---|
  | ★ link: `user: false` on the person side | `1 failed \| 12 skipped (13)` | `AssertionError: expected [ Array(1) ] to deeply equal [ …(2) ]` |
  | ★ link dialog: `atDesk` not disabling | `1 failed \| 3 skipped (4)` | `expect(element).toHaveAttribute("aria-disabled", "true")` |
  | ★ link actions: an admin enabled | `1 failed \| 1 passed \| 3 skipped (5)` | `expected { label: 'Link to a space', …(2) } to match object { disabled: true, …(1) }` |
  | ★ link actions: the reason dropped | `1 failed \| 1 passed \| 3 skipped (5)` | same |
  | menu: `returnFocus` not passed | `1 failed \| 1 skipped (2)` | `Error: expect(element).toHaveFocus()` |
  | routes: the users route left on its placeholder | `1 failed \| 38 skipped (39)` | `Unable to find role="table" and name "Users"` |
  | row: `both` mapped to `google` | `1 failed \| 6 passed (7)` | `… to match object { role: 'Admin', …(2) }` |
  | filters: `?role=gone` kept | `1 failed \| 4 skipped (5)` | `expected { role: 'gone', page: 2 } to deeply equal { page: 2 }` |
  | filters: role dropped from the request | `1 failed \| 4 skipped (5)` | `expected { page: 1 } to deeply equal { role: 'admin', page: 1 }` |
  | filters hook: push | `1 failed \| 3 skipped (4)` | `expected 'PUSH' to be 'REPLACE'` |
  | filters hook: the page kept | `1 failed \| 3 skipped (4)` | `expected '?q=Rima&role=admin&page=3' to be '?q=Rima&role=admin'` |
  | filters hook: `fixedRole` ignored | `1 failed \| 3 skipped (4)` | `expected true to be false` |
  | users hook: role left out of the request | `1 failed \| 1 skipped (2)` | `expected { q: 'Rima', state: 'active', page: 2 } to deeply equal { …role: 'admin'… }` |
  | users hook: `selfId` always null | `1 failed \| 1 skipped (2)` | `expected [ false, false ] to deeply equal [ true, false ]` |
  | list: the desks' group not drawn | `1 failed \| 4 skipped (5)` | `expected [ 'Nour', … ] to deeply equal [ 'Nour', … ]` |
  | list: `cardsBelow` not passed | `1 failed \| 4 skipped (5)` | `expect(element).not.toBeInTheDocument()` |
  | list: the slot called for the own row | `1 failed \| 4 skipped (5)` | `Unable to find an element with the text: You` |
  | list: the role chips' `choose` not wired | `1 failed \| 4 skipped (5)` | `expected '' to be '?role=admin'` |
  | list: a chip group unnamed (axe) | **green** `1 passed \| 4 skipped (5)` | — |
  | → list: the role chip group unnamed, run against the chips test | `1 failed \| 4 skipped (5)` | `Unable to find an accessible element with the role "radiogroup" and name "Role"` |
  | → list: the role chips unlabelled (axe) | `1 failed \| 4 skipped (5)` | `Error: expect(received).toHaveNoViolations(expected)` |
  **Departure:** the plan's axe break (a chip group unnamed) cannot turn axe red: axe has no rule that a `radiogroup` be named. That naming is proven by the chips test (red above); axe's break became the role chips without labels (red).
- `npm run lint` → exit 0; `npm run typecheck` → exit 0; prettier → clean after `index.ts` was formatted; `npm run check:links` → `2224 links in 176 documents and 1293 source files all resolve.`; `npm run check:classes` → `No physical direction or arbitrary-value classes in 909 files.`
- **Departures:** files beyond §7's list — `hooks/link/usePersonChoices.ts` and `components/owner-actions/OwnerActionsMenu.component.test.tsx` (the row view's new `words`/`now` parameters), `hooks/add-owner/useAddOwnerForm.component.test.tsx` (`atDesk: false` in a `SpaceChoiceView` literal). `useUserLinkActions(row)` takes no `{ ownersLink, deletedSpacesLink }` yet: only commit 5's role item reads them, so they arrive with it (`adminOwnersSearchPath` is in `navigation.ts` here, as §7 lists). `UserCard` takes its spaces and actions as rendered nodes from `UsersList` (one place renders `UserSpaces` and «أنت»). `useAdminUsersList`'s options are a union: a fixed role with the shared words, or no fixed role with the role chips' words too.

### Commit 5 — `01346c4b` `feat(space-links): change a person's role` (41 chars)
- Red before the code: repository → `Tests  1 failed | 16 passed (17)` (`TypeError: createSpaceLinksRepository(...).changeRole is not a function`); `useRoleDialog` (stub) → 8 failed (`Error: Not built yet`); `RoleDialog` (stub) → 1 failed (`Unable to find an accessible element with the role "alertdialog"…`); `useUserLinkActions`' role tests → 5 failed (`expected undefined to match object { label: 'Change role', …(2) }`). The menu's «puts the role change first» was written after its code: its break is its red.
- Green after: `npx vitest run --project component src/features/space-links src/pages` → `Test Files  32 passed (32)` / `Tests  236 passed (236)`; unit `src/features/space-links` → `Test Files  7 passed (7)` / `Tests  66 passed (66)`.
- Breaks, all red:
  | Break | Result | Error |
  |---|---|---|
  | repository: `put` sent as `post` | `1 failed \| 16 skipped (17)` | `expected { …(19) } to match object { method: 'put', …(2) }` |
  | repository: the body changed | `1 failed \| 16 skipped (17)` | `expected { role: 'USER' } to deeply equal { role: 'ADMIN' }` |
  | ★ link actions: the role's reason dropped | `3 failed \| 7 skipped (10)` | `expected { label: 'Change role', …(3) } to match object { … }` |
  | ★ link actions: a lead dropped | `1 failed \| 2 passed \| 7 skipped (10)` | `expected undefined to deeply equal { label: 'Deleted spaces', …(1) }` |
  | ★ link actions: a receptionist enabled | `1 failed \| 2 passed \| 7 skipped (10)` | `expected { label: 'Change role', …(2) } to match object { … }` |
  | link actions: an admin held | `1 failed \| 1 passed \| 8 skipped (10)` | `expected { label: 'Change role', …(3) } to match object { … }` |
  | ★ role dialog: the lines swapped | `1 failed \| 7 skipped (8)` | `expected 'They lose the admin dashboard at once…' to be 'They get every admin power over the p…'` |
  | role dialog: the same role sent | `2 failed \| 6 skipped (8)` | `expected { role: 'USER' } to deeply equal { role: 'ADMIN' }` |
  | role dialog: the toast before the refresh (`void refresh()`) | `1 failed \| 7 skipped (8)` | `AssertionError: expected false to be true` (still busy while the admin view refetches) |
  | role dialog: `lines.refusals` removed | `3 failed \| 2 passed \| 3 skipped (8)` | `expected { kind: 'refused', …(2) } to match object { … }` |
  | role dialog: `close()` on a failure | `5 failed \| 3 skipped (8)` | `expected "vi.fn()" to not be called at all, but actually been called 1 times` |
  | RoleDialog: `AlertDialogAction` that closes on click | first run red with no error line: the break lacked its import, so it crashed — not counted; re-run with the import → `1 failed (1)` | `Error: expect(element).toHaveClass("bg-destructive")` |
  | menu: the lead not rendered | `1 failed \| 2 skipped (3)` | `expected [ …(2) ] to deeply equal [ …(3) ]` |
- `npm run lint` → exit 0; `npm run typecheck` → exit 0; prettier → clean after `useUserLinkActions.ts` was formatted; `npm run check:links` → `2224 links in 176 documents and 1298 source files all resolve.`
- Added beyond §10: «sends the user role for an admin» (the other direction's body). `useUserLinkActions` now takes `{ ownersLink, deletedSpacesLink }` (see commit 4's departure); `MenuActionItem` renders the lead as `DropdownMenuItem asChild` around a `Link` (§13.5: `asChild` forwarded). The held owner-of-deleted-spaces reason reuses `usersList.allSpacesDeleted` (finding 50's line), as the plan's `allSpacesDeleted`.

### Commit 6 — `b7a7f695` `feat(users): suspend and restore an account` (43 chars)
- Red before the code: users repository → `Tests  1 failed | 3 passed (4)` (`TypeError: repository.setSuspended is not a function`); `useSuspendDialog`, `SuspendDialog`, `useAccountActions` (stubs) → `Failed Tests 8` (`Error: Not built yet`, `Unable to find … "alertdialog"`). The `RefusalText` move: `spaces`' tests unchanged → `npx vitest run --project component src/features/spaces src/shared/forms` → `Test Files  26 passed (26)` / `Tests  242 passed (242)`.
- Green after: the three new files → `Tests  8 passed (8)`; users unit → `Tests  4 passed (4)`; the menu → `Tests  3 passed (3)` (its order expectation gained «Suspend», the planned change).
- Breaks, all red:
  | Break | Result | Error |
  |---|---|---|
  | repository: the path changed | `1 failed \| 3 skipped (4)` | `… to match object [ { method: 'put', …(2) }, …(1) ]` |
  | repository: the body changed | `1 failed \| 3 skipped (4)` | `expected [ { isSuspended: true }, …(1) ] to deeply equal [ … ]` |
  | ★ suspend dialog: the owner line not added | `1 failed \| 4 skipped (5)` | `expected [ Array(1) ] to deeply equal [ …(2) ]` |
  | ★ suspend dialog: the desk line not added | `1 failed \| 4 skipped (5)` | `expected [ Array(1) ] to deeply equal [ …(2) ]` |
  | suspend dialog: `isSuspended: false` sent | `1 failed \| 4 skipped (5)` | `expected { isSuspended: false } to deeply equal { isSuspended: true }` |
  | suspend dialog: `close()` on a failure | `3 failed \| 2 skipped (5)` | `expected "vi.fn()" to not be called at all, but actually been called 1 times` |
  | SuspendDialog: `AlertDialogAction` (imported) | `1 failed (1)` | `Error: expect(element).toHaveClass("bg-destructive")` |
  | account actions: the items swapped | `1 failed \| 1 skipped (2)` | `expected { label: 'Restore the account', …(3) } to match object { label: 'Suspend', …(2) }` |
  | account actions: a dialog asked for the restore | `1 failed \| 1 skipped (2)` | `expected 'suspend' to be null` |
  | account actions: the failure silent | `1 failed \| 1 skipped (2)` | `Unable to find an element with the text: (…) => element?.hasAttribute("data-title")…` |
  | the `RefusalText` move: its body dropped, `spaces`' tests | `3 failed \| 209 passed (212)` | `Error: expect(element).toHaveTextContent()` |
- `npm run lint` → exit 0; `npm run typecheck` → exit 0; prettier → `All matched files use Prettier code style!`; `npm run check:links` → `2229 links in 176 documents and 1309 source files all resolve.`; `npm run check:classes` → `No physical direction or arbitrary-value classes in 925 files.`
- A wider focused run (72 files: users, spaces, space-links, pages, shared/forms) → `Tests  1 failed | 533 passed (534)`; re-run, two different tests failed, each a cold-load wait (`Unable to find role="navigation" and name "Space dashboard"` in routes › «lists the owner’s eleven pages», `Unable to find role="main"` in authPages); no other vitest was running (`Get-CimInstance … vitest` → empty). The two files alone → `Test Files  2 passed (2)` / `Tests  50 passed (50)`. Noted for the full lane (finding 87 watched there); not a stop by itself, since the full lane on the head is the measure.
- **Departures:** `useAccountActions` declares its own `AccountActionItem` (same shape as `space-links`' `UserActionItem`; `users` cannot import it); the restore item is disabled while its request is pending. `toastRestoreFailed` words the refusal through `RefusalText`, i.e. the errors catalogue (`not_found` → «We couldn’t find what you were looking for.»), as the plan's body-unchanged move implies. `space-links.md` › How it composes now names `users`' account items, as §9 commit 4 wrote it whole.

### Commit 7 — `66dc0622` `feat(users): issue a temporary password` (39 chars)
- Red before the code: users repository → 1 failed (`TypeError: createUsersRepository(...).issueTemporaryPassword is not a function`); component `src/features/users` → 12 failed (the issue hook and dialog stubs, the `kind` line, the issue item's three tests).
- Green after: `npx vitest run --project component src/features/users src/pages/dashboard/admin` → `Test Files  17 passed (17)` / `Tests  71 passed (71)`; users unit → `Tests  5 passed (5)`. The first green run had «keeps none in the cache» red: the check ran before the `gcTime: 0` collection's timer; it now waits for the collection (`waitFor`) — the two breaks below still turn it red.
- Breaks, all red:
  | Break | Result | Error |
  |---|---|---|
  | repository: the method changed | `1 failed \| 4 skipped (5)` | `expected { …(19) } to match object { method: 'post', …(2) }` |
  | repository: the path changed | `1 failed \| 4 skipped (5)` | same |
  | ★ account actions: `googleOnly` dropped | `1 failed \| 1 passed \| 3 skipped (5)` | `expected { …(3) } to match object { disabled: true, …(1) }` |
  | ★ account actions: a Google-only account enabled | `1 failed \| 1 passed \| 3 skipped (5)` | same |
  | ★ issue: the line not drawn | `1 failed \| 5 skipped (6)` | `expected '' to be 'To recover the account once you’ve co…'` |
  | issue: `gcTime: 0` removed | `1 failed \| 5 skipped (6)` | `expected [ Array(1) ] to not deep equally contain { temporaryPassword: 'Tmp-4821-xk' }` |
  | issue: `reset()` removed | `1 failed \| 5 skipped (6)` | same |
  | issue: `close()` on a failure | `4 failed \| 2 skipped (6)` | `expected "vi.fn()" to not be called at all, but actually been called 1 times` |
  | IssuePasswordDialog: the password dialog not rendered | `1 failed \| 1 skipped (2)` | `Unable to find role="dialog" and name "Temporary password"` |
  | TemporaryPasswordDialog: `kind` ignored | `1 failed \| 5 skipped (6)` | `Unable to find an element with the text: Hand it over once you’ve confirmed who they are; …` |
- `npm run lint` → exit 0; `npm run typecheck` → exit 0; prettier → `All matched files use Prettier code style!`; `npm run check:links` → `2230 links in 176 documents and 1314 source files all resolve.`; `npm run check:classes` → `No physical direction or arbitrary-value classes in 930 files.`
- **Departures:** `hooks/temporary-password/useTemporaryPasswordDialog.component.test.tsx` passes `kind: 'created'` (the prop is required; a file beyond §7). `IssuePasswordDialog` has a second test, «asks first, opening on Back, with no accessibility violations». The issue's confirm uses the default `Button` (not destructive), as §9's design issue 2 says.

## 3. On the head (`66dc0622`), once each

- `Get-CimInstance … Where-Object { $_.CommandLine -match 'app-b' -and $_.CommandLine -match 'vitest' }` → empty (`no vitest under app-b`).
- `npm run test:unit` → exit 0: api `Test Files  13 passed (13)` / `Tests  216 passed (216)`; shared `Test Files  45 passed (45)` / `Tests  743 passed (743)`; web `Test Files  80 passed (80)` / `Tests  842 passed (842)`.
- `npm run test:component` → exit 0: `Test Files  171 passed (171)` / `Tests  1126 passed (1126)`, `Duration  404.96s`.
- **Finding 87 (the routes test's time):** in the full lane, «lists the owner’s eleven pages, the overview marked as the page shown» passed, but the default reporter prints no per-test time (the log has no line for the file). The lane is not re-run (§3: once on the head). Measured alone: `npx vitest run --project component src/pages/dashboard/routes.component.test.tsx --reporter=json` → `passed 2653 ms`, `39 passed of 39`. Earlier, in a wider focused run of 72 files (commit 6), this test failed once on a cold-load wait (`Unable to find role="navigation" and name "Space dashboard"`) and passed alone: the margin under load is thin, as finding 87 says.
- `$env:NODE_ENV='production'; npm run build; Remove-Item Env:NODE_ENV` → exit 0, `✓ built in 1.46s`.
- `npm run check:build` → exit 0: `No showcase code in 38 build files (1033 strings checked).` / `No dashboard code in the site's first download.` / `No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download.`
- **The site's first download (§11):** the base `a8c39bda` built the same way (`git switch --detach a8c39bda`, web build, back) → `index-Bl-dBPBq.js 252.94 kB │ gzip: 79.33 kB`; the head → `index-B0jyLDR_.js 253.25 kB │ gzip: 79.37 kB` (+0.31 kB, +0.04 kB gzip). A string search of the head's entry finds none of the new code or words (`/suspended`, `temporary-password\``, `/role\``, `issueTemporaryPassword`, `setSuspended`, «Restore the account», «Make them an admin», `min-width: 1024px`, `atDesk`: 0 each). The +0.31 kB's cause is not pinned down (a candidate: `@shared/forms`' barrel now exports `RefusalText`); noted for the review.
- `npm run check:classes` → `No physical direction or arbitrary-value classes in 930 files.`; `npm run format:check` → `All matched files use Prettier code style!`; `npm run check:links` → `2230 links in 176 documents and 1314 source files all resolve.`
- **Not run:** `npm run test:api` — no `apps/api` or `packages/shared` change (CI runs it).

## 4. The real run

- **Tool:** no `playwright` MCP tools in this session → local headless Chrome over CDP (Node 24's `WebSocket`, no dependency; PR 3's helper, its shots folder changed), real screenshots of the real app. Scripts in this session's scratchpad (`run/cdp.mjs`, `common.mjs`, `api.mjs`, `run0*.mjs`–`run4.mjs`), outside the repository.
- **Servers:** `masaha-postgres-1` up (healthy); `npx prisma migrate status` → `Database schema is up to date!` (the branch's 18 migrations; #92's is not on this branch, see the owner's note above); API `npm run dev -w @masaha/api` → `GET /health` `{"status":"ok","db":"up"}`; web `npm run dev` → 200 on 5320. Signed in as the seeded admin (credentials read from `apps/api/.env` inside the scripts, never printed).
- **Data:** the seeded admin (id 1, «أنت»); the demo owner (14, Demo Space) and the demo receptionist (15, Demo Space's desk), both from `demo.ts`; another admin (18); an owner whose every space is deleted (21, finding 50); a Google-only account already in `masaha_dev` (16). Registered at `/register`, through the screen: user 1 «لينا عوض» (`users1-33078@example.com`, 34) and user 2 "Karim Users" (`users2-33078@example.com`, 33). The first attempt timed out on Vite's cold first load; it registered on the retry.
- **Cases and shots** (`shots\`, 49 PNGs):

| Case | Seen | Shots |
|---|---|---|
| The list: a table at 1440, cards at 768 and 390 | `layout: table` / `cards` / `cards`, both languages; «عدد المستخدمين: 28»; role and state chips beside it | `{ar-light,en-dark}-{1440,768,390}-list` |
| An owner's menu, every width | «[held] تغيير الدور — دوره يتبع روابطه — فُكّ ربطه أولًا · فك روابطه · ربط بمساحة · إصدار كلمة مرور مؤقتة · إيقاف» | `{ar-light,en-dark}-{1440,768,390}-owner-menu` |
| «أنت» on the admin's row | «Basel · أدمن · كلمة مرور وGoogle · 28 سبتمبر · — لا مساحات · نشط · أنت» | `ar-light-1440-own-row` |
| Spaces and desks | owners «مالك» and a badge; the receptionist «استقبال» and Demo Space; «—» for none | the list shots |
| The receptionist's held role | «[held] تغيير الدور — يعمل في مكتب استقبال — يفكّه مالك المساحة أولًا» | `ar-light-1440-receptionist-menu` |
| An admin's link held | «[held] ربط بمساحة — حساب أدمن — لا يُربط بمساحة» | `ar-light-1440-admin-menu` |
| An owner of deleted spaces | «[held] تغيير الدور — كل مساحاته محذوفة — …» and «المساحات المحذوفة» | `ar-light-1440-deleted-spaces-owner-menu` |
| A Google-only account (the plan expected none locally) | «[held] إصدار كلمة مرور مؤقتة — حساب Google — يستعيده من Google» | `ar-light-1440-google-only-menu` |
| Search, role and state chips, the address | `/dashboard/admin/users?q=example.com&role=owner&state=active`, «عدد المستخدمين: 13» | `ar-light-1440-filtered` |
| «فك روابطه» lands on the owners page; Back keeps the filters | landed `/dashboard/admin/owners?q=demo-owner%40example.com`; after Back `/dashboard/admin/users?q=demo-owner&role=owner&state=active`, the field «demo-owner», chips «مالك, نشط» | `ar-light-1440-unlink-them-owners-page`, `ar-light-1440-after-back` |
| No match | «لا يوجد مستخدمون يطابقون البحث»; «مسح الفلاتر» → `/dashboard/admin/users` | `ar-light-1440-no-match` |
| User 1 made an admin, then a user again | dialogs open on «Back»; toasts «لينا عوض is now an admin; their sessions ended», «… is a user again; their sessions ended»; as an admin, the link held | `en-dark-1440-make-admin-dialog`, `-made-admin-toast`, `-make-user-dialog`, `-made-user-toast`; Arabic `ar-light-390-make-admin-dialog` |
| A temporary password issued to user 1 | the confirm; the one-time dialog with «Hand it over once you’ve confirmed who they are; they’ll be asked to change it at their next sign-in.»; «Done» disabled before «Copy», enabled after; toast «Handover recorded: لينا عوض · In person» | `en-dark-1440-issue-confirm`, `-issued-dialog`, `-issued-dialog-copied`, `-handover-toast`; Arabic `ar-light-768-issue-confirm`, `-issued-dialog`, `-handover-toast` |
| Then «Make them an admin» refused | «The role didn’t change / They haven’t changed their temporary password yet; …», the dialog open | `en-dark-1440-make-admin-refused-pending` |
| Then «Link to a space» refused | «Not linked / This person hasn’t changed their temporary password yet; …», the dialog open | `en-dark-1440-link-refused-pending` |
| User 2 linked to Focus Hub | «They become another owner of Focus Hub; it stays verified. / Their account becomes an owner’s, and they’re asked to sign in again.»; toast «Karim Users linked to Focus Hub»; the row then «مالك · Focus Hub» | `en-dark-768-link-space-options`, `-link-consequence`, `-linked-toast`, `ar-light-1440-user2-owner-row` |
| The receptionist's link dialog | Demo Space «Verified · Front desk», `aria-disabled=true`; Arabic «مساحة تجريبية · موثّقة · مكتب استقبال» | `en-dark-768-receptionist-link-desk`, `ar-light-390-receptionist-link-desk` |
| The demo owner suspended, then restored | «Suspend أحمد الشوا? / All their sessions end … / Their spaces stay verified; …»; toast «… suspended; their sessions ended»; the menu then «Restore the account», the link and the issue held «The account is suspended — restore it first»; restored at once, toast «أحمد الشوا’s account restored» | `en-dark-390-suspend-dialog`, `-suspended-toast`, `-suspended-menu`, `-restored-toast` |
| The receptionist's suspension (dismissed) | «… يبقى رابطه بمكتب الاستقبال، ولا يعمل فيه حتى يُسترجع.» | `ar-light-768-suspend-dialog-desk` |
| The add-owner upgrade confirm (finding 88) | «This email has an account / Name ليلى النجار / Joined 7 Oct / Spaces None / Front desk Demo Space …»; not confirmed | `en-dark-768-upgrade-confirm-desk` |
| The spaces list at 768 (alternative B) | `cards` at 768 in both languages; `table` at 1024 | `ar-light-768-spaces-list`, `en-dark-768-spaces-list` |

- Page errors: none in any run. Not performed, by design: `LAST_ADMIN` (a race; the component lane proves it).
- **Focus after each dialog** (probed in `run3`, `run3b`): after «رجوع» in the role dialog and in the suspension dialog, and after the link dialog closes → `{"onTrigger":true,"tag":"BUTTON","label":"إجراءات: …"}`. **After «تم» in the issued password's dialog → `{"onTrigger":false,"tag":"BODY"}`** (the English run too: `focus on: null`). See §5.
- **Data left changed in `masaha_dev`:** users 33 and 34 registered; user 1 made an admin and a user again, with a temporary password pending; Test Owner PR2 (22) with a temporary password pending; user 2 an owner of Focus Hub; the demo owner suspended and restored.
- **Slip, owned:** a log line meant to mask the one-time password printed user 1's throwaway temporary password into this session's tool output (the masking pattern missed). It is in no file, report or commit; the later run logged only the dialog's line, never the password.
- Servers stopped by PID (tsx watch, the server, pino-pretty, vite; no CDP Chrome left); `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` → none; `git status --short` → empty.

## 5. STOPPED (then resumed, §6) — the plan's focus return after «تم» proves false in the browser

**What:** §9 commit 7 builds `IssuePasswordDialog` with `onDone={() => { done(); returnFocus.current?.focus(); }}`, and its docblock says the focus returns to the control that opened it. In the real app, after «تم» the focus lands on `<body>`, in both languages.

**Why:** Radix's `FocusScope` runs its unmount auto-focus when `TemporaryPasswordDialog` unmounts, after `onDone`'s `focus()`, and moves the focus to the element focused when it opened: the confirm's «إصدار» button, already removed, so the focus falls to the body. No planned test checks this focus, so the lanes stayed green.

**Fix offered (the owner chooses):**
- **A (recommended):** `TemporaryPasswordDialog` takes an optional `returnFocus` ref, and its `DialogContent` gets `onCloseAutoFocus={(event) => { if (returnFocus) { event.preventDefault(); returnFocus.current?.focus(); } }}` (Radix calls it on unmount as on close); `IssuePasswordDialog` passes its `returnFocus`, and its `onDone` becomes `done` alone. A test in `IssuePasswordDialog.component.test.tsx`, «returns the focus to the menu’s button after «Done»», red before, green after; folded into commit 7 (`--fixup`); 3 files. The owners page's created-password flow passes nothing and keeps today's behaviour (whether it loses the focus too is not probed here).
- **B:** record a finding (the next free number, 98 if SETTINGS's 94–97 are the last) and leave the behaviour.
- **C (not recommended):** move the focus a tick later (`setTimeout`) in `onDone`; it races Radix's own focus.

**Where the work stands:** seven commits on `feat/admin-users`, local, **not pushed**; every planned test and break done; every lane green on the head; the real run done. Not done: the fix, `#PRNUM` replaced, the push, the PR, CI, `CLEAN`, the conflict check. Once the owner chooses A or B: that, then §13's push steps from `#PRNUM`.

## 6. Resumed — the owner's decision, the push and the PR

- **The owner's decision (2026-10-19):** the focus after «تم» (§5) is **known and deferred** to this PR's review fix round, recorded in `C:\dev\masaha\workspace\WORKER_A\USERS\0_CARRIED_FROM_91.md`, item 2 (option A). Not fixed here; the PR description names it under *Known and deferred*.
- **`#PRNUM`:** `gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number'` → `92`, so **#93**. In Git Bash: `git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#93/g'" a8c39bda..HEAD` → `Ref 'refs/heads/feat/admin-users' was rewritten`; `git update-ref -d refs/original/refs/heads/feat/admin-users`; `git grep -n "#PRNUM" HEAD` → 0 lines; `git diff --stat a8c39bda HEAD` → `93 files changed, 3537 insertions(+), 186 deletions(-)`, the same as before. (A `.webp` under `docs/design/` happens to contain the bytes `#93`; it is unchanged.) The range was `a8c39bda..HEAD`, the branch's own base, since `origin/main` has moved to `eff0a3d1` (#92).
- **Commits now** (subjects unchanged):
  - `64ae74ac` feat(design-system): keep a table's cards to lg (47)
  - `3ba64325` refactor(space-links): share the users list's core (50)
  - `033477e4` fix(space-links): show front desks before upgrade (49)
  - `4d41ad65` feat(space-links): add the admin's users page (45)
  - `db5ea80e` feat(space-links): change a person's role (41)
  - `ce34b6b2` feat(users): suspend and restore an account (43)
  - `4daedc94` feat(users): issue a temporary password (39) — head `4daedc9453119a9668c321857f7becd611815568`
- `git push -u origin feat/admin-users` → `* [new branch] feat/admin-users -> feat/admin-users`.
- `gh pr create --assignee @me --label feat --label area:web --label area:docs --label area:design-system --title "feat(space-links): add the admin's users page"` → **https://github.com/Basel-Ghonaim/masaha/pull/93** (the number written in the docs). The description follows workflow §3: summary, scope / criteria (each with its test) / out of scope, the deferred focus issue, change type, evidence run and not run, screenshots (attached by the owner), Definition of Done.
- **CI:** `gh pr checks 93 --watch` → build, check:classes, check:links, format:check, lint, test:api (4m9s), test:component (6m37s), test:unit, typecheck — all `pass`; CodeRabbit `pass` (review skipped). `gh pr view 93 --json headRefOid,mergeStateStatus` → `{"headRefOid":"4daedc9453119a9668c321857f7becd611815568","mergeStateStatus":"CLEAN","mergeable":"MERGEABLE"}`, the head that was pushed.
- **Conflict check:** `gh pr list --state open` → only #93 (SETTINGS, #92, merged as `eff0a3d1`): no other PR to `merge-tree`. GitHub reports #93 `CLEAN` against `main` with #92 in it, so #92's shared documents did not conflict.
- `git status --short` → empty; ports 3320 and 5320 free (§4).

## 7. Summary (final-report order)

1. **PR:** #93, https://github.com/Basel-Ghonaim/masaha/pull/93, head `4daedc94`, CI green, `CLEAN`. Not merged.
2. **Commits:** §6.
3. **Run / not run:** §2–§3 per commit and on the head; CI ran everything, `test:api` included. Not run locally: `test:api` (no API or shared change), E2E.
4. **Breaks:** every planned break red (§2). One of the plan's breaks — axe and an unnamed chip group — cannot turn axe red; the chips test caught that break instead, and axe got one it can catch (the chips without labels), red.
5. **Real run:** §4, 49 shots. Every planned case performed, plus a Google-only account (the plan expected none locally). Not performed: `LAST_ADMIN` (by design).
6. **Problems:** the focus after «تم» (§5, deferred by the owner); finding 87's thin margin under load (§3); a 0.31 kB growth of the site entry whose cause is not pinned down (§3); a masked log that printed a throwaway test password into the session's output (§4, owned).
7. **Departures:** gathered at each commit (§2): the extra files the new parameters required, the spaces list's test, `useUserLinkActions`' links arriving with commit 5, `useAdminUsersList`'s union options, `AccountActionItem` declared in `users`, the restore item held while pending, the axe break.

## Fix round 1 (2026-10-20) — `7_FIXES_PROMPT.md`, review `6_REVIEW_CLAUDE_CODE.md`, `0_CARRIED_FROM_91.md`

### FR1.1 First checks
- `git status --short` → empty; head `4daedc94`; `gh pr view 93 --json headRefOid,mergeStateStatus` → `4daedc94…`, `CLEAN`. The owner took review finding 3 (the dialogs at the page).
- **How the fixes fold:** the page-level dialogs reshape code that commits 4–7 each built, so a fix commit made on the head would conflict when autosquashed onto commit 4. Instead: `GIT_SEQUENCE_EDITOR="sed -i -e 's/^pick /edit /'" git rebase -i a8c39bda`, each commit changed at its own stop (`git commit --amend`), the later commits resolved onto the new shape. Subjects unchanged; bodies extended. #91's carried unlink fix (carried item 1) has no commit in this PR: it takes a commit of its own, after commit 7 (a departure from "fold into their commits", which it cannot).

### FR1.2 The fixes, by commit (each red before its code, then green; each break seen red)

Breaks run by the scratchpad's `breaks2.py` (edits one or more files, runs the focused test, restores; never prints a line holding a temporary password).

**Commit 1 — `8f7b00b6`** (review 4, 6, 13): the rule cited to **A7**, which names the lists (spaces, users, data reports) as cards until 1024, in `DataTable.tsx`'s prop doc, foundation §12's row, `space-links.md`'s decision, `AdminSpacesList`'s docblock and its test title, and the commit's body (A7 states no "more than five columns"; foundation §9 does not either). `space-links.md`'s spaces-list line: «its filters inline, not in a sheet, from 768 px». `DataTable`'s main docblock re-wrapped.

**Commit 2 — `ff74e5e0`** (review 12, 13): `types/OwnersListView.ts` deleted (unused since the core moved); the docblocks re-wrapped.

**Commit 3 — `15d667f3`** (review 13): `AddOwnerNotice`'s docblock re-wrapped.

**Commit 4 — `af0469cf`** (review 1, 3, 10, 11, 13):
- **The blocker, as it really is:** `useQuery` re-renders only for the fields read, and an identical refetch keeps the same `data`, so a plain refresh did not redraw the list; **a refresh with a change does** — every successful action's — and then `spacesWords`, a new object each render, rebuilt the columns and remounted every row. `spacesWords` is now memoised on the words. Test (`UsersList`) «keeps each row, its actions included, when the list is fetched again with a change»: first written with an identical refetch, it passed on the old code (no redraw) — strengthened to a changed answer, red before the fix: `AssertionError: expected <button type="button"></button> to be <button type="button"></button> // Object.is equality`; green after. Break (`spacesWords: { ...spacesWords }`): red, the same error.
- **The dialogs at the page** (the owner's decision): `space-links` exports `useUserLinkDialog` (the open dialog's state, with its `personId`), `useUserLinkActions(row, { …, open })` returns the items only, `UserLinkDialog({ dialog, onClose, returnFocus })`; the page holds the state above the list, the menu gets `openLink` and a `triggerRef`, and `useRowTriggers` (page) keeps each person's current menu button, the dialog's `returnFocus` a ref that reads it when the dialog closes. `UserActionsMenu.component.test.tsx` became `UsersPage.component.test.tsx` (the menu cannot open a dialog alone now).
  - «keeps an open dialog through the switch from cards to the table, and returns the focus to the row’s menu»: red on the old code (`Unable to find … role "dialog"`), green after.
  - «keeps an open dialog through a refresh that changes the list, and returns the focus to the row’s menu»: green on the memo fix alone.
  - Breaks — the dialog's state held in the row again (the old design: the menu keeps its own `useUserLinkDialog` and renders the dialog): cards to table → red (`Unable to find an accessible element with the role "dialog"…`); with the words rebuilt too, the refresh → red (same); a control with the state in the row and the words stable → green (either fix alone holds the refresh). A first break that only moved where the dialog renders (its state still at the page) did not model the bug — the refresh run stayed green and the switch failed on the hidden table instead — and was replaced by these.
  - The ref read once, when the dialog opens (a stale button after the switch) → red (`expect(element).toHaveFocus()`).
- **Nit 10:** «reads an owner whose every space is deleted as finding 50’s line, a link to the deleted spaces» — break (`owns` without `allSpacesDeleted`) → red (`Unable to find … role "link" and name "All their spaces are deleted …"`).
- **Nit 11:** `useUsersFilters({ fixedRole })` takes no default; `chooseRole` does nothing when the role is fixed — test extended («…never reads a role from the address, writes one, or counts it as a filter»): red before (`expected '?role=admin&state=active' to be '?state=active'`); break (the guard removed) → red, same.
- Docs: `space-links.md` — how it composes (the three exports), a new web decision (**the dialog a row's menu opens is held by the page, above the list**, amending "beside the menu"), the users list's A7 line, the code map. Docblocks re-wrapped (`UserSpaces`, `UsersList`, `useLinkOwnerDialog`, `userRowView`'s new paragraph, `usersFiltersOf`, `navigation.ts`'s one-liner).

**Commit 5 — `66373a28`** (resolved onto the new shape; review 2 for the role):
- The role item opens `{ kind: 'role', personId, person }` through `open`; `UserLinkDialog` renders `RoleDialog` for it; the page needed no change. The menu's «puts the role change first» moved into the page test.
- `RoleDialog` holds «Back» (`disabled`) and Escape (`onEscapeKeyDown` prevented) while pending. Test «holds «Back» and Escape while the change is pending, so its answer is never lost»: red before (`expect(element).toBeDisabled()`); breaks — «Back» not held → red (same); Escape not held → red (`expected "vi.fn()" to not be called at all, but actually been called 1 times`).

**Commit 6 — `de91b3d1`** (resolved; review 2, 3, 7, 8):
- `users` exports `useAccountDialog`; `useAccountActions(person, { open })` returns the items; `AccountActionDialog({ dialog, onClose, returnFocus })`; the page holds the account dialog beside the link one.
- Nit 7: the restore item is no longer disabled (without a reason) while pending. Nit 8: `ownsSpaces: row.spaces.length > 0` — page test «says nothing of spaces staying verified when suspending an owner whose every space is deleted»; break (`row.role === 'OWNER'`) → red (`expect(element).toHaveAccessibleDescription()`).
- `SuspendDialog` holds «Back» and Escape while pending — test red before (`toBeDisabled()`), breaks red (as the role's).
- Docs: `users.md` composition decision (hooks and dialog, held by the page), the owner line «for an owner of spaces», the pending hold.

**Commit 7 — `5209b712`** (resolved; review 2, 3, 5, carried item 2):
- **Finding 2:** the issue confirm holds «Back» and Escape while pending. Test «holds «Back» and Escape while the issue is pending, so the new password is never lost»: red before (`toBeDisabled()`); breaks — «Back» → red; Escape → red (`expected "vi.fn()" to not be called …`).
- **Carried item 2 (the focus after «تم»):** `TemporaryPasswordDialog` takes an optional `returnFocus`, focused from `onCloseAutoFocus` (Radix calls it on unmount too), `preventDefault` first; `IssuePasswordDialog` passes its own and its `onDone` is `done` alone. Tests (`it.each`, the review's addition): «returns the focus to the control that opened it once done: the handover recorded» and «…: the handover refused, the password no longer pending» — both red before (`expect(element).toHaveFocus()`); break (the focus dropped) → red, 2 failed.
- **The owners page's created flow** (the review's addition): `TemporaryPasswordSlot` gains `returnFocus`; `AddOwner` hands «Add owner» (held in state through a callback ref: passing a `useRef` into the slot call during render failed `react-hooks/refs`); `OwnersPage` passes it to the dialog. `AddOwner`'s slot test asserts the slot gets «Add owner»: red before (the slot crashed on a missing ref); break (`{ current: null }`) → red (`expected null to be <button …>`).
- **The issued password at the page:** «keeps the issued password through a refresh that changes the list and the switch from cards to the table, and returns the focus once done» (768 → refresh with a change → 1280 → copy, channel, «Done» → the focus on Nour's menu button): green after; breaks — the account dialog's state held in the row → red (`Unable to find … role "dialog" and name "Temporary password"`); `returnFocus` not handed to the one-time dialog → red (`toHaveFocus()`).
- **Nit 9:** `it.each` «returns the focus to the row’s menu when … is dismissed» for the role change, the suspension and the temporary password.
- **Review 5:** `users.md`'s restore bullet back under «Suspending and restoring on the web.», the issue paragraph after it. Docs: the issue's pending hold, the dialog held by the page, the focus after «تم»; two web decisions in `users.md`; `space-links.md`'s slot decision gains «إضافة مالك».

**New commit 8 — `9714165f` `fix(space-links): hold the unlink's line once sent` (50 chars)** (carried item 1, #91's code: no commit of this PR owns it): `reading = owners.isFetching && !unlink.isPending`. Test «keeps its line once the unlink is sent, while the admin’s views are fetched again»: red before (`expected null to be 'The other owners stay, and it stays v…'`), green after. `space-links.md`'s unlink decision extended.

**Nit 13 (the docblocks):** each commit's own comment lines over 100 characters re-wrapped (a scratchpad `wide.py` lists the lines a commit added; `reflow.py` re-wraps only a paragraph that holds one); paragraphs that predate the PR (#50, #88) are left as they were.

### FR1.3 Checks on the new head `9714165f`
- `npm run lint` → exit 0; `npm run typecheck` → exit 0; `npm run check:classes` → `No physical direction or arbitrary-value classes in 932 files.`; `npm run check:links` → `2230 links in 176 documents and 1316 source files all resolve.`; `npm run format:check` → `All matched files use Prettier code style!`.
- The touched test files, once: `npx vitest run --project component <the 13 touched test files> src/features/space-links/hooks/{users-list,link,owners-list} …/components/{owners-list,link,unlink,space-owners} src/features/users/hooks/{suspend,temporary-password} src/features/spaces/components/toast src/shared/design-system/components/data src/pages/dashboard/routes.component.test.tsx` → `Test Files  25 passed (25)` / `Tests  194 passed (194)`; `npx vitest run --project unit src/features/space-links src/features/users` → `Test Files  8 passed (8)` / `Tests  71 passed (71)`. Not run (the owner's rule for a fix round): the full lanes, the build, `check:build`, `test:api` — CI runs them.
- Noted, not fixed: `docs/design/INDEX.md:868` holds a `<<<<<<< HEAD` marker on `a8c39bda` and on `origin/main` — not this PR's; recorded here for the owner.

### FR1.4 The real run of the round
Local headless Chrome over CDP, as before; `masaha-postgres-1` up; API and web started from `9714165f`; scripts `run/run5.mjs` (the password is never logged; only whether it is shown).
- **The receptionist's desk, retaken (review 14):** `en-dark-768-receptionist-link-desk` — «Demo» typed, the list filtered to «Demo Space · Verified · Front desk [disabled]», the option in view; `ar-light-390-receptionist-link-desk` — «مساحة تجريبية · موثّقة · مكتب استقبال [disabled]».
- **The suspension dialog alone (review 14):** `ar-light-768-suspend-dialog-desk` — dialogs open before: 0; now: 1, «إيقاف ليلى النجار؟ / … / يبقى رابطه بمكتب الاستقبال، ولا يعمل فيه حتى يُسترجع.»; dismissed with «رجوع». (The first round's stacked shot was its script's: the link dialog of the step before was still open.)
- **What the round fixed, in the browser:** Test Owner PR2's temporary password issued at 768 (`en-dark-768-issued-dialog`); the width switched to 1440 → `layout table · dialog still open: true · password shown: true` (`en-dark-1440-issued-dialog-after-switch`); «Done» after «Copy» and «In person» → `{"onTrigger":true,"tag":"BUTTON","label":"Actions: Test Owner PR2"}`, toast «Handover recorded: Test Owner PR2 · In person» (`en-dark-1440-focus-after-done`). Page errors: none in either run.
- Servers stopped by PID (4 node processes; no CDP Chrome left); `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` → none.

### FR1.5 Push, PR, CI
- `git push --force-with-lease=feat/admin-users:4daedc94… origin feat/admin-users` → `+ 4daedc94...9714165f feat/admin-users -> feat/admin-users (forced update)`.
- PR description updated (`gh pr edit 93 --body-file …`): eight commits; a *Review round 1* paragraph in place of *Known and deferred*; this round's evidence above the first round's.
- `gh pr checks 93 --watch` on `9714165f`: build, check:classes, check:links, format:check, lint, test:api (4m30s), test:component (5m47s), test:unit, typecheck — all `pass`; CodeRabbit `pass` (skipped). `gh pr view 93 --json headRefOid,mergeStateStatus` → `{"headRefOid":"9714165fa48c0c6507b3dc8055ee75ecba870107","mergeStateStatus":"CLEAN"}`.
- Conflict check: `gh pr list --state open` → only #93.
- `git status --short` → empty.

### FR1.6 Round summary
1. **PR:** #93, head `9714165f`, CI green, `CLEAN`. Not merged.
2. **Commits:** `8f7b00b6` feat(design-system): keep a table's cards to lg (47) · `ff74e5e0` refactor(space-links): share the users list's core (50) · `15d667f3` fix(space-links): show front desks before upgrade (49) · `af0469cf` feat(space-links): add the admin's users page (45) · `66373a28` feat(space-links): change a person's role (41) · `de91b3d1` feat(users): suspend and restore an account (43) · `5209b712` feat(users): issue a temporary password (39) · `9714165f` fix(space-links): hold the unlink's line once sent (50, new).
3. **Run / not run:** FR1.3 (static checks; touched tests 194 + 71). Not run locally: full lanes, build, `check:build`, `test:api` (the owner's rule for a fix round); CI ran all and passed.
4. **Breaks:** FR1.2, every one red. Two breaks that did not model the bug were replaced and said so: the "dialog under the row" that kept its state at the page (FR1.2, commit 4).
5. **Problems:** the blocker's test first passed on the old code (an identical refetch does not redraw the list) — strengthened to a refetch with a change; the first rebase pass committed commit 4 on a conflict without stopping, so a second pass stopped at 4–7; `react-hooks/refs` refused a ref passed into the slot during render — the trigger is held in state instead; the re-wrapper touched two paragraphs that predate the PR — restored by hand.
6. **Unexpected:** the review's mechanism for the blocker is narrower than it says (`isFetching` is not read, so a plain refetch never redraws); its scenarios after a successful action still hold, and the fix and its test cover them.
7. **Departures:** the carried unlink fix is a commit of its own (no commit of this PR owns #91's code); the role and suspension confirms hold «Back» and Escape too (the review's "preferably"), each with a test; nit 7 by dropping the disabled state rather than adding a reason; `UserActionsMenu.component.test.tsx` became `UsersPage.component.test.tsx`.
8. **Noted for the owner:** `docs/design/INDEX.md:868` carries a merge-conflict marker on `main` (not this PR's).

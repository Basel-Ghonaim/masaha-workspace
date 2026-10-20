# USERS — PR #93 — independent review (Claude Code)

**Head:** `4daedc9453119a9668c321857f7becd611815568` (checked at the start and the end: unmoved). CI: every lane `pass`
(build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck); `CLEAN`.
Read only: commit objects in `C:\dev\masaha\app-design` (`git show`, `git diff origin/main...4daedc94`), plus
TanStack Table's installed `FlexRender.js` (read, not run). Two subagents reviewed commits 1–4 and 5–7 in parallel.
I re-verified every blocker and should-fix below in the code myself.

**Verdict: not ready. One blocker and four should-fixes, all small, for one fix round on this PR.** One of
them (the home of the account dialogs) changes Stronger 7, so the owner decides it.

## The five most important findings

1. **[blocker] At ≥ 1024 px the users table remounts every row on each list render, so open dialogs vanish and focus is lost.**
   - **Where:** `features/space-links/hooks/users-list/useUsersList.ts:21` and `components/users-list/UsersList.tsx`.
   - **The cause, seen in the code:**
     - `spacesWords: { owned: words.owned, desk: words.desk, none: words.noSpaces }` is a new object on every call.
     - `UsersList` builds `spacesOf = useMemo(…, [spacesWords, …])` and `columns = useMemo(…, [headers, spacesOf, actionsOf])`, so `columns` is new on every render.
     - `DataTable` draws cells with `<FlexRender cell={cell} />`, and TanStack's `flexRender` renders a function `cell` as `React.createElement(Comp, props)` (`node_modules/@tanstack/react-table/dist/FlexRender.js:5,22`). A new function is a new component type, so every cell, `UserActionsMenu` included, unmounts and remounts. `UsersList`'s own comment states the same premise ("new columns would draw every row anew").
   - **Failing scenarios, at desktop width only** (cards reuse `renderCard`):
     - **(a)** A successful link, role change or suspension awaits the admin refresh before `close()`. The refetch re-renders the list, the menu and its dialog remount mid-flow, and the trigger ref is gone when focus should return. The focus falls to the list section, not «إجراءات: …», which breaks the plan's "focus after each dialog".
     - **(b)** The one-time issued-password dialog lives in that cell. The admin copies the password and switches to WhatsApp to hand it over. On return after 30 s, `refetchOnWindowFocus: true, staleTime: 30_000` (`shared/api/query/queryClient.ts:16,19`) toggles `isFetching`, the list re-renders, and the dialog is gone before «تم». The handover is never recorded, and the password itself is lost if it was not yet copied.
   - **Why the run stayed green:**
     - The executor probed focus only after «رجوع» or a close, and ran the successful link at 768 (cards).
     - No test re-renders the list with a dialog open at 1280.
   - **Fix:**
     - Make `spacesWords` stable: `useMemo` on `words`, or pass `words` and read the three keys in `UserSpaces`.
     - Add a test at 1280 with the real menu: complete a link (or re-render the list) and assert focus on the row's trigger and the dialog still mounted.
   - **Belongs to:** a fix round on this PR (commit 4).

2. **[should-fix] «رجوع» or Escape while the issue request is pending loses the issued password.**
   - **Where:** `features/users/components/issue-password/IssuePasswordDialog.tsx`. The root has `onOpenChange={(open) => { if (!open) onClose(); }}`, and the footer has a plain `<AlertDialogCancel>` that is not disabled while `dialog.confirm.busy`. Escape is not stopped either.
   - **Scenario:**
     1. The admin presses «إصدار», then «رجوع» or Escape before the answer arrives.
     2. The dialog unmounts.
     3. The server still replaces the password and ends the person's sessions.
     4. The answer lands on an unmounted hook, and `gcTime: 0` collects it.
     5. Nobody knows the new password and no handover is recorded: finding 49's class, on the screen meant to recover from it.
   - **The same pattern elsewhere:**
     - `RoleDialog` and `SuspendDialog` behave the same: a success still toasts (the hook's `onSuccess`), but a refusal is lost silently. That is a nit.
     - PR 3's `UnlinkOwnerDialog` has the same pattern.
   - **Fix:**
     - While busy, disable `AlertDialogCancel` and `preventDefault` in `onEscapeKeyDown` on `IssuePasswordDialog` (and preferably on the role and suspend dialogs).
     - Add a test that «رجوع» is disabled while the issue is pending (break: the `disabled` removed).
   - **Belongs to:** a fix round on this PR (commit 7).

3. **[should-fix] Crossing 1024 px unmounts the row's dialogs, including the one-time password.** This holds even after finding 1 is fixed.
   - **Where:**
     - `DataTable.tsx:178` (`if (!tableUp) { … }`): cards and table are different trees.
     - `useMediaQuery` follows the width live (`useSyncExternalStore` on `matchMedia` change).
     - `UserActionsMenu.tsx` renders `<AccountActionDialog>` and `<UserLinkDialog>` inside the row.
   - **Scenario:** a tablet admin at 768 (cards) issues a password and rotates to landscape 1024 (or resizes or zooms a desktop window) before «تم». Every `UserActionsMenu` unmounts, and `issued` (hook state only) goes with it.
   - **Fix:**
     - Hold the open account dialog (person + kind) at page level: `UsersPage` renders one `AccountActionDialog` outside `UsersList`, and the row menu calls `open(person, kind)`.
     - At minimum, lift the issued password and its `TemporaryPasswordDialog` out of the row, as the owners page holds its created password above the list (`AddOwner`'s slot).
   - **Belongs to:** this departs from Stronger 7 ("each item's dialog rendered beside the menu"), so the **owner decides**. Proposed for this fix round; otherwise record a finding.
   - **Status:** the unmount is verified in code. The rotation is plausible usage, not run.

4. **[should-fix] The documents cite a rule that foundation §9 does not contain.**
   - **Where:** foundation §12's DataTable row ("for a table of more than five columns … (§9; A7)"), `DataTable.tsx:80`'s doc, `space-links.md:167` ("eight columns (foundation §9)") and `:193`, and commit 1's body.
   - **What §9 says at head:** only the Phone / Tablet / Desktop table. "Tables become stacked cards" sits on Phone, and nothing mentions five columns or `lg`.
   - **Where the rule lives:** A7 (`docs/design/CHANGES.md`, G5 · A7). The plan's §5.1 made the same mistake, and the executor carried it into four places.
   - **Fix:** cite A7. Alternatively, with the owner's approval, add the rule to §9's Tablet row so the citations become true.
   - **Belongs to:** a fix round (commits 1 and 4).

5. **[should-fix] `users.md`'s restore bullet sits under the issue paragraph.**
   - **Where:** `docs/features/users.md:56–60`.
     - Line 56 is «**Suspending and restoring on the web.**» and line 57 its «إيقاف» bullet.
     - Line 59 is «**Issuing a temporary password on the web.** …».
     - Line 60 is «- **«استرجاع الحساب» acts at once:** …».
   - **The cause:** commit 7 inserted its paragraph between commit 6's two bullets, so the restore reads as part of issuing.
   - **Fix:** move line 60 up under line 57.
   - **Belongs to:** a fix round, folded into commit 7.

## The rest

6. **[should-fix] `space-links.md:193` says the spaces list keeps "its toolbar still in one row from 768 px".**
   - **What the code and the shot show:** `AdminSpacesToolbar.tsx:28` is `grid … md:grid-cols-2 xl:grid-cols-3`, so from 768 to 1279 px the search and region share one row and the status sits on a second. `shots\ar-light-768-spaces-list.png` shows exactly that.
   - **Fix:** reword to "its filters inline, not in a sheet, from 768 px".
   - **Belongs to:** fix round (commit 1).

7. **[nit] The restore item is disabled while pending with no `reason`.**
   - **Where:** `useAccountActions.ts`, `disabled: restore.isPending` with no reason.
   - **Rule:** foundation §10 says a disabled action says why. The executor declared the disabled state, not the missing reason.
   - **Fix:** add a reason, or drop the disabled state.

8. **[nit] The suspension's owner line for an owner whose spaces are all deleted.**
   - **Where:** `UserActionsMenu.tsx`, `ownsSpaces: row.role === 'OWNER'`.
   - **What it says:** «تبقى مساحاته موثّقة…», about spaces that are deleted.
   - **Fix:** use `row.spaces.length > 0`, or accept the wording.
   - **Status:** Plausible — a product call.

9. **[nit] Focus return is tested only for the link dialog.**
   - **Where:** `UserActionsMenu.component.test.tsx`.
   - **Not asserted:** the role dialog's, the suspension's and the issue confirm's «رجوع». They share the code, and the executor's report says it saw focus return in the browser for role and suspend (read in the report, not seen).
   - **Fix:** one `it.each`.

10. **[nit] Finding 50's line on the users page is never proven.** `UsersList.component.test.tsx` has no OWNER with `spaces: []`. Dropping `|| row.allSpacesDeleted` in `UserSpaces` or the `deletedSpacesLink` would stay green. **Fix:** one test row.

11. **[nit] `useUsersFilters`: a test-only default, and a write path its docblock denies.**
    - **The default:** `useUsersFilters({ fixedRole } = {})` — the `= {}` serves only the tests; `useAdminUsersList` always passes an object. This is against the project's no-test-only-code rule.
    - **The write path:** with `fixedRole`, `chooseRole` still writes `role` to the address, while the docblock says the role is "neither read, nor written". It is unreachable today, since the owners toolbar has no role chips.
    - **Fix:** drop the default; return no `chooseRole` (or ignore the call) when the role is fixed.

12. **[nit] `types/OwnersListView.ts` is dead since commit 2.** `git grep OwnersListView 4daedc94` finds only its definition. **Fix:** delete it in commit 2.

13. **[nit] Docblocks.**
    - `UserActionsMenu.tsx:16–23` splices the temporary-password clause into the held-owner sentence, on a line over 100 columns.
    - Other docblocks run well past the print width: `DataTable.tsx`'s main block (≈ 140), `useAdminUsersList.ts` (≈ 150), `AddOwnerNotice.tsx`, `useLinkOwnerDialog.ts`, `usersFiltersOf.ts`.
    - **Fix:** re-wrap. Prettier leaves comments alone, so CI cannot catch this.

14. **[nit] The screenshots do not show two of the cases claimed.**
    - **The receptionist's desk:** `en-dark-768-receptionist-link-desk.png` and `ar-light-390-receptionist-link-desk.png` never show the Demo Space option with «مكتب استقبال». The English shot has «Demo» typed but the list unfiltered (Arrival Hub, Bare Space, …). The claim "aria-disabled=true" is only in the report; the component test does prove it.
    - **Two dialogs at once:** `ar-light-768-suspend-dialog-desk.png` shows the suspension dialog stacked over a second dialog, the link dialog with its X and its primary button. That is most likely the script's artefact, but the page does hold two independent dialog states (`links.dialog`, `account.dialog`), and the report does not explain the shot.
    - **Fix:** retake the two desk shots with the option in view, and the suspend shot alone, in the fix round's run.

15. **[note, evidence] Finding 87 and the site entry's growth.**
    - **The routes test's time:** it was recorded alone (2653 ms), not within the full lane (the reporter printed none). The report says so honestly, and it also notes one cold-load failure of that test under a 72-file run. Finding 87's margin is thin, as recorded.
    - **The site entry:** grew by 0.31 kB for an unpinned cause, which I did not verify (read in the report only).

### On the known and deferred items (`0_CARRIED_FROM_91.md`)

Item 2's fix A (`TemporaryPasswordDialog` takes an optional `returnFocus`, focused from `onCloseAutoFocus` with
`preventDefault`) is right in principle: Radix's `FocusScope` runs the unmount auto-focus on any unmount. It is incomplete in four ways:

- **The diagnosis.** The executor's report blames the removed «إصدار» button. More precisely (from Radix's modal `DialogContent`, plausible, not run), Radix focuses `context.triggerRef`, which is null with no `Dialog.Trigger`, so the focus stays on the removed «تم» and falls to body. Today's `focus()` in `onDone` cannot win, because the trap is still mounted. The cure is the same.
- **The owners page.** Its created-password flow (`OwnersPage` slot → `AddOwner`) loses the focus the same way, and fix A gives it no ref unless the slot's signature gains one (`temporaryPassword(added, done, returnFocus)`, with `AddOwner` passing its trigger). Fold it into the same fix, or carry it to OWNER_SETUP, which reuses the dialog. Plausible: not probed in a browser.
- **The failure path.** The test should also cover the handover's not-pending / not-found path, which also calls `onDone`.
- **Fix A needs findings 1 and 3.** As long as findings 1 and 3 stand, the `returnFocus` target can be a ref of a remounted row (null), and the dialog can disappear before «تم» at all.

## Checked and fine

- **`DataTable cardsBelow`:** default `'md'`; test at 768 / 1023 / 1024. The spaces list passes `"lg"` (alternative B) with its 768 test red before. No finding `<n>` was created, as the approval note asks.
- **Commit 2 is a pure refactor:** `role: 'owner'`, status order, busy, count, pages, failure, 429, empty / no-match and the state chips are line-for-line the same. The owners tests are unchanged across the PR.
- **Finding 88:** the desks are mapped with `nameOf` (lang/dir), drawn as neutral badges, and the finding is Resolved with its index line moved. Shot `en-dark-768-upgrade-confirm-desk` shows «Front desk · Demo Space».
- **The users page:**
  - `?q=&role=&state=&page=` are read by the contract's schema; the chips replace the address and return to page 1; the pages are links.
  - The owners page never reads `?role=` and does not count it as a filter.
  - «أنت» replaces the menu on the admin's own row; emails are `dir="ltr"`; the dash carries an sr-only «لا مساحات»; finding 50's line runs through `OwnerSpaces`.
  - The route is lazy.
- **«ربط بمساحة» from a person:**
  - PR 3's `LinkOwnerDialog` is reused, not copied, and a USER's link carries the becomes-owner line.
  - `atDesk` disables the option and captions it.
  - The link is held with its reason for an admin and a suspended account.
- **The role change:**
  - Only user ⇄ admin; held for an owner (lead to the owners page by email), an owner of deleted spaces (lead to the deleted spaces) and a receptionist.
  - A destructive footer `Button`, not `AlertDialogAction`; «رجوع» first-focused.
  - The toast comes after the refresh.
  - Every code the API answers is worded: `OWN_ACCOUNT`, `not_found`, `ACCOUNT_HAS_LINKS`, `ACCOUNT_PASSWORD_PENDING`, `LAST_ADMIN`, plus 429.
- **Suspend and restore:**
  - The owner and desk lines are conditional; the restore acts at once with no undo; its failure toast goes through `RefusalText` and stays.
  - Every code is worded: `OWN_ACCOUNT`, `LAST_ADMIN`, `not_found`.
- **Issuing a temporary password:**
  - The confirm comes first, in the default variant, then `kind="issued"`: no X, no Escape, no outside click, «تم» after «نسخ».
  - Held for a suspended or a Google-only account.
  - Every code is worded: `ACCOUNT_SUSPENDED`, `GOOGLE_ONLY_ACCOUNT`, `OWN_ACCOUNT`, `not_found`.
  - The password never reaches a toast or a log; the cache test fails without `gcTime: 0` or `reset()`.
  - Finding 49's dated line is in place.
- **`RefusalText`:** a true `git mv` into `shared/forms`, exported; `spaces` imports it from there; architecture § Forms names it.
- **Boundaries:** neither `users` nor `space-links` imports the other. The page composes the menu and maps `AccountPerson`.
- **Frontend rules:**
  - Both catalogues have matching keys (`satisfies`); names are `isolate`d or in `<bdi>`.
  - No physical-direction classes or raw colours in the new files.
- **Commits:** seven subjects of 39–50 characters; every body says why; no attribution trailer.
- **Docs:** `architecture.md` (Built so far, Forms), `overview.md` and the users-page and role parts of `space-links.md` match the code, apart from findings 4–6.
- **Screenshots:**
  - The list is a table at 1440 and cards at 768 and 390, in both themes and languages.
  - Held items show their reasons, at every width.
  - The role dialogs and toasts, the issue confirm and the one-time dialog with the issued line, the suspended menu, and the spaces list as cards at 768.

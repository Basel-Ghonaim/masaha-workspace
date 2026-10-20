# USERS — the admin's users page (screen 29) — the plan

> Written 2026-10-19 from `origin/main` `18ab1705` (#90 merged) **plus OWNERS PR 3**, `feat/admin-owner-links`
> at **`02cc70ae`** (local, not pushed, not merged: `aa0c8a4e` #89's leftovers, `0ee60d62` linking and
> unlinking, `02cc70ae` the editor names its owners). **The executor starts only after PR 3 has merged.**
> One PR (the owner's choice), branch `feat/admin-users`, **seven commits, ≈ 88 files — over the prompt's
> ~60: see §14, decision 1.** The executor may be any capable coding agent: no step depends on a Claude
> skill (the appendix is only a map).

> **Approved by the owner, 2026-10-19 — binding on the executor:**
> - **§14.1 — one PR, all seven commits** (the owner's choice; alternative A is not taken). The review is
>   split in two halves run in parallel by one reviewer (commits 1–4 and 5–7) — nothing for the executor.
> - **§14.2–4, 6, 7 as recommended:** `DataTable cardsBelow` (its own commit); Stronger 2–8; design issues
>   1–9; finding 49's dated line; the words of §9.
> - **§14.5 — alternative B is taken, not the finding:** the spaces list passes `cardsBelow="lg"` too, in
>   commit 1 (A7 already decided cards at 768 for Spaces, Users and Data reports); **no finding `<n>`** —
>   drop it and its index line. The real run adds the spaces list at 768 (Arabic light, English dark).
>   If `AdminSpacesList`'s own tests assume the table at 768, update them in commit 1 and say so.
> - **Before any edit:** OWNERS PR 3 (#91) has merged. Its head changed after this plan (rebased and a fix
>   round: `02cc70ae` is no longer its head) — run the first checks against the merged `origin/main`
>   (`git diff --name-status 02cc70ae origin/main` for the code files this plan names); a difference the
>   plan does not cover → stop and ask. Finding numbers: the next free ones on the latest index.

## 1. Summary

The admin gets the **users page** (`/dashboard/admin/users`, screen 29, replacing its placeholder): every
account, searched by name or email, filtered by role and by state with chips, the address keeping all of it,
paged; a table from 1024 px and a card per person below it (A7, by a new `DataTable` prop); each person's
role, way of signing in, joining date, **owned spaces and reception desks** (DI-24) and state; the admin's
own row reads «أنت». Each other row has a menu: **change the role** («مستخدم» ⇄ «أدمن» through an
`AlertDialog`; held, with its reason, for an owner or a receptionist), **«ربط بمساحة»** (PR 3's link dialog,
from the person), **issue a temporary password** (a confirm, then #89's one-time password dialog; held for a
suspended or a Google-only account, AD-021), and **suspend** (an `AlertDialog`) or **restore** (at once).
Every refusal the API can answer is worded. **Finding 88 is resolved:** the add-owner upgrade confirm shows
the account's reception desks. Nothing in `apps/api`, `packages/shared`, the schema or the dependencies; one
design-system change (`DataTable`'s card breakpoint), in its own commit.

## 2. The contract

### Scope
- `DataTable` keeps its cards until 1024 px when asked (`cardsBelow="lg"`), foundation §9's own rule.
- The users list's core (read, filters, states, toolbar) shared by the owners list and the users list.
- Finding 88: the upgrade confirm shows the account's reception desks.
- The users page: list, search, role and state chips, address, pages, states, cards below 1024, the
  person's spaces and desks, «أنت»; the row menu composed by the page from `space-links` and `users`.
- The person's actions: link to a space (`space-links`), change the role (`space-links`), suspend and
  restore (`users`), issue a temporary password (`users`).

### Acceptance criteria
- [ ] `/dashboard/admin/users` shows `GET /admin/users`: name, email (`dir="ltr"`), role («مستخدم» · «مالك» · «أدمن»), sign-in («كلمة مرور» · «Google» · «كلمة مرور وGoogle»), joined (the lists' short date), spaces («مالك» + a badge per owned space; «استقبال» + a badge per desk; a dash read as «لا مساحات»; finding 50's line for an owner of deleted spaces only), state badge, actions.
- [ ] A table from 1024 px; a card per person below it, 768 included (A7).
- [ ] Search (paused), role chips «الكل · مستخدم · مالك · أدمن» and state chips «الكل · نشط · موقوف» beside the count, at every width, no sheet; `?q=&role=&state=&page=`, each read by the contract's rule; the pages are links; the owners page never reads `?role=`.
- [ ] Loading, failure (reference, «إعادة المحاولة», 429 wait), empty and no-match states; the focus kept when the row that held it leaves.
- [ ] The admin's own row reads «أنت», no menu.
- [ ] «تغيير الدور»: a user with no visible link → «جعل {name} أدمن؟»; an admin → «إعادة {name} مستخدمًا؟»; each an `AlertDialog` naming the consequence, its destructive action staying until the answer; held with its reason for an owner (with «فك روابطه» to the owners page), an owner of deleted spaces (with «المساحات المحذوفة»), and a receptionist; `ACCOUNT_HAS_LINKS`, `ACCOUNT_PASSWORD_PENDING`, `LAST_ADMIN`, `OWN_ACCOUNT` and an account gone worded in the dialog, which stays open.
- [ ] «ربط بمساحة» opens PR 3's link dialog from the person; held for an admin and a suspended account; a user's link says «ويصبح حسابه حساب مالك…»; the person's owned spaces read «مربوطة» and desks «مكتب استقبال», neither choosable; `ACCOUNT_PASSWORD_PENDING` worded.
- [ ] «إصدار كلمة مرور مؤقتة»: a confirm naming the consequence, then the one-time password dialog (no X, no Escape, no outside click, «تم» after «نسخ», the handover) with the issued line; held for a suspended account and a Google-only one (AD-021); `ACCOUNT_SUSPENDED`, `GOOGLE_ONLY_ACCOUNT`, `OWN_ACCOUNT`, an account gone worded in the confirm; no password kept in the cache.
- [ ] «إيقاف»: an `AlertDialog`, destructive, naming the consequence (sessions end; an owner's spaces stay verified; a receptionist's desk link kept); «استرجاع الحساب» at once with a toast; each refusal worded.
- [ ] The add-owner upgrade confirm lists the account's reception desks (finding 88 Resolved).
- [ ] Both catalogues complete; Arabic light and English dark, at 390, 768 and 1440, in a real run.

### Out of scope
Unlinking from the users page (the owners page and the editor own it; the role item leads there); the
spaces list's cards until 1024 (a finding, §6); finding 89 (stays open); any API, shared-package, schema or
dependency change; any design-system change but `DataTable`'s `cardsBelow`; a showcase example for it (§9,
commit 1); the owners page's look.

## 3. The reading done

From `origin/main` `18ab1705` and `feat/admin-owner-links` `02cc70ae`: `CLAUDE.md`; `docs/development/workflow.md`;
`testing.md`; `docs/frontend/architecture.md` §3 (capabilities, layout, components/hooks, what a feature
exports, forms) and §7; `design-system/foundation.md` (§12's DataTable row, §9's rule via the `DataTable`
source); `docs/frontend/localisation.md`; `docs/features/users.md` (whole), `space-links.md` (whole, PR 3's);
`docs/api/api-contract.md` §1–4, *Owners (the admin)*, *Users (the admin)*, §6; ADR 0009 rule 2 and ADR 0013
through the two capability documents and the contract; `docs/design/SCREENS.md` (29), `INDEX.md` (§46 frames,
`?fail=role`, `?temp=1`), `docs/design/prototype/Admin users.html` and `masaha/admin.jsx` (`TempPassDialog`,
`AdminList`, `LinkOwnerDialog`); `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md` (A4–A7, AD-021,
AD-028, every amendment, DI-23, DI-24) and `DECISIONS_SHARED.md` (P1, P5, P8, P9 and amendments); the OWNERS
plan `C:\dev\masaha\workspace\WORKER_A\OWNERS\2_PLAN.md` (whole, its approval note) and
`3_EXEC_PROMPT_PR3.md` §2; findings 49, 82, 87, 88, 89, 91 and the open findings' titles; the documentation
map's deferred table (nothing triggered). Code (PR 3's): `features/space-links/**` (users list, owners list,
add owner, link, unlink, owner actions, space choices, repository, keys, copy), `features/users/**`
(repository, the password dialog and its hook, index), `features/spaces/components/toast/{actionToasts,ActionRefusal}.tsx`,
`shared/forms/index.ts`, `shared/session/index.ts` and `store.ts`'s `useSession`, the design system's
`DataTable`, `pages/dashboard/{routes.tsx,navigation.ts,admin/OwnersPage.tsx,admin/SpacesPage.tsx}`,
`shared/copy/{arabic,english}/{spaceLinks,users,errors}.ts`, `packages/shared/src/{space-links/requests.ts,users/requests.ts}`,
`apps/api/src/modules/{users/users.admin.routes.ts,space-links/space-links.admin.routes.ts}` (the routes
exist), `apps/api/src/db/seed/demo.ts` (a demo owner and a demo receptionist).

## 4. The owner's decisions, as they will be built

- **U1 — the whole screen 29** (A5, A7, AD-021; DI-24): §2's criteria; the words in §9.
- **U2 — finding 88 resolved here** (commit 3); **finding 89 stays open.**
- **U3 — one PR**, Claude Code throughout (but see §14, decision 1: ≈ 88 files).
- **Placement, by the rule that owns each file** (architecture §3 *Names match the backend*; ADR 0013):

| Piece | Lives in | Why |
|---|---|---|
| The users list (read, filters, row, chips, cards) | `features/space-links` (`users-list/`) | `GET /admin/users` is the `space-links` module's composed read (O2, #88) |
| «ربط بمساحة» from a person | `features/space-links` (PR 3's `LinkOwnerDialog`) | reuse, never copy |
| The role change and its dialog | `features/space-links` (`role/`) | `PUT /admin/users/:id/role` is `space-links`' (`admin-roles/`); only the links decide it |
| The menu's link and role items | `features/space-links` (`user-actions/`), exported hook + dialog | their rules read the links |
| Suspend / restore, issue a temporary password, their dialogs and items | `features/users` (`suspend/`, `issue-password/`, `account-actions/`), exported hook + dialog | `PUT …/suspended` and `POST …/temporary-password` are the `users` module's; the one-time dialog is `users`' (#89) |
| The row menu combining both | `pages/dashboard/admin/UserActionsMenu.tsx` | "a component that combines several capabilities never lives in one of them" (architecture › What a feature exports) |
| `DataTable`'s card breakpoint | the design system | foundation §9's rule for a table of more than five columns; the component lacked it (DI-23) |
| A refusal under a toast's title | `shared/forms` (`RefusalText`, moved from `spaces`) | its second instance (engineering principles §1) |

## 5. Stronger decisions

1. **`DataTable` gains `cardsBelow?: 'md' | 'lg'`** (default `'md'`, today's behaviour). *What:* the media
   query becomes `(min-width: 1024px)` for `'lg'`. *Why:* A7 makes the users list cards at 768, and
   foundation §9 already says a table of more than five columns becomes cards below `lg`; the prototype had to
   copy the table's card markup (`AdminList`, DI-23). *Cost:* one prop, one test, one §12 line; a
   design-system change, so its own commit and decision 2. **Recommended.**
2. **The users list's core is shared at its second instance** (commit 2, a refactor): `useOwnersList`'s
   read, status, count, pages, failure, empty and no-match, search and state chips move to
   `useAdminUsersList({ fixedRole?, words })`; `OwnersToolbar` becomes `users-list/UsersToolbar` with optional
   role chips. *Why:* engineering principles §1; a copy would drift. *Cost:* 4 files, proven by the owners
   list's tests unchanged. **Recommended.**
3. **`useUsersFilters({ fixedRole })`:** with a fixed role, the address's `role` is neither read nor counted
   as a filter. *Why:* otherwise `/dashboard/admin/owners?role=admin` would count as a filter («لا يوجد … يطابقون
   البحث») while still asking for owners. *Cost:* one option, one test. **Recommended.**
4. **A person's reception desks are unavailable in the link's space choices** («مكتب استقبال»), as their
   own spaces are («مربوطة»). *Why:* the server refuses `RECEPTION_LINK_ACTIVE` there; the row now knows the
   desks (DI-24), so the admin is told before choosing. *Cost:* `SpaceChoiceView.atDesk`, one line, one test.
   **Recommended.**
5. **The role item is held up front for every case the row can see** (an owner, an owner of deleted spaces,
   a receptionist) and the link item for an admin. *Why:* foundation §10 (a disabled action says why); the
   refusal remains for what the row cannot see (a deleted space's link, a link made meanwhile). *Cost:* the
   rules in one hook, one `it.each`. **Recommended.**
6. **`ActionRefusal` moves to `shared/forms` as `RefusalText`** at its second instance (the restore's failure
   toast). *Why:* engineering principles §1; `users` cannot import `spaces`. *Cost:* a `git mv`, one import
   in `spaces`, one export, one clause in architecture § Forms; proven by `spaces`' tests unchanged.
   **Recommended.**
7. **The page composes the row menu from two capabilities' exported hooks and dialogs**, rather than one
   feature's menu taking the other's items through a slot. *Why:* a menu item's dialog must outlive the
   closed menu, so its state sits beside the menu; architecture allows a feature to export hooks "when a
   higher layer needs the capability's actions to compose something the capability does not own". *Cost:*
   `space-links` exports `useUserLinkActions` + `UserLinkDialog`, `users` exports `useAccountActions` +
   `AccountActionDialog`. **Recommended.**
8. **The temporary password dialog takes a required `kind: 'created' | 'issued'`.** *Why:* the issued line
   is not the created one («عند الدخول التالي» against «عند أول دخول»); the place shows the capability's
   own fact differently, by a prop. *Cost:* the owners page passes `kind="created"`. **Recommended.**
9. **No rule is weakened.** P8's exception (no success toast when the row shows the change) is for in-row
   controls; the role change and the suspension act through a dialog and the row may leave a filtered list,
   so they toast, as the prototype does. P9's undo is not offered after a restore: its undo would be a
   suspension, which asks first (design issue 6).

### Proposed alternatives (the owner may prefer them)
- **A — two PRs** instead of one (decision 1): PR A = commits 1–5 (≈ 59 files), PR B = commits 6–7 (≈ 31),
  PR B cut once A merged. Same commits, same tests.
- **B — the spaces list's cards until 1024 folded here** (one prop on `AdminSpacesList`'s `DataTable`, its
  screenshots at 768) instead of finding `<n>`. It changes another screen; recommended: the finding.
- **C — one shared `useRefreshAdmin`** (in `shared/api`) for `spaces`, `space-links` and now `users`. An
  architecture change across three features; recommended: `users` keeps its own three lines, as architecture
  §7 has each feature invalidate the admin scope itself.

## 6. Related findings

| Finding | Folded? | Why · cost |
|---|---|---|
| **88** the upgrade confirm shows no front desks | **Yes, commit 3** (U2) | The data arrived in #90 (`receptionSpaces`); one row in the notice, one test. Resolved. |
| 89 «تحقّق من البريد» stands for three causes | No (U2) | The owner keeps it open. |
| 50 an owner whose spaces are all deleted | Its line reused | The users row shows the same line, and the role item leads to the deleted spaces. No status change. |
| 49 a lost answer loses the temporary password | A dated line (commit 7) | It was resolved on the API; the users page is now its screen. One line. |
| 82 `features/users` keeps operations flat | No | The new operations take their own folders (`suspend/`, `issue-password/`, `account-actions/`); the old flat files are left alone. |
| 87 the owners shell cold-loads the space-links index | No — **watched** | This item grows that index; §13 has the executor record the routes test's time, and stop if it fails. |
| 83, 84, 90–93 | No | Other screens or the API. |

**New (one number, `<n>`, the next free on the latest `origin/main`'s index; 94 onward are being taken by
PR 3 and SETTINGS):** **`<n>` — the spaces list shows a table at 768.** *Evidence:* A7 makes the spaces list
cards at 768, and `DataTable` can now keep them (`cardsBelow="lg"`, this PR), but `AdminSpacesList` still
switches at 768 (foundation §9: more than five columns). *Resolves when:* the spaces list passes
`cardsBelow="lg"`, or the owner keeps the table at 768. Recorded in commit 1.

## 7. The files

`apps/web` and `docs` only. Paths from `apps/web/src/` unless they start with `docs/`.
**Shared with worker B's SETTINGS** (it runs in parallel on `apps/api`, `packages/shared`, `docs`): likely text
conflicts in **`docs/project/overview.md`** (the *Built* lines), **`docs/architecture/findings/README.md`**
(index lines), and possibly `docs/frontend/architecture.md`; each side keeps to its own lines; a conflict
there takes the documents' fast path. This item does not edit `docs/api/api-contract.md`. No code file is
shared with SETTINGS.

| Commit | Files (new ones marked +) | Count |
|---|---|---|
| 1 | `shared/design-system/components/data/DataTable/DataTable.tsx`, `DataTable.component.test.tsx`; `docs/frontend/design-system/foundation.md`; + `docs/architecture/findings/<n>-the-spaces-list-shows-a-table-at-768.md`, `docs/architecture/findings/README.md` | 5 |
| 2 | `features/space-links/`: + `hooks/users-list/useAdminUsersList.ts`, `hooks/owners-list/useOwnersList.ts`, `git mv components/owners-list/OwnersToolbar.tsx components/users-list/UsersToolbar.tsx`, `components/owners-list/OwnersList.tsx` | 4 |
| 3 | `features/space-links/`: `services/userRowView.ts` (+ `.unit.test.ts`), `types/UserRowView.ts`, `hooks/add-owner/useEmailAccount.ts`, `types/EmailAccountView.ts`, `components/add-owner/AddOwnerNotice.tsx`, `components/add-owner/AddOwner.component.test.tsx`; `shared/copy/{english,arabic}/spaceLinks.ts`; `docs/architecture/findings/88-the-upgrade-confirm-shows-no-front-desks.md`, `docs/features/space-links.md` | 11 |
| 4 | `features/space-links/`: `services/usersFiltersOf.ts` (+ test), `types/UsersFilters.ts`, `hooks/users-list/useUsersFilters.ts` (+ test), + `hooks/users-list/useUsersList.ts` (+ test), + `components/users-list/{UsersList,UserCard,UserSpaces}.tsx` (+ `UsersList.component.test.tsx`), `types/LinkTarget.ts`, `hooks/link/useLinkOwnerDialog.ts` (+ test), `hooks/useSpaceChoices.ts`, `types/SpaceChoiceView.ts`, `components/SpaceCombobox.tsx`, `components/link/LinkOwnerDialog.component.test.tsx`, `hooks/owner-actions/useOwnerActions.ts`, + `hooks/user-actions/useUserLinkActions.ts` (+ test), + `components/user-actions/UserLinkDialog.tsx`, `index.ts`; `pages/dashboard/admin/`: + `UsersPage.tsx`, + `UserActionsMenu.tsx` (+ test), + `MenuActionItem.tsx`; `pages/dashboard/{navigation.ts,routes.tsx,routes.component.test.tsx}`; `docs/frontend/architecture.md`, `docs/project/overview.md` | 32 |
| 5 | `features/space-links/`: `repository/spaceLinksRepository.ts` (+ unit test), + `hooks/role/{useChangeRole,useRoleDialog}.ts` (+ test of the second), + `components/role/RoleDialog.tsx` (+ test) | 7 |
| 6 | `features/users/`: `repository/usersRepository.ts` (+ unit test), + `types/AccountPerson.ts`, + `hooks/useRefreshAdmin.ts`, + `hooks/suspend/{useSetSuspended,useSuspendDialog}.ts` (+ test of the second), + `components/suspend/SuspendDialog.tsx` (+ test), + `hooks/account-actions/useAccountActions.ts` (+ test), + `components/account-actions/{AccountActionDialog,accountToasts}.tsx`, `index.ts`; `git mv features/spaces/components/toast/ActionRefusal.tsx shared/forms/components/RefusalText.tsx`, `shared/forms/index.ts`, `features/spaces/components/toast/actionToasts.tsx`; `shared/copy/{english,arabic}/users.ts`; `docs/features/users.md` | 20 |
| 7 | `features/users/`: + `hooks/issue-password/{useIssueTemporaryPassword,useIssuePasswordDialog}.ts` (+ test of the second), + `components/issue-password/IssuePasswordDialog.tsx` (+ test), `hooks/temporary-password/useTemporaryPasswordDialog.ts`, `components/temporary-password/TemporaryPasswordDialog.component.test.tsx`; `pages/dashboard/admin/OwnersPage.tsx`; `docs/architecture/findings/49-a-lost-answer-to-adding-an-owner-loses-its-temporary-password.md` | 9 |

Files touched again in later commits (not counted twice): `useAdminUsersList.ts`, `userRowView.ts` (+ test),
`UserRowView.ts`, `UsersToolbar.tsx`, `OwnersList.tsx`, `useOwnersList.ts`, `useEmailAccount.ts`,
`useUserLinkActions.ts` (+ test), `UserLinkDialog.tsx`, `UserActionsMenu.tsx` (+ test), `index.ts` (both
features), the four catalogue files, `space-links.md`, `users.md`, `architecture.md`, `overview.md`,
`findings/README.md`. **Total ≈ 88 files.**

## 8. Design issues (built only once the reply approves them)

1. **Role and state are two `Select`s in a `FilterSheet`** (prototype). P5: a status filter of four or fewer
   choices is `ToggleGroup` chips; A7: a filter is a chip; the owners page already shows its state as chips. →
   **Two chip groups by the count, «الدور» (الكل · مستخدم · مالك · أدمن) and «الحالة» (الكل · نشط · موقوف),
   at every width, no sheet.** *If not approved:* the role a `Select` field inline from 768 and in a
   `FilterSheet` below it; the state chips stay.
2. **The three confirms close on their action** (`AlertDialogAction`), so a refusal has nowhere to show. →
   A footer `Button` (`variant="destructive"` for the suspension and the role change, the default for the
   issue) with `loading`, staying until the answer, the refusal inside (P8), Cancel «رجوع» first-focused —
   as the unlink (OWNERS design issue 10).
3. **The role refusal guesses «استقبال على الأرجح»** because the list showed no desks. The row now carries
   them (DI-24). → «تغيير الدور» held up front for a receptionist («يعمل في مكتب استقبال — يفكّه مالك
   المساحة أولًا»); the remaining `ACCOUNT_HAS_LINKS` is worded without a guess (a deleted space's link, or
   one made meanwhile).
4. **Cards between 768 and 1023 drawn by copying `DataTable`'s markup** (`AdminList`, DI-23). → The layer's
   `DataTable cardsBelow="lg"` (Stronger 1); no copied markup.
5. **The suspension says nothing of a receptionist's desk.** → For a person with a desk: «يبقى رابطه بمكتب
   الاستقبال، ولا يعمل فيه حتى يُسترجع.»
6. **A restore acts at once with a toast and no «تراجع»,** though P9's act-at-once has an undo. Its undo would
   be a suspension, which asks first. → **Keep the design:** no undo; the toast says the account is
   restored. (Recorded as a web decision.)
7. **«ربط بمساحة» is not in the prototype's menu** (the prompt adds it). → After «تغيير الدور»; held with its
   reason for an admin («حساب أدمن — لا يُربط بمساحة») and a suspended account («الحساب موقوف — استرجعه
   أولًا»), as foundation §10 asks of a disabled item.
8. **The count reads «العدد: N».** → «عدد المستخدمين: N», as every list.
9. **The prototype's spaces column is absent.** DI-24 (owner's U1) adds it: «مالك» and «استقبال» groups of
   neutral badges, finding 50's line for an owner of deleted spaces, a dash read as «لا مساحات». (Settled; listed
   so the look is approved.)

## 9. What is built — interfaces, words, states

Every new decision and history line in a document ends with the commit's date and **`#PRNUM`** (replaced
before the push, §13). A person's name inside a line is `isolate`d (a string) or in a `<bdi>` (JSX); a
space's name is its own element with `lang`/`dir` (`lineParts`, `NamedLine`). Every user-facing string is in
both catalogues. `en` / `ar` below.

### Commit 1 — `DataTable` keeps its cards to `lg`
- `DataTableProps.cardsBelow?: 'md' | 'lg'` — *the width below which each row is a card: `'md'` (768 px, the
  default) or `'lg'` (1024 px), for a table of more than five columns (foundation §9)*. `const tableUp =
  useMediaQuery(cardsBelow === 'lg' ? '(min-width: 1024px)' : '(min-width: 768px)')`. The `renderCard` doc
  says "below the `cardsBelow` width".
- `foundation.md` §12, Table + DataTable row, append: «· `cardsBelow="lg"` keeps the cards until 1024px, for a
  table of more than five columns that names no column priority (§9; A7)».
- Finding `<n>` (Open, today's date) and its index line under *Open*. No showcase example: the showcase's
  DataTable already shows both layouts, and the prop only moves the switch (said in the PR).

### Commit 2 — the users list's core shared (refactor, no behaviour change)
- **`hooks/users-list/useAdminUsersList({ fixedRole, words })`**, `fixedRole: 'owner' | undefined` (commit 4
  widens it), `words`: `Pick<Catalogue['spaceLinks']['ownersList'], 'label' | 'search' | 'searchPlaceholder' |
  'state' | 'states' | 'count' | 'empty' | 'emptyHint' | 'noMatch' | 'clearFilters' | 'loadFailed' | 'pagination'>`
  → today's `useOwnersList` body minus `intro`, `columns`, `allSpacesDeleted`: `{ status, rows, busy, label,
  count, pagination, empty, noMatch, failure, filters: { search, state } }`; request `{ ...filters.request,
  role: fixedRole }`.
- **`useOwnersList()`** = `{ ...useAdminUsersList({ fixedRole: 'owner', words: lines }), intro, columns,
  allSpacesDeleted }`.
- **`components/users-list/UsersToolbar.tsx`** (moved): props `{ filters: AdminUsersListView['filters']; count }`
  where `AdminUsersListView = ReturnType<typeof useAdminUsersList>` (declared in the hook's file as an exported
  type alias; no new types file). `OwnersList` imports it from there.
- **Proof:** `useOwnersList.component.test.tsx`, `OwnersList.component.test.tsx`, `useUsersFilters.component.test.tsx`
  unchanged and green. No doc (a pure refactor).

### Commit 3 — the upgrade confirm shows the reception desks (finding 88)
- `UserRowView` gains `receptionSpaces: SpaceNameView[]` (*the spaces of its active reception links, each named
  in the interface's language*); `userRowView` maps `row.receptionSpaces` with the same `nameOf`.
- `EmailAccountView` gains `receptionSpaces: SpaceNameView[]`; `useEmailAccount` sets it from the row view.
- `AddOwnerNotice`'s `dl` gains a row after «المساحات»: `labels.reception` and the desks as neutral `Badge`s
  (name marked), or `labels.noReception`.
- **Words, `spaceLinks.addOwner.account`:** `reception` Front desk / الاستقبال · `noReception` None / لا مكاتب استقبال.
- **Docs:** finding 88 → **Resolved**, «**Resolution (<date>, #PRNUM):** the upgrade confirm lists the account's
  reception desks beside its spaces, from the users list's `receptionSpaces` (#90).»; its index line moves to
  *Resolved*. `space-links.md`: *Behaviour* › adding an owner, «— the name, when it joined, its spaces and its
  reception desks —»; *Web decisions*: «**The upgrade confirm lists the account's reception desks** (finding
  88). *Why:* an account the server lets be upgraded owns no space, so its desks are what tells the admin
  whose it is. <date>, #PRNUM.»; *Open findings*: 88 removed; *Web history*: «#PRNUM — the users page …» (one
  line for the PR, extended by each commit).

### Commit 4 — the users page
- **Filters.** `UsersFilters` gains `role?: UserRoleFilter` (`UserRoleFilter = NonNullable<AdminUsersRequest['role']>`,
  `'user' | 'owner' | 'admin'`). `usersFiltersOf` reads `role` by `RULES.role`; `usersParamsOf` writes it;
  `usersRequestOf` asks for it. **`useUsersFilters({ fixedRole }: { fixedRole?: UserRoleFilter } = {})`**: with
  `fixedRole`, the address's role is dropped on read and on write, `request.role = fixedRole`, `anyApplied`
  ignores role; without it, `chooseRole(role?)` replaces the address and returns to page 1, and `anyApplied`
  counts it. `useAdminUsersList` passes `fixedRole` through and, without it, adds `filters.role: { label,
  value: role ?? 'all', options: [all, user, owner, admin], choose }` (`''` ignored, as the state's).
- **Row.** `userRowView(row, { words, english, now })`, `words: Catalogue['spaceLinks']['usersList']['row']`;
  `UserRowView` gains `role: string` (`words.roles[row.role]`), `signIn: string` (`password && google` →
  `both`, `google` only → `google`, else `password`), `joined: string` (`updatedOn(row.joinedAt, language,
  now)`). `state` reads `words.states`. The owners list and `useEmailAccount` pass `copy.spaceLinks.usersList.row`.
- **`useUsersList()`** = `useAdminUsersList({ words: copy.spaceLinks.usersList })` plus `columns`,
  `allSpacesDeleted`, `spacesWords: { owned, desk, none }`, `you`, `selfId` (`useSession((state) =>
  state.status === 'authenticated' ? state.user.id : null)`), `cardLine(row) = words.cardLine({ role, signIn,
  joined })`.
- **`UsersList({ actions, deletedSpacesLink })`** — `actions: (row: AdminUserRow) => ReactNode` (the page's
  slot, as the spaces list's): a `section` like `OwnersList` (`aria-label`, `aria-busy`, `tabIndex={-1}`,
  `useFocusKeeper`), then `DataTable cardsBelow="lg"`: columns **name** (`text-label`, `dir="auto"`), **email**
  (`dir="ltr" whitespace-nowrap`), **role**, **signIn**, **joined**, **spaces** (`UserSpaces`), **state**
  (`Badge`), **actions** (`meta: { className: 'w-px' }`: `row.id === selfId` → `<span className="text-caption
  text-muted-foreground">{you}</span>`, else `actions(row.row)`); `renderCard` → `UserCard`; `loading`,
  `empty` (`ListState`), `toolbar` (`UsersToolbar` with the role chips), `pagination` (`ListPagination`).
  Columns memoised on their words, `actions`, `deletedSpacesLink` and `selfId`.
- **`UserCard`:** name and email (`dir="ltr"`), the `cardLine` caption, `UserSpaces`, then at the end the
  state `Badge` and the actions (or «أنت»), as `OwnerCard`.
- **`UserSpaces({ row, words, allSpacesDeleted, deletedSpacesLink })`:** a column of groups — owned:
  `<span className="text-caption text-muted-foreground">{words.owned}</span>` + `OwnerSpaces` (which already
  draws finding 50's link); desks: `{words.desk}` + neutral badges (name marked); neither → `<span
  aria-hidden="true">—</span><span className="sr-only">{words.none}</span>`.
- **Link from a person.** `LinkTarget`'s person gains `role: 'USER' | 'OWNER'` and `deskIds: readonly
  number[]`; `useLinkOwnerDialog`'s person side sets `user: target.person.role === 'USER'` (so a user's link
  says `becomesOwner`); `useSpaceChoices({ enabled, linked, desks })` adds `atDesk` to each option;
  `SpaceCombobox` disables `linked || atDesk` and captions `linked ? words.linked : atDesk ? words.atDesk :
  owners`. `useOwnerActions` passes `role: 'OWNER'`, `deskIds: row.row.receptionSpaces.map(id)`.
- **`useUserLinkActions(row: AdminUserRow, { ownersLink, deletedSpacesLink })`** (exported) → `{ trigger: {
  label: menu({ name: isolate(name) }) }, link: Item, role: Item & { lead?: { label; to } }, dialog: { kind:
  'link'; target: LinkTarget } | { kind: 'role'; person: { id; name; role: 'USER' | 'ADMIN' } } | null, close }`,
  `Item = { label: string; disabled: boolean; reason?: string; run: () => void }`. In this commit, `role` is
  absent (commit 5 adds it). **Link:** `row.role === 'ADMIN'` → disabled, `isAdmin`; `row.isSuspended` →
  disabled, `suspended`; else opens `{ from: 'person', person: { id, name, role, spaceIds, deskIds } }`.
- **`UserLinkDialog({ actions, returnFocus })`** (exported): renders `LinkOwnerDialog` for `dialog.kind ===
  'link'` (commit 5: `RoleDialog` for `'role'`), `onClose = actions.close`.
- **Page.** `pages/dashboard/admin/UsersPage.tsx`: `<PageHeader />` + `<UsersList actions={userActions}
  deletedSpacesLink={ADMIN_DELETED_SPACES_PATH} />`, `userActions = (row) => <UserActionsMenu row={row} />` made
  once at module level. **`UserActionsMenu({ row })`:** `const links = useUserLinkActions(row, { ownersLink:
  adminOwnersSearchPath(row.email), deletedSpacesLink: ADMIN_DELETED_SPACES_PATH })`; a `DropdownMenu` whose
  trigger is `Button variant="ghost" size="icon"` (`EllipsisVerticalIcon aria-hidden`, `aria-label={links.trigger.label}`,
  `ref={trigger}`), `DropdownMenuContent align="end"` with `MenuActionItem`s; then `<UserLinkDialog
  actions={links} returnFocus={trigger} />`. **`MenuActionItem({ item, destructive? })`:** a `DropdownMenuItem`
  (`disabled`, `onSelect={item.run}`) whose content is the label with the reason under it (`text-caption
  text-muted-foreground`), as `OwnerActionsMenu`'s; a `lead` renders a second item, `asChild` around a
  `Link to={lead.to}` (fallback in §13). `navigation.ts`: `adminOwnersSearchPath(q: string) =
  \`${ADMIN_OWNERS_PATH}?q=${encodeURIComponent(q)}\``. `routes.tsx`: `ADMIN_PAGES.users` lazy-loads `UsersPage`.
- **Words, `spaceLinks.usersList`:** `label` Users / المستخدمون · `search` Search / بحث · `searchPlaceholder`
  Name or email / الاسم أو البريد · `role` Role / الدور · `roles` { `all` All / الكل; `user` User / مستخدم; `owner`
  Owner / مالك; `admin` Admin / أدمن } · `state` Status / الحالة · `states` { `all` All / الكل; `active` Active /
  نشط; `suspended` Suspended / موقوف } · `columns` { `name` Name / الاسم; `email` Email / البريد; `role` Role /
  الدور; `signIn` Sign-in / طريقة الدخول; `joined` Joined / انضم; `spaces` Spaces / المساحات; `state` Status /
  الحالة; `actions` Actions / إجراءات } · `row` { `states` { `active` Active / نشط; `suspended` Suspended /
  موقوف }; `roles` { `USER` User / مستخدم; `OWNER` Owner / مالك; `ADMIN` Admin / أدمن }; `signIn` { `password`
  Password / كلمة مرور; `google` Google / Google; `both` Password and Google / كلمة مرور وGoogle } } · `owned`
  Owner / مالك · `desk` Front desk / استقبال · `noSpaces` No spaces / لا مساحات · `allSpacesDeleted` (as
  `ownersList`'s, both languages) · `you` You / أنت · `cardLine({role, signIn, joined})` {role} · {signIn} ·
  {joined} (both) · `count({count})` Users: {count} / عدد المستخدمين: {count} · `empty` No users yet / لا يوجد
  مستخدمون بعد · `emptyHint` Everyone who creates an account shows here. / يظهر هنا كل من ينشئ حسابًا. · `noMatch`
  No users match / لا يوجد مستخدمون يطابقون البحث · `clearFilters` Clear filters / مسح الفلاتر · `loadFailed` We
  couldn’t load the users / تعذّر تحميل المستخدمين · `pagination` { `label` Pages of the users list / صفحات
  قائمة المستخدمين; the rest as `ownersList.pagination`'s }.
- **Words, `spaceLinks.userActions`:** `menu({name})` Actions: {name} / إجراءات: {name} · `link` Link to a space
  / ربط بمساحة · `isAdmin` An admin’s account — never linked to a space / حساب أدمن — لا يُربط بمساحة ·
  `suspended` The account is suspended — restore it first / الحساب موقوف — استرجعه أولًا. **`spaceLinks.choices.atDesk`**
  Front desk / مكتب استقبال.
- **Docs:** `space-links.md` — *What it does* (the users page on the dashboard), *Who uses it*, *How it
  composes* («The users page on the web reads the same list under its key with the role from the address; its
  row menu is composed by the page from this capability's link and role items and `users`' account items»),
  *Behaviour* («**The users page on the web.**» — columns, cards below 1024, the two chip groups, the address,
  «أنت», the spaces and desks, finding 50's line, the states; «ربط بمساحة» from a person, held for an admin or a
  suspended account, a user's link saying the role line, the person's spaces «مربوطة» and desks «مكتب
  استقبال»), *Web decisions* (one line each, dated, `#PRNUM`: the users list's core shared with the owners
  list (Stronger 2); the owners page never reads a role from its address (Stronger 3); role and state chips,
  no sheet (design issue 1); cards below 1024 (A7, Stronger 1); the row menu composed by the page, this
  capability exporting `useUserLinkActions` and `UserLinkDialog` (Stronger 7); the admin's own row «أنت»;
  desks unavailable in the space choices (Stronger 4)), *Code map* (`users-list/`, `user-actions/`, the
  exports), *Web history*. `architecture.md` §2 *Built so far*: after the owners page, «the users page, which
  shows [space-links](../features/space-links.md)' users list, its rows' menu composed from space-links' and
  [users](../features/users.md)' actions». `overview.md` › Space links: «… and the admin's owners page …, and
  the admin's users page, with its search, role and state filters and linking a person, on the dashboard».

### Commit 5 — the role change (`space-links`)
- **Repository:** `changeRole(userId: number, role: AdminRoleChoice): Promise<undefined>` →
  `api.put('/admin/users/{userId}/role', { role } satisfies ChangeRoleRequest)`.
- **`useChangeRole()`:** `useMutation<undefined, AppError, { userId; name; role: AdminRoleChoice }>`;
  `onSuccess`: `await refresh()` (`useRefreshAdmin`), then `toast(role === 'ADMIN' ? nowAdmin({ name: isolate(name) })
  : nowUser(…))`, words read with `currentCopy()`.
- **`useRoleDialog(person: { id; name; role: 'USER' | 'ADMIN' }, close)`** → `{ title, line, confirm: { label,
  run, busy, blocked }, cancelLabel, failure }`; `toAdmin = person.role === 'USER'`; `run` sends the other role,
  then `close()`; a refusal → `failure` (`useRefusalView(refusal, lines.failed, lines.refusals)`), the dialog open.
- **`RoleDialog({ person, onClose, returnFocus })`:** as `UnlinkOwnerDialog`: `AlertDialog open`, title (the
  name isolated), description, `FormFailure`, footer `AlertDialogCancel` «رجوع» and `Button
  variant="destructive" loading disabled={blocked}`.
- **`useUserLinkActions` adds `role`:** `OWNER` with spaces → disabled, `roleFollowsLinks`, `lead: { label:
  unlinkThem, to: ownersLink }`; `OWNER` with none → disabled, `allSpacesDeleted`, `lead: { label: deletedSpaces,
  to: deletedSpacesLink }`; `USER` with desks → disabled, `atDesk`; else opens `{ kind: 'role', person }`.
  `UserLinkDialog` renders `RoleDialog`. `UserActionsMenu` puts «تغيير الدور» (and its lead) first.
- **Words, `spaceLinks.userActions`:** `changeRole` Change role / تغيير الدور · `roleFollowsLinks` Their role
  follows their links — unlink them first / دوره يتبع روابطه — فُكّ ربطه أولًا · `unlinkThem` Unlink them / فك
  روابطه · `deletedSpaces` Deleted spaces / المساحات المحذوفة · `atDesk` They work a front desk — its space’s owner
  ends that first / يعمل في مكتب استقبال — يفكّه مالك المساحة أولًا.
- **Words, `spaceLinks.role`:** `toAdminTitle({name})` Make {name} an admin? / جعل {name} أدمن؟ · `toAdminLine`
  They get every admin power over the platform and all its spaces, and their sessions end so they sign in
  again. / يحصل على كل صلاحيات الإدارة على المنصة وكل مساحاتها، وتنتهي جلساته فيدخل من جديد. · `toAdmin` Make them an
  admin / جعله أدمن · `toUserTitle({name})` Make {name} a user again? / إعادة {name} مستخدمًا؟ · `toUserLine` They
  lose the admin dashboard at once, and their sessions end. / يفقد لوحة الإدارة فورًا، وتنتهي جلساته. · `toUser`
  Make them a user / إعادته مستخدمًا · `cancel` Back / رجوع · `failed` The role didn’t change / لم يتغيّر الدور ·
  `refusals` { `ACCOUNT_HAS_LINKS` They hold a link the list doesn’t show — to a deleted space, or one made
  meanwhile; their role can’t change until it ends. / له رابط بمساحة لا تُظهره القائمة — بمساحة محذوفة، أو رابط
  جديد؛ لا يتغيّر دوره حتى ينتهي.; `ACCOUNT_PASSWORD_PENDING` They haven’t changed their temporary password yet;
  they can’t be made an admin until they sign in and change it. / لم يغيّر كلمة المرور المؤقتة بعد؛ لا يُجعل
  أدمن حتى يدخل ويغيّرها.; `not_found` This account no longer exists. / لم يعد هذا الحساب موجودًا. }
  (`OWN_ACCOUNT`, `LAST_ADMIN`: the errors catalogue's lines) · `nowAdmin({name})` {name} is now an admin; their
  sessions ended / أصبح {name} أدمن، وانتهت جلساته · `nowUser({name})` {name} is a user again; their sessions ended
  / عاد {name} مستخدمًا، وانتهت جلساته.
- **Docs:** `space-links.md` — *Behaviour* («**The role change on the web.**»: who is offered which, the held
  cases and their leads, the two dialogs, the refusals, the toast after the admin's views arrive), *Web
  decisions* (the role item held for every case the row can see, the refusal for the rest (Stronger 5, design
  issue 3); the dialog's action stays until the answer (design issue 2); a toast though the row shows the role
  (Stronger 9)), *Code map* (`role/`), *Web history*. `overview.md` Space links: «… and changing a person's role».

### Commit 6 — suspend and restore (`users`)
- **Repository:** `setSuspended(userId, request: SetSuspendedRequest): Promise<undefined>` →
  `api.put('/admin/users/{userId}/suspended', request)`.
- **`types/AccountPerson.ts`:** `{ id; name; email; isSuspended; hasPassword: boolean; ownsSpaces: boolean;
  atDesk: boolean }` — the page maps the row: `hasPassword: row.signIn.password`, `ownsSpaces: row.role ===
  'OWNER'`, `atDesk: row.receptionSpaces.length > 0` (`users` never reads `space-links`' row).
- **`hooks/useRefreshAdmin.ts`** (users' own, architecture §7): `invalidateQueries({ queryKey: ['admin'] },
  { cancelRefetch: false })`.
- **`useSetSuspended()`:** `useMutation<undefined, AppError, { userId; name; isSuspended }>`; `onSuccess`: `await
  refresh()`, then `toast(isSuspended ? suspended({ name }) : restored({ name }))` (name isolated, `currentCopy()`).
- **`useSuspendDialog(person, close)`** → `{ title, lines: string[] (line, then ownerLine if ownsSpaces, then
  deskLine if atDesk), confirm, cancelLabel, failure }`; refusals by `useRefusalView(…, failed, refusals)`.
- **`SuspendDialog({ person, onClose, returnFocus })`:** as `RoleDialog`, each line its own `<p>` in the
  description.
- **`useAccountActions(person)`** (exported) → `{ issue: Item (commit 7), state: Item & { destructive: boolean },
  dialog: 'suspend' | 'issue' | null, close }`: active → «إيقاف», destructive, opens `'suspend'`; suspended →
  «استرجاع الحساب», runs the restore at once; its failure → `toastRestoreFailed(name, refusal)`.
- **`AccountActionDialog({ actions, person, returnFocus })`** (exported): `SuspendDialog` for `'suspend'`
  (commit 7: `IssuePasswordDialog` for `'issue'`).
- **`components/account-actions/accountToasts.tsx`:** `toastRestoreFailed(name, refusal)` → `toast.error(failed
  line, { description: <RefusalText refusal={refusal} title={…} />, duration: Infinity })`, as `spaces`' `toastFailed`.
- **`RefusalText`** = `ActionRefusal` moved (`git mv`, renamed, body unchanged), exported from `@shared/forms`;
  `spaces`' `actionToasts.tsx` imports it from there.
- **Page:** `UserActionsMenu` adds `const account = useAccountActions(personOf(row))` (the mapping inline),
  a `DropdownMenuSeparator`, the state item (`variant="destructive"` when `destructive`), and `<AccountActionDialog
  actions={account} person={…} returnFocus={trigger} />`.
- **Words, `users.accountActions`:** `suspend` Suspend / إيقاف · `restore` Restore the account / استرجاع الحساب ·
  `restored({name})` {name}’s account restored / استُرجع حساب {name} · `restoreFailed({name})` We couldn’t restore
  {name}’s account / تعذّر استرجاع حساب {name}. **`users.suspend`:** `title({name})` Suspend {name}? / إيقاف {name}؟
  · `line` All their sessions end at once, and they can’t sign in until you restore the account. / تنتهي كل
  جلساته فورًا ولا يدخل حتى تسترجع حسابه. · `ownerLine` Their spaces stay verified; the Masaha team edits them only
  once they’re unlinked. / تبقى مساحاته موثّقة، ولا يعدّلها فريق مساحة إلا بعد فك ربطه. · `deskLine` Their
  front-desk link is kept; they can’t work the desk until restored. / يبقى رابطه بمكتب الاستقبال، ولا يعمل فيه حتى
  يُسترجع. · `confirm` Suspend / إيقاف · `cancel` Back / رجوع · `failed` The account wasn’t suspended / لم يُوقَف
  الحساب · `refusals.not_found` This account no longer exists. / لم يعد هذا الحساب موجودًا. (`OWN_ACCOUNT`,
  `LAST_ADMIN`: the errors catalogue's) · `suspended({name})` {name} suspended; their sessions ended / أُوقف
  {name}، وانتهت جلساته.
- **Docs:** `users.md` — *What it does* (web: suspend and restore from the users page), *Behaviour* («**Suspending
  and restoring on the web.**»), *Web decisions* (the account actions exported as a hook and a dialog for the
  page's menu (Stronger 7); the suspension asks first, destructive, its consequence for an owner and a
  receptionist (design issue 5); a restore at once, no undo (design issue 6); the admin scope refreshed whole,
  the action pending until it arrives; the new operations in their own folders (finding 82)), *Code map*, *Web
  history*. `architecture.md` › Forms: «… and `RefusalText` renders such a refusal under a toast's title».

### Commit 7 — issue a temporary password (`users`)
- **Repository:** `issueTemporaryPassword(userId): Promise<IssuedTemporaryPassword>` →
  `api.post('/admin/users/{userId}/temporary-password')`.
- **`useIssueTemporaryPassword()`:** `useMutation<IssuedTemporaryPassword, AppError, number>`, `gcTime: 0`.
- **`useIssuePasswordDialog(person, close)`** → `{ title, line, confirm, cancelLabel, failure, issued: string |
  null, done }`: `confirm.run` issues; on success `issued = answer.temporaryPassword` (hook state only) and the
  mutation `reset()`; a refusal → `failure`, open. `done()` clears `issued` and closes.
- **`IssuePasswordDialog({ person, onClose, returnFocus })`:** while `issued === null`, the `AlertDialog`
  confirm (as `RoleDialog`, its action the default variant); then `<TemporaryPasswordDialog kind="issued"
  person={{ userId, name, email }} password={issued} onDone={() => { done(); returnFocus.current?.focus(); }} />`.
- **`TemporaryPasswordDialogInput.kind: 'created' | 'issued'`** (required); `line = kind === 'issued' ?
  lines.issuedLine : lines.line`. `OwnersPage`'s slot passes `kind="created"`.
- **`useAccountActions.issue`:** suspended → disabled, `suspendedFirst`; `!hasPassword` → disabled, `googleOnly`
  (AD-021); else opens `'issue'`. `UserActionsMenu` puts it after «ربط بمساحة», before the separator.
- **Words, `users.accountActions`:** `issue` Issue a temporary password / إصدار كلمة مرور مؤقتة · `googleOnly`
  A Google account — they recover it through Google / حساب Google — يستعيده من Google · `suspendedFirst` The account
  is suspended — restore it first / الحساب موقوف — استرجعه أولًا. **`users.issuePassword`:** `title({name})` Issue a
  temporary password for {name}? / إصدار كلمة مرور مؤقتة لـ {name}؟ · `line` To recover the account once you’ve
  confirmed who they are. Their current password stops working and their sessions end; they must change it at the
  next sign-in. / لاستعادة الحساب بعد التأكد من هويته. تُلغى كلمة مروره الحالية وتنتهي جلساته، ويُطلب منه تغييرها
  عند الدخول التالي. · `confirm` Issue / إصدار · `cancel` Back / رجوع · `failed` No password was issued / لم تُصدَر
  كلمة مرور · `refusals` { `ACCOUNT_SUSPENDED` The account is suspended — restore it first. / الحساب موقوف —
  استرجعه أولًا.; `not_found` This account no longer exists. / لم يعد هذا الحساب موجودًا. } (`OWN_ACCOUNT`,
  `GOOGLE_ONLY_ACCOUNT`: the errors catalogue's). **`users.temporaryPassword.issuedLine`** Hand it over once you’ve
  confirmed who they are; they’ll be asked to change it at their next sign-in. / سلّمها له بعد التأكد من هويته؛
  سيُطلب منه تغييرها عند الدخول التالي.
- **Docs:** `users.md` — *What it does*, *Behaviour* («**Issuing a temporary password on the web.**»: the confirm,
  the one-time dialog with the issued line, held for a suspended or a Google-only account), *Web decisions* (a
  confirm before the issue, felt by the person (P9); the dialog's `kind`; nothing in the cache; AD-021), *Web
  history*. `overview.md` › Users: «… ; on the dashboard, the admin's suspension and restore and temporary password
  for an account, from the users page». Finding 49: «*<date>, #PRNUM:* its screen — the users page issues a temporary
  password from a person's row, so a lost answer is recovered there.»

## 10. Tests — each with its lane, title and the break that must make it fail

**For every test** (testing §3): seen failing first in its lane; for code that already exists, the named
break is made once, **the red output recorded in the report**, then restored. Expectations by hand. Every
`AdminUserRow` literal carries `receptionSpaces`. Each confirm that names a consequence and each disabled
action has its own deliberate break (marked ★).

| C | Lane · file | Title | The break |
|---|---|---|---|
| 1 | Component · `DataTable.component.test.tsx` | keeps each row a card until 1024px when asked, and shows the table from there | the query ignores `cardsBelow` |
| 2 | (existing, unchanged) owners list hook and component tests, `useUsersFilters` | — | a refactor mistake |
| 3 | Unit · `userRowView.unit.test.ts` | names each reception desk in the interface's language, an English-only one marked as English | desks read from `row.spaces`, or no `lang` |
| 3 | Component · `AddOwner.component.test.tsx` ★ | shows the account's reception desks beside its spaces before the upgrade | the desks' row not drawn |
| 4 | Unit · `usersFiltersOf.unit.test.ts` | reads the role by the contract's rule, an unknown one dropped | `?role=gone` kept |
| 4 | Unit · same | writes the role to the address and asks for it | `role` dropped from the params or the request |
| 4 | Component · `useUsersFilters.component.test.tsx` | chooses a role, replacing the address and returning to the first page | `push`, or the page kept |
| 4 | Component · same | with its role fixed, never reads a role from the address nor counts it as a filter | `fixedRole` ignored |
| 4 | Unit · `userRowView.unit.test.ts` (`it.each`) | words the role, how the account signs in, and when it joined | `both` mapped to `google` |
| 4 | Component · `useUsersList.component.test.tsx` | asks for the address's search, role, state and page | `role` left out of the request |
| 4 | Component · same | marks the signed-in admin's own row | `selfId` always null |
| 4 | Component · `UsersList.component.test.tsx` | shows each person's role, sign-in, joined date, spaces, reception desks and state | the desks' group not drawn |
| 4 | Component · same | keeps a card per person until 1024px | `cardsBelow` not passed |
| 4 | Component · same | shows «You» in place of the actions on the admin's own row | the slot called for the own row |
| 4 | Component · same | filters by role and by state from the chips | the role chips' `choose` not wired |
| 4 | Component · same | has no accessibility violations | (vitest-axe) a chip group unnamed |
| 4 | Component · `useLinkOwnerDialog.component.test.tsx` ★ | from a user's row, says their account becomes an owner's | `user: false` on the person side |
| 4 | Component · `LinkOwnerDialog.component.test.tsx` ★ | from a person, offers their reception desks as unavailable, saying so | `atDesk` not disabling |
| 4 | Component · `useUserLinkActions.component.test.tsx` ★ (`it.each`) | offers to link a user or an owner, and holds it, with its reason, for an admin and a suspended account | the reason dropped, or an admin enabled |
| 4 | Component · `UserActionsMenu.component.test.tsx` | opens the link dialog from the row's menu, and returns the focus to the menu | `returnFocus` not passed |
| 4 | Component · `routes.component.test.tsx` | shows the admin's users page under its title, with the users | the route left on its placeholder |
| 5 | Unit · `spaceLinksRepository.unit.test.ts` | changes a person's role | method, path or body changed |
| 5 | Component · `useUserLinkActions.component.test.tsx` ★ (`it.each`) | holds the role change, with its reason, for an owner (leading to their links), an owner of deleted spaces (leading to the deleted spaces), and a receptionist | a reason or a lead dropped, or a receptionist enabled |
| 5 | Component · same | offers the role change to a user with no link and to an admin | an admin held |
| 5 | Component · `useRoleDialog.component.test.tsx` ★ | says what making a user an admin does, and what making an admin a user does | the lines swapped |
| 5 | Component · same | sends the other role, waits for the admin's views, then says so | the same role sent, or the toast before the refresh |
| 5 | Component · same (`it.each`) | words each refusal in the dialog, which stays open | `lines.refusals` removed, or `close()` on a failure |
| 5 | Component · `RoleDialog.component.test.tsx` | opens on Back, its action destructive and staying until the answer, with no accessibility violations | `AlertDialogAction` that closes on click |
| 5 | Component · `UserActionsMenu.component.test.tsx` | puts the role change first, with its lead when held | the lead not rendered |
| 6 | Unit · `usersRepository.unit.test.ts` | suspends and restores an account | path or body changed |
| 6 | Component · `useSuspendDialog.component.test.tsx` ★ | says the sessions end, and what stays for an owner's spaces and a receptionist's desk | the owner line or the desk line not added |
| 6 | Component · same | suspends, waits for the admin's views, then says so | `isSuspended: false` sent |
| 6 | Component · same (`it.each`) | words each refusal in the dialog, which stays open | `close()` on a failure |
| 6 | Component · `SuspendDialog.component.test.tsx` | opens on Back, its action destructive and staying until the answer, with no accessibility violations | `AlertDialogAction` |
| 6 | Component · `useAccountActions.component.test.tsx` | offers to suspend an active account and to restore a suspended one | the items swapped |
| 6 | Component · same | restores at once, then says so; a refusal is said in a toast | a dialog asked, or the failure silent |
| 6 | (existing, unchanged) `spaces`' toast and menu tests | — | the `RefusalText` move |
| 7 | Unit · `usersRepository.unit.test.ts` | issues a temporary password | method or path changed |
| 7 | Component · `useAccountActions.component.test.tsx` ★ (`it.each`) | holds the temporary password, with its reason, for a suspended account and a Google-only one | `googleOnly` dropped, or enabled |
| 7 | Component · `useIssuePasswordDialog.component.test.tsx` ★ | says what issuing does before it is done | the line not drawn (the confirm skipped) |
| 7 | Component · same | issues, hands the password on once, and keeps none in the cache | `gcTime: 0` or `reset()` removed |
| 7 | Component · same (`it.each`) | words each refusal in the confirm, which stays open | `close()` on a failure |
| 7 | Component · `IssuePasswordDialog.component.test.tsx` | after the issue, shows the one-time dialog, with no way out but «Done» | the password dialog not rendered |
| 7 | Component · `TemporaryPasswordDialog.component.test.tsx` | says an issued password is changed at the next sign-in, a new account's at the first | `kind` ignored |

The refusals of each `it.each`: role — `ACCOUNT_HAS_LINKS`, `ACCOUNT_PASSWORD_PENDING`, `LAST_ADMIN`,
`OWN_ACCOUNT`, `not_found`; suspend — `OWN_ACCOUNT`, `LAST_ADMIN`, `not_found`; issue — `OWN_ACCOUNT`,
`ACCOUNT_SUSPENDED`, `GOOGLE_ONLY_ACCOUNT`, `not_found`. **Not run:** `test:api` (no `apps/api` or
`packages/shared` change; CI runs it); E2E (end of project).

## 11. Review Focus — inputs no planned test exercises

- A Google-only account and `LAST_ADMIN` in a real browser (the local run has neither; the component lane proves both).
- Another admin changing the same person meanwhile: the row is stale until the refresh; the refusals say why.
- «فك روابطه» searches the owners page by the email, which may also list longer emails that hold it.
- The link dialog's person-side `validation` line («… — اختر غيره») when the person no longer exists.
- A 429 on the role, suspend, restore or issue (the shared `useRefusalView` is proven elsewhere).
- Mixed-direction names in titles and toasts, Arabic and English.
- The site's first download: `users`' new admin hooks must be tree-shaken out of it (`check:build` refuses the
  dashboard chunk only; compare the site entry's size before and after in the report).
- Finding 87's margin (§13 records it).
- More than 20 people, a page past the last (the shared pieces are proven by the owners and spaces lists).

## 12. The commits

1. `feat(design-system): keep a table's cards to lg` (47)
2. `refactor(space-links): share the users list's core` (50)
3. `fix(space-links): show front desks before upgrade` (49)
4. `feat(space-links): add the admin's users page` (45) — **the PR's title**
5. `feat(space-links): change a person's role` (41)
6. `feat(users): suspend and restore an account` (43)
7. `feat(users): issue a temporary password` (39)

Each body says *why*. Code, tests and the documents of a unit go in its commit. Stage by path (`git add
<path> …`), `git status` before each commit; never `git add -A` / `git add .`. No tool attribution. A fix
before the push folds into its commit: `git commit --fixup=<sha>`, then `GIT_SEQUENCE_EDITOR=: git rebase -i
--autosquash $(git merge-base HEAD origin/main)`.

## 13. The procedure and the verification

### First checks (before any edit), in `C:\dev\masaha\app`
1. `git status` clean, on `main`; `git fetch origin`; `git switch main && git pull --ff-only`.
2. **PR 3 merged:** `gh pr list --state merged --head feat/admin-owner-links --json number,mergeCommit`; empty → stop.
3. **`git diff --name-status 02cc70ae origin/main`** (the plan's PR 3 head). Read `C:\dev\masaha\workspace\WORKER_A\OWNERS\4_REPORT_PR3.md`
   (its fixes, its departures). A code file this plan names that changed in a way the plan does not cover →
   **stop and ask.** `packages/shared` changed → `npm run build -w @masaha/shared` before any web check.
4. The next free finding number from `docs/architecture/findings/README.md` on `origin/main` → `<n>`.
5. **Checks, with their fallback:**
   - The layer's `DropdownMenuItem` forwards `asChild` (read `shared/design-system/components/**/DropdownMenu.tsx`).
     If not: the lead item uses `onSelect={() => navigate(lead.to)}` (`useNavigate` in `UserActionsMenu`).
   - `useSession`'s `SessionState` has `user` when `status === 'authenticated'` (read `shared/session/model.ts`); else stop and ask.
   - `adminUsersQuerySchema.shape.role` exists (`packages/shared/src/space-links/requests.ts`); else stop and ask.
   - The `DataTable` test's `matchMedia` stub reads any `min-width` (it does today); keep it.
6. Branch: `git switch --no-track -c feat/admin-users origin/main`.

### Per commit
`npm run lint` and `npm run typecheck`; focused runs of the touched files while working.

### On the head, once each
First: no `vitest` running under `C:\dev\masaha\app-b\` —
`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'app-b' -and $_.CommandLine -match 'vitest' }`
must be empty (else wait). Then: `npm run test:unit` · `npm run test:component` (**record the time of
`routes.component.test.tsx` › "lists the owner's eleven pages"**, finding 87; a timeout there → stop and ask,
never raise the limit) · `$env:NODE_ENV='production'; npm run build; Remove-Item Env:NODE_ENV` · `npm run
check:build` · `npm run check:classes` · `npm run format:check` · `npm run check:links`. **Not run:** `test:api`
(no API or shared change; CI runs it).

### The real run
- `docker start masaha-postgres-1` (never `db:up`; never `npm ci`); the API on 3320 (`npm run dev -w @masaha/api`,
  worker A's `masaha_dev`, migrated to `main`), the web on 5320 (`npm run dev`).
- **Data:** the seeded admin; the demo owner and the demo receptionist (`demo.ts`). If the receptionist is
  missing, create one as the demo owner (`POST /api/v1/auth/login`, then `POST /manage/spaces/:id/staff`).
  Register two users at `/register` (passwords). Everything else through the screens.
- **Browser:** the `playwright` MCP tools if present, else local headless Chrome over CDP; say which. Arabic
  light and English dark, at 390, 768 and 1440.
- **Cases:** the list (table at 1440, cards at 768 and 390); the search, the role and state chips, the address
  after Back; «أنت» on the admin's row; the owner's and the receptionist's spaces and desks; an owner's held
  role with «فك روابطه» landing on the owners page; a user made admin, then a user again (both dialogs,
  toasts); a receptionist's held role; issue a temporary password to user 1 (the confirm, the one-time dialog
  with the issued line, «تم» after «نسخ», the handover), then «جعله أدمن» refused `ACCOUNT_PASSWORD_PENDING`
  and «ربط بمساحة» refused `ACCOUNT_PASSWORD_PENDING`; link user 2 to a space (the role line; the space's
  owners); the receptionist's link dialog (its desk «مكتب استقبال»); suspend the demo owner (the owner line),
  restore it at once (the toast); an admin's row (link held); the add-owner sheet with the receptionist's email
  (the upgrade confirm lists the desk, finding 88); the empty no-match state.
- **Not performed, by design:** a Google-only account (no Google sign-in locally) and `LAST_ADMIN` (a race):
  the component lane proves them. Any other case not performed → §2's stop rule.
- Screenshots to `C:\dev\masaha\workspace\WORKER_A\USERS\shots\` (moved there if saved elsewhere); never committed.
- Stop the servers by PID (`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object {
  $_.CommandLine -match 'C:\\dev\\masaha\\app\\' }`, `Stop-Process -Id …`); `Get-NetTCPConnection -LocalPort
  3320,5320 -State Listen` empty; `git status` clean.

### Push and the PR
1. `git grep -n "#PRNUM" HEAD`; the next number: `gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number'` + 1 (SETTINGS may take it first: check at that moment).
2. In Git Bash: `git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#<n>/g'" origin/main..HEAD`,
   then `git update-ref -d refs/original/refs/heads/feat/admin-users`; `git grep -n "#PRNUM" HEAD` empty; `git diff origin/main --stat` the same files.
3. `git push -u origin feat/admin-users`, then `gh pr create --assignee @me --label feat --label area:web
   --label area:docs --label area:design-system` (commit 1 is the layer's), title = commit 4's subject, the
   description per workflow §3 (Summary; Scope / Acceptance criteria / Out of scope; Change type; Evidence —
   run and not run; Screenshots — attached by the owner; the Definition of Done). Confirm the number matches.
4. `gh pr checks <n>` green on the pushed head's SHA; `gh pr view <n> --json mergeStateStatus` `CLEAN`.
5. The conflict check: for each other open PR (SETTINGS's), `git fetch origin <its head ref>` and `git
   merge-tree --write-tree origin/feat/admin-users origin/<other>`; record it.
6. The report `C:\dev\masaha\workspace\WORKER_A\USERS\4_REPORT_PR1.md`, written **as you go** (after the first
   checks, after each commit with its sha, subject length, red line and green line, after each break with its
   red output, after the real run, after the push), UTF-8. **Never merge.** This PR is reviewed in a separate
   conversation (over 25 files; a design-system change).

### The stop rule (as `OWNERS\3_EXEC_PROMPT_PR3.md` §2)
**A test you cannot run stops the work.** A test **failing** because its code is not written yet is the
plan's red step — normal. A test, lane or command you **cannot run** is not: it errors before any test runs
(the database unreachable, Docker down, a port taken, a module or `dist` missing, a migration pending, `No
test files found`, a Vitest or TypeScript startup error, the whole run timing out, a crash with no result); a
break you could not make or run; a real-run case you could not perform. **Then stop at once** — never skip,
`.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never mock what the
plan does not, never run a narrower command and call it the lane, never call it "flaky" and move on. Write the
command, its exact error and where you were into the report, and reply with `Status: STOPPED`.
**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do not
choose it yourself. **A break that stays green:** stop, unless it is plainly your own test's defect — then
strengthen the test, see the break go red, and state it as a departure.
**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line. A break counts only when you saw it red. No "all tests pass".

### Stop and ask
- PR 3 not merged; or the base diff changes a code file this plan names in a way it does not cover; or SETTINGS's open PR edits one of this plan's code files.
- Anything would need `apps/api`, `packages/shared`, the schema, a dependency, or a design-system change other than `cardsBelow`.
- `useSession` or `adminUsersQuerySchema.shape.role` not as §13 reads them.
- An existing owners-list, spaces or `spaces`-toast test fails after commit 2 or the `RefusalText` move, and the cause is not the move's own mistake.
- `check:build` fails because a module of this item reaches the site's first download.
- The routes test times out (finding 87).
- Three fixes of one failure have failed; a decision this plan does not settle.

## 14. Decisions needed from the owner

1. **Size: ≈ 88 files, above the prompt's ~60.** Keep **one PR** (the owner's U3; seven atomic commits, a
   separate review conversation either way), or **two** (alternative A: PR A commits 1–5 ≈ 59 files, PR B
   commits 6–7 ≈ 31, cut after A merges). *Recommended: two*, as OWNERS was split again at ≈ 85; the plan
   serves both unchanged.
2. **Stronger 1 — `DataTable cardsBelow`** (a design-system change, its own commit). *Recommended: yes.*
3. **Stronger 2–8** (the users list's core shared; `fixedRole`; desks unavailable in the space choices; the role
   item held up front; `RefusalText` in `shared/forms`; the page composing the menu; the dialog's `kind`).
   *Recommended: all.*
4. **Design issues 1–9** — each approved or not. *Recommended: all* (issue 1's fallback is written).
5. **Finding `<n>`** (the spaces list's table at 768) recorded, not folded (alternative B). *Recommended: record.*
6. **Finding 49's dated line.** *Recommended: yes.*
7. **The words** (§9), both languages, «أدمن» as the role's word, «استقبال» for a desk in the row.

## Appendix — steps mapped to Claude Code skills (only a map; no step depends on them)

| Step | Skill |
|---|---|
| The first checks, the branch | `start-work-item` |
| Each test seen failing, each break made | `superpowers:test-driven-development` |
| A failure's cause | `superpowers:systematic-debugging` |
| Every claim with its command | `superpowers:verification-before-completion` |
| Scope check, commits, `#PRNUM`, push, the PR | `open-pr` |
| The report once CI is green and `CLEAN` | `final-report` |

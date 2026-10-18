# OWNERS — the admin's owners page, adding and linking an owner, the editor naming its owners (web) — the plan

> Written 2026-10-18 from `origin/main` `5e8c979d` (#84, #85, #86 merged; the highest issue/PR number then: #86).
> Built as **three pull requests** (the owner's choice, 2026-10-18), each cut from `main` once the one before
> it has merged: **PR 1** `feat/admin-owners` (≈ 50 files), **PR 2** `feat/admin-add-owner` (≈ 48),
> **PR 3** `feat/admin-owner-links` (≈ 45). One plan, three reports.
> The executor may be any capable coding agent: no step depends on a Claude skill (the appendix is only a map).

> **Approved by the owner, 2026-10-18 — binding on every executor of this plan:**
> - §14's six points, as recommended: **1** `owners` leaves architecture §3 and `dashboardOnly.ts` (PR 3);
>   **2** the unlink reads the space's owners on every opening; **3** `sendMultipart`'s `signal` stays
>   optional; **4** design issues 1–12 all approved (issue 7's `unsaved` in the slot included); **5** findings
>   82 and 83 recorded (PR 2).
> - **6 — the words:** «مالك» in actions and short phrases («إضافة مالك»، «ربط مالك»، «فك ربط {name}»،
>   «مالك · {space}»), as the approved design writes them; «صاحب المساحة» stays the role's name (the
>   glossary's term, `terms.owner`, the page title «أصحاب المساحات»). **PR 1's commit 3 adds one line to
>   `docs/project/glossary.md`'s *Owner* row** saying so (the short form «مالك» in the dashboard's actions).
>   No existing line is reworded.
> - **Reports:** `4_REPORT_PR1.md`, `4_REPORT_PR2.md`, `4_REPORT_PR3.md` in this folder (not §13's names).
>   Screenshots in `shots\pr1\`, `shots\pr2\`, `shots\pr3\`.
> - **Each PR has its own execution prompt** (`3_EXEC_PROMPT_PR<n>.md`); an executor builds only the PR its
>   prompt names, and the next PR starts only after the previous one has merged.
> - **Added 2026-10-18 (security, PR 2's adding an owner):** after `EMAIL_HAS_ACCOUNT`, the upgrade step
>   **shows whose account it is before the admin confirms** — the account's name, when it joined and its
>   current spaces, read with `GET /admin/users?q=<the email>` (the users list PR 1 builds) — and says
>   «تأكّد أنه الشخص المقصود: سيصبح مالكًا لهذه المساحة». A mistyped email that belongs to someone else must
>   never become an owner by one click. No API change. Test it (a component test: the confirm shows the
>   matched account; with no exact email match, no upgrade is offered).

## 1. Summary

The admin gets the **owners page** (A6): the users list filtered to the owners, with a search and a state
filter, each owner's spaces in the row, and an owner whose spaces are all deleted pointed to the deleted
spaces (finding 50's screen). Then (PR 2) the admin **adds an owner** (A5) from that page and sees the new
account's **temporary password once**, in a dialog that cannot be dismissed by accident and that records how
it was handed over. Last (PR 3), the admin **links** an owner from either end and **unlinks** one (A4), and a
space's **editor names its owners** with an unlink per owner, or offers the link on an unverified space
(finding 59, resolved).
First, #85's two leftovers (D4). Nothing in `apps/api`, `packages/shared`, the schema or the dependencies.

## 2. The contract

### Scope
- **PR 1:** #85's leftovers (D4); the spaces list's paging, page links, states, paused search and focus
  keeper shared inside `features/space-links`; the users list's read, row, search and state filter in
  `features/space-links`; the owners page at `/dashboard/admin/owners`, replacing its placeholder; finding
  50's line and its dated note.
- **PR 2:** the design system's `Combobox` taking a caller's own search; `lineParts` moved to
  `shared/localisation`; the one-time password dialog in `features/users`; adding an owner; findings 82 and
  83 recorded.
- **PR 3:** linking from a person (the owners row's menu) and from a space (the editor); unlinking; the
  editor's notice naming its owners; finding 59 resolved.

### Acceptance criteria
PR 1
- [ ] The gallery's failed move or cover is titled «تعذّر تغيير ترتيب الصور», a failed removal «تعذّر حذف الصورة», never «تعذّر تحميل الصور».
- [ ] `sendMultipart` and `uploadPhoto` require their progress callback; the "no callback" branch and its test are gone.
- [ ] `/dashboard/admin/owners` shows the owners (`GET /admin/users?role=owner`): name, email (under the name until 1024 px, its own column from there), linked spaces, state; a card per owner below 768 px.
- [ ] The search (name or email, written to the address once typing pauses) and the state chips (الكل · نشط · موقوف) live in the address (`?q=&state=&page=`), read by the contract's rules; the pages are links.
- [ ] An `OWNER` row with no space reads «كل مساحاته محذوفة — استرجع المساحة لفك ربطه», the whole line a link to `/dashboard/admin/spaces?status=deleted`.
- [ ] Loading, failure (with its reference and «إعادة المحاولة», waiting out a 429), empty and no-match states; the focus moves to the list when the row that held it leaves.
- [ ] The spaces list behaves exactly as before (its tests unchanged and green).
- [ ] Both catalogues complete; RTL/LTR, light/dark, phone/768/desktop checked in a real run.

PR 2
- [ ] `Combobox` with `search` shows the caller's options unfiltered, hands it each change of the text, and shows `loading` in place of the empty text.
- [ ] «إضافة مالك», above the list at its end, opens the add sheet: name, email, one space (searched on the server, each option with its state and owners); «سيُنشأ حساب ويظهر رمز مرور مؤقت مرة واحدة — جهّز طريقة تسليمه.» and «إنشاء حساب وربط»; after `EMAIL_HAS_ACCOUNT`, «سيُرقّى حسابه…» and «ترقية وربط», sent with `upgradeExisting: true`; `ACCOUNT_IS_ADMIN`, `ACCOUNT_SUSPENDED`, `ALREADY_OWNER` worded on the form.
- [ ] A new account's password shows once: no X, no Escape, no click outside; «تم» enabled only after «نسخ»; asks واتساب · شفهيًا · أخرى and sends the handover; no password stays in the query cache.
- [ ] Both catalogues complete; RTL/LTR, light/dark, phone/768/desktop checked in a real run.

PR 3
- [ ] The owners row's menu: «ربط بمساحة» (disabled with its reason for a suspended account) and «فك الربط من {space}» per space; the editor: «فك ربط {name}» per owner of a verified space, «ربط مالك» on an unverified one.
- [ ] Each link and unlink says its consequence before the act; refusals (`ACCOUNT_IS_ADMIN`, `ACCOUNT_SUSPENDED`, `RECEPTION_LINK_ACTIVE`, `invalid_choice`, a space deleted meanwhile) are worded in the dialog, which stays open.
- [ ] Unlinking is an `AlertDialog`, destructive, «تصبح … غير موثّقة وتختفي حالتها المباشرة…» when it is the last owner.
- [ ] The verified notice reads «يعدّلها {names}» from `AdminSpace.owners`; finding 59 Resolved.
- [ ] Both catalogues complete; RTL/LTR, light/dark, phone/768/desktop checked in a real run.

### Out of scope
The users page and its actions (USERS: role change, suspension, issuing a temporary password, AD-021);
reception links in a user's row (DI-24, step 6); any API, shared-package, schema or dependency change; any
design-system change other than the `Combobox` search; the data reports' link in the verified notice; the
gallery's other test gaps (the owner's rule).

## 3. The reading done

From `origin/main`: CLAUDE.md; `docs/development/workflow.md`; `testing.md`; `engineering-principles.md` §1–3;
`docs/frontend/architecture.md` (whole); `design-system/foundation.md` §5, §9, §10, §12; `localisation.md`
(catalogues, content in two languages); `docs/features/space-links.md`, `users.md`, `spaces.md` (behaviour, web
decisions, code map); `docs/api/api-contract.md` (§1–4, *Spaces (the admin)*, *Owners (the admin)*, *Users
(the admin)*, §6); ADR 0009 (decision 2); findings 45, 49, 50, 59, 69 and the open findings' titles; the
documentation map's deferred table (nothing triggered); `docs/design/INDEX.md` (§43, §44, §46, the fix-phase
parameters); `docs/design/prototype/Admin owners.html`, `Admin users.html`, `Admin space edit.html` and
`masaha/admin.jsx` (`TempPassDialog`, `LinkOwnerDialog`, `unlinkLine`); `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md`
(A3–A7, AD-012, AD-021, every amendment) and `DECISIONS_SHARED.md` (P1, P5, P8, P9 and amendments);
`GALLERY_REPORT.md` › *Left alone*. Code: `features/space-links/**`, `features/users/**`, `features/spaces/`
(`index.ts`, `components/editor/{SpaceEditor,VerifiedNotice}.tsx`, `hooks/editor/{useSpaceEditor,useSpaceQuery,useSpaceName}.ts`,
`hooks/photos/{usePhotoGallery,usePhotoRemove}.ts`, `hooks/add/*`, `hooks/delete/useDeleteSpace.ts`,
`hooks/useRefreshAdmin.ts`, `components/{photos/PhotoRemoveDialog,delete/DeleteSpaceDialog,toast/*}.tsx`,
`services/lineParts.ts`, `repository/spacesRepository.ts`), `shared/forms/**`, `shared/uploads/**`,
`shared/copy/{arabic,english}/{spaceLinks,users,spaces,errors,terms}.ts`, the design system's `Combobox`,
`Dialog`, `AlertDialog`, `Field`, `Button`, `DataTable`, `DropdownMenu`, `ToggleGroup`, `RadioGroup`,
`pages/dashboard/{routes.tsx,navigation.ts,admin/*}`, `routes.component.test.tsx`, `scripts/dashboardOnly.ts`,
`packages/shared/src/{space-links,users}/*`, `apps/api/src/db/seed/demo.ts` (one verified space, an owner).

## 4. The settled decisions, as they will be built

The prompt's D1–D5 (2026-10-17) and the owner's three answers during planning (2026-10-18):

- **O1 — `Combobox` takes a caller's search** (PR 2's first commit). The layer's `Combobox` filters only
  the options it holds (cmdk's own filter; its search box not exposed), and both lists it must choose from
  are paged, so `ComboboxContent` gains an optional controlled `search` that turns cmdk's filter off, and a
  `loading` line. D5's "no design-system component" is overridden for this one extension, by the owner.
- **O2 — the users list lives in `features/space-links`**, beside the spaces list (overrides D2's
  `features/users` for the list only). *Why:* a web capability carries the name of the backend module it
  calls, and `GET /admin/users` is the `space-links` module's composed read (`admin-users/`), as the spaces
  list is; the paged list's pieces are reused, not copied; `space-links` is dashboard-only. USERS later adds
  the `users` row actions through a slot, as `spaces` fills the spaces list's.
- **O3 — three PRs** (≈ 50, 48 and 45 files), so each stays under the prompt's ~70; each is cut from
  `main` once the one before it has merged, because each builds on the last one's files.
- **D1.1 — the owners page** is `GET /admin/users?role=owner`, `role` fixed by its own hook; the search and
  the state filter are the users list's (`?q=&state=&page=`), so USERS reuses the read, the row view, the
  filters' address and the query.
- **D1.2 — adding an owner**: one space (a `Combobox` searching the spaces), the line before the act, the
  submit's words, the three refusals on the form; the upgrade is asked only after the server's
  `EMAIL_HAS_ACCOUNT`, as the contract and the design's `?sheet=add&email=` frame have it.
- **D1.3 — the one-time password dialog lives in `features/users`.** *Why (the dependency rule):* the
  temporary password and its handover (`POST /admin/users/:userId/temporary-password/handover`) are the
  `users` capability's, and USERS's issued password shows the same dialog; `space-links` cannot import
  `users` (no sibling imports), so the add sheet takes it through a **slot** the page fills, as the spaces
  list takes its row actions ("a component that combines several capabilities lives in the page").
- **D1.4 — one way to link** (`LinkOwnerDialog`, two entries): from a space, a `Combobox` of one person
  (owners and users by name or email; `state=active`, admins dropped, each option saying what it is); from
  a person, a `Combobox` of one space (its state badges and owners, a space already theirs disabled
  «مربوطة»). Both say the consequence before the act.
- **D1.5 — unlinking**: «فك ربط {name}» (editor) / «فك الربط من {space}» (owners row), one item each, an
  `AlertDialog` with a destructive action (P9); the consequence read fresh from the space when it opens.
- **D1.6 — the editor names its owners** from `AdminSpace.owners`, with the unlink items; an unverified
  space's editor offers the link. Finding 59 Resolved.
- **D2 (as amended by O2)** — `features/space-links`: the users list, the owners list, the add sheet, the
  link and unlink dialogs and their hooks; `features/users`: the password dialog; `pages/dashboard/admin/OwnersPage.tsx`,
  replacing the `owners` route's placeholder (`ADMIN_NAV` already lists it; `routes.tsx` gives it a lazy page).
- **D3** — finding 50's line on screen, no API change, a dated line in finding 50.
- **D4** — commit 1 of PR 1: the gallery's removal and order failures titled by their action;
  `onProgress` required. Nothing else from the gallery.
- **D5** — out: the users page, reception links, API changes, design-system changes (O1 aside).

## 5. Stronger decisions

1. **Architecture §3 names an `owners` feature for the admin's linking; D2 puts linking in `space-links`.**
   What: PR 3's link commit removes `owners` from §3's capabilities table and from the "names match the
   backend" paragraph (leaving `staff`), and from `apps/web/scripts/dashboardOnly.ts`. Why: a document
   must not describe a capability that will never exist; the list and the table are one fact in two places
   the document says must agree. Cost: one paragraph and one list entry; `dashboardOnly.ts` is a build
   check, so PR 3 is reviewed in a separate conversation (it is already over 25 files). **Recommended.**
2. **The unlink reads the space's owners when it opens, from both entries** (`GET /admin/spaces/:spaceId`,
   its `owners`). Why: a person's row (`AdminUserRow.spaces`) cannot tell whether they are the space's last
   owner, and the editor's copy may be stale; a destructive consequence is said from the server's answer.
   Cost: one GET per opening, and a line that waits (a `Skeleton`); if the read fails, a conditional line
   that stays true. **Recommended.**
3. **Second instances generalised, inside their owners** (engineering principles §1): the spaces list's
   pagination view, page links, states, paused search, page-in-range and focus keeper become shared pieces
   of `space-links` (PR 1, commit 2); `lineParts` moves to `shared/localisation` (PR 2, commit 2), because a
   second capability names a space inside a line. Each feature keeps its own eight-line `NamedLine`
   render: `shared/localisation` has no component, and giving it one is not worth an architecture change.
   Cost: ~14 files of pure refactor, proven by the existing tests unchanged. **Recommended.**
4. **`sendMultipart`'s `signal` is optional by the same pattern** (production always passes it). D4 takes
   `onProgress` only; **recommended: leave `signal`** (the owner's rule: nothing else from the gallery).
5. **The person's role is never predicted at an unlink** (see design issue 1); **the role line at a link is
   said only when it is certain** (a `USER` becomes an owner and signs in again).
6. No rule of the documents is weakened. The vocabulary point (design issue 11) is the owner's words.

## 6. Related findings

| Finding | Folded? | Why · cost |
|---|---|---|
| **59** the verified editor cannot name its owner | **Yes, PR 3** (D1.6) | Its API half landed (#82); resolved by the notice and the unlink. |
| **50** an owner whose only spaces are deleted stays an owner | **Its screen, PR 1** (D3) | Stays Resolved; a dated line records the screen. |
| 69 the owners endpoint refuses a deleted space with an unnamed code | No | API-side (the schema's type check); the web sends numbers, so its screens meet `invalid_choice`; an API change is out (D5). |
| 49 a lost answer loses the temporary password | No (resolved) | Recovered by USERS's issued password; nothing here. |
| 27, 45 dashboard chunks / the table library | No | `check:build` covers them; this item adds only dashboard code (`space-links` is dashboard-only). |
| 73, 74 the gallery | No | The owner's rule: no other gallery gap. |

**New (PR 2, range 82–83):** **82** — `features/users` keeps several operations flat in `hooks/` and
`components/` (architecture §3's one folder per operation); the new dialog takes `temporary-password/`
folders and the old files are left alone (no drive-by). **83** — `ALREADY_OWNER` names no account, so
the add form cannot open the link dialog for that owner as the design's «اربطه بالمساحة» does
(`INDEX.md` `?link=<user>&space=<id>`); resolves when the 409 carries the owner's id (worker B, a contract
change) or the owner accepts the wording.

## 7. The files

`apps/web` and `docs` only. Paths below are from `apps/web/src/` unless they start with `docs/` or `apps/`.
**Shared with worker B's PACKAGES** (re-read on the latest `origin/main` before editing; each side its own
lines; a conflict there takes the documents' fast path): `docs/project/overview.md` (the *Built* lines of
Users / Space links / Spaces), `docs/architecture/findings/README.md` (index lines 82–83 and 59's move).
This item does not edit `docs/api/api-contract.md`.

### PR 1 (≈ 50 files)
- **Commit 1:** `features/spaces/hooks/photos/usePhotoGallery.ts` · `features/spaces/components/photos/PhotosSection.component.test.tsx` ·
  `shared/copy/{english,arabic}/spaces.ts` · `shared/uploads/services/sendMultipart.ts` (+ `.unit.test.ts`) ·
  `features/spaces/repository/spacesRepository.ts` · `docs/features/spaces.md` (one history line).
- **Commit 2 (refactor, `features/space-links/`):** new `components/ListPagination.tsx` (moved from
  `components/admin-list/AdminSpacesPagination.tsx`), `components/ListState.tsx` (moved from
  `components/admin-list/AdminSpacesState.tsx`), `types/PaginationView.ts`, `types/ListStateView.ts`,
  `services/paginationView.ts`, `hooks/usePausedSearch.ts`, `hooks/usePageInRange.ts`, `hooks/useFocusKeeper.ts`;
  edited `hooks/admin-list/useAdminSpacesList.ts`, `hooks/admin-list/useAdminSpacesFilters.ts`,
  `components/admin-list/AdminSpacesList.tsx`.
- **Commit 3:** `features/space-links/`: `repository/spaceLinksRepository.ts` (+ `.unit.test.ts`),
  `hooks/queryKeys.ts`, `types/AdminUsersRequest.ts`, `types/UsersFilters.ts`, `types/UserRowView.ts`,
  `services/usersFiltersOf.ts` (+ unit test), `services/userRowView.ts` (+ unit test),
  `hooks/users-list/useAdminUsersQuery.ts`, `hooks/users-list/useUsersFilters.ts` (+ component test),
  `hooks/owners-list/useOwnersList.ts` (+ component test), `components/owners-list/{OwnersList,OwnersToolbar,OwnerCard,OwnerSpaces}.tsx`
  (+ `OwnersList.component.test.tsx`), `index.ts`; `pages/dashboard/admin/OwnersPage.tsx`,
  `pages/dashboard/{routes.tsx,navigation.ts,routes.component.test.tsx}`; `shared/copy/{english,arabic}/spaceLinks.ts`;
  `docs/features/space-links.md`, `docs/frontend/architecture.md` (§2 *Built so far*), `docs/project/overview.md`,
  `docs/architecture/findings/50-an-owner-whose-only-spaces-are-deleted-stays-an-owner.md`.

### PR 2 (≈ 48 files)
- **Commit 1:** `shared/design-system/components/fields/Combobox/Combobox.tsx` (+ `.component.test.tsx`) ·
  `pages/showcase/sections/fields/ComboboxSection.tsx` · `pages/showcase/fixtures.json` ·
  `docs/frontend/design-system/foundation.md` (§12, the Combobox row).
- **Commit 2:** `git mv features/spaces/services/lineParts.ts shared/localisation/lineParts.ts` and its
  `.unit.test.ts` · `shared/localisation/index.ts` · `features/spaces/components/toast/actionToasts.tsx` ·
  `features/spaces/hooks/menu/useSpaceActionsMenu.ts` · `docs/frontend/localisation.md` (one line).
- **Commit 3:** `features/users/`: `repository/usersRepository.ts` (+ unit test), `hooks/temporary-password/{useHandover,useTemporaryPasswordDialog}.ts`
  (+ component test of the second), `components/temporary-password/TemporaryPasswordDialog.tsx` (+ component test),
  `index.ts`; `shared/copy/{english,arabic}/users.ts`; `docs/features/users.md`;
  `docs/architecture/findings/82-the-users-feature-keeps-several-operations-flat.md`, `docs/architecture/findings/README.md`.
- **Commit 4:** `features/space-links/`: `repository/spaceLinksRepository.ts` (+ test), `hooks/queryKeys.ts`,
  `hooks/useRefreshAdmin.ts`, `hooks/usePausedText.ts`, `hooks/useSpaceChoices.ts`, `components/SpaceCombobox.tsx`,
  `types/{SpaceChoiceView,TemporaryPasswordSlot,NamedLineView}.ts`, `services/namedLine.ts`, `components/NamedLine.tsx`,
  `components/toast/namedToast.tsx`, `hooks/add-owner/{useAddOwner,useAddOwnerForm}.ts` (+ component test of the second),
  `components/add-owner/AddOwner.tsx` (+ component test), `index.ts`; `pages/dashboard/admin/OwnersPage.tsx`,
  `pages/dashboard/routes.component.test.tsx`;
  `shared/copy/{english,arabic}/spaceLinks.ts`; `docs/features/space-links.md`;
  `docs/architecture/findings/83-already-owner-names-no-account.md`, `docs/architecture/findings/README.md`.

### PR 3 (≈ 45 files)
- **Commit 1:** `features/space-links/`: repository (+ test), `hooks/queryKeys.ts`, `types/LinkTarget.ts`,
  `hooks/useSpaceChoices.ts`, `components/SpaceCombobox.tsx`, `types/SpaceChoiceView.ts` (an option already the person's),
  `hooks/link/{usePersonChoices,useLinkOwner,useLinkOwnerDialog}.ts` (+ component test of the dialog's hook),
  `components/link/{LinkOwnerDialog,PersonCombobox}.tsx` (+ `LinkOwnerDialog.component.test.tsx`),
  `hooks/unlink/{useSpaceOwnersQuery,useUnlinkOwner,useUnlinkOwnerDialog}.ts` (+ component test of the dialog's hook),
  `components/unlink/UnlinkOwnerDialog.tsx` (+ component test), `hooks/owner-actions/useOwnerActions.ts`,
  `components/owner-actions/OwnerActionsMenu.tsx` (+ component test), `components/owners-list/{OwnersList,OwnerCard}.tsx`;
  `shared/copy/{english,arabic}/spaceLinks.ts`; `apps/web/scripts/dashboardOnly.ts`; `docs/features/space-links.md`,
  `docs/frontend/architecture.md` (§3), `docs/project/overview.md`.
- **Commit 2:** `features/spaces/`: `types/OwnersSlot.ts`, `components/editor/{SpaceEditor,VerifiedNotice}.tsx`,
  `components/editor/SpaceEditor.component.test.tsx`, `hooks/editor/useSpaceEditor.ts`, `index.ts`;
  `features/space-links/`: `hooks/space-owners/useSpaceOwnersActions.ts`, `components/space-owners/SpaceOwnersActions.tsx`
  (+ component test), `index.ts`; `pages/dashboard/admin/SpaceEditPage.tsx`, `pages/dashboard/navigation.ts`;
  `shared/copy/{english,arabic}/{spaces,spaceLinks}.ts`; `docs/features/{spaces,space-links}.md`,
  `docs/architecture/findings/59-the-verified-spaces-editor-cannot-name-its-owner.md`,
  `docs/architecture/findings/README.md`, `docs/project/overview.md`.

## 8. Design issues (built only once the reply approves them)

1. **The prototype's unlink says the person «لا يبقى مالكًا» when their row shows one space.** A deleted
   space's link still counts for the role and no read shows it (finding 50), so that line can be false.
   → Say only the space's consequence; never predict the person's role at an unlink.
2. **«مالك مسبقًا — اربطه بالمساحة» links to the link dialog for that owner,** but the 409 carries no
   user id. → The form says «هذا البريد لمالك مسبقًا — اربطه بالمساحة من صفّه في القائمة.»; finding 83.
3. **«الحساب موقوف — استرجعه أولًا» links to the users page,** a placeholder until USERS. → Words only,
   no link (no entry point that leads nowhere); the owners row's disabled «ربط بمساحة» gives the same reason as text.
4. **The owners page's single three-choice state filter sits in a `FilterSheet`.** P5: a single status
   filter of four or fewer choices is `ToggleGroup` chips; A7: a filter is a chip. → Chips «الكل · نشط ·
   موقوف» by the count, at every width; no sheet on this page.
5. **«نسخ» can fail** (clipboard blocked, or no secure context), and the prototype marks it copied anyway.
   → On a failure: «تعذّر النسخ — حدّدها وانسخها يدويًا.» under the password (selectable), and «تم» is
   enabled all the same, so the dialog never traps the admin.
6. **A handover refused because the password is no longer pending** (the person has already changed it)
   would trap the admin. → That refusal (`TEMPORARY_PASSWORD_NOT_PENDING`, or a 404) closes the dialog
   with an error toast «لم تُسجَّل طريقة التسليم» and its line; any other failure stays in the dialog.
7. **Linking from an unverified editor with unsaved changes** turns it read-only and drops them. → While
   the editor has unsaved changes, «ربط مالك» is disabled with «احفظ التغييرات أو تجاهلها أولًا» beside it
   (the slot receives `unsaved`). *If not approved: leave it out, and it goes to Review Focus.*
8. **The verified notice's «بلاغات <المساحة>» path (AD-012)** leads to the data reports, not built. → Left out.
9. **The owner's name in the notice's title links to the owners page `?q=<email>`,** but `AdminSpace.owners`
   carries no email and a name search can match others. → The title stays text; the unlink buttons are the actions.
10. **The prototype's unlink closes on its action** (`AlertDialogAction`). → A `Button variant="destructive"
    loading` in the footer, so the dialog stays open until the answer and a failure shows inside it (P8), as
    the photo removal does; Cancel keeps the first focus.
11. **Vocabulary:** the design and the prompt say «مالك», the glossary «صاحب المساحة» (`terms.owner`, the
    errors). → New lines use «مالك», as the editor's «يعدّلها مالكها» already does; the page title stays
    «أصحاب المساحات». The owner approves the words.
12. **«إضافة مالك» beside the count, inside the toolbar.** P1 (amended): a list's add sits in a row above the
    list, at its end, at every width. → Above the list, as «إضافة مساحة».

## 9. What is built — interfaces, words, states

Every new decision and history line in a document ends with the commit's date and **`#PRNUM`** (replaced
before the push, §13). A name inside a line is set apart: a person's name isolated (`isolate`), a space's
name its own element with `lang`/`dir` when English-only in Arabic (`lineParts`, `NamedLine`).

### PR 1 · commit 1 — #85's leftovers
- `usePhotoGallery`: `useRefusalView(order.refusal, words.orderFailed, lines)` and `useRefusalView(removal.refusal, words.removeFailed, lines)`.
- Catalogue `spaces.editor.photos`: `orderFailed` — en «We couldn’t change the photos’ order» / ar «تعذّر تغيير ترتيب الصور»; `removeFailed` — en «We couldn’t delete the photo» / ar «تعذّر حذف الصورة».
- `MultipartUpload.onProgress: UploadProgress` (required); the body always sets `onUploadProgress`. `SpacesRepository.uploadPhoto(spaceId, file, onProgress: UploadProgress, signal?)` passes it straight.
- `sendMultipart.unit.test.ts`: delete «sends no progress callback when the caller wants none»; the other calls pass `onProgress: vi.fn()`. `grep -rn "uploadPhoto(\|sendMultipart(" src` must show no call without it.
- `spaces.md` › *Web history*: «#PRNUM — the gallery's failed moves and removals titled by their action, and `sendMultipart`'s progress always passed.»

### PR 1 · commit 2 — the list's pieces, shared inside `space-links` (no behaviour change)
- `types/PaginationView.ts`: `{ label; more; summary; previous: { label; search: string | null }; next: same; items: ({ kind: 'page'; page; label; search; current } | { kind: 'gap'; key: PageItem gap })[] }` — today's `NonNullable<AdminSpacesListView['pagination']>`.
- `services/paginationView.ts`: `paginationView({ current, total, words, searchOf }): PaginationView | null` (null for one page or none); `words`: `{ label; more; previous; next; page({page}); summary({page,total}) }` — the body moved from `useAdminSpacesList`, using `pageItems`.
- `components/ListPagination.tsx` (`{ pagination: PaginationView }`) and `components/ListState.tsx` (`{ list: ListStateView }`, `ListStateView = { status; failure: { title; message?; reference?; retryLabel; blocked; retry }; noMatch: { title; clearLabel; clear }; empty: { title; description } }`): the two components moved, renamed.
- `hooks/usePausedSearch.ts`: `usePausedSearch({ q, searchOf, write }) → { text, change, clear }` — the field's text, its resync when the address reads another search, and the 400 ms pause (moved with `SEARCH_PAUSE_MS`); `write(q)` is called once typing pauses, and the caller compares it with the address as it stands (keep `write` stable with a ref).
- `hooks/usePageInRange.ts`: `usePageInRange({ answer, placeholder, page, replacePage }) → pastLast` — the effect that shows the last page in place of one past it.
- `hooks/useFocusKeeper.ts`: `useFocusKeeper(rows) → { region, onFocus }` — the effect that moves the focus to the list when the element that held it leaves.
- The three spaces-list files use them. **Their existing tests stay as they are and pass** (no new test: a refactor is proven by the tests of the behaviour it keeps).

### PR 1 · commit 3 — the users list, the owners page
- **Repository:** `adminUsers(request: AdminUsersRequest): Promise<Page<AdminUserRow[]>>` → `api.getPage('/admin/users', { params: request })`; `AdminUsersRequest = Omit<Partial<AdminUsersQuery>, 'limit'>`.
- **Key:** `spaceLinksKeys.adminUsers(request) = ['admin', 'space-links', 'users', request]`.
- **`services/usersFiltersOf.ts`:** `usersFiltersOf(params): UsersFilters` (`{ q?; state?: 'active' | 'suspended'; page }`, each read by `adminUsersQuerySchema.shape`'s rule, an invalid one dropped); `usersParamsOf(filters)` (defaults left out); `usersRequestOf(filters): AdminUsersRequest`.
- **`hooks/users-list/useAdminUsersQuery(request)`:** `useQuery<Page<AdminUserRow[]>, AppError>`, `placeholderData: keepPreviousData`.
- **`hooks/users-list/useUsersFilters()`:** `{ filters, request, search: { text, change }, chooseState(state?), anyApplied, clearAll, searchOf(page), replacePage(page) }`; a choice replaces the address and returns to page 1; the search through `usePausedSearch`.
- **`services/userRowView(row, { english })`: `UserRowView`** = `{ id, row, name, email, state: { label, variant: 'success' | 'neutral' }, spaces: SpaceNameView[], allSpacesDeleted }` — `allSpacesDeleted` is `row.role === 'OWNER' && row.spaces.length === 0` (finding 50's rule); a space named in the interface's language, an English-only one marked `lang="en" dir="ltr"`.
- **`hooks/owners-list/useOwnersList()`:** request `{ ...filters.request, role: 'owner' }`; returns `status` (`loading | error | ready | noMatch | empty`), `rows`, `busy` (`isPlaceholderData`), `label`, `intro`, `columns`, `count`, `pagination` (`paginationView` with `ownersList.pagination`), `failure` (`useRefusalView`, the retry waiting out a 429), `empty`, `noMatch` (clear = `clearAll`), `filters: { search: { label, placeholder, text, change }, state: { label, value: 'all' | 'active' | 'suspended', options, choose } }`, `allSpacesDeleted` (the line). Uses `usePageInRange`.
- **`OwnersList({ deletedSpacesLink })`:** a `section` (`aria-label`, `aria-busy`, `tabIndex={-1}`, `useFocusKeeper`), the intro (`text-body-sm text-muted-foreground`), then `DataTable`: columns **name** (`text-label`, `dir="auto"`; under it the email, `text-caption text-muted-foreground lg:hidden`, `dir="ltr"`), **email** (`meta: { className: 'hidden lg:table-cell' }`, `dir="ltr" whitespace-nowrap`), **linked spaces** (`OwnerSpaces`), **state** (`Badge`); `renderCard` → `OwnerCard`; `loading` → the table's skeleton; `empty` → `ListState`; `toolbar` → `OwnersToolbar`; `pagination` → `ListPagination`.
- **`OwnersToolbar`:** `Field` «بحث» + `Input type="search"` (`SearchIcon`, `maxLength={NAME_MAX_LENGTH}`), then a row: the count (`aria-live="polite"`) and `ToggleGroup type="single"` (named «الحالة»; a click on the chip already on keeps it).
- **`OwnerSpaces`:** neutral `Badge`s, each name marked; or, for `allSpacesDeleted`, a `Link` to `deletedSpacesLink` (`text-body-sm text-muted-foreground underline underline-offset-4`), the whole line its text.
- **Page:** `OwnersPage` = `<PageHeader />` + `<OwnersList deletedSpacesLink={ADMIN_DELETED_SPACES_PATH} />`; `navigation.ts`: `ADMIN_DELETED_SPACES_PATH = \`${ADMIN_SPACES_PATH}?status=deleted\``; `routes.tsx`: `ADMIN_PAGES.owners` lazy-loads it.
- **Words, `spaceLinks.ownersList`** (en / ar): `label` Space owners / أصحاب المساحات · `intro` Linking an owner makes a space verified; from then on the owner edits it and alone sees its operations. / ربط مالك بمساحة يجعلها موثّقة؛ بعدها يعدّلها المالك ويرى تشغيلها وحده. · `search` Search / بحث · `searchPlaceholder` Name or email / الاسم أو البريد · `state` Status / الحالة · `states.all` All / الكل · `states.active` Active / نشط · `states.suspended` Suspended / موقوف · `columns.name` Name / الاسم · `columns.email` Email / البريد · `columns.spaces` Linked spaces / المساحات المرتبطة · `columns.state` Status / الحالة · `columns.actions` Actions / إجراءات · `allSpacesDeleted` All their spaces are deleted — restore the space to unlink them / كل مساحاته محذوفة — استرجع المساحة لفك ربطه · `count({count})` Space owners: {count} / عدد أصحاب المساحات: {count} · `empty` No space owners yet / لا يوجد أصحاب مساحات بعد · `emptyHint` Add an owner and link their space to verify it. / أضف مالكًا واربطه بمساحته لتصبح موثّقة. · `noMatch` No space owners match / لا يوجد أصحاب مساحات يطابقون البحث · `clearFilters` Clear filters / مسح الفلاتر · `loadFailed` We couldn’t load the space owners / تعذّر تحميل أصحاب المساحات · `pagination` { `label` Pages of the space owners list / صفحات قائمة أصحاب المساحات; `previous`, `next`, `page`, `summary`, `more` as `adminList.pagination`'s }.
- **Docs:** `space-links.md` — *What it does* (the owners page on the web), *How it composes* (the users list under `['admin', 'space-links', 'users', request]`), *Behaviour* (a paragraph «The owners page on the web»: columns, widths, chips, address, finding 50's line, states), *Web decisions* (O2 with its why; the owners page = the users list with `role=owner` fixed by its hook; the state chips (design issue 4); finding 50's line, the whole line a link; the list's pieces shared at their second instance), *Code map* (web), *Web history*. `architecture.md` §2 *Built so far*: add the owners page, which shows `space-links`' owners list. `overview.md` › *Built*, Space links: «… and the admin's owners page, with its search and state filter, on the dashboard». Finding 50: «*2026-10-18, #PRNUM:* its screen — an owner whose only spaces are deleted reads «كل مساحاته محذوفة — استرجع المساحة لفك ربطه» on the owners page, the line a link to the deleted spaces, where the restore begins the way out.»

### PR 2 · commit 1 — `Combobox` takes a caller's search
- `ComboboxContentProps` gains `search?: { value: string; onValueChange: (value: string) => void }` (*the caller's own search, for options found elsewhere: with it the list shows the options it is given as they are, never filtered*) and `loading?: ReactNode` (*shown in place of the empty text while the options are on their way*). `CommandPrimitive` gets `shouldFilter={search === undefined}`; `CommandPrimitive.Input` gets `value`/`onValueChange` when `search` is given; with `loading`, a `<div role="status">` (the empty text's classes) replaces `CommandPrimitive.Empty`.
- Showcase: a third example, «searched by its caller», whose section filters its own fixture options after a 300 ms pause to stand for a server; its words in `fixtures.json` beside the `areas` sample, in both languages.
- `foundation.md` §12, the Select / Combobox row: «· a caller that finds its own options, such as a server's search, passes `search` (the text and its change): the list shows the options as given, unfiltered, and `loading` stands in for the empty text while they come.»

### PR 2 · commit 2 — `lineParts` shared
`git mv` the file and its unit test to `shared/localisation/`; export it from `shared/localisation/index.ts`;
the two `spaces` importers read `@shared/localisation`. `localisation.md` › *Writing a line*: «A line that
names a record whose language may not be the interface's is cut around the name with `lineParts`, so the
name is set as its own element with its `lang` and `dir`; the line stays whole in the catalogue.»

### PR 2 · commit 3 — the one-time password dialog (`features/users`)
- **Repository:** `handOver(userId: number, request: HandoverRequest): Promise<undefined>` → `api.post('/admin/users/{userId}/temporary-password/handover', request)`.
- **`useHandover()`:** `useMutation<undefined, AppError, { userId; channel: HandoverChannel }>`, `gcTime: 0`.
- **`useTemporaryPasswordDialog({ person: { userId, name, email }, password, onDone })`** returns `{ title, person, password, copy: { label, copied, run }, copyFailed: string | null, line, channel: { label, value, options, choose, error, ref }, done: { label, disabled, reason, busy, run }, failure: FormFailureView | null }`. `copy.run` writes with `navigator.clipboard.writeText`; success or failure, `copied` turns true (a failure also sets `copyFailed`, design issue 5). `done.run`: no channel → `error` «اختر طريقة التسليم» and the group focused (`ref`), nothing sent; else the handover — on success a toast (`currentCopy()` read then) and `onDone()`; `TEMPORARY_PASSWORD_NOT_PENDING` or a 404 → an error toast with its line and `onDone()` (design issue 6); any other failure → `failure` (`useRefusalView`, title «تعذّر تسجيل طريقة التسليم»), the dialog open, «تم» trying again.
- **`TemporaryPasswordDialog({ person, password, onDone })`:** `Dialog open` with no `onOpenChange`; `DialogContent` without `closeLabel` (no X), `onEscapeKeyDown` and `onInteractOutside` calling `preventDefault()`; header: title, and «{name} · {email}» (email `dir="ltr"`); the password in `rounded-lg bg-muted p-3`, `dir="ltr" text-heading-3 select-all`, with `Button size="sm" variant="outline"` «نسخ» → `CheckIcon` + «نُسخت»; the copy failure line; the handover line; `Field` «طريقة التسليم» (error) around `RadioGroup` (each `RadioGroupItem` in a horizontal `Field`); `FormFailure`; footer: the reason caption (`aria-describedby` of «تم») while not copied, and `Button` «تم» (`disabled` until copied, `loading` while the handover is sent).
- **Words, `users.temporaryPassword`** (en / ar): `title` Temporary password / كلمة المرور المؤقتة · `copy` Copy / نسخ · `copied` Copied / نُسخت · `copyFailed` We couldn’t copy it — select it and copy it by hand. / تعذّر النسخ — حدّدها وانسخها يدويًا. · `line` Hand it over; they’ll be asked to change it at their first sign-in. / سلّمها لصاحبها؛ سيُطلب منه تغييرها عند أول دخول. · `channel` How it was handed over / طريقة التسليم · `channels.WHATSAPP` WhatsApp / واتساب · `channels.IN_PERSON` In person / شفهيًا · `channels.OTHER` Other / أخرى · `chooseChannel` Choose how it was handed over / اختر طريقة التسليم · `copyFirst` Copy it first — it won’t be shown again / انسخها أولًا — لن تظهر مرة أخرى · `done` Done / تم · `recorded({name, channel})` Handover recorded: {name} · {channel} / سُجّلت طريقة التسليم: {name} · {channel} · `failed` We couldn’t record the handover / تعذّر تسجيل طريقة التسليم · `notRecorded` The handover wasn’t recorded / لم تُسجَّل طريقة التسليم.
- **Docs:** `users.md` — *What it does* (web: the one-time password dialog and its handover), *Behaviour* («The one-time password»), *Web decisions* (D1.3's where and why; no X, Escape or outside click, «تم» only after «نسخ» (A5); design issues 5 and 6; the handover keeps nothing in the cache), *Code map*, *Web history*. Finding 82 (Open) and its index line.

### PR 2 · commit 4 — adding an owner
- **Repository:** `addOwner(request: AddOwnerRequest): Promise<AddedOwner>` → `api.post('/admin/owners', request)`; `spaceChoices(q?: string): Promise<Page<AdminSpaceRow[]>>` → `api.getPage('/admin/spaces', { params: { q?, limit: 50 } })` (no status: the server leaves deleted spaces out).
- **Keys:** `spaceChoices(q) = ['admin', 'space-links', 'space-choices', q]`.
- **`useRefreshAdmin()`** (space-links' own): `() => client.invalidateQueries({ queryKey: ['admin'] }, { cancelRefetch: false })` — the whole admin scope, the editor's space included (a link changes its verification); a mutation that returns it stays pending until the lists have arrived.
- **`usePausedText(text)`:** the text once typing has paused 400 ms.
- **`useSpaceChoices({ enabled })`** → `{ search: { value, onValueChange }, loading?: string, empty: string, options: SpaceChoiceView[] }`; `SpaceChoiceView = { value: string; id; name: SpaceNameView; badges: BadgeView[] (the verification, «مخفية»); owners: string (names isolated, or `adminList.noOwner`); isVerified }`; the query `keepPreviousData`; a failure makes `empty` «تعذّر البحث؛ اكتب من جديد لإعادة المحاولة.». (PR 3 adds `linked: readonly number[]` to the input and `linked` to each option, for the person side.)
- **`SpaceCombobox({ choices, chosen, choose, placeholder, triggerRef, disabled })`:** `Combobox type="single"`, `ComboboxTrigger empty={!chosen}` (the chosen name, marked), `ComboboxContent` with `search`, `loading`, `emptyText`; each `ComboboxItem value={String(id)}`: the name, then a caption row with the badges and the owners. The chosen option is kept by the hook, so it stays on the trigger when the results change. (PR 3: an option already the person's is `disabled` and reads «مربوطة» in place of the owners.)
- **`useAddOwner()`:** `useMutation<AddedOwner, AppError, { request: AddOwnerRequest; spaceName: SpaceNameView }>`, `gcTime: 0`; `onSuccess`: `await refresh()`; an upgrade (`temporaryPassword === null`) toasts «رُقّي {name} إلى مالك ورُبط بـ {space}».
- **`useAddOwnerForm()`:** `useServerForm<{ name: string; email: string; spaceId: number | null }, AddOwnerRequest>` — `schema: addOwnerSchema`, `fields: ['name', 'email', 'spaceId']`, `prepare` (`spaceId ?? undefined`, so none is `required`), `fieldLines` and `failureLines` below, `failureTitle` «لم يُضَف المالك»; the space through `useController` (its `ref` on the trigger, so a refusal focuses it). `submit`: sends `{ ...request, ...(upgrade && { upgradeExisting: true }) }`; on `EMAIL_HAS_ACCOUNT` while not upgrading it **resolves** (no failure) and remembers the email (normalised as `emailSchema` does); `upgrade` holds while the watched email is that one. On success: a new account sets `added = { userId, name, email, temporaryPassword }`; either way the sheet closes, the form, the upgrade and the chosen space reset, and the mutation is `reset()` so the cache keeps no password. Returns the sheet's `open`/`setOpen`, the fields' bindings, labels and errors, the space's choices/chosen/choose, `notice` (`{ kind: 'create', text } | { kind: 'upgrade', title, text }`), `submit` (`label`, `run`, `isPending`, `blocked`), `failure`, `added`, `done` (clears `added`).
- **`AddOwner({ temporaryPassword: TemporaryPasswordSlot })`:** `Sheet` with `SheetTrigger` `Button` «إضافة مالك»; `SheetContent side="end" closeLabel`; header; a `form noValidate` with `SheetBody` (`Field`+`Input` name; `Field`+`Input type="email" dir="ltr"` email; `Field`+`SpaceCombobox`; the notice: `p text-body-sm text-muted-foreground`, or `Alert variant="info"` with title and text; `FormFailure`) and `SheetFooter` (`Button type="submit" className="w-full"`, `loading`, disabled while `blocked`); then `{added && temporaryPassword(added, done)}`.
- **`types/TemporaryPasswordSlot.ts`:** `AddedOwnerView = { userId; name; email; temporaryPassword: string }`; `TemporaryPasswordSlot = (added: AddedOwnerView, done: () => void) => ReactNode`.
- **`NamedLine`, `namedLine`, `namedToast`:** `namedLine(line, name): NamedLineView` (`lineParts` around the space's name, other values bound by the caller), `NamedLine({ line })` renders it, `toastNamed(line, name, description?)` calls `toast(<NamedLine …/>, …)` as `spaces`' `toastDone` does.
- **Page:** `OwnersPage` adds, above the list, `<div className="flex justify-end"><AddOwner temporaryPassword={temporaryPassword} /></div>`, with `temporaryPassword` made once at module level: `(added, done) => <TemporaryPasswordDialog person={{ userId: added.userId, name: added.name, email: added.email }} password={added.temporaryPassword} onDone={done} />`.
- **Words, `spaceLinks.addOwner`:** `open` / `title` Add owner / إضافة مالك · `description` Linked to one space; link more afterwards. / يُربط بمساحة واحدة؛ اربطه بغيرها بعد ذلك. · `close` Close / إغلاق · `name` Name / الاسم · `email` Email / البريد الإلكتروني · `emailPlaceholder` name@example.com (both) · `space` Space / المساحة · `chooseSpace` Choose the space / اختر المساحة · `willCreate` An account will be created and a temporary password shown once — have a way to hand it over ready. / سيُنشأ حساب ويظهر رمز مرور مؤقت مرة واحدة — جهّز طريقة تسليمه. · `hasAccount` This email has an account / لهذا البريد حساب · `willUpgrade` Their account will be upgraded to owner and linked to the space; it keeps its name and its way of signing in, and no password is shown. / سيُرقّى حسابه إلى مالك ويُربط بالمساحة، ويحتفظ باسمه وطريقة دخوله، ولا تظهر كلمة مرور. · `create` Create account and link / إنشاء حساب وربط · `upgrade` Upgrade and link / ترقية وربط · `failed` The owner wasn’t added / لم يُضَف المالك · `fieldErrors`: `name.required` Enter the name / أدخل الاسم; `email.required` Enter the email / أدخل البريد الإلكتروني; `email.invalid_format` Enter a valid email, e.g. name@example.com / أدخل بريدًا صحيحًا، مثل name@example.com; `spaceId.required` Choose the space / اختر المساحة; `spaceId.invalid_choice` That space is no longer available — choose another / لم تعد هذه المساحة متاحة — اختر غيرها · `refusals`: `ACCOUNT_IS_ADMIN` This email is an admin’s account, and an admin can’t be linked to a space. / هذا البريد لحساب أدمن، ولا يُربط أدمن بمساحة.; `ACCOUNT_SUSPENDED` This account is suspended; it can’t be linked until it’s restored. / هذا الحساب موقوف؛ لا يُربط حتى يُسترجع.; `ALREADY_OWNER` This email is already an owner’s — link them to the space from their row in the list. / هذا البريد لمالك مسبقًا — اربطه بالمساحة من صفّه في القائمة. (`RECEPTION_LINK_ACTIVE` keeps the errors catalogue's line) · `upgraded({name, space})` {name} upgraded to owner and linked to {space} / رُقّي {name} إلى مالك ورُبط بـ {space}.
- **Words, `spaceLinks.choices`** (shared by the add sheet and, in PR 3, the link dialog): `search` Search / بحث · `spacesPlaceholder` Space name / اسم المساحة · `spaces` Spaces / المساحات · `noResults` No results / لا نتائج · `searching` Searching… / جارٍ البحث… · `searchFailed` We couldn’t search; type again to retry. / تعذّر البحث؛ اكتب من جديد لإعادة المحاولة. PR 3 adds `peoplePlaceholder` Name or email / الاسم أو البريد · `people` People / الأشخاص · `linked` Linked / مربوطة · `owner({spaces})` Owner · {spaces} / مالك · {spaces} · `ownerOfNone` Owner / مالك · `user` User / مستخدم.
- **Docs:** `space-links.md` — *Behaviour* («Adding an owner on the web»), *Web decisions* (the upgrade asked only after `EMAIL_HAS_ACCOUNT`; the refusals on the form (design issues 2, 3); the space searched on the server (O1); the password dialog through the page's slot (D1.3); the sheet as the design draws it; no password in the cache), *Code map*, *Web history*. Finding 83 (Open) and its index line.

### PR 3 · commit 1 — linking and unlinking
- **Repository:** `linkOwner(spaceId, userId)` → `api.post('/admin/spaces/{spaceId}/owners', { userId })`; `unlinkOwner(spaceId, userId)` → `api.delete('/admin/spaces/{spaceId}/owners/{userId}')`; `personChoices(q?)` → `api.getPage('/admin/users', { params: { q?, state: 'active', limit: 50 } })`; `spaceOwners(spaceId)` → `api.get<AdminSpace>('/admin/spaces/{spaceId}')`, answering its `owners`.
- **Keys:** `personChoices(q)`, `spaceOwners(spaceId)` under `['admin', 'space-links', …]`.
- **`LinkTarget`** = `{ from: 'space'; space: { id; name: SpaceNameView }; addOwnerLink: string } | { from: 'person'; person: { id; name; spaceIds: number[] } }` (a space is linked from its editor only while unverified; a person from the owners page is an owner).
- **`usePersonChoices({ enabled })`:** like the spaces' choices; rows with `role === 'ADMIN'` dropped; each `{ value, id, name, email, role, kind }` — `kind` «مالك · {spaces}», «مالك», or «مستخدم».
- **`useLinkOwner()`:** mutation `{ spaceId, userId, toast: { person, space: SpaceNameView, wasVerified } }`, `gcTime: 0`; `onSuccess`: `await refresh()`, then «رُبط {person} بـ {space}», with «المساحة موثّقة الآن» when it was not.
- **`useLinkOwnerDialog(target, close)`** → `{ title: NamedLineView | string, description, field: { label, helper?, placeholder, error, triggerRef }, choices, chosen, choose, consequence: (NamedLineView | string)[], addOwner?: { text, link }, submit: { label, run, busy, blocked }, failure, closeLabel }`. Consequence, from the chosen option's own facts: a space unverified → «تصبح {space} موثّقة ويعدّلها مالكها، ولا يعدّلها فريق مساحة بعد الآن.»; verified → «يصبح مالكًا آخر لـ {space}؛ تبقى موثّقة.»; a chosen person who is a `USER` adds «ويصبح حسابه حساب مالك، ويُطلب منه الدخول من جديد.». `submit.run` with nothing chosen → `error` and the trigger focused. Refusals by `useRefusalView(…, «لم يُربط», lines)`: `RECEPTION_LINK_ACTIVE`, `ACCOUNT_IS_ADMIN`, `ACCOUNT_SUSPENDED`, `validation` (the person's `invalid_choice`), `not_found`. A new choice resets the last failure.
- **`LinkOwnerDialog({ target, onClose, returnFocus })`:** `Dialog` (`closeLabel`), header, `FormFailure`, `Field` with `PersonCombobox` (space side) or `SpaceCombobox` (person side), the consequence (`aria-live="polite"`), on the space side a `Link` line to the owners page, footer `Button` «ربط» (`loading`).
- **`useSpaceOwnersQuery(spaceId)`:** `refetchOnMount: 'always'`. **`useUnlinkOwner()`:** mutation `{ spaceId, userId, toast: { person, space, last } }`, `gcTime: 0`; `onSuccess`: `await refresh()`, then «فُك ربط {person} من {space}», with «المساحة غير موثّقة الآن» when it was the last.
- **`useUnlinkOwnerDialog({ space, owner }, close)`** → `{ title (NamedLineView: «فك ربط {person} من {space}؟»), consequence: NamedLineView | string | null (null while the owners load), confirm: { label, run, busy, disabled (while loading) }, cancelLabel, failure }`. Others left = the read's owners without this person: none → «تصبح {space} غير موثّقة وتختفي حالتها المباشرة، ويعدّلها فريق مساحة.»; some → «يبقى المالكون الآخرون، وتبقى موثّقة.»; the read failed → «إن كان مالكها الوحيد، تصبح غير موثّقة وتختفي حالتها المباشرة.». Refusals: `not_found` «حُذفت المساحة في هذه الأثناء.».
- **`UnlinkOwnerDialog({ space, owner, onClose, returnFocus })`:** `AlertDialog` (`onCloseAutoFocus` → `returnFocus`), title, description (a `Skeleton h-4 w-3/4` while loading), `FormFailure`, footer `AlertDialogCancel` «رجوع» and `Button variant="destructive" loading` «فك الربط» (design issue 10).
- **`useOwnerActions(row)` / `OwnerActionsMenu({ row })`:** `DropdownMenu`, trigger `Button variant="ghost" size="icon"` (`EllipsisVerticalIcon`, named «إجراءات: {name}»); «ربط بمساحة» (`disabled` with its reason under it for a suspended account); a `variant="destructive"` item «فك الربط من {space}» per space; the chosen dialog rendered with the trigger as `returnFocus`. `OwnersList` gains the actions column (`meta: { className: 'w-px' }`), `OwnerCard` the menu at its end.
- **Words, `spaceLinks.link`:** `titleFromSpace({space})` Link an owner to {space} / ربط مالك بـ {space} · `titleFromPerson({name})` Link {name} to a space / ربط {name} بمساحة · `noOwner` It has no owner today. / ليس لها مالك اليوم. · `oneAtATime` One space at a time. / مساحة واحدة في كل مرة. · `person` Person / الشخص · `personHelper` Owners and users, by name or email. Suspended accounts can’t be linked. / المالكون والمستخدمون، بالاسم أو البريد. الحسابات الموقوفة لا تُربط. · `choosePerson` Choose a person / اختر شخصًا · `space` Space / المساحة · `chooseSpace` Choose a space / اختر مساحة · `becomesVerified({space})` (above) · `anotherOwner({space})` They become another owner of {space}; it stays verified. / (above) · `becomesOwner` Their account becomes an owner’s, and they’re asked to sign in again. / (above) · `addOwner` A new owner with no account? Add them on the space owners page. / مالك جديد بلا حساب؟ أضفه من صفحة أصحاب المساحات. · `submit` Link / ربط · `failed` Not linked / لم يُربط · `refusals`: `RECEPTION_LINK_ACTIVE` This person has a reception link at this space; its owner ends it first. / لهذا الشخص رابط استقبال في هذه المساحة؛ يفكّه مالكها أولًا.; `ACCOUNT_IS_ADMIN` This is an admin’s account; an admin can’t be linked to a space. / هذا حساب أدمن، ولا يُربط أدمن بمساحة.; `ACCOUNT_SUSPENDED` (as `addOwner`'s); `validation` That account no longer exists — choose another. / لم يعد هذا الحساب موجودًا — اختر غيره.; `not_found` The space was deleted meanwhile. / حُذفت المساحة في هذه الأثناء. · `linked({person, space})` {person} linked to {space} / رُبط {person} بـ {space} · `nowVerified` The space is now verified / المساحة موثّقة الآن. English lines for the consequences: «{space} becomes verified and its owner edits it; the Masaha team no longer does.»
- **Words, `spaceLinks.unlink`:** `title({person, space})` Unlink {person} from {space}? / فك ربط {person} من {space}؟ · `lastOwner({space})` {space} becomes unverified, its live status disappears, and the Masaha team edits it. / (above) · `othersStay` The other owners stay, and it stays verified. / يبقى المالكون الآخرون، وتبقى موثّقة. · `ifLast` If they are its only owner, it becomes unverified and its live status disappears. / إن كان مالكها الوحيد، تصبح غير موثّقة وتختفي حالتها المباشرة. · `confirm` Unlink / فك الربط · `cancel` Back / رجوع · `failed` Not unlinked / لم يُفك الربط · `refusals.not_found` (as `link`'s) · `unlinked({person, space})` {person} unlinked from {space} / فُك ربط {person} من {space} · `nowUnverified` The space is now unverified / المساحة غير موثّقة الآن.
- **Words, `spaceLinks.ownerActions`:** `menu({name})` Actions: {name} / إجراءات: {name} · `link` Link to a space / ربط بمساحة · `suspended` The account is suspended — restore it first / الحساب موقوف — استرجعه أولًا · `unlinkFrom({space})` Unlink from {space} / فك الربط من {space}.
- **Docs:** `space-links.md` — *Behaviour* («Linking and unlinking on the web»), *Web decisions* (one dialog, two entries (A4); the consequence from the chosen option's facts, the role line only when certain; the unlink reads the space's owners (Stronger 2); the person's role never predicted (design issue 1); the admin scope refreshed whole, the editor's space included; the refusals in the dialog; the unlink's action stays until the answer (design issue 10)), *Code map*, *Web history*; the deleted row's line «of the three steps, only the restore has a screen…» → the restore and the unlink have screens. `architecture.md` §3 and `dashboardOnly.ts` (Stronger 1). `overview.md` Space links: «… adding, linking and unlinking owners on the dashboard».

### PR 3 · commit 2 — the editor names its owners (finding 59)
- **`features/spaces/types/OwnersSlot.ts`:** `OwnedSpace = { id; name: SpaceNameView; isVerified; owners: { id; name }[] }` (+ `unsaved: boolean` if design issue 7 is approved); `OwnersSlot = (space: OwnedSpace) => ReactNode`; exported from `spaces`' `index.ts`.
- **`SpaceEditor`** gains `ownerActions: OwnersSlot`; its output goes inside `VerifiedNotice` (new `children`, under the description) or, unverified, inside the warning `Alert`'s description, in a `flex flex-wrap gap-2` row.
- **`useSpaceEditor`:** `verified.title` = `words.verified.ownedBy({ names })`, the owners' names isolated and joined by `words.verified.namesSeparator`; `owned: OwnedSpace` (the name by `spaceNameOf`). `words.verified.title` is removed (a verified space always has an owner in the same read).
- **`useSpaceOwnersActions(space, addOwnerLink)` / `SpaceOwnersActions({ space, addOwnerLink })`:** verified → one `Button variant="outline" size="sm"` «فك ربط {name}» per owner, each opening `UnlinkOwnerDialog` (that button as `returnFocus`); unverified → `Button variant="outline" size="sm"` «ربط مالك» opening `LinkOwnerDialog` from the space (disabled with its reason while `unsaved`, if design issue 7 is approved).
- **Page:** `SpaceEditPage` passes `ownerActions`, made once: `(space) => <SpaceOwnersActions space={space} addOwnerLink={ADMIN_OWNERS_PATH} />`; `navigation.ts`: `ADMIN_OWNERS_PATH = \`${DASHBOARD_PATHS.admin}/owners\`` (also the link dialog's `addOwnerLink`).
- **Words:** `spaces.editor.verified.ownedBy({names})` Edited by {names} / يعدّلها {names} · `namesSeparator` «, » / «، »; `spaceLinks.spaceOwners.unlink({name})` Unlink {name} / فك ربط {name} · `link` Link an owner / ربط مالك (· `unsavedReason` Save or discard your changes first / احفظ التغييرات أو تجاهلها أولًا, if design issue 7 is approved).
- **Docs:** `spaces.md` — *Behaviour* (the verified notice names its owners and offers an unlink per owner; the unverified editor offers the link; «The way back from a deleted space to a user»: the unlink is built, but none of the three steps reaches a deleted space's links without the restore), *Web decisions* («A verified space's notice names no owner» marked *Superseded 2026-10-18 by #PRNUM's…*, and the new decision; the slot filled from `space-links`), *Open findings* (59 removed), *Web history*. `space-links.md` (the editor's owner actions, code map). Finding 59: status **Resolved**, a resolution paragraph dated `2026-10-18, #PRNUM`; the index moves it to *Resolved*. `overview.md` Spaces: «… a verified one read-only, naming its owners».

## 10. Tests — each with its lane, title and the break that must make it fail

**Rule for every test below** (testing §3): it is seen failing first in its own lane; for code that already
exists, the named break is made once, the red output recorded in the report, then restored. Expectations
are written by hand.

### PR 1
| Lane · file | Title | The break that makes it fail |
|---|---|---|
| Component · `PhotosSection.component.test.tsx` | titles a refused move by the move, not by a failed load | `tileFailure` titled `words.loadFailed` again |
| Component · same | titles a refused removal in its dialog by the removal | `removalFailure` titled `words.loadFailed` again |
| Unit · `sendMultipart.unit.test.ts` | (existing) sends one part … and reports its progress — kept; the "no callback" test deleted | — (a type: a call without `onProgress` fails `typecheck`) |
| Component · spaces list tests (existing, unchanged) | all of `useAdminSpacesList`, `useAdminSpacesFilters`, `AdminSpacesList`, the spaces page in `routes` | a mistake in the refactor (they are its proof) |
| Unit · `spaceLinksRepository.unit.test.ts` | reads a page of the admin's users with the request's filters | the path or the params changed |
| Unit · `usersFiltersOf.unit.test.ts` | reads the search, the state and the page by the contract's rules, an invalid one falling back to its default | `state` read without the schema's rule (`?state=gone` kept) |
| Unit · same | writes the address with the defaults left out | `page=1` written |
| Unit · same | asks for the filters as the contract names them | `state` dropped from the request |
| Unit · `userRowView.unit.test.ts` | words the state: active as success, suspended as neutral | the variants swapped |
| Unit · same | names each space in the interface's language, an English-only one marked as English | `nameEn` always, or no `lang` |
| Unit · same | marks an owner with no space as one whose spaces are all deleted, and never a user | the role check removed |
| Component · `useUsersFilters.component.test.tsx` | chooses a state, replacing the address and returning to the first page | `push` instead of `replace`, or the page kept |
| Component · same | clears the search and the state at once | `clearAll` keeps the state |
| Component · `useOwnersList.component.test.tsx` | asks for the owners only, with the address's search, state and page | `role: 'owner'` left out of the request |
| Component · same | is empty with no filter, and no match with one | the status always `empty` |
| Component · `OwnersList.component.test.tsx` | shows each owner with their email, their spaces and their state | the spaces cell drawn empty |
| Component · same | leads an owner whose spaces are all deleted to the deleted spaces | the line not drawn, or the link's path not the one given |
| Component · same | filters by state from the chips | the chips' `choose` not wired |
| Component · same | has no accessibility violations | (vitest-axe) a chip group with no name |
| Component · `routes.component.test.tsx` | shows the admin's owners page under its title, with the owners | the route left on its placeholder |

### PR 2
| Lane · file | Title | The break that makes it fail |
|---|---|---|
| Component · `Combobox.component.test.tsx` | with its caller's search, hands each change of the text to the caller and keeps the options it is given | `shouldFilter` left on |
| Component · same | shows the loading text in place of the empty text while its options come, with no accessibility violations | `CommandPrimitive.Empty` drawn while loading |
| Unit · `lineParts.unit.test.ts` (moved, unchanged) | its existing tests | — (moved code; must pass unchanged) |
| Unit · `usersRepository.unit.test.ts` | records how a temporary password was handed over | the path or the body changed |
| Component · `useTemporaryPasswordDialog.component.test.tsx` | waits for the copy before it lets the admin finish, and copies the password | «تم» enabled from the start |
| Component · same | lets the admin finish when the copy fails, saying to copy it by hand | «تم» left disabled on a failed copy |
| Component · same | asks how it was handed over before it records anything | the handover sent with no channel |
| Component · same | lets the place close only once the handover is recorded, and says so | `onDone` called before the answer |
| Component · same | keeps the dialog open on a failure, with its reason | `onDone` called on any failure |
| Component · same | closes on a password no longer pending, saying the handover was not recorded | the dialog kept open on `TEMPORARY_PASSWORD_NOT_PENDING` |
| Component · `TemporaryPasswordDialog.component.test.tsx` | offers no close button, and neither Escape nor a click outside closes it | `closeLabel` given, or a `preventDefault` removed |
| Component · same | shows the password left to right, with the person it is for | `dir="ltr"` removed |
| Component · same | names «Done»'s reason until the password is copied, then marks the copy | no `aria-describedby` on «تم» |
| Component · same | names the handover choices as a group, and focuses it when none is chosen | the focus not moved |
| Component · same | has no accessibility violations | (vitest-axe) the radio group unnamed |
| Unit · `spaceLinksRepository.unit.test.ts` | adds an owner · finds up to fifty spaces by name | each call's method, path, body or params changed |
| Component · `useAddOwnerForm.component.test.tsx` | sends a new owner without asking to upgrade, and hands on the password once | `upgradeExisting: true` always sent |
| Component · same | turns to upgrading when the email has an account, and sends the upgrade | `EMAIL_HAS_ACCOUNT` shown as a failure |
| Component · same | goes back to creating once the email changes | the upgrade kept for another email |
| Component · same (`it.each`) | words an admin's, a suspended and an owner's email on the form | the form's `failureLines` removed |
| Component · same | asks for the space before anything is sent | `prepare` sends `spaceId: null` (another code) |
| Component · same | keeps no temporary password in the cache once it is handed on | the mutation's `gcTime: 0` or `reset()` removed |
| Component · `AddOwner.component.test.tsx` | opens the sheet from «Add owner», its fields named, the notice saying what will happen | the notice not drawn |
| Component · same | searches the spaces, each option with its state and its owners | the badges or the owners not drawn |
| Component · same | shows the page's password dialog once the owner is added, until it is done | the slot never rendered, or `done` not clearing it |
| Component · same | has no accessibility violations, the sheet open | (vitest-axe) |
| Component · `routes.component.test.tsx` | offers «Add owner» above the owners list | the add row not set by the page |

### PR 3
| Lane · file | Title | The break that makes it fail |
|---|---|---|
| Unit · `spaceLinksRepository.unit.test.ts` | links · unlinks · finds active people · reads a space's owners | each call's method, path, body or params changed |
| Component · `useLinkOwnerDialog.component.test.tsx` | says, before the act, that an unverified space becomes verified, and that a user becomes an owner | the person line said for an owner, or the space line wrong |
| Component · same | says that a verified space only gains another owner | the unverified line used |
| Component · same | asks for a choice before anything is sent | the link sent with nothing chosen |
| Component · same (`it.each`) | words each refusal in the dialog, which stays open | `lines` removed, or the dialog closed on a failure |
| Component · `LinkOwnerDialog.component.test.tsx` | from a space: offers people by name or email, each saying what it is | the kind not drawn |
| Component · same | from a person: offers spaces, the ones already theirs unavailable | `disabled` dropped |
| Component · `useUnlinkOwnerDialog.component.test.tsx` | says the space turns unverified when this is its last owner, as the server reads it | the count taken from the row, not the read |
| Component · same | says the others stay when it has other owners | the lines swapped |
| Component · same | holds the action until the owners are read | `disabled` not tied to the read |
| Component · `UnlinkOwnerDialog.component.test.tsx` | opens on Back, its action destructive, staying open on a failure | `AlertDialogAction` that closes on click |
| Component · `OwnerActionsMenu.component.test.tsx` | offers to link and one unlink per space, the link unavailable with its reason for a suspended account | the reason not drawn, or one item for all spaces |
| Component · `SpaceEditor.component.test.tsx` | names a verified space's owners, and places the owners' actions in its notice | the title without names, or the slot not rendered |
| Component · same | places the owners' actions in an unverified space's notice | the slot rendered only when verified |
| Component · `SpaceOwnersActions.component.test.tsx` | offers one «Unlink {name}» per owner of a verified space, each asking first | one button for all owners |
| Component · same | offers to link an owner to an unverified space, and no unlink | both drawn |

## 11. Review Focus — inputs no planned test exercises

- More than 50 people or spaces match a search: only the first 50 are offered, with no "type more" line.
- An admin among a page of people is dropped in the browser, so that page shows fewer than 50.
- A 429 on adding, linking, unlinking or the handover: the countdown in the dialog and the blocked submit (the shared `useRefusalView` is proven elsewhere).
- The owners list past its last page, its pages and its states: the shared pieces are proven by the spaces list's tests.
- The clipboard in a real browser (the run uses `localhost`, a secure context; production is HTTPS).
- The layout: the email under the name at 768–1023 px, its own column from 1024 (the component lane cannot see it; the real run's screenshots do).
- Mixed-direction names in dialog titles and toasts (an Arabic person, an English-only space) in both languages.
- Two admins linking or unlinking the same space at once (the server is idempotent and takes the locks).
- If design issue 7 is not approved: a link from an editor with unsaved changes drops them.

## 12. The commits

PR 1 — `feat/admin-owners`
1. `fix(spaces): title the gallery's failed writes` (46)
2. `refactor(space-links): share the list's paging` (46)
3. `feat(space-links): add the admin's owners page` (46) — the PR's title.

PR 2 — `feat/admin-add-owner`
1. `feat(design-system): let callers search a combobox` (50)
2. `refactor(localisation): share lineParts` (39)
3. `feat(users): show a temporary password once` (43)
4. `feat(space-links): add an owner to a space` (42) — the PR's title.

PR 3 — `feat/admin-owner-links`
1. `feat(space-links): link and unlink owners` (42) — the PR's title.
2. `feat(spaces): name a verified space's owners` (44)

Each body says *why*. Code, tests and the documents describing a unit go in its commit. Stage by path
(`git add <path> …`), `git status` before each commit; never `git add -A` / `git add .`. No tool
attribution. A fix before the push folds into its commit: `git commit --fixup=<sha>`, then
`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash $(git merge-base HEAD origin/main)`.

## 13. The procedure and the verification

Each PR runs this whole procedure on its own, from its own branch; PR 2 and PR 3 begin only once the PR
before has merged.

### First checks (each PR, before any edit)
1. In `C:\Users\basel\masaha`: `git status` clean, on `main`; `git fetch origin`; `git switch main && git pull --ff-only`.
2. `git diff --name-status <base> origin/main` (PR 1's base `5e8c979d`; PR 2's and PR 3's base = the merge of the PR before). A change to a code file this plan names that the plan does not cover → **stop and ask**. If `packages/shared` changed: `npm run build -w @masaha/shared` before any web check.
3. Re-read the shared documents (§7) on `origin/main`.
4. **Checks the executor makes first, with the fallback:**
   - cmdk `^1.1.1` takes `shouldFilter` on `Command` and `value`/`onValueChange` on `Command.Input` (read `node_modules/cmdk/dist/index.d.ts`, never cwd into `node_modules`); if not → stop and ask.
   - `userEvent.setup()` installs a clipboard stub in jsdom (user-event 14.6); if `navigator.clipboard` is still undefined in a hook test, define it in that test only, on `navigator`, as a platform seam.
   - `ToggleGroup type="single"` hands `''` when the chip already on is clicked; the hook ignores `''`.
   - `useServerForm` builds its resolver once, so `prepare` must not read state that changes: the upgrade flag goes in `submit`, never in `prepare`.
5. Branch: `git switch --no-track -c feat/admin-owners origin/main` (PR 2: `feat/admin-add-owner`; PR 3: `feat/admin-owner-links`; each from the latest `origin/main`).

### Per commit
`npm run lint` and `npm run typecheck`; focused runs of the files touched are allowed while working.

### On the head, once each (the owner's rule: no lane re-run unless a file it covers changed after it passed)
First check that worker B's folder runs no test:
`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'masaha-b' -and $_.CommandLine -match 'vitest' }` must be empty.
Then: `npm run test:unit` · `npm run test:component` · `$env:NODE_ENV='production'; npm run build; Remove-Item Env:NODE_ENV` · `npm run check:build` · `npm run check:classes` · `npm run format:check` · `npm run check:links`.
**Not run:** `npm run test:api` — no `apps/api` or `packages/shared` change; CI runs it.

### The real run (each PR)
- `docker start masaha-postgres-1` (never `db:up`); the API on 3320 (`npm run dev -w @masaha/api`, `apps/api/.env` present; worker A's `masaha_dev`), the web on 5320 (`npm run dev`). Never `npm ci` while VS Code is open (no install is needed: no dependency changes).
- Data: sign in as the seeded admin; the demo seed gives one verified space and its owner (`demo-owner@example.com`). PR 1 also needs (by `POST /admin/owners`, `PUT /admin/users/:id/suspended`, `DELETE /admin/spaces/:id` with the admin's token from `POST /api/v1/auth/login`): a second owner, a suspended owner, and an owner whose only space is deleted. PR 2 and PR 3 make theirs through the screens (and a user registered at `/register`).
- Drive it with the **`playwright` MCP tools**: Arabic light and English dark, at 390, 768 and 1440.
  - PR 1: the owners list; the search and the chips (and the address after Back); the finding-50 row and its link; the empty and no-match states; a card at 390; the email under the name at 768.
  - PR 2: the space search in the sheet (its loading line, an option's badges and owners); add a new owner (the password dialog: Escape and an outside click do nothing; «تم» waits for «نسخ»; the handover recorded; its toast); an existing user's email (the upgrade line and «ترقية وربط», then its toast); an admin's email (the refusal on the form); the showcase's new Combobox example at `/__showcase`.
  - PR 3: link from an owner's row (a verified space: "another owner"); unlink (the last owner → the unverified line; the row leaving the list keeps the focus on the list); the verified editor («يعدّلها …», «فك ربط …»); the unverified editor («ربط مالك», a user chosen: the role line; it turns read-only once linked).
- Screenshots to `D:\masahaWorkspace\WORKER_A\OWNERS\shots\pr1\`, `…\shots\pr2\`, `…\shots\pr3\` (the tool saves a relative name in the session's folder: move them there at the end); `git status` clean afterwards; never commit an image.
- Stop the servers by PID (`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'C:\\Users\\basel\\masaha' }`, `Stop-Process -Id …`) and check the ports: `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` empty.

### Push and the PR
1. `git grep -n "#PRNUM" HEAD` lists the placeholders; the next number: `gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number'` + 1 (worker B's PACKAGES may take it first: check at that moment).
2. In Git Bash: `git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#<n>/g'" origin/main..HEAD`, then `git update-ref -d refs/original/refs/heads/<branch>`; `git grep -n "#PRNUM" HEAD` must be empty, and `git diff origin/main --stat` the same files as before.
3. `git push -u origin <branch>`, then at once `gh pr create --assignee @me --label feat --label area:web --label area:docs` (PR 2 adds `--label area:design-system`; a missing label is created with `gh label create`; PR 1's commit 1 also touches `spaces` and `shared/uploads`, both `area:web`), the title = the main commit, the description written out (workflow §3: Summary; Scope / Acceptance criteria / Out of scope; Change type; Evidence — what was run and what was not; Screenshots — RTL and LTR, light and dark, phone and desktop, attached by the owner; the Definition of Done checklist). Confirm the number it got matches the one written.
4. `gh pr checks <n>` green on the pushed head's SHA, and `gh pr view <n> --json mergeStateStatus` `CLEAN`.
5. The early conflict check: for each other open PR, `git fetch origin <its head ref>` and `git merge-tree --write-tree origin/<branch> origin/<other>`; record the result.
6. The report, written in parts, UTF-8: PR 1 → `D:\masahaWorkspace\WORKER_A\OWNERS\4_REPORT.md`; PR 2 → `…\OWNERS\4_REPORT_ADD.md`; PR 3 → `…\OWNERS\4_REPORT_LINKS.md`, unless a later prompt names another. It gives the head and the commits, what was run and not, **every break made with its red output**, the problems and their solutions, anything unexpected, the conflict check, any departure from this plan. Never merge.

### Stop and ask
- The base diff touches a code file this plan names and does not cover; worker B's open PR edits one of this plan's code files.
- Anything would need `apps/api`, `packages/shared`, the schema, a dependency, or a design-system change other than the `Combobox` search (for example a loading `AlertDialogAction`, or a `DataTable` breakpoint).
- cmdk cannot take the controlled search as §9 describes.
- An existing spaces-list test fails after PR 1's refactor and the cause is not the refactor's own mistake.
- `check:build` fails because a module of this item reaches the site's first download.
- The `playwright` MCP tools are not available.
- Three fixes of one failure have failed.
- A decision this plan does not settle.

## 14. Decisions needed from the owner

Settled during planning (2026-10-18): O1 extend `Combobox`; O2 the users list in `space-links`; O3 three
PRs (two were chosen first on an estimate of ~65 files for the second; counted file by file it was ~85, so
the owner split it again).
Still open, each with the plan's recommendation:
1. **Stronger 1** — remove the never-built `owners` feature from architecture §3 and `dashboardOnly.ts`. *Recommended: yes.*
2. **Stronger 2** — the unlink reads the space's owners on every opening. *Recommended: yes.*
3. **Stronger 4** — leave `sendMultipart`'s optional `signal`. *Recommended: leave it.*
4. **Design issues 1–12** — each approved or not; issue 7 adds `unsaved` to the slot and one line. *Recommended: all.*
5. **Findings 82 and 83** — record both (PR 2). *Recommended: yes.*
6. **The new words** (§9), in both languages, «مالك» in the new lines (design issue 11).

## Appendix — steps mapped to Claude Code skills (only a map; no step depends on them)

| Step | Skill |
|---|---|
| The first checks, the branch | `start-work-item` |
| Each test seen failing, each break made | `superpowers:test-driven-development` |
| A failure's cause | `superpowers:systematic-debugging` |
| Every claim with its command | `superpowers:verification-before-completion` |
| Scope check, commits, `#PRNUM`, push, the PR | `open-pr` |
| The report once CI is green and `CLEAN` | `final-report` |

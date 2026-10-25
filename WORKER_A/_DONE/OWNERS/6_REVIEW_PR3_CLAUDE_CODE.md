# Review — PR #91 (`feat/admin-owner-links`), independent review

## Head

`54dae070a2fbb9ae0938d1868a74395f49d0f6f3`, fetched from `refs/pull/91/head`. `gh pr view 91` → `CLEAN` at the
start and again at the end, so the head did not move. Base `origin/main` = `18ab1705` (#90). There are three commits:
`ac7122d7` fix(space-links): finish the add-owner sheet (44) · `766341f5` feat(space-links): link and unlink
owners (41) · `54dae070` feat(spaces): name a verified space's owners (44). 58 files, `apps/web` and `docs`
only. `gh pr checks 91` passed all nine jobs: build, check:classes, check:links, format:check, lint,
test:api, test:component, test:unit and typecheck.

I ran nothing: no lane, build or browser. Unless a line is marked otherwise, everything below is something
I **saw in the code** at `54dae070` (or in the screenshots in `shots\pr3\`). The red outputs of the breaks,
the local lanes and the real run's steps are **read in `4_REPORT_PR3.md`**.

## Verdict

**Not ready. There is no blocker, but one fix round is needed on this PR.** Two problems need fixing. On a
reopening, the unlink dialog says its destructive consequence from a cached read and enables «فك الربط»
before the read arrives. After every successful link or unlink from the editor, the focus is lost.

## The five most important findings

**1. Should-fix: on every opening after the first, the unlink shows the previous opening's owners, and «فك
الربط» works before the read arrives.**
`apps/web/src/features/space-links/hooks/unlink/useSpaceOwnersQuery.ts:13-18` combined with
`hooks/unlink/useUnlinkOwnerDialog.ts:33-49`.
- **How it breaks:** the query has `refetchOnMount: 'always'` and the app's default `gcTime` (5 min,
  `shared/api/query/queryClient.ts` sets no `gcTime`). On a second opening within five minutes, TanStack
  returns the cached owners with `isPending === false` and refetches in the background. So
  `consequence` is worded from the old owners, the `Skeleton` never shows, and `confirm.disabled`
  (`owners.isPending || blocked`) is `false` while the read is in flight.
- **`useRefreshAdmin` does not help:** it invalidates `['admin']`, but an inactive query is only marked
  stale, not refetched.
- **Scenario:** open «فك الربط من X» on Rima's row while X's only owner is Rima, then press «رجوع». Link
  Sami to X from Sami's row. Reopen Rima's unlink. The dialog says «تصبح X غير موثّقة وتختفي حالتها
  المباشرة…», and «فك الربط» is enabled at once. A click before the GET answers unlinks Rima and toasts
  «المساحة غير موثّقة الآن» (`last` is taken from the stale read), but X stays verified with Sami.
- **A refetch that fails** after cached data keeps the old `data`, so it never falls back to the
  `ifLast` line.
- **What this contradicts:** the plan's Stronger 2 / §14 point 2 («on every opening»), the commit body
  («reads the space's owners each time it opens»), and `space-links.md` › *Linking and unlinking on the
  web* («the line and «فك الربط» wait while they are read»). The test «holds the action until the owners
  are read» uses a fresh `QueryClient` per test, so it cannot see this.
- **Fix:** `gcTime: 0` on `useSpaceOwnersQuery`, so each opening starts pending. Alternatively, treat
  `isFetching` as "reading" for both the line and the action, and a refetch error as a failed read.
- **Test:** render the dialog, unmount it, change the server's owners, render it again in the same
  `QueryClient`, and assert the line is `null` and the action disabled until the new read arrives. The
  break is to remove `gcTime: 0` or the `isFetching` check.
- *Where:* a fix round on this PR (commit 2).

**2. Should-fix: after a successful link or unlink in the editor, the focus is lost to `<body>`.**
`apps/web/src/features/space-links/components/space-owners/SpaceOwnersActions.tsx:23-24,37,52` and
`features/spaces/components/editor/SpaceEditor.tsx:72-83`. The dialog returns the focus to `opener.current`,
the button that opened it. On success, `useRefreshAdmin` refetches the space before the dialog closes, and
in each of these three cases that button is gone:
- **A link on an unverified space:** `readOnly` flips, and `SpaceEditor` swaps `<Alert>` for
  `<VerifiedNotice>`. Those are different component types, so the whole slot remounts and the «ربط مالك»
  button is detached.
- **Unlinking the last owner:** the same swap happens in reverse.
- **Unlinking one of several owners:** that owner's button, keyed by `owner.id`, leaves the list.

`returnFocus.current?.focus()` on a detached node does nothing. The editor has no focus keeper of the kind
the owners list has (`useFocusKeeper`). The review prompt's item 5 asks for «focus returned to the trigger,
or to the list when the row leaves it». The report shows only Escape returning the focus («Escape returned
the focus to «فك ربط basel»»), and no test checks the focus after a success.
- **Fix:** when the opener is no longer connected, move the focus to a stable element, such as the
  notice. For example, `SpaceEditor` gives the notice a `tabIndex={-1}` and a ref, and the slot hands a
  `focusFallback`. Another option is to keep `SpaceOwnersActions` mounted once, outside the branch.
- **Test:** unlink one of two owners and assert the focus lands on the fallback. The break is to drop the
  fallback.
- *Where:* a fix round on this PR (commit 3).

**3. Should-fix (small): the real run's screenshots cover RTL only at desktop and LTR only at 390 and 768,
but the PR description ticks the full matrix.**
- **What exists:** `shots\pr3\` holds `ar-light-1440-*` (17) and `en-dark-{390,768}-*` (16). There is no
  Arabic at 390 or 768 and no English at 1440. Plan §13 asks for «Arabic light and English dark, at 390,
  768 and 1440».
- **What is unseen:** the RTL phone card with its menu, the link and unlink dialogs at phone width in RTL,
  and the editor's notice buttons wrapping in RTL at 390.
- **What the PR claims:** the description ticks «UI checked in RTL and LTR, light and dark, phone and
  desktop» and the criterion «RTL/LTR, light/dark, phone/768/desktop checked in a real run».
- The approval note's (d), PR 2's English/dark/390/768 shots, **is** done: I looked at
  `en-dark-390-upgrade-confirm.png`, and the add sheet's fields are now spaced with the submit at its foot.
- **Fix:** take `ar-light-390-*` and `ar-light-768-*` for the owners cards and menu, the link and unlink
  dialogs, and both editor notices, plus `en-dark-1440-*`. Or have the owner waive them explicitly, and
  word the description as it is.
- *Where:* a fix round on this PR (the real run and the description).

**4. Nit (plausible): the link from a space takes its verification from the editor's copy, and the link
from a person takes it from the chosen option as it was when chosen. Both can be stale.**
- **From a space:** `hooks/link/useLinkOwnerDialog.ts:51` fixes `verified: false` for the space end, and
  `LinkTarget` carries no `isVerified`. If another admin linked the space meanwhile, the line says «تصبح …
  موثّقة» and the toast «المساحة موثّقة الآن», but the space only gained another owner.
- **From a person:** `useState<SpaceChoiceView>` keeps the option object chosen from a possibly cached
  search, so a re-searched, refreshed option does not update the chosen one's `isVerified`.
- The link is not destructive, the server's answer stands, and the refresh shows the truth.
- **Fix, if cheap:** carry `isVerified` in `LinkTarget` from the editor's read. On the person side, look
  the chosen id up in `choices.options` on each render.
- *Where:* a fix round on this PR if touched for finding 1; otherwise a finding to record.

**5. Nit: the first commit's scope says `space-links`, but it also changes `features/users`, and `users.md`
records nothing.**
`ac7122d7` edits `features/users/components/temporary-password/TemporaryPasswordDialog.tsx` (the name in a
`<bdi>`) and `features/users/hooks/temporary-password/useTemporaryPasswordDialog.ts` (the toast's name
isolated), with their tests. Its only history line is in `space-links.md` («#91 — #89's leftovers: the
names in the add sheet's toast…»). The users dialog's change is that capability's, so its one home is
`users.md` › *Web history*.
- **Fix:** add a line to `users.md` in the same commit (fixup). The subject can stay, because the change
  serves the add sheet's flow.
- *Where:* a fix round on this PR (commit 1).

## The other findings

**6. Nit (plausible, not run): «ربط مالك», disabled while there are unsaved changes, is a native-disabled
button.**
`SpaceOwnersActions.tsx:49-51` (`disabled` + `aria-describedby`). A disabled button leaves the tab order,
so a keyboard user never reaches it and never hears its reason. The text is visible in the alert, so a
screen reader that reads the alert's flow still meets it. The dashboard's row actions use `aria-disabled`
for this reason (`spaces.md` › *Web decisions*, «The row's actions wait marked, not disabled»).
- **Fix:** `aria-disabled` and a guarded `onClick`, if the owner agrees that this pattern applies here.
- *Where:* a fix round on this PR (commit 3) or USERS.

**7. Finding to record: the person search calls a receptionist «مستخدم».**
`hooks/link/usePersonChoices.ts:43-48` words `kind` from `role` and `spaces` only. Since #90,
`AdminUserRow.receptionSpaces` tells a front-desk worker apart. Linking such a person as owner of
another space is allowed: `RECEPTION_LINK_ACTIVE` refuses only a link at the same space. Their reception
link elsewhere stays, and the dialog never says so. This is the same gap as PR 2's review finding 10 (the
upgrade confirm).
- *Where:* a finding to record (or USERS, which words a user's row with its reception spaces).

**8. Nit: the unsaved-changes rule of the editor's link is written as behaviour in two capability
documents.**
`spaces.md` › *Behaviour* («…which waits, saying «احفظ التغييرات أو تجاهلها أولًا», while a section has
unsaved changes…») and its *Web decisions* line, and `space-links.md` › *Linking and unlinking on the web*
(«waiting with «احفظ…» while the editor has unsaved changes»). The rule's code is `space-links`'
(`useSpaceOwnersActions.ts:40-42`); `spaces` only hands `unsaved`.
- **Fix:** keep the behaviour and the decision in one document, and have the other link to it.
- *Where:* a fix round on this PR (commit 3), if touched anyway.

**9. Nit: `link.refusals.validation` says «… — اختر غيره» even when the link starts from a person's row,
where no person is chosen.**
`shared/copy/{arabic,english}/spaceLinks.ts`, `link.refusals.validation`. From the person end, the
account that no longer exists is the row's own, so «choose another» points nowhere.
- **Fix:** a neutral line, «لم يعد هذا الحساب موجودًا.», or one line per end.
- *Where:* a fix round on this PR, if cheap.

**10. Nit: two copies of the open-dialog union.**
`hooks/owner-actions/useOwnerActions.ts:10` and `hooks/space-owners/useSpaceOwnersActions.ts:26-28`
declare the same `{ kind: 'link'; target } | ({ kind: 'unlink' } & UnlinkSubject)`.
`EditedSpace` (`useSpaceOwnersActions.ts:10-16`) mirrors `spaces`' `OwnedSpace`, which is the cost of the
slot across features and acceptable.
- **Fix:** one `types/OwnerDialog.ts`.
- *Where:* a fix round on this PR, if touched.

**Read only in the report (not a code finding):** §4 and §6.6 say two secrets were printed into the
executor's own tool output: the dev-only demo password, and a throwaway account's temporary password.
Neither reached the repository, a commit, the PR or the report. Nothing is in the diff. It is noted for the
owner's process.

## The breaks that changed shape (judged)

- «the count taken from the row» → «the last owner assumed, not read». The hook has no row count, so the
  rewording is right. However, neither break covers a cached read (finding 1).
- «both drawn» → «the link drawn, not the unlinks» (`SpaceOwnersActions`). This is the break that branch
  can show. Enough.
- Every other §10 *PR 3* test exists under its planned title. The report lists each named break as red:
  20 for commit 2 and 7 for commit 3 (**read in the report**). The `it.each` of the link's refusals
  includes `ACCOUNT_PASSWORD_PENDING` (seen, `useLinkOwnerDialog.component.test.tsx:224`).

## Checked and fine

- **#89's leftovers (a)–(c):**
  - The upgrade toast goes through `namedLine`/`toastNamed`, with the person isolated and the space its
    own element.
  - The password dialog's name is a `<bdi>`, and its handover toast isolates the name.
  - The space options' owners are isolated through `rowView`.
  - `SpaceCombobox` uses «بحث» / «اسم المساحة» / «المساحات».
  - `useSpaceChoices` builds options from `rowView`, so «مخفية» is `warning` in both places. The copied
    rules and the dead ternary are gone. Each change has a test asserting it.
- **The consequence before the act:**
  - Unverified → «تصبح … موثّقة…», verified → «يصبح مالكًا آخر…».
  - The role line appears only for a chosen `USER`, and the API ends that user's sessions
    (`adminOwners.api.test.ts:129-138`), so «ويُطلب منه الدخول من جديد» is true.
  - The unlink never predicts the role. A failed first read gives `ifLast` with the action enabled.
- **Refusals:** the link words `RECEPTION_LINK_ACTIVE`, `ACCOUNT_IS_ADMIN`, `ACCOUNT_SUSPENDED`,
  `ACCOUNT_PASSWORD_PENDING`, `validation` and `not_found`. The unlink words `not_found` (the contract's
  only refusal; a missing link is a 204). Both dialogs stay open, and a new choice clears the last
  refusal. A 429's `blocked` disables «ربط» and «فك الربط».
- **The editor:**
  - The verified notice reads «يعدّلها {names}», isolated and joined by «، » / «, », with one unlink per
    owner.
  - The unverified warning offers «ربط مالك», disabled while `dirty.length > 0`, with its reason.
  - `refresh` awaits the active `['admin', 'spaces', 'space', id]`, so the editor turns read-only or
    editable before the toast. Seen in the screenshots `editor-linked-read-only` and
    `editor-unsaved-holds-link`.
- **Dialogs:**
  - The unlink is an `AlertDialog` with no X, `AlertDialogCancel` first (the test asserts the focus on
    «Back»), and a `Button variant="destructive" loading` that stays until the answer.
  - The link is a `Dialog` with its close label.
  - On the owners page, focus returns to the menu trigger. When the row leaves, `useFocusKeeper` takes
    the focus to the section (as the report says).
  - Rows are keyed by id (`getRowId`), so a dialog's state never jumps rows.
- **Boundary:**
  - `owners` is gone from architecture §3's table, from the «Names match the backend» paragraph and from
    `dashboardOnly.ts`. No other mention is left in `docs` or `apps/web`.
  - `SpaceEditPage` imports `@features/space-links` and `@features/spaces` through their `index.ts`. No
    feature imports another (`git grep @features/` in the three features: none).
  - `check:build`'s three lines are **read in the report**.
- **Frontend rules:** no colour or arbitrary class (`w-px`, `self-center`, tokens only). Every new string
  exists in both catalogues with the same keys. Names are isolated in accessible names
  (`Actions: ⁨name⁩`, `Unlink ⁨name⁩`).
- **Documents:**
  - Finding 59 is Resolved with a dated resolution and moved in the index.
  - The old `spaces.md` decision is marked *Superseded*.
  - `overview.md`'s two lines are true to the code.
  - `space-links.md`'s deleted-row line («the restore and the unlink have screens…») is true.
  - The history lines carry `#91`.
  - The one claim that is not true to the code is finding 1's.
- **Commits:** subjects are 44 / 41 / 44 (counted). Each body says why. There is no attribution.
- **Worker B:** no other open PR (`gh pr list --state open` → only #91), so there is no text conflict and
  no clash of findings numbers.
- **Screenshots looked at:** `ar-light-1440-editor-verified`, `-editor-unsaved-holds-link`,
  `-link-people`, `-link-user-role-line`, `-unlink-toast-row-gone`; `en-dark-390-row-menu`,
  `-link-dialog`, `-unlink-dialog`, `-editor-verified`, `-upgrade-confirm`. Each shows what the report says.

# OWNERS — PR 3 (`feat/admin-owner-links`) — the executor's report

> Written as the work went, 2026-10-19. Executor: Claude Code (Opus), in `C:\dev\masaha\app`, building
> PR 3 only (`3_EXEC_PROMPT_PR3.md`): #89's leftovers, then `2_PLAN.md` §9 *PR 3* commits 1 and 2.
> Nothing here re-decides the plan.

## 1. First checks (2026-10-19)

| Check | Result |
|---|---|
| Precondition — `gh pr view 89 --json state,mergeCommit` | `{"mergeCommit":{"oid":"60a78063590e8660c937629bf633b18aa2f9a4f1"},"state":"MERGED"}` |
| Working folder | `C:\dev\masaha\app`; `git status --short --branch` → `## main...origin/main`, clean |
| `git fetch origin --prune`; `git pull --ff-only` | `Already up to date.`; `origin/main` = `18ab1705` (#90's merge) |
| Base diff — `git diff --name-status 60a78063 origin/main` | 66 files, all #90 (STAFF). `apps/web`: `receptionSpaces: []` added to seven `AdminUserRow` test literals (incl. `spaceLinksRepository.unit.test.ts`, `OwnersList.component.test.tsx`), the errors catalogues gain `TEMPORARY_PASSWORD_EXPIRED` and `ACCOUNT_PASSWORD_PENDING`, auth's Google line reworded. No §7 *PR 3* code file changed beyond what the prompt names. |
| `packages/shared` changed | Yes (`core/errors.ts`, `space-links/{requests,responses}.ts`, `users/requests.ts`) → `npm run build -w @masaha/shared` → `tsc -p tsconfig.build.json`, exit 0 |
| Contract read (`api-contract.md` › *Owners (the admin)*) | `POST /admin/spaces/:spaceId/owners` refuses `validation` (`userId` `invalid_choice`), `ACCOUNT_IS_ADMIN`, `ACCOUNT_SUSPENDED`, `RECEPTION_LINK_ACTIVE`, `ACCOUNT_PASSWORD_PENDING`, `not_found`; `DELETE …/owners/:userId` refuses `not_found`. As the plan + the prompt's #90 note. |
| Open PRs | `gh pr list --state open` → `[]` |
| Next free finding number | 94 (prompt) |
| Branch | `git switch --no-track -c feat/admin-owner-links origin/main` → `Switched to a new branch 'feat/admin-owner-links'` |

## 2. Commits

### Commit 1 — `aa0c8a4e` `fix(space-links): finish the add-owner sheet` (44 chars)

The approval note's (a)–(c) (`6_REVIEW_PR2_CLAUDE_CODE.md` findings 5, 6, 7):
- (a) `useAddOwner`'s upgrade toast → `toastNamed(namedLine(({ name }) => lines.upgraded({ name: isolate(personName), space: name }), spaceName))` (the PR 2 pieces are now used); `useTemporaryPasswordDialog`'s `recorded` toast isolates the name; `TemporaryPasswordDialog`'s description sets the name in `<bdi>`; the space options' owners isolated (via (c)).
- (b) `SpaceCombobox` names the search box `choices.search` («بحث»), its placeholder `choices.spacesPlaceholder` («اسم المساحة»), the list `choices.spaces` («المساحات»).
- (c) `useSpaceChoices` builds each option from `rowView` (name, state badges — «مخفية» now `warning` as in the list —, owners isolated, `noOwner` when none); the copied rules, the dead ternary and the stray comment are gone.
- `space-links.md`: one web decision and one history line (`#PRNUM`).

Tests written first, then run against the code at `origin/main` (the code changes backed up and set aside):
`npx vitest run --project component AddOwner… TemporaryPasswordDialog… useTemporaryPasswordDialog…` →
`Tests  5 failed | 14 passed (19)`, each failure the change it proves:

| Test | Red seen before the code |
|---|---|
| `AddOwner` › searches the spaces, each option with its state and its owners (extended: «Hidden» `data-variant="warning"`, the owner `⁨Hadi⁩`) | `Error: expect(element).toHaveAttribute("data-variant", "warning")` |
| `AddOwner` › names the space search by its own words, apart from the field it fills (new) | `TestingLibraryElementError: Unable to find role="combobox" and name "Search"` |
| `AddOwner` › shows whose account the email is… (the toast: `⁨Rima Haddad⁩ upgraded to owner and linked to Focus Hub`, the space its own `SPAN`) | `TestingLibraryElementError: Unable to find an element with the text: (_content, element) => element?.hasAttribute("data-title") …` |
| `useTemporaryPasswordDialog` › lets the place close only once the handover is recorded, and says so (the toast with `⁨Rima⁩`) | `TestingLibraryElementError: Unable to find an element with the text: Handover recorded: ⁨Rima⁩ · WhatsApp.` |
| `TemporaryPasswordDialog` › shows the password left to right, with the person it is for (the name a `BDI`) | `AssertionError: expected 'SPAN' to be 'BDI' // Object.is equality` |

Code restored → the same command: `Test Files  3 passed (3)` / `Tests  19 passed (19)`. Then `npx vitest run --project component src/features/space-links src/features/users` → `Test Files  22 passed (22)` / `Tests  137 passed (137)`.
`npm run lint` → `> eslint .`, no problem printed; `npm run typecheck` → `tsc --noEmit` and `tsc -b`, no error; `npx prettier --check` on the changed code → `All matched files use Prettier code style!`.

### Commit 2 — `0ee60d62` `feat(space-links): link and unlink owners` (41 chars; the plan counted 42)

34 files. §9 *PR 3 · commit 1* as planned: repository `linkOwner`/`unlinkOwner`/`personChoices`/`spaceOwners`; keys `personChoices`, `spaceOwners`; `LinkTarget`; `useSpaceChoices({ enabled, linked })` and `SpaceCombobox` (an option already the person's `disabled`, «مربوطة»); `hooks/link/{usePersonChoices,useLinkOwner,useLinkOwnerDialog}`, `components/link/{LinkOwnerDialog,PersonCombobox}`; `hooks/unlink/{useSpaceOwnersQuery,useUnlinkOwner,useUnlinkOwnerDialog}`, `components/unlink/UnlinkOwnerDialog` (`AlertDialog`, Back first, a destructive `Button loading` that stays until the answer, a `Skeleton` while the owners are read); `hooks/owner-actions/useOwnerActions`, `components/owner-actions/OwnerActionsMenu`; `OwnersList` gains the actions column (`w-px`), `OwnerCard` the menu beside the badge; words `link`, `unlink`, `ownerActions`, `choices` additions in both catalogues; `dashboardOnly.ts` and architecture §3 lose `owners` (§14 point 1); `space-links.md` (*What it does*, *Behaviour* «Linking and unlinking on the web», six *Web decisions*, the deleted row's three-steps line, *Code map*, the `#PRNUM` history line extended); `overview.md` Space links.

Red before the code: the five new test files written first against stub modules (`throw new Error('not built')`) and the repository test against the repository without the four calls:
- `npx vitest run --project unit src/features/space-links/repository` → `Tests  4 failed | 12 passed (16)`, each `TypeError: createSpaceLinksRepository(...).linkOwner is not a function` (and `unlinkOwner`, `personChoices`, `spaceOwners`).
- `npx vitest run --project component …/hooks/link …/hooks/unlink …/components/link …/components/unlink …/components/owner-actions` → `Test Files  5 failed (5)` / `Tests  23 failed (23)`, each `Error: not built`.

Green after: repository → `Tests  16 passed (16)`; the five files → first run `Tests  2 failed | 21 passed (23)`, both the tests' own matching (the unlink's line is split around the space's name, so it is now read as the dialog's accessible description; the admin refresh re-reads the space after the DELETE, so the DELETE is found by method, not as the last request) — fixed in the tests, then `npx vitest run --project component src/features/space-links` → `Test Files  16 passed (16)` / `Tests  112 passed (112)`; `--project unit src/features/space-links` → `Test Files  7 passed (7)` / `Tests  59 passed (59)`.
Also changed, beyond §7's list: `OwnersList.component.test.tsx` (the header list and row cells now include «Actions», and the row's menu button is asserted — first run red `expected [ 'Name', 'Email', …(3) ] to deeply equal [ 'Name', 'Email', …(2) ]`, an expected change); `useAddOwnerForm.component.test.tsx` (`linked: false` in a `SpaceChoiceView` literal, for `typecheck`); `types/PersonChoiceView.ts` (new, the person option's type); one new word each language, `link.close` («إغلاق»), the dialog's close button.
`npm run lint` → `> eslint .`, nothing printed; `npm run typecheck` → no error; `npm run check:links` → `2210 links in 174 documents and 1274 source files all resolve.`; prettier on the changed code → `All matched files use Prettier code style!`.

**Breaks (§10 PR 3, commit 2's tests)** — each made once, its focused test run (`npx vitest run --project <lane> <file> -t <title>`), the file restored from a copy:

| Break | Result | First error |
|---|---|---|
| repo: link path changed | red — `Tests  1 failed / 15 skipped (16)` | `AssertionError: expected { …(19) } to match object { method: 'post', …(2) }` |
| repo: link body changed | red — `Tests  1 failed / 15 skipped (16)` | `AssertionError: expected { id: 5 } to deeply equal { userId: 5 }` |
| repo: unlink method changed | red — `Tests  1 failed / 15 skipped (16)` | `AssertionError: expected { …(19) } to match object { method: 'delete', …(2) }` |
| repo: people params changed (state dropped) | red — `Tests  1 failed / 15 skipped (16)` | `AssertionError: expected '/api/v1/admin/users?q=rim&limit=50' to be '/api/v1/admin/users?q=rim&state=activ…' // Object.is equality` |
| repo: space owners path changed | red — `Tests  1 failed / 15 skipped (16)` | `AssertionError: expected { …(19) } to match object { method: 'get', …(1) }` |
| link: the person line said for an owner | red — `Tests  1 failed / 10 skipped (11)` | `AssertionError: expected [ …(2) ] to deeply equal [ Array(1) ]` |
| link: the space line wrong (verified line for an unverified space) | red — `Tests  1 failed / 10 skipped (11)` | `AssertionError: expected [ …(2) ] to deeply equal [ …(2) ]` |
| link: the unverified line used for a verified space | red — `Tests  1 failed / 10 skipped (11)` | `AssertionError: expected [ Array(1) ] to deeply equal [ Array(1) ]` |
| link: sent with nothing chosen | red — `Tests  1 failed / 10 skipped (11)` | `AssertionError: expected undefined to be 'Choose a person' // Object.is equality` |
| link: the refusal lines removed | red — `Tests  6 failed / 5 skipped (11)` | `AssertionError: expected { kind: 'refused', …(2) } to match object { kind: 'refused', …(2) }` |
| link: the dialog closed on a failure | red — `Tests  6 failed / 5 skipped (11)` | `AssertionError: expected "vi.fn()" to not be called at all, but actually been called 1 times` |
| link dialog: the kind not drawn | red — `Tests  1 failed / 2 skipped (3)` | `TestingLibraryElementError: Unable to find an element with the text: User. This could be because the text is broken up by multiple elements. In this case, you can provide a functio` |
| link dialog: disabled dropped | red — `Tests  1 failed / 2 skipped (3)` | `Error: expect(element).toHaveAttribute("aria-disabled", "true") // element.getAttribute("aria-disabled") === "true"` |
| unlink: the last owner assumed, not read | red — `Tests  1 failed / 4 skipped (5)` | `AssertionError: expected 'Focus Hub becomes unverified, its liv…' to be 'The other owners stay, and it stays v…' // Object.is equality` |
| unlink: the lines swapped | red — `Tests  2 failed / 1 passed / 2 skipped (5)` | `AssertionError: expected 'The other owners stay, and it stays v…' to be 'Focus Hub becomes unverified, its liv…' // Object.is equality` |
| unlink: disabled not tied to the read | red — `Tests  1 failed / 4 skipped (5)` | `AssertionError: expected false to be true // Object.is equality` |
| unlink dialog: an AlertDialogAction that closes on click | red — `Tests  1 failed / 1 skipped (2)` | `AssertionError: expected "vi.fn()" to not be called at all, but actually been called 1 times` |
| menu: the reason not drawn | red — `Tests  1 failed / 1 skipped (2)` | `TestingLibraryElementError: Unable to find an element with the text: The account is suspended — restore it first. This could be because the text is broken up by multiple elements. ` |
| menu: one item for all spaces | red — `Tests  1 failed / 1 skipped (2)` | `AssertionError: expected [ 'Unlink from Focus Hub' ] to deeply equal [ 'Unlink from Focus Hub', …(1) ]` |
| owners list: the actions column left out | red — `Tests  1 failed / 4 skipped (5)` | `TestingLibraryElementError: Unable to find an accessible element with the role "button" and name `(name) => name.replace(/[⁦-⁩]/g, "") === "Actions: Rima"`` |

After the breaks, the files restored: `--project component src/features/space-links` → `Tests  112 passed (112)`; `--project unit src/features/space-links` → `Tests  59 passed (59)`.

### Commit 3 — `02cc70ae` `feat(spaces): name a verified space's owners` (44 chars)

§9 *PR 3 · commit 2*, design issue 7 included: `features/spaces/types/OwnersSlot.ts` (`OwnedSpace` with `unsaved`, `OwnersSlot`, exported); `useSpaceEditor` → `verified.title = ownedBy({ names })` (each isolated, `namesSeparator`), `owned` (name by `spaceNameOf`, `unsaved = dirty.length > 0`); `words.verified.title` removed; `SpaceEditor` takes `ownerActions` and renders it in `VerifiedNotice`'s new `children` or in the warning's description, in a `flex flex-wrap gap-2` row; `space-links`' `useSpaceOwnersActions`/`SpaceOwnersActions` (an outline `sm` «فك ربط {name}» per owner, or «ربط مالك» disabled with its reason as its description while unsaved; one `opener` ref for the focus's return), exported; `SpaceEditPage` fills the slot once at module level with `ADMIN_OWNERS_PATH` (new in `navigation.ts`); words `spaces.editor.verified.{ownedBy,namesSeparator}`, `spaceLinks.spaceOwners.{unlink,link,unsavedReason}`; docs: `spaces.md` (*Behaviour*: the notice and the link; the way back's line; *Web decisions*: the old one superseded, three new; *Code map*; *Open findings* without 59; history), `space-links.md` (behaviour bullet, code map, history line), finding 59 **Resolved** with its resolution paragraph, the index moved to *Resolved*, `overview.md` Spaces «… a verified one read-only, naming its owners».

Red before the code (tests first, `SpaceOwnersActions` a stub): `npx vitest run --project component …/SpaceEditor.component.test.tsx …/space-owners` → `Tests  6 failed | 24 passed (30)`: the three `SpaceOwnersActions` tests `Error: not built`; «places the owners’ actions in an unverified space’s notice» `Unable to find an accessible element with the role "button" and name "Owners’ actions"`; the verified tests `Unable to find an element with the text: Edited by ⁨Rima⁩` / `Edited by ⁨Rima⁩, ⁨Sami⁩`.
Green after: the same → `Test Files  2 passed (2)` / `Tests  30 passed (30)`.
A fixture fix: `useSpaceEditor.component.test.tsx`'s partial space (`as unknown as AdminSpace`) had no `owners`, which every real read carries; its 10 tests failed with `TypeError: Cannot read properties of undefined (reading 'map')` until `owners: []` was added (a test-file change beyond §7's list). In that same run `routes.component.test.tsx` › «lists the owner’s eleven pages…» failed once (3 s wait, three suites at once); re-run: `npx vitest run --project component src/features/spaces/hooks/editor src/pages` → `Test Files  13 passed (13)` / `Tests  106 passed (106)` — noted for the full lane (finding 55/87's wait). Then `npx vitest run --project component src/features/spaces src/features/space-links` → `Test Files  37 passed (37)` / `Tests  327 passed (327)`.
`npm run lint` → exit 0 (one `no-unnecessary-condition` in the new test fixed first); `npm run typecheck` → no error; `npm run check:links` → `2212 links in 174 documents and 1278 source files all resolve.`; prettier → `All matched files use Prettier code style!`.

**Breaks (commit 3's tests):**

| Break | Result | First error |
|---|---|---|
| editor: the title without the names isolated | red — `Tests  1 failed / 26 skipped (27)` | `TestingLibraryElementError: Unable to find an element with the text: Edited by ⁨Rima⁩, ⁨Sami⁩. This could be because the text is broken up by multiple elements. In this c` |
| editor: the slot not rendered in the verified notice | red — `Tests  1 failed / 26 skipped (27)` | `TestingLibraryElementError: Unable to find an accessible element with the role "button" and name "Owners’ actions"` |
| editor: the slot rendered only when verified | red — `Tests  1 failed / 1 passed / 25 skipped (27)` | `TestingLibraryElementError: Unable to find an accessible element with the role "button" and name "Owners’ actions"` |
| editor: unsaved never handed on | red — `Tests  1 failed / 1 passed / 25 skipped (27)` | `AssertionError: expected { id: 7, …(4) } to match object { unsaved: true }` |
| owners actions: one button for all owners | red — `Tests  1 failed / 2 skipped (3)` | `AssertionError: expected [ 'Unlink Rima' ] to deeply equal [ 'Unlink Rima', 'Unlink Sami' ]` |
| owners actions: the link drawn, not the unlinks, for a verified space | red — `Tests  1 failed / 2 skipped (3)` | `AssertionError: expected [ 'Link an owner' ] to deeply equal [ 'Unlink Rima', 'Unlink Sami' ]` |
| owners actions: the link not held while unsaved | red — `Tests  1 failed / 2 skipped (3)` | `Error: expect(element).toBeDisabled()` |

After the breaks, restored: the two files → `Tests  30 passed (30)`.

## 3. On the head `02cc70ae`, once each

Worker B's folder checked first (`Get-CimInstance … app-b … vitest` → `no vitest under app-b`; before the component lane, no vitest running anywhere).

- `npm run test:unit` → api `Test Files  13 passed (13)` / `Tests  216 passed (216)`; shared `Test Files  45 passed (45)` / `Tests  743 passed (743)`; web `Test Files  80 passed (80)` / `Tests  833 passed (833)`.
- `npm run test:component` → `Test Files  160 passed (160)` / `Tests  1064 passed (1064)` (`Duration  345.67s`). (A first attempt was stopped by the owner before it ran; re-run once, in the background.)
- `$env:NODE_ENV='production'; npm run build; Remove-Item Env:NODE_ENV` → `✓ built in 2.09s`.
- `npm run check:build` → `No showcase code in 38 build files (1034 strings checked).` / `No dashboard code in the site's first download.` / `No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download.`
- `npm run check:classes` → `No physical direction or arbitrary-value classes in 894 files.`
- `npm run format:check` → `All matched files use Prettier code style!`
- `npm run check:links` → `2212 links in 174 documents and 1278 source files all resolve.`
- Not run: `npm run test:api` — no `apps/api` or `packages/shared` change; CI runs it.

## 4. The real run (2026-10-19)

- **Tool:** no `playwright` MCP tools in this session; local headless Chrome over CDP (Node 24's `WebSocket`, no dependency), real screenshots of the real app, as PR 2 did — a departure from §13's named tool. Scripts in this session's scratchpad (`run/cdp.mjs`, `run1*.mjs`, `run2.mjs`), outside the repository.
- **Servers:** `masaha-postgres-1` was up (healthy); `npx prisma migrate status` → `Database schema is up to date!` (worker A's `masaha_dev`); API `npm run dev -w @masaha/api` → `API listening` on 3320; web `npm run dev` → Vite on `http://localhost:5320`. Signed in as the seeded admin (credentials read from `apps/api/.env` by the script). Data: the accounts and spaces already in `masaha_dev` from PR 1/2's runs, plus those made through the screens here.
- **Slips, owned:** two diagnostic outputs printed into this session's tool output only (nothing written to the repository, the report or a commit): the dev-only demo password line of `apps/api/.env` (a `grep` meant for variable names), and the temporary password of a throwaway test account created in this run (a dialog's text dumped while debugging). No later output prints either.

Arabic, light, 1440 px (`shots/pr3/ar-light-1440-*`):

| Case | Seen | Shot |
|---|---|---|
| An owner's row menu | «ربط بمساحة», then «فك الربط من …» per space | `row-menu` |
| A suspended owner's menu | «ربط بمساحة» `aria-disabled="true"`, «الحساب موقوف — استرجعه أولًا» under it | `row-menu-suspended` |
| Link from a row, the space search | the owner's own space disabled, «مربوطة» (`Focus Hub موثّقة مربوطة`) | `link-search` |
| Link from a row to a verified space | «يصبح مالكًا آخر لـ مساحة تجريبية؛ تبقى موثّقة.» before «ربط»; linked: toast «رُبط basel بـ مساحة تجريبية», the focus back on «إجراءات: basel» | `link-another-owner`, `link-toast` |
| A link refused, password pending (Rima, PR 1's owner, never signed in) | «لم يُربط» / «لم يغيّر هذا الشخص كلمة المرور المؤقتة بعد؛ لا يُربط حتى يدخل ويغيّرها.», the dialog open | `link-refused-password-pending-rima` |
| Unlink the last owner (Test Owner PR2 from Bare Space) | «فك ربط Test Owner PR2 من Bare Space؟» / «تصبح Bare Space غير موثّقة وتختفي حالتها المباشرة، ويعدّلها فريق مساحة.», first focus on «رجوع»; unlinked: toast «فُك ربط … من Bare Space» + «المساحة غير موثّقة الآن», the row left the list and the focus is on `SECTION أصحاب المساحات` | `unlink-last-owner`, `unlink-toast-row-gone` |
| The verified editor | «يعدّلها أحمد الشوا، basel», «فك ربط أحمد الشوا» and «فك ربط basel» in the notice | `editor-verified` |
| Its unlink with another owner | «يبقى المالكون الآخرون، وتبقى موثّقة.»; Escape returned the focus to «فك ربط basel» | `editor-unlink-others-stay` |
| The unverified editor (Focus Hub) | «ربط مالك» in the warning | `editor-unverified` |
| …with unsaved changes | «ربط مالك» disabled, «احفظ التغييرات أو تجاهلها أولًا» beside it; enabled again after «تجاهل التغييرات» | `editor-unsaved-holds-link` |
| Link a user from the editor | people search (email and kind); «تصبح Focus Hub موثّقة…» and «ويصبح حسابه حساب مالك، ويُطلب منه الدخول من جديد.»; linked: toast «رُبط basel بـ Focus Hub» + «المساحة موثّقة الآن», the editor read-only («يعدّلها basel», no text field left) | `link-people`, `link-user-role-line`, `editor-linked-read-only` |
| A new owner added, then linked to a second space | the password dialog; handover recorded «سُجّلت طريقة التسليم: نور الحلو · شفهيًا»; their link to Golden Hub refused with `ACCOUNT_PASSWORD_PENDING`, worded in the dialog, which stays open | `password-dialog`, `link-refused-password-pending` |

English, dark, at 390 and 768 px (`shots/pr3/en-dark-{390,768}-*`) — the approval note's (d) and PR 3's screens:

| Case | Seen | Shots |
|---|---|---|
| The add sheet (PR 2) | fields spaced, «Create account and link» at its foot | `add-sheet` |
| The upgrade confirm (PR 2) | an existing user's email: «This email has an account», name «cc cc», joined, spaces «None», «Make sure this is the person you mean…», the submit «Upgrade and link» (closed without upgrading) | `upgrade-confirm` |
| The password dialog (PR 2) | the dialog over the page; handover recorded, toast «Handover recorded: Hala 390 · WhatsApp» (and 768) | `password-dialog` |
| A card's / row's menu | «Link to a space», «Unlink from Focus Hub», «Unlink from Demo Space» | `row-menu` |
| The link dialog from a row, an unverified space | «Golden Hub becomes verified and its owner edits it; the Masaha team no longer does.» (closed without linking) | `link-dialog` |
| The verified editor, its unlink | «Edited by …», the unlink buttons; «The other owners stay, and it stays verified.» | `editor-verified`, `unlink-dialog` |
| The unverified editor | «Link an owner» in the warning | `editor-unverified` |

Page errors (`Runtime.exceptionThrown`): none in any run. First-pass failures were the scripts' own (a menu step reused before the earlier dialog closed; a click on the wrong `[role=radio]` — the theme toggles carry that role too), each re-run passing; the first link attempt from Rima's row was the real `ACCOUNT_PASSWORD_PENDING` refusal, kept as its own case.
Servers stopped by PID (23460 tsx watch, 8352 server, 1684 pino-pretty, 23412 vite); `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` → none (`ports 3320 and 5320 free`); no `cdp-` Chrome left; `git status --short` → empty.

## 5. #PRNUM, push, PR

- `git grep -n "#PRNUM" HEAD` → 14 lines in `docs/`. Next number: `gh api …/issues?state=all&per_page=1&sort=created&direction=desc --jq '.[0].number'` → `90`, so **91** (checked again just before the push: `90`; no open PR).
- `git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#91/g'" origin/main..HEAD` → `Ref 'refs/heads/feat/admin-owner-links' was rewritten`; `git update-ref -d refs/original/…`; `git grep -n "#PRNUM" HEAD` → none; `git diff origin/main --stat` identical to before (58 files, 2202 insertions, 103 deletions).
- Commits now: `ac7122d7` fix(space-links): finish the add-owner sheet (44) · `766341f5` feat(space-links): link and unlink owners (41) · `54dae070` feat(spaces): name a verified space's owners (44). Head `54dae070a2fbb9ae0938d1868a74395f49d0f6f3`.
- `git push -u origin feat/admin-owner-links` → `* [new branch] feat/admin-owner-links -> feat/admin-owner-links`.
- `gh pr create --assignee @me --label feat --label area:web --label area:docs` → **https://github.com/Basel-Ghonaim/masaha/pull/91** (the number written in the docs).

## 6. Final report (2026-10-19)

### 6.1 The pull request and its head
**#91** https://github.com/Basel-Ghonaim/masaha/pull/91 — `feat(space-links): link and unlink owners`, head `54dae070a2fbb9ae0938d1868a74395f49d0f6f3`. `gh pr checks 91` on that head: build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck — all `pass`. `gh pr view 91 --json headRefOid,mergeStateStatus,state` → `{"headRefOid":"54dae070…","mergeStateStatus":"CLEAN","state":"OPEN"}`. Not merged.

### 6.2 The commits
`ac7122d7` fix(space-links): finish the add-owner sheet (44) · `766341f5` feat(space-links): link and unlink owners (41) · `54dae070` feat(spaces): name a verified space's owners (44). 58 files, `apps/web` and `docs` only. Bodies say why; no tool attribution; messages from UTF-8 LF files without a BOM, `git commit -F`.

### 6.3 What was run, and what was not
§3 above: unit 833 (web) / 743 (shared) / 216 (api); component 160 files / 1064 tests; build; check:build; check:classes (894 files); format:check; check:links (2212). Per commit: lint and typecheck clean. CI: all nine jobs pass, `test:api` included. **Not run locally:** `npm run test:api` — no `apps/api` or `packages/shared` change (CI ran it: pass).

### 6.4 Breaks and tests seen failing first
§2: commit 1 — 5 tests red before the code; commit 2 — 4 repository tests and 23 component tests red before the code, then 20 named breaks, each red; commit 3 — 6 tests red before the code, then 7 named breaks, each red. **No break stayed green.**

### 6.5 Problems met, and how each was solved
- Two new tests' own matching (commit 2): the unlink's line is cut around the space's name, and the admin refresh re-reads the space after the DELETE — the tests read the dialog's accessible description and find the DELETE by method.
- `useSpaceEditor.component.test.tsx`'s partial `AdminSpace` fixture had no `owners` → 10 tests `TypeError … reading 'map'`; `owners: []` added (the real read always carries it).
- `OwnersList.component.test.tsx` asserted the four columns; the actions column is the planned change, so the expectation gained «Actions» and the row's menu button.
- Shell heredocs failed to parse some multi-line edits (`unexpected EOF while looking for matching`); edits were written through script files instead (as the memory note warns).
- The real run's first passes: a script step reused a page with a dialog still open, and a click hit the theme toggle's `[role=radio]`; both fixed in the script, the steps re-run and passing.

### 6.6 Anything that behaved unexpectedly
- **Rima (rima.pr1, PR 1's owner) cannot be linked to another space:** her temporary password, issued when PR 1's run added her, was never changed, so #90's `ACCOUNT_PASSWORD_PENDING` refuses any link — the dialog words it and stays open (kept as a case). A probe link to a space she already owns answered `204`: the server finds the existing link before it checks the password, so a re-link of an existing owner never reports the pending password (API behaviour, not this PR's; noted, not a finding).
- `routes.component.test.tsx` › «lists the owner’s eleven pages…» failed once in a focused run of three suites together (its 3 s wait), passed on the re-run and in the full lane (finding 55/87's known wait).
- The first full component run was stopped by the owner before it produced a result; the lane was run once afterwards (§3).
- `useAddOwnerForm`'s add form now also meets `ACCOUNT_PASSWORD_PENDING` from `POST /admin/owners` (#90); it falls back to the errors catalogue's line there (out of this PR's scope; no form-specific words were planned).
- Finding 50's 2026-10-15 resolution still says «the repository has no web unlink UI» — true when written, in its dated paragraph; left as history.
- Two slips: the dev-only demo password and a throwaway test account's temporary password were printed into this session's tool output (§4). Nothing reached the repository, a commit, the PR or this report.

### 6.7 The early conflict check
`gh pr list --state open` → only #91 (`[{"headRefName":"feat/admin-owner-links","number":91}]`). No other open pull request, so no `merge-tree` to run. `origin/main` unchanged since the branch was cut (`18ab1705`).

### 6.8 Departures from the prompt and the plan
1. **The real run's tool:** local headless Chrome over CDP, not the `playwright` MCP tools (absent in this session) — the prompt's allowed fallback, as PR 2.
2. **Files beyond §7's list:** `types/PersonChoiceView.ts` (the person option's type); `OwnersList.component.test.tsx`, `useAddOwnerForm.component.test.tsx`, `useSpaceEditor.component.test.tsx` (expectation or fixture updates the change requires).
3. **Words beyond §9:** `spaceLinks.link.close` («إغلاق» / Close) for the dialog's close button; `spaceLinks.link.refusals.ACCOUNT_PASSWORD_PENDING` (the prompt's #90 instruction).
4. **Tests beyond §10:** the link dialog's success and «forgets the last refusal», the unlink hook's failed read and its 404, the dialogs' axe checks, `SpaceOwnersActions`' «holds the link while unsaved», the menu's active-owner case, and the editor's `unsaved` hand-on. Breaks were named as §10's; «both drawn» became «the link drawn, not the unlinks» (what a break of that branch can show); «the count taken from the row» became «the last owner assumed, not read» (the hook has no row count).
5. **Commit 2's subject is 41 characters,** where the plan counted 42.
6. **One `opener` ref** for the editor's unlink buttons (the button that opened the dialog), rather than one per button.

---

## Fix round 1 (2026-10-19) — `7_FIXES_PROMPT_PR3.md`, review `6_REVIEW_PR3_CLAUDE_CODE.md`

### FR1.1 First checks
`git rev-parse HEAD` → `54dae070…`; `git status` clean on `feat/admin-owner-links`; `gh pr view 91` → `CLEAN` at `54dae070`; `git fetch origin`: `origin/main` still `18ab1705`; open PRs: only #91; highest finding file 93, so **94** and **95** are free.

Where each fix goes: commit 1 ← fix 4 (`users.md`); commit 2 ← fix 1 (the unlink's fresh read), fix 3 (the person side), the `validation` line, the one dialog type, findings 94 and 95; commit 3 ← fix 2 (the editor's focus), «ربط مالك» `aria-disabled`, the unsaved rule's one home.

### FR1.2 Fixes and their tests

1. **The unlink's read (review 1)** — `useUnlinkOwnerDialog`: `reading = owners.isFetching`; the line and the toast's `last` come only from a read that is neither fetching nor failed (`reading || isError ? undefined : data`); «فك الربط» is disabled while `reading || blocked`. Chosen over `gcTime: 0`, which relies on the cache's removal timer firing before the next opening; this holds whatever the cache keeps, and a failed refetch now falls to the `ifLast` line. New test «reads the owners again on each opening, and waits for that read before it words or allows the unlink» (one `QueryClient`, open → unmount → owners changed → open again): red before the fix, `AssertionError: expected { before: '', …(2) } to be null` (the review's scenario reproduced), green after.
2. **Focus after a link or an unlink from the editor (review 2)** — `SpaceEditor` wraps the notice in a `div ref tabIndex={-1} outline-none` that stays while its content is swapped and hands it through the slot (`OwnedSpace.focusFallback`); `LinkOwnerDialog` and `UnlinkOwnerDialog` take an optional `fallbackFocus` and focus it when their `returnFocus` is no longer connected. Three new tests in `SpaceOwnersActions.component.test.tsx` with a harness that holds the actions as the editor does (a notice that stays, its content swapped by the space's verification, the owners changed by each link/unlink): «…when a link turns the space verified», «…when the last owner’s unlink turns the space unverified», «…when one of several owners is unlinked» — each red before the fix, `Error: expect(element).toHaveFocus()`, green after. `SpaceEditor.component.test.tsx`'s two slot tests now assert the fallback is the focusable element around the notice.
3. **The link's verification (review 4)** — **the person end** words the chosen space from the latest search answer (`spaces.options.find(id) ?? chosen`): new test «words the chosen space as the latest answer has it, not as it was when chosen» red before (`AssertionError: expected [ Array(1) ] to deeply equal [ Array(1) ]`), green after. **The space end** needs a new read (no answer fresher than the editor's own is in hand, and the link is offered only while that read says unverified): recorded as **finding 95**.
4. **`users.md` (review 5)** — *Web history*: «#91 — the one-time password dialog's person isolated, in its description and its handover toast.» (folded into commit 1).
5. **Nits** — «ربط مالك» waits `aria-disabled`, its reason its description, the click guarded (`if (space.unsaved) return`): the test «holds the link while the editor has unsaved changes, saying why, and keeps it in reach» (tab reaches it; a click opens nothing) red before (`expect(element).toHaveAttribute("aria-disabled", "true")`), green after. `link.refusals.validation` → «لم يعد هذا الحساب موجودًا.» / “That account no longer exists.” (its `it.each` expectation changed first: red, then green). `types/OwnerDialog.ts` declared once, used by both hooks. **Finding 94** (a receptionist offered as «مستخدم»). The unsaved rule kept in **one home**: its behaviour and decision in `space-links.md` (with the new focus decision); `spaces.md`'s behaviour line links there and its duplicate decision is gone (the slot decision now names the notice it hands) — so no finding for it.
6. Screenshots: §FR1.5.

### FR1.3 Breaks (each made once, its focused test run, the file restored from a copy)

| Break | Result | First error |
|---|---|---|
| fix 1: a cached read taken for this opening (isPending, not isFetching) | red — `Tests  1 failed / 5 skipped (6)` | `AssertionError: expected { before: '', …(2) } to be null` |
| fix 3: the chosen space kept as it was when chosen | red — `Tests  1 failed / 11 skipped (12)` | `AssertionError: expected [ Array(1) ] to deeply equal [ Array(1) ]` |
| fix 2: the link dialog drops the fallback | red — `Tests  1 failed / 5 skipped (6)` | `Error: expect(element).toHaveFocus()` |
| fix 2: the unlink dialog drops the fallback (last owner) | red — `Tests  1 failed / 5 skipped (6)` | `Error: expect(element).toHaveFocus()` |
| fix 2: the unlink dialog drops the fallback (one of several) | red — `Tests  1 failed / 5 skipped (6)` | `Error: expect(element).toHaveFocus()` |
| fix 2: the editor hands no notice (ref dropped) | red — `Tests  2 failed / 25 skipped (27)` | `Error: expect(received).toHaveAttribute()` |
| nit 6: the waiting link opens all the same | red — `Tests  1 failed / 5 skipped (6)` | `Error: expect(element).not.toBeInTheDocument()` |
| nit 6: the link disabled again (out of the tab order) | red — `Tests  1 failed / 5 skipped (6)` | `Error: expect(element).toHaveAttribute("aria-disabled", "true") // element.getAttribute("aria-disabled") === "true"` |

Touched files after the breaks: `npx vitest run --project component src/features/space-links/hooks/link …/hooks/unlink …/components/owner-actions …/components/link …/components/unlink` → `Tests  25 passed (25)` (commit 2's fixes); `npx vitest run --project component src/features/space-links/components src/features/space-links/hooks/link src/features/space-links/hooks/unlink …/SpaceEditor.component.test.tsx …/useSpaceEditor.component.test.tsx` → `Test Files  12 passed (12)` / `Tests  111 passed (111)` (all fixes).

### FR1.4 Folded commits and the checks the round touches

Three `amend! <subject>` commits (a message file each: `git commit --fixup=amend:<sha> -F` is refused — `fatal: options '-F' and '--fixup' cannot be used together` — and a commit whose subject begins `amend! ` is folded the same way), then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main` → tree before and after identical. Commits: `5ae65fc9` fix(space-links): finish the add-owner sheet (44) · `82126047` feat(space-links): link and unlink owners (41) · `db1fc6f0` feat(spaces): name a verified space's owners (44); subjects unchanged, bodies extended with the why.
Per commit (checked out detached, then back): `5ae65fc9` and `82126047` → typecheck 0 errors, lint exit 0. On the head `db1fc6f0`: `npm run typecheck` → 0 errors; `npm run lint` → exit 0; `npm run check:classes` → `No physical direction or arbitrary-value classes in 895 files.`; `npm run format:check` → `All matched files use Prettier code style!`; `npm run check:links` → `2220 links in 176 documents and 1279 source files all resolve.` Not run (the owner's rule for this round): the full unit and component lanes, the build, `check:build`, `test:api` — CI runs them.

### FR1.5 The real run of the round (review 3, and fix 2 seen in the app)

Headless Chrome over CDP (as before); `masaha-postgres-1` up; API on 3320 and web on 5320 started from the head `db1fc6f0`. Arabic light at 390 and 768 and English dark at 1440 (`shots/pr3/`): `{ar-light-390,ar-light-768,en-dark-1440}-{row-menu,link-dialog,editor-verified,unlink-dialog,editor-unverified,link-dialog-from-space}.png` — 18 shots: the cards or rows with a menu open, the link dialog from a row (Golden Hub: «becomes verified»), the verified editor («يعدّلها أحمد الشوا، basel» / “Edited by …”) and its unlink dialog («يبقى المالكون الآخرون…»), the unverified editor («ربط مالك») and its link dialog from the space. Every dialog closed without acting.
The focus, in the app (Arabic, 768, Golden Hub): linked basel from the editor → `after the link, focus on: DIV[tabindex=-1] يعدّلها basel…` (`ar-light-768-focus-after-link`); the demo owner linked by the API (`204`), then unlinked from the editor, one of two → `DIV[tabindex=-1] يعدّلها basel…`; then basel, the last owner, unlinked → `DIV[tabindex=-1] أنت تعدّل مساحة غير موثّقة…` (`ar-light-768-focus-after-last-unlink`). Golden Hub ends unverified, as it began. Page errors: none.
Servers stopped by PID (30224 28388 32784 21308); ports 3320 and 5320 free; no `cdp-` Chrome left; `git status --short` empty. No secret printed this round.

### FR1.6 Push, description, CI, state

- `git fetch origin`: `origin/main` still `18ab1705`. `git push --force-with-lease=feat/admin-owner-links:54dae070… origin feat/admin-owner-links` → `+ 54dae070...db1fc6f0 feat/admin-owner-links -> feat/admin-owner-links (forced update)`.
- PR description updated (`gh pr edit 91 --body-file …`): a *Review fixes (round 1)* section; Evidence split by head (this round's touched checks on `db1fc6f0`, the full lanes on the first head); Screenshots now naming the full matrix taken; findings 94 and 95.
- `gh pr checks 91 --watch` on `db1fc6f0`: build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck — all `pass` (CodeRabbit `pass`). `gh pr view 91 --json headRefOid,mergeStateStatus` → `{"headRefOid":"db1fc6f0ee6d5752b642fb3b3d55e02dcbd47e51","mergeStateStatus":"CLEAN"}`. `git status --short` → empty.

### FR1.7 Round summary (final-report order)

1. **PR and head:** #91, `db1fc6f0ee6d5752b642fb3b3d55e02dcbd47e51`, CI green, `CLEAN`, not merged.
2. **Commits:** `5ae65fc9` fix(space-links): finish the add-owner sheet (44) · `82126047` feat(space-links): link and unlink owners (41) · `db1fc6f0` feat(spaces): name a verified space's owners (44).
3. **Run / not run:** FR1.4 (lint, typecheck per commit and on the head; touched files 111/111; check:classes, format:check, check:links). Not run locally: full lanes, build, check:build, test:api — the owner's rule for this round; CI ran all and passed.
4. **Breaks and first-failing tests:** FR1.2 (each new test red before its fix) and FR1.3 (8 breaks, all red; none stayed green).
5. **Problems:** `git commit --fixup=amend:<sha> -F` is refused by git; the `amend! <subject>` message form was used instead (same autosquash). A typecheck error in the new link test (a literal's narrowed type) fixed in the test.
6. **Unexpected:** after a confirmed unlink the dialog's line briefly shows its placeholder while the admin refresh refetches the space's owners (the dialog is busy then and closes once the lists arrive) — a consequence of treating any fetch as reading; harmless, noted.
7. **Conflict check:** `gh pr list --state open` → only #91; nothing to `merge-tree`.
8. **Departures:** review 1 fixed by `isFetching` rather than `gcTime: 0` (holds whatever the cache keeps, and covers a failed refetch); the focus fallback's tests use a harness that holds `SpaceOwnersActions` as `SpaceEditor` does, since a `spaces` test cannot import `space-links` (the editor's own test asserts the fallback it hands); the space end of review 4 recorded as finding 95 (it needs a new read); the unsaved rule's second home removed rather than recorded as a finding; findings numbered 94 and 95 from the index.

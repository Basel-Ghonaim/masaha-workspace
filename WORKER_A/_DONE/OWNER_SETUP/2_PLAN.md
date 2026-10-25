# OWNER_SETUP — the owner sets up their space: profile, prices & packages, staff, settings (screens 20, 21, 22, 24) — the plan

> Written 2026-10-19 from `origin/main` **`eff0a3d1`** (#88–#92 merged: OWNERS, STAFF, SETTINGS) **plus USERS**,
> `feat/admin-users` at **`4daedc94`** (pushed, not merged; its PR is #93 in its own documents). **The executor
> starts only after USERS has merged**, and its first step is `git diff --name-status 4daedc94 origin/main`
> (§13). Two PRs in sequence (the owner's decision 1): **PR 1** — the space profile and Prices & packages
> (screens 20, 21), branch `feat/owner-space-profile`, seven commits, ≈ 105 files; **PR 2** — staff and settings
> (screens 22, 24), branch `feat/owner-staff-settings`, cut from `main` once PR 1 has merged, six commits,
> ≈ 60 files. Both are reviewed in a separate conversation (over 25 files). The executor may be any capable
> coding agent: no step depends on a Claude skill (the appendix is only a map).
>
> Finding numbers are written `<n>`, `<n+1>`: the next free ones on the latest index when the executor
> starts. `#PRNUM` stands for the PR's number until the push (§13).

> **Approved by the owner, 2026-10-20 — binding on every executor of this plan** (it wins where the plan
> below differs):
> - **§14 as the supervisor recommended:** (1) the plan with S1–S11 — S1's explicit threading, not A1 —
>   **except S4, replaced by A3** (below); (2) the retired amenities accepted for v1 with the counting line,
>   finding `<n>` recorded, A2 not taken; (3) findings 67, 81, 90 and 96 folded; (4) design issues 1–18 as
>   written, **15 folded** (no finding `<n+1>`: §13 check 6's `<n+2>`, if needed, becomes `<n+1>`); (6) finding 92
>   left for a later API decision; (7) the Arabic copy as written, with the corrections below.
> - **A4 taken — three PRs, not two**, each cut from the latest `origin/main` once the one before it has
>   merged, each with its own execution prompt (`3_EXEC_PROMPT_PR<n>.md`) and its own review:
>   - **PR 1** `feat/owner-space-profile` — the plan's commits 1–5 (≈ 70 files); title = commit 5's subject.
>   - **PR 2** `feat/owner-packages` — the plan's commits 6–7 (≈ 40 files); title = commit 7's subject;
>     tests 13, 15–20 and test 14's Packages case; the Packages page's real-run cases.
>   - **PR 3** `feat/owner-staff-settings` — the plan's "PR 2" (its commits 1–6, tests 21–41).
>   Wherever the plan says "PR 1", read PRs 1 and 2, split at commit 5/6; where it says "PR 2", read PR 3.
>   Each PR's docs lines (`overview.md`, `architecture.md`, `docs/README.md`) say only what that PR built.
> - **A3 taken (replaces S4):** USERS' one-time password dialog takes the handover's write from its caller —
>   a required `recordHandover` (the user and the channel in, a promise out) — instead of a place; the
>   dialog keeps its pending state and its outcome lines as today («لم تُسجَّل طريقة التسليم» on
>   `not_found` or `TEMPORARY_PASSWORD_NOT_PENDING`). `users` exports the admin's (its repository's
>   `/admin/users/:id/temporary-password/handover`), passed by `OwnersPage` and `IssuePasswordDialog`;
>   `staff` owns the space's (`StaffRepository.handOver`, `POST
>   /manage/spaces/:spaceId/staff/:userId/temporary-password/handover`), passed by `StaffPage`. *Why:* the
>   route is the space-links module's; the capability that serves it holds its call. Test 21 moves to
>   `staffRepository.unit.test.ts`; test 22 becomes "records the handover through the write its caller
>   gives" (break: the dialog ignores it). The exact shape is the executor's, within these lines.
> - **The refusal lines' causes (a correction found in review):** the managed boundary answers **404** to a
>   caller with no active link (`requireSpaceAccess`, `docs/backend/security.md`), so a link ended meanwhile
>   is a 404, never a 403; an owner's 403 means only that the action is no longer theirs. Therefore:
>   - every owner-side `forbidden` line names no cause: the editor (S6) and the settings «لم يعد هذا متاحًا
>     لك في هذه المساحة؛ لم يُحفظ شيء.» / "This is no longer open to you at this space; nothing was saved.";
>     the packages the same; the staff's add «لم يعد هذا متاحًا لك في هذه المساحة؛ لم يُضف أحد.» / "…; no
>     one was added."; the staff's actions «لم يعد هذا متاحًا لك في هذه المساحة.» / "This is no longer open
>     to you at this space.";
>   - S6's 404 «لم تعد هذه المساحة متاحة لك.» stays for the editor; a 404 on a package's or a staff
>     member's route says both causes: «لم تعد هذه الباقة موجودة، أو لم تعد المساحة متاحة لك.» / "This
>     package no longer exists, or the space is no longer open to you." and «لم يعد هذا الشخص من موظفي
>     المساحة، أو لم تعد المساحة متاحة لك.» / "This person is no longer on the space's staff, or the space
>     is no longer open to you.";
>   - test 11's title becomes "never tells the owner the space was verified meanwhile, on a 403" (its break
>     unchanged).
> - **Copy:** `staff.count` zero «لا يوجد موظفون» (not «لا موظفون»), as `spaceLinks`' «لا يوجد أصحاب مساحات».
> - **The owner's review rule (2026-10-20):** a serious or large review fix reopens its PR (folded into its
>   commit); small ones are deferred to the **next PR as a dedicated commit at its start**, named in that
>   PR's description. If the supervisor leaves a `0_CARRIED_FROM_<n>.md` naming one of these PRs, its items
>   are that PR's first commit — `#93`'s carried items, if any, open PR 1.

## 1. Summary

The owner's four setup screens, on the web only; every API they call is built.

- **PR 1.** The owner's **Space profile** (20) is the admin's editor, the same component with a second
  *place* (O1): its calls go to `/manage/spaces/:spaceId/…`, its cache sits under the space's scope, and the
  place decides only what the owner's page shows differently — a head line with the public page's link,
  the prices as a link row to Prices & packages, no owners' notice, no link to the platform's amenities list,
  the lookups' fields read from the public catalogue. **Prices & packages** (21) puts the same prices
  section on a page of its own («الأسعار المعلنة», O6) above the new `packages` feature: the private
  packages as rows, each offered or paused by its switch, added and edited in the package sheet (O8). Before
  them: the shekel helpers move to `shared/lib` (prices and packages both type money), and the prices table
  starts at 1024 px (finding 67).
- **PR 2.** **Staff** (22), the new `staff` feature over the `space-links` module's staff routes: the
  reception accounts as a table; adding one in one submit, the consequence said first, then USERS' one-time
  password dialog recording its handover on the managed route; «إيقاف وصوله» through an `AlertDialog`
  saying the sessions end; re-activation at once; a new temporary password only while one is pending; the
  pending badge; every refusal in the owner's own words (finding 90). **Settings** (24), the new
  `space-settings` web feature: visit pricing, reception's hand-typed prices and the reminder template
  (an editor whose buttons insert the three placeholders, its two refusals worded); and the page's
  attendance card «الحضور والحالة المباشرة», which saves the capacity (`occupancy`) and then the
  settings in one save, saying exactly what was saved when the second fails (finding 96).

## 2. The contract

### Scope

**PR 1**
- `shared/lib`: the shekel helpers (`agorotOf`, `shekelsOf`, `priceText`) moved from `features/spaces/services`.
- `features/spaces`: the editor takes a place, `admin` or `owner`, which picks its calls, its keys, what a
  write refreshes, who may edit, the refusals' words and the frame's differences; the owner's frame; the
  prices section exported for its own page (`SpacePricesEditor`) and the space's shifts for the packages
  (`useSpaceShifts`); the prices table from `lg` (finding 67).
- `features/lookups`: `AreaSelect` and `AmenityChecklist` take a `source`, `admin` or `public`.
- `features/packages` (new, dashboard-only): the private packages list, the switch, the sheet, a paused
  package's held shift (finding 81).
- `pages/dashboard`: `space/ProfilePage`, `space/PackagesPage`, the space pages' lazy map in `routes.tsx`,
  the space pages' paths in `navigation.ts`; `admin/SpaceEditPage` and `admin/AddSpacePage` pass the new
  props.
- Copy (both catalogues): `spaces`, `lookups`, a new `packages` section.
- Docs: `features/spaces.md`, `packages.md`, `lookups.md`, `frontend/architecture.md`, `project/overview.md`,
  `docs/README.md` (the map's lines), findings 67 and 81 resolved, finding `<n>` recorded.

**PR 2**
- `features/users`: the one-time password dialog's `handover` prop (`admin` or a space).
- `features/staff` (new, dashboard-only): the list, the add sheet, the row menu, the deactivation, the
  re-activation, the re-issue.
- `features/space-settings` (new, dashboard-only): the settings' query and save, the card frame, the visit
  pricing, reception and reminder cards.
- `features/occupancy` (new web feature): the capacity's query and save, as hooks.
- `pages/dashboard`: `space/StaffPage`, `space/SettingsPage`, `space/settings/AttendanceCard` and its hook.
- Copy: `staff`, `spaceSettings` sections; `users` (the forced change's line, design issue 15, if approved).
- Docs: `features/space-links.md` (its staff web section), `space-settings.md`, `occupancy.md`, `users.md`,
  `frontend/architecture.md`, `project/overview.md`, `docs/README.md`, findings 90 and 96 resolved.

### Acceptance criteria

**PR 1**
- [ ] The demo owner opens «ملف المساحة»: the five fact groups and the photos, each section saved, dated
  and confirmed alone on the managed routes; the head line with «عرض الصفحة العامة»; «الأسعار» as a row
  with its date and a link to «الباقات والأسعار»; no owners' notice; the missing checklist; the leave
  guard. Reception is refused the page (403 in the shell).
- [ ] The owner's area and amenity fields read only `GET /lookups`; no `/admin/*` request leaves the
  owner's pages (proven by the component tests and the real run's network log).
- [ ] The admin's editor behaves as before (its tests unchanged but for the `'admin'` argument), its prices
  table now from 1024 px.
- [ ] «الباقات والأسعار»: «الأسعار المعلنة» saved, dated and confirmed, with its own leave guard; the
  private packages listed whole, retired ones on a muted row with «موقوفة»; the switch offers or pauses one
  at once; the sheet adds and edits one (validity, limits on demand, billing with its labelled amount, the
  audience, the space's shifts), checked in the browser by the contract's schema, a repeated name on its
  field; a paused package that keeps its shift says so and clears it (finding 81).
- [ ] Every counted noun through the catalogue's plural forms (O5).
- [ ] Lint, typecheck, `test:unit`, `test:component`, build, `check:build`, `check:classes`,
  `format:check`, `check:links` green; CI green; `CLEAN`.

**PR 2**
- [ ] «الموظفون»: the reception links as a table from 768 px (cards below), name and email, the state
  («نشط» / «بلا وصول») and «لم يغيّر كلمة المرور المؤقتة بعد» (or its expired form); empty state.
- [ ] «إضافة موظف» in one submit, the consequence said before it; then the one-time dialog, its handover
  recorded on `POST /manage/spaces/:spaceId/staff/:userId/temporary-password/handover`; `EMAIL_HAS_ACCOUNT`
  on the email field in the owner's words.
- [ ] «إيقاف وصوله» asks in an `AlertDialog` that says every session ends, opens on «رجوع», its
  destructive action staying until the answer, a refusal inside; «إعادة وصوله» at once; «كلمة مرور
  مؤقتة جديدة» held with its reason unless one is pending; every refusal of the staff routes worded
  (finding 90).
- [ ] «الإعدادات»: the attendance card saves the capacity, then the settings, in one save; if the second
  fails it says what was saved and what was not, and keeps the form's values (finding 96); visit pricing,
  reception and the reminder each save alone; the reminder's buttons insert `{الاسم}`, `{المبلغ}`,
  `{المساحة}` at the caret; its two refusals worded (a missing amount, an unknown placeholder named).
- [ ] The same checks and CI as PR 1.

### Out of scope

- Any API, `packages/shared`, schema, migration or dependency change (§14 if one seems needed).
- The owner's overview, data-report notices on the profile (`OwnerReportNotice`, step 10), the
  collections per staff member (step 9), the account settings (`/me`), the sidebar's task groups (P3), the
  owner's audit (finding 14), the platform's defaults editor (finding 97, step 11).
- The admin's editor's behaviour, but for finding 67's breakpoint.
- Findings 80, 91, 92, 93 (API or owner decisions; §6).

## 3. The reading done

`CLAUDE.md`; `docs/development/workflow.md`; `testing.md`; `docs/frontend/architecture.md` (and USERS' diff to
it); `design-system/foundation.md` (§9, §10, §12 fields, §13 screens 20–24); `localisation.md`;
`documentation.md` §5; `docs/features/spaces.md`, `packages.md`, `space-links.md` and `users.md` (USERS'
versions), `space-settings.md`, `occupancy.md`; `docs/api/api-contract.md` §1–4 and the managed routes
(space, photos, packages, staff, settings, capacity) and the admin's photos and temporary password; ADR 0009;
`docs/plans/v1-mvp.md` steps 5, 6, 11; `docs/design/SCREENS.md`; the prototype pages `Owner space profile.html`,
`Packages.html`, `Staff.html`, `Owner settings.html` and `masaha/profile-b.jsx`'s prices and amenities;
`DECISIONS_OWNER.md`, `DECISIONS_SHARED.md`; the findings index and findings 14, 67, 74, 80, 81, 87, 90–93,
96, 97; the code of `features/spaces` (the repository, the keys, the editor, its sections' hooks, the
photos' hooks, `useRefreshAdmin`), `features/lookups` (`useAreaOptions`, `useAmenityChecklist`, the keys,
the repository), `features/users` (the one-time dialog, `useHandover`, the repository), `features/space-links`
(the index, the add-owner form), `shared/forms` (`useServerForm`, `schemaResolver`), `shared/copy`
(`plural.ts`, the sections), `shared/routing` (`dashboardPaths.ts`), `pages/dashboard` (`navigation.ts`,
`routes.tsx` and its test's titles, `SpaceEditPage`, `OwnersPage`, `SpaceLayout`, `useSpaceShell`,
`PageHeader`), `scripts/dashboardOnly.ts`, `packages/shared` (`packages`, `space-settings`,
`occupancy`, `space-links` staff), the demo seed (`apps/api/src/db/seed/demo.ts`); USERS' `3_EXEC_PROMPT.md` and
`2_PLAN.md` for the procedure's shape.

**What the reading changed.** The editor's lookups fields read the admin's lists (`/admin/amenities`,
`/admin/governorates`), which refuse an owner (403): the owner's page cannot reuse them as they are (S2).
The editor's refusal lines say "verified meanwhile" for a 403, which is the admin's cause, not the owner's
(S6). Documentation §5 settles where the staff web feature is documented: a section of `space-links.md`.

## 4. The owner's decisions, as they will be built

1. **Two PRs in sequence** (PR 1: screens 20, 21; PR 2: 22, 24); PR 2 from `main` after PR 1 merges.
2. **One editor, two permissions (O1).** `SpaceEditor` takes `place`, a discriminated prop:
   `{ kind: 'admin'; ownerActions; amenitiesListLink; areaName; amenityNames }` or
   `{ kind: 'owner'; pricesLink }`. Everything else is the same component, the same sections, the same
   hooks. Who may edit is the server's (`adminWhileUnverifiedElseOwner`); the page shows it through one pure
   rule, `mayEdit(place, isVerified)` (admin: unverified; owner: verified — an owner's link *is* the
   verification), and a refusal fetches the space again as today.
3. **Prices live in Prices & packages (O6).** On the owner's place the editor draws «الأسعار» as a link row
   (its date, «قديمة», «لم تُضف بعد», «تُعدَّل وتُؤكَّد في الباقات والأسعار», a link). The Packages page
   shows the same prices section, titled «الأسعار المعلنة», with its own date, confirm and leave guard. The
   admin's editor keeps its prices section. Packages as O8.
4. **The attendance card (O2)** is one card, one save: `PUT …/capacity` first, then `PATCH …/settings`, each
   only when its part changed. A second failure says «حُفظت السعة، ولم تُحفظ إعدادات الخروج التلقائي»
   with the refusal, the saved capacity becomes the card's new baseline, and the form keeps every value —
   finding 96 resolved. The reminder template is built with its insert buttons and both refusals.
5. **Staff (OW-017–019, O4)** as §2 says.
6. **Claude Code throughout** — nothing in the procedure needs it (the appendix is only a map).

## 5. Stronger decisions

**S1 — the place is threaded explicitly, as `spaceId` is, through one scope table.** Each editor hook that
reads or writes the space takes `place: EditorPlace` beside the space's id; `hooks/editor/editorScope.ts` is
the one home of what differs by place for data: the repository, the space's, the photos' and the writes'
keys, the scope a write marks out of date, and the scope that holds the lookups' lists. *Why:* the codebase
threads `spaceId` the same way; a hook's inputs stay visible; a context would default silently. *Cost:* ≈ 20
hook signatures and their tests change mechanically (`'admin'` added). *Recommend:* take it (alternative A1
below).

**S2 — the owner's lookups fields read the public catalogue.** `AreaSelect` and `AmenityChecklist` take a
required `source: 'admin' | 'public'`. `public` reads `GET /lookups` only: an area hidden since shows as
«المنطقة الحالية — لم تعد متاحة للاختيار» (never sent, since the profile sends only changed fields); a
retired amenity the space still has stays in the value, unseen, and one line counts them. *Why:* the admin's
lists answer an owner 403; the space's own fields must still save. *Cost:* two lookups hooks, two props, one
new finding (`<n>`: the owner cannot see or remove a retired amenity by name). *Recommend:* take it; the API
read that would name them is §14.2.

**S3 — the shekel helpers move to `shared/lib`.** `agorotOf`, `shekelsOf` and `priceText` become
`shared/lib/money/`, with their unit tests. *Why:* packages type and show amounts as prices do; a copy would
drift (engineering principles §1, the second instance). `shared/lib` is already in architecture §1's list;
this builds it. *Cost:* one refactor commit, three importers. *Recommend:* take it.

**S4 — the handover's route is a prop of USERS' dialog, `handover: { at: 'admin' } | { at: 'space'; spaceId }`, required.**
`useHandover` sends to `/admin/users/:id/…/handover` or `/manage/spaces/:spaceId/staff/:id/…/handover`. *Why:*
one dialog (#89's), and the handover's write is `users`' in the API (`recordHandoverLocked`), shared by both
routes; required, as USERS made `kind`, so no caller can forget the place. *Cost:* `users`' repository names a
route under the space-links module's path; the two existing callers pass `{ at: 'admin' }`. *Recommend:* take
it (alternative A3).

**S5 — the staff web feature is documented as a section of `space-links.md`,** by documentation §5 ("a web
feature that serves a second audience over the same module is a section of that module's document"), not a
new `staff.md`. *Recommend:* as the rule says.

**S6 — a refusal's words follow the place.** For the owner, a 403 says «انتهى ربطك بهذه المساحة في
الأثناء؛ لم يُحفظ شيء.» and a 404 «لم تعد هذه المساحة متاحة لك.» (the managed boundary answers 404
without a link), where the admin's say "verified meanwhile" / "deleted meanwhile". One helper,
`meanwhileLines(place, copy)`, feeds every section, the confirmation and the gallery. *Why:* the admin's
cause would be false for the owner. *Recommend:* take it.

**S7 — the owner's writes mark the signed-in user's scope out of date (`['me']`, fetched now).** *Why:* the
switcher shows the space's name and area, which «المساحة» changes; it is `space-links`' key, so the whole
scope, as the admin's writes mark the admin's. *Cost:* one small `GET /manage/spaces` after an owner's save.
*Recommend:* take it.

**S8 — the attendance card is composed in the page,** `pages/dashboard/space/settings/` (a component and its
hook), from `occupancy`'s and `space-settings`' exported hooks and the card frame `space-settings`
exports; its form checks with a `FormSchema` that runs both contract schemas and merges their issues. *Why:*
"a component that combines several capabilities never lives in one of them" (architecture §3); `pages/` holds
`useLookupsTab` already; no zod internals are needed. *Recommend:* take it.

**S9 — finding 67 is folded:** the prices table starts at `lg`, cards below — the admin's editor too (one
editor). *Why:* foundation §9 (more than five columns → cards below `lg`); the owner's page has the same
width problem. *Cost:* class changes in one component. *Recommend:* fold.

**S10 — every disabled action stays reachable with its reason** (foundation §10): the staff row's
«كلمة مرور مؤقتة جديدة» is held, not hidden, when nothing is pending («غيّر كلمة المرور المؤقتة؛ إن نسي
كلمة مروره يستعيدها بالبريد») and on a deactivated row («أعد وصوله أولًا»). *Why:* the owner learns the
way out instead of a missing item. *Recommend:* take it.

**S11 — the package edit sends its terms whole** (limits off as `null`); the server writes and audits only
what changed. *Why:* one `prepare` for add and edit; no client diff to drift. *Recommend:* take it.

**No rule is weakened.** The authorization stays the server's (the page only mirrors `can()` for display, S1's
`mayEdit`); the design system is not changed (a missing full-width sheet is a finding, §13 check 6).

### Proposed alternatives (the owner may prefer them)

- **A1 — a feature-internal context for the place** (architecture §3's experimental clause): `SpaceEditor`
  provides it, the hooks read it. *Why:* ≈ 20 hook signatures and their tests unchanged. *Cost:* the clause is
  for shared client *state*, and a missing provider would fall back silently; the experiment would need
  judging. *If taken:* S1's commit 2 shrinks to the provider and `editorScope`; the tests wrap the provider.
- **A2 — a managed read of the lookups** (`GET /manage/spaces/:id/lookups` or retired names in `/lookups`),
  by worker B, so the owner sees and removes a retired amenity by name. *Cost:* an API item. *If taken:*
  finding `<n>` resolves with it; S2's public source stays for the area.
- **A3 — the dialog takes a `recordHandover` function** from the caller instead of a place. *Why:* `users`
  would name no space route. *Cost:* each caller needs a handover mutation; `users` exports one for the admin.
- **A4 — split PR 1** into 1a (commits 1–5: the profile) and 1b (6–7: Prices & packages), ≈ 70 and ≈ 40
  files. *Why:* two smaller reviews. *Cost:* a third PR and its CI. Not taken: the owner chose two PRs.
- **A5 — the attendance card as two saves** (one per capability): no partial state at all. *Cost:* departs from
  O2/DI-38. Not taken: the owner decided one save.

## 6. Related findings

| Finding | Folded? | Why · cost |
|---|---|---|
| **96** the attendance card saves two capabilities | **Yes, PR 2** | The owner's decision 4; resolved with the order and the partial line. |
| **90** the staff refusals reuse the admin's messages | **Yes, PR 2** | The staff screen words them itself (field and failure lines in `staff`); the shared `errors` lines stay the admin's, so worker B's errors catalogues are not touched. Small. |
| **81** a retired package's shift blocks the shift's removal | **Yes, PR 1** | The packages row says it and offers «إزالة الوردية» (`PATCH {shiftId: null}`). Small. |
| **67** the prices table cuts its shift at 768 | **Yes, PR 1** (S9) | One component's classes. |
| 87 the owners shell cold-loads `space-links` | No | Record the routes test's time, as USERS did; a timeout stops (§13). |
| 92 an owner can end another space's owner's sessions | No | An owner decision (§14.6); the web cannot tell a person's other links. |
| 93 three staff refusals untested | No | API tests (`apps/api`): outside this item. |
| 91 a pending account locks its address | No | An owner decision; the add sheet's line says an existing email is refused. |
| 80 packages' price check in the database | No | A migration (worker B's desk step). |
| 14 the owner's audit screen | No | Step 11. |
| 97 the rounding rule written twice | No | The defaults' editor (step 11); this item reads `@masaha/shared/space-settings` only. |
| 74 the design's gallery copy | No | The archive; the built gallery already says the contract's limits. |
| **New `<n>`** the owner's checklist cannot name a retired amenity | Recorded in PR 1 | S2. Resolves with A2, or when the public catalogue names retired amenities a space holds. |

## 7. The files

**PR 1** (A: added, M: modified, D: deleted, R: renamed).
- `apps/web/src/shared/lib/` — A `index.ts`, A `money/shekels.ts`, A `money/shekels.unit.test.ts`,
  R `features/spaces/services/priceText.ts` → `shared/lib/money/priceText.ts` (and its test).
- `features/spaces/services/` — M `pricesForm.ts` (imports `agorotOf`, `shekelsOf`), M `pricesForm.unit.test.ts`
  (its `agorotOf`/`shekelsOf` cases move to `shekels.unit.test.ts`); A `mayEdit.ts` + `mayEdit.unit.test.ts`.
- `features/spaces/repository/` — M `spacesRepository.ts` (the admin's life only: create, hidden, delete,
  restore), A `spaceEditorRepository.ts` + `.unit.test.ts` (the editor's calls, by place), M its existing test.
- `features/spaces/types/` — A `EditorPlace.ts` (`EditorPlace`, `AdminPlace`, `OwnerPlace`).
- `features/spaces/hooks/` — A `editor/editorScope.ts` + `.unit.test.ts`, A `editor/meanwhileLines.ts`,
  M `queryKeys.ts`, M `mutationKeys.ts`, M `useRefreshAdmin.ts`, M `add/useCreateSpace.ts`,
  M `editor/useSpaceQuery.ts`, `useSpaceAnswer.ts`, `useSaveGroup.ts`, `useSpaceEditor.ts`, `useSectionFrame.ts`,
  `useSpaceName.ts`, M `confirm/useConfirmGroup.ts`, M `profile/useProfileSection.ts`, `hours/useHoursSection.ts`,
  `prices/usePricesSection.ts`, `amenities/useAmenitiesSection.ts`, `contacts/useContactsSection.ts`,
  M `photos/usePhotosQuery.ts`, `usePhotoGallery.ts`, `usePhotoOrder.ts`, `usePhotoRemove.ts`, `usePhotoUploads.ts`,
  `staleGallery.ts`, `useReadOnlyPhotos.ts`, M `prices/useReadOnlyPrices.ts` (import); A `prices/useSpacePricesEditor.ts`,
  A `editor/useSpaceShifts.ts`, A `editor/usePricesLink.ts`; and each of these hooks' existing tests (M, the
  `'admin'` argument), plus the new tests of §10.
- `features/spaces/components/` — M `editor/SpaceEditor.tsx`, A `editor/OwnerHead.tsx`, A `editor/PricesLinkCard.tsx`,
  M `profile/ProfileSection.tsx`, `hours/HoursSection.tsx`, `prices/PricesSection.tsx` (place, the note's link,
  `lg`), `amenities/AmenitiesSection.tsx` (`listLink: string | null`), `contacts/ContactsSection.tsx`,
  `photos/PhotosSection.tsx`, `photos/ReadOnlyPhotos.tsx`; A `prices/SpacePricesEditor.tsx`; M `index.ts`.
- `features/lookups/` — M `hooks/area/useAreaOptions.ts`, `hooks/amenities/useAmenityChecklist.ts`,
  `components/area/AreaSelect.tsx`, `components/amenities/AmenityChecklist.tsx`, their tests; A
  `types/LookupsSource.ts`; M `index.ts` (the type).
- `features/packages/` (A, whole): `index.ts`; `repository/packagesRepository.ts` + `.unit.test.ts`;
  `hooks/queryKeys.ts`; `hooks/list/usePackagesQuery.ts`, `usePackagesSection.ts` (+ test);
  `hooks/toggle/useSetPackageActive.ts`; `hooks/shift/useClearPackageShift.ts`; `hooks/sheet/usePackageSheet.ts`
  (+ test), `useCreatePackage.ts`, `useUpdatePackage.ts`; `services/packageSummary.ts` (+ unit test),
  `services/packageValues.ts` (+ unit test); `types/ShiftChoice.ts`, `types/PackageRowView.ts`;
  `components/PackagesSection.tsx` (+ component test), `components/list/PackageRow.tsx`,
  `components/sheet/PackageSheet.tsx`, `components/sheet/LimitsField.tsx`.
- `pages/dashboard/` — A `space/ProfilePage.tsx`, A `space/PackagesPage.tsx`, M `routes.tsx` (`SPACE_PAGES`),
  M `navigation.ts` (`spacePagePath`), M `routes.component.test.tsx`, M `admin/SpaceEditPage.tsx`,
  M `admin/AddSpacePage.tsx` (`source="admin"`).
- `shared/copy/{english,arabic}/` — M `spaces.ts`, `lookups.ts`, `dashboard.ts` (nothing if no line is needed
  there), A `packages.ts`, M `index.ts` ×2.
- Docs — M `docs/features/spaces.md`, `packages.md`, `lookups.md`, `docs/frontend/architecture.md`,
  `docs/project/overview.md`, `docs/README.md`; M findings `67-…md`, `81-…md`; A `<n>-the-owners-checklist-cannot-name-a-retired-amenity.md`;
  M `docs/architecture/findings/README.md`.

**PR 2**
- `features/users/` — M `components/temporary-password/TemporaryPasswordDialog.tsx` (type only),
  `hooks/temporary-password/useTemporaryPasswordDialog.ts`, `useHandover.ts`, `repository/usersRepository.ts`
  (+ its unit test), `components/issue-password/IssuePasswordDialog.tsx`, their component tests; M
  `copy/*/users.ts` (design issue 15 only).
- `features/staff/` (A, whole): `index.ts`; `repository/staffRepository.ts` + test; `hooks/queryKeys.ts`;
  `hooks/list/useStaffQuery.ts`, `useStaffList.ts` (+ test); `hooks/add/useAddStaffForm.ts` (+ test),
  `useAddStaff.ts`; `hooks/access/useSetStaffActive.ts`, `useDeactivateDialog.ts` (+ test), `useStaffActions.ts`
  (+ test); `hooks/reissue/useReissue.ts`, `useReissueDialog.ts` (+ test); `services/staffBadges.ts` (+ unit
  test); `types/ShownPassword.ts`, `types/StaffRowView.ts`; `components/StaffList.tsx` (+ test),
  `components/add/AddStaff.tsx`, `components/access/DeactivateDialog.tsx`, `components/reissue/ReissueDialog.tsx`,
  `components/StaffActionsMenu.tsx`.
- `features/space-settings/` (A, whole): `index.ts`; `repository/spaceSettingsRepository.ts` + test;
  `hooks/queryKeys.ts`, `hooks/useSpaceSettingsQuery.ts`, `hooks/useSaveSettings.ts`; `hooks/card/useSettingsCard.ts`
  (the frame's state); `hooks/pricing/usePricingCard.ts` (+ test); `hooks/reception/useReceptionCard.ts` (+ test);
  `hooks/reminder/useReminderCard.ts` (+ test); `services/roundingExample.ts` (+ unit test),
  `services/reminderPreview.ts` (+ unit test); `components/SettingsCard.tsx`, `components/SpaceSettingsCards.tsx`
  (+ test), `components/pricing/PricingCard.tsx`, `components/reception/ReceptionCard.tsx`,
  `components/reminder/ReminderCard.tsx`.
- `features/occupancy/` (A): `index.ts`, `repository/occupancyRepository.ts` + test, `hooks/queryKeys.ts`,
  `hooks/useCapacityQuery.ts`, `hooks/useSetCapacity.ts`.
- `pages/dashboard/` — A `space/StaffPage.tsx`, `space/SettingsPage.tsx`, `space/settings/AttendanceCard.tsx`,
  `space/settings/useAttendanceCard.ts` (+ component test), `space/settings/attendanceSchema.ts` (+ unit test);
  M `routes.tsx`, `routes.component.test.tsx`, `admin/OwnersPage.tsx` (`handover`).
- `shared/copy/{english,arabic}/` — A `staff.ts`, `spaceSettings.ts`; M `index.ts` ×2.
- Docs — M `docs/features/space-links.md`, `space-settings.md`, `occupancy.md`, `users.md`,
  `docs/frontend/architecture.md`, `docs/project/overview.md`, `docs/README.md`; findings `90-…`, `96-…`,
  `README.md`.

**Shared with worker B's DESK** (`apps/api`, `packages/shared`, `docs`, the two errors catalogues). No code
file is shared: this item never edits `shared/copy/*/errors.ts` (finding 90 is worded in `staff`).
Likely **text conflicts** in shared documents, each side keeping to its own section (workflow §9, the fast
path): `docs/features/packages.md`, `occupancy.md`, `space-settings.md` (B: *API* parts; this item: the
header, *Who uses it*, *Web* parts, code map's Web line), `docs/project/overview.md` (*Built* lines),
`docs/architecture/findings/README.md`, `docs/README.md` (the map's lines), `docs/frontend/architecture.md`
(unlikely for B). If DESK changes `packages/shared/src/packages`, `space-settings` or `occupancy`, or the
staff routes, before this item's commit — stop and ask (§13).

## 8. Design issues (built only once the reply approves them)

PR 1
1. **The owner's state.** The design shows no state; an owner whose space the admin hid would not know why
   it is gone from the site. *Fix:* on the owner's place, a `warning` badge «مخفية عن الزوار» only while
   hidden (the verified badge is always true there, so it is left out).
2. **The dirty alert at the profile's head** (the design's «لديك تغييرات غير محفوظة في N أقسام»). *Fix:* not
   built: one editor — each section says «تغييرات غير محفوظة», and the leave guard names them, as the admin's.
3. **The amenities' link to the platform's list** is the admin's page (403 for the owner). *Fix:* none on the
   owner's place (`listLink: null`), as the design's `manage` prop does; S2's retired-amenities line instead.
4. **The packages' "chosen at the desk" lines** («أسعار الأسبوع والشهر تُختار أيضًا في المكتب…»,
   «…وتُختار في مكتب الاستقبال») describe a desk not built yet. *Fix:* dropped; the section says «لا تظهر
   للزوار.» and the sheet «باقة خاصة — لا تظهر للزوار.»; the switch is «متاحة», not «متاحة في المكتب».
5. **The sheet's shift chips** have no visible "none". *Fix:* a first chip «بدون وردية», the single choice
   always on one.
6. **The sheet's amounts** take digits only. *Fix:* the prices' rule: shekels with up to two decimals, Arabic
   digits read (`agorotOf`).
7. **A paused package that holds a shift** (finding 81) has no design. *Fix:* on its muted row, under the
   summary: «موقوفة وما زالت تحجز وردية «{shift}»؛ لا تُحذف الوردية قبل إزالتها منها.» and an outline
   small button «إزالة الوردية», acting at once (P9: reversible, no one else affected; P8: the row shows it).
8. **The prices card on its page** is the editor's section titled «الأسعار المعلنة», intro «تظهر في صفحة
   المساحة · للعرض فقط · الدفع في المساحة» (SH-021, once), its "add shifts first" line a link to
   «ساعات العمل» on the profile.

PR 2
9. **Staff columns.** «أُضيف في» has no date in `StaffMember`, «مقبوضاته هذا الشهر» and «عرض مقبوضاته»
   need payments (step 9). *Fix:* the name (email under it, left to right), the state, the actions.
10. **The add sheet's line** says an existing account is linked — false since ADR 0009's revision. *Fix:*
    «يُنشأ حساب جديد لهذا البريد برمز مرور مؤقت يظهر لك مرة واحدة — جهّز طريقة تسليمه. لا يُربط
    حساب موجود.», above the submit «إنشاء حساب الاستقبال». The design's re-add of a removed email becomes
    the row's «إعادة وصوله»; `EMAIL_HAS_ACCOUNT`'s line says so.
11. **No new temporary password in the design** (OW-019's pending case). *Fix:* the row menu's «كلمة مرور
    مؤقتة جديدة» (S10), and the pending badge's expired form «انتهت صلاحية كلمة المرور المؤقتة» (from
    `expiresAt`).
12. **P8 in the staff rows:** the design toasts the re-activation. *Fix:* no success toast for the
    deactivation or the re-activation (the row shows it); a failure's toast stays.
13. **Settings: «حسابي»** leads to `/me`, not built. *Fix:* dropped.
14. **Settings: hand-typed prices** (`receptionMayTypePrices`, #92) has no place in the design. *Fix:* a card
    «الاستقبال» with one switch «يكتب الاستقبال سعرًا يدويًا» and its helper.
15. **The forced change says «كلمة مرور مؤقتة من فريق مساحة»** — false for a receptionist the owner created.
    *Fix:* both catalogues' `users.passwordChange.description`: «هذه كلمة مرور مؤقتة. اختر كلمة مرورك
    لتتابع.» / "This is a temporary password. Choose your own password to continue." (in commit 1 of PR 2). If
    not approved: record it as finding `<n+1>` instead.
16. **Visit pricing's amounts** (the hour and day prices in the description, «= 7 ₪» in an example) need the
    space's prices on this page. *Fix:* the description links «الباقات والأسعار»; the examples say no money.
17. **The reminder** has no way back to the default. *Fix:* «استعادة النص الافتراضي» (a ghost button) puts
    the catalogue's text back and saves `null`.
18. **Attendance's helper** names the closing hour (from the hours). *Fix:* «يُسجَّل خروج من بقي عند موعد
    الإغلاق.», no hour.

## 9. What is built — interfaces, words, states

Words: Arabic first, then English. A plural line gives `arabicPlural` all six forms and `englishPlural`
`one`/`other` (`shared/copy/plural.ts`). Every line in both catalogues; the Arabic sections `satisfies`.

### PR 1 · Commit 1 — `refactor(spaces): share the shekel helpers`
- `shared/lib/money/shekels.ts`: `agorotOf(text): number | string | undefined`, `shekelsOf(agorot): string`
  (moved as they are); `shared/lib/money/priceText.ts`: `priceText(agorot, language)`; `shared/lib/index.ts`
  exports the three. Importers: `spaces/services/pricesForm.ts`, `hooks/prices/useReadOnlyPrices.ts`, and
  whatever `git grep` finds. The tests move with them, unchanged. Architecture §1's status line names
  `shared/lib` built ("the money helpers").

### PR 1 · Commit 2 — `refactor(spaces): give the editor its place`
No behaviour change for the admin; the owner's values are used from commit 5 (said in the body).
- `types/EditorPlace.ts`: `export type EditorPlace = 'admin' | 'owner'`.
- `repository/spaceEditorRepository.ts`: `SpaceEditorRepository` = today's `get`, `updateProfile`,
  `updateHours`, `updatePrices`, `updateAmenities`, `updateContacts`, `confirm`, `listPhotos`, `uploadPhoto`,
  `removePhoto`, `orderPhotos`, moved from `SpacesRepository`; `createSpaceEditorRepository(place)`, base
  `/admin/spaces/:id` or `/manage/spaces/:id`. `SpacesRepository` keeps `create`, `setHidden`, `remove`,
  `restore`.
- `hooks/editor/editorScope.ts`:
  ```ts
  type EditorScope = {
    repository: SpaceEditorRepository;
    spaceKey: (id: number) => readonly unknown[];   // admin ['admin','spaces','space',id] · owner ['space',id,'spaces','space']
    photosKey: (id: number) => readonly unknown[];  // admin ['admin','spaces','photos',id] · owner ['space',id,'spaces','photos']
    writeKey: (id: number) => readonly unknown[];   // admin ['admin','spaces','write',id] · owner ['space',id,'spaces','write']
    answered: readonly unknown[];                   // marked out of date after a write: admin ['admin'] · owner ['me'] (S7)
    lists: readonly unknown[];                      // the lookups' lists: admin ['admin'] · owner ['public']
  };
  export const EDITOR_SCOPES: Record<EditorPlace, EditorScope>;  // made once, at module level
  ```
  `queryKeys.ts`/`mutationKeys.ts` keep the admin's `hold` and action keys and lose `space`/`photos`/
  `spaceWriteKey` to the scope; `useRefreshAdmin`'s `isSpaceKey` reads `EDITOR_SCOPES.admin.spaceKey`.
- `useSpaceAnswer(place, spaceId)`: `keep` marks `scope.answered` — the admin's with `refetchType: 'none'`
  as today, the owner's fetched now (`['me']`, S7) — then sets `scope.spaceKey`.
- `hooks/editor/meanwhileLines.ts`: `meanwhileLines(place, copy) → { forbidden, not_found }` (S6); the admin's
  are today's lines, so nothing changes here; the owner's lines are added in commit 5.
- `services/mayEdit.ts`: `mayEdit(place, isVerified) = place === 'admin' ? !isVerified : isVerified`.
- Signatures: `useSpaceQuery(place, id)`, `useSaveGroup(place, id, group, send)`, `useConfirmGroup(place, id,
  group)`, `useSpaceEditor(place, id)`, `useSectionFrame({ place, … })`, every `use*Section({ place, … })`,
  `usePhotosQuery(place, id)`, `usePhotoGallery(place, id, onUploadingChange)`, `usePhotoOrder`/`usePhotoRemove`/
  `usePhotoUploads(place, id, …)`, `staleGallery(client, place, id, refusal)`, `useReadOnlyPhotos(place, id)`,
  `useSpaceName(id)` (admin's, unchanged signature, reads the admin scope). `useAmenitiesSection`'s retired
  refusal invalidates `scope.lists`; every `spacesKeys.space(…)` in the sections reads `scope.spaceKey`.
- Components: `SpaceEditor`'s props become §4.2's (`place: AdminPlace | OwnerPlace`), `SpaceEditPage` passes
  `{ kind: 'admin', ownerActions, amenitiesListLink, areaName, amenityNames }`; the sections take `place`.
- Docs: `spaces.md` *Web decisions*: «**The editor takes a place, `admin` or `owner`, which picks its
  calls, its keys and what a write refreshes; one scope table holds them** (O1). *Why:* one editor, two
  permissions; the owner's calls are the managed routes. {date}, #PRNUM.»; code map: `repository/` two
  repositories, `hooks/editor/` the scope.

### PR 1 · Commit 3 — `fix(spaces): start the prices table at 1024 px`
`PricesSection`: every `md:` that lays the table out (the header row, the grid's columns, `RowLabel`'s
`md:sr-only`) becomes `lg:`; below 1024 px each price is a card. `spaces.md` *Behaviour* («from 768 px a
small table» → «from 1024 px»), a *Web decisions* line («**The prices table starts at 1024 px**… *Why:*
foundation §9; the shift's select was cut at 768 (finding 67). {date}, #PRNUM.»); finding 67 → Resolved,
with its resolution line, and moved in the index.

### PR 1 · Commit 4 — `feat(lookups): offer the public lists to owners`
- `types/LookupsSource.ts`: `export type LookupsSource = 'admin' | 'public'` (exported from `index.ts`).
- `AreaSelect({ source, … })`, `useAreaOptions({ source, value, onValueChange })`: `public` never enables
  `useGovernoratesQuery`; an area not offered gives `kept = { value, label: copy.lookups.areaSelect.unavailable }`.
  `admin` as today.
- `AmenityChecklist({ source, … })`, `useAmenityChecklist({ source, … })`: `public` reads
  `useCatalogueQuery().data.amenities` (active only, every one `inactive: false`); the linked ids absent from
  it stay in the value (never toggled); `retiredKept: string | null`, the plural line of their count, shown
  under the list.
- Callers: `AddSpacePage` and `SpaceEditPage` pass `source="admin"`.
- Words (`lookups`):

| key | ar | en |
|---|---|---|
| `areaSelect.unavailable` | المنطقة الحالية — لم تعد متاحة للاختيار | Current area — no longer offered |
| `amenityChecklist.retiredKept(n)` | zero/other «يبقى {n} مرفق لم تعد في قائمة المنصة مرتبطة بالمساحة.» · one «يبقى مرفق واحد لم يعد في قائمة المنصة مرتبطًا بالمساحة.» · two «يبقى مرفقان لم يعودا في قائمة المنصة مرتبطين بالمساحة.» · few «تبقى {n} مرافق لم تعد في قائمة المنصة مرتبطة بالمساحة.» · many «يبقى {n} مرفقًا لم تعد في قائمة المنصة مرتبطة بالمساحة.» | one «One amenity no longer on the platform’s list stays linked to the space.» · other «{n} amenities no longer on the platform’s list stay linked to the space.» |

- Docs: `lookups.md` *Behaviour* and *Web decisions* («**The area and amenity fields read the admin's lists
  or the public catalogue, as the page says (`source`)** … *Why:* an owner is refused the admin's lists;
  the space's own fields must still save. {date}, #PRNUM.»); finding `<n>` (Open) and its index line.

### PR 1 · Commit 5 — `feat(spaces): add the owner's space profile`
- `useSpaceEditor('owner', id)` returns, besides today's: `readOnly: !mayEdit(place, space.isVerified)`;
  `head` for the owner — `{ intro, publicLink: { label, href } }` — and `notice` for the admin (today's); the
  owner's `badges`: only «مخفية عن الزوار» when hidden (design issue 1); `privacy` only for the admin;
  `pricesLink` for the owner from `usePricesLink(space, place)`: `{ title, description, date, stale, missing,
  action: { label, href } }`.
- `SpaceEditor` draws, on the owner's place: `OwnerHead` (the intro, then the link, `target="_blank"`
  `rel="noopener"`, as the shell's `PublicPageLink`); the checklist; the sections, with `PricesLinkCard`
  (`id="prices"`, a `Card` whose header is the title as `h2`, the description «تُعدَّل وتُؤكَّد في الباقات
  والأسعار ·» and the date or «لم تُضف بعد», «قديمة» as a `warning` badge, and `CardAction` an outline small
  link-button with `ArrowEndIcon`) in place of `PricesSection`; `AmenitiesSection listLink={null}`; the gallery.
- `meanwhileLines('owner')` gives S6's lines; the gallery's `verifiedMeanwhile`/`deletedMeanwhile` use them too.
- `pages/dashboard/navigation.ts`: `spacePagePath(spaceId, name: DashboardPageName): string`, from `SPACE_NAV`'s
  segment below `spaceOverviewPath(spaceId)`.
- `pages/dashboard/space/ProfilePage.tsx`: `parseSpaceId(useParams().spaceId)` (the guard has checked it),
  `<PageHeader />`, `<SpaceEditor key={spaceId} spaceId place={{ kind: 'owner', pricesLink:
  spacePagePath(spaceId, 'packages') }} areaField={publicAreaField} amenitiesField={publicAmenitiesField}
  publicLink={publicSpacePath} />`, the fields made once at module level with `source="public"`.
- `routes.tsx`: `SPACE_PAGES: Partial<Record<DashboardPageName, () => Promise<ReactElement>>>`, each lazily
  imported; the space branch's map uses it inside `RequireSpaceRole roles={roles}`, else `PlaceholderPage`.
- Words (`spaces.editor.owner`):

| key | ar | en |
|---|---|---|
| `intro` | كل قسم يُحفظ وحده، ويظهر للزوار فور حفظه. | Each section saves on its own and shows to visitors as soon as it’s saved. |
| `viewPublic` | عرض الصفحة العامة | View public page |
| `hidden` | مخفية عن الزوار | Hidden from visitors |
| `pricesLink.description` | تُعدَّل وتُؤكَّد في الباقات والأسعار | Edited and confirmed in Packages & prices |
| `pricesLink.action` | الباقات والأسعار | Packages & prices |
| `meanwhile.forbidden` | انتهى ربطك بهذه المساحة في الأثناء؛ لم يُحفظ شيء. | Your link to this space ended meanwhile; nothing was saved. |
| `meanwhile.notFound` | لم تعد هذه المساحة متاحة لك. | This space is no longer available to you. |

- Docs: `spaces.md` — header (the owner's screen built), *What it does*, *Who uses it* (the owner, on the
  dashboard), *Behaviour* «**The owner's space profile on the web**» (the head line, the prices row, the
  public lookups, no notice, the refusal lines), *Web decisions* (O1's place; S6; S7; design issues 1–3 with
  their reasons; each line ending «{date}, #PRNUM.»), code map, *Web history*; `architecture.md` *Built so
  far* (`space/` pages: the profile); `overview.md` *Built* (the spaces line: the owner's profile on the
  dashboard); `docs/README.md` (spaces' map line drops "(API only)" if it says so).

### PR 1 · Commit 6 — `feat(spaces): edit prices on packages & prices`
- `SpacePricesEditor({ spaceId, hoursLink })` (exported): `useSpacePricesEditor('owner', spaceId)` — the
  space's query, its loading (`EditorLoading`), failure (`EditorFailure`, with «إعادة المحاولة»), 404
  (`NotFoundState`); `PricesSection place="owner" hoursUnsaved={false}`; its own `useLeaveGuard([prices],
  saving, false)` and `LeaveDialog`.
- `PricesSection` on the owner's place: the title `prices.publishedTitle`, the intro `prices.publishedIntro`;
  `notes` become `{ text: string; link: { label: string; href: string } | null }[]`, the no-shift note's link
  `hoursLink` when given (the admin's editor gives none: its hours are on the page).
- `useSpaceShifts(place, spaceId): Shift[] | null` (exported, `null` while the space loads or failed).
- `pages/dashboard/space/PackagesPage.tsx`: `<PageHeader />`, `<SpacePricesEditor spaceId hoursLink={`${spacePagePath(spaceId,'profile')}#hours`} />`.
- Words (`spaces.editor.prices`): `publishedTitle` «الأسعار المعلنة» / "Published prices";
  `publishedIntro` «تظهر في صفحة المساحة · للعرض فقط · الدفع في المساحة» / "Shown on the space’s page ·
  display only · paid at the space"; `noShiftsLink` «أضف ورديات في ساعات العمل» / "Add shifts in the opening
  hours".
- Docs: `spaces.md` *Behaviour* (the prices on their own page), *Web decisions* (O6; design issue 8).

### PR 1 · Commit 7 — `feat(packages): keep a space's private packages`
- **Repository** `PackagesRepository`: `list(spaceId): Promise<SpacePackage[]>` (GET), `create(spaceId, request:
  CreatePackageRequest): Promise<SpacePackage>` (POST), `update(spaceId, packageId, request:
  UpdatePackageRequest): Promise<SpacePackage>` (PATCH), at `/manage/spaces/:spaceId/packages`.
- **Keys** `packagesKeys.list(spaceId) = ['space', spaceId, 'packages']`.
- **Exports** `PackagesSection({ spaceId, shifts: ShiftChoice[] | null, hoursLink })`; `type ShiftChoice =
  { id: number; nameAr: string; nameEn: string | null }`.
- **`usePackagesSection`**: the list's states (skeleton rows; a failure with its reference and «إعادة
  المحاولة»; empty `EmptyState` with «باقة جديدة»); `rows: PackageRowView[]` —
  `{ key, name, summary, price, paused: string | null, available: { label, checked, pending, toggle },
  edit: { label, run }, heldShift: { text, clear: { label, pending, run } } | null }`; `add: { label, run }`;
  the sheet's view. The switch: `useSetPackageActive` → `PATCH {isActive}`, `aria-disabled` while pending,
  the list replaced from the answer (`setQueryData`), a failure a toast that stays, «تعذّر تغيير إتاحة
  {name}» with `RefusalText`. `heldShift` only for a paused package with a shift; «إزالة الوردية» →
  `useClearPackageShift` → `PATCH {shiftId: null}`, the same answer handling.
- **`services/packageSummary.ts`**: `summaryOf(pkg, shifts, words, language): string` — the parts joined by
  « · »: validity, each set limit, «للطلاب» for `STUDENT`, the shift's name (`nameEn ?? nameAr` in English);
  `priceLineOf(pkg, words, language)` — `FIXED` the amount, `PER_HOUR`/`PER_DAY` the rate's line, by `priceText`.
- **`services/packageValues.ts`**: `PackageValues = { name, validityDays, limits: LimitName[], totalDays,
  daysPerWeek, hoursPerDay, totalHours, billing, amount, audience, shiftId: string }` (texts as typed);
  `valuesOf(pkg | null)` (a new one: validity «30», billing `FIXED`, audience `GENERAL`, no limit, no shift);
  `prepare(values)` — digits read Arabic-Indic too, a limit off `null`, a limit on and empty `''` (check §13.5),
  `agorotOf(amount)`, `shiftId` `''` → `null`.
- **`usePackageSheet`**: `open(pkg | null)`, `close`; `useServerForm` with `createPackageSchema` (new) or
  `updatePackageSchema` (edit, the terms whole, S11); `fields` in display order; `fieldLines` below;
  `failureLines` `{ forbidden, not_found }`; the limits' `ToggleGroup type="multiple"` (turning one off clears
  its field); the billing's `ToggleGroup type="single"` and the amount's label by billing; the audience; the
  shift chips (design issue 5) or, with no shift, the line and its link `hoursLink`, or, while `shifts` is
  `null`, «جارٍ تحميل الورديات…»; the summary box (`aria-live="polite"`). Saved: the list fetched again and
  waited for (the mutation's `onSuccess` returns the invalidation), the sheet closes, toast «حُفظت الباقة
  {name}» (the name isolated). A 422 on `shiftId` invalidates the whole `['space', spaceId]` (the space's
  shifts are `spaces`', architecture §7). A 409 lands `not_unique` on the name.
- **Components**: `PackagesSection` (an `h2` «الباقات الخاصة», its line, «باقة جديدة» at the row's end, then
  a `Card` with a `ul` of `PackageRow`: name and «موقوفة» `neutral` badge, the summary, the price, the
  `Switch` in a horizontal `Field` «متاحة» (accessible name «{name}: متاحة»), «تعديل» outline small
  (accessible «تعديل {name}»); a paused row `bg-muted`); `PackageSheet` (`Sheet side="end"`, `SheetBody`
  `min-w-0`, the footer's full-width submit «حفظ الباقة»); `LimitsField`.
- **`PackagesPage`** adds `<PackagesSection spaceId shifts={useSpaceShifts('owner', spaceId)} hoursLink={…#hours} />`
  under the prices.
- Words (`packages`, new section):

| key | ar | en |
|---|---|---|
| `title` | الباقات الخاصة | Private packages |
| `description` | لا تظهر للزوار. | Never shown to visitors. |
| `add` | باقة جديدة | New package |
| `loadFailed` | تعذّر تحميل الباقات | We couldn’t load the packages |
| `empty.title` / `empty.text` | لا توجد باقات خاصة / أنشئ باقة مثل «10 أيام» أو «20 ساعة». | No private packages / Create a package such as “10 days” or “20 hours”. |
| `paused` | موقوفة | Paused |
| `available` / `availableNamed({name})` | متاحة / {name}: متاحة | Available / {name}: available |
| `edit` / `editNamed({name})` | تعديل / تعديل {name} | Edit / Edit {name} |
| `toggleFailed({name})` | تعذّر تغيير إتاحة {name} | Couldn’t change whether {name} is offered |
| `heldShift({shift})` | موقوفة وما زالت تحجز وردية «{shift}»؛ لا تُحذف الوردية قبل إزالتها منها. | Paused, but still holds the shift “{shift}”; the shift can’t be removed until it’s cleared here. |
| `clearShift` / `clearShiftFailed({name})` | إزالة الوردية / تعذّرت إزالة وردية {name} | Clear the shift / Couldn’t clear {name}’s shift |
| `summary.validity(n)` | one «صالحة يومًا واحدًا» · two «صالحة يومين» · few «صالحة {n} أيام» · many «صالحة {n} يومًا» · zero/other «صالحة {n} يوم» | one «valid 1 day» · other «valid {n} days» |
| `summary.totalDays(n)` | one «يوم واحد» · two «يومان» · few «{n} أيام» · many «{n} يومًا» · zero/other «{n} يوم» | «1 day» / «{n} days» |
| `summary.daysPerWeek(n)` | one «يوم واحد بالأسبوع» · two «يومان بالأسبوع» · few «{n} أيام بالأسبوع» · many/zero/other «{n} يوم بالأسبوع» | «1 day a week» / «{n} days a week» |
| `summary.hoursPerDay(n)` | one «ساعة واحدة باليوم» · two «ساعتان باليوم» · few «{n} ساعات باليوم» · many «{n} ساعة باليوم» · zero/other «{n} ساعة باليوم» | «1 hour a day» / «{n} hours a day» |
| `summary.totalHours(n)` | one «رصيد ساعة واحدة» · two «رصيد ساعتين» · few «رصيد {n} ساعات» · many «رصيد {n} ساعة» · zero/other «رصيد {n} ساعة» | «1-hour balance» / «{n}-hour balance» |
| `summary.students` / `summary.separator` | للطلاب / « · » | students / « · » |
| `price.perHour({price})` / `price.perDay({price})` | {price} للساعة / {price} لليوم | {price} an hour / {price} a day |
| `sheet.newTitle` / `sheet.editTitle` / `sheet.description` | باقة جديدة / تعديل الباقة / باقة خاصة — لا تظهر للزوار. | New package / Edit package / Private — never shown to visitors. |
| `sheet.close` | إغلاق | Close |
| `sheet.name` / `sheet.validity` / `sheet.validityHelp` | اسم الباقة / الصلاحية (أيام) / ينتهي الاشتراك بعد هذه المدة من بدايته. | Package name / Validity (days) / A subscription ends this long after it starts. |
| `sheet.limits` / `sheet.limitsHelp` / `sheet.optional` | الحدود / اختر ما ينطبق؛ يظهر لكل حد حقله. / اختياري | Limits / Choose what applies; each limit shows its field. / Optional |
| `sheet.limitNames` | totalDays «عدد الأيام» · daysPerWeek «أيام بالأسبوع» · hoursPerDay «ساعات باليوم» · totalHours «مجموع الساعات» | Number of days · Days a week · Hours a day · Total hours |
| `sheet.billing` / `sheet.billings` | طريقة الحساب / FIXED «سعر ثابت» · PER_HOUR «بالساعة» · PER_DAY «باليوم» | Billing / Fixed price · Per hour · Per day |
| `sheet.amount` | FIXED «السعر الكلي (₪)» · PER_HOUR «سعر الساعة (₪)» · PER_DAY «سعر اليوم (₪)» | Total price (₪) · Price per hour (₪) · Price per day (₪) |
| `sheet.audience` / `sheet.audiences` | لمن / GENERAL «الجميع» · STUDENT «الطلاب» | For / Everyone · Students |
| `sheet.shift` / `sheet.noShift` / `sheet.noShifts` / `sheet.addShifts` / `sheet.shiftsLoading` | الوردية / بدون وردية / لا ورديات محفوظة بعد. / أضف ورديات في ساعات العمل / جارٍ تحميل الورديات… | Shift / No shift / No shifts are saved yet. / Add shifts in the opening hours / Loading the shifts… |
| `sheet.summary` / `sheet.unnamed` / `sheet.noPrice` | الملخّص / باقة بدون اسم / بدون سعر بعد | Summary / Unnamed package / No price yet |
| `sheet.submit` / `sheet.failed` / `saved({name})` | حفظ الباقة / تعذّر حفظ الباقة / حُفظت الباقة {name} | Save package / Couldn’t save the package / Package {name} saved |
| `fieldErrors.name` | required «أدخل اسم الباقة» · not_unique «اسم مستخدم لباقة أخرى، موقوفة أو متاحة» · too_long «الاسم أطول من 60 حرفًا» · invalid_format «احذف الرموز غير المسموحة من الاسم» | Enter the package name · Another package, paused or not, has this name · The name is longer than 60 characters · Remove the characters that aren’t allowed |
| `fieldErrors.count` (validity, totalDays, totalHours) | required «أدخل العدد» · out_of_range / invalid_format «عدد صحيح من 1 فأكثر» | Enter the number · A whole number from 1 |
| `fieldErrors.limitEmpty` | أدخل العدد أو أطفئ هذا الحد | Enter the number, or turn this limit off |
| `fieldErrors.daysPerWeek` / `hoursPerDay` | out_of_range «من 1 إلى 7» / «من 1 إلى 24» | From 1 to 7 / From 1 to 24 |
| `fieldErrors.amount` | required «أدخل السعر» · out_of_range «أدخل مبلغًا أكبر من صفر، حتى 100,000 ₪» · invalid_format «أدخل مبلغًا بالشيكل، حتى منزلتين عشريتين» | Enter the price · Enter an amount above zero, up to ₪100,000 · Enter an amount in shekels, up to two decimals |
| `fieldErrors.shift` | invalid_choice «لم تعد هذه الوردية موجودة؛ اختر غيرها.» | This shift no longer exists; choose another. |
| `refusals` | forbidden «انتهى ربطك بهذه المساحة؛ لم يُحفظ شيء.» · not_found «لم تعد هذه الباقة موجودة.» | Your link to this space ended; nothing was saved. · This package no longer exists. |

- Docs: `packages.md` — header (the web feature built; scope adds `features/packages`, dashboard-only),
  *What it does*, *Who uses it* (the owner, on the dashboard), *How it composes* (the page sets the space's
  shifts from `spaces`; the 422 refreshes the space's scope), *Behaviour* «**The owner's packages on the web**»,
  *Web decisions* (O8; S11; design issues 4–7; finding 81's way out; each with «{date}, #PRNUM.»), code map
  *Web*, *Web history*; finding 81 → Resolved; `architecture.md` *Built so far* (the packages page);
  `overview.md` *Built* (the packages line); `docs/README.md` (packages' line).

### PR 2 · Commit 1 — `feat(users): record a handover at a space`
- `TemporaryPasswordDialogInput.handover: { at: 'admin' } | { at: 'space'; spaceId: number }` (required);
  `useHandover()` takes `{ userId, channel, at }`; `UsersRepository.handOverAtSpace(spaceId, userId, request)`
  → `POST /manage/spaces/:spaceId/staff/:userId/temporary-password/handover`. `OwnersPage` and
  `IssuePasswordDialog` pass `{ at: 'admin' }`. A `not_found` or `TEMPORARY_PASSWORD_NOT_PENDING` closes
  with «لم تُسجَّل طريقة التسليم», as today, for both.
- Design issue 15 (if approved): `users.passwordChange.description` in both catalogues.
- Docs: `users.md` *Behaviour* (the one-time password, the handover's place), *Web decisions* (S4: «{date},
  #PRNUM.»), *Web history*.

### PR 2 · Commit 2 — `feat(staff): add the owner's staff page`
- **Repository** `StaffRepository`: `list(spaceId): Promise<StaffMember[]>`, `add(spaceId, AddStaffRequest):
  Promise<AddedStaff>`, `setActive(spaceId, userId, SetStaffActiveRequest): Promise<StaffMember>`,
  `reissue(spaceId, userId): Promise<IssuedTemporaryPassword>` (used in commit 3).
- **Keys** `staffKeys.list(spaceId) = ['space', spaceId, 'staff']`.
- **Exports** `StaffList({ spaceId, temporaryPassword: (shown: ShownPassword, done: () => void) => ReactNode })`,
  `type ShownPassword = { userId: number; name: string; email: string; password: string }`.
- **`useStaffList`**: rows `{ key, name, email, badges: { label, variant }[], actions }`; the count line
  (plural); states as the users list's (skeleton rows, failure with reference and «إعادة المحاولة», empty).
  `services/staffBadges.ts`: `badgesOf(member, now)`: active `success` «نشط» / inactive `neutral` «بلا
  وصول»; while active with `temporaryPassword`: `warning` «لم يغيّر كلمة المرور المؤقتة بعد», or, past
  `expiresAt`, `warning` «انتهت صلاحية كلمة المرور المؤقتة» (now from `shared/forms`' `clock`).
- **`StaffList`**: `DataTable` (three columns, cards below `md`; the toolbar: the count at the start,
  «إضافة موظف» at the end), `renderCard` with the same facts; the empty state carries «إضافة موظف».
- **`useAddStaffForm`** (`useServerForm`, `addStaffSchema`): the sheet's open state; the notice (design issue
  10) above the submit; on 201, the list invalidated and waited for, the sheet closed and reset, the mutation
  reset (no password in the cache, `gcTime: 0`), and `ShownPassword` handed to the page's slot; on
  `EMAIL_HAS_ACCOUNT` the field line `not_unique` below; `failureLines` `{ forbidden }`; a 429 counts down.
- **`StaffPage`**: `<PageHeader />`, the role line, `<StaffList spaceId temporaryPassword={(shown, done) =>
  <TemporaryPasswordDialog kind="created" person={…} password={shown.password} handover={{ at: 'space',
  spaceId }} onDone={done} />} />`.
- Words (`staff`, new section):

| key | ar | en |
|---|---|---|
| `intro` | يصل موظف الاستقبال إلى المكتب والزبائن والإعلانات ودفعاته اليوم، ولا يرى المالية ولا الإعدادات. | A receptionist reaches the desk, the customers, the announcements and their own payments today — never the finance or the settings. |
| `label` / `count(n)` | الموظفون / zero «لا موظفون» · one «موظف واحد» · two «موظفان» · few «{n} موظفين» · many «{n} موظفًا» · other «{n} موظف» | Staff / one «1 staff member» · other «{n} staff members» |
| `columns` | name «الاسم» · status «الحالة» · actions «إجراءات» | Name · Status · Actions |
| `badges` | active «نشط» · inactive «بلا وصول» · pending «لم يغيّر كلمة المرور المؤقتة بعد» · expired «انتهت صلاحية كلمة المرور المؤقتة» | Active · No access · Hasn’t changed the temporary password yet · The temporary password has expired |
| `loadFailed` | تعذّر تحميل الموظفين | We couldn’t load the staff |
| `empty.title` / `empty.text` | لا يوجد موظفون / يمكنك إدارة المكتب بنفسك أو إضافة موظف استقبال. | No staff yet / You can run the desk yourself, or add a receptionist. |
| `add.open` / `add.title` / `add.description` | إضافة موظف / إضافة موظف / الدور: الاستقبال | Add staff member / Add staff member / Role: Reception |
| `add.name` / `add.email` | الاسم / البريد الإلكتروني | Name / Email |
| `add.notice` | design issue 10's line | A new account is created for this email, with a temporary password shown to you once — have a way to hand it over ready. An existing account is never linked. |
| `add.submit` / `add.failed` / `add.close` | إنشاء حساب الاستقبال / تعذّر إضافة الموظف / إغلاق | Create the reception account / Couldn’t add the staff member / Close |
| `add.fieldErrors` | name required «أدخل الاسم» · too_long «الاسم أطول من المسموح» · email required «أدخل البريد الإلكتروني» · invalid_format «أدخل بريدًا صحيحًا، مثل name@example.com» · email not_unique «لهذا البريد حساب في مساحة، ولا يُربط حساب موجود. استخدم بريدًا آخر؛ وإن كان موظفًا سابقًا هنا فأعد وصوله من قائمته.» | Enter the name · The name is too long · Enter the email · Enter a valid email, e.g. name@example.com · This email already has a Masaha account, and an existing account is never linked. Use another email; if they worked here before, give their access back from their row. |
| `add.refusals` | forbidden «انتهى ربطك بهذه المساحة؛ لم يُضف أحد.» | Your link to this space ended; no one was added. |

- Docs: `space-links.md` — header's *Authority* names the owner's staff screen; *What it does* (on the
  dashboard); a *Behaviour* paragraph «**The owner's staff on the web** (`features/staff`)»; *Web decisions*
  (S5's placement — the feature over this module, documented here; design issues 9, 10; finding 90's
  wording, each «{date}, #PRNUM.»); code map *Web* (`features/staff`); *Web history*; finding 90 → Resolved
  (its line names the staff copy); `architecture.md` *Built so far* (the staff page); `overview.md` *Built*
  (space links' line: the owner's staff on the dashboard).

### PR 2 · Commit 3 — `feat(staff): deactivate, reactivate and reissue`
- **`useStaffActions(spaceId, member)`** → the row menu «إجراءات: {name}»: active — «إيقاف وصوله» (opens
  the deactivation), «كلمة مرور مؤقتة جديدة» (offered while `temporaryPassword` is set; else held,
  `aria-disabled`, its reason under it, S10); inactive — «إعادة وصوله» (at once), «كلمة مرور مؤقتة
  جديدة» held «أعد وصوله أولًا». While any action of the row waits, the menu button is marked busy
  (`aria-disabled`, kept in the focus order).
- **Deactivation** `useDeactivateDialog`: `AlertDialog`, opens on «رجوع», the action a destructive `Button`
  (not `AlertDialogAction`) that stays until the answer; refused → its line inside, the dialog open; done →
  the answer replaces the row (`setQueryData`), the dialog closes, the focus back to the row's menu button;
  no success toast (design issue 12).
- **Re-activation** `useSetStaffActive` at once; the answer replaces the row; refused → a toast that stays,
  «تعذّر إعادة وصول {name}», `RefusalText` under it.
- **Re-issue** `useReissueDialog`: `AlertDialog` as the deactivation's; issued → the dialog closes and
  `ShownPassword` goes to the page's slot (the issue's mutation `gcTime: 0`, reset once handed on); refused
  → inside; `TEMPORARY_PASSWORD_NOT_PENDING` and 404 also fetch the list again.
- Words (`staff`):

| key | ar | en |
|---|---|---|
| `menu({name})` | إجراءات: {name} | Actions: {name} |
| `deactivate.item` / `.title({name})` / `.description` | إيقاف وصوله / إيقاف وصول {name}؟ / تنتهي كل جلساته على كل الأجهزة فورًا، ولا يصل إلى هذه المساحة حتى تعيد وصوله. يبقى اسمه على الدفعات وفي السجل. | Remove access / Remove {name}’s access? / Every session of theirs ends on every device now, and they can’t reach this space until you give their access back. Their name stays on the payments and in the log. |
| `deactivate.cancel` / `.confirm` / `.failed` | رجوع / إيقاف الوصول / تعذّر إيقاف الوصول | Back / Remove access / Couldn’t remove the access |
| `reactivate.item` / `.failed({name})` | إعادة وصوله / تعذّر إعادة وصول {name} | Give access back / Couldn’t give {name} their access back |
| `reissue.item` / `.title({name})` / `.description` | كلمة مرور مؤقتة جديدة / كلمة مرور مؤقتة جديدة لـ {name}؟ / تحلّ محلّ كلمة المرور المؤقتة السابقة وتنتهي جلساته، ويُطلب منه تغييرها عند أول دخول. | New temporary password / A new temporary password for {name}? / It replaces the previous temporary password and ends their sessions; they’ll be asked to change it at their first sign-in. |
| `reissue.cancel` / `.confirm` / `.failed` | رجوع / إصدار / تعذّر إصدار كلمة مرور مؤقتة | Back / Issue / Couldn’t issue a temporary password |
| `reissue.heldSettled` / `.heldInactive` | غيّر كلمة المرور المؤقتة؛ إن نسي كلمة مروره يستعيدها بالبريد. / أعد وصوله أولًا. | They’ve changed the temporary password; if they forget their password, they recover it by email. / Give their access back first. |
| `refusals` | ACCOUNT_SUSPENDED «حسابه موقوف من فريق مساحة؛ لا يعود وصوله حتى يُسترجع حسابه.» · ACCOUNT_IS_ADMIN «صار هذا الحساب حساب أدمن، ولا يعمل في الاستقبال.» · ACCOUNT_HAS_LINKS «صار لهذا الحساب مساحة أخرى؛ يستعيد كلمة مروره من فريق مساحة.» · TEMPORARY_PASSWORD_NOT_PENDING «غيّر كلمة المرور المؤقتة بالفعل؛ لا حاجة لأخرى.» · not_found «لم يعد هذا الشخص من موظفي هذه المساحة.» · forbidden «انتهى ربطك بهذه المساحة.» | Their account is suspended by the Masaha team; their access comes back once it’s restored. · This account is now an admin’s and doesn’t work at reception. · This account now has another space; they recover their password from the Masaha team. · They’ve already changed the temporary password; no new one is needed. · This person is no longer on this space’s staff. · Your link to this space ended. |

- Docs: `space-links.md` *Behaviour* (the staff's actions), *Web decisions* (S10; P8 here; the dialogs that stay
  until the answer), *Web history* line extended.

### PR 2 · Commit 4 — `feat(space-settings): add the owner's settings`
- **Repository** `SpaceSettingsRepository`: `get(spaceId): Promise<SpaceSettings>`, `update(spaceId,
  UpdateSpaceSettingsRequest): Promise<SpaceSettings>` at `/manage/spaces/:spaceId/settings`.
- **Keys** `spaceSettingsKeys.settings(spaceId) = ['space', spaceId, 'space-settings']`.
- **Exports** `SpaceSettingsCards({ spaceId, pricesLink, spaceName })`, `SettingsCard` (the frame:
  `{ id, title, description?, unsaved, failure, save: { label, pending, blocked, submit }, discard, note,
  children }`), `useSpaceSettingsQuery(spaceId)`, `useSaveSettings(spaceId)` (its `onSuccess` sets the
  answer as the query's data and toasts «حُفظت إعدادات «{card}»»).
- **`useSettingsCard`**: the frame's state from a `useServerForm` — «تغييرات غير محفوظة» while dirty,
  «تجاهل التغييرات», a save that changed nothing sends nothing and says «لم يتغيّر شيء», the answer
  resets the form.
- **`usePricingCard`**: the rounding `RadioGroup` (the minutes `Input` enabled only on `UP_AFTER_MINUTES`,
  its unit word plural by N); `prepare` sends `visitRounding` and `visitRoundingMinutes` together whenever
  either changed (the minutes `null` for the two other rules); the example from `roundingExample(n, words)`
  (`n` 1–59: «{ساعتان و(n−1)} = ساعتان · {ساعتان و(n+1)} = 3 ساعات», `n = 1` giving «ساعتان» alone on the
  left); the cap and student switches.
- **`useReceptionCard`**: `receptionMayTypePrices` (design issue 14).
- The cards' loading (a `Skeleton` card each) and failure (one `Alert` with «إعادة المحاولة») are
  `SpaceSettingsCards`' own (architecture › A section owns its own states).
- **`SettingsPage`**: `<PageHeader />`, a `max-w-3xl` column: `<SpaceSettingsCards spaceId pricesLink={spacePagePath(spaceId,'packages')} spaceName={…} />` (`spaceName` from `space-links`' `useMySpacesQuery`, the
  Arabic name when there is one, else the English; commit 6 uses it).
- Words (`spaceSettings`, new section):

| key | ar | en |
|---|---|---|
| `loadFailed` | تعذّر تحميل الإعدادات | We couldn’t load the settings |
| `card.save` / `card.discard` / `card.unsaved` / `card.unchanged` | حفظ / تجاهل التغييرات / تغييرات غير محفوظة / لم يتغيّر شيء | Save / Discard changes / Unsaved changes / Nothing changed |
| `card.saved({card})` / `card.failed({card})` | حُفظت إعدادات «{card}» / تعذّر حفظ «{card}» | “{card}” saved / Couldn’t save “{card}” |
| `pricing.title` / `pricing.description` / `pricing.pricesLink` | تسعير الزيارات / كيف يُحسب سعر الزيارة من أسعار الساعة واليوم. / الباقات والأسعار | Visit pricing / How a visit’s price is worked out from the hour and day prices. / Packages & prices |
| `pricing.rounding` | التقريب | Rounding |
| `pricing.upAfter` / `pricing.minutesLabel` / `pricing.minutesUnit(n)` | تقريب لأعلى بعد / دقائق التقريب / one «دقيقة» · two «دقيقتين» · few «دقائق» · many/zero/other «دقيقة» | Round up after / Rounding minutes / one «minute» · other «minutes» |
| `pricing.twoHours` / `pricing.twoHoursAnd(n)` | ساعتان / one «ساعتان ودقيقة» · two «ساعتان ودقيقتان» · few «ساعتان و{n} دقائق» · many/zero/other «ساعتان و{n} دقيقة» | 2 h / «2 h {n} min» |
| `pricing.example({under, over})` | {under} = ساعتان · {over} = 3 ساعات | {under} = 2 h · {over} = 3 h |
| `pricing.half` / `pricing.halfHint` | لأقرب نصف ساعة / ساعتان و20 دقيقة = ساعتان ونصف | To the nearest half hour / 2 h 20 min = 2.5 h |
| `pricing.minute` / `pricing.minuteHint` | بالدقيقة / ساعتان و20 دقيقة تُحسب كما هي | By the minute / 2 h 20 min is charged as it is |
| `pricing.cap` / `pricing.students` | لا يتجاوز سعر اليوم / استخدام أسعار الطلاب للزيارات عند توفرها | Never more than the day price / Use student prices for visits when available |
| `pricing.fieldErrors.minutes` | required «أدخل عدد الدقائق» · out_of_range / invalid_format «من 1 إلى 59 دقيقة» | Enter the minutes · From 1 to 59 minutes |
| `reception.title` / `.switch` / `.help` | الاستقبال / يكتب الاستقبال سعرًا يدويًا / لاشتراك مخصّص أو زيارة بلا سعر، مع سبب يُسجَّل. أنت تكتب السعر دائمًا. | Reception / Reception may type a price by hand / For a custom subscription, or a visit with no price, with a reason recorded. You can always type one yourself. |
| `refusals` | forbidden «انتهى ربطك بهذه المساحة؛ لم يُحفظ شيء.» | Your link to this space ended; nothing was saved. |

- Docs: `space-settings.md` — header (the web feature built; scope adds `features/space-settings`), *What it
  does*, *Who uses it* (the owner, on the dashboard), *Behaviour* «**The owner's settings on the web**»,
  *Web decisions* (design issues 13, 14, 16; the rounding pair always sent together; each «{date},
  #PRNUM.»), code map *Web*, *Web history*; `architecture.md`, `overview.md`, `docs/README.md` lines.

### PR 2 · Commit 5 — `feat(space-settings): save the attendance card`
- **`features/occupancy`** (new web feature; not dashboard-only, as architecture §3 lists it):
  `OccupancyRepository` `getCapacity(spaceId)`, `setCapacity(spaceId, SetCapacityRequest)` at
  `/manage/spaces/:spaceId/capacity`; keys `['space', spaceId, 'occupancy', 'capacity']`; exports
  `useCapacityQuery(spaceId)`, `useSetCapacity(spaceId)` (its `onSuccess` sets the answer).
- **`pages/dashboard/space/settings/attendanceSchema.ts`**: `attendanceSchema: FormSchema<AttendanceRequest>`
  where `AttendanceRequest = SetCapacityRequest & Pick<UpdateSpaceSettingsRequest, 'autoCheckoutAtClosing' |
  'maxStayMinutes'>`; `safeParse(input)` runs `setCapacitySchema.safeParse({ capacity })` and
  `updateSpaceSettingsSchema.safeParse({ autoCheckoutAtClosing, maxStayMinutes })` and merges their data or
  their issues (S8).
- **`useAttendanceCard(spaceId)`**: both queries; values `{ capacity: string, autoCheckoutAtClosing: boolean,
  maxStayHours: string }`; `prepare`: capacity `''` → `null`, else its digits (Arabic-Indic read); hours `''`
  → `null`, else × 60. **Submit:** capacity changed → `await setCapacity`, then the card's baseline takes the
  answer (`capacitySaved = true`); settings changed → `await save` with only the changed of the two; a failure
  after `capacitySaved` sets the failure's title to `attendance.partial` and rethrows, so `useServerForm`
  shows it with the refusal's line and its field errors (`maxStayMinutes` on the hours field) and keeps every
  value; a failure before it uses `card.failed`. Nothing changed → nothing sent, «لم يتغيّر شيء». Saved →
  one toast «حُفظت إعدادات «الحضور والحالة المباشرة»».
- **`AttendanceCard`** renders `SettingsCard` (from `space-settings`) with the three fields; `SettingsPage`
  places it first.
- Words (`spaceSettings.attendance`):

| key | ar | en |
|---|---|---|
| `title` | الحضور والحالة المباشرة | Attendance and the live status |
| `capacity` / `capacityHelp` | السعة / لا تظهر للزوار. بها تُحسب الحالة «ممتلئ»؛ بدونها لا تظهر حالة مباشرة. | Capacity / Never shown to visitors. It decides when the space shows “Full”; without it there is no live status. |
| `autoOut` / `autoOutHelp` | خروج تلقائي عند الإغلاق / يُسجَّل خروج من بقي عند موعد الإغلاق. | Automatic check-out at closing / Whoever is still in is checked out at closing time. |
| `maxStay` / `maxStayHelp` | خروج تلقائي بعد (ساعات) / يُسجَّل خروج من يبقى أكثر من هذه المدة قبل الإغلاق. اتركه فارغًا ليكون الخروج عند الإغلاق فقط. | Automatic check-out after (hours) / Whoever stays longer is checked out, before closing. Leave it empty to check out at closing only. |
| `optional` | اختياري | Optional |
| `fieldErrors.capacity` | out_of_range / invalid_format «عدد صحيح من 1 إلى 1000» | A whole number from 1 to 1,000 |
| `fieldErrors.maxStay` | out_of_range «من 1 إلى 23 ساعة» · invalid_format «عدد ساعات صحيح» | From 1 to 23 hours · A whole number of hours |
| `partial` | حُفظت السعة، ولم تُحفظ إعدادات الخروج التلقائي | The capacity was saved; the automatic check-out settings were not |

- Docs: `occupancy.md` (header: a web feature, its hooks only; *Who uses it*: the owner's settings page;
  *Web decisions*: «**The capacity is saved through the settings page's attendance card, before the
  settings**… finding 96. {date}, #PRNUM.»; code map; *Web history*); `space-settings.md` (*Behaviour* the
  attendance card; *Web decisions* the order, the partial line and the kept values, S8); finding 96 → Resolved.

### PR 2 · Commit 6 — `feat(space-settings): edit the debt reminder`
- **`useReminderCard({ spaceId, spaceName, textareaRef })`**: values `{ text }` — the saved template, or, when
  it is `null`, `copy.spaceSettings.reminder.defaultText` (`usesDefault = true`); `insert(token)` puts the
  token at the textarea's caret (`selectionStart`/`selectionEnd`), marks the form dirty, then puts the caret
  after it and the focus back; `restore` sets the default text and `usesDefault`; `prepare`: `usesDefault` and
  the text unchanged → `{ reminderTemplate: null }`, else `{ reminderTemplate: text }`; the field's error text by
  `form.codes.reminderTemplate`: `invalid_choice` → `unknown({ token })` with the first `placeholdersIn(text)`
  not in `REMINDER_PLACEHOLDERS`; `invalid_format` → `missingAmount` when the text lacks `REMINDER_AMOUNT`,
  else `badCharacters`; `too_short`, `too_long` their lines. `preview` from `reminderPreview(text, sample)`
  (`{الاسم}` → the sample name, `{المبلغ}` → `priceText(15000, language)`, `{المساحة}` → `spaceName`).
- **`ReminderCard`**: the `Textarea` (rows 4, `dir="rtl"` only for its Arabic placeholders' buttons, never
  the field), «إدراج:» and three outline small buttons (visible token, accessible «إدراج الاسم» …), the
  preview box (`bg-muted`, «معاينة»), «استعادة النص الافتراضي» (ghost) in the footer.
- Words (`spaceSettings.reminder`):

| key | ar | en |
|---|---|---|
| `title` / `description` | رسالة التذكير / رسالة واتساب جاهزة لتذكير زبون بدينه؛ ترسلها أنت. | Reminder message / A ready WhatsApp message to remind a customer of a debt; you send it yourself. |
| `text` / `insert` / `insertNamed` | نص الرسالة / إدراج: / name «إدراج الاسم» · amount «إدراج المبلغ» · space «إدراج المساحة» | Message text / Insert: / Insert the name · Insert the amount · Insert the space |
| `preview` / `sampleName` | معاينة / رهف | Preview / Rahaf |
| `restore` | استعادة النص الافتراضي | Restore the default text |
| `defaultText` | مرحبًا {الاسم}، تذكير من {المساحة}: عليك {المبلغ}. يمكنك الدفع في المساحة. شكرًا. | Hello {الاسم}, a reminder from {المساحة}: you owe {المبلغ}. You can pay at the space. Thank you. |
| `fieldErrors` | too_short «اكتب نص الرسالة» · too_long «الرسالة أطول من 500 حرف» · missingAmount «أضف {المبلغ} ليعرف الزبون كم عليه.» · unknown({token}) «{token} ليس من الكلمات المتاحة؛ استخدم الأزرار لإدراج {الاسم} أو {المبلغ} أو {المساحة}.» · badCharacters «احذف الرموز غير المسموحة من النص» | Write the message · The message is longer than 500 characters · Add {المبلغ} so the customer knows how much they owe. · {token} isn’t one of the words you can use; use the buttons to insert {الاسم}, {المبلغ} or {المساحة}. · Remove the characters that aren’t allowed |

  (`unknown`'s token is isolated with `isolate`, not a literal mark.)
- Docs: `space-settings.md` *Behaviour* (the reminder), *Web decisions* (the default's `null`, design issue
  17, the token named), *Web history* line.

## 10. Tests — each with its lane, title and the break that must make it fail

Each new test is seen red first (testing §3.5); for code that exists, the break is made once and its red
output recorded in the report. **Bold** = a consequence-naming confirm, a disabled action or a
permission-dependent difference (each has its break).

### PR 1
| # | Lane · file | Title | Break |
|---|---|---|---|
| 1 | unit · `shared/lib/money/shekels.unit.test.ts` (moved cases) | reads shekels typed with up to two decimals as whole agorot… (the moved titles) | `Math.round(shekels * 100)` → `Math.floor(shekels * 100)` |
| 2 | unit · `spaceEditorRepository.unit.test.ts` | **sends the owner's editor calls to the managed routes, and the admin's to the admin's** (each call's method and path, both places) | the owner's base `/admin/spaces` |
| 3 | unit · `editorScope.unit.test.ts` | **keeps the owner's space under the space's scope and the admin's under the admin's**; **marks the user's scope after an owner's write, the admin's after the admin's** | the owner's `spaceKey` `['admin', …]`; the owner's `answered` `['admin']` |
| 4 | unit · `mayEdit.unit.test.ts` | **lets the admin edit an unverified space only, and the owner a verified one only** | `mayEdit` → `!isVerified` for both |
| 5 | component · existing spaces hook tests | unchanged titles, `'admin'` passed | (refactor: all green; no break) |
| 6 | component · `useAreaOptions.component.test.tsx` | **reads only the public catalogue for an owner, a hidden area kept as "no longer offered"** (fake adapter: no `/admin/governorates`) | enable `useGovernoratesQuery` for `public` |
| 7 | component · `useAmenityChecklist.component.test.tsx` | **offers an owner the public catalogue's amenities, keeping a retired linked one in the value and counting it** (no `/admin/amenities`; the line «يبقى مرفق واحد…»; toggling another keeps the retired id) | drop retired ids from the value on toggle; read `useAmenitiesQuery` for `public` |
| 8 | component · `useSpaceEditor.component.test.tsx` | **gives the owner the head line and the public link, no notice and no privacy line**; **draws the prices as a link to Packages & prices on the owner's place, with its date, stale and missing** | return the admin's notice for the owner; `pricesLink` for the admin |
| 9 | component · `SpaceEditor.component.test.tsx` | **shows the owner «الباقات والأسعار» in place of the prices' fields, and no «يعدّلها»**; **shows the owner «مخفية عن الزوار» only while hidden** | render `PricesSection` for the owner; push the verified badge for the owner |
| 10 | component · `useSaveGroup.component.test.tsx` | **keeps an owner's answer under the space's scope and fetches the user's spaces again** (fake adapter: a second `GET /manage/spaces`) | `answered` → `refetchType: 'none'` for the owner |
| 11 | component · `useSectionFrame.component.test.tsx` | **says to the owner that their link ended on a 403, never that the space was verified** | `meanwhileLines` ignores the place |
| 12 | component · `AmenitiesSection.component.test.tsx` | **offers the owner no way to the platform's amenities list** | pass `listLink` for the owner |
| 13 | component · `SpacePricesEditor.component.test.tsx` | titles the prices «الأسعار المعلنة» with its own intro; **asks before leaving with unsaved prices**; the no-shift line links the opening hours | drop the guard; omit the link |
| 14 | component · `routes.component.test.tsx` | shows the owner the space profile under its title, read from the managed route; shows the owner Packages & prices; **refuses reception the space profile with the 403** | route `profile` with `BOTH` |
| 15 | unit · `packagesRepository.unit.test.ts` | lists, adds and edits a space's packages on the managed routes | the edit as `PUT` |
| 16 | unit · `packageSummary.unit.test.ts` | words a package's terms in Arabic plurals (validity 1, 2, 7, 30, 11; limits; students; shift) and its price by billing | leave `daysPerWeek` out of `summaryOf` |
| 17 | unit · `packageValues.unit.test.ts` | sends a limit turned off as none and one left empty as empty; reads Arabic digits; an amount in shekels as agorot | send `undefined` for an off limit |
| 18 | component · `usePackagesSection.component.test.tsx` | lists the packages, a paused one muted with «موقوفة»; **holds the switch while its change waits** (`aria-disabled`); replaces the row from the answer; a failure's toast stays; **offers a paused package that keeps its shift «إزالة الوردية», and no other package** | remove `pending` from the switch; offer `heldShift` for an active package |
| 19 | component · `usePackageSheet.component.test.tsx` | refuses in the browser a missing name, a validity of 0, 8 days a week, a price of 0, and a limit on but empty, sending nothing; lands a repeated name (409) on its field; fetches the space's scope again on a shift gone (422); sends the terms whole on an edit; closes and toasts once the list has arrived | `prepare` sends a limit on and empty as `null`; drop the `['space', id]` invalidation |
| 20 | component · `PackagesSection.component.test.tsx` | names each row's switch and edit by its package; the sheet's amount is labelled by its billing; **with no shift saved, says so and links the opening hours** (axe clean) | drop `availableNamed`; omit the link |

### PR 2
| # | Lane · file | Title | Break |
|---|---|---|---|
| 21 | unit · `usersRepository.unit.test.ts` | records a handover at a space on the managed staff route | the admin's path |
| 22 | component · `useTemporaryPasswordDialog.component.test.tsx` | **records the handover where the password was issued: the admin's route, or the space's** | ignore `handover.at` |
| 23 | unit · `staffRepository.unit.test.ts` | lists, adds, sets active and re-issues on the managed staff routes | `setActive` as `PUT` |
| 24 | unit · `staffBadges.unit.test.ts` | marks an active member's pending password, or its expiry, and none for a deactivated one | compare `expiresAt` with `>` reversed |
| 25 | component · `useStaffList.component.test.tsx` | lists the staff whole with their badges and count (plural); the empty state; a failure with its reference | drop the pending badge |
| 26 | component · `useAddStaffForm.component.test.tsx` | **says a new account is made and no existing one linked, before the submit**; lands `EMAIL_HAS_ACCOUNT` on the email in the owner's words; hands the password to the page once the list has arrived, keeping none in the cache; counts a 429 down | drop the notice; word the field with `errors.EMAIL_HAS_ACCOUNT` |
| 27 | component · `useDeactivateDialog.component.test.tsx` | **says every session ends, opens on «رجوع», and keeps its action until the answer**; a refusal stays inside; the answer replaces the row | close on confirm (`AlertDialogAction`); drop the sessions line |
| 28 | component · `useStaffActions.component.test.tsx` | **holds «كلمة مرور مؤقتة جديدة» with its reason when none is pending, and on a deactivated row**; re-activates at once with no toast, and a refusal's toast stays (`ACCOUNT_SUSPENDED`, `ACCOUNT_IS_ADMIN` worded) | offer the re-issue when settled |
| 29 | component · `useReissueDialog.component.test.tsx` | **says the previous password ends and the sessions with it**; hands the new password to the page; words `TEMPORARY_PASSWORD_NOT_PENDING`, `ACCOUNT_HAS_LINKS`, `ACCOUNT_SUSPENDED`, 404, and fetches the list again for the first and the last | drop the refetch |
| 30 | component · `StaffList.component.test.tsx` | the table's names (the menu «إجراءات: {name}»), the add button in the toolbar and the empty state; axe clean | menu label without the name |
| 31 | unit · `spaceSettingsRepository.unit.test.ts`, `occupancyRepository.unit.test.ts` | each call's method and path | `PATCH` capacity |
| 32 | unit · `roundingExample.unit.test.ts` | words the example at 1, 2, 3, 11 and 59 minutes through the plural forms | `n − 1` → `n` |
| 33 | component · `usePricingCard.component.test.tsx` | **enables the minutes only for "up after"**; sends the rule and its minutes together, `null` minutes for the others; refuses 0 and 60 before sending; a save that changed nothing sends nothing | send the rule alone when only it changed |
| 34 | component · `useReceptionCard.component.test.tsx` | saves the hand-typed price switch alone and says so | (new code: red first) |
| 35 | unit · `attendanceSchema.unit.test.ts` | merges both contracts' refusals onto their fields (capacity 0, 24 hours as 1440) | drop the settings' issues |
| 36 | component · `useAttendanceCard.component.test.tsx` | **saves the capacity, then the settings** (the fake adapter's order); **when the settings fail after the capacity, says the capacity was saved and the rest not, keeps every value, and sends only the settings on the next save**; an empty capacity sends `null`; hours sent as minutes; nothing changed sends nothing | swap the two calls; reset the form on a partial failure; keep the old capacity baseline |
| 37 | unit · `reminderPreview.unit.test.ts` | fills every placeholder, each time it appears | replace the first only |
| 38 | component · `useReminderCard.component.test.tsx` | inserts a placeholder at the caret; names the unknown placeholder; asks for `{المبلغ}`; shows the default text for `null` and keeps it `null` when unchanged; restores the default as `null` | `insert` appends; `prepare` sends the default text |
| 39 | component · `SpaceSettingsCards.component.test.tsx` | shows each card's title, its unsaved badge and discard; the load's failure with «إعادة المحاولة»; axe clean | drop the unsaved badge |
| 40 | component · `routes.component.test.tsx` | shows the owner the staff page and the settings page under their titles; **refuses reception the staff page with the 403** | route `staff` with `BOTH` |
| 41 | unit · `catalogues.unit.test.ts` (existing) | parity of the new sections | (existing; runs in the lane) |

## 11. Review Focus — inputs no planned test exercises

- An owner whose link ends while the profile is open: the next write's 403/404 (managed boundary) and the
  editor's 404 state inside the shell; the session's links still list the space until refreshed.
- Two tabs: the profile's prices row and the Packages page's prices card after a save in the other tab
  (the shared owner key, `staleTime` 30 s).
- The profile's `#hours` link from the Packages page while the editor is still loading (§13 check 7).
- 40 prices at 1024 px; a shift's long name in a chip and in a card at 390.
- A package with all four limits, a 60-character name, Arabic-Indic digits in every count, `daysPerWeek` 7,
  an amount `99999.99`.
- A deactivated receptionist whose temporary password is also pending (the held re-issue's line).
- An expired temporary password seen around midnight (UTC vs Asia/Gaza: `expiresAt` is compared as an instant).
- The reminder: 500 characters, a `{` alone, mixed Arabic and Latin with the caret between, Undo after an
  insert, a template saved in English then shown in Arabic.
- Capacity `1000`; the stay limit `23`; Arabic-Indic digits in both.
- The attendance card's partial failure in the real run (not producible locally; test 36 owns it).

## 12. The commits

| PR | # | Subject (chars) | Body (why) |
|---|---|---|---|
| 1 | 1 | `refactor(spaces): share the shekel helpers` (42) | packages type and show money as prices do (S3) |
| 1 | 2 | `refactor(spaces): give the editor its place` (43) | O1: one editor; the owner's place is used from commit 5 |
| 1 | 3 | `fix(spaces): start the prices table at 1024 px` (46) | finding 67, foundation §9 |
| 1 | 4 | `feat(lookups): offer the public lists to owners` (47) | the admin's lists refuse an owner (S2); finding `<n>` |
| 1 | 5 | `feat(spaces): add the owner's space profile` (43) | screen 20, O1 |
| 1 | 6 | `feat(spaces): edit prices on packages & prices` (46) | O6 |
| 1 | 7 | `feat(packages): keep a space's private packages` (47) | screen 21, O8; finding 81 |
| 2 | 1 | `feat(users): record a handover at a space` (41) | S4; design issue 15 |
| 2 | 2 | `feat(staff): add the owner's staff page` (39) | screen 22, OW-019; finding 90 |
| 2 | 3 | `feat(staff): deactivate, reactivate and reissue` (47) | OW-017, OW-018, O4 |
| 2 | 4 | `feat(space-settings): add the owner's settings` (46) | screen 24 |
| 2 | 5 | `feat(space-settings): save the attendance card` (46) | O2; finding 96 |
| 2 | 6 | `feat(space-settings): edit the debt reminder` (44) | O2's reminder |

Recount each subject before committing (≤ 50). A unit's code, tests and docs in its commit. A fix before the
push folds into its commit (`git commit --fixup <sha>`, then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash
origin/main`). No tool attribution. Stage by path; `git status` before each commit.

## 13. The procedure and the verification

Work in `C:\dev\masaha\app` only (never `app-b`, never `app-design`). Each commit message is written to a UTF-8
file without a BOM, LF endings, a body saying why, and `git commit -F <file>`.

### First checks (before any edit), PR 1
1. `git status` clean on `main`; `git fetch origin`; `git switch main && git pull --ff-only`.
2. **USERS merged:** `gh pr list --state merged --head feat/admin-users --json number,mergeCommit`; empty → stop.
3. **`git diff --name-status 4daedc94 origin/main`.** Read USERS' `4_REPORT_PR1.md` (its fixes, departures).
   A code file this plan names that changed in a way the plan does not cover → **stop and ask**.
   `packages/shared` changed → `npm run build -w @masaha/shared` before any web check, and re-read
   `packages`, `space-settings`, `occupancy` and `space-links`' staff types against §9; a difference → stop.
4. Open PRs: `gh pr list --state open --json number,headRefName,files`; one that edits a code file of this
   plan → stop and ask. Note DESK's head for the conflict check.
5. **Checks, each with its fallback:**
   - `toFieldErrors` (`packages/shared/src/core`) gives `required` for a count field sent as `''` (read it, or
     a focused unit run of `packageValues`' test once written). If it gives `invalid_format`, the limit's
     `fieldLines` word `invalid_format` with `fieldErrors.limitEmpty` too (inputs hold digits only, so no other
     `invalid_format` can reach them); state it as a departure.
   - `useServerForm` reads `failureTitle` on every render (it passes it to `useFormFailure` in its body —
     PR 2's attendance card depends on it). If not, stop and ask.
   - `TemporaryPasswordDialog`'s `kind` and `RefusalText` in `shared/forms` are as USERS left them; else stop.
6. The layer's `Sheet side="end"` is full width below 768 px with a `min-w-0` body (OW-010): read
   `shared/design-system/components/**/Sheet.tsx`. If not, build with it as it is and record finding `<n+2>`
   (no design-system change in this item).
7. React Router's `ScrollRestoration` scrolls to `location.hash` once the target exists: read how the editor's
   section links land today (`SectionNav`, `useSectionInView`). If a link from another page to
   `profile#hours` would not reach the section after the editor loads, the profile page passes the hash to
   `useSectionInView`'s `choose` once the space is ready (in `ProfilePage`, a two-line effect), stated as a
   departure; if that needs more than the page, link to the profile without the hash and say so.
8. The next free finding number → `<n>` (and on).
9. Branch: `git switch --no-track -c feat/owner-space-profile origin/main`.

### First checks, PR 2 (after PR 1 merged)
1. As 1 above; 2. `gh pr list --state merged --head feat/owner-space-profile`; empty → stop;
3. `git diff --name-status <PR 1's reported head> origin/main`: a code file of PR 2's list changed in a way
   not covered → stop and ask; 4–5 as above (DESK, `useServerForm`); 6. finding numbers;
7. `git switch --no-track -c feat/owner-staff-settings origin/main`.

### Per commit
`npm run lint` and `npm run typecheck`; focused runs of the touched test files while working; each new test
seen red first, its red line recorded; each break of §10 made, its red output recorded, then restored.

### On the head, once each
First: no `vitest` under `C:\dev\masaha\app-b\` —
`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'app-b' -and $_.CommandLine -match 'vitest' }`
empty (else wait). Then: `npm run test:unit` · `npm run test:component` (**record the time of
`routes.component.test.tsx` › "lists the owner's eleven pages"**, finding 87; a timeout → stop and ask, never
raise a limit) · `$env:NODE_ENV='production'; npm run build; Remove-Item Env:NODE_ENV` · `npm run check:build`
· `npm run check:classes` · `npm run format:check` · `npm run check:links`. **Not run:** `test:api` (no API or
shared change; CI runs it).

### The real run
- `docker start masaha-postgres-1` (never `db:up`; never `npm ci`); the API on 3320 (`npm run dev -w
  @masaha/api`, worker A's `masaha_dev`, migrated to `main`; `npm run db:seed` with `SEED_DEMO=true` only if
  the demo space is missing); the web on 5320 (`npm run dev`).
- Sign in as `demo-owner@example.com`, its password read from `apps/api/.env`'s `SEED_DEMO_PASSWORD` by the
  browser script itself — **never printed**, never in a screenshot or the report. Reception:
  `demo-reception@example.com` (same password). The admin: the seeded admin.
- **Browser:** the `playwright` MCP tools if present, else local headless Chrome over CDP; say which. Arabic
  light and English dark, at 390, 768 and 1440. Record the network log of the owner's pages.
- **PR 1 cases:** the profile (the head line, the checklist, each section's date; save «المساحة»'s Arabic
  name and see the switcher follow; add a shift and save the hours; tick an amenity and add one of its own;
  a contact; confirm a group; upload two photos, move one, make it the cover, remove one; leave with unsaved
  changes → the guard); the prices row → Packages & prices; «الأسعار المعلنة» at 1440 (table) and 768/390
  (cards, finding 67), save, confirm; a package: new (two limits, per day, students, a shift), edit, the
  repeated name refused, pause one with the switch; pause «صباحي» (the demo's package with the morning
  shift) → its held-shift line → «إزالة الوردية»; reception opens `/profile` → 403; the network log shows
  no `/admin/` request from the owner's pages; the admin's editor of an unverified space still saves a section
  and shows its amenities (regression), its prices table at 768 as cards.
- **PR 2 cases:** the staff page (the demo receptionist, «نشط»); add one with a new email (the notice, the
  one-time dialog, «نسخ», WhatsApp, «تم» → the toast) — the new row's pending badge; add with
  `admin@example.com` → the email's line; «كلمة مرور مؤقتة جديدة» on the new row (the confirm, the dialog,
  the handover); the same item on the demo receptionist (held, its reason); deactivate the demo receptionist
  (the dialog's line, «بلا وصول»), re-activate it; the settings page: each card's save and discard; the
  attendance card (capacity 40 → 35 and the stay limit 4 → 5 in one save; clear the stay limit); visit
  pricing (up after 10 → half hour → up after 15; the example); the reception switch; the reminder (insert
  each token at the caret; remove `{المبلغ}` → its line; type `{الاسم الكامل}` → its line naming it; save;
  restore the default); reception opens `/staff` and `/settings` → 403.
- **Not performed, by design:** the attendance card's partial failure, a re-issue's
  `ACCOUNT_HAS_LINKS`, a re-activation's `ACCOUNT_IS_ADMIN`, a package's shift removed meanwhile, the
  owner's link ending mid-session, a space with no shift saved (the demo's shifts are used by prices and
  packages) — their component tests prove them. Any other case not performed → the stop rule.
- Screenshots to `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\shots\pr<n>\` (moved there if saved elsewhere);
  never committed. Stop the servers by PID (`Get-CimInstance Win32_Process -Filter "Name='node.exe'" |
  Where-Object { $_.CommandLine -match 'C:\\dev\\masaha\\app\\' }`, `Stop-Process -Id …`);
  `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` empty; `git status` clean.

### Push and the PR
1. `git grep -n "#PRNUM" HEAD`; the next number: `gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number'` + 1 (DESK may take it first: check at that moment).
2. In Git Bash: `git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#<n>/g'" origin/main..HEAD`,
   then `git update-ref -d refs/original/refs/heads/<branch>`; `git grep -n "#PRNUM" HEAD` empty; `git diff
   origin/main --stat` the same files as before.
3. `git push -u origin <branch>`; `gh pr create --assignee @me --label feat --label area:web --label area:docs`,
   title = PR 1's commit 5 / PR 2's commit 2 subject; the description per workflow §3 (Summary; Scope /
   Acceptance criteria / Out of scope; Change type; Evidence — run and not run; Screenshots — attached by the
   owner; the Definition of Done). Confirm the number matches.
4. `gh pr checks <n>` green on the pushed head's SHA; `gh pr view <n> --json mergeStateStatus` `CLEAN`.
5. The conflict check: for each other open PR (DESK's), `git fetch origin <its head ref>` and `git merge-tree
   --write-tree origin/<branch> origin/<other>`; record it.
6. The report `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\4_REPORT_PR<n>.md`, written **as you go** (after the
   first checks, after each commit with its sha, subject length, red line and green line, after each break with
   its red output, after the real run, after the push), UTF-8. **Never merge.** Each PR is reviewed in a
   separate conversation (over 25 files).

### The stop rule (as `USERS\3_EXEC_PROMPT.md` §2)
**A test you cannot run stops the work.** A test **failing** because its code is not written yet is the plan's
red step — normal. A test, lane or command you **cannot run** is not: it errors before any test runs (the
database unreachable, Docker down, a port taken, a module or `dist` missing, a migration pending, `No test files
found`, a Vitest or TypeScript startup error, the whole run timing out, a crash with no result); a break you
could not make or run; a real-run case you could not perform (other than those the plan names). **Then stop at
once** — never skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never
mock what the plan does not, never run a narrower command and call it the lane, never call it "flaky" and move
on. Write the command, its exact error and where you were into the report, and reply with `Status: STOPPED`.
**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do not
choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the
plan's break cannot change the outcome (as a bound already excluded by another); then make the break that can,
see it red, and state it as a departure.
**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that line
(read it by its exit code). A break counts only when you saw it red.

### Stop and ask
- USERS (for PR 1) or PR 1 (for PR 2) not merged; a base diff changes a code file this plan names in a way it
  does not cover; an open PR edits one of this plan's code files.
- Anything would need `apps/api`, `packages/shared`, the schema, a dependency, `shared/copy/*/errors.ts`, or a
  design-system change.
- `packages/shared`'s `packages`, `space-settings`, `occupancy` or staff types differ from §9.
- `useServerForm` does not read `failureTitle` per render (check 5).
- An existing spaces, lookups or users test fails after commit 2 (PR 1) or commit 1 (PR 2), and the cause is
  not the threading's own mistake.
- `check:build` fails because a module of this item reaches the site's first download.
- The routes test times out (finding 87).
- Three fixes of one failure have failed; a decision this plan does not settle.

## 14. Decisions needed from the owner

1. **The plan as written**, with S1–S11 as recommended (S1's explicit threading rather than A1's context;
   S2's public lookups; S3's `shared/lib`; S4's `handover` prop; S8's page-composed attendance card).
2. **The retired amenities an owner cannot name** (S2, finding `<n>`): accept for v1 with the counting line, or
   ask worker B for A2's read (a separate API item; this plan does not wait for it).
3. **The folded findings:** 67 (PR 1, the admin's editor's table moves to `lg` too), 81 (PR 1), 90 and 96 (PR 2).
4. **The design issues 1–18**, each as written; 15 (the forced change's line) folded or recorded as `<n+1>`.
5. **PR 1's size** (≈ 105 files, seven commits): keep one PR (the owner's decision 1), or take A4's split.
6. **Finding 92** (an owner's deactivation can sign out a person who owns another space): the staff screen
   deactivates as the API does; decide later whether the API should end sessions only when no other link is
   held — not in this item.
7. **The Arabic copy** of §9 (the owner approves Arabic copy, localisation › Catalogues).

## Appendix — steps mapped to Claude Code skills (only a map; no step depends on them)

| Step | Skill (if present) |
|---|---|
| Before the branch | `start-work-item` (its git checks; the plan is already saved) |
| Each test red first; each break | Superpowers `test-driven-development` (with `writing-good-tests.md`), per workflow §10 |
| A failure or a flake | `systematic-debugging` |
| Claims in the report and the PR | `verification-before-completion` |
| Opening the PR, its self-review, a conflict with `main` | `open-pr` |
| After CI is green and `CLEAN` | `final-report` |
| The real run's screenshots | `run`, or the Chrome tools; else headless Chrome over CDP |

# S2b-4a — The admin's space editor, first half (web)

**Worker A** · main folder `C:\Users\basel\masaha`, on `main` (`e30a86c`), tree clean · branch
`feat/admin-space-editor`, cut with `git switch -c feat/admin-space-editor origin/main` after
`git fetch --prune origin`. Databases `masaha_dev` / `masaha_test` (migrated); API on 3320, web on
5320. Its `apps/web/.env` sets `NODE_ENV=development`: build with `NODE_ENV=production` before
`check:build`.

**Model:** Opus 5.5, effort high. **Size cap:** at most 3 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\S2B4A_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\S2B4A_REPORT.md` (`final-report`).
**Screenshots:** `C:\Users\basel\Downloads\s2b4a-shots\` (never committed).
Follow the skills from start to end: `start-work-item`, `write-plan`, `open-pr`, `final-report`.

## 1. The task in brief

The admin edits a space on the dashboard, from the design the living prototype now holds (#61, #66).
The editor is built in **two items**; this is the first. The second (S2b-4b) adds the hours with their
shifts and the prices.
- **The editor's frame:** a page per space, its title the space's own name, the section navigation
  (a side list from `lg`, a sticky row of chips below it, the section in view marked).
- **«المساحة»:** the profile — the basics and the location as two blocks, one footer, one date, one
  «المعلومات ما زالت صحيحة» (built from #57's `BasicsFields` / `LocationFields`, made for this reuse).
- **«المرافق»:** the platform's common amenities to tick, then the space's «مرافق إضافية» (own
  amenities, #64), saved together, dated and confirmed together; «إدارة قائمة المرافق» under the list.
- **«التواصل»:** the contract's seven types, «هاتف» with its carrier derived from the prefix beside
  it, each value's helper showing its stored form, refused on its field when it cannot be stored.
- **Every group:** «لم تُضف بعد» with Save only while never saved; the date otherwise, a «قديمة» badge
  when stale, and the confirm; save always enabled with «تغييرات غير محفوظة» beside a dirty section.
- **«ما زال ناقصًا»:** the checklist heads a space with any missing group, each line linking its
  section, and goes once nothing is missing.
- **After a creation (A2):** the add page now lands on the new space's editor, under the checklist,
  not on the list (#57's D2 changes; record it).
- **The verified space:** the editor is read-only (the API refuses the admin's edit), its Alert naming
  the owner, with «عرض في الموقع» and the unlink's way.
- **An entry point:** «تعديل» in each row's menu of the admin's spaces list, and the space's name a
  link to it.

## 2. Read first

In the order workflow §2 *Reading before work* gives.
- **The capability documents first:** `docs/features/spaces.md` (all: its web decisions D1–D8 of #57,
  the API's groups, save and confirm) and `docs/features/lookups.md` (the area field, the public
  catalogue, the amenities).
- **The design:** the screenshots in `C:\Users\basel\Downloads\a-edit-space-screens\` (frames 01–04
  and 06; 05 is a later item) and the prototype itself: `docs/design/prototype/Admin space edit.html`,
  `Admin space add.html`, `masaha/profile-a.jsx`, `profile-b.jsx` (serve `docs/design/prototype` with
  `npx serve`); `docs/design/CHANGES.md` › batches 2a and 2b (what each decision built);
  `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md` › A1, A2, Contacts, AD-012 and its
  *Amended* notes.
- `docs/api/api-contract.md` › *Spaces (the admin)* (`AdminSpace`, `PATCH`, the group `PUT`s, the
  confirms, the errors); `docs/frontend/architecture.md` (§2 the routes and the record-name title rule
  of #68, §3, *Forms*, §7); `docs/frontend/design-system/foundation.md` §5, §9, §10, §12;
  `docs/frontend/localisation.md`; `docs/development/testing.md`; Issue #70.

## 3. The settled decisions (review them in "Stronger decisions")

- **D1 — two items:** this one as §1 says; the hours, the shifts and the prices are S2b-4b. Until
  then their sections are absent (not "coming soon"); the checklist still lists the five groups.
- **D2 — leaving with unsaved changes warns:** a dirty section makes a navigation away (a link, Back,
  the switcher) ask first, naming the sections, and closing or reloading the tab asks through the
  browser. Saving or discarding clears it.
- **D3 — no photos and no report notice:** the gallery and the open-report Alert need APIs not built
  (photos; data reports): absent from this item, nothing promised.
- **D4 — the title is the space's name** (#68's record-name rule, built here for its first page): the
  route's title while it loads, then the space's own name (its language marked) in the top bar and the
  tab, through the one place both read. **Fix Issue #70** in its own commit: `PageHeader` never renders
  an empty heading.
- **D5 — the editor's sections are the capability's, made for the owner to reuse** (step 5, O1):
  nothing in them only the admin's page uses; the page sets what differs (the lookups link, the
  read-only state).
- **D6 — the add page's landing (A2):** after a creation, the new space's editor under the checklist;
  the toast stays. Supersede #57's D2 in `spaces.md` with the date and the reason.

## 4. Findings and issues

- **Issue #70:** fixed here (D4), its own commit, closed by the PR.
- Read the open findings' titles; open those that touch the editor. Your new findings number **59–60**.

## 5. Risks

- **The sections' forms:** each saves alone, on its own route, with its own errors (422 on its fields,
  409, 429); a failure in one leaves the others as they are. Follow `shared/forms` and #57's patterns.
- **Truth to the API:** the admin edits only an unverified space; the contacts' stored form is the
  shared rule's (`@masaha/shared/spaces`), never a copy of it in the web.
- **The machine (the owner's rule):** **one full test run at a time on this machine.** Before a full
  lane (`test:component`, `test:api`), check that worker B is not running one (its folder is
  `masaha-b`; `Get-Process node` / the lanes' CPU); if it is, wait. Two at once made your last item's
  runs fail under load.

## 6. Boundaries with the other workers

- **Worker B** builds the public directory's API in `masaha-b` (`apps/api`, `packages/shared`'s public
  types, the contract's public sections). You change nothing in `apps/api` or `packages/shared`; if
  the editor needs a change there, stop and say so in the plan. Shared documents (`spaces.md` — yours
  is the *Web* part, the overview's *Built* line) are resolved by the fast path.
- **Two design fixers** work in `docs/design/` only (the account and the owner's batches). The owner's
  batch does not touch the admin's editor while you build it.
- Test files that change because a shared type changes are listed in the plan too.
- No new dependency (declare one in the plan if the section navigation truly needs it — it should not).

## 7. Checks, the pull request and the report

- **Locally, once each on the head, one at a time:** `test:unit`, `test:component`;
  `NODE_ENV=production npm run build` and `check:build`; `lint`, `typecheck`, `check:classes`,
  `format:check`, `check:links`. No API change: `test:api` not run (say so).
- **A real run** on 5320 with the API on 3320: create a space and land on its editor; save and confirm
  each section; add own amenities; a contact refused on its field; leave with a dirty section; open a
  verified space read-only. Screenshots at 390, 768 and 1440, RTL and LTR, light and dark, in the
  folder above. Stop the servers by PID and check the ports free.
- **PR:** title `feat(spaces): the admin's space editor` (≤ 50), labels `feat`, `area:web`,
  `area:docs`, assigned to the owner, `Closes #70`. An independent review follows. Don't merge.
- **The documents:** `spaces.md` (*Web decisions*, *Web history*, the code map, D6 superseding #57's
  D2), `lookups.md` if its amenities field is reused, `frontend/architecture.md` if the record-name
  title's place changes, the overview's *Built* line.
- At the report, `git merge-tree --write-tree` against every open PR. Stop every background shell you
  start; `jq` is not installed — use `gh … --jq`.

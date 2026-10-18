# S2b-4b — The admin's space editor, second half: hours with shifts, and prices (web) — PLAN ONLY

**Worker A, the planning conversation** · main folder `C:\Users\basel\masaha`, on `main` (`1240736`),
tree clean. **You write the plan, and only the plan:** no branch, no edit, no commit. Databases
`masaha_dev` / `masaha_test` (migrated); API on 3320, web on 5320 — only to look at the running
editor if you want to; stop what you start.

**Model:** Opus 5.5, effort high. **Size cap:** at most 3 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\S2B4B_PLAN.md` (`write-plan`; save, then stop).
Use `start-work-item` (steps 1–4) and `write-plan`; this prompt's §0 adds to `write-plan`'s sections.

## 0. A new way of working — on trial for this item (the owner, 2026-10-13)

This item runs in **three conversations**, not one:
1. **This one plans.** It reads, decides, and saves the plan. It ends there.
2. **A fresh conversation executes** the approved plan — the same model and effort, **with none of
   this conversation's context**: it reads CLAUDE.md, the plan, and the documents the plan names, and
   builds, verifies, opens the PR and reports. Review fixes go back to that conversation.
3. **A third conversation reviews** the PR independently.

*Why:* the owner's usage shows most of it spent in conversations past 150 k tokens of context; a
plan written for a reader without context is also a better plan; and **the executor may be another
tool** (Copilot or Codex) when Claude Code is out of its limits or its subscription lapses — so the
work goes on. Write the plan for any capable coding agent: **no step may depend on Claude's skills or
plugins** — where a skill would apply (`open-pr`, `final-report`, `add-error-code`), write its steps
into the procedure, with the commands. This is a trial: workflow §9's "one
Work Item is one fresh conversation" is **set aside for this item by the owner**, and becomes a rule
only if the execution comes out better.

**So the plan must stand alone.** Write it for a capable engineer who has never seen this
conversation, the analyst's notes or the design review, and who will **not** re-decide anything:
- **every decision taken,** with its reason in one line, so the executor can tell a slip from a choice;
- **the files,** each with what changes in it, and for a new hook, component or service its
  **interface** (name, inputs, what it returns or renders, which query keys it reads or invalidates) —
  not its full code;
- **every user-facing string written out in Arabic and English**, with its catalogue key;
- **the design** of each state named to the design system's components and variants (loading, empty,
  error, pending, dirty, saved, refused on a field, 409, 429, read-only), with the frames to match;
- **each test**: its lane and file, its title, and **the break that must make it fail** (testing §3);
- **the commits** with their subjects counted (≤ 50) and what each holds;
- **the executor's procedure**: branch command, the order of work, the checks after each commit, the
  local verification (phase 4), the real run (what to click, at which widths), the screenshots, the PR
  (title, labels, the description written out), CI and `CLEAN`, the report's path and sections, the
  early conflict check;
- **a "Stop and ask" list:** the situations in which the executor must stop rather than improvise
  (any change outside the files listed, a contract the API does not hold, a decision the plan did not
  take, a test that cannot be made to fail).

The executor's report goes to `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\S2B4B_REPORT.md`;
screenshots to `C:\Users\basel\Downloads\s2b4b-shots\` (never committed). The executor's branch:
`feat/space-hours-prices`, cut with `git switch -c feat/space-hours-prices origin/main` after
`git fetch --prune origin`.

## 1. The task in brief

The second half of the admin's space editor (S2b-4a, PR #74, built the frame, «المساحة», «المرافق»,
«التواصل», the checklist, the leave guard and the read-only verified space). This item adds:
- **«ساعات العمل»:** the week with its shifts, saved together, dated and confirmed as one group.
- **«الأسعار»:** the space's prices, saved, dated and confirmed as one group.

Both join the editor's navigation, the «ما زال ناقصًا» checklist, the leave guard and the verified
space's read-only view exactly as the first three sections do, and are made for the owner's editor to
reuse (the owner's page will show prices as a link to Packages, O1/O6 — not built here).

## 2. Read first

In the order workflow §2 *Reading before work* gives.
- **The capability document first:** `docs/features/spaces.md` (whole: the editor's web decisions of
  #74; *Hours*, *Prices*, *Save a group*, *Confirm*; the API decisions F3–F5, D4, D8–D9, prices above
  zero) and `docs/features/lookups.md` only where the editor reuses it.
- **What the editor already is:** `apps/web/src/features/spaces/` (`components/editor/`,
  `hooks/editor/`, the three sections' hooks and their `renderHook` tests — the pattern to copy,
  established by #74's review); `pages/dashboard/admin/SpaceEditPage.tsx`; #74's PR description and
  its "Review fixes" comment (what the review corrected, so you do not repeat it).
- **The contract:** `docs/api/api-contract.md` › *Spaces (the admin)*: `PUT …/hours` (the week and
  the shifts, ids kept, a removed shift in use refused 409), `PUT …/prices`, the confirms, their
  errors; `@masaha/shared/spaces` (the requests' schemas and their rules — use them, never copy them).
- **The design:** the prototype's `docs/design/prototype/Admin space edit.html` and
  `masaha/profile-b.jsx` (the hours and prices sections; serve `docs/design/prototype` with
  `python -m http.server`), `docs/design/CHANGES.md` › batch 2a/2b; the frames in
  `C:\Users\basel\Downloads\a-edit-space-screens\`; `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md`
  › *Hours*, *Prices* and its *Amended 2026-10-12* note; `DECISIONS_OWNER.md` › O6.
- `docs/frontend/architecture.md` (§3, *Forms*, §7); `docs/frontend/design-system/foundation.md`
  §5, §9, §10, §12; `docs/frontend/localisation.md` (times and numbers in both languages);
  `docs/development/testing.md` §1–§4; finding 60.

## 3. The settled decisions

- **D1 — scope: hours with shifts, and prices. No gallery** (the photos' API, PR #77, is not merged;
  the gallery is its own item, S2b-4c, with the browser's shrinking and the upload).
- **D2 — midnight:** no «24 ساعة» switch (no space in Gaza opens around the clock); «إلى» accepts
  24:00 as a day's end (DI-15); each day reads «مفتوحة» or «مغلقة»; a range 0–1,440 is the contract's
  open-all-day. «من» and «إلى» are two labelled fields, side by side from `md`, stacked below.
- **D3 — «نسخ إلى كل الأيام»** in the section's header, copying the first open day's range to every
  day (AD-007).
- **D4 — a shift lies inside the range of at least one open day** (the shared rule); its error names
  the day; the shift's English name is marked optional.
- **D5 — the price table's words are O6's (DI-30):** the period column «الفترة» / "Period", the
  audience «لمن: الجميع · الطلاب» / "For: Everyone · Students" (the prototype still says «المدة» and
  «الفئة»; the prototype catches up later — record it in the report, do not touch `docs/design/`).
  A small table from `md` with the labels once in its header, one card per price on a phone; every
  amount above zero; «إضافة سعر» disabled at the contract's limit with its reason; a repeated row
  refused on the field that would tell it apart.
- **D6 — «الوردية» in prices lists the space's saved shifts only.** None → the field disabled with
  «أضف ورديات أولًا». While «ساعات العمل» has unsaved changes, a line under the field says
  «احفظ ساعات العمل لتظهر الوردية الجديدة هنا» (write the English). Each section still saves alone.
- **D7 — a shift a saved price uses cannot be removed:** its remove button is disabled with the reason
  «يستعملها سعر — احذف السعر أولًا» (write the English), read from the space's saved prices; the
  server's 409 on the hours save stays handled (a price saved meanwhile elsewhere).
- **D8 — finding 60 folded:** a space whose area was hidden since shows that area in the area field,
  marked «(مخفية)», instead of an empty field; resolve the finding.
- **D9 — the patterns are #74's, as its review corrected them:** each section saves alone through
  its own hook (the profile's lesson: diff against what the form was filled from, never against a
  newer server answer); «لم تُضف بعد» with Save only while missing; its date, «قديمة», the confirm;
  «تغييرات غير محفوظة»; the leave guard; 403 → read-only, 404 → the 404; a 429 holds Save and the
  confirm with its reason; the hooks' logic proven in `renderHook` tests, the components' tests for
  what renders, the repository's for paths and bodies.

## 4. Findings

Read the open findings' titles; open those that touch the editor. Finding 60 is folded (D8). Your new
findings number **67–68**.

## 5. Risks

- **The hours' save shape:** the week and the shifts in one `PUT`; shifts keep their ids; a renamed
  shift is the same shift; the server's passing-name trick is the server's — the web sends names as
  typed.
- **Times in two languages and directions:** 24-hour times, Western digits, LTR inside Arabic; the
  day names from the locale or the catalogue — say which.
- **The machine (the owner's rule): one full test run at a time.** The executor checks that worker B
  (`masaha-b`) and the media worker (`masaha-media`) run no lane before `test:component`.

## 6. Boundaries

- **`apps/web` and the documents only.** Nothing in `apps/api` or `packages/shared`; if the editor
  needs a change there, the plan says so and stops.
- **Open items elsewhere:** worker B (PR #78, `apps/api`: sessions, users, auth), the media worker
  (PR #77, `apps/api`, `packages/shared/src/spaces/` additions only — **no type the web imports
  changes**), two design items in `docs/design/` (batch 5's fixes, batch 6's plan). Shared documents
  (`spaces.md` — yours is the *Web* part; the findings index; the overview's *Built* line) take the
  fast path.
- No new dependency.

## 7. Checks, the pull request and the report (for the executor; write them into the plan)

- Locally, once each on the head, one at a time: `test:unit`, `test:component`;
  `NODE_ENV=production npm run build` and `check:build`; `lint`, `typecheck` (on each commit),
  `check:classes`, `format:check`, `check:links`. `test:api` not run (no API change; say so).
- A real run on 5320 with the API on 3320: hours entered, a day to 24:00, copy to all days, a shift
  outside every open day refused, a shift in use not removable; prices added, a duplicate refused, the
  limit reached, a price for a shift; each section saved and confirmed; the checklist emptied; a
  verified space's two sections read-only. Screenshots at 390, 768 and 1440, Arabic and English,
  light and dark.
- PR: title ≤ 50 (for example `feat(spaces): the editor's hours and prices`), labels `feat`,
  `area:web`, `area:docs`, assigned to the owner. An independent review follows. Don't merge.
- Documents: `spaces.md` (*Web decisions*, *Web history*, the code map), finding 60 and the index,
  the overview's *Built* line.

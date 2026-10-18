# FIX_SHARED — review fixes for PR #59

Found by the owner's review of the pushed head `ac25093` on the local prototype; each item verified
against the code by the analyst. **Build F1, F2 and X1 only**; the last two sections are records for
later batches — do not touch them.

**The owner's override of the method, stated:** these fixes go in **one new commit** on top of the
branch (no fixup, no autosquash, no force-push), e.g. `docs(design): fix the review's three items`
(≤ 50 characters). Light verification: the Babel parse on the files you touch, `format:check`,
`check:links`, and a look at each fixed page at 390 and 1440 (F2 also at 1023/1024). Then push, wait
for CI and `CLEAN`, post ONE "Review fixes" comment, and add a "Review fixes" section to
`REPORT\FIX_SHARED_REPORT.md`. Before you finish, stop every background shell you started; `jq` is
not installed in Git Bash — use `gh … --jq`.

## From the owner's review

### F1 — The save footer sits flush against the content above it

- **What:** in a section card, the footer row («حفظ» and «المعلومات ما زالت صحيحة») has no gap
  above it: the save button touches the last field or button of the section (the Arabic description's
  textarea in «المساحة», «إضافة وسيلة تواصل» in «التواصل», «رفع صور» in «الصور»), as if it were part of
  that control. The footer is not set apart from the section's fields.
- **Where:** every section built with `ProfileSection` (`masaha/profile-a.jsx`, used by
  `profile-b.jsx`): `Owner space profile.html` and `Admin space edit.html`. Check every other card
  footer that holds a save the same way (`Owner settings.html`, `Admin settings.html`, `Settings.html`,
  `Packages.html`, `Announcements.html`, `Customer file.html`) and fix each that shows it.
- **Note:** the original frames show the same (screens `30-owner-space-profile-kept/01-…`), so it
  predates this PR; it is fixed here because P10 made this button the section's one save.
- **Fix:** one footer for every card that saves, from the design system's own card parts and spacing
  scale (no new class or colour): a clear gap between the content and the footer, the same at every
  width; «حفظ» first (primary), then the secondary action. Show before/after at 390 and 1440.

### F2 — The Directory shows its filters twice from 1024 (a regression of this PR)

- **What:** in list view from `lg`, the whole filter form is drawn inline in the toolbar, between the
  title and the results, **and** again in the sidebar; the toolbar grows to a screen of filters and
  the search and sort are pushed apart. Seen at 1118 px; `main` does not do it.
- **Cause (verified in the code):** `FilterSheet` (`masaha/shared.jsx`) returns its `children`
  inline when it is "wide". For every other list that is right (P5: inline from 768); the Directory
  calls it with `at="lg"` because **its sidebar** takes over from 1024, so there the sheet must draw
  nothing — before this PR the Directory drew only its own `Sheet` and the sidebar.
- **Fix:** a way for a caller whose filters live elsewhere at the wide width to get nothing back
  (the Directory's list view from `lg`); the map view keeps the sheet at every width (`always`).
  Check the Directory at 390, 768, 1023, 1024 and 1440, list and map, and the other eight pages that
  use `FilterSheet` at 768 and 1440 to see they are unchanged.
- **Also:** the 420-load matrix reported no problem here; it checks blanks and errors, not a layout
  drawn twice. Say so in the report's *unexpected* section.

## From the analyst

### X1 — `npx serve` drops every page parameter

- **What:** `serve`'s clean URLs redirect `X.html?…` to `X` and drop the query string, so no URL in
  `INDEX.md`, nor the new parameter table, opens its state, and `role`, `auth` and `id` are lost when
  navigating inside the prototype. `docs/design/README.md` recommends `npx serve .`.
- **Fix:** add `docs/design/prototype/serve.json` with `{ "cleanUrls": false }`, so `npx serve`
  keeps `.html` and the query; check one parameterised URL from `INDEX.md` through it.

## Decided at this review, for a later batch (not for this PR)

- **U12 — a cover photo on the space card** (the owner chose option 1): recorded in
  `DECISIONS_PUBLIC.md`; built with the public batch.

## Seen, not for this PR

- The «الصور» section carries a date, «المعلومات ما زالت صحيحة» and «حفظ»; A1 and O7 decide photos
  have no date, no confirm and no save. Batch 2 / batch 5 fix, not batch 1.
- **Admin spaces: «بيانات قديمة فقط» is a horizontal switch among stacked fields**, so it sits on its
  own line and does not align with the search, place and state fields (the owner). Predates this PR;
  **A7** already decides it: a `ToggleGroup` chip by the count. Batch 2.
- **Admin spaces: «إضافة مساحة» opens the edit page in a "new" mode** (`Admin space edit.html?new=1`)
  (the owner). Predates this PR; **AD-002** decides the design catches up with the built creation form
  (#57), and **A2** sends a created space to its edit screen. Batch 2.
- **Admin lookups: the content stops at `max-w-4xl`, the rest of a 1440 screen empty** (the owner).
  Predates this PR (the page is untouched). See the doubt on AD-029 in the analyst's notes.

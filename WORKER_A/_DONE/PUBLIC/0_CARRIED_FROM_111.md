# Carried from #111 (PUBLIC PR 4, `feat/home-about`) into the public site's fix PR (after the owner's in-person review)

**The owner's decision (2026-10-24):** #111 merged; its review
(`C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR4_CLAUDE_CODE.md`, head `03633534`) found no blocker. Every
fix waits for the owner's in-person review of the whole public site and goes into **one fix PR** with the
owner's own list. These are that PR's first commits, each code fix red first, then green. Read the review for
each item's file, line and scenario. The supervisor confirmed items 1 and 2 in the code.

**Already taken elsewhere (not here):** review items 9 and 13 (findings 137, 138), 11b (`lookups.md`'s scope)
and 11c (`architecture.md`'s date) ride on `TASKS\CONFLICT_GUARD_BASEL` — check they merged before this PR
starts; if not, they come back here.

**Decided by the owner (2026-10-24), as the supervisor recommended:**

1. **A link to a section focuses that section** (review 1; changes S8's rule "not when only the hash changes",
   approved): arriving at `/about#owners` or `/about#contact` — from another page or from About itself — moves
   the focus to the named section's heading (`tabIndex={-1}`), not to `main`; no hash → `main` as today. A routes
   test for each case; break: the old rule → red.
2. **«تواصل معنا» once** (review 2): the freshness note's last sentence becomes the link itself: «إن وجدت معلومة
   خاطئة، تواصل معنا.» with «تواصل معنا» linking `#contact` (design issue 41), the rest of the note word for word.
3. **Home's owners' card** (review 3): «تواصل معنا لإضافة مساحتك، وإدارة ساعاتها وأسعارها، وتظهر حالتها المباشرة
   تلقائيًا من تسجيل الحضور.» / "Contact us to add your space and manage its hours and prices; its live status
   shows automatically from the check-ins."
4. **Home's title waits for its answer** (review 4): keep the previous title while the list shows placeholder
   data (or show skeletons when available ↔ nearest changes); a test.
5. **A second retry while offline is announced** (review 5): the status line re-announces on each press; test
   80 presses twice.
6. **The phone's single tile names «عرض كل الصور (n)»** (review 6): its accessible name or description carries
   the pill when `more` is set; a test.
7. **The page's live badge through `statusViewOf`** (review 7): one mapping of status → word and tone.
8. **Three tests** (review 8): the footer's room given back on leaving a space page; «اختر منطقتك» scrolls to and
   focuses the areas' heading; «حدّد موقعي على الخريطة» starts the pick and opens `/spaces?view=map`.
9. **Documents** (review 11a, 11d, 11e): `directory.md`'s *Authority* names Home's spaces and counts and About's
   legend; `overview.md`'s Directory line leaves the contact to `platform-settings`; `SiteFooter.tsx`'s JSDoc
   within 100 characters.
10. **`maxLength` from the shared constant** (review 12): `HomeSearch` and `DirectorySearch` read
    `SPACE_NAME_MAX_LENGTH` from `@masaha/shared/spaces`.
11. **The two slow site tests** (review 10, plausible): record them under finding 87 (the cold lazy import inside
    a 3 s `findBy`), with the fix it names; no change to the timeout. **Add (from #116, 2026-10-25):**
    `App.component.test.tsx` › "renders the main landmark" and `router.component.test.tsx` › "shows the
    root's general error…" missed 3 s the same way locally (the site's lazy shell), passed alone and in CI.
    **And (from #117):** `routes.component.test.tsx` › "lists reception's four pages".
    **And the owner's own find (2026-10-25):** changing a page of the Directory makes the screen jump twice —
    `ScrollRestoration` resets to the top on the pushed address, then `DirectoryResults.tsx:39`'s
    `scrollIntoView` runs before the new page arrives. **Fix:** `preventScrollReset` on `ListPagination`'s three
    links (`shared/lists/components/ListPagination.tsx` 29, 41, 54), and the results' scroll and focus moved to
    after the new page has arrived (`isPlaceholderData` false); a test that no scroll happens while the old page
    still shows.

**Not carried:** review 14 (the report's "21 areas" sentence) — the report only.

Every item is done in that PR; one you would leave, or one that proves larger than this file says → **stop and
ask**, never silently. A new finding takes **139** and on.

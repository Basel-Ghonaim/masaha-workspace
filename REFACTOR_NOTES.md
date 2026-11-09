# The owner's notes for the future refactor table

Raw notes from the owner's use of the live site, kept until the refactor table is planned (after the 2026-11-03
presentation). Each one is checked in the code and becomes a finding or a work item then.

- **2026-11-02 — Home's «المتاحة الآن» is empty on the live site.** A space's live status shows only on a verified
  space (an owner linked — v1's rule); the live site's 13 spaces are all unverified, so the section stays empty and
  every card reads "No live status". The owner: an empty section is not sensible. Options to weigh then: a fallback
  for the section (e.g. the spaces open now by their hours, marked unverified), a status by hours for unverified
  spaces, or default hours. Not for tomorrow: the local demo has verified spaces.
- **2026-11-02 — The pagination bar shows with a single page** (the directory, one page of results: «Previous 1
  Next»). It should hide when there is only one page. Check every paged list (the directory and the dashboard's
  tables).
- **2026-11-02 — "many problems" seen while browsing the live site** — the owner will list them for the table.
- **2026-11-04 — the online cron runs every 60 minutes, not 15 (the owner's decision while the site is not
  launched):** fewer Neon wake-ups; a late run never corrupts data (the auto check-out records its due cut-off). The
  documents still say 15 (setup.md › The deployment, ADR 0014's revision line, conventions §12, api-contract
  *Internal*, finding 213): correct them in the next PR, and revisit the interval at the official launch.
- **2026-11-05 — the privacy page's contact line (#135):** the email shows inside About's contact card, and the
  sentence's closing «.» is left alone after the card. Show the email inline in the sentence, or drop the stray dot.
- **2026-11-05 — the reset email lands in spam (Gmail SMTP from a new Masaha Gmail, no own domain; ADR 0014's email
  deviation).** Works, but users may miss it. Cheap: a line on the "link sent" screen — «لم تصلك الرسالة؟ تفقّد مجلد
  الرسائل غير المرغوب فيها» (both languages). Real fix at launch: an own domain and a domain-verified email provider
  (SPF, DKIM, DMARC).
  **Checked 2026-11-05:** the "link sent" text already ends «تفقّد مجلد الرسائل غير المرغوب فيها» — no change needed there.
- **2026-11-05 — nits from #136's review (for the next PR's first commit):** `ListPagination.tsx` names a variable
  `here0` (read the location once as `search`, then `here = searchKey(search)`), and its comment cites the workspace
  task «QUICK_FIXES_1» — a repository comment names the rule or the PR, never a workspace folder.
- **2026-11-05 — refactor round 1: the directory's filters (decided).** The price range and the period leave the
  panel; «السعر» joins the sort with its subscription (monthly default) and direction; a space without that price
  leaves the list while sorting by it; the card shows that price then; the place filter by governorate then area;
  new filters «مفتوحة الآن» (by hours), amenities, «مفتوحة مساءً». Decisions and method:
  `TASKS\DIRECTORY_FILTERS\0_OWNER_DECISIONS.md`; the prototype round first (OpenCode, `3_EXEC_PROMPT.md`).
  **Revised the same day (Revision 1, `3_EXEC_PROMPT_FIX1.md`):** no chips anywhere; the price sort is one Select of
  whole options; no amenities, no live/open-now filters for now; «أخرى» as checkboxes with «مساءً»; the place is one
  dropdown with a search and six collapsible rows (five governorates + «كل المناطق»), one choice, `?gov=` for a whole
  governorate. **Final: Revision 2 (2026-11-07)** in `0_OWNER_DECISIONS.md` — segmented subscription + range, the
  direction in the sort, «الدوام» (open now / evening / Friday), «أخرى» (verified / students); «مفتوحة الآن» by hours
  for every space (ADR 0008 revision owed in the production step); «ممتلئ» a badge; hours optional; women's spaces
  approved as a direction (own ticket later). Worker prompt: `3_EXEC_PROMPT_FINAL.md`.
  **Merged 2026-11-07 as #137 (`40cb481d`, prototype only).** The web/API step is still owed (new branch, new PR):
  the production notes in `0_OWNER_DECISIONS.md` › Revision 1's end and Revision 2 (A1–A4), ADR 0008's revision,
  a segmented-control component in the design system, `openNow`/`evening`/`sort=price` in the API.
- **2026-11-07 — a flaky component test (to fix in its own small PR, record as finding 214 — check the index
  first):** `apps/web/src/pages/site/public/home/HomePage.component.test.tsx` › «Set my location on the map» starts
  the pick on the Directory's map — after navigating to `/spaces?view=map` it waits for the searchbox with
  `findByRole`'s default 1 s; under CI load the lazy map view takes longer. It failed twice on #137 (which changed no
  app code; it passes locally alone; main's last runs passed). #137 was merged on the owner's word with that one
  check red. Fix: wait for the route's content properly (a longer `findByRole` timeout, or await the lazy chunk),
  no production change.

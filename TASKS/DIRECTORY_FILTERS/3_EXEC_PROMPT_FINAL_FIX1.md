# DIRECTORY_FILTERS — final round, review fixes 1 (the owner approved, 2026-11-07)

Same session, same rules as `3_EXEC_PROMPT_FINAL.md` (prototype only, **no commit**, stop at ready for review). One
more allowed file for this note: `docs/design/prototype/masaha/space-parts.jsx`. Before starting:
`git branch backup/directory-filters-3b` (a branch at the same commit is fine) and copy the modified files to
`C:\dev\masaha\workspace\TASKS\DIRECTORY_FILTERS\backup-3b\`.

1. **An unverified space's card says its state by its hours.** Today `LiveStatus` (`masaha/shared.jsx`) shows «لا
   تتوفر حالة مباشرة» for every unverified space, which contradicts «مفتوحة الآن» listing it. Change: an unverified
   space **with hours** shows «مفتوحة الآن» / "Open now" or «مغلقة الآن» / "Closed now" by its hours on Gaza's clock
   (and «مغلقة الآن» under a closure in force), as a **neutral** badge (`variant="neutral"`, never `success`: it is
   not a live state); one **without hours** keeps «لا تتوفر حالة مباشرة». Verified spaces are unchanged (متاح /
   ممتلئ / مغلق الآن). To do this, **move** `gazaNow`, `toMins` and the open-now rule from `Directory.html` into
   `masaha/shared.jsx` (one definition; `Directory.html` uses it). Check the global scope (no name another script of
   those pages already has). Look at Home, the directory (list and map card), Favorites and Space details: each
   shows the same state for the same space. A page that does not load `details-data.js` has no closures — say which
   in the report.
2. **A space without hours on its own page.** Make `masaha/space-parts.jsx` cope with `space.hours` null: the today
   line (`TodayLine`, around line 92) shows «ساعات العمل غير متوفرة» / "Hours not available"; the hours section
   (`HoursSection`, `groupDays`, around line 209) shows the same text in place of the week (the section stays, with
   its heading). Then give **ZM Hub** `hours: null` in `masaha/data.js` for good, and **remove** the `?demo=nohours`
   switch from `Directory.html` (and its INDEX row; an INDEX row for `Space details.html?space=zm` or however that
   page picks a space, showing the text). Check every other reader of `s.hours` still copes
   (`grep -rn "\.hours" docs/design/prototype`).
3. **No dead items in the sort.** Under «الكل» the sort `Select` lists only «الأحدث تحديثًا» and «حسب الاسم»: the
   two price items are **not rendered** (not disabled). Once a subscription is chosen they appear: «الأرخص شهريًا» /
   «الأغلى شهريًا» (by the subscription). Clearing the subscription while sorting by price returns to «الأحدث
   تحديثًا», as now.

Then: update `CHANGES.md` (R3's card state for unverified spaces, R5's space page, R2's hidden items) and `INDEX.md`;
both checks; look at 390, 768, 1024 and 1440, Arabic and English, light and dark; screenshots to
`C:\Users\basel\Downloads\directory-filters-shots\final-fix1\`. **Stop, nothing committed**, and print `git status
-s`, `git diff --stat`, the checks' output and the ready URLs (the directory with «مفتوحة الآن», ZM Hub's card and its
page, the sort under «الكل» and under «شهر»).

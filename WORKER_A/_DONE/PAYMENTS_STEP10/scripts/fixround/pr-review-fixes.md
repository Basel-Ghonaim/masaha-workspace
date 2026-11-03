
## Review fixes (2026-10-28/29)

Every finding of the three Claude reviews fixed (the owner's decision: nothing carried), each folded into the commit that made the code, each code fix with a test seen red before it and a break that turns it red again:

- **R1-F1 (blocker)** — an edit never sends a start or an end the user did not change: compared at the Gaza date and minute the sheet shows, not to the millisecond (a start posted «الآن» keeps its seconds on the server). → `feat(announcements): post and edit an announcement`.
- **R1-F2** — a 409 or a 404 stays in the extension's or the delete's dialog: the list holds the opened dialog (as it holds the sheet), so a refetch that changes the card no longer unmounts it; on close the focus goes to the opener, else the card's first action, else the next card or the tab. → `…end, start or delete one`, `…extend after a closure`.
- **R1-F3** — finding 169's resolution names the announcement sheet's period among the calendar's importers. **R1-F4** — the sheet's calendar marks Gaza's today. → `…post and edit an announcement`.
- **R1 (outside its range)** — `announcements.md`'s *Web history* line starts "#129 —". → `…show a space's announcements`.
- **R2-F1** — `data-reports.md`'s *Open findings* lists 167. → `…list every space's reports`.
- **R2-F2** — after `REPORT_ALREADY_DECIDED` the sheet shows the decision, read from page 1 of «الكل» of the same scope, and never a stale «جديد» («تمت المراجعة» until it is read); the owner's and the admin's. → `…decide a space's reports`, `…list every space's reports`.
- **R2-F3** — the focus after a filter tag or «مسح الفلاتر» leaves: the next tag's button, else «مسح الفلاتر», else the count. → `…list every space's reports`.
- **R2-F4** — recorded as **finding 184** («تعديل الحقل»'s anchor may not scroll on arrival; plausible, not run in a browser). → `…list every space's reports`.
- **R3-F1** — **the owner's decision on DI-58, option (a):** «إزالة» of a space that left offers no «تراجع» (the API answers 404 to a re-save) and says it cannot be saved again while out of the directory; **finding 187** recorded (an undo would need the API to allow it). → `feat(favorites): list a user's favourite spaces`.
- **R3-F2** — a guest's held favourite and report expire: after 15 minutes, or when the guest lands on another page of the site (the shell reports each page through `@shared/routing`, so it imports no feature). Memory only, as S14. → `feat(data-reports): report wrong information`, `feat(favorites): save a space from its card`.
- **R3-F3** — the heart keeps one name, «حفظ {name} في المفضّلة», with `aria-pressed` (a departure from §9's two names). → `…save a space from its card`.
- **R3-F4** — `overview.md` names the report from a space's page. → `…report wrong information`.

Verified locally on `819e1eea`: lint, typecheck, `test:unit -w @masaha/web` (157 files, 1075 tests), `test:component -w @masaha/web` (300 files, 1744 tests), `check:links`, `check:classes`, `check:conflicts`, `format:check`. No API or shared change in this round; CI ran every lane green on `819e1eea`, `CLEAN`.

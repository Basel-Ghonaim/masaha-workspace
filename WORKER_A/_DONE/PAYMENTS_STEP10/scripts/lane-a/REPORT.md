# Lane A — report (saved by the lead from the sub-agent's reply; the harness refuses a sub-agent's report file)

## DONE (2026-10-28 ≈ 11:05)

- `lane/a` head `df4b8a88` (from `cf0dcb0c`): `fcc42f60 feat(announcements): list a space's announcements` (49) ·
  `8e64db2d feat(announcements): post and edit an announcement` (50) · `0ec5a23e feat(announcements): end, start or
  delete one` (45) · `df4b8a88 feat(announcements): extend after a closure` (43).
- Red per commit (new code moved aside by `aside.py`, restored by copy): c1 "Cannot find module
  './announcementsRepository'…", "Failed to resolve import './AnnouncementsList'…", routes "…AnnouncementsPage"
  (`red-c1.txt`) → unit 6 files/20 tests, component 3/13, routes describe 2/2; c2 (`red-c2.txt`) → unit 7/32,
  component 5/25; c3 (`red-c3.txt`) → unit 7/33, component 8/40; c4 (`red-c4.txt`) → unit 7/34, component 10/54.
- Breaks, all red (`break-<name>.txt`): #25 post's key dropped "expected undefined to be 'key-1'"; #25b edit by PUT;
  #25 end path; #25 extension key dropped "expected undefined to be 'key-2'"; #26 browser zone "expected '1 أكتوبر
  01:00–11:00' to be '1 أكتوبر 08:00–18:00'" (4 tests); #27 closure neutral (2); #28 tab not in address; #29 pages
  always drawn; #30 status badge (1440, 390); #31 browser zone "expected '2026-07-01T12:00:00.000Z' to be
  '2026-07-01T05:00:00.000Z'" (5); #32 renew on each submit; #33 field lines left out; #34 tab not named; #35 focus on
  the group; #36 «تراجع» on an extended closure; #37 delete on an extended closure; #38 one text for every state (3);
  #39 focus on body; #40 proposal sent "expected { days: 2 } to deeply equal { days: 3 }"; #41 closed on failure; #42
  action shown to reception; #43 count left out (5 Arabic forms); #44 placeholder kept.
- Heavy (final): lint 0 (10:53–10:55); typecheck 0 (10:55–10:56); `test:unit -w @masaha/web` "Test Files 149 passed
  (149) · Tests 1038 passed (1038)"; `test:component -w @masaha/web` "Test Files 1 failed | 273 passed (274) · Tests 1
  failed | 1620 passed (1621)" (10:56–11:03) — routes › "refuses reception the owner’s payments with the 403 inside the
  shell" ("Test timed out in 5000ms"; alone "Unable to find role="main""); with `cf0dcb0c`'s `routes.tsx` and test
  restored by backup, red too (`c1-routes-base-full.txt`, `c1-routes-base.txt`). Per commit: typecheck fixed before c2
  (generic `setValue`), c3 (the tabs ref's type), c4 (`invalid_type` no field code); lint fixed before c2; Prettier,
  `check:links`, `check:classes` 0 on every commit.
- Shared: `routes.tsx` (`SPACE_PAGES.announcements` first); routes test (one import, `describe("the space's
  announcements")` appended); copy index ×2 (`announcements` before `auth`); architecture §2 (a «الإعلانات» segment
  after #127's), §3 (S2), §7 (S12); overview (Announcements *Built*); foundation §13 screen 18; `subscriptions.md` (one
  *Who uses it* sentence); new `src/test/announcement.ts`.
- Decisions (none SERIOUS): LA-D1 #128's count — «شمل الإغلاق {n} اشتراكات.» → «يشمل التمديد {n} اشتراكات.» /
  "The extension moves {n} subscriptions.", and the line «هي التي شملها الإغلاق، وتجديداتها التي لم تبدأ بعد؛ يتأخر
  كلٌّ منها بعدد الأيام أدناه. لا يمكن التراجع، ولا التمديد مرة ثانية لهذا الإغلاق.» (six forms kept; DI-20's line in
  `announcements.md` says so); LA-D2 report as text; LA-D3 `SheetValues` time fields named `startsAt`/`endsAt`; LA-D4 an
  unchanged edit says «لم يتغيّر شيء» (info) and sends nothing; LA-D5 `sheet.close`; LA-D6 `announcementToasts.tsx` in
  c2; LA-D7 the focus keeper `hooks/list/useCardFocus.ts` in the component, last resort the tab shown; LA-D8 5.f, 5.g
  hold, 5.h by `onOpenAutoFocus` (break #35); LA-D9 `ExtensionAction.tsx` (not in §8), the card's next action takes the
  focus once it leaves; LA-D10 the days field focused at opening or `autoFocus` once the preview arrives; LA-D11
  «تراجع» calls `edit` directly then reads the space; LA-D12 end/start failure toasts `duration: Infinity`; LA-D13
  `useAnnouncementsFilters` its own test, `useDeleteDialog` takes `onDone`; LA-D14 an extended running closure keeps
  «تعديل»; LA-D15 test 29 updated in c4.
- Left: `AnnouncementItem`, `ClosureNotice` built, not exported; `public.title` unused until commit 6; the sheet
  preview's `ClosureNotice` is a polite status region (announced while typing) — the public page's semantics are
  commit 6's.

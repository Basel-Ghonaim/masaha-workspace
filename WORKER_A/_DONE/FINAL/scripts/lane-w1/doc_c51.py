p = r'C:\dev\masaha\app-lane-w1\docs\features\overview.md'
s = open(p, encoding='utf8', newline='').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)

rep("The API is built; no screen yet.", "The API is built; on the web, the owner's overview (screen 12).")
rep("> **Scope:** the API module `overview` (L5); `@masaha/shared/overview`.",
    "> **Scope:** the API module `overview` (L5); `@masaha/shared/overview`; the web feature `features/overview`, dashboard-only.")
rep("Reception has none and is refused (the owner's OV3). The owner's screen (12) is to come, worker A's.",
    "Reception has none and is refused (the owner's OV3). On the web, «نظرة عامة» at `/dashboard/spaces/:spaceId`, the owner's landing; reception gets the 403 there (2026-10-29, #PRNUM).")
rep("""## Decisions
""", """**The owner's screen** (`OwnerOverview`, screen 12). One read, never polled: read again each time the page opens, and on returning to the window once stale (OV7). In the top bar, the live status visitors see and its control, `occupancy`'s, as the desk's (P2). «يحتاج انتباهك» lists, in order, each fact group never saved («لم تُضف بعد»), each stale one with its days counted («قديمة»), the open reports, the uncollected visits, the unpriced ones, the customers who owe, the closures awaiting their extension — each a count above zero — and the capacity when it is not set; each row leads where it is acted on (the profile's section or Packages & prices' `#prices`, the reports `?status=open`, the desk `#uncollected` or `#unpriced`, Finance `?tab=debts`, the announcements, the settings `#attendance`), and nothing waiting reads «كل شيء على ما يرام». «الحاضرون الآن» shows the count over the capacity, with the meter only once a capacity is set, the subscribers and the visits counted, and what visitors see with its line. The announcements' tile counts the running ones and names their types. «اشتراكات تنتهي هذا الأسبوع» counts them, lists five — the name a link to the file, the subscription and when it ends («ينتهي اليوم», «ينتهي غدًا», «ينتهي بعد {n} يوم»), «تجديد» to the file — and «عرض الكل» leads to the customers `?status=ENDING_SOON`. Its states: three blocks while it loads; a failure, «تعذّر تحميل النظرة العامة» with «إعادة المحاولة»; offline, its own state.

## Decisions
""")
rep("""## Code map
""", """### Web decisions

- **No amount anywhere** (O3): the answer holds none, and a component test reads the whole screen for one. 2026-10-29, #PRNUM.
- **The unpriced visits have a row** (DI2), after the uncollected, to the desk's card of them; **«لم تُحصَّل» has no «اليوم»** (DI3): the count has no day. 2026-10-29, #PRNUM.
- **«الآن: {المشتركين} و{الزيارات}» only** (DI5): no field says who left today. 2026-10-29, #PRNUM.
- **The closures awaiting their extension are one counted row** (DI6) to the announcements page. 2026-10-29, #PRNUM.
- **«تجديد» opens the customer's file** (DI26), where the renewal is; no address opens the sheet. 2026-10-29, #PRNUM.
- **Every link is the page's** (architecture §3): `OwnerOverviewLinks`. 2026-10-29, #PRNUM.

## Code map
""")
rep("""- `packages/shared/src/overview/` — the answers.
""", """- `packages/shared/src/overview/` — the answers.
- `apps/web/src/features/overview/`, entry `index.ts` (`OwnerOverview`, `OwnerOverviewLinks`), read by `pages/dashboard/space/overview/OverviewPage.tsx`, which passes the links and sets `occupancy`'s `LiveStatusControl` in the top bar: the repository in `repository/`; the keys, the query and the view (`owner/`) and the failure's view (`useLoadFailure`) in `hooks/`; the work queue's rows (`attentionRows`) and an end's words (`endsText`) in `services/`; the screen and its cards (`owner/`) and the failure in `components/`. Words: the catalogue's `overview` section.
""")
rep("""- 2026-10-29, #131 — the owner's overview (`GET /manage/spaces/:spaceId/overview`) and the admin's (`GET /admin/overview`), with a set-based count added in each owning module.
""", """- 2026-10-29, #131 — the owner's overview (`GET /manage/spaces/:spaceId/overview`) and the admin's (`GET /admin/overview`), with a set-based count added in each owning module.

### Web history

- 2026-10-29, #PRNUM — the owner's overview (screen 12).
""")
open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')

p = r'C:\dev\masaha\app-lane-w1\docs\features\finance.md'
s = open(p, encoding='utf8', newline='').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)

rep("The API is built; no screen yet.", "The API is built; on the web, the owner's Finance (screen 19).")
rep("> **Scope:** the API module `finance` (L5); `@masaha/shared/finance`.",
    "> **Scope:** the API module `finance` (L5); `@masaha/shared/finance`; the web feature `features/finance`, dashboard-only.")
rep("The owner's Finance screen (19) is to come, on the web.",
    "On the web, «المالية والتقارير» at `/dashboard/spaces/:spaceId/finance`; reception gets the 403 there (2026-10-29, #PRNUM).")
rep("""## Decisions
""", """**The owner's screen** (`FinanceScreen`, screen 19). The tabs «الدخل», «الديون», «الإشغال» and, beside them from 1024 px, «الشهر»: the current Gaza month and the 23 before it, newest first, each «{month} {year}» with Western digits; the tab and the month are in the address (`?tab=`, `?month=`), the defaults never written and a month outside the 24 read as the current one. The month moves the month-bound blocks only; the charts keep their fixed windows, named. In the top bar, the export of the tab shown (in «⋯» on a phone), a CSV built in the browser and saved on the owner's device, then «نُزّل الملف» with its name.

**Income.** What income counts, in a line; three tiles — today, up to the time read; the month asked, with «+{n}% عن {الشهر السابق}» when the month before had income; all time, since its first month or «لا دفعات بعد»; «الدخل حسب الشهر» over the last 12 months (subscriptions and visits stacked) and «دخل الزيارات يوميًا» over the last 30 days, a tick under every fifth day back from today; and «التحصيل حسب الموظف», the month's collections per person — how many, the total, cash and transfer — a table from 768 px, a card each below it. Its export, `masaha-income-{YYYY-MM}.csv`: a row per month of the 12, the amounts in shekels with a dot. `useMonthCollections` hands a page this month's collections per person. Its states: blocks while it loads; a failure, «تعذّر تحميل المالية» with «إعادة المحاولة»; offline, its own state.

## Decisions
""")
rep("""## Code map
""", """### Web decisions

- **Finance's address is its tab and its month** (DI29), the defaults left out. 2026-10-29, #PRNUM.
- **The export is the browser's, from the figures read** (the owner's decision 5): no export route; the file is saved by the owner's own download. 2026-10-29, #PRNUM.
- **The month's change is a whole percentage, and none without a month before** (D5.3): no ratio of nothing. 2026-10-29, #PRNUM.
- **Every link is the page's** (architecture §3): `FinanceLinks`. 2026-10-29, #PRNUM.

## Code map
""")
rep("""- `packages/shared/src/finance/` — the queries (the month and its bound, the debts', the payers') and the answers.
""", """- `packages/shared/src/finance/` — the queries (the month and its bound, the debts', the payers') and the answers.
- `apps/web/src/features/finance/`, entry `index.ts` (`FinanceScreen`, `FinanceExport`, `FinanceLinks`, `useMonthCollections`), read by `pages/dashboard/space/finance/FinancePage.tsx`, which passes the links and the space's name and sets the export in the top bar: the repository (four reads) in `repository/`; the keys, the address (`useFinanceTabs`), the screen's view, the export and each tab's query and view (`income/`) in `hooks/`; the months, their words, the month's change and each CSV in `services/`; the screen, the month, the tabs' cards and the failure in `components/`. Words: the catalogue's `finance` section.
""")
rep("""- #131 — a month's income and the staff's collections; who owes and who is in credit, with the totals and the reminder template; who paid in a month; the occupancy statistics.
""", """- #131 — a month's income and the staff's collections; who owes and who is in credit, with the totals and the reminder template; who paid in a month; the occupancy statistics.

### Web history

- 2026-10-29, #PRNUM — Finance (screen 19): its tabs and month, and the income with its export.
""")
open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')

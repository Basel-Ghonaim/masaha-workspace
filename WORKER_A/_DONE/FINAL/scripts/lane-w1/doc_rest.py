import sys
D = r'C:\dev\masaha\app-lane-w1\docs'

def edit(path, pairs):
    s = open(path, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:70])
        s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)

FIN = D + r'\features\finance.md'
which = sys.argv[1]

if which == 'c54':
    edit(FIN, [
        ("""`useMonthCollections` hands a page this month's collections per person.""",
         """`useMonthCollections` hands a page this month's collections per person.

**Debts.** Four tiles — what is owed and by how many customers, the customers' credit, how many paid in the month, and the uncollected visits with what they owe, «لا تُجمع مع الديون», and the unpriced ones, a link to the desk's card — the two figures never added ([finding 193](../architecture/findings/193-a-visit-left-to-a-customer-is-both-a-debt-and-uncollected.md)); «عليهم مبالغ», the largest first, paged by 20 (`?page=`): the name a link to the file, «مؤرشف» when archived, since when and the oldest item, the amount, «تذكير على واتساب» when there is a phone — the space's reminder, else the catalogue's, filled with the first name, the amount and the space — and «استلام دفعة» to the file; «لهم رصيد», paged by 20 (`?credit=`); and five of who paid in the month, «عرض الكل» to the ledger over that month's days up to today. Its export, `masaha-debts-{YYYY-MM-DD}.csv`: every page of who owes, 50 at a time, read in turn; a failed page saves nothing and offers «إعادة المحاولة»."""),
        ("""- **Every link is the page's** (architecture §3): `FinanceLinks`. 2026-10-29, #PRNUM.
""", """- **Every link is the page's** (architecture §3): `FinanceLinks`. 2026-10-29, #PRNUM.
- **The uncollected visits are a fourth debts tile, never added to the debts** (DI9, 193 accepted). 2026-10-29, #PRNUM.
- **«استلام دفعة» opens the customer's file** (DI15), where «استلام {المبلغ}» is: finance stays a read. 2026-10-29, #PRNUM.
- **The reminder names the customer by the first word of their name** (DI28), as the prototype's. 2026-10-29, #PRNUM.
- **The debts' two lists keep their pages in the address,** `?page=` and `?credit=`, beside DI29's tab and month, since a list's pages are links (`shared/lists`); a list of one page shows no steps. 2026-10-29, #PRNUM.
"""),
        ("the screen's view, the export and each tab's query and view (`income/`) in `hooks/`;",
         "the screen's view, the export and each tab's queries and view (`income/`, `debts/`, with the debts' export) in `hooks/`;"),
        ("the months, their words, the month's change and each CSV in `services/`;",
         "the months, their words, the month's change, a date's words, the reminder and each CSV in `services/`;"),
        ("- 2026-10-29, #PRNUM — Finance (screen 19): its tabs and month, and the income with its export.\n",
         "- 2026-10-29, #PRNUM — Finance (screen 19): its tabs and month, and the income with its export; the debts, with the WhatsApp reminder and their export.\n"),
    ])
elif which == 'c55':
    edit(FIN, [
        ("""a failed page saves nothing and offers «إعادة المحاولة».""",
         """a failed page saves nothing and offers «إعادة المحاولة».

**Occupancy.** Three tiles of the month — the average stay as «{h}:{mm} س», with the members' and the visits'; the peak hour «{h}:00–{h+1}:00»; the average daily attendance, one decimal — «—» and «لا جلسات مغلقة في {الشهر}» with no closed stay; «ساعات الذروة», the average present per weekday and hour over the last 4 weeks, the weekdays in the language's week order and a weekday with no presence left out, the hours from the first to the last with any, scrolling sideways below 768 px, or «لا جلسات مغلقة في آخر 4 أسابيع»; and visits and members per day over the last 14 days. Its export, `masaha-occupancy-{YYYY-MM-DD}.csv`: a row per weekday with its 24 averages."""),
        ("""- **The debts' two lists keep their pages in the address,**""",
         """- **The heatmap shows only what has presence** (DI16): weekdays in the language's week order, one with none left out, and the hours from the first to the last with any; the prototype's 08–17 was its sample. 2026-10-29, #PRNUM.
- **The debts' two lists keep their pages in the address,**"""),
        ("(`income/`, `debts/`, with the debts' export) in `hooks/`;", "(`income/`, `debts/`, with the debts' export, `occupancy/`) in `hooks/`;"),
        ("a date's words, the reminder and each CSV in `services/`;", "a date's and a weekday's words, a stay's, the reminder and each CSV in `services/`;"),
        ("; the debts, with the WhatsApp reminder and their export.\n", "; the debts, with the WhatsApp reminder and their export; the occupancy.\n"),
    ])
elif which == 'c57':
    SS = D + r'\features\space-settings.md'
    edit(SS, [
        ("- **No «حسابي» card** (design issue 13). *Why:* it leads to `/me`, which is not built. 2026-10-20, #99.",
         "- **No «حسابي» card** (design issue 13). *Why:* it leads to `/me`, which is not built. 2026-10-20, #99. Superseded: the last card, «حسابي», leads to the personal settings, `/me` (D5.7, with the owner's approval in the plan). 2026-10-29, #PRNUM.\n- **The auto check-out's helper says where unpaid visits go, «غير محصّل», and the reminder's where it opens, the customer's file and Finance** (G24.2, G24.3). 2026-10-29, #PRNUM."),
        ("- #PRNUM — the reminder's preview fills it with the shared `fillReminder`, the one filler finance and the customer's file use too.\n",
         "- #PRNUM — the reminder's preview fills it with the shared `fillReminder`, the one filler finance and the customer's file use too.\n- 2026-10-29, #PRNUM — «حسابي», the settings' last card, to the personal settings; the auto check-out's and the reminder's lines say where things go.\n"),
    ])
elif which == 'c58':
    PK = D + r'\features\packages.md'
    edit(PK, [
        ("- **The section and the sheet say the packages are never shown to visitors, and nothing of the desk** (design issue 4). *Why:* the desk that will choose from them is not built; the switch is «متاحة». 2026-10-20, #98.",
         "- **The section and the sheet say the packages are never shown to visitors, and nothing of the desk** (design issue 4). *Why:* the desk that will choose from them is not built; the switch is «متاحة». 2026-10-20, #98. Superseded: the desk is built, so its five lines are back — the page's, that the week and month prices are chosen at the desk too; the section's, «لا تظهر للزوار · تُختار في المكتب عند إنشاء اشتراك»; the switch «متاحة في المكتب»; the sheet's; and the empty state's (D5.8, with the owner's approval in the plan). 2026-10-29, #PRNUM.\n- **A row's price sits at its end, beside its switch, in `label` weight** (G21.2), as the design's. 2026-10-29, #PRNUM."),
        ("- #124 — the side sheet full width on a phone (finding 101, the layer's); `useOfferedPackages` gives the desk's subscription sheet the offered packages.\n",
         "- #124 — the side sheet full width on a phone (finding 101, the layer's); `useOfferedPackages` gives the desk's subscription sheet the offered packages.\n- 2026-10-29, #PRNUM — the desk's words restored on Packages & prices; a row's price at its end.\n"),
    ])
elif which == 'c59':
    PK = D + r'\features\packages.md'
    edit(PK, [
        ("""## Open findings

- [102](../architecture/findings/102-the-package-sheets-summary-is-announced-on-every-keystroke.md): the sheet's summary is announced on every keystroke.

""", ""),
        ("- **A row's price sits at its end, beside its switch, in `label` weight** (G21.2), as the design's. 2026-10-29, #PRNUM.",
         "- **A row's price sits at its end, beside its switch, in `label` weight** (G21.2), as the design's. 2026-10-29, #PRNUM.\n- **The sheet's summary announces only its terms and its price, never the name typed** ([finding 102](../architecture/findings/102-the-package-sheets-summary-is-announced-on-every-keystroke.md), D5.9). *Why:* the owner hears what follows from what they type, not their own typing again. 2026-10-29, #PRNUM."),
        ("- 2026-10-29, #PRNUM — the desk's words restored on Packages & prices; a row's price at its end.\n",
         "- 2026-10-29, #PRNUM — the desk's words restored on Packages & prices; a row's price at its end.\n- 2026-10-29, #PRNUM — the sheet's summary announces its terms and price only (finding 102 resolved).\n"),
    ])
    F = D + r'\architecture\findings\102-the-package-sheets-summary-is-announced-on-every-keystroke.md'
    s = open(F, encoding='utf8', newline='').read()
    old = '**Status:** Open · **Date:** 2026-10-20'
    assert s.count(old) == 1
    s = s.replace(old, '**Status:** Resolved · **Date:** 2026-10-20 · **Resolved:** 2026-10-29')
    s = s.rstrip('\n') + '\n\n**Resolution (#PRNUM):** The live region holds only the terms and the price (D5.9).\n'
    open(F, 'w', encoding='utf8', newline='').write(s)
print('ok', which)

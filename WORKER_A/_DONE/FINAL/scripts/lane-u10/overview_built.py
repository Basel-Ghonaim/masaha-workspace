import sys
p = r'C:\dev\masaha\app-lane-u10\docs\project\overview.md'
s = open(p, encoding='utf8', newline='').read()
reps = [
 # Users: the account's settings
 ("each handover recorded, and a suspension or a role change that holds from the account's next request.\n",
  "each handover recorded, and a suspension or a role change that holds from the account's next request; on the site, one's own «إعدادات حسابي»: the name, the language saved to the account and the theme, and the ways of signing in, with the password change or a Google-only account's link to set one.\n"),
 # Spaces: reception has no space screen in v1's design
 (" on the managed routes, its prices a link to Packages & prices, where the owner edits and confirms them. Reception's web screens remain planned.\n",
  " on the managed routes, its prices a link to Packages & prices, where the owner edits and confirms them.\n"),
 # Space settings: the account card
 ("and the attendance card with the capacity.\n",
  "and the attendance card with the capacity, and «حسابي», leading to one's own settings.\n"),
 # Front desk: the log and the written-off visits
 ("on the dashboard, the desk: who is present, the live status and its override, a visit's check-in and check-out with its payment.\n",
  "on the dashboard, the desk: who is present, the live status and its override, a visit's check-in and check-out with its payment, a customer checked in as their visit; the uncollected and unpriced visits; «السجل», a day's visits and check-ins; the owner's «لن تُحصَّل», the written-off visits with their undo; and a renewal or a new subscription from a subscriber's card.\n"),
 # Customers: the corrections, the actions by state, the reminder (U8)
 ("on the dashboard, the customers list, a customer's file, and the subscription sheet: a new customer, a new subscription from a published price, a package or custom terms, and a renewal.\n",
  "on the dashboard, the customers list, a customer's file, and the subscription sheet: a new customer, a new subscription from a published price, a package or custom terms, and a renewal; a customer's actions by their state, in the list and the file; the file's WhatsApp reminder of a debt; and a subscription's corrections from its card: its name, dates and limits, and the owner's price.\n"),
 # Payments: the other owners in the staff filter (U8)
 ("on the dashboard, the owner's ledger with its filters and totals,",
  "on the dashboard, the owner's ledger with its filters and totals, its staff filter naming the space's other owners,"),
 # Audit
 ("paged, the last 30 days or all, searched by target and filtered by actor and action.\n",
  "paged, the last 30 days or all, searched by target and filtered by actor and action; on the dashboard, both «سجل التدقيق»: the owner's, in «الفريق والإعدادات», and the admin's.\n"),
 # Platform settings
 ("each read and saved on its own, and the contact as anyone reads it.\n",
  "each read and saved on its own, and the contact as anyone reads it; on the dashboard, the admin's «إعدادات المنصة», the three cards; on the site, the contact on About and in an unverified space's dialog.\n"),
 # Finance
 ("and the occupancy statistics — the owner's alone.\n",
  "and the occupancy statistics — the owner's alone; on the dashboard, the owner's «المالية والتقارير»: a month's income, who owes, with the WhatsApp reminder, and who paid, each exported as a CSV built in the browser, and the occupancy.\n"),
 # Overview
 ("the platform's tiles and the spaces with incomplete data.\n",
  "the platform's tiles and the spaces with incomplete data; on the dashboard, «نظرة عامة», the owner's landing and the admin's.\n"),
]
for a, b in reps:
    n = s.count(a)
    if n != 1:
        sys.exit('count %d: %s' % (n, a[:70]))
    s = s.replace(a, b)
open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')

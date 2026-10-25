"""Commit 4's documents: desk.md, subscriptions.md, spaces.md, overview.md."""
D = 'C:/dev/masaha/app/docs/'


def edit(path, pairs):
    p = D + path
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:80], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


WEB = """- **The renewal starts where its statement says** (K3, DK-007): «تجديد» on the file's latest subscription opens the sheet, which reads that subscription's statement — `renewal.startsOn`, never a start of the browser's — offers its package as one line with «تغيير الباقة», or repeats its custom terms, and sends `renewalOfId`; a subscription renewed meanwhile is said (`SUBSCRIPTION_ALREADY_RENEWED`) and the sheet makes a new subscription instead. 2026-10-26, #PRNUM.
- **The published week and month prices are sold first** (spec D, DI-51): under «منشورة للزوار», «أسبوعي» / «شهري» (with «· للطلاب» and the shift's name), each sent as `published: { period, audience, shiftId?, name }` — the name the line shows, in the desk's language — never a price's id; reception sells them, nothing being typed. A custom-labelled price is not offered. 2026-10-26, #PRNUM.
- **A published price is read afresh, and charged as the server says** ([finding 171](../architecture/findings/171-a-published-price-changed-between-the-desks-read-and-the-subscribe-is-charged-silently.md), the supervisor's decision for the owner to confirm): the sheet reads the space's prices again each time it opens, never showing an older read; the toast states the price the answer charged; a subscribe refused for the price (`invalid_choice` on `published`, or `PAYMENT_EXCEEDS_DUE`) says so, keeps every field and reads the prices again. *Why:* the API compares no amount; the finding stays open for that. 2026-10-26, #PRNUM.
"""

# desk.md: the three lines after commit 3's last web decision.
p = D + 'features/desk.md'
s = open(p, encoding='utf-8').read()
anchor = "both days counted, and never sent: the server sets it. 2026-10-26, #PRNUM.\n"
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + WEB)
old = ("customer's new one, from an offered package or «مخصّص», over their earlier debts, the parts "
       "said from the answer (finding 125).")
assert s.count(old) == 1
s = s.replace(old, ("customer's new one, from a published week or month price, an offered package or «مخصّص», "
                    "over their earlier debts, the parts said from the answer (finding 125); the renewal "
                    "from its statement's start."))
open(p, 'w', encoding='utf-8', newline='').write(s)

edit('features/subscriptions.md', [
    ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
    ("opens its statement and ends it early (`POST …/end`) (2026-10-25, #122).",
     "opens its statement and ends it early (`POST …/end`) (2026-10-25, #122); the subscription sheet "
     "subscribes (`POST …/customers/:customerId/subscriptions`) from a published price, a package or "
     "custom terms, and renews from the statement's `renewal` (2026-10-26, #PRNUM)."),
])

edit('features/spaces.md', [
    ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
    ("""- **[`packages`](packages.md),** whose writes take the space's lock first.
""", """- **[`packages`](packages.md),** whose writes take the space's lock first.
- **The desk's subscription sheet, on the web** ([desk](desk.md)): reads the space's shifts (`useSpaceShifts`) and its published prices, read again each time the sheet opens (`useSpacePrices`, finding 171) (2026-10-26, #PRNUM).
"""),
    ("`useSpaceName`, `useSpaceShifts`,", "`useSpaceName`, `useSpaceShifts`, `useSpacePrices`,"),
])
p = D + 'features/spaces.md'
s = open(p, encoding='utf-8').read().rstrip('\n')
s += "\n- #PRNUM — the space's published prices for the desk's subscription sheet, read again each time it opens (`useSpacePrices`).\n"
open(p, 'w', encoding='utf-8', newline='').write(s)

edit('project/overview.md', [
    ("and the check-ins listed ([subscriptions](../features/subscriptions.md), [payments](../features/payments.md)).",
     "and the check-ins listed ([subscriptions](../features/subscriptions.md), [payments](../features/payments.md)); "
     "on the dashboard, the customers list, a customer's file, and the subscription sheet: a new customer, a new "
     "subscription from a published price, a package or custom terms, and a renewal."),
])
print('ok')

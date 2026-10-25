import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'docs/api/api-contract.md'
rep(p, "subscribing and correcting a subscription's limits, dates and name are the staff's (🧾);",
    "subscribing, correcting a subscription's limits, dates and name, and ending it early are the staff's (🧾);")
rep(p, "`subscription.priceCorrected` (`before`: `{ billing, priceAgorot }`; `after`: the same with `reason`). A correction that changes nothing writes nothing.",
    "`subscription.priceCorrected` (`before`: `{ billing, priceAgorot }`; `after`: the same with `reason`); `subscription.ended` (`before`: `{ endsOn }`; `after`: `{ endsOn, endedAt }`). A correction that changes nothing, and a repeated end, write nothing.")
s = open(p, encoding='utf-8', newline='').read()
marker = "### Front desk (managed)"
i = s.index(marker)
s = s[:i] + """#### `POST /manage/spaces/:spaceId/subscriptions/:subscriptionId/end` · 🧾
- **No body.** Ends the subscription early («إنهاء الاشتراك»): its end becomes today — its start, if it has not started; never later than its end was — with who ended it and when. It is `EXPIRED` from then. No payment, refund or proration; what is owed stays owed, and an open check-in on it stays open.
- **200:** `SubscriptionState`; one already ended is answered as it is, writing nothing.
- **Errors**, each writing nothing: `forbidden` (403) for an owner or reception whose link ended meanwhile; `not_found` (404) for a subscription that is not the space's.

""" + s[i:]
open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'docs/architecture/data-model.md'
rep(p, "  - The desk can end any subscription early («إنهاء الاشتراك»): its end becomes today, and who ended it is recorded.",
    "  - The desk can end any subscription early («إنهاء الاشتراك»): its end becomes today — its start, if it has not started, and never later than it was (2026-10-22, #PRNUM) — and who ended it, and when, is recorded. Ending changes no money.")

p = 'docs/architecture/decisions/0009-space-scoped-reception-role.md'
rep(p, "owner and reception correct a subscription's limits, dates and name; the owner alone",
    "owner and reception correct a subscription's limits, dates and name, and end it early; the owner alone")
rep(p, "   | Correct a subscription's limits, dates and name | ✓ | ✓ |", "   | Correct a subscription's limits, dates and name; end it early | ✓ | ✓ |")

p = 'docs/backend/security.md'
rep(p, "subscribing a customer and correcting a subscription's limits, dates and name (`subscriptions.manage`, the staff's),",
    "subscribing a customer, correcting a subscription's limits, dates and name, and ending it early (`subscriptions.manage`, the staff's),")

p = 'docs/features/subscriptions.md'
rep(p, "- Corrects a subscription: its limits, dates and name, by the staff; its price and billing, by the owner, with a reason; each audited.",
    "- Corrects a subscription: its limits, dates and name, by the staff; its price and billing, by the owner, with a reason; each audited.\n- Ends a subscription early, by the staff: its end today (its start if it has not started), audited; no money changes.")
rep(p, "the corrections (`requireCan('subscriptions.manage')`;", "the corrections and the end (`requireCan('subscriptions.manage')`;")
rep(p, "**The renewal's start**", "**The end.** In its transaction, the same opening as a correction; one already ended is answered as it is; else its end becomes today — its start if it has not started, never later than it was — with who and when, audited `subscription.ended`. The status rule then answers `EXPIRED`.\n\n**The renewal's start**")
rep(p, "the corrections, the price the owner's.", "the corrections, the price the owner's; the end.")

p = 'docs/project/overview.md'
rep(p, "and a customer's file with their subscriptions' status and progress, their debt and their unpaid visits ([subscriptions](../features/subscriptions.md), [payments](../features/payments.md)).",
    "and a customer's file with their subscriptions' status and progress, their debt and their unpaid visits; their subscriptions made from a package or custom, renewed with a payment the server allocates oldest debt first, paid, read as a statement, corrected (the price the owner's) and ended early ([subscriptions](../features/subscriptions.md), [payments](../features/payments.md)).")

p = 'docs/plans/v1-mvp.md'
rep(p, "- **Built:** customers created, edited, archived and restored; the list and the file, debts in the database (#102).",
    "- **Built:** customers created, edited, archived and restored; the list and the file, debts in the database (#102); subscriptions made from a package or custom, renewed with a payment allocated oldest debt first, paid, read as a statement, corrected and ended early (#PRNUM).")
rep(p, "the archive and the restore (`POST …/customers/:customerId/archive`, `…/restore`) (#102) (",
    "the archive and the restore (`POST …/customers/:customerId/archive`, `…/restore`) (#102), and the subscriptions: subscribing and renewing (`POST …/customers/:customerId/subscriptions`), a subscription's payment (`POST …/payments`), its statement (`GET …/subscriptions/:id`), its corrections (`PATCH …/subscriptions/:id`, the owner's `PUT …/subscriptions/:id/price`) and its end (`POST …/subscriptions/:id/end`) (#PRNUM) ([Subscriptions (managed)](../api/api-contract.md#subscriptions-managed), ")
rep(p, "| GET / PATCH | `/manage/spaces/:spaceId/subscriptions/:id` | 🧾 | progress and statement; correct one |",
    "| GET / PATCH / PUT | `/manage/spaces/:spaceId/subscriptions/:id[/price]` | 🧾 · the price 🏢 | progress and statement; correct its limits, dates and name; the owner its price and billing, with a reason |")
rep(p, "| POST | `/manage/spaces/:spaceId/subscriptions/:id/end` | 🧾 | end early: the end becomes today |",
    "| POST | `/manage/spaces/:spaceId/subscriptions/:id/end` | 🧾 | end early: the end becomes today (its start, if it has not started) |")
print('ok')

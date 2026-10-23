import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'docs/api/api-contract.md'
rep(p, "bounded by one customer (§5, *Customers (managed)*; 2026-10-21, #102).\n",
    "bounded by one customer (§5, *Customers (managed)*; 2026-10-21, #102);\n- a subscription's check-ins and payments in its statement (`GET /manage/spaces/:spaceId/subscriptions/:subscriptionId`), bounded by one subscription (§5, *Subscriptions (managed)*; 2026-10-22, #PRNUM).\n")
rep(p, "A customer's subscriptions, at the desk: made from a package of the space or typed there ([data-model › Front desk and money](../architecture/data-model.md#front-desk-and-money)). The endpoints sit under `/manage/spaces/:spaceId` and answer as *Managed spaces* says: without an active `OWNER` or `RECEPTION` link at the live space, `not_found` (404). Subscribing is the staff's (🧾),",
    "A customer's subscriptions, at the desk: made from a package of the space or typed there ([data-model › Front desk and money](../architecture/data-model.md#front-desk-and-money)). The endpoints sit under `/manage/spaces/:spaceId` and answer as *Managed spaces* says: without an active `OWNER` or `RECEPTION` link at the live space, `not_found` (404). The statement is the staff's read; subscribing is the staff's (🧾),")
rep(p, """  debtAgorot: number                                                 // the customer's, as of the answer
}
```
""", """  debtAgorot: number                                                 // the customer's, as of the answer
}
SubscriptionStatement = SubscriptionState & { paidAgorot, balanceAgorot } & {
  customer: { id, name, phone: string | null },
  checkIns: { id, checkedInAt, checkedOutAt: string | null, checkoutMethod: "MANUAL" | "AUTO" | null,
              minutes: number | null }[],                            // a closed stay's whole minutes; the earliest first
  payments: ItemPayment[],                                           // voided ones marked; the earliest received first
  renewal: { startsOn: string } | null,                              // while not renewed: the start a renewal would take
  renewedById: number | null
}
```
""")
s = open(p, encoding='utf-8', newline='').read()
marker = "### Front desk (managed)"
i = s.index(marker)
s = s[:i] + """#### `GET /manage/spaces/:spaceId/subscriptions/:subscriptionId` · 🧾
- **200:** `SubscriptionStatement`: the subscription's state, what was paid and what it owes, its customer, every check-in with a closed stay's whole minutes (an open one's are `null`), every payment, voided ones marked, and, while no subscription renews it, the start a renewal would take (the day after its end while it is not expired and its end is not before today, else today); once renewed, `renewal` is `null` and `renewedById` names the renewal. Its lists are answered whole (§4). Read without a lock.
- **Errors:** `not_found` (404), also for a subscription that is not the space's.

""" + s[i:]
open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'docs/features/desk.md'
rep(p, "- Answers the customers list, paged, searched and filtered by their subscription and payment state, and a customer's file.",
    "- Answers the customers list, paged, searched and filtered by their subscription and payment state, a customer's file, and a subscription's statement.")
rep(p, "**The archive of a customer.**", "**A subscription's statement.** The subscription's state (404 when not the space's), with its money from `payments`' one query; its customer; its check-ins (`subscriptions`), each with a closed stay's whole minutes; its payments, voided ones marked (`payments`); and the renewal's proposed start (`proposedStart`) while `subscriptions` names no renewal, else who renewed it. Read without a lock.\n\n**The archive of a customer.**")
s = open(p, encoding='utf-8', newline='').read()
s = s.replace("a renewal with its payment allocated oldest debt first.", "a renewal with its payment allocated oldest debt first; a subscription's statement.")
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')

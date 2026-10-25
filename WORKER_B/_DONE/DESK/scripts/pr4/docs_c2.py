import io, os
os.chdir('C:/dev/masaha/app-b')
def edit(path, pairs):
    t = io.open(path, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:70], t.count(old))
        t = t.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(t)
def write(path, text):
    io.open(path, 'w', encoding='utf-8', newline='').write(text)

# --- api-contract
edit('docs/api/api-contract.md', [
("The desk's day: a visitor checked in by name, and checked out with the charge and its payment ([data-model › Front desk and money](../architecture/data-model.md#front-desk-and-money)).",
 "The desk's day: a visitor checked in by name, and checked out with the charge and its payment; once closed, what a visit still owes, which the owner may write off ([data-model › Front desk and money](../architecture/data-model.md#front-desk-and-money)), 2026-10-20, #PRNUM."),
("Every route is the staff's (🧾). Each write sends an `Idempotency-Key` (§1), read before its body; a retry with the same key answers the first result. Built 2026-10-20, #95.",
 "Every route is the staff's (🧾), except the write-off's, the owner's (🏢). The check-in and the check-out send an `Idempotency-Key` (§1), read before the body; a retry with the same key answers the first result. Built 2026-10-20, #95."),
("- **200:** a page of `UncollectedVisit` (`@masaha/shared/payments`): the space's visits closed by the auto check-out and not fully paid, the unpriced ones included,",
 "- **200:** a page of `UncollectedVisit` (`@masaha/shared/payments`): the space's visits closed by the auto check-out, not fully paid and not written off (2026-10-20, #PRNUM), the unpriced ones included,"),
("""  balanceAgorot: number | null    // what is still owed; null while it has no charge (unpriced)
}
```
""",
"""  balanceAgorot: number | null    // what is still owed; null while it has no charge (unpriced)
}
```

#### `POST /manage/spaces/:spaceId/visits/:visitId/write-off` · 🏢
- **Body** (`writeOffVisitSchema`, `@masaha/shared/visits`): `reason`, 1–200 characters, required.
- **200:** `DeskVisit`, its `writeOff` set: now, by the caller, with the reason. What the visit still owed is written off (K6); its payments stay, and the write-off is never a payment. A visit already written off is answered as it is, its first reason kept, writing nothing. Built 2026-10-20, #PRNUM.
- **Errors:** `forbidden` (403) for reception, at the route before the body is read, and for an owner whose link ended meanwhile; `validation` (422) on the body, before anything is read; `conflict` (409) `VISIT_NOT_PRICED` for a visit with no charge, `VISIT_ALREADY_PAID` for one with nothing owed, and no code for a visit still open (it is settled at its check-out); `not_found` (404), also for a visit that is not the space's.
- **Audit:** `visit.writtenOff` (`after`: `{ reason, balanceAgorot }`, the amount written off), in the change's own transaction.

#### `DELETE /manage/spaces/:spaceId/visits/:visitId/write-off` · 🏢
- **200:** `DeskVisit`, its `writeOff` cleared: it is uncollected again (or its customer's debt), and takes payments. A visit not written off is answered as it is, writing nothing. Built 2026-10-20, #PRNUM.
- **Errors:** `forbidden` (403) for reception, and for an owner whose link ended meanwhile; `not_found` (404), also for a visit that is not the space's.
- **Audit:** `visit.writeOffUndone` (`before`: `{ writtenOffAt, writtenOffById, reason }`), in the change's own transaction.
"""),
("`VISIT_NOT_PRICED` (a payment on a visit with no charge, from the ledger)",
 "`VISIT_NOT_PRICED` (a payment on, or a write-off of, a visit with no charge; the payment's from the ledger)"),
("`VISIT_ALREADY_PRICED` (pricing a visit that already has a charge).",
 "`VISIT_ALREADY_PRICED` (pricing a visit that already has a charge) · `VISIT_ALREADY_PAID` (writing off a visit with nothing owed, 2026-10-20, #PRNUM)."),
])

# --- data model
edit('docs/architecture/data-model.md', [
("- **Uncollected visits:** visits closed by the auto check-out and left unpaid, the unpriced ones included (2026-10-20, #97).",
 "- **Uncollected visits:** visits closed by the auto check-out, left unpaid and not written off, the unpriced ones included (2026-10-20, #97; #PRNUM).\n- **Written-off visit** (K6): the owner may write off what is still owed on a closed, priced visit, with a required reason, recorded with who and when. The payments made stay; it is never a payment and never a deletion. It can be undone, and the audit keeps both. A written-off visit takes no payment until then, and leaves the uncollected visits and the customer's debt (2026-10-20, #PRNUM)."),
("- **Customer debt:** the sum of the positive balances of the customer's subscriptions and unpaid visits.",
 "- **Customer debt:** the sum of the positive balances of the customer's subscriptions and unpaid visits not written off (2026-10-20, #PRNUM)."),
])

# --- conventions §9
edit('docs/backend/conventions.md', [
("- **check-out of a visit** with its charge and its payment;\n",
 "- **check-out of a visit** with its charge and its payment;\n- **the write-off of a visit's unpaid rest** by the owner, and its undo;\n"),
])

# --- security
edit('docs/backend/security.md', [
("and the desk's writes (`attendance.record`, the staff's), ask `can()` first,",
 "and the desk's writes (`attendance.record`, the staff's; a visit's write-off and its undo, `visits.writeOff`, the owner's, 2026-10-20, #PRNUM), ask `can()` first,"),
])

# --- ADR 0009
edit('docs/architecture/decisions/0009-space-scoped-reception-role.md', [
("   | Void a payment (with a reason) | – | ✓ |\n",
 "   | Void a payment (with a reason) | – | ✓ |\n   | Write off a visit's unpaid rest that will not be collected, with a reason; undo it | – | ✓ |\n"),
("> **Revised:** 2026-10-19 — rule 5: reception types a price by hand only where the space's settings allow it, off by default; every hand-typed price, the owner's included, carries a reason. #92\n",
 "> **Revised:** 2026-10-19 — rule 5: reception types a price by hand only where the space's settings allow it, off by default; every hand-typed price, the owner's included, carries a reason. #92\n> **Revised:** 2026-10-20 — rule 5: the owner alone writes off a visit's unpaid rest that will not be collected, with a reason, and may undo it (K6). #PRNUM\n"),
])

# --- desk.md
edit('docs/features/desk.md', [
("- Checks a visit out: the charge at the quote's time, the payment taken, the rest left unpaid to a customer found or created by phone, and a price typed by hand where the visit has no rate, or an unpriced close; a retry answers the first result.\n",
 "- Checks a visit out: the charge at the quote's time, the payment taken, the rest left unpaid to a customer found or created by phone, and a price typed by hand where the visit has no rate, or an unpriced close; a retry answers the first result.\n- Writes off, as the owner, what a closed, priced visit still owes, with a reason, and undoes it.\n"),
("No web screen yet; the shared desk device is not settled (who signs out an idle reception account, and switching staff on one device): step 9.",
 "No web screen yet; the shared desk device is not settled (who signs out an idle reception account, and switching staff on one device): the desk's screen item."),
("- Each write asks `can()` (`attendance.record`, the staff's) at the route, then reads its `Idempotency-Key`, both before the body is read; the service asks `can()` again under the space's lock.",
 "- Each write asks `can()` at the route, before the body is read: `attendance.record` (the staff's) for the check-in and the check-out, which then read their `Idempotency-Key`; `visits.writeOff` (the owner's) for the write-off and its undo. The service asks `can()` again under the space's lock."),
("The rows are taken in one order: the space's, the visit's, the customer, the payment.\n",
 "The rows are taken in one order: the space's, the visit's, the customer, the payment.\n\n**The write-off and its undo.** The owner's, each in one transaction, in this order: the space's lock and `can()` (`visits.writeOff`); the visit's row (`FOR UPDATE`), not the space's → 404, still open → 409 with no code. The write-off: a visit already written off is answered as it is; no charge → `VISIT_NOT_PRICED`; then what it was paid and still owes, read from [`payments`](payments.md) under the visit's lock; nothing owed → `VISIT_ALREADY_PAID`; else `visits` writes it off with the amount, now, by the caller, with the reason. The undo: a visit not written off is answered as it is; else `visits` clears it, audited with what it was.\n"),
("- **A check-out time before the visit's check-in is refused (`out_of_range`).** *Why:* the database refuses a visit closed before it opened, which would answer 500. 2026-10-20, #97.\n",
 "- **A check-out time before the visit's check-in is refused (`out_of_range`).** *Why:* the database refuses a visit closed before it opened, which would answer 500. 2026-10-20, #97.\n- **The write-off is a sub-resource: `POST` writes it off, `DELETE` undoes it; a second of either answers the visit as it is.** *Why:* a repeated write is idempotent by design, as a repeated check-out is, so it needs no key ([conventions §13](../backend/conventions.md#idempotency)); the first reason is kept. 2026-10-20, #PRNUM.\n- **The balance is read under the visit's lock, and nothing owed is refused (`VISIT_ALREADY_PAID`).** *Why:* two desks can collect the last part while the owner writes the visit off; the one that waits decides on what was committed. 2026-10-20, #PRNUM.\n- **An unpriced visit is refused with the payment's own code, `VISIT_NOT_PRICED`.** *Why:* one rule — a visit with no price is priced first — so one code (the owner's answer, Q2 of the plan). 2026-10-20, #PRNUM.\n"),
("- #97 — a payment on a visit another key closed refused; a check-out time before the check-in refused.",
 "- #97 — a payment on a visit another key closed refused; a check-out time before the check-in refused.\n- #PRNUM — the owner's write-off of a visit's unpaid rest, and its undo."),
])

# --- payments.md
edit('docs/features/payments.md', [
("- Answers a space's uncollected visits: closed by the auto check-out and not fully paid, with what was paid and what is still owed.",
 "- Answers a space's uncollected visits: closed by the auto check-out, not fully paid and not written off, with what was paid and what is still owed.\n- Answers what one visit was paid and still owes, in the desk's transaction (`balanceOfVisit`), for the write-off."),
("**The uncollected visits.** `visits` names the space's visits closed by the auto check-out, with their charges;",
 "**The uncollected visits.** `visits` names the space's visits closed by the auto check-out and not written off, with their charges;"),
])

# --- visits.md
edit('docs/features/visits.md', [
("- Lists a space's unpriced visits, and prices one by hand, with its reason, for whoever may type a price.\n",
 "- Lists a space's unpriced visits, and prices one by hand, with its reason, for whoever may type a price.\n- Writes a closed visit off, and undoes it, in the desk's transaction: audited `visit.writtenOff` and `visit.writeOffUndone`.\n"),
])

# --- finding 110
F = 'docs/architecture/findings/'
write(F + '110-the-desk-prototypes-uncollected-visits-disagree-with-the-owners-decisions.md', """# 110. The desk prototype's uncollected visits disagree with the owner's decisions

**Status:** Open · **Date:** 2026-10-20

**Evidence:** the desk prototype (`desk-core.jsx`, `desk-data.js` in the design archive) disagrees with the decisions the API builds (#PRNUM) in three places:
- its `WriteOffDialog` says the write-off cannot be undone; the owner made it reversible (K6);
- its `PayDialog` with `remainder="uncollected"` leaves a partial payment's rest uncollected with no phone; the owner requires a phone, so the rest is a customer's debt ([data model › Unpaid visit](../data-model.md#front-desk-and-money));
- its `unpaid` list holds visits checked out by hand and left unpaid («خرج بدون دفع»), which the contract keeps out of the uncollected visits: their rest is a customer's debt.

**Resolves when:** the desk's screen item builds the «غير محصّلة» tab and its dialogs to the contract, or the prototype is corrected first.
""")
edit(F + 'README.md', [
("- [100. An unpaid check-out moves a visit's customer to the phone's](100-an-unpaid-check-out-moves-a-visits-customer-to-the-phones.md)\n",
 "- [100. An unpaid check-out moves a visit's customer to the phone's](100-an-unpaid-check-out-moves-a-visits-customer-to-the-phones.md)\n- [110. The desk prototype's uncollected visits disagree with the owner's decisions](110-the-desk-prototypes-uncollected-visits-disagree-with-the-owners-decisions.md)\n"),
])
print('ok')

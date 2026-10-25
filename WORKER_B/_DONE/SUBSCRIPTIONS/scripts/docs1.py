import sys
def edit(p, pairs):
    s = open(p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a)
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='').write(s)

edit('docs/api/api-contract.md', [(
"- **200:** `CheckInCheckOut`: the check-in closed now, `MANUAL`, with what",
"- **200:** `CheckInCheckOut`: the check-in closed now, `MANUAL`; a stay past its due time ([data-model](../architecture/data-model.md#front-desk-and-money), *Auto check-out*) is closed at that due time, its `checkedOutAt`, and the audit keeps the request's own time (2026-10-24, #PRNUM). Answered with what",
)])
edit('docs/features/desk.md', [
("**Last Updated:** 2026-10-22", "**Last Updated:** 2026-10-24"),
("not the space's → 404; closed already → answered as it is; else closed now, `MANUAL`, audited by `subscriptions`.",
 "not the space's → 404; closed already → answered as it is; else closed now, but never past the stay's due time, by the space's week and settings read under its lock, `MANUAL`, audited by `subscriptions`."),
("([finding 116](../architecture/findings/116-a-desk-check-out-of-an-overdue-stay-is-charged-up-to-now.md)). 2026-10-21, #102.\n",
 "([finding 116](../architecture/findings/116-a-desk-check-out-of-an-overdue-stay-is-charged-up-to-now.md)). 2026-10-21, #102.\n"
 "- **A subscriber's stay checked out after its due time is closed at that due time too, by the one rule the visit's check-out uses (`spaces.stayEnd`); the audit keeps the request's own time.** *Why:* the subscriber's check-out closed at now, so an overnight stay counted every hour to the morning in the subscription's minutes and due, which no route corrects; one rule for both stays, so the two cannot drift (#109's review). 2026-10-24, #PRNUM.\n"),
("a subscriber's check-in, with its warnings, and check-out.\n",
 "a subscriber's check-in, with its warnings, and check-out.\n- #PRNUM — a subscriber's check-out after its due time closed at it.\n"),
])

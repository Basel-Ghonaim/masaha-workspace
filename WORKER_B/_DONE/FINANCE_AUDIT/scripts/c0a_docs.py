import io
import os

os.chdir(r'C:\dev\masaha\app-b')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:90])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


edit('docs/architecture/findings/README.md', [
('''- [125. The allocation's order is not exposed to the client](125-the-allocations-order-is-not-exposed-to-the-client.md)
''', '''- [125. The allocation's order is not exposed to the client](125-the-allocations-order-is-not-exposed-to-the-client.md)
- [151. A renewal sold before a closure's extension stays where it is](151-a-renewal-sold-before-a-closures-extension-stays-where-it-is.md)
'''),
])

edit('docs/api/api-contract.md', [
('**Last Updated:** 2026-10-26', '**Last Updated:** 2026-10-27'),
('''  subscriptions: number,           // how many it covered; once applied, how many it moved''',
 '''  subscriptions: number,           // how many it will move: those it covered and their renewals not started; once applied, how many it moved'''),
('''one running through it, one ending during it, one starting on its last day. One with no end is never covered.''',
 '''one running through it, one ending during it, one starting on its last day. One with no end is never covered.
- **Their renewals not started** ([finding 151](../architecture/findings/151-a-renewal-sold-before-a-closures-extension-stays-where-it-is.md)): each covered subscription's renewal whose start is after the Gaza date of the read and that was not ended early, then that renewal's own, and so on, moves with it. A renewal started, or with no start, is judged by the covered rule alone. 2026-10-27, #PRNUM.'''),
('''the closure's covered Gaza days, the days proposed and how many subscriptions it covered now;''',
 '''the closure's covered Gaza days, the days proposed and how many subscriptions it would move now, those it covered and their renewals not started (2026-10-27, #PRNUM);'''),
('''- **201:** `ClosureExtension`: every subscription the closure covered, as the preview counts them, has its end moved by `days`, in one transaction, with one link each; audited `closure.subscriptionsExtended` (the announcement the entity, its space the entry's; `after`: `{ days, subscriptionIds }`).''',
 '''- **201:** `ClosureExtension`: every subscription the closure covered has its end moved by `days`, and each of their renewals not started its start and end (2026-10-27, #PRNUM), as the preview counts them, in one transaction, with one link each; audited `closure.subscriptionsExtended` (the announcement the entity, its space the entry's; `after`: `{ days, subscriptionIds, renewalIds }`, the covered apart from the renewals).'''),
('''two owners at once make one (the space's lock, then the closure's, then the subscriptions' by id).''',
 '''two owners at once make one (the space's lock, then the closure's, then the subscriptions' by id, the renewals with the covered ones).'''),
])

edit('docs/architecture/data-model.md', [
('**Last Updated:** 2026-10-26', '**Last Updated:** 2026-10-27'),
('''**SubscriptionExtension** links it to each subscription it moved on; how many is the count of those links.''',
 '''**SubscriptionExtension** links it to each subscription it moved on, the covered ones and their renewals not started (2026-10-27, #PRNUM); how many is the count of those links.'''),
('''with an end on or after the closure's first covered day and a start, or none, on or before its last (decision 4, approved 2026-10-21; 2026-10-26, #123);''',
 '''with an end on or after the closure's first covered day and a start, or none, on or before its last (decision 4, approved 2026-10-21; 2026-10-26, #123); and by the same days the start and end of each of their renewals not started — a start after the extension's Gaza date, not ended early — a renewal's renewal too, so an end moved never runs into the renewal sold after it ([finding 151](findings/151-a-renewal-sold-before-a-closures-extension-stays-where-it-is.md), the owner's option A; 2026-10-27, #PRNUM);'''),
])

edit('docs/features/subscriptions.md', [
('**Last Updated:** 2026-10-26', '**Last Updated:** 2026-10-27'),
('''- Extends the subscriptions a closure covered, by the owner: a preview of the days it proposes and how many it covered, then every covered subscription's end moved by the days typed, once per closure, audited.''',
 '''- Extends the subscriptions a closure covered, by the owner: a preview of the days it proposes and how many it moves, then every covered subscription's end moved by the days typed, and each of their renewals not started, start and end, once per closure, audited.'''),
('''else its days, the proposal (at most 365) and how many it covers.''',
 '''else its days, the proposal (at most 365) and how many it moves. *The moved set* adds to the covered the chain of their renewals not started — a renewal of one, then of that renewal, whose start is after today's Gaza date and that was not ended early — read by one recursive query beside the fragment (`movedCount`, `lockMoved`).'''),
('''the covered subscriptions locked by id, their ends moved by the days in one statement; the extension and its links; the audit entry.''',
 '''the covered subscriptions and their renewals not started locked by id in one statement, the covered ones' ends moved by the days, the renewals' starts and ends; the extension and its links to both; the audit entry, the renewals named apart (`renewalIds`).'''),
('''- **The days proposed are the closure's Gaza days, at most 365;''',
 '''- **The extension also moves each covered subscription's renewals not started, start and end, by the same days** ([finding 151](../architecture/findings/151-a-renewal-sold-before-a-closures-extension-stays-where-it-is.md), the owner's option A, 2026-10-26): a renewal, then its own renewal, whose start is after today and that was not ended early; linked like the covered, counted by the preview, audited apart (`renewalIds`). *Why:* a renewal starts the day after the end it renews, so an end moved alone runs into it and the customer's days are lost; a renewal started runs on its own days, and the covered rule judges it. 2026-10-27, #PRNUM.
- **The days proposed are the closure's Gaza days, at most 365;'''),
('''- **The extension locks the space, then the closure, then the covered subscriptions by id**''',
 '''- **The extension locks the space, then the closure, then the covered subscriptions and their renewals not started, by id, in one statement**'''),
('''every subscription write takes the space's lock first, so the covered set is read as committed, and an edit of the closure waits. 2026-10-26, #123.''',
 '''every subscription write takes the space's lock first, so the covered set and its renewals are read as committed, and an edit of the closure waits. 2026-10-26, #123.'''),
('''- #118 — a subscription made from a published week or month price (through `desk`).
''', '''- #118 — a subscription made from a published week or month price (through `desk`).
- #PRNUM — a closure's extension moves the covered subscriptions' renewals not started too (finding 151).
'''),
])
print('ok')

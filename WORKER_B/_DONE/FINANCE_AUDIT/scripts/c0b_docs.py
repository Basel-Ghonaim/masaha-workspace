import io
import os

os.chdir(r'C:\dev\masaha\app-b')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:90])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


edit('docs/api/api-contract.md', [
('''`validation` (422) on `idempotencyKey` (§1), then on the body; `conflict` (409) for a key that extended another closure; `not_found` (404) for an announcement that is not the space's, not a `CLOSURE`, or deleted; `conflict` (409) `CLOSURE_ALREADY_EXTENDED`''',
 '''`validation` (422) on `idempotencyKey` (§1), then on the body; `conflict` (409) for a key that extended another closure, or a closure of another space, answering nothing of that extension (2026-10-27, #PRNUM); `not_found` (404) for an announcement that is not the space's, not a `CLOSURE`, or deleted; `conflict` (409) `CLOSURE_ALREADY_EXTENDED`'''),
])

edit('docs/features/subscriptions.md', [
('''the extension this key applied, for a retry (another closure's → `conflict`);''',
 '''the extension this key applied, for a retry (another closure's, or another space's, → `conflict`);'''),
('''so its key is unique alone, and a key that extended another closure is a conflict; a wrong one is corrected per subscription. 2026-10-26, #123.''',
 '''so its key is unique alone, and a key that extended another closure is a conflict; a wrong one is corrected per subscription. 2026-10-26, #123. A key that extended a closure of another space is the same conflict, checked before anything is answered, so the key tells nothing of that space (#123's review). 2026-10-27, #PRNUM.'''),
('''- #PRNUM — a closure's extension moves the covered subscriptions' renewals not started too (finding 151).''',
 '''- #PRNUM — a closure's extension moves the covered subscriptions' renewals not started too (finding 151); a key that extended another space's closure is a conflict.'''),
])
print('ok')

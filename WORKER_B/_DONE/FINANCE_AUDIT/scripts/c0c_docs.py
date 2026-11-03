import io
import os

os.chdir(r'C:\dev\masaha\app-b')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:90])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


edit('docs/architecture/data-model.md', [
('''an announcement, 2026-10-24, #112; a closure's extension, 2026-10-26, #123) carries the client's **idempotency key**''',
 '''an announcement, 2026-10-24, #112; a closure's extension, 2026-10-26, #123, whose key is unique on its own, as it has no space column — [Constraints worth stating](#constraints-worth-stating), 2026-10-27, #PRNUM) carries the client's **idempotency key**'''),
])

edit('docs/features/subscriptions.md', [
('''- #123 — a closure's extension: the preview, and the owner's extension of the subscriptions it covered, once per closure under one key.
- #118 — a subscription made from a published week or month price (through `desk`).
''', '''- #118 — a subscription made from a published week or month price (through `desk`).
- #123 — a closure's extension: the preview, and the owner's extension of the subscriptions it covered, once per closure under one key.
'''),
])
print('ok')

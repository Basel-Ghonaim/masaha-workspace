import io
import sys

R = 'C:/dev/masaha/app-b/'
D = '2026-10-26, #PRNUM'


def edit(path, pairs):
    p = R + path
    s = io.open(p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        n = s.count(a)
        if n != 1:
            sys.exit(f'{path}: {n}x {a[:70]!r}')
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


# 1. The contract
edit('docs/api/api-contract.md', [
    ("- **The list and its summary** show each closure's extension of the subscriptions it covered, which `subscriptions` owns: they are composed there ([conventions §9](../backend/conventions.md#composed-reads)), on the same path. Reads of the staff, asking no `can()`.",
     "- **The list and its summary** show each closure's extension of the subscriptions it covered, which `subscriptions` owns: they are composed there ([conventions §9](../backend/conventions.md#composed-reads)), on the same path. Reads of the staff, asking no `can()`. A closure's extension is `subscriptions`' too, on the same path: its preview the staff's, the extension itself the owner's (`subscriptions.extendAfterClosure`), once per closure, with no undo."),
    ("  applied: ExtensionApplied | null\n}\n```\n",
     "  applied: ExtensionApplied | null\n}\n\nClosureExtension = ExtensionApplied & { announcementId: number }\n```\n"),
    ("- **Errors:** `not_found` (404) for an announcement that is not the space's, not a `CLOSURE`, or deleted; `conflict` (409) `ANNOUNCEMENT_NOT_STARTED` for a closure not started yet.\n",
     "- **Errors:** `not_found` (404) for an announcement that is not the space's, not a `CLOSURE`, or deleted; `conflict` (409) `ANNOUNCEMENT_NOT_STARTED` for a closure not started yet.\n\n"
     "#### `POST /manage/spaces/:spaceId/announcements/:announcementId/extend-subscriptions` · 🏢 · `Idempotency-Key`\n"
     "- **Body:** `{ days }`, the days the owner types from the proposal: whole, 1–365 (`EXTENSION_MAX_DAYS`; `out_of_range` otherwise).\n"
     f"- **201:** `ClosureExtension`: every subscription the closure covered, as the preview counts them, has its end moved by `days`, in one transaction, with one link each; audited `closure.subscriptionsExtended` (the announcement the entity, its space the entry's; `after`: `{{ days, subscriptionIds }}`). A subscription's status and progress follow from its new end. A retry with the same key answers the first extension as it was, 201, moving nothing; two owners at once make one (the space's lock, then the closure's, then the subscriptions' by id). **No undo:** a wrong extension is corrected subscription by subscription (*Subscriptions (managed)*, the corrections). Once extended, the closure keeps its type, start and existence (`CLOSURE_EXTENDED` on its edit and delete). Built {D}.\n"
     "- **Errors**, each writing nothing: `forbidden` (403) for reception, before the key or the body is read, and for an owner whose link ended meanwhile; `validation` (422) on `idempotencyKey` (§1), then on the body; `conflict` (409) for a key that extended another closure; `not_found` (404) for an announcement that is not the space's, not a `CLOSURE`, or deleted; `conflict` (409) `CLOSURE_ALREADY_EXTENDED` for a closure extended already; `conflict` (409) `ANNOUNCEMENT_NOT_STARTED` for one not started yet.\n"),
    ("given a later end or none; from the database, 2026-10-26, #PRNUM) · ",
     f"given a later end or none; from the database, 2026-10-26, #PRNUM) · `CLOSURE_ALREADY_EXTENDED` (409: a closure's subscriptions extended already, under another key, {D}) · "),
])

# 2. The data model
edit('docs/architecture/data-model.md', [
    ("- **ClosureExtension** — the owner extended the space's active subscriptions after a closure: the closure announcement (at most one extension each), the days, who applied it and when.",
     "- **ClosureExtension** — the owner extended the subscriptions a closure covered, once it had started: the closure announcement (at most one extension each), the days, who applied it and when, and the client's idempotency key."),
    ("- a closure extension belongs to a `CLOSURE` announcement, and extends only that space's active subscriptions;\n",
     f"- a closure extension belongs to a started `CLOSURE` announcement of the space, and moves by its days the end of every subscription the closure covered: the space's, not ended early, with an end on or after the closure's first covered day and a start, or none, on or before its last (decision 4, approved 2026-10-21; {D}); the database holds the once (a unique key) and the closure's period afterwards (its trigger);\n"),
])

# 3. Conventions
edit('docs/backend/conventions.md', [
    ("  - announcements created, edited, started, ended and deleted (2026-10-24, #112);\n",
     f"  - announcements created, edited, started, ended and deleted (2026-10-24, #112); a closure's extension of the subscriptions it covered ({D});\n"),
    ("Subscriptions, their check-ins and closure extensions; the managed announcements list with each closure's extension, and its summary (§9);",
     "Subscriptions, their check-ins and closure extensions; the managed announcements list with each closure's extension, and its summary (§9); a closure's extension, previewed and applied;"),
    ("and a retried post must not make a second closure.\n",
     f"and a retried post must not make a second closure. A closure's extension has one since {D}, required and unique on its own (it has no space column): two tabs of the owner must not move the ends twice. It locks the space, then the closure, then the covered subscriptions by id.\n"),
])

# 4. Security
edit('docs/backend/security.md', [
    ("- **A suspension keeps the account's links:**",
     f"- **A closure's extension is its owner's** (`subscriptions.extendAfterClosure`): `requireCan` refuses reception before the key or the body is read, and the extension asks `can()` again on the links read under the space's lock, so an owner unlinked meanwhile is refused. Its preview is the staff's. {D}.\n- **A suspension keeps the account's links:**"),
])

# 5. ADR 0009
edit('docs/architecture/decisions/0009-space-scoped-reception-role.md', [
    ("   | Extend all active subscriptions after a closure | – | ✓ |",
     "   | Extend the subscriptions a closure covered, once it has started | – | ✓ |"),
    ("the owner alone corrects its price or billing, with a reason. #106\n",
     "the owner alone corrects its price or billing, with a reason. #106\n> **Revised:** 2026-10-26 — rule 5: the owner extends the subscriptions a closure covered (decision 4: running on any of its days), once it has started and once per closure, not \"all active subscriptions\". #PRNUM\n"),
])

# 6. The capabilities
edit('docs/features/subscriptions.md', [
    ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
    ("- Answers the space's managed announcements list, each closure with the extension of the subscriptions it covered, and its summary, composed with [`announcements`](announcements.md).\n",
     "- Answers the space's managed announcements list, each closure with the extension of the subscriptions it covered, and its summary, composed with [`announcements`](announcements.md).\n- Extends the subscriptions a closure covered, by the owner: a preview of the days it proposes and how many it covered, then every covered subscription's end moved by the days typed, once per closure, audited.\n"),
    ("- **The space's staff**, who read the managed announcements list and its summary through it.\n",
     "- **The space's staff**, who read the managed announcements list and its summary through it, and a closure's extension's preview; **the owner**, who extends a closure's subscriptions.\n"),
    ("- **Owns** the `subscriptions` and `check_ins` tables,",
     "- **Owns** the `subscriptions` and `check_ins` tables, the `closure_extensions` and `subscription_extensions` tables (a closure's extension and the subscriptions it moved),"),
    ("- The managed announcements list and its summary are its `closures` router, mounted at `/announcements` beside `announcements`' writes (S10, [conventions §9](../backend/conventions.md#composed-reads)).\n",
     "- The managed announcements list and its summary are its `closures` router, mounted at `/announcements` beside `announcements`' writes (S10, [conventions §9](../backend/conventions.md#composed-reads)); so is a closure's extension: its preview the staff's, its apply the owner's (`requireCan('subscriptions.extendAfterClosure')`), with the `Idempotency-Key`. It reads the closure through `announcements` (`closureIn`, and `lockClosure` under the space's lock) and its days through `closureSpan`.\n"),
    ("\n## Decisions\n\n### API decisions\n",
     "\n**A closure's extension** (`closures/`). *The covered subscriptions* are one SQL fragment both reads use: the space's, not ended early, with an end on or after the closure's first Gaza day and a start, or none, on or before its last (the days `closureSpan` answers, to today while it runs). *The preview*, read without a lock: the closure (a `CLOSURE` of the space, not deleted); one applied answers it with how many it moved; one not started yet is `ANNOUNCEMENT_NOT_STARTED`; else its days, the proposal (at most 365) and how many it covers. *The apply*, in one transaction: the space's lock and `can()` on the links under it; the extension this key applied, for a retry (another closure's → `conflict`); the closure, locked; one extended already → `CLOSURE_ALREADY_EXTENDED`; one not started → `ANNOUNCEMENT_NOT_STARTED`; the covered subscriptions locked by id, their ends moved by the days in one statement; the extension and its links; the audit entry. The next read derives each one's status from its new end.\n\n## Decisions\n\n### API decisions\n"),
    ("- **The summary counts a closure as awaiting its extension only for 30 days from its start** (the owner's Q6).",
     f"- **The extension moves every subscription the closure covered, by the days the owner types** (decisions 3 and 4, approved 2026-10-21): running on any of its days, even one that ended during it; never one ended early or with no end. *Why:* those are the days its subscribers lost; one fragment for the preview and the move, so the owner sees exactly what moves. {D}.\n"
     f"- **The days proposed are the closure's Gaza days, at most 365; an end at midnight covers the day before** (S4, S5). *Why:* «من الخميس 08:00 حتى السبت 00:00» is two days, not three; the owner may type other days, 1–365. {D}.\n"
     f"- **Once per closure, under one key unique on its own; no undo** (S11, decision 5). *Why:* a second extension would move the ends twice; the extension has no space column, so its key is unique alone, and a key that extended another closure is a conflict; a wrong one is corrected per subscription. {D}.\n"
     f"- **The extension locks the space, then the closure, then the covered subscriptions by id** ([conventions §13](../backend/conventions.md#13-idempotency-and-concurrency)). *Why:* one fixed order; every subscription write takes the space's lock first, so the covered set is read as committed, and an edit of the closure waits. {D}.\n"
     "- **The summary counts a closure as awaiting its extension only for 30 days from its start** (the owner's Q6)."),
    ("`closures/`, the managed announcements list and its summary.",
     "`closures/`, the managed announcements list and its summary, and a closure's extension."),
    ("- #112 — the managed announcements list, each closure with its extension, and its summary (`closures/`).\n",
     "- #112 — the managed announcements list, each closure with its extension, and its summary (`closures/`).\n- #PRNUM — a closure's extension: the preview, and the owner's extension of the subscriptions it covered, once per closure under one key.\n"),
])
edit('docs/features/announcements.md', [
    ("- **[`subscriptions`](subscriptions.md),** whose managed list and summary read its pages, its counts and its started closures.",
     "- **[`subscriptions`](subscriptions.md),** whose managed list and summary read its pages, its counts and its started closures, and whose closure extension reads a closure (`closureIn`), locks it (`lockClosure`) and its days (`closureSpan`)."),
    ("and the pure rules (`announcementState`, `period`, `announcementChange`).",
     "and the pure rules (`announcementState`, `period`, `announcementChange`, `closureSpan`)."),
])

# 7. The plan and the overview
edit('docs/plans/v1-mvp.md', [
    ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
    ("newest saved first or nearest first (#121, [api-contract › Favourites](../api/api-contract.md#favourites)). The screens remain planned.",
     "newest saved first or nearest first (#121, [api-contract › Favourites](../api/api-contract.md#favourites)); the closure extension, on the API: its preview, and the owner's extension of the subscriptions a closure covered, once per closure under one key, an extended closure guarded by the database (#PRNUM, [api-contract › Announcements (managed)](../api/api-contract.md#announcements-managed)). The screens remain planned."),
    ("| POST | `/manage/spaces/:spaceId/announcements/:id/extend-subscriptions` | 🏢 | closure notices only; once per closure |",
     "| GET / POST | `/manage/spaces/:spaceId/announcements/:id/extend-subscriptions` | 🧾 / 🏢 | closure notices only: the preview, the staff's; the extension of the subscriptions it covered, the owner's, once per closure (built, #PRNUM) |"),
])
edit('docs/project/overview.md', [
    ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
    ("a space's page's running and upcoming announcements; the closure warning at check-in.",
     "a space's page's running and upcoming announcements; the closure warning at check-in; after a closure, the owner's extension of the subscriptions it covered, previewed first, once per closure."),
    ("- Announcements, including a closure notice; after a closure, the owner extends all active subscriptions by the closure days.",
     "- Announcements, including a closure notice; after a closure, the owner extends the subscriptions it covered by the days typed."),
])
print('ok')

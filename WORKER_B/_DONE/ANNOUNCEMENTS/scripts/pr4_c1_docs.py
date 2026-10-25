import io, sys
R = 'C:/dev/masaha/app-b/'
def edit(path, pairs):
    p = R + path
    s = io.open(p, encoding='utf-8', newline='').read()
    for a, b in pairs:
        n = s.count(a)
        if n != 1:
            sys.exit(f'{path}: {n}x {a[:70]!r}')
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)

edit('docs/architecture/data-model.md', [
    ("**Last Updated:** 2026-10-25", "**Last Updated:** 2026-10-26"),
    ("(a check-in, a visit, a payment, a customer; an announcement, 2026-10-24, #112) carries",
     "(a check-in, a visit, a payment, a customer; an announcement, 2026-10-24, #112; a closure's extension, 2026-10-26, #PRNUM) carries"),
    ("(`schema` for spaces, prices and accounts, `front-desk`, `subscriptions`, `payments`, `dataReports`).",
     "(`schema` for spaces, prices and accounts, `front-desk`, `subscriptions`, `payments`, `dataReports`, `closureExtensions`)."),
    ("announcements, required, 2026-10-24, #112).\n",
     "announcements, required, 2026-10-24, #112). A closure extension's key is unique on its own, required: the extension has no space column (S11, 2026-10-26, #PRNUM).\n"),
    ("- Check-ins, visits, subscriptions, payments and audit-log entries are never deleted.\n",
     "- **An extended closure** (the trigger `announcements_guard_extended`, migration `closure_extension_key`): once a closure's subscriptions were extended, it keeps its type and its start, is never deleted, and its end only comes earlier, end now included; its text may change. A violation is `CLOSURE_EXTENDED`. The database owns the rule because `announcements` cannot read the extensions, `subscriptions`' table ([conventions §7](../backend/conventions.md#7-modules-and-levels)). 2026-10-26, #PRNUM.\n- Check-ins, visits, subscriptions, payments and audit-log entries are never deleted.\n"),
])
edit('docs/api/api-contract.md', [
    ("`not_found` (404) for an announcement that is not the space's, or deleted; `validation` (422) on the period.\n",
     "`not_found` (404) for an announcement that is not the space's, or deleted; `validation` (422) on the period; `conflict` (409) `CLOSURE_EXTENDED` for a closure whose subscriptions were extended, given a new type or start, a later end or no end — its text and an earlier end still change (from the database, 2026-10-26, #PRNUM).\n"),
    ("- **Errors**, each writing nothing: `forbidden` (403); `not_found` (404) for an announcement that is not the space's.\n",
     "- **Errors**, each writing nothing: `forbidden` (403); `not_found` (404) for an announcement that is not the space's; `conflict` (409) `CLOSURE_EXTENDED` for a closure whose subscriptions were extended (from the database, 2026-10-26, #PRNUM).\n"),
    ("(ending now an announcement that has not started, 2026-10-24, #112) · ",
     "(ending now an announcement that has not started, 2026-10-24, #112) · `CLOSURE_EXTENDED` (409: a closure whose subscriptions were extended, deleted, retyped, restarted, or given a later end or none; from the database, 2026-10-26, #PRNUM) · "),
])
edit('docs/backend/conventions.md', [
    ("- **Services do not repeat these rules.** They write,",
     "- **An extended closure is the database's too:** the trigger `announcements_guard_extended` keeps a closure whose subscriptions were extended from being deleted, retyped, restarted or ended later (`CLOSURE_EXTENDED`), since `announcements` cannot read the extensions (§7) ([data-model.md](../architecture/data-model.md#constraints-worth-stating)). 2026-10-26, #PRNUM.\n- **Services do not repeat these rules.** They write,"),
])
edit('docs/features/announcements.md', [
    ("**Last Updated:** 2026-10-24", "**Last Updated:** 2026-10-26"),
    ("and leaves every read and the live status.\n",
     "and leaves every read and the live status.\n\n**An extended closure.** Once its subscriptions were extended ([`subscriptions`](subscriptions.md)), an edit giving it a new type or start, a later end or no end, and its delete, are refused `CLOSURE_EXTENDED`, writing nothing; its text and an earlier end, end now included, change. The database's trigger refuses them ([data model › Constraints](../architecture/data-model.md#constraints-worth-stating)); this module asks nothing of the extensions.\n"),
    ("- **No title and no author on an announcement** (O9).",
     "- **An extended closure keeps its type, its start and its existence; its end only comes earlier** (decision 6, refined by S3, the owner's Q3), held by a trigger (S2), `CLOSURE_EXTENDED`. *Why:* the days were given for the closure as it was; `announcements` (L2) cannot read the extensions, and a check in the service would race with an extension; a running closure, once extended, must still be able to end. 2026-10-26, #PRNUM.\n- **No title and no author on an announcement** (O9)."),
    ("the running and upcoming ones a space's public page reads.\n",
     "the running and upcoming ones a space's public page reads.\n- 2026-10-26, #PRNUM — an extended closure guarded by the database (`CLOSURE_EXTENDED`).\n"),
])
print('ok')

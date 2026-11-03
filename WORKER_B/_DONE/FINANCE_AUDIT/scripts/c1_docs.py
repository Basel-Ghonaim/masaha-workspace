import io
import os

os.chdir(r'C:\dev\masaha\app-b')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:90])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


AUDIT_SECTION = '''### Audit log

The audit log's reader (`audit`, [conventions §6](../backend/conventions.md#6-audit)): a space's owner reads every entry of the space. Entries are never deleted ([data-model › Operations](../architecture/data-model.md#operations)). Built 2026-10-27, #PRNUM.

- **The period** (`period`): `LAST_30_DAYS`, the default — from the Gaza midnight 29 days before today, so today and the 29 days before it — or `ALL`; `invalid_choice` otherwise.
- **`q`:** 1–80 characters, NFC-normalised and trimmed, with no bidirectional or other control characters: the entries whose target's current name holds it, in either language, as the directory searches (Arabic folded, [data-model › Conventions](../architecture/data-model.md#conventions), *Search*).
- **`actions`:** a comma list of the actions the API writes (`AUDIT_ACTIONS`, `@masaha/shared/audit`), at most 30, a repeat counted once: `invalid_choice` for an unknown one, `too_long` past 30.
- **Every filter applies before the page is cut** (§4), so `totalRecords` counts what they keep. Newest first, then the higher id.
- **The actor:** `PERSON`, named, for anyone with a link of any state to the space — one whose link ended is still named; `MASAHA`, never named and with no id, for anyone with none: the admin; `SYSTEM` for the timed jobs.
- **The target:** its type and id, and its current name where it has one — a space's and a lookup's in both languages; a person's, a customer's, a subscription's, a package's; a visit's visitor, else its customer; a check-in's customer. A payment, an announcement and a data report have none: the client words them from `before` and `after`. `deleted` marks a deleted space or announcement; an archived customer is not deleted.
- **`before` and `after` as stored;** the writer never stores a secret ([security › Passwords](../backend/security.md#passwords)). `action` as stored: one written later and not yet on `AUDIT_ACTIONS` is still answered.

```ts
AuditActor = { kind: 'PERSON', id: number, name: string } | { kind: 'MASAHA' } | { kind: 'SYSTEM' }

AuditTarget = {
  type: AuditEntityType,            // space, user, governorate, area, amenity, dataReport, customer,
                                    // subscription, checkIn, visit, payment, package, announcement
  id: number | null,
  name: string | null,              // its current name; a space's or a lookup's English
  nameAr: string | null,            // a space's or a lookup's Arabic
  deleted: boolean                  // a deleted space or announcement
}

AuditEntry = {
  id: number,
  at: string,
  action: string,
  actor: AuditActor,
  target: AuditTarget,
  before: object | null,            // as stored
  after: object | null
}

AuditMeta = §4's meta & {
  actors: AuditActor[]              // the actors of the entries every filter but `actor` keeps, each once,
}                                   // at most 50: persons by name, then MASAHA, then SYSTEM
```

#### `GET /manage/spaces/:spaceId/audit-log` · 🏢
- **Query:** `period`, `q`, `actions`, `actor` — a person's id, `MASAHA` or `SYSTEM` (`invalid_format`; `out_of_range` for an id below 1 or past the largest) — and §4's `page` and `limit`.
- **200:** `AuditEntry[]`, the space's entries the filters keep, with `AuditMeta`. `actor=<id>` keeps a person linked to the space only, so an admin's id finds nothing; the admin's entries are `actor=MASAHA`.
- **Errors:** `forbidden` (403) for reception, before the query is read; `validation` (422) on the query; `not_found` (404) for anyone who is not the space's staff, the admin included (the boundary).

### Internal
'''

edit('docs/api/api-contract.md', [
('''- **Errors:** `unauthorized` (401) without a signed-in user; `not_found` (404) for a malformed id.

### Internal
''', '''- **Errors:** `unauthorized` (401) without a signed-in user; `not_found` (404) for a malformed id.

''' + AUDIT_SECTION),
])

edit('docs/backend/conventions.md', [
('**Last Updated:** 2026-10-26', '**Last Updated:** 2026-10-27'),
('''the scheduler port (§12), with the auto check-out of `visits` and `subscriptions`. **Not yet built:** `optionalAuth` (§7); the audit reader (§6); every other module''',
 '''the scheduler port (§12), with the auto check-out of `visits` and `subscriptions`; the audit reader's owner's log (§6, 2026-10-27, #PRNUM). **Not yet built:** `optionalAuth` (§7); the audit reader's admin's log (§6); every other module'''),
('''- **Reading is a module**, `audit` (L5, §7). It owns no table and has a `manage` and an `admin` router.''',
 '''- **Reading is a module**, `audit` (L5, §7), a read model (R7): it reads the audit table with its actors' and targets' current names in its own queries, owns no table and writes nothing. It has a `manage` router, the owner's log of the space (2026-10-27, #PRNUM), and an `admin` router ([features/audit.md](../features/audit.md)).'''),
('''An event type not on the list stays hidden from the admin. The owner sees their space's entries.''',
 '''An event type not on the list stays hidden from the admin. The owner sees every entry of their space; an actor with no link of any state to it — the admin — is shown as `MASAHA`, never named, and the owner's actor filter never names one (2026-10-27, #PRNUM).'''),
('''- The owner's audit screen is in v1 scope ([overview.md](../project/overview.md)) but has no design yet ([finding 14](../architecture/findings/14-the-owners-audit-screen-has-no-design.md)).''',
 '''- The owner's audit screen is in v1 scope ([overview.md](../project/overview.md)) and designed (O13, `Owner audit.html`); its screen is not built yet ([finding 14](../architecture/findings/14-the-owners-audit-screen-has-no-design.md)).'''),
('''| `audit` | L5 | — (reads the audit table) | manage, admin | The audit reader (§6) |''',
 '''| [`audit`](../features/audit.md) | L5 | — (reads the audit table) | manage, admin | The audit reader (§6): the owner's log of the space |'''),
])

edit('docs/backend/security.md', [
('''- **A closure's extension is its owner's** (`subscriptions.extendAfterClosure`)''',
 '''- **A space's audit log is its owner's** (`space.auditLog.read`): `requireCan` refuses reception before the query is read; the admin, who has no link to a space, is refused by the boundary like any stranger. In the log, the admin is `MASAHA`, never named (2026-10-27, #PRNUM).
- **A closure's extension is its owner's** (`subscriptions.extendAfterClosure`)'''),
])

edit('docs/architecture/data-model.md', [
('''- **AuditLog** — who did what to which entity, with before and after, optionally scoped to a space. The actor is null for system actions such as auto check-out. Never deleted.''',
 '''- **AuditLog** — who did what to which entity, with before and after, optionally scoped to a space. The actor is null for system actions such as auto check-out. Never deleted: kept for ever in v1, with no retention job (the owner's decision 10, 2026-10-27, #PRNUM).'''),
])
print('ok')

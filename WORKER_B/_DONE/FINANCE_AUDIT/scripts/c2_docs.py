import io
import os

os.chdir(r'C:\dev\masaha\app-b')


def edit(path, reps):
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:90])
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


F152 = '152-audit-entries-kept-for-ever-meet-the-databases-05-gb.md'

edit('docs/architecture/findings/README.md', [
('''- [138. A failed refresh keeps a status that still reads live](138-a-failed-refresh-keeps-a-status-that-still-reads-live.md)
''', '''- [138. A failed refresh keeps a status that still reads live](138-a-failed-refresh-keeps-a-status-that-still-reads-live.md)
- [152. Audit entries kept for ever meet the database's 0.5 GB](''' + F152 + ''')
'''),
])

edit('docs/api/api-contract.md', [
('''The audit log's reader (`audit`, [conventions §6](../backend/conventions.md#6-audit)): a space's owner reads every entry of the space. Entries are never deleted''',
 '''The audit log's reader (`audit`, [conventions §6](../backend/conventions.md#6-audit)): a space's owner reads every entry of the space; the admin reads the platform's events only, of every space and of none, by a default-deny list (conventions §6). Entries are never deleted'''),
('''AuditMeta = §4's meta & {''', '''PlatformAuditEntry = AuditEntry & {   // the admin's: the actor always a PERSON (or SYSTEM)
  space: { id: number, nameEn: string, nameAr: string | null, deleted: boolean } | null   // the space it names
}

AuditMeta = §4's meta & {'''),
('''- **Errors:** `forbidden` (403) for reception, before the query is read; `validation` (422) on the query; `not_found` (404) for anyone who is not the space's staff, the admin included (the boundary).
''', '''- **Errors:** `forbidden` (403) for reception, before the query is read; `validation` (422) on the query; `not_found` (404) for anyone who is not the space's staff, the admin included (the boundary).

#### `GET /admin/audit-log` · 🛡
- **Query:** `period`, `q`, `actions`, `actor` — a person's id (`invalid_format`, `out_of_range`) — and §4's `page` and `limit`. `q` also finds every entry of a space by the space's names.
- **200:** `PlatformAuditEntry[]`, with `AuditMeta`: only the platform's events — the spaces' public facts and their confirmations, their photos, their creation, hiding, deletion and restoring, and their owners linked and unlinked, whoever acted; the lookups; the data reports' decisions; an account's creation, role, suspension, temporary passwords and email, only when the entry names no space. **Never** an entry about a space's customers, subscriptions, check-ins, visits, payments, packages, announcements or closure extensions, its capacity, its live-status override, its settings or its staff, an owner's reception account's included; an action on no list is never answered ([conventions §6](../backend/conventions.md#6-audit), [ADR 0002](../architecture/decisions/0002-authorization-model.md)).
- **Errors:** `unauthorized` (401), `forbidden` (403), and `forbidden` (403) `PASSWORD_CHANGE_REQUIRED`, by `/admin`'s guard; `validation` (422) on the query.
'''),
])

edit('docs/backend/conventions.md', [
('''; the audit reader's owner's log (§6, 2026-10-27, #PRNUM). **Not yet built:** `optionalAuth` (§7); the audit reader's admin's log (§6); every other module''',
 '''; the audit reader (§6): the owner's log and the admin's (2026-10-27, #PRNUM). **Not yet built:** `optionalAuth` (§7); every other module'''),
('''It has a `manage` router, the owner's log of the space (2026-10-27, #PRNUM), and an `admin` router ([features/audit.md](../features/audit.md)).''',
 '''It has a `manage` router, the owner's log of the space, and an `admin` router, the platform's events (2026-10-27, #PRNUM; [features/audit.md](../features/audit.md)).
- **Entries are kept for ever in v1** (the owner's decision 10): no retention job; what that costs is [finding 152](../architecture/findings/152-audit-entries-kept-for-ever-meet-the-databases-05-gb.md).'''),
('''- **Privacy is a default-deny allowlist.** The admin sees only the platform event types on the audit module's list, never an entry''',
 '''- **Privacy is a default-deny allowlist.** The admin sees only the platform event types on the audit module's list (`audit/platformEvents.ts`, one list the SQL is built from: the spaces' public facts and existence, their owners, the lookups, the reports' decisions; an account's events only when the entry names no space, since an owner's staff account's name the space and are the space's; 2026-10-27, #PRNUM), never an entry'''),
('''| The audit reader (§6): the owner's log of the space |''',
 '''| The audit reader (§6): the owner's log of the space, the admin's of the platform's events |'''),
])

edit('docs/backend/security.md', [
('''- **A closure's extension is its owner's** (`subscriptions.extendAfterClosure`)''',
 '''- **The admin's audit log is the platform's events only** (`/admin/audit-log`, behind `/admin`'s guard): a default-deny list ([conventions §6](conventions.md#6-audit)) — never an entry about a space's customers, subscriptions, check-ins, visits, payments, packages, announcements or extensions, its capacity, its override, its settings or its staff (2026-10-27, #PRNUM).
- **A closure's extension is its owner's** (`subscriptions.extendAfterClosure`)'''),
])

edit('docs/architecture/data-model.md', [
('''Never deleted: kept for ever in v1, with no retention job (the owner's decision 10, 2026-10-27, #PRNUM).''',
 '''Never deleted: kept for ever in v1, with no retention job (the owner's decision 10, 2026-10-27, #PRNUM); its cost against the database's size is [finding 152](findings/''' + F152 + ''').'''),
])

edit('docs/features/audit.md', [
('''- Filters a log by its period''', '''- Pages the platform's events for the admin, of every space and of none, by a default-deny list: never a space's operations, money, people, settings or staff; each entry with the space it names.
- Filters a log by its period'''),
('''- **The space's owner,** under `/manage/spaces/:spaceId/audit-log`. Reception is refused. The owner's screen is designed (O13) but not built ([finding 14](../architecture/findings/14-the-owners-audit-screen-has-no-design.md)).''',
 '''- **The space's owner,** under `/manage/spaces/:spaceId/audit-log`. Reception is refused. The owner's screen is designed (O13) but not built ([finding 14](../architecture/findings/14-the-owners-audit-screen-has-no-design.md)).
- **The admin,** under `/admin/audit-log`. The admin's screen (31) is not built.'''),
('''- **Owns** no table: it reads `audit_logs`, which `shared/audit` alone writes, append-only; it writes nothing.''',
 '''- **Owns** no table: it reads `audit_logs`, which `shared/audit` alone writes, append-only; it writes nothing. It owns the admin's list of the platform's events (`platformEvents.ts`).'''),
('''- **Leaves** who may read to `can()` (`space.auditLog.read`, [security › Authorization](../backend/security.md#authorization)) and the boundary of `/manage/spaces/:spaceId`;''',
 '''- **Leaves** who may read to `can()` (`space.auditLog.read`, [security › Authorization](../backend/security.md#authorization)), the boundary of `/manage/spaces/:spaceId` and `/admin`'s guard;'''),
('''its route asks `requireCan('space.auditLog.read')` before the query is read.''',
 '''its route asks `requireCan('space.auditLog.read')` before the query is read. Its admin router sits at `/audit-log` inside `/admin`, behind its one guard.'''),
('''`q` is matched against both names through `masaha_search_text`, in the same statement, before the page is cut ([data-model › Conventions](../architecture/data-model.md#conventions), *Search*).''',
 '''`q` is matched against both names through `masaha_search_text`, in the same statement, before the page is cut ([data-model › Conventions](../architecture/data-model.md#conventions), *Search*).

**The admin's log.** The same three statements, scoped by the platform's list instead of a space: an action on `PLATFORM_ACTIONS`, whatever space it names, or on `PLATFORM_ACCOUNT_ACTIONS` with no space; the SQL is built from the same two arrays as the pure `isPlatformEvent`, so the rule and its test cannot drift. Each entry carries the space it names, a deleted one marked, and `q` matches that space's names too. The actor is a person, named, or `SYSTEM`; `actor` is a person's id.'''),
('''- **The period is the last 30 days or all time, no free range**''',
 '''- **The admin's log is a default-deny list of the platform's events** (S5, the owner's decision 9, §13 Q7). *Why:* ADR 0002 and 0009 keep a space's operations, money, capacity, settings and staff from the admin, while its public facts, existence, owners and moderation are the platform's; a list of what may be shown hides every action added later until it is listed. 2026-10-27, #PRNUM.
- **An account's event is the platform's only when it names no space** (S5). *Why:* an owner's staff account's temporary password names the space and is the space's; the admin's own accounts' name none. 2026-10-27, #PRNUM.
- **Kept for ever** (the owner's decision 10). *Why:* v1 has no retention rule; [finding 152](../architecture/findings/152-audit-entries-kept-for-ever-meet-the-databases-05-gb.md) records the cost. 2026-10-27, #PRNUM.
- **The period is the last 30 days or all time, no free range**'''),
('''- `apps/api/src/modules/audit/` — the module: its service, its repository (the queries), its mapper, the period (`auditPeriod.ts`) and its manage router.''',
 '''- `apps/api/src/modules/audit/` — the module: its service, its repository (the queries), its mapper, the period (`auditPeriod.ts`), the admin's list (`platformEvents.ts`) and its manage and admin routers.'''),
('''- [14. The owner's audit screen has no design](../architecture/findings/14-the-owners-audit-screen-has-no-design.md)
''', '''- [14. The owner's audit screen has no design](../architecture/findings/14-the-owners-audit-screen-has-no-design.md)
- [152. Audit entries kept for ever meet the database's 0.5 GB](../architecture/findings/152-audit-entries-kept-for-ever-meet-the-databases-05-gb.md)
'''),
('''- #PRNUM — the owner's audit log of the space, the admin shown as Masaha; paged, the last 30 days or all, searched by target, filtered by actor and action.''',
 '''- #PRNUM — the owner's audit log of the space, the admin shown as Masaha, and the admin's log of the platform's events, by a default-deny list; paged, the last 30 days or all, searched by target, filtered by actor and action.'''),
])

edit('docs/plans/v1-mvp.md', [
('**Last Updated:** 2026-10-26', '**Last Updated:** 2026-10-27'),
('''- **Settles:** charts and CSV exports.
''', '''- **Settles:** charts and CSV exports.
- **Built:** the audit reader, on the API: the owner's log of the space, the admin shown as Masaha, and the admin's log of the platform's events, by a default-deny list (2026-10-27, #PRNUM).
'''),
('''| GET | `/manage/spaces/:spaceId/audit-log` | 🏢 | |''',
 '''| GET | `/manage/spaces/:spaceId/audit-log` | 🏢 | every entry of the space, the admin as Masaha; paged, the last 30 days or all, searched and filtered (built, #PRNUM) |'''),
('''| GET | `/admin/audit-log` | |''',
 '''| GET | `/admin/audit-log` | the platform's events only, by a default-deny list (built, #PRNUM) |'''),
])

edit('docs/project/overview.md', [
('**Last Updated:** 2026-10-26', '**Last Updated:** 2026-10-27'),
('''- [Occupancy](../features/occupancy.md):''', '''- [Audit](../features/audit.md): on the API, the owner's audit log of the space, the admin shown as Masaha, and the admin's log of the platform's events only; paged, the last 30 days or all, searched by target and filtered by actor and action.
- [Occupancy](../features/occupancy.md):'''),
])

edit('docs/README.md', [
('''- [desk.md](features/desk.md)''', '''- [audit.md](features/audit.md) — the audit logs' reader: the owner's log of the space, the admin shown as Masaha, and the admin's log of the platform's events by a default-deny list (API only).
- [desk.md](features/desk.md)'''),
])
print('ok')

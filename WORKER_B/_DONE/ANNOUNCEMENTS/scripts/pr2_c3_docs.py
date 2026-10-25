import io, os
os.chdir(r'C:\dev\masaha\app-b')

def edit(p, pairs):
    s = io.open(p, encoding='utf-8', newline='').read()
    for o, n in pairs:
        assert s.count(o) == 1, (p, o)
        s = s.replace(o, n)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)

edit('docs/backend/security.md', [
("the customers' writes and the subscriptions';", "the customers' writes and the subscriptions', and the data reports' owner routes (2026-10-25, #PRNUM);"),
("""- **A suspension keeps the account's links:**""", """- **A space's data reports are its owner's** (`space.dataReports.read` to list them, `dataReports.resolve` to decide one): `requireCan` refuses reception before the query or the body is read, and the decision asks `can()` again on the links read under the space's lock, so an owner unlinked meanwhile is refused. The owner never sees who reported: the list's query selects no reporter. 2026-10-25, #PRNUM.
- **A suspension keeps the account's links:**"""),
])

edit('docs/api/api-contract.md', [
("""- **The limit:** 10 reports an hour per user, counted before the body is read, a repeat and an invalid body included""", """- **Deciding:** a report is resolved, with a reply or none, or dismissed, with a reply required (`required` on `note`), by the space's owner, or by the admin while the space is unverified ([security › Authorization](../backend/security.md#authorization)). A decided report is final: another decision is `conflict` (409) `REPORT_ALREADY_DECIDED`; the same decision again — the same status, the same reply, by the same person — answers the report as it is, 200, writing nothing. Resolving never edits the space.
- **Audit**, in the decision's own transaction ([conventions §6](../backend/conventions.md#6-audit)), with the report as the entity and its space as the entry's: `dataReport.resolved` and `dataReport.dismissed` (`after`: `{ note }`). A report itself is not audited.
- **The limit:** 10 reports an hour per user, counted before the body is read, a repeat and an invalid body included"""),
("""so the screen shows its name as text. Built 2026-10-25, #PRNUM.
""", """so the screen shows its name as text. Built 2026-10-25, #PRNUM.

#### `GET /manage/spaces/:spaceId/data-reports` · 🏢
- Under `/manage/spaces/:spaceId`, as *Managed spaces* says: without an active link at the live space, `not_found` (404); reception is `forbidden` (403) before the query is read.
- **Query:** `status` (`OPEN` or `DECIDED`; all when absent), `field` (one of the six) and §4's `page` and `limit`; `invalid_choice` otherwise.
- **200:** `SpaceReport[]`, the space's own, newest first, then id, with §4's `meta`. **Never who reported:** no name, id or email anywhere in the answer. Built 2026-10-25, #PRNUM.

#### `PATCH /manage/spaces/:spaceId/data-reports/:reportId` · 🏢
- **Body:** `{ status: 'RESOLVED' | 'DISMISSED', note? }`.
- **200:** `SpaceReport`, decided now with `repliedBy: 'SPACE'`; the same decision again answers it as it is.
- **Errors**, each writing nothing: `forbidden` (403) for reception, before the body is read; `validation` (422) on the body; `not_found` (404) for a report that is not the space's; `forbidden` (403) for an owner whose link ended while the decision waited; `conflict` (409) `REPORT_ALREADY_DECIDED`. Built 2026-10-25, #PRNUM.
"""),
])

edit('docs/features/data-reports.md', [
("""- Pages the user's own reports, newest first, open or decided, each with its decision and who replied, and whether its space is still listed.
""", """- Pages the user's own reports, newest first, open or decided, each with its decision and who replied, and whether its space is still listed.
- Pages a space's reports for its owner, by status and field, never showing who reported; lets the owner resolve one, with a reply or none, or dismiss it with a reply. A decided report is final; the same decision again answers it as it is.
"""),
("""The space page's report button and the account's reports are not built.""", """The space page's report button and the account's reports are not built.
- **The space's owner,** under `/manage/spaces/:spaceId/data-reports`: the list and the decision. Reception is refused. The owner's screen is not built."""),
("""- **Owns** the `data_reports` table, a report's rules (one open per user, space and field; a decision's fields together) and the report limit.""", """- **Owns** the `data_reports` table, a report's rules (one open per user, space and field; a decision's fields together; a decided report final) and the report limit.
- **Leaves** who may read and decide to `can()` (`space.dataReports.read`, `dataReports.resolve`, [security › Authorization](../backend/security.md#authorization)), on the links [`space-links`](space-links.md) loads; the space's lock to `spaces`."""),
("""- A report is dated by the one clock ([conventions §11](../backend/conventions.md#11-time)).""", """- Its manage router sits at `/data-reports` below `/manage/spaces/:spaceId`, behind the one boundary ([conventions › Routers](../backend/conventions.md#routers)); each route asks `can()` first through `requireCan`, and the decision again under the space's lock ([conventions › Space access](../backend/conventions.md#space-access)).
- A decision is audited in its own transaction ([conventions §6](../backend/conventions.md#6-audit)).
- A report and a decision are dated by the one clock ([conventions §11](../backend/conventions.md#11-time))."""),
("""`repliedBy` is read from who decided, as stored with the decision (`OWNER` → `SPACE`, `ADMIN` → `MASAHA`).
""", """`repliedBy` is read from who decided, as stored with the decision (`OWNER` → `SPACE`, `ADMIN` → `MASAHA`).

**The owner's list.** A page of the space's rows, newest first, by status and field, and its count. The repository's select names no reporter column, so no mapper can show one.

**Decide.** The report's space, read without a lock, must be the path's (else `not_found`). Then, in one transaction: the space's lock; `can('dataReports.resolve')` on the links read under it, so a link ended meanwhile decides; the report's row, locked (`FOR UPDATE`); `decisionOf` (pure): an open report is decided; one decided with the same status, reply and decider is answered as it is, writing nothing; any other decision is `REPORT_ALREADY_DECIDED`. The decision writes its status, who, when, the reply and the side (`OWNER`) together, audited. Lock order: the space's row, then the report's; a report's create takes the user's row only, so no two orders cross.
"""),
("""- **"Publicly listed" is asked""", """- **Dismissing needs a reply; resolving takes one or none** (decision 10). *Why:* a reporter told "not changed" deserves the reason; a fixed field speaks for itself. The schema's refinement and a `CHECK` hold it. 2026-10-25, #PRNUM.
- **A decided report is final: `REPORT_ALREADY_DECIDED`** (decision 11); **the same decision again answers it as it is** (S8). *Why:* a reporter must not see the reply change; updates are idempotent by design, so a retry after a lost answer is no refusal ([conventions §13](../backend/conventions.md#13-idempotency-and-concurrency)). 2026-10-25, #PRNUM.
- **The owner never sees who reported** (O12). *Why:* a reporter must not fear the space; the admin, who answers for the platform, sees them. The repository's select leaves the reporter out, so no mapper can leak them. 2026-10-25, #PRNUM.
- **"Publicly listed" is asked"""),
("""the user's own reports with the replies.""", """the user's own reports with the replies; the owner's list and decision."""),
("its service, its repository, its site router and its limit.", "its service, its repository, its site and manage routers, its limit and the decision's rule (`decision.ts`)."),
])
print('ok')

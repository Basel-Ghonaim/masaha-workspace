"""Commit 2's documents: data-reports.md (Web parts), architecture §2, overview, finding 150's evidence."""
ROOT = 'C:/dev/masaha/app-lane-b/docs/'


def edit(rel, pairs):
    path = ROOT + rel
    with open(path, encoding='utf8', newline='') as handle:
        text = handle.read()
    for old, new in pairs:
        assert text.count(old) == 1, (rel, old[:70], text.count(old))
        text = text.replace(old, new)
    with open(path, 'w', encoding='utf8', newline='') as handle:
        handle.write(text)


edit('features/data-reports.md', [
    (
        '**Last Updated:** 2026-10-25',
        '**Last Updated:** 2026-10-28',
    ),
    (
        "its entity by the [data model](../architecture/data-model.md#operations). The API is built; no screen yet.\n"
        "> **Scope:** the API module `data-reports` (L3); `@masaha/shared/data-reports`.",
        "its entity by the [data model](../architecture/data-model.md#operations). The API is built; on the web, the owner's «بلاغات البيانات».\n"
        "> **Scope:** the API module `data-reports` (L3); `@masaha/shared/data-reports`; the web feature `features/data-reports`, any page group: the owner's list of a space's reports and the decision sheet.",
    ),
    (
        "- **The space's owner,** under `/manage/spaces/:spaceId/data-reports`: the list and the decision. Reception is refused. The owner's screen is not built.",
        "- **The space's owner,** under `/manage/spaces/:spaceId/data-reports`: the list and the decision. Reception is refused. On the dashboard, the owner reads «بلاغات البيانات» (`/dashboard/spaces/:spaceId/reports`) and decides each report in its sheet (2026-10-28, #PRNUM).",
    ),
    (
        "\n## Decisions\n",
        "\n**The owner's reports on the web** (`features/data-reports`, composed by `pages/dashboard/space/reports/DataReportsPage.tsx`). «بلاغات البيانات» says what it lists, then «الكل · جديدة · تمت المراجعة» — the server filters `OPEN` or `DECIDED`, so «تمت المراجعة» is either decision — the chip and the page in the address (`?status=open|decided&page=`), and the count. It lists `GET …/data-reports` 20 a page, newest first: from 768 px a table of five columns — the field, the report on two lines at most in its own direction («لم يكتب المُبلِّغ تفاصيل.», muted, when there is none), the day on Gaza's calendar and never the time («21 أكتوبر», the year when it is not this one), the status («جديد» `info`, «تم التصحيح» `success`, «لم يُعتمد» `neutral`) and «فتح» — and below it a card each, «زائر · {day}» on it. The reporter is never named. Its states: loading, a failure with its reference and a retry, a failed refresh over the rows shown, «لا توجد بلاغات», and a chip that matches nothing, with «عرض الكل». «فتح» opens the decision sheet at the end side, full width below 768 px: «بلاغ عن {field}», «زائر · {day}» and the status; the report in a box; «تعديل الحقل», to Packages & prices for the prices and to the field's section of the space profile for the others («أخرى» to the profile); then, while the report is open, «ردّ إدارة المساحة» — its helper says the reply is shown to the reporter, required for «لم يُعتمد» and optional for «تم التصحيح» — focused first, and «تم التصحيح» and «لم يُعتمد». A blank reply with «لم يُعتمد» sends nothing: the reply is focused with «اكتب السبب؛ هو ما سيقرؤه صاحب البلاغ.». The decision is sent once, with no key; no answer says «لم يصل الرد. أعد المحاولة — القرار نفسه لا يُسجَّل مرتين.» with a retry; `REPORT_ALREADY_DECIDED` and a report gone are worded, the list read again and the sheet read-only; a 403 says «لم يعد هذا متاحًا لك في هذه المساحة.» and the user's spaces are read again. Done, the sheet closes, the space's reports are read again, and the toast says «عُلّم «تم التصحيح»» or «عُلّم «لم يُعتمد»», «في «تمت المراجعة»» with «عرض», and «أُرسل الردّ لصاحب البلاغ.» when a reply was written. A decided report opens read-only: its decision with «الردّ: …» or «بلا ردّ», no buttons. Closed, the sheet gives the focus back to its «فتح», or, that row gone, to the count.\n\n## Decisions\n",
    ),
    (
        "\n## Code map\n",
        "\n### Web decisions\n\n"
        "- **The chip and the page in the address** (S8): `?status=open|decided&page=`; a value the server would refuse falls back to «الكل»; a change replaces the address and returns to page 1; no default is written. 2026-10-28, #PRNUM.\n"
        "- **«الكل · جديدة · تمت المراجعة», each row's badge saying which decision** (DI-31): the API filters `OPEN | DECIDED` only, so the chips promise no more; «جديد» `info`, «تم التصحيح» `success`, «لم يُعتمد» `neutral`. 2026-10-28, #PRNUM.\n"
        "- **«تعديل الحقل» leads to the field, with no current value shown** (DI-33): the report's reads carry no current value, and showing one would be a second formatter of five fact groups (A10); the prices lead to Packages & prices, the rest to their section of the space profile. 2026-10-28, #PRNUM.\n"
        "- **The owner sees a report's day, never its time** (DI-34, [finding 150](../architecture/findings/150-the-owner-sees-a-reports-exact-time.md)), and the reporter as «زائر» (O12). *Why:* a time beside the desk's check-ins could narrow the reporter to who was present. 2026-10-28, #PRNUM.\n"
        "- **A report with no details says so** (DI-35): «لم يكتب المُبلِّغ تفاصيل.», muted. 2026-10-28, #PRNUM.\n"
        "- **«لم يُعتمد»'s reply is said required before it is sent** (DI-36): the reply's helper says so first; a blank one is focused with its line, nothing sent. 2026-10-28, #PRNUM.\n"
        "- **A decided report is read-only** (DI-37): its decision, its reply or «بلا ردّ», no buttons — a decision is final on the server. 2026-10-28, #PRNUM.\n"
        "- **The toast says where a decided report went** (DI-41): it leaves «جديدة», so the toast names «تمت المراجعة» with «عرض», and says when the reply reached the reporter. 2026-10-28, #PRNUM.\n"
        "- **A chip that matches nothing offers «عرض الكل»** (DI-42), apart from the list that has no report at all. 2026-10-28, #PRNUM.\n"
        "- **The decision is sent once, with no key** (S4): the same decision again answers the report as it is, so a lost answer is retried from the sheet. 2026-10-28, #PRNUM.\n"
        "\n## Code map\n",
    ),
    (
        "- `packages/shared/src/data-reports/` — the requests and answers.\n",
        "- `packages/shared/src/data-reports/` — the requests and answers.\n"
        "- **Web:** `apps/web/src/features/data-reports/`, entry `index.ts` (`SpaceReportsList`), read by `pages/dashboard/space/reports/DataReportsPage.tsx`, which gives each field's place: the repository in `repository/`; the keys, the owner's list and its chip in the address (`space/`), and the decision sheet's view and its write (`decide/`) in `hooks/`; the address's query (`reportsQueryOf`) and a report's words — its field, its status by audience, its day, its message (`reportView`) — in `services/`; the owner's list (`space/`), the decision sheet (`decide/`), the status chips and the decision's toast in `components/`. Words: the catalogue's `dataReports` section.\n",
    ),
    (
        "- 2026-10-25, #120 — a signed-in user's report of a listed space, 10 an hour, a repeat answering the open one; the user's own reports with the replies; the owner's and the admin's lists and decisions.\n",
        "- 2026-10-25, #120 — a signed-in user's report of a listed space, 10 an hour, a repeat answering the open one; the user's own reports with the replies; the owner's and the admin's lists and decisions.\n"
        "\n### Web history\n\n"
        "- 2026-10-28, #PRNUM — «بلاغات البيانات», the owner's: the space's reports by status, the reporter a visitor and the day only, and the decision sheet.\n",
    ),
])

edit('frontend/architecture.md', [
    (
        "and «دفعاتي اليوم», reception's own payments of today with the handover's figures (2026-10-27, #127), each space page",
        "and «دفعاتي اليوم», reception's own payments of today with the handover's figures (2026-10-27, #127), «بلاغات البيانات», the owner's list of [data-reports](../features/data-reports.md) with its decision sheet, «تعديل الحقل» leading to Packages & prices or the space profile (2026-10-28, #PRNUM), each space page",
    ),
])

edit('project/overview.md', [
    (
        "the owner's and the admin's lists and decisions, the reporter anonymous to the owner.\n",
        "the owner's and the admin's lists and decisions, the reporter anonymous to the owner; on the dashboard, the owner's «بلاغات البيانات» with the decision sheet.\n",
    ),
])

edit('architecture/findings/150-the-owner-sees-a-reports-exact-time.md', [
    (
        "This is the approved shape (`SpaceReport.createdAt`), not a defect of #120.\n",
        "This is the approved shape (`SpaceReport.createdAt`), not a defect of #120. #PRNUM: the owner's screen shows a report's day only.\n",
    ),
])
print('ok')

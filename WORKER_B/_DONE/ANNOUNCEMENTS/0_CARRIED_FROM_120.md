# Carried from #120 (ANNOUNCEMENTS PR 2, `feat/data-reports`) into worker B's next API PR (ANNOUNCEMENTS PR 3, `feat/favorites`)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones go to the **next PR as
dedicated commits at its start**, named in that PR's description ("Carried from #120"). #120's review
(`C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\6_REVIEW_PR2_CLAUDE_CODE.md`, head `36718fde`) found no
blocker and no should-fix. These are the next PR's first commits. Read the review for each item's file and
lines. The supervisor confirmed items 1 and 2's code points (`data-reports.service.ts` `decideUnder`: `can()`
before the report is read; `data-reports.mapper.ts` `toSpaceReport` answers `createdAt` whole).

Suggested subjects (recount, ≤ 50): `refactor(data-reports): name its router me` (item 1);
`docs(data-reports): state the decision race and fixes` (items 2–4, finding 150).

1. **The "site" router is a `me` router** (review 2): conventions › *Routers* defines four kinds (public, me,
   manage, admin); this one serves signed-in users only. Rename `data-reports.site.routes.ts` →
   `data-reports.me.routes.ts`, `createDataReportsSiteRouter` → `createDataReportsMeRouter`, in `index.ts` and
   `app.ts`; conventions §7's row "me (at the API's root: a report, and the reporter's own)" and §9 likewise. No
   behaviour changes: the existing data-reports API tests stay green unchanged (run those files); no new test.
2. **The owner and the admin at once** (review 3): `data-reports.md` › *Behaviour and flows* › **Decide**, the
   contract's `PATCH /admin/data-reports/:reportId` errors, as the review's fix says — an owner's decision while
   the admin's waits makes it 403 while the owner is still linked, and `REPORT_ALREADY_DECIDED` once the space is
   unverified again; the admin's decision first makes the owner's 409. Documents only.
3. **A sentence under the wrong bullet** (review 4): in `data-reports.md` › *API decisions*, move "The
   repository's select leaves the reporter out, so no mapper can leak them. 2026-10-25, #120." to the O12 bullet
   it belongs to.
4. **A comment past the wrap** (review 5): `apps/api/test/app.ts` line 24, re-wrapped at 100 — only if a commit of
   this PR touches the file anyway; otherwise leave it and say so.
5. **Record finding 150 — decided by the owner (2026-10-25): record only, change nothing** (review 1): the
   owner's list answers a report's exact `createdAt`, which a small space's owner may match against the desk's
   check-ins to guess the reporter (against O12). Status: **accepted as built** (the approved shape, D2); the
   option not taken: coarsen the owner's `createdAt` to the Gaza day or the hour. Its file in
   `docs/architecture/findings/` and its index line. **A new finding of this PR takes 151** and on.

Every item is done in that PR; one you would leave, or one that proves larger than this file says → **stop and
ask**, never silently.

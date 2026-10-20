# Carried from #94 (DESK PR 1, `feat/live-status`) into DESK PR 2 (`feat/desk-visits`)

**The owner's review rule (2026-10-20):** a serious or large review fix reopens its PR; small ones are
deferred to the **next PR as a dedicated commit at its start**, named in that PR's description ("Carried
from #94"). #94's review (`6_REVIEW_PR1_CLAUDE_CODE.md`, head `e07308b4`) found no blocker and three small
should-fix items; the supervisor confirmed each in the code. #94 merged at `eabdb919` (2026-10-20). They are **DESK PR 2's first commit**, before
the plan's commit 1, with its own red-then-green tests and breaks, recorded in `4_REPORT_PR2.md`.

Suggested subject: `fix(occupancy): prove the directory's live inputs` (≤ 50, recount).

1. **Two live-status inputs on the directory's side have no test.** `occupancy.service.ts`'s
   `liveStatusFor` builds `closureNow: closed.has(id)` (from `announcements.closedAt`) and
   `override: state?.override ?? null` itself; no directory test sets up a closure or an override, so
   breaking either line leaves every test green — the public site would show a closed space as
   `AVAILABLE`, or ignore the desk's override. Fix: in the directory's live-status API test
   (`apps/api/src/modules/directory/liveStatus.api.test.ts` or its setup), a space under a closure in force
   and a space with an override in force, each asserted on the public card/pin and on
   `GET /spaces/:slug/occupancy`. Breaks: `closureNow: false`; `override: null` — each seen red.
2. **`docs/plans/v1-mvp.md:218`** still says "reception is read-only"; reception now sets and clears the
   override. Fix the sentence.
3. **`docs/backend/security.md:82`** says each write is decided by "its own owner-only `can()` action",
   then lists the override as the staff's — it contradicts itself. Fix: each write by its own `can()`
   action (owner-only, or the staff's for the override).

**The two review nits — taken by the owner (2026-10-20), as recommended:**

4. The override is refused (`409 SPACE_NOT_OPEN`) only outside the space's hours; it is still stored during
   an active closure or on an unverified space, where the rule ignores it silently — the silent no-op the
   refusal exists to prevent. *Recommended:* refuse it in both cases with the same code, under the same
   lock, with a test and break each.
5. During a closure, the staff's answer shows the override "in force" beside `CLOSED`. *Recommended:* the
   staff's answer carries the override only while the rule uses it (a closure announced after an override
   was set hides it), with a test.

Items 4–5 are a **second carried commit**, right after the first: `fix(occupancy): refuse an ignored
override` (42, recount) — the refusal under the space's lock, the staff's answer, a test and a break each;
`docs/features/occupancy.md` (*Behaviour*, *API decisions* with «{date}, #PRNUM.») and the API contract's
override refusal say so. No new error code: `SPACE_NOT_OPEN` covers all three cases (its catalogue line
re-read: if it names only the hours, stop and ask).

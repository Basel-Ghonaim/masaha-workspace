# Carried from #118 (DESK_API, `feat/desk-api`) into worker B's next API PR (ANNOUNCEMENTS PR 2, `feat/data-reports`)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones go to the **next PR as
dedicated commits at its start**, named in that PR's description ("Carried from #118"). #118's review
(`C:\dev\masaha\workspace\WORKER_B\DESK_API\6_REVIEW_CLAUDE_CODE.md`, head `12abd264`) found no blocker. These
are the next PR's first commits, each test seen **red under the break it names** (the code is right today, so
each new test is proven by its break, not by a red step). The supervisor confirmed item 1 in the code.

Suggested subjects (recount, ≤ 50): `test(auth): prove a refresh renews no idle clock` (items 1, 4);
`test(desk): subscribe from a shift's published price` (item 2); `docs: say the guard refuses an idle session`
(item 3, findings).

1. **A refresh renews nothing for a live reception session** (review 1): an API test — reception signs in at T,
   refreshes at T+10 min (200), the new token row's `last_activity_at` is still T; a request at T+15:01 with the
   new access token → 401 `SESSION_IDLE`. **Break:** `issueInFamily` writes `lastActivityAt: at` → red.
2. **Spec D with a shift's price** (review 2): a space with a shift and two month prices (no shift, and that
   shift); subscribe with each key; assert the `priceAgorot` and `shiftId` copied. **Break:** `findStandard`
   drops the shift from its `where` → red.
3. **ADR 0003's revised line** (review 3): "the guard refuses an idle one (401 `SESSION_IDLE`) and the refresh
   ends it"; and half a line in `security.md`'s *Idle (reception)* row: links at a soft-deleted space count, as
   for `OWNER` (review departure 8).
4. **The test helper's session clock** (review 4): `apps/api/test/app.ts` `signAccess` sets `lastActivityAt:
   FAR_AHEAD`, as it does `expiresAt` and `sessionEndsAt`.
5. **Findings to record** (B's block; the next free from **170**):
   - **170** a request's renewal racing a rotation can be lost on the newest row (review 5; the cost is an early
     sign-in, never a session kept alive; the fix it names: `max(last_activity_at)` over the family).
   - **171** a published price changed between the desk's read and the subscribe is charged silently (review 6;
     to decide with DESK_SCREENS PR 4: an optional `published.amountAgorot` compared by the server → 409, or the
     screen reading the price again before confirming).

Every item is done in that PR; one you would leave, or one that proves larger than this file says → **stop and
ask**, never silently.

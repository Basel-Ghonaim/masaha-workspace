# Review of #129 — R3: the user's side (my reports, the report dialog, favourites) and the space page

Read this file, then `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\5_REVIEW_PROMPT_LEAD_COMMON.md` whole, and do
it. Your report: `6_REVIEW_LEAD_R3_CLAUDE_CODE.md`. Your new findings, if any: **187–189**.

**Your range:** `dc427a54..fcf46637` — 6 commits:
`fda9559c feat(data-reports): show a user's own reports` (screen 11) · `c9739dcd feat(data-reports): report wrong
information` (finding 168) · `97ec50fe feat(design-system): add the heart icon` · `1285d9ab feat(favorites): save a
space from its card` (with LEAD-D12's fold: a guest's favourite shown unpressed after sign-in) · `0b75e262
feat(favorites): list a user's favourite spaces` (screen 10) · `fcf46637 feat(announcements): show a space's
announcements` (commit 6, by the lead; finding 131).

**Read in the plan:** §2 PR 4a's and PR 4b's scope and acceptance criteria; §5 S13, S14, S15, S16 and any S the lane
names; §7 *PR 4* (DI-* to DI-61; U8's order of the space page); §8 *PR 4* and *Shared with the other items*; §9 *PR
4 · Commit 1–6*; §10 *PR 4* and *Review Focus*; §13's PR 4a and 4b real run. **In the lead's report:** *The lanes as
they ran* (lane C), *The joins* (lane C), *Commit 6*, LEAD-D8, LEAD-D9, LEAD-D10 (*Finding 180*), LEAD-D12 (*A
defect found in the real run*), the real run's PR 4a/4b cases; `scripts\lane-c\REPORT.md` whole. **On
`origin/main`:** the contract's *Data reports* (the user's report: signed-in, 10 an hour, a repeat answering the open
one, `201` vs `200`; the user's own with replies), *Favourites* (saved/removed idempotent, at most 200,
`FAVORITES_LIMIT_REACHED`, read whole as the directory's cards, newest or nearest), the space page's announcements;
findings 131, 168.

**Look hardest at:**
- **The guest's intent (S14/S15):** a guest's heart or report → the sign-in prompt → back on the page with the
  intent resumed **once** (favourite saved and shown pressed — LEAD-D12's fix: is it right with TanStack v5's
  in-flight dedupe, and is its test real?; the report dialog reopened, never sent by itself); the intent never
  survives into another account, another space, or a later visit; finding 168 (password recovery) true.
- **The favourite toggle:** optimistic or not as planned, the undo, a double press, a failure rolling back, the
  limit's line, the heart's name and `aria-pressed`, 44 px on touch; the same state on the Directory's cards, Home's
  and the page (one source); «المفضّلة» newest / nearest (the location only to sort, never stored or sent beyond the
  header the contract names), a space that left the directory shown by name.
- **The report dialog:** the field, the text bounded, the repeat line (`200` → the open report), 429's line, the
  toast saying who reads it; «بلاغاتي» with status and replies — the user's own only.
- **The account area:** `AccountLayout`, its navigation and the account menu's links; the guards (a guest
  redirected; a staff account's view).
- **Commit 6 — the space page:** U8's order (the running closure's notice at the top, the other announcements after
  the status, before the prices, at 390 and 1440), `runningClosure`'s boundary at now (Gaza vs UTC), LEAD-D8's split
  (`ClosureAlert` / `ClosureNotice`), LEAD-D9's polite `role="status"`.
- **Finding 180 (LEAD-D10):** the site page's chunk reaching `data-table` and the calendar's library — is the cause
  as stated (feature barrels exporting dashboard screens) and is recording it rather than fixing it sound, given this
  PR moved the calendar out of the first download?
- **The joins:** lane C's commits were rebased onto lane B's with conflicts kept both sides (`data-reports`'
  `queryKeys`, `index.ts`, repository, copy, `src/test/dataReport.ts`, documents): anything lost or duplicated?
- **Tests and breaks:** §10 PR 4's (and commit 6's 82–84b) present / missing / weaker, and would each fail.
- **Documents:** `data-reports.md`, `users.md`, `favorites.md`, `directory.md`, `announcements.md`,
  `architecture.md` §2, §7 (S13), `overview.md`, `foundation.md` §13 screen 11's line, findings 131 (*Resolved*),
  168, 180 and the index — true to the code, one home per fact, `#129`.

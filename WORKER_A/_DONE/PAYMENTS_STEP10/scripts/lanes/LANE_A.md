# Lane A — announcements (the plan's PR 2, commits 1–4)

Read `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\lanes\LANE_COMMON.md` whole first: it binds you.
This file adds your lane's facts.

- **Worktree:** `C:\dev\masaha\app-lane-a` · **branch:** `lane/a` (from Lane 0's `cf0dcb0c`).
- **Scripts and report folder:** `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\lane-a\`.
- **Grant name:** `lane-a`. **Your new finding numbers, if any:** 174, 175.

## What you build

The plan's **PR 2 — announcements (screen 18)**, its four commits in order, each atomic:

| # | Subject (§12) | §9 | §8 | §10 tests |
|---|---|---|---|---|
| 1 | `feat(announcements): list a space's announcements` | *PR 2 · Commit 1* | PR 2 commit 1 | 25–30, 44 (and 24/85's catalogue parity) |
| 2 | `feat(announcements): post and edit an announcement` | *PR 2 · Commit 2* | commit 2 | 31–35 |
| 3 | `feat(announcements): end, start or delete one` | *PR 2 · Commit 3* | commit 3 | 36–39 |
| 4 | `feat(announcements): extend after a closure` | *PR 2 · Commit 4* | commit 4 | 40–43 |

Plan line ranges: §2 PR 2 scope 98–104, AC 159–178; §7 PR 2 607–650; §8 PR 2 763–788; §9 PR 2 1065–1248; §10 PR 2
1581–1604, Review Focus 1654–1669; §11 1677–1680; §13 checks 5.f, 5.g, 5.h.

**Your capability documents:** `docs/features/announcements.md` (its *Web* parts, S16), `subscriptions.md` (one
line, and commit 4's *Who uses it*), `docs/frontend/architecture.md` §2, §3 (S2's line), §7 (S12's line),
`docs/project/overview.md` (*Built* lines), `docs/frontend/design-system/foundation.md` §13 screen 18's line
(§14.8 of the plan: "the owner can then extend the subscriptions it covered, by the days typed, once").

## What changed since the plan was written — adapt to it and record each adaptation

- **#128 merged** (worker B, API only): **the closure extension now also moves each covered subscription's renewals
  not started.** The preview's `subscriptions` count includes them, and the extension's `201` moves them; a key of
  another space's closure is `409 conflict`. Read the contract at your worktree's
  `docs/api/api-contract.md` › *Announcements (managed)* (the two `extend-subscriptions` routes, lines ≈ 700–770)
  and `packages/shared/src/announcements/responses.ts` (`ExtensionPreview`, `ExtensionApplied`,
  `ClosureExtension` — the web types did not change). **Commit 4's dialog words the count as the server answers it**
  (the subscriptions it would move now: those it covered and their renewals not started — still "subscriptions";
  say so truthfully in the line, the plan's §9 Arabic adapted only as far as needed, recorded as a decision with the
  words before and after), and any test or copy the plan wrote before #128 is adapted.
- `dayText`/`dayWord` are in `@shared/lib` (PR 1). The layer's `Calendar`/`DatePicker` come from
  `@shared/design-system/calendar` (Lane 0). PR 2's sheet draws `DatePicker` + `Calendar mode="single"`.
- The public pieces (`components/public/AnnouncementItem.tsx`, `ClosureNotice.tsx`) you build in commit 2 are reused
  later by the lead's commit 6 (PR 4's last, `SpaceAnnouncements`): build them as §9 says, **not exported yet**.

## Files

**Yours:** `apps/web/src/features/announcements/**` (new), `apps/web/src/pages/dashboard/space/announcements/**`
(new), copy `apps/web/src/shared/copy/{english,arabic}/announcements.ts` (new), the documents above.
**Shared (your own lines only):** `pages/dashboard/routes.tsx` (`SPACE_PAGES.announcements`, alphabetical — first
in the map), `pages/dashboard/routes.component.test.tsx` (your tests appended in their own `describe`/`it`s), copy
`{english,arabic}/index.ts` (the `announcements` import and entry, alphabetical), `architecture.md`, `overview.md`,
`foundation.md`, `subscriptions.md`.
**Not yours (never edit):** `features/data-reports`, `features/favorites`, `features/directory`, `features/users`,
`pages/site/**`, `shared/design-system/**` (lane B adds `FilterTag`, lane C the heart icon), copy `dataReports.ts`,
`favorites.ts`, `site.ts`, `users.ts`, `directory.ts`, any `errors.ts`. If you find you need a change there, record it
as a decision and tell the lead in your reply instead.

## When you end

Build commits 1–4. Then run the heavy checks of LANE_COMMON §4 (lint, typecheck, the two full web lanes) through the
grant, all green, and end your turn with the reply of LANE_COMMON §9 marked **DONE**. If the lead later sends you
fixes, fold them into their commits and re-run what they touched and the lane they failed in.

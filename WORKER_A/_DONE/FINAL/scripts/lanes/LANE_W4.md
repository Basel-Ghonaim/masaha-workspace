# Lane W4 — U9: the public site and the account

Read `LANE_COMMON.md` and `LANE_W_COMMON.md` (same folder) first and follow them; this file adds your lane's facts.

- **Worktree** `C:\dev\masaha\app-lane-w4`, **branch** `lane/w4`, **base** `4550b5b2` (U0 + the lanes joined: lane L (U3 whole) and lane T's C4.1 (the `public.ts` entries)).
- **Scripts folder:** `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\lane-w4\`. **Finding numbers:** 214–215.
- **The plan's parts for you** (`2_PLAN.md` lines): **§2's carried fixes, lines 145–219** (the owner's words,
  binding: each code fix red first); §5.9 **1674–1818** (D9.1–D9.15); §8 U9 **2133–2146**; §9.1 U9 **2282–2298**
  (C9.1–C9.16); §10.4 T250–T298 (**2632–2680**); §12.1 U9 **2806–2808**; §4.1's rows 1–11 (**311–330**); §7's rows
  for 32 (web half), 82, 133, 134, 135, 136, 137, 138, 168 (**1947–2018**); DI14, DI20–DI22, DI31, DI33
  (**1874–1943**); OD5. Read `docs/features/{directory,users,auth,favorites}.md` and the contract's *Me*, *Session* first.
- **The foundation in your base already did:** carried item 1's focus rule (`shared/routing/focus/useMainFocus`: a
  hash naming an element focuses it) — you make About's two sections' headings focusable targets (`tabIndex={-1}`,
  C9.8); the site header's phone layout (G1.1, G1.2) and the account menu's items for `/me` («إعدادات حسابي») — you
  build the page itself (D9.2) into the stub `pages/site/account/settings/AccountSettingsPage.tsx`.
- **Your files:** §8 U9 (2133–2146); copy `{site,auth,users,directory,favorites,status}.ts` (both languages; in
  `users.ts` and `site.ts` add your own sub-objects only); `packages/shared/src/users/passwordPolicy.ts` (§9.3's
  exception). `features/data-reports/public.ts` and `features/platform-settings/public.ts` exist (lane T's C4.1, in
  your base): the site imports only those entries.
- **C9.1 (D9.1)** moves `features/users`' files, which U0's C0.5 edited (`AccountMenuContent`, `AccountMenu`,
  `CompactAccountMenu`, `useAccount`): move U0's versions (your base), with their tests; `index.ts`'s exports
  unchanged.
- **What each commit needs from other lanes** (build those whose needs are in your base first):
  - C9.1, C9.4, C9.5, C9.6, C9.7, C9.8, C9.9 (the place filter's cap: `DIRECTORY_AREAS_MAX` — check it exists in
    `@masaha/shared`; if not, record and tell the lead), C9.10–C9.15 — none beyond your base (C9.4's WhatsApp needs
    the platform's public contact read: lane W2's C6.4 `usePlatformContact` — if not in your base, build C9.4's other
    parts and leave the WhatsApp line for a later fold, said in your reply). C9.2 — A1's C1.6 (`hasPassword`,
    `hasGoogle`). C9.3 — A1's C1.3 (`created`). C9.16 — L's C3.5 (the range).
- Reply DONE when all 16 commits are made and the lane-wide checks are green.

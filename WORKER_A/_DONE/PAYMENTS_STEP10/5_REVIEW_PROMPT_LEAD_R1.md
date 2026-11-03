# Review of #129 — R1: the foundation and the announcements

Read this file, then `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\5_REVIEW_PROMPT_LEAD_COMMON.md` whole, and do
it. Your report: `6_REVIEW_LEAD_R1_CLAUDE_CODE.md`. Your new findings, if any: **181–183**.

**Your range:** `origin/main..2fa45cf8` — 7 commits:
`4ebc2785 perf(design-system): serve the calendar on its own` (finding 169) · `18db0601 fix(design-system): start a
range on each click` (finding 173) · `a23896a7 test(web): pre-bundle the calendar for jsdom` (not in the plan:
LEAD-D11) · `ddaa3db2 feat(announcements): list a space's announcements` · `74000c57 feat(announcements): post and
edit an announcement` · `2279134a feat(announcements): end, start or delete one` · `2fa45cf8 feat(announcements):
extend after a closure`. (Commit 6, the site page's announcements, is R3's.)

**Read in the plan:** §2 PR 2's scope and acceptance criteria; §5 S2, S4, S11, S12 and any S the lane names; §7 *PR 2*
(DI-10 … DI-22 and on); §8 *PR 2*; §9 *PR 2 · Commit 1–4*; §10 *PR 2* and *Review Focus*; §13's PR 2 real run.
**In the lead's report:** *Lane 0*, *The seams*, *The lanes as they ran* (lane A), *The joins* (lane A), *The cause,
found (LEAD-D11)*, the real run's PR 2 cases and *Every write of the run*; `scripts\lane-a\REPORT.md` whole.
**On `origin/main`:** findings 45, 169, 173; foundation §3 and §12; `vite.config.ts`, `scripts/libraryChunks.ts`,
the `check:build` script; the contract's *Announcements (managed)* — the extension's preview and `201` as **#128**
changed them (the count includes the renewals not started; `renewalIds`).

**Look hardest at:**
- **The extension (money: subscriptions' dates move, no undo):** the owner only (reception told the owner extends);
  only a started closure; the preview's days and count shown as the server answers (#128's renewals included, LA-D1's
  wording true to the contract); the days typed bounded 1–365 as the shared schema says; **one key per intent**, kept
  across a retry and a double press, never renewed on an error; `CLOSURE_ALREADY_EXTENDED` / `CLOSURE_EXTENDED` and a
  lost answer worded truthfully; what the list shows after it (the closure's extension state).
- **The post and the edit:** the post's key (S4) — one per opening, kept on retry; the edit is a `PATCH` with no key;
  the period on **Gaza's calendar** (never the browser's zone; the unit lane's `TZ` now catches it), «بدون نهاية»;
  the type's rules (a closure's type/start locked once extended — the server's `CLOSURE_EXTENDED`, shown how?); the
  English text optional; the sheet's fields and errors; focus on open and after close.
- **End / start / delete:** each offered only when the server allows it, with the right role; the undo of «إنهاء
  الآن» (if planned); the delete's confirmation; the focus after a card leaves; the shared invalidation (S12) — which
  query keys, any missed (the space's live status, the desk's closure warning).
- **The list:** the tabs (running / upcoming / ended) in the address; paging; the summary's counts the server's.
- **Finding 169's fix:** the new layer entry (`calendar.ts`), `LAYER_ENTRIES`, the library chunk, `check:build`
  refusing it in the first download (the break made through the main barrel — LEAD-D3: is the guard real for the
  leak #127 met?), every importer moved, foundation §3 and architecture §3 true. **Finding 173:** `resetOnSelect`
  defaulted for range mode only, a caller may override, the test of a first click real.
- **LEAD-D11's commit:** `deps.optimizer.client` for the component lane only — does it hide a real defect (a slow
  import a user would also feel) or change what the tests prove? Is the build untouched?
- **Tests and breaks:** §10 PR 2's (25–44 and on, as the plan numbers them) present / missing / weaker, and would each
  fail if its behaviour regressed.
- **Documents:** `announcements.md`, `subscriptions.md` (*Who uses it*), `foundation.md` §13 screen 18's line and §3,
  `architecture.md` §2, §3, §7 (S12), `overview.md`, findings 169 and 173 *Resolved* and the index — true to the code,
  one home per fact, `#129` where the number goes.

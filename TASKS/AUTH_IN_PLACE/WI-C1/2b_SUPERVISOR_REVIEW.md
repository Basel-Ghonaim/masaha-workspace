# WI-C1 — the supervisor's review of `2_PLAN.md` (2026-11-24)

**Verdict: sound; recommend approval as written, with the three notes below folded in.** The plan reads the code it
touches (the router's popstate handling, Radix's focus return, `useMainFocus`, `noteSitePage`, the one `useBlocker`,
`startPreferences`' `matchMedia` stub), keeps the layer free of the router, and names a break for every test.

## On the owner's decisions
- **D1 — one width, 30 rem, no `size` prop:** agree. A second value nobody passes is test-only code.
- **D2 — the history API beside the router:** agree. Opening is not a navigation (ADR 0021 point 3), and the plan
  checked every listener the one POP reaches.
- **D3 — S1 to S4:** agree with all four. S1 also fixes a real bug of today's prompt (the focus is lost on close,
  because the heart is not a Radix trigger). S3 closes the dead Back after a reload that the prompt only half covered.
- **D4 — the title on the scale (24 px phone, 22 px wide):** agree.

## Notes to fold in (no decision needed)
1. **Design issue 1 is void:** `p1-signin-390-light-ar.png` (captured 12:40, after the prototype's fix) shows the close
   button at the inline start, as the dark one does. Build the inline start, as planned.
2. **S1's `pointerdown` listener:** register it when the first `AdaptiveDialog` mounts (once, kept), not as a side
   effect of importing the layer, so importing the design system stays free of global listeners.
3. **S3's reach:** the stale-entry check runs only where an `AdaptiveDialog` is mounted; a reload on a page that mounts
   none keeps a marked entry (one dead Back). Say so in architecture §2's bullet as a known limit, or mount the check
   once in the app shell if it is cheap — the executor's call, stated in the report.

## The approval message (sent with `--resume` in the worker's session once the owner says so)

> APPROVED by the owner: D1 (one width, 30 rem), D2 (the history API), D3 (S1–S4), D4 (the title on the scale). Fold
> in the supervisor's three notes in `TASKS\AUTH_IN_PLACE\WI-C1\2b_SUPERVISOR_REVIEW.md`. Cut the branch and execute
> the plan to the end without stopping: local verification, the Chrome pass, the PR, green CI and CLEAN, then
> `4_REPORT.md`. Never merge.

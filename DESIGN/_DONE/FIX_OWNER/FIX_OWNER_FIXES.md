# Batch 5 (the owner) — rebase and three small fixes for PR #76

The independent review passed PR #76 (`REPORT\REVIEW76_OPENCODE_REPORT.md`, verdict PASS). **PR #75
(batch 4) has merged** (`main` = `1240736`), so #76 now conflicts with `main` in the four shared
archive files, as planned. One push does both: the rebase and the fixes below. Work in
`C:\Users\basel\masaha-design`, on `design/owner`. Never merge.

## 1. Rebase (the fast path, workflow §9 *Conflicts*)

`git fetch --prune origin`, then `git rebase origin/main`. The conflicts are only in
`docs/design/CHANGES.md`, `docs/design/INDEX.md`, the board (`Flows - states.html`) and
`docs/design/README.md`: **keep both sides** — batch 4's section 54 and its rows stay, batch 5's
section 55 and its rows follow them; README's counts become the true totals after both batches
(count the frames, the sections and the pages; do not add the two PRs' numbers by hand). Board
positions must not overlap (batch 4 at its place, batch 5 at top 150000). If any conflict reaches a
file outside those four, stop and say so.

## 2. Three fixes, folded into their commits (fixup + autosquash; no fix commit except (b))

a. **`ExtendDialog` closes when the extension succeeds** (`Announcements.html`, the review's nit):
   after `onDone` in the success path call `onClose()`, so the dialog leaves once the toast and the
   card's update show; a failure keeps it open with its error, as P8 says. Fold into
   `docs(design): the closure extension stands alone`.
b. **`AdminShell`'s conditional hook** (`masaha/admin.jsx:27`, pre-existing on `main`, found by the
   review): `const rail = useIsTablet() && !useIsDesktop();` calls a hook conditionally, the crash you
   fixed in `OwnerShell`. Call both hooks unconditionally (`const tablet = useIsTablet(); const
   desktop = useIsDesktop(); const rail = tablet && !desktop;`). **Its own commit**, for example
   `fix(design): the admin shell's hooks run always` (47; count yours: ≤ 50). No other open item edits
   `admin.jsx`. Check an admin page while cycling widths 390 → 768 → 1440: no hook warning.
c. **`docs/design/scripts/check-classes.mjs`:** drop `hover:opacity-90`, `md:max-w-32` and `md:w-72`
   from `KNOWN` (no longer used); the script's output is then clean. Fold into the commit that
   stopped using them, or the board's commit if they span several.

## 3. Check, push, report

- `node docs/design/scripts/check-parse.mjs` and `check-classes.mjs`; `npm run format:check` and
  `npm run check:links` if this folder can run them (else CI runs them); the board, `Announcements.html`
  (`?extend=…`: extend, then the dialog is gone) and one admin page opened at 390, 768 and 1440.
- Every subject ≤ 50 (count them); `git push --force-with-lease`; wait for CI on the pushed head and
  `CLEAN`.
- One **"Review fixes"** comment on #76 (the rebase, (a), (b), (c)); update the PR description if its
  counts changed; add a short "Review fixes" section to `REPORT\FIX_OWNER_REPORT.md`.
- Remove your leftover `final-report-76.md` from the folder (untracked, never committed). Stop every
  server, browser and shell you start; check port 5346 free. Never commit images; never merge.

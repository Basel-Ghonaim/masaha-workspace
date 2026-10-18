# FIX ADMIN EDITOR — reply to your plan

A strong plan, approved with the answers below. Writing it straight to the file without plan mode
was right: the prompt asked for that. Cut `design/admin-editor` and build.

## The owner's decisions (§13)

1. **DI-17 / E5's «فك ربط المالك»:** approved — change that one expression in `Admin spaces.html` so
   `?unlink=` takes the space's own first owner. Do the same on `Admin owners.html` only if it is one
   expression too; otherwise leave it for 2b (A4 rewrites unlinking) and say so in the report.
2. **E5's «بلاغات Focus Hub»:** link to `Admin reports.html?space=focus` now; 2b adds the filter.
   Note it in `CHANGES.md` as waiting on 2b.
3. **S1–S10:** approved as recommended. **S2 is the right reading**: the server takes a shift inside
   at least one open day, so the error is "fits no open day", and the days it does not fit are its
   helper.
4. **Design issues:**
   - **DI-12, DI-13, DI-14:** fold.
   - **DI-15 (24:00):** fold **only if it is built in the prototype's own code** (a page or module
     wrapper). **Never edit the vendored bundle in `_ds/`**: if it needs `TimeInput` itself to change,
     don't build it — record it in the report as a design-system issue for worker A (the web's time
     field must take 24:00 for `closesMinute = 1440`).
   - **DI-16 (a price of 0):** not in this item. It is a product question (does a free price exist,
     and how it reads publicly, «مجانًا») for the public batch, where prices are shown.

## Reminders

- **The shared editor:** after each commit, open both `Admin space edit.html` and
  `Owner space profile.html` at 390 and 1440; F1's 20 px footer gap must hold.
- **Your browser pass** asserts layout (titles drawn once, no overflow) — keep it, and still look
  with your own eyes: fix 1's F2 passed every automated check.
- **The report** lists what `Owner space profile.html` inherited (E7), every owner's addition, and
  the new design issues found while building.
- Stop every background shell you start; `jq` is not installed — use `gh … --jq`.

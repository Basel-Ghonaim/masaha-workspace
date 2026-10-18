# Review — PR #79 (S2b-4b: the admin's space editor, second half — hours with shifts, prices; finding 60)

You are the **independent reviewer** of PR #79 in the Masaha repository (Basel-Ghonaim/masaha), the
third conversation of a trial: one conversation planned, another executed the plan, you review.
Write your report to `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW79_<YOU>_REPORT.md`, where
`<YOU>` is your tool's name in capitals (`OPENCODE`, `COPILOT`).

## Rules

- **Run from `C:\Users\basel\masaha`** and **read only commit objects.** No edits, commits,
  checkouts, switches, installs, npm or test runs, servers, database commands, no GitHub comments.
  **Do not run the tests:** CI ran every lane on this head and passed. `git fetch origin`, then pin to
  **the PR's current head** (`gh pr view 79 --json headRefOid` — expected `7782391`; write it at the
  top of your report and check it again at the end). Base: `git merge-base origin/main <head>`. Use
  `git diff <base>...<head> -- <paths>` and `git show <head>:<file>`.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario,
  the severity (**blocker / should-fix / nit**) and the fix. No praise, no summary. If unsure, say
  "plausible" and why. **No tool attribution** in what you write.

## What the PR must be

Web and documents only (41 files); nothing in `apps/api` or `packages/shared`; no dependency.
- **The plan, your checklist:** `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\S2B4B_PLAN.md` — the
  contract (§2), the decisions (§4: D1–D9 and the owner's four design answers), the stronger decisions
  S1–S4 (§5), the design issues A–H (§9), the tests and their breaks (§10), the copy (§11), the
  commits (§13), *Stop and ask* (§16). Approved as written.
- **The executor's report:** `REPORT\S2B4B_REPORT.md` — judge each departure (the `ReadOnlyItem`
  label, test 15's `ar-PS`, finding 67, the two folded fixes).
- **The pattern it must follow:** PR #74's editor as its review corrected it (`REVIEW74_FIXES.md`):
  each section saves alone through its own hook; "nothing changed" judged against what the form was
  filled from; 403 → read-only, 404 → the 404 even with cached data; a 429 holds Save and the confirm;
  the hooks' logic in `renderHook` tests, the components' tests for rendering only, paths and bodies
  in the repository's test.
- **The contract:** `docs/api/api-contract.md` › *Spaces (the admin)* (`PUT …/hours` with the shifts,
  ids kept, a removed shift in use refused 409; `PUT …/prices`; the confirms; their errors) and
  `@masaha/shared/spaces`' schemas — used, never copied.

## Look at these, in this order

1. **Truth to the API.** The hours' body (the week and the shifts, ids kept, new shifts without ids,
   0–1,440 minutes, 24:00 as 1,440 only as a day's end); the prices' body (amounts in agorot from
   shekels typed — rounding, Arabic digits, a decimal comma —, period, audience, shift id, label);
   every 422 path landing on its field (S2's `shifts.<i>.id`, S3's `prices.<i>.shiftId`), the 409 (S1),
   the 429.
2. **The rules in the browser:** a shift inside at least one open day (the error and the helper of
   design issue A); «نسخ إلى كل الأيام» to open days only (B); a shift a saved price uses not
   removable (D7) — and what happens when it is removed in the form but not yet saved; «الوردية» lists
   saved shifts only, with D6's line while hours are dirty (C, once above the rows).
3. **State and the guard.** Each section's dirty flag, discard, the leave guard naming the two new
   sections, the checklist's links, refetch after save, a section unmounting on 403.
4. **Finding 60.** The hidden area shown only for the space that has it, marked «(مخفية)»; no other
   space offered it; the empty-catalogue case the executor fixed.
5. **Design and localisation.** Times LTR inside Arabic, Western digits, the day names; the table from
   768 and cards below (and finding 67's cut between 768 and ~900 — is a fix within the plan's layout
   possible?); semantic tokens only; every string in both catalogues; accessibility (labels for each
   time field, the switches' names, focus after a refusal).
6. **The tests.** Each would fail with its planned break; hooks tested as hooks; expectations by hand.
7. **The documents.** `spaces.md` (*Web decisions*, *Web history*, code map), finding 60 resolved,
   finding 67 recorded, the index, the overview's *Built* line — each true to the code.
8. **The commits:** three; count each subject's characters yourself (≤ 50).

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; and one line judging the trial: did the plan leave
the executor anything to guess? Then stop.

# Review — PR #85, GALLERY (an independent reviewer)

You are the **independent reviewer** of PR **#85** (`feat/space-gallery`, head `b40a69b8`) in
Basel-Ghonaim/masaha. It was executed by OpenCode (commits) and Copilot (the resumption: build, real
run, PR); you are neither. Write your report to
`C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW85_<YOU>_REPORT.md` (`<YOU>` = your tool's name in
capitals), in parts: first the verdict and the five most important findings, then the rest.

## Rules
- **Run from `C:\Users\basel\masaha-design-b`, read only commit objects:** `git fetch origin`; base =
  `93f152fe`; `git diff 93f152fe...b40a69b8`, `git show <commit>`, `git show b40a69b8:<file>`. No edits,
  checkouts, installs, npm or test runs, servers, database commands, no GitHub comments. **Do not run the
  tests:** CI ran every lane on this head. At the end, check the head has not moved
  (`gh pr view 85 --json headRefOid`).
- Report **concrete problems only**, each verified: file and line, the failing scenario, the severity
  (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. No praise. No tool
  attribution. **Do not use any project skill.**

## What the PR must be
The plan `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\GALLERY_PLAN.md` — **the owner's approval at its top
binds** (seven amendments: `accept="image/*"`, `shrinkImage(file)` with no options, the decode with
`imageOrientation: 'from-image'`, `#85` on decisions, fixes folded, the database by `docker start`,
**commit 0 = §14, #84's review corrections**). The report
`C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\GALLERY_REPORT.md` (Part 1: the commits, red runs,
17 problems, 12 departures; Part 2: the resumption). Judge each departure. Scope: `apps/web` and `docs`.

## Look at these, in this order
1. **Commit 0 against §14** (rows 0.1–0.9): the phone sheet's count and clear; a deleted row as one muted
   line; the delete dialog's line; the chip's words; the two added tests; the documents with `#84`;
   finding 69. Is it complete and self-consistent on its own?
2. **The upload layer** (`shared/uploads`): domain-free; through the one client; progress per file;
   1600 px / 0.85 / JPEG; the orientation option really passed; no parameter only a test uses; the fake
   canvas reached through globals, no `vi.mock`.
3. **The gallery against #77's API:** order, cover, arrows, removal dialog, 409 refetch, 403/404 through
   `useSpaceAnswer`, no optimistic move; one upload at a time; the ten-photo limit and its summary;
   retry only where a re-send can work; the leave guard while an upload runs; a verified space read-only.
4. **The tests:** each would fail with its planned break (§9). The report says **commit 2's tests were
   never seen failing against absent code** — for each of them, judge from the code whether its break
   would make it red, and name any that would not. The two failures under load
   (`useAdminSpacesFilters`, `routes.component.test.tsx`): a real defect or a flake?
5. **What the real run did not exercise** (Part 2: the ten-photo limit, the over-limit selection, the
   leave guard during an upload, a disconnect and retry, an EXIF-6 portrait photo, a server 415): for
   each, is a test proving it instead? Name the ones nothing proves.
6. Frontend rules: design system only, semantic tokens, no physical direction class, every string in both
   catalogues; the documents true to the code, one home per fact; findings 73–74 honest.
7. The commits: count each subject's characters yourself (≤ 50).

## Your output
One file: the head; a one-line verdict; the findings, most severe first, each with **where its fix
belongs** (a fix round on this PR / a finding to record); a short "Checked and fine" list; then stop.

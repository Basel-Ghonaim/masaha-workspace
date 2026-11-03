# #129 (`feat/step10-screens`) — the fix round, in full

You are worker A's lead, back on your own PR **#129** (head `fcf46637`). Its three Claude reviews, one per range, each
say **mergeable after a fix round**:
`C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\6_REVIEW_LEAD_R1_CLAUDE_CODE.md` (the foundation and the
announcements), `…_R2_…` (the data reports), `…_R3_…` (the user's side and the space page). **The owner's decision
(2026-10-28): every finding of the three — blocker, should-fix and nit — is fixed in this round; nothing is carried**
(this is the plan's last PR). The supervisor confirmed R1-F1 and R3-F1 in the code and the contract. Read the three
reviews' *Findings* sections whole (and R1's *Outside my range*), then this file; nothing else unless a fix needs it
(search first, read the section). Do not run the `start-work-item` skill. **Do it yourself — no sub-agents** (the
fixes are small, and worker B is running on the machine).

## 0. The rule for this run — you never stop until the whole task is done

As your lead prompt's §0 (`3_EXEC_PROMPT_LEAD.md`), unchanged: no stop and no question until #129 is ready for
review again (pushed, CI green on the new head, `CLEAN`, the report and the PR's description updated, the final reply
sent); every decision recorded (met, options, chose, why, undo), a SERIOUS one first; the hard limits hold (never
merge, push to `main` or force-push another branch; no data changed through the app, the API or the database, no
reseed; never skip or weaken a test, check or lane; no secret printed; no tool attribution; never `git checkout --
<file>`, `stash` or `reset --hard`; stage by path). A refused command (the classifier) → carry on with everything
else and write the exact command in the report and the reply. **Never stop for the file count.**

## 1. The base

`git fetch origin`; `gh pr view 129 --json mergeStateStatus`. **Rebase only if it is not `CLEAN`** (worker B's PR 2
may merge meanwhile: `apps/api`, `packages/shared`, documents — a document conflict keeps both sides' lines; then
`npm run build -w @masaha/shared`). Make `backup/step10-pre-review-fix` at `fcf46637` before the first fold. No
rebase left in progress at the end.

## 2. The fixes — each folded into the commit that made the code

The owner's method: `git commit --fixup=<sha>` then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`;
never a fix commit; no `fixup!` left; **every subject unchanged** (check after each autosquash). The homes below are
the reviewers' — check them with `git log -L` / `git blame` at the head; a home that is wrong → the commit that made
the lines, recorded. Every code fix: **its new test red before the fix** (copy the line), green after, and a break
that turns it red again (from a backup copy, restored by copy).

**R1 — the foundation and the announcements**
1. **R1-F1 (blocker) — an edit never sends a start or an end the user did not change.** In `editRequestOf`, decide
   "changed" at the precision the sheet shows: compare the typed Gaza date and minute with the loaded instant's
   `gazaClockOf` date and minute (start and end alike), never instant to the millisecond. Tests in
   `sheetRequest.unit.test.ts`: a loaded `startsAt` with seconds (`…T05:00:42.123Z`), nothing changed → `{}`; only
   `textEn` changed → `{ textEn }`; the start moved one minute → `startsAt` sent; the same for `endsAt`; and in
   `useAnnouncementSheet.component.test.tsx`: «Save» untouched on such a start sends nothing and says «Nothing
   changed». Add a fixture with seconds to `src/test/announcement.ts` if the tests need it. → `74000c57`.
2. **R1-F2 — a refusal stays in its dialog.** The extension's dialog and the delete's dialog stay mounted while open,
   whatever the list's refetch makes of the card (hold the opened dialog at the list, as `AnnouncementsList` holds the
   sheet, or keep the opener rendered while its dialog is open — your choice, recorded); the 409 / 404 line stays
   until «رجوع»; on close the focus goes to the card's next action, else the tabs (`useCardFocus.leave`). A list-level
   test: the extension answered `409 CLOSURE_ALREADY_EXTENDED` and the refetch answering the closure extended → the
   dialog and its line stay until «رجوع», then the focus on a card action or the tab; the same shape for the delete
   answered `CLOSURE_EXTENDED`. → `2fa45cf8` (extension) and `2279134a` (delete).
3. **R1-F3 — finding 169's resolution names every importer:** "…which only the ledger's filters, the announcement
   sheet's period and the showcase import"; finding 180's text agrees. → `74000c57`.
4. **R1-F4 — the sheet's calendar marks Gaza's today:** `PeriodFields` passes `today={dayOf(gazaClockOf(new
   Date()).date)}` (through the module's clock if it has one); a test with the clock near Gaza's midnight. → `74000c57`.
5. **R1's *Outside my range*:** `announcements.md`'s *Web history* line added by commit 6 starts "#129 —" like every
   other line (not "2026-10-28, #129 —"). → `fcf46637`.

**R2 — the data reports**
6. **R2-F1 — `data-reports.md`'s *Open findings* lists 167** (the reviewer's line), the later 168 and 180 kept.
   → `dc427a54`.
7. **R2-F2 — after `REPORT_ALREADY_DECIDED`, the sheet shows the decision, never a stale «جديد».** Prefer the fix that
   shows the truth: read the decided report into the sheet (from the «الكل» key of the same scope, or a refetch of it);
   at least never draw the stale status badge once `settled` and the report has left the page. The owner's and the
   admin's sheets alike. A case in `SpaceReportsList.component.test.tsx` under `?status=open`: the 409, then a list
   read without the row → no «New» in the sheet (and the decision shown if you read it); the admin's likewise. →
   `44e8ee1f` (the owner's) and `dc427a54` (the admin's).
8. **R2-F3 — the focus after a filter tag or «مسح الفلاتر» leaves:** to the next tag's remove button, else «مسح
   الفلاتر», else the count. One test: remove the first of two tags → the second's button has the focus. → `dc427a54`.
9. **R2-F4 — «تعديل الحقل»'s `#section` on arrival:** the cause is the editor's (`spaces`), outside this PR's scope —
   **record it as finding 184** (the scroll to `location.hash` once the editor's cards have drawn, as
   `useUncollectedCard` does; "Plausible — not run in a browser" unless you prove it by a test), linked from
   `data-reports.md`'s *Open findings* and the index. → `dc427a54`.

**R3 — the user's side and the space page**
10. **R3-F1 — «إزالة» of a space that left offers no «تراجع»** (the owner's decision on DI-58, option (a)): the
    contract answers `404` to a re-save of a space that is not listed, so the undo can never work. «إزالة» on a
    `listed: false` row removes it with a toast that says it was removed and **cannot be saved again while it is out
    of the directory** — no «تراجع». Copy in both languages through the catalogue. Test 81's undo case becomes "no
    undo offered" (red with the undo restored). `favorites.md:35` and `directory.md:134` corrected. **Record finding
    187**: the API might allow re-saving a favourite the user just removed, for an undo — for a later item. →
    `0b75e262`.
11. **R3-F2 — a guest's held favourite and report expire.** Bound the held intent to the round trip it serves: keep
    a timestamp with it and drop it once stale (15 minutes), **and** drop it when the site shell sees a guest land on
    a page that is neither the sign-in / register pages nor the page that held it. S14 stays: memory only, never the
    address. Tests: a held favourite is not saved by a sign-in after the guest left the auth pages, nor after the
    bound; the same for the held report (its dialog does not open). → `1285d9ab` (favourite) and `c9739dcd` (report).
12. **R3-F3 — the heart keeps one name:** `aria-pressed` with one fixed name («حفظ {name} في المفضّلة» / "Save {name}
    to favourites") — the WAI-ARIA toggle pattern; test 77 and `favorites.md`'s heart paragraph updated (a departure
    from §9's wording, recorded). → `1285d9ab`.
13. **R3-F4 — `overview.md` names the report from a space's page** (the reviewer's sentence). → `c9739dcd`.

## 3. What runs

- **While fixing:** only the test files each fix touches (`npm run test:unit -w @masaha/web -- <files>` /
  `test:component -w @masaha/web -- <files>`), each new test red first; `npm run lint` and `npm run typecheck` before
  each fold; Prettier on the touched files; `npm run check:links` and `check:classes` when documents or classes
  change.
- **Before the push, once, on the final head:** `npm run lint`; `npm run typecheck`; `npm run test:unit -w
  @masaha/web`; `npm run test:component -w @masaha/web` — all green (the fixes touch six areas). No API or shared
  change, so `test:api` is CI's. **Worker B is running:** before each of these heavy runs read the free memory
  (≥ 4 GB → run; less → wait 2 minutes, bounded) — your `scripts\heavy.mjs` does it; never stop worker B's processes. A
  run killed for low memory: re-run once when free; killed again → run it in parts until every file has run green.
- **No real run** this round (the fixes are proven by their tests); the data stays as it is.

## 4. Push and the end

- `#129` is known: write it directly; `git grep '#PRNUM'` on the head → nothing.
- `git push --force-with-lease=feat/step10-screens:fcf46637bf84ab2de598abf0f8080bb42f8964f2` (your own branch; if you
  pushed in between, lease on that sha; refused → §0).
- `gh pr checks 129 --watch` (bounded; no command timeout) → green; `CLEAN`. A red lane → fix, fold, re-run that lane
  locally in full, push, watch again.
- `gh pr edit 129 --body-file …`: a *Review fixes* section — each finding (R1-F1 … R3-F4, R1's outside line) and how
  it was fixed; findings 184 and 187 recorded; R3-F1's option (a) as the owner's decision on DI-58.
- Append to `4_REPORT_LEAD.md` a section *The reviews' fix round (2026-10-28)*: the base, each fix (its commit, the
  red line, the green line, its break), the runs (with memory readings), the push, CI, *Decisions taken without the
  owner* for this round.
- `git status --short` clean; no rebase in progress; name every `backup/*` branch you made.

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
SERIOUS decisions: <each>   (or "none")
PR: #129 · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Rebased: <yes, on <sha> / no, CLEAN>
Commits: <sha> <subject> (<chars>) — all, after the folds
Fixes: R1-F1 … R3-F4 — <folded into <sha>; test red then green; break red>
Findings: 184, 187 recorded
Ran: <each command with its result line; memory readings>
CI on the head: <each lane>
Decisions taken without the owner: <each>   (or "none")
Refused commands: <command>   (or "none")
Backup branches: <names>
Report: C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\4_REPORT_LEAD.md
```

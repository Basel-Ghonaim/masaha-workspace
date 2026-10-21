# OWNER_SETUP PR 3 (#99) — fix round: resolve the conflict with `main`, fix the review's items

You are worker A's executor, in a fresh conversation (or the one that built #99). **#99 is reopened** by the
owner's rule: DESK PR 4 (#100) merged first (at `5d42a527`), so #99 must be rebased onto `main` anyway, and
its review's fixes — small ones included — are done in this same round, folded into their commits. Read
`CLAUDE.md`, then the review `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\6_REVIEW_PR3_CLAUDE_CODE.md` whole,
then your report `4_REPORT_PR3.md`. Work in `C:\dev\masaha\app` only, on `feat/owner-staff-settings`.

## 1. First

1. `git status --short` clean; `git fetch origin`; `docker start masaha-postgres-1` (never `db:up`, never
   `npm ci`; if Docker Desktop is not running, stop and ask the owner to start it); in `apps/api`,
   `npx prisma migrate status` — if #100's `visit_write_off` (or any) migration is pending on `masaha_dev`,
   `npx prisma migrate deploy`, then `npx prisma generate`.
2. **Rebase:** `git rebase origin/main`. Expected text conflicts in three documents only —
   `docs/architecture/findings/README.md`, `docs/features/space-settings.md`, `docs/project/overview.md` — keep
   both sides, each in its own section (workflow §9); never drop #100's lines. A conflict in a code file → stop
   and ask. Then `npm run build -w @masaha/shared`, `npm run lint`, `npm run typecheck`, and — **after the
   rebase**, since #100's migration arrives with it — in `apps/api` `npx prisma migrate deploy` and
   `npx prisma generate` (`masaha_dev` still lacks `visit_write_off`).

## 2. The fixes (each folded into the commit that owns the code: `git commit --fixup <sha>`, then
`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`; bodies kept, a line added where the *why*
changes)

1. **The attendance card's partial fact survives any failure** (review 1): show «حُفظت السعة» apart from the
   failure view (e.g. the card's note while `partial` holds), so it shows beside a network failure, a timeout,
   a 429 or a field refusal; on the partial path the forbidden line drops «لم يُحفظ شيء»; `space-settings.md`
   and finding 96's resolution say "after the capacity, whatever the second request's failure". A test with a
   network failure on the second request (break: the note dropped), seen red then green.
2. **A 404 on the staff, settings and capacity routes refreshes `['me']`** (review 2), as the packages' do:
   **one shared hook** (the third use — move `features/packages`' `useLinkEnded` to `shared/` beside the
   session's other cross-feature helpers, say where and why), used by `packages`, `staff`, `space-settings`
   and `occupancy`; architecture §7's line names them all. One test per page (break: the call dropped).
3. **A lost add answer shows the new row** (review 3): on any add failure, invalidate `staffKeys.list(spaceId)`
   so a row the server holds appears with its pending badge and «كلمة مرور مؤقتة جديدة»; the
   `EMAIL_HAS_ACCOUNT` line no longer points an active row to «إعادة وصوله» (word it for both cases — the
   Arabic listed in the PR description for the owner). A test: a network failure, then the list read again
   (break: no invalidation).
4. **The default reminder after a language switch** (review 4): the text counts as the default when it equals
   **any** catalogue's `defaultText`, read at check time. A test that switches the language and saves
   unchanged → «لم يتغيّر شيء» (break: compare with the first language only).
5. **The documents** (review 5): `occupancy.md`'s header, `users.md`'s *Last Updated*, `space-links.md`'s
   blank line.
6. **The review's other nits** (its *The rest*): the misplaced comment in the English copy, the loading state a
   screen reader cannot hear, the two alerts when the settings fail to load — each as the review says.
7. **Findings to record, numbered 103 and on** (worker A's; PUBLIC uses 130+): the Arabic-digit readers (five
   copies); `useMenuTriggers` copying the admin page's `useRowTriggers`; held menu items possibly unreachable
   by keyboard (the project-wide menu pattern — say it is unverified in Radix's source); the two approved copy
   lines the review names. Each a file and an index line, in the documents commit they belong with.

If an item proves larger than this says, **stop and ask** — never leave one undone silently.

## 3. Verify, push, report

- **Run what the change touches** (the owner's rule for fix rounds): `lint`, `typecheck`, the touched and new
  test files (each new test red first, each break red then restored), `check:classes`, `format:check`,
  `check:links`; the production build and `check:build` once on the head. CI runs the rest.
- **Memory (the owner's standing rule):** before a large run, no `vitest` of `C:\dev\masaha\app-b\` running and
  the free memory recorded; a lane killed for memory: re-run once when quieter, then carry on with CI as its
  judge. Finding 87's routes test missing its 3 s locally while passing alone → CI judges.
- A short real run of the fixed cases (headless Chrome over CDP or Playwright; Arabic light, English dark, 390
  and 1440): the attendance card's partial note (simulate the second request's failure only if the app allows
  it without changing code or data; else its test proves it), the staff list after a lost add if producible,
  the reminder after a language switch. Screenshots to `shots\pr3-fixes\`. A demo account refusing its
  password → stop and report.
- `#PRNUM` is already `#99`; `git push --force-with-lease`; `gh pr checks 99` green on the new head and
  `CLEAN`. Edit the PR description: "Fix round (review of #99)" with each item, and the reworded Arabic lines
  for the owner.
- **A test you cannot run stops the work** (any failure other than the two standing exceptions); never skip,
  never change a config, a timeout, `.env` or a lane; never claim a result you did not see. Stage by path;
  messages from a UTF-8 file without BOM, LF; no tool attribution; never print a password; never merge.
- Append *Fix round 1* to `4_REPORT_PR3.md` as you go. Final reply: Status, PR head, CI, CLEAN, the commits
  (subjects ≤ 50), each item done (red/green, break), ran and passed, COULD NOT RUN, departures, report path.

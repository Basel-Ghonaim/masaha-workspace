# GALLERY — resume the execution (the previous executor hit its limit)

You take over one Work Item mid-way, in a fresh conversation. Read `CLAUDE.md` at the root of
`C:\Users\basel\masaha`, the plan **whole** — `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\GALLERY_PLAN.md`
(the owner's approval at its top binds) — and the previous executor's record
`C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\GALLERY_REPORT_PART1.md`. **Do not re-decide anything.**

## The owner's rule for this resumption

**Nothing that already passed is run or done again.** A check is re-run only if a file it covers changed
after it passed. The four commits are finished: do not rewrite, re-test or "improve" them.

## Where it stands

- `C:\Users\basel\masaha`, branch `feat/space-gallery`, head **`b40a69b8`**, 4 commits ahead of
  `origin/main` (`93f152fe`), tree clean, nothing pushed, no PR, no screenshots.
- **Already passed on this head (do not re-run):** `lint`, `typecheck`, `format:check`, `check:links`,
  `check:classes` (each commit); `test:unit` (78 files, 818 tests); `test:component` (147 files, 980
  tests). The red runs, the break, the two failures under load, 17 problems and 12 departures are in PART1.

## What remains — only this, in this order

1. `git rev-parse --short HEAD` is `b40a69b8` and `git status --short` is empty. If not, stop and say so.
2. **The two checks never run:** `$env:NODE_ENV='production'; npm run build`, then `npm run check:build`.
3. **The real run, §12.4** (steps 8–11), with the **`playwright` MCP tools** (`browser_navigate`,
   `browser_resize`, `browser_take_screenshot` with a relative filename `gallery-shots/<name>.png`,
   `browser_press_key`, `browser_evaluate`). Start the database with `docker start masaha-postgres-1`
   (never `db:up`). Every case of step 10, the portrait phone photo and commit 0's list included. Stop
   both servers by PID; check ports 3320 and 5320 are free. **If you have no `browser_navigate` tool,
   stop here and say so — do not push.** The screenshots may land in `C:\Users\basel\masaha\gallery-shots\`
   (the tool resolves the name from the session's folder): at the end, move that folder's files to
   `C:\Users\basel\Downloads\gallery-shots\`, delete the empty folder, and check `git status --short` is
   empty — never stage a screenshot.
4. **Finding 70:** record it only if the real run reproduces a verified space with no owner — as a
   `--fixup` into commit 0 (the finding file and the index), folded by
   `$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash origin/main`. Then re-run only
   `npm run format:check` and `npm run check:links`. If the run shows a code defect: stop and ask — do
   not fix it here.
5. **§12.5:** step 12b (the PR number: the highest issue/PR must be 84; if worker B's HARDEN took 85
   meanwhile, every `#85` becomes the next number, folded into the commits that hold it, then
   `format:check` and `check:links` only); `git push -u origin feat/space-gallery`; the PR with §12.6's
   description (title `feat(spaces): add the editor's gallery`, labels `feat`, `area:web`, `area:docs`,
   assignee `@me`); `gh pr checks` until green on the pushed head; `CLEAN`; the conflict check against any
   open PR (HARDEN: a documents-only conflict takes the fast path; a code conflict: stop and ask).
6. **The report** `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\GALLERY_REPORT.md` (UTF-8): copy PART1
   into it unchanged, then append `## Part 2 — the resumption` with: who resumed, the build and
   check:build results, the real run case by case with its screenshots, finding 70's decision, the PR
   number, CI, `CLEAN`, the conflict check, and any departure. Leave PART1's file as it is.

Never merge, create an Issue, add tool attribution, print a secret, or use `git add -A` / `.`. Do not use
the project's skills; the plan is enough. **One full test run at a time on this machine** (none should be
needed). When the PR is green and `CLEAN` and the report is saved, say so in a short summary and stop.

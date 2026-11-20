# SPACE_PROFILE — PR-C: RESUME after the executor's context ran out (fresh session, 2026-11-11)

You are a **Claude Code executor** on **Masaha**, in **`C:\dev\masaha\app`**, in a fresh conversation. The previous
executor built PR-C and ran out of context **before verifying, pushing or reporting**. **Model Opus 5.5, effort high.**

## Where it stands (checked by the main supervisor, 2026-11-11 15:16)

- Branch **`feat/space-profile`**, working tree **clean**, **not pushed**, **no PR**. Five commits on `origin/main`
  (`93fe4105`), as the plan's §14: `4ed2af88` C1 lookups · `0e7e6b06` C2 the profile, view first · `7cb3bb44` C3
  drag · `3bfc18f7` C4 the admin's hide/delete · `dec5da08` C5 prices in the profile only. 217 files.
- The `sortable` library chunk (moved from #141) is in (`libraryChunks.ts` + its test). Finding 216 is written.
- `#PRNUM` is still in the docs (expected: it is replaced just before the push). Backups `backup/space-profile-1`,
  `-2` exist locally.
- **Unknown:** which verification the previous session ran. **Trust none of it — run all of it.**

## Read first

`CLAUDE.md`, `docs/development/workflow.md`, `docs/development/testing.md`; the plan
`C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\2_PLAN_PROD.md` (its APPROVED note, §12 test matrix, §15 EC, §16
verification, §17 limits); the original prompt `3_EXEC_PROMPT.md` (its §2–§4 rules apply unchanged); the decisions
`0_OWNER_DECISIONS.md`. Then `git log --stat origin/main..HEAD` to see what was built. Do not re-plan and do not
rebuild what exists; fix what verification finds, folded into its commit (`backup/space-profile-3` first, `--fixup`
+ autosquash).

## Do, without stopping

1. **Check the matrix:** every `T…` of §12 that belongs to PR-C is present; a missing one is written now (seen
   failing first).
2. **Complete local verification** (§16): `lint`, `typecheck`, `format:check`, `check:classes`, `check:links`,
   `check:conflicts`, `NODE_ENV=production npm run build` then `check:build` (the `sortable` chunk out of the first
   download), `test:unit`, `test:component`, `test:api` **in full**. **Memory is short on this machine** (another
   worker runs a screenshot review): **one heavy lane at a time**; a lane killed for memory: retry once, then CI judges
   — say so in the PR. Lint and typecheck per commit, one command at a time, back on the branch after each.
3. **Real run** (§16): both profile pages in the browser at 390 / 768 / 1440, RTL/LTR, light/dark, every Sheet, a
   mouse, keyboard and touch-emulated drag, «نسخ الرابط», «استخدم موقعي الحالي». Screenshots to
   `C:\Users\basel\Downloads\wi142-shots\`, never pushed. Headless Chrome over CDP if the extension is unavailable;
   stop every server by PID.
4. **`open-pr`**: check the next PR number (expected **#142**), replace `#PRNUM` in every commit's tree, push, open the
   PR (assignee the owner; labels `feat`, `area:web`, `area:docs`, `area:design-system` if touched), Evidence naming
   every command run, Deviations, **"What changes on merge"** (§17).
5. **CI** with a bounded loop (≤ 60 min, `gh --jq`): green on the head and `CLEAN`.
6. **`final-report`** → `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\4_REPORT_C.md`: the PR number and **full head
   sha**, commits, file count, every command's result, the EC outcomes, deviations (including the context
   restart), findings. **Then stop. Never merge.**

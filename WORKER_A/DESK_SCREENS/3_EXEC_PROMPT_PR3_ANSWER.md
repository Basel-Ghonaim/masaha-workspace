# DESK_SCREENS PR 3 — the owner's answer to the size stop (2026-10-25)

**Option A: one PR of 81 files, as it is**, titled `feat(desk): show a customer's file`. The owner grants it as a
one-off exception to the prompt's 72-file bound (as #116's 90 files); say so in the report and in the PR's
description. Do not split.

**Accepted by the supervisor, recorded as departures:** the routes test's `beforeAll` warm-up import (the file's
own idiom, no timeout or config changed); break 64 made on the trigger's label; the restored `desk.md` edits
(checked: each of commits 1–4 carries its own `desk.md` change). **Never `git checkout` a file again** while work
is uncommitted — restore from a backup copy.

Then continue `3_EXEC_PROMPT_PR3.md` from where you stopped, in its order:
1. `git fetch origin`. `main` moved to `1a89da5d` (#121, favourites: API, `packages/shared`, the two `errors.ts`,
   docs; it shares only the findings index with this branch, and `merge-tree` is clean). **Do not rebase** — the
   branch merges cleanly; rebase only if GitHub later shows it not `CLEAN`.
2. The head-wide checks of §3.2, once each, with the memory check before each test lane (worker B is idle; no
   `vitest` of `app-b` should run): `test:unit -w @masaha/web`, the scoped `test:component` folders, the
   production build, `check:build`, `check:classes`, `format:check`, `check:links`, `check:conflicts`.
3. The real run of §1.9–§1.10 (PR 3's writes only, the carried fixes shown live, the network log, the width
   break, touch targets; the idle sign-out if the run can wait 15 minutes, else test 67 owns it).
4. `#PRNUM` (the next free number checked just before the push — expected **#122**), push, the PR with `--label
   feat --label area:web --label area:docs`, "Carried from #119" and the size exception in its description; CI
   green on the pushed head and `CLEAN`; the conflict check.
5. The final reply in §6's shape, and the report completed.

The owner is away until tomorrow: **the autonomy rule applies to this run** — read
`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md` and follow it (decide, record under *Decisions taken
without the owner*, never cross its hard limits). Finding 87's family and the memory rule stay as the prompt
says.

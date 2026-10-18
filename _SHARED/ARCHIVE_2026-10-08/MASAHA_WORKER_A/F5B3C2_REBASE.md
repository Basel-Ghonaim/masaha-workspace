PR #39 (the dashboard shell) is merged, so #40 is now in conflict with main. Rebase it.

1. `git fetch --prune origin`, then rebase `feat/recovery-pages` on `origin/main`. Resolve each
   conflict by keeping both sides, as you predicted: `pages/site/routes.tsx`,
   `shared/routing/index.ts`, architecture.md §2–§3. In §3, #39 added the "one component, one hook,
   one responsibility per file" bullet; place your "group files by operation" sentences right after
   it, so the two read as one rule.
2. Record one finding, in its own commit (`docs(findings): ...`): Vite's dev proxy is fixed at port
   3320, so two folders can't run the web against their own API at once (you hit it: you ran on 5330
   with a one-off `CORS_ORIGIN`). Symptom and evidence only, no fix. Number it after main's last
   finding (28).
3. Checks: **don't check each commit on its own.** Run the full lanes once, on the head, one at a
   time: lint, typecheck, check:classes, unit, component, api, build + check:build. Then push with
   `--force-with-lease`.
4. Update the PR description: the rebase resolutions, the new head and counts.
5. Report once CI is green on the new head. Don't merge. No subagents.

# DESK PR 2 — move `feat/desk-visits` onto the latest `main` (after #93)

`main` moved while you work: **#93** (worker A's USERS, web and docs) merged at `7d48c9c3` on 2026-10-20,
after your branch was cut from `eabdb919`. Today none of its files overlaps your commits or your working
tree, but your later commits (C3) edit two documents it changed — `docs/project/overview.md` and
`docs/architecture/findings/README.md` — so rebase now, while it is free. **Do it when it suits you, at a
commit boundary; this does not change the plan or your prompt (`3_EXEC_PROMPT_PR2.md`).**

1. Finish the commit you are on (or the step you are on) so `git status --short` is empty — never stash or
   discard uncommitted work to make room; if the tree cannot be clean yet, wait.
2. `git fetch origin`, then `git rebase origin/main` (a plain rebase; your `fixup!` commits stay as they are
   until the autosquash before the push).
3. A conflict: keep both sides in their own sections (workflow §9); never drop #93's lines. Three tries of one
   conflict that fail → stop and report.
4. After it: `npm run build -w @masaha/shared` (no change expected), `npm run lint`, `npm run typecheck`
   (it covers the web, where #93 changed code your C3 catalogue lines join). Nothing else to install or
   migrate (#93 has no dependency, schema or shared change).
5. **Finding numbers:** the latest index on `main` ends at **97**; any finding you record takes the next
   free number on the index at the time you write it.
6. Append to `4_REPORT_PR2.md`: "Rebased on `origin/main` `<sha>` (after #93)", the conflicts met (or
   none), and the lint and typecheck lines you saw. Then carry on with your prompt.

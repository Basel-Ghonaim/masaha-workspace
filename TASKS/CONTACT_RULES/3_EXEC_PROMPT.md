# CONTACT_RULES — EXECUTE the plan (OpenCode or Codex)

You are a coding agent on **Masaha**, launched in `C:\dev\masaha\app-design`; you work only in the worktree the plan
creates, `C:\dev\masaha\app-cr`. **Never run a command in `C:\dev\masaha\app`** — another worker is using it. Read
whole, in order:

1. `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\0_OWNER_DECISIONS.md` — the owner's decisions (binding).
2. `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\2_PLAN.md` — **your instructions. Execute them exactly, in order.**
   The owner approved its choices (decision C10); one addition: in commit 5, also record **finding 228** — the
   customers' search reads a phone's last digits typed in Arabic digits as a name (the plan's report outline names the
   observation) — its own file in `docs/architecture/findings/` in the format of its neighbours, Status Open, and its
   index line with the others.
3. `CLAUDE.md` of the repository — its rules bind you too.

Rules above everything:
- **The gate after every commit is mandatory** (the plan's §3): lint, typecheck, Prettier on the changed files, the
  touched tests. A failure is fixed before the next commit. **Never push anything that has not passed the plan's
  final verification** — the last PR of this kind went red three times in CI because local checks were skipped.
- Do only what the plan says. When the plan does not cover what you meet, or a check fails twice, **stop and write it
  in `4_REPORT.md`** rather than improvise.
- Never touch the files the decisions' C7 lists; never `git add -A`; never push to `main`; never merge; no tool
  attribution anywhere.
- Watch your context: if it passes 75 %, finish the step you are in, write `4_HANDOFF_STATE.md` beside the plan
  (branch, local and pushed heads, the step reached, what passed), and stop.

End: the PR green and `CLEAN`, `4_REPORT.md` written, servers stopped by PID. Stop.

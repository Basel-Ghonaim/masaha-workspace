# FINDING_232 — remove the unused `PASSWORD_RULES`, and the stale "checklist" words

You work in the repository `C:\dev\masaha\app` (GitHub `Basel-Ghonaim/masaha`): Masaha, a bilingual Arabic / English
web platform (npm workspaces: `apps/web`, `apps/api`, `packages/shared`; Node 24). `main` is **live in production**:
every merge deploys. Work in **two phases**.

## Phase 1 — plan only (now)
Read, then write the plan to `C:\dev\masaha\workspace\TASKS\FINDING_232\2_PLAN.md` and **stop**. Change nothing in the
repository in phase 1. The plan lists: every file you will change and the exact change in each; the test changes; the
commands you will run; the commit message (as text); the PR title and body (as text). If anything below is wrong when
you read the code, say so in the plan under "Differences" instead of improvising.

Read first: `CLAUDE.md`; `docs/architecture/findings/232-password-rules-is-read-only-by-its-test-and-two-comments-still-say-checklist.md`
(the finding: its Evidence and "Resolves when"); `docs/architecture/findings/README.md` (how a finding is resolved);
`packages/shared/src/users/passwordPolicy.ts` and `passwordPolicy.unit.test.ts`; every reader of `PasswordRule`,
`passwordRules` and `PASSWORD_RULES` (search `packages/` and `apps/`, not `dist/` or `node_modules/`).

## Phase 2 — after the message "APPROVED" (later, in this same session)
Do exactly the approved plan, then the verification, the PR, and the report.

## The change
1. **Remove `PASSWORD_RULES`** from `packages/shared/src/users/passwordPolicy.ts`. Keep the type `PasswordRule` as the
   literal union of the four ids it has today (`'minLength' | 'letter' | 'digit' | 'bytes'`), so every reader keeps
   compiling unchanged. Keep `passwordRules()` as it is. Rewrite the two doc comments there that speak of a
   "checklist" to speak of the policy's one line (the password's condition shown as one line since #157).
2. **The unit test:** remove the assertions on `PASSWORD_RULES` (`passwordPolicy.unit.test.ts`, around lines 79–85) and,
   so nothing is lost, assert instead that `Object.keys(passwordRules('x'))` equals `['minLength', 'letter', 'digit',
   'bytes']`. See it fail once by breaking it (e.g. drop `bytes` from the returned record), then restore.
3. **The two stale comments in `features/users`** named by the finding (one is
   `apps/web/src/features/users/hooks/settings/usePasswordChangeForm.ts:20`, "the rules' checklist"; find the second
   — the finding names `ForcedPasswordChangeForm.tsx`): say the policy's line instead. Comments only.
4. **The finding:** mark it resolved as `docs/architecture/findings/README.md` says (status, a dated resolution naming
   the PR as `#PRNUM`), and its line in the findings index.

## Hard limits
- Touch only the files above. Stage by path, never `git add -A` / `git add .`. No other change, no refactoring.
- No tool attribution anywhere: no `Co-authored-by` trailer, no "generated with", in commits, the PR or files.
- Never push to `main`, never merge, never force-push. The owner merges.
- One commit, Conventional, subject ≤ 50 characters, with a body (e.g. `refactor(shared): drop the unused password rules`).
- `#PRNUM` in the finding is replaced with the real PR number just before the push (check `gh pr list --state all
  --limit 1` and `gh issue list --state all --limit 1`; the next number is the larger plus one — expected **#160**).

## Verification (phase 2, all must pass, from `C:\dev\masaha\app`)
1. `git fetch origin` and `git switch -c chore/finding-232 origin/main` (the status must be clean first).
2. `npm run build -w @masaha/shared` (the shared package's `dist` must be rebuilt after the change).
3. `npm run format:check`, `npm run lint`, `npm run typecheck`, `npm run check:links`, `npm run check:conflicts`,
   `npm run test:unit`. All must pass. If one fails, fix it within the limits above, or stop and report.
4. Commit, replace `#PRNUM`, amend that one line into the same commit, push `chore/finding-232`, open the PR with
   `gh pr create` (title = the commit subject; body = the plan's text: what, why, the finding, the checks run).
5. Wait for CI, bounded: `gh pr checks <n>` every 2 minutes, at most 20 times; a network error or "no checks reported"
   is not a failure. Expected: every check passes and `gh pr view <n> --json mergeStateStatus` says `CLEAN`.
6. `git switch main`. Write `C:\dev\masaha\workspace\TASKS\FINDING_232\4_REPORT.md`: the PR number and URL, the head's
   full sha, each check's result, the break you saw fail, anything that did not go as planned. Then stop.

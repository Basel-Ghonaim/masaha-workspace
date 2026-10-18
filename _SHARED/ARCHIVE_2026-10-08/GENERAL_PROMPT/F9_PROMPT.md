Work Item — Finding 9: the Vitest lanes and the drive letter's case · branch `fix/vitest-drive-letter`

## How to work (mandatory)

1. Read CLAUDE.md, then docs/development/workflow.md, then docs/README.md, then docs/architecture/findings.md › finding 9 and docs/development/testing.md. Follow the project's workflow exactly.
2. You are **worker B**. You work in the worktree `C:\Users\basel\masaha-b`, which is detached at the latest `origin/main`. Never work in the main folder `C:\Users\basel\masaha`.
   - Before planning, check:
     - `git rev-parse --show-toplevel` is that folder;
     - the tree is clean;
     - after `git fetch`, HEAD is at the latest `origin/main`.

     If not, stop and report.
3. Start in PLAN MODE. Investigate and reproduce first. Then present a SHORT plan: this is a small fix, so keep it to the essentials, with no long sections. The plan covers:
   - the root cause, proven, not guessed;
   - the fix;
   - every file to change;
   - the commits;
   - how you verify;
   - any question.

   No edit, no branch and no commit before the owner approves.
4. After approval: `git fetch origin`, then `git switch --no-track -c fix/vitest-drive-letter origin/main`. Implement only the approved plan. The first push is `git push -u origin fix/vitest-drive-letter`.
5. Finish at "Ready for review": self-review, push, open the PR. Never merge.

## The problem

Finding 9:
- From a working directory whose drive letter is lowercase (`c:\…`, as an editor's terminal sometimes opens), every Vitest file fails before its tests run.
- From `C:\…`, the same commands pass.
- The finding's suspected mechanism is unproven: the runner and the test files load `vitest` through two spellings of the path, so they get two module instances.
- Today setup.md tells everyone to use an uppercase path. It is a workaround, and both workers have had to remember it.

**Goal:** `test:unit`, `test:component` and `test:api` pass from either case of the drive letter, for both workspaces.

## Rules for the fix

- **Find and prove the root cause before changing anything.** Reproduce both failures from `c:\`, then show where the path splits, then fix it there.
- **The fix lives in the test tooling** (the Vitest configs or their setup), not in production code (testing.md §3: "No production code exists only to serve a test").
- **Prefer a fix at the source** (for example, normalising the root the configs give Vitest) over a wrapper script around the commands. If only a workaround is possible, say so in the plan and let the owner decide.
- **CI runs on Linux, where this can't happen.** Say how the fix is proven, and whether a guard against a regression is possible on Windows only.

## Databases

`test:api` needs a database.
- Use your OWN, never `masaha_test`: worker A's API lane runs at the same time, and the lane empties every table between files, so a shared database would break both.
- In the container `masaha-postgres-1`:
  - create `masaha_b_dev` and `masaha_b_test` (the test one must end in `_test`);
  - copy `apps/api/.env` into the worktree, with `DATABASE_URL` and `TEST_DATABASE_URL` pointing at them.
- Don't start another container. The lane migrates `masaha_b_test` by itself.

## Parallel work (read before planning)

**Worker A** runs at the same time in the MAIN folder, on **F-5a** (`feat/auth-api`): the identity modules, the auth endpoints, rate limits, redaction and the request id. Never touch that folder.

**F-5a's files** that matter here:
- it changes `apps/api/test/setup.ts` (the API lane clears the new `rate_limits` table) and adds tests across `apps/api`;
- it updates `docs/development/setup.md` (environment, email) and adds findings to `docs/architecture/findings.md`;
- it does NOT touch the Vitest configs.

**Your files:**
- `apps/web/vite.config.ts` (its `test` block) and `apps/api/vitest.config.ts`, and only what the root cause requires;
- `docs/development/setup.md`: the Windows note under *Commands* goes once the fix holds;
- `docs/architecture/findings.md`: finding 9's resolution.

**Shared files:**
- `setup.md` and `findings.md`: edit only finding 9's entry and the Windows note.
- `apps/api/test/setup.ts`: avoid it. If the root cause is there, say so in the plan first.
- `apps/web/vite.config.ts` is changed again later by F-5b (ports, proxy). This fix must merge before F-5b starts.

**Before opening the PR:** fetch and rebase on the latest `main`. Whoever merges second rebases, and resolves any conflict by keeping both sides.

## Out of scope

Any other test or config change; production code; new dependencies (propose one only if the root cause needs it).

## Verification and PR

- **Proof in the PR's Evidence:** before and after, each of `test:unit`, `test:component` and `test:api` from `c:\…` and from `C:\…`, for both workspaces.
- `npm run lint`, `typecheck` and `build` pass.

The PR follows workflow §3:
- labels `fix` + `area:ci`, assigned to me (`--assignee @me`);
- the description template;
- no AI attribution.

Don't merge.

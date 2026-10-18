# Review — PR #45 (H-1 housekeeping) at e5bf577

**Verdict:** approve after small fixes. The code is correct. There are no blockers. Five should-fix items: one is an unrecorded finding of the same class as 34, and four are document contradictions or claims that are not true.

## Findings

### Should-fix

1. **`useResetPassword` keeps the new password in the cache for five minutes, and no finding records it.** `apps/web/src/features/auth/hooks/reset-password/useResetPassword.ts:20`
   - Scenario: `ResetPasswordRequest` is `{ password }` (`packages/shared/src/auth/requests.ts:52`). The hook sets no `gcTime`. So the leak finding 34 describes (the variables, and the refusal's `config.data`, kept for 300 s after the page has gone) still happens on the reset page. Finding 34's evidence names `useCheckResetLink` and passes over the hook that actually carries the password.
   - Fix: record it as a new finding. This PR is scoped to finding 34's three hooks, so record, don't do. If the owner approves folding it in, apply the same `gcTime: 0` and the same unmount-then-empty-cache test.

2. **Finding 31 says "the documents now follow the rule", but engineering-principles still prescribes the injected repository.** `docs/development/engineering-principles.md:32`
   - Scenario: it still says "Factory functions with injectable defaults … `createService(repo = createRepository())`". That contradicts conventions §2 (`conventions.md:59`) and testing §3 rule 3 as revised here. A reader of the code-design rules gets the opposite rule.
   - Fix: reword to "Factory functions instead of classes and containers; what a service receives is in [conventions §2](../backend/conventions.md#2-layers)". Alternatively, narrow the finding 31 resolution and record the leftover.

3. **`plans/foundation.md` still says "Whoever merges second rebases."** `docs/plans/foundation.md:33`
   - Scenario: this is the line right under the edited line 32. It contradicts workflow §9 (`workflow.md:153`): a PR is rebased only when GitHub shows a conflict.
   - Fix: change it to "merge order does not matter", or drop the second sentence.

4. **Testing §5 "CI gate" lists the CI checks without `format:check`.** `docs/development/testing.md:60`
   - Scenario: setup.md › CI (`setup.md:164`) and `ci.yml` now run `format:check`, and testing §5 does not list it. The same list is owned twice and now disagrees.
   - Fix: add `format:check`, or better, replace the list with a link to [setup › CI](setup.md#ci).

5. **The finding 28 resolution says "No test sets its own timeout", but one test does, and it is now shorter than the lane's.** `apps/web/src/features/auth/hooks/resend-link/useResendLinkForm.component.test.tsx:49`
   - Scenario: the test passes `{ timeout: 2500 }`, which predates this PR. It used to raise the wait above 1 s. With the 3 s default it now lowers that test's wait below every other test's under load, which works against the fix. The claim also appears in `findings.md` (finding 28, point 2) and in the PR body ("No per-test timeout").
   - Fix: drop the override in commit 1 (the 1 s window fits easily in 3 s), or correct the claim.

### Nits

6. **Workflow §10 owns facts that belong elsewhere.**
   - `workflow.md:178` brings in a new commit and PR rule: "Fixes fold into their commits, with ONE 'Review fixes' comment and no thread replies". No other document owns it, and it sits inside a tooling bullet. It belongs in §3 *Commits* or in `open-pr` step 7, with §10 linking to it.
   - §10's "Precedence" list restates CLAUDE.md › *Decision precedence*. It names "the task's prompt" where CLAUDE.md names "the owner's explicit instruction".
   - "A red test is never committed" is now stated three times: testing rule 5, §10 at `workflow.md:172-173`, and §3's "Every commit … passes tests".
   - Fix: keep one owner for each and link from the others.

7. **`devServer` says less than it does, and accepts some odd values.** `apps/web/scripts/devServer.ts:10-11`
   - The doc says a bad value "stops the server". Because `vite.config.ts` is evaluated for every command, a bad `WEB_PORT` or `API_PROXY_TARGET` in `apps/web/.env` also fails `vite build` and both Vitest lanes. Finding 29 uses the same wording.
   - `Number()` accepts `" 5321"`, `"0x14C8"` and `"1e3"`. This is harmless.
   - Fix (optional): reword to "stops Vite".

## Verified OK

- **The wait.** `asyncUtilTimeout: 3_000` is set once, in `componentSetup.ts`. Only the `component` project's `setupFiles` loads that file. No `testTimeout` override exists in the config or the scripts, so Vitest's 5 s default holds and 3 s < 5 s.
- **`gcTime: 0` placement.** It is on exactly `useSignIn`, `useRegister` and `useChangePassword`, each with its comment.
- **The three new assertions fail without it.** Without `gcTime: 0`, `createQueryClient` (which the test wrapper uses) sets no mutation `gcTime`, so the default 300 000 ms applies. The unmounted mutation then stays in the cache, and `waitFor(getAll() == [])` times out at 3 s. That is the named break, and it matches the PR evidence.
- **No other production change.** With an observer present, the mutation is not collected, so the forms' error and pending state are unchanged. No `useMutationState` reads these mutations.
- **`devServer` behaviour.**
  - Defaults are 5320 and `http://localhost:3320`.
  - An empty value counts as unset (`||`). A copied `.env.example` with empty keys gives the defaults, and this is tested.
  - Invalid values throw naming `WEB_PORT` or `API_PROXY_TARGET`.
  - `scripts/**/*.unit.test.ts` is in the unit lane, and `scripts` is in `tsconfig.node.json`.
- **Vitest projects still work.** `vite.config.ts` became a function config. Both projects use `extends: true`, and `server` was already present before this PR.
- **The env keys cannot reach the browser.** `envPrefix` is not set (default `VITE_`), so `WEB_PORT` and `API_PROXY_TARGET` never reach `import.meta.env`. `loadEnv` is used only for `server`. The PR also grepped `dist` for them.
- **`format:check` covers the same files as `format`.** It is `prettier --check .` against `prettier --write .`, with the same `.prettierignore`. CI runs it as a matrix task through `npm run`.
- **API side.** The API already reads `PORT` (default 3320) and `CORS_ORIGIN` from its own env (`apps/api/src/config/env.ts`), as finding 29 says.
- **Conventions §2's list of older services is accurate:** `users`, `sessions`, `space-links`, `spaces` and `lookups.service` default a repository parameter. The admin lookups services create their own.
- **Links.** All new and changed anchors resolve at e5bf577: `#10-ai-tooling`, `#3-rules-that-bind-every-test`, `#commits`, `#running-a-second-folder`, `#the-web`, `#8-stop-rules`, `#9-parallel-work`, `#2-layers`, `#8-module-rules`, `#5-definition-of-done-and-accepted`.
- **Workflow §10's claims hold.** `.claude/settings.local.json` is gitignored, and the tracked `.claude/settings.json` enables no plugin. Superpowers' `writing-good-tests.md` exists in the installed plugin.
- **ADR 0014.** The "Revised" line follows the other ADRs' convention. Point 3 keeps the decision (one origin, `/api` proxied) and changes only "fixed port" to "a port of its own, 5320/3320 by default".
- **Finding 30** is marked Accepted with the owner's reason, and no code changed.
- **Scope.** Six units only. `preferences.unit.test.ts` is reformatted only (two wrapped `toMatchObject` calls). The only production behaviour change is `gcTime: 0`.
- **Commits.**
  - All six are Conventional, 37–45 characters, and contain no `Co-Authored-By` or "generated with" line.
  - Each is one unit with its findings.md resolution in the same commit. `CLAUDE.md`'s format line is in commit 4, and the precedence line is in commit 6.

**Tokens used:** about 105k.

Work Item F-5 — Authentication and session · branch `feat/auth` (or `feat/auth-api`, if split)

## How to work (mandatory)

1. Read CLAUDE.md, then docs/development/workflow.md, then docs/README.md. Follow the project's workflow exactly: task classes, Git lifecycle, scope control, Definition of Done, decision authority, stop rules.
2. You are **worker A**. You work in the MAIN folder `C:\Users\basel\masaha`. Do NOT create a git worktree.
3. Start in PLAN MODE. No edit, no branch, no migration and no commit before the owner approves a written plan.
   - Before planning, check that `git status` is clean, that you are on `main`, and that `main` matches `origin/main` after a fetch. If not, stop and report.
   - The plan lists:
     - the split decision (below);
     - the modules, endpoints and screens;
     - every file to create or change;
     - the schema change and its migration;
     - every new dependency, for approval;
     - the commits (atomic units per workflow §3);
     - how you verify;
     - any question or divergence you found.

   Wait for approval.
4. After approval: pull `main` again, cut the branch, and implement only the approved plan. Anything outside it: stop and ask. Unrelated problems are recorded as findings, not fixed.
5. Finish at "Ready for review": self-review against the Definition of Done, push, open the PR. Never merge.

## The contract

F-5's contract is in `docs/plans/foundation.md` › *F-5 — Authentication and session*. A-1 and A-3 extended it. **Read it in full: it is the scope.** It is backed by:
- ADR 0003 (session), ADR 0009 (space-scoped reception), ADR 0012 (modules and levels), ADR 0013 (identity as `sessions`, `users`, `auth`), ADR 0014 (deployment constraints: rate limits in PostgreSQL, email without a domain, ports and proxy), ADR 0015 (the idempotency key's name);
- `docs/backend/conventions.md` (§7 modules and levels, §8 rules, §10 logging, §12 environments, §13 idempotency), `docs/backend/security.md`, `docs/api/api-contract.md`;
- `docs/frontend/architecture.md`, `docs/frontend/localisation.md`;
- the designs: `docs/design/SCREENS.md` rows **5** (sign in, with Google), **6** (register) and **7** (forgot and reset password, with the reset email). Also the **forced password change** part of row **9**: reception accounts change their temporary password at first sign-in. The rest of row 9 (the account settings page) belongs to F-6.

## The split decision (decide in the plan)

The contract has grown large: the identity modules, the ESLint level rule, every auth endpoint, Google, the reset email, the rate-limit table, log redaction, the request id, the `idempotencyKey` rename, the dev ports and proxy, the web client, the session, the guards, four screens, and the deferred `architecture/system-overview.md`.

The analyst recommends splitting it into two Work Items, each its own conversation and PR:
- **F-5a, the API** (`feat/auth-api`): the modules and endpoints, the level rule, rate limits, redaction, the request id and the rename. Proven by the API and unit lanes.
- **F-5b, the web** (`feat/auth-web`): the ports and proxy, the Axios client and refresh, `shared/session`, the guards, the screens, and `system-overview.md` (the first end-to-end request).

Evaluate the split in the plan and recommend.
- **If the owner approves it,** this conversation does F-5a only. Add F-5b's drafted entry to `foundation.md`, splitting F-5's contract between the two, so nothing is lost.
- **If not,** this conversation does all of F-5.

## Parallel work (read before planning)

**Worker B** runs at the same time in the worktree `C:\Users\basel\masaha-b`. Never open, edit or run anything there.
- **Its first item is P-1** (`docs/build-map`). It maps the build sequence in `docs/plans/v1-mvp.md` › *Sequence inside the build* to screens and supporting documents. Then comes Finding 9 (the Vitest drive-letter failure), which changes the test configuration.

**Shared file: `docs/plans/v1-mvp.md`.**
- F-5 edits ONLY its *Planned API surface* section: the password change moves to `/me/password`, as the contract says.
- P-1 edits ONLY *Sequence inside the build*, and possibly *Timeline*.
- Never edit the other's section. If both change the status line's date, keep the later date when rebasing.

**Other shared risk:**
- Worker B's Finding 9 fix changes the Vitest configuration. If F-5 needs to change the same config files, say so in the plan.
- F-5b changes `vite.config.ts` (ports, proxy). Finding 9 is planned to merge before F-5b starts.

**Databases:** you use `masaha_dev` and `masaha_test`, as today.
- `masaha_dev` is up to date: all 8 migrations, seeded.
- `masaha_test` still has only the first migration. The API test lane applies every migration before it runs, so this is expected.
- Worker B uses its own databases if it ever needs any.

**Before opening the PR:** fetch and rebase on the latest `main`. Merge order doesn't matter: whoever merges second rebases, and resolves any conflict by keeping both sides.

## Out of scope

- F-6 (the shells, the preferences and the account settings page) and F-7 (deployment).
- Any feature module beyond `sessions`, `users`, `auth` and the minimum of `space-links` the refresh response needs.
- `docs/plans/v1-mvp.md` › *Sequence inside the build* (P-1's).

## Verification and PR

Per the Definition of Done:
- lint, typecheck, `check:classes`, `test:unit`, `test:component`, `test:api`, `build` and `check:build`, run from the uppercase `C:\` path (finding 9);
- for screens: the UI checked in RTL and LTR, light and dark, phone and desktop. Curated screenshots go to `C:\Users\basel\Downloads\f5-shots`, never committed.

The PR follows workflow §3:
- labels `feat` + `area:api` (+ `area:web` if the web part is in);
- assigned to me (`--assignee @me`);
- the description template;
- no AI attribution.

Don't merge.

# Fix — a racing first Google sign-in is refused as "linked to another Google account"

**Worker B** · folder `C:\Users\basel\masaha-b` · branch `fix/google-first-sign-in-race`

**This is a small, fully specified fix. Keep it small.**
- At most 1 subagent; no workflows.
- **Do not read the project's documentation set.** CLAUDE.md is already loaded; it is enough. Skip the reading step of the `start-work-item` skill. Read ONLY the files listed in §2.
- Plan mode: present a plan of **at most 10 lines** (the change, the test, the commit), then wait for approval.

## 1. Start

```
git fetch --prune origin
git status                     # must be clean
git rev-parse HEAD origin/main # must be equal (detached at origin/main)
```
If a check fails, stop and report. After the plan is approved: `git switch --no-track -c fix/google-first-sign-in-race origin/main`.

## 2. Read only these

1. `apps/api/src/modules/users/users.service.ts`, lines ~154–195: `accountForGoogle`.
2. `apps/api/src/modules/users/users.service.unit.test.ts`, the `describe('users: Google', …)` block (from line ~118), for its `setup` fakes.
3. `apps/api/src/modules/auth/google.api.test.ts`, the test `creates one account when two first sign-ins race` (line ~81), only to understand the failure.
4. `docs/backend/security.md`, the *Sign-in methods* section only, to confirm the rule.

## 3. The bug (already diagnosed — don't re-investigate)

CI failed once on `main` (merge of PR #30, `test:api`):
`google.api.test.ts › creates one account when two first sign-ins race`: `expected [ 401, 200 ] to deeply equal [ 200, 200 ]`.

The interleaving:
1. Requests A and B, the same new Google identity, both call `findByGoogleSubject` → `null`.
2. A creates the account (with `googleSubject = G`) and commits.
3. B calls `findByEmail` → finds A's new account, whose `googleSubject` is `G`.
4. B hits `if (byEmail.googleSubject)` and throws `GOOGLE_TOKEN_INVALID` ("Linked to another Google account") — although the linked identity is **its own**.

## 4. The fix

In `accountForGoogle`, when the account found by email is already linked:
- linked to **the same** subject (`byEmail.googleSubject === google.subject`) → it is this identity's account: return `{ userId: byEmail.account.id, link: false }`;
- linked to a **different** subject → keep the existing refusal, unchanged.

Change nothing else: not the retry loop, not the authoritative-domain rule, not the repository, not the error codes.

## 5. Test (the unit lane, deterministic)

In `users.service.unit.test.ts`'s Google block, using its existing `setup` fakes, add:
- `findByGoogleSubject` → `null`, `findByEmail` → `{ account: sara, googleSubject: <the same subject as the token> }` → `accountForGoogle` resolves to `{ userId: sara.id, link: false }`, and `create` is never called.

Keep the existing test where a **different** subject is refused (`g-other`); it must still pass.

Prove the test catches the bug: run it once against the old code (it must fail), then with the fix (it must pass). Say so in the PR.

## 6. Checks

Run: `npm run lint`, `npm run typecheck`, `npm run test:unit -w @masaha/api`, and `npm run test:api` (database up; this folder's `apps/api/.env` points at `masaha_b_test`). `test:component`, `build` and the web lanes are not needed (no web change); say so in the PR.

## 7. Commit and PR

- **One commit:** `fix(users): accept a racing first google sign-in`. The body explains the interleaving in two or three sentences.
- **Documents:** none. security.md already states the rule correctly; this makes the code match it. Don't add a finding.
- **PR:** labels `fix`, `area:api`; `gh pr create --assignee @me`; the workflow §3 template, short. No tool or AI attribution anywhere.
- **Report only once CI is green on the pushed head** (`gh pr checks <n>`). Then stop. Don't merge; don't create an Issue.

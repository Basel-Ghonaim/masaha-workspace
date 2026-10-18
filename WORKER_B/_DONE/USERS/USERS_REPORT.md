# USERS — report

## 1. The pull request

- **#62** `feat(users): suspend, role and temporary password` — https://github.com/Basel-Ghonaim/masaha/pull/62
- **Head:** `50fdcea5b336349ed7588822fe93375a2e958680` · CI green on that head (10 checks: lint, format:check, typecheck, test:unit, check:classes, check:links, build, test:component, test:api, CodeRabbit) · GitHub `CLEAN`.
- Labels `feat`, `area:api`, `area:docs`, `area:web`; assigned to the owner. Not merged.

## 2. The commits

1. `4fad251` docs(workflow): a merge apart needs no new CI run — D7, alone: workflow §9 *Merging*, `open-pr` step 3.
2. `ca88003` feat(api): read the account on each signed-in call — D5: the guard's account reader, `SignedIn`, the token without `role`; ADR 0003 and ADR 0002 *Revised*; security.md; the contract's auth line; finding 51.
3. `e98c7aa` feat(users): suspend and restore an account — D1, D2, D4, S4, S5, S6; `OWN_ACCOUNT`, `LAST_ADMIN`; the admin-set lock; conventions §13.
4. `4734373` feat(space-links): change a person's role — D1, D3; `ACCOUNT_HAS_LINKS`; `admin-roles/`.
5. `50fdcea` feat(users): issue a temporary password — D6; `GOOGLE_ONLY_ACCOUNT`; finding 49 resolved; overview's *Built*.

One review-free fixup was folded before the push (the contract's Users preamble, "reads them" → "reads and changes them", into commit 3).

## 3. What was run

Once each on the head `50fdcea`, one at a time:

| Check | Result |
|---|---|
| `test:unit` | shared 158 · API 660 · web 724 passed |
| `test:api` | 40 files, 665 passed (the whole lane) |
| `test:component` | 123 files, 786 passed |
| `lint` · `typecheck` · `format:check` · `check:links` · `check:classes` | clean |
| `NODE_ENV=production npm run build` · `check:build` | clean |

**Real requests** on 3321 (`masaha_b_dev`, demo data):
- the demo owner (id 2) signs in 200 and reads its spaces 200; suspended 204; **the same token's next request 401; its refresh 401** (the web's chain: the session ends); its space `isVerified: true`; restored 204; signs in again 200;
- a user (id 7) promoted to ADMIN 204, then demoted with the seed admin present 204;
- the last admin demoting or suspending themselves: 409 `OWN_ACCOUNT` (`LAST_ADMIN` is reachable only in the race, proven in the API lane, as the plan said);
- promoting the linked owner: 409 `ACCOUNT_HAS_LINKS`;
- a temporary password for user 7: 200, `Cache-Control: no-store`, 12 characters; its handover 204; the old password 401; sign-in with it 200 `mustChangePassword: true`; the next request 403 `PASSWORD_CHANGE_REQUIRED`; the forced change 200.
- The server, its `tsx watch` and its log pipe stopped; port 3321 checked free.

**Not run:** E2E (end of project); screenshots (no UI change).

## 4. The breaks, and the tests seen failing first

**Seen failing first:** the guard's unit tests (4 red), the role change's API tests (15 red: no route), the temporary password's (9 red: no route).
**Written after their code** (an order slip on my side), each proven by breaking what it guards: the guard's API tests, the suspension's tests.

Every break ran through a script that restores the files byte for byte; each restore was checked.

| Break | Fails |
|---|---|
| The guard reads no account | all 5 guard API tests |
| The reader answers a stale role | promotion and demotion (2) |
| No suspended check / no unknown-id check (guard) | their unit test each |
| The `role` claim back in the token | "carries who and the pending claim, and no role" |
| A trigger that refuses nothing (governorates) | both audit-rollback tests |
| Admin-set lock removed (suspension) | `LAST_ADMIN` race |
| Admin-set lock removed (role) | `LAST_ADMIN` race and the promotion-waiting-on-a-link race |
| Links counted before the lock | the promotion race |
| #60's person lock removed from a link | the link-waiting-on-a-promotion race |
| A deactivated link counted | "a person whose links have all ended" |
| The last-admin check removed | the `LAST_ADMIN` race |
| S4's lock and check removed | the password change racing a suspension |
| S5 removed / idempotency removed / self-refusal removed | their test each |
| Temporary password: session lock removed | "an account suspended while the issue waited" |
| `no-store` removed / reset links kept / Google-only check removed / the password in the audit entry | their test each (the last, 2) |

**Two breaks did not fail as planned** (as #60's B5a): removing the lock *alone* from the suspension, or from the temporary password, leaves the "session opened while it waited for the lock" tests green. The change's own `UPDATE` of the row waits for the other transaction, and the revocation runs after it, so no session survives. Those tests fail once the revocation also moves before the write (lock removed + revoke first). So they guard the order write-then-revoke; the explicit lock is guarded elsewhere: by the `LAST_ADMIN` race for the suspension, and, for the temporary password, by a test the plan did not list, added for this: *an account suspended while the issue waited is refused* — it fails with the lock removed, since the lock keeps the checks (suspended, Google-only) true until the write.

## 5. Problems met, and how each was solved

- **A break restored the wrong file.** After the first guard break I restored with `git checkout --`, which brought back the committed guard, not my edit. Restored from the backup taken just before the break and re-ran the tests; from then on every break went through a script that restores byte for byte.
- **Two governorate tests** made their audit insert fail with a token that outlived its account; the new guard refuses that token (401) first. They now refuse the insert with a temporary trigger on `audit_logs` (dropped in `finally`; the lane runs one file at a time); proven by a trigger that refuses nothing.
- **The forced-change test's probe app** wired `createRequireAuth` without a reader; it now uses the real `GET /manage/spaces`.
- **Heredoc edits failed to parse** once; edits moved to scratchpad Python files.
- **Docker Desktop stopped** between sessions (overnight); restarted it and ran `docker start masaha-postgres-1`, not `db:up` (finding 48).

## 6. Anything that behaved unexpectedly

- The two breaks of §4 that did not fail as planned.
- **The real run's first owner** (ids 5 and 6, #60's real-run accounts) does not sign in with the demo password; the chain was rerun with the demo owner (id 2). Neither is a defect.
- **A side effect on dev data:** user 7 (`plain-user-…@example.com`, #60's real-run account) now has the demo password, set through its forced change.
- **`npm run dev` stopped by its task** left its `tsx watch`, the server child and `pino-pretty` running, holding 3321; stopped by PID, port checked free. Worth knowing for every worker that stops the API this way.

## 7. The early conflict check

| PR | Head | Result |
|---|---|---|
| #61 `design/admin-editor` | `7aa5087` | clean (`git merge-tree --write-tree`); it touches only `docs/design/` |

`main` has not moved since `d7d800e`.

## 8. Departures from the prompt

- **ADR 0002 got a *Revised* line** (rule 6 said the access token carries the role for `requireRole`), not in the prompt's list of documents: needed for it to stay true.
- **The test helpers:** `test/admin.ts`'s `signIn` takes an optional email (a second admin in one test); a new `test/locks.ts` holds rows while a request waits (the races of three files). `sessionLock.api.test.ts` keeps its own helper (no drive-by refactor).
- **The users service takes the clock** (`now`, conventions §11) for the suspension's time; its unit test passes one.
- **One test beyond the plan:** the temporary password's "suspended while the issue waited" (§4).
- **The expectations changed by D5**, each with why: the suspended `/me/password` case 403 `ACCOUNT_SUSPENDED` → 401 (S3: the guard refuses first); the register test's token claims without `role` (S2); the forced change's probe → the real route (its last expectation `{ userId }` → `{ success: true, data: [] }`); the two governorate rollback tests' provocation (expectations unchanged); 15 token-signing sites without `role`.
- The documents' decision lines are dated 2026-10-11, the day the item started; the work finished on 2026-10-12.

---

# Review fixes — round 1 (from `REVIEW62_CLAUDE_REPORT.md`, `PROMPT\USERS_FIXES.md`)

## 1. The pull request

#62, new head **`aa08e6f10145f0a4215878c8ca23383a23e743e8`** · CI green on that head (the same 10 checks) · GitHub `CLEAN`. One "Review fixes" comment: https://github.com/Basel-Ghonaim/masaha/pull/62#issuecomment-6122977683. The PR description updated to the final state.

## 2. The commits

Still five; each fix folded into the commit it corrects (fixup + autosquash on the PR's own base `d7d800e`, `main` unchanged), pushed with `--force-with-lease`:

1. `4fad251` docs(workflow): a merge apart needs no new CI run — unchanged.
2. `54e2478` feat(api): read the account on each signed-in call — R1, R2, R3 (finding 51, security.md's token row).
3. `1280d41` feat(users): suspend and restore an account — R3 (conventions §13), R4 (finding 52).
4. `37cc2c8` feat(space-links): change a person's role — rebased only.
5. `aa08e6f` feat(users): issue a temporary password — rebased only.

## 3. What was run

Once each on `aa08e6f`: `test:unit` (shared 158, API 660, web 724), `test:api` (40 files, 665: the whole lane), `lint`, `typecheck`, `format:check`, `check:links` — all clean. Not run (not asked by the fixes prompt, no web code changed): `test:component`, the build and `check:build`; CI ran them green on the head.

## 4. The breaks, and the tests seen failing first

- **R1:** the guard's unit case "answers 401, with no code, when only the account says a change is pending, even where one is allowed" and the API test "refuses a token signed before a temporary password with 401, the change included" (the password replaced and the flag set, as the issue leaves them) were changed first and seen failing (1 red each) before the guard's fix. A new API test, "holds a token signed while a change was pending to the change alone", passed before and after: it pins the 403 that stays.
- **R2:** with a trigger and function planted in `masaha_b_test` as a killed run would leave them, the old helper failed 10 tests (its `CREATE FUNCTION` fails, so the leftover stays and refuses every audit insert); the new helper ran over the same leftover and dropped it (0 triggers, 0 functions left).

## 5. Problems met

- Docker Desktop had stopped again; restarted it and ran `docker start masaha-postgres-1` (not `db:up`, finding 48).
- `gh pr view` showed the old head right after the push; `git ls-remote` confirmed `aa08e6f` on the remote.

## 6. Anything that behaved unexpectedly

- **R2's fix leaves one window open:** with the prompt's fix, the helper cleans a leftover only when it is first called. In the run of the file that follows a killed run, the four tests before its first call still failed while the planted trigger was there (seen: 4 red, then clean). Any other file run before it would fail the same way. Not fixed, as the prompt's fix was built exactly; the review's stronger option is one line in the lane's global setup (`test/global-setup.ts`): `DROP TRIGGER IF EXISTS refuse_audit ON audit_logs` and `DROP FUNCTION IF EXISTS refuse_audit()` before any file runs. The owner decides.
- **A timeout once:** in the first batch run after the database restarted, `issueTemporaryPassword.api.test.ts` › "opens a session that must change the password, and takes the handover" failed at 5.26 s (the 5 s default; four bcrypt hashes at cost 12). It passed alone and in every later run, the whole lane and CI included. Worth a longer timeout if it shows again.
- `users.api.test.ts`'s skipped-current-password table lost its account-pending row: that case now ends at the guard (401), proven in `requireAuth.api.test.ts`; the service's double check stays.

## 7. The early conflict check

| PR | Head | Result |
|---|---|---|
| #61 `design/admin-editor` | `1a08fcf` | clean |

The amenities item's PR is not open. `main` is still `d7d800e`.

## 8. Departures from the prompt

None. The global-setup cleanup (§6) is proposed, not built.

## Addition — the leftover trigger in the lane's global setup (approved)

- **Change:** `apps/api/test/global-setup.ts` drops any leftover `refuse_audit` trigger and function (`IF EXISTS`) once, after the migrations, before any file runs. Folded into `feat(api): read the account on each signed-in call` (R2's commit). This closes the window of §6 above: no file now starts with every audit entry refused after a killed run.
- **Commits:** still five: `4fad251`, `66711c7` (the guard, R1, R2 and the setup), `e3a983b`, `faefb06`, **`18e0edc`** (the new head, pushed with `--force-with-lease`). `18e0edc` differs from `aa08e6f` by `test/global-setup.ts` only (`git diff --stat aa08e6f 18e0edc`).
- **Run:** with a trigger and function planted in `masaha_b_test` as a killed run would leave them, `test:api` once: 40 files, 665 passed, and none was left afterwards (before this change, the same plant failed 4 tests in the governorates file). Prettier and ESLint on the changed file. Nothing else run, as asked.
- **The Review fixes comment** was updated in place with this addition and the new head.
- **Not waited for:** CI on `18e0edc`; a fresh independent review follows.

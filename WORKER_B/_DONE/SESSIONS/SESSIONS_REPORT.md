# SESSIONS — report (findings 51, 20, 16, 39 · API)

Worker B · `masaha-b` · branch `feat/session-ends` · 2026-10-13

## 1. Pull request and head

- **PR #78**, `feat(sessions): end a session when it should`: https://github.com/Basel-Ghonaim/masaha/pull/78
- Labels `feat`, `area:api`, `area:docs`; assigned to the owner. Not merged.
- **Head:** `fe233f836eb7082a5901a128dd6fe14fff43b8d8`.
- CI passed on that head: build, check:classes, check:links, format:check, lint, test:api (4m7s), test:component (4m34s), test:unit and typecheck.
- GitHub shows `CLEAN`.
- Based on `origin/main` `3c3dc47`, which has not moved since.

## 2. Commits

1. `f09bd6ec` `refactor(users): hash passwords in the module` — finding 39. The `passwords` parameter is gone. The comparison rule is unit-tested on `verifyPassword`. The service tests that used fake passwords are removed, because each already had its twin in the API lane.
2. `c8e612fb` `feat(sessions): end a session 30 days on` — finding 20.
   - The one migration, `20261013111955_session_ends`, adds both columns.
   - Backfill: every existing family gets the migration's time + 30 days (S6).
   - The deadline is copied on each rotation, refused at the lock, and the family deleted.
   - A sign-in or a refresh sweeps rows past their deadline (S3).
   - The `profileUpdatedAt` comment drops "and photos" (D6).
3. `3940436c` `feat(auth): end access tokens with their session` — finding 51.
   - The `sessionVersion` claim, and the version check in `requireAuth`.
   - `users.endSessions` is the only path to `sessions.revokeAll` (S5). It covers a password change, a reset, a suspension, a role change, the temporary password, a Google link (S2) and the refused refresh.
   - The pending check is kept (S1 rejected by the owner).
4. `fe233f83` `feat(auth): wait as a send would when none is made` — finding 16.
   - `NO_SEND_WAIT` is 1.5–3.0 s, drawn anew with `crypto.randomInt`.
   - The wait applies to forgot and to resend (S4), and only when nothing was delivered (S7).
   - The `wait` port takes 4 lines in `app.ts` (O1).
   - Finding 65 is recorded.

Documents: security.md; ADR 0003 *Revised*; ADR 0017 *Revised*; the data model; conventions §2, R5, §11, §12, §13 and the header; the contract (§1, *Me*, *Users (the admin)* role and suspended); users.md and auth.md (decisions, history `#78`, open findings, code map); findings 16, 20, 39 and 51 resolved, 65 opened, and the index.

## 3. What was run, and what was not

**Locally, once each, one at a time, on the head before the `#78` rewrite.** The rewrite changed documents only, and format and links were run again after it.

| Check | Result |
|---|---|
| `test:unit` | shared 205, api 664, web 734: all passed |
| `test:api` | 738 tests in 44 files, all passed (277 s) |
| `lint`, `typecheck` | clean |
| `format:check`, `check:links` | clean (2,000 links in 112 documents) |

**Before each full lane** I checked that no other folder was running vitest. Earlier in the item, I waited once for the media worker's full API lane to finish.

**Real requests against 3321**, with `EMAIL_MODE` as found (log); a fresh account was registered for them:

| Request | Answer |
|---|---|
| Laptop token before / after a password change on the phone | 200 / **401** |
| Phone's old token after its own change | **401** |
| Phone's new token (the changer) | **200** |
| Token before a suspension / after it | 200 / **401** |
| Same token after the restore | **401** |
| A new sign-in after the restore | 200 |
| A token of the old shape (no `sessionVersion`) | **401** |
| The refresh the web then makes, and its new token | 200, 200 |
| Refresh before the deadline | 200 |
| Rows of a family past its deadline after a sign-in | 0 (swept) |
| Refresh with `session_ends_at` set in the past | **401**, family rows 0 |

Forgot answer times (ms), 8 runs each, side by side. The rate limits were cleared in `masaha_b_dev` before each run:

| Run | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Real account (log mode: link logged, no relay) | 60 | 60 | 43 | 38 | 41 | 39 | 52 | 42 |
| Unknown address (waits 1.5–3 s) | 1944 | 1643 | 2730 | 1650 | 2464 | 2419 | 1658 | 2516 |

In log mode this is the reverse tell security.md names: development only.

The server was stopped (TaskStop, then the two leftover `server.ts` node processes by PID), and port 3321 was checked free.

**Not run:**
- `test:component`, `build` and `check:build`: nothing the web imports changed (no edit in `apps/web` or `packages/shared`). CI ran test:component and build anyway, and both passed.
- **A real SMTP send:** this folder's `.env` has the SMTP key names, but `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD` and `EMAIL_FROM` are empty (length 0). With `EMAIL_MODE=smtp` the API refused to start ("Required with EMAIL_MODE=smtp"), so no email left. The owner then chose the documented estimate.

## 4. Breaks made, and tests seen failing first

Each break was made once by hand, its test seen failing, and the file restored from a backup copy, then run green again:

| Break | Failed |
|---|---|
| `verifyPassword` returns early without a hash | `password.unit` (0.9 ms vs ≥ 40 ms) |
| The deadline renewed on rotation instead of copied | `auth.api` "ends a session 30 days after its sign-in…" |
| The deadline check removed from `rotate` | the same |
| The sweep's `sessionEndsAt` condition removed | `auth.api` "deletes a session past its end…" |
| The version comparison removed from `requireAuth` | `requireAuth.unit` (new test) |
| `verify` accepting a missing or invalid `sessionVersion` | `accessToken.unit` (new test) |
| No version raise in `endSessions` | 6 API tests: password change, reset, suspension restore, admin role, owner links, Google |
| The changer's token signed with the account read before the raise | `users.api` (2 tests) |
| The Google session read before the raise | `google.api` (3 tests) |
| Logout calling `endSessions` | `auth.api` (2 tests) |
| Login signing with the account read before the lock | `sessionLock.api` race test |
| No wait for a suspended address | `password.api` forgot wait test |
| A fixed delay | `password.api` "draws each wait anew" |
| A wait after a delivered email | `password.api` (2 tests) |
| No wait on resend | `password.api` resend wait test |

**By design:** with the version raise removed, the temporary-password test still passes. The pending check you kept refuses that token too: two guards for one case.

The new tests were written alongside code that already existed in my tree, so each was proven by reverting its code once, as testing §3 rule 5 allows.

## 5. Problems met, and how each was solved

- **`git checkout` wiped uncommitted code.** While making the deadline breaks, I restored files with `git checkout`. That reset `sessions.service.ts` and `sessions.repository.ts` to HEAD and wiped the uncommitted D3 code. The two later breaks therefore ran against the wrong code and proved nothing. I reapplied the edits from the saved script, redid all three breaks with backup copies, and every later break used backups. Saved as a memory.
- **Python on Windows wrote CRLF.** My edit scripts converted two files to CRLF (git warned). I converted them back to LF and passed `newline=''` from then on.
- **A heredoc failed to parse** in Git Bash on one long edit script. I moved the scripts to scratchpad `.py` files.
- **Typecheck after the schema change:** six API test files insert refresh tokens directly, and the new column is not null. Each fixture gained `sessionEndsAt`. Two of these files are in `space-links`, outside the plan's list (§8).
- **Typecheck after the claim:** tests and two shared helpers (`test/admin.ts`, `test/spaces.ts`) sign tokens directly. They now pass `sessionVersion`; the helpers pass the account's own.
- **`app.ts` default for the timer:** to stay within about three lines, the default is `new Promise((resolve) => setTimeout(resolve, ms))`, with no import. The total is 4 lines with the doc comment.
- **The SMTP values were empty:** I asked the owner (§3). I first picked "fill the values" by mistake, then the owner corrected to the estimate. `EMAIL_MODE=smtp` was added once and removed at once; the `.env` is as found.

## 6. Anything unexpected

- **`requireAuth.api.test.ts`** changes the account directly in the database, so its role tests are untouched: they prove "the account now", not the end of sessions. The plan said both would change to 401. Instead, the version tests go through the real endpoints, in the files that own them.
- **The `POST /admin/spaces/:id/owners` link answers 204, not 201.** My first test assumed 201.
- **The first unit run** of my touched folders reported 418 tests; vitest's path filters took in more files than I expected. It was harmless.
- **The development database** keeps the account registered for the real requests (`real-…@example.com`), and some password-recovery rows. The log file in the scratchpad holds dev-only reset links.
- **The media worker's PR #77 edits `apps/api/test/spaces.ts` too,** and `git merge-tree` merges it cleanly with this branch.

## 7. Early conflict check (`git merge-tree --write-tree`, head `fe233f83`)

| PR | Head | Result |
|---|---|---|
| #77 `feat/space-photos` | `9bc0b705` | **conflict in documents only:** `docs/architecture/findings/README.md` and `docs/backend/conventions.md` (the header's *Built* line, and the §12 table's end, where my *Timer* row meets their storage paragraph). `apps/api/src/app.ts`, `test/spaces.ts`, the contract, the data model and security.md all **merge cleanly** |
| #76 `design/owner` | `5a226763` | clean |
| #75 `design/account` | `f100a287` | clean |
| #74 `feat/admin-space-editor` | `e858f16b` | conflict in `docs/architecture/findings/README.md` only |

Every conflict is in documents, so the second to merge takes the fast path: keep both sides, `format:check`, one push. The `app.ts` lines do not conflict with #77 as it stands.

## 8. Departures from the prompt and the plan

- **Finding 16's bounds are an estimate, not a measurement** (the owner's correction). The SMTP values were empty, so no send was timed.
- **Finding 65's title** is "The forgotten password's wait is an estimate, not a measurement" instead of the reply's "…was measured from a development machine", which would no longer be true. Its *Resolves when* is as the reply asked.
- **No pure helper or unit test for the draw.** `drawNoSendWait()` is a one-line `crypto.randomInt` within `NO_SEND_WAIT`. A helper taking the random source as a parameter would be one only tests pass (testing §3 rule 2). The bounds and the jitter are proven in the API lane, with breaks for a fixed delay and for wrong waits.
- **Two planned tests dropped as redundant** (one behaviour, one lane):
  - "a password change's new session gets its own 30 days": the auth test proves `issue` gives 30 days, and the change calls `issue`;
  - the race "a refresh that waited on a password change": once the change commits, the refresh's own token is already deleted, so the existing test "keeps a refresh waiting on a revocation from renewing the session" proves it, and a version check would add nothing.
- **Test placement:** the token tests for the admin's role change, the owner links and the temporary password are in `adminRoles.api`, `adminOwners.api` and `issueTemporaryPassword.api` (the files that own those endpoints), not in `requireAuth.api.test.ts` as planned.
- **Files outside the plan's list, all small and owned by no other open item:**
  - `src/modules/space-links/space-links.api.test.ts` and `admin-roles/adminRoles.api.test.ts`;
  - `src/modules/spaces/space/space.api.test.ts`: one signed token. It sits under `modules/spaces/` but is not in the media worker's list, and it merges cleanly with #77;
  - `test/admin.ts` and `test/spaces.ts`.
- **`app.ts`:** 4 lines rather than 3, the extra one being the doc comment; all in commit 4 only (O1).
- **Docs cite `#78`.** The docs were written with the placeholder `#PRNUM`, then each commit's tree was rewritten with `git filter-branch` just before the push; the number was confirmed by `gh pr create`.

---

# Review fixes — round 1 (with the rebase after #77)

## 1. Pull request and head

- PR #78, new head **`563a7d686494ccf5053692a03f7a2f80121b60a5`**, on `origin/main` `a7d52f25` (#77 merged).
- CI passed on that head: build, check:classes, check:links, format:check, lint, test:api (4m15s), test:component (5m24s), test:unit and typecheck.
- GitHub shows `CLEAN`.
- One "Review fixes" comment posted: https://github.com/Basel-Ghonaim/masaha/pull/78#issuecomment-6148346475
- PR description updated (the summary of 20, a new acceptance line, the evidence counts, the new break). Not merged.

## 2. Commits

1. `6424b3fd` `refactor(users): hash passwords in the module` (45)
2. `7ab30cf8` `feat(sessions): end a session 30 days on` (40) — the fix is folded here (fixup + autosquash)
3. `e233fcbf` `feat(auth): end access tokens with their session` (48)
4. `563a7d68` `feat(auth): wait as a send would when none is made` (50)

**The fix:** a refresh past the deadline deletes the family whatever the token's own expiry.
- `rotate` checks `sessionEndsAt` before `expiresAt`.
- `auth.refresh` finds the holder through `holderOf` (expired or not) instead of `ownerOf`, which is removed.
- The new `auth.api` test is named "ends a session past its end even when the token presented is past its own 7 days".
- security.md (*Session*) and auth.md (the decision) each gained "whatever the token's own expiry".

## 3. What was run, and what was not

**Once each, on the new head; neither other folder was running a lane:**

| Check | Result |
|---|---|
| `test:unit` | shared 208, api 718, web 768: all passed |
| `test:api` | 791 tests in 47 files, all passed (427 s) |
| `lint`, `typecheck` | clean |
| `format:check`, `check:links` | clean (2,052 links in 116 documents) |

**Not run:**
- `test:component`, `build` and `check:build`: nothing the web imports changed (CI ran test:component and build, both passed).
- No new real request: the fix is proven by the API test on the real database.

## 4. Breaks made, and tests seen failing first

The new test was seen failing three times, each with "expected 1 to be +0": one row of the family survived.

| Code | New test |
|---|---|
| The old code | fails |
| The review's reorder alone | fails |
| The break: the old order, with `holderOf` in place | fails |
| Restored | passes |

## 5. Problems met, and how each was solved

- **The proposed fix was not enough on its own.** `auth.refresh` gated on `ownerOf`, which refused an expired token before the lock, so `rotate` never saw it. I proved this by running the new test with only the reorder, then added `holderOf` in refresh. `rotate` keeps refusing an expired token under the lock.
- **The rebase** conflicted in documents only:
  - the findings index: 63 and 64 from #77, then 65, keeping both;
  - `conventions.md`: the *Built* header merges #77's storage port with "the clock and the timer of §11", and my *Timer* row stays in the §12 table, followed by #77's storage paragraph.
  - `app.ts` and `test/spaces.ts` merged cleanly.
- **The autosquash** conflicted twice on the same auth.md line, because commit 4 adds the next line. I kept the amended line in commit 2, and the amended line plus commit 4's decision in commit 4. The final tree differs from the rebased head by exactly the fix (6 files).
- **After the rebase, typecheck failed on `multer` and `sharp`,** which #77 added. `npm ci` (with Prisma's postinstall generate) and a rebuild of `packages/shared`'s `dist` fixed it. That was an environment gap, not a code conflict, so lint and typecheck were then clean.

## 6. Anything unexpected

- The reviewer's fix, as written, would not have changed the behaviour it targets (§5).
- `20261013111955_session_ends` is still the latest migration after the rebase.

## 7. Early conflict check (head `563a7d68`)

| PR | Head | Result |
|---|---|---|
| #76 `design/owner` | `5a226763` | conflict in `docs/design/CHANGES.md`, `INDEX.md`, `README.md` and `prototype/Flows - states.html`. These are **#76's conflicts with `main` itself** (`git merge-tree origin/main` gives the same four); this branch touches nothing in `docs/design/` |

#74, #75 and #77 are merged.

## 8. Departures

- **Beyond the review's text:** `auth.refresh` now uses `holderOf`, and `ownerOf` is removed. Without that, the reorder alone does not delete the family (shown by the test). As a result, a refresh with a known but expired token now counts under the refresh limit and takes the user's lock before it is refused, as a logout already does. The security.md *Refresh* limit row still holds: "every refresh, by the user its cookie belongs to".

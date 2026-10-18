# OWNERS — report

Worker B · `masaha-b` · branch `feat/admin-owners` · 2026-10-11

## 1. Pull request and head

- **PR:** [#60](https://github.com/Basel-Ghonaim/masaha/pull/60), `feat(space-links): add the admin's owners`.
  - Labels: `feat`, `area:api`, `area:docs` and `area:web`. Assigned to the owner.
- **Head:** `ca3d42b98167fbbced18e976bfbbc15a92033b66`, cut from `origin/main` at `b66ddfe`.
- **CI:** every check passed on that head (build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck). GitHub shows `CLEAN` and `MERGEABLE`.
- **Not merged.** An independent review follows (authorization, security and transactions).

## 2. Commits

1. `3e28cce` **fix(spaces): decide on the links under the lock**
   - The loaded space gains `linksUnder(tx)`; a save re-reads the links under the space's lock.
   - The read takes the lock in share mode.
   - Its race tests, conventions §8 and §13, and spaces.md.
2. `2c0b1b6` **feat(space-links): list the users for the admin**
   - `GET /admin/users`, composed in `space-links` over `users.page`.
   - Each row has `signIn` and `joinedAt` (S2).
   - The contract, the plan's table, space-links.md and users.md.
3. `d84f500` **feat(space-links): link and unlink the admin's owners**
   - Link and unlink, the role rule (`ownerRoleFor`) and `users.changeRole` with its revocation.
   - `ACCOUNT_IS_ADMIN` and `RECEPTION_LINK_ACTIVE`; `OWNER_ALREADY_LINKED` removed (S3).
   - The reception row's `before: { role: "RECEPTION" }` (the owner's addition).
   - Documents: security.md's revocation, ADR 0009 *Revised*, data-model, and conventions §13's lock order. Finding 43 resolved.
4. `af24445` **feat(space-links): add an owner with a temporary password**
   - `POST /admin/owners`, the generator, `EMAIL_HAS_ACCOUNT` and `ALREADY_OWNER`.
   - `no-store`, and the logger's redaction of `temporaryPassword`.
   - security.md › *Passwords*, and finding 49.
5. `49bdb41` **feat(users): record a temporary password's handover**
   - The handover endpoint and `TEMPORARY_PASSWORD_NOT_PENDING`.
   - overview's *Built* line.
6. `ca3d42b` **refactor(api): read the signed-in claims from shared/auth**
   - Finding 25, folded as its own last commit, as the owner asked.

## 3. What was run

**On the head's code, once each, one at a time:**

| Check | Result |
|---|---|
| `test:unit` | 158, 654 and 724 passed, one count per workspace, as the lane prints them |
| `test:component` | 786 passed (see §6) |
| `test:api` | 601 passed, on `masaha_b_test` |
| `NODE_ENV=production npm run build` and `check:build` | clean: no showcase, dashboard or heavy library in the first download |
| `lint`, `typecheck`, `check:classes` | clean |
| `format:check`, `check:links` | clean (1,880 links) |

These ran on `be170d9`. The head `ca3d42b` differs from it only in the PR number (#59 → #60) in five documents. After that change, `format:check` and `check:links` ran again, which is workflow phase 4's exception for documents. CI then ran every lane on `ca3d42b`.

**Real requests against the API on 3321** (`masaha_b_dev`, the seeded admin, with users the script registered and three spaces it created):
1. **A new owner with a space:** 201, `Cache-Control: no-store`, a 12-character password with a letter and a digit.
   - The space went from unverified to verified.
   - The new owner signed in with the password: 200, `mustChangePassword: true`, `OWNER`.
   - The handover answered 204.
2. **An email with an account:** 409 `EMAIL_HAS_ACCOUNT`.
   - With `upgradeExisting`: 201 and `temporaryPassword: null`; the name kept; `OWNER`; one space.
   - Their session ended: refresh answered 401.
3. **A plain user linked from a space:** 204, `OWNER`, the space verified. Their refresh answered 401.
4. **One more space linked** (two spaces), **then one of the two unlinked:** 204. The role stayed `OWNER`, that space became unverified, and the session's refresh still answered 200.
5. **The last unlinked:** 204, `USER`, the space unverified.
6. **`GET /admin/users?role=owner&q=<run>`:** 200, the two owners with their spaces.
7. **Refusals:** the demo space's reception answered 409 `RECEPTION_LINK_ACTIVE`; the admin answered 409 `ACCOUNT_IS_ADMIN`.

**Cleanup:** the server's log holds no `temporaryPassword` field. The API and its `tsx watch` parent were stopped, and port 3321 was checked free. The dev database keeps the users and spaces the script created (suffix `mv3nfaoc`).

**Not run:**
- E2E, which waits for the end of the project;
- the web dev server and screenshots, since no screen changes.

## 4. Breaks made, and tests seen failing

Each break was applied once by a script that backed up the file, ran the test that must catch it, and restored the file.

| Break | Test that failed |
|---|---|
| A save decides on the loader's links, not `linksUnder` (43, half 1) | hours › refuses the admin when an owner joined while the save waited |
| The read without `FOR SHARE` (43, half 2) | space › waits for a change in progress and answers it whole |
| `spaces.lock` without `FOR NO KEY UPDATE` | owners › waits for the space's lock |
| Unlink counts before the person's lock (S5) | owners › makes a person a user again when their two links end at once |
| Link without the person's lock **and** revoking before the role is written | owners › ends a session a sign-in opened while the link waited |
| The temporary password in an audit entry | owners › no log line and no audit entry |
| Two changes together: the controller logs its answer (`req.log.info({ added })`), and `temporaryPassword` is removed from `SECRET_FIELDS`. The redaction alone is proven in the unit lane since the review fixes (§9) | owners › no log line and no audit entry |
| No space check on creation | owners › refuses a soft-deleted or unknown space on its field |
| Handover without the pending check | handover › refuses once the temporary password was changed |
| The reception row audited as a plain link | owners › makes a deactivated reception link an owner's |
| The users list keeps deactivated links | users › gives an owner only their active owner links |
| No `Cache-Control` | owners › creates an owner's account… |
| Unlink without the role rule | owners › ends the last owner link |
| `ownerRoleFor` without its admin guard | `ownerRole.unit.test.ts` (2 failed) |
| The generator without its policy check; length 10 | `temporaryPassword.unit.test.ts` |
| The loader ignoring `tx` | `spaceLinks.unit.test.ts` |

**Two controls passed, as intended:**
- the role written before the revocation, with the person's lock kept;
- the answer logged while its field is still redacted.

**Order of work.** The code of each commit was written before its tests, because Docker was down while the commits were made (§5). Every test above was therefore proven by reverting its code once (testing §3 rule 5's second form). The remaining assertions of the list and refusal tests were not each broken one by one. Their behaviours share the code that the breaks above exercised.

## 5. Problems met, and how each was solved

- **Docker Desktop was not running** for most of the build, and stopped again after the session restarted.
  - The commits were made with lint and typecheck clean. The API lane and the breaks then ran once the database was up.
  - The shared container (the main folder's compose project) had exited. I started it with `docker start masaha-postgres-1`, never `db:up` from this folder (finding 48).
- **A break restored with `git checkout` lost my edit** to `spaceLinks.ts`. I rewrote the file from the conversation. From then on, every break used a backup copy.
- **Edits through Python wrote CRLF** (text mode on Windows). I converted the files back to LF; later scripts write with `newline=''`.
- **One heredoc failed to parse.** Long scripts went to scratchpad files from then on.
- **One edit script applied twice.** Its idempotency check failed because the new text contained the old. The duplicates were removed before the commit; the typecheck caught them.
- **Two code-map trims landed in commit 6.** They went back, by fixup and autosquash, to the commits that last touched those lines (4 and 5).
- **Two style faults found in self-review:** a doc comment past 100 characters, and an `if` without braces. Both were folded into commit 4.
- **The PR number:** #59 was taken by worker A's design PR, opened meanwhile. My documents cited #59. I rewrote it to #60 in the five documents across the six commits with a tree filter. Only those 22 lines changed, which I checked by diff. PR #60 then confirmed it.

## 6. Unexpected behaviour

- **A first `test:component` run on `be170d9` failed 19 tests** in 12 files this branch does not touch. Each file took 20–55 s, against seconds normally, and the machine was under load.
  - One failing file passed alone, and the whole lane then passed 786/786 alone.
  - The cause was not proven beyond load: I did not keep that run's failure messages. It is close to findings 28, 42 and 47.
- **The named break of the refresh race did not fail** (B5a: the person's lock removed alone). Without the explicit lock, the role's `UPDATE` itself waits for the user's row. The revocation that follows then still sees the new session.
  - The test fails only when the lock is gone **and** the revocation comes before the role is written (B5b). It passes when the revocation comes first but the lock is kept (B5c).
  - So the explicit lock is what makes the order inside `changeRole` free. The test proves that property. Its break is not the single change the plan named.
- **Plan's B6, the hash audited, did not fail:** the hash holds no plain password. The real breaks, the plain password audited and the answer logged without redaction, both failed.

## 7. Early conflict check

| Open PR | Head | `git merge-tree --write-tree` against `ca3d42b` |
|---|---|---|
| #59 `design: apply the shared layer's decisions` (worker A) | `ac25093` | clean (it touches only `docs/design/`) |

## 8. Departures from the prompt and the plan

- **D5's 404 for the space in `POST /admin/owners` is 422** `errors.spaceId = ["invalid_choice"]`: the owner's S4. The path routes keep the 404.
- **The space's read is consistent through a share lock, not a snapshot:** the owner's S1. Conventions §13 now says a future writer of a space's facts or links takes the lock.
- **Conventions §13's link parts went into commit 3, not commit 1**, so commit 1 claims nothing not yet built.
- **The refresh race's break** is the two-part one (§6).
- **The PR number** is #60, not the #59 the plan assumed (§5).
- **Not built, as agreed:** suspension, `PATCH /admin/users` and the admin's temporary password; reception links; `status=deleted`.

## For the owner

- **Approve the Arabic of the five new codes,** listed in the PR description.
- **New finding 49:** a lost answer to adding an owner loses its temporary password until the users item can issue another.

## 9. Review fixes (round 1, from `OWNERS_FIXES.md`)

### 9.1 Pull request and head

- **Head:** `b47530899f6e5ad90a2eb77039fe91a31a57b92c`, pushed with `--force-with-lease` over `ca3d42b`.
- **CI:** every check passed on that head. GitHub shows `CLEAN` and `MERGEABLE`.
- **The PR:** one *Review fixes* comment posted ([#issuecomment-6109990180](https://github.com/Basel-Ghonaim/masaha/pull/60#issuecomment-6109990180)); the description updated to the final state.

### 9.2 Commits

Each fix was folded into the commit it corrects (fixup and autosquash). R1 then reworded four subjects with a message filter, which leaves the tree untouched; I checked by diff.

| Commit | Subject | Characters |
|---|---|---|
| `259de10` | fix(spaces): decide on the links under the lock | 47 |
| `fadecfa` | feat(space-links): list the users for the admin | 47 |
| `fa1a615` | feat(space-links): link and unlink owners | 41 |
| `7c70ac9` | feat(space-links): add an owner's account | 41 |
| `19ea0b2` | feat(users): record the password's handover | 43 |
| `b475308` | refactor(api): share the signed-in claims helper | 48 |

**Where each fix went:**
- **Commit 1:** the conventions header (R7).
- **Commit 2:** R2.
- **Commit 3:** R6: the two narrowed lines, the consequence and its way out, and finding 50 with its index line.
- **Commit 4:** R3, R4 and R5, and R7's lines about adding an owner:
  - space-links' authority, *Who uses it*, the lock sentence and the shared code map;
  - users.md's "an account the admin creates";
  - conventions' order line, and the service's doc comment.
- **Commit 5:** users.md's authority, *Who uses it* and shared code map (R7).
- **Commit 6:** finding 50 in space-links' *Open findings*.

### 9.3 What was run

On `b475308`, once each, one at a time:
- `test:unit`: 158, 656 and 724 passed;
- `test:api`: 606 passed;
- `lint`, `typecheck`, `format:check` and `check:links`: clean (1,889 links).

**Not run:** the component lane and the build, since no web code changed, as the fixes file says. CI ran both on the head and passed.

### 9.4 Breaks made, and tests seen failing

| Fix | Break | What failed |
|---|---|---|
| R2 | the count without its `where` | 7 tests: the search and the six role and state cases |
| R3 | `!upgradeExisting` moved above `assertMayOwn` | the three refusals without the flag |
| R4 | the concurrent-creation branch removed (a 500) | "refuses an email another creation took while this one waited for the space" |
| R5 | `temporaryPassword` removed from `SECRET_FIELDS` | its unit case |
| R5 | `newPassword` removed (a case that was missing) | its unit case |

Each test passed once its code was restored.

### 9.5 Problems met

- **The autosquash stopped twice, both times in the findings index.**
  - My R6 fixup had been written on a tree that already held finding 49, and it put 50 *before* 49.
  - I resolved commit 3 with 48 then 50, and commit 4 with 49 then 50.
  - The result differs from the pre-rebase tree only in that order, now correct. I checked by diff.
- **R5's widened `it.each` was not formatted by Prettier.** `format:check` found it; it was formatted and folded into commit 4.

### 9.6 Unexpected

- **#59 merged at 14:25:37 UTC, five minutes after this head's CI run started** (14:20:48 UTC). So CI has not run against `main` as it is now.
  - #59 changed 46 files, all under `docs/design/`, and none of this branch's.
  - `git merge-tree` against the new `main` (`43bb7a7`) is clean, and GitHub shows `CLEAN`.
  - Workflow §9 rebases only on a conflict, and leaves ready a clean PR whose CI ran after `main`'s last change. This case is neither, so I did not rebase. **The owner's call:** leave it as it is, or have me rebase onto `43bb7a7` and run CI again.

### 9.7 Early conflict check

- **#59 (`bc7f291`):** clean before the push. It has since merged.
- **No other pull request is open.**

### 9.8 Departures

None from the fixes file. R6 was built as option A, re-read after the owner's message: no code change. The owner approved the five codes' Arabic, and the PR description says so.

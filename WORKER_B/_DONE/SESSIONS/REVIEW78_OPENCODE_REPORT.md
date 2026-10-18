# Review — PR #78 (SESSIONS)

Head: `fe233f836eb7082a5901a128dd6fe14fff43b8d8` (pinned before and after this read; base `3c3dc47`).

Verdict: one should-fix below, otherwise the change does what it claims — no surviving token, guard, deadline, wait, finding 39, tests, documents and commits all check out.

## Findings

### 1. should-fix — a refresh past the deadline with an already-expired token leaves the family behind

`apps/api/src/modules/sessions/sessions.service.ts:132` (with `:134`–`:136`):

```ts
if (!stored || stored.expiresAt <= at) return { outcome: 'invalid' };
if (stored.sessionEndsAt <= at) {
  await repository.deleteFamily(stored.familyId, tx);
  return { outcome: 'invalid' };
}
```

Scenario: a family 31 days old (past its `sessionEndsAt`) whose presented token is 8 days old (past its 7-day `expiresAt`). The first line returns `invalid` without deleting the family, so the family's rows survive this refresh. The spec the PR documents (security.md › Tokens and cookies; finding 20's resolution) is that a refresh past the deadline deletes the family. No live token can succeed past the deadline (any live-token presentation reaches the second check and deletes), so this is dead-row cleanup only, swept later by the next sign-in — not a surviving session.

Fix: check the deadline first, so a past-deadline family is deleted on any presentation:

```ts
if (!stored) return { outcome: 'invalid' };
if (stored.sessionEndsAt <= at) {
  await repository.deleteFamily(stored.familyId, tx);
  return { outcome: 'invalid' };
}
if (stored.expiresAt <= at) return { outcome: 'invalid' };
```

## Checked and fine

- No surviving token: `endSessions` (`users.service.ts:194`) is the only caller of `sessions.revokeAll` (`users.service.ts:196`); password change, reset (`auth.service.ts:376`), refused refresh of a suspended account (`auth.service.ts:252`), suspension, role change (`users.service.ts:332`), owner-link role changes through `changeRole`, temporary password, and Google link (`users.service.ts:318`) all go through it in the caller's transaction under the session lock; bump precedes deletion (fail-closed) in one atomic transaction; changer's token (`users.service.ts:568`–`:573`) and Google session (`auth.service.ts:222`–`:228` via `linkGoogle`'s post-bump read) are signed from the version read after the bump. Sign-out uses `sessions.end` only.
- Guard: `verify` (`accessToken.ts:39`–`:55`) refuses missing, non-number, non-integer and negative `sessionVersion`; `requireAuth` (`requireAuth.ts:76`–`:80`) compares on every request including `allowPendingPasswordChange` routes, 401 either way; all production `sign` calls go through `users.accessClaims(account)`, nothing client-supplied.
- Deadline: set at sign-in, copied on rotation, never renewed (`sessions.service.ts:75`–`:88`); boundary `<=` matches the at-deadline/1ms-before tests; migration backfills `now() + 30 days` then `SET NOT NULL` in one transaction-safe file, `ADD COLUMN ... DEFAULT 0` for the version; sweep `OR` condition in `deleteExpired` correct.
- Wait: no-delivery paths (`auth.service.ts:288`, `:308`–`:315`) wait, delivered send adds none; `randomInt(minMs, maxMs + 1)` uniform over `[1500, 3000]`; `wait` port wired only in `app.ts` (4 lines, commit 4 only), awaited before the response; capped-sender caps and sender failures return `sent: false`, never throw past the wait.
- Finding 39: `passwords` parameter and `Passwords` type gone; `verifyPassword(password, null)` still spends a cost-12 comparison (`password.ts`); removed unit tests each have the API-lane twin the report names.
- Tests: deadline, version (6 API files), logout-leaves-other-session, suspension-restore, Google-link, owner-link role, resend-wait and race tests assert the security property directly; fixture `sessionEndsAt`/`sessionVersion` additions preserve each fixture's original semantics; draw-variation flake probability negligible (`1/1501²`).
- Documents: security.md (version row, 30 days, wait/estimate/reverse-tell/residual, both 401 checks), ADR 0003 *Revised* 2026-10-13, ADR 0017, data model (both columns), conventions (§2, R5, §11 timer, §12 row, §13 `endSessions`), contract 401 wording (§1, *Me*, role, suspended), users.md/auth.md decisions+history+code map, findings 51/20/16/39 resolved with resolution lines, 65 opened, index groups correct — each true to the code, one home per fact.
- Commits: four, subjects counted by hand at 45 / 40 / 48 / 50 characters (`refactor(users): hash passwords in the module`, `feat(sessions): end a session 30 days on`, `feat(auth): end access tokens with their session`, `feat(auth): wait as a send would when none is made`), all ≤ 50; one migration; `app.ts` touched in commit 4 only; nothing in `apps/web` or `packages/shared`; no new dependency.

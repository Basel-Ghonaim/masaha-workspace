# OWNERS — reply to your plan

A strong plan. Approved, with one addition. **First, save it** (as approved here) to
`C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\OWNERS_PLAN.md` — `PLAN\` is still empty — then cut the
branch and build.

## The owner's decisions (§13)
1. **S1 — the space's share lock for its read,** not a snapshot: approved (one isolation level,
   ADR 0015; the only kind a test can prove). Write the rule for future writers into conventions §13.
2. **S2 — `joinedAt` and `signIn` in the rows:** approved.
3. **S3 — re-linking is idempotent (204, nothing written), and `OWNER_ALREADY_LINKED` goes** (core,
   both catalogues, contract §6): approved.
4. **S4 — 422 `errors.spaceId = ["invalid_choice"]`** for the body's space: approved.
5. **S8 — fold finding 25:** approved, as its own last commit.
6. **The codes:** `EMAIL_HAS_ACCOUNT`, `ALREADY_OWNER`, `ACCOUNT_IS_ADMIN`, `RECEPTION_LINK_ACTIVE`,
   `TEMPORARY_PASSWORD_NOT_PENDING` approved; **`ACCOUNT_SUSPENDED` reused** as the 409 approved —
   its catalogue line («هذا الحساب موقوف.» / "This account is suspended.") is neutral, so it reads
   right to the admin too. List each new code's English and Arabic in the PR for approval.
7. **The handover:** `POST /admin/users/:userId/temporary-password/handover` with `{ channel }`
   (`WHATSAPP | IN_PERSON | OTHER`): approved.

S5, S6 and S7 approved as written. New finding 49 approved (50 stays free).

## One addition
**A reception row that becomes an owner's says so in the audit.** When D4 reactivates a deactivated
`RECEPTION` row as `OWNER`, its `space.ownerLinked` entry carries `before: { role: "RECEPTION" }`, so
the space's log shows that the person's role there changed, not only that a link appeared. One test.

## Reminders
- Every new endpoint tested as a guest, a USER, an OWNER, an ADMIN with a pending change, and an
  ADMIN; each race with its lock removed once (testing §3 rule 7).
- At the report: `git merge-tree --write-tree` against every other open PR.
- **An independent review follows** (authorization, security and transactions). Don't merge.

# Review of #131 — R1: the foundation and the items left

Read this file, then `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\5_REVIEW_PROMPT_COMMON.md` whole, and do it.
Your report: `6_REVIEW_R1_CLAUDE_CODE.md`. **Head: `c41a5397`.** New findings, if any: **190–192**.

**Your range:** `origin/main..6d563549` — the first 8 commits: #130's fixes and finding 153 (`test(platform-settings):
pin a stored contact form`, `fix(seed): store the contact in its one form`, `docs: resolve finding 97`), **the
`payments` totals** both finance and the owner's overview read (`feat(payments): total a space's balances`), finding
170 (`fix(sessions): read a family's latest activity`), `GET`/`PATCH /me` (`feat(users): read and edit one's own
account`), finding 167 (`feat(data-reports): filter by who handles them`), `GET …/visits` (`feat(visits): list a
space's visits by day`).

**Read in the plan:** §3.1–§3.3 for these parts; §4.1 and §4.3; §5.1 and §5.2 for their routes and shapes; §5.5; D30
and the units U0, U1, U5; §9.1, §9.2, §9.6, §9.7, §9.8; §10's cases for them; OD5–OD8.

**Look hardest at:**
- **The `payments` totals (money):** every total from the database by one rule — debts by `payments`' own balance
  rule, voided payments in nothing, written-off visits as the contract says; set-based (no N+1); read through `tx`
  where the caller holds one; each total equal to the sum of the list it summarises (the plan's own claim).
- **Finding 170 (auth):** the family's latest activity read as `max(last_activity_at)`; a rotation copying it; the
  race test real (would it fail?).
- **`/me`:** a user reads and edits only their own name and language; validation by the shared schema; audited as
  the plan says; no other field writable (role, email, password).
- **`GET …/visits`:** the owner any range up to the bound, reception **today only** (OD7) — refused, not narrowed
  silently?; Gaza days; paging; no customer data reception may not see.
- **Finding 167:** `handledBy=ADMIN|OWNER` on the admin's reports, by the same rule as the decision's authority.
- **#130's fixes and 153:** the seed's contact through the shared schemas; the stored-form round trip pinned.
- Tests and breaks of your range; documents (contract sections, `payments.md`, `users.md`, `visits`' document,
  `data-reports.md`, findings 97, 153, 161, 167, 170 and the index) true to the code.

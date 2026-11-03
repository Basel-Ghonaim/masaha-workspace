# Review of #132 — R2: the whole API (identity, accounts, staff, owners, jobs, migrations, desk money)

Read this file, then `C:\dev\masaha\workspace\WORKER_A\FINAL\5_REVIEW_PROMPT_COMMON.md` whole, and do it. Your report:
`C:\dev\masaha\workspace\WORKER_A\FINAL\6_REVIEW_R2.md`. New findings, if any: **224–227**.

**Your commits (35):**
- U1 (identity, accounts, staff, owners): `9284b98d b046ce99 79aaed8d 748ce34f 14bdecc4 958782bb 6626ad4f a31cb3d0
  c7fe46c4 e620ba83 2fad3c23 1cf7cd7c d3afe676 ae1e86a8 efb0d0d8 4908f217 b8fceb03`
- U2 (the desk, the money, the data reports, the spaces, the jobs, the migrations M1 and M2): `bd7e9d0f d9e81909
  06753d3c 0fce0315 dab7973e f0240b98 3fa5ab42 37caa0a4 347e32de 47ccd91d c675195f 1879e0b1 7e3244f0 627eeaa6 9f801981
  1716f006 57851f54 108dbff8`

**Read in the plan:** §5.1 (U1), §5.2 (U2) — every `D1.*` and `D2.*`, **M1 and M2 in full**; §5.11 S1 (finding 91's
narrow rule — OD6 (a)); §9.1's commits for U1 and U2; §10.2 and §10.3; §11's API cases; the contract at the head for
every route these commits add or change; `docs/architecture/data-model.md`; `docs/backend/conventions.md` §6, §8, §13;
`docs/backend/security.md`.

**Look hardest at:**
- **The migrations — read the SQL in full** (`apps/api/prisma/migrations/*` added by `06753d3c`, `7e3244f0`): M1
  (`subscription_usage` computing the due in `bigint` — finding 122: the function's result type, every caller, no
  overflow left, the old results unchanged for normal values); M2 (`published_period` with its `CHECK` — existing rows,
  a subscribe from `published` setting it, nothing else writing it); no PR number in SQL; the Prisma schema matches (no
  drift).
- **Sessions (21):** a replay within the grace returns the same successor, derived deterministically (an HMAC under a
  server key — the key's source and length, never logged); no new family; the race tests real.
- **Accounts:** finding 91 — **only a never-used account with no owner link** is replaced (OD6 (a)): can a stranger
  retire an owner's or a used account?; Google's `created` flag (32); the reset link printed in the email (23's
  neighbour: no token in a log); "how an account signs in" exposes nothing private.
- **Staff and owners:** 92 (deactivating ends sessions only with no other active link); an admin's account refused by
  its code; `ALREADY_OWNER` naming the account (83) — to the admin only; the exact-email search (89); each reception
  link dated.
- **The jobs:** the sweep of expired counters and tokens (17); the reclaim of files no photo holds (63, OD11 — can it
  delete a photo still referenced, or a file mid-upload?); a batch whose failures fill it answering 500 (121).
- **Desk money:** the visit checked in for its customer (160); **the subscribe refused when the published price
  changed (171 (a) — the 409, the new code, compared in agorot, under the lock)**; who recorded and voided on the
  statement (162); the written-off visits listed (164); a phone matched under either code (126); check-ins bounded by
  midnights (127); one report read by id; the retired amenities named (99).
- Locks and transactions (every read through `tx`), keys, roles (`requireCan`), the codes in both catalogues and §6.

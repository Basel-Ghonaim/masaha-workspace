HEAD SHA: a82541b1435366854d253f88cfe9258f87d36b8d
origin/main SHA: 1efe2b8afa6a81866a8440246b6258475e5ccb7a
HEAD is an ancestor of origin/main (origin/main is 2 commits ahead: admin space owners read). Reviewed at HEAD.

Verdict: the account prototype mostly matches the data model and settled decisions; the main API-truth gap is that the contract does not yet name the two account lists the UI depends on.

## Five most important points
1. `GET /me/favorites` and `GET /me/reports` are assumed by the prototype and by decisions C7/C8, but are not defined in api-contract.md §5.
2. Favourites are correctly designed as whole-answer lists per C8's §4 exception; My reports pages per P6.
3. Forced password change lands per role match `ROLE_HOME` in Change password.html (owner overview, desk, admin overview, Home).
4. Recovery steps come from the server cookie per ADR 0017; masked email is held by the server.
5. Sign-in has no designed state for the contract's 403 `ACCOUNT_SUSPENDED` (once the password matches).

## Issues

### R2-AU-TR-001 — Account lists are not in the API contract
**type:** defect · **level:** page · **impact:** high · **where:** Favourites / My reports frames, 1440/390 AR light · **evidence:** r2-shots/AU-TR/R2-AU-TR-001.png
The prototype and decisions C7/C8 (`listed: false` on `/me/favorites` and `/me/reports`) assume two endpoints, but api-contract.md §5 has no `GET /me/favorites` or `GET /me/reports` and §4's exceptions only name favourites.
**proposal:** Add both endpoints to the contract with their shapes, including `listed`, pagination for reports, and the whole-list rule for favourites.
**why:** Without them the API truth the review checks against is incomplete.
**cost:** S
**rule:** api-contract.md §4, §5; decisions-account.md C7, C8

### R2-AU-TR-002 — No designed answer for a suspended account on sign-in
**type:** improvement · **level:** page · **impact:** medium · **where:** Sign in frames, 1440/390 AR light
The contract's `POST /auth/login` returns 403 `ACCOUNT_SUSPENDED` once the password matches, but the prototype has no state for it on Sign in (only wrong password and 429).
**proposal:** Add a suspended-account message/empty handling on the sign-in screen for that 403.
**why:** Every defined failure code should have a designed answer.
**cost:** S
**rule:** api-contract.md §5 Session, `POST /auth/login`

## Decisions in doubt
None.

## What was not reviewed
Inputs and visual/mechanical axes (UX/VD/DF/EX/CP/AX) are out of this prompt's scope. Build/code truth was not checked (prototype-only). Screens for many Batch 4 frames have no saved screenshots; live-rendered via the prototype.
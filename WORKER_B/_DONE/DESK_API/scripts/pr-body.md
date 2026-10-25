## Summary
Three API needs of the desk's screens (DESK_SCREENS §6, approved 2026-10-24), and the small fixes carried from #114's review.

- **Spec B: one snapshot.** A subscription's statement and a customer's file are each read in one read-only `REPEATABLE READ` transaction, so their sums agree with their lists (finding 124 resolved).
- **Spec C: reception's idle session.** A session of an account with an active `RECEPTION` link, no `OWNER` link, and not the admin ends after 15 minutes with no request.
  - The access token now names its session (`sid`).
  - The session carries its last use, renewed by its requests at most once a minute.
  - The desk's polled state (`GET …/occupancy`) is passive and renews nothing.
  - An idle request answers 401 `SESSION_IDLE` and keeps the session; the refresh then ends it, clears the cookies and answers `SESSION_IDLE`, so the web can say why. Only this device's session ends.
- **Spec D: subscribe from a published week or month price.** The subscribe body takes `published: { period, audience, shiftId?, name }`, named by its key, never an id: a prices save writes the rows anew. Its terms are copied: fixed at the price's amount, its audience and shift, no limits, 7 or 30 days. Reception may use it.

### Carried from #114
- Reception's refusal of the payments list, said exactly: the query is validated first (422), then a valid range or `recordedById` is `forbidden` (documents).
- The check-ins list's 92 days counted with both ends, as the payments list (`fix(subscriptions)`, its test seen red first).
- The rule "no PR number in a migration", in `data-model.md`.
- The cosmetics in `payments.repository.ts` (`ITEM_PAYMENT` reused, a JSDoc rewrapped).

## Scope / Acceptance criteria / Out of scope
- In scope: specs B, C and D as approved, with the owner's decisions O1–O4 (2026-10-25); one migration, `session_activity`, which adds `refresh_tokens.last_activity_at`.
- Out of scope: spec A (an allocation quote; finding 125 decided (c)); every screen (worker A's PRs 3 and 4 read these routes). The web's sign-in page line for `SESSION_IDLE` is worker A's PR 3; this PR adds only the catalogue entry.

## Change type
feat: API code, the shared contract, tests and documents.
- **A migration:** `20261025081716_session_activity` adds `last_activity_at timestamptz(3) NOT NULL DEFAULT CURRENT_TIMESTAMP`. Sessions alive at the migration count their idle time from it.
- **One new error code**, `SESSION_IDLE` (401):
  - Arabic, for the owner's approval: «انتهت جلستك بعد 15 دقيقة دون نشاط. سجّل الدخول من جديد.»
  - English: "Your session ended after 15 minutes with no activity. Sign in again."
- **Every access token alive at deploy is refused once** (no `sid`) and refreshed silently by the web.

## Evidence
- **Every commit:** shared build, `lint` and `typecheck` (`git rebase -x`), all 8 OK.
- **On the head:**
  - `test:unit`: shared 256, api 874, web 946, all passed.
  - `test:api`, run 1: 1 of 1174 failed. A 5-second timeout in `customers.api.test.ts`'s scale test (1,000 subscriptions, 2,000 paid visits).
    - Investigated: the test passes alone, and its requests take the same time as on main (the file read 51–54 ms on the head, 50–68 ms on main).
    - Its bulk setup, slowed by the full parallel lane, crossed 5 s. No code changed.
  - `test:api`, run 2: 1174 passed.
  - `format:check`, `check:links`, `check:conflicts`: clean.
- **Seen failing first:**
  - the check-ins range's edge (`expected null to deeply equal { to: [ 'out_of_range' ] }`);
  - both snapshot tests on the old code (`expected 500 to be 300`, `expected 1000 to be 500`);
  - the token without `sid` (3 unit tests);
  - the six idle tests (5 red; the owner's is green by design);
  - spec D's schema and API tests (`expected 422 to be 201`).
- **Deliberate breaks, each red, then restored from a backup:**
  - B1 `ReadCommitted`: both snapshot tests red;
  - B2 the passive mark removed: the desk-left-open test red;
  - B3 the idle refresh ending every session: the second-device test red;
  - B4 owners included: the owner-who-is-reception test red;
  - B5 the period's days off by one: the copied-terms test red;
  - B6 a labelled price taken: the invalid-choice test red.
- **Real run on 3321** (`masaha_b_dev`, demo data), `ALL PASS`:
  - the statement's and the file's sums match their lists;
  - reception idle 16 minutes answers 401 `SESSION_IDLE`, and its refresh answers 401 `SESSION_IDLE`, clears the cookies and deletes the session. The idle time was set by moving that one session's `last_activity_at` back with one SQL statement; the real 15 minutes were not waited;
  - reception subscribes from the demo month price (201, ₪350, 30 days, nothing typed);
  - the owner's session is never renewed or ended.
- **Not run locally (CI judges):** `test:component`, the web `build`, `check:build`, `check:classes`. The web change is the two catalogue lines, whose parity the typecheck and the unit lane check.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean on every commit; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (a code and its two catalogue lines).
- [x] Authorization on the server (the idle end in `requireAuth` and the refresh; the subscribe's `can()` unchanged).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.

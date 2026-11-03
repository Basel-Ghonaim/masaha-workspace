## Summary

The platform's settings as three cards the admin reads and saves on its own — the new-space defaults, the staleness thresholds and the contact, now in the typed catalogue (finding 40) — and the public contact.

- `GET` / `PUT /admin/settings/{new-space-defaults|staleness|contact}` (🛡), one resource per card (AD-029): each save locks the card's rows by key, writes and audits only what changed (`platformSettings.<card>Edited`, no entity id), and a save of the same values writes nothing.
- `GET /settings/public` (🌐): the contact, `null` while unset, `Cache-Control: public, max-age=300`.
- The contact's two keys join the catalogue, optional, read in the form the seed stores; the admin's save lowercases the email and normalises the number. Finding 40 resolved.
- `@masaha/shared/platform-settings` (new): the thresholds' (1–365 days) and the contact's schemas and answers; the new-space defaults' schema moves to `@masaha/shared/space-settings`.
- The audit writer takes an entry with no entity id; the three actions join the admin's allowlist and `AUDIT_ACTIONS`, the entity type `platformSettings` joins `AUDIT_ENTITY_TYPES`.

## Scope / Acceptance criteria / Out of scope

**Scope (plan §2, PR 2):** the shared shapes and the moved defaults' schema; the catalogue's contact keys; the six admin routes and the public one; the three audit actions on the admin's list, the writer's nullable entity id; `docs/features/platform-settings.md`.

**Acceptance criteria — how each is met**
- [x] The admin reads and saves each card on its own; a save answers the card as saved; only what changed is audited, an unchanged save writes nothing; a refusal 422 on its field writes nothing — T1, T2, T8 (`adminSettings.api.test.ts`); B4, B5.
- [x] A new default applies to the next space created, never to an existing one; a new threshold applies at once — T3 (`POST /admin/spaces`), T4 (`GET /admin/spaces/:id`); B6.
- [x] The contact: an email (lowercased) and a WhatsApp number (normalised, Palestinian or Israeli), each or both `null` to clear; `GET /settings/public` answers both, `null` while unset, `Cache-Control: public, max-age=300` — U1, T2, T9, T10 (`publicContact.api.test.ts`); B1, B10, B11.
- [x] Two saves of one card at once: the second's `before` is the first's `after`; two first saves of the contact make one row per key — T5, T6 (held rows / a held insert); B7, B8.
- [x] A non-admin is 403 on every admin route, a guest 401; the admin's log shows the three settings actions — T7, T11 (`platformAuditLog.api.test.ts`, through the real routes); B9, B12.

**Out of scope:** any `apps/web` change (screen 32 is worker A's later item); moving the site's contact from `VITE_CONTACT_*` to `GET /settings/public` (worker A's); a data migration (none needed: the dev rows pass their read schemas).

**Finding 40 resolved** in the first commit, with its *Resolution* line and the index moved under *Resolved*.

## Change type

feat — API code, the shared contract, tests and documents; no migration; no web change; no dependency.

## New error codes

None.

## Evidence

Run locally on the head (code identical to the commits pushed; the last fold changed documents only, re-checked by `check:links` and `format:check`):
- `npm run build -w @masaha/shared` exit 0 · `npm run lint` exit 0 · `npm run typecheck` exit 0 (also after each commit).
- `npm run test:unit`: `Tests 267 passed (267)` · `881 passed (881)` · `1004 passed (1004)`.
- `npm run test:api`: `Test Files 99 passed (99)` · `Tests 1260 passed (1260)` (731 s).
- `npm run test:component` (no web change; the whole suite once): `Test Files 264 passed (264)` · `Tests 1564 passed (1564)`.
- `npm run format:check` "All matched files use Prettier code style!" · `npm run check:links` "2966 links in 201 documents and 2119 source files all resolve." · `npm run check:conflicts` "No conflict markers found."
- `git diff --stat origin/main -- apps/web package.json package-lock.json`: empty.

**Seen failing first:** U1 (shared `platform-settings/requests.unit.test.ts`, the defaults' lines in `space-settings/requests.unit.test.ts`) before the schemas; the allowlist's new unit line (`platformSettings.newSpaceDefaultsEdited: expected false to be true`); U2 against a stub; T1–T8 before the router (`Tests 7 failed | 4 passed (11)`; T7 passed before it, the guard answering first — B9 is its proof); T9–T10 before the public router (`expected 404 to be 200`, `expected 404 to be 500`); T11 with the three actions off the list (`expected [] to deeply equal [ { …(4) }, … ]`).

**Deliberate breaks, each red then restored from a backup (SHA-256 same) and green:** B1 the thresholds' upper bound · B2 the defaults' refinement · B3 every field counted · B4 the optional keys read as required (500) · B5 the no-change branch · B6 the defaults' write skipped · B7 `lock`'s `FOR UPDATE` · B8 `ensure` (the second save never waits) · B9 the router outside `/admin` (200 for a guest, a user, an owner, a pending admin) · B10 the cache header · B11 the read without its parse · B12 the three actions off the admin's list.

**Real run on 3321** (`masaha_b_dev`, self-judging, `ALL PASS`): the admin reads the three cards; the same values write nothing on each; the contact saved (normalised) and put back, audited with no entity id and only what changed; `GET /settings/public` anonymous with `Cache-Control: public, max-age=300`; a threshold saved to 1 day makes the demo space's five groups stale at once, then put back; the defaults' switch flipped and put back; a guest 401, a user and an owner 403 on the six routes. Every setting ends as it was before the run (fingerprints equal), with the exception below.

**Not run:** the web's `build`, `check:build`, `check:classes` — no web file changes; CI runs them.

## Screenshots

None: API and documents only.

## Decisions taken without the owner

1. **SERIOUS (data) — the development database's contact WhatsApp was rewritten from `+972…` to `+970…` by the real run's first "same values" save, and left so.** The seeded number is a Palestinian mobile given with `+972`; the project's phone rule stores those as `+970`, so the save normalised and audited it (one entry). Restoring the raw value would need an SQL write the run may not make, and the app always normalises. Recorded as **finding 153** (the seed accepts any E.164 contact number and stores it as given). Undo: restore the seeded value on `masaha_b_dev` by SQL, or re-seed the contact.
2. Finding 153 recorded, folded into the first commit (the seed's code is outside this PR).
3. `features/audit.md` gains one decision and one history line (the admin's list changed; a `platformSettings` target has no id) — not on the plan's file list, kept true to the code.
4. `shared/audit`'s index exports the writer's `AuditValue` type, used by the pure change rule.
5. The saves take the actor's id (the `/admin` guard already decided).
6. T11 runs through the real routes (the three saves, then the admin's log), not inserted entries (PR 1's review F1).
7. The real run saved each card and put it back (the exec prompt's list), beyond §12.6's contact-only write; no space was created (T3 proves the copy).
8. "A user" in the real run's refusals is the demo reception account (global role `USER`).
9. B8 is red by the lock wait (`never waited on a lock`), not by the plan's unique-violation 500: without `ensure` the save never inserts.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes and data only).
- [x] Authorization on the server (`/admin`'s guard; the admin's allowlist).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.

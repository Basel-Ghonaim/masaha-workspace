# Lane A1 notes
## C1.1
- red T20 (old service): auth.api.test.ts › "a token presented twice within the grace gets one successor, the same token" — AssertionError: expected 'w1FV…' to be 'LXs7…' → green (6 files, 150 tests)
- B21: "ends only that session when a token is reused after the grace window" — expected 200 to be 401
- B22: tokens.unit.test.ts › "the successor key is derived from the secret and its label" — expected Buffer[221,…] to deeply equal Buffer[101,…]
## C1.2
- red (code from HEAD): sweep.api.test.ts both tests — TypeError: sessions.sweepExpired is not a function; counter.api.test.ts › "a sweep deletes ended rate-limit windows, at most 5,000 a run" — TypeError: sweepEndedWindows is not a function; jobs.api.test.ts 3 tests — expected {…} to deeply equal {…} → green 3 files 13 tests
- B23: sweep › "…sessions past their end, keeping live ones" — expected { refreshTokens: 1 } to deeply equal { refreshTokens: 2 }
- B24: sweep › "…expired reset tokens and recoveries" — expected {…} to deeply equal {…} (recoveries 0)
- B25: counter › "…at most 5,000 a run" — expected 5001 to be 5000
## C1.3
- red T26: google.api.test.ts › "Google's answer says created for a new account, not for a linked one" — expected {…} to match object { data: { created: true, … } } → green (google.api 17 tests; users.service.unit 10)
- B26 (created always false): same test red, same message
## C1.4
- red (before code): replacement.api.test.ts 4 of 9 red — T27 "registering an expired pending account’s address replaces it and creates the new one" expected 409 to be 201; T28 same; T31 "Google’s first sign-in …" expected 409 to be 200; T32 expected 409 to be 201 (T29, T30 green before: they pin the refusals) → green 9/9; related api 10 files 183 tests; unit 15 files 82
- B27 (step removed): T27, T28, T32 red — expected 409 to be 201
- B28 (link kept): T28 red — expected {…} to match object { deactivatedAt: Any<Date> }; T32 red — expected [] to deeply equal [ObjectContaining…]
- B29 (footprint check removed): T29 ×4 red — expected 201 to be 409
- B30 (expiry check removed): T30 red — expected 201 to be 409
- B31 (Google not wired): T31 red — expected 409 to be 200
- B32 (no user.replaced entry): T32 red
## C1.5
- red T33: resetEmail.unit.test.ts › "the reset email holds the link as text in both parts and languages" — TypeError: Cannot read properties of undefined (reading 'replace') (copyLink missing) → green 15 tests (email folder)
- B33 (text part without it): same test — expected 'مرحبًا،…' to contain 'إن لم يعمل الزر، انسخ هذا الرابط:\nht…'
## C1.6
- red T34: me.api.test.ts › "GET /me answers hasPassword and hasGoogle" — expected {…(3)} to match object { hasPassword: false, hasGoogle: true } (and the two updated reads, deeply equal) → green 5/5
- B34 (hasGoogle from the password): T34 red — expected {…} to match object { hasPassword: false, hasGoogle: true }; both reads red too
## C1.7
- red T35: adminOwners.api.test.ts › "ALREADY_OWNER carries the owner’s id" — expected { type: 'conflict', …(3) } to match object { code: 'ALREADY_OWNER', …(1) } → green 50/50
- B35 (no details): same test red, same message
## C1.8
- red T36: adminUsers.api.test.ts › "the users list’s email filter keeps the exact account only" — expected [ 'Maha Saleh', 'Maha', 'Sara' ] to deeply equal [ 'Maha' ] → green 17/17
- B36 (email read as a contains search): same test — expected [ 'Maha Saleh', 'Maha' ] to deeply equal [ 'Maha' ]
## C1.9
- red T49: packages/shared requests.unit.test.ts › "the spaces list’s schema takes editable and the four others" — expected [ 'verified', 'unverified', …(2) ] to deeply equal [ …(3) ] → green; api admin-spaces unit 15, api admin-spaces+overview 3 files 42 tests; web filtersOf unit green
- B49 (editable removed): same test red, same message
- title: the plan's "and the five others" counts five with editable; written "the four others"
## C1.10
- red T37: staff.api.test.ts › "deactivating a link of a person with another active link keeps their sessions" — expected 401 to be 404 → green 14/14
- B37 (endSessions always): T37 red — expected 401 to be 404
- B38 (endSessions never): T38 (kept: "deactivating ends the person’s link and every session") red — expected 404 to be 401
## C1.11
- red T39: staff.api.test.ts › "the re-issue refuses an admin’s account with ACCOUNT_IS_ADMIN" — expected 'ACCOUNT_HAS_LINKS' to be 'ACCOUNT_IS_ADMIN' → green 15/15
- B39 (the admin check after the links'): same test red, same message
- finding 106's file left to the web lane (D5.10 finishes it)
## C1.12
- red T40: staff.api.test.ts › "a staff member is answered with the date their link was made" — expected [ { userId: 2, name: 'Sara', …(3) } ] to deeply equal [ ObjectContaining{…} ] → green 16/16; web staff component tests 7 files 26 green
- B40 (the date of the read, not the link's created_at; the plan's updatedAt is not selected, so the break stands in for it): same test red
## C1.13 (tests of existing code: red seen through the breaks)
- green: staff.api + sessionLock.api 2 files 28 tests
- B41 (role !== 'USER' removed): "the re-issue refuses an OWNER-role account with no link here: ACCOUNT_HAS_LINKS" — expected 200 to be 409
- B42 (active check removed): "the re-issue and the handover answer 404 for a deactivated reception link" — expected 200 to be 404
- B43 (re-activation's admin check removed): "a re-activation refuses an admin: ACCOUNT_IS_ADMIN" — expected 200 to be 409
- B44 (confirm's expiry check removed): "a temporary password that expires between the check and the lock is refused at confirm" — expected 200 to be 403
## C1.14 (a test of existing behaviour: red through its break)
- T45 green at once (adminOwners.api.test.ts › "the add-owner names invalid_format for a string id and invalid_choice for a deleted space")
- B45 (the schema coerces): expected { spaceId: [ 'invalid_choice' ] } to deeply equal { spaceId: [ 'invalid_format' ] }
## C1.15
- each race's table found by one instrumented run of the 41 race files (race-map.jsonl / race-map-summary): every race waits on a tuple or relation lock of one table; two (subscriberCheckIn's unique index, adminSettings' first contact save) wait on a transaction only, while writing check_ins / settings: the helper's third clause
- green: 41 race files + locks.api.test.ts — 42 files, 570 tests, after one fix (subscriberCheckIn's race named check_ins, not spaces: "1 request(s) never waited on a lock of spaces")
- T46 (db/locks.api.test.ts › "waitingOnLock needs its table, and counts only that table’s waiters"); B46 (`on` optional, any waiter counted): AssertionError: expected [ 97331, 97332 ] to have a length of 1 but got 2; and tsc: TS2578 Unused '@ts-expect-error' directive
- T46 is in the api lane (it needs PostgreSQL), not the unit lane the plan names
## C1.16
- T47 (space.api.test.ts › "reads the owners’ names on the read’s own connection, inside its transaction"), by the statement: green
- B47 (the names read without the read's transaction): AssertionError: expected 97732 to be 97742
## C1.17
- red T48 (typecheck, before the code): users.service.unit.test.ts(194,5): error TS2578: Unused '@ts-expect-error' directive → tsc clean; users unit 17 green
- B48 (`tx?` again): the same TS2578

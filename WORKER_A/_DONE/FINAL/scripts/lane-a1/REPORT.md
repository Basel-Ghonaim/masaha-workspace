# Lane A1 — the sub-agent's report (returned as text; saved by the lead)

Lane A1 · DONE · Branch lane/a1 head b328768f (base 37a84e65). Nothing serious, nothing left out. Size: 125 files,
+3582 / −1965 (most of it C1.15's re-indented race tests).

Commits (17, plan order): d250b829 feat(sessions): give a replay its successor (43) · e97a4027 feat(jobs): sweep
expired counters and tokens (45) · 8cd3e797 feat(auth): say a Google sign-in made the account (49) · e8a4d2d9
feat(auth): free an expired account's address (45) · ee00491c feat(auth): print the reset link in the email (45) ·
8b72f67d feat(users): say how an account signs in (40) · 41fb8052 feat(space-links): name the owner in ALREADY_OWNER
(50) · d605a531 feat(space-links): find an account by exact email (49) · a0bca2aa feat(space-links): one schema of
space statuses (47) · a7924de9 fix(staff): keep sessions held by another link (46) · 1270f31c fix(staff): refuse an
admin's account by its code (49) · 1232562a feat(staff): date each reception link (37) · 6de740c2 test(staff): pin
three refusals and the expiry (46) · 8a12bda0 docs(api): name the owners' type-check code (43) · ae359c60 test(api):
aim the race helper at its own wait (46) · 4d731b97 test(spaces): find the names' own query (39) · b328768f
refactor(users): require the names' transaction (47).

Red/green (notes `scripts\lane-a1\NOTES.md`): C1.1 T20 "expected 'w1FV…' to be 'LXs7…'" → 6 files / 150 · C1.2
sweep.api "sessions.sweepExpired is not a function", counter.api "sweepEndedWindows is not a function", jobs.api 3
"deeply equal" → 3 files / 13 · C1.3 T26 "to match object { data: { created: true … } }" → 17 · C1.4
replacement.api 4/9 red (T27, T28, T32 "expected 409 to be 201"; T31 "409 to be 200"; T29, T30 pin refusals that held,
proven by breaks) → 9/9, neighbours 10 files / 183, unit 15 / 82 · C1.5 T33 "TypeError … reading 'replace'" → 15 ·
C1.6 T34 "to match object { hasPassword: false, hasGoogle: true }" → 5 · C1.7 T35 "to match object { code:
'ALREADY_OWNER', …(1) }" → 50 · C1.8 T36 "[ 'Maha Saleh', 'Maha', 'Sara' ] to deeply equal [ 'Maha' ]" → 17 · C1.9
T49 "[ …(2) ] to deeply equal [ …(3) ]" → admin-spaces, overview api 42/42, web filtersOf 18/18 · C1.10 T37 "401 to
be 404" → 14 · C1.11 T39 "'ACCOUNT_HAS_LINKS' to be 'ACCOUNT_IS_ADMIN'" → 15 · C1.12 T40 "[ {…(3)} ] to deeply equal
[ ObjectContaining{…} ]" → 16, web staff components 26 · C1.13 T41–T44 green at once (existing code), each proven by
its break · C1.14 T45 green at once, B45 · C1.15 T46 with the code, B46; 41 race files + locks test 42 files / 570 ·
C1.16 T47 green, B47 · C1.17 T48 typecheck red "TS2578: Unused '@ts-expect-error' directive" → tsc clean, users unit
17/17.

Breaks (backup copy, restored by copy): B20 = T20's red · B21 "200 to be 401" · B22 "Buffer[221…] to deeply equal
Buffer[101…]" · B23 "{ refreshTokens: 1 } to … 2" · B24 recoveries kept · B25 "5001 to be 5000" · B26 = T26 · B27
T27, T28, T32 "409 to be 201" · B28 "deactivatedAt: Any<Date>" and T32 · B29 four cases "201 to be 409" · B30 "201 to
be 409" · B31 "409 to be 200" · B32 T32 · B33 "to contain 'إن لم يعمل الزر، انسخ هذا الرابط:\nht…'" · B34 T34 and
both reads · B35 = T35 · B36 "[ 'Maha Saleh', 'Maha' ] to … [ 'Maha' ]" · B37 "401 to be 404" · B38 "404 to be 401" ·
B39 = T39 · B40 (the read's own time as the date; `updatedAt` is not selected) T40 · B41 "200 to be 409" · B42 "200 to
be 404" · B43 "200 to be 409" · B44 "200 to be 403" · B45 "{ spaceId: [ 'invalid_choice' ] } to … 'invalid_format'" ·
B46 "[ 97331, 97332 ] to have a length of 1 but got 2" + TS2578 · B47 "97732 to be 97742" · B48 TS2578 · B49 = T49.

Heavy checks (grant, re-run 2026-10-30 after the restart, UTC): lint 0 (13:00:56) · typecheck 0 (13:02:04) · unit
shared 28 / 272 · unit api 76 / 908 · unit web 157 / 1076 · component whole exit 1: 4 files failed | 296 passed, 5
failed | 1739 passed (13:16:13) — timeouts, "Unable to find role=main/navigation", one axe "already running", none in
a file this lane touched; the four re-run together: only timeouts, different tests; alone: dashboard routes 62/62,
AnnouncementSheet 3/3, PaymentsLedger 4/4, site routes 12/13 twice ("shows the Directory under its title", no main in
3 s — finding 87) · **test:api whole on masaha_a_lane_a1_test: 117 files / 1347 tests, exit 0.** Per commit: touched
tests, prettier, check:links, `tsc --noEmit -p apps/api`; whole lint/typecheck at points (after C1.12 it caught five
web fixtures, folded into C1.12).

Shared files: `apps/api/src/app.ts` (successor key; two sweep jobs after the auto check-outs; space-links built with
`audit` and `now`; auth's `hasActed` port to the audit reader) · contract: Session (register, google), Me, Staff,
Owners, Users, Spaces › status, Internal · security.md (Tokens and cookies, Passwords, Rate limits) · data-model.md
(the swept rows under *Users and sessions*) · localisation.md (OD1's line) · features auth, users, space-links,
audit (91, 92, 69 out of space-links' Open findings) · shared: auth `created`, users `hasPassword`/`hasGoogle`, audit
`user.replaced`, space-links requests (email, one schema) + test + responses (`addedAt`) · apps/api shared/jobs
(`SWEEP_BATCH`), shared/rate-limit (`sweepEndedWindows`), audit (`hasActed`, `user.replaced` in platformEvents) ·
C1.17's `, undefined` in data-reports.service, finance.service, closures.service (A2's area) · web `filtersOf.ts`
(LIST_STATUSES keeps four until D6.4) · eight web staff fixtures gain `addedAt` · adminSpaces.api.test passes a
sessions service · all 41 race test files (each names its table, RACE_TIMEOUT_MS; prettier re-indented bodies).

Findings closed: 17, 21, 69, 77, 78, 79, 91, 92, 93. Left to web lanes: 32 (D9.3), 83, 89 (D6.5), 106 (D5.10), 158
(D6.4). 22 the lead's (U10). Index untouched.

Decisions (none SERIOUS): LA1-D1 per-commit light checks, whole lint/typecheck at intervals and at the end · LA1-D2
`successorKeyOf(secret)` in sessions/tokens.ts, derived in createApi from jwtSecret, env unchanged; `successorKey`
required, so users' `sessions` dependency required · LA1-D3 (EC2) `rate_limits` has no id; delete by `reset_at <= now`
ordered by reset_at then key, LIMIT 5,000; the other three oldest id first · LA1-D4 one port `hasActed`, wired in
app.ts to one SQL read in the audit read model (audit entry as actor, or a favourite, or a data report) · LA1-D5 the
replacement: users.register / accountForGoogle take a `FreeAddress` callback; users judges its half of S1
(`replaceableHolder`) and re-checks under the lock; auth's `freeAddress` locks the reception space then the account
(conventions §13), checks owner links and `hasActed`, ends the link by the system, retires the account; register reads
the holder before inserting (EC3) · LA1-D6 the web narrows LIST_STATUSES to its four worded statuses until D6.4 ·
LA1-D7 T46 is an api test (`db/locks.api.test.ts`); the helper covers a table lock awaited, a row's tuple lock, a
unique key's second writer; each race's table from one instrumented run (race-map.jsonl) · LA1-D8 swept rows under
*Users and sessions* · LA1-D9 T49 "the four others"; B40 uses the read's time · LA1-D10 `addedAt` required → 8 web
fixtures, folded into C1.12.

Notes for the lead: A2's reclaim job beside the two sweeps in app.ts; jobs.api.test expects visits, subscriptions,
sessions.sweepExpired, rateLimits.sweepExpired — A2's adds one more entry and one more `{}` in the stalled test;
`waitingOnLock` requires `on`, `whileHeld(on, …)`: every new race test passes its table and RACE_TIMEOUT_MS; expect
conflicts where A2 edits the same race test bodies; AUDIT_ACTIONS holds `user.replaced` (U6 words it).

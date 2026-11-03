# Review — FINANCE_AUDIT PR 2 (#130, `feat/platform-settings`) — Claude Code

- **Head:** `299d8abd6a58fa18d6607ef7aedd357c74437236` at the start and at the end (`gh pr view 130` re-read: same
  head, `CLEAN`). Base `origin/main` = `76661f7c` = the merge-base; 2 commits (`052f0e11`, `299d8abd`); 36 files.
- **CI on the head:** all green — build, check:classes, check:conflicts, check:links, format:check, lint, test:api
  (7m9s), test:component, test:unit, typecheck; CodeRabbit skipped.
- **Read:** every changed file at `299d8abd` (code, tests, shared, documents), plus the code they lean on: `core/phone.ts`,
  `core/fields.ts` (`emailSchema`), `space-settings/requests.ts` (`roundingPair`), `seed/{run,seed}.ts`, `test/{admin,locks}.ts`,
  `app.ts`'s mounts, `directory/cache.ts`, `eslint.config.js`'s level map, `packages/shared/package.json`'s exports. Nothing run.
- **Seen only in the report (`4_REPORT_PR2.md`), not verifiable from commit objects:** every red line (tests and B1–B12),
  the local verification, the real run and its database writes (entries 56–62), the memory readings.

## Verdict

**Mergeable.** No blocker. One should-fix and three nits, all small: they belong in worker B's next PR's first commit.

## Findings (most severe first)

### F1 — should-fix · S10 is neither tested nor stated in the contract: a contact stored in another form
- **Where:** `apps/api/src/modules/platform-settings/settingKeys.ts:24-30` (the read regex),
  `platform-settings.service.ts:103-121` (the save compares the normalised body with the stored form);
  `publicContact.api.test.ts` and `adminSettings.api.test.ts` (no such case); `docs/api/api-contract.md` › *Platform
  settings*, the contact bullet.
- **What I saw:** the only stored contacts the tests use are already in their one form (`'+970591234567'`,
  `'hello@masaha.ps'`, T9), or fail the read schema (`'0591234567'`, T10). Nothing stores what the seed can store and
  the save would rewrite — `'+972591234567'` (a Jawwal number given with `+972`) or `'Hello@Masaha.PS'`.
- **Failing scenario 1 (the decision's reason, unguarded):** someone tightens `contactWhatsapp`'s read to the phone
  rule (e.g. `.refine((v) => normalisePhone(v) === v)`). A database seeded with `SEED_CONTACT_WHATSAPP=+97259…` then
  answers `GET /settings/public` with a **500** on the site's About — exactly what S10 exists to prevent — and every
  test stays green.
- **Failing scenario 2 (the SERIOUS behaviour, unpinned and unwritten):** the admin's `GET …/contact` answers
  `+97259…`; a `PUT` of the same body writes `+97059…` and audits `before {whatsapp:'+97259…'}` /
  `after {whatsapp:'+97059…'}`. That is the right behaviour (below), but no test fixes it and the contract says only
  "a save that changes nothing writes nothing", which a reader takes to cover a GET→PUT round trip.
- **Fix:** T9 (or T1) gains a stored `'+972591234567'` and `'Hello@Masaha.PS'` → 200, answered as stored; T2 gains the
  `PUT` of those values → stored `+970591234567` / lowercase, one `contactEdited` with exactly those `before`/`after`.
  The contract's contact bullet gains one sentence: a value stored in another form (the seed's) is answered as stored
  and stored in its one form by the next save, audited. **Where:** worker B's next PR's first commit.

### F2 — nit · Finding 153's wording, and a case it leaves out
- **Where:** `docs/architecture/findings/153-…md`, *Evidence* and *Resolves when*.
- **What I saw:** the seed accepts `^\+[1-9][0-9]{7,14}$` (`seed/run.ts:28`) and stores it as given (`seed.ts:39-43`);
  the catalogue reads the same regex (`settingKeys.ts`); the save's `phoneSchema` keeps only +970/+972
  (`core/phone.ts:23`). So 153 is **true**. Two corrections:
  1. "audits a change no one made" is not accurate: the admin's save made it, and the entry is true (the stored form
     changed). Say "a change of form the admin did not ask for".
  2. It misses the sharper case: `SEED_CONTACT_WHATSAPP=+201001234567` (any E.164) is read and answered by the card,
     but a `PUT` of the card unchanged except the email is **422 on `whatsapp`** — the admin cannot save the email
     without retyping the number. *Resolves when*'s second branch ("the documents accept the first save's rewrite")
     does not cover it; its first branch (the seed through `emailSchema`/`phoneSchema`) does.
- **Fix:** both lines in the finding. **Where:** worker B's next PR's first commit.

### F3 — nit · `platform-settings.md` claims the browser checks the bodies
- **Where:** `docs/features/platform-settings.md:29` — "each save's body is checked by its shared schema, in the
  browser too".
- **What I saw:** `git grep` at the head finds no `apps/web` import of `stalenessSchema`, `platformContactSchema` or
  `newSpaceDefaultsSchema`; the document's own authority line says "no screen yet", and its class is *Description —
  what is built*. (The same idiom stands in `packages.md:33` and `space-settings.md:32`; there a web may use it.)
- **Fix:** drop "in the browser too" until screen 32 uses them. **Where:** worker B's next PR's first commit (or worker
  A's screen-32 PR, which makes it true).

### F4 — nit · "A save that changes nothing writes nothing" is not literally true for an unset contact
- **Where:** `platform-settings.service.ts:103-106` (`ensure` runs before the no-change return); the contract's *A save*
  bullet and `platform-settings.md` › *What it does*.
- **Scenario:** a database with no contact rows; `PUT /admin/settings/contact {email:null, whatsapp:null}` → 200,
  no audit entry, but two rows (`'null'::jsonb`) are inserted and committed. Nothing a reader sees changes (a missing
  row and a JSON `null` both read `null`), so harmless.
- **Fix:** word it "changes no value" (or accept as is). **Where:** optional, with F1.

## The SERIOUS decision (5) — the contact's WhatsApp left normalised

- **Is the normalisation right by the phone rule?** Yes. `normalisePhone` (`core/phone.ts:15,29`) puts every
  Palestinian mobile (`5[69]…`) on `+970`, whatever code it was typed with; data-model › *Conventions, Contacts*:
  one number, one form. `+97259…` → `+97059…` is the rule, not a slip.
- **Is a "same values" save that changes the stored form a defect of the API?** No. The save compares the normalised
  body with the stored value (`service.ts:107-114`); the stored value **did** change, so the write and the entry are
  true (`before` the seed's form, `after` the one form). Comparing normalised forms instead would either keep a form
  the rule forbids while answering the normalised one as "saved" (a false answer), or need a lenient-normalising
  read — a change to S10, the owner's to decide, not a fix. The defect is the seed's (153), and the gap is that the
  behaviour is neither tested nor stated (F1).
- **Is 153 true?** Yes (F2 for its wording and the missing foreign-number case).
- **Leaving entry 56 and the `+970` value on `masaha_b_dev`:** right. Restoring by SQL breaks the run's hard limit;
  through the app it is impossible; the value is the same number in its legal form, on worker B's own database. The
  undo (the owner's SQL) is stated. *Seen in the report only.*

## The other eight decisions

1. **`audit.md` touched (not on §7's list):** right — the admin's list really gained three actions and a target with
   no id; the line at `audit.md` (decision + history) is true to the code (`platformEvents.ts:43-45`).
2. **`AuditValue` exported from `shared/audit`:** right; one existing type reused, no new surface.
3. **`saveX(actorId, …)` instead of `actor`:** fine — only the id is audited; the `/admin` guard decided.
4. **T11 through the real routes:** better than the plan (PR 1's F1 lesson); seen in `platformAuditLog.api.test.ts`.
6. **153 recorded, folded into C1:** right to record, not fix (the seed is outside the scope); see F2.
7. **Each card saved and put back in the run:** within the exec prompt's §5; each write named (57–62) and the values'
   fingerprints equal before/after the second run — *report only*. Note: "after = before" holds against the second
   run's start, not the first's (the WhatsApp's form, decision 5).
8. **"A user" = the demo reception account (role `USER`):** fine for the run; T7 proves a real `USER` with
   `REFUSED_CALLERS` (`test/admin.ts:14-24`).
9. **B8 red on the lock wait, not a 500:** acceptable — see the tests below.

## Tests and breaks (code seen; red lines from the report)

- **U1** shared `platform-settings/requests.unit.test.ts` + `space-settings` defaults: bounds 1–365, whole; email
  lowercased; Jawwal `059…` → `+970…`; `+20…` refused; minutes codes `required`/`invalid_format`/`out_of_range` — can
  fail (B1, B2).
- **U2** `settingsChange.unit.test.ts`: only the changed fields; `null` when equal — can fail (B3).
- **PR 1's U1** gains the three actions on `AUDIT_ACTIONS` and `isPlatformEvent` — can fail.
- **T1** reads, the contact `null` while unset — B4 red (`500`).
- **T2** saves, normalised answers, exact stored rows, exact audit entries (`entityId: null`, `spaceId: null`, only the
  changed fields), same values (other casing/spacing) write nothing, `null` clears — B5 red. Missing: F1's stored-form case.
- **T3** the next space gets the new default, the existing keeps its own (`POST /admin/spaces`) — B6 red.
- **T4** a threshold applies at once (`staleGroups` `['prices']` → all five) — no break planned; its red-first is the
  route's 404.
- **T5** `whileHeld` on `stalenessDays` then commits 50: the second's `before` is 50 — B7 red (`before` 60). Sound:
  without `FOR UPDATE` the request still waits on its `update`, so the guard passes and the assertion catches it.
- **T6** a held insert of both contact rows; the save waits (`waitingOnLock`), answers 200, `before` is the first's
  email — B8 red on the guard. It still proves the race: without `ensure` the `FOR UPDATE` sees no row (uncommitted),
  never waits, and its `update` of an invisible row would fail the `200` anyway. "One row per key" itself is the
  primary key's and cannot fail by any code change; the meaningful claims (both 200, the second after the first) can.
- **T7** guest 401, `USER` and `OWNER` 403, pending-password admin 403 `PASSWORD_CHANGE_REQUIRED`, on all six routes,
  nothing written — passed before the router existed (the guard answers first); **B9** (router mounted outside the
  guard) is its proof — red ×4.
- **T8** 422 on its field, nothing written or audited (0, 366, no `@`, `+20…`, a key missing, minutes `null`).
- **T9** anonymous, `Cache-Control: public, max-age=300`, both `null` unset, then set; `toEqual` keeps any other key
  out — B10 red.
- **T10** a stored `'0591234567'` → 500, `type: server`, the value not in the body — B11 red.
- **T11** the three actions on the admin's log, target `{type:'platformSettings', id:null, name:null, nameAr:null,
  deleted:false}`, `space: null` — B12 red.

## Checked and fine

- **Authorization:** `admin.use('/settings', …)` (`app.ts:629`) inside `api.use('/admin', requireAuth(),
  requireRole('ADMIN'), admin)` (`app.ts:643`), so the guard precedes every `validate`; the public router answers only
  `GET /public` (`platform-settings.public.routes.ts`) with `contact()` — email and WhatsApp, nothing else of the catalogue.
- **The save (D7):** `ensure` (`INSERT … ON CONFLICT ("key") DO NOTHING`, `updated_at` passed as `now()`) only for the
  optional keys, then `lock` (`ORDER BY "key" FOR UPDATE`, `LockRows` above the sort, so one fixed order), parse,
  `settingsChange`, `write` per changed key through `tx` (`Prisma.JsonNull` for `null`), audit in the same `tx`. No
  card shares a row with another; a space's creation reads the defaults without a lock (D14). Two concurrent first
  saves insert in the same key order, so no deadlock. The no-change branch writes no value and audits nothing.
- **The audit:** `entityType: 'platformSettings'`, `entityId: null`, no `spaceId`; the writer's `entityId: number |
  null` only widens an input type, so no caller breaks; the owner's log is scoped by `space_id`, so it never shows
  them; #128's per-type joins match nothing for this type, so `name: null` (T11).
- **Validation:** thresholds `z.int().min(1).max(365)` in the request and the read; email trimmed, lowercased, ≤ 254;
  WhatsApp through `phoneSchema` (≤ 30 chars, +970/+972 only); the defaults reuse `roundingPair`, so a space's own codes;
  a stored value failing its schema throws → 500 on both reads (T10), never answered; a client cannot cause a 500.
- **Normalisation reaches the service:** `validate` replaces the body with the parsed output (T2's `'0591234567'` →
  `+970591234567`).
- **Documents:** contract *Platform settings* and *Audit log* true to the code; conventions header, §6, §7, §9, §13;
  data model *Conventions › Settings* and *Setting*; finding 40 *Resolved* with its *Resolution* and the index line
  moved; 153 and its index line; `platform-settings.md` (template headings as `audit.md`), `space-settings.md`,
  `audit.md`, `v1-mvp.md`, `overview.md`, `docs/README.md` — each with `#130`, no `#PRNUM` left. Exceptions: F1, F3, F4.
- **Scope:** only `apps/api`, `packages/shared`, `docs`; no migration, no `package.json` or lock change (the shared
  `./*` export serves the new folder; `platform-settings` already L0 on the one level map). Subjects 48 and 50, each with
  a body; no `fixup!`, no tool attribution; author Basel-Ghonaim.

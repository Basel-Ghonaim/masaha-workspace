# Targeted review of #149 (CONTACT_RULES)
Head: a28f74dfce93bfc5900db2ccbdbfdde96ac4f976 · checks: green (all 10 pass; CodeRabbit skipped) · head moved: no (CLEAN at the end)
Verdict: mergeable after a fix round (no blocker; three should-fix items, all in tests or documents)

## Verdicts
R1 PASS — `packages/shared/src/core/digits.ts:10-17` maps U+0660–0669 and U+06F0–06F9 only; exported from `core/index.ts:1`; the web file was renamed into shared (no copy left; `git grep 0x0660|٠-٩` hits only `digits.ts`); `shekels.ts:1`, `wholeNumber.ts:1`, `coordinates.ts:1`, `packageValues.ts:1` import `@masaha/shared/core`; `digits.unit.test.ts` (moved test) fails on a wrong mapping (Breaks log, checked: the Eastern zero is its own constant at `digits.ts:2`).
R2 PASS — `phone.ts:25` runs `toWesternDigits` before the trunk and separator strips; every row derives as expected (table below); Arabic/Eastern rows at `phone.unit.test.ts:51-56` fail if `:25` loses `toWesternDigits`.
R3 PASS — no phone input bypasses the rule. Browser: `useContactsSheet.ts:122` (`normaliseContact`), `useEditDialog.ts:42` (`updateCustomerSchema` → `phoneSchema`) and `:53`, `usePhoneOwner.ts:18`, `useDebtDialog.ts:45` / check-out / pay via the `desk/requests.ts:22,41,61` schemas, `platformContact.ts:17`. Server: `spaces.admin.routes.ts:66` and `spaces.manage.routes.ts:43` (`updateSpaceContactsSchema` → `requests.ts:284`), `customers.manage.routes.ts:23,29`, `desk.manage.routes.ts:38,53,65`, `platform-settings.admin.routes.ts:24` (`whatsapp: phoneSchema`, `platform-settings/requests.ts:27`), `customerSearch.ts:23` for a whole phone. The suffix path (`customerSearch.ts:25-26`) is finding 228, out of scope by C10.
R4 PASS — `contacts.ts:44` (`DOMAIN`) at `:120`; every row derives as expected; `javascript:alert(1)` is untested (see F2).
R5 PASS — `contacts.ts:71-72` (paths), `:148` (handles), `:154-158` (profile.php before the path check); every row derives as expected; `facebook.com/search/?q=x`, `facebook.com/masaha/about`, `notfacebook.com/masaha` and a bare `facebook.com/profile.php` untested as such (see F2). «وسيلة أخرى» IP link refused (`contacts.unit.test.ts:283-285`); no copy file in the diff, so the Facebook error's copy is unchanged.
R6 PASS — Sheet: `ContactsSheet.component.test.tsx` (new test after `:176`) asserts each row's error and `writes()` equal `[]`; API: `contacts.api.test.ts` (new `it.each` after `:209`) asserts 422 `invalid_format` and `stored()` unchanged (`contacts: [], contactsUpdatedAt: BEFORE`); desk: `useEditDialog.component.test.tsx` (new test after `:116`) asserts the field error and `patches(requests)` length 0.
R7 PASS — no migration, seed or script in the diff; the demo seed's Facebook `freelancershouse.gaza` (`demoDirectory.ts:279`) and website `campus.example.com` (`:367`) still pass `normaliseContact` (`:620-621` would throw otherwise); report §5: 0 refused in `masaha_cr_dev`.
R8 PASS — `Button.tsx:29`: `[[data-slot=table-row]_&]:hover:bg-hover-on-muted` and `…:aria-expanded:bg-hover-on-muted` on ghost only; `TableRow` carries `data-slot="table-row"` and `hover:bg-hover has-data-open:bg-hover` (`Table.tsx:62-64`), so the row keeps `hover` while the menu is open; the scoped selector adds an attribute selector, so it outranks `hover:bg-hover` by specificity; outside a row (e.g. `CustomerMenu`) the selector cannot match. Tokens: `semantic.css:65` light `neutral-900 10%`, `:144` dark `neutral-50 8%` — as the report says. Tests: `Button.component.test.tsx` (class assertion, and no other variant carries `table-row`); `semantic.unit.test.ts` adds `hover-on-muted` over `hover` for text and fill in both themes (Breaks log: 10 %→2 % failed both).
R9 WEAK — `componentSetup.ts`: `afterEach` records `[data-sonner-toast]`, `afterAll` waits 300 ms on real timers only when a toast was drawn; no try/catch, nothing swallowed. But `toastTeardown.component.test.tsx` passed before the fix (Breaks log, commit 4) — it cannot fail (F3).
R10 PASS — the four files add `beforeAll(() => warm(...), 60_000)` with the modules they open, as testing §3 rule 8 says at `<HEAD>` (`docs/development/testing.md:38`).
R11 WEAK — every changed rule has a test that fails on its revert (checked against the code: `DOMAIN` → the bare-number, IP and IPv6 rows; the Facebook `paths` → the refused list; the profile.php reorder → `contacts.unit.test.ts:62`; `toWesternDigits` in `normalisePhone` → `phone.unit.test.ts:51-56`; OTHER's `toWesternDigits` → `contacts.unit.test.ts:273-281`); a few rows of R4/R5 untested (F2); R9's test cannot fail (F3).
R12 FAIL — finding 217's resolution quotes the Sheet's input as `٠٥٩٩٧٧٧٧٨٨٨` (11 digits), which the rule refuses; the test types `٠٥٩٩٧٧٧٨٨٨` (10) (F1). Everything else checked true: spaces.md's two rules and history lines, customers/desk/platform-settings change-log lines, foundation.md's row wash and verified pairs, findings 217–219, 225, 226 Resolved (file and index), 228 Open in the index and accurate (`customerSearch.ts:25-26`: `\d` reads Western digits only; `customersQuerySchema.q` is a plain `textSchema`, no conversion). `#149` in nine doc files, all this PR; no `#PRNUM`, no stray `#148`.

## Findings (FAIL and WEAK only, most severe first)

### F1 — should-fix · R12 · Finding 217's resolution quotes a number the rule refuses
- Where: `docs/architecture/findings/217-contacts-and-every-phone-refuse-arabic-indic-digits.md:9` (the Resolution line) at a28f74df.
- What: it says the Sheet "sends `+970599777888` for `٠٥٩٩٧٧٧٧٨٨٨`" — four ٧, eleven digits. `normalisePhone` reads `05997777888`, national `5997777888` (ten digits), which fails `MOBILE` (`phone.ts:14`) and `LANDLINE` (`:16`): refused. The test (`ContactsSheet.component.test.tsx`, the Arabic-Indic test) types `٠٥٩٩٧٧٧٨٨٨` (three ٧, ten digits).
- Fix: write `٠٥٩٩٧٧٧٨٨٨`. Folds into `a28f74df docs: resolve findings 217, 218, 219, 225, 226`.

### F2 — should-fix · R4, R5, R11 · Some table rows have no test
- Where: `packages/shared/src/spaces/contacts.unit.test.ts:93-155` at a28f74df.
- What: these rows are refused by the code (traced below) but no test names them:
  - `WEBSITE javascript:alert(1)` — refused only because `https://javascript:alert(1)` fails to parse (invalid port), not by an explicit rule.
  - `FACEBOOK facebook.com/search/?q=x` — the single segment `/search` is refused only by the `search` word in the lookahead (`contacts.ts:72`); the existing test `search/top?q=masaha` has two segments and would still pass if `search` left the list. The same holds for `events`, `share`, `reels`, `videos`, `posts` alone (only `watch`, `photo` and, as handles, `watch`/`groups` are proved one segment).
  - `FACEBOOK facebook.com/masaha/about` — C10's explicit "refused, not shortened"; covered only by the same mechanism (`/masaha/videos/123`).
  - `FACEBOOK notfacebook.com/masaha` and `facebook.com/profile.php` (no id) — unchanged logic (`onHostOf` exact match, `:126`; `id` null at `:156`), covered only by neighbours (`tiktok.com.evil.ps`, `profile.php?id=abc`).
- Fix: add these five inputs to the refusal tests (`one('WEBSITE', 'javascript:alert(1)')`; the four Facebook inputs to the `it.each` at `:133`). Folds into `1873382b fix(spaces): accept only real links in contacts`.

### F3 — should-fix · R9, R11 · Finding 219's regression test cannot fail
- Where: `apps/web/src/test/toastTeardown.component.test.tsx` at a28f74df; `apps/web/src/test/componentSetup.ts` (`afterAll`).
- What: the setup change is sound and swallows nothing, but the report's Breaks log says the test passed three times before the fix: it does not reproduce the race, so it proves nothing about the wait. Finding 219's resolution says so honestly ("CI's repeated component runs are its evidence").
- Fix: either make the test reproduce the race (e.g. a second test file that dismisses a toast in its last test with the setup's wait removed, asserting no unhandled error — likely costly), or keep it and the owner accepts it as a smoke test, the finding's wording as it is. Owner's call; if kept, no commit changes.

## R2, R4, R5 traced (each input: derived result · file:line · test or "untested")

Library behaviour relied on: WHATWG `URL` (Node and browsers alike) — a host whose last label is numeric is parsed as IPv4 (`123` → `0.0.0.123`, `127.1` → `127.0.0.1`), an IPv6 host keeps its brackets in `hostname`, an invalid port throws, `hostname` is lowercased and an IDN host comes back in `xn--` form. JS `\d` matches ASCII digits only. zod `.transform` with `z.NEVER` fails the parse.

**R2 — `normalisePhone`, `phone.ts:24-36`**
- `٠٥٩٩١٢٣٤٥٦` → `:25` `0599123456` → `:28` local, national `599123456` → `MOBILE` → `PALESTINIAN_MOBILE` → `+970599123456` · `phone.unit.test.ts:51`
- `۰۵۹۹۱۲۳۴۵۶` → same → `+970599123456` · `:52`
- `+970599123456` → given `970` → `+970599123456` · `:17`; `00970599123456` → same · `:18`
- `+972599123456` → national `599…` is a Palestinian mobile → `+970599123456` (as before; `:34` unchanged) · `:28`; `00972599123456` → same · untested as such (`00972569123456` at `:29` takes the same branch)
- `0599123456` → `+970599123456` · `:19`; `0569123456` → `+970569123456` · `:20` (local form accepted, stored E.164 as before — C2)
- `02…` landline, e.g. `022981234` → national `22981234` → `LANDLINE` → `+97022981234`, accepted as before · `02` untested; same branch as `082821234` at `:34`
- `+1 202 555 0100` → `+12025550100` → no match at `:28` → refused · `contacts.unit.test.ts:27` (PHONE), `phone.unit.test.ts:62` without spaces
- `05991234` → national `5991234` (7) → neither rule → refused · `:63`
- `abc` → no match → refused · untested as such (`letters` at `:67`)
- empty → no match → refused · `:70`

**R4 — website, `linkOf` `contacts.ts:110-121`, `websiteAddress` `:163-167`**
- `example.ps` → `https://example.ps`, `DOMAIN` ok → accepted · `contacts.unit.test.ts:87` (`masaha.ps`)
- `www.example.com` → accepted · `:115` (`www.masaha.ps/about`)
- `https://masaha.ps/about` → accepted, path kept · `:115`, `:88`
- `http://example.com` → accepted, stored `https://` · `:88`
- `123.ps` → last label `ps` not numeric → not IPv4 → `DOMAIN` ok → `https://123.ps` · `:117`
- `123` → IPv4 `0.0.0.123` → TLD `123` fails `DOMAIN` → refused · `:100`
- `10.0.0.1` → TLD `1` fails → refused · `:103` (`10.0.0.1/menu`)
- `http://10.0.0.1` → refused · `:102`
- `localhost` → no dot → refused · `:94`
- `http://localhost:3000` → hostname `localhost` → refused · `:106` (`:5173`)
- `masaha` → no dot → refused · `:107` (`example`)
- `http://[::1]` → hostname `[::1]` → refused · `:105`
- `ftp://example.com` → protocol `ftp:` → refused · `:95`
- `javascript:alert(1)` → no `://`, so `https://javascript:alert(1)` → port `alert(1)` invalid → `URL` throws → refused · **untested** (F2)

**R5 — Facebook, `networkAddress` `contacts.ts:144-160`, `paths` `:71-72`**
- `facebook.com/masaha` → link, path `/masaha` → first branch → `https://www.facebook.com/masaha` · `:48`, `:49` (fb.com, m.facebook.com)
- `https://www.facebook.com/Masaha-Space-123456` → `[\w.-]+` → accepted · `:127` (m. host, trailing slash)
- `m.facebook.com/masaha` → host listed → accepted · `:49`
- `facebook.com/profile.php?id=100012345` → `:154-156` before the paths check → `…/profile.php?id=100012345` · `:62`
- `facebook.com/people/Some-Name/100012345` → first branch fails at `/`, second `people\/[^/]+\/\d+` → accepted · `:124`
- `facebook.com/watch?v=1` → path `/watch` → lookahead blocks → refused · `:134`
- `facebook.com/watch` → same · `:135` (`/watch/?v=123`), handle `watch` `:151`
- `facebook.com/masaha/videos/1` → two `/` → neither branch → refused · `:137`
- `facebook.com/reel/1` → two segments → refused · `:136`
- `facebook.com/groups/x` → refused · `:141`
- `facebook.com/events/1` → refused · `:142`
- `facebook.com/photo?fbid=1` → path `/photo` → lookahead `photos?` → refused · `:143`
- `facebook.com/share/abc` → two segments → refused · `:146` (`share/p/abc`)
- `facebook.com/search/?q=x` → path `/search` → lookahead → refused · **untested** as one segment (F2)
- `facebook.com/masaha/about` → two segments → refused, not shortened (C10) · **untested** as such (F2)
- `facebook.com/masaha/posts/1` → refused · `:138`
- `facebook.com/profile.php` → `id` null → `:156` null → refused · **untested** as such (F2; `:65` `id=abc` takes the same line)
- `notfacebook.com/masaha` → host not in `hosts` (`:126`) → refused · **untested** for Facebook (F2)

## Not checked, and why
- Rendered colours and the specificity in the built CSS — the review is read-only (no build, no browser); derived from the Tailwind v4 variant order and the report's captures (§6).
- That each `warm(...)` list names every lazy module its file opens — checked against the rule's wording, not by running the files.
- The data count in `masaha_cr_dev` — no database access; taken from report §5.
- Whether every Facebook username Facebook allows passes `[\w.-]+` (e.g. non-ASCII page names) — outside C3's examples; not traced.

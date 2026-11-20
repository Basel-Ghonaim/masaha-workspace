# Review of #140 (PR-A) — Claude Code, Opus 5.5
Head: 29bcf80ae2b4441478abc7ecbf81f42fb500849c · commits 2 · files 37 · checks: green (10 pass, CodeRabbit skipped) · head moved: no (still `29bcf80a`, `CLEAN`, at the end)
Verdict: mergeable after a fix round

## Findings (verified defects only, most severe first)

### F1 — should-fix · A YouTube video's page link is stored as a dead `/watch` address
- **Where:** `packages/shared/src/spaces/contacts.ts:79–84` (YOUTUBE: hosts `youtube.com`, `m.youtube.com`) with `networkAddress`, `:120–126` (keeps the path, drops the query; Facebook's `profile.php?id` is the only exception).
- **Seen in the code.** `normaliseContact('YOUTUBE', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')`: no handle → `linkOf` → host `youtube.com` is on the list → path `/watch` is not empty → stored `https://www.youtube.com/watch`. The same for `/playlist?list=…` → `/playlist` and `/results?search_query=…` → `/results`. No test covers it (T4 has `@h`, `/channel/…`, `m.youtube.com`, `youtu.be`).
- **Scenario:** from the day of merge the current editor offers YouTube. An owner copies a video's address from the browser bar; it is accepted, saved, and the public page links visitors to `youtube.com/watch` with no video, which opens YouTube's home. `youtu.be` is refused on the ground that "a video is no channel" (plan §8, data-model line 19), but the same video through `youtube.com/watch` passes and loses its id. `data-model.md:19` says "a YouTube channel on `www.youtube.com`", which the rule does not hold.
- **Fix:** refuse YouTube addresses whose path names no channel: allow `/@h`, `/channel/…`, `/c/…`, `/user/…` (Review Focus keeps `/c/` and `/user/`), refuse `/watch`, `/shorts/…`, `/playlist`, `/results`, `/live/…`. A per-network path rule on `Network` is enough, the way `handlePath` became optional. T4 gains `youtube.com/watch?v=abc` → `invalid_format`. · **Belongs:** a fix round on #140, folded into `29bcf80a`. Facebook's `facebook.com/watch?v=…` → `/watch` has the same flaw and predates #48: put it in finding **218** (see F2).

### F2 — should-fix · «وسيلة أخرى» stores a mistyped number as a link to an IP address
- **Where:** `packages/shared/src/spaces/contacts.ts:159–160` (`normalisePhone(value) ?? websiteAddress(value)`) through `linkOf`, `:87–97` (accepts a host when `hostname.includes('.')`).
- **Seen in the code;** the host parsing follows the WHATWG URL standard (not run here: running `node` needed an approval). `'599123456'` (a mobile written without its 0) fails the phone rule, which needs `+970`/`+972`/`00…`/`0`. `linkOf` then reads `https://599123456`: in a special-scheme URL, a host made of one number up to 2³²−1 is parsed as IPv4. The hostname becomes `35.181.230.0`, it contains a dot, and `websiteAddress` stores `https://35.181.230.0`. Every Gaza mobile typed without its leading 0 (`59…`/`56…`, 9 digits) ends up like this, as does any short number (`1800` → `https://0.0.7.8`). T5 checks `+44 20 7946 0000` (refused only because of its spaces) and `two words`, not a bare number.
- **Scenario:** after #142 offers «وسيلة أخرى», an owner adds «سيجنال» with `599123456`. The rule meant to refuse it (SD4: a number by the phone rule, else a web link) saves it instead, and visitors see a link to an IP address rather than a call. Through the API this can happen from #140's merge.
- **Fix:** in the `OTHER` branch, a value made only of digits, `+` and the phone rule's separators that `normalisePhone` refuses is refused (`invalid_format`) and never read as a link. T5 gains `599123456` and `1800` → `invalid_format`. · **Belongs:** a fix round on #140, folded into `29bcf80a`. WEBSITE has had the same `linkOf` path since #48 (`123` → `https://0.0.0.123`). Record it, with F1's Facebook case, as finding **218**: "a website's bare number is stored as an IP address; a Facebook video link loses its id". Fixing it inside `linkOf` would change an existing type, which T6 keeps unchanged.

### F3 — should-fix · T19's package case is missing, and EC8 (T16–T20) was moved to a web-only PR without saying so
- **Where:** `apps/api/src/modules/spaces/hours/hours.api.test.ts:205` has the case "a shift a price uses" (409). No test in the file names a package (`git grep -i package` finds nothing there or in `hours.service.ts`). The report, §4 EC8, says "PR-C (T16–T20 are its checks)". The departures (§9) do not list it.
- **Seen in the code and only in the report.** §12's API rows (T9–T20) are `test:api`. §2 makes PR-A the only PR with an API change, and §8's PR-C list is `apps/web/src/` only. EC8 says "add only the missing ones, each proven by reverting its code once", and T19 says "(the package case added if missing)". It is missing. T16–T18 and T20 have near matches (`keeps each named shift's id…`, `confirm.api.test.ts`, `photos.api.test.ts:505`, `list.api.test.ts:102`), but nobody has checked them by name against T16–T20 or proven them by a break.
- **Scenario:** SD5 and T43 rest on the server's 409 for a shift a package uses (finding 216: the admin can only rely on it). The FK is `NoAction` (`schema.prisma:644`), so the 409 is likely, but nothing proves it. PR-C, being web-only, will either change an API test file outside its list or leave the gap.
- **Fix:** run EC8 now. Name the existing test behind each of T16–T18 and T20 in the PR, and add T19's package case (an owner's package on a shift; `PUT …/hours` leaving the shift out → 409, nothing written, no audit), seen failing by a break restored from a `cp` backup. · **Belongs:** a fix round on #140 as its own `test(spaces): …` commit, since the behaviour is not contacts. Alternatively, the owner adds `hours.api.test.ts` to PR-C's files explicitly.

### F4 — should-fix · T5 is weaker: no contact reads Arabic-Indic digits, against C2's "as today", and no finding was recorded
- **Where:** `packages/shared/src/core/phone.ts` (`/^(?:(?:\+|00)(970|972)|0)(\d+)$/`: `\d` without `u` is ASCII only). In the web, `toWesternDigits` is used only by `clockTime.ts`, `shekels.ts` and `wholeNumber.ts`, never by a contact or phone form. `packages/shared/src/spaces/contacts.unit.test.ts` drops T5's `٠٥٩٩١٢٣٤٥٦` case.
- **Seen in the code** (the report's §7 says the same). C2 (binding, for PR-C's Sheet) says the value is "normalised as today (Arabic-Indic digits, …)", but today no phone rule reads them. The executor rightly left the platform's phone rule (D6, which customers use too) alone and wrote the reason down. The report then says "offered to the owner, not recorded", while workflow §8 says "an observation or divergence → record a finding".
- **Scenario:** an owner on a phone with an Arabic keyboard types `٠٥٩٩١٢٣٤٥٦` for WhatsApp and is told «رقم غير صالح». This is already true on `main` and will stay true in PR-C's Sheet, which C2 assumes reads it.
- **Fix:** the owner decides whether `normalisePhone` (core, every phone) reads Arabic-Indic digits, and so whether C2 stands as written. · **Belongs:** finding **217**, recorded now (in this fix round or by the owner). If the owner says yes, its own small item before #142, and T5's case comes back there.

### F5 — nit · The current editor mishandles a saved «وسيلة أخرى» in two places (PR-A's window only)
- **Where:** `apps/web/src/features/spaces/hooks/contacts/useContactsSection.ts:33–34, 44, 151–152`; `apps/web/src/features/spaces/hooks/contacts/useReadOnlyContacts.ts:16`.
- **Seen in the code.** (a) A saved `OTHER` row is offered every type (deviation 8). Choosing `WEBSITE` changes `type` but keeps `label` in the row's values. On «حفظ» the schema refuses `contacts.0.label: invalid_format`, but `FIELDS` lists only the value paths, so the refusal has no field, no failure and no focus. Nothing is sent and nothing is said. (b) The admin's read-only view of a verified space names an `OTHER` «وسيلة أخرى», not by its own name (plan §5 lists `useReadOnlyContacts` among the readers, §8 does not).
- **Scenario:** only with an `OTHER` made through the API between #140 and #142.
- **Fix:** none in PR-A. PR-C removes both hooks. Its contacts Sheet must clear (or keep showing) the name when a row leaves `OTHER`, and T41 can assert it. · **Belongs:** PR-C.

### F6 — nit · Plausible: a LinkedIn country-subdomain link is refused
- **Where:** `packages/shared/src/spaces/contacts.ts:74–77` (`hosts: ['linkedin.com']`; `www.` is the only prefix stripped).
- **Seen in the code;** how common such links are is unverified. `https://ps.linkedin.com/in/name` (the form search engines often show) is refused with "paste the page's full link", though it is the full link.
- **Fix:** accept a two-letter subdomain of `linkedin.com` and store it on `www.linkedin.com`, with a T3 case. · **Belongs:** the fix round (folded into `29bcf80a`) if the owner wants it; otherwise drop it.

## The test matrix rows of this PR (present / missing / weaker · would it fail on its break?)

- **T1** Telegram: present (`@`, bare, `t.me/…`, `telegram.me/…?x=1`; `example.com/masaha` refused) · yes.
- **T2** X: present (handle, `twitter.com?s=20`, `mobile.twitter.com`, `x.com`) · yes.
- **T3** LinkedIn: present (company link, `/in/…?trk` path kept, bare name refused) · yes.
- **T4** YouTube: present (`@h`, `/channel/`, `m.youtube.com`, `youtu.be` refused) · yes. It has no `/watch` case, which is how F1 got through.
- **T5** OTHER: **weaker.** The Arabic-Indic case was dropped with a written reason (F4), and no bare-number case exists (F2). `discord.gg`, `059-912 3456`, `+44 …` and `two words` are present · yes for what is asserted.
- **T6** existing rules: present (the existing tests are untouched; only the helper's signature changed) · yes.
- **T7** label rules: present, every sub-case (`required` both ways, `too_short`, `too_long`, bidi `invalid_format`, WHATSAPP `invalid_format`, trimmed / `null` output, `TWITTER` `invalid_choice`, two OTHERs `not_unique`). It sits in `contacts.unit.test.ts` (deviation 7) · yes. The break was made (rule dropped: 2 red).
- **T9** stored forms, labels, order, audit `after`: present · yes.
- **T10** 422 codes; nothing written; date unchanged: present · yes.
- **T11** a label alone is a change: present. The `beforeEach` dates the group `BEFORE`, so the compare matters · yes (break made: values-only compare).
- **T12** the CHECK by raw inserts (NULL label, blank `'  '`, WHATSAPP with a label; valid ones pass): present in `apps/api/src/db/schema.api.test.ts` · yes (constraint dropped once in `masaha_test`).
- **T13** public page's label / `null`: present (`page.api.test.ts`) · yes.
- **T14** managed route: present (the existing rows' body is now an `OTHER`: owner 200, reception 403, strangers/unrelated owner/admin 404) · yes.
- **T15** existing rows untouched: EC5 (58 rows, equal by type, zero labels). Only in the report.
- **T16–T20:** **not done here.** T19's package case is **missing** (F3).
- **T27** `contactLinkOf`: present (wa.me, `tel:` with carrier, `mailto:`, the four networks external with `ownName: false`, OTHER link external named by its label, OTHER number `tel:`) · yes.
- **T53** catalogue parity: the existing test with the new keys · yes.
- Beyond the matrix: `mapsLink` (latitude first; break: swapped), the public page's `dir="auto"` on the own name, and the editor hook's three tests (no OTHER offered, a saved OTHER kept with its name, LinkedIn's own refusal) · each would fail on its break.
- No test cannot fail, none is bent to pass, and no production code exists only for a test.

## Decisions, ODs, DIs and SDs of this PR (built / departed, judged)

- **M4** (four networks + «وسيلة أخرى» with its name, `CONTACT_TYPES`, the migration): built. The YouTube rule departs from its own stated intent (F1).
- **C1 types / §8 order** (`WHATSAPP … WEBSITE, OTHER`, twelve): built.
- **C2** "normalised as today (Arabic-Indic digits…)": its premise is false today (F4). It is PR-C's to build, and the owner's to settle first.
- **SD1** (contact and map links in `shared/lib`, the words as a parameter): built. A1 is a pure move plus `mapsLink`, and the directory's callers are re-aimed. `git grep contactLinks|directionsTo` finds nothing left.
- **SD4** (OTHER: phone rule, else a web link): built, but a bare number that fails the phone rule becomes an IP link (F2).
- **§7 migration:** built exactly as shown. Five `ADD VALUE` (appended, as Prisma's enum lists them after `WEBSITE`), `label TEXT` with no default and no `UPDATE`, and the CHECK with `"type"::text`. There is no drift: Prisma's `label String?` has no `@map` and the column is `label`, and Prisma compares no CHECK. PostgreSQL 18 (compose and CI) allows `ADD VALUE` in a transaction, and the CHECK uses no new value as an enum literal. Existing rows are all old types with NULL, so the CHECK holds when added. The unique key is unchanged. `btrim` trims spaces only, where the schema's `trim()` trims all whitespace; the CHECK is a backstop, so this is acceptable.
- **OD1 (a)** three PRs, A first: kept. **EC10:** the description says one migration runs online, with the revert path.
- **§17 merge day** for #140: matches the description's "What changes on merge".
- **A3:** nothing built or reserved.
- **The plan's PR-A editor minimum** (four networks offered, no OTHER, `label: null` sent): built. A saved OTHER is kept (deviation 8, F5).

## The report's deviations, judged

- **6 — T5's Arabic-Indic case not asserted:** acceptable (it does not change D6's platform rule silently). **Wrong** not to record a finding (F4 → 217).
- **7 — T7 in `contacts.unit.test.ts`:** sound (the schema's existing tests live there).
- **8 — the editor offers OTHER on a saved OTHER row:** sound. It keeps the name through a save, but leaving OTHER keeps the label silently (F5, PR-C's to carry).
- **9 — the audit names a label only where one is held:** sound (old entries keep their shape; the contract says it).
- **10 — T14 by the existing managed rows with an OTHER body:** sound, and what T14 asks.
- **11 — a throwaway `masaha_wi140_dev` for the real run:** sound (`masaha_dev` was never seeded or written beyond §7).
- **EC8 → PR-C (not in the departures list):** **wrong.** It is undeclared, and it sends API-lane rows to a web-only PR (F3).
- **EC7 → PR-C (icons):** sound. **EC9** partial («الأسعار المعلنة», «سعر» with PR-C): sound.
- §6/§7 problems (Docker restart, encoding, a refused kill, `masaha_test` holding the migration): no effect on the head.

## Documents

- `api-contract.md`: `Contact` (twelve types, `label`), the body's `label` rules and codes, the audit's shape: true to the code. A label sent blank on a non-OTHER type gives `too_short`, not the `invalid_format` the line implies. The web never sends one, so I do not report it.
- `data-model.md`: the contacts convention and the CHECK in *later migrations*: true, except line 19's "a YouTube channel" (F1).
- `features/spaces.md` (API decision, web decision, both histories) and `features/directory.md` (decision, code map naming `@shared/lib`'s `contactLinkOf` and `mapsLink`, history): true.
- `glossary.md` (EC9: «وسيلة تواصل», the twelve, «وسيلة أخرى»): true.
- The PR description matches the head. Its claims each name a test or command.
- Both catalogues gain every new key (types, examples, `linkOnly`), in both languages. No hardcoded text; no class or colour outside the design system (`dir="auto"` is an attribute).

## Scope and commits

- `4622a003` `refactor(lib): share the contact and map links` (9 files, no behaviour change) and `29bcf80a` `feat(spaces): contacts of any kind` (30 files) match §14's A1/A2. Subjects are ≤ 50 characters, the bodies explain why, and there is no attribution or `fixup!`.
- The 37 files are §8's PR-A list, plus `apps/api/src/db/schema.api.test.ts` (T12's place by the data model's rule), the test fixtures given `label: null` (`publicSpace.ts`, `useSpacePage`'s test, the repository's unit test) and `SpacePageView.ts`. Nothing is outside the item. No file is shared with #141.
- Authorization is unchanged and stays on the server: the same `validate(updateSpaceContactsSchema)` guards both routes, and T14 covers the roles.

## Not checked, and why

- No lane, build, `node`, server or database was run (the rules). F2's host parsing rests on the WHATWG URL standard; a `node -e new URL(...)` check needed an approval I did not take.
- EC5's before/after counts, the real run and the screenshots (`Downloads\wi140-shots`): only in the report, not seen.
- Production data (OD7): out of reach.
- #141 and the PR-C items of the report: not this role.

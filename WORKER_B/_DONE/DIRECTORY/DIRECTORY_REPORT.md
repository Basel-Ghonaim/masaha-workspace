# DIRECTORY — report (worker B)

## 1. The pull request and its head

**PR:** [#73](https://github.com/Basel-Ghonaim/masaha/pull/73), `feat(directory): the public directory's API`.
- Labels `feat`, `area:api`, `area:docs`; assigned to the owner; `Closes #69`.
- Branch `feat/public-directory`, cut from `origin/main` at `e30a86c`.
- **Head `28275b226047780f666008c9cf7f9a1a199099b3`.** CI passed on this head: lint, format:check, typecheck, test:unit, check:classes, check:links, test:api, test:component, build, and CodeRabbit (no comments). GitHub shows `CLEAN`.
- Not merged.

## 2. The commits

1. `99c2944` **docs(api): name both refusals of a price amount.** This is D9 and Issue #69: the prices line now names `out_of_range` outside 1–10,000,000 and `invalid_format` for a non-integer.
2. `315ce37` **feat(directory): the public directory's reads.**
   - **The migration** `20261013083824_directory_search`: `pg_trgm`, plus two SQL functions, `masaha_search_text` (the normaliser) and `masaha_search_score` (containment, else `word_similarity`).
   - **`@masaha/shared/directory`:** its requests and responses.
   - **`lookups`:** `listedAreaIds`, `areaMatches` and `activeAmenitiesNamed`.
   - **`space-links`:** `verifiedSpaceIds`.
   - **`spaces`:**
     - `public/`: the listing in raw SQL, and the page read under the share lock;
     - the hours repository's `weeksFor`;
     - `pricesHidden` in `staleness.ts`;
     - `findShownBySlug`.
   - **`directory` module:** the service, controller and router, and the caching.
   - **Endpoints:** `GET /spaces` (without distance), `GET /map/spaces` and `GET /spaces/:slug`.
   - **Tests:** the list, pins and page tests.
   - **Documents:** the contract, `directory.md` (new), its map line, `spaces.md`, `lookups.md`, `space-links.md`, the data model, conventions §9, the overview's *Built* line and the plan's rows.
3. `28275b2` **feat(directory): sort the directory by distance.**
   - The `Masaha-Near` header, read with the query by a directory middleware and kept on `res.locals`.
   - The header's redaction in the request logger.
   - The `no-store` answer, and `distanceMeters`.
   - **Tests:** the near tests, including the whole-line log proof.
   - **Documents:** security.md's new *Location* section, the overview's *Near me* line, foundation §13, and the contract.

## 3. What was run, and what was not

**Run once each, on the head, one at a time.** Before the API lane I checked that no vitest process was running. Worker A's component run on `features/spaces/components/editor` was in progress, so I waited for it to end.

| Run | Result |
|---|---|
| `test:unit` | shared 11 files, 205 tests · api 36 files, 667 tests · web 67 files, 734 tests: all passed |
| `test:api` | 44 files, 724 tests passed |
| `lint` | clean |
| `typecheck` | clean |
| `format:check` | clean |
| `check:links` | 1,975 links in 111 documents resolve |
| `prisma migrate diff`, database to schema | empty: no drift |

Lint, typecheck and the directory's tests were also run on commit 2's own tree before it was committed.

**Real requests against 3321.** I used the dev data plus 24 temporary spaces, removed afterwards.
- **The list, `?area=2,3&limit=10`:**
  - page 1 and page 2: `totalRecords` 24, `totalPages` 3;
  - `Cache-Control: public, max-age=30` and a weak ETag.
- **`openFriday=true`:** only the one space with Friday open.
- **Search:** a typo («مصاحة الابداع»), mixed hamzas («الأبداع») and an English typo ("Ibdea") each found «مساحة الإبداع / Al-Ibdaa Hub».
- **`sort=distance` with `Masaha-Near: 31.523,34.452`:**
  - `Cache-Control: no-store`;
  - distances 0 m, 100 m, 100 m, 300 m, …;
  - a 4-decimal point answered 422 `near: invalid_format`.
- **Pins:** `area=2,3` answered all 24 with `truncated: false`; `bounds=31.5,34.4,31.52,34.46` answered 13.
- **The page:** a space's page came back whole; a hidden space answered 404.
- **Caching:** a repeat with `If-None-Match` answered **304**.
- **The log:** of 1,168 lines, none held `31.523`, `34.452` or `31.5234`. The header appears only as `"masaha-near": "[Redacted]"`.

The server was stopped by PID (tsx watch, the server and pino-pretty), and port 3321 is free.

**Not run locally:** `test:component`, the build and `check:build`. Nothing in `apps/web` changes, and nothing there imports `@masaha/shared/directory`. CI ran all three, and they passed.

## 4. The breaks made, and the tests seen failing

The code was written before its tests. Each new test was proven by breaking or reverting its code once, as testing §3 rule 5 allows for code that already exists, and each break was restored.

- **The `NOT s.is_hidden` clause removed.** The publicly-listed test failed.
- **`SEARCH_THRESHOLD` set to 0.6.** The English typo, Arabic typo and ranking tests failed.
- **The hidden-price rule removed from the query (`pricesShown = TRUE`).** The stale-unverified test failed.
- **`masaha_search_text` replaced by `lower()` in the test database.**
  - At first only the tashkeel test failed. The hamza and ة cases still matched through trigram similarity alone, so they did not prove the fold.
  - I added a test («مركز إقرأ» found by `اقرا`, «دار الأمل» by `امل»), whose scores without the fold are 0 and 0.25. It failed, and the function was restored.
- **The `masaha-near` redaction path removed.** The whole-line log test failed.
- **The pins' look-ahead (`ceiling + 1`) removed.** The 1,001-space truncation test failed.
- **The listed-area check removed from the page.** The hidden area and hidden governorate 404 tests failed.
- **The verified check removed from `pricesHidden`.** Its unit test failed.
- **The 3-decimal limit and the empty-`q` refinement removed** (each once). Their shared unit tests failed.
- **Not proven by a break:** the tie by id under the default order. Postgres tends to return equal rows in insertion order anyway, so removing `, id` may not fail. The distance tie test asks for page 2 of one-row pages.

## 5. Problems met, and how each was solved

- **The `\u` escapes became literal characters.**
  - The Write tool, and Bash heredocs, turn `\uXXXX` into the characters themselves. The tashkeel regex in `requests.ts`, three test strings and the migration's regex were written as invisible characters.
  - The behaviour was right, but the source was unreadable. I rewrote them as escapes through a script that builds the backslash from `chr(92)`.
  - The migration was not yet committed, so I re-applied it to `masaha_b_dev` and `masaha_b_test`.
  - Postgres reads `ً` in a regex: `masaha_search_text('مَسـاحة   الإبداع')` gives `مساحه الابداع`.
- **Python wrote CRLF.** Editing on Windows in text mode turned three lookups files into CRLF. I converted them back to LF, and every later edit writes with `newline=''`.
- **A second SQL function.** To keep the matching rule in one place, I added `masaha_search_score` beside the normaliser. The migration was re-applied before it was committed.
- **ES2023 lib.** `Map.groupBy` is ES2024, so I grouped by hand.
- **Fakes in older unit tests.** `lookups.service.unit.test.ts` and `space-links.service.unit.test.ts` build whole service or repository objects, so they gained stubs for the new functions.
- **The test data's prices.** Price rows with no prices date fell outside the hidden-price rule. Real saves always date the group, so the tests now date it.

## 6. What behaved unexpectedly

- **ICU's root collation (`und-x-icu`) orders Latin before Arabic.** The plan's "by name" in Arabic put "Mike" before «باب». I now use each language's collation, `ar-x-icu` for `lang=ar` (Arabic names first) and `en-x-icu` for `en`. Both exist in the local Postgres 18; Neon builds with ICU, but I have not checked those two on Neon.
- **The trigram similarity alone already forgives most hamza and ة differences in longer names.** Only short words, or several hamzas, need the fold. The added test covers this, as §4 says.
- **Express sets an ETag on error answers too** (the 422 and 404 above carry one). This is harmless, and I left it alone.
- **Distances with the same rounded value keep their true order.** "Run Space 12, 100 m" came before "Run Space 11, 100 m", because the order uses the exact distance, not the rounded one.

## 7. The early conflict check

`gh pr list --state open` shows only #73, so there is no other head to merge against.

## 8. Departures from the prompt and the plan

- **Commits:** 3, not the plan's 5.
  - #69 stands alone, and the location ("sort by distance") has its own commit, so the privacy review sees it whole.
  - The list, the pins and the page are one commit, "the public directory's reads". They share one service, one router, one shared schema file and one SQL builder, so splitting them would have created intermediate states that exist only for the history.
- **Collation:** `ar-x-icu` and `en-x-icu` instead of the plan's `und-x-icu` (§6).
- **A second SQL function**, `masaha_search_score`, so the "contained, else similar" rule is the database's alone, like the normaliser. The data model records both.
- **The name score** is computed per name (English and Arabic separately) and per area name, not over "nameEn + nameAr" joined. A query spanning both names would otherwise match oddly.
- **`period` alone** (no bounds) keeps the spaces with a general price of that period, under the same hiding rule. The plan only said a bound needs a period. It is documented in the contract's filter line as "within the bounds", which are open.
- **Test helpers** were added to `apps/api/test/spaces.ts`, as the plan allowed: `createPublicSpace`, `setWeek`, `addPrice`, and names for `createArea`.

## For the analyst and the owner

- **The privacy line.** The prototype's `PRIVACY_LINE` («يبقى موقعك على جهازك فقط، ولا يُرسَل إلى أي جهة.», `shared.jsx`, shown in `LocationStatus`'s four states) is now untrue: the location is sent, in a header, only to sort. Per the reply, the account design fixer rewords it in `shared.jsx` this round. The web must use the new wording when the screen is built.
- **For the web (worker A, step 3):**
  - round the location with `toFixed(3)` and send it in `Masaha-Near`, with `sort=distance` only;
  - price bounds are in agorot;
  - the governorate comes from the public catalogue, by the area's id;
  - Home's counts per area come from the pins' `areaId`.
- **Findings 61 and 62:** not used.
- **An independent review follows** (privacy, a migration).

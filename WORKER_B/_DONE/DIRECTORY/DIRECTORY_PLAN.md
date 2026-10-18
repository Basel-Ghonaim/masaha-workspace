# DIRECTORY — the public directory's API (worker B) — plan

> **Approved 2026-10-13** with the owner's reply (`DIRECTORY_PLAN_REPLY.md`), folded in below. Changes from the draft:
> - the location travels in the `Masaha-Near` header, not the query;
> - precision is 3 decimals, not 2;
> - no finding 61;
> - a `q` that normalises to nothing is refused;
> - the PR title is `feat(directory): …`;
> - S2, S9 and D4 are approved as proposed.

## 1. Summary

Build step 3's API: what anyone reads without signing in, over the **publicly listed** spaces
(data-model › Derived values).

- `GET /spaces`: a list, paged and filtered on the server (D1).
- `GET /map/spaces`: the map's light pins, for the whole filtered set (D3).
- `GET /spaces/:slug`: a space's public page (D8).

Search is forgiving: Arabic is normalised and the match is typo-tolerant, through `pg_trgm` (D6).
"Near me" sorts on the server. The device rounds the location and sends it in a request header,
only to sort by distance; the server never stores or logs it (D2). The documents that said the
location never leaves the device are rewritten, dated as the owner's change. Issue #69 is closed in a
commit of its own (D9).

The work sits in the `directory` module (L5, public router), which conventions §7 has already
reserved for it. `directory` composes `spaces` (L1), `space-links` (L2), `lookups` and
`platform-settings` (L0) by conventions §5 and §9, *Composed reads*.

## 2. The contract

**Scope**
- `GET /spaces`:
  - filters: `area`, `period` + `priceMin`/`priceMax`, `studentPrices`, `openFriday`, `verified`, `q`;
  - sorts: `updated` (the default), `name`, `distance` (needs the `Masaha-Near` header), `relevance` (the default when `q` is given);
  - pages by §4;
  - cached for 30 s with a validator; `no-store` when sorted by distance.
- `GET /map/spaces`: the same filters, no paging, `bounds`, a ceiling of 1,000 pins, and the same cache.
- `GET /spaces/:slug`: the public page, the same cache; `not_found` unless the space is publicly listed.
- A migration: `pg_trgm` and one SQL function, `masaha_search_text`. No table changes.
- The request log redacts the `Masaha-Near` header.
- The documents (§7 of the prompt), and #69.

**Acceptance criteria**
- [ ] Only publicly listed spaces appear anywhere. Hidden spaces, soft-deleted spaces, and spaces in an inactive area or governorate are left out. A page for any of those answers 404.
- [ ] Every filter applies before the page is cut. Every page is full and the total is right. Ties are ordered by `id` under every sort.
- [ ] A search finds a space by either of its names or either of its area's names, and finds it:
  - with a typo;
  - with mixed hamzas (أ إ آ);
  - with ة/ه or ى/ي swapped;
  - with tashkeel or tatweel.

  With `q`, results are ranked best match first.
- [ ] A `q` that normalises to nothing (only tashkeel, tatweel or spaces) is refused with `invalid_format`.
- [ ] The price filter:
  - reads the general audience's prices for the period;
  - leaves out an unverified space whose prices are stale.

  `studentPrices` follows the same hiding rule (S5).
- [ ] `openFriday` keeps only spaces whose Friday is open. Spaces with no hours are left out.
- [ ] A list item and a pin carry no prices, capacity, counts, live status or photo.
- [ ] The page carries:
  - the profile, the hours with the shifts, and the prices by audience. Prices are `null` when hidden: unverified and stale;
  - one amenities list: the active common ones, then the space's own;
  - the contacts, each group's date, the stale groups, and verified.

  It carries no capacity, counts, live status or announcements.
- [ ] The `Masaha-Near` header:
  - has at most 3 decimals per coordinate and lies inside the Strip's box;
  - is sent only with `sort=distance`, and is required with it;
  - its answer is `no-store` and carries `distanceMeters` rounded to 100 m.

  No log line holds it; an API test proves this, with the break made once.
- [ ] A repeated list request with its ETag answers 304. Answers not sorted by distance carry `Cache-Control: public, max-age=30`.
- [ ] Pins: the whole filtered set up to 1,000. Past that, the first 1,000 by id, with `truncated: true`. `bounds` narrows the set to the map's viewport.
- [ ] The documents are updated as §7 below lists. #69 is closed.

**Out of scope**
- Live status and `availableNow` (step 7).
- Announcements, reports and favourites (step 10).
- Photos and a cover thumbnail (a later decision; U12's API part).
- Every screen: the web is worker A's.
- The prototype's privacy line: the account design fixer rewords it in `shared.jsx` this round.
- Counts per area for Home: the device derives them from the pins' `areaId` (S2); no endpoint.

## 3. Reading done

- **Bootstrap:** CLAUDE.md, the workflow, the docs map, and the findings index.
- **Capabilities:** `features/spaces.md`, `lookups.md`, and `space-links.md` (its composition of the admin list).
- **Plan and scope:** `plans/v1-mvp.md` › step 3 and the planned public rows; `project/overview.md` › Public site; `foundation.md` §13 › Directory.
- **Data model:** Conventions, Spaces, Derived values.
- **Contract:** §1–§4, §5 (*Lookups (public)*, *Spaces (the admin)*), and §6.
- **Backend:** `conventions.md` §1–§13 (§5, §9 *Composed reads*, §10, §11, §12, §13); `security.md` (rate limits, redaction, hardening); `testing.md` §1–§4.
- **ADRs:** 0008 and 0014. `documentation.md` §5 and `shared-package.md` (*Adding a capability*).
- **Design:** `DECISIONS_PUBLIC.md` (the *Changed 2026-10-13* and *Amended* notes, U1–U5, U9, U12). The prototype's `Directory.html`, `Home.html`, `Space details.html` and their scripts (`shared.jsx` `PRIVACY_LINE`, `location.jsx`, `map.jsx`, `space-parts.jsx`).
- **Issue #69.** Open findings: I opened 17 and 23; none are folded (§6).
- **Code:**
  - `app.ts`: mounting, the general limits, and the clock;
  - `spaces/listing/*`, `staleness.ts`, `space/space.service.ts` (the share-locked read), `facts/facts.ts`, `hours/hours.repository.ts`;
  - `space-links/admin-spaces/*` (the composition pattern, `findVerifiedSpaceIds`);
  - `lookups/lookups.service.ts`, `lookups.repository.ts` and its public router;
  - `shared/http/requestLogging.ts`: pino-http's default serializer logs `req.url`, `req.query` and the headers;
  - `packages/shared` `core/pagination.ts`, `spaces/responses.ts`, `gazaStrip.ts`;
  - the API test helpers, including log capture through `createLogger('info', Writable)`.
- **Checked in the database** (`masaha_b_dev`, in a rolled-back transaction):
  - `pg_trgm` 1.6 is available;
  - the databases are `en_US.utf8`;
  - `show_trgm('مساحة')` yields trigrams, so Arabic is indexed;
  - `word_similarity('مصاحه','مساحه الرمال') = 0.33` and `word_similarity('fucus','focus hub') = 0.33`;
  - the `und-x-icu` collation exists.

  Neon lists `pg_trgm` 1.6 for Postgres 17 and 18 (neon.com/docs/extensions/pg-extensions).

## 4. The settled decisions, as built

**D1 — the paged, filtered list.**
`GET /spaces?area=&period=&priceMin=&priceMax=&studentPrices=&openFriday=&verified=&q=&sort=&lang=&page=&limit=`, plus the `Masaha-Near` header for `sort=distance`.
- **`area`:** a comma list of area ids, at most 50. It is intersected with the listed areas, so an inactive or unknown id narrows to nothing rather than being refused.
- **Price:**
  - `period` is one of `PRICE_PERIODS` (`HOUR|DAY|WEEK|MONTH`);
  - `priceMin` and `priceMax` are **in agorot** (S4), integers from 1 to 10,000,000, inclusive;
  - `period` is required with a bound (`required` on `period`), and a bound is refused without `period`;
  - `priceMin > priceMax` is `out_of_range` on `priceMax`;
  - a space matches when it has a `GENERAL` price for that period within the bounds, any shift or label;
  - an unverified space whose prices are stale never matches (data model).
- **`studentPrices=true`:** at least one `STUDENT` price, under the same hiding rule (S5).
- **`openFriday=true`:** the Friday row (weekday 5) exists and is not closed.
- **`verified=true`:** the space has an active `OWNER` link, resolved to ids by `space-links`.
- **`q`:** 1–80 characters (`textSchema`). A `q` with no searchable character is `invalid_format` (owner's addition). That means one made only of tashkeel (U+064B–U+065F, U+0670), tatweel (U+0640) or whitespace. A shared refinement checks that a searchable character is left; the normalisation itself stays in SQL. See D6.
- **`sort`:**
  - `updated`: the default without `q`; the latest of the groups' dates, newest first;
  - `name`: the display name in `lang` (`ar`: `coalesce(nameAr, nameEn)`; `en`: `nameEn`), `COLLATE "und-x-icu"`;
  - `distance`: needs the `Masaha-Near` header (D2);
  - `relevance`: the default with `q`; refused without it (`invalid_choice`).

  Every sort ends with `id`.
- **Paging:** `page` and `limit` by §4 (default 20, max 50); a page beyond the last answers an empty page with the right `meta`, as the admin list does. No `amenities`, no price sort, no `availableNow`: an unknown parameter is ignored, as elsewhere.

**D2 — "near me" on the server, for privacy** (security.md owns the rules; the owner's decisions 4 and 5).
- **The `Masaha-Near: lat,lng` request header:**
  - the point travels in a header, never in the query. The hosting's own request log, and every proxy's, records URLs, and Masaha cannot redact either; a header reaches neither;
  - each coordinate has **at most 3 decimals**. The server **refuses more** (`invalid_format` on `near`), so a client that forgets to round fails loudly instead of sending a precise location (S3);
  - it lies inside `GAZA_STRIP_BOUNDS` (`out_of_range` on `near`);
  - `sort=distance` without the header is `required` on `near`; the header without `sort=distance` is `invalid_choice` on `near`. The location travels only to sort.
- **How it is read.** A directory-only middleware validates the query and the header together, against one shared schema whose field is `near`. It keeps the result in `res.locals`, never on `req`, so nothing the logger serializes ever holds the parsed point.
- **Why 3 decimals** (the owner): 0.001° is about 110 m north–south and 95 m east–west at 31.4° N. Spaces in Gaza sit close together, and at about a kilometre "near me" would lose its meaning inside a neighbourhood. Sent in a header, and never stored or logged, a 110 m square names a block of many buildings, not a home. Its error, at most about 75 m, is far inside the 2 km accuracy below which foundation §13 drops a location.
- **The answer:**
  - each item carries `distanceMeters`, straight-line (haversine, R = 6,371 km) from the rounded point, rounded to 100 m;
  - the answer is `Cache-Control: no-store`, so nothing caches it.
- **Never stored or logged:**
  - pino-http's default serializer logs the request's headers, so `req.headers["masaha-near"]` joins the redaction paths;
  - the value is never written to the database: the query passes it as a parameter and stores nothing. The rate limiter keys by address;
  - a 422 carries field codes only.

  An API test reads the whole log line of a real request for the digits (S6), with the break made once.
- **CORS:** the web and the API share one origin (ADR 0014), so the header needs no preflight rule. The `cors` package reflects requested headers anyway.
- **Documents:** `overview.md` › *Near me*, foundation §13's rule, and security.md's new *Location* section all say: "sent in a header, only to sort by distance, rounded on the device to 3 decimals, never stored or logged (the owner's change, 2026-10-13)". The prototype's `PRIVACY_LINE` («يبقى موقعك على جهازك فقط…») becomes untrue. The account design fixer rewords it in `shared.jsx` this round (the analyst routed it), and the report says so.

**D3 — `GET /map/spaces`** (named for the slug clash in S1).
- The same filters as the list, with no paging and no sort.
- `bounds=south,west,north,east`, optional: the map's viewport. A malformed one, or one with south ≥ north, is `invalid_format`.
- **The answer:** `{ pins: MapPin[], truncated: boolean }`:
  - `MapPin = { id, slug, nameEn, nameAr, areaId, location, isVerified, days }` (S2);
  - at most **1,000** (`MAP_PINS_CEILING`): past it, the first 1,000 by id, with `truncated: true`, and the web asks again within the viewport's `bounds`.
- **Size:** 1,000 pins with their weeks come to about 150 kB raw and about 25 kB gzip.
- It is an exception in §4 (whole, without `page` or `meta`).

**D4 — the card.**
`DirectorySpace = { id, slug, nameEn, nameAr, area: { id, nameAr, nameEn }, isVerified, days, distanceMeters? }`.
- `days` is the week (D5) or `null` while the hours are missing.
- No prices, photo, capacity or live status.
- **Freshness:** none, since the prototype's card shows none. The sort reads the dates on the server.
- The device finds the governorate from the public catalogue it already holds for the area filter.

**D5 — the week's hours go to the device.**
- `days: (OpeningRange | null)[]`, 7 entries, Sunday first, the admin's shape.
- The device computes "today" in Asia/Gaza at view time.
- `openFriday` is derived on the server from the same rows (weekday 5).

**D6 — forgiving search, with `pg_trgm`.**
- **One migration** (created once with `migrate dev --create-only`, then `ls`; applied to `masaha_b_dev` and the test lane's database):
  - `CREATE EXTENSION IF NOT EXISTS pg_trgm`;
  - an `IMMUTABLE PARALLEL SAFE` SQL function, `masaha_search_text(text)`. It lowercases, removes tashkeel (U+064B–U+065F, U+0670) and tatweel (U+0640), folds أ إ آ ٱ → ا, ة → ه and ى → ي, and collapses spaces.

  `schema.prisma` does not change. Prisma ignores functions, and ignores extensions without the `postgresqlExtensions` preview, so later migrations leave both alone.
- **One rule in one place:** the function normalises the stored names and the query alike, so there is no TypeScript copy of the rule. The shared refinement only checks that a searchable character is left.
- **The match:**
  - `score = greatest(name score, area score)`;
  - the name score is 1 when the normalised `q` is contained in the normalised `nameEn || ' ' || nameAr`, else `word_similarity(q, …)`;
  - the area score comes from `lookups`, by the same rule, over the area's Arabic and English names (not its governorate's);
  - a space matches when `score ≥ 0.3`, pg_trgm's own default `similarity_threshold`, which the probes above put at a one-letter typo;
  - `relevance` orders by `score desc, id`.
- **At a thousand spaces, no trigram index:** a scan of 1,000 short names is a few milliseconds, and "indexes only for queries that run". An expression index Prisma does not know would be dropped by a later migration.
- **Against an in-app similarity:** that would load every listed space into the function's memory on each search, then cut the page in JavaScript, against conventions §5 ("filter before paginating"). `pg_trgm` keeps one query, set-based. Neon supports it.

**D7 — short caching.**
- The list, the pins and the page: `Cache-Control: public, max-age=30`, plus Express's default weak ETag, which already answers 304 to a matching `If-None-Match`. Nothing disables it today.
- Any answer sorted by distance: `no-store`.
- The pins and the page take the same header as the list (S7).

**D8 — `GET /spaces/:slug`.**
`PublicSpace = { id, slug, nameEn, nameAr, descriptionAr, descriptionEn, area: { id, nameAr, nameEn }, addressAr, addressEn, landmarkAr, landmarkEn, location, isVerified, hours: SpaceHours | null, prices: Price[] | null, amenities: PublicAmenity[], contacts: Contact[], updatedAt: Record<FactGroup, string | null>, staleGroups: FactGroup[] }`.
- `PublicAmenity = { nameAr, nameEn: string | null, icon: AmenityIconKey | null }`: the active common amenities in the platform's order, then its own in its order (icon `null`). A retired amenity is left out (S8).
- `prices: null` when hidden: unverified and stale.
- **It is read like the admin's read,** under the space's share lock (finding 43's reason), through a new `spaces` public read by id. Verified comes from `space-links` just before that read. An owner linked between the two reads shows the page as unverified for one request; this is accepted, since the page holds nothing private.
- **Not found** when the slug is unknown, the space is deleted or hidden, or its area or governorate is inactive.

**D9 — #69:** `docs(api): name both refusals of a price amount`, alone. The prices line names `out_of_range` outside 1–10,000,000 and `invalid_format` for a non-integer. The PR body carries `Closes #69`.

## 5. Stronger decisions

- **S1 — the pins live at `/map/spaces`, not `/spaces/pins`.**
  - Why: slugs come from English names, so a space called "Pins" would hold the slug `pins`, and `/spaces/pins` would shadow its page.
  - Cost: none.
  - Recommended.
- **S2 — a pin also carries `areaId` and the week's `days`.**
  - Why: D3's criterion is what the pin and its selected card need. The prototype's selected card shows the area line and today's hours. `areaId` also gives Home its counts per area, with no endpoint.
  - Cost: about 70 bytes a pin raw.
  - Approved.
- **S3 — the server refuses a coordinate with more than 3 decimals.**
  - Why: the rounding is a privacy rule, so a client that skips it should fail, not send a precise location quietly.
  - Cost: the web must round before sending (`toFixed(3)`).
  - Recommended.
- **S4 — price bounds in agorot.**
  - Why: the contract's one unit for amounts (`amountAgorot`); no float conversion on the server.
  - Cost: the web multiplies the shekel inputs by 100.
  - Recommended.
- **S5 — `studentPrices` follows the hidden-price rule.**
  - Why: a space whose prices the page hides would otherwise be found by "student prices", which it cannot then show.
  - Cost: none. The data model's *Stale prices* line widens from "the price filter" to "the price filters".
  - Recommended.
- **S6 — the redaction's proof reads the whole line.**
  - Why: a test that only checks one header path would miss the URL, the query or a future field.
  - Cost: none.
  - Recommended. The break is made once.
- **S7 — the pins and the page are cached as the list is.**
  - Why: same data, same staleness; a page reopened within 30 s costs nothing.
  - Cost: an admin's edit reaches the public within 30 s.
  - Recommended.
- **S8 — a retired amenity is not shown on the public page.**
  - Why: retiring removes it from what the platform offers. The admin still sees the link.
  - Cost: none.
  - Recommended.
- **S9 — a capability document of its own, `docs/features/directory.md`.**
  - Why: documentation §5 has one document per backend module. `spaces.md`, `lookups.md` and `space-links.md` keep what their modules add.
  - Approved, with its map line.
- **The location's channel:** the header was weighed in the draft against the query. The owner chose the header (decision 4), and it is built as D2 says.
- **No document rule is weakened.** The one commitment changed (the location never sent) is the owner's D2, and it is rewritten in its three homes.

## 6. Related findings

- **17 (counters never swept):** not folded. Guest browsing adds counters per address, as every public route does. Folding it needs the scheduler port (step 7).
- **23 (no per-address ceiling when signed in):** not folded. It is unrelated to public reads.
- **46 (map tiles' headers):** web and deployment. Not this item.
- **New, 61–62:** none planned. The header removes the hosting-log concern (the owner's decision 4). Both numbers stay free for anything found during the build.

## 7. Files

**API (mine)**
- `apps/api/prisma/migrations/<ts>_directory_search/migration.sql`: new.
- `apps/api/src/modules/directory/`: new.
  - `index.ts`, `directory.routes.ts` (public: `/spaces`, `/spaces/:slug`, `/map/spaces`), `directory.controller.ts`, `directory.service.ts` (list, pins, page), `directory.mapper.ts`;
  - the query-and-header validation middleware;
  - `cache.ts`: the Cache-Control rule;
  - `*.api.test.ts`.
- `apps/api/src/modules/spaces/`:
  - `public/`: new. `publicListing.repository.ts` holds the raw SQL: filters, the score, distance, sorts, page and count, the pins with their ceiling and bounds, and the week for a set of ids. Also `publicListing.service.ts` and `publicSpace.service.ts` (the read by id, under the share lock, and the slug's lookup);
  - `staleness.ts`: `pricesHidden(isVerified, dates, cutoffs)` and its unit test;
  - `hours/hours.repository.ts`: the weeks of many spaces;
  - `index.ts`: exports.
- `apps/api/src/modules/lookups/lookups.service.ts` and `lookups.repository.ts`:
  - `listedAreaIds()`: active areas in active governorates;
  - `areaMatches(q)`: `{ id, score }` over the active areas' names, through `masaha_search_text`;
  - `amenitiesNamed(ids)`: active ones, in order, with icon.
- `apps/api/src/modules/space-links/space-links.service.ts`: `verifiedSpaceIds()`, over the existing repository query.
- `apps/api/src/app.ts`: wiring and mounting.
- `apps/api/src/shared/http/requestLogging.ts`: the `masaha-near` header redacted; its proof is in `directory/near.api.test.ts`.
- `apps/api/test/spaces.ts`: helpers to seed hours, prices and links, if the existing ones fall short.

**Shared (mine, the contract)**
- `packages/shared/src/directory/`: new, L5. `index.ts`; `requests.ts` (`directoryQuerySchema`, `mapPinsQuerySchema`, the `near`, `bounds` and searchable-`q` rules) with `requests.unit.test.ts`; `responses.ts`.

**Documents**
- `api-contract.md`: §4 (the planned line replaced by the pins' exception), §5 *Directory (public)*, the prices line (D9).
- `features/directory.md`: new. `README.md`: its map line.
- `features/spaces.md`: the API parts, the code map's API and Shared lines, and a *What it does* bullet.
- `features/lookups.md` and `features/space-links.md`: a bullet and a history line each.
- `data-model.md`: the search function in *Conventions*; *Stale prices* widened (S5).
- `security.md`: *Location*; the redaction line.
- `conventions.md` §9 *Composed reads*: one bullet; the header's *Built* (`directory`).
- `overview.md`: *Near me*, *Built*.
- `foundation.md` §13: *Near me*.
- `plans/v1-mvp.md`: the public rows.
- Findings 61–62, only if the build finds something, and the index.

**Shared with other open items**
- Worker A edits `apps/web` only. No shared type I change reaches the web: `@masaha/shared/directory` is new and nothing in the web imports it. So nothing in `apps/web` changes.
- The documents A may touch are the fast path:
  - `spaces.md`: I keep to the API parts, and to the code map's API and Shared lines;
  - the overview's *Built* line;
  - foundation §13 *Near me*, a rule of the public site that A's admin editor does not touch.
- I touch nothing in `docs/design/`.
- No dependency is added. `pg_trgm` is an extension.

## 8. Design issues

None: this item builds no screen. The prototype's `PRIVACY_LINE` becomes untrue under D2. The account design fixer rewords it in `shared.jsx` this round, and the report records it.

## 9. Tests: lane, test and the break it catches

**Unit: `packages/shared/src/directory/requests.unit.test.ts`**
- `near` (from the header):
  - 3 decimals pass, 4 are refused. Break: dropping the precision check;
  - outside the box: `out_of_range`;
  - without `sort=distance`: `invalid_choice`; `sort=distance` without it: `required`.
- `q` made only of tashkeel, tatweel or spaces: `invalid_format`. Break: dropping the refinement.
- `period` with bounds: missing period is `required`; min > max is `out_of_range`; 0 is refused.
- `relevance` without `q` is refused.
- `area` parsing: commas, at most 50, a malformed id refused.
- `bounds`: format, and south < north.

**Unit: `staleness.unit.test.ts`**
- `pricesHidden` is true only when unverified and stale. Breaks: verified hidden, or missing prices treated as stale.

**API: `directory/list.api.test.ts`**
- Publicly listed only: hidden, deleted, inactive area and inactive governorate spaces are absent. Break: drop each clause.
- Paging: 23 spaces give a full first page and a second of 3, `meta` right, ties by id.
- Each filter:
  - `area` list, including an inactive id;
  - `verified`;
  - `openFriday`: closed Friday and missing hours excluded;
  - `studentPrices`, with stale unverified excluded (S5);
  - price: general only, inclusive bounds, a student price not matching, stale unverified excluded, stale verified kept.
- Sorts: `updated` (newest first, ties by id); `name` in `ar` and `en`.
- Search:
  - a typo («مصاحة», "Fucus") finds the space;
  - mixed hamzas («الإبداع» ↔ «الابداع»), ة/ه, ى/ي and tashkeel find it;
  - the area's Arabic and English names match;
  - an exact match ranks above a typo.

  Break: drop the normalisation, or set the threshold to 0.6.
- The item's shape holds exactly D4's keys. Break: a price field added.
- Cache: `public, max-age=30`, ETag; the same request with `If-None-Match` answers 304.

**API: `directory/near.api.test.ts`**
- Distance order and `distanceMeters` rounded to 100, with ties by id.
- `no-store` on the answer.
- A 4-decimal header answers 422 on `near`; the header without `sort=distance` answers 422.
- **The log line of a real request with `Masaha-Near` holds neither coordinate**, read whole: the headers, the URL and the query. Made-break: the redaction path removed, and the test fails.
- A request with the point in the query (`?near=`) is not read as a location: the parameter is ignored, as unknown parameters are.

**API: `directory/pins.api.test.ts`**
- The same filters apply. 25 spaces all come back with no paging.
- `bounds` narrows to the viewport.
- 1,001 listed spaces give 1,000 pins and `truncated: true`; 1,000 give `false`. Seeded with `createMany`.
- The pin's shape. Cache header.

**API: `directory/page.api.test.ts`**
- 404 for: an unknown slug, a hidden space, a deleted space, an inactive area, an inactive governorate.
- The full shape:
  - amenities: active common ones in order, then own; a retired one absent (S8);
  - prices `null` when unverified and stale; present with `staleGroups` when verified and stale;
  - no capacity or occupancy key, even with a `space_occupancy` row seeded. Break: a field added. This covers testing §4's "no public response carries capacity".
- Cache header.

**Lanes and process**
- `migrate` is proven by the API lane, which runs on the migrated test database. The function is exercised by the search tests.
- Each new test is seen failing first. A red test is never committed.

## 10. Review Focus (inputs no planned test exercises)

- `q` mixing one searchable character with tashkeel (it passes the refinement; the SQL handles the rest).
- Very long `area` lists near 50.
- `Masaha-Near` exactly on the box's edge; the header sent twice, or with spaces around the comma.
- `bounds` that cross no listed space.
- Arabic names that differ only by ؤ/ئ (not folded).
- `lang=en` with names sorting under ICU.
- `limit=50` under `relevance` with many equal scores.
- A space whose only Friday is open around the clock (0–1,440).
- Concurrent admin edits while a list is paged: read committed, so a space can move between pages. This is accepted, as in the admin list.

## 11. Commits

1. `docs(api): name both refusals of a price amount` (D9, #69).
2. `feat(directory): page the public directory` (the migration, the shared requests and responses, lookups', space-links' and spaces' public listing, the module and `GET /spaces` without distance, the cache, the tests, and the contract, directory, spaces, lookups, space-links, data-model, conventions and plan documents).
3. `feat(directory): sort the directory by distance` (the `Masaha-Near` header, its redaction, `no-store`, the tests, security.md, overview *Near me*, foundation §13).
4. `feat(directory): the map's pins` (the endpoint, the tests, the contract §4 and §5).
5. `feat(directory): a space's public page` (the read, the endpoint, the tests, the contract, directory.md, and the overview's *Built* line).

## 12. Verification (phase 4)

**Before the runs**
- Rebuild `packages/shared`'s dist before typecheck and the lanes, since a stale dist once hid a CI failure.
- Apply the migration to `masaha_b_dev` and `masaha_b_test`.

**One at a time, on the head**
- `test:unit`.
- `test:api`, after checking that worker A is not running a lane in the main folder; if it is, wait.
- `lint`, `typecheck`, `format:check`, `check:links`.

**Not run:** `test:component`, the build and `check:build`. No shared type reaches the web, since nothing in `apps/web` imports `@masaha/shared/directory` or changes. The report says why. CI runs them.

**Real requests against 3321** (the demo seed), each in the report:
- the list's first and second page with `area` and `openFriday`;
- `q` with a typo, and with mixed hamzas, finding the space;
- `sort=distance` with `Masaha-Near: 31.523,34.452`, with the API's log lines grepped to show no coordinates;
- the pins for the same filters;
- a space's page, and a hidden space's page answering 404;
- a repeated list request with `If-None-Match` answering 304.

Then stop the server by PID and check that the port is free.

**At the report:**
- `git merge-tree --write-tree` against every open PR; `gh pr checks` green and `CLEAN` before the report.
- **The privacy line:** the report says the prototype's «يبقى موقعك على جهازك فقط، ولا يُرسَل إلى أي جهة.» (`shared.jsx` `PRIVACY_LINE`) is now untrue. The account design fixer rewords it in `shared.jsx` this round (routed by the analyst), and the web does the same when the screen is built.
- Every background shell started is stopped. `jq` is not installed: use `gh … --jq`.

**The PR:** `feat(directory): the public directory's API`; labels `feat`, `area:api`, `area:docs`; assigned to the owner; `Closes #69`. An independent review follows (privacy, a migration). Not merged.

## 13. The owner's decisions (2026-10-13 reply)

1. **S9 approved:** `docs/features/directory.md`, with its map line. `spaces.md`, `lookups.md` and `space-links.md` keep what their modules add.
2. **S2 approved:** a pin carries `areaId` and the week's `days`.
3. **D4 approved:** no freshness on the card. The sort reads the dates on the server.
4. **The location travels in the `Masaha-Near` header,** not the query (against the draft's recommendation). It is redacted in the request log, `no-store`, and finding 61 is dropped (D2).
5. **Precision: 3 decimals (about 110 m),** refused when finer. `distanceMeters` is rounded to 100 m (D2, S3).
6. **Added:** a `q` that normalises to nothing is refused (`invalid_format`), with its unit test. The PR's title is `feat(directory): the public directory's API`.

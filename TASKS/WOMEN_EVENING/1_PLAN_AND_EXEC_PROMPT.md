# WOMEN_EVENING — the evening switch and the women's hall — PLAN, then BUILD (one session, no PR)

You are a **Claude Code worker** on **Masaha** (a bilingual Arabic RTL / English platform for coworking spaces in
Gaza), a fresh session, **Opus 5.5, effort high**, in **`C:\dev\masaha\app`** (on `main` `f58c12a8`, clean). Every
point of this task is decided by the owner. You **plan briefly, save the plan, then build at once — no stop for
approval** (the owner's pattern for small, decided tasks). The owner is away: **you take every open decision
yourself, the safest one the documents allow, and record it**; he reviews them all at the end.

**The owner's hard rules for this task:**
- **Never push, never open a PR, never merge.** Your branch stays **local** until the owner says so — after the
  identity PR (`feat/ink-berry-identity`, in `C:\dev\masaha\app-design`, being finished now) has merged.
- **No conflict with the identity branch:** never edit a file that branch changes. Before every commit, read
  `git diff --name-only origin/main...feat/ink-berry-identity` (a local branch of this repository; it may still move)
  — no file you stage may be in it. Today it holds, among others, **the directory's card
  (`features/directory/components/card/SpaceCard.tsx`)** and **`docs/frontend/design-system/foundation.md`**. What
  needs them waits: build everything else, and list the waiting items precisely (§6).

## 1. Read first

`CLAUDE.md`; `docs/development/workflow.md`, `engineering-principles.md`, `testing.md`; **the decisions, binding:
`C:\dev\masaha\workspace\TASKS\WOMEN_EVENING\0_OWNER_DECISIONS.md` (E1–E9, W1–W6)**; `docs/features/directory.md`
(the filters, decision 8's 20:00 rule that E7 replaces, the card, the public page), `spaces.md` (the hours group,
«ساعات العمل», the admin's editor), `lookups.md` (the amenity catalogue; keys never change), `packages.md`;
`docs/api/api-contract.md`; `docs/architecture/data-model.md`; `docs/backend/conventions.md`;
`docs/frontend/architecture.md`; `foundation.md` (read only); the Prisma schema (`model Amenity`: `key` unique, "code
refers to amenities by key"; the icon is a key from the fixed list `packages/shared/src/lookups/amenityIcons.ts`);
the migrations; the findings index (the identity branch takes the next numbers — check it and use the numbers after
its own, said in the report). **Never revive a cancelled decision:** the general amenities filter stays dropped
(DIRECTORY_FILTERS R2); `women's hall` is one fixed filter.

## 2. What to build (from the decisions)

- **The evening (E1–E9):** one switch on the space — the owner declares the space works in the evening; its
  regular hours say until when. It belongs to the **hours group** (its date and staleness), edited in **«ساعات
  العمل»**'s Sheet as a box «المساحة تعمل مساءً» under the hours, shown in its view as a line «دوام مسائي»; the
  admin's editor the same. **The gentle hint (E9):** with the switch on and no open day closing after 18:00, the
  profile says so, never blocking (your wording, both languages, recorded). **The directory (E7):** «مفتوحة مساءً»
  passes a space **by the switch only**; the 20:00 rule goes (update `directory.md`, marking decision 8 revised).
  The public page shows «دوام مسائي» where its hours are. No evening prices, no evening section (E4, E5).
- **The women's hall (W1–W6):** a catalogue amenity **`womens_hall`** («قاعة للنساء» / "Women's hall") added by the
  migration in every environment, with a **new icon key** in the shared icon list and its glyph in the design
  system's icon set (choose a fitting Lucide glyph already installed; record why); ticked in «المرافق» like any other;
  shown with the amenities on the public page. **The filter** «قاعة للنساء» in the panel's «أخرى» group (beside
  «موثّقة» and «أسعار للطلاب»), its address parameter and API filter by the amenity's **key**, never its id. **What
  the admin may do to that amenity** (rename, reorder, retire, delete): decide the safest rule, enforce it on the
  server, record it. **Never «مختلطة»** (W6).
- **The card's two marks (E6, W4):** the directory card is the identity branch's file → **waits** (§6). Build the API
  fields the card will read now.
- Copy in **both** catalogues; the design system only (existing components and semantic roles; no colour or class
  outside it); authorization on the server.

## 3. The migration (one)

`migrate dev --create-only` **once** (a second run applies it); then read the SQL. It holds: the space's evening
column (name by the conventions, default false); **E8's one-time switch-on** — true for every space whose hours have
an open day closing at 20:00 (1200 minutes) or later; **W3's amenity row** (`womens_hall`, both names, the new icon
key, last in the order; idempotent on the unique key). No data lost; existing rows untouched otherwise. On a
data-loss refusal use `migrate diff --script`. `migrate reset` needs the owner: never.

**Databases — your own, never `masaha_dev`:** in the shared container create `masaha_we_dev` as a **copy of
`masaha_dev`** (`pg_dump` / restore inside the container — `masaha_dev` is in use by another session, so no
template copy) and an empty `masaha_we_test`; back up `apps/api/.env` to `apps/api/.env.bak-we` and point its
`DATABASE_URL` / `TEST_DATABASE_URL` at them (never print the file). **Never `db:seed` any database holding the demo
set; never touch `masaha_dev`, `masaha_test`, `masaha_design_*`.** Leave the `.env` pointing at your databases at the
end (the work continues after the identity merges) and say so in the report.

## 4. The plan (short), then the build

- Run `start-work-item` for its checks and reading, then **`write-plan`**: save the plan to
  **`C:\dev\masaha\workspace\TASKS\WOMEN_EVENING\2_PLAN.md`** — the files, the migration's SQL in full, the API
  (routes, shapes, error codes), `packages/shared`, the web, the documents, a numbered test matrix (`T…`: behaviour,
  break, lane), the commits, **"Decisions taken without the owner"** (each with its options and why), the waiting
  items (§6). **Then go straight on to the build — do not wait for approval.**
- Branch: `git switch -c feat/women-evening` from `main` (local only).
- **Tests: the owner's bar** — they must work and point the right way, never bent to pass, no gap; every new test
  **seen failing first** (make the break, see it fail, restore from a `cp` backup — never `git checkout --`); no
  production code only a test uses. At least: the migration's backfill and the amenity row; the hours group's save
  with the switch (alone, and never clearing the hours); the directory filters (`evening` by the switch only,
  `womens_hall` by the key), each combined with the others; the admin rule on the amenity; the Sheet's box, the view's
  line, the hint (both languages, axe); the panel's new filter and its address parameter.
- **Commits:** Conventional, atomic, subject ≤ 50 characters with a body, staged by path (never `git add -A` / `.`),
  no tool attribution; `#PRNUM` in documents where a PR number belongs (replaced later, before a push).
- Documents: `directory.md`, `spaces.md`, `lookups.md`, `api-contract.md`, `data-model.md`, the copy glossary if a
  term is new; an ADR only if a choice is architectural (record why or why not).

## 5. Verification (complete, before you stop)

- **Heavy runs through the shared grant script**, so you and the identity's lead never overload the machine:
  `node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs we <command…>` (it waits for ≥ 4 GB free and a free
  slot; the identity's lead goes first). Heavy = `lint`, `typecheck`, any test lane or file run, a build, `npm ci`, a
  browser batch.
- `lint` and `typecheck` on **every** commit; `format:check`; `check:classes`, `check:links`, `check:conflicts`;
  `NODE_ENV=production npm run build` + `check:build`; `test:unit`, `test:component`, `test:api` **in full**, one at
  a time. A lane killed for memory: retry once; killed again — record it (no CI will judge yet; it is run again
  before the PR).
- **A real run:** API on **3320**, web on **5320** (this folder's ports; free now) against `masaha_we_dev`; the owner's
  profile — the box, the line, the hint; the directory — both filters with others, the address round trip; the
  public page; the admin's editor and its rule on the amenity; 390 / 1440, Arabic / English, light / dark.
  Screenshots to `C:\Users\basel\Downloads\women-evening-shots\` (curated, never committed). Stop every server you
  started by its PID; check the ports free.

## 6. Then stop — the report

Write **`C:\dev\masaha\workspace\TASKS\WOMEN_EVENING\4_REPORT.md`**: the branch and its head (full sha), the
commits, what ran and what did not, the tests seen failing (the break for each), the migration and the databases,
**"Decisions taken without the owner"** (every one, its options and why), **"Waiting for the identity merge"** (the
card's two marks, any `foundation.md` line, anything else in that branch's files — each with its exact design so it
is a short step later), problems met, anything unexpected. **Then stop. No push, no PR.**

## 7. Limits

No merge; no push; no PR; no force-push; no file of the identity branch; one migration only, on your databases;
never `db:seed` the demo set; no new dependency (an icon already in the installed Lucide); no secret printed; never
weaken, skip or delete a test, a check or a lane to pass; never stop on file count — report it; public text never
names hosting providers, free plans or session durations; nothing in `C:\dev\masaha\app-design` or its lanes.

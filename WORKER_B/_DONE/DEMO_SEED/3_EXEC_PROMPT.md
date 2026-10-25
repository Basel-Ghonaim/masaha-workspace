# DEMO_SEED — the directory's demo set (development data only) — plan briefly, then execute

You are worker B's **executor** for a small item, in a fresh conversation. The owner settled its decisions
(below); you write a **short plan at the top of your report first** (the files, the data set as a table, the
tests and their breaks), then build it — no separate approval. **Stop and ask** only on a decision this
prompt does not settle.

## 1. Why, and when

Worker A's public site (`C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md`, read its §14.3 and §13's real-run
cases) needs real-run data a fresh database does not hold: today the demo seed adds **one** verified space with
no photo. **Precondition:** SUBSCRIPTIONS PR 1 (#102) is merged — `gh pr view 102 --json state` → `MERGED` (at
`43b34cd3`, 2026-10-21); if not, stop. PUBLIC PRs 1a and 1b are merged (#101, #103; 1b's real run used older
dev data, by the owner's waiver); **this set is for PUBLIC PR 2 (the map: pins by each live state) and PR 3
(the space page: photos, stale hidden prices, no hours, shifts, contacts)**. It runs now, before SUBSCRIPTIONS
PR 2. You seed `masaha_b_dev` only; the supervisor seeds worker A's `masaha_dev`.

## 2. The owner's decisions (2026-10-21)

1. **Development only, in the existing demo seed:** `SEED_DEMO=true`, refused with `NODE_ENV=production`, as
   `apps/api/src/db/seed/demo.ts` does. The directory set is **its own idempotent unit**: created once, when its
   marker (e.g. the first set space's slug) is absent — so `npm run db:seed` adds it to a database that already
   holds the demo space, and changes nothing the second time. The demo space itself is untouched.
2. **≈ 24 publicly listed spaces** across at least two governorates and four areas, with real Gaza Strip
   coordinates (inside the bounds the API accepts), covering at least: **21 or more listed** (two pages of the
   Directory); **verified and unverified** spaces (verified ones linked as OWNER to **one new demo account**,
   `demo-directory-owner@example.com`, with `SEED_DEMO_PASSWORD` — never to `demo-owner@example.com`, whose
   switcher worker A's runs read); an **unverified space whose prices' date is 60 days back** (stale, so hidden
   as the public rule says); spaces **with photos and without**; a space **with no hours**; **shift prices**;
   **student prices**; a space **open on Friday** and ones closed; **phone and WhatsApp contacts**; amenities,
   own amenities included; each live state the public page can show from data alone (a capacity with people
   present for «ممتلئ», a space outside its hours for «مغلق»), as far as the existing tables allow without new
   code paths. Names in Arabic and English, some with Arabic only.
3. **Photos through the local storage port** the app already uses (no new dependency, **no binary file
   committed**): generate small images in code (e.g. the image library the photo pipeline already uses, or an
   in-memory buffer), store them through the same port, and write the photo rows; each space's cover first.
   If the port cannot be used from the seed without new production code, **stop and ask**.
4. **No schema change, no new dependency, no change outside the seed** (and its tests, `setup.md`'s demo
   paragraph, `.env.example`'s demo comment if it names what is created).
5. **Tests:** the demo seed's API test proves the set: the count, each case of decision 2 present, created
   once (a second run changes nothing), and the demo space untouched — each with a break seen red.

## 3. The procedure

- Work in `C:\dev\masaha\app-b` only. Read `CLAUDE.md`, `docs/development/workflow.md`, `testing.md`,
  `docs/development/setup.md`, `docs/architecture/data-model.md` (the space, its facts' dates, photos), the
  directory's public rules (`docs/features/directory.md`, the contract's `GET /spaces`), the photo port, and
  the seed's code and tests on `origin/main`.
- Branch `chore/directory-demo-set` from the latest `origin/main` (`--no-track`). `docker start
  masaha-postgres-1` (never `db:up`, never `npm ci`); `masaha_b_dev` / `masaha_b_test`.
- **What runs where (the owner's rule, 2026-10-21: no run that only repeats another):** a test seen red
  before its code is its own break — a separate break only for a guard the red step did not prove (created
  once, the demo space untouched, refused in production). Per commit `lint` + `typecheck`; on the head once
  `npm run test:api -w @masaha/api -- src/db` (the seed's folder; add any other folder whose files change),
  `npm run test:unit -w @masaha/api` if a unit file changes, `format:check`, `check:links`. **Not run locally —
  CI's run on the pushed head judges:** the full `test:api`, `test:unit` of the other workspaces and
  `test:component`; report them under "Not run locally (CI judges)", not under COULD NOT RUN.
- **The real run:** `npm run db:seed` (with `SEED_DEMO=true`) on `masaha_b_dev` **twice** — the second changes
  nothing; then `GET /spaces` on 3321 shows the set (count, two pages, the cases); photos served.
- One or two commits, e.g. `chore(seed): add the directory's demo set` (recount, ≤ 50), a body saying why.
  `#PRNUM` replaced before the push; `gh pr create --assignee @me --label chore --label area:api --label
  area:docs`; CI green and `CLEAN`; the conflict check against any open PR.
- **Memory (the owner's standing rule):** one full lane at a time, none while a `vitest` of
  `C:\dev\masaha\app\` runs, the free memory recorded first; a lane killed for memory is re-run once when the
  machine is quieter; killed again → record it, carry on, and CI's run of that lane on the pushed head is the
  judge (red there → stop).
- **A test you cannot run stops the work** (any other failure: never skip, never change a config, a timeout,
  `.env` or a lane; never call it flaky); a break that stays green stops unless it is your own test's defect;
  never claim a result you did not see. Stage by path; message from a UTF-8 file without BOM, LF; no tool
  attribution; never print a password; never merge.
- The report `C:\dev\masaha\workspace\WORKER_B\DEMO_SEED\4_REPORT.md`, written as you go, with the plan at its
  top. Final reply: Status, PR, commits (subject lengths), ran and passed, COULD NOT RUN, breaks, real run,
  departures, report path.

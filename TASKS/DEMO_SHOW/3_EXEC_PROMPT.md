# DEMO_SHOW — a presentation-grade local demo, built tonight, no repository change

You are **worker B** in `C:\dev\masaha\app-b` (web **5321**, API **3321**, `masaha_b_dev`). You build, **outside the
repository**, a script set that turns a freshly seeded development database into a demo that makes Masaha look like a
platform in real use, prove it on `masaha_b_dev`, then apply it to the owner's presentation database `masaha_dev`
(`C:\dev\masaha\app`, web 5320, API 3320). The owner presents **tomorrow, 2026-11-03**, from `C:\dev\masaha\app`.
Everything must be ready tonight. Model Opus, effort high. Read `0_OWNER_DECISIONS.md` in this folder first.

## 0. Rules for this run

- **This is not a Work Item:** do not run `start-work-item`; **no branch, commit, push, PR or Issue; no file in either
  repository changes** (`git status --short` clean in `app` and `app-b` at the end, but the API's `.storage` photo
  folders, which git ignores). All your code and notes go in `C:\dev\masaha\workspace\TASKS\DEMO_SHOW\` (`scripts\`,
  `shots\`, `RUN.md`, `4_REPORT.md`).
- **No stop, no question** until it is applied to `masaha_dev`, verified and reported. Decide by the safest option,
  record each decision in the report, go on. Plan briefly in `2_PLAN.md` first (no approval wait).
- **The live site is read-only:** only public `GET`s on `https://masaha-omega.vercel.app/api/v1/…` and its
  `res.cloudinary.com` photos. Never Neon, never a write, never a secret.
- **Never print a password or a secret.** All demo accounts use the `SEED_DEMO_PASSWORD` already in each folder's
  `apps/api/.env` (read it in the script, never echo it). The admin is the owner's own (`SEED_ADMIN_*` in `.env`).
- **Data integrity:** write through the same models and rules the app enforces (the database's triggers stay on:
  the ledger, the closures; never disable one). Match the shapes the app writes: copy them from the repository's
  services and `apps/api/src/db/seed/demo.ts`, `demoDirectory.ts`. Where the app writes an audit entry for an action,
  write the same entry (conventions §6), so the owner's «سجل التدقيق» reads true. Photos go through the **local
  API's own upload** as the admin (re-encoded, keyed, in `.storage`), never a hand-copied file.
- **No «ممتلئ» anywhere:** no space's live status may read full — clear the seed's day-bound full state (and any
  override) and make no visit count reach a capacity.
- Never touch production, `app-review`, `app-design`, `masaha_test`/`masaha_b_test`. Stop every server you start by its
  process id; ports free at the end. Scripts in files (heredocs can fail); `jq` is absent (`gh --jq` / Node).

## 1. Read first (closed list)

`CLAUDE.md`; `docs/project/overview.md` (what v1 has: show only that — nothing from *Not in v1*); `docs/architecture/
data-model.md`; `docs/backend/conventions.md` §6 (audit), §13 (keys, ledger); the seed: `apps/api/src/db/seed/*.ts`;
the feature documents you write data for (`docs/features/` — desk, visits, payments, customers, subscriptions,
packages, announcements, data-reports, favorites, finance, overview, occupancy, spaces, space-links, users).

## 2. What the demo holds

**A. The 13 real spaces** (from the live site's public list and each space's page): keep their names (Arabic and
English), descriptions, area, address and location; **complete what is missing**: weekly hours (some with morning and
evening shifts, some open Friday, a couple 24h-free none), prices (hour, day, week, month; student prices where it
fits; shifts' monthly prices), amenities from the lookups (and a few of their own), English address where missing,
contacts — **phone/WhatsApp numbers visibly fictional** (`0599 000 0xx` style), no invented social handles or sites.
Realistic Gaza values (prices in shekels as the app stores them). **The owner's 13 photos, matched by the supervisor
(file in `C:\Users\basel\Downloads\spaceImg` → live slug):** إلفييت هاب.jpg → `elevate-hub` · السلام هب.jpg →
`al-salam-hub` · بال هب.jpg → `pal-hub` · برانش هب.png → `branch-hub` · جاردين هب.jpg → `garden-hub` · جريس هاب.png
→ `jreas-hub` · جولدن هب.jpg → `golden-hub` · فوكس هب.png → `focus-hub` · كوما سبيس.jpg → `coma-io` · مساحات.png →
`masahat` · مسار تيك.jpg → `masar-tech` · نمبر ون هب.jpg → `number-one-hub` · وايت سبيس.jpg → `white-space`.
**Photos:** every file in
`C:\Users\basel\Downloads\spaceImg` matched to its space by name (Arabic or English, forgiving: «هب» = «هاب», «تيك» =
«تِك», a dropped letter — record each match and each unmatched file; **re-list the folder just before applying to
`masaha_dev`**, as the owner may add more), plus the live cover of each space, downloaded from its public URL. Order:
the owner's photo first.

**A2. Generated covers (the owner's ChatGPT images)** in `C:\Users\basel\Downloads\spaceImg\` itself (beside the
Arabic-named real photos), named by
slug (`noor-hub.png` … `khan-younis-library.png`, the seed's 24 directory spaces; `pal-hub-2.png` … `pal-hub-4.png`,
the managed space's gallery after its own photo) — the prompts are in this folder's `CHATGPT_IMAGE_PROMPTS.md`. For
each of the 24 seed spaces with a generated file: **replace** the seed's plain drawn pictures with it (remove them
through the app's photo service or API, then upload the new one as the cover), so every card in the directory shows a
real-looking photo; a seed space that had no photo gets it too. A missing file: keep what the seed made and record it.
Re-list the folder before applying to `masaha_dev`.

**B. Owners and verified spaces:** about **6 of the 13** get an owner account (fictional Arabic names,
`@example.com`), linked, so they show as verified; the rest stay unverified (the directory shows both, as v1 does).

**C. The managed space** — the demo owner **«أحمد الشوا»** (`demo-owner@example.com`) and reception **«ليلى النجار»**
(`demo-reception@example.com`) run **«بال هاب» (Pal Hub, `pal-hub`)** — the owner's photos for its gallery are made
for it. The seed's «مساحة تجريبية» must not show anywhere (soft-delete it after moving the accounts' links, or the
equivalent the app supports — record). At that space, **60 days of history ending yesterday**, believable and
consistent:
- 4–5 packages (daily, weekly, monthly morning shift, monthly evening shift, student monthly), one retired;
- about **30 customers** (Arabic names, fictional `059…` numbers), some archived;
- subscriptions in every state the app shows: active, about to end, ended, ended early, renewed, with debt, in credit,
  with day/hour limits;
- daily visits (busier Sunday–Thursday, quieter Friday), check-ins of subscribers, check-outs at believable hours,
  the auto check-out at closing for a few;
- payments, cash and transfer, by **both** the owner and the reception (so «تحصيل الموظفين» has two), a couple voided
  with a reason, partial payments, uncollected visits, one written-off visit, priced-by-hand visits with a reason;
- an ended **closure** (e.g. 2 days, power outage) with its subscriptions **extended**, and a running announcement;
- data reports about the space: one pending, one resolved with a note, one dismissed with a reply;
- the space's capacity set (so occupancy statistics show), its settings sensible.
The owner's «نظرة عامة» and «المالية والتقارير» (this month and last) must look full and add up.

**D. The platform:** about **40 users** (Arabic names, `@example.com`), with favourites; data reports across spaces
(about 5 pending for the admin, others resolved/dismissed); the admin's overview, users, owners, reports and audit
pages populated. Keep the seed's 24 fictional directory spaces (no full state).

**E. Today** — a separate script for **the morning of 2026-11-03**: 5–7 people present now at the managed space
(visitors and subscribers, checked in over the last hours), a few of today's payments, nothing full, the closed-today
state left as the seed made it. It must be **safe to run more than once** (no duplicates) and fast.

## 3. Deliverables (in this folder)

- `scripts\build-demo.*` — A–D on a database that has just had `db:reset` + `db:seed` with `SEED_DEMO=true`; refuses
  to run on anything but a `*_dev` database and refuses `NODE_ENV=production`.
- `scripts\today.*` — E.
- `RUN.md` — short: (1) how the demo was applied tonight; (2) **the owner's one command for tomorrow morning** (from
  `C:\dev\masaha\app`, with the API running), and how to start the servers; (3) the accounts to sign in with — each
  role, its email, "the demo password" (never the value) — and which pages to show for each; (4) how to rebuild from
  scratch if needed.

## 4. Order of work

1. Plan (`2_PLAN.md`). Snapshot the live site's 13 spaces into `scripts\live-spaces.json` (public data only).
2. Build on **`masaha_b_dev`**: `npm run db:reset` in `app-b` (with `SEED_DEMO=true` for the seed), the API on 3321
   for the photo uploads, `build-demo`, `today`. Then the **real run** with local headless Chrome over CDP (models:
   `C:\dev\masaha\workspace\WORKER_A\_DONE\PAYMENTS_STEP10\scripts\cdp2.mjs`, `run2.mjs`; never keep an `/auth/` body):
   Arabic light at 1440 and 390 — Home, the directory (list and map), three space pages (photos shown), sign in as
   the admin (overview, spaces, owners, users, reports, audit), the owner (overview, desk, customers and a file,
   payments, finance this month, announcements, staff, audit), the reception (desk with people present, my payments
   today), a user (favourites, my reports). Fix whatever looks thin, wrong or broken; **no «ممتلئ» visible anywhere**.
   Shots in `shots\b\`.
3. Apply to **`masaha_dev`**: first a backup — `docker exec masaha-postgres-1 pg_dump -U masaha -Fc masaha_dev >
   scripts\masaha_dev_before.dump` (name it in the report); then in `C:\dev\masaha\app`: `npm run db:reset` with
   `SEED_DEMO=true` (the admin comes back from `SEED_ADMIN_*`), the API on 3320, `build-demo`, `today` (so tonight's
   check shows people present; tomorrow's run renews it). Re-list `spaceImg` first. Repeat the real run's key pages on
   5320 (shots in `shots\dev\`). Stop the servers; ports 3320/3321/5320/5321 free; both folders' `git status` clean.
4. `4_REPORT.md`: what was built, the counts (spaces, users, customers, visits, payments, reports), the photo matches
   (and unmatched files), the managed space chosen, every decision, the backup's path, anything not done.

## 5. The final reply

```
Status: READY | INCOMPLETE (what, why)
masaha_dev: backed up to <path> · reset · demo applied · today applied
Spaces: 13 real (<n> verified, <n> photos) + 24 seed · managed: <name>
Counts: users <n> · customers <n> · visits <n> · payments <n> · reports <n>
Photos unmatched: <files>   (or "none")
Full state anywhere: none
Real run: <pages checked> · shots <folder>
Tomorrow: <the one command from RUN.md>
Repositories: app clean · app-b clean
Decisions: <count>, in the report
```

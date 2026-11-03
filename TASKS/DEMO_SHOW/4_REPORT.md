# DEMO_SHOW — report (2026-11-02, evening)

**Status: READY.** `masaha_dev` is backed up, reset, built and checked. `today.ts` was applied tonight;
tomorrow's command is in `RUN.md` §2. Nothing in either repository changed.

## What was built (all in `scripts\`)

| File | What it does |
|---|---|
| `snapshot-live.mjs` → `live-spaces.json`, `live-covers\` | The live site's 13 spaces and their covers. Public GETs only. |
| `spaces-config.ts` | What each real space lacked, completed. Also the photo table and the 41 users. |
| `lib.ts` | Guards, the app's own modules (Prisma client, `hashPassword`, `chargeOf`, `gazaClock`, `normaliseContact`), the audit writer, and the day generator. |
| `build-demo.ts` | Parts A–D: `--phase=data` (Prisma, backdated) and `--phase=photos` (through the local API). Ends with checks: nothing full, plus counts. |
| `today.ts` | Part E. Keys are derived from the date, so it is idempotent. |
| `realrun.mjs` | The real run: headless Chrome over CDP, Arabic, light, 1440 and 390. |
| `build-summary-<db>.json`, `photos-done-<db>.json` | Each run's decisions, counts and photo outcomes. |
| `masaha_dev_before.dump` | **The backup** of `masaha_dev` before the reset (pg_dump `-Fc`, 218 KB, 33 tables). |

**How it writes.** History goes straight through Prisma with explicit timestamps. The services stamp
`now`, and the audit table's `createdAt` is the database default, so writing through the running API would
date 60 days of history tonight. Every row copies its service's shape. Every audited action gets the same
entry its service writes (action, entity, before/after built the same way), dated when the action happened.
The database triggers stayed on and checked every payment and void. Photos went only through
`POST/DELETE …/photos` on the local API, by the actor the app allows: the admin on an unverified space,
the owner on a verified one, since the API refuses the admin there.

## Counts (masaha_dev, after `today`)

- **Spaces:** 37 listed. That is the 13 real spaces plus the seed's 24; «مساحة تجريبية» is soft-deleted.
  19 are verified: 6 of the 13 real spaces and 13 of the seed's.
- **Users:** 50 in all: 41 users (the demo user included), 6 owners of real spaces (أحمد among them), the
  reception account, the directory owner, and the admin.
- **Pal Hub:**
  - 30 customers, 3 of them archived; 33 subscriptions.
  - 538 visits and 316+ check-ins; 565 payments, 2 of them voided with a reason.
  - 6 packages, one retired.
  - A closed-and-extended closure (Oct 8–9, 8 subscriptions extended by 2 days), a running offer, an
    upcoming event, and an ended notice.
- **Data reports:** 18 in all. 9 are open: 7 for the admin, 1 for Pal Hub's owner, 1 for Branch Hub's owner.
  5 are resolved and 4 dismissed.
- **Other:** 113 favourites; 2,513 audit entries; 40 photos.

**Pal Hub's states, all present:**

- **Subscriptions:**
  - running, ending soon (by date, and a 30-hour pack nearly used), ended, ended early (خالد منصور);
  - renewed (محمد عوض, سارة خالد, هبة الشريف, ريم السويركي), not started yet;
  - with a debt (بلال, سارة, سامر, نور) and in credit (لينا, per hour, 120 ₪ ahead);
  - with limits: days per week, total days, total hours, hours per day.
- **Visits:**
  - hand-typed charges on the two days before the prices were published, and one priced the next morning
    (`visit.priced`);
  - auto check-outs at closing, most paid the next day and 5 left uncollected;
  - debts left to a phone's customer, a partial payment, and a write-off (كريم الزعانين).
- **Payments:** both staff collect (ليلى and أحمد in «التحصيل حسب الموظف»).
- **Data reports about Pal Hub:** one pending, one resolved with a note, one dismissed with a reply.

## Photos

Re-listed before applying: **40 files**, all matched, **none unmatched**.

- **The 13 owner photos:** matched by the supervisor's table; each is its space's cover.
- **The 27 generated files:**
  - 24 seed covers, matched by slug. Each replaced the seed's drawn pictures: removed and uploaded through
    the API, by the admin on unverified spaces and by the directory owner on verified ones.
  - Pal Hub's gallery: `pal-hub-2..4`, after its own photo (4 photos).
- **The live covers:** all 13 are the same picture as the owner's file (thumbnail difference ≤ 5/255, same
  sizes), so none was added twice.

## Decisions (made on the safest option; 16)

1. **Database writes.** Direct Prisma writes with backdated, service-shaped audit entries, rather than the
   running API (reasoning above). Photos go through the API, as required.
2. **The seed's 24 spaces are dated 20 days back as a whole** (their staleness is unchanged), so the 13
   real spaces, entered over the last 17 days, list first. Reports and favourites are always dated after
   their space existed.
3. **Pal Hub is backdated** (created 66 days ago) because it carries 60 days of history. Its owner
   confirmed every fact group yesterday evening, so it lists first and its prices stay fresh.
4. **Pal Hub's prices were published 58 days ago.** That is why the first two days' charges were typed by
   the owner, with a reason: the only way the app has hand-priced visits when rates exist.
5. **«مساحة تجريبية» is soft-deleted** by the admin, seconds after the seed made it. Its links are kept
   and count for nothing (the app's rule).
   - It remains in the admin's deleted filter and in one audit entry, which is 56th among the platform's
     events (page 3).
6. **The seed's full space** (`sada-space`, 4 present of 4) got capacity 12 through its owner's audited
   capacity edit. There were no overrides to clear.
7. **Owner accounts of the real verified spaces:** created by the admin with a temporary password
   (`user.created`, as the app does), since changed. Each owner set a capacity, so the live status shows
   «متاح».
8. **The 6 verified real spaces:**
   - Pal Hub (أحمد الشوا);
   - Elevate Hub (verified on the live site);
   - Branch, Number One, Focus and Garden (the ones with the most data).
9. **Live contacts are kept as entered** (they are the spaces' own public numbers). A fictional `0599 000 0xx`
   number is added only where a space had no phone and no WhatsApp. No handle or site is invented.
10. **Jreas Hub publishes no prices:** its own description says it is free. The admin's overview lists it
    as «الأسعار · لم تُضف بعد».
11. **Live names are kept exactly,** typos included («إاليفييت هاب», «coma,io»), as the prompt says.
12. **Area as on the live site,** for example Golden Hub's «North Gaza Strip», although its address is in
    Al-Saraya.
13. **Seed accounts' creation dates moved to fit the story.** أحمد and ليلى were made by the seed tonight;
    their `createdAt` was moved to 67 and 64 days ago, with ليلى's account creation by أحمد audited. The
    directory owner's date was moved with his spaces.
14. **The prompt's "a couple 24h-free none"** is read as "a couple open around the clock (Masar Tech,
    Masahat), none without hours".
15. **The dry run.** Prisma refuses `migrate reset` from an AI agent. I asked you, and you answered
    "Yes, reset both", so `masaha_b_dev` and `masaha_dev` were reset with that consent. `masaha_b_dev` was
    reset several times during the dry run.
16. **`today.ts` has a test-only `DEMO_NOW` override.** I used it to rehearse tomorrow (Nov 3, 10:40) on
    `masaha_b_dev`.
    - It closed last night's 5 stays at 22:00, filled Nov 2 as a whole day, and put 5 present.
    - A second run added nothing.
    - So `masaha_b_dev` now holds Nov 3 records; it is the dry-run database only.

## The real run

- **`shots\b\` (masaha_b_dev, 56 shots) and `shots\dev\` (masaha_dev, 56 shots),** at 1440 and 390. They
  cover:
  - the public pages: Home, the directory (list and map), and the pages of Pal Hub, Branch, Noor and
    Masahat, with photos;
  - the admin: overview, spaces, owners, users, reports, audit;
  - the owner: overview, desk, customers, Sara's file, payments, finance, packages, announcements,
    reports, staff, audit;
  - reception: the desk with 5 present, and my payments;
  - the user: favourites and my reports.
- **No JavaScript errors, and no error text.** No space reads full.
- **The only «ممتلئ» on any page is the map legend's key,** which is the app's code, not data. I can't
  remove it without a code change, so it is noted in RUN.md.
- **Fixed after the first run:**
  - too many auto check-outs (74, now 19);
  - the deleted demo space at the top of the admin's audit;
  - لينا's per-hour plan showing a small debt instead of credit.

## Not done, or worth knowing

- **"This month" is November, 2–3 days old.** Finance shows it at −94% against October. October (and
  September) are full. Tomorrow's run adds Nov 2 as a whole day and the morning of Nov 3.
- **The map's tiles didn't draw in headless Chrome** on the directory map (the space page's map did). Check
  it once in your browser.
- **Servers and processes:**
  - A vite on 5321 had been started from a separate PowerShell window (not by me). It was serving stale
    dependencies, after my own duplicate start rewrote the shared `.vite` cache, and had already exited
    when I went to stop it. I then ran my own.
  - All servers I started are stopped. Ports 3320, 3321, 5320 and 5321 are free.
  - Docker Desktop and the `masaha-postgres-1` container were not running when I started. I started them
    and left them running for tomorrow.
- **Files outside the repositories:** `scripts\package.json` (`"type": "module"`) exists only so the
  scripts run as ES modules. `apps/api/.storage` holds the new photos (git-ignored).
- **Repositories:** `git status --short` is empty in both `app` and `app-b`.

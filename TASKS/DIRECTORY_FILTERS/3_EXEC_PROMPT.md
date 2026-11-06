# DIRECTORY_FILTERS — execution prompt (OpenCode worker, prototype only)

You are a worker on **Masaha**, a bilingual (Arabic RTL / English) directory of coworking spaces in Gaza. This task
redesigns the filters and the sort of the directory page **in the design prototype only**. Everything you need is in
this prompt. Read it whole before you start.

## 0. Where and how

- Repository: `C:\dev\masaha\app`. Read `CLAUDE.md` and `docs/design/README.md` first (the prototype's rules and its
  two checks).
- `git switch main && git pull --ff-only`, then `git switch -c refactor/directory-filters`.
- **Allowed files: `docs/design/` only** — `docs/design/prototype/**` (mainly `Directory.html`, `masaha/data.js`,
  `masaha/i18n.js` and `masaha/shared.jsx` if a shared piece is needed), `docs/design/INDEX.md`,
  `docs/design/CHANGES.md`, `docs/design/prototype/Flows - states.html`. **Never touch** `apps/`, `packages/`, or any
  other file under `docs/`.
- **Hard limits:** no PR, **no push** (the branch stays local), no merge, nothing on `main`, no test lane, no build,
  no lint, no `npm ci`. No tool attribution anywhere (no `Co-Authored-By`, no "generated with").
- Commits: Conventional Commits, subject ≤ 50 characters, a body saying what and why, staged by explicit path (never
  `git add -A` / `git add .`). Suggested series (adjust if needed, each one passing both checks):
  1. `feat(design): sort the directory by a subscription's price` — §2 items 1–4
  2. `feat(design): choose the directory's place by governorate` — §2 item 5
  3. `feat(design): add open-now, evening and amenity filters` — §2 items 6–7
  4. `docs(design): record the directory filters' round` — `INDEX.md`, `CHANGES.md`, the board
- The checks, from the repository root, before every commit:
  `node docs/design/scripts/check-parse.mjs` and `node docs/design/scripts/check-classes.mjs`.

## 1. The prototype's traps (from `docs/design/README.md`)

- Every module and inline script of a page shares **one global scope**: no new top-level name that already exists in
  another script of the page, and none the browser owns (such as `name`).
- **No object rest** (`const { a, ...rest } = props`) anywhere — pick props by hand.
- The CSS is a **prebuilt bundle**: a class no stylesheet defines is silently dead and `check-classes` fails on it.
  Use only classes already used elsewhere in the prototype, or the design system's components (`ToggleGroup`,
  `Field`, `Switch`, `Select`, `Sheet`, `Badge`, `Button`…). No raw colours, no inline styles for colour.
- Every user-facing text in **both languages** with `tr("…", "…")`, Arabic first, as the file already does. Arabic
  wording: plain and short, matching the existing lines.
- The checks cannot see runtime problems (a block drawn twice, a wrong gap). **Open the page in a browser** at 390,
  768 and 1440, in Arabic and English, light and dark, and look before you stop. Serve with
  `cd docs/design/prototype && npx serve .`.

## 2. What to build (the owner's decisions)

Today `Directory.html` has: a sort `Select` (`SORTS()`: latest update, name; distance comes from the separate
«الأقرب إليّ» button), and a filter panel (sidebar from 1024 px, `FilterSheet` below) with `PlaceField` (a combobox of
areas grouped by governorate), two switches (available now, verified only), `PriceField` (period `ToggleGroup` + «من/إلى»
inputs, `priceRange`) and «أخرى» (student prices, Friday). The URL holds the state (`?area=`, `?available=`,
`?verified=`, `?period=`, `?priceMin=`, `?priceMax=`, `?other=`, `?view=`).

1. **Remove the price range and the period from the filter panel.** Delete `PriceField`, `priceRange` and their URL
   params (`period`, `priceMin`, `priceMax`; an old link still opens, unfiltered by them). The active-filter count no
   longer counts a price.
2. **Add «السعر» to the sort, with its subscription and direction as one choice.**
   - The sort list: «الأحدث تحديثًا» · «الاسم» · «السعر». «الأقرب إليّ» stays its own control, unchanged.
   - When «السعر» is chosen, show directly beside/under the sort control two single-choice chip rows
     (`ToggleGroup type="single"`):
     - the subscription: **شهري** (default) · أسبوعي · يومي · ساعة — from `M.periods` (use their `filter` labels:
       شهري، أسبوعي، يومي، بالساعة), ordered month, week, day, hour;
     - the direction: **الأقل سعرًا** (default) · الأعلى سعرًا.
   - On a phone (below 768) the sort lives where it does today; the two chip rows appear inside the same control's
     surface (the sort's sheet or directly under the select, whichever the current phone layout allows cleanly — no
     second copy of the controls). On the map view there is no sort today on a phone; leave the map's behaviour as is.
   - URL: `?sort=price&sub=month&dir=asc` (defaults may be omitted from the URL, as the page does for other defaults).
   - Ties keep the existing tie order (then by id).
3. **While the price sort is on, a space without a price for the chosen subscription leaves the list**, and so does a
   space whose prices are hidden (`M.priceHidden(s)` — unverified and stale). The count line says it, for example
   «8 مساحات لها سعر شهري» / "8 spaces with a monthly price" (keep the file's existing Arabic number agreement, as
   `countLabel` does). The map is unchanged.
4. **The card shows the chosen subscription's price, only while the price sort is on**: one line on the card such as
   «250 ₪ / شهر» / "₪250 / month" (the number and currency isolated LTR, as other always-LTR values in the prototype
   are). With any other sort the card is exactly as today. Home and Favorites cards are untouched.
5. **The place filter on two levels (replace the combobox):**
   - Desktop sidebar (from 1024): under «المنطقة», the active governorates as chips (`M.governorates`, skipping a
     `hidden` one or one with no areas). Tapping a governorate opens its areas below it as chips, the first one
     «كل {المحافظة}» / "All of {governorate}", which selects all its areas; areas are multi-select, across
     governorates. One governorate's areas are open at a time; a governorate with a chosen area shows a small count.
   - Phone/tablet (the `FilterSheet`): «المنطقة» is a row showing the current choice; tapping it shows the
     governorates as a list inside the sheet; a governorate shows its areas (with «كل …» first) and a «رجوع» back to
     the governorates. Keep it inside the one sheet (a view swap inside the sheet, not a second sheet).
   - The chosen areas show as removable chips (×) under «المنطقة», at every width.
   - The URL stays `?area=id,id` (an "all of a governorate" choice writes its areas). `placeLine` and
     `placeSummary` keep working.
6. **New filters**, in the panel, each counted once in the active-filter count:
   - «مفتوحة الآن» / "Open now" — a `Switch`: the space's hours (`s.hours`, the `week` helper's shape; `fri` may be
     `null`) say it is open at the current time on today's day. It applies to **every** space, verified or not. Put it
     with the existing switches, above «متاحة الآن فقط». Rewrite the caption under the switches so the two are told
     apart in one short line, for example «"مفتوحة الآن" حسب ساعات الدوام، و"متاحة الآن" حسب الحالة المباشرة للمساحات
     الموثّقة.» with its English.
   - «مفتوحة مساءً» / "Open in the evening" — a chip in «أخرى» beside student prices and Friday: today's closing time
     is 20:00 or later. URL: add `evening` to `?other=`.
   - «الخدمات» / "Amenities" — a new group: the amenities (`M.amenities`, catalogue order) as multi-select chips; a
     space passes when it offers **all** chosen ones. If more than six exist, show six and a «عرض الكل» toggle. URL:
     `?am=id,id`.
   - Make the sample data exercise them: adjust a few spaces' `hours`/`amenities`/`prices` in `masaha/data.js` so each
     new filter and the price sort visibly change the list (some spaces lacking a weekly price, one closing at 22:00,
     varied amenities). Keep every existing `?demo=` and state parameter working.
7. **Unchanged:** «أخرى»'s student prices and Friday, «المساحات الموثّقة فقط», «متاحة الآن فقط», the search, the
   map/list toggle, «الأقرب إليّ», «مسح» clearing every filter (now including the new ones; it does not reset the
   sort), and the sheet's footer «عرض N نتيجة».

## 3. The records

- `docs/design/INDEX.md`: replace the `?period=…&priceMin=…` row and update the `?area=` row; add rows for
  `?sort=price&sub=…&dir=…`, `?am=`, and the new `?other=evening`.
- `docs/design/CHANGES.md`: a new batch section «Refactor 1 — the directory's filters (2026-11-05)» with one line per
  decision (what changed, where), naming the earlier decisions it revises: the card's no-price rule (D4), U1's
  combobox and "no governorate filter", U5's price range, and "the amenities are no filter" (2026-10-12).
- `Flows - states.html`: add frames for the price sort (desktop 1440 and phone 390) and the place filter open on a
  governorate (desktop and phone). Follow the file's existing frame pattern and spacing.

## 4. Plan, run, stop once

1. Write a short plan (≤ 40 lines) to `C:\dev\masaha\workspace\TASKS\DIRECTORY_FILTERS\2_PLAN.md`: the files, the
   commits, anything in §2 you could not build as written and what you will do instead. Do not wait for approval.
2. Build and commit the series, both checks passing before each commit. Look at the pages in a browser.
3. Take screenshots into `C:\Users\basel\Downloads\directory-filters-shots\` (never into the repository): the list
   with the price sort (desktop 1440, phone 390, Arabic; one English; one dark), the place filter open on a
   governorate (desktop, and the phone sheet's two screens), the new filters on, and one card with its price.
4. **Stop once.** Print for the owner: the branch and `git log --oneline main..HEAD`, the serve command, and a list of
   ready-to-open URLs with their states (each decision in §2, desktop and phone, `?lang=en`, `?theme=dark`). Then wait.
5. The owner's notes come in this same session. For each round: `git branch backup/directory-filters-<n>` first,
   fix, `git commit --fixup=<the commit it belongs to>`, then
   `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash main` (non-interactive). No standalone fix commits. Both checks
   again, look again, new screenshots for what changed, print the URLs again, wait.
6. When the owner says the round is done: write `C:\dev\masaha\workspace\TASKS\DIRECTORY_FILTERS\4_REPORT.md` — the
   head sha, the commits (`git log --format='%h %s' main..HEAD`), the files changed (`git diff --stat main`), the
   checks' output, what differs from §2 and why, and any finding you noticed outside scope (recorded, not fixed).
   Delete the `backup/directory-filters-*` branches only when the owner says so.

# DIRECTORY_FILTERS — the final round (plan, build, stop before committing)

You are a worker on **Masaha**, a bilingual (Arabic RTL / English) directory of coworking spaces in Gaza. This round
finishes the directory page's filters **in the design prototype only**. Everything you need is in this prompt; read
it whole before you touch anything.

## 0. Where you are — a branch under development, with commits and uncommitted work

- Repository `C:\dev\masaha\app`, branch **`refactor/directory-filters`** (local, never pushed). Do **not** switch
  branch, do **not** pull, do **not** rebase, do **not** reset, do **not** stash. Check first:
  `git branch --show-current` (must be `refactor/directory-filters`) and `git status -s`.
- The branch already has **5 commits** on top of `main`:
  `b414db72 feat(design): rework the directory's filters and sort`, `9abca5c4 docs(design): record the directory
  filters' round`, `d83a16bd feat(design): add price range controls`, `7f6156c3 fix(design): require price sort
  direction`, `b4a4a5a8 fix(design): toggle off price sorting`.
- **The working tree holds approved, uncommitted work** — the base you build on, never to be discarded:
  `docs/design/prototype/Directory.html` (the new price filter) and `docs/design/prototype/masaha/masaha.css` (the
  `.dir-filters` / `.dir-results` columns between 1024 and 1279). Read both diffs (`git diff`) before planning.
- First, a safety copy: `git branch backup/directory-filters-3` and copy the two modified files to
  `C:\dev\masaha\workspace\TASKS\DIRECTORY_FILTERS\backup-3\` (create it).
- Read `CLAUDE.md` and `docs/design/README.md` (the prototype's rules and its two checks).

## 1. Hard limits

- **Prototype only.** Allowed files: `docs/design/prototype/Directory.html`, `docs/design/prototype/masaha/data.js`,
  `docs/design/prototype/masaha/shared.jsx`, `docs/design/prototype/masaha/masaha.css`,
  `docs/design/prototype/Flows - states.html`, `docs/design/INDEX.md`, `docs/design/CHANGES.md`. **Never touch
  `apps/`, `packages/`, or any other file under `docs/`** — no production file under any circumstances.
- **No commit, no amend, no push, no PR, no merge** in this round — you stop at "ready for review" with everything
  uncommitted (§5). Committing comes later, only when the owner says so (§6).
- No test lane, no build, no lint, no `npm ci`. The only checks are the prototype's two, from the repository root:
  `node docs/design/scripts/check-parse.mjs` and `node docs/design/scripts/check-classes.mjs`.
- The prototype's traps: every script of a page shares **one global scope** (no new top-level name that another
  script of the page has, none the browser owns such as `name`); **no object rest** (`const { a, ...rest } = x`);
  the CSS is a **prebuilt bundle**, so use only classes already used in the prototype (`check-classes` fails on a new
  one) — a layout rule that needs a new class goes in `masaha/masaha.css` with a comment, as `.dir-filters` does.
  No raw colours. Every text in both languages with `tr("…", "…")`.
- No tool attribution anywhere.

## 2. What is already built (keep it exactly)

The price block, approved by the owner on 2026-11-07: a segmented radiogroup «الكل · ساعة · يوم · أسبوع · شهر»
(`SubscriptionChoice`, «الكل» default, arrow keys); once a subscription is chosen, «من / إلى» fields in shekels with
placeholders from the data, validation (whole numbers above zero, Arabic-Indic digits converted, «إلى» under «من»
flagged on «إلى»); only the spaces with that price are listed and their cards show it; the sort Select holds the
price order (disabled under «الكل»); «مسح» resets the subscription and the range; the URL keeps `sub`, `priceMin`,
`priceMax`, `sort=price`, `dir=desc`.

## 3. What to build

1. **The panel's order and groups**, top to bottom:
   - «المنطقة» — unchanged (the multi-select `Combobox`).
   - «السعر» — unchanged (§2).
   - **«الدوام»** / "Hours" — a new group of three `Checkbox` rows (each a `Field`, as «أخرى» does now): «مفتوحة
     الآن» / "Open now", «مفتوحة مساءً» / "Open in the evening", «مفتوحة يوم الجمعة» / "Open on Friday".
   - **«أخرى»** / "Other" — `Checkbox` rows: «المساحات الموثّقة فقط» / "Verified spaces only" (was a `Switch` under an
     «المساحات» heading — remove that heading and the switch), «أسعار للطلاب» / "Student prices".
   URL: `?open=1`, `?other=evening,friday,students,verified` (old `?verified=1` still read on load, then written the
   new way). The active count counts each box once. «مسح» clears them all.
2. **«مفتوحة الآن»** — a space passes when, on **Gaza's clock now** (`Asia/Gaza`, not the browser's zone), today's
   hours contain the current minute and no closure is in force. Applies to verified **and unverified** spaces. If the
   prototype's data has closure announcements, honour them; if it has none, use the hours only and say so in the
   report. A verified space whose live status is FULL **stays** in the results (its card's «ممتلئ» badge is enough).
   A space **without hours** never passes.
3. **«مفتوحة مساءً»** — a space passes when it closes at **20:00 or later on at least one of its open days** (its
   weekly schedule, not today), **or** when its sample data carries `eveningShift: true` (the owner's future
   direction: an owner-declared evening-hours feature; the prototype only simulates it in `data.js`, nothing edits
   it). A space without hours and without the flag never passes. Replace today's `openEvening` (it reads today only).
4. **Spaces without hours.** In `masaha/data.js`, give **one unverified** sample space no hours (`hours: null`) —
   **only after** checking every reader of `s.hours` in the prototype (`grep -n "\.hours" docs/design/prototype -r`):
   Home, the directory card's today line, Space details, Favorites, the map. Each must cope: a card shows no hours
   line (or «ساعات العمل غير متوفرة» / "Hours not available"), the space's page shows that text in its hours
   section. If a reader would break and fixing it means touching a file outside §1's list, do **not** add the
   null — say so in the report. Also give one sample space `eveningShift: true` with a closing time before 20:00, so
   the flag is visible in the filter.
5. **The sort's price labels**: «الأرخص شهريًا» / «الأغلى شهريًا», «الأرخص أسبوعيًا» / «الأغلى أسبوعيًا», «الأرخص
   يوميًا» / «الأغلى يوميًا», «الأرخص بالساعة» / «الأغلى بالساعة»; English "Monthly price: low to high" / "…: high to
   low" (Weekly, Daily, Hourly). Under «الكل» the two items read «الأرخص» / «الأغلى» ("Price: low to high" / "…high to
   low") and stay disabled. The trigger keeps its «الترتيب: » prefix.
6. **The range caption** under «من / إلى»: «بالشيكل، على السعر الشهري.» (the chosen subscription's name; English
   "In shekels, on the monthly price.").
7. **The sheet's button** (`resultsLabel` in `masaha/shared.jsx`, shared by every page's filter sheet): correct
   Arabic plurals — 0 «لا توجد نتائج», 1 «عرض نتيجة واحدة», 2 «عرض نتيجتين», 3–10 «عرض N نتائج», 11+ «عرض N نتيجة»;
   English unchanged. Check two other pages that use `FilterSheet` still render.
8. **Remove dead code** left from earlier builds (unused imports such as `SelectGroup`/`SelectLabel` if nothing uses
   them, stale comments describing the grouped price Select or the direction chips).

## 4. The records

- `docs/design/INDEX.md`: one row per URL state, matching the final set (`sub`, `priceMin`/`priceMax`,
  `sort=price`+`dir`, `area`, `open`, `other=evening,friday,students,verified`); remove the duplicated rows and the
  rows for states that no longer exist; fix «الأسبوقي». Frames for: the price filter (desktop, phone sheet), the price
  sort, «الدوام» with «مفتوحة الآن» on, a space without hours.
- `docs/design/CHANGES.md`: rewrite the «Refactor 1» section to what is built now — the price (segmented
  subscription, range, the direction in the sort), «الدوام», «أخرى», «مفتوحة الآن» for every space by its hours,
  «ممتلئ» a badge not a filter, hours optional, «مفتوحة مساءً» by the schedule (+ the future owner-declared feature),
  the plurals, the 1024–1279 column — naming what each revises (D4, U1, U5, the 2026-10-12 «المتاحة الآن» filter, ADR
  0008's filter by `AVAILABLE`, recorded for the production step).
- `Flows - states.html`: frames pointing at the final states only.

## 5. Plan, build, stop at "ready for review"

1. Write a short plan (≤ 40 lines) to `C:\dev\masaha\workspace\TASKS\DIRECTORY_FILTERS\2_PLAN_FINAL.md`: the files,
   the order of work, anything in §3 you cannot build as written and what you will do instead. **Do not wait** — start
   building right after writing it.
2. Build. Serve the prototype: `python -m http.server 5325 --directory docs/design/prototype` (if 5325 is taken, it is
   already serving this folder — use it).
3. Look at every state in a browser at **390, 768, 1024 and 1440**, **Arabic and English**, **light and dark**: nothing
   clipped or wrapping badly, no leftover switch/heading/chip, no console error, the URL round-trips on reload. Both
   checks pass.
4. Screenshots to `C:\Users\basel\Downloads\directory-filters-shots\final\` (never into the repository).
5. **Stop — ready for review, nothing committed.** Print: `git status -s`, `git diff --stat`, the checks' output, the
   serve command, and ready URLs for each item of §3 (desktop and phone, `?lang=en`, `?theme=dark`). Then wait. The
   owner and the main supervisor review; their notes come in this same session and you apply them, still without
   committing, and stop again.

## 6. Only when the owner says "commit"

1. `git branch backup/directory-filters-4`.
2. `git reset --soft main`, then `git restore --staged .` so nothing is staged.
3. Two commits, each staged **by explicit path** (never `git add -A` / `git add .`), subjects ≤ 50 characters, a body
   saying what and why, no tool attribution:
   - `feat(design): rework the directory's filters` — `Directory.html`, `masaha/data.js`, `masaha/shared.jsx`,
     `masaha/masaha.css`, `Flows - states.html`.
   - `docs(design): record the directory filters' round` — `docs/design/INDEX.md`, `docs/design/CHANGES.md`.
4. Both checks again; `git log --oneline main..HEAD` (exactly two lines); `git status -s` (clean). Then write
   `C:\dev\masaha\workspace\TASKS\DIRECTORY_FILTERS\4_REPORT.md`: the two shas, `git diff --stat main`, the checks'
   output, what differs from §3 and why, and anything noticed outside scope (recorded, not fixed). No push.

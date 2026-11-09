# Handover Prompt — Directory Filters (design prototype)

Use this prompt to bring a fresh conversation up to speed. It is pure context: it does not assign any
task. The owner will continue the work with simple, specific tasks in each new prompt.

---

You are continuing the **Directory Filters** design-prototype task on branch
`refactor/directory-filters`, in the Masaha repo at `C:\dev\masaha\app`.

## Workflow and work constraints (imposed on you)

- Task origin: `C:\dev\masaha\workspace\TASKS\DIRECTORY_FILTERS\3_EXEC_PROMPT.md` (read whole before starting).
- You are redesigning the **directory page's filters and sort**, design prototype only, on branch
  `refactor/directory-filters`.
- Allowed files only: `docs/design/` — mainly `prototype/**` (`Directory.html`, `masaha/data.js`,
  `masaha/i18n.js`, `masaha/shared.jsx` if needed), `docs/design/INDEX.md`, `docs/design/CHANGES.md`,
  `docs/design/prototype/Flows - states.html`. Never touch `apps/`, `packages/`, or any other file under `docs/`.
- Hard limits: no PR, no push, no merge, nothing on `main`, no test lane, no build, no lint, no `npm ci`.
- Prototype checks (must pass before handing off):
  - `node docs/design/scripts/check-parse.mjs`
  - `node docs/design/scripts/check-classes.mjs`
- Screenshots go to `C:\Users\basel\Downloads\directory-filters-shots/` — never into the repo.
- Stop-once loop: after finishing a round, print branch, `git log --oneline main..HEAD`, serve command,
  and ready-to-open URLs.

## Current point reached in the work

- Branch `refactor/directory-filters`, two commits on top of `main`:
  - `b414db72` feat(design): rework the directory's filters and sort
  - `9abca5c4` docs(design): record the directory filters' round
- Final design state as of 2026-11-06:
  - **Area**: restored to the pre-work form — `Combobox type="multiple"` in `PlaceField`, governorates
    grouped, searchable in both languages, nothing chosen by default, trigger reads «كل المناطق» / area /
    «منطقتان محددتان» / «N مناطق محددة»; URL `?area=id,id`; `?gov=` gone; no chips.
  - **Price**: panel field is a grouped `Select` (4 headings = the period: «الشهري»/«الأسبوقي»/«اليومي»/«بالساعة»,
    English Monthly/Weekly/Daily/Hourly) with, under each heading, the **lowest** and the **highest** price
    option (8 options total). Choosing it sets the price sort (`price:<sub>:<low|high>`) via
    `onPickPrice` → `setPs` + `setSort('price')`; the toolbar keeps the same grouped price sort; results
    filter by price (spaces without that subscription's price / with hidden prices leave the list) and cards
    show the price.
  - **Other filters**: «المساحات» group keeps only the «المساحات الموثّق فقط» Switch; «أخرى» = three
    Checkboxes (students / friday / evening); no amenities filter; live-status / open-now out of filters.
  - The typed «من» / «إلى» bounds machinery (period / priceMin / priceMax, From/To fields, range validation)
    was removed as dead code.
- Working tree clean; both prototype checks pass; server live on port 5325 serving
  `C:\dev\masaha\app\docs\design/prototype` (started with
  `python -m http.server 5325 --directory C:\dev\masaha\app\docs\design/prototype`).

## Hard constraints for you going forward

- **Never touch the production environment under any circumstances.** The only workspace you may work in is
  the **Prototype** environment (`docs/design/prototype`), served locally.
- You may only change files under `docs/design/`.
- No PR, no push, no merge, nothing on `main`, no test lane, no build, no lint, no `npm ci`.
- Screenshots → `C:\Users\basel\Downloads\directory-filters-shots/` (never in the repo).

## How the owner works with you

- The owner (the user you are assisting) will continue the work by giving you **simple, specific tasks**,
  one per prompt, on this same branch.
- Follow the stop-once loop after each round: branch, `git log --oneline main..HEAD`, serve command, ready
  URLs.
- The handover prompt itself contains no task — do not treat it as an instruction to do work.

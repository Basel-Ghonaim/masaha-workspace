# Round 3 design review — part SH: the shared layer: the design system, the identity, the shells, and consistency across parts

> **This is not a Work Item.** Use no project skill (`start-work-item`, `write-plan`, `open-pr`, `final-report`), no plan mode, no branch, commit, push, pull request, issue or comment, and ignore a `CLAUDE.md` or `AGENTS.md` that asks for them. **You never edit the repository**: `C:\dev\masaha\app-dr` and every other `C:\dev\masaha\app*` folder are read-only to you. You write only the files this prompt names, all under `C:\dev\masaha\workspace\DESIGN\ROUND3`.

## 1. Your task

You are the **SH** reviewer of Masaha's design review round 3: one of six reviewers, one per part (PU public · AU sign-in and account · OW owner · DK desk and reception · AD admin · SH shared), each applying every axis to its part. Masaha (مساحة) is a bilingual Arabic RTL / English platform for coworking spaces in Gaza: a public directory with live status, an account area, and one dashboard for owners, their reception staff and the platform admin. Its users are students, freelancers, space owners and reception staff, often on a phone, on a weak connection, in Arabic first.

**The goal is not only to find defects: it is to arrive at the best design** for every page, pattern and component of your part. **Nothing is fixed in this round**: you write one report; a lead reviewer checks it and merges the six; then the owner decides. **The owner's bar:** production-ready, no errors; he reacts strongly to sloppy UI and to an unexplained disabled control. **Never revive a decision the owner cancelled** (search the decisions files first): for example, amenities are no filter of the directory; a directory card shows no price except the chosen subscription's while sorting by it; no «24 ساعة» switch; no money on the owner's overview; no «sign out of all devices».

## 2. The subject

- **The real web app** at the identity PR's head `HEADSHA` (PR #144, `feat/ink-berry-identity`: the ink + berry colours and the logo), with real data and every role. It runs from its own worktree `C:\dev\masaha\app-dr` on **http://localhost:5336** (web) and **http://localhost:3336** (API), over the database `masaha_dr_dev` (a copy of the demo data). Its source at that head is `C:\dev\masaha\app-dr` — read it freely, never change it.
- **The prototype** (`docs/design/prototype/`, `docs/design/README.md`) is the reference for the intended design, not the subject. Report a difference between the app and the prototype only when the app is the worse of the two (or the prototype is — say which).
- **When:** the frames were taken (time pending). Gaza is UTC+2, and 2026-11-13 is a Friday: many spaces close early on Fridays, Pal Hub (space 26) from 20:00 Gaza; open / closed / live states depend on the hour a frame was taken — read the frame's own state before calling one wrong.
- **How each state was reached** is in `C:\dev\masaha\workspace\DESIGN\ROUND3\INVENTORY.md` (§2 and the base's row): by address, by scripted clicks, or by the capture tool answering a request at the network layer — held (loading), a 500 or a 429 simulated (the contract's envelope, `Retry-After: 60`), aborted (offline), mocked (an empty list), or a real answer patched (one field). Those are faithful to what the app draws for that answer. The **named states** written to `masaha_dr_dev` (people present, payments today, a long name) are listed there (§3); so is what was not captured (§4).

## 3. Read first

- In `C:\dev\masaha\app-dr` (the head): `CLAUDE.md`; `docs/frontend/design-system/foundation.md` **whole**; `docs/frontend/architecture.md`; `docs/project/overview.md` (v1 and *Not in v1*); `docs/project/glossary.md`; `docs/api/api-contract.md` (§1–§4, and the endpoints your screens call: every list is paged, every action can fail and answer 429); `docs/architecture/decisions/0019-ink-and-spark-brand.md` and `0008-live-status-not-counts.md`; `docs/design/README.md`; `docs/features/README.md` if present, and the capability of any screen you judge.
- The lens: `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` (§3 what to look for, §4 how to propose, §5 the report), **adapted to the app**: an issue's *level* is page | pattern | component | design system | rule; *where* is the app's URL, the role, the state and the frame's path in the pack.
- Settled decisions — **never reported again**, only how a page applies them, or a "rule in doubt" with why: `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` and every other `DECISIONS_*.md` in that folder (you judge consistency across parts).
- The identity's rules and values: `C:\dev\masaha\workspace\TASKS\IDENTITY\0_OWNER_DECISIONS.md` and `C:\dev\masaha\workspace\TASKS\IDENTITY\2_PLAN_PROD.md` §4–§6 and §9 (D1–D5 were accepted).
- Known items — cite them by their number, never as new: `C:\dev\masaha\workspace\REFACTOR_NOTES.md` and the repository's findings index `C:\dev\masaha\app-dr\docs\architecture\findings\README.md` (search it for your topic before you write an issue).
- The data you will see: `C:\dev\masaha\workspace\DESIGN\ROUND3\tools\survey-admin.md` (a read-only survey of the screens, their states and the demo data), and `survey-site.md`, `survey-space.md` beside it.

## 4. Your screens and your evidence

- **Frames:** `C:\dev\masaha\workspace\DESIGN\ROUND3\pack\SH\frames\` — each `<ID>-<width>-<lang>-<theme>`: `.png` (the first screen), `.full.png` (the whole page, at most 9000 px) and `.json` (measured facts).
- **Contact sheets:** `C:\dev\masaha\workspace\DESIGN\ROUND3\pack\SH\sheets\` — per base and width, `<ID>-<width>.png` (its four first screens side by side: ar light, ar dark, en light, en dark) and `<ID>-<width>-full.png` (its four whole pages). **156 sheets** for your 30 bases.
- **Measured leads:** `C:\dev\masaha\workspace\DESIGN\ROUND3\pack\SH\summary.md` — each fact once per base, with the frames it was measured on; and `C:\dev\masaha\workspace\DESIGN\ROUND3\pack\LEADS-ALL.md`, the leads of every part grouped across parts. A lead is not an issue until you have looked at the frame.
- **The facts JSON** (per frame; `firstScreen` read at the viewport, `wholePage` read with the viewport stretched to the page): `consoleErrors` and `apiErrors`; `horizontalPageOverflow`; `contrast.fails` (each visible text against the colour painted under it: `fg`, `ground`, `ratio`, `need` 4.5 or 3 for large text; text over a photo or the map is skipped and counted; disabled text is exempt); `targets.small` (an interactive element under 40 px, or 44 px on a coarse pointer — 390 and 768 are emulated as touch, 1440 as a mouse; `hit` counts a pseudo-element hit area; links inside running text are excluded); `seaValues` (any of the old *Sea* identity's 22 ramp values still painted); `sparkAsText`, `sparkOnAction`, `sparkMarks` (the berry ramp's values as text, on an action, or as a mark); `focusAfterTab` (the first Tab stops: the element, its outline, the outline's ratio to its ground, whether it is in view); `clipped`, `offscreen`, `headings`, `landmarks`, `dialogs`, `toasts`, `skeletons`, `text`.
- **Index:** `C:\dev\masaha\workspace\DESIGN\ROUND3\pack\INDEX.md` (every base of every part, its frames and sheets).

Your bases (30):

| ID | Screen | State | Role | URL | Widths |
|---|---|---|---|---|---|
| SH-01 | Showcase · actions | Button, toggles, DropdownMenu (the layer's own preview) | visitor | `/__showcase/preview/actions?theme={theme}&lang={lang}` | 390, 768, 1440 |
| SH-02 | Showcase · fields | every field component | visitor | `/__showcase/preview/fields?theme={theme}&lang={lang}` | 390, 768, 1440 |
| SH-03 | Showcase · display | Badge, Card, Avatar, StatCard, FilterTag, Meter, Logo | visitor | `/__showcase/preview/display?theme={theme}&lang={lang}` | 390, 768, 1440 |
| SH-04 | Showcase · data | Table, DataTable, BarChart, Heatmap | visitor | `/__showcase/preview/data?theme={theme}&lang={lang}` | 390, 768, 1440 |
| SH-05 | Showcase · feedback | Skeleton, Spinner, Alert, Toast, EmptyState, Refreshing | visitor | `/__showcase/preview/feedback?theme={theme}&lang={lang}` | 390, 768, 1440 |
| SH-06 | Showcase · overlays | Tooltip, Dialog, AlertDialog, Sheet, Popover triggers | visitor | `/__showcase/preview/overlays?theme={theme}&lang={lang}` | 390, 768, 1440 |
| SH-07 | Showcase · navigation | Tabs, Breadcrumb, Pagination, Sidebar | visitor | `/__showcase/preview/navigation?theme={theme}&lang={lang}` | 390, 768, 1440 |
| SH-08 | Showcase · icons | the icon set and its mirroring | visitor | `/__showcase/preview/icons?theme={theme}&lang={lang}` | 390, 768, 1440 |
| SH-09 | Site shell · phone menu | open, guest | visitor | `/spaces` | 390 |
| SH-10 | Site shell · phone menu | open, signed-in user | user | `/spaces` | 390 |
| SH-11 | Site shell · account menu | open (signed-in user) | user | `/spaces` | 768, 1440 |
| SH-12 | Dashboard shell · phone drawer | open (owner) | owner | `/dashboard/spaces/26` | 390 |
| SH-13 | Dashboard shell · phone drawer | open (admin, with the logo) | admin | `/dashboard/admin` | 390 |
| SH-14 | Dashboard shell · account menu | open (owner) | owner | `/dashboard/spaces/26/customers` | 768, 1440 |
| SH-15 | Dashboard shell · tablet rail | a rail item focused, its tooltip (admin) | admin | `/dashboard/admin/spaces` | 768 |
| SH-16 | Every shell · skip link | the first Tab: the skip link shown | visitor | `/spaces` | 390, 768, 1440 |
| SH-17 | States · loading | the directory's list loading (request held) | visitor | `/spaces` | 390, 768, 1440 |
| SH-18 | States · loading | the desk loading (who is present: request held) | reception | `/dashboard/spaces/26/desk` | 390, 768, 1440 |
| SH-19 | States · loading | the admin's spaces list loading (request held) | admin | `/dashboard/admin/spaces` | 390, 768, 1440 |
| SH-20 | States · loading | account settings loading (request held) | user | `/me` | 390, 768, 1440 |
| SH-21 | States · failure | a space's page fails to load (500 simulated, with the retries) | visitor | `/spaces/pal-hub` | 390, 768, 1440 |
| SH-22 | States · failure | the customers list fails to load (500 simulated) | owner | `/dashboard/spaces/26/customers` | 390, 768, 1440 |
| SH-23 | States · failure | the admin's users list fails to load (500 simulated) | admin | `/dashboard/admin/users` | 390, 768, 1440 |
| SH-24 | States · too many requests | the directory answered 429 (simulated, Retry-After 60) | visitor | `/spaces` | 390, 768, 1440 |
| SH-25 | States · too many requests | finance answered 429 (simulated) | owner | `/dashboard/spaces/26/finance` | 390, 768, 1440 |
| SH-26 | States · offline | the directory with no connection (request aborted) | visitor | `/spaces` | 390, 768, 1440 |
| SH-27 | States · 403 | reception on an owner's page | reception | `/dashboard/spaces/26/payments` | 390, 768, 1440 |
| SH-28 | States · 404 | an unknown page inside the dashboard | owner | `/dashboard/spaces/26/nope` | 390, 768, 1440 |
| SH-29 | Feedback · toast | a success toast: the profile's public link copied | owner | `/dashboard/spaces/26/profile` | 390, 768, 1440 |
| SH-30 | Feedback · toast | a toast with an undo: a favourite removed (write answered by the tool) | user | `/me/favorites` | 390, 768, 1440 |

For consistency across parts, also open the first-screen sheets (`-390`, `-768`, `-1440`) of these bases — one per screen of each other part — in `pack\<PART>\sheets\`:

- PU: PU-01, PU-05, PU-10, PU-13, PU-23, PU-24, PU-25
- AU: AU-01, AU-05, AU-08, AU-12, AU-13, AU-16, AU-19
- OW: OW-01, OW-02, OW-08, OW-11, OW-13, OW-20, OW-24, OW-26, OW-30, OW-32
- DK: DK-01, DK-08, DK-17, DK-23, DK-30, DK-31
- AD: AD-01, AD-02, AD-09, AD-10, AD-18, AD-19, AD-21, AD-26, AD-29, AD-31, AD-32

## 5. What to look at especially

- The design system as the showcase draws it (SH-01…08, the layer's own preview pages): every component's look and states against foundation §11–§12, in both themes and directions.
- The shells: the site header and phone menu (SH-09/10), the account menus (SH-11, SH-14), the focus shell (the AU frames), the dashboard's sidebars, the 768 rail (SH-15), the phone drawers (SH-12/13), page headers, the skip link (SH-16).
- States across parts: loading (SH-17…20), failure (SH-21…23), 429 (SH-24/25), offline (SH-26), 403 (SH-27), 404 (SH-28 and PU-25), toasts (SH-29/30), and the empty states in the other parts.
- **The identity across the product** (ADR 0019, foundation §4–§5, §16): ink on every action; the spark only where ADR 0019 allows (never small text, never an action, never destructive); hover never the selected tint; links underlined in running text; the logo (its places, sizes, its name in both languages, never mirrored) and the favicon (`/favicon.svg`, `/favicon.ico`, `/apple-touch-icon.png` on 5336); any of Sea's old values still painted. Start from `pack\LEADS-ALL.md` (every part's measured leads, grouped across parts).
- RTL / LTR, dark, the three widths, motion and reduced motion (live and in the source), and **the same job done the same way in every part**: filtering (the filter sheet, chips, selects), adding (where «add» sits), row menus, confirm-or-undo dialogs, empty states, page headers, pagination, toasts. For this, besides your own sheets, open at least the first-screen sheets at 390, 768 and 1440 of one base per screen of every other part (named in §4) and list them.

## 6. The axes — apply all eight

- **AX** accessibility — contrast, focus, names, order, targets, reduced motion (foundation §10)
- **CP** content and Arabic copy — the glossary, Arabic that reads as Arabic, one name per thing, labels that say what happens
- **DF** defects — what is broken: overflow, overlap, clipping, wrong state, console errors, a layout that breaks at a width
- **EX** excess — what could go: a duplicate, a decoration, a word too many, a control nobody needs
- **TR** truth to product, data and API — v1 and Not in v1, ADR 0008, the data model, the contract (every list paged, every action can fail and answer 429)
- **UX** the way through — the flow, the primary action, feedback and recovery, the fewest steps, the phone and the counter
- **VD** visual — alignment, spacing, hierarchy, type, colour roles, the design system used as designed
- **ID** the identity — ink + berry (ADR 0019), the spark's rules, hover vs selected, links underlined, the logo and its rules (§16)

Tag every issue with its axis or axes.

## 7. Skills — as lenses

Load with the Skill tool, first: `vectorlab-ux-skills:ux-audit`, `vectorlab-ux-skills:anti-slop`, `frontend-design:frontend-design` (polish and character, never a restyle against the design system), and for your part `vectorlab-ux-skills:colour-palette`, `vectorlab-ux-skills:typography`, `vectorlab-ux-skills:spacing`, `vectorlab-ux-skills:surfaces`, `vectorlab-ux-skills:icon-buttons`, `vectorlab-ux-skills:motion`, `vectorlab-ux-skills:transitions`, `vectorlab-ux-skills:reduced-motion`, `vectorlab-ux-skills:keyboard`. **Never `brand-guidelines`** (it is Anthropic's own brand; Masaha's is `foundation.md`, ADR 0019 and §16). The owner's word sets aside workflow §10's "review sessions use no plugin skill" for this round. A skill's advice that contradicts `foundation.md` or a settled decision is a **rule in doubt**, never a defect (for example, P9's «رجوع» on every dismiss button, or Arabic action labels written as a verbal noun such as «تسجيل الدخول»). List under **Skills loaded** which loaded; one that does not: say so and go on with the lens alone.

## 8. The method — gates the lead checks

1. **Open every contact sheet of your part** — all 156, no sampling — base by base. After each base, append to your notes file `C:\dev\masaha\workspace\DESIGN\ROUND3\REPORT\_work\R3-SH-notes.md` what you saw and the sheets you opened, so nothing is lost if your context is compacted. When a sheet shows something, open that frame's own `.png` / `.full.png` at full size and read its `.json`.
2. **Every issue states an observed fact with its measured value** — a ratio, a size in px, a count, the exact words on the screen, the console line, the element. Never "ensure", "must", "should be verified", "unverified", "no browser", "might".
3. **Every issue has its own cropped capture**, `C:\dev\masaha\workspace\DESIGN\ROUND3\shots\issues\R3-SH-NNN.png`, no two issues sharing one: cut it from a pack frame with `node C:\dev\masaha\workspace\DESIGN\ROUND3\tools\r3-crop.mjs <frame.png> <out.png> <x> <y> <w> <h> [--mark x,y,w,h] [--scale 2]` (pixels of the frame; a `.full.png`'s y is the page's; `--mark` draws a red box on the defect), or capture it live (8.5). Open each crop once to check it shows the defect.
4. **At least one issue re-checked in the app's source**: name the file and line in `C:\dev\masaha\app-dr` that causes it.
5. **Live checks** only where a still frame cannot answer (a keyboard path, focus order and its return, a discard question, a 429's countdown, hover): only on 5336 / 3336, **through the grant script, one Chrome at a time**, with the pack tool and an inventory of your own — write `C:\dev\masaha\workspace\DESIGN\ROUND3\live\SH\inv.json` (the same shape as `C:\dev\masaha\workspace\DESIGN\ROUND3\tools\inventory.json`; a step `{ "shot": "name" }` saves a screenshot and the focused element mid-path; `"tabStops": 15` records 15 Tab stops; `"widths"`, `"langs"`, `"themes"` narrow it), then run from `C:\dev\masaha\app-dr`: `node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs dr node C:\dev\masaha\workspace\DESIGN\ROUND3\tools\r3-pack.mjs C:\dev\masaha\workspace\DESIGN\ROUND3\live\SH\inv.json --out C:\dev\masaha\workspace\DESIGN\ROUND3\live --widths 390 --langs ar --themes light` (it may wait for memory; that is expected). Never start, stop or restart the servers. **No write to the database** — a live check that would write (a check-in, a save, a sign-out) is not done; if one is truly needed, it is named in your report.
6. Settled decisions are not reported again; a known item is cited by its number; a skill's contrary advice is a rule in doubt.

## 9. The report

Write `C:\dev\masaha\workspace\DESIGN\ROUND3\REPORT\R3-SH_REPORT.md`, in English, concise, in this order:

1. **Head and scope:** the head `HEADSHA`, your 30 bases, when the frames were taken.
2. **Summary:** the five most important points, one line each.
3. **Patterns** (level: pattern) — the cross-page proposals first; each names every page it changes.
4. **Issues**, most important first, IDs `R3-SH-001`…, one block each: **title**; **axis** (AX | CP | DF | EX | TR | UX | VD | ID, one or more); **type** (defect | improvement); **level** (page | pattern | component | design system | rule); **impact** (high | medium | low, for the user); **where** (the URL, the role, the state, and the frame paths: `pack\SH\frames\<frame>.png`); **evidence** (`shots\issues\R3-SH-NNN.png`); **observed** (the fact and its measured value); **what is wrong / what could be better**; **proposal** (built from the design system's own components and tokens — foundation §12; a new component says so and why); **why it is better** for the user; **cost** (S | M | L); **rule** (the document and section it applies or puts in doubt).
5. **Rules in doubt:** each rule of the documents (or a settled decision) you think makes the design worse, with why.
6. **Not reviewed:** what was out of reach, and why.
7. **Skills loaded** · **Sheets opened** (every sheet file name) · **Source re-checks** (file and line) · **Live checks** (what, the command, what it showed) · **Database writes** (expected: none).

Prefer one strong proposal to three options; give options only where the choice is the owner's. Fewer true issues beat many: an issue a reader cannot see in its capture is not an issue.

## 10. Limits

Never edit the repository; no commit, branch, push, PR, issue or comment; no migration, no dependency, never `db:seed`; only `masaha_dr_dev`, and no write to it; never print a secret (the passwords live in `C:\dev\masaha\app-dr\apps\api\.env` — the pack tool reads them itself); ports 5336 / 3336 only; never stop on the volume of work — report it. When your report is written, reply with only: its path, the number of issues, and the number of sheets opened.

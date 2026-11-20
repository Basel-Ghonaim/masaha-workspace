# Round 3 design review — part AD: the admin's dashboard

> **This is not a Work Item.** Use no project skill (`start-work-item`, `write-plan`, `open-pr`, `final-report`), no plan mode, no branch, commit, push, pull request, issue or comment, and ignore a `CLAUDE.md` or `AGENTS.md` that asks for them. **You never edit the repository**: `C:\dev\masaha\app-dr` and every other `C:\dev\masaha\app*` folder are read-only to you. You write only the files this prompt names, all under `C:\dev\masaha\workspace\DESIGN\ROUND3`.

## 1. Your task

You are the **AD** reviewer of Masaha's design review round 3: one of six reviewers, one per part (PU public · AU sign-in and account · OW owner · DK desk and reception · AD admin · SH shared), each applying every axis to its part. Masaha (مساحة) is a bilingual Arabic RTL / English platform for coworking spaces in Gaza: a public directory with live status, an account area, and one dashboard for owners, their reception staff and the platform admin. Its users are students, freelancers, space owners and reception staff, often on a phone, on a weak connection, in Arabic first.

**The goal is not only to find defects: it is to arrive at the best design** for every page, pattern and component of your part. **Nothing is fixed in this round**: you write one report; a lead reviewer checks it and merges the six; then the owner decides. **The owner's bar:** production-ready, no errors; he reacts strongly to sloppy UI and to an unexplained disabled control. **Never revive a decision the owner cancelled** (search the decisions files first): for example, amenities are no filter of the directory; a directory card shows no price except the chosen subscription's while sorting by it; no «24 ساعة» switch; no money on the owner's overview; no «sign out of all devices».

## 2. The subject

- **The real web app** at the identity PR's head `HEADSHA` (PR #144, `feat/ink-berry-identity`: the ink + berry colours and the logo), with real data and every role. It runs from its own worktree `C:\dev\masaha\app-dr` on **http://localhost:5336** (web) and **http://localhost:3336** (API), over the database `masaha_dr_dev` (a copy of the demo data). Its source at that head is `C:\dev\masaha\app-dr` — read it freely, never change it.
- **The prototype** (`docs/design/prototype/`, `docs/design/README.md`) is the reference for the intended design, not the subject. Report a difference between the app and the prototype only when the app is the worse of the two (or the prototype is — say which).
- **When:** the frames were taken (time pending). Gaza is UTC+2, and 2026-11-13 is a Friday: many spaces close early on Fridays, Pal Hub (space 26) from 20:00 Gaza; open / closed / live states depend on the hour a frame was taken — read the frame's own state before calling one wrong.
- **How each state was reached** is in `C:\dev\masaha\workspace\DESIGN\ROUND3\INVENTORY.md` (§2 and the base's row): by address, by scripted clicks, or by the capture tool answering a request at the network layer — held (loading), a 500 or a 429 simulated (the contract's envelope, `Retry-After: 60`), aborted (offline), mocked (an empty list), or a real answer patched (one field). Those are faithful to what the app draws for that answer. The **named states** written to `masaha_dr_dev` (people present, payments today, a long name) are listed there (§3); so is what was not captured (§4).

## 3. Read first

- In `C:\dev\masaha\app-dr` (the head): `CLAUDE.md`; `docs/frontend/design-system/foundation.md` **whole**; `docs/frontend/architecture.md`; `docs/project/overview.md` (v1 and *Not in v1*); `docs/project/glossary.md`; `docs/api/api-contract.md` (§1–§4, and the endpoints your screens call: every list is paged, every action can fail and answer 429); `docs/architecture/decisions/0019-ink-and-spark-brand.md` and `0008-live-status-not-counts.md`; `docs/design/README.md`; your capabilities: `docs/features/overview.md`, `docs/features/spaces.md`, `docs/features/space-links.md`, `docs/features/users.md`, `docs/features/data-reports.md`, `docs/features/lookups.md`, `docs/features/audit.md`, `docs/features/platform-settings.md`.
- The lens: `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` (§3 what to look for, §4 how to propose, §5 the report), **adapted to the app**: an issue's *level* is page | pattern | component | design system | rule; *where* is the app's URL, the role, the state and the frame's path in the pack.
- Settled decisions — **never reported again**, only how a page applies them, or a "rule in doubt" with why: `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md`, `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_ADMIN.md`.
- The identity's rules and values: `C:\dev\masaha\workspace\TASKS\IDENTITY\0_OWNER_DECISIONS.md` and `C:\dev\masaha\workspace\TASKS\IDENTITY\2_PLAN_PROD.md` §4–§6 and §9 (D1–D5 were accepted).
- Known items — cite them by their number, never as new: `C:\dev\masaha\workspace\REFACTOR_NOTES.md` and the repository's findings index `C:\dev\masaha\app-dr\docs\architecture\findings\README.md` (search it for your topic before you write an issue).
- The data you will see: `C:\dev\masaha\workspace\DESIGN\ROUND3\tools\survey-admin.md` (a read-only survey of the screens, their states and the demo data).

## 4. Your screens and your evidence

- **Frames:** `C:\dev\masaha\workspace\DESIGN\ROUND3\pack\AD\frames\` — each `<ID>-<width>-<lang>-<theme>`: `.png` (the first screen), `.full.png` (the whole page, at most 9000 px) and `.json` (measured facts).
- **Contact sheets:** `C:\dev\masaha\workspace\DESIGN\ROUND3\pack\AD\sheets\` — per base and width, `<ID>-<width>.png` (its four first screens side by side: ar light, ar dark, en light, en dark) and `<ID>-<width>-full.png` (its four whole pages). **194 sheets** for your 33 bases.
- **Measured leads:** `C:\dev\masaha\workspace\DESIGN\ROUND3\pack\AD\summary.md` — each fact once per base, with the frames it was measured on. A lead is not an issue until you have looked at the frame.
- **The facts JSON** (per frame; `firstScreen` read at the viewport, `wholePage` read with the viewport stretched to the page): `consoleErrors` and `apiErrors`; `horizontalPageOverflow`; `contrast.fails` (each visible text against the colour painted under it: `fg`, `ground`, `ratio`, `need` 4.5 or 3 for large text; text over a photo or the map is skipped and counted; disabled text is exempt); `targets.small` (an interactive element under 40 px, or 44 px on a coarse pointer — 390 and 768 are emulated as touch, 1440 as a mouse; `hit` counts a pseudo-element hit area; links inside running text are excluded); `seaValues` (any of the old *Sea* identity's 22 ramp values still painted); `sparkAsText`, `sparkOnAction`, `sparkMarks` (the berry ramp's values as text, on an action, or as a mark); `focusAfterTab` (the first Tab stops: the element, its outline, the outline's ratio to its ground, whether it is in view); `clipped`, `offscreen`, `headings`, `landmarks`, `dialogs`, `toasts`, `skeletons`, `text`.
- **Index:** `C:\dev\masaha\workspace\DESIGN\ROUND3\pack\INDEX.md` (every base of every part, its frames and sheets).

Your bases (33):

| ID | Screen | State | Role | URL | Widths |
|---|---|---|---|---|---|
| AD-01 | 25 Overview | the platform's work queue | admin | `/dashboard/admin` | 390, 768, 1440 |
| AD-02 | 26 Spaces | 37 spaces, page 1 of 2 | admin | `/dashboard/admin/spaces` | 390, 768, 1440 |
| AD-03 | 26 Spaces | the «stale or missing» chip on | admin | `/dashboard/admin/spaces?stale=true` | 390, 768, 1440 |
| AD-04 | 26 Spaces | deleted spaces, restore | admin | `/dashboard/admin/spaces?status=deleted` | 390, 768, 1440 |
| AD-05 | 26 Spaces | a search that matches nothing | admin | `/dashboard/admin/spaces?q=zzzz` | 390, 768, 1440 |
| AD-06 | 26 Spaces | filters bottom sheet open | admin | `/dashboard/admin/spaces` | 390 |
| AD-07 | 26 Spaces | a row's menu | admin | `/dashboard/admin/spaces` | 390, 768, 1440 |
| AD-08 | 26 Spaces | delete a space: the question | admin | `/dashboard/admin/spaces` | 390, 768, 1440 |
| AD-09 | 26 Spaces (add) | add a space: sent empty | admin | `/dashboard/admin/spaces/new` | 390, 768, 1440 |
| AD-10 | 26 Spaces (editor) | unverified, one group missing (A2) | admin | `/dashboard/admin/spaces/32` | 390, 768, 1440 |
| AD-11 | 26 Spaces (editor) | verified: read-only, its owner named | admin | `/dashboard/admin/spaces/26` | 390, 768, 1440 |
| AD-12 | 26 Spaces (editor) | stale prices: «still correct» | admin | `/dashboard/admin/spaces/10#prices` | 390, 768, 1440 |
| AD-13 | 26 Spaces (editor) | prices sheet saved with an empty amount | admin | `/dashboard/admin/spaces/32?sheet=prices` | 390, 768, 1440 |
| AD-14 | 26 Spaces (editor) | hours sheet, each day set | admin | `/dashboard/admin/spaces/10?sheet=hours` | 390, 768, 1440 |
| AD-15 | 26 Spaces (editor) | amenities sheet (common and own) | admin | `/dashboard/admin/spaces/10?sheet=amenities` | 390, 768, 1440 |
| AD-16 | 26 Spaces (editor) | contacts sheet | admin | `/dashboard/admin/spaces/10?sheet=contacts` | 390, 768, 1440 |
| AD-17 | 26 Spaces (editor) | location sheet (map) | admin | `/dashboard/admin/spaces/24?sheet=location` | 390, 768, 1440 |
| AD-18 | 27 Space owners (link) | link an owner: sent with no person | admin | `/dashboard/admin/spaces/32` | 390, 768, 1440 |
| AD-19 | 27 Space owners | 7 owners | admin | `/dashboard/admin/owners` | 390, 768, 1440 |
| AD-20 | 27 Space owners | add an owner: sent empty | admin | `/dashboard/admin/owners?sheet=add` | 390, 768, 1440 |
| AD-21 | 29 Users | the one-time password dialog (issue answer mocked, nothing written) | admin | `/dashboard/admin/users` | 390, 768, 1440 |
| AD-22 | 29 Users | 50 users, page 1 of 3 | admin | `/dashboard/admin/users` | 390, 768, 1440 |
| AD-23 | 29 Users | an owner's menu: role change held, with its reason | admin | `/dashboard/admin/users?q=garden.owner%40example.com` | 390, 768, 1440 |
| AD-24 | 29 Users | make a user an admin: the question | admin | `/dashboard/admin/users` | 390, 768, 1440 |
| AD-25 | 29 Users | suspend a user: the question | admin | `/dashboard/admin/users` | 390, 768, 1440 |
| AD-26 | 28 Data reports | 18 reports | admin | `/dashboard/admin/reports` | 390, 768, 1440 |
| AD-27 | 28 Data reports | deciding (unverified space): not accepted with no reply | admin | `/dashboard/admin/reports?open=4` | 390, 768, 1440 |
| AD-28 | 28 Data reports | a verified space's report: read only | admin | `/dashboard/admin/reports?open=1` | 390, 768, 1440 |
| AD-29 | 30 Lookups | governorates and areas | admin | `/dashboard/admin/lookups` | 390, 768, 1440 |
| AD-30 | 30 Lookups | amenities: add, saved empty | admin | `/dashboard/admin/lookups?tab=amenities` | 390, 768, 1440 |
| AD-31 | 31 Audit log | the platform's last 30 days | admin | `/dashboard/admin/audit` | 390, 768, 1440 |
| AD-32 | 32 Settings | the three cards | admin | `/dashboard/admin/settings` | 390, 768, 1440 |
| AD-33 | 32 Settings | freshness: 999 days saved (unsaved changes, the error) | admin | `/dashboard/admin/settings` | 390, 768, 1440 |

## 5. What to look at especially

- A1–A8 and the amendments: the shared space editor (five groups and the gallery, «لم تُضف بعد», the A2 checklist, the sheets; a verified space read-only), hours (no «24 ساعة» switch), prices, contacts (the carrier derived), own amenities beside the common ones.
- Owners and users: A4 (one way to link), A5 (say what an action does to someone else before it is done; the one-time password dialog AD-21), A6, AD-021, a held role change with its reason (AD-23).
- Lists: A7 (cards until 1024 for spaces, users and reports), filters, the «stale or missing» chip, deleted spaces and restore (A3), data reports (A8, a verified space's report read only), lookups (never paged; arrows; the amenities' icons), the audit log, platform settings (AD-029).

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

Load with the Skill tool, first: `vectorlab-ux-skills:ux-audit`, `vectorlab-ux-skills:anti-slop`, `frontend-design:frontend-design` (polish and character, never a restyle against the design system), and for your part `vectorlab-ux-skills:forms`, `vectorlab-ux-skills:labels`, `vectorlab-ux-skills:empty-states`, `vectorlab-ux-skills:errors`, `vectorlab-ux-skills:defaults`. **Never `brand-guidelines`** (it is Anthropic's own brand; Masaha's is `foundation.md`, ADR 0019 and §16). The owner's word sets aside workflow §10's "review sessions use no plugin skill" for this round. A skill's advice that contradicts `foundation.md` or a settled decision is a **rule in doubt**, never a defect (for example, P9's «رجوع» on every dismiss button, or Arabic action labels written as a verbal noun such as «تسجيل الدخول»). List under **Skills loaded** which loaded; one that does not: say so and go on with the lens alone.

## 8. The method — gates the lead checks

1. **Open every contact sheet of your part** — all 194, no sampling — base by base. After each base, append to your notes file `C:\dev\masaha\workspace\DESIGN\ROUND3\REPORT\_work\R3-AD-notes.md` what you saw and the sheets you opened, so nothing is lost if your context is compacted. When a sheet shows something, open that frame's own `.png` / `.full.png` at full size and read its `.json`.
2. **Every issue states an observed fact with its measured value** — a ratio, a size in px, a count, the exact words on the screen, the console line, the element. Never "ensure", "must", "should be verified", "unverified", "no browser", "might".
3. **Every issue has its own cropped capture**, `C:\dev\masaha\workspace\DESIGN\ROUND3\shots\issues\R3-AD-NNN.png`, no two issues sharing one: cut it from a pack frame with `node C:\dev\masaha\workspace\DESIGN\ROUND3\tools\r3-crop.mjs <frame.png> <out.png> <x> <y> <w> <h> [--mark x,y,w,h] [--scale 2]` (pixels of the frame; a `.full.png`'s y is the page's; `--mark` draws a red box on the defect), or capture it live (8.5). Open each crop once to check it shows the defect.
4. **At least one issue re-checked in the app's source**: name the file and line in `C:\dev\masaha\app-dr` that causes it.
5. **Live checks** only where a still frame cannot answer (a keyboard path, focus order and its return, a discard question, a 429's countdown, hover): only on 5336 / 3336, **through the grant script, one Chrome at a time**, with the pack tool and an inventory of your own — write `C:\dev\masaha\workspace\DESIGN\ROUND3\live\AD\inv.json` (the same shape as `C:\dev\masaha\workspace\DESIGN\ROUND3\tools\inventory.json`; a step `{ "shot": "name" }` saves a screenshot and the focused element mid-path; `"tabStops": 15` records 15 Tab stops; `"widths"`, `"langs"`, `"themes"` narrow it), then run from `C:\dev\masaha\app-dr`: `node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs dr node C:\dev\masaha\workspace\DESIGN\ROUND3\tools\r3-pack.mjs C:\dev\masaha\workspace\DESIGN\ROUND3\live\AD\inv.json --out C:\dev\masaha\workspace\DESIGN\ROUND3\live --widths 390 --langs ar --themes light` (it may wait for memory; that is expected). Never start, stop or restart the servers. **No write to the database** — a live check that would write (a check-in, a save, a sign-out) is not done; if one is truly needed, it is named in your report.
6. Settled decisions are not reported again; a known item is cited by its number; a skill's contrary advice is a rule in doubt.

## 9. The report

Write `C:\dev\masaha\workspace\DESIGN\ROUND3\REPORT\R3-AD_REPORT.md`, in English, concise, in this order:

1. **Head and scope:** the head `HEADSHA`, your 33 bases, when the frames were taken.
2. **Summary:** the five most important points, one line each.
3. **Patterns** (level: pattern) — the cross-page proposals first; each names every page it changes.
4. **Issues**, most important first, IDs `R3-AD-001`…, one block each: **title**; **axis** (AX | CP | DF | EX | TR | UX | VD | ID, one or more); **type** (defect | improvement); **level** (page | pattern | component | design system | rule); **impact** (high | medium | low, for the user); **where** (the URL, the role, the state, and the frame paths: `pack\AD\frames\<frame>.png`); **evidence** (`shots\issues\R3-AD-NNN.png`); **observed** (the fact and its measured value); **what is wrong / what could be better**; **proposal** (built from the design system's own components and tokens — foundation §12; a new component says so and why); **why it is better** for the user; **cost** (S | M | L); **rule** (the document and section it applies or puts in doubt).
5. **Rules in doubt:** each rule of the documents (or a settled decision) you think makes the design worse, with why.
6. **Not reviewed:** what was out of reach, and why.
7. **Skills loaded** · **Sheets opened** (every sheet file name) · **Source re-checks** (file and line) · **Live checks** (what, the command, what it showed) · **Database writes** (expected: none).

Prefer one strong proposal to three options; give options only where the choice is the owner's. Fewer true issues beat many: an issue a reader cannot see in its capture is not an issue.

## 10. Limits

Never edit the repository; no commit, branch, push, PR, issue or comment; no migration, no dependency, never `db:seed`; only `masaha_dr_dev`, and no write to it; never print a secret (the passwords live in `C:\dev\masaha\app-dr\apps\api\.env` — the pack tool reads them itself); ports 5336 / 3336 only; never stop on the volume of work — report it. When your report is written, reply with only: its path, the number of issues, and the number of sheets opened.

# SPACE_PROFILE — the space profile redesign in the PROTOTYPE (plan, then build, then stop uncommitted)

You are a worker on **Masaha**, a bilingual (Arabic RTL / English) directory and dashboard for coworking spaces in
Gaza. This task redesigns **the owner's space profile and the admin's space editor in the design prototype only**.
You **write a short plan, then build it straight away** (no approval stop), and you **stop before committing** so the
owner and the main supervisor review the result in the browser. Read this prompt whole first.

## 0. Where you work — a worktree of its own

- Folder: **`C:\dev\masaha\app-design`** (a worktree; clean). Do not work in `C:\dev\masaha\app` (another worker is
  building the directory there) or `C:\dev\masaha\app-b` (the palette lab).
- Start: `git fetch origin` then `git switch -c design/space-profile origin/main` (`40cb481d` or later). Leave the
  old local branch `feat/owner-space-profile-design` alone (the owner decides its deletion).
- Read `CLAUDE.md` and **`docs/design/README.md`** (the prototype's rules, its two checks, how to serve it).

## 1. What to build — the owner's decisions

The binding source: **`C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\0_OWNER_DECISIONS.md`** — read it whole: the page
(G1–G5 and the settled order), the header (H1–H4), الصور (P1–P7 and the settled lines), الأسعار (**R1, R2, R5–R9**;
R3 and R4 were replaced), ساعات العمل (W1–W5), الورديات (S1–S5), المرافق (A1–A3), عن المساحة (B1–B2), الموقع (L1–L2),
التواصل (C1–C2), and **«After the mock-up» M1–M4, which override earlier lines** (photos on a phone, the header on a
phone, contacts as tiles, the new contact types and «وسيلة أخرى»).

**A behaviour reference:** the owner approved an interactive mock-up —
`C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\mockup\index.html` (open it in Chrome; it runs without a server). Use it
to see each section's view and edit states, the Sheets, the row editors, the simple/custom hours, the drag with the
keyboard, the confirmations. It is **plain HTML with its own CSS — a specification of behaviour, not code to copy**:
the prototype is built with the design-system components already vendored (`Card`, `Sheet`, `Button`, `Badge`,
`Field`, `Input`, `Select`, `Checkbox`, `Switch`, `AlertDialog`, `Combobox`, `Meter`, …), semantic tokens, and the
prototype's own patterns. Its known bug: on a phone the header's buttons overflowed — the decisions say they take
the card's full width.

## 2. The prototype's files

- Pages: `docs/design/prototype/Owner space profile.html`, `docs/design/prototype/Admin space edit.html`, and
  `docs/design/prototype/Packages.html` (its prices become read-only with «تعديل الأسعار في ملف المساحة», R1).
- Modules they share: `docs/design/prototype/masaha/profile-a.jsx`, `masaha/profile-b.jsx`, `masaha/space-parts.jsx`
  (find which section lives where before planning), `masaha/owner-data.js` / `masaha/admin-data.js` /
  `masaha/data.js` / `masaha/details-data.js` for sample data, `masaha/i18n.js` if the copy lives there,
  `masaha/masaha.css` only for a layout rule no bundled class can express.
- Records: `docs/design/INDEX.md` (the pages' states), `docs/design/CHANGES.md` (a section «Refactor 2 — the space
  profile (2026-11-08)», one line per decision, naming what it revises: O1/O6 prices, P9 kept, the old section
  order), `docs/design/prototype/Flows - states.html` (frames for the new states).
- **Allowed: `docs/design/` only.** Never touch `apps/`, `packages/` or any other file under `docs/` — no production
  file under any circumstances. If a module is shared with a page outside this task (for example `space-parts.jsx`
  with Space details), keep that page working and look at it.

## 3. The prototype's traps

- One **global scope** per page: no new top-level name that another script of the page has; none the browser owns
  (`name`, …). **No object rest** (`const { a, ...rest } = x`).
- The CSS is a **prebuilt bundle**: only classes already used somewhere in the prototype; `check-classes` fails on a
  new one. A missing layout goes in `masaha/masaha.css` with a comment.
- Every text in **both languages** with `tr("…", "…")`. Arabic first, plain; numbers and links LTR-isolated.
- Dragging: the prototype has no library — build it with native drag and drop **plus the keyboard** (focus a
  photo/contact, Space to lift, arrows to move, Space to drop, Escape to cancel, each step announced in a live
  region). Touch dragging is the production library's job (an approved dependency); say so in the report.
- The checks, from the worktree root: `node docs/design/scripts/check-parse.mjs` and
  `node docs/design/scripts/check-classes.mjs`. They cannot see runtime problems: **open the pages**.

## 4. Plan, then build — no stop in between

1. Write a short plan (≤ 60 lines) to `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\2_PLAN.md`: which module holds
   which section today and where each new piece goes; the order of work; the sample data you add (an empty section,
   a stale one, a space with shifts, a «وسيلة أخرى» contact, a space without hours, ten photos to show the limit);
   anything in the decisions you cannot build in the prototype as written and what you do instead; **Proposed
   alternatives** where you think a decision is weaker than another way (you may challenge; never deviate silently).
   **Do not wait** — start building right after writing it.
2. Build the owner's page first, then the admin's editor (the same design; its header adds «غير موثّقة» /
   «مخفية عن الزوار»; its actions stay in the top bar), then «الباقات والأسعار».
3. Serve: `cd docs/design/prototype` then `python -m http.server 5331` (5325 and 5330 are in use). Look at every
   state at **390, 768, 1024 and 1440**, **Arabic and English**, **light and dark**: nothing overflowing (the phone
   header above all), no block drawn twice, no leftover old control (the always-open fields, the per-section Save on
   the page, «نسخ إلى كل الأيام», the move buttons, the custom description), no console error; the Sheets trap the
   focus and return it; «تجاهل التغييرات؟» on closing with changes; every dismiss reads «رجوع» (P9).
4. Both checks pass. Screenshots to `C:\Users\basel\Downloads\space-profile-shots\` (never into the repository).

## 5. Stop — ready for review, nothing committed

**No commit, no push, no PR.** Print: the branch, `git status -s`, `git diff --stat`, the checks' output, the serve
command, and ready URLs for each section's view and edit state, the owner's and the admin's page, phone and desktop,
`?lang=en`, `?theme=dark`. Then wait: the owner's notes come in this same session; apply them, still uncommitted,
check again, and stop again. Committing (one commit, by explicit path, Conventional, no tool attribution), the push
and the PR happen only when the owner says so.

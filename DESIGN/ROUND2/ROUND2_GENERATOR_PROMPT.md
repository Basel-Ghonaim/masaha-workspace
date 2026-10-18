# Design review, round 2 — write the review prompts (for OpenCode)

You are the **prompt writer** for the second design review of Masaha's living prototype. **You do not
review anything yourself.** You write a set of review prompts — one per *part* of the product and per
*axis* of judgement — that other OpenCode sessions will run **in parallel**, each alone, each without
your context. Then you write a run sheet and the summary prompts. Then you stop.

## 0. Where, and what you may touch

- **Read from** `C:\dev\masaha\design` (a git worktree of the repository, detached at
  `origin/main`). `git fetch origin` first; read files, never edit, commit, check out or install.
- **Write only into** `C:\dev\masaha\workspace\DESIGN\ROUND2\`:
  `PROMPT\` (the review prompts and the summary prompts), and `RUN_SHEET.md` at its root. The reviews
  will write to `ROUND2\REPORT\`, the summaries to `ROUND2\SUMMARY\`; you create neither file.
- No tool attribution in anything you write.

## 1. Read first (to write good prompts, not to review)

1. `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` — the lens every reviewer follows: what the
   design owns, what is settled, the three checks every review makes, what to look for, how to
   propose, the report's shape. **Every prompt you write points to it and builds on it.**
2. `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_*.md` (shared, public, account, admin, owner,
   desk), with every *Amended* / *Decided* / *Changed* note at their tops: **what they settle is not
   reported again** in round 2; a reviewer who thinks a settled decision makes the product worse
   reports it as a **"decision in doubt"**, with why, in its own section, never as a defect.
3. `docs/design/README.md`, `docs/design/INDEX.md` (every frame, by section, with its prototype URL and
   parameters), `docs/design/SCREENS.md` (the 32 screens of foundation §13 mapped to the archive),
   `docs/design/CHANGES.md` (what batches 1–6 changed).
4. The rules the reviews judge by: `docs/frontend/design-system/foundation.md`,
   `docs/project/glossary.md`, `docs/project/overview.md` (v1 and *Not in v1*),
   `docs/architecture/data-model.md`, `docs/api/api-contract.md`, the ADRs in
   `docs/architecture/decisions/` (0008 live status, 0009 roles, 0010 the ledger above all).

## 2. The parts (six) — each prompt covers one

Assign each prototype page, and each INDEX section, to exactly one part; list them in each prompt by
**page file name and INDEX section** (read `INDEX.md` at write time; do not copy this list blindly).
1. **AU — Signing in and the account:** sign in, register, forgot and reset password, the reset email,
   Google, the forced password change; the signed-in header, account settings, favourites, my reports.
2. **PU — The public site:** home, the directory (list, map, filters, near me), a space's page, about,
   the error and offline pages.
3. **AD — The admin's dashboard:** the overview, spaces (list, add, the editor, the verified space),
   owners, users, data reports, lookups, the audit log, platform settings.
4. **OW — The owner's management:** the overview, the space profile, packages and prices,
   announcements, staff, finance and reports, settings, data reports, the owner's audit log.
5. **DK — The front desk and reception:** the desk, check-in and check-out, the money block, customers,
   the customer file, subscriptions and renewals, payments, «دفعاتي اليوم».
6. **SH — The shared layer:** the shells (site and dashboard), navigation and the space switcher, top
   bars and drawers, the account menu, page headers, toasts, dialogs and sheets, the states (loading,
   empty, error, offline, 403, 404, 429), the filter bar and pagination, as they recur across parts.

## 3. The axes (seven) — each prompt judges one

Each prompt judges its part **through one axis only**, deeply, and leaves the others to their own
prompts. Write the axis's questions into the prompt, adapted to the part (a desk's "fewest steps" is
not a sign-in's).
1. **UX — Experience and flow:** can each role finish its daily tasks in the fewest steps, with no
   dead end, nothing asked twice, a way back, and feedback after each action? Arabic first, phone
   first, a weak connection in Gaza.
2. **VD — Visual design and consistency:** hierarchy, layout and grid, spacing on the scale, type
   styles, colour by semantic role and token, the same job done the same way on every page (name the
   pattern and where it differs).
3. **DF — Design defects:** what is broken: overflow, cut or overlapping content, a wrong component or
   variant, a missing or wrong state, broken RTL/LTR (numbers, phones, Latin names, icons), dark mode,
   the three widths **390, 768, 1440**, console errors, blank frames.
4. **EX — Excess and simplification («الزوائد»):** what can go: duplicated information, controls nobody
   needs, a section doing two jobs, decoration without meaning, text that repeats the label, steps that
   can merge. Every removal says what the user gains.
5. **CP — Content and Arabic copy:** wording that reads as a translation, a term against the glossary,
   one thing named two ways, a label that does not say what happens, plurals and gender, numbers and
   dates, the English mirror, truth (a promise the product cannot keep).
6. **AX — Accessibility and resilience:** focus visible and in order, names for every control,
   information not by colour alone, contrast, 44 × 44 touch targets, screen-reader order; and the
   states a weak connection meets: loading, offline, failure with retry, 429, a slow image.
7. **TR — Truth to the product, the data and the API:** nothing on screen the API, the data model or
   v1 cannot hold (*Not in v1*: no online payment, no QR check-in, no booking, no reviews); live status
   a state, never a public count; privacy (the location, a reporter's name, money in view of others);
   roles (who may see and do what, ADR 0009).

**Prompts per part:** all seven axes for AU, PU, AD, OW and DK; for **SH** write UX, VD, DF, CP and AX
(EX and TR are judged inside the parts). That is **40 review prompts**.

## 4. What every review prompt contains (write each in full; no "see above")

- **Title and ID prefix:** `R2-<PART>-<AXIS>` (e.g. `R2-DK-UX`); each issue the reviewer reports takes
  the next number (`R2-DK-UX-001`).
- **Who it is for:** an independent reviewer (OpenCode), alone, read-only, with no context but the
  prompt.
- **Where:** read from `C:\dev\masaha\design` at `origin/main` (check `git rev-parse HEAD`
  equals `git rev-parse origin/main` after `git fetch`; write it at the top of the report); never edit,
  commit, check out or install.
- **Its own port**, so forty can run at once: `python -m http.server <port> --bind 127.0.0.1
  --directory docs/design/prototype`, ports **5401–5440**, one per prompt (list them in the run sheet);
  stop the server by its PID at the end and check the port free. Evidence captures as `<ID>.png` in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\<PART>-<AXIS>\`.
- **The scope:** the part's pages and INDEX sections (by name, with their frame URLs and parameters
  from `INDEX.md`), the roles that use them (guest, user, admin, owner, reception), and the widths and
  modes to open (390, 768, 1440; Arabic and English; light and dark — narrowed only where the axis
  allows, and saying so).
- **The axis:** its questions, adapted to the part, and **what is out of this prompt's axis** (so two
  reviewers do not report the same thing).
- **What is settled:** the decision files to read and the rule that settled decisions are not
  reported again (only as "decisions in doubt").
- **The lens:** follow `REVIEW_LENS.md` §3–§5 for what to look for, how to propose (built from the
  design system's own components and tokens, why it is better, its cost S/M/L) and the report's shape.
- **The report:** `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-<PART>-<AXIS>_REPORT.md`:
  a one-line verdict; the five most important points; the issues (ID, title, type, level, impact,
  where — frame label, URL with parameters, width and mode —, evidence, what is wrong, proposal, why,
  cost, rule); the decisions in doubt; what was not reviewed and why. English, concise.
- **A cap:** at most 25 issues, the most important first; no praise; one issue per problem.

## 5. The summary prompts (seven)

- **One per part** (`R2-<PART>-SUMMARY`): read that part's axis reports, merge duplicates across
  axes, rank by impact for the user, mark contradictions between axes, and write
  `ROUND2\SUMMARY\R2-<PART>_SUMMARY.md` as a **decision list for the owner**: each item with its
  options and a recommendation, the decisions in doubt apart, and the IDs it came from.
- **One across all** (`R2-ALL-SUMMARY`): read the six part summaries and write
  `ROUND2\SUMMARY\R2-ALL_SUMMARY.md`: the patterns that recur across parts (one proposal each, naming
  every page it changes), the ten most important items overall, and the order to fix them in.
- Each summary prompt is read-only and opens no server (it reads reports only).

## 6. The run sheet (`ROUND2\RUN_SHEET.md`)

A table of the 40 review prompts (ID, part, axis, file, port, report path) and the 7 summary prompts;
**the order:** the 40 reviews in **four waves of ten** (mix the parts in each wave, so one part is not
judged by ten sessions at once), then the six part summaries, then the summary across all; and one
line to paste into each OpenCode session:
`Read C:\dev\masaha\workspace\DESIGN\ROUND2\PROMPT\<file> whole and follow it.`

## 7. When you are done

Check that the 40 + 7 prompt files exist and are complete, that no two share a port, that every page
of the prototype belongs to one part, and that the run sheet lists them all. Report in a few lines:
the files written, the page-to-part assignment, anything in the prototype you could not place.
Then stop. **Do not run any review.**

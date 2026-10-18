# Review — PR #74 (S2b-4a: the admin's space editor, first half — web)

You are an **independent reviewer** of PR #74 in the Masaha repository (Basel-Ghonaim/masaha), in a
fresh Claude Code conversation (Opus 5.5, effort high) — never the conversation that built it.
Write your report to `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW74_CLAUDE_REPORT.md`.

**Size cap:** at most 3 read-only subagents (for example one per area of §"Look at these": the
sections and the API calls; the leave guard, the title and the state; the tests and the documents),
no workflow. Each subagent reads commit objects only, as below. **No plugin skill** (workflow §10:
review sessions use none); `writing-good-tests.md`'s mutation check may be read as a lens on the
tests. Do not enter plan mode: read, verify, write the report.

## Rules

- **Run from `C:\Users\basel\masaha`**, but **read only commit objects** (that folder's working tree
  belongs to worker A). No edits, commits, checkouts, switches, installs, npm or test runs, no
  servers, database or Docker commands, no GitHub comments. **Do not run the tests:** CI ran every
  lane on this head and passed; your job is to read. `git fetch origin`, then pin to **the PR's
  current head** (`gh pr view 74 --json headRefOid` — expected `b5406c0`; write it at the top of your
  report and check it again at the end). Base: `git merge-base origin/main <head>`. Use
  `git diff <base>...<head> -- <paths>` and `git show <head>:<file>`.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario,
  the severity (**blocker / should-fix / nit**) and the fix. No praise, no summary. If unsure, say
  "plausible" and why.
- **No tool attribution** in what you write.

## What the PR must be (the owner's decisions)

Web and documents only (~106 files); nothing in `apps/api` or `packages/shared`; no dependency. The
prompt is `C:\Users\basel\.prompt\MASAHA_WORKER_A\PROMPT\S2B4A_PROMPT.md`, the approved plan
`PLAN\S2B4A_PLAN.md` with its reply `PROMPT\S2B4A_PLAN_REPLY.md` (Q1 (b), design issues 1–5,
stronger decisions 1–9); the worker's report `REPORT\S2B4A_REPORT.md` (read its departures). The
design: `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md` › A1, A2, Contacts, AD-012.
- **The editor's frame:** a page per space at the admin's route; its title the space's own name
  (#68's record-name rule, one place both the top bar and the document title read), the route's title
  while it loads; the section navigation (side list from `lg`, sticky chips below, the section in view
  marked).
- **Three sections, each saved, dated and confirmed alone:** «المساحة» (basics and location, one
  footer, one date, one confirm, saved by its changes alone), «المرافق» (common ticked + «مرافق
  إضافية», saved and confirmed together, «إدارة قائمة المرافق»), «التواصل» (the seven types, «هاتف»
  with its carrier derived from the prefix, the stored form as helper, refused on its own field).
  Hours, shifts, prices and photos are **absent** (later items), not "coming soon".
- **Every group:** «لم تُضف بعد» with Save only while never saved; else its date, «قديمة» when
  stale, the confirm; save always enabled; «تغييرات غير محفوظة» beside a dirty section.
- **«ما زال ناقصًا»:** heads a space with any missing group (all five listed), each line linking its
  section; gone once nothing is missing.
- **Leaving with unsaved changes asks first** (a link, Back, the switcher), naming the sections;
  closing or reloading the tab asks through the browser; saving or discarding clears it; jumping to a
  section never asks.
- **A verified space is read-only:** the Alert says «يعدّلها مالكها» with no owner name (finding 59),
  «عرض في الموقع» and the unlink's way.
- **Entry points:** «تعديل» in the list's row menu, the space's name a link; after a creation the add
  page lands on the new editor under the checklist (#57's D2 superseded, recorded).
- **Issue #70:** `PageHeader` never renders an empty heading, in its own commit.
- **Finding 60:** a space whose area was hidden since shows an empty area field; recorded, not fixed.

## Look at these, in this order

1. **Truth to the API.** Each section sends exactly the contract's request (`docs/api/api-contract.md`
   › *Spaces (the admin)*): the profile's `PATCH` with only the changed fields (why a whole resend
   would fail), each group's `PUT` whole, each confirm; 422 errors land on their fields (a contact on
   its row), 409 and 429 handled; a failure in one section leaves the others' state alone. The
   contacts' stored form and the carrier come from `@masaha/shared/spaces`, never a copy in the web.
2. **The leave guard.** Every way out is caught (links, Back, the space switcher, the browser's
   close/reload) and none that should not be (a section jump, a successful save's own navigation);
   cleared on save and discard; no stuck guard after an error or unmount; the router's blocker used
   as React Router intends.
3. **State and data.** Server state in TanStack Query under the admin's keys (frontend architecture
   §7), form state in the form; after a save or confirm the right queries refetch (the list, the
   editor) and the date shown is the server's; no stale form after a refetch; the read-only state
   cannot be bypassed in the UI (and the API refuses anyway).
4. **The record title.** One owner for the title; the space's name with its language marked; no empty
   heading anywhere (#70); the route's title while loading; nothing leaks to the next page.
5. **The design system and localisation.** No colour, font or CSS outside the design-system layer;
   semantic tokens only; no physical direction classes; every string in both catalogues; RTL/LTR
   correct for numbers, phones and Latin names; accessibility (labels, focus after save and error,
   the chips' current state announced, the Alert's links named).
6. **The tests.** Each would fail if its code broke (testing §3, rules 5–7); hooks tested as hooks,
   components as components; expectations by hand; the leave guard and the record title named by
   their breaks; the 429 test the worker changed ("Edit never waits by design") — is that the design?
7. **Scope and documents.** Nothing outside `apps/web` and the documents; `spaces.md` (*Web
   decisions*, *Web history*, code map, D6 superseding #57's D2), `lookups.md`,
   `frontend/architecture.md` (the record-name title), the overview's *Built* line, findings 59 and 60
   and the index — each true to the code, one home per fact.
8. **The commits:** six; count each subject's characters yourself (≤ 50, no exception).

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; then stop.

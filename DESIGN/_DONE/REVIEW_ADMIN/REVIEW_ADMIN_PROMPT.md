# Design review 2 — the admin's dashboard

**The design-review-admin worker** (a one-off reviewer, named after its task). **Read-only:** you
write nothing in the repository, run no git command that changes anything, and touch no worker's
folder.

**Size cap:** at most 2 subagents, no workflow; the whole review under 500,000 tokens.
**Report:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_ADMIN_REPORT.md`.
**Evidence images:** `C:\Users\basel\Downloads\design-review-admin\` (create it).

## 1. The task in brief

The second of six design reviews. The shared layer (shells, navigation, page-level patterns) is
reviewed and **decided**; this review takes **the admin's pages themselves**: what each page is for,
how it is divided into sections and components, its flows and states, and the better design for each.
The admin's space edit screen is the next to be built (S2b-4), so give it the most care.

## 2. Read first

1. **The lens:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REVIEW_LENS.md` — your method and the report's
   shape; follow it exactly.
2. **What is settled:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_SHARED.md`. Don't report it
   again (lens §2b).
3. `docs/design/README.md`, `docs/design/SCREENS.md` (admin rows 25–32), `docs/design/INDEX.md`,
   `docs/design/prototype/BRIEF.md`.
4. `docs/frontend/design-system/foundation.md` §5, §7–§10, §12, §13 (*Admin dashboard*);
   `docs/project/overview.md` (the admin's v1 scope); `docs/project/glossary.md`; the admin's part of
   `docs/api/api-contract.md` §5 (*Spaces (the admin)*, *Lookups (the admin)*, and the planned admin
   endpoints in `docs/plans/v1-mvp.md` › *Planned API surface*); ADRs 0007 (soft delete) and 0009.
5. The prototype's source: `masaha/admin.jsx`, `admin-data.js`, `profile-a.jsx`, `profile-b.jsx`,
   and the `Admin *.html` pages.

## 3. Your scope

The admin's eight screens (SCREENS.md rows 25–32) and their frames, board sections **42–49** and the
admin frames of **50–52**:
- **25 Overview**, **26 Spaces** with **add / edit an unverified space** and the verified read-only
  view (the edit is the long one-page form with a section per fact group: the most important page of
  this review), **27 Space owners** (linking and unlinking), **28 Data reports**, **29 Users** (with
  the temporary password), **30 Lookups**, **31 Audit log**, **32 Platform settings**.

**Three of them are already built in code** (the spaces list, the add form — in progress — and the
lookups): review the design anyway; say where the built screen already took a better choice, if you
know it from `docs/features/spaces.md`, `space-links.md` and `lookups.md` (read only their *Web
decisions*).

**Issue IDs:** `AD-001`, `AD-002`, …

## 4. How to look

- **Serve a copy, never the repository's folder:** extract the archive from `origin/main` to a short
  path and serve it on **port 5341**:
  `git archive origin/main docs/design | tar -x -C C:\Users\basel\design-review-admin` (create the
  folder), then serve `C:\Users\basel\design-review-admin\docs\design\prototype` on 5341.
- Every page in Arabic and English, light and dark, at 390, 768 and 1440, with the keyboard; evidence
  by headless Chrome (a script in your scratchpad, never committed).
- Read the source of each page, so a proposal names what really changes.
- At the end: stop the server, delete `C:\Users\basel\design-review-admin`, check port 5341 is free.

## 5. Risks

- **Writing anything** in the repository or in `masaha`, `masaha-b`: other workers are building there.
- **Reporting settled decisions** again, or the archive's known limits.
- **A proposal outside the design system** (a colour, size or font outside its tokens).
- **A design the API cannot serve** (lens §2c): a field the contract has not, a list it does not page.
- **Many small items, no big picture:** lead with the *Patterns* (admin-wide) and the space edit
  screen's structure.

## 6. When you finish

Save the report; summarise it here in ten lines at most: the five most important points, the counts
by level and impact, and the proposals for the space edit screen. Change nothing else.

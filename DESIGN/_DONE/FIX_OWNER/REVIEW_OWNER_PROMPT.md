# Design review 5 — the owner's management

**The design-review-owner worker** (a one-off reviewer, named after its task). **Read-only:** you
write nothing in the repository, run no git command that changes anything, and touch no worker's
folder.

**Size cap:** at most 1 subagent, no workflow; the whole review under 500,000 tokens. Two other
reviews and a building worker run beside you, so keep the load light.
**Report:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_OWNER_REPORT.md`.
**Evidence images:** `C:\Users\basel\Downloads\design-review-owner\` (create it).

## 1. The task in brief

The fifth of six design reviews. The shared layer, the admin's dashboard and the public site are
reviewed and **decided**. This review takes **the owner's management of their space**: what an owner
does away from the front desk to run their space and keep it true. Look at what each page is for, its
sections and components, its flows and states, and the better design for each. The owner's space
profile and prices are the next of these to be built (build step 5), so give them the most care.

## 2. Read first

1. **The lens:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REVIEW_LENS.md`. It sets your method and the
   report's shape; follow it exactly.
2. **What is settled:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_SHARED.md` (read its amended
   head), `DECISIONS_ADMIN.md` and `DECISIONS_PUBLIC.md`. Don't report any of it again (lens §2b).
   - The admin's space edit (A1, A2) is the same profile and facts the owner keeps. Where the owner's
     page should follow it or differ, say so and why: a verified space is edited by its owner, an
     unverified one by the admin.
3. The design's guides:
   - `docs/design/README.md`;
   - `docs/design/SCREENS.md`, owner rows 12 and 18–24;
   - `docs/design/INDEX.md`;
   - `docs/design/prototype/BRIEF.md`.
4. The product's documents:
   - `docs/frontend/design-system/foundation.md` §5, §7–§10, §12, §13 (*Owner and reception
     dashboard*);
   - `docs/project/overview.md` (the dashboard's v1 scope, what drops first, *Not in v1*);
     `docs/project/glossary.md`;
   - ADRs 0008 (live status), 0009 (roles at a space) and 0010 (the manual ledger);
   - `docs/architecture/data-model.md` › *Derived values*;
   - `docs/features/spaces.md` › *Behaviour and flows* (the fact groups, freshness, confirming);
   - `docs/plans/v1-mvp.md`, steps 5–9 and *Planned API surface* › the owner's rows.
5. The prototype's source: `masaha/owner.jsx`, `owner-data.js`, `profile-a.jsx`, `profile-b.jsx`,
   `finance.jsx`, and `Owner overview.html`, `Owner space profile.html`, `Packages.html`,
   `Staff.html`, `Announcements.html`, `Finance.html`, `Data reports.html`, `Owner settings.html`.

## 3. Your scope

The owner's screens and their frames:
- **12 Overview**;
- **18 Announcements**, with the closure extension (owner only);
- **19 Finance and statistics**;
- **20 Space profile**;
- **21 Prices and packages**;
- **22 Staff**;
- **23 Data reports**;
- **24 Settings**.

Board sections **29–30**, **33–40**, and the owner's variants of **41** and **49–52**. Reception's view
of a shared screen (announcements) is in scope as far as it differs.

The front desk, customers, subscriptions and payments are review 6's; don't review them here.

**Issue IDs:** `OW-001`, `OW-002`, …

## 4. How to look

- **Serve a copy, never the repository's folder.** Extract the archive from `origin/main` to a short
  path and serve it on **port 5344**:
  `git archive origin/main docs/design | tar -x -C C:\Users\basel\design-review-owner` (create the
  folder), then serve `C:\Users\basel\design-review-owner\docs\design\prototype` on 5344.
- Look at every page in Arabic and English, light and dark, at 390, 768 and 1440, and with the
  keyboard. Take evidence with headless Chrome (a script in your scratchpad, never committed).
- Read the source of each page, so a proposal names what really changes.
- At the end: stop the server, delete `C:\Users\basel\design-review-owner`, and check port 5344 is
  free.

## 5. Risks

- **Writing anything** in the repository or in `masaha` or `masaha-b`: other workers are building
  there.
- **Reporting settled decisions** again, or the archive's known limits.
- **A proposal outside the design system:** a colour, size or font outside its tokens.
- **A proposal against a product rule:**
  - live status shown as a count;
  - a payment edited rather than voided;
  - anything on the *Not in v1* list.
- **A design the API cannot serve** (lens §2c).
- **Many small items, no big picture:** lead with the *Patterns* (owner-wide), then the space
  profile's and the prices' structure.

## 6. When you finish

Save the report. Summarise it here in ten lines at most: the five most important points, the counts
by level and impact, and the proposals for the space profile and the prices. Change nothing else.

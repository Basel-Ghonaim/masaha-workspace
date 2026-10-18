# Design review 1 — the shared layer: shells, navigation and the patterns every page inherits

**The design-review-shared worker** (a one-off reviewer, named after its task). **Read-only:** you
write nothing in the repository, run no git command that changes anything, and touch no worker's
folder.

**Size cap:** at most 2 subagents, no workflow; the whole review under 600,000 tokens.
**Report:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_SHARED_REPORT.md`.
**Evidence images:** `C:\Users\basel\Downloads\design-review-shared\` (create it).

## 1. The task in brief

Masaha's screens were designed in Claude Design and archived in `docs/design/`; that tool is no
longer available, so the prototype will become the living design and be fixed and improved by hand.
This is the **first of six reviews**, and the one every other builds on: the parts **every page
inherits**. Find the defects, and above all find **the better design**: how each shell, each shared
component and each page-level pattern should be divided and behave so that every screen is clear,
easy and logical. Judge by the lens.

## 2. Read first

1. **The lens:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REVIEW_LENS.md` — your method and the report's
   shape. Follow it exactly.
2. `docs/design/README.md` (how to open the prototypes; *Known limits*), `docs/design/SCREENS.md`,
   `docs/design/INDEX.md`, `docs/design/prototype/BRIEF.md`.
3. `docs/frontend/design-system/foundation.md` — all of it (§2 principles, §5–§10, §12 inventory, §13
   the 32 screens); `docs/frontend/architecture.md` §2 (the page groups, the shells, `PageHeader`);
   `docs/project/overview.md`; `docs/project/glossary.md`; ADR 0008.
4. The prototype's source, not only its pictures (`docs/design/prototype/masaha/*.jsx`, `masaha.css`).

## 3. Your scope

**The shells and navigation**
- the public site's header, footer and account menu (`shared.jsx`: `SiteHeader`, `SiteFooter`,
  `UserMenu`), and the auth pages' shell (`auth.jsx`: `AuthShell`);
- the account area's shell (`account.jsx`);
- the dashboard's shells: the owner and reception's (`owner.jsx`: `OwnerShell`, `SpaceSwitcher`,
  `OwnerUserMenu`, `StatusControl`, `PublicStateBadge`) and the admin's (`admin.jsx`: `AdminShell`);
  the sidebar per role, the top bar, the phone drawer; **how each role finds its daily tasks**.

**The patterns every page uses** — judge each across all the pages that use it:
- the page header (title, breadcrumb, the page's actions) and the primary action's place;
- sections and cards on a page; how a long page is divided;
- forms: fields, bilingual pairs, optional marks, helpers, errors, the submit and its place; the
  sheet versus the page versus the dialog for a form;
- lists: table on desktop, cards on a phone; filters (`FilterSheet` and every other filter bar),
  search, pagination, the count;
- feedback: toasts (`PageToaster`), alerts, confirmations, undo;
- states: loading (`SpaceCardSkeleton` and the rest), empty, error, offline, "too many requests";
- shared display pieces: `SpaceCard`, `LiveStatus`, `SpacePrices`, `SpaceMeta`, `DateField`,
  `TimeInput`.

**The frames:** use `INDEX.md`. Above all sections 01 (*Flow*), 10 (*About & error pages*), 11–12
(*Variants*, *Variants — phone 390*), 14 (*Account — signed-in header*), 50–52 (*Dashboard variants*:
Arabic dark, English light, phone 390); and, for each pattern, the frames of the pages that use it.

**Not your scope:** a single page's own content (the next five reviews take them: the admin, the
public site, account and sign-in, the owner's management, the front desk). Note it in *Not reviewed*
if you see it, in one line.

**Issue IDs:** `SH-001`, `SH-002`, …

## 4. How to look

- **Serve a copy, never the repository's folder:** extract the archive from `origin/main` to a short
  path (Windows limits long paths) and serve it on **port 5340**:
  `git archive origin/main docs/design | tar -x -C C:\Users\basel\design-review` (create the folder),
  then serve `C:\Users\basel\design-review\docs\design\prototype` on 5340. Open
  `Flows - states.html` for the whole board, or any page with its state parameters.
- **Look at every pattern in Arabic and English, light and dark, at 390, 768 and 1440,** with the
  keyboard too. Capture evidence with headless Chrome (a script in your scratchpad, never committed).
- **Read the source** of each shared component, so a proposal names what really changes.
- **Stop the server** and delete `C:\Users\basel\design-review` at the end; check port 5340 is free.

## 5. Risks

- **Writing anything** in the repository, or in `masaha`, `masaha-b` — the other workers are
  building there. Read-only means read-only.
- **Reporting the archive's known limits** as defects (the lens §2).
- **Proposing a component that bypasses the design system,** or a colour, a size or a font outside
  its tokens.
- **Judging a page's content** that belongs to a later review: stay on what is shared.
- **Many small items, no big picture:** the *Patterns* section matters most; lead with it.

## 6. When you finish

Save the report; summarise it here in ten lines at most: the five most important points, the count
of issues by level and impact, and the patterns you propose. Don't change anything else.

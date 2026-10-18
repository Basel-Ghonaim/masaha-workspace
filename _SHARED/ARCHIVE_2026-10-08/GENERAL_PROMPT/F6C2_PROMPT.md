# F-6c2 — The dashboard shell

**Worker B** · folder `C:\Users\basel\masaha-b` · branch `feat/dashboard-shell`

**Size cap:** use at most 4 subagents in total. Do not run any workflow.

## 1. How to work

- **Start with the `start-work-item` skill.** The worktree is ready: detached at `origin/main` (412b90f), dependencies installed, the database migrated.
- **The owning documents:**
  - `docs/frontend/architecture.md` (§1 folders by role; §2 the page groups, the layout tree, *Landing and guards*; §3 the feature rules H1–H8 and the capability table; §7);
  - ADR 0011 and ADR 0016;
  - `docs/development/testing.md` (*A feature, layer by layer*);
  - `docs/frontend/design-system/foundation.md` (§9 layout, §12 the Sidebar);
  - `docs/frontend/localisation.md`.
- **The designs:**
  - SCREENS.md (the dashboard rows);
  - `docs/design/screens/29-owner-overview-kept/`, `21-front-desk-reception-vs-owner/`, `42-admin-overview/`, and the `50`–`52` dashboard variants (Arabic dark, English LTR light, phone 390).

  They define the sidebar, its header, the top bar and each role's navigation.
- **When finished, follow the `open-pr` skill.**
- **The owner's rules:**
  - every test's title states what it asserts;
  - the lockfile rule;
  - **report only once CI is green on the pushed head**;
  - review fixes are folded into the commits they correct, and a genuinely new unit gets new commits; ONE "Review fixes" comment;
  - **no production code exists only for a test:** no parameter, option or callback that only tests pass or that nothing uses. Tests stub the platform's own seams (`fakeTransport` / `fakeAdapter`, `vi.stubGlobal`);
  - **guards own navigation; pages pass no navigating callbacks;**
  - **run the checks one at a time** (the machine ran out of memory before). The per-commit check is still required.

## 2. What this item delivers

The dashboard shell on top of F-6c1's foundation (`GET /manage/spaces`, `useMySpacesQuery`, `RequireSpaceRole`, `landingPath`, `rememberSpace`, `dashboardPaths`).

### Decided (do not reopen)

**Structure (architecture.md §2, ADR 0016):**
- `pages/dashboard/` holds:
  - `index.ts`: the route subtree, the group's only export, loaded lazily as a whole;
  - `shell/`: the layout, the sidebar, the top bar;
  - `navigation.ts`: each role's items, and the roles each item allows;
  - `admin/` and `space/`.
- **The two branches:** `/dashboard/admin/…` under `RequireRole(['ADMIN'])`, and `/dashboard/spaces/:spaceId/…`. Each space route is visibly wrapped in `RequireSpaceRole`, with its item's roles.
- **The selected space is the URL's `:spaceId`,** never client state. The switcher only navigates.
- **Capabilities stay role-agnostic:** the page passes scope.

**The shell:**
- **The sidebar,** in the design system's `Sidebar` form for each width: expanded from `lg`, an icon rail from `md`, a start-side Sheet on a phone.
  - **Its header:** the space switcher for a space; the admin's fixed header for the platform.
  - **Its foot:** "View the public page", built from the space's `slug` (L8).
  - **Item counts** (like the data-reports badge) are deferred to step 10. Don't build a count prop now: nothing would pass it.
- **The top bar:** the page's title, **a slot the page fills** (L7), the language and theme toggles (wired as in the site shell), and the account.
- **N5 — the account:** the `users` capability's account menu, in a compact form (the avatar only, as the design draws). `features/users` exports it as a variant of its own UI (H3: one unit per file).

**Behaviour:**
- **N6 — `/dashboard`:** redirects through `landingPath`. A plain user with no role and no links goes to `/`.
- **Remembering the space:** entering a space's routes calls `rememberSpace` (L2). The space branch's element does it, not a page callback.
- **L5 — the landing's owner:** `RequireGuest` now uses `landingPath`, replacing `safeReturnUrl`. After signing in, an admin, an owner or reception lands in their dashboard (or on a safe `next`).
- **L4 — "Dashboard" in the account menu,** for an `ADMIN` or a user with active links. It goes to `/dashboard`.
- **K4 holds:**
  - an invalid `:spaceId` → the 404 state;
  - no link at that space → the 403 state;
  - both inside the dashboard shell.

**Capabilities and pages:**
- **N1 — `space-links` is dashboard-only.** Add its row to architecture.md §3's capability table, under "The dashboard only" (F-6c1 left this to you).
- **N2 — the switcher's UI:** `SpaceSwitcher` lives in `features/space-links/components/`, and the feature exports it. The shell places it. It shows the space's name and area. For more than one active link it opens a list, and choosing a space navigates.
- **N3 — placeholder pages:** **one** placeholder component that renders its item's title from the navigation config. No 23 near-identical files. Each real page replaces its entry later (L6: the title only, no invented text).
- **N4 — payments:** two routes, two screens.
  - `payments` is `OWNER`: the ledger;
  - `my-payments` is `RECEPTION`: "My payments today".
- **The navigation per role,** from the designs:
  - the owner's 11 items;
  - reception's 4 (desk, customers, my payments today, announcements);
  - the admin's 8.

  The owner's audit screen is not in the navigation (finding 14).

**The boundary (ADR 0011):**
- **The dashboard-only lint:** `pages/site` never imports a dashboard-only capability (§3's list). Lint enforces it, with probe tests that refuse and allow.
- **N7 — proof in the build:** extend `check:build`, so it fails if the site's initial download includes dashboard code. Read the build manifest: the site's entry chunk and its static imports must not reach `pages/dashboard` or a dashboard-only capability.

### Your plan decides

- the files inside `pages/dashboard/shell/`;
- how the navigation config is typed;
- how the placeholder takes its title;
- the switcher's loading and error states (the design system's `Skeleton`; a retry);
- the admin header's content, from the design;
- the exact lint mechanism, and the manifest check.

## 3. Tests (testing.md, layer by layer)

- **`SpaceSwitcher`:** its rendering states (one space, several, loading, error). Choosing a space navigates (through the real path; no injection).
- **The compact account menu:** rendering, and the "Dashboard" item for an admin or a linked user only.
- **Routes,** with test routes or the real dashboard routes:
  - each role sees only its navigation;
  - reception is refused (403) on an owner-only route such as `payments`, and allowed on `my-payments`;
  - `/dashboard` redirects per role, and a plain user goes to `/`;
  - entering a space remembers it;
  - an invalid or unlinked `:spaceId` shows 404 or 403 inside the shell;
  - **after signing in, `RequireGuest` lands each role in its dashboard,** or on a safe `next`.
- **Lint probes** for the dashboard-only rule.
- **The build check** fails on a deliberate dashboard import from the site (prove it once, revert).

**Screenshots** (`C:\Users\basel\Downloads\f6c2-shots`, never committed):
- the shell for the owner, reception and the admin;
- the switcher open;
- the phone sheet;
- in RTL and LTR, light and dark, phone and desktop.

Sign in with the seeded demo accounts. This folder's API runs on **3321** (`.env`); Vite's proxy targets 3320. So for the browser check, start the web with the proxy pointing at 3321 **without committing that change**, or ask the owner.

## 4. Out of scope

- Any real dashboard screen.
- The account settings page.
- Item counts.
- The owner's audit screen.
- Any API change.
- The storage layer (Issue #37).

## 5. Parallel work

**Worker A** works in `C:\Users\basel\masaha` on **F-5b3c1**:
- the forced-change gate in `app/RootLayout.tsx`;
- `RequirePasswordChange` and new paths in `shared/routing`;
- `features/users` (it extracts `useSignOutAction` from `useAccount`, and adds `SignOutButton` and the forced-change form);
- a `FocusLayout` `actions` prop;
- architecture.md §2–§4.

**Your rules for this:**
- **Expect conflicts** in `app/RootLayout.tsx`, `app/router.tsx`, `shared/routing/index.ts`, `features/users/` (index and the account menu), `pages/site/routes.tsx` and architecture.md §2–§3. Declare them in the plan, keep to your lines, and **resolve by keeping both sides** when you rebase.
- **If A merges first,** build your compact account menu and the "Dashboard" item on A's `useSignOutAction`, not on the old `useAccount` shape.

## 6. Commits and PR

- **Commits:** propose the split in the plan. Atomic, Conventional, subjects of 50 characters or fewer.
- **Labels:** `feat`, `area:web`, `area:docs`.
- **Review:** the review gate, with two independent reviews. This item adds the dashboard boundary and changes where every role lands. After CI is green, stop and report.
- **The Arabic** for any line not in a design is listed for the owner's approval.
- No tool or AI attribution anywhere. Don't merge. Don't create an Issue.

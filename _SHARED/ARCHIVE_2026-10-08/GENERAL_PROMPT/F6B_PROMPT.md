# F-6b — The layout tree and the site shell

**Worker B** · folder `C:\Users\basel\masaha-b` · branch `feat/site-shell`

**Size cap:** use at most 4 subagents in total. Do not run any workflow.

## 1. How to work

- **Start with the `start-work-item` skill.** Worker B: the worktree must be detached at `origin/main` after `git fetch --prune origin`.
- **The owning documents for this item:**
  - `docs/frontend/architecture.md` (§1–§3);
  - ADR 0011 (one web app, two domains) and ADR 0016 (dashboard URLs);
  - `docs/frontend/design-system/foundation.md` §9 (layout) and §12 (components);
  - `docs/frontend/localisation.md`.
- **The designs:**
  - `docs/design/SCREENS.md`, row 8 and the public-site rows;
  - the screens in `docs/design/screens/10-about-error-pages/`, `11-variants/` (404, general error, offline, home) and `12-variants-phone-390/`;
  - the prototypes `docs/design/prototype/Error.html` and `Home.html`, for the header and footer.
- **When finished, follow the `open-pr` skill.**
- **Rules the skills don't carry yet:**
  - every test's title states something the test actually asserts;
  - on a lockfile conflict, take main's `package-lock.json` and run `npm install`;
  - keep exactly ONE "Review fixes" comment on the PR, edited in later rounds.

## 2. Context

The web app has two domains, the **site** and the **dashboard** (ADR 0011). This item settles the **whole layout tree** for both, so the structure is decided once, and builds the first branch of it: the site shell with its header and footer, the placeholder pages, and the not-found, error and offline states.

The rest of the old F-6 becomes **F-6c**: the dashboard shells (sidebar, top bar, space switcher), the landing after sign-in, and the dashboard-only lint rule.

## 3. Decisions already made (do not reopen)

The owner approved these.

### L. The layout tree (the structure; write it into architecture.md §2)

```
RootLayout (app)                 ScrollRestoration; a last-resort error state with no shell
├── site
│   ├── SiteLayout               full header + footer
│   │   ├── public/*             home, directory, space details, about, the site's 404
│   │   └── AccountLayout        + the account's side navigation
│   │       └── account/*        favourites, my reports, settings
│   └── FocusLayout              short header (logo, language, theme), no footer
│       └── auth/*               sign in, register, forgot/reset password, the forced change
│                                (the forced change's short header: logo and sign out)
└── dashboard
    └── DashboardLayout          sidebar + top bar (ADR 0016)
        ├── admin/*
        └── spaces/:spaceId/*
```

Each level adds one thing around its `<Outlet/>`. Each domain owns its own shell, and places the status states inside it.

### L1. Two page groups, one per domain

`pages/site` and `pages/dashboard`, replacing the earlier `public`, `auth` and `account` groups. They are symmetric:

```
apps/web/src/
  app/
    router.tsx        RootLayout + siteRoutes + dashboardRoutes (F-6c) + showcase (development only)
    RootLayout.tsx
  pages/
    site/
      index.ts        siteRoutes: the group's only export
      shell/          SiteLayout, SiteHeader, SiteFooter, SiteMenu (phone); FocusLayout later
      navigation.ts   the site's links: configuration, no logic
      public/         home/, directory/, about/ (placeholders now)
      auth/           (F-5b3)
      account/        AccountLayout and its screens (later)
    dashboard/        (F-6c), as architecture.md §2 already lays it out:
      index.ts, shell/, navigation.ts, admin/, space/
    showcase/         unchanged
  shared/routing/     the status states now; the guards later (F-5b2)
```

- The dashboard-only rule becomes simpler: `pages/site` never imports a dashboard-only capability. Its lint comes with F-6c.
- **Build only what has a consumer.** `FocusLayout` is built with the auth screens (F-5b3), `AccountLayout` with the first account screen, and `DashboardLayout` in F-6c. All three are **documented now** in §2, and none is built here.

### L2. The toggles

- **Their visual controls** are the design-system layer's `LanguageToggle` and `ThemeToggle`.
- **Wiring:** each shell wires them to `shared/preferences` itself, in a line or two. There is no shared "connected toggle" component: `shared/preferences` stays without UI, and the site and the dashboard can't import each other.
- **The theme toggle** sets the opposite of the theme shown (architecture §4).

### L3. Lazy loading

- **A group's `index.ts`** exports route definitions only, and their components load through React Router's `lazy`, so a visitor never downloads dashboard code.
- **Each site page** loads lazily on its own.

### S1. The status states live in `shared/routing`

- They are route-level elements: `NotFoundState`, `RouteErrorState`, and a pure `classifyRouteError`.
- They take their actions as props (the site's 404 offers "Home" and "Browse spaces"; the dashboard's will offer its own).
- Each domain renders them inside its own shell. They compose the layer's `EmptyState`.

### S2. The sign-in button

It is shown as the design has it and links to `/login`. Until F-5b3 builds that route, it shows the site's 404. That is acceptable: nothing is deployed before sign-in works (F-7).

### S3. Offline

- `RouteErrorState` uses `classifyRouteError` to choose the state. A failed lazy chunk load, or `navigator.onLine === false`, shows **offline**; anything else shows the **general error**.
- **Retrying:**
  - "Retry" reloads the route, and the browser's `online` event retries automatically;
  - after F-5b1 merges, an `AppError` of type `network` will become a third cause. Don't depend on it here.

### S4. The placeholder pages

Home, the directory and about show only their page title, from the catalogue: the same words as their navigation link. Invent no other text; step 3 builds their content.

### S5. The routes

| Route | Page |
|---|---|
| `/` | home (placeholder) |
| `/spaces` | directory (placeholder) |
| `/about` | about (placeholder), with a `#contact` anchor for the footer's "Contact us" link |
| `*` | the site's 404, inside the site shell |
| any route error | the general error or offline state, inside the site shell |

### S6. The copy

- **The Arabic and English** come from the designs as they are (the header, the footer, the three states). The designs approved them.
- **Any line not in a design** (for example an `aria-label` for the phone menu) is listed in the PR for the owner's approval.
- **New catalogue sections** go in their own files (for example `site.ts` and `status.ts`). Never edit `errors.ts`: it is worker A's.

## 4. What to build

- **`RootLayout`:** `ScrollRestoration`, `<Outlet/>`, and the root `errorElement`, which shows the error state with no shell (the last resort, if a shell itself fails). No toaster yet: the first toast's item mounts it.
- **The site shell:**
  - **the header on desktop:** the logo (link home), Home, Spaces, About, the language toggle, the theme toggle, and the sign-in button;
  - **the header on a phone:** the menu button, the logo and the theme toggle. The menu (a layer `Sheet`, opened from the start side) holds the links, the language toggle and sign-in;
  - **the footer:** the tagline, About, and Contact us (`/about#contact`).
  - Follow the designs at 360/390 and 1440, RTL and LTR, light and dark.
- **The status states:** the 404, the general error and offline, as the designs show them, with their actions.
- **The router:**
  - the site group mounted under `RootLayout`;
  - `*` inside the site shell;
  - the site's `errorElement` on `SiteLayout`;
  - the showcase still added only in development.

## 5. Tests

**The component lane:**
- **the layout:** it renders the header, the outlet and the footer; the links point where §S5 says; the current link carries `aria-current="page"`;
- **the language toggle:** it changes the language, and `<html>`'s `lang` and `dir` follow;
- **the theme toggle:** it sets `data-theme` to the opposite of the theme shown;
- **the phone menu:** it opens, shows the links, language and sign-in, and closes when a link is chosen;
- **the routing:**
  - an unknown path shows the 404 inside the site shell, with its two actions;
  - a route that throws shows the general error;
  - a failed lazy load, or `navigator.onLine === false`, shows offline;
  - Retry reloads the route.

**The unit lane:** `classifyRouteError`, one case per cause.

**Already guarded:** catalogue parity, `check:classes`, and `check:build` (the showcase stays out of the build).

**Screenshots:** the three states, the header and the footer, and the phone menu open. RTL and LTR, light and dark, phone and desktop. Save them to `C:\Users\basel\Downloads\f6b-shots`, and never commit them.

## 6. Documents

- **`docs/frontend/architecture.md`:**
  - **§2, rewritten for L1:**
    - the groups table becomes `site` (with its areas public, auth and account, and their guards per route), `dashboard` and `showcase`;
    - the layout tree of §3 L goes in, with which levels are built and which are not;
    - add L2 and L3, and the status states in `shared/routing` (S1);
  - **§3:** the dashboard-only rule names `pages/site` (its lint still to come, F-6c);
  - **the status line:** the site shell and the status states are built.
- **`docs/plans/foundation.md`:** the F-6 entry records the split, dated, as the F-5 split was: F-6a (built), F-6b (this) and F-6c (the dashboard shells, the landing and switcher, the dashboard-only lint, the account's profile and settings in the `users` capability).
- **Not touched:** ADR 0011. §2 owns its operative rules, and the decision itself is unchanged.

## 7. Contract

**Acceptance criteria**
- [ ] architecture.md §2 holds the whole layout tree and the two-group structure; built and not-built parts are marked truthfully.
- [ ] `pages/site` exists as in L1, exporting only `siteRoutes`; its pages load lazily.
- [ ] The site shell matches the designs on phone and desktop, RTL and LTR, light and dark.
- [ ] The 404, general error and offline states render inside the site shell, from `shared/routing`; offline is chosen by `classifyRouteError`.
- [ ] The toggles change the language and the theme through `shared/preferences`.
- [ ] Every new string is in both catalogues; lines not from a design are listed for approval.
- [ ] No dependency is added.

**Out of scope**
- `FocusLayout`, `AccountLayout`, `DashboardLayout` and any dashboard code (documented only).
- The session, the account menu, the guards, and any auth screen.
- The real content of home, the directory and about (step 3).
- A toaster, the request id in the error state (it comes after F-5b1), and the dashboard-only lint (F-6c).

## 8. Parallel work

**Worker A** is working in `C:\Users\basel\masaha` on F-5b1 (`feat/web-transport`): the transport, `AppError` and TanStack Query.

- **Worker A's files. Do not touch them:**
  - `shared/api/**`, `shared/errors/**`, `src/test/fakeAdapter.ts`;
  - `app/bootstrap.ts`, `app/providers.tsx` and its test;
  - `vite.config.ts`, `eslint.config.js`, `apps/web/package.json`, everything in `apps/api`;
  - the copy files `english/errors.ts` and `arabic/errors.ts`;
  - `docs/development/setup.md`, `CLAUDE.md`.
- **Shared files.** Declare them in the plan, and keep to your section:
  - `app/router.tsx`: yours; A doesn't touch it;
  - the copy catalogues: your new section files, and their registration in `index.ts` / `shape.ts`;
  - `docs/frontend/architecture.md`: you own §2, §3 and the site-shell part of the status line; A owns §5, §7 and its part of the status line;
  - `docs/plans/foundation.md`: you edit only the F-6 entry; A edits the F-5b entry;
  - `docs/architecture/findings.md`: append only, if you record anything.
- **Dependencies:** you add none, so `package-lock.json` must not change.
- **Rebasing:** before the PR, fetch and rebase on `origin/main`. Whoever merges second rebases again and keeps both sides. The status line of architecture.md will likely conflict: keep both parts.

## 9. Commits

Propose the split in the plan. A likely one:
1. `docs(plans): split the rest of f-6 into f-6b and f-6c`
2. `docs(architecture): set the layout tree of the site and the dashboard`: §2 and §3
3. `feat(site): add the site shell`: RootLayout, the router, `pages/site`, the toggles, the placeholders, their copy
4. `feat(routing): add the not-found, error and offline states`: `shared/routing`, its copy, the error elements

## 10. Pull request

- **Labels:** `feat`, `area:web`, `area:docs`.
- **Review:** one independent review. After opening the PR, stop and report.
- **No tool or AI attribution** anywhere. Don't merge. Don't create an Issue.

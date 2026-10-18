# F-6c1 — My spaces, the space guard and the landing rule

**Worker B** · folder `C:\Users\basel\masaha-b` · branch `feat/my-spaces`

**Size cap:** use at most 4 subagents in total. Do not run any workflow.

## 1. How to work

- **Start with the `start-work-item` skill.**
- **The owning documents for this item:**
  - `docs/backend/conventions.md` §2, §7 (levels, the module table), §8 (R1, R2, R4) and §9 (*Composed reads*);
  - `docs/api/api-contract.md` §1–§5;
  - `docs/architecture/data-model.md` (bilingual pairs, soft delete);
  - `docs/architecture/shared-package.md`;
  - `docs/frontend/architecture.md` §1–§3 and §7;
  - ADR 0009 and ADR 0016;
  - `docs/architecture/findings.md`, finding 18.
- **Read the code you build on:**
  - `apps/api/src/modules/space-links/`, `users/` and `auth/`, and `app.ts`;
  - `apps/web/src/shared/session/`, `shared/routing/`, `shared/api/`;
  - the seed's demo data (`apps/api/src/db/seed/`).
- **When finished, follow the `open-pr` skill.**
- **The owner's rules the skills don't carry yet:**
  - every test's title states what it asserts;
  - on a lockfile conflict, take main's `package-lock.json` and run `npm install`;
  - **report only once CI is green on the pushed head**;
  - **review fixes are folded into the commits they correct** (fixup + autosquash, `--force-with-lease`), with ONE "Review fixes" comment;
  - a genuinely new unit of work gets new commits.
- **Your environment is ready** (see §4, *Your environment*). If the API doesn't start, stop and tell the owner. Don't edit `.env` yourself.

## 2. Context

F-6c, the dashboard shells, is split in two:
- **F-6c1 (this item):** the foundation:
  - the endpoint listing the caller's spaces;
  - the web's `space-links` capability that reads it;
  - the space-role guard;
  - the full landing rule.
- **F-6c2 (later):** the shell, the sidebar, the top bar, the switcher, the placeholder pages, the dashboard-only lint, and wiring the landing into the sign-in pages.

Nothing in F-6c1 is visible to a user yet. The guard and the landing rule are built and tested, and F-6c2 is their first user. Say so in the PR.

**The account settings page** (SCREENS row 9) is no longer part of F-6. It needs `GET`/`PATCH /me` on the API, and becomes its own later item. Record that in the plan's F-6 entry.

## 3. Decisions already made (do not reopen)

The owner approved these.

### The endpoint — `GET /manage/spaces`

- **Who may call it:** any signed-in user. It answers with the spaces the caller holds an **active** link to, with the caller's role at each.
- **It never reveals another user's spaces.**
- **Mounting:** under `requireAuth` only. There is no `:spaceId`, so no space middleware. Mount it at `/manage/spaces`, where the API contract already plans it.
- **Each item:** `spaceId`, `role` (`OWNER` | `RECEPTION`), `slug`, `nameAr`, `nameEn`, and the area's `nameAr` / `nameEn`.
- **Order:** oldest link first, as the session's links are.
- **K2 — bilingual fields:** `nameAr` / `nameEn`, as data-model's bilingual pairs, and as every admin endpoint will be.
- **K3 — which spaces:**
  - soft-deleted spaces are left out: the spaces repository filters them by default;
  - hidden spaces are included: an owner still manages a hidden space;
  - finding 18 (a link to a deleted space still opens the dashboard) stays open.
- **The layers** (conventions §7–§9):
  - **`spaces` (L1), a new module:** only what this needs, a set-based read of space summaries by ids (names, slug, area id). No router.
  - **`lookups` (L0), a new module:** only area names by ids. No router.
  - **`space-links` (L2):** `mySpaces(userId)` composes its active links, `spaces`' summaries and `lookups`' area names. Set-based: one query per module, no N+1. It is its `me`-audience router, mounted at the contract's path.
  - Each module exports through its `index.ts` (R2), and the level rule must pass.
- **The response type** lives in `packages/shared/src/space-links/responses.ts` (for example `ManagedSpace`), exported from `space-links/index.ts`. The mapper returns that type.
- **`api-contract.md`:** the endpoint's entry, built.

### The web — `features/space-links` (K1)

```
features/space-links/
  index.ts                             useMySpacesQuery (the only export for now)
  repository/spaceLinksRepository.ts   SpaceLinksRepository { mySpaces } + createSpaceLinksRepository(client = api)
  hooks/useMySpacesQuery.ts
  hooks/queryKeys.ts                   ['me', 'spaces']
```
- **The structure:** the agreed feature structure (`repository/`, `hooks/`, `components/`, `services/`, `types/`, absent when empty; one exported unit per file). Worker A is writing it into architecture.md §3 in PR #35.
- **The export:** the hook is exported because a higher layer (F-6c2's shell) composes it with its own layout.
- **The switcher component comes in F-6c2.**

### The guard — `shared/routing/guards/RequireSpaceRole.tsx`

- **Its question:** the user's role **at the space in the URL** (`:spaceId`), from the session's links. Never the global role (ADR 0009).
- **Props:** the roles the route allows, for example `['OWNER']` or `['OWNER', 'RECEPTION']`.
- **Its behaviour,** with the existing guards' states (spinner while restoring, `RetryState` when unreachable, sign-in with `next` for a guest):
  - **K4:** a `:spaceId` that isn't a positive integer → the 404 state (`NotFoundState`);
  - **K4:** a valid id the user holds no active link to → the 403 state (`ForbiddenState`);
  - a link with a role the route doesn't allow → the 403 state;
  - allowed → the children.
- **It never redirects silently** (ADR 0016).

### The landing rule — `shared/routing/landing/`

**K5:** the dashboard's URL shape lives in `shared/routing`, because the landing rule needs it and can't import `pages/` (ADR 0016 fixes the shape). Put it in `dashboardPaths.ts`:
- `/dashboard/admin`;
- `/dashboard/spaces/:spaceId`;
- `/dashboard/spaces/:spaceId/desk`.

**`landingPath.ts`** decides where a signed-in user lands (architecture.md §2 › *Landing*):
1. a safe return URL (`next`, via the existing `safeReturnUrl`), when there is one;
2. otherwise, **K6:**
   - an `ADMIN` → `/dashboard/admin`;
   - a user with links → the last space they used (`lastSpace.ts`), else their oldest active link. The page follows the link's role there: an `OWNER` lands on the space's overview, `/dashboard/spaces/:id`; a `RECEPTION` lands on the desk, `/dashboard/spaces/:id/desk`;
   - a user with no role and no links → `/`.

**`lastSpace.ts`:**
- remembers the last space per user in `localStorage`, under a key that names the user;
- on read, it returns the space only if the user still holds an active link to it;
- every storage access is wrapped in try/catch: storage may be unavailable;
- it offers `rememberSpace(userId, spaceId)` and the read the landing uses. F-6c2's space branch calls `rememberSpace`.

**Not here:** the sign-in pages keep their current landing until F-6c2 switches them to `landingPath`. They are worker A's files in PR #35.

## 4. Tests

**The API lane:**
- the caller sees only their active links' spaces, with the right roles, names and area names;
- a deactivated link is left out;
- a soft-deleted space is left out, and a hidden one is included;
- another user's spaces never appear;
- the order is oldest link first;
- a guest gets 401;
- an ADMIN with no links gets an empty list.

**The unit lane:**
- `spaces` and `lookups`' reads, with fakes;
- the mapper;
- `landingPath`, every branch: `next` wins; an unsafe `next` is ignored; an ADMIN; an OWNER lands on the overview; a RECEPTION lands on the desk; the last space vs the oldest link; a remembered space whose link is gone falls back to the oldest; a user with nothing goes to `/`;
- `lastSpace`: per-user keys; storage throwing is harmless.

**The component lane:**
- `RequireSpaceRole` with test routes:
  - an owner allowed;
  - reception allowed on a both-roles route and refused (403) on an owner-only route;
  - a valid id not in the links gives 403;
  - a non-integer id gives 404;
  - a guest is sent to sign-in with `next`;
  - restoring and unreachable states;
- `useMySpacesQuery` through the real path (`fakeAdapter`).

**Your environment (prepared by the owner):**
- this folder's `apps/api/.env` runs the API on **3321**, with `CORS_ORIGIN=http://localhost:5321`, so it never collides with worker A's 3320/5320;
- `masaha_b_dev` is migrated and seeded with the demo data (`SEED_DEMO=true`; the demo accounts' password is `SEED_DEMO_PASSWORD` in that `.env`).

Vite's proxy target is fixed at 3320 (worker A's API). So for your manual check, call your API **directly** on `http://localhost:3321`, with the access token from `POST /api/v1/auth/login`. Don't edit `vite.config.ts` or `.env`.

**The manual check,** in the Evidence: with the seeded demo data, call `GET /api/v1/manage/spaces` on 3321 as:
- the demo owner;
- the reception account;
- the admin;
- an anonymous caller.

## 5. Documents

- **`api-contract.md`:** the endpoint.
- **`architecture.md` §2:**
  - *Landing and guards*: the space guard and the landing rule are built, with no route using them yet (F-6c2);
  - the dashboard URL shape now lives in `shared/routing`.
- **`docs/plans/foundation.md`, the F-6 entry:**
  - F-6c is split into F-6c1 (this) and F-6c2;
  - the account settings page moves out to its own later item, with `GET`/`PATCH /me`.
- **`conventions.md`:** only if the module table's "Owns / Holds" text for `spaces` or `lookups` needs a word of truth: they are built minimally.

## 6. Parallel work

**Worker A** is reworking PR #35 (F-5b3a) in `C:\Users\basel\masaha`:
- `features/auth`;
- `features/users` (the account menu);
- `shared/forms`;
- `shared/session` (renaming `gateway/` to `repository/`);
- the sign-in pages;
- architecture.md §3 and §4.

**Rules for you:**
- **Don't touch** any of those.
- **Shared files, declared in the plan, each kept to your section:**
  - `architecture.md`: you edit §2;
  - `foundation.md`: you edit the F-6 entry, A edits the F-5b3 entry (adjacent: expect a conflict, keep both);
  - `shared/routing/index.ts`: your export lines;
  - copy catalogues, if you add a line.
- **If A merges first,** rebase and keep both sides. Your session imports may need the renamed `repository/` paths.
- **No new dependency.**

## 7. Commits

Propose the split in the plan. A likely one:
1. `docs(plans): split f-6c and move account settings out`
2. `feat(space-links): list the caller's spaces`: the API (spaces, lookups, space-links), the shared type, the contract, tests
3. `feat(space-links): read my spaces on the web`: the feature, tests
4. `feat(routing): add the space-role guard`: tests, architecture.md §2
5. `feat(routing): add the landing rule`: `dashboardPaths`, `landingPath`, `lastSpace`, tests

## 8. Pull request

- **Labels:** `feat`, `area:api`, `area:web`, `area:docs`.
- **The review gate:** two independent reviews. This item decides who sees which spaces and who may open a space's pages. After CI is green, stop and report. Don't start fixes until the owner sends the list.
- No tool or AI attribution anywhere. Don't merge. Don't create an Issue.

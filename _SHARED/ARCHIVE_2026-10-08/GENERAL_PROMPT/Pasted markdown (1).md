# Migration path to the four-zone structure

Nothing implemented. This is the route, sized against the real tree — **169 files under** **`modules/auth/`**, 9 stories, 16 CSS modules.

---

## 0 · The discipline that makes this safe

Three rules govern every Work Item below. They are what let you restructure 169 files without a single behavioural risk.

**1. A move is a move.** `git mv` only. Never a delete paired with an add — [ADR 0013's migration invariant](vscode-webview://1agot9io9rs6ljvkigtguglga2t21kjilju91bd82qq5iljv3l98/docs/architecture/decisions/0013-applications-and-cross-tier-packages.md) requires history to survive, and `git log --follow` is the check. **No commit both moves a file and changes it.** If a file must change to land somewhere, that's a second commit, or a different Work Item.

**2. The counts are the proof.** A pure move changes nothing observable, so:

> **web unit** **`53 files / 208 tests`** **· storybook** **`24 files / 222 tests`** **— identical before and after, every Work Item.**

A count that moves means something wasn't a move. This is cheap, exact, and bites — it's the mutation-style proof the project already uses.

**3. Shim the barrel, move once.** `modules/auth/index.ts` stays as a re-export shim through Phases 2–3, so `app/` is touched **exactly once** (WI-8) instead of eight times. Same for the `@modules` alias — it lives until the end.

---

## 1 · Two things must happen before any file moves

**WI-0 · The ADR.** Going from three zones to four, and moving the route-subtree rule from the feature to the page group, is *"a new direction"* — [Strategy §8](vscode-webview://1agot9io9rs6ljvkigtguglga2t21kjilju91bd82qq5iljv3l98/docs/architecture/documentation-strategy.md) requires an ADR in either phase, and [§11.3](vscode-webview://1agot9io9rs6ljvkigtguglga2t21kjilju91bd82qq5iljv3l98/docs/architecture/documentation-strategy.md) makes it architectural. This is not ceremony: it's the instrument that makes the restructure authorized rather than drift.

It records the four zones and their direction; that a page group exports a route subtree and a feature does not; that a feature owns interaction UI but never layout; that **a page composes and owns no fact**; that `entities/` is declined, with RTK Query's cache named as the reason; and that `widgets/` is deferred.

**To be clear on your earlier ruling:** this is *decision* documentation, not documentation catching up. The *descriptive* documents — `architecture.md`, `authentication.md`, the platform index — stay untouched until **WI-10**, exactly as you said.

**The plan itself.** Per [ADR 0006](vscode-webview://1agot9io9rs6ljvkigtguglga2t21kjilju91bd82qq5iljv3l98/docs/architecture/decisions/0006-execution-plans-home-and-lifecycle.md), a plan is drafted **outside the tracked tree** (`.project/`) and enters `docs/plans/` **in the first branch of its first Work Item** — never on a branch of its own.

---

## 2 · Order, and why this order

**Capabilities out first, composition second.** Extract the capabilities and *what remains in* *`modules/auth/`* *is exactly the page material* — it identifies itself rather than being guessed at. Doing it the other way means deciding what a page is before you know what's left.

svg

```
Phase 0  decide        WI-0
Phase 1  scaffold      WI-1                    config only, zero moves
Phase 2  capabilities  WI-2 … WI-5             ~118 files, the bulk, purely mechanical
Phase 3  composition   WI-6 … WI-7             ~40 files
Phase 4  close         WI-8 … WI-10            cutover, enforcement, docs

```

---

## 3 · The Work Items

| WIScopeFilesNotes |                                                                                                                          |      |                                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------ | ---- | ----------------------------------------------------------------------------------------------------------- |
| **0**             | **ADR — four zones**                                                                                                     | 1    | Own branch/PR. Gates everything below.                                                                      |
| **1**             | Add `@features` + `@pages` aliases; **keep ****`@modules`** (`tsconfig.json`, `vite.config.ts`)                          | 2    | Zero moves. Carries the plan into `docs/plans/` as its first commit.                                        |
| **2**             | `modules/auth/session/` → `features/session/`                                                                            | 52   | Largest, most mechanical. Shim barrel keeps `app/` untouched.                                               |
| **3**             | `modules/auth/recovery/` → `features/recovery/`                                                                          | 39   | Steps + `StepLayout` go too — they *are* recovery's interaction.                                            |
| **4**             | `modules/auth/profile/` → `features/user/` **+ ****`screens/Profile/`**** → ****`features/user/ui/`**                    | 20   | Move **and** rename — the rename is the point; it finally lands in its real home.                           |
| **5**             | `modules/auth/journey/` → `features/journey/`                                                                            | 11   | It owns the `OnboardingJourney` fact → a capability, not a page.                                            |
| **6**             | `pages/auth/` — `authRoutes.tsx`→`routes.tsx`, `layout/`, `navigation/`, `GuestOnly`, `components/Stepper/`              | \~30 | Routing and chrome.                                                                                         |
| **7**             | `pages/auth/onboarding/` — `screens/Onboarding/`, `screens/Verify/`                                                      | \~10 | These arrange `features/journey` + `features/user` + `shared/channel-verification`. Textbook page material. |
| **8**             | **Cutover** — `app/` imports `@pages`/`@features` directly; delete the shim barrel, `modules/`, and the `@modules` alias | \~6  | The only WI that touches `app/`.                                                                            |
| **9**             | **Enforcement** — ESLint zone rules + extend `checks/` to intra-app zones                                                | \~3  | §5 below.                                                                                                   |
| **10**            | Documentation catches up — `architecture.md`, `authentication.md`, platform index, `docs/README.md`                      | \~5  | The deferred one, done once at the end.                                                                     |

---

## 4 · Three decisions the migration will force — name them now, not mid-branch

These are the only places where "just move it" doesn't answer. Deciding them **before** Phase 2 means no Work Item has to invent an answer under momentum (onboarding §6.4).

**(a)** **`MessageRegion`** **— the real one.** It's consumed by session's forms, recovery's steps, and the verify screens. After the split those are a feature, a feature, and a page. A feature may not import a page or another feature — **so it must go to** **`shared/`**, and `shared/` has no generic component home outside the Design System.

Two options, both legitimate: admit it to the Design System as the interim **`Alert`** — which [ux-direction.md](vscode-webview://1agot9io9rs6ljvkigtguglga2t21kjilju91bd82qq5iljv3l98/docs/features/authentication/product/ux-direction.md) already anticipates (*"auth's messages bind* *`Alert`* *once it exists"*) and which committed scope grounds — or open a second component home in `shared/`, which I'd advise against. **This is a decision, not a move, so it needs its own Work Item, sequenced before WI-2.**

**(b)** **`config/`** **splits three ways.** `authValidationRules` + `validationMessages` are consumed by session, recovery and user → shared vocabulary. `copy.ts` is wording, which `authentication.md` says is feature-owned, but one file serves several capabilities. Splitting a file is a change, not a move — decide the split up front and let each WI carry its own fragment.

**(c)** **`JourneyLayout`** **is used by both signup and onboarding.** That's why I'd keep **one page group,** **`pages/auth/`**, covering the whole `/auth/*` URL space with `onboarding/` nested inside it — rather than two sibling groups needing a shared layout between them. Fewer zones, no cross-group layout problem, and it matches the URL.

---

## 5 · Your caution, made mechanical

> *"We do not want Pages to turn into a place that contains logic."*

A stated rule erodes — that's [onboarding §10.8](vscode-webview://1agot9io9rs6ljvkigtguglga2t21kjilju91bd82qq5iljv3l98/docs/development/agent-onboarding.md) and it's how you got here. Two cheap, exact fences in **WI-9**:

**Fence 1 — a page may not reach the wire.** ESLint `no-restricted-imports`: nothing under `pages/**` may import `@shared/api` or `@shared/rtk-query`. This forces every server interaction through a feature, which is precisely the line you want. It is one config block and it cannot be argued with.

**Fence 2 — a page may not own state.** No `createSlice` / `createApi` / `injectEndpoints` under `pages/**`, and no reducer registered from a page. A page that owns a fact has become a feature.

Plus the zone direction itself — `shared ↛ features ↛ pages ↛ app` — enforced the way [Bulletproof React](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md) enforces its unidirectional rule. Note that **nothing enforces the current zone rule either** ([checks/boundaries.test.ts](vscode-webview://1agot9io9rs6ljvkigtguglga2t21kjilju91bd82qq5iljv3l98/checks/boundaries.test.ts) stops at the application edge), so this closes a live gap rather than adding ceremony.

**I'd put WI-9 immediately after WI-8, not last** — the fences should be live before the first new feature arrives, not after.

---

## 6 · Explicitly out of scope

Per your ruling, and worth writing into the plan so no branch drifts:

- ✗ The `unifiedBaseQuery` token bug — known, deliberately not now
- ✗ The 9 lint errors
- ✗ `shared/domain/` — nothing needs it until the first RTK Query feature; creating it now is a folder made empty in anticipation
- ✗ `widgets/` — deferred until a block is genuinely reused
- ✗ #623's contract machinery — most of what motivated it resolves by composition under this model
- ✗ Any new component, endpoint, test or behaviour
- ✗ Splitting a component into form + page — record it, don't do it

---

## 7 · Evidence per Work Item

Because the storybook lane is **not in CI** and story paths are exactly what a move breaks, each WI runs and states:

| GateExpected                         |                                      |
| ------------------------------------ | ------------------------------------ |
| `tsc --noEmit` (web)                 | pass — *the* real gate on a move     |
| web unit                             | **53 files / 208 tests** — unchanged |
| storybook                            | **24 files / 222 tests** — unchanged |
| `npm run build`                      | pass                                 |
| `check:boundaries`                   | 1 / 4                                |
| `git log --follow` on one moved file | traces through                       |

Lint stays red at 9 — pre-existing, named in the PR, not touched.

**Risk is low and bounded.** Each WI is independently revertible, `main` is green after each, and the shim barrel means a failed WI can be rolled back without touching `app/`. The one genuine hazard is a stale Vite transform after a large move — the register (Worker E #40/#41) records that no gate runs the dev server, so I'd spot-check `npm run dev` once after WI-8 and say so rather than imply it.

---

## Recommendation on sequencing

Do **WI-0 (ADR)** and **decision (a) MessageRegion** first, together. They're the only two things that can invalidate the rest, and both are cheap. Everything after them is mechanical enough that it could run largely unattended.

Want me to draft the ADR, or the execution plan in `.project/` first? I'd suggest the **ADR** — the plan's shape depends on what the ADR settles, and drafting the plan first risks writing a sequence against a decision that hasn't been taken.
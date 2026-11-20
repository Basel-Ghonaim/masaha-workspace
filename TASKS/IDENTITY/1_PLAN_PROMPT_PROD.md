# IDENTITY — ink + berry and the logo in production — PLAN (execution later, by a fresh session)

You are a **Claude Code planner** on **Masaha**, in **`C:\dev\masaha\app-design`** (a worktree detached at `main`
`f0709d28`, clean). This task brings the adopted visual identity — **ink + berry spark** — and **the new logo** from
the design prototype (#142, behind `?identity=slate-berry`) into **production**: the web's design system, its shells,
the favicon and app icon, the API's e-mail, the documents. You **plan only**: the plan is saved, your turn ends, the
owner approves, and **a fresh Claude Code session executes it**. **Model Opus 5.5, effort xhigh — be complete.**

## 0. How this task runs

1. Run the project's **`start-work-item`** skill, then plan with **`write-plan`**: the plan is saved to
   **`C:\dev\masaha\workspace\TASKS\IDENTITY\2_PLAN_PROD.md`** and **your turn ends** — no branch, no edit, no install,
   no server, no test run.
2. **No trial builds:** no temporary copies, no trial worktrees, no scratch runs, no rendering of the SVGs, no
   measuring by running code. What reading cannot settle becomes an executor check (`EC…`). The measured numbers you
   need are already in the trial's report (§2).
3. **#143 is open** (`feat/space-profile`, the space profile, view first) and **merges before this executes**. It
   touches `foundation.md`, the design system's icons and index, and adds profile components that use `accent` /
   `primary` classes. Read its diff (`git diff origin/main...origin/feat/space-profile`) and plan as if it is in
   `main`; the executor's first step re-checks the counts on the real `main`.
4. **Memory is short on this machine** (1–3 GB free at times). Nothing in your planning needs a heavy command.

## 1. The owner's decisions — binding (copy them into the plan's binding section, word for word)

Read **`C:\dev\masaha\workspace\TASKS\IDENTITY\0_OWNER_DECISIONS.md`** whole. Binding:

- **I1 — ink + spark:** a dark **ink** for actions and structure, a warm **spark** for "what matters now", sparingly.
- **I4 — berry adopted:** `slate-berry` is the identity and the logo's colours. **Production gets berry only, in two
  themes** (light, dark). Coral stays **in the prototype only**, for a later comparison; Sea leaves production.
- **The values are the trial's, as the owner approved them after round 4** — the `slate-berry` block of
  `docs/design/prototype/masaha/identity-ink-spark.css` at `main`: the neutral ramp in the ink's hue, the spark ramp,
  the remap of `primary` / `ring` / `sidebar-ring` to ink, `accent` / `sidebar-accent` to the spark tint (light
  spark-100; dark spark-900 lifted 30 % toward spark-800), `sidebar-primary` and `chart-1` to the spark, **a hover
  role of its own** (light neutral-200, dark `muted`; an ink wash on muted tracks), status colours unchanged.
- **The spark's rules:** fills, large text and icons only (≥ 3:1 on its ground); **never on an action, never small
  text, never destructive**. Links in running text are ink and **underlined**. Hover and selected differ from each
  other (hue, plus a second mark where the trial gives one: the sidebar's 3 px bar, the chip's spark edge).
- **The logo** (round 3 of the trial; files already in `docs/design/prototype/masaha/logo/`, the `-berry` ones):
  «مساحة» as the hero with "MASAHA" under it, the ة's two dots in the spark; the **full logo** in the site's header,
  the phone menu and the sign-in / account pages (40 px tall), and in the admin's sidebar (replacing the «م» tile);
  the **small mark** (the ة + dots) in the collapsed rail and the browser tab; **never mirrored**, never cropped;
  its accessible name «مساحة» / "Masaha" in each language. The name «مساحة / Masaha» is kept.
- **Also in this task (the owner's list, 2026-11-11):** `foundation.md` **and an ADR** for the spark and hover roles;
  the berry tokens in `apps/web/src/shared/design-system/`; the logo in header / sidebar / auth; **favicon + app
  icon** in `apps/web/public/`; **the skeleton's fill** (today 1.11 on a card — give it the hover fill, ≈ 1.27) and
  **the photo strip's «+N» scrim** (white on a 55 % scrim, 3.64 — darken to ≈ 70 % for 4.5:1); **Google Branding**
  (the owner's steps, §3.7).
- **Pending — the owner's call, not yet given:** the owner / reception shell (its sidebar head is the space switcher)
  shows **no platform logo** — the supervisor recommends keeping none. Plan it as an `OD` with that recommendation.

## 2. Read before planning

- `CLAUDE.md`; `docs/development/workflow.md` (§2, §3, §5, §7, §8, §9, **§10 — each prompt caps its sub-agents**),
  `engineering-principles.md`, `testing.md`; `docs/frontend/architecture.md`; **`docs/frontend/design-system/
  foundation.md` whole** (§4's palette and §5's values are marked *locked — Sea*: changing them is an architectural
  decision → an ADR; the next number is **0019**, check); `docs/design/README.md` (*Rules for implementing*: the
  prototype is a specification, not code to copy); the ADR index; the findings index (next free **219**, check —
  #143 may take one).
- The prototype at `main`: `masaha/identity-ink-spark.css` (every rule and its comment), `masaha/i18n.js` (how
  `?identity=` and the tab's icon work), the `data-brand-mark` hooks in `shared.jsx`, `auth.jsx`, `admin.jsx`,
  `Change password.html`; `masaha/logo/`; `docs/design/CHANGES.md` («Identity trial — ink + spark» and its rounds)
  and `INDEX.md`'s `?identity=` row.
- The workspace (read only): `TASKS\IDENTITY\4_PLAN_INK_ACCENT.md` (the idea and its criteria),
  **`6_REPORT_INK_SPARK.md` all four rounds** (its measured tables are the acceptance numbers; its *Two fixes the
  remap needed*, *Defects fixed*, *For the owner* and *Proposed alternatives* each need a production answer),
  `7_REVIEW_FINAL.md`; `TASKS\LOGO\LOGO_NOTES.md` (Axis 6 — the deliverables and favicon set — and the sections from
  «The symbol dropped» on) and `LOGO_DECISION.md` (its rules of use only; it predates the final logo).
- The code, at `main`: `tokens/primitives.css`, `semantic.css`, `tailwind.css`, `themes.ts`, `semantic.unit.test.ts`;
  **every** use of `accent`, `sidebar-accent`, `primary`, `ring` as a class or a variable across `apps/web/src`
  (the design system's components first, then features and pages, then #143's); `Button`'s primary hover; links
  styled by colour alone; `Skeleton`; the photo strip's «+N»; the covers' colour mixing (the trial had to mix in
  OKLab, not OKLCH); `leaflet.css` (pins); charts; the shells — `SiteHeader`, `SiteMenu`, `FocusLayout`,
  `AdminLayout`, the design system's `Sidebar`, the owner / reception shell — and every user of
  `copy.site.wordmark`; `apps/web/index.html` (**no favicon today, no `apps/web/public/` folder**); `check:build` and
  the site's first download; the showcase. In the API: **`apps/api/src/modules/auth/email/resetEmail.ts` hardcodes
  Sea's colours** (`#02787d` …) and its tests.

## 3. Questions the plan must settle (by reading, or as an `EC…`)

1. **The tokens' shape:** how the primitives change (the neutral ramp in the ink's hue; a spark ramp; whether
   `brand-*` is renamed to the spark or kept as its alias — and what `semantic.unit.test.ts` then guards); the new
   semantic roles (hover, hover on a muted track, and any spark role) and their Tailwind utilities; every value in
   a table, light and dark. No colour outside the design system.
2. **Each fix the trial needed, in production:** the primary hover (primary mixed with foreground vanishes under ink);
   the covers' mix; hover vs selected per component (rows, cards, chips, menu / select / combobox items, sidebar
   items, tabs, the segmented control); the selected chip's edge; links underlined.
3. **The logo's form:** an inline SVG component whose fills are semantic tokens (follows the app's own theme toggle)
   or image files per theme — weigh the site's first download (the traced logo is ~14 KB of paths; `check:build`),
   theming, the accessible name, never mirrored in RTL; its sizes and clear space; where the files live.
4. **The favicon and app icon:** the files (an SVG favicon that follows the browser's scheme, PNG sizes, `.ico` or
   not, the 180 px home-screen icon), the `index.html` links and `theme-color`, and **how the raster files are made
   without a new dependency** (the owner's Axis 6 said he exports them; or they are produced outside the repository)
   — an `OD`.
5. **The reset e-mail:** its colours to ink / berry (e-mail clients: no CSS variables), contrast, its tests. A logo
   in the e-mail is out of scope unless you propose it.
6. **The prototype after production:** production becomes berry while the prototype's default is still Sea. Does
   berry become the prototype's default (Sea and coral behind `?identity=`), so the design source matches
   production? An `OD`, with the files it touches.
7. **Google Branding (the owner's steps, not code):** the logo file Google asks for (size, format), where the owner
   uploads it, and whether adding a logo to a published app needs Google's brand verification and what users see
   meanwhile (an `EC` or a point for the owner — do not guess).
8. **The merge day:** every screen changes colour at once for visitors, owners, reception and the admin — say
   exactly what each sees change.

## 4. The task's size and how it executes — the owner's request

Estimate the work **before** recommending its shape:

- **Count** the files per area (tokens, design-system components, features and pages, shells, assets, the API's
  e-mail, documents, prototype, tests), the commits, and the verification load (the visual pass in §6).
- **Recommend one of two shapes, as an `OD` with your reasons:**
  - **(a) one executor session** builds everything in order;
  - **(b) a lead executor and sub-agents:** the lead builds **the shared layer** itself — the tokens and the new roles
    and their utilities, the logo component's interface, `foundation.md` and the ADR — commits it, runs `lint`,
    `typecheck`, the token test and the build green, and **only then** splits the rest into **lanes**, each run by a
    sub-agent, and joins them into one branch.
- **If (b):** a lanes table — each lane's files, commits, tests and breaks, and what it may not touch. Rules: lanes
  are **disjoint by files** (a shared file is the lead's, or given to exactly one lane); no lane starts before the
  shared layer is committed and green; **at most 3 sub-agents** (this prompt's cap, workflow §10); **the heavy runs
  are the lead's, one at a time** (full lanes, builds — the machine may have 1–3 GB free); each sub-agent's prompt
  is self-contained and written by the lead; the lead joins the lanes by rebase in a stated order, folds a fix into
  its commit, and keeps the plan's atomic commits.
- **The PR split, as an `OD`:** one PR, or several — knowing that **every merge to `main` deploys to production**,
  so no PR may leave the live site half Sea and half berry.

## 5. Tests — the owner's bar

**The tests must work and point the right way — never bent to pass; no gap.** A numbered **test matrix** (`T…`),
each test naming the behaviour it proves, the break it catches and its lane (`testing.md`). At least: every semantic
role resolves in both themes, the new roles included; **the contrast pairs the trial measured as a test that fails
when a pair drops below its threshold** (if you judge it sound — computed from the token files, no production code
only a test uses); the spark never on an action (where a test can hold it); the logo — its name in both languages,
never mirrored, the right colours per theme; each shell shows it; the favicon and app icon linked; the reset e-mail's
colours; axe in both themes on the touched screens. Every new test **seen failing first**.

## 6. The visual pass (written into the plan for the executor)

A real run, one headless Chrome at a time: the trial's screens and more — Home, the directory (cards, filters, a map
pin selected), a space's page, sign-in and the account pages, the desk (check-in, «إلغاء الدفعة»), the owner's
overview and space profile with a Sheet open, the admin's overview, spaces and a space's editor, a loading state —
at **390, 768 and 1440**, **Arabic and English**, **light and dark**; compared with the prototype at
`?identity=slate-berry`; a computed-colour scan for any Sea teal left; focus rings on every surface; hover vs
selected seen. Screenshots to `C:\Users\basel\Downloads\identity-prod-shots\`, curated, never pushed.

## 7. What the plan contains

Number everything: the binding decisions (verbatim); the token tables (light and dark, every value); per area — the
files, the change, its documents and its tests; the documents (`foundation.md` §4 / §5 / §15 and the logo's rules of
use, the ADR, `docs/frontend/architecture.md` if it changes, the design archive if the prototype changes, the
*Deferred documents* triggers of `docs/README.md`); a dependency only if unavoidable (none expected — an `OD` if
any); the commits (Conventional, subject ≤ 50 characters, each with a body); the size estimate and the execution
shape (§4); `EC…`; risks; **"Proposed alternatives"** (you may challenge any decision above — never deviate
silently); open points for the owner (`OD…`, each with options and your recommendation); what changes on the merge
day.

## 8. Limits (for the plan, and written into it for the executor)

- No migration. No new dependency without an approved `OD`. **Never `db:seed` `masaha_dev`.**
- Complete local verification before any PR: `lint`, `typecheck`, `format:check`, `check:classes`, `check:links`,
  `check:conflicts`, `build` + `check:build` (with `NODE_ENV=production`), `test:unit`, `test:component`, `test:api`
  in full (the e-mail is API code), and the visual pass. **A lane killed for memory: retry once; if killed again, CI
  judges** — said in the PR and the report.
- Stage by path; never `git add -A` / `git add .`; no tool attribution; no `#PRNUM` left (the next PR is expected to
  be **#144** — checked just before the push). No push to `main`, no merge, no force-push of another branch, no secret
  printed. Workers never stop on file count; they report it. Review fixes fold into their commits (`backup/*` first).
- Public text never names hosting providers, free plans or session durations.

When the plan is saved, print a short summary — the size, the recommended shape, the number of `OD`s and `EC`s — and
stop.

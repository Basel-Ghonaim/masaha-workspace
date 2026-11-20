# Sign in — 3 to 4 new designs, from your own analysis — the DESIGNER

You are the **designer** of a new round for Masaha's **Sign in** page: a fresh **Claude Code** session, **Opus 5.5,
effort high**, started in **`C:\dev\masaha\masaha-prototype`** (the design repository, public:
`Basel-Ghonaim/masaha-prototype`, on `main` at `96f7bc6`, two local commits ahead of `origin/main` — leave them).
Masaha (مساحة) is a bilingual **Arabic-first (RTL)** / English platform for coworking spaces in the **Gaza Strip**: a
public directory with live availability, a small account area, and a dashboard for space owners and their reception.
It is **live** (`https://masaha-omega.vercel.app`).

**The owner's request, in his words (2026-11-19):** a real effort of your own — **analyse, understand, then build
3–4 new designs** of the sign-in page, **different from the ones that exist**. The drawing of the Strip is **not
required**: use it only if your design truly needs it.

**The owner's bar:** a page that looks like **a strong, real product** — confident, crafted, with a character of its
own — never a beginner's page, never a template, never "AI-looking". He decides by looking, and he reacts strongly to
sloppy UI, empty-feeling space, parts that don't relate, and unexplained disabled controls.

**The owner is away for the whole run: never stop to ask.** No question, no waiting for an approval, from the first
read to the report. When something is unclear, choose the safest option that keeps to this prompt and the
repository's rules, write the choice and its reason in `8_REPORT.md` § 6, and go on. A command that fails: read the
error, fix the cause, go on; a run killed for memory: retry once, then go on without it and say so. The hard limits
still hold (never push, never edit the production repository, the original page or the shared modules).

## 0. Read first — in this order

1. **This repository's rules:** `CLAUDE.md`, `README.md` (§ How to run it, § Variants, § Checking the prototype),
   `prototype/BRIEF.md`, `decisions/README.md`. They bind you.
2. **The history of these pages — what was tried and why it failed:** `decisions/auth.md` (whole) and
   `C:\dev\masaha\workspace\DESIGN\AUTH\0_OWNER_DECISIONS.md` (A1–A12, binding). Then look at the three designs that
   exist, in a browser, at 1440 and 390, Arabic and English, light and dark:
   - `prototype/Sign in.html` — **the original**: a card centred in an empty page (the owner: weak).
   - `Sign in.html?v=slate` — **Slate**: form beside an ink panel with a drawing of the Strip and a lens (the owner:
     "half empty", "its parts unrelated", "not professional").
   - `Sign in.html?v=slate2` — **Slate 2**: a narrower panel, the Strip drawn large (the owner: the drawing "is
     neither east nor west — nothing can be understood from it").
   Also `C:\dev\masaha\workspace\DESIGN\AUTH\1_CRITIQUE_CHECKED.md` (the confirmed defects of the original) and
   `5_REVIEW.md` (the review of the first three designs).
3. **The production facts, read-only** (the production repository at `C:\dev\masaha\app`; **never edit it, never run
   anything in it**): `docs/project/overview.md` (v1 and *Not in v1*), `docs/features/auth.md` (the sign-in page,
   its states and rules — production is the truth), `docs/frontend/design-system/foundation.md` (§2–§10, §16 the
   logo), `docs/architecture/decisions/0019-*.md` (ink + berry: the berry's job), the copy catalogue
   `apps/web/src/shared/copy/arabic/auth.ts` and `english/auth.ts` (the product's real words), and
   `apps/web/src/pages/site/auth/SignInPage.tsx` with its feature folder (what the page really holds).
4. **How the auth variants are built:** `prototype/variants/index.js`, `prototype/variants/_auth/kit.jsx` (one kit:
   the page logic and every state of Sign in — error, Google, rate limit, offline, pending, idle — with `AxFrame`
   drawing the frame), `_auth/base.css`, `_auth/slate.css`, `_auth/slate2.css`.

## 1. Analyse before you draw — and write it down

Before any code, write **`C:\dev\masaha\workspace\DESIGN\AUTH\8_REPORT.md` § 1 Diagnosis** (short, concrete):
- why each existing design fails the owner's bar — in terms of composition, hierarchy, alignment, density, type,
  surface and brand, not taste;
- what a sign-in page of a strong product does (look at real products' sign-in pages — the skills below help — and
  name what you take from each, never copy one);
- what is specific to Masaha that a sign-in page can carry: Arabic first, ink + berry, the logo, the Gaza Strip's
  coworking community, a weak connection, a phone first;
- then **3–4 directions**, each one paragraph: its idea, why it answers the diagnosis, and how it differs from the
  others and from the three that exist. **They must be genuinely different from each other** — not one layout in
  four colours.

Then build them — you do not wait for an approval (the owner asked for your own effort; he judges the result).

## 2. Build

- **Sign in only.** Each design a variant `Sign in.html?v=<name>`, registered in `prototype/variants/index.js`
  (Sign in's list: keep `slate` and `slate2` first, add yours after them), labelled in Arabic and English (short).
  A short English `name` of your own (not `slate…`, `coast`, `dots`).
- **Use the kit** for the page's logic and states: add your designs to `AX_DESIGNS` and give each its stylesheet
  (`_auth/<name>.css` over `_auth/base.css`), its two-line `variants/Sign in/<name>.jsx` and `.css` like
  `slate2`'s. Where a design needs a different frame or panel, add **its own** component in the kit (as `AxPanelV2`
  is Slate 2's), named `Ax…`. **Slate and Slate 2 must render exactly as they do now** — check them after your work.
  Never edit the original page, the shared modules (`masaha/*.jsx`, `masaha/*.js`) or the sample data.
- **Every state** of Sign in must work in each design (`?state=error|google|ratelimit|offline|loading|idle` — see how
  the kit reads them), at **390, 768, 1280, 1440 and 1920**, **Arabic and English**, **light and dark**.

**Fixed points (no design changes them):**
- **Identity:** ink + berry and the logo as they are (ADR 0019, foundation §16; the logo files in
  `prototype/masaha/logo/`). The berry marks — never text, never an action, never an error.
- **Arabic first:** designed right to left, then checked left to right; logical sides only.
- **The product's words:** the copy catalogue's. A new line of your own is allowed only where the page needs one, in
  both languages, listed in `decisions/auth.md` › *New words* as a proposal.
- **Not allowed (the owner's past decisions, still binding — A2, A3, A11):** a photo; a glimpse of the product
  (screens, cards or mock data); a plain text-only panel; **any count or figure that changes** (spaces, users,
  bookings…); fake data of any kind (no ratings, no capacity, no invented claims); anything on *Not in v1* (no
  booking, no online payment…). **If you draw the Strip**, it must read as a place — north up, never mirrored, the sea
  to the west, its outline round 3's approximate one already in the kit — and its dots, if any, the real spaces.
- **Google's button** keeps Google's own look (light, or Google's dark with no white frame) at the box production
  draws: 40 px tall, at most 400 wide.
- **Accessibility:** WCAG AA contrast in both themes; one visible focus ring; 44 px targets on touch; labels tied to
  fields; the h1 is the page's title; a failed submit focuses the first invalid field (the kit does this — keep it).
- **Calm on a weak connection:** inline SVG or CSS only, no image files over a few KB, no web font beyond what the
  prototype loads; motion only if it earns its place, and off under `prefers-reduced-motion`.

**Skills you may use** (load them, they help): `frontend-design:frontend-design` (direction and craft),
`ui-design-review:compare` and `website-design:review-page` (real products as reference), the
`vectorlab-ux-skills` `anti-slop`, `spacing`, `typography` and `viewports` skills (checks). Do not use
`anthropic-skills:brand-guidelines` (it is another company's brand) and no paid service.

## 3. Check — your own eyes before the owner's

- `node scripts/check-parse.mjs` and `node scripts/check-classes.mjs` pass before each commit.
- The supervisor's server already serves `prototype/` at `http://localhost:5410` — use it (it serves your edits as
  you save; reload with the cache bypassed). If it is down, serve your own as README says on a free port and stop it
  at the end. **Look at every design** at the widths, languages, themes and states above. Capture with headless Chrome — every
  heavy run (headless Chrome batches) through the machine's grant script from `C:\dev\masaha\app`:
  `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs design <command…>` (it waits for ≥ 4 GB free; let it
  wait). Captures to `D:\MASAHA\DT\AUTH\round4\` named `<design>-<width>-<lang>-<theme>[-<state>].png`; never in the
  repository.
- Look for: overflow at 390 (`scrollWidth` = the width), the focus ring, Arabic line-breaks, the panel or art at
  every width (nothing cut by accident), dark theme surfaces, and the states' boxes.
- If you started a server of your own, **stop it by its PID** at the end and say the port is free. Leave 5410 running.

## 4. Record and commit

- `decisions/auth.md`: one section per design under *Variants* (its idea, what it changes, what it proposes against
  masaha's design system and why, what it keeps), and its new words if any.
- **Commits** on this repository's `main`, **local only — never push**: one commit per design (its kit part, its
  styles, its variant files, its decision section), Conventional, subject ≤ 50 characters, a body that says why,
  staged by path, no tool attribution.

## 5. Report — `C:\dev\masaha\workspace\DESIGN\AUTH\8_REPORT.md`

§ 1 Diagnosis (above); § 2 the designs — each one's link (`http://localhost:<port>/Sign%20in.html?v=<name>`), its
idea in two lines, what to look at first, its weak point stated honestly; § 3 **your recommendation** — which one,
and why; § 4 what you checked (widths, languages, themes, states) and what you could not; § 5 commits (hash and
subject); § 6 anything you were unsure of. Then **stop**. Never push, never merge, never edit the production
repository.

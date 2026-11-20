# The auth pages — three designs, every auth page, and a lab to compare them — the LEAD

You are the **lead designer** of Masaha's authentication pages: a fresh **Claude Code** session, **Opus 5.5, effort
high**, started in **`C:\dev\masaha\masaha-prototype`** (the design repository, public:
`Basel-Ghonaim/masaha-prototype`). Masaha (مساحة) is a bilingual **Arabic-first (RTL)** / English platform for
coworking spaces in the **Gaza Strip** — a public directory with live availability, an account area, and a dashboard
for owners. It is **live** (`https://masaha-omega.vercel.app`).

**The owner's bar:** a design that looks like **a strong, real product** — confident, crafted, with a touch of its
own — never a beginner's page and never a template. Calm and fast on a weak connection.

**Your output:** **three distinct designs** of **every auth page**, each page's three designs reachable as variants
(`?v=`), and **one simple dashboard-like page that switches between them** — design, page, state, language, theme and
width — so the owner compares them side by side and chooses.

## 0. Read first — in this order

1. **This repository's rules: `CLAUDE.md`, `README.md` (§ Variants, § How to run it, § Checking the prototype),
   `prototype/BRIEF.md`, `decisions/README.md`.** They bind you (the original page is never edited; variants only;
   no shared module or sample data edited; checks before each commit; no attribution).
2. **The owner's decisions for this work — binding:** `C:\dev\masaha\workspace\DESIGN\AUTH\0_OWNER_DECISIONS.md`
   (A1–A4: the layout direction and the Strip's conditions) and `1_CRITIQUE_CHECKED.md` (the confirmed defects and
   design points every design must answer).
3. **The production facts, read-only** (the production repository at `C:\dev\masaha\app-design`, `main`; **never
   edit it, never run anything in it**): `CLAUDE.md`; `docs/project/overview.md` (v1 and *Not in v1*);
   `docs/project/glossary.md`; `docs/features/auth.md` (every auth page, its states and its rules — **production is
   the truth; the prototype's auth pages may be behind it**); `docs/frontend/design-system/foundation.md` (§2–§5,
   §7–§10, §12–§16); `docs/architecture/decisions/0019-*.md` (ink and the berry's role); the copy catalogue
   `apps/web/src/shared/copy/arabic/auth.ts` and `english/auth.ts` (**the product's real words — use them**);
   `apps/web/src/features/auth/` (to see which states exist: e.g. forgot password's *sent* state with the masked
   address and the resend held by its window; the reset link open, invalid or unreachable; offline and the general
   error with «إعادة المحاولة»; Google; the forced change).
4. **What exists in the prototype:** `prototype/Sign in.html`, `Register.html`, `Forgot password.html`,
   `Reset password.html`, `Change password.html`, `Reset email.html`, `Sign in - board.html`, the shared
   `prototype/masaha/auth.jsx`, `i18n.js`, `variants.js`, `variants/index.js`; how each page reads `?state=`.
5. **Round 3's material you may reuse** (`C:\dev\masaha\workspace\DESIGN\ROUND3\`): `DIAGNOSIS.md` (what makes the
   site read as a template); direction B's Strip — `directions\_shared\data\strip-outline.json` (an approximate
   outline, not survey data) and the spaces' real coordinates in `directions\_shared\data\spaces\` (a snapshot of the
   live public API, 2026-11-14); `directions\B\` for how it drew the Strip. Round 3's directions as a whole were judged
   weak by the owner: take ideas, not their designs.
6. **The current pages as they are live:** `D:\MASAHA\DT\AUTH\*.png` (36 captures: 5 pages + the expired link, 390 /
   768 / 1920, light / dark).

## 1. What every design keeps (fixed)

- **A1, the layout direction:** from **1280 px** two columns — the form on the **start side** (right in Arabic) with
  **no card**, and an **ink brand panel** on the other side: the logo, a confident title, one line on what an account
  gives, and **the Strip**. **768–1279:** one column, the form at a **fixed offset from the top** (no vertical
  centring). **The phone:** the form at full width, **no card, no frame**; larger fields and buttons; a clearer title;
  the Strip at most a small touch.
- **A2, the Strip:** an **artistic drawing, not an official map** — no governorate borders drawn as fact, no
  geographic detail held to accuracy; its dots are **real spaces** (the snapshot's coordinates, its date stated) in
  the **berry**, or no dots at all — never invented ones; an **inline SVG**, light on the network; with
  `prefers-reduced-motion` respected if it moves.
- **The identity:** ink + berry and the logo, as ADR 0019 and foundation §16 define them (the logo's files are in
  `prototype/masaha/logo/`). The berry gets **a job** (it marks what matters), not decoration.
- **Arabic first:** each page designed in Arabic, RTL, then checked in English, LTR; logical sides only.
- **The product's real words** from the copy catalogue. **New words** (the panel's title and line, any context note)
  are **proposals**, given in Arabic and English, marked as such in the decision file — the owner settles them.
- **No fake data, nothing on *Not in v1***: no counts or claims that are not real; no booking, payments, ratings.
- **Every confirmed point of `1_CRITIQUE_CHECKED.md` answered in all three:** Google's button in dark with no white
  frame and as wide as the fields; forgot password's form shown at once (no bare spinner); the forced change with a
  language switch; password conditions that never read as radio buttons; one fixed top offset; a real hierarchy; no
  frame inside a frame on the phone; the berry beyond the logo; «حرف واحد على الأقل» saying any letter counts.
- Accessibility: WCAG 2.1 AA contrast in both themes, a visible focus on every control (Google's and the show-password
  button included), targets ≥ 44 px, errors tied to their fields, `autocomplete` as production has it.

## 2. What the three designs vary (make them genuinely different)

Within §1, the three differ in **composition and character**, not in colour tweaks. Axes to vary: how the panel is
composed (the Strip full height, the Strip as an edge or band, the Strip as a quiet watermark behind the title…);
**the type** (scale, weight, rhythm; a display face only as a proposal, Arabic shaping first); how the berry works;
how the form's states feel (errors, sent, link invalid, offline); motion (the Strip drawing in, or none); how the
phone carries the brand. **One of the three stays closest to A1 as written**; the other two push further. Name each
with a short, telling name (Arabic and English) and describe it in two lines in the decision file.

## 3. The pages and their states — every one, in all three designs

1. **Sign in** — default; wrong e-mail or password; the account made with Google; the rate limit; offline; pending
   (the button busy). Google's button in both themes.
2. **Register** — default; the e-mail already has an account; field errors; the password conditions as the user
   types (unmet / met); the space owners' note (where it belongs).
3. **Forgot password** — the request; **sent** (the masked address, the resend held by its window); the resend's
   limit; offline; the way to contact the team.
4. **Reset password** — the new password (with «للحساب …»); **the link invalid** (one state for expired or used —
   the API never says which, on purpose); the check unreachable; saved.
5. **Change password (forced)** — the temporary password's context; the conditions; errors; the language switch.
6. **Reset e-mail** — the e-mail template, following each design within e-mail limits (tables, inline styles, no
   reliance on SVG or web fonts; the logo as it is in production's e-mail).

Each variant handles the page's `?state=` values (keep the original's names; add the missing states with clear
names, listed in the decision file).

## 4. The lab — one page to compare

Add **`prototype/Auth lab.html`** (a new page; it edits no original): a simple dashboard in Masaha's own look.
- Controls: **the design** (Original / your three), **the page**, **the state** (the page's states), **language**
  (ar / en), **theme** (light / dark), **width** (390 / 768 / 1440, or **all three side by side**).
- It shows the page in iframes at those widths (the variants' own switcher stays hidden inside a frame — README) and
  links each frame to its full page. Its choices live in its own address (`?design=&page=&state=…`), so the owner can
  send a view as a link.
- An option **"compare designs"**: one page and state, the original and the three side by side at one width.
- Arabic first, both themes, keyboard usable; no shared module edited.

## 5. Method, cost and the machine

- **You design first:** write the three designs' specs in `decisions/auth.md` (the decision file of all auth pages,
  in the template's form: each design's idea, its type / spacing / surfaces / motion as proposals against masaha's
  design system with their reasons, the Strip's data and date, the new words, the states added). Then **build Sign
  in in all three yourself** and look at it hard (390 / 768 / 1440, ar / en, light / dark) before going on.
- **Then up to three sub-agents, one per design**, each extending its design to the other five pages from your spec
  and your Sign in; you review each one's pages against the spec and §1 and send fixes back; you build the lab. (If
  you judge one session enough, say so and do it alone.)
- **The server:** `python -m http.server 5410 --directory C:\dev\masaha\masaha-prototype\prototype`. If your session
  refuses to start a server, **do not work around it**: say so in the chat — the supervisor keeps one running on
  5410 from his launch configuration.
- **Heavy runs** (any headless Chrome batch) only through the machine's grant script, one at a time:
  `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs auth <command…>`. Other workers share this machine.
- **Never touch** `C:\dev\masaha\app`, `app-cr` or `app-dr` (other workers), and never `README.md` or `CLAUDE.md` of
  this repository (another worker adds a link there).
- Before each commit: `node scripts/check-parse.mjs` and `node scripts/check-classes.mjs` (a class the prebuilt
  bundle lacks is dead — new styles go in the variant's own `.css`); then look at the pages. Commit straight to
  `main` by path, Conventional (`feat(auth): add the <name> designs of sign in`), subject ≤ 50, a body, no
  attribution; `git pull --rebase` before you push; push at the end.

## 6. The captures and the report

- **Captures for the owner** (through the grant script): every page × design (the three and the original) × its
  default state, at **390 / 768 / 1920**, **light and dark**, Arabic, PNG at 2x, the switcher hidden
  (`?switcher=0`), into `D:\MASAHA\DT\AUTH\variants\`, named **`<n>-<page>-<design>-<width>-<theme>.png`** (the page
  numbers of `D:\MASAHA\DT\AUTH\`: 1 sign in, 2 register, 3 forgot password, 4 reset password, 5 change password,
  6 reset e-mail). Plus the lab at 1440, light and dark. Look at every capture yourself before you report.
- **The report:** `C:\dev\masaha\workspace\DESIGN\AUTH\4_REPORT.md` — the three designs in a few lines each, with
  their best captures named; how each answers §1; the proposals against masaha's design system (type, spacing,
  surfaces, motion, the berry's role) — **these become a masaha decision only if the owner chooses them**; the new
  words in both languages; the states added; the commits and the pushed head; what you could not do, and why.
- Then a short Arabic summary for the owner at the top of the report: what each design is, and your recommendation.

**Stop when the report is written.** Nothing here touches production.

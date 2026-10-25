# Masaha — the logo worker's handoff (2026-10-25)

You are taking over a **side task** for the owner of Masaha: **designing its logo**. You discuss it with the
owner, who will produce the logo **outside the project** (with external design tools) and later bring the
result to the main supervisor's conversation. **Your job is the thinking and the brief, not the code.** Reply
to the owner **in Arabic**, short, decisions as items with options and a recommendation (never tables in
Arabic replies; no Arabic line that starts with an English word or a code token).

## 0. Your limits (read first)

- You run in `C:\dev\masaha\app`, which is **worker A's live worktree** (it builds the front desk's screens
  there). **Never edit, create or delete a file in any repository folder; never `git checkout`, `switch`,
  `reset`, `stash`, `commit` or `push`; never run `npm`, a server, a test or a database command.** Read the code
  through commit objects only: `git fetch origin`, then `git show origin/main:<path>`, `git grep -n <x>
  origin/main -- <path>`, `git ls-tree -r --name-only origin/main <dir>`.
- Write only in `C:\dev\masaha\workspace\TASKS\LOGO\` (your notes, the brief, the prompts for image tools).
- This task is **not** in the main handoff or the board, and creates **no** branch, PR or Issue. Building the
  chosen logo into the code is a later Work Item the main supervisor plans.
- Keep it cheap: read only what §3 names, each once.

## 1. The product, in five lines

**Masaha (مساحة, "space")** is a bilingual web platform (Arabic first, right-to-left; English) for **coworking
spaces in the Gaza Strip**: a public directory with a map and the **live status** of each space (available,
busy, full, closed now), a page per space, and one role-based dashboard where owners and their reception run
the day (check-ins, visits, subscriptions, payments). It is the owner's own project, built by one developer,
where engineering quality is part of the product. **Never name a university, a supervisor or a defence in
anything about it.**

**Who sees the logo:** freelancers and students in Gaza looking for a desk with power and internet; space
owners and their staff, all day, on phones and laptops; often on a **weak, intermittent connection**.

**Tone (settled, foundation §1):** calm, trustworthy, practical — **no playful or decorative styling**.

## 2. The brand facts already settled (do not reopen them)

- **Name:** «مساحة» / "Masaha". Tagline in the site: «مساحة — دليل مساحات العمل المشتركة في قطاع غزة» /
  "Masaha — a directory of coworking spaces in the Gaza Strip".
- **Colour — the "Sea" palette, petrol teal**, brand colour `brand-600` = `#02787d`. The full ramp (for light and
  dark variants): 50 `#eafbfc` · 100 `#d5f4f5` · 200 `#b3e6e8` · 300 `#85d0d4` · 400 `#50b3b8` · 500 `#15959b` ·
  **600 `#02787d`** · 700 `#096165` · 800 `#05494c` · 900 `#023235` · 950 `#001d1f`. In dark mode the primary is
  `brand-400` on `brand-950`. Neutrals carry a slight teal cast.
- **Font:** IBM Plex Sans Arabic (400 / 500 / 600) for both languages. A wordmark may use it or a custom
  lettering that sits well beside it.
- **Radius:** soft (8 px base). **Icons:** Lucide (thin, line icons).
- **The logo is the one open visual decision:** foundation §15 row 5 — "Logo / wordmark for «مساحة» / Masaha —
  **Open**".

## 3. Where the logo will live (read these, at `origin/main`)

| What | Where | What it shows today |
|---|---|---|
| The site's header | `apps/web/src/pages/site/shell/SiteHeader.tsx` | the word «مساحة» / "Masaha" as text (`copy.site.wordmark`) |
| The admin's and owners' sidebar | `apps/web/src/pages/dashboard/shell/AdminLayout.tsx`, the `Sidebar`'s `mark` slot (`shared/design-system/components/navigation/Sidebar/Sidebar.tsx`: "always shown, also on the rail: the logo mark") | a tile with the first letter «م» |
| The browser tab | `apps/web/index.html` (`<title>مساحة</title>`) | **no favicon at all** (`apps/web/public/` does not exist) |
| A space with no photo | the directory's cards | a teal tile with the space's first letter — **the logo must not look like these tiles** |
| The design system's rules | `docs/frontend/design-system/foundation.md` §1 (context), §4–§7 (tokens, theming, typography), §8 (RTL), §10 (accessibility), §15 (visual decisions) | |
| The tokens | `apps/web/src/shared/design-system/tokens/{primitives,semantic}.css` | |
| The scope | `docs/project/overview.md` | |

Also worth a glance (both themes, both languages): `docs/design/prototype/` — the clickable prototype the
screens were built from (open `Home.html`, `Directory.html`, `Space.html` in a browser; read-only).

## 4. Constraints the logo must meet (each one a point to discuss)

- **Works in Arabic first**, with an English lockup for the English interface; right-to-left reading.
- **Light and dark themes** (two colour versions, or one that works on both).
- **Small sizes:** a favicon at 16–32 px, the sidebar's rail mark at ≈ 32–40 px, a phone header — so a **mark**
  (symbol) that stands alone, plus a **wordmark**, plus their lockup.
- **One colour** version (stamps, receipts, a printed sign at a space's door) and a monochrome one.
- **Light to load:** delivered as clean **SVG** (no embedded bitmaps), small file size; it lives in the design
  system layer (`apps/web/src/shared/design-system/`) as a component, coloured by semantic tokens.
- **Accessible:** enough contrast on both backgrounds; never the only carrier of meaning.
- **Distinct from the live-status colours** (available green, busy amber, full red) and from the spaces' letter
  tiles.
- **Culturally and locally apt** for Gaza, and calm: no clichés that read as charity, war or tourism; no
  map of the Strip that could read as political; consider what reads well on a cracked phone screen in sunlight.

## 5. The axes to settle with the owner (your first conversation)

Propose, for each, 2–3 options with a recommendation:
1. **The idea:** what the mark says — a space/room (a door, a desk, an open square), a place on a map (a pin),
   the word itself (a monogram from «م» or a wordmark only), connection/availability (a signal, a live dot).
2. **The form:** wordmark only · mark + wordmark · monogram; geometric vs. calligraphic; how Arabic and Latin
   versions relate.
3. **The colour use:** brand-600 alone, a two-tone from the ramp, or neutral with a teal accent.
4. **The typography of the wordmark:** IBM Plex Sans Arabic set as is, adjusted, or custom lettering.
5. **The tools and the method** (the owner works outside the project): which AI or design tools, how to keep
   the Arabic letters correct (AI image tools often break Arabic letterforms — a common route is an AI-made
   mark plus the wordmark set in a real font), how to get a clean SVG.
6. **The deliverables** the main supervisor will need later: the files (SVG mark, wordmark, lockups in Arabic
   and English, light/dark/mono, favicon sizes and `.ico`/PNG), and a one-page note of the choice and its
   rules (clear space, minimum size, do and don't).

## 6. When the logo is ready

The owner brings it to the main supervisor's conversation. Prepare for that moment a short file
`C:\dev\masaha\workspace\TASKS\LOGO\LOGO_DECISION.md`: the chosen logo's files and where they are, the decision
in one paragraph, the rules of use, and what the code change will need (the header, the sidebar's mark, the
favicon and `index.html`, foundation §15 row 5 settled, the showcase). The main supervisor turns it into a Work
Item; you do not plan or write code.

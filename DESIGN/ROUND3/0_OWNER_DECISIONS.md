# Design review round 3 — the owner's decisions (2026-11-13)

A full design review of the whole product, redone from scratch (round 2, Issue #81, reached 30 of 40 reviews of the
prototype and is not continued). **Approved by the owner, every point as the supervisor recommended:**

- **R3-1 — the subject:** the **real web app** at the identity PR's head (`feat/ink-berry-identity`, ink + berry and
  the logo), with real data and every role (visitor, signed-in user, owner, reception, admin). The prototype
  (`docs/design/`) is the reference for the intended design, not the subject. The PR need not be merged; it may merge
  at any moment (the tree is the same).
- **R3-2 — six agents by part,** each applying every axis to its part (round 2's parts and axes): **PU** public ·
  **AU** sign-in and account · **OW** owner · **DK** desk and reception · **AD** admin · **SH** shared (the design
  system, the identity, the shells and navigation, RTL / dark / responsive, motion, and consistency across parts).
  Axes: AX accessibility · CP content and Arabic copy · DF defects · EX excess · TR truth to product, data and API ·
  UX the way through · VD visual · **ID the identity** (new). One **lead** (Claude Code, Opus 5.5 xhigh) builds the
  inputs, runs the six, checks and merges them, and writes the summary across all.
- **R3-3 — one capture pack first** (round 2's lesson): the lead captures every screen and state at 390 / 768 / 1440,
  Arabic / English, light / dark, with measured facts and contact sheets; each agent judges from its own frames, with
  a few live checks (keyboard, states) through the machine's grant script.
- **R3-4 — skills:** `frontend-design` and the Vectorlab UX skills as **lenses** (they never override the design
  system or a settled decision — a conflict is a "rule in doubt"). **Not `brand-guidelines`** (it is Anthropic's own
  brand); Masaha's brand is `foundation.md`, ADR 0019 and §16 (the logo). The owner's word sets aside workflow §10's
  "review sessions use no plugin skill" for this round — stated.
- **R3-5 — timing and place:** starts once the identity PR is open and green (its head pinned); in its own worktree
  (`C:\dev\masaha\app-dr`), its own database (a copy of `masaha_dev`), its own ports (3336 / 5336). WOMEN_EVENING is
  not on that head: reviewed later, apart.
- **R3-6 — the output:** a report per part and one summary across all — every issue with its own capture, a measured
  fact and a proposal for the best design. **Nothing is fixed in this round.** Then a decisions round with the owner
  (`DECISIONS_ROUND3.md`), then fix batches.
- **R3-7 — Issue #81** becomes stale with this round: closing it is the owner's word, later.

## Changed by the owner (2026-11-14) — R3-2 and R3-3 replaced

The six-part defect review is **not run** (its lead stopped at `npm ci` on 2026-11-13; nothing was captured). The
owner's new direction:

- **R3-8 — two axes only: the design system, and the public site** — the parts every visitor sees in full.
- **R3-9 — the aim is a stronger design, not a defect list:** people with design experience who saw the live site told
  the owner it must be stronger — it should feel like a real, strong product, **not a site made with AI**. The review
  goes as far as **the division of each page**, and ends in **real changes to the design**.
- The lead's preparation stays usable: `HEAD.md` (4cff26c7 = `main`'s tree), `INVENTORY.md`, `tools\`, the PU and SH
  prompt drafts, the worktree `app-dr` and `masaha_dr_*`.
- Details (scope of "the public site", the output, the limits, the budget) are being decided — next section.

## The details (2026-11-14)

- **R3-10 — the pages: everything a regular user sees** — Home, the directory (the list, the map, the filters and a
  space's page), About (and the privacy page), the sign-in pages (sign in, register, forgot, reset, the forced
  change), and the signed-in user's own pages (the account, favourites) — with the 404. Not the owner's, reception's
  or the admin's dashboard. Plus the design system those pages are built from.
- **R3-11 — the skills and plugins (settled 2026-11-14):** install three plugins from the Anthropic directory —
  **Website Design** (UXKIN: a direction drawn from real websites, written as a DESIGN.md, then built and reviewed),
  **UI Design Review** (UXKIN: a senior designer's review of the rendered screens, compared with real products) and
  **Design** (Anthropic: critique, design-system, UX copy); use the installed **frontend-design** and the Vectorlab
  skills that serve the aim (`anti-slop`, `typography`, `spacing`, `surfaces`, `page-patterns`, `viewports`,
  `motion`). **Not** `brand-guidelines` (Anthropic's brand), and no plugin that hooks every prompt (e.g. Critique).
  **The UXKIN MCP server is allowed** (the owner: an outside service is fine) — the design worker's launch loads it.
- **R3-12 — the bar (the owner's words):** "a design I look at and am shocked by its quality and by the difference."
- **R3-13 — the output of this round:** a written diagnosis (what exactly makes the site read as AI-made, with
  captures) and **two or three distinct design directions as real, interactive HTML mock-ups** of the key pages, for
  the owner to look at and choose — as the space profile's mock-up was. No production code in this round; the
  prototype and production follow the owner's choice, by their own prompts.
- **R3-14 — what stays fixed:** the identity's colours and the logo (ink + berry, ADR 0019, §16), Arabic first and
  RTL, the v1 scope (no feature on *Not in v1*; no fake data — no ratings, no seat counts). **Open to change:** the
  division of every page, the type (scale and, as a proposal, the typeface), spacing, grid, surfaces, imagery,
  iconography, components' look, motion. Earlier settled design decisions may be overturned by a direction — each
  says which and why.
- **R3-15 — the cost:** one lead (Opus 5.5 xhigh) and up to three sub-agents, one per direction (the supervisor's
  earlier lean recommendation was one sub-agent; raised for R3-12's bar, said to the owner).
- **R3-16 — effort high, not xhigh (the owner, 2026-11-14):** the lead runs at **Opus 5.5, effort high** (R3-15's
  xhigh replaced; this week's quota). Its sub-agents run at the lead's effort. The three plugins of R3-11 offered to
  the owner for install on 2026-11-14 (an install card); **installed — confirmed enabled by ListPlugins on 2026-11-14**
  (Website Design, UI Design Review, Design; frontend-design and Canva already on). A session started before the
  install does not see them: the lead's fresh session does.
- **R3-17 — no UXKIN (the owner, 2026-11-14):** UXKIN's MCP service turned out to be paid ($9.99 a month or $99
  once); the round runs **without it** — the plugins' skills only; references from real products' public pages and the
  lead's knowledge. If the diagnosis's comparisons prove thin, the owner may subscribe for one month then.

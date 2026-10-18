# Plan — README: Masaha's public face on GitHub

**Worker:** the readme worker · worktree `C:\Users\basel\masaha-readme`, detached at `origin/main` (`1333e66`), clean · branch: `docs/readme` · prompt: `C:\Users\basel\.prompt\MASAHA_README\PROMPT\README_PROMPT.md`

## 1. Summary

Rebuild the three-line root `README.md` into a product-facing GitHub page (15 ordered sections, English with Arabic under the explanatory parts), illustrated by ~16–19 curated WebP screens plus one short GIF — half captured from this worktree's running app (ports 3322/5322), half from an edited **scratchpad copy** of the design prototypes (real OpenStreetMap tiles swapped in for the map) — all fed one fictional-but-realistic Gaza-flavoured dataset created through the API as the admin. Add one sentence to `CLAUDE.md`'s "Claim only what is true" rule, and prepare (not apply) repository metadata.

## 2. Contract

**Scope**

- `README.md` — full rebuild per the prompt's 15 sections.
- `docs/assets/readme/` — the image set (≤ ~19 files incl. the GIF), WebP ≤ 300 KB each, alt text on every image.
- `CLAUDE.md` — exactly one sentence added to the "Claim only what is true" bullet.
- Prepared (not committed, not applied): one-line repo description, ~8 topics, a 1280×640 social-preview image → `C:\Users\basel\Downloads\readme-assets\`.
- 2 commits, one PR (`docs: rebuild the README as the project's face`, labels `docs` + `area:docs`, assigned to owner), report → `C:\Users\basel\.prompt\MASAHA_README\REPORT\README_REPORT.md`.

**Acceptance criteria**

- All 15 sections present in the given order; Arabic only under intro, problem/idea, and the three audience descriptions, each in `<div dir="rtl" lang="ar">`.
- Nothing from *Not in v1*; live status written as a **state, never a seat count** (ADR 0008); reception staff present in the dashboard story; "near me" stated as device-location-never-sent-to-Masaha.
- Zero mentions of university / supervisor / defence / graduation project anywhere in the diff (text, alt text, metadata) — verified by search before push.
- Every relative link and image path resolves on GitHub, both themes; `format:check` clean; all images ≤ 300 KB (hero target ≤ 250 KB), GIF ≤ 3 MB, image files ≤ ~19, PR files < 25.
- Map shot shows real OSM tiles of the Gaza Strip with **"© OpenStreetMap contributors"** visible; one honest gallery line: *"Screens from Masaha's product design and its running build."*
- `CLAUDE.md` gains only the one sentence; no other file of workers A/B touched; no server on 3320/3321/5320/5321; ports 3322/5322 free after the run.

**Out of scope**

- Applying repo metadata (owner's job); any code, tests, schema, dependency, CI, or capability-document change; editing the design archive (`docs/design/`) — it stays frozen; any *Not in v1* feature; issue #53's other university mentions (`CLAUDE.md` mission paragraph, plan, ADR 0014); folding any finding.

## 3. Reading done

CLAUDE.md · `workflow.md` (all; §2 Phases, §4, §9 in detail) · `docs/README.md` map + deferred-documents (via briefing) · findings index (all open titles) · `overview.md` (v1 + Not in v1 verbatim) · `glossary.md` · `design/README.md`, `SCREENS.md`, `prototype/BRIEF.md` + prototype inventory · `foundation.md` §1–§2, §13 (and §4–§8 for honest token facts) · `system-overview.md` · ADRs 0001, 0008, 0011, 0012 · `setup.md` Commands · `testing.md` lanes · `documentation.md` (rules incl. §8 link integrity) · `.github/workflows/ci.yml` checks (via briefing). `docs/features/` (5 documents: auth, lookups, spaces, users, space-links) will be read for each fact cited; other capabilities have no document yet, so those facts cite overview/ADRs/platform docs.

## 4. Settled decisions, as they will be built

- **Identity:** © 2026 Basel Ghoneim, all rights reserved; no licence file; contact `baselghonaim@gmail.com`, LinkedIn `basel-ghonaim`, GitHub profile; no university anywhere.
- **Language:** English throughout; Arabic under intro, problem/idea, and each audience blurb only, `<div dir="rtl" lang="ar">`; technical sections English only.
- **Build-state exception:** written into `CLAUDE.md`'s "Claim only what is true" bullet as one sentence: *"The root `README.md` presents Masaha as designed (its v1 scope) rather than its build state, and never states that a feature is built."* The README itself carries no build labels or roadmap dates.
- **Sections 1–15** exactly as the prompt orders them (header with «Masaha · مساحة», one value line, CI badge live from GitHub + Node 24 + TypeScript badges, rights line; intro; hero; problem/idea; three audiences; screens; bilingual/accessibility; stack w/ ADR 0001 link; Mermaid diagram w/ `system-overview.md` link; engineering quality; ~5 commands w/ `setup.md` link; five-line tree; documentation; author/contact; rights).
- **Images:** running-app shots = sign-in, dashboard shell, admin lookups (amenities), admin spaces list (filters, menu, dialog, toast), captured headless at 1440×900 / 390×844, no chrome, fixed zoom; prototype shots = home, directory list, map (Leaflet + OSM in the scratchpad copy only, Gaza Strip bounds, pins on seeded areas, attribution visible), space page, owner overview, front desk; one honest static line under the gallery; `<picture>` dark variants for GitHub dark mode; one GIF (language flip → direction flips → then theme); extras in `<details>`; every image alt-texted.
- **One dataset, both sources:** ~6 fictional spaces (coined Gaza-flavoured names — Manara, Wasl, Siraj, Rukn, Maidan, Darb — never a real business), areas from seeded lookups, ILS prices, hours, amenities, `example.com` e-mails; created **through the API as the admin** (owner accounts created + linked so some spaces are verified and can show live status); the same names patched into the scratchpad prototype's `data.js`. No real person's data, no secrets in any shot.
- **Ports/tooling:** API 3322, web 5322 (`.env` already set, never printed/committed); prototype copy served from scratchpad on a free port (e.g. 5330); Chrome headless + a small dependency-free Node CDP driver (Node 24 built-in WebSocket) in the scratchpad for interactions and the GIF screencast; image conversion/GIF assembly in a scratchpad Python venv with Pillow; nothing installed into the repository.
- **Subagent cap:** 2 — both already spent on research; implementation is done directly.

## 5. Stronger decisions

1. **Live-status phrasing stated affirmatively** — every mention says "available, full or closed now — never a seat count", not just "live status". *Why:* the current README's "live available seats" is exactly the ADR 0008 error. *Cost:* two extra words per mention. *Recommendation: adopted.*
2. **README as pointer, not copy** — where a fact has an owner document (scope, glossary, setup, ADRs), the README links instead of restating lists in full. *Why:* documentation §1 "one home per fact"; keeps the page short and trustworthy. *Cost:* slightly less self-contained. *Recommendation: adopted.*
3. **Weight stricter than the cap** — target ≤ 250 KB hero, ≤ 150 KB typical, GIF ≤ 3 MB, whole README ≈ ≤ 5 MB. *Why:* §6 risk, weak connections. *Cost:* WebP quality tuned down a notch. *Recommendation: adopted.*
4. **Identity grep over the whole diff including filenames, alt text, and the prepared metadata** before push. *Why:* one mention fails the item. *Cost:* one command. *Recommendation: adopted.*
5. **Payment wording** — dashboard bullets say "record payments by hand (cash or transfer)". *Why:* "payments" alone could read as online payment (*Not in v1*). *Cost:* three words. *Recommendation: adopted.*
6. **Badges: three, no more** — CI (GitHub Actions badge, live), Node 24, TypeScript. *Why:* honest, fewest external requests. *Cost:* shields.io is an external image host. *Recommendation: accepted.*
7. **Screens captions reuse `SCREENS.md`'s canonical screen names.** *Why:* caption vocabulary has one home. *Cost:* none. *Recommendation: adopted.*

No prompt or document rule is weakened by this plan; the `CLAUDE.md` sentence is the one deliberate, owner-gated exception and it narrows only the build-state clause.

## 6. Related findings

Read the open index; none is folded (prompt §5) and none blocks this item. Closest neighbours, recorded not touched: **#37** (links checked by hand — this item performs that manual check), **#45** (data-table library in the first download — the quality section must not claim it passes; `check:build` is described only as the check that keeps dashboard code out of the first download), **#35** (no document title — irrelevant). If a genuine new divergence appears it is written as a finding numbered from **60** (only if unavoidable, since the file scope is README/assets/one CLAUDE.md sentence).

## 7. Files

- **This item's files:** `README.md` (rewrite) · `docs/assets/readme/*` (new, ~16–19 images) · `CLAUDE.md` (one sentence added to the "Claim only what is true" bullet only).
- **Other layers' files:** none — no file of workers A or B edited; nothing on 3320/3321/5320/5321; only this worktree's `.env`-driven servers on 3322/5322.
- **Shared files:** `CLAUDE.md` is repo-wide; this item owns only that one sentence (issue #53 owns the rest).
- **Scratchpad (never committed):** prototype copy with the Leaflet/OSM swap and patched `data.js`, CDP driver, capture frames, Pillow venv, composite-canvas page.
- **Downloads (never committed):** `C:\Users\basel\Downloads\readme-assets\` — social preview 1280×640 + the metadata text.

## 8. Lanes, tests, and what they catch

No code, so no test lanes are added. The manual equivalents this item runs:

| Check | Command / action | The break it catches |
|---|---|---|
| Format | `npm run format:check` | style drift in README/CLAUDE.md |
| Link integrity | manual per documentation §8: every relative link + anchor resolved on the pushed branch | dead paths/anchors |
| Rendered review | GitHub page, light + dark, desktop + phone width | broken `<picture>`/Mermaid/RTL layout |
| Identity search | case-insensitive search of the full diff for university/supervisor/graduation/الجامعة | identity failure |
| Image weight | script asserting ≤ 300 KB each / GIF ≤ 3 MB / ≤ ~19 files | page too heavy |
| Attribution | visual check of the map shot | missing OSM attribution |
| Port hygiene | confirm 3322 and 5322 free after the run | leaked servers |

## 9. Review Focus (no planned check exercises these)

- Arabic rendering quality of the `<div dir="rtl" lang="ar">` blocks on GitHub.
- Truth of each prose claim vs `overview.md`/ADRs (spot-read twice: drafting, then review).
- Whether the Mermaid diagram renders acceptably at GitHub's width and in dark mode.
- Whether the hero composite reads as one product at phone width.
- Badge URLs actually resolving (CI badge path vs `.github/workflows/ci.yml`).
- GIF legibility and its ≤ 3 MB weight after GitHub's processing.

## 10. Commits

1. `docs(readme): add the product screenshots` — `docs/assets/readme/` only.
2. `docs: rebuild the README as the project's face` — `README.md` + `CLAUDE.md`.

Staged by path, `git status` before each; no tool attribution; PR titled `docs: rebuild the README as the project's face`, labels `docs` + `area:docs` (create `area:docs` with `gh label create` if absent), `--assignee @me`.

## 11. Verification (phase 4)

**Runs:** `npm run format:check`; the manual link check; the real run itself (API 3322 + web 5322 + prototype copy) to capture the shots — sign-in, admin navigation, state/dialog/toast frames — then all servers stopped with 3322/5322 (and the prototype port) confirmed free; the image-weight script; the identity grep; after push, the rendered-page review in both themes at desktop and phone width.

**Does not run:** lint, typecheck, build, `check:build`, `check:classes`, and all four test lanes — **why:** no code, no dependencies, no CI or build-check change; workflow §4's documents-only exception applies (format + links by hand only).

## 12. Decisions needed from the owner

1. **The `CLAUDE.md` sentence** (approved): *"The root `README.md` presents Masaha as designed (its v1 scope) rather than its build state, and never states that a feature is built."*
2. **The image list** (~16–19 files, section 4) — exact screens under the ~20-file cap, `<picture>` dark variants on hero + home.
3. **The fictional space names** (Manara, Wasl, Siraj, Rukn, Maidan, Darb) — coined, Gaza-flavoured, no real business.

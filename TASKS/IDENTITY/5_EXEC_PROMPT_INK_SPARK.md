# IDENTITY — "ink + spark" trial in the PROTOTYPE (short plan, then build, then stop uncommitted)

You are a **Claude Code worker** on **Masaha** (a bilingual Arabic RTL / English directory and dashboard for coworking
spaces in Gaza), in **`C:\dev\masaha\app-identity`** (a worktree of its own, branch `design/ink-spark`). You try a new
colour identity **in the design prototype only**. You write a short plan, build at once (no approval stop), and
**stop uncommitted** so the owner and the main supervisor look at it in the browser. **Model Opus 5.5, effort high.**

## 0. Read first

1. `CLAUDE.md`, `docs/design/README.md` (the prototype's rules, its two checks, how to serve it),
   `docs/frontend/design-system/foundation.md` §4–§5 (the two ramps, the semantic roles and their verified pairs).
2. **The plan, whole:** `C:\dev\masaha\workspace\TASKS\IDENTITY\4_PLAN_INK_ACCENT.md` (the "ink + spark" idea, the
   remap table, the candidates, the criteria). The owner approved trying it.
3. The palette lab, for its engine (OKLCH ramps from a seed, the contrast pairs): in the worktree `C:\dev\masaha\app-b`,
   `docs/design/prototype/masaha/palette-lab.js` (read only; never edit `app-b`). The measured search the supervisor
   used: `C:\Users\basel\AppData\Local\Temp\claude\cf371fb19a552a62\45b389ce-6711-41bd-83ee-ed291fcde2cf\scratchpad\palette_search.mjs`
   and `score_lab.mjs` (if gone, rebuild the same measures: OKLab distance and a protan/deutan simulation, Machado
   2009).

## 1. Plan (≤ 50 lines), then build without waiting

Write `C:\dev\masaha\workspace\TASKS\IDENTITY\5_PLAN_INK_SPARK.md`: where the semantic tokens are defined and which
pages load what; how the new stylesheet `docs/design/prototype/masaha/identity-ink-spark.css` is loaded last on every
page and how `?identity=<id>` (kept across links, default = today's identity) switches the candidate; every place that
must show the spark (sidebar current item, selected states, the selected map pin, the sortable lift, `tone-primary`,
the brand mark) and every place that must **not** (action buttons, small text, destructive); the candidates with their
measured numbers; **Proposed alternatives** if you think a rule is weaker than another way. **Do not wait** — build.

## 2. Build

- **Candidates (3):** slate-blue ink + coral spark (the Sea sunset seed `#C2492F`), slate ink + berry spark (`#A149A0`,
  hue 328), warm charcoal ink + coral spark. Tune within each family until **every** criterion passes; a candidate that
  cannot pass is dropped and named in the report with its numbers.
- **Criteria (measured, written into the plan and the report):** foundation §5's pairs at AA in both themes (text
  4.5:1; control borders, focus ring, icons, large text 3:1); ink primary vs the destructive red: OKLab ΔE ≥ 0.10 and,
  under protan and deutan simulation, ΔE ≥ 0.08; the spark ≥ 3:1 on every ground it sits on, never small text, never an
  action button; destructive stays a true red (not pink) in dark; success / warning / info unchanged.
- **Only `docs/design/`.** Do not edit the vendored `_ds/*/_ds_bundle.css` / `.js`. The prototype's traps: one global
  scope per page (no new top-level name another script has, none the browser owns), no object rest, only classes the
  prebuilt CSS has (layout or colour rules go in the new stylesheet, with a comment), every text in both languages.
- Record the trial in `docs/design/CHANGES.md` («Identity trial — ink + spark (2026-11-11)», marked a trial, not
  adopted) and a line in `docs/design/INDEX.md` for `?identity=`.

## 3. Look, check, stop

- Serve: `cd docs/design/prototype` then `python -m http.server 5402`. For each candidate: Home, Directory (cards,
  filters, map with a selected pin), Space details, Desk (a check-in, the «إلغاء الدفعة» dialog), Owner overview,
  Owner space profile, Admin spaces — at **390 and 1440**, **Arabic and English**, **light and dark**: no leftover
  brand colour where ink or spark belongs, no console error, focus rings visible. Screenshots (curated) to
  `C:\Users\basel\Downloads\identity-shots\` — never into the repository. If the Chrome extension is unavailable, use
  headless Chrome over CDP.
- Both checks pass: `node docs/design/scripts/check-parse.mjs`, `node docs/design/scripts/check-classes.mjs`.
- **Stop, nothing committed:** print the branch, `git status -s`, `git diff --stat`, the checks' output, the serve
  command, ready URLs per candidate (`?identity=…&theme=dark&lang=en`), and a table of every candidate's measured
  numbers. Write the same to `C:\dev\masaha\workspace\TASKS\IDENTITY\6_REPORT_INK_SPARK.md`. The owner's notes come in
  this session; commit (one commit, by path, Conventional, no tool attribution), push or PR **only on his word**.

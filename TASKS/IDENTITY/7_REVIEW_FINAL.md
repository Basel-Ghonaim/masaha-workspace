# IDENTITY — the final, comprehensive review of the ink + spark trial (berry first, 2026-11-11)

**Scope:** the whole trial, before the owner decides to commit it — **part A** fixes what is already known (light
mode, hover), **part B** reviews everything else. Berry (`slate-berry`) is the adopted identity and comes first;
coral stays in the prototype and gets the same rules so a later comparison is fair.

## For a fresh session (read first)

You are a **Claude Code worker** on **Masaha** (a bilingual Arabic RTL / English directory and dashboard for coworking
spaces in Gaza), starting with an empty context. You continue a **colour-identity trial in the design prototype
only**, built by an earlier session and **not committed**.

- **Where:** the worktree **`C:\c\dev\masaha\app-identity`** (that exact path; `C:\dev\masaha\app-identity` does not
  exist), branch `design/ink-spark`. Run `git status -s` first: ~50 changed files under `docs/design/` plus new
  `docs/design/prototype/masaha/identity-ink-spark.css` and `docs/design/prototype/masaha/logo/` — that is the
  trial; **keep it, build on it, never reset, stash or checkout anything.**
- **Read first:** `CLAUDE.md`, `docs/design/README.md` (the prototype's rules: one global scope per page, no object
  rest, only classes already in the prebuilt bundle — layout and colour rules go in `identity-ink-spark.css`),
  `C:\dev\masaha\workspace\TASKS\IDENTITY\4_PLAN_INK_ACCENT.md` (the "ink + spark" idea), and
  `C:\dev\masaha\workspace\TASKS\IDENTITY\6_REPORT_INK_SPARK.md` (what the trial built, its measures, its rounds).
- **How the trial works:** `?identity=slate-berry` or `?identity=slate-coral` on any prototype page (carried on links
  by `masaha/i18n.js`) sets `<html data-identity>`; every trial rule lives in `identity-ink-spark.css` under
  `html[data-identity…]`; without the parameter the page is today's identity, untouched — keep it so.
- **Serve:** a server may already run on port 5402 (`python -m http.server 5402` from `docs/design/prototype`);
  if not, start it. **Memory is short on this machine** (~1 GB free at times): take screenshots in small batches,
  one browser at a time; stop what you start (by PID) at the end.
- **Checks:** `node docs/design/scripts/check-parse.mjs` and `node docs/design/scripts/check-classes.mjs` must pass.
- **Limits:** only `docs/design/`; **no commit, no push, no PR** (the owner decides); no file outside the worktree
  except your report and screenshots. Write your results as a new section «Round 4 — the final review» in
  `6_REPORT_INK_SPARK.md`, then print a short summary with ready URLs and stop.

## The task

The owner adopted **`slate-berry`** officially (I4); coral stays in the prototype for later comparison. Before
committing the trial, one round on **light mode**, above all **hover**: the owner sees almost no difference between a
hovered item and its surface.

## Measured (supervisor, WCAG contrast of the fill against its surface)

| Fill (light) | on card `#FFFFFF` | on background `#F7FBFF` |
|---|---|---|
| hover = `--muted` = neutral-100 `#ECF4FC` (buttons' outline/ghost, menu items, sidebar items) | **1.11** | **1.07** |
| neutral-200 `#DDE5ED` | 1.27 | 1.22 |
| selected tint = spark-50 `#FEF3FE` | 1.08 | **1.04** |
| spark-100 `#FFE3FD` | 1.19 | 1.14 |

Today's Sea has the same weakness (neutral-100 on white 1.11) — it predates the trial. A hover fill needs no WCAG
ratio, but under ≈ 1.15 it is invisible on many screens and in sunlight; the target is **≈ 1.2–1.3**.

## Part A — fix light mode and hover (berry first; the same rule for coral)

1. **Hover in light:** give hover its own value instead of `--muted`: about neutral-200 at 60–100 % (measure; land
   between 1.18 and 1.30 on both card and background). Buttons (outline, ghost, secondary), menu items, sidebar
   items, table rows, list rows, tabs, the segmented control, chips. The text on it keeps AA (4.5:1).
2. **Selected (spark tint) in light:** spark-100 instead of spark-50 where the tint marks "you are here"; keep the 3 px
   spark bar on the current sidebar item. Hover and selected must also differ **from each other**.
3. **Dark mode:** check the same pairs; change only what is below ≈ 1.2.
4. **Light-mode pass** of the rest while there: borders and dividers visible (`--border` on card), the input's border
   ≥ 3:1, disabled states readable, cards distinguishable from the page background, focus rings visible on every
   surface.
5. **Report:** a before/after table of every pair, screenshots of hover states (Desk table row, sidebar item, outline
   button, menu item, directory filter chip) light at 1440, berry and coral, to
   `Downloads\identity-shots\hover-*`. Both prototype checks pass. **Then go straight on to part B** (no stop).

## Part B — the comprehensive review (after part A; fix what is clearly a defect, list what needs the owner)

Go through **every page the trial touches** (the 38 app pages; at least: Home, Directory with a map pin selected,
Space details, Sign in / Register / Forgot / Reset, Favorites, My payments, Desk with a check-in and the «إلغاء
الدفعة» dialog, Customers, Customer file, Payments, Packages, Owner overview, Owner space profile with a Sheet open,
Announcements, Staff, Settings, Admin overview, Admin spaces, Admin users, Admin space edit), berry first, at **390,
768 and 1440**, **Arabic and English**, **light and dark**. For each, answer:

1. **Colour roles:** ink on every action, spark only where the plan allows (current item, selection, chips, the
   selected pin, the lifted item, the logo's dots, drawn covers) — never on an action button or small text; no
   leftover teal; status colours (success, warning, destructive, info) untouched and never confused with the spark.
2. **Contrast:** every text pair ≥ 4.5:1 (large text, icons, borders, focus rings ≥ 3:1), in both themes — a table of
   every pair you measured, failing ones first.
3. **States:** hover, focus-visible, active/pressed, selected, disabled, loading — each visible and distinct from the
   others, on every surface (background, card, muted, sidebar, dialog/Sheet).
4. **The logo:** right file per identity and theme (header, auth pages, admin sidebar expanded and collapsed rail,
   phone drawer, favicon); its size and clear space; never cropped, stretched or on a busy ground; the accessible
   name in both languages.
5. **Layout and RTL:** nothing overflowing, nothing clipped, mirrored where it should be (arrows, the sidebar bar on
   the inline start), the logo never mirrored.
6. **Today's identity untouched:** the same pages without `?identity=` look exactly as on `main` (spot-check five).
7. **The code:** `identity-ink-spark.css` — every rule scoped under `html[data-identity…]`, no duplicate or dead
   rule, comments say why; no new class outside the bundle; `CHANGES.md` / `INDEX.md` true to the pages.

**Report** (Round 4 in `6_REPORT_INK_SPARK.md`): part A's before/after table; part B as one line per check —
**passed / fixed (what) / for the owner (why)**; the defects you fixed; anything you left with its reason; screenshots
curated to `Downloads\identity-shots\final-*` (berry first, coral only where it differs). Both prototype checks pass.
Uncommitted. Stop.

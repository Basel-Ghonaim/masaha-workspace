> **Note 2026-10-14 (the analyst):** all six design batches are merged into `main` (`34a6c59`). Known on `main`: a stray `<<<<<<< HEAD` line before `INDEX.md` § 54, a leftover of a merge, already recorded — do not report it.

# R2-SH-VD — Round 2 review: The shared layer · Visual design and consistency

## 1. Who you are

You are an independent design reviewer running inside OpenCode. You work alone, read-only, with no
context but this prompt. You do not review anything outside this prompt's scope and axis. You do
not edit, commit, check out, install, or move files. You judge shared visual consistency only
(section 5).

## 2. Where

- Read from `C:\dev\masaha\design` (a git worktree, detached at `origin/main`).
- First: `git fetch origin`. Then check `git rev-parse HEAD` equals `git rev-parse origin/main`. If
  it does not, stop and say so in the report's last section. Write both SHAs at the top of the
  report.
- Never edit, commit, check out, install, or move anything in that directory.

## 3. How to open the prototype

- Serve it on your own port **5437** (no other review uses it), so all forty reviews can run at once:
  `python -m http.server 5437 --bind 127.0.0.1 --directory docs/design/prototype`
  run with `C:\dev\masaha\design` as the working directory.
- Open pages as `http://127.0.0.1:5437/<Prototype URL>` with the parameters exactly as listed.
- You open other parts' pages **read-only for pattern comparison only**: report pattern-level
  issues here; page-level issues belong to the parts, not to you.
- At the end: stop the server by its PID and check the port is free (`5437` answers nothing).
- Evidence captures: save each issue's cropped capture as `<ID>.png` (e.g. `R2-SH-VD-001.png`) in
  `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\SH-VD\` (create it if missing).

## 4. Scope: SH — the shared layer (VD angle)

**This part owns no pages.** It owns the recurrences listed in the sibling SH scope.

**INDEX sections (read `docs/design/INDEX.md` at run time — it is authoritative; the list below is
the entry point, not a copy):** 11, 12, 41, 50, 51, 52 — the variant sections are your primary
evidence: every page in AR/EN × light/dark × desktop/phone. For pattern evidence, open the same
representative pages as the sibling SH scope, each with `?lang=en`, `?theme=dark`, and both.

**Roles:** all five — consistency must hold for every shell.

**Widths and modes:** all three widths **390, 768, 1440**; Arabic and English; light and dark —
the variant sections exist for exactly this comparison. Narrow only with a stated reason.

## 5. Your axis: VD — visual design and consistency (of the shared patterns)

Judge the shared layer through this axis only, deeply:

1. Hierarchy, layout and grid held across shells: sidebar groups with `sr-only` labels on the 768
   rail (P3), the switcher's mark trigger (SH-006), top-bar minimum height, the 61 px phone bar.
2. Spacing on the scale (foundation §5) across shells, menus, sheets, filter bars, pagination.
3. Type styles (foundation §7) used the same way for the same job in site and dashboard shells.
4. Colour by semantic role and token (never raw): both themes complete resolutions of the same keys
   — compare every §50–§52 dark frame against its light twin; menu items in the menu's own colour
   (SH-020 as settled); state colours identical wherever a state shows.
5. The same job done the same way on every page: page headers (P1), filter bar + sheet + count
   (P5), pagination (P6), states (P7), toasts (P8), confirm/undo (P9), account menu (P4), language
   and theme placement (SH-005) — name the pattern and every page where it differs.

**Out of this prompt's axis (leave to the other SH prompts and the parts, do not report):** flow
opinions (UX — R2-SH-UX); anything broken, overflowing, mis-mirrored, or console errors (DF —
R2-SH-DF); removals (parts); wording and translation (CP — R2-SH-CP); focus, names, contrast,
touch targets, screen-reader order (AX — R2-SH-AX); API/model/v1 truth (parts). Page-level issues
belong to the parts — report pattern-level only. A flaw *in* a component (a Button's look, a
Field's states) is reported with **level: design system** (lens §2 — fixed in code, not in the
prototype).

## 6. What is settled — do not report again

- Read `C:\dev\masaha\workspace\DESIGN\DECISIONS\REVIEW_LENS.md` §2b first, then
  `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_SHARED.md` in full (P1–P10 with all Amended
  notes, SH-005/006/016/018/020).
- What these settle is **not reported again**. Report only misapplications and pages where a
  settled pattern does not fit, with why.
- If you believe a settled decision makes the product worse, report it under **Decisions in doubt**
  with why — never as a defect.

## 7. The lens

Follow `REVIEW_LENS.md` §3 (especially A.1–A.4 and B.4), §4 (proposals from the design system's own
components and tokens — foundation §12 is the inventory; a proposal needing a new component says so
and why; cost S/M/L; **pattern-level proposals name every page they change**) and the report shape
in section 8 below. Known limits of the archive (lens §2) are not reported. Visual rules:
`docs/frontend/design-system/foundation.md`.

## 8. The report

Save it to `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-SH-VD_REPORT.md`. English, concise.
In this order:

1. The commit SHAs from section 2.
2. A one-line verdict.
3. The five most important points, one line each.
4. The issues, most important first, one block each: **ID** (`R2-SH-VD-001`…), title,
   **type** (defect | improvement), **level** (design system | pattern | component | page),
   **impact** (high | medium | low, for the user), **where** (frame label from INDEX.md, prototype
   URL with parameters on your local server, width and mode, screenshot path in
   `docs/design/screens/`), **evidence** (the capture's path), what is wrong / what could be better,
   **proposal**, **why** it is better, **cost** (S/M/L),
   **rule** (the document and section it applies or puts in doubt, if any).
5. Decisions in doubt (if any).
6. What was not reviewed and why.

## 9. Cap

At most 25 issues, the most important first. No praise. One issue per problem.

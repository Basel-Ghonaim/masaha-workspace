# WI-B — the berry on the main action (ADR 0022)

You are a **Claude Code worker** on **Masaha**, a bilingual Arabic RTL / English platform for coworking spaces in Gaza.
This is a fresh session, **Opus 5.5, effort high**, started in **`C:\dev\masaha\app`** (on `main` = `c3968a74` or later, clean;
the API on 3320 against `masaha_dev`, tests on `masaha_test`, the web on 5320). `main` is **live in production**:
every merge deploys.

**Another worker runs beside you:** WI-C2 in `C:\dev\masaha\app-design`, branch `feat/sign-in-in-place`, expected
**#157**: the sign-in form inside the overlay (`pages/site/public/SignInPrompt*`, `pages/site/auth/**`,
`features/auth/**`, `shared/routing/guest/**`, its documents `docs/frontend/architecture.md`, `docs/features/auth.md`,
`favorites.md`, `data-reports.md`, the copy catalogue's auth and site files). Its plan:
`C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\WI-C2\2_PLAN.md`. **The no-conflict rule:** you may plan now, but you
edit none of the files C2's PR touches until it has merged; if your work needs one, say so in the plan and that part
waits.

## Two phases

1. **Now: read and plan only.** Save the plan to `C:\dev\masaha\workspace\TASKS\BERRY_PRIMARY\6_PLAN.md`, say in the
   conversation that it is saved, and **stop**. Do not wait inside plan mode: the approval comes later as a message
   in this same session. Edit nothing in the repository in this phase.
2. **After the owner's approval:** `git fetch`, cut `feat/berry-main-action` from the latest `origin/main`, and execute
   to the end without stopping: local verification, the Chrome pass, the PR, green CI and `CLEAN`, then
   `7_REPORT.md` beside the plan. **Never merge.**

Follow the project's skills `start-work-item`, `write-plan`, `open-pr` and `final-report` (with the two phases above
in place of their stop-and-wait).

## Read first — binding

- **ADR 0022** (`docs/architecture/decisions/0022-the-berry-on-the-main-action.md`) and ADR 0019 with its new
  *Revised* line;
- `C:\dev\masaha\workspace\TASKS\BERRY_PRIMARY\0_OWNER_DECISIONS.md` and **A18** in
  `C:\dev\masaha\workspace\DESIGN\AUTH\0_OWNER_DECISIONS.md`;
- `docs/frontend/design-system/foundation.md` §4–§5 (palette, semantic roles, the contrast and distance criteria),
  §12 (`Button` and every component that draws `primary`);
- the layer's tokens (`tokens/primitives.css`, `semantic.css`, `semantic.unit.test.ts`, `themes.ts`) and `Button`;
- the approved pictures where the berry action is seen: masaha-prototype (public,
  `https://github.com/Basel-Ghonaim/masaha-prototype`) `prototype/variants/Space details/inplace.css` (`.inplace-primary`:
  `spark-600` + white in light; its dark values are superseded by B1 below) and the captures in
  `C:\dev\masaha\workspace\DESIGN\AUTH\inplace-P2\`; the real screens before / after in
  `C:\Users\basel\Downloads\berry-trial-shots\` (an injected stylesheet, not code).

## The work (the plan settles the details)

1. **A role of its own for the main action**, apart from `primary` (the ink), which keeps links, checked and active
   controls (Checkbox, RadioGroup, Switch, Tabs' active pill), Meter, Heatmap, Toast and the rest it draws today —
   ADR 0022 point 2. Its foreground, its hover, its focus ring if it differs. Name it in the plan.
   **The owner's decision B1 (2026-11-25, `0_OWNER_DECISIONS.md`): the berry in the light theme only.**
   - **Light:** `spark-600` with white text, hover `spark-700`.
   - **Dark:** the main action keeps **today's** `primary` look — `neutral-50` with `neutral-950` text and today's
     `primary-hover` — so the dark theme's buttons do not change at all.
   - The supervisor measured these with the test file's own method before the decision (text 5.91 : 1, shape
     5.69 : 1; distance from `destructive` 0.163 / protan 0.161 / deutan 0.160, hover 0.174 / 0.131 / 0.172); your
     tests make them permanent.
   - **ADR 0022 gains this dated line, word for word, under its status line, as its own commit** (`docs(adr): keep
     dark main action in the ink`, with a body):
     `> **Revised:** <the commit's date> — the berry main action is the light theme's; in the dark theme the main action keeps the ink's light step with dark text, as before (the owner, after seeing both on the real screens). The body below is left as first written.`
2. **`Button`'s main variant takes it.** Decide in the plan, from a full inventory, whether the main variant *is*
   today's default (`primary`) — so every default button becomes berry — or a new variant callers opt into. ADR 0022
   point 1 says **one main action per screen**: list every screen where today's default buttons number more than one,
   and propose which one is the main action and what the others become (outline, secondary, ghost), screen by
   screen, for the owner to approve. Destructive stays red.
3. **The dashboard is quieter** (point 5): the berry marks its selected item (today's spark) and its main action only.
4. **The measured criteria become tests** (point 6): the main action's steps on their grounds (text ≥ 4.5 : 1, the
   shape ≥ 3 : 1 on the page and card), and their distance from `destructive`, with and without simulated protanopia
   and deuteranopia, in both themes — in the same test file and with the same method as 0019's criteria.
5. **Not here:** brand surfaces with the berry-to-plum scale (designed with the owner page by page later), the logo,
   the icons, the e-mails; anything in C2's files before C2 merges.
6. **Documents:** foundation §4–§5 (the role, its values, its criteria) and §12 (`Button`); the showcase; claim only
   what is built.

## Hard limits

- Web and docs only: no API code, schema, migration, new dependency or database write. No secret printed.
- Touch only what this Work Item needs. Stage by path, never `git add -A` / `git add .`. No drive-by refactoring.
- The design system is one layer in one place; semantic tokens only; logical classes; no colour outside the layer.
- Never weaken a test. No production code only a test uses.
- Commits: Conventional, **subject ≤ 50 characters, with a body**; no tool attribution; no `fixup!` left. `#PRNUM` in
  documents, replaced just before the push (expect **#158**, or the next free number: check the PR and Issue lists,
  since C2 may open #157 first).
- Never push to `main`, never merge, never force-push a branch that is not yours.
- Heavy commands through the grant script: `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs b <command…>`
  — C2 runs beside you, so expect to wait for its slot. A run killed for memory: retry once, then CI judges, and say
  so. If the memory guard stops your servers, restart them once at ≥ 4 GB free; if that fails, skip the Chrome pass
  and say so.
- **Ports 3320 / 5320 only** (3323 / 5323 are C2's). Stop your servers by PID and check the ports are free.

## Verification (phase 2)

- On the head: `format:check`, `lint`, `typecheck`, `check:classes`, `check:links`, `check:conflicts`, `test:unit`,
  `test:component`, a production build (`NODE_ENV=production`), then `check:build`. `test:api` is left to CI.
- **Chrome** (the browser pane shown before any layout or axe check): the home, a space page, the directory, the
  sign-in page, one owner screen and one admin screen, at 390 and 1440, Arabic and English, light and dark; the main
  action's colour and hover, the focus ring on it, every other control unchanged; axe on each. Shots to
  `C:\Users\basel\Downloads\berry-shots\`, curated, never in the repository — **a before / after pair for each screen**
  so the owner sees the change.
- Push, open the PR with `open-pr`, wait for `gh pr checks` green on the pushed head and `CLEAN`, then `7_REPORT.md`
  with `final-report`.

## Proposed alternatives

If a decision here or in ADR 0022 is wrong in practice, say so in the plan's "Proposed alternatives" with the reason.
Build nothing alternative before the owner's answer.
